import { useSession } from 'next-auth/react'
import { useEffect } from 'react'
import { useRouter } from 'next/router'
import Head from 'next/head'
import Link from 'next/link'

export default function CheckoutSuccess() {
  const { data: session, status } = useSession()
  const router = useRouter()

  useEffect(() => {
    if (status === 'unauthenticated') {
      router.push('/auth/signin')
    }
  }, [status, router])

  return (
    <>
      <Head>
        <title>결제 완료 - KeyPoint Pro</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>

      <main className="min-h-screen bg-gradient-to-br from-black via-slate-900 to-black flex items-center justify-center px-4">
        <div className="max-w-md w-full text-center">
          {/* 성공 아이콘 */}
          <div className="mb-8">
            <div className="text-7xl mb-4">🎉</div>
            <div className="inline-block bg-emerald-500/20 border border-emerald-500/40 rounded-full p-4">
              <svg
                className="w-12 h-12 text-emerald-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M5 13l4 4L19 7"
                />
              </svg>
            </div>
          </div>

          {/* 헤드라인 */}
          <h1 className="text-4xl font-bold text-white mb-4">업그레이드 완료!</h1>

          {/* 설명 */}
          <p className="text-slate-400 mb-8 text-lg">
            {session?.user?.name}님,<br />
            <span className="text-emerald-400 font-semibold">Pro 플랜</span>에 오신 것을 환영합니다!
          </p>

          {/* 혜택 박스 */}
          <div className="bg-emerald-500/10 border border-emerald-500/20 rounded-xl p-8 mb-8">
            <h3 className="font-semibold text-white mb-6">이제 사용 가능한 기능:</h3>
            <ul className="space-y-3 text-left text-slate-300 text-sm">
              <li className="flex items-center gap-3">
                <span className="text-emerald-400">✓</span>
                <span>무제한 키워드 분석</span>
              </li>
              <li className="flex items-center gap-3">
                <span className="text-emerald-400">✓</span>
                <span>6개 포털 동시 분석</span>
              </li>
              <li className="flex items-center gap-3">
                <span className="text-emerald-400">✓</span>
                <span>검색 의도 분석</span>
              </li>
              <li className="flex items-center gap-3">
                <span className="text-emerald-400">✓</span>
                <span>경쟁사 분석</span>
              </li>
              <li className="flex items-center gap-3">
                <span className="text-emerald-400">✓</span>
                <span>12개월 트렌드 분석</span>
              </li>
              <li className="flex items-center gap-3">
                <span className="text-emerald-400">✓</span>
                <span>뉴스/블로그 추적</span>
              </li>
              <li className="flex items-center gap-3">
                <span className="text-emerald-400">✓</span>
                <span>CSV/PDF 다운로드</span>
              </li>
            </ul>
          </div>

          {/* CTA 버튼 */}
          <div className="space-y-3 mb-8">
            <Link
              href="/"
              className="block w-full bg-emerald-500 hover:bg-emerald-600 text-black font-bold py-3 rounded-lg transition"
            >
              분석 시작하기 →
            </Link>
            <Link
              href="/pricing"
              className="block w-full bg-slate-700 hover:bg-slate-600 text-white font-semibold py-3 rounded-lg transition"
            >
              요금제 관리
            </Link>
          </div>

          {/* 추가 정보 */}
          <div className="space-y-2 text-xs text-slate-500">
            <p>✓ 매달 자동으로 갱신됩니다</p>
            <p>✓ 30일 환불 보장 정책</p>
            <p>✓ 언제든지 취소 가능</p>
          </div>

          {/* 다음 단계 */}
          <div className="mt-12 p-4 bg-slate-800/30 rounded-lg border border-slate-700">
            <p className="text-slate-400 text-sm mb-4">
              다음 단계: 첫 번째 키워드를 분석해보세요
            </p>
            <Link
              href="/"
              className="inline-block text-emerald-400 hover:text-emerald-300 text-sm font-semibold"
            >
              분석 페이지로 이동 →
            </Link>
          </div>
        </div>
      </main>
    </>
  )
}
