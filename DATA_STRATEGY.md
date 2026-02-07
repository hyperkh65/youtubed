# 📡 KPP 데이터 통합 전략

## Executive Summary

**목표**: Black Kiwi 수준의 신빙성 + Semrush 수준의 깊이로 실제 데이터 기반 분석 제공

**현실적 접근**:
- ❌ 모든 데이터를 자체 크롤링하기는 불가능
- ✅ 공개 API + 파트너십 + 하이브리드 모델
- ✅ Phase별로 단계적 통합
- ✅ 초기: 공개 데이터 + 시뮬레이션 (신뢰도 높게)
- ✅ 6개월 후: 실제 API 연동

---

## 1️⃣ 포털별 데이터 소스 전략

### 1.1 Google (전 세계)

**Option A: Google Ads API** ✅ 권장
```
✓ 공식 API (Google에서 제공)
✓ 신뢰도 100%
✓ 월 검색량 정확
✗ 비용: $0-$500+/월 (API 호출량 기반)
✗ 설정: 복잡 (OAuth 2.0)

비용 구조:
- 월 1,000,000 요청: $0 (프리 티어)
- 초과: $6 per 1,000 requests
- 우리 추정: 월 500K 요청 → $3,000/월

대응:
1. 초기: 공개 데이터 + 시뮬레이션 (신뢰도 높게)
2. 3개월: 파일럿 (100 고객에만 제공)
3. 6개월: 정식 출시 (API 비용 사용자 분담)
```

**Option B: SEMrush API** (파트너십)
```
✓ 세계 최고 수준 데이터
✓ 이미 정제된 정보
✗ 비용: 높음 (협상 필요)
✗ 라이선스: 재판매 제한 가능

추진:
1. Semrush와 파트너십 협상
2. "화이트라벨" 옵션 협의
3. 수익 공유 모델 (30% ~ 50%)
```

**Option C: 자체 크롤링 + AI 학습** (장기)
```
✓ 완전 독립적
✗ 비용: 높음 (인프라 + 엔지니어)
✗ 시간: 6-12개월
✗ 정확도: 80-90%

우리 접근: 3년 후 고려
```

### 1.2 Naver (한국 최고)

**Option A: Naver Search Advisor API** ✅ 권장
```
✓ 공식 API (네이버 제공)
✓ 한국 데이터 최고 신뢰도
✓ 무료 티어 있음
✗ 문서: 부족 (한글)

비용: 무료 (일일 1,000 요청)

데이터:
- 월간 검색 트렌드
- 검색어 추이
- 관련 검색어
- 검색 인기도

우리 구현:
1. Naver OAuth 통합
2. 사용자 Naver 계정 연동
3. API 요청 (1회 분석 = 5-10 요청)
4. 결과 캐싱 (7일)
```

**Option B: 협력사 데이터 활용**
```
Black Kiwi와 데이터 협력:
- 한국 시장 크롤링 데이터
- 추정 정확도: 85-90%
- 비용: 수익 공유 또는 라이선스

초기 추진:
→ Black Kiwi 접촉 (협력 제안)
→ 상호 이익 모델 구성
```

### 1.3 Daum / Kakao (한국 2위)

**상태: 공개 API 없음**

대응:
```
Option A: 웹 크롤링 (합법적 범위)
├─ 검색결과 수 (경쟁도 지표)
├─ 검색 트렌드 그래프
└─ 관련 검색어

Option B: Kakao API (카테고리 검색)
├─ Kakao 로컬 API 활용
├─ 위치 기반 검색 데이터
└─ 예: "서울 카페" 검색량

우리 방안:
→ 초기: 시뮬레이션 (Google 기반 추정)
→ 6개월: 공개 데이터 활용
→ 1년: 협력사 데이터
```

### 1.4 YouTube (영상 검색)

**Option A: YouTube Data API v3** ✅ 권장
```
✓ 공식 API
✓ 무료 (쿼터: 일일 10,000 단위)
✓ 조회수, 댓글, 좋아요 수 제공

데이터:
- 검색 결과 수 (영상 경쟁도)
- 채널 구독자 수
- 영상 조회수
- 업로드 주기

우리 구현:
1. YouTube API 키 등록 (무료)
2. 상위 영상 10개 분석
3. 평균 조회수 → 월간 검색 추정
4. 상승/정체/하락 트렌드

비용: 무료
정확도: 80% (추정)
```

**Option B: VidIQ / TubeBuddy API**
```
✗ 비용: 높음 ($30-100/월)
✗ 우리 모델과 맞지 않음
→ 장기 고려 (엔터프라이즈 고객용)
```

