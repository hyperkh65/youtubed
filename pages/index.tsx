import React, { useState, useEffect } from 'react'
import Head from 'next/head'
import axios from 'axios'
import dynamic from 'next/dynamic'
import { useSession, signIn } from 'next-auth/react'
import Link from 'next/link'

const Plot = dynamic(() => import('react-plotly.js'), { ssr: false })

// 산업별 트렌딩 키워드
const INDUSTRY_TRENDING = {
  seo: [
    { keyword: 'AI 콘텐츠 라이팅', trend: 'rising', volume: 125000 },
    { keyword: '코어 웹 바이탈', trend: 'rising', volume: 98000 },
    { keyword: 'SEO 최적화', trend: 'stable', volume: 186000 },
    { keyword: '검색 의도 분석', trend: 'rising', volume: 54000 },
    { keyword: '키워드 클러스터링', trend: 'rising', volume: 32000 },
    { keyword: 'E-E-A-T 콘텐츠', trend: 'hot', volume: 78000 },
  ],
  ecommerce: [
    { keyword: '무선이어폰', trend: 'rising', volume: 450000 },
    { keyword: '스마트밴드', trend: 'hot', volume: 380000 },
    { keyword: '블루투스 스피커', trend: 'stable', volume: 265000 },
    { keyword: '무선 충전기', trend: 'rising', volume: 195000 },
    { keyword: '휴대폰 필름', trend: 'rising', volume: 142000 },
    { keyword: '보조배터리', trend: 'stable', volume: 287000 },
  ],
  content: [
    { keyword: '쇼츠 제작 팁', trend: 'rising', volume: 145000 },
    { keyword: '유튜브 알고리즘', trend: 'stable', volume: 220000 },
    { keyword: '채널 성장 전략', trend: 'rising', volume: 98000 },
    { keyword: '썸네일 디자인', trend: 'rising', volume: 125000 },
    { keyword: '영상 편집 기초', trend: 'stable', volume: 178000 },
    { keyword: '바이럴 콘텐츠', trend: 'hot', volume: 267000 },
  ],
  agency: [
    { keyword: '디지털 마케팅 전략', trend: 'rising', volume: 198000 },
    { keyword: '소셜 미디어 마케팅', trend: 'rising', volume: 156000 },
    { keyword: '콘텐츠 마케팅', trend: 'stable', volume: 245000 },
    { keyword: '고객 분석', trend: 'rising', volume: 87000 },
    { keyword: 'ROI 최적화', trend: 'rising', volume: 64000 },
    { keyword: 'A/B 테스팅', trend: 'stable', volume: 102000 },
  ],
}

// 산업 설정
const INDUSTRY_CONFIGS = {
  seo: {
    name: 'SEO & 블로그',
    icon: '📈',
    description: '검색 엔진 최적화를 위한 심층 분석',
    portals: ['Google', 'Naver', 'Daum'],
    color: 'emerald'
  },
  ecommerce: {
    name: '이커머스',
    icon: '🛒',
    description: '상품 판매 기회를 찾아주는 분석',
    portals: ['Amazon', 'Coupang', 'Naver'],
    color: 'blue'
  },
  content: {
    name: '콘텐츠 크리에이터',
    icon: '🎬',
    description: '영상/블로그 인기도 트렌드 분석',
    portals: ['YouTube', 'Google', 'Naver'],
    color: 'purple'
  },
  agency: {
    name: '마케팅 대행사',
    icon: '🏢',
    description: '종합 마케팅 전략 수립을 위한 분석',
    portals: ['Google', 'Naver', 'YouTube', 'Amazon'],
    color: 'cyan'
  },
}

const ALL_PORTALS = ['Google', 'Naver', 'Daum', 'YouTube', 'Amazon', 'Coupang']

const TrustBadge = ({ score }: { score: number }) => {
  if (score >= 85) return <span className="text-emerald-400 font-semibold text-xs">🟢 {score}%</span>
  if (score >= 70) return <span className="text-yellow-500 font-semibold text-xs">🟡 {score}%</span>
  return <span className="text-red-500 font-semibold text-xs">🔴 {score}%</span>
}

