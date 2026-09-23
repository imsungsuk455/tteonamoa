#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TourAPI detailIntro2로 15개 축제 공식 정보 확보."""
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


def intro(key, cid):
    params = {'serviceKey': key, 'contentId': cid, 'contentTypeId': '15',
              'MobileOS': 'ETC', 'MobileApp': 'tteonamoa', '_type': 'json'}
    url = 'https://apis.data.go.kr/B551011/KorService2/detailIntro2?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={'User-Agent': 'tteonamoa/1.0'})
    with urllib.request.urlopen(req, timeout=30) as res:
        data = json.loads(res.read().decode('utf-8', 'replace'))
    items = (data.get('response', {}).get('body', {}).get('items') or {}).get('item', [])
    if isinstance(items, dict):
        items = [items]
    return items[0] if items else {}


KEYS = ['sponsor1', 'sponsor1tel', 'playtime', 'eventplace', 'eventhomepage',
        'agelimit', 'bookingplace', 'placeinfo', 'subevent', 'program',
        'usetimefestival', 'discountinfofestival', 'spendtimefestival']

key = load_key()
fp = os.path.join(BASE, 'festivals.json')
festivals = json.load(open(fp, encoding='utf-8'))
for x in festivals:
    cid = str(x.get('contentId', ''))
    if not cid:
        continue
    try:
        d = intro(key, cid)
        info = {k: (d.get(k, '') or '').strip() for k in KEYS}
        x['official'] = info
        filled = sum(1 for v in info.values() if v)
        print('OK', x.get('title', '')[:16], filled, 'fields')
    except Exception as e:
        print('ERR', cid, str(e)[:80])
    time.sleep(1)
json.dump(festivals, open(fp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('done')
