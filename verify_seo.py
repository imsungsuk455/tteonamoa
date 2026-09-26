#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""빌드 결과 SEO 검증 (발행 게이트 — fire-your-seo-agency 기준)."""
import glob
import json
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
pages = ['dist/index.html', 'dist/about/index.html', 'dist/privacy/index.html',
         'dist/terms/index.html', 'dist/contact/index.html'] \
    + sorted(glob.glob('dist/articles/*/index.html'))
print('pages:', len(pages))
failures = []


def check(cond, msg):
    if not cond:
        failures.append(msg)


mn = 10 ** 9
CAN = 'rel="canonical"'
INS = '<ins '
LD = 'application/ld+json'
LAZY = 'loading="lazy"'
REL = '함께 보면 좋은 축제'
ORG_ID = 'https://tteonamoa.org/#organization'

# 소스 데이터 로드 (관련글·사이트맵·llms 대조용)
articles = json.load(open(os.path.join(BASE, 'src/data/articles.json'), encoding='utf-8'))
slugs = {a['slug'] for a in articles}
sitemap = open(os.path.join(BASE, 'dist/sitemap-0.xml'), encoding='utf-8').read()
llms = open(os.path.join(BASE, 'public/llms.txt'), encoding='utf-8').read()

for p in pages:
    t = open(os.path.join(BASE, p), encoding='utf-8').read()
    check('ca-pub-3484572882367046' in t, f'{p}: AdSense ID 없음')
    check(CAN in t, f'{p}: canonical 없음')
    check(INS not in t, f'{p}: 수동 <ins> 잔존')
    for og in ['og:title', 'og:description', 'og:url', 'og:site_name']:
        check(og in t, f'{p}: {og} 없음')
    m = re.search(r'<title>(.*?)</title>', t, re.S)
    title = m.group(1).strip() if m else ''
    m = re.search(r'name="description" content="(.*?)"', t, re.S)
    desc = m.group(1) if m else ''
    # 길이 게이트는 색인 대상(홈·글)에만 적용 — 소개/법적 페이지는 제외
    if 'articles' in p or p == 'dist/index.html':
        check(15 <= len(title) <= 60, f'{p}: title 길이 범위 밖 ({len(title)}자)')
        check(50 <= len(desc) <= 200, f'{p}: description 길이 범위 밖 ({len(desc)}자)')
    if 'articles' in p:
        body = re.sub(r'<script.*?</script>', '', t, flags=re.S)
        ko = len(re.findall(r'[가-힣]', re.sub(r'<[^>]+>', '', body)))
        mn = min(mn, ko)
        check(ko >= 2000, f'{p}: 한글 {ko}자 (2000 미만)')
        check(LD in t, f'{p}: JSON-LD 없음')
        check(REL in t, f'{p}: 관련글 섹션 없음')
        check(LAZY in t, f'{p}: lazy 로딩 없음')
        check(t.count('<h1') == 1, f'{p}: h1 {t.count("<h1")}개 (1개여야 함)')
        check('datePublished' in t and 'dateModified' in t,
              f'{p}: 발행일/갱신일 LD 없음')
        check(ORG_ID in t, f'{p}: 전역 Organization @id 참조 없음')
        slug = p.replace('\\', '/').split('dist/articles/')[1].split('/')[0]
        check(slug in slugs, f'{p}: articles.json에 없는 slug')
        check(f'/articles/{slug}/' in sitemap, f'{p}: 사이트맵 누락')
        check(f'/articles/{slug}/' in llms, f'{p}: llms.txt 누락')

# 관련글 링크 실존 검사 (related.id는 slug 형식 — 렌더된 href 기준 대조)
for a in articles:
    for r in (a.get('related') or []):
        check(r['id'] in slugs, f"{a['slug']}: 끊긴 관련글 {r['id']}")

# 발행 산출물 존재
for f in ['dist/llms.txt', 'dist/ads.txt', 'dist/404.html']:
    check(os.path.exists(os.path.join(BASE, f)), f'{f} 없음')

h = open(os.path.join(BASE, 'dist/index.html'), encoding='utf-8').read()
check('fetch(' not in h, 'index: fetch() 잔존 (SSR 위반)')
check('/articles/gyeongbok-byeolbit-yahaeng/' in h, 'index: 대표 글 누락')
check('이번 주말,' in h, 'index: 히어로 문구 누락')
check('<img ' in h, 'index: 이미지 없음')
check('date-pill' in h, 'index: date-pill 누락')
check(ORG_ID in h, 'index: Organization LD 없음')
print('min article ko:', mn)
if failures:
    print('FAIL:')
    for f in failures:
        print(' -', f)
    raise SystemExit(1)
print('ALL OK')
