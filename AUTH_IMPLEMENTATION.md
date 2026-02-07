# 🔐 KeyPoint Pro 사용자 인증 시스템

## 개요
**목표**: NextAuth.js를 사용한 간단하고 안전한 인증 시스템 구축

---

## 🏗️ 아키텍처

### 1. 인증 제공자 (Auth Providers)

#### Option A: Google OAuth (추천)
```
✅ 장점:
- 사용자가 Gmail로 바로 로그인
- 프로필 정보 자동 수집
- 보안이 높음

코드:
GoogleProvider({
  clientId: process.env.GOOGLE_CLIENT_ID,
  clientSecret: process.env.GOOGLE_CLIENT_SECRET,
})
```

#### Option B: GitHub OAuth
```
✅ 개발자 친화적
- 기술 커뮤니티 접근 용이

코드:
GithubProvider({
  clientId: process.env.GITHUB_ID,
  clientSecret: process.env.GITHUB_SECRET,
})
```

#### Option C: 이메일 인증 (자체)
```
✅ 간단함
- 별도 외부 서비스 불필요
```

**선택**: Google + GitHub (소셜 로그인 추천)

---

## 📊 데이터베이스 스키마

### User 테이블
```typescript
interface User {
  id: string              // UUID
  email: string          // 고유
  name: string           // 사용자명
  image: string          // 프로필 이미지
  createdAt: Date        // 가입일
  emailVerified: boolean // 이메일 검증

  // 구독 정보
  tier: 'free' | 'pro' | 'team'
  stripeCustomerId: string
  subscriptionId: string
  subscriptionStatus: 'active' | 'cancelled' | 'expired'
  subscriptionEndsAt: Date

  // 사용량
  monthlyAnalysisCount: number
  analysisCountResetAt: Date
}
```

### Session 테이블 (NextAuth 자동 생성)
```typescript
interface Session {
  sessionToken: string
  userId: string
  expires: Date
}
```

### Account 테이블 (OAuth 정보, NextAuth 자동 생성)
```typescript
interface Account {
  userId: string
  type: 'oauth'
  provider: 'google' | 'github'
  providerAccountId: string
  access_token: string
  token_type: string
  scope: string
}
```

---

## 🔧 구현 단계

### Step 1: NextAuth.js 설치 및 설정

```bash
npm install next-auth
```

`.env.local`:
```env
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your_random_secret_key

# Google OAuth
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret

# GitHub OAuth (선택)
GITHUB_ID=your_github_id
GITHUB_SECRET=your_github_secret
```

### Step 2: [...nextauth].ts 생성

```typescript
// pages/api/auth/[...nextauth].ts

import NextAuth from "next-auth"
import GoogleProvider from "next-auth/providers/google"
import GithubProvider from "next-auth/providers/github"

export const authOptions = {
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID || "",
      clientSecret: process.env.GOOGLE_CLIENT_SECRET || "",
    }),
    GithubProvider({
      clientId: process.env.GITHUB_ID || "",
      clientSecret: process.env.GITHUB_SECRET || "",
    }),
  ],

  callbacks: {
    async jwt({ token, user, account }) {
      if (user) {
        token.id = user.id
        token.email = user.email
        token.image = user.image
        token.tier = 'free' // 기본값
      }
      return token
    },

    async session({ session, token }) {
      if (session.user) {
        session.user.id = token.id as string
        session.user.tier = token.tier as 'free' | 'pro' | 'team'
      }
      return session
    },
  },

  pages: {
    signIn: '/auth/signin',
    error: '/auth/error',
  },
}

export default NextAuth(authOptions)
```

### Step 3: 로그인 페이지

```typescript
// pages/auth/signin.tsx

import { signIn, useSession } from "next-auth/react"
import { useRouter } from "next/router"
import { useEffect } from "react"

export default function SignIn() {
  const { data: session } = useSession()
  const router = useRouter()

  useEffect(() => {
    if (session) {
      router.push('/')
    }
  }, [session])

  return (
    <div className="min-h-screen bg-black flex items-center justify-center">
      <div className="max-w-md w-full px-4">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold mb-2">KeyPoint Pro</h1>
          <p className="text-slate-400">로그인 후 분석 시작하기</p>
        </div>

        <div className="space-y-4">
          <button
            onClick={() => signIn('google')}
            className="w-full flex items-center justify-center gap-2 bg-white text-black py-3 rounded-lg font-bold hover:bg-slate-100 transition"
          >
            <svg className="w-5 h-5" viewBox="0 0 24 24">
              {/* Google 로고 */}
            </svg>
            Google로 로그인
          </button>

          <button
            onClick={() => signIn('github')}
            className="w-full flex items-center justify-center gap-2 bg-slate-800 text-white py-3 rounded-lg font-bold hover:bg-slate-700 transition"
          >
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
              {/* GitHub 로고 */}
            </svg>
            GitHub로 로그인
          </button>
        </div>

        <div className="text-center text-xs text-slate-500 mt-8">
          로그인하면 이용약관에 동의하는 것입니다
        </div>
      </div>
    </div>
  )
}
```

### Step 4: Navbar 업데이트 (인증 표시)

