import type { NextApiRequest, NextApiResponse } from 'next'
import {
  classifyKeywordType,
  calculateKeywordMetrics,
  generateRelatedKeywords,
  calculateKeywordScore,
  calculateRecommendationScore,
  generateNewsAndBlogData,
  generateTrendData,
  calculateNewsAndBlogScore,
  generate12MonthTrendData,
  analyzeSeasonality,
  type NewsAndBlogData,
  type TrendDataPoint,
  type MonthlyTrendData,
  type SeasonalityAnalysis
} from '@/lib/keyword-analyzer'

interface AnalysisResponse {
  success: boolean
  keyword: string
  analysis?: any
  error?: string
}

const KEYWORD_DATABASE: Record<string, Record<string, any>> = {
  'python': {
    Naver: { estimated_search_volume: 185000, monthly_searches: 185000, competition_level: 'High', trend: 'rising', keyword_difficulty_score: 78, cpc: '2.50', opportunity_score: '42.3', related_keywords: ['파이썬', '파이썬 강좌', '파이썬 기초', '파이썬 자료구조', '파이썬 라이브러리'], search_intent: 'educational' },
    Google: { estimated_search_volume: 2500000, monthly_searches: 2500000, competition_level: 'High', trend: 'stable', keyword_difficulty_score: 85, cpc: '3.20', opportunity_score: '35.7', related_keywords: ['Python tutorial', 'Python programming', 'Python for beginners', 'Python download'], search_intent: 'educational' },
    Daum: { estimated_search_volume: 12000, monthly_searches: 12000, competition_level: 'Medium', trend: 'stable', keyword_difficulty_score: 45, cpc: '0.80', opportunity_score: '62.1', related_keywords: ['파이썬', '코딩', '프로그래밍'], search_intent: 'informational' },
    YouTube: { estimated_search_volume: 450000, monthly_searches: 450000, competition_level: 'High', trend: 'rising', keyword_difficulty_score: 72, cpc: '1.50', opportunity_score: '48.2', related_keywords: ['Python tutorial', 'Python course', 'Learn python', 'Python project'], search_intent: 'educational' }
  },
  'youtube': {
    Naver: { estimated_search_volume: 156000, monthly_searches: 156000, competition_level: 'Medium', trend: 'rising', keyword_difficulty_score: 65, cpc: '1.80', opportunity_score: '55.4', related_keywords: ['유튜브', '유튜브 채널', '유튜브 마케팅', '유튜브 수익', '유튜브 구독자'], search_intent: 'informational' },
    Google: { estimated_search_volume: 5200000, monthly_searches: 5200000, competition_level: 'High', trend: 'stable', keyword_difficulty_score: 88, cpc: '4.10', opportunity_score: '31.2', related_keywords: ['YouTube channel', 'YouTube video', 'YouTube tips', 'YouTube SEO'], search_intent: 'navigational' },
    Daum: { estimated_search_volume: 8500, monthly_searches: 8500, competition_level: 'Low', trend: 'rising', keyword_difficulty_score: 32, cpc: '0.60', opportunity_score: '72.8', related_keywords: ['유튜브', '동영상', '채널'], search_intent: 'navigational' },
    YouTube: { estimated_search_volume: 2800000, monthly_searches: 2800000, competition_level: 'High', trend: 'rising', keyword_difficulty_score: 82, cpc: '2.20', opportunity_score: '45.6', related_keywords: ['YouTube channel ideas', 'YouTube monetization', 'YouTube growth'], search_intent: 'educational' }
  },
  'seo': {
    Naver: { estimated_search_volume: 142000, monthly_searches: 142000, competition_level: 'High', trend: 'stable', keyword_difficulty_score: 81, cpc: '3.50', opportunity_score: '38.9', related_keywords: ['검색엔진최적화', 'SEO 기초', 'SEO 전략', 'SEO 도구', 'SEO 마케팅'], search_intent: 'educational' },
    Google: { estimated_search_volume: 6800000, monthly_searches: 6800000, competition_level: 'High', trend: 'stable', keyword_difficulty_score: 91, cpc: '5.80', opportunity_score: '22.4', related_keywords: ['SEO tips', 'SEO tools', 'SEO strategies', 'SEO ranking'], search_intent: 'educational' },
    Daum: { estimated_search_volume: 5200, monthly_searches: 5200, competition_level: 'Medium', trend: 'declining', keyword_difficulty_score: 55, cpc: '1.20', opportunity_score: '48.3', related_keywords: ['검색', '웹마케팅'], search_intent: 'educational' },
    YouTube: { estimated_search_volume: 580000, monthly_searches: 580000, competition_level: 'High', trend: 'rising', keyword_difficulty_score: 75, cpc: '2.90', opportunity_score: '51.2', related_keywords: ['SEO tutorial', 'SEO for beginners', 'White hat SEO'], search_intent: 'educational' }
  },
  'marketing': {
    Naver: { estimated_search_volume: 198000, monthly_searches: 198000, competition_level: 'High', trend: 'rising', keyword_difficulty_score: 76, cpc: '2.70', opportunity_score: '46.1', related_keywords: ['마케팅 전략', '디지털 마케팅', '콘텐츠 마케팅', '소셜 미디어 마케팅', '마케팅 팁'], search_intent: 'educational' },
    Google: { estimated_search_volume: 9200000, monthly_searches: 9200000, competition_level: 'High', trend: 'rising', keyword_difficulty_score: 89, cpc: '4.50', opportunity_score: '33.8', related_keywords: ['Marketing strategy', 'Digital marketing', 'Content marketing', 'Marketing tips'], search_intent: 'educational' },
    Daum: { estimated_search_volume: 9800, monthly_searches: 9800, competition_level: 'Medium', trend: 'rising', keyword_difficulty_score: 52, cpc: '0.95', opportunity_score: '58.6', related_keywords: ['마케팅', '광고', '판매'], search_intent: 'informational' },
    YouTube: { estimated_search_volume: 620000, monthly_searches: 620000, competition_level: 'High', trend: 'rising', keyword_difficulty_score: 74, cpc: '2.40', opportunity_score: '52.3', related_keywords: ['Marketing for beginners', 'Digital marketing course', 'Marketing strategy'], search_intent: 'educational' }
  }
}

