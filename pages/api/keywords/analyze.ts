import type { NextApiRequest, NextApiResponse } from 'next'

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' })
  }

  try {
    const { keyword } = req.body

    if (!keyword) {
      return res.status(400).json({ error: 'Keyword is required' })
    }

    // Python 백엔드 호출 (FastAPI)
    const response = await fetch('http://localhost:8000/api/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ keyword })
    })

    const data = await response.json()
    res.status(200).json(data)
  } catch (error) {
    console.error('Analysis error:', error)
    res.status(500).json({ error: 'Internal server error' })
  }
}
