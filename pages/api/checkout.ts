import type { NextApiRequest, NextApiResponse } from 'next'
import { getServerSession } from 'next-auth/next'
import { authOptions } from './auth/[...nextauth]'

interface CheckoutRequest {
  planTier: 'pro' | 'team'
}

interface CheckoutResponse {
  url?: string
  error?: string
  message?: string
}

const STRIPE_PRICES = {
  pro: {
    id: process.env.NEXT_PUBLIC_STRIPE_PRICE_PRO || 'price_pro_demo',
    amount: 1900, // $19.00 in cents
    name: 'Pro Plan',
  },
  team: {
    id: process.env.NEXT_PUBLIC_STRIPE_PRICE_TEAM || 'price_team_demo',
    amount: 9900, // $99.00 in cents
    name: 'Team Plan',
  },
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<CheckoutResponse>
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' })
  }

  const session = await getServerSession(req, res, authOptions)

  if (!session?.user) {
    return res.status(401).json({ error: 'Unauthorized' })
  }

  const { planTier } = req.body as CheckoutRequest

  if (!planTier || !['pro', 'team'].includes(planTier)) {
    return res.status(400).json({ error: 'Invalid plan tier' })
  }

  try {
    // 실제 구현에서는 Stripe API를 호출합니다
    // 지금은 데모용 응답을 반환합니다
    const price = STRIPE_PRICES[planTier]

    // 데모: Stripe Checkout URL 시뮬레이션
    const checkoutUrl = `/checkout/demo?plan=${planTier}&amount=${price.amount}&user=${session.user.email}`

    return res.status(200).json({
      url: checkoutUrl,
      message: `${price.name} 결제 페이지로 이동합니다.`,
    })
  } catch (error) {
    console.error('Checkout error:', error)
    return res.status(500).json({ error: 'Failed to create checkout session' })
  }
}