```typescript
// components/Navbar.tsx (수정)

import { useSession, signOut } from "next-auth/react"
import Link from "next/link"

export default function Navbar() {
  const { data: session } = useSession()

  return (
    <nav className="sticky top-0 bg-gradient-to-r from-slate-950 to-slate-900 border-b border-emerald-500/20 z-50">
      <div className="max-w-7xl mx-auto px-4 flex justify-between items-center h-16">
        <Link href="/" className="flex items-center gap-2 font-bold text-xl text-white hover:text-emerald-400">
          <span className="text-2xl">🔍</span>
          KeyPoint Pro
        </Link>

        <div className="flex gap-8 items-center">
          <Link href="/pricing" className="text-slate-400 hover:text-white text-sm transition">
            가격책정
          </Link>

          {session?.user ? (
            <div className="flex items-center gap-4">
              <span className="text-sm text-slate-400">
                {session.user.name}
                {session.user.tier === 'pro' && (
                  <span className="ml-2 bg-emerald-500/20 text-emerald-400 px-2 py-1 rounded text-xs">Pro</span>
                )}
              </span>
              <img
                src={session.user.image || ''}
                alt={session.user.name || ''}
                className="w-8 h-8 rounded-full"
              />
              <button
                onClick={() => signOut()}
                className="text-slate-400 hover:text-white text-sm transition"
              >
                로그아웃
              </button>
            </div>
          ) : (
            <Link
              href="/auth/signin"
              className="px-4 py-2 rounded-lg bg-emerald-500 hover:bg-emerald-600 text-black font-semibold transition"
            >
              로그인
            </Link>
          )}
        </div>
      </div>
    </nav>
  )
}
```

### Step 5: 보호된 페이지 생성

```typescript
// pages/dashboard.tsx

import { useSession } from "next-auth/react"
import { useRouter } from "next/router"
import { useEffect } from "react"

export default function Dashboard() {
  const { data: session, status } = useSession()
  const router = useRouter()

  useEffect(() => {
    if (status === 'unauthenticated') {
      router.push('/auth/signin')
    }
  }, [status])

  if (status === 'loading') {
    return <div>로딩 중...</div>
  }

  if (!session?.user) {
    return null
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-12">
      <h1 className="text-3xl font-bold mb-8">
        {session.user.name}의 대시보드
      </h1>

      {/* 사용자 정보 */}
      <div className="bg-slate-900/50 border border-slate-700 rounded-lg p-6 mb-8">
        <h2 className="text-xl font-bold mb-4">구독 정보</h2>
        <div className="grid md:grid-cols-3 gap-4">
          <div>
            <p className="text-slate-400 text-sm">현재 플랜</p>
            <p className="text-2xl font-bold text-emerald-400">{session.user.tier.toUpperCase()}</p>
          </div>
          <div>
            <p className="text-slate-400 text-sm">이메일</p>
            <p className="text-lg">{session.user.email}</p>
          </div>
          {session.user.tier === 'free' && (
            <div>
              <p className="text-slate-400 text-sm">업그레이드</p>
              <a href="/pricing" className="text-emerald-400 hover:text-emerald-300">
                Pro 보기 →
              </a>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
```

---

## 🔐 보안 고려사항

### 1. CSRF 방지
```typescript
// NextAuth.js가 자동으로 처리
// NEXTAUTH_SECRET 설정 필수
```

### 2. 이메일 검증
```typescript
// 선택사항: 이메일 검증 메일 발송
async signIn({ email, user }) {
  // 이메일 검증 로직
  return true
}
```

### 3. Rate Limiting (DDoS 방지)
```typescript
// pages/api/auth/[...nextauth].ts에 추가
import { Ratelimit } from "@upstash/ratelimit"

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(10, "1 h"),
})
```

### 4. 세션 보안
```typescript
// .env.local
NEXTAUTH_SECRET=$(openssl rand -base64 32)
```

---

## 🔄 인증 플로우

```
비인증 사용자
    ↓
로그인 페이지
    ↓
Google/GitHub OAuth
    ↓
NextAuth 세션 생성
    ↓
사용자 DB에 저장
    ↓
홈페이지 (로그인 상태)
    ↓
분석 기능 사용
    ↓
월 10회 제한 (Free)
    ↓
Pro 업그레이드 유도
```

---

## 📱 UI 업데이트 (pages/index.tsx)

```typescript
import { useSession, signIn } from "next-auth/react"

export default function Home() {
  const { data: session } = useSession()

  if (!session?.user) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-4xl font-bold mb-6">KeyPoint Pro</h1>
          <p className="text-slate-400 mb-8">
            모든 산업의 키워드 기회를 찾아주는 데이터 분석 플랫폼
          </p>
          <button
            onClick={() => signIn('google')}
            className="px-8 py-4 bg-emerald-500 text-black font-bold rounded-lg hover:bg-emerald-600 transition"
          >
            무료 시작하기
          </button>
        </div>
      </div>
    )
  }

  // 기존 홈페이지 코드...
}
```

---

## 🚀 배포 설정

### Vercel 배포
```env
# 환경변수 설정 (Vercel 대시보드)
NEXTAUTH_URL=https://yourdomain.com
NEXTAUTH_SECRET=your_secret
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
```

---

## 📊 마이그레이션 계획

### Phase 1: NextAuth.js 기본 설정 ✅
- [ ] 설치 및 설정
- [ ] Google OAuth 설정
- [ ] 로그인 페이지 생성

### Phase 2: 사용자 데이터 관리 ✅
- [ ] 사용자 정보 저장
- [ ] 세션 관리
- [ ] 프로필 페이지

### Phase 3: 기존 기능 통합 ✅
- [ ] 인증 필수 페이지
- [ ] 사용자별 분석 횟수 추적
- [ ] 구독 상태 연동

### Phase 4: 결제 연동 (다음)
- [ ] Stripe API 연동
- [ ] 결제 처리
- [ ] 구독 관리

---

## 🔗 참고 자료

- NextAuth.js: https://next-auth.js.org
- Google OAuth: https://developers.google.com/identity
- Stripe Integration: https://stripe.com/docs

---

**다음 단계**: Phase 6 (결제 시스템 - Stripe)