### 1.5 Amazon (이커머스 - Phase 2)

**Option A: Amazon Product API**
```
✗ 비용: 높음 (해외 서버, 복잡한 인증)
✗ 접근 제한: 엄격

대응:
→ Keepa / JungleScout와 파트너십
→ 기존 데이터 활용
```

**Option B: 웹 크롤링 (합법 범위)**
```
✓ 검색결과 수 (판매량 추정)
✓ 평점 분포
✓ 리뷰 수 (인기도)

우리 방안:
→ 3개월차에 구현
→ 정확도: 70-75%
```

### 1.6 쿠팡 (한국 이커머스 - Phase 2)

**상태: API 없음 (폐쇄적)**

대응:
```
Option A: 공개 데이터
├─ 검색 결과 수
├─ 리뷰 수 (판매량 지표)
└─ 카테고리별 트렌드

Option B: 파트너십
├─ 쿠팡 판매자 API 접근
├─ 매출 데이터 공유
└─ 상호 이익 모델

우리 방안:
→ 초기: 검색결과수 + 리뷰수 활용
→ 6개월: 파트너십 협상
```

---

## 2️⃣ 초기 데이터 모델 (MVP)

### 2.1 신뢰도 높은 "하이브리드" 모델

```
┌─────────────────────────────────────┐
│   사용자가 보는 분석 결과            │
├─────────────────────────────────────┤
│                                      │
│  📊 검색량 (월간)                    │
│  ├─ 공개 API: 50% (Google API)     │
│  ├─ 파트너 데이터: 30% (Black K)   │
│  └─ AI 추정: 20% (머신러닝)        │
│                                      │
│  🎯 난이도 (0-100)                  │
│  ├─ 공개 API: 40%                   │
│  ├─ 경쟁사 데이터: 40%              │
│  └─ 알고리즘: 20%                   │
│                                      │
│  🔄 트렌드 (12개월)                 │
│  ├─ 구글 트렌드 API: 60%            │
│  └─ AI 추정: 40%                    │
│                                      │
└─────────────────────────────────────┘

신뢰도 표시:
🟢 실제 데이터 (80%+): API 직접
🟡 추정 데이터 (70-80%): 파트너/크롤링
🔴 AI 학습 (60-70%): 머신러닝 모델
```

### 2.2 Phase별 데이터 신뢰도

| Phase | Google | Naver | YouTube | 신뢰도 | 설명 |
|-------|--------|-------|---------|--------|------|
| 1 (MVP) | API 30% + 추정 70% | API 100% | API 80% | 75% | 부분 실제 데이터 |
| 2 (Month 3) | API 60% + 추정 40% | API 100% | API 80% | 85% | 대부분 실제 데이터 |
| 3 (Month 6) | API 100% | API 100% | API 100% | 95% | 모두 실제 데이터 |

---

## 3️⃣ 데이터 정확도 보증

### 3.1 신뢰도 스탬프 시스템

```
UI 표시 방식:

🟢 High Confidence (85%+)
   └─ Google API 직접 데이터

🟡 Medium Confidence (70-85%)
   └─ 공개 데이터 + 추정

🔴 Low Confidence (50-70%)
   └─ AI 학습 기반 추정

사용자가 신뢰도를 이해하고
우리 신뢰성을 높일 수 있음
```

### 3.2 "실제 데이터" 보증

```
고객에게 증명:

1️⃣ 공개 API 직접 연동 증명
   └─ API 호출 로그 공개
   └─ 응답 시간 표시 (<2초)

2️⃣ 데이터 소스 명시
   └─ "Google API (공식)"
   └─ "Naver API (공식)"
   └─ "AI 학습 (추정)"

3️⃣ 정확도 벤치마킹
   └─ Black Kiwi와 비교 (Naver)
   └─ Semrush와 비교 (Google)
   └─ 오차율 공개

4️⃣ 정기적 검증
   └─ 월 1회 정확도 리포트
   └─ 사용자 피드백 반영
```

---

## 4️⃣ 기술 구현 (실제 API 연동)

### 4.1 Google Ads API 연동

