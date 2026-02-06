# 🚀 완전한 설정 및 배포 가이드

## 📋 6단계 완벽 자동화 프로세스

이 가이드는 Notion Database 6개를 설정하고 배포하는 **모든 과정을 5분 안에 완료**합니다.

---

## 📌 준비 사항

### 필요한 것들
- ✅ Notion Account
- ✅ Node.js 16+ (`node --version`)
- ✅ Python 3.8+ (`python3 --version`)
- ✅ Git (선택사항)
- ✅ 이 프로젝트 (`youtubed`)

### 가져야 할 정보
- ✅ Notion API Token: `ntn_T84053591181vVGMJGrESxdEGryJX6sO9EZIeeQ4OzS2YJ`
- ✅ Notion Workspace ID (선택사항)

---

## 🎯 단계별 가이드

### 1️⃣ **자동 설정 시작**

가장 간단한 방법 - 자동화 스크립트 사용:

```bash
chmod +x deploy_helper.sh
./deploy_helper.sh
```

**또는 수동으로 각 단계 진행:**

---

### 2️⃣ **Notion에서 Database 생성**

#### 방법 A: Template 복제 (추천 - 2분)

1. Notion 웹사이트 접속
2. "Templates" 클릭
3. "YouTube Keyword Analyzer" 검색
4. "Duplicate" 클릭
5. 자신의 Workspace 선택

✅ 6개 Database가 자동으로 생성됩니다!

#### 방법 B: 수동 생성 (5분)

`NOTION_TEMPLATE_SETUP.md` 참고하여 각 Database 생성

---

### 3️⃣ **Database ID 수집**

각 Database를 열고 URL에서 ID를 복사합니다:

```
https://www.notion.so/{32자-DATABASE-ID}?v={VIEW-ID}
                        ↑
                    여기를 복사
```

**수집할 6개 ID:**

```
1. Keyword Analysis ID:        2ff1f4ff9a0e80c0b53ae305e66fecd8
2. Trend Data ID:               (YOUR_ID_HERE)
3. Recommendations ID:          (YOUR_ID_HERE)
4. Competitor Analysis ID:      (YOUR_ID_HERE)
5. Search Intent ID:            (YOUR_ID_HERE)
6. Performance Prediction ID:   (YOUR_ID_HERE)
```

---

### 4️⃣ **자동 설정 스크립트 실행**

#### 4-1: 기본 설정

```bash
cd youtubed

# 의존성 설치
npm install
pip install -r requirements.txt

# 환경 변수 설정
cat > .env.local << EOF
NOTION_API_TOKEN=ntn_T84053591181vVGMJGrESxdEGryJX6sO9EZIeeQ4OzS2YJ
NOTION_DB_KEYWORD_ANALYSIS=YOUR_DB_ID_1
NOTION_DB_TREND_DATA=YOUR_DB_ID_2
NOTION_DB_RECOMMENDATIONS=YOUR_DB_ID_3
NOTION_DB_COMPETITOR=YOUR_DB_ID_4
NOTION_DB_INTENT=YOUR_DB_ID_5
NOTION_DB_PREDICTION=YOUR_DB_ID_6
EOF
```

#### 4-2: Database 설정 검증

```bash
python3 setup_notion_db.py \
  --token "ntn_T84053591181vVGMJGrESxdEGryJX6sO9EZIeeQ4OzS2YJ" \
  --db-ids '{
    "keyword_analysis": "YOUR_DB_ID_1",
    "trend_data": "YOUR_DB_ID_2",
    "recommendations": "YOUR_DB_ID_3",
    "competitor_analysis": "YOUR_DB_ID_4",
    "search_intent": "YOUR_DB_ID_5",
    "performance_prediction": "YOUR_DB_ID_6"
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

#### 4-3: Database 초기화

```bash
python3 init_databases.py \
  --config .env.local \
  --add-samples
```

**결과:**
- ✅ 각 Database 연결 확인
- ✅ 샘플 데이터 추가 (3개 키워드 + 3개 추천)
- ✅ 프로덕션 환경 준비 완료

#### 4-4: Database 검증

```bash
python3 validate_databases.py \
  --config .env.local \
  --full
```

**테스트 항목:**
- ✅ 각 Database 연결
- ✅ 데이터 추가 작업
- ✅ 쿼리 작업
- ✅ 업데이트 작업

---

### 5️⃣ **로컬 테스트 (5분)**

#### 5-1: FastAPI 백엔드 실행

**터미널 1:**
```bash
python -m uvicorn backend:app --reload --port 8000
```

출력:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

#### 5-2: Next.js 프론트엔드 실행

**터미널 2:**
```bash
npm run dev
```

출력:
```
> youtubed@2.0.0 dev
> next dev

▲ Next.js 14.0.0
- Local:        http://localhost:3000
- Environments: .env.local

✓ Ready in 2.5s
```

#### 5-3: 브라우저에서 테스트

```
http://localhost:3000
```

**테스트 항목:**
- ✅ 5개 탭이 모두 보이는가?
- ✅ 키워드 분석이 작동하는가?
- ✅ 추천 기능이 작동하는가?
- ✅ Notion DB와 연동되는가?

---

### 6️⃣ **Vercel 배포 (5분)**

#### 6-1: Vercel CLI 설치

```bash
npm install -g vercel
```

#### 6-2: 프로젝트 배포

```bash
# Vercel에 프로젝트 배포
vercel

