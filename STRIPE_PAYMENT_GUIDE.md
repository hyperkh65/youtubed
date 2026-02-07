# 💳 KeyPoint Pro Stripe 결제 시스템

## 개요
**목표**: Stripe을 사용한 안전하고 신뢰할 수 있는 결제 시스템 구축

---

## 🏗️ 아키텍처

### 1. Stripe 상품 설정

#### Product: Pro ($19/월)
```
Name: KeyPoint Pro - Pro Plan
Price: $19/month
Billing: Recurring (Monthly)
Interval: Month
Type: Service
```

#### Product: Team ($99/월)
```
Name: KeyPoint Pro - Team Plan
Price: $99/month
Billing: Recurring (Monthly)
Interval: Month
Type: Service
```

---

## 📊 결제 플로우

```
로그인 사용자 (Free)
    ↓
가격책정 페이지 방문
    ↓
Pro/Team 플랜 클릭
    ↓
Stripe Checkout 페이지
    ↓
카드 정보 입력
    ↓
결제 승인
    ↓
Stripe Webhook 콜백
    ↓
사용자 DB 업데이트 (tier = pro)
    ↓
대시보드 반영
    ↓
Pro 기능 사용 가능
```

---

## 🔧 구현 단계

### Step 1: Stripe 계정 설정

```bash
1. https://dashboard.stripe.com 접속
2. 계정 생성 및 검증
3. API Keys 생성
   - Publishable key (공개)
   - Secret key (비공개)
4. Webhook endpoint 생성
   - URL: https://yourdomain.com/api/webhooks/stripe
   - Events: customer.subscription.updated, customer.subscription.deleted
```

### Step 2: 환경 변수 설정

`.env.local`:
```env
# Stripe API Keys
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Product IDs (Stripe에서 생성 후)
NEXT_PUBLIC_STRIPE_PRICE_PRO=price_...
NEXT_PUBLIC_STRIPE_PRICE_TEAM=price_...
```

### Step 3: 라이브러리 설치

```bash
npm install stripe @stripe/react-stripe-js @stripe/js
```

### Step 4: API 엔드포인트

#### `/api/checkout` - 결제 세션 생성
```typescript
import Stripe from 'stripe'

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!)

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).end()
  }

  const { priceId, userId, email } = req.body

  const session = await stripe.checkout.sessions.create({
    payment_method_types: ['card'],
    customer_email: email,
    line_items: [
      {
        price: priceId,
        quantity: 1,
      },
    ],
    mode: 'subscription',
    success_url: `${process.env.NEXTAUTH_URL}/dashboard?session_id={CHECKOUT_SESSION_ID}`,
    cancel_url: `${process.env.NEXTAUTH_URL}/pricing`,
    metadata: {
      userId,
    },
  })

  res.json({ sessionId: session.id })
}
```

#### `/api/webhooks/stripe` - Webhook 핸들러
```typescript
import Stripe from 'stripe'
import { buffer } from 'micro'

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!)

export const config = {
  api: {
    bodyParser: false,
  },
}

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).end()
  }

  const buf = await buffer(req)
  const sig = req.headers['stripe-signature']

  let event

  try {
    event = stripe.webhooks.constructEvent(
      buf,
      sig,
      process.env.STRIPE_WEBHOOK_SECRET!
    )
  } catch (err) {
    res.status(400).send(`Webhook Error: ${err.message}`)
    return
  }

  switch (event.type) {
    case 'customer.subscription.created':
    case 'customer.subscription.updated':
      const subscription = event.data.object

      // 구독 상태에 따라 사용자 업데이트
      const tier = subscription.metadata.plan === 'team' ? 'team' : 'pro'

      // DB 업데이트
      // await updateUserTier(subscription.metadata.userId, tier, subscription.id)

      break

    case 'customer.subscription.deleted':
      // 구독 취소 처리
      // await updateUserTier(subscription.metadata.userId, 'free', null)
      break
  }

  res.json({ received: true })
}
```

### Step 5: 결제 버튼 UI

```typescript
// components/CheckoutButton.tsx

import { useSession } from 'next-auth/react'
import { loadStripe } from '@stripe/js'

const stripePromise = loadStripe(
  process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY!
)

export default function CheckoutButton({ priceId, planName }) {
  const { data: session } = useSession()
  const [loading, setLoading] = useState(false)

  const handleCheckout = async () => {
    setLoading(true)

    const response = await fetch('/api/checkout', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        priceId,
        userId: session?.user?.id,
        email: session?.user?.email,
      }),
    })

    const { sessionId } = await response.json()

    const stripe = await stripePromise
    await stripe?.redirectToCheckout({ sessionId })
  }

  return (
    <button
      onClick={handleCheckout}
      disabled={loading}
      className="w-full bg-emerald-500 text-black font-bold py-3 rounded-lg hover:bg-emerald-600 disabled:bg-slate-600 transition"
    >
      {loading ? '로딩 중...' : `${planName} 시작하기`}
    </button>
  )
}
```

### Step 6: 성공 페이지

