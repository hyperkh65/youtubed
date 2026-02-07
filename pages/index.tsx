import React, { useState } from 'react'
import Head from 'next/head'
import axios from 'axios'

export default function Home() {
  const [keyword, setKeyword] = useState('')
  const [analysis, setAnalysis] = useState<any>(null)
  const [loading, setLoading] = useState(false)
  const [recommendations, setRecommendations] = useState<any[]>([])

  const handleAnalyze = async () => {
    if (!keyword.trim()) {
      alert('Please enter a keyword')
      return
    }

    setLoading(true)
    try {
      const response = await axios.post('/api/keywords/analyze', { keyword })
      setAnalysis(response.data)
    } catch (error) {
      console.error('Analysis error:', error)
      alert('Error analyzing keyword')
    } finally {
      setLoading(false)
    }
  }

  const handleGetRecommendations = async () => {
    if (!keyword.trim()) {
      alert('Please enter a keyword')
      return
    }

    setLoading(true)
    try {
      const response = await axios.post('/api/keywords/recommendations', {
        keywords: [keyword]
      })
      setRecommendations(response.data.recommendations || [])
    } catch (error) {
      console.error('Recommendations error:', error)
      alert('Error getting recommendations')
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <Head>
        <title>YouTube Keyword Analyzer</title>
        <meta name="description" content="Advanced keyword analysis tool" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>

      <div className="container mx-auto px-4 py-8 max-w-6xl">
        {/* Header */}
        <div className="mb-12 text-center">
          <h1 className="text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-cyan-400 mb-4">
            🎯 YouTube Keyword Analyzer
          </h1>
          <p className="text-xl text-gray-300 mb-2">
            Multi-Portal Keyword Analysis Tool
          </p>
          <p className="text-sm text-gray-400">
            Analyze keywords across Google, Naver, Daum, and YouTube
          </p>
        </div>

        {/* Search Section */}
        <div className="bg-slate-800 rounded-lg p-8 mb-8 border border-slate-700">
          <div className="flex gap-3 mb-4">
            <input
              type="text"
              value={keyword}
              onChange={(e) => setKeyword(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleAnalyze()}
              placeholder="Enter keyword to analyze..."
              className="flex-1 px-4 py-3 bg-slate-700 text-white rounded border border-slate-600 focus:outline-none focus:border-blue-500"
            />
            <button
              onClick={handleAnalyze}
              disabled={loading}
              className="px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white rounded font-semibold transition"
            >
              {loading ? 'Analyzing...' : 'Analyze'}
            </button>
            <button
              onClick={handleGetRecommendations}
              disabled={loading}
              className="px-6 py-3 bg-green-600 hover:bg-green-700 disabled:bg-gray-600 text-white rounded font-semibold transition"
            >
              {loading ? 'Loading...' : 'Recommendations'}
            </button>
          </div>
        </div>

        {/* Analysis Results */}
        {analysis && (
          <div className="bg-slate-800 rounded-lg p-8 mb-8 border border-slate-700">
            <h2 className="text-2xl font-bold text-white mb-6">📊 Analysis Results</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {Object.entries(analysis.analysis?.portals || {}).map(([portal, data]: [string, any]) => (
                <div
                  key={portal}
                  className="bg-slate-700 rounded p-4 border border-slate-600 hover:border-blue-500 transition"
                >
                  <h3 className="font-bold text-lg text-blue-400 mb-3">{portal}</h3>
                  <div className="space-y-2 text-sm text-gray-300">
                    <div>
                      <span className="text-gray-400">Search Volume:</span>
                      <p className="font-semibold text-white">
                        {data.estimated_search_volume?.toLocaleString() || data.monthly_searches?.toLocaleString() || 'N/A'}
                      </p>
                    </div>
                    <div>
                      <span className="text-gray-400">Trend:</span>
                      <p className="font-semibold text-white capitalize">
                        {data.trend || 'N/A'}
                      </p>
                    </div>
                    <div>
                      <span className="text-gray-400">Difficulty:</span>
                      <p className="font-semibold text-white">
                        {data.keyword_difficulty_score || data.difficulty || 'N/A'}
                      </p>
                    </div>
                    {data.cpc && (
                      <div>
                        <span className="text-gray-400">CPC:</span>
                        <p className="font-semibold text-white">${data.cpc}</p>
                      </div>
                    )}
                    {data.opportunity_score && (
                      <div>
                        <span className="text-gray-400">Opportunity:</span>
                        <p className="font-semibold text-white">{data.opportunity_score}</p>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Recommendations */}
        {recommendations.length > 0 && (
          <div className="bg-slate-800 rounded-lg p-8 border border-slate-700">
            <h2 className="text-2xl font-bold text-white mb-6">💡 Keyword Recommendations</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {recommendations.map((rec, idx) => (
                <div
                  key={idx}
                  className="bg-slate-700 rounded p-4 border border-slate-600 hover:border-green-500 transition"
                >
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="font-bold text-green-400">{rec.keyword}</h3>
                    <span className="text-xs bg-blue-600 text-white px-2 py-1 rounded capitalize">
                      {rec.type}
                    </span>
                  </div>
                  <div className="text-sm text-gray-300 space-y-1">
                    <p>Score: <span className="text-white font-semibold">{rec.score}</span></p>
                    <p>Volume: <span className="text-white font-semibold">{rec.volume?.toLocaleString()}</span></p>
                    <p>Difficulty: <span className="text-white font-semibold">{rec.difficulty}</span></p>
                    <p>Trend: <span className="text-white font-semibold capitalize">{rec.trend}</span></p>
                    {rec.opportunity_score && (
                      <p>Opportunity: <span className="text-white font-semibold">{rec.opportunity_score}</span></p>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Info */}
        {!analysis && !recommendations.length && (
          <div className="bg-slate-800 rounded-lg p-8 text-center border border-slate-700">
            <p className="text-gray-400 mb-4">
              Enter a keyword above to analyze it across multiple search portals
            </p>
            <div className="grid grid-cols-4 gap-4 mt-8">
              <div>
                <div className="text-3xl mb-2">🔍</div>
                <p className="text-sm text-gray-300">Google Analysis</p>
              </div>
              <div>
                <div className="text-3xl mb-2">📊</div>
                <p className="text-sm text-gray-300">Naver Search</p>
              </div>
              <div>
                <div className="text-3xl mb-2">🎯</div>
                <p className="text-sm text-gray-300">Daum Trends</p>
              </div>
              <div>
                <div className="text-3xl mb-2">📹</div>
                <p className="text-sm text-gray-300">YouTube Video</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </>
  )
}
