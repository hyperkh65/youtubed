import Link from 'next/link'

export default function Navbar() {
  return (
    <nav className="bg-slate-950 border-b border-slate-700 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <Link href="/" className="font-bold text-xl text-white hover:text-blue-400">
            🎯 Keyword Analyzer
          </Link>
          <div className="flex gap-4">
            <span className="text-slate-400 text-sm">v2.0.0</span>
          </div>
        </div>
      </div>
    </nav>
  )
}
