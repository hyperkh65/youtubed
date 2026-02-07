import type { NextApiRequest, NextApiResponse } from 'next'
import { getServerSession } from 'next-auth/next'
import { authOptions } from '../auth/[...nextauth]'

interface UpdateSubscriptionRequest {
  planTier: 'free' | 'pro' | 'team'
  stripeSubscriptionId?: string
  stripeCustomerId?: string
}

interface UpdateSubscriptionResponse {
  success?: boolean
  error?: string
  user?: any
}

// 실제 구현에서는 데이터베이스에 저장합니다
// 현재는 메모리에만 저장됩니다 (데모용)
const userSubscriptions: Record<string, any> = {}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<UpdateSubscriptionResponse>
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' })
  }

  const session = await getServerSession(req, res, authOptions)

  if (!session?.user) {
    return res.status(401).json({ error: 'Unauthorized' })
  }

  const { planTier, stripeSubscriptionId, stripeCustomerId } =
    req.body as UpdateSubscriptionRequest

  if (!planTier || !['free', 'pro', 'team'].includes(planTier)) {
    return res.status(400).json({ error: 'Invalid plan tier' })
  }

  try {
    const userId = session.user.id || session.user.email

    // 구독 정보 업데이트 (데모용)
    userSubscriptions[userId] = {
      planTier,
      stripeSubscriptionId,
      stripeCustomerId,
      updatedAt: new Date(),
      subscriptionStatus: planTier === 'free' ? 'cancelled' : 'active',
    }

    // 실제 구현에서는:
    // await db.user.update({
    //   where: { id: userId },
    //   data: {
    //     tier: planTier,
    //     stripeSubscriptionId,
    //     stripeCustomerId,
    //   },
    // })

    return res.status(200).json({
      success: true,
      user: {
        id: userId,
        email: session.user.email,
        tier: planTier,
      },
    })
  } catch (error) {
    console.error('Subscription update error:', error)
    return res.status(500).json({ error: 'Failed to update subscription' })
  }
}
