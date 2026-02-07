# 🚀 KeyPoint Pro - Vercel 배포 가이드

## 개요
**목표**: KeyPoint Pro를 Vercel에 배포하여 전 세계에서 접근 가능하게 하기

---

## 🔧 배포 전 준비사항

### 1. Vercel 계정 생성
```bash
https://vercel.com/signup
```
- GitHub 계정으로 로그인 추천
- 프리 플랜으로 충분함

### 2. GitHub 저장소 연결
```bash
1. GitHub에서 저장소 생성
2. 로컬 repo를 GitHub로 푸시
3. Vercel 대시보드에서 import

git remote add origin https://github.com/yourusername/keypointpro.git
git push -u origin main
```

### 3. 환경변수 설정

Vercel 프로젝트 → Settings → Environment Variables에서 추가:

```
# NextAuth 설정 (필수)
NEXTAUTH_SECRET=your_secret_here
NEXTAUTH_URL=https://yourdomain.vercel.app

# Google OAuth (선택)
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret

# GitHub OAuth (선택)
GITHUB_ID=your_github_app_id
GITHUB_SECRET=your_github_app_secret

# Stripe (선택)
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

---

## 📋 배포 체크리스트

### 단계 1: 로컬 빌드 테스트
```bash
npm run build
npm run start
```
✅ 에러 없이 빌드되는지 확인

### 단계 2: GitHub 푸시
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

### 단계 3: Vercel 연결 및 배포
```bash
# Option A: Vercel CLI (추천)
npm install -g vercel
vercel

# Option B: Vercel 웹 대시보드
1. https://vercel.com/dashboard 접속
2. "New Project" 클릭
3. GitHub 저장소 선택
4. 환경변수 입력
5. Deploy 클릭
```

### 단계 4: 도메인 설정 (선택)
```bash
Vercel 대시보드 → Settings → Domains
- 커스텀 도메인 추가
- DNS 설정 확인
- HTTPS 자동 설정
```

### 단계 5: 배포 확인
```bash
1. Vercel 대시보드에서 배포 상태 확인
2. Production URL 방문
3. 모든 기능 테스트
```

---

## ✅ 배포 후 체크리스트

### 기능 테스트
- [ ] 로그인 페이지 작동
- [ ] Google OAuth 작동
- [ ] 분석 기능 작동
- [ ] 가격책정 페이지 표시
- [ ] 체크아웃 페이지 작동
- [ ] 성공 페이지 표시

### 성능 확인
- [ ] Lighthouse 점수 확인
- [ ] 로딩 시간 측정
- [ ] 모바일 반응성 확인

### 보안 확인
- [ ] HTTPS 적용
- [ ] 환경변수 보안 확인
- [ ] API 엔드포인트 접근 제어

---

## 🔐 NextAuth 설정 (필수)

### 1. NEXTAUTH_SECRET 생성
```bash
openssl rand -base64 32
```
출력값을 복사하여 `NEXTAUTH_SECRET`에 입력

### 2. NEXTAUTH_URL 설정
```
개발: http://localhost:3000
배포: https://yourdomain.vercel.app
```

### 3. OAuth 제공자 설정

#### Google OAuth
1. https://console.cloud.google.com 접속
2. 프로젝트 생성
3. OAuth 2.0 Client ID 생성
4. Authorized redirect URIs 설정:
   ```
   http://localhost:3000/api/auth/callback/google
   https://yourdomain.vercel.app/api/auth/callback/google
   ```
5. Client ID, Client Secret 복사

#### GitHub OAuth
1. Settings → Developer settings → OAuth Apps
2. New OAuth App 생성
3. Authorization callback URL:
   ```
   http://localhost:3000/api/auth/callback/github
   https://yourdomain.vercel.app/api/auth/callback/github
   ```
4. Client ID, Client Secret 복사

---

## 📊 Vercel 성능 최적화

### 1. 이미지 최적화
```bash
next/image 사용 (이미 적용됨)
```

### 2. 번들 크기 최적화
```bash
npm run analyze
```

### 3. 캐싱 설정
```bash
vercel.json에서 자동 설정됨
```

---

## 🔗 커스텀 도메인 설정

### Vercel에서 도메인 구매
1. Vercel 대시보드 → Domains
2. "Add Domain" 클릭
3. 도메인명 입력
4. $12/년 비용

### 기존 도메인 연결
1. DNS 제공자 (GoDaddy, Namecheap 등)로 접속
2. CNAME 레코드 추가:
   ```
   www CNAME cname.vercel-dns.com
   ```
3. Vercel에서 도메인 추가
4. 검증 대기 (24-48시간)

---

## 📈 모니터링 및 분석

### Vercel Analytics
```bash
Vercel 대시보드 → Analytics
- 페이지 뷰
- 성능 메트릭
- 에러 추적
```

### Google Analytics (선택)
```bash
pages/_document.tsx에 추가:
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_ID"></script>
```

### Sentry (에러 모니터링)
```bash
npm install @sentry/nextjs
```

---

## 🐛 배포 후 문제 해결

### 로그인 안 됨
```
확인사항:
1. NEXTAUTH_URL 올바른지 확인
2. NEXTAUTH_SECRET 설정되었는지 확인
3. Google/GitHub OAuth 콜백 URL 확인
```

### 데이터베이스 연결 안 됨
```
확인사항:
1. DATABASE_URL 환경변수 설정
2. 데이터베이스 방화벽 설정
3. 네트워크 접근 권한 확인
```

### 정적 파일 로드 안 됨
```
확인사항:
1. public 폴더 위치 확인
2. .next 폴더 빌드 확인
```

---

## 📞 배포 후 지원

### Vercel Support
- https://vercel.com/support
- 이메일: support@vercel.com

### 문제 해결
```bash
# 빌드 로그 확인
vercel logs

# 재배포
vercel --prod

# 이전 버전으로 롤백
Vercel 대시보드 → Deployments → 이전 배포 클릭
```

---

## 🎯 배포 후 다음 단계

1. **SEO 최적화**
   - robots.txt 추가
   - sitemap.xml 생성
   - Meta 태그 최적화

2. **마케팅**
   - Google Search Console 등록
   - Product Hunt 출시
   - 소셜 미디어 공유

3. **모니터링**
   - 실시간 분석 대시보드 구축
   - 사용자 피드백 수집
   - 성능 메트릭 추적

4. **확장**
   - 데이터베이스 연동
   - Stripe 실제 결제 연동
   - 이메일 시스템 구축

---

## 💡 배포 팁

### 1. 점진적 롤아웃
```
1. 프리뷰 배포로 테스트
2. 5% 사용자에게 먼저 배포
3. 문제 없으면 100% 배포
```

### 2. 롤백 계획
```
배포 실패 시 이전 버전으로 돌릴 수 있도록 준비
```

### 3. 모니터링
```
배포 후 첫 24시간 집중 모니터링
```

---

## 🚀 성공 배포 신호

✅ 프로덕션 URL 접근 가능
✅ 모든 페이지 로드됨
✅ 로그인/로그아웃 작동
✅ 분석 기능 작동
✅ API 엔드포인트 응답
✅ HTTPS 활성화
✅ 성능 메트릭 정상

---

**준비 완료! 이제 배포하세요! 🎉**
