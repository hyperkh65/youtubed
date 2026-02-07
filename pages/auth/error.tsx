import { useRouter } from 'next/router'
import Head from 'next/head'
import Link from 'next/link'

export default function Error() {
  const router = useRouter()
  const { error } = router.query

  const errorMessages: { [key: string]: string } = {
    Callback: '로그인 중 오류가 발생했습니다',
    OAuthSignin: 'OAuth 제공자 설정 오류',
    OAuthCallback: 'OAuth 콜백 오류',
    EmailCreateAccount: '이메일 계정 생성 오류',
    OAuthAccountNotLinked: '이메일이 다른 제공자에 연결되어 있습니다',
    EmailSignInError: '이메일 로그인 실패',
    CredentialsSignin: '인증 정보가 일치하지 않습니다',
    SessionCallback: '세션 콜백 오류',
    AccessDenied: '접근이 거부되었습니다',
  }

  const message = errorMessages[error as string] || '알 수 없는 오류가 발생했습니다'

  return (
    <>
      <Head>
        <title>로그인 오류 | KeyPoint Pro</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>

      <main className="min-h-screen bg-gradient-to-br from-black via-slate-900 to-black flex items-center justify-center px-4">
        <div className="max-w-md w-full">
          <div className="bg-red-500/10 border-2 border-red-500/30 rounded-2xl p-8 text-center">
            <div className="text-5xl mb-4">❌</div>
            <h1 className="text-2xl font-bold text-red-400 mb-4">
              로그인 오류
            </h1>
            <p className="text-slate-400 mb-6">
              {message}
            </p>

            <div className="space-y-3">
              <Link
                href="/auth/signin"
                className="block w-full bg-emerald-500 text-black py-3 rounded-lg font-bold hover:bg-emerald-600 transition"
              >
                다시 로그인하기
              </Link>
              <Link
                href="/"
                className="block w-full bg-slate-700 text-white py-3 rounded-lg font-bold hover:bg-slate-600 transition"
              >
                홈으로 돌아가기
              </Link>
            </div>

            <p className="text-xs text-slate-500 mt-6">
              문제가 계속되면{' '}
              <a href="mailto:support@keypointpro.com" className="text-slate-400 hover:text-white underline">
                지원팀에 문의
              </a>
              하세요
            </p>
          </div>
        </div>
      </main>
    </>
  )
}
