#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TourAPI detailImage2로 축제별 추가 이미지 수집 → articles.json 주입."""
import json
import os
import time
import urllib.parse
import urllib.request

BASE = os.path.dirname(os.path.abspath(__file__))


def load_key():
    for line in open(os.path.join(BASE, '.env'), encoding='utf-8'):
        line = line.strip()
        if line.startswith('TOURAPI_KEY='):
            return line.split('=', 1)[1].strip()
    return ''


def images(key, cid):
    params = {'serviceKey': key, 'contentId': cid, 'MobileOS': 'ETC',
              'MobileApp': 'tteonamoa', '_type': 'json', 'imageYN': 'Y',
              'subImageYN': 'Y', 'numOfRows': '10', 'pageNo': '1'}
    url = 'https://apis.data.go.kr/B551011/KorService2/detailImage2?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={'User-Agent': 'tteonamoa/1.0'})
    with urllib.request.urlopen(req, timeout=30) as res:
        data = json.loads(res.read().decode('utf-8', 'replace'))
    items = (data.get('response', {}).get('body', {}).get('items') or {}).get('item', [])
    if isinstance(items, dict):
        items = [items]
    return [it.get('originimgurl', '') for it in items if it.get('originimgurl')]


key = load_key()
festivals = json.load(open(os.path.join(BASE, 'festivals.json'), encoding='utf-8'))
arts = json.load(open(os.path.join(BASE, 'src', 'data', 'articles.json'), encoding='utf-8'))
by_id = {x['id']: x for x in arts}
for x in festivals:
    cid = str(x.get('contentId', ''))
    if not cid:
        continue
    try:
        imgs = images(key, cid)
        x['images'] = imgs
        if imgs:
            print('OK', x.get('title', '')[:14], len(imgs))
        else:
            print('--', x.get('title', '')[:14], '(이미지 없음)')
    except Exception as e:
        print('ERR', cid, str(e)[:80])
    time.sleep(1)

for x in festivals:
    a = by_id.get(x.get('id'))
    if a:
        imgs = x.get('images', [])
        keep = [i for i in imgs if i not in (a.get('image'),)][:3]
        a['gallery'] = keep

json.dump(festivals, open(os.path.join(BASE, 'festivals.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
json.dump(arts, open(os.path.join(BASE, 'src', 'data', 'articles.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print('done')