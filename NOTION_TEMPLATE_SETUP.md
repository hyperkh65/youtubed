# 📝 Notion Database Template Setup Guide

## 🎯 목표
6개 Database를 가장 빠르게 설정하는 방법 (5분 완료)

---

## 🚀 방법 1: 자동 생성 템플릿 사용 (추천)

### Step 1: 템플릿 페이지 복제

Notion에서 우리가 제공하는 템플릿을 복제합니다:

```
https://www.notion.so/YouTube-Keyword-Analyzer-Template-[TEMPLATE_ID]
```

**복제 방법:**
1. 링크 접속
2. 우측 상단의 "Duplicate" 클릭
3. 자신의 Workspace 선택
4. "Duplicate" 확인

### Step 2: Database ID 확인

각 Database를 열고 URL에서 ID를 복사합니다:

```
https://www.notion.so/{DATABASE_ID}?v={VIEW_ID}
                        ↑
                    여기를 복사
```

**6개 Database 목록:**
```
1️⃣  Keyword Analysis
2️⃣  Trend Data
3️⃣  Recommendations
4️⃣  Competitor Analysis
5️⃣  Search Intent Analysis
6️⃣  Performance Prediction
```

### Step 3: 자동 설정 스크립트 실행

```bash
python setup_notion_db.py \
  --token "ntn_T84053591181vVGMJGrESxdEGryJX6sO9EZIeeQ4OzS2YJ" \
  --db-ids '{
    "keyword_analysis": "db1_id_here",
    "trend_data": "db2_id_here",
    "recommendations": "db3_id_here",
    "competitor_analysis": "db4_id_here",
    "search_intent": "db5_id_here",
    "performance_prediction": "db6_id_here"
  }' \
  --add-samples
```

### Step 4: 완료!

✅ 모든 Database가 자동으로 설정됩니다.

---

## 🔧 방법 2: 수동 생성

Notion에서 각 Database를 직접 만드는 방법입니다.

### Database 1: Keyword Analysis 🔍

**생성 방법:**
1. Notion 워크스페이스 열기
2. "New" → "Database" → "Table"
3. 이름: "Keyword Analysis"
4. 다음 속성 추가:

| 속성명 | 타입 | 옵션 |
|--------|------|------|
| Keyword | Title | (기본값) |
| Google Volume | Number | |
| Naver Volume | Number | |
| Daum Volume | Number | |
| YouTube Volume | Number | |
| Avg Volume | Formula | `(prop("Google Volume") + prop("Naver Volume") + prop("Daum Volume") + prop("YouTube Volume")) / 4` |
| Difficulty Score | Number | 0 ~ 100 |
| Google CPC | Number | |
| Naver CPC | Number | |
| Opportunity Score | Number | |
| Google Trend | Select | rising, stable, declining |
| Naver Trend | Select | rising, stable, declining |
| Search Intent | Select | informational, navigational, commercial, transactional |
| Related Keywords | Multi-select | (자유롭게) |
| Tags | Multi-select | (자유롭게) |
| Status | Select | active, inactive, archived |
| Notes | Text | |

### Database 2: Trend Data 📊

| 속성명 | 타입 |
|--------|------|
| Date | Date |
| Keyword | Relation → Keyword Analysis |
| Search Volume | Number |
| Interest Level | Number (0-100) |
| Trend Direction | Select: up, down, stable |
| Portal | Select: Google, Naver, Daum, YouTube |
| Peak Day | Checkbox |
| Notes | Text |

### Database 3: Recommendations 💡

| 속성명 | 타입 |
|--------|------|
| Recommendation | Title |
| Base Keyword | Relation → Keyword Analysis |
| Score | Number (0-100) |
| Type | Select: related, trending, niche, low_competition |
| Estimated Volume | Number |
| Difficulty | Number (0-100) |
| Trend | Select: rising, stable, declining |
| Conversion Potential | Number (0-1) |
| Reason | Text |
| Status | Select: recommended, used, discarded |
| Priority | Number (1-5) |

