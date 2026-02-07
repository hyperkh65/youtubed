import Link from 'next/link'

export default function Navbar() {
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
          <div className="flex gap-8 items-center">
            <a href="#features" className="text-slate-400 hover:text-white text-sm transition">
              기능
            </a>
            <a href="#pricing" className="text-slate-400 hover:text-white text-sm transition">
              가격책정
            </a>
            <button className="px-4 py-2 rounded-lg bg-emerald-500 hover:bg-emerald-600 text-black font-semibold transition">
              무료 시작
            </button>
          </div>
        </div>
      </div>
    </nav>
  )
}
