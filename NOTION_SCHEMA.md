# Notion Database Schema 설계

## 📋 전체 Database 구조

Notion에 5개의 관련된 Database를 생성합니다:

---

## 1️⃣ **Keyword Analysis** (포털별 키워드 분석)

| 속성명 | 타입 | 설명 | 예시 |
|--------|------|------|------|
| **Keyword** | Title | 분석한 키워드 | "파이썬 튜토리얼" |
| **Google Volume** | Number | Google 추정 검색량 | 1500 |
| **Naver Volume** | Number | Naver 추정 검색량 | 1200 |
| **Daum Volume** | Number | Daum 추정 검색량 | 900 |
| **YouTube Volume** | Number | YouTube 추정 검색량 | 2000 |
| **Avg Volume** | Formula | 평균 검색량 | `(prop("Google Volume") + prop("Naver Volume") + prop("Daum Volume") + prop("YouTube Volume")) / 4` |
| **Difficulty Score** | Number | 난이도 (0-100) | 45 |
| **Google CPC** | Number | Google CPC 추정 | 1.50 |
| **Naver CPC** | Number | Naver CPC 추정 | 1.20 |
| **Opportunity Score** | Number | 기회 점수 | 33.5 |
| **Google Trend** | Select | Google 트렌드 | rising/stable/declining |
| **Naver Trend** | Select | Naver 트렌드 | rising/stable/declining |
| **Search Intent** | Select | 검색 의도 | informational/navigational/commercial/transactional |
| **Related Keywords** | Multi-select | 관련 키워드 | "best 파이썬", "파이썬 가이드" |
| **Tags** | Multi-select | 태그 | "프로그래밍", "교육" |
| **Status** | Select | 상태 | active/inactive/archived |
| **Created Date** | Created time | 생성 날짜 | 2026-02-06 |
| **Updated Date** | Last edited time | 마지막 수정 | 2026-02-06 |
| **Notes** | Text | 메모/분석 내용 | "높은 기회 점수, 트렌딩 중" |

**Relational Links:**
- Related to: Recommendations, Trend Data, Competitor Analysis, Search Intent

---

## 2️⃣ **Trend Data** (시간대별 트렌드)

| 속성명 | 타입 | 설명 | 예시 |
|--------|------|------|------|
| **Date** | Date | 분석 날짜 | 2026-02-06 |
| **Keyword** | Relation | 연결된 Keyword Analysis | "파이썬 튜토리얼" |
| **Search Volume** | Number | 해당 날짜 검색량 | 1450 |
| **Interest Level** | Number | 관심도 (0-100) | 65 |
| **Trend Direction** | Select | 트렌드 방향 | up/down/stable |
| **Portal** | Select | 포털명 | Google/Naver/Daum/YouTube |
| **Peak Day** | Checkbox | 피크 여부 | true/false |
| **Notes** | Text | 특이사항 | "주말 증가 추세" |
| **Created Date** | Created time | 생성 날짜 | 2026-02-06 |

**목적:** 일별 트렌드 추적으로 월간/계절성 패턴 분석

---

## 3️⃣ **Recommendations** (실시간 추천 키워드)

| 속성명 | 타입 | 설명 | 예시 |
|--------|------|------|------|
| **Recommendation** | Title | 추천 키워드 | "best 파이썬 튜토리얼" |
| **Base Keyword** | Relation | 기반이 된 원본 키워드 | "파이썬 튜토리얼" |
| **Score** | Number | 추천 점수 (0-100) | 85.5 |
| **Type** | Select | 추천 타입 | related/trending/niche/low_competition |
| **Estimated Volume** | Number | 예상 검색량 | 1200 |
| **Difficulty** | Number | 난이도 (0-100) | 35 |
| **Trend** | Select | 트렌드 | rising/stable/declining |
| **Conversion Potential** | Number | 전환율 잠재력 (0-1) | 0.75 |
| **Reason** | Text | 추천 이유 | "높은 검색량과 낮은 경쟁도의 조합" |
| **Status** | Select | 상태 | recommended/used/discarded |
| **Channel Topic** | Text | 채널 주제 (선택) | "프로그래밍" |
| **Created Date** | Created time | 생성 날짜 | 2026-02-06 |
| **Priority** | Number | 우선순위 (1-5) | 4 |

**목적:** 실시간으로 생성된 최적 키워드 추천 저장

---

## 4️⃣ **Competitor Analysis** (경쟁사 분석)

| 속성명 | 타입 | 설명 | 예시 |
|--------|------|------|------|
| **Analysis Name** | Title | 분석명 | "채널A vs 우리 채널" |
| **Competitor Name** | Text | 경쟁사명 | "채널A" |
| **Our Channel Name** | Text | 우리 채널명 | "우리 채널" |
| **Our Keywords** | Multi-select | 우리의 키워드들 | ["파이썬", "머신러닝"] |
| **Competitor Keywords** | Multi-select | 경쟁사 키워드들 | ["파이썬", "데이터분석"] |
| **Overlap Keywords** | Multi-select | 겹치는 키워드 | ["파이썬"] |
| **Our Unique** | Multi-select | 우리만의 키워드 | ["머신러닝"] |
| **Competitor Unique** | Multi-select | 경쟁사만의 키워드 | ["데이터분석"] |
| **Opportunity Keywords** | Relation | 발굴된 기회 키워드 | (Keyword Analysis와 연결) |
| **Total Opportunities** | Number | 발견된 기회 수 | 5 |
| **Largest Gap** | Text | 가장 큰 격차 | "검색량 2배 차이: 데이터분석" |
| **Recommendations** | Text | 전략 추천 | "데이터분석 관련 콘텐츠 우선 제작" |
| **Analysis Date** | Date | 분석 날짜 | 2026-02-06 |
| **Next Review** | Date | 다음 검토 날짜 | 2026-03-06 |