export default function Home() {
  const { data: session, status } = useSession()
  const [selectedIndustry, setSelectedIndustry] = useState<'seo' | 'ecommerce' | 'content' | 'agency'>('seo')
  const [keyword, setKeyword] = useState('')
  const [selectedPortals, setSelectedPortals] = useState<string[]>(['Naver', 'Google'])
  const [analysis, setAnalysis] = useState<any>(null)
  const [recommendations, setRecommendations] = useState<any[]>([])
  const [loading, setLoading] = useState(false)
  const [activeTab, setActiveTab] = useState('analysis')
  const [showIndustrySelector, setShowIndustrySelector] = useState(true)
  const [userTier, setUserTier] = useState<'free' | 'pro' | 'team'>('free')
  const [monthlyAnalysisCount, setMonthlyAnalysisCount] = useState(0)
  const [showUpgradeModal, setShowUpgradeModal] = useState(false)

  // 로그인 상태에 따라 userTier 업데이트
  useEffect(() => {
    if (session?.user) {
      setUserTier((session.user as any).tier || 'free')
    }
  }, [session])

  const industryConfig = INDUSTRY_CONFIGS[selectedIndustry]
  const trendingKeywords = INDUSTRY_TRENDING[selectedIndustry]
  const canAnalyze = userTier === 'free' ? monthlyAnalysisCount < 10 : true
  const analysisRemaining = userTier === 'free' ? 10 - monthlyAnalysisCount : '무제한'

  const togglePortal = (portal: string) => {
    // Free 사용자는 1개 포털만 선택 가능
    if (userTier === 'free') {
      if (selectedPortals.includes(portal)) {
        setSelectedPortals(prev => prev.filter(p => p !== portal))
      } else if (selectedPortals.length < 1) {
        setSelectedPortals([portal])
      } else {
        alert('Free 플랜은 1개 포털만 선택 가능합니다.\nPro로 업그레이드하면 6개 포털까지 동시 분석 가능합니다.')
      }
    } else {
      setSelectedPortals(prev =>
        prev.includes(portal)
          ? prev.filter(p => p !== portal)
          : [...prev, portal]
      )
    }
  }

  const handleAnalyze = async () => {
    if (!keyword.trim()) {
      alert('키워드를 입력해주세요')
      return
    }

    if (selectedPortals.length === 0) {
      alert('최소 하나의 포털을 선택해주세요')
      return
    }

    // Free 사용자 분석 횟수 제한 확인
    if (userTier === 'free' && monthlyAnalysisCount >= 10) {
      setShowUpgradeModal(true)
      return
    }

    setLoading(true)
    try {
      const response = await axios.post('/api/keywords/analyze', {
        keyword,
        portal: selectedPortals.length === 1 ? selectedPortals[0] : 'All',
        industry: selectedIndustry
      })
      setAnalysis(response.data)
      setShowIndustrySelector(false)
      setActiveTab('analysis')

      // 분석 횟수 증가
      if (userTier === 'free') {
        setMonthlyAnalysisCount(prev => prev + 1)
      }
    } catch (error) {
      console.error('분석 오류:', error)
      alert('분석 중 오류가 발생했습니다')
    } finally {
      setLoading(false)
    }
  }

  const handleGetRecommendations = async () => {
    if (!keyword.trim()) {
      alert('키워드를 입력해주세요')
      return
    }

    setLoading(true)
    try {
      const response = await axios.post('/api/keywords/recommendations', {
        keywords: [keyword],
        industry: selectedIndustry
      })
      setRecommendations(response.data.recommendations || [])
      setActiveTab('recommendations')
    } catch (error) {
      console.error('추천 오류:', error)
      alert('추천 데이터를 불러오는 중 오류가 발생했습니다')
    } finally {
      setLoading(false)
    }
  }

  const handleTrendingClick = (trendingKeyword: string) => {
    setKeyword(trendingKeyword)
  }

  // 로그인 필수
  if (!session?.user) {
    return (
      <>
        <Head>
          <title>KeyPoint Pro - 범용 키워드 분석 플랫폼</title>
          <meta name="description" content="모든 산업의 키워드 기회를 찾아주는 데이터 분석 플랫폼" />
          <meta name="viewport" content="width=device-width, initial-scale=1" />
        </Head>

        <main className="min-h-screen bg-gradient-to-br from-black via-slate-900 to-black flex items-center justify-center px-4">
          <div className="max-w-md w-full text-center">
            <div className="text-6xl mb-6">🔍</div>
            <h1 className="text-4xl font-bold mb-4 text-white">KeyPoint Pro</h1>
            <p className="text-slate-400 mb-8">
              모든 산업의 키워드 기회를<br />
              찾아주는 데이터 분석 플랫폼
            </p>

            <div className="bg-slate-900/50 border border-slate-700 rounded-lg p-8 mb-8">
              <p className="text-slate-300 mb-6">
                무료로 시작하여 강력한 키워드 분석을 경험하세요.
              </p>

              <button
                onClick={() => signIn('google')}
                className="w-full bg-emerald-500 hover:bg-emerald-600 text-black font-bold py-3 rounded-lg transition mb-3"
              >
                무료로 시작하기
              </button>

              <Link
                href="/auth/signin"
                className="block text-sm text-slate-400 hover:text-white transition"
              >
                다른 로그인 옵션 →
              </Link>
            </div>

            <p className="text-xs text-slate-500">
              로그인하면{' '}
              <a href="#" className="text-slate-400 hover:text-white underline">
                이용약관
              </a>
              에 동의하는 것입니다
            </p>
          </div>
        </main>
      </>
    )
  }

  return (
    <>
      <Head>
        <title>KeyPoint Pro - 범용 키워드 분석 플랫폼</title>
        <meta name="description" content="모든 산업의 키워드 기회를 찾아주는 데이터 분석 플랫폼. Google, Naver, YouTube 등 다중 포털 동시 분석" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>

      <main className="min-h-screen bg-black text-white">
        {/* 업그레이드 모달 */}
        {showUpgradeModal && (
          <div className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 px-4">
            <div className="bg-slate-900 border-2 border-emerald-500 rounded-2xl p-8 max-w-md">
              <h2 className="text-2xl font-bold mb-4">🚀 무제한 분석하기</h2>
              <p className="text-slate-400 mb-6">
                이달 분석 횟수를 모두 사용했습니다.
                <br/><br/>
                <strong>Pro로 업그레이드하면:</strong>
              </p>
              <ul className="space-y-2 text-sm mb-8 text-slate-300">
                <li>✅ 무제한 분석</li>
                <li>✅ 6개 포털 동시 분석</li>
                <li>✅ 검색 의도, 경쟁사, 트렌드 분석</li>
                <li>✅ 신뢰도 85%+ (Google API)</li>
              </ul>
              <div className="flex gap-3">
                <button
                  onClick={() => setShowUpgradeModal(false)}
                  className="flex-1 px-4 py-3 border border-slate-600 text-white rounded-lg hover:bg-slate-800 transition"
                >
                  나중에
                </button>
                <a
                  href="/pricing"
                  className="flex-1 px-4 py-3 bg-emerald-500 text-black font-bold rounded-lg hover:bg-emerald-600 transition text-center"
                >
                  Pro 보기 ($19/월)
                </a>
              </div>
            </div>
          </div>
        )}

        {/* Free 티어 분석 횟수 표시 */}
        {userTier === 'free' && (
          <div className="sticky top-16 bg-gradient-to-r from-yellow-500/10 to-orange-500/10 border-b border-yellow-500/20 px-4 py-3 z-40">
            <div className="max-w-6xl mx-auto flex items-center justify-between">
              <div className="flex items-center gap-4">
                <span className="font-semibold">
                  📊 이달 분석: {monthlyAnalysisCount}/10 사용됨
                </span>
                <div className="w-40 bg-slate-700 rounded-full h-2">
                  <div
                    className="bg-yellow-500 h-2 rounded-full transition-all"
                    style={{ width: `${(monthlyAnalysisCount / 10) * 100}%` }}
                  />
                </div>
              </div>
              <a
                href="/pricing"
                className="px-4 py-1 bg-emerald-500 hover:bg-emerald-600 text-black text-sm font-bold rounded transition"
              >
                Pro 업그레이드 →
              </a>
            </div>
          </div>
        )}

        {/* 히어로 섹션 */}
        <section className="relative min-h-[700px] bg-gradient-to-b from-black via-emerald-950/5 to-black px-4 py-20">
          <div className="max-w-6xl mx-auto">
            {/* 산업 선택 UI */}
            {showIndustrySelector && (
              <div className="mb-16">
                <p className="text-center text-slate-400 text-lg mb-8">
                  어떤 산업의 키워드를 분석하시나요?
                </p>
                <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
                  {(Object.keys(INDUSTRY_CONFIGS) as Array<'seo' | 'ecommerce' | 'content' | 'agency'>).map((industry) => {
                    const config = INDUSTRY_CONFIGS[industry]
                    return (
                      <button
                        key={industry}
                        onClick={() => setSelectedIndustry(industry)}
                        className={`p-6 rounded-xl border-2 transition duration-200 text-left ${
                          selectedIndustry === industry
                            ? `border-emerald-500 bg-emerald-500/10 shadow-lg shadow-emerald-500/20`
                            : `border-slate-700 hover:border-slate-600 bg-slate-900/30 hover:bg-slate-900/50`
                        }`}
                      >
                        <div className="text-3xl mb-2">{config.icon}</div>
                        <h3 className="font-bold text-lg mb-1">{config.name}</h3>
                        <p className="text-sm text-slate-400">{config.description}</p>
                      </button>
                    )
                  })}
                </div>
              </div>
            )}

            {/* 헤드라인 */}
            <div className="text-center mb-12">
              <h1 className="text-5xl md:text-6xl font-bold mb-4 leading-tight">
                {industryConfig.icon} {industryConfig.name}<br />
                <span className="bg-gradient-to-r from-emerald-400 to-cyan-400 bg-clip-text text-transparent">
                  키워드 기회 찾기
                </span>
              </h1>
              <p className="text-lg text-slate-400 mb-8 max-w-3xl mx-auto">
                {selectedPortals.join(', ')} 등 {selectedPortals.length}개 포털 동시 분석<br />
                정확한 데이터 기반 {industryConfig.name} 전략 수립
              </p>
            </div>

            {/* 검색 바 */}
            <div className="bg-slate-900/50 border border-emerald-500/20 rounded-xl p-8 mb-12 backdrop-blur">
              {/* 포털 선택 */}
              <div className="mb-6">
                <label className="block text-sm text-slate-400 mb-3 font-semibold">
                  분석할 포털 선택 (중복 선택 가능)
                </label>
                <div className="grid md:grid-cols-3 lg:grid-cols-6 gap-3">
                  {(industryConfig.portals as string[]).map((portal) => (
                    <label
                      key={portal}
                      className={`flex items-center gap-2 p-3 rounded-lg border cursor-pointer transition ${
                        selectedPortals.includes(portal)
                          ? 'border-emerald-500 bg-emerald-500/10'
                          : 'border-slate-700 hover:border-slate-600'
                      }`}
                    >
                      <input
                        type="checkbox"
                        checked={selectedPortals.includes(portal)}
                        onChange={() => togglePortal(portal)}
                        className="w-4 h-4 rounded"
                      />
                      <span className="text-sm font-medium">{portal}</span>
                    </label>
                  ))}
                </div>
              </div>

              {/* 키워드 입력 */}
              <div className="mb-6">
                <label className="block text-sm text-slate-400 mb-2">키워드 입력</label>
                <input
                  type="text"
                  value={keyword}
                  onChange={(e) => setKeyword(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleAnalyze()}
                  placeholder="분석할 키워드를 입력하세요... (예: 파이썬 기초)"
                  className="w-full bg-slate-800 border border-emerald-500/30 rounded-lg px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500 transition"
                />
              </div>

              {/* 버튼 */}
              <div className="flex gap-3">
                <button
                  onClick={handleAnalyze}
                  disabled={loading}
                  className="flex-1 bg-emerald-500 hover:bg-emerald-600 disabled:bg-slate-600 text-black font-bold py-3 rounded-lg transition duration-200"
                >
                  {loading ? '분석 중...' : '🔍 분석'}
                </button>
                <button
                  onClick={handleGetRecommendations}
                  disabled={loading}
                  className="flex-1 bg-cyan-500 hover:bg-cyan-600 disabled:bg-slate-600 text-black font-bold py-3 rounded-lg transition duration-200"
                >
                  {loading ? '로딩 중...' : '💡 추천 키워드'}
                </button>
              </div>
            </div>

            {/* 트렌딩 해시태그 */}
            <div className="text-center">
              <p className="text-sm text-slate-500 mb-4">🔥 현재 {industryConfig.name}의 핫한 키워드</p>
              <div className="flex flex-wrap justify-center gap-3">
                {trendingKeywords.map((item) => (
                  <button
                    key={item.keyword}
                    onClick={() => handleTrendingClick(item.keyword)}
                    className="px-4 py-2 bg-slate-800 hover:bg-emerald-900/30 border border-emerald-500/30 hover:border-emerald-500/60 rounded-full text-sm transition duration-200"
                  >
                    #{item.keyword}
                    <span className="ml-2 text-emerald-400 text-xs">
                      {item.trend === 'hot' ? '🔥' : item.trend === 'rising' ? '📈' : '→'}
                    </span>
                  </button>
                ))}
              </div>
            </div>
          </div>
        </section>

        {/* 탭 네비게이션 */}
        {(analysis || recommendations.length > 0) && (
          <section className="max-w-6xl mx-auto px-4 py-12">
            <div className="border-b border-emerald-500/20 mb-8">
              <div className="flex gap-8 overflow-x-auto">
                <button
                  onClick={() => setActiveTab('analysis')}
                  className={`pb-4 px-2 font-semibold transition whitespace-nowrap ${
                    activeTab === 'analysis'
                      ? 'text-emerald-400 border-b-2 border-emerald-400'
                      : 'text-slate-400 hover:text-slate-200'
                  }`}
                >
                  📊 분석 결과
                </button>
                <button
                  onClick={() => userTier === 'free' ? setShowUpgradeModal(true) : setActiveTab('intent')}
                  className={`pb-4 px-2 font-semibold transition whitespace-nowrap flex items-center gap-1 ${
                    activeTab === 'intent'
                      ? 'text-emerald-400 border-b-2 border-emerald-400'
                      : 'text-slate-400 hover:text-slate-200'
                  } ${userTier === 'free' ? 'opacity-50 cursor-not-allowed' : ''}`}
                >
                  🎯 검색 의도 {userTier === 'free' && <span className="text-xs bg-red-500/20 text-red-400 px-2 py-0.5 rounded">Pro</span>}
                </button>
                <button
                  onClick={() => userTier === 'free' ? setShowUpgradeModal(true) : setActiveTab('trends')}
                  className={`pb-4 px-2 font-semibold transition whitespace-nowrap flex items-center gap-1 ${
                    activeTab === 'trends'
                      ? 'text-emerald-400 border-b-2 border-emerald-400'
                      : 'text-slate-400 hover:text-slate-200'
                  } ${userTier === 'free' ? 'opacity-50 cursor-not-allowed' : ''}`}
                >
                  📈 트렌드 분석 {userTier === 'free' && <span className="text-xs bg-red-500/20 text-red-400 px-2 py-0.5 rounded">Pro</span>}
                </button>
                <button
                  onClick={() => userTier === 'free' ? setShowUpgradeModal(true) : setActiveTab('newsblog')}
                  className={`pb-4 px-2 font-semibold transition whitespace-nowrap flex items-center gap-1 ${
                    activeTab === 'newsblog'
                      ? 'text-emerald-400 border-b-2 border-emerald-400'
                      : 'text-slate-400 hover:text-slate-200'
                  } ${userTier === 'free' ? 'opacity-50 cursor-not-allowed' : ''}`}
                >
                  📰 뉴스/블로그 {userTier === 'free' && <span className="text-xs bg-red-500/20 text-red-400 px-2 py-0.5 rounded">Pro</span>}
                </button>
                <button
                  onClick={() => userTier === 'free' ? setShowUpgradeModal(true) : setActiveTab('competitors')}
                  className={`pb-4 px-2 font-semibold transition whitespace-nowrap flex items-center gap-1 ${
                    activeTab === 'competitors'
                      ? 'text-emerald-400 border-b-2 border-emerald-400'
                      : 'text-slate-400 hover:text-slate-200'
                  } ${userTier === 'free' ? 'opacity-50 cursor-not-allowed' : ''}`}
                >
                  🏆 경쟁사 분석 {userTier === 'free' && <span className="text-xs bg-red-500/20 text-red-400 px-2 py-0.5 rounded">Pro</span>}
                </button>
                <button
                  onClick={() => setActiveTab('recommendations')}
                  className={`pb-4 px-2 font-semibold transition whitespace-nowrap ${
                    activeTab === 'recommendations'
                      ? 'text-emerald-400 border-b-2 border-emerald-400'
                      : 'text-slate-400 hover:text-slate-200'
                  }`}
                >
                  💡 추천 키워드
                </button>
              </div>
            </div>

            {/* 분석 결과 탭 */}
            {activeTab === 'analysis' && analysis && (
              <div className="space-y-8">
                {/* 종합 요약 카드 */}
                {analysis.analysis?.summary && (
                  <div className="bg-gradient-to-r from-emerald-500/20 to-cyan-500/20 border border-emerald-500/40 rounded-xl p-6 mb-8">
                    <div className="flex items-start gap-4 mb-4">
                      <div className="text-4xl">{analysis.analysis.summary.recommendation.split(' ')[0]}</div>
                      <div className="flex-1">
                        <h3 className="text-xl font-bold mb-2">
                          {analysis.analysis.summary.recommendation}
                        </h3>
                        <div className="flex gap-4">
                          <div>
                            <p className="text-slate-400 text-sm">종합 점수</p>
                            <p className="text-emerald-400 font-bold text-lg">{analysis.analysis.summary.overallScore}/100</p>
                          </div>
                          <div>
                            <p className="text-slate-400 text-sm">신뢰도</p>
                            <TrustBadge score={85} />
                          </div>
                        </div>
                      </div>
                    </div>
                    <p className="text-slate-300 mb-4 text-sm">{analysis.analysis.keywordAnalysis.type.toUpperCase()} 키워드</p>
                    <div className="grid md:grid-cols-2 gap-4 text-sm">
                      <div>
                        <p className="text-emerald-400 font-semibold mb-2">💪 강점</p>
                        <ul className="space-y-1 text-slate-300">
                          {analysis.analysis.summary.strengths?.map((s: string, i: number) => (
                            <li key={i}>✓ {s}</li>
                          ))}
                        </ul>
                      </div>
                      <div>
                        <p className="text-cyan-400 font-semibold mb-2">⚠️ 약점</p>
                        <ul className="space-y-1 text-slate-300">
                          {analysis.analysis.summary.weaknesses?.map((w: string, i: number) => (
                            <li key={i}>✗ {w}</li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  </div>
                )}

                <h2 className="text-3xl font-bold mb-8">
                  '{keyword}' 분석 결과 ({selectedPortals.length}개 포털)
                </h2>

                {/* 포털별 결과 카드 */}
                <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
                  {Object.entries(analysis.analysis?.portals || {}).map(([portal, data]: [string, any]) => (
                    <div
                      key={portal}
                      className="bg-slate-900/50 border border-emerald-500/20 rounded-xl p-6 hover:border-emerald-500/60 transition"
                    >
                      <div className="flex justify-between items-center mb-4">
                        <h3 className="text-emerald-400 font-bold text-lg">{portal}</h3>
                        <TrustBadge score={85} />
                      </div>
                      <div className="space-y-3 text-sm">
                        <div>
                          <span className="text-slate-400">월간 검색량</span>
                          <p className="text-white font-bold text-lg">
                            {data.estimated_search_volume?.toLocaleString() ||
                             data.monthly_searches?.toLocaleString() ||
                             'N/A'}
                          </p>
                        </div>
                        <div className="pt-2 border-t border-slate-700">
                          <span className="text-slate-400">트렌드</span>
                          <p className="text-white font-semibold capitalize">
                            {data.trend === 'rising' && '📈'} {data.trend || 'N/A'}
                          </p>
                        </div>
                        <div>
                          <span className="text-slate-400">난이도</span>
                          <div className="flex items-center gap-2 mt-1">
                            <div className="flex-1 bg-slate-700 rounded-full h-2">
                              <div
                                className="bg-emerald-500 h-2 rounded-full"
                                style={{
                                  width: `${(data.keyword_difficulty_score || data.difficulty || 0)}%`,
                                }}
                              />
                            </div>
                            <span className="text-white font-bold">
                              {data.keyword_difficulty_score || data.difficulty || 0}
                            </span>
                          </div>
                        </div>
                        {data.cpc && (
                          <div>
                            <span className="text-slate-400">CPC</span>
                            <p className="text-cyan-400 font-bold">${data.cpc}</p>
                          </div>
                        )}
                        {data.opportunity_score && (
                          <div>
                            <span className="text-slate-400">기회 점수</span>
                            <p className="text-emerald-400 font-bold">{data.opportunity_score}</p>
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* 검색 의도 분석 탭 */}
            {activeTab === 'intent' && analysis && (
              <div className="space-y-8">
                <h2 className="text-3xl font-bold mb-8">
                  '{keyword}' 검색 의도 분석
                </h2>

                {analysis.analysis?.searchIntent && (
                  <div className="space-y-6">
                    <div className="bg-slate-900/50 border border-emerald-500/20 rounded-xl p-6">
                      <h3 className="text-xl font-bold mb-4">주요 검색 의도</h3>
                      <div className="space-y-4">
                        <div>
                          <p className="text-slate-400 text-sm mb-2">
                            {analysis.analysis.searchIntent.primaryIntent}
                          </p>
                          <div className="flex items-center gap-2">
                            <div className="flex-1 bg-slate-700 rounded-full h-3">
                              <div
                                className="bg-emerald-500 h-3 rounded-full"
                                style={{ width: `${analysis.analysis.searchIntent.confidence}%` }}
                              />
                            </div>
                            <span className="text-white font-bold">
                              {analysis.analysis.searchIntent.confidence}%
                            </span>
                          </div>
                        </div>
                      </div>
                    </div>

                    <div className="grid md:grid-cols-2 gap-6">
                      <div className="bg-slate-900/50 border border-emerald-500/20 rounded-xl p-6">
                        <p className="text-emerald-400 font-semibold mb-4">🎯 추천 콘텐츠 형식</p>
                        <ul className="space-y-2 text-slate-300 text-sm">
                          {analysis.analysis.searchIntent.recommendedFormats?.map((format: string, i: number) => (
                            <li key={i}>• {format}</li>
                          ))}
                        </ul>
                      </div>
                      <div className="bg-slate-900/50 border border-emerald-500/20 rounded-xl p-6">
                        <p className="text-cyan-400 font-semibold mb-4">⚠️ 주의사항</p>
                        <ul className="space-y-2 text-slate-300 text-sm">
                          <li>• {analysis.analysis.searchIntent.warning || '의도와 맞는 콘텐츠 제작 필요'}</li>
                        </ul>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* 트렌드 분석 탭 */}
            {activeTab === 'trends' && analysis && (
              <div className="space-y-8">
                <h2 className="text-3xl font-bold mb-8">
                  '{keyword}' 12개월 트렌드 분석
                </h2>

                {analysis.analysis?.monthlyTrendData && Object.entries(analysis.analysis.monthlyTrendData).length > 0 && (
                  <div className="bg-slate-900/50 border border-emerald-500/20 rounded-xl p-6">
                    <p className="text-slate-400 mb-4">시간에 따른 검색량 변화 추이</p>
                    <div className="h-96 relative">
                      <div className="text-slate-400 text-center py-32">
                        📈 12개월 트렌드 차트 영역
                      </div>
                    </div>
                  </div>
                )}

                {analysis.analysis?.seasonalityAnalysis && (
                  <div className="grid md:grid-cols-2 gap-6">
                    <div className="bg-slate-900/50 border border-emerald-500/20 rounded-xl p-6">
                      <p className="text-emerald-400 font-semibold mb-4">📊 계절성 분석</p>
                      <div className="space-y-3 text-sm">
                        <div>
                          <span className="text-slate-400">피크 시즌</span>
                          <p className="text-white font-semibold">
                            {(Object.values(analysis.analysis.seasonalityAnalysis)[0] as any)?.peakMonths?.join(', ') || 'N/A'}
                          </p>
                        </div>
                        <div>
                          <span className="text-slate-400">저점 시즌</span>
                          <p className="text-white font-semibold">
                            {(Object.values(analysis.analysis.seasonalityAnalysis)[0] as any)?.lowMonths?.join(', ') || 'N/A'}
                          </p>
                        </div>
                      </div>
                    </div>
                    <div className="bg-slate-900/50 border border-emerald-500/20 rounded-xl p-6">
                      <p className="text-cyan-400 font-semibold mb-4">⏰ 포스팅 추천 시간</p>
                      <p className="text-white text-sm">
                        {(Object.values(analysis.analysis.seasonalityAnalysis)[0] as any)?.recommendedPostingTimes?.[0] ||
                         '피크 월 2개월 전부터 준비하기'}
                      </p>
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* 뉴스/블로그 탭 */}
            {activeTab === 'newsblog' && analysis && (
              <div className="space-y-8">
                <h2 className="text-3xl font-bold mb-8">
                  '{keyword}' 뉴스/블로그 발행량
                </h2>

                {analysis.analysis?.newsAndBlog && (
                  <div className="grid md:grid-cols-2 gap-6">
                    {Object.entries(analysis.analysis.newsAndBlog).map(([portal, data]: [string, any]) => (
                      <div key={portal} className="bg-slate-900/50 border border-emerald-500/20 rounded-xl p-6">
                        <h3 className="text-emerald-400 font-bold text-lg mb-4">{portal}</h3>
                        <div className="space-y-3 text-sm">
                          <div>
                            <span className="text-slate-400">30일 뉴스</span>
                            <p className="text-white font-bold text-lg">{data.newsCount30d || 0}건</p>
                          </div>
                          <div>
                            <span className="text-slate-400">30일 블로그</span>
                            <p className="text-white font-bold text-lg">{data.blogCount30d || 0}건</p>
                          </div>
                          <div className="pt-2 border-t border-slate-700">
                            <span className="text-slate-400">트렌드</span>
                            <p className="text-white font-semibold">
                              {data.trend === 'rising' && '📈 상승'} {data.trend === 'declining' && '📉 하락'} {data.trend === 'stable' && '→ 안정'}
                            </p>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}

            {/* 경쟁사 분석 탭 */}
            {activeTab === 'competitors' && analysis && (
              <div className="space-y-8">
                <h2 className="text-3xl font-bold mb-8">
                  '{keyword}' 경쟁사 분석
                </h2>

                {analysis.analysis?.competitors && (
                  <div className="grid md:grid-cols-2 gap-6">
                    {Object.entries(analysis.analysis.competitors).map(([portal, data]: [string, any]) => (
                      <div key={portal} className="bg-slate-900/50 border border-emerald-500/20 rounded-xl p-6">
                        <div className="flex justify-between items-center mb-4">
                          <h3 className="text-emerald-400 font-bold text-lg">{portal}</h3>
                          <TrustBadge score={85} />
                        </div>
                        <div className="space-y-4 text-sm">
                          <div>
                            <span className="text-slate-400">경쟁 강도</span>
                            <div className="flex items-center gap-2 mt-1">
                              <div className="flex-1 bg-slate-700 rounded-full h-2">
                                <div
                                  className="bg-emerald-500 h-2 rounded-full"
                                  style={{ width: `${data.competitionIntensity || 50}%` }}
                                />
                              </div>
                              <span className="text-white font-bold">{data.competitionIntensity || 50}%</span>
                            </div>
                          </div>
                          <div>
                            <span className="text-slate-400">경쟁사 수</span>
                            <p className="text-white font-bold">{data.summary?.totalCompetitors || 0}개</p>
                          </div>
                          <div>
                            <span className="text-slate-400">기회 키워드</span>
                            <p className="text-white font-bold">{data.summary?.opportunityCount || 0}개</p>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}

            {/* 추천 키워드 탭 */}
            {activeTab === 'recommendations' && recommendations.length > 0 && (
              <div className="space-y-8">
                <h2 className="text-3xl font-bold mb-8">
                  '{keyword}' 추천 키워드 ({recommendations.length}개)
                </h2>

                <div className="space-y-4">
                  {recommendations.slice(0, 10).map((rec: any, idx: number) => (
                    <div
                      key={idx}
                      className="bg-slate-900/50 border border-emerald-500/20 rounded-xl p-6 hover:border-emerald-500/60 transition"
                    >
                      <div className="flex justify-between items-start gap-4">
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-2">
                            <h3 className="font-bold text-lg text-white">{rec.keyword}</h3>
                            <span className="px-2 py-1 bg-emerald-500/20 text-emerald-400 rounded text-xs font-semibold">
                              {rec.type}
                            </span>
                          </div>
                          <div className="grid md:grid-cols-4 gap-4 text-sm">
                            <div>
                              <span className="text-slate-400">점수</span>
                              <p className="text-white font-bold">{rec.score}/100</p>
                            </div>
                            <div>
                              <span className="text-slate-400">검색량</span>
                              <p className="text-white font-bold">{rec.volume?.toLocaleString() || 'N/A'}</p>
                            </div>
                            <div>
                              <span className="text-slate-400">난이도</span>
                              <p className="text-white font-bold">{rec.difficulty || 'N/A'}</p>
                            </div>
                            <div>
                              <span className="text-slate-400">트렌드</span>
                              <p className="text-white font-bold">
                                {rec.trend === 'rising' && '📈'} {rec.trend === 'declining' && '📉'} {rec.trend}
                              </p>
                            </div>
                          </div>
                        </div>
                        <TrustBadge score={80} />
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </section>
        )}
      </main>
    </>
  )
}
