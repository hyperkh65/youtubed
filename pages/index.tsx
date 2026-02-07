import React, { useState, useEffect } from 'react'
import Head from 'next/head'
import axios from 'axios'
import dynamic from 'next/dynamic'

const Plot = dynamic(() => import('react-plotly.js'), { ssr: false })

const TRENDING_KEYWORDS = [
  { keyword: '유튜브 SEO', trend: 'rising', volume: 45000 },
  { keyword: '콘텐츠 마케팅', trend: 'rising', volume: 38000 },
  { keyword: '숏폼 영상', trend: 'hot', volume: 72000 },
  { keyword: '키워드 분석', trend: 'rising', volume: 28000 },
  { keyword: '유튜브 알고리즘', trend: 'stable', volume: 55000 },
  { keyword: '채널 성장', trend: 'rising', volume: 34000 },
]

const PORTALS = ['Naver', 'Google', 'Daum', 'YouTube']

export default function Home() {
  const [keyword, setKeyword] = useState('')
  const [selectedPortal, setSelectedPortal] = useState('Naver')
  const [analysis, setAnalysis] = useState<any>(null)
  const [recommendations, setRecommendations] = useState<any[]>([])
  const [loading, setLoading] = useState(false)
  const [activeTab, setActiveTab] = useState('analysis')

  const handleAnalyze = async () => {
    if (!keyword.trim()) {
      alert('키워드를 입력해주세요')
      return
    }

    setLoading(true)
    try {
      const response = await axios.post('/api/keywords/analyze', {
        keyword,
        portal: selectedPortal
      })
      setAnalysis(response.data)
      setActiveTab('analysis')
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
        portal: selectedPortal
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

  return (
    <>
      <Head>
        <title>KeyPoints - YouTube Keyword Analyzer</title>
        <meta name="description" content="유튜브 마케팅을 위한 가장 강력한 키워드 분석 도구" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>

      <main className="min-h-screen bg-black text-white">
        {/* 히어로 섹션 */}
        <section className="relative min-h-[600px] bg-gradient-to-b from-black via-emerald-950/10 to-black px-4 py-20">
          <div className="max-w-5xl mx-auto">
            {/* 헤드라인 */}
            <div className="text-center mb-12">
              <h1 className="text-5xl md:text-6xl font-bold mb-4 leading-tight">
                유튜브 마케팅을 위한<br />
                <span className="bg-gradient-to-r from-emerald-400 to-cyan-400 bg-clip-text text-transparent">
                  가장 강력한 키워드 분석 도구
                </span>
              </h1>
              <p className="text-lg text-slate-400 mb-8">
                Naver, Google, Daum, YouTube 전 포털 동시 분석<br />
                정확한 데이터 기반 마케팅 전략 수립
              </p>
            </div>

            {/* 검색 바 */}
            <div className="bg-slate-900/50 border border-emerald-500/20 rounded-xl p-8 mb-12 backdrop-blur">
              {/* 포털 선택 */}
              <div className="flex flex-col md:flex-row gap-4 mb-6">
                <div className="flex-1">
                  <label className="block text-sm text-slate-400 mb-2">포털 선택</label>
                  <select
                    value={selectedPortal}
                    onChange={(e) => setSelectedPortal(e.target.value)}
                    className="w-full bg-slate-800 border border-emerald-500/30 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-emerald-500 transition"
                  >
                    {PORTALS.map((portal) => (
                      <option key={portal} value={portal}>
                        {portal}
                      </option>
                    ))}
                  </select>
                </div>
                <div className="flex-[3]">
                  <label className="block text-sm text-slate-400 mb-2">키워드 입력</label>
                  <input
                    type="text"
                    value={keyword}
                    onChange={(e) => setKeyword(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleAnalyze()}
                    placeholder="분석할 키워드를 입력하세요..."
                    className="w-full bg-slate-800 border border-emerald-500/30 rounded-lg px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500 transition"
                  />
                </div>
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
              <p className="text-sm text-slate-500 mb-4">🔥 지금 핫한 키워드</p>
              <div className="flex flex-wrap justify-center gap-3">
                {TRENDING_KEYWORDS.map((item) => (
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
          <section className="max-w-5xl mx-auto px-4 py-12">
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
                  onClick={() => setActiveTab('trends')}
                  className={`pb-4 px-2 font-semibold transition whitespace-nowrap ${
                    activeTab === 'trends'
                      ? 'text-emerald-400 border-b-2 border-emerald-400'
                      : 'text-slate-400 hover:text-slate-200'
                  }`}
                >
                  📈 트렌드 분석
                </button>
                <button
                  onClick={() => setActiveTab('newsblog')}
                  className={`pb-4 px-2 font-semibold transition whitespace-nowrap ${
                    activeTab === 'newsblog'
                      ? 'text-emerald-400 border-b-2 border-emerald-400'
                      : 'text-slate-400 hover:text-slate-200'
                  }`}
                >
                  📰 뉴스/블로그
                </button>
                <button
                  onClick={() => setActiveTab('competitors')}
                  className={`pb-4 px-2 font-semibold transition whitespace-nowrap ${
                    activeTab === 'competitors'
                      ? 'text-emerald-400 border-b-2 border-emerald-400'
                      : 'text-slate-400 hover:text-slate-200'
                  }`}
                >
                  🏆 경쟁사 분석
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
                <h2 className="text-3xl font-bold mb-8">
                  '{keyword}' 분석 결과
                </h2>

                {/* 포털별 결과 */}
                <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
                  {Object.entries(analysis.analysis?.portals || {}).map(([portal, data]: [string, any]) => (
                    <div
                      key={portal}
                      className="bg-slate-900/50 border border-emerald-500/20 rounded-xl p-6 hover:border-emerald-500/60 transition"
                    >
                      <h3 className="text-emerald-400 font-bold text-lg mb-4">{portal}</h3>
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

            {/* 트렌드 분석 탭 */}
            {activeTab === 'trends' && analysis && (
              <div className="space-y-8">
                <h2 className="text-3xl font-bold mb-8">
                  '{keyword}' 12개월 트렌드 분석
                </h2>

                {/* 포털별 트렌드 분석 */}
                {Object.entries(analysis.analysis?.monthlyTrendData || {}).map(([portal, monthlyData]: [string, any]) => {
                  const seasonality = analysis.analysis?.seasonalityAnalysis?.[portal]

                  // 월별 검색량 차트 데이터
                  const monthlyChartData = {
                    x: monthlyData.map((d: any) => d.date),
                    y: monthlyData.map((d: any) => d.searches),
                    type: 'scatter',
                    mode: 'lines+markers',
                    name: '검색량',
                    line: { color: '#10b981', width: 3 },
                    marker: { size: 6 }
                  }

                  // 계절성 지수 차트
                  const seasonalityChartData = {
                    x: monthlyData.map((d: any) => d.date),
                    y: monthlyData.map((d: any) => d.seasonalityIndex),
                    type: 'bar',
                    name: '계절성 지수',
                    marker: {
                      color: monthlyData.map((d: any) =>
                        d.seasonalityIndex > 110
                          ? '#06b6d4'
                          : d.seasonalityIndex < 90
                          ? '#ef4444'
                          : '#6b7280'
                      )
                    }
                  }

                  return (
                    <div key={portal} className="space-y-6">
                      <div className="bg-slate-900/50 border border-emerald-500/20 rounded-xl p-6">
                        <h3 className="text-emerald-400 font-bold text-lg mb-6">{portal} - 월별 검색량 트렌드</h3>
                        <div className="bg-slate-800/50 rounded-lg p-4 mb-6 overflow-x-auto">
                          <svg viewBox="0 0 800 300" className="w-full" style={{ minHeight: '300px' }}>
                            {/* 간단한 라인 차트 대체 */}
                            <text x="10" y="30" fill="#94a3b8" fontSize="14">
                              📈 12개월 트렌드: {seasonality?.averageSearches.toLocaleString()} 평균 검색량
                            </text>
                            <text x="10" y="60" fill="#10b981" fontSize="14" fontWeight="bold">
                              🔝 피크: {seasonality?.peakValue.toLocaleString()} ({seasonality?.peakMonths.join(', ')})
                            </text>
                            <text x="10" y="90" fill="#ef4444" fontSize="14" fontWeight="bold">
                              📉 최저: {seasonality?.lowestValue.toLocaleString()} ({seasonality?.lowMonths.join(', ')})
                            </text>
                            <text x="10" y="120" fill="#94a3b8" fontSize="14">
                              변동성 (표준편차): {seasonality?.volatility}
                            </text>
                          </svg>
                        </div>

                        {/* 계절성 분석 카드 */}
                        <div className="grid md:grid-cols-3 gap-4">
                          <div className="bg-slate-800/50 rounded-lg p-4">
                            <h4 className="text-emerald-400 font-semibold mb-3">📈 피크 시즌</h4>
                            <div className="space-y-2">
                              {seasonality?.peakMonths.map((month: string) => (
                                <div key={month} className="text-white text-sm font-semibold">
                                  {month}
                                </div>
                              ))}
                            </div>
                          </div>

                          <div className="bg-slate-800/50 rounded-lg p-4">
                            <h4 className="text-cyan-400 font-semibold mb-3">📉 저점 시즌</h4>
                            <div className="space-y-2">
                              {seasonality?.lowMonths.map((month: string) => (
                                <div key={month} className="text-white text-sm font-semibold">
                                  {month}
                                </div>
                              ))}
                            </div>
                          </div>

                          <div className="bg-slate-800/50 rounded-lg p-4">
                            <h4 className="text-emerald-300 font-semibold mb-3">⏰ 추천 포스팅 시기</h4>
                            <div className="space-y-2">
                              {seasonality?.recommendedPostingTimes.map((time: string) => (
                                <div key={time} className="text-white text-sm font-semibold">
                                  {time}
                                </div>
                              ))}
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  )
                })}
              </div>
            )}

            {/* 뉴스/블로그 탭 */}
            {activeTab === 'newsblog' && analysis && (
              <div className="space-y-8">
                <h2 className="text-3xl font-bold mb-8">
                  '{keyword}' 뉴스 & 블로그 분석
                </h2>

                {/* 포털별 뉴스/블로그 데이터 */}
                <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
                  {Object.entries(analysis.analysis?.newsAndBlog || {}).map(([portal, data]: [string, any]) => (
                    <div key={portal} className="bg-slate-900/50 border border-emerald-500/20 rounded-xl p-6">
                      <h3 className="text-emerald-400 font-bold text-lg mb-6 border-b border-slate-700 pb-4">
                        {portal}
                      </h3>

                      {/* 뉴스 섹션 */}
                      <div className="mb-6">
                        <div className="flex items-center justify-between mb-3">
                          <span className="text-slate-400 font-semibold">📰 뉴스</span>
                          <span
                            className={`text-sm px-2 py-1 rounded-full ${
                              data.newsTrend === 'rising'
                                ? 'bg-emerald-500/20 text-emerald-300'
                                : data.newsTrend === 'declining'
                                ? 'bg-red-500/20 text-red-300'
                                : 'bg-slate-500/20 text-slate-300'
                            }`}
                          >
                            {data.newsTrend === 'rising' ? '📈' : data.newsTrend === 'declining' ? '📉' : '→'}
                          </span>
                        </div>
                        <p className="text-white font-bold text-2xl mb-2">{data.newsCount30d}</p>
                        <p className="text-slate-400 text-sm">
                          일일 {data.newsVelocity}개 / 30일 기준
                        </p>
                      </div>

                      {/* 블로그 섹션 */}
                      <div className="pt-6 border-t border-slate-700">
                        <div className="flex items-center justify-between mb-3">
                          <span className="text-slate-400 font-semibold">📝 블로그</span>
                          <span
                            className={`text-sm px-2 py-1 rounded-full ${
                              data.blogTrend === 'rising'
                                ? 'bg-emerald-500/20 text-emerald-300'
                                : data.blogTrend === 'declining'
                                ? 'bg-red-500/20 text-red-300'
                                : 'bg-slate-500/20 text-slate-300'
                            }`}
                          >
                            {data.blogTrend === 'rising' ? '📈' : data.blogTrend === 'declining' ? '📉' : '→'}
                          </span>
                        </div>
                        <p className="text-white font-bold text-2xl mb-2">{data.blogCount30d}</p>
                        <p className="text-slate-400 text-sm">
                          일일 {data.blogVelocity}개 / 30일 기준
                        </p>
                      </div>

                      {/* 활동 점수 */}
                      {data.score !== undefined && (
                        <div className="pt-6 border-t border-slate-700">
                          <span className="text-slate-400 text-sm">활동 점수</span>
                          <p className="text-cyan-400 font-bold text-xl mt-1">{data.score.toFixed(1)}/10</p>
                        </div>
                      )}
                    </div>
                  ))}
                </div>

                {/* 트렌딩 뉴스 및 상위 블로그 */}
                <div className="grid md:grid-cols-2 gap-6">
                  {/* 트렌딩 뉴스 */}
                  {Object.entries(analysis.analysis?.newsAndBlog || {}).map(([portal, data]: [string, any]) =>
                    data.trendingNews && data.trendingNews.length > 0 ? (
                      <div key={`${portal}-news`} className="bg-slate-900/50 border border-emerald-500/20 rounded-xl p-6">
                        <h4 className="text-emerald-400 font-bold mb-4">🔥 {portal} 트렌딩 뉴스</h4>
                        <div className="space-y-3">
                          {data.trendingNews.map((news: any, idx: number) => (
                            <div key={idx} className="pb-3 border-b border-slate-700 last:border-0">
                              <p className="text-white text-sm font-semibold mb-1">{news.title}</p>
                              <p className="text-slate-400 text-xs">{news.date}</p>
                            </div>
                          ))}
                        </div>
                      </div>
                    ) : null
                  )}

                  {/* 상위 블로그 */}
                  {Object.entries(analysis.analysis?.newsAndBlog || {}).map(([portal, data]: [string, any]) =>
                    data.topBlogs && data.topBlogs.length > 0 ? (
                      <div key={`${portal}-blogs`} className="bg-slate-900/50 border border-emerald-500/20 rounded-xl p-6">
                        <h4 className="text-emerald-400 font-bold mb-4">⭐ {portal} 상위 블로그</h4>
                        <div className="space-y-3">
                          {data.topBlogs.map((blog: any, idx: number) => (
                            <div key={idx} className="pb-3 border-b border-slate-700 last:border-0">
                              <div className="flex justify-between items-center">
                                <p className="text-white text-sm font-semibold">{blog.blog}</p>
                                <span className="text-emerald-400 text-xs font-bold">{blog.posts}개</span>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    ) : null
                  )}
                </div>
              </div>
            )}

            {/* 경쟁사 분석 탭 */}
            {activeTab === 'competitors' && analysis && (
              <div className="space-y-8">
                <h2 className="text-3xl font-bold mb-8">
                  '{keyword}' 경쟁사 분석
                </h2>

                {/* 포털별 경쟁 요약 */}
                <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
                  {Object.entries(analysis.analysis?.competitors || {}).map(([portal, data]: [string, any]) => (
                    <div key={portal} className="bg-slate-900/50 border border-emerald-500/20 rounded-xl p-6">
                      <h3 className="text-emerald-400 font-bold text-lg mb-6 border-b border-slate-700 pb-4">
                        {portal}
                      </h3>

                      {/* 경쟁 강도 */}
                      <div className="mb-4">
                        <span className="text-slate-400 text-sm">경쟁 강도</span>
                        <div className="flex items-center gap-2 mt-1">
                          <div className="flex-1 bg-slate-700 rounded-full h-2">
                            <div
                              className={`h-2 rounded-full ${
                                data.competitionIntensity > 70
                                  ? 'bg-red-500'
                                  : data.competitionIntensity > 40
                                  ? 'bg-yellow-500'
                                  : 'bg-emerald-500'
                              }`}
                              style={{ width: `${Math.min(data.competitionIntensity, 100)}%` }}
                            />
                          </div>
                          <span className="text-white font-bold text-sm">
                            {data.competitionIntensity}%
                          </span>
                        </div>
                      </div>

                      {/* 요약 통계 */}
                      <div className="space-y-2 text-sm pt-4 border-t border-slate-700">
                        <div className="flex justify-between">
                          <span className="text-slate-400">경쟁사 수</span>
                          <span className="text-white font-bold">{data.summary?.totalCompetitors}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-400">평균 강도</span>
                          <span className="text-cyan-400 font-bold">{data.summary?.averageCompetitorStrength}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-400">기회 키워드</span>
                          <span className="text-emerald-400 font-bold">{data.summary?.opportunityCount}</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>

                {/* 상세 경쟁사 분석 */}
                <div className="space-y-6">
                  {Object.entries(analysis.analysis?.competitors || {}).map(([portal, data]: [string, any]) => (
                    <div key={`${portal}-detail`} className="space-y-6">
                      <h3 className="text-2xl font-bold text-emerald-400 mt-8 mb-6">{portal} 경쟁사 상세 분석</h3>

                      {data.list?.map((competitor: any, idx: number) => (
                        <div key={idx} className="bg-slate-900/50 border border-emerald-500/20 rounded-xl p-6">
                          <div className="flex justify-between items-start mb-6">
                            <h4 className="text-lg font-bold">{competitor.name}</h4>
                            <div className="flex items-center gap-2">
                              <span className="text-slate-400 text-sm">강도</span>
                              <span className="bg-emerald-500/20 text-emerald-300 px-3 py-1 rounded-full font-bold">
                                {competitor.competitorStrength}
                              </span>
                            </div>
                          </div>

                          {/* 경쟁사 주요 키워드 */}
                          <div className="mb-6">
                            <h5 className="text-emerald-400 font-semibold mb-3">🎯 주요 키워드 (Top 5)</h5>
                            <div className="space-y-2">
                              {competitor.dominantKeywords?.map((kw: any, kidx: number) => (
                                <div key={kidx} className="flex justify-between items-center bg-slate-800/50 px-3 py-2 rounded">
                                  <span className="text-white text-sm">{kw.keyword}</span>
                                  <div className="flex gap-2">
                                    <span className="text-cyan-400 text-xs">난이도: {kw.difficulty}</span>
                                    <span className="text-emerald-400 text-xs font-bold">{kw.score.toFixed(0)}점</span>
                                  </div>
                                </div>
                              ))}
                            </div>
                          </div>

                          {/* 기회 키워드 */}
                          {competitor.opportunityKeywords?.length > 0 && (
                            <div>
                              <h5 className="text-cyan-400 font-semibold mb-3">💡 기회 키워드</h5>
                              <div className="space-y-2">
                                {competitor.opportunityKeywords?.map((kw: any, kidx: number) => (
                                  <div key={kidx} className="flex justify-between items-center bg-cyan-500/10 px-3 py-2 rounded border border-cyan-500/30">
                                    <span className="text-white text-sm">{kw.keyword}</span>
                                    <span className="text-cyan-400 text-xs font-bold">{kw.searchVolume?.toLocaleString()}</span>
                                  </div>
                                ))}
                              </div>
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* 추천 키워드 탭 */}
            {activeTab === 'recommendations' && recommendations.length > 0 && (
              <div className="space-y-8">
                <h2 className="text-3xl font-bold mb-8">
                  '{keyword}' 연관 키워드 추천
                </h2>

                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {recommendations.map((rec, idx) => (
                    <div
                      key={idx}
                      className="bg-slate-900/50 border border-emerald-500/20 rounded-xl p-6 hover:border-emerald-500/60 transition"
                    >
                      <div className="flex justify-between items-start mb-4">
                        <h3 className="text-emerald-400 font-bold flex-1">{rec.keyword}</h3>
                        <span className="text-xs bg-emerald-500/20 text-emerald-300 px-3 py-1 rounded-full capitalize">
                          {rec.type}
                        </span>
                      </div>

                      <div className="space-y-3 text-sm">
                        <div className="grid grid-cols-2 gap-4">
                          <div>
                            <span className="text-slate-400">점수</span>
                            <p className="text-emerald-400 font-bold text-lg">{rec.score}</p>
                          </div>
                          <div>
                            <span className="text-slate-400">검색량</span>
                            <p className="text-white font-bold">{rec.volume?.toLocaleString()}</p>
                          </div>
                        </div>
                        <div className="grid grid-cols-2 gap-4 pt-2 border-t border-slate-700">
                          <div>
                            <span className="text-slate-400">난이도</span>
                            <p className="text-white font-bold">{rec.difficulty}</p>
                          </div>
                          <div>
                            <span className="text-slate-400">트렌드</span>
                            <p className="text-white font-bold capitalize">
                              {rec.trend === 'rising' && '📈'}
                              {rec.trend === 'stable' && '→'}
                              {rec.trend === 'declining' && '📉'}
                            </p>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </section>
        )}

        {/* 초기 상태 - 정보 섹션 */}
        {!analysis && recommendations.length === 0 && (
          <section className="max-w-5xl mx-auto px-4 py-20">
            <div className="grid md:grid-cols-4 gap-8">
              <div className="text-center">
                <div className="text-5xl mb-4">🔍</div>
                <h3 className="text-lg font-bold mb-2">다중 포털 분석</h3>
                <p className="text-slate-400 text-sm">Naver, Google, Daum, YouTube 동시 분석</p>
              </div>
              <div className="text-center">
                <div className="text-5xl mb-4">📊</div>
                <h3 className="text-lg font-bold mb-2">상세 데이터</h3>
                <p className="text-slate-400 text-sm">검색량, 난이도, 트렌드 등 정확한 정보</p>
              </div>
              <div className="text-center">
                <div className="text-5xl mb-4">💡</div>
                <h3 className="text-lg font-bold mb-2">키워드 추천</h3>
                <p className="text-slate-400 text-sm">AI 기반 연관 키워드 추천</p>
              </div>
              <div className="text-center">
                <div className="text-5xl mb-4">⚡</div>
                <h3 className="text-lg font-bold mb-2">실시간 분석</h3>
                <p className="text-slate-400 text-sm">즉시 결과 확인 및 활용</p>
              </div>
            </div>
          </section>
        )}

        {/* 푸터 */}
        <footer className="border-t border-slate-800 mt-20">
          <div className="max-w-5xl mx-auto px-4 py-12">
            <div className="grid md:grid-cols-4 gap-8 mb-8">
              <div>
                <h4 className="font-bold mb-4 text-emerald-400">KeyPoints</h4>
                <p className="text-slate-400 text-sm">유튜브 마케팅 성공의 첫 걸음</p>
              </div>
              <div>
                <h4 className="font-bold mb-4">제품</h4>
                <ul className="space-y-2 text-slate-400 text-sm">
                  <li><a href="#" className="hover:text-emerald-400 transition">분석</a></li>
                  <li><a href="#" className="hover:text-emerald-400 transition">추천</a></li>
                  <li><a href="#" className="hover:text-emerald-400 transition">비교</a></li>
                </ul>
              </div>
              <div>
                <h4 className="font-bold mb-4">회사</h4>
                <ul className="space-y-2 text-slate-400 text-sm">
                  <li><a href="#" className="hover:text-emerald-400 transition">소개</a></li>
                  <li><a href="#" className="hover:text-emerald-400 transition">블로그</a></li>
                  <li><a href="#" className="hover:text-emerald-400 transition">문의</a></li>
                </ul>
              </div>
              <div>
                <h4 className="font-bold mb-4">법률</h4>
                <ul className="space-y-2 text-slate-400 text-sm">
                  <li><a href="#" className="hover:text-emerald-400 transition">이용약관</a></li>
                  <li><a href="#" className="hover:text-emerald-400 transition">개인정보</a></li>
                </ul>
              </div>
            </div>
            <div className="border-t border-slate-800 pt-8 text-center text-slate-500 text-sm">
              <p>&copy; 2024 KeyPoints. All rights reserved.</p>
            </div>
          </div>
        </footer>
      </main>
    </>
  )
}