```typescript
// pages/checkout/success.tsx

import { useSession } from 'next-auth/react'
import Link from 'next/link'

export default function CheckoutSuccess() {
  const { data: session } = useSession()

  return (
    <div className="min-h-screen bg-black flex items-center justify-center">
      <div className="max-w-md text-center">
        <div className="text-6xl mb-6">🎉</div>
        <h1 className="text-3xl font-bold text-white mb-4">
          업그레이드 완료!
        </h1>
        <p className="text-slate-400 mb-8">
          {session?.user?.name}님, Pro 플랜에 오신 것을 환영합니다.
        </p>

        <div className="bg-emerald-500/10 border border-emerald-500/20 rounded-lg p-4 mb-8">
          <p className="text-emerald-400 text-sm">
            ✅ 무제한 분석<br/>
            ✅ 6개 포털 동시<br/>
            ✅ 모든 고급 기능
          </p>
        </div>

        <Link
          href="/dashboard"
          className="inline-block px-8 py-3 bg-emerald-500 text-black font-bold rounded-lg hover:bg-emerald-600 transition"
        >
          분석 시작하기 →
        </Link>
      </div>
    </div>
  )
}
```

---

## 🔐 보안 고려사항

### 1. API 키 관리
```
✅ Secret Key는 서버에서만 사용
✅ Publishable Key는 클라이언트에서 사용
✅ .env.local에 저장 (git 무시)
✅ 프로덕션에서는 환경변수로 주입
```

### 2. Webhook 검증
```typescript
// Signature 검증 필수
const event = stripe.webhooks.constructEvent(
  body,
  signature,
  webhookSecret
)
```

### 3. 결제 금액 검증
```typescript
// 클라이언트에서 보낸 금액과 실제 가격 비교
const priceId = req.body.priceId
const price = await stripe.prices.retrieve(priceId)
if (price.unit_amount !== expectedAmount) {
  throw new Error('Price mismatch')
}
```

---

## 📊 구독 상태 관리

### 사용자 DB 스키마 업데이트
```typescript
interface UserSubscription {
  userId: string
  stripeCustomerId: string
  stripeSubscriptionId: string
  subscriptionStatus: 'active' | 'past_due' | 'cancelled' | 'unpaid'
  currentPeriodStart: Date
  currentPeriodEnd: Date
  planTier: 'free' | 'pro' | 'team'
  cancelAtPeriodEnd: boolean
}
```

### NextAuth 콜백 업데이트
```typescript
async jwt({ token, user, account }) {
  if (user) {
    // 사용자 구독 정보 조회
    const subscription = await getSubscription(user.id)
    token.tier = subscription?.planTier || 'free'
    token.stripeSubscriptionId = subscription?.stripeSubscriptionId
    token.subscriptionStatus = subscription?.subscriptionStatus
  }
  return token
}
```

---

## 🧪 테스트 카드

Stripe 테스트 환경에서 사용 가능한 카드:

```
결제 성공:
4242 4242 4242 4242
12/25, CVC: 123

결제 실패:
4000 0000 0000 0002
12/25, CVC: 123

3D Secure (추가 인증):
4000 2500 0000 3155
12/25, CVC: 123
```

---

## 📈 운영 대시보드

Stripe Dashboard에서 모니터링:
- MRR (Monthly Recurring Revenue)
- Churn Rate (해약률)
- Customer LTV (Lifetime Value)
- Payment Success Rate

---

## 💡 결제 흐름 최적화

### 1. 원클릭 결제
```
기존: 가격페이지 → Checkout → 카드 입력 → 결제
개선: 프로필에서 저장된 카드 선택 → 즉시 구독 갱신
```

### 2. 자동 재시도
```
Stripe 자동 설정:
- 결제 실패 시 3일 후 재시도
- 7일 후 재재시도
- 결제 수단 업데이트 알림 발송
```

### 3. 할인 및 쿠폰
```typescript
const session = await stripe.checkout.sessions.create({
  // ...
  discounts: [
    {
      coupon: 'LAUNCH_50', // 50% 할인
    },
  ],
})
```

---

## 🚀 배포 체크리스트

- [ ] Stripe Production 계정 생성
- [ ] API 키 환경변수 설정
- [ ] Webhook URL 등록
- [ ] SSL 인증서 설정 (HTTPS 필수)
- [ ] 결제 테스트 (여러 시나리오)
- [ ] 환불 정책 문서화
- [ ] 고객 지원 체계 구축
- [ ] 모니터링 대시보드 설정

---

## 📞 고객 지원

### 결제 관련 FAQ
```
Q: 어떤 카드를 지원하나요?
A: Visa, Mastercard, American Express를 지원합니다.

Q: 환불은 어떻게 하나요?
A: 구독 취소 후 환불을 요청할 수 있습니다.
   30일 환불 보장 정책으로 전액 환불됩니다.

Q: 구독을 취소하려면?
A: 대시보드에서 "구독 취소" 클릭 후 즉시 처리됩니다.
```

---

## 🔗 참고 자료

- Stripe 공식 문서: https://stripe.com/docs
- Stripe Checkout: https://stripe.com/docs/payments/checkout
- Webhooks: https://stripe.com/docs/webhooks

---

**다음 단계**: Stripe API 통합 구현
