import type { NextApiRequest, NextApiResponse } from 'next'

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' })
  }

  try {
    const { keywords, channelTopic } = req.body

    if (!keywords || !Array.isArray(keywords)) {
      return res.status(400).json({ error: 'Keywords array is required' })
    }

    // Python 백엔드 호출
    const response = await fetch('http://localhost:8000/api/recommendations', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ keywords, channel_topic: channelTopic })
    })

    const data = await response.json()
    res.status(200).json(data)
  } catch (error) {
    console.error('Recommendations error:', error)
    res.status(500).json({ error: 'Internal server error' })
  }
}
