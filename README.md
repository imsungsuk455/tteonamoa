# 떠나모아 (tteonamoa)

주말 축제·행사 일정(B) + 항공·호텔 특가(A) 하이브리드 사이트.

## 구조
- `index.html` — 홈 (특가 + 축제 목록, festivals.json/deals.json 읽기)
- `festivals.json` — 축제 DB (TourAPI 기반, 매일 diff)
- `deals.json` — 특가 DB (status: pending/active/expired)
- `articles/` — 글 3개 (축제 2 + 특가 1)
- `threads_queue.json` — 스레드 발행 큐 (특가는 requires_approval)

## 운영 규칙
- B 축제: 매일 07:00 자동 (TourAPI diff → 상위 5건)
- A 특가: 수집·초안 자동, 발행은 승인 후만
- 특가 만료: expires_at 지나면 expired + 댓글 종료 업데이트
- 제휴: subid에 글 ID, 본문에 "제휴 링크 포함" 표시 필수

## 다음 할 일 (나중)
1. TourAPI 키 발급 → fetch 스크립트 연결
2. 트립닷컴 제휴 가입 → 실링크 교체 (현재 샘플 URL)
3. 도메인 연결 (tteonamoa.org) + Search Console
4. 축제명·날짜 샘플값 실데이터 교체
