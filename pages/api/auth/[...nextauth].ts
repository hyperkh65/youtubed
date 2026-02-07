import NextAuth from 'next-auth'
import type { NextAuthOptions } from 'next-auth'
import GoogleProvider from 'next-auth/providers/google'
import GithubProvider from 'next-auth/providers/github'
import CredentialsProvider from 'next-auth/providers/credentials'

export const authOptions: NextAuthOptions = {
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID || '',
      clientSecret: process.env.GOOGLE_CLIENT_SECRET || '',
      allowDangerousEmailAccountLinking: true,
    }),
    GithubProvider({
      clientId: process.env.GITHUB_ID || '',
      clientSecret: process.env.GITHUB_SECRET || '',
      allowDangerousEmailAccountLinking: true,
    }),
    // 데모용 이메일 인증 (개발 환경)
    CredentialsProvider({
      name: 'Email (Demo)',
      credentials: {
        email: { label: 'Email', type: 'email' },
      },
      async authorize(credentials) {
        // 데모: 모든 이메일 허용
        if (!credentials?.email) {
          return null
        }

        return {
          id: credentials.email.replace('@', '-').replace('.', '-'),
          email: credentials.email,
          name: credentials.email.split('@')[0],
          image: null,
        }
      },
    }),
  ],

  callbacks: {
    async jwt({ token, user, account }) {
      if (user) {
        token.id = user.id
        token.email = user.email
        token.name = user.name
        token.image = user.image
        // Free 기본값
        token.tier = 'free' as const
        token.monthlyAnalysisCount = 0
        token.stripeCustomerId = null
        token.subscriptionStatus = null
      }

      return token
    },

    async session({ session, token }) {
      if (session.user && token) {
        session.user.id = token.id as string
        session.user.email = token.email as string
        session.user.name = token.name as string
        session.user.image = token.image as string
        session.user.tier = (token.tier as 'free' | 'pro' | 'team') || 'free'
        session.user.monthlyAnalysisCount = (token.monthlyAnalysisCount as number) || 0
        session.user.stripeCustomerId = token.stripeCustomerId as string | null
        session.user.subscriptionStatus = token.subscriptionStatus as string | null
      }

      return session
    },
  },

  pages: {
    signIn: '/auth/signin',
    error: '/auth/error',
  },

  session: {
    strategy: 'jwt',
    maxAge: 30 * 24 * 60 * 60, // 30 days
    updateAge: 24 * 60 * 60, // 24 hours
  },

  jwt: {
    secret: process.env.NEXTAUTH_SECRET,
  },

  events: {
    async signIn({ user, account, profile, isNewUser }) {
      // 로그인 이벤트 처리
      console.log(`User ${user?.email} signed in`)
    },
  },
}

export default NextAuth(authOptions)