```typescript
// Google Keyword Planner 데이터 가져오기
import { SearchAdsService } from 'google-ads-api'

async function getGoogleKeywordData(keyword: string) {
  const service = new SearchAdsService({
    customerId: process.env.GOOGLE_CUSTOMER_ID,
    accessToken: userToken  // OAuth 2.0
  })

  const result = await service.generateKeywordIdeas({
    keyword_plan_id: 'plan123',
    keywords: [keyword],
    language: 'ko'  // 한국어
  })

  return {
    avgMonthlySearches: result.avg_monthly_searches,
    searchVolume: result.search_volume,
    competition: result.competition_level,  // LOW, MEDIUM, HIGH
    cpc: result.approximate_cpc_micros
  }
}

// 비용: 월 500K 요청 → $3,000
// 우리 고객 분담: Pro 고객은 +$5/월
```

### 4.2 Naver Search Advisor API 연동

```typescript
// Naver 검색 트렌드 API
import axios from 'axios'

async function getNaverKeywordData(keyword: string, userToken: string) {
  const response = await axios.get(
    `https://openapi.naver.com/v1/search/news.json`,
    {
      params: {
        query: keyword,
        display: 100,
        sort: 'sim'  // 정확도순
      },
      headers: {
        'X-Naver-Client-Id': process.env.NAVER_CLIENT_ID,
        'X-Naver-Client-Secret': process.env.NAVER_CLIENT_SECRET
      }
    }
  )

  return {
    newsCount: response.data.total,  // 뉴스 발행량
    trendingNews: response.data.items.slice(0, 5)
  }
}

// 비용: 무료 (일일 1,000 요청)
// 추적: 사용자가 직접 Naver 계정 연동
```

### 4.3 YouTube Data API 연동

```typescript
// YouTube 검색 데이터
import { google } from 'googleapis'

async function getYoutubeKeywordData(keyword: string) {
  const youtube = google.youtube({
    version: 'v3',
    auth: process.env.YOUTUBE_API_KEY
  })

  const res = await youtube.search.list({
    q: keyword,
    part: 'snippet',
    maxResults: 50,
    type: 'video',
    regionCode: 'KR'
  })

  // 상위 10개 영상 상세 정보 추출
  const videoIds = res.data.items.map(item => item.id.videoId)

  const stats = await youtube.videos.list({
    id: videoIds.join(','),
    part: 'statistics',
    maxResults: 50
  })

  return {
    totalResults: res.data.pageInfo.totalResults,  // 경쟁도
    avgViewCount: stats.data.items.reduce(
      (sum, item) => sum + parseInt(item.statistics.viewCount),
      0
    ) / stats.data.items.length,
    avgLikesRatio: // 인기도 지표
  }
}

// 비용: 무료 (일일 10,000 쿼터)
```

---

## 5️⃣ 초기 출시 전략 (신뢰도 높게)

### 5.1 Month 1-2: Controlled Data Release

```
우리가 할 것:

1️⃣ 공개 데이터 우선 사용
├─ Google 검색결과 수 (경쟁도)
├─ YouTube 비디오 수 (경쟁도)
├─ Naver 뉴스/블로그 발행량
└─ 신뢰도: 명시 (🟡 Medium)

2️⃣ "공개 API 기반" 강조
├─ "Google API 직접 연동"
├─ "Naver 공식 파트너"
├─ "YouTube 데이터 실시간"
└─ 신뢰도 높이기

3️⃣ Beta 고객 募集 (100명)
├─ 무료 접근권
├─ 피드백 수집
├─ 실제 API 테스트

타겟:
→ 개발자 (Product Hunt)
→ SEO 전문가 (블로그 커뮤니티)
→ 이커머스 운영자 (커뮤니티)
```

### 5.2 신뢰도 증명 방법

```
사용자가 신뢰하도록:

1️⃣ "데이터 소스" 명확히
   ✓ Google: Google Ads API (공식)
   ✓ Naver: Naver Search Advisor (공식)
   ✓ YouTube: YouTube Data API (공식)

2️⃣ "실시간 업데이트" 보여주기
   ✓ 마지막 업데이트: 2초 전
   ✓ 다음 업데이트: 6시간 후

3️⃣ "정확도" 공개
   ✓ Google: 95% (API 직접)
   ✓ Naver: 90% (공개 데이터)
   ✓ YouTube: 85% (추정 기반)

4️⃣ "비교" 가능하게
   ✓ Black Kiwi와 Naver 데이터 비교
   ✓ 오차율: ±5-10%
```

---

## 6️⃣ 6개월 이후: 완전 API 통합

### 6.1 Google Ads API 정식 출시

```
Timeline:
Month 1-3: Pilot (100 고객)
Month 4-5: Testing (1,000 고객)
Month 6+: Public (모두)

비용 분담:
- KPP 부담: 월 $3,000 (기본)
- Pro 고객: +$5/월 (월 10회 분석)
- Team 고객: 포함됨
- Enterprise: 커스텀

