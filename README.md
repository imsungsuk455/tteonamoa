# 떠나모아 (tteonamoa)

주말 축제·행사 일정(B) + 항공·호텔 특가(A) 하이브리드 사이트. Astro SSG.

## 구조
- `src/pages/index.astro` — 홈 (축제 카드 목록, festivals.json 기반 정적 렌더)
- `src/pages/articles/[slug].astro` — 축제 상세 글 (Article + Event 스키마, 브레드크럼)
- `src/layouts/Base.astro` — 공통 레이아웃 (애드센스 메타, 검증 태그, Airbnb 기반 디자인)
- `festivals.json` — 축제 DB (TourAPI + detailIntro 공식 정보)
- `src/data/articles.json` — 글 본문·메타·related·review
- `fetch_tourapi.py` — TourAPI 수집 (축제 60일 diff)
- `fetch_homepage.py` — detailIntro2 공식 요금·시간·프로그램
- `verify_seo.py`, `verify_extra.py` — 빌드 후 게이트
- `deals.json`, `threads_queue.json` — 특가·스레드 큐 (승인 후 사용)

## 운영 규칙
- 승인 전(현재): 글 15개 유지, 하루 1개 추가 발행, 같은 게이트 통과분만
- 승인 후: 제휴 링크·특가 공개, 매일 자동 발행
- 끝난 행사: 종료 처리 + 목록 정리 (stale 방치 금지)

## 방문 후기 입력 포맷
`src/data/articles.json`의 각 글 `review` 필드가 비어 있으면 렌더 안 됨.
실제 방문 후 아래 형식으로 채우면 모든 글 자동 렌더:
```json
"review": {
  "visited_at": "2026-10-05",
  "weather": "맑음, 18도",
  "crowd": "오후 2시 기준 인파 정도",
  "transport": "주차·대중교통 실제 경험",
  "facilities": "화장실·먹거리·시설 실제 상태",
  "verdict": "총평 한두 문장",
  "tip": "실제로 도움된 꿀팁",
  "photos": ["https://..."]
}
```
**절대 지어내지 않는다** — 허위 경험 콘텐츠는 애드센스 정책 위반(ADS-PUB-05/06)이자 E-E-A-T 사기로, 승인 반려 원인이 됨.

## 다음 할 일 (나중)
1. 도메인 배포 (tteonamoa.org) + Search Console
2. 트립닷컴 제휴 가입 → 실링크 (승인 후)
3. 실제 방문 후기 수집 → review 필드 채우기
4. 하루 1개 글 발행 루틴