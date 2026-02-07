import type { AppProps } from 'next/app'
import { SessionProvider } from 'next-auth/react'
import Navbar from '@/components/Navbar'
import { Toaster } from 'react-hot-toast'

export default function App({ Component, pageProps: { session, ...pageProps } }: AppProps) {
  return (
    <SessionProvider session={session}>
      <>
        <Navbar />
        <main className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
          <Component {...pageProps} />
        </main>
        <Toaster position="bottom-right" />
      </>
    </SessionProvider>
  )
}
