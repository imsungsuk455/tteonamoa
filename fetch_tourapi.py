#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""떠나모아 TourAPI 축제 수집 → festivals.json 갱신 (키 노출 없이 .env에서 로드)."""
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import date, timedelta

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

BASE = os.path.dirname(os.path.abspath(__file__))


def load_key():
    if os.environ.get("TOURAPI_KEY"):
        return os.environ["TOURAPI_KEY"].strip()
    env_path = os.path.join(BASE, ".env")
    if os.path.exists(env_path):
        with open(env_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("TOURAPI_KEY="):
                    return line.split("=", 1)[1].strip()
    return ""


def fetch_festivals(key, start_yyyymmdd, end_yyyymmdd, area_code="", num_rows=100, page_no="1"):
    params = {
        "serviceKey": key,
        "eventStartDate": start_yyyymmdd,
        "eventEndDate": end_yyyymmdd,
        "numOfRows": str(num_rows),
        "pageNo": str(page_no),
        "MobileOS": "ETC",
        "MobileApp": "tteonamoa",
        "_type": "json",
    }
    if area_code:
        params["areaCode"] = area_code
    url = "https://apis.data.go.kr/B551011/KorService2/searchFestival2?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "tteonamoa/1.0"})
    with urllib.request.urlopen(req, timeout=30) as res:
        data = json.loads(res.read().decode("utf-8", "replace"))
    header = data.get("response", {}).get("header", {})
    if header.get("resultCode") != "0000":
        raise RuntimeError(f"TourAPI 오류: {header.get('resultCode')} {header.get('resultMsg')}")
    body = data.get("response", {}).get("body", {})
    items = (body.get("items") or {}).get("item", [])
    if isinstance(items, dict):
        items = [items]
    return body.get("totalCount", len(items)), items


def to_record(it):
    cid = str(it.get("contentid", ""))
    return {
        "id": f"f-{cid}",
        "contentId": cid,
        "title": it.get("title", ""),
        "region": (it.get("addr1", "") or "").split(" ")[0:2] and " ".join((it.get("addr1", "") or "").split(" ")[0:2]),
        "place": it.get("addr1", ""),
        "start": it.get("eventstartdate", ""),
        "end": it.get("eventenddate", ""),
        "fee": "공식 확인",
        "summary": (it.get("title", "") or "") + " 일정·장소 확인",
        "tel": it.get("tel", ""),
        "image": it.get("firstimage", ""),
        "mapx": it.get("mapx", ""),
        "mapy": it.get("mapy", ""),
        "source": "TourAPI",
        "status": "upcoming",
    }


def main():
    key = load_key()
    if not key:
        print("TOURAPI_KEY 없음 (.env 확인)")
        sys.exit(1)
    today = date.today()
    start = today.strftime("%Y%m%d")
    end = (today + timedelta(days=60)).strftime("%Y%m%d")
    args = [a for a in sys.argv[1:] if not a.startswith("--") and not a.startswith("page")]
    page = "1"
    for a in sys.argv[1:]:
        if a.startswith("page"):
            page = a.replace("page", "")
    area = args[0] if args else ""
    save = "--save" in sys.argv
    total, items = fetch_festivals(key, start, end, area, page_no=page)
    print(f"기간: {start}~{end} / 전체: {total} / 조회: {len(items)}")
    for it in items[:10]:
        print(f"- {it.get('title', '')} | {it.get('eventstartdate', '')}~{it.get('eventenddate', '')} | {it.get('addr1', '')}")
    if save and items:
        path = os.path.join(BASE, "festivals.json")
        old = []
        if os.path.exists(path):
            old = json.load(open(path, encoding="utf-8"))
        by_id = {r.get("id"): r for r in old}
        added = 0
        for it in items:
            r = to_record(it)
            if r["id"] not in by_id:
                by_id[r["id"]] = r
                added += 1
        json.dump(list(by_id.values()), open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print(f"저장: {path} (신규 {added}건, 전체 {len(by_id)}건)")


if __name__ == "__main__":
    main()