### Database 4: Competitor Analysis ⚔️

| 속성명 | 타입 |
|--------|------|
| Analysis Name | Title |
| Competitor Name | Text |
| Our Channel Name | Text |
| Our Keywords | Multi-select |
| Competitor Keywords | Multi-select |
| Overlap Keywords | Multi-select |
| Our Unique | Multi-select |
| Competitor Unique | Multi-select |
| Total Opportunities | Number |
| Recommendations | Text |
| Analysis Date | Date |
| Next Review | Date |

### Database 5: Search Intent Analysis 🔍

| 속성명 | 타입 |
|--------|------|
| Keyword | Relation → Keyword Analysis |
| Primary Intent | Select: informational, navigational, commercial, transactional |
| Intent Confidence | Number (0-100) |
| Informational Score | Number |
| Navigational Score | Number |
| Commercial Score | Number |
| Transactional Score | Number |
| Content Type Recommendation | Multi-select: tutorial, guide, comparison, review |
| Target Audience | Text |
| Suggested Format | Select: article, video, course, comparison |
| Analysis Date | Date |
| Notes | Text |

### Database 6: Performance Prediction 📈

| 속성명 | 타입 |
|--------|------|
| Keyword | Relation → Keyword Analysis |
| Current Volume | Number |
| Predicted 1M Volume | Number |
| Predicted 2M Volume | Number |
| Predicted 3M Volume | Number |
| Predicted Trend | Select: increasing, stable, decreasing |
| Growth Rate | Number |
| Confidence Level | Select: high, medium, low |
| Confidence Score | Number (0-100) |
| Peak Season | Multi-select: 월(January~December) |
| Low Season | Multi-select: 월 |
| Seasonality Strength | Number (0-1) |
| Best Posting Day | Select: 요일 |
| Best Posting Month | Select: 월 |
| Posting Frequency | Select: Daily, Weekly, BiWeekly |
| ROI Estimate | Number |
| Created Date | Date |
| Next Update | Date |

---

## ⚡ 방법 3: 대화형 설정

가장 간단한 방법:

```bash
python setup_notion_db.py --token "ntn_YOUR_TOKEN"
```

**진행 과정:**
1. 각 Database ID를 입력하라고 요청
2. 자동 검증
3. 샘플 데이터 추가 여부 확인
4. 완료!

---

## 🔗 Database 간 Relation 설정

**Relation이란:** 2개 이상의 Database를 연결하는 것

### 설정 방법:

1. **Trend Data에서:**
   - "Keyword" 속성 선택
   - Type: "Relation"
   - Select "Keyword Analysis" Database

2. **Recommendations에서:**
   - "Base Keyword" 속성
   - Type: "Relation"
   - Select "Keyword Analysis" Database

3. **Search Intent Analysis에서:**
   - "Keyword" 속성
   - Type: "Relation"
   - Select "Keyword Analysis" Database

4. **Performance Prediction에서:**
   - "Keyword" 속성
   - Type: "Relation"
   - Select "Keyword Analysis" Database

---

## 📊 Database ID 확인 및 저장

### 각 Database의 ID 복사:

**URL 형식:**
```
https://www.notion.so/{32자-DATABASE-ID}?v={32자-VIEW-ID}
```

**복사 방법:**
1. 각 Database 열기
2. 브라우저 주소창에서 DATABASE ID 복사
3. `-` (하이픈) 포함해서 복사 (자동으로 처리됨)

### 환경 변수에 저장:

`.env.local` 파일 생성:

