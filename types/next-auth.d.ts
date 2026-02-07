import 'next-auth'
import 'next-auth/jwt'

declare module 'next-auth' {
  interface Session {
    user: {
      id: string
      email: string
      name: string | null
      image: string | null
      tier: 'free' | 'pro' | 'team'
      monthlyAnalysisCount: number
      stripeCustomerId: string | null
      subscriptionStatus: string | null
    }
  }

  interface User {
    id: string
    email: string
    name: string | null
    image: string | null
    tier?: 'free' | 'pro' | 'team'
  }
}

declare module 'next-auth/jwt' {
  interface JWT {
    id: string
    email: string
    name: string | null
    image: string | null
    tier: 'free' | 'pro' | 'team'
    monthlyAnalysisCount: number
    stripeCustomerId: string | null
    subscriptionStatus: string | null
  }
}
