import React, { useState } from 'react'
import Head from 'next/head'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/Tabs'
import KeywordAnalysis from '@/components/KeywordAnalysis'
import TrendAnalysis from '@/components/TrendAnalysis'
import AdvancedFeatures from '@/components/AdvancedFeatures'
import Performance from '@/components/Performance'
import Settings from '@/components/Settings'

export default function Home() {
  const [activeTab, setActiveTab] = useState('keyword-analysis')

  return (
    <>
      <Head>
        <title>YouTube Keyword Analyzer - Advanced Analysis Tool</title>
        <meta name="description" content="Advanced keyword analysis for YouTube content creators" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-12 text-center">
          <h1 className="text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-cyan-400 mb-4">
            🎯 YouTube Keyword Analyzer
          </h1>
          <p className="text-xl text-gray-300 mb-2">
            Advanced Multi-Portal Keyword Analysis with Notion Integration
          </p>
          <p className="text-sm text-gray-400">
            Google • Naver • Daum • YouTube | Powered by Notion DB
          </p>
        </div>

        {/* Tabs */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full grid-cols-5 mb-8 bg-slate-800 p-2 rounded-lg">
            <TabsTrigger value="keyword-analysis" className="text-sm md:text-base">
              🔍 Analysis
            </TabsTrigger>
            <TabsTrigger value="trend-analysis" className="text-sm md:text-base">
              📊 Trends
            </TabsTrigger>
            <TabsTrigger value="advanced" className="text-sm md:text-base">
              🎯 Advanced
            </TabsTrigger>
            <TabsTrigger value="performance" className="text-sm md:text-base">
              📈 Performance
            </TabsTrigger>
            <TabsTrigger value="settings" className="text-sm md:text-base">
              ⚙️ Settings
            </TabsTrigger>
          </TabsList>

          {/* Tab Contents */}
          <TabsContent value="keyword-analysis" className="space-y-6">
            <KeywordAnalysis />
          </TabsContent>

          <TabsContent value="trend-analysis" className="space-y-6">
            <TrendAnalysis />
          </TabsContent>

          <TabsContent value="advanced" className="space-y-6">
            <AdvancedFeatures />
          </TabsContent>

          <TabsContent value="performance" className="space-y-6">
            <Performance />
          </TabsContent>

          <TabsContent value="settings" className="space-y-6">
            <Settings />
          </TabsContent>
        </Tabs>

        {/* Footer */}
        <div className="mt-16 pt-8 border-t border-slate-700 text-center text-gray-400 text-sm">
          <p>
            Advanced Keyword Analyzer v2.0 | Powered by Notion API | Deployed on Vercel
          </p>
          <p className="mt-2 text-xs text-gray-500">
            © 2026 YouTube Channel Manager. All rights reserved.
          </p>
        </div>
      </div>
    </>
  )
}