```env
NOTION_API_TOKEN=ntn_T84053591181vVGMJGrESxdEGryJX6sO9EZIeeQ4OzS2YJ

NOTION_DB_KEYWORD_ANALYSIS=2ff1f4ff9a0e80c0b53ae305e66fecd8
NOTION_DB_TREND_DATA=abc123def456ghi789jkl012mno345pqr
NOTION_DB_RECOMMENDATIONS=xyz789abc012def345ghi678jkl901mno
NOTION_DB_COMPETITOR=pqr456stu789vwx012yza345bcd678efg
NOTION_DB_INTENT=hij123klm456nop789qrs012tuv345wxy
NOTION_DB_PREDICTION=efg678hij901klm234nop567qrs890tuv
```

---

## ✅ 설정 검증

설정이 완료되면 검증합니다:

```bash
python setup_notion_db.py \
  --token "ntn_T84053591181vVGMJGrESxdEGryJX6sO9EZIeeQ4OzS2YJ" \
  --db-ids '{
    "keyword_analysis": "2ff1f4ff9a0e80c0b53ae305e66fecd8",
    ...
  }' \
  --verify-only
```

**예상 출력:**
```
✅ keyword_analysis: Keyword Analysis
✅ trend_data: Trend Data
✅ recommendations: Recommendations
✅ competitor_analysis: Competitor Analysis
✅ search_intent: Search Intent Analysis
✅ performance_prediction: Performance Prediction

✅ All databases verified successfully!
```

---

## 📝 샘플 데이터 추가

각 Database에 샘플 데이터를 추가:

```bash
python setup_notion_db.py \
  --token "ntn_T84053591181vVGMJGrESxdEGryJX6sO9EZIeeQ4OzS2YJ" \
  --db-ids '{"keyword_analysis": "...", ...}' \
  --add-samples
```

**추가되는 샘플:**
- Keyword Analysis: "Python Tutorial", "Machine Learning", "Data Analysis"
- Recommendations: "best python tutorial", "python for beginners"
- (기타는 API를 통해 자동 추가)

---

## 🎓 팁과 트릭

### 1️⃣ 빠른 Database ID 복사

**Chrome Extension 사용:**
- Notion Web Clipper 설치
- 각 Database 열기 후 "Copy Database ID" 클릭

### 2️⃣ Bulk 데이터 임포트

CSV 파일에서 데이터 임포트:

1. Database 열기
2. "Import" 클릭
3. CSV 파일 선택
4. 컬럼 매핑
5. 임포트

### 3️⃣ API Rate Limiting

Notion API는 분당 약 3개의 요청만 허용합니다.
대량 작업 시 스크립트가 자동으로 대기합니다.

### 4️⃣ Database Views 추천

각 Database에 유용한 View를 만들어보세요:

- **Keyword Analysis:**
  - "High Opportunity" (기회점수 > 50)
  - "Rising Trends" (트렌드 = rising)
  - "By Status" (상태별 그룹)

- **Recommendations:**
  - "Top Scored" (점수 높은 순)
  - "By Type" (타입별)
  - "Priority Matrix" (우선순위)

---

## 🐛 Troubleshooting

### 문제: "Invalid database ID"

**해결책:**
1. URL에서 정확히 복사했는지 확인
2. `-` (하이픈) 포함되어 있는지 확인
3. 공백이 없는지 확인

### 문제: "Relation 설정 안 됨"

**해결책:**
1. 두 Database가 같은 Workspace에 있는지 확인
2. Database 이름이 정확히 맞는지 확인
3. Notion 페이지 새로고침

### 문제: "API Token 오류"

**해결책:**
1. Token이 유효한지 확인
2. Token 재생성: https://www.notion.so/my-integrations
3. Integration 권한 확인

---

## 📋 완료 체크리스트

- [ ] Notion Workspace 생성
- [ ] 6개 Database 생성 또는 Template 복제
- [ ] 각 Database의 ID 복사
- [ ] `.env.local` 파일 생성
- [ ] `setup_notion_db.py` 실행
- [ ] Database 검증 완료
- [ ] 샘플 데이터 추가 (선택)
- [ ] 백엔드 실행 가능 확인

---

**🎉 완료! 이제 다음 단계로 진행하세요: VERCEL_DEPLOYMENT.md**
