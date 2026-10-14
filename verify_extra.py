#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""빌드 후 부가 검증: Event 스키마·크럼·이메일."""
import glob
import json
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

BASE = os.path.dirname(os.path.abspath(__file__))
checks = {}
warns = []
for p in sorted(glob.glob(os.path.join(BASE, 'dist/articles/*/index.html'))):
    slug = p.replace('\\', '/').split('dist/articles/')[1].split('/')[0]
    t = open(p, encoding='utf-8').read()
    ev = None
    for tag in re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
        d = json.loads(tag)
        if d.get('@type') == 'Event':
            ev = d
    checks[f'{slug} Event schema'] = ev is not None
    if ev:
        off = ev.get('offers') or {}
        checks[f'{slug} offers'] = isinstance(off, dict) and 'url' in off
        checks[f'{slug} offers.priceCurrency'] = off.get('priceCurrency') == 'KRW'
        checks[f'{slug} offers.validFrom'] = bool(off.get('validFrom'))
        checks[f'{slug} performer'] = bool((ev.get('performer') or {}).get('name'))
        checks[f'{slug} organizer.url'] = bool((ev.get('organizer') or {}).get('url'))
        checks[f'{slug} event.url'] = bool(ev.get('url'))
        if 'price' not in off:
            # 요금 미상 — 허위 금액 기입 금지 정책에 따라 생략 허용(경고만, GSC 비치명 경고 가능)
            warns.append(f'{slug}: offers.price 생략 (요금 미상 — 정직 표기 정책)')

t = open(os.path.join(BASE, 'dist/articles/gangneung-coffee-festival/index.html'), encoding='utf-8').read()
checks['crumb'] = 'class="crumb"' in t
for p in ['about', 'contact', 'privacy', 'terms']:
    s = open(os.path.join(BASE, f'dist/{p}/index.html'), encoding='utf-8').read()
    checks[f'{p} email'] = 'imsungsuk455@gmail.com' in s
ok = True
for k, v in checks.items():
    if not v:
        print(k, ': MISS')
    ok = ok and v
for w in warns:
    print('WARN', w)
print('pages checked:', len(glob.glob(os.path.join(BASE, 'dist/articles/*/index.html'))))
print('ALL OK' if ok else 'FAIL')
if not ok:
    raise SystemExit(1)