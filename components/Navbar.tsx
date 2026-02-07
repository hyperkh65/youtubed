import Link from 'next/link'
import { useSession, signOut } from 'next-auth/react'

export default function Navbar() {
  const { data: session } = useSession()

  return (
    <nav className="bg-gradient-to-r from-slate-950 to-slate-900 border-b border-emerald-500/20 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* 로고 */}
          <Link href="/" className="flex items-center gap-2 font-bold text-xl text-white hover:text-emerald-400 transition">
            <span className="text-2xl">🔍</span>
            <span>KeyPoint Pro</span>
          </Link>

          {/* 네비게이션 링크 */}
          <div className="flex gap-6 items-center">
            <Link href="/pricing" className="text-slate-400 hover:text-white text-sm transition">
              가격책정
            </Link>

            {session?.user ? (
              <>
                {/* 프로필 정보 */}
                <div className="flex items-center gap-3">
                  <div className="text-right">
                    <p className="text-sm font-semibold text-white">{session.user.name}</p>
                    <div className="flex items-center gap-1">
                      <p className="text-xs text-slate-400">
                        {session.user.tier === 'free' ? 'Free' : session.user.tier.toUpperCase()}
                      </p>
                      {session.user.tier === 'pro' && (
                        <span className="bg-emerald-500/20 text-emerald-400 px-2 py-0.5 rounded text-xs font-semibold">
                          Pro
                        </span>
                      )}
                    </div>
                  </div>

                  {session.user.image && (
                    <img
                      src={session.user.image}
                      alt={session.user.name || 'User'}
                      className="w-8 h-8 rounded-full border border-slate-600"
                    />
                  )}
                </div>

                {/* 로그아웃 */}
                <button
                  onClick={() => signOut()}
                  className="px-4 py-2 rounded-lg bg-slate-700 hover:bg-slate-600 text-white text-sm font-semibold transition"
                >
                  로그아웃
                </button>
              </>
            ) : (
              <Link href="/auth/signin" className="px-4 py-2 rounded-lg bg-emerald-500 hover:bg-emerald-600 text-black font-semibold transition">
                로그인
              </Link>
            )}
          </div>
        </div>
      </div>
    </nav>
  )
}