# 또는 이미 연결된 경우
vercel --prod
```

**배포 과정:**
1. GitHub 계정 선택
2. 저장소 선택
3. 환경 변수 추가:
   - `NOTION_API_TOKEN`
   - `NOTION_DB_KEYWORD_ANALYSIS`
   - `NOTION_DB_TREND_DATA`
   - ... (6개 모두)

#### 6-3: 배포 완료

```
🎉 Production: https://youtubed.vercel.app
✅ Deployment complete!
```

---

## 📊 완료 체크리스트

```
초기 준비:
☐ Node.js 설치 확인
☐ Python 설치 확인
☐ Notion API Token 확인

Database 설정:
☐ 6개 Database 생성 또는 복제
☐ Database ID 6개 수집
☐ .env.local 파일 생성

자동 설정:
☐ setup_notion_db.py 실행 (검증)
☐ init_databases.py 실행 (초기화)
☐ validate_databases.py 실행 (검증)

로컬 테스트:
☐ Backend 실행 (포트 8000)
☐ Frontend 실행 (포트 3000)
☐ 브라우저에서 http://localhost:3000 접속
☐ 모든 기능 테스트 완료

배포:
☐ Vercel CLI 설치
☐ GitHub 연결
☐ 환경 변수 설정
☐ 배포 실행
☐ https://youtubed.vercel.app 접속 및 테스트
```

---

## 🆘 Troubleshooting

### 문제: "Database ID invalid"

**해결책:**
1. Notion URL에서 정확히 복사했는지 확인
2. `-` (하이픈) 포함되어 있는지 확인
3. 공백이 없는지 확인

### 문제: "NOTION_API_TOKEN invalid"

**해결책:**
1. Token 유효성 확인
2. Token 재생성: https://www.notion.so/my-integrations
3. .env.local 파일 다시 저장

### 문제: "Backend 포트 8000 이미 사용 중"

**해결책:**
```bash
# 다른 포트 사용
python -m uvicorn backend:app --reload --port 8001
```

### 문제: "Vercel 배포 실패"

**해결책:**
1. `vercel.json` 확인
2. 환경 변수 모두 설정되었는지 확인
3. 로컬에서 동작하는지 재확인

---

## 📈 다음 단계

### 프로덕션 운영
1. ✅ Vercel에 배포됨
2. ✅ Notion DB 연동됨
3. ✅ API 작동 중

### 추가 설정 (선택사항)
1. **커스텀 도메인**: Vercel 대시보드에서 설정
2. **자동 분석 스케줄**: `backend.py`에서 scheduler 추가
3. **사용자 인증**: NextAuth.js 통합
4. **분석 리포트**: 정기적 이메일 발송

---

## 🎓 유용한 명령어

```bash
# 로컬 개발
npm run dev                          # Next.js 시작
python -m uvicorn backend:app --reload  # FastAPI 시작

# Database 관리
python3 setup_notion_db.py --token YOUR_TOKEN
python3 init_databases.py --config .env.local
python3 validate_databases.py --config .env.local

# 배포
vercel                              # 배포 시작
vercel --prod                       # 프로덕션 배포
vercel env add NOTION_API_TOKEN     # 환경 변수 추가

# 빌드
npm run build                       # 프로덕션 빌드
python -m py_compile *.py           # Python 문법 검사
```

---

## 📞 필요한 파일 목록

이 설정에 필요한 모든 파일:

```
✅ backend.py               - FastAPI 백엔드
✅ keyword_analyzer.py      - 분석 엔진
✅ notion_db.py            - Notion API 클라이언트
✅ setup_notion_db.py      - Database 설정 스크립트
✅ init_databases.py       - Database 초기화 스크립트
✅ validate_databases.py   - Database 검증 스크립트
✅ deploy_helper.sh        - 배포 헬퍼 (자동화)
✅ pages/index.tsx         - 메인 페이지
✅ pages/_app.tsx          - Next.js 설정
✅ pages/api/keywords/...  - API Routes
✅ package.json            - Node.js 설정
✅ requirements.txt        - Python 설정
✅ vercel.json             - Vercel 설정
✅ next.config.js          - Next.js 설정
```

---

## ✅ 완료!

🎉 **축하합니다! 모든 설정이 완료되었습니다!**

- ✅ 6개 Notion Database 설정
- ✅ 자동 초기화 및 검증
- ✅ 로컬 환경에서 정상 작동
- ✅ Vercel에 배포 완료
- ✅ 프로덕션 환경 운영 중

---

**이제 YouTube 채널의 키워드 분석을 시작하세요! 🚀**

더 자세한 정보는 다음 문서를 참고하세요:
- `NOTION_TEMPLATE_SETUP.md` - Notion Database 설정 상세 가이드
- `NOTION_SCHEMA.md` - Database 스키마 상세 정보
- `VERCEL_DEPLOYMENT.md` - Vercel 배포 가이드
- `MIGRATION_SUMMARY.md` - Streamlit → Vercel 마이그레이션 요약
