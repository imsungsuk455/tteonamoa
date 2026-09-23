#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""빌드 후 부가 검증: Event 스키마·크럼·이메일."""
import os

BASE = os.path.dirname(os.path.abspath(__file__))
t = open(os.path.join(BASE, 'dist/articles/gangneung-coffee-festival/index.html'), encoding='utf-8').read()
checks = {
    'Event schema': '"@type":"Event"' in t,
    'crumb': 'class="crumb"' in t,
}
for p in ['about', 'contact', 'privacy', 'terms']:
    s = open(os.path.join(BASE, f'dist/{p}/index.html'), encoding='utf-8').read()
    checks[f'{p} email'] = 'imsungsuk455@gmail.com' in s
ok = True
for k, v in checks.items():
    print(k, ':', 'OK' if v else 'MISS')
    ok = ok and v
print('ALL OK' if ok else 'FAIL')