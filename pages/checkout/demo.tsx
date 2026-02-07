import { useRouter } from 'next/router'
import { useSession } from 'next-auth/react'
import { useState } from 'react'
import Head from 'next/head'
import Link from 'next/link'

export default function CheckoutDemo() {
  const router = useRouter()
  const { data: session } = useSession()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const { plan, amount } = router.query

  if (!session?.user) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <p className="text-white">로그인 필요</p>
      </div>
    )
  }

  const planInfo = {
    pro: {
      name: 'Pro',
      price: 19,
      features: ['무제한 분석', '6개 포털 동시', '모든 고급 기능'],
    },
    team: {
      name: 'Team',
      price: 99,
      features: ['Pro의 모든 기능', '5개 팀 계정', 'Slack 연동'],
    },
  }

  const info = planInfo[plan as keyof typeof planInfo]

  const handleUpgrade = async () => {
    setLoading(true)
    setError('')

    try {
      // 구독 상태 업데이트
      const response = await fetch('/api/subscription/update', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          planTier: plan,
          stripeSubscriptionId: `sub_${Date.now()}`,
          stripeCustomerId: `cus_${Date.now()}`,
        }),
      })

      if (!response.ok) {
        throw new Error('Failed to upgrade')
      }

      // 성공 페이지로 이동
      router.push('/checkout/success')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error upgrading plan')
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <Head>
        <title>결제 - KeyPoint Pro</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>

      <main className="min-h-screen bg-black text-white px-4 py-20">
        <div className="max-w-md mx-auto">
          <Link href="/pricing" className="text-slate-400 hover:text-white mb-8 inline-block">
            ← 돌아가기
          </Link>

          <div className="bg-slate-900/50 border border-emerald-500/20 rounded-2xl p-8">
            <h1 className="text-3xl font-bold mb-2 text-emerald-400">
              {info?.name} 플랜
            </h1>
            <p className="text-slate-400 mb-8">
              월 ${info?.price} · 매달 자동 갱신
            </p>

            {/* 가격 */}
            <div className="bg-slate-800/50 rounded-lg p-6 mb-8">
              <div className="text-5xl font-bold mb-2">
                ${info?.price}<span className="text-lg text-slate-400">/월</span>
              </div>
              <p className="text-sm text-slate-400">
                신용카드로 결제 · 언제든 취소 가능
              </p>
            </div>

            {/* 포함된 기능 */}
            <div className="mb-8">
              <h3 className="font-semibold mb-4 text-sm">포함된 기능:</h3>
              <ul className="space-y-3">
                {info?.features.map((feature, idx) => (
                  <li key={idx} className="flex items-center gap-3 text-sm">
                    <span className="text-emerald-400">✓</span>
                    <span>{feature}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* 에러 메시지 */}
            {error && (
              <div className="bg-red-500/10 border border-red-500/20 rounded-lg p-4 mb-8 text-sm text-red-400">
                {error}
              </div>
            )}

            {/* 결제 버튼 */}
            <button
              onClick={handleUpgrade}
              disabled={loading}
              className="w-full bg-emerald-500 hover:bg-emerald-600 disabled:bg-slate-600 text-black font-bold py-3 rounded-lg transition mb-4"
            >
              {loading ? '처리 중...' : '구독 시작'}
            </button>

            {/* 테스트 카드 정보 */}
            <div className="bg-blue-500/10 border border-blue-500/20 rounded-lg p-4 text-xs text-blue-400">
              <p className="font-semibold mb-2">🧪 테스트 모드</p>
              <p>이것은 데모 페이지입니다.</p>
              <p className="mt-2 text-blue-300">
                실제 결제는 Stripe 통합 후 처리됩니다.
              </p>
            </div>

            {/* 30일 환불 보장 */}
            <p className="text-xs text-slate-500 text-center mt-8">
              30일 환불 보장 정책 · 숨겨진 수수료 없음
            </p>
          </div>

          {/* 사용자 정보 */}
          <div className="mt-8 bg-slate-800/30 rounded-lg p-4 text-sm">
            <p className="text-slate-400">
              <span className="font-semibold text-white">{session.user.name}</span>
              <br />
              {session.user.email}
            </p>
          </div>
        </div>
      </main>
    </>
  )
}
