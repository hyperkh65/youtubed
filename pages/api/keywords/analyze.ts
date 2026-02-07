import type { NextApiRequest, NextApiResponse } from 'next'

interface AnalysisResponse {
  success: boolean
  keyword: string
  analysis?: any
  error?: string
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<AnalysisResponse>
) {
  if (req.method !== 'POST') {
    return res.status(405).json({
      success: false,
      keyword: '',
      error: 'Method not allowed'
    })
  }

  try {
    const { keyword } = req.body

    if (!keyword || typeof keyword !== 'string') {
      return res.status(400).json({
        success: false,
        keyword: '',
        error: 'Keyword is required'
      })
    }

    // 🚀 Vercel 배포용 시뮬레이션 데이터
    const analysis = {
      keyword: keyword,
      timestamp: new Date().toISOString(),
      portals: {
        Google: {
          portal: 'Google',
          keyword: keyword,
          status: 'available',
          estimated_search_volume: Math.floor(Math.random() * 5000) + 500,
          competition_level: ['Low', 'Medium', 'High'][Math.floor(Math.random() * 3)],
          trend: ['rising', 'stable', 'declining'][Math.floor(Math.random() * 3)],
          related_keywords: [`${keyword} tutorial`, `best ${keyword}`, `${keyword} guide`],
          search_intent: 'informational',
          monthly_searches: Math.floor(Math.random() * 150000) + 15000,
          cpc: (Math.random() * 3 + 0.5).toFixed(2),
          keyword_difficulty_score: Math.floor(Math.random() * 100),
          opportunity_score: (Math.random() * 100).toFixed(1)
        },
        Naver: {
          portal: 'Naver',
          keyword: keyword,
          status: 'available',
          estimated_search_volume: Math.floor(Math.random() * 4000) + 400,
          related_keywords: [`${keyword} 가이드`, `${keyword} 방법`],
          trend: ['rising', 'stable', 'declining'][Math.floor(Math.random() * 3)],
          monthly_search: Math.floor(Math.random() * 120000) + 12000,
          cpc: (Math.random() * 2.5 + 0.8).toFixed(2),
          difficulty: ['Easy', 'Medium', 'Hard'][Math.floor(Math.random() * 3)]
        },
        Daum: {
          portal: 'Daum',
          keyword: keyword,
          status: 'available',
          estimated_search_volume: Math.floor(Math.random() * 3000) + 300,
          related_keywords: [`${keyword} 정보`, `${keyword} 뜻`],
          trend: ['rising', 'stable', 'declining'][Math.floor(Math.random() * 3)],
          monthly_searches: Math.floor(Math.random() * 90000) + 9000,
          difficulty: ['Easy', 'Medium', 'Hard'][Math.floor(Math.random() * 3)]
        },
        YouTube: {
          portal: 'YouTube',
          keyword: keyword,
          status: 'available',
          estimated_search_volume: Math.floor(Math.random() * 6000) + 600,
          video_count_estimate: Math.floor(Math.random() * 1000000) + 100000,
          trend: ['rising', 'stable', 'declining'][Math.floor(Math.random() * 3)],
          recommendations: [
            `${keyword} tutorial`,
            `${keyword} for beginners`,
            `${keyword} 2025`,
            `best ${keyword}`,
            `${keyword} tips`
          ]
        }
      }
    }

    res.status(200).json({
      success: true,
      keyword: keyword,
      analysis: analysis
    })
  } catch (error) {
    console.error('Analysis error:', error)
    res.status(500).json({
      success: false,
      keyword: '',
      error: 'Internal server error'
    })
  }
}