function generateDefaultData(keyword: string, portal: string): any {
  const baseVolume: Record<string, number> = { Naver: 80000, Google: 1500000, Daum: 5000, YouTube: 200000 }
  const volumeVariance = Math.random() * 0.4 - 0.2
  const baseVol = baseVolume[portal] || 50000
  const searchVolume = Math.floor(baseVol * (1 + volumeVariance))

  return {
    estimated_search_volume: searchVolume,
    monthly_searches: searchVolume,
    competition_level: ['Low', 'Medium', 'High'][Math.floor(Math.random() * 3)],
    trend: ['rising', 'stable', 'declining'][Math.floor(Math.random() * 3)],
    keyword_difficulty_score: Math.floor(Math.random() * 100),
    cpc: (Math.random() * 5 + 0.5).toFixed(2),
    opportunity_score: (Math.random() * 100).toFixed(1),
    related_keywords: [`${keyword} tutorial`, `${keyword} guide`, `${keyword} tips`, `${keyword} for beginners`, `${keyword} advanced`],
    search_intent: ['informational', 'navigational', 'commercial', 'educational'][Math.floor(Math.random() * 4)]
  }
}

export default async function handler(req: NextApiRequest, res: NextApiResponse<AnalysisResponse>) {
  if (req.method !== 'POST') {
    return res.status(405).json({ success: false, keyword: '', error: 'Method not allowed' })
  }

  try {
    const { keyword, portal = 'Naver' } = req.body

    if (!keyword || typeof keyword !== 'string') {
      return res.status(400).json({ success: false, keyword: '', error: 'Keyword is required' })
    }

    const normalizedKeyword = keyword.toLowerCase().trim()
    const portalsToAnalyze = portal === 'All' ? ['Naver', 'Google', 'Daum', 'YouTube'] : [portal]

    // 🎯 롱테일/숏테일 분석 추가
    const keywordType = classifyKeywordType(keyword)
    const keywordMetrics = calculateKeywordMetrics(keyword, 100000)
    const relatedKeywords = generateRelatedKeywords(keyword, portal)

    const analysis: any = {
      keyword: keyword,
      timestamp: new Date().toISOString(),
      keywordAnalysis: {
        type: keywordType,
        wordCount: keywordMetrics.wordCount,
        difficulty: keywordMetrics.difficulty,
        recommendedForBeginners: keywordMetrics.recommendedForBeginners,
        conversionPotential: keywordMetrics.conversionPotential,
        recommendationScore: calculateRecommendationScore(keyword, 100000, 'beginner')
      },
      advancedRelatedKeywords: relatedKeywords,
      portals: {},
      newsAndBlog: {},
      trendData: {},
      monthlyTrendData: {},
      seasonalityAnalysis: {}
    }

    for (const p of portalsToAnalyze) {
      const dbData = KEYWORD_DATABASE[normalizedKeyword]?.[p]
      if (dbData) {
        analysis.portals[p] = {
          ...dbData,
          keywordScore: calculateKeywordScore(dbData.estimated_search_volume, dbData.keyword_difficulty_score, dbData.competition_level as 'Low' | 'Medium' | 'High', 70)
        }
      } else {
        const defaultData = generateDefaultData(keyword, p)
        analysis.portals[p] = {
          ...defaultData,
          keywordScore: calculateKeywordScore(defaultData.estimated_search_volume, defaultData.keyword_difficulty_score, defaultData.competition_level as 'Low' | 'Medium' | 'High', 70)
        }
      }

      // 뉴스/블로그 데이터 추가
      const newsAndBlogData = generateNewsAndBlogData(keyword, p)
      const trendData = generateTrendData(keyword, p)

      analysis.newsAndBlog[p] = {
        ...newsAndBlogData,
        score: calculateNewsAndBlogScore(newsAndBlogData.newsCount30d, newsAndBlogData.blogCount30d, analysis.portals[p].estimated_search_volume)
      }

      analysis.trendData[p] = trendData

      // 12개월 트렌드 데이터 및 계절성 분석 추가
      const monthlyTrend = generate12MonthTrendData(keyword, p)
      const seasonality = analyzeSeasonality(monthlyTrend)

      analysis.monthlyTrendData[p] = monthlyTrend
      analysis.seasonalityAnalysis[p] = seasonality
    }

    return res.status(200).json({ success: true, keyword: keyword, analysis: analysis })
  } catch (error) {
    console.error('Analysis error:', error)
    return res.status(500).json({ success: false, keyword: '', error: 'Internal server error' })
  }
}