**목적:** 경쟁사와의 키워드 전략 차이 분석

---

## 5️⃣ **Search Intent Analysis** (검색 의도 분석)

| 속성명 | 타입 | 설명 | 예시 |
|--------|------|------|------|
| **Keyword** | Relation | 분석한 키워드 | "파이썬" |
| **Primary Intent** | Select | 주요 의도 | informational/navigational/commercial/transactional |
| **Intent Confidence** | Number | 신뢰도 (0-100) | 85 |
| **Informational Score** | Number | 정보 검색 점수 | 75 |
| **Navigational Score** | Number | 네비게이션 점수 | 20 |
| **Commercial Score** | Number | 상업 점수 | 40 |
| **Transactional Score** | Number | 거래 점수 | 15 |
| **Content Type Recommendation** | Multi-select | 추천 콘텐츠 타입 | tutorial/guide/comparison/review |
| **Target Audience** | Text | 대상 고객층 | "프로그래밍 초급자" |
| **Suggested Format** | Select | 추천 형식 | article/video/course/comparison |
| **Call to Action** | Text | 클릭 유도 문구 | "무료 튜토리얼 보기" |
| **Analysis Date** | Date | 분석 날짜 | 2026-02-06 |
| **Notes** | Text | 추가 노트 | "강한 정보 검색 의도, 교육 콘텐츠 최적" |

**목적:** 키워드의 검색 의도에 맞는 콘텐츠 전략 수립

---

## 6️⃣ **Performance Prediction** (성능 예측)

| 속성명 | 타입 | 설명 | 예시 |
|--------|------|------|------|
| **Keyword** | Relation | 대상 키워드 | "파이썬 튜토리얼" |
| **Current Volume** | Number | 현재 검색량 | 1500 |
| **Predicted 1M Volume** | Number | 1개월 후 예상 검색량 | 1620 |
| **Predicted 2M Volume** | Number | 2개월 후 예상 검색량 | 1750 |
| **Predicted 3M Volume** | Number | 3개월 후 예상 검색량 | 1890 |
| **Predicted Trend** | Select | 예상 트렌드 | increasing/stable/decreasing |
| **Growth Rate** | Number | 성장률 (%) | 26.0 |
| **Confidence Level** | Select | 신뢰도 | high/medium/low |
| **Confidence Score** | Number | 신뢰도 점수 (0-100) | 78 |
| **Peak Season** | Multi-select | 피크 시즌 | November/December |
| **Low Season** | Multi-select | 저점 시즌 | June/July |
| **Seasonality Strength** | Number | 계절성 강도 (0-1) | 0.35 |
| **Best Posting Day** | Select | 최적 발행 요일 | Friday |
| **Best Posting Month** | Select | 최적 발행 월 | November |
| **Posting Frequency** | Select | 발행 주기 | Daily/Weekly/BiWeekly |
| **ROI Estimate** | Number | 예상 ROI (%) | 45 |
| **Created Date** | Date | 분석 날짜 | 2026-02-06 |
| **Next Update** | Date | 다음 업데이트 예정 | 2026-03-06 |

**목적:** 키워드의 미래 성능 예측 및 포스팅 일정 최적화

---

## 📊 Database Relationships

```
Keyword Analysis (메인)
    ├── → Trend Data (1:Many)
    ├── → Recommendations (1:Many)
    ├── → Search Intent Analysis (1:1)
    └── → Performance Prediction (1:1)

Competitor Analysis
    └── → Keyword Analysis (Many:Many)
```

---

## 🔑 주요 특징

### 1. **자동 계산 (Formula)**
- 평균 검색량 = (Google + Naver + Daum + YouTube) / 4
- 기회 점수 = 검색량 / (난이도 + 1)

### 2. **관계 설정 (Relations)**
- Keyword Analysis를 중심으로 모든 테이블 연결
- Competitor Analysis에서 여러 키워드 참조 가능

### 3. **필터 및 정렬**
- Status로 활성/비활성 관리
- Score로 우선순위 정렬
- Date로 시간대별 추적

### 4. **배치 작업**
- 매일 자동으로 Trend Data 추가
- 주간 Performance Prediction 업데이트
- 월간 Competitor Analysis 갱신

---

## 💾 사용 시나리오

### 시나리오 1: 새 키워드 분석
1. Keyword Analysis에 새 키워드 추가
2. 자동으로 Recommendations 생성
3. Search Intent Analysis 자동 완성
4. Performance Prediction 기반 발행 일정 결정

### 시나리오 2: 경쟁 분석
1. Competitor Analysis 생성
2. 경쟁사 키워드 입력
3. 자동으로 Opportunity Keywords 식별
4. 전략 수립

### 시나리오 3: 트렌드 추적
1. 매일 Trend Data 자동 수집
2. 월별/계절성 패턴 분석
3. Performance Prediction 갱신
4. 포스팅 일정 최적화

---

## 🔐 Notion API 권한 필요

- `read`: 모든 Database 읽기
- `update`: 모든 속성 업데이트
- `create`: 새로운 페이지/데이터 생성
- `delete`: 불필요한 데이터 삭제
