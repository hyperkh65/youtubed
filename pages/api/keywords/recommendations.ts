import type { NextApiRequest, NextApiResponse } from 'next'

interface RecommendationResponse {
  success: boolean
  keyword?: string
  recommendations?: any[]
  error?: string
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<RecommendationResponse>
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ success: false, error: 'Method not allowed' })
  }

  try {
    const { keywords, channelTopic } = req.body

    if (!keywords || !Array.isArray(keywords)) {
      return res.status(400).json({ success: false, error: 'Keywords array is required' })
    }

    // 🚀 Vercel 배포용 시뮬레이션 추천 데이터
    const recommendationTypes = ['related', 'trending', 'niche', 'low-competition']
    const recommendations: any[] = []

    keywords.forEach((keyword: string) => {
      // 각 키워드마다 4-6개의 추천 생성
      const recommendationCount = Math.floor(Math.random() * 3) + 4

      for (let i = 0; i < recommendationCount; i++) {
        const type = recommendationTypes[i % recommendationTypes.length]
        const suffix = ['tutorial', 'guide', 'tips', 'how to', 'best', 'vs', 'review', 'tools'][Math.floor(Math.random() * 8)]

        recommendations.push({
          original_keyword: keyword,
          keyword: `${keyword} ${suffix}`,
          type: type,
          score: (Math.random() * 40 + 60).toFixed(1),
          volume: Math.floor(Math.random() * 50000) + 1000,
          difficulty: Math.floor(Math.random() * 100),
          trend: ['rising', 'stable', 'declining'][Math.floor(Math.random() * 3)],
          monthly_searches: Math.floor(Math.random() * 200000) + 10000,
          cpc: (Math.random() * 4 + 0.5).toFixed(2),
          opportunity_score: (Math.random() * 100).toFixed(1)
        })
      }
    })

    res.status(200).json({
      success: true,
      recommendations: recommendations
    })
  } catch (error) {
    console.error('Recommendations error:', error)
    res.status(500).json({
      success: false,
      error: 'Internal server error'
    })
  }
}
