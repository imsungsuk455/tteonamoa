#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""빌드 결과 SEO 검증."""
import glob
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
pages = ['dist/index.html', 'dist/about/index.html', 'dist/privacy/index.html',
         'dist/terms/index.html', 'dist/contact/index.html'] \
    + sorted(glob.glob('dist/articles/*/index.html'))
print('pages:', len(pages))
mn = 10 ** 9
CAN = 'rel="canonical"'
INS = '<ins '
LD = 'application/ld+json'
LAZY = 'loading="lazy"'
REL = '함께 보면 좋은 축제'
for p in pages:
    t = open(os.path.join(BASE, p), encoding='utf-8').read()
    assert 'ca-pub-3484572882367046' in t, p
    assert CAN in t, p
    assert INS not in t, p
    if 'articles' in p:
        body = re.sub(r'<script.*?</script>', '', t, flags=re.S)
        ko = len(re.findall(r'[가-힣]', re.sub(r'<[^>]+>', '', body)))
        mn = min(mn, ko)
        assert ko >= 2000, (p, ko)
        assert LD in t, p
        assert REL in t, p
        assert LAZY in t, p
h = open(os.path.join(BASE, 'dist/index.html'), encoding='utf-8').read()
assert 'fetch(' not in h
assert '/articles/gyeongbok-byeolbit-yahaeng/' in h
assert '가을 축제 가이드' in h
print('min article ko:', mn)
print('ALL OK')
