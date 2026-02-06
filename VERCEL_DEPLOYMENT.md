# 🚀 Vercel 배포 가이드 (Next.js + FastAPI + Notion)

## 📋 목차
1. [프로젝트 구조](#프로젝트-구조)
2. [Notion DB 설정](#notion-db-설정)
3. [로컬 개발 환경](#로컬-개발-환경)
4. [Vercel 배포](#vercel-배포)
5. [환경 변수](#환경-변수)
6. [API 엔드포인트](#api-엔드포인트)

---

## 📁 프로젝트 구조

```
youtubed/
├── pages/
│   ├── _app.tsx              # Next.js 앱 설정
│   ├── index.tsx             # 메인 페이지
│   ├── api/
│   │   └── keywords/
│   │       ├── analyze.ts    # 분석 API
│   │       └── recommendations.ts  # 추천 API
│
├── components/               # React 컴포넌트
│   ├── KeywordAnalysis.tsx
│   ├── TrendAnalysis.tsx
│   ├── AdvancedFeatures.tsx
│   ├── Performance.tsx
│   ├── Settings.tsx
│   ├── Navbar.tsx
│   └── ui/                   # UI 컴포넌트
│
├── styles/
│   └── globals.css           # Tailwind CSS
│
├── backend.py                # FastAPI 백엔드
├── keyword_analyzer.py       # 분석 엔진
├── notion_db.py              # Notion API 통합
│
├── package.json              # Node.js 의존성
├── requirements.txt          # Python 의존성
├── vercel.json               # Vercel 배포 설정
├── next.config.js            # Next.js 설정
├── tsconfig.json             # TypeScript 설정
└── NOTION_SCHEMA.md          # Notion DB 스키마

```

---

## 🔗 Notion DB 설정

### 1️⃣ Notion Workspace에서 Database 생성

각 Database를 다음 속성으로 생성하세요:

#### **Keyword Analysis Database**
```
- Keyword (Title)
- Google Volume (Number)
- Naver Volume (Number)
- Daum Volume (Number)
- YouTube Volume (Number)
- Difficulty Score (Number, 0-100)
- Google CPC (Number)
- Naver CPC (Number)
- Opportunity Score (Number)
- Google Trend (Select: rising/stable/declining)
- Naver Trend (Select: rising/stable/declining)
- Search Intent (Select: informational/navigational/commercial/transactional)
- Related Keywords (Multi-select)
- Tags (Multi-select)
- Status (Select: active/inactive/archived)
- Created Date (Created time)
- Updated Date (Last edited time)
- Notes (Text)
```

#### **Trend Data Database**
```
- Date (Date)
- Keyword (Relation → Keyword Analysis)
- Search Volume (Number)
- Interest Level (Number, 0-100)
- Trend Direction (Select: up/down/stable)
- Portal (Select: Google/Naver/Daum/YouTube)
- Peak Day (Checkbox)
- Notes (Text)
- Created Date (Created time)
```

#### **Recommendations Database**
```
- Recommendation (Title)
- Base Keyword (Relation → Keyword Analysis)
- Score (Number, 0-100)
- Type (Select: related/trending/niche/low_competition)
- Estimated Volume (Number)
- Difficulty (Number, 0-100)
- Trend (Select: rising/stable/declining)
- Conversion Potential (Number, 0-1)
- Reason (Text)
- Status (Select: recommended/used/discarded)
- Priority (Number, 1-5)
- Created Date (Created time)
```

#### **Competitor Analysis Database**
```
- Analysis Name (Title)
- Competitor Name (Text)
- Our Channel Name (Text)
- Our Keywords (Multi-select)
- Competitor Keywords (Multi-select)
- Overlap Keywords (Multi-select)
- Our Unique (Multi-select)
- Competitor Unique (Multi-select)
- Total Opportunities (Number)
- Recommendations (Text)
- Analysis Date (Date)
- Next Review (Date)
```

#### **Search Intent Analysis Database**
```
- Keyword (Relation → Keyword Analysis)
- Primary Intent (Select: informational/navigational/commercial/transactional)
- Intent Confidence (Number, 0-100)
- Informational Score (Number)
- Navigational Score (Number)
- Commercial Score (Number)
- Transactional Score (Number)
- Content Type Recommendation (Multi-select)
- Target Audience (Text)
- Suggested Format (Select: article/video/course/comparison)
- Analysis Date (Date)
- Notes (Text)
```

#### **Performance Prediction Database**
```
- Keyword (Relation → Keyword Analysis)
- Current Volume (Number)
- Predicted 1M Volume (Number)
- Predicted 2M Volume (Number)
- Predicted 3M Volume (Number)
- Predicted Trend (Select: increasing/stable/decreasing)
- Growth Rate (Number)
- Confidence Level (Select: high/medium/low)
- Confidence Score (Number, 0-100)
- Peak Season (Multi-select: months)
- Low Season (Multi-select: months)
- Seasonality Strength (Number, 0-1)
- Best Posting Day (Select: days)
- Best Posting Month (Select: months)
- Posting Frequency (Select: Daily/Weekly/BiWeekly)
- ROI Estimate (Number)
- Created Date (Date)
- Next Update (Date)
```

### 2️⃣ Database ID 얻기

각 Database를 열고 URL에서 Database ID를 복사합니다:

```
https://www.notion.so/{DATABASE_ID}?v={VIEW_ID}
```

---

## 💻 로컬 개발 환경

### 1️⃣ 설치

```bash
# Node.js 의존성
npm install

# Python 의존성
pip install -r requirements.txt
```

### 2️⃣ 환경 변수 설정

`.env.local` 파일 생성:

```env
# Notion API
NOTION_API_TOKEN=ntn_T84053591181vVGMJGrESxdEGryJX6sO9EZIeeQ4OzS2YJ

# Notion Database IDs
NOTION_DB_KEYWORD_ANALYSIS=your_database_id_here
NOTION_DB_TREND_DATA=your_database_id_here
NOTION_DB_RECOMMENDATIONS=your_database_id_here
NOTION_DB_COMPETITOR=your_database_id_here
NOTION_DB_INTENT=your_database_id_here
NOTION_DB_PREDICTION=your_database_id_here

# Backend
BACKEND_URL=http://localhost:8000
```

### 3️⃣ 개발 서버 실행

**터미널 1: FastAPI 백엔드**
```bash
python -m uvicorn backend:app --reload --port 8000
```

**터미널 2: Next.js 프론트엔드**
```bash
npm run dev
```

브라우저에서 `http://localhost:3000` 접속

---

## 🚀 Vercel 배포

### 1️⃣ Vercel CLI 설치

```bash
npm install -g vercel
```

### 2️⃣ 프로젝트 배포

```bash
vercel
```

### 3️⃣ 환경 변수 설정

Vercel 대시보드 → Project Settings → Environment Variables

다음 변수들을 추가:

```
NOTION_API_TOKEN=ntn_T84053591181vVGMJGrESxdEGryJX6sO9EZIeeQ4OzS2YJ
NOTION_DB_KEYWORD_ANALYSIS=your_id
NOTION_DB_TREND_DATA=your_id
NOTION_DB_RECOMMENDATIONS=your_id
NOTION_DB_COMPETITOR=your_id
NOTION_DB_INTENT=your_id
NOTION_DB_PREDICTION=your_id
```

### 4️⃣ Python 런타임 설정

`vercel.json`이 자동으로 구성을 설정합니다.

Python 함수는 자동으로 `/api` 엔드포인트에 배포됩니다.

---

## 🔑 환경 변수

| 변수명 | 설명 | 예시 |
|--------|------|------|
| `NOTION_API_TOKEN` | Notion API 토큰 | `ntn_T84...` |
| `NOTION_DB_KEYWORD_ANALYSIS` | Keyword Analysis DB ID | `2ff1f4ff...` |
| `NOTION_DB_TREND_DATA` | Trend Data DB ID | `abc12345...` |
| `NOTION_DB_RECOMMENDATIONS` | Recommendations DB ID | `def67890...` |
| `NOTION_DB_COMPETITOR` | Competitor Analysis DB ID | `ghi11111...` |
| `NOTION_DB_INTENT` | Search Intent DB ID | `jkl22222...` |
| `NOTION_DB_PREDICTION` | Performance Prediction DB ID | `mno33333...` |

---

## 📡 API 엔드포인트

### 기본 분석

**POST `/api/analyze`**
```json
{
  "keyword": "파이썬 튜토리얼"
}
```

**POST `/api/compare`**
```json
{
  "keywords": ["파이썬", "머신러닝", "데이터분석"],
  "channel_topic": "프로그래밍"
}
```

### 고급 분석

**POST `/api/short-long-analysis`**
```json
{
  "keyword": "파이썬 프로그래밍 튜토리얼"
}
```

**POST `/api/recommendations`**
```json
{
  "keywords": ["파이썬"],
  "channel_topic": "기술교육"
}
```

**POST `/api/competitor-analysis`**
```json
{
  "competitor_keywords": ["파이썬", "데이터분석"],
  "your_keywords": ["파이썬", "머신러닝"]
}
```

**POST `/api/search-intent`**
```json
{
  "keyword": "파이썬 배우기"
}
```

### 트렌드 및 예측

**POST `/api/trend-analysis`**
```json
{
  "keyword": "파이썬",
  "days": 30
}
```

**POST `/api/seasonality`**
```json
{
  "keyword": "크리스마스"
}
```

**POST `/api/prediction`**
```json
{
  "keyword": "파이썬",
  "months": 3
}
```

### 데이터 내보내기

**POST `/api/export`**
```json
{
  "keyword": "파이썬"
}
```

---

## 📊 성능 최적화

### 1️⃣ 이미지 최적화
- Next.js `Image` 컴포넌트 사용
- Vercel이 자동으로 최적화

### 2️⃣ API 캐싱
- Next.js ISR (Incremental Static Regeneration) 사용
- Notion 데이터 캐싱

### 3️⃣ 번들 크기
- Dynamic imports 사용
- Tree shaking 활성화

---

## 🔐 보안

### 1️⃣ CORS 설정
`backend.py`에서 프로덕션 도메인으로 제한:

```python
allow_origins=[
    "https://yourdomain.vercel.app",
    "https://yourdomain.com"
]
```

### 2️⃣ API 레이트 제한
```python
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
```

### 3️⃣ 입력 검증
- Pydantic 모델로 자동 검증
- SQL Injection 방지 (Notion API 사용)

---

## 🐛 troubleshooting

### 문제: Notion API 연결 실패

**해결책:**
1. API Token 확인
2. Database IDs 확인
3. Notion 워크스페이스 권한 확인

### 문제: 프론트엔드에서 API 호출 실패

**해결책:**
1. CORS 설정 확인
2. 백엔드 실행 중 확인
3. 브라우저 콘솔 오류 확인

### 문제: Vercel 배포 실패

**해결책:**
1. `vercel.json` 확인
2. Python 의존성 확인
3. 환경 변수 설정 확인

---

## 📝 배포 체크리스트

- [ ] Notion Workspace 권한 설정
- [ ] 6개 Database 생성 및 ID 복사
- [ ] `.env.local` 파일 생성
- [ ] 로컬에서 테스트
- [ ] GitHub에 푸시
- [ ] Vercel 연결
- [ ] 환경 변수 설정
- [ ] 배포 테스트
- [ ] 프로덕션 도메인 설정
- [ ] CORS 설정 조정

---

## 🎯 다음 단계

1. **모니터링:** Vercel Analytics 설정
2. **백업:** Notion 데이터 정기 백업
3. **스케일링:** 더 많은 사용자 대비
4. **자동화:** 정기적 분석 스케줄링

---

**배포 완료! 🎉**

더 구체적인 사항은 각 파일의 주석을 참조하세요.