결과:
→ 검색량 정확도: 95%+
→ CPC 정확도: 90%+
→ 난이도 정확도: 85%+
```

### 6.2 Naver 파트너십 강화

```
협력 대상: Naver, Black Kiwi

가능한 모델:
1️⃣ 데이터 라이선스
   └─ Black Kiwi의 크롤링 데이터
   └─ 월 $2,000-5,000

2️⃣ 수익 공유
   └─ KPP 매출의 5-10%
   └─ 무제한 데이터 접근

3️⃣ 상호 마케팅
   └─ KPP ← Black Kiwi 추천
   └─ Black Kiwi ← KPP 추천
   └─ Win-Win
```

### 6.3 크롤링 인프라 구축

```
우리의 자체 크롤링 (보조용):

기술:
├─ Puppeteer (자동화 브라우저)
├─ BeautifulSoup (HTML 파싱)
└─ 분산 크롤링 (AWS Lambda)

수집 데이터:
├─ 검색결과 수 (경쟁도)
├─ 관련 검색어
├─ 트렌딩 토픽
└─ 광고 수 (경쟁 강도)

비용:
├─ 개발: $20K (2개월)
├─ 인프라: $500-1,000/월
└─ 운영: 1명의 엔지니어

정확도: 80-85% (API 대비)
```

---

## 7️⃣ 마케팅에서 사용할 메시지

### 7.1 "신뢰도" 강조

```
광고 카피:

"Google API 직접 연동"
└─ 정확도 95%+ (공식 출처)

"Naver 공식 파트너"
└─ 한국 데이터 신뢰도 최고

"YouTube 실시간 데이터"
└─ 영상 콘텐츠 전략에 최적

"Black Kiwi와 대비 동급"
└─ 훨씬 저렴한 가격 (85% 할인)
```

### 7.2 증명 방법

```
웹사이트에 표시:

✅ "공개 API 인증 배지"
   ├─ Google Partner Badge
   ├─ YouTube Official Badge
   └─ Naver Developer Badge

✅ "정확도 보증"
   └─ "Google API 기반 95%+ 정확도"
   └─ "업계 유일 한글 최적화"

✅ "고객 후기"
   └─ "Black Kiwi와 비교했는데 수치가 거의 같음"
   └─ "이 가격에 이 기능이면 충분"
```

---

## 8️⃣ 비용 요약

### 초기 (Month 1-3)

| 항목 | 비용 | 설명 |
|------|------|------|
| API 호출 | $0 | 파일럿 기간 (우리 부담) |
| 개발 | $15K | 통합 개발 |
| 인프라 | $2K | AWS/서버 |
| 총계 | $17K | |

### 성장 (Month 4-12)

| 항목 | 월 비용 | 설명 |
|------|--------|------|
| Google API | $3,000 | 월 500K 요청 |
| Naver 라이선스 | $3,000 | 데이터 파트너십 |
| 인프라 | $1,000 | AWS + CDN |
| 크롤링 | $500 | 보조 데이터 |
| 총계 | $7,500 | |

### 매출과의 관계

```
Pro 고객 100명 × $19/월 = $1,900
├─ 데이터 비용: $7,500 / 100 = $75/고객
└─ 손실... ❌

Pro 고객 500명 × $19/월 = $9,500
├─ 데이터 비용: $7,500 / 500 = $15/고객
├─ 마진: $4/고객/월
└─ 연간: $24,000 ✅

Pro 고객 1,000명 × $19/월 = $19,000
├─ 데이터 비용: $7,500 / 1,000 = $7.50/고객
├─ 마진: $11.50/고객/월
└─ 연간: $138,000 ✅ Great!

결론:
→ 500명 이상 유료 고객 필요
→ Year 1 목표: 750명
→ 충분한 마진 확보 가능
```

---

## ✅ 결론

**데이터 신빙성을 위한 전략**:

1. **초기**: 공개 API + 파트너 데이터 (신뢰도 75%)
2. **3개월**: 부분 Google API 통합 (신뢰도 85%)
3. **6개월**: 완전 실제 API (신뢰도 95%)

**마케팅 메시지**:
- "Google API 직접 연동" (신뢰도 강조)
- "Naver 공식 파트너" (한국 최강)
- "Black Kiwi 수준, Semrush 가격" (경쟁력)

**비용 구조**:
- 초기 투자: $17K (Month 1-3)
- 운영 비용: $7.5K/월 (Month 4+)
- Break-even: 500명 유료 고객

**다음 단계**: UI/UX 재설계로 모든 산업군 지원
