import Link from 'next/link'

export default function Navbar() {
  return (
    <nav className="bg-black border-b border-emerald-500/20 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* 로고 */}
          <Link href="/" className="flex items-center gap-2 hover:opacity-80 transition">
            <div className="w-8 h-8 bg-emerald-500 rounded-lg flex items-center justify-center font-bold text-black">
              K
            </div>
            <span className="font-bold text-lg text-white hidden sm:inline">KeyPoints</span>
          </Link>

          {/* 네비게이션 */}
          <div className="hidden md:flex gap-8">
            <a href="#features" className="text-slate-300 hover:text-emerald-400 transition text-sm">
              기능
            </a>
            <a href="#analytics" className="text-slate-300 hover:text-emerald-400 transition text-sm">
              분석
            </a>
            <a href="#pricing" className="text-slate-300 hover:text-emerald-400 transition text-sm">
              요금제
            </a>
          </div>

          {/* 오른쪽 버튼 */}
          <div className="flex gap-3 items-center">
            <button className="text-slate-300 hover:text-white text-sm transition">
              로그인
            </button>
            <button className="bg-emerald-500 hover:bg-emerald-600 text-black font-semibold px-4 py-2 rounded-lg transition text-sm">
              14일 무료 시작
            </button>
          </div>
        </div>
      </div>
    </nav>
  )
}
