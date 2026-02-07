import React from 'react'
import Head from 'next/head'
import Link from 'next/link'

const PRICING_PLANS = [
  {
    name: 'Free',
    price: '$0',
    period: '/월',
    icon: '🎯',
    description: '키워드 분석 시작하기',
    cta: '무료 시작',
    ctaHref: '/',
    highlight: false,
    features: [
      { text: '월 10회 분석', included: true },
      { text: '단일 포털만 (1개)', included: true },
      { text: '기본 메트릭 (검색량, 난이도)', included: true },
      { text: '신뢰도 🔴 50-70% (AI 추정)', included: true },
      { text: '관련 키워드 (3개 제한)', included: true },
      { text: '검색 의도 분석', included: false },
      { text: '경쟁사 분석', included: false },
      { text: '12개월 트렌드 분석', included: false },
      { text: '뉴스/블로그 추적', included: false },
      { text: 'CSV 다운로드', included: false },
      { text: '이메일 지원', included: false },
    ]
  },
  {
    name: 'Pro',
    price: '$19',
    period: '/월',
    icon: '⚡',
    description: '전문가 수준의 분석',
    cta: 'Pro 시작하기',
    ctaHref: '/upgrade?plan=pro',
    highlight: true,
    features: [
      { text: '무제한 분석', included: true },
      { text: '6개 포털 동시 분석', included: true, badge: '⭐ 인기' },
      { text: '모든 메트릭 (CPC, 기회점수 포함)', included: true },
      { text: '신뢰도 🟢 85%+ (Google API)', included: true },
      { text: '관련 키워드 무제한', included: true },
      { text: '검색 의도 분석', included: true },
      { text: '경쟁사 분석 (5개)', included: true },
      { text: '12개월 트렌드 & 계절성', included: true },
      { text: '뉴스/블로그 30일 추적', included: true },
      { text: 'CSV/PDF 다운로드', included: true },
      { text: '우선 이메일 지원', included: true },
    ]
  },
  {
    name: 'Team',
    price: '$99',
    period: '/월',
    icon: '🏢',
    description: '팀 협업과 확장',
    cta: 'Team 시작하기',
    ctaHref: '/upgrade?plan=team',
    highlight: false,
    features: [
      { text: 'Pro의 모든 기능', included: true },
      { text: '최대 5개 팀 계정', included: true },
      { text: '팀 대시보드 & 멤버 관리', included: true },
      { text: '공유 키워드 라이브러리', included: true },
      { text: '팀 분석 리포트', included: true },
      { text: 'Slack 알림 연동', included: true },
      { text: '월별 자동 리포트', included: true },
      { text: '우선 전화 지원', included: true },
      { text: '맞춤 보고서', included: false },
      { text: 'API 접근', included: false },
      { text: 'SLA 보장 (99.9%)', included: false },
    ]
  },
]

const FAQ = [
  {
    q: 'Free 플랜으로 정말 무료인가요?',
    a: '네, 완전히 무료입니다! 월 10회 분석까지 무제한 사용 가능하며, 신용카드 등록이 필요 없습니다.'
  },
  {
    q: 'Pro에서 무제한 분석이 정말 무제한인가요?',
    a: '네, 무제한입니다. 월 1회든 월 1000회든 추가 요금 없이 사용 가능합니다.'
  },
  {
    q: '언제든지 플랜을 변경할 수 있나요?',
    a: '물론입니다. 매달 플랜을 변경하거나 취소할 수 있으며, 요금은 일할 계산됩니다.'
  },
  {
    q: 'Team 플랜은 언제 필요한가요?',
    a: '팀의 2명 이상이 함께 분석하거나, 공유 키워드 라이브러리가 필요할 때 추천합니다. Pro 5개월 비용으로 5개 계정을 관리할 수 있습니다.'
  },
  {
    q: '신뢰도 배지가 무엇인가요?',
    a: '🟢 High(85%+)는 Google Ads API 직접 연동, 🟡 Medium(70-85%)는 파트너 데이터, 🔴 Low(50-70%)는 AI 추정값입니다.'
  },
  {
    q: '환불 정책은?',
    a: '30일 환불 보장 정책으로 신청 후 30일 내에 환불 신청 가능합니다. 질문 없는 전액 환불입니다.'
  },
]

export default function Pricing() {
  return (
    <>
      <Head>
        <title>KeyPoint Pro 가격책정 | 범용 키워드 분석 플랫폼</title>
        <meta name="description" content="KeyPoint Pro의 투명한 가격 정책. Free부터 Enterprise까지 모든 규모의 사용자를 위한 플랜" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>

      <main className="min-h-screen bg-black text-white">
        {/* 상단 네비게이션 */}
        <nav className="border-b border-slate-700">
          <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
            <Link href="/" className="flex items-center gap-2 font-bold text-xl hover:text-emerald-400">
              <span className="text-2xl">🔍</span>
              <span>KeyPoint Pro</span>
            </Link>
            <Link href="/" className="text-slate-400 hover:text-white transition">
              ← 돌아가기
            </Link>
          </div>
        </nav>

        {/* 헤더 */}
        <section className="relative bg-gradient-to-b from-black via-emerald-950/5 to-black px-4 py-20">
          <div className="max-w-6xl mx-auto text-center">
            <h1 className="text-5xl md:text-6xl font-bold mb-6 leading-tight">
              모든 규모를 위한<br />
              <span className="bg-gradient-to-r from-emerald-400 to-cyan-400 bg-clip-text text-transparent">
                명확한 가격책정
              </span>
            </h1>
            <p className="text-lg text-slate-400 mb-8 max-w-3xl mx-auto">
              숨겨진 수수료 없음. 언제든지 업그레이드/다운그레이드 가능.<br />
              30일 환불 보장으로 안심하세요.
            </p>
          </div>
        </section>

        {/* 가격 카드 */}
        <section className="max-w-7xl mx-auto px-4 py-20">
          <div className="grid md:grid-cols-3 gap-8">
            {PRICING_PLANS.map((plan) => (
              <div
                key={plan.name}
                className={`relative rounded-2xl border-2 p-8 transition duration-300 ${
                  plan.highlight
                    ? 'border-emerald-500 bg-emerald-500/10 shadow-xl shadow-emerald-500/20 md:scale-105'
                    : 'border-slate-700 bg-slate-900/30 hover:border-slate-600'
                }`}
              >
                {plan.highlight && (
                  <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                    <span className="bg-emerald-500 text-black px-4 py-1 rounded-full text-sm font-bold">
                      인기 선택
                    </span>
                  </div>
                )}

                {/* 플랜 이름 */}
                <div className="text-center mb-8">
                  <div className="text-4xl mb-2">{plan.icon}</div>
                  <h3 className="text-2xl font-bold mb-2">{plan.name}</h3>
                  <p className="text-slate-400 text-sm mb-4">{plan.description}</p>

                  {/* 가격 */}
                  <div className="mb-6">
                    <span className="text-5xl font-bold">{plan.price}</span>
                    <span className="text-slate-400 ml-2">{plan.period}</span>
                  </div>

                  {plan.name === 'Team' && (
                    <p className="text-sm text-slate-400 mb-4">5개 계정 포함</p>
                  )}

                  {/* CTA 버튼 */}
                  <a
                    href={plan.ctaHref}
                    className={`block w-full py-3 rounded-lg font-bold transition duration-200 mb-6 ${
                      plan.highlight
                        ? 'bg-emerald-500 hover:bg-emerald-600 text-black'
                        : 'bg-slate-700 hover:bg-slate-600 text-white'
                    }`}
                  >
                    {plan.cta}
                  </a>
                </div>

                {/* 기능 목록 */}
                <div className="space-y-4 border-t border-slate-700 pt-8">
                  {plan.features.map((feature, idx) => (
                    <div key={idx} className="flex items-start gap-3">
                      <span className="text-lg mt-1">
                        {feature.included ? '✅' : '❌'}
                      </span>
                      <div className="flex-1">
                        <p className={feature.included ? 'text-white' : 'text-slate-500'}>
                          {feature.text}
                          {feature.badge && (
                            <span className="ml-2 text-xs bg-emerald-500/20 text-emerald-400 px-2 py-1 rounded">
                              {feature.badge}
                            </span>
                          )}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>

          {/* Enterprise */}
          <div className="mt-12 text-center">
            <h3 className="text-2xl font-bold mb-4">Enterprise 플랜이 필요하신가요?</h3>
            <p className="text-slate-400 mb-6">
              대규모 팀, API 접근, 맞춤 연동, SLA 보장이 필요한 기업을 위한 맞춤 요금제를 제공합니다.
            </p>
            <button className="px-8 py-3 border border-emerald-500 text-emerald-400 rounded-lg font-bold hover:bg-emerald-500/10 transition">
              📧 영업팀에 문의하기
            </button>
          </div>
        </section>

        {/* 기능 비교 테이블 */}
        <section className="max-w-7xl mx-auto px-4 py-20">
          <h2 className="text-3xl font-bold text-center mb-12">상세 기능 비교</h2>

          <div className="overflow-x-auto">
            <table className="w-full text-left">
              <thead>
                <tr className="border-b border-slate-700">
                  <th className="px-4 py-4 font-bold text-white bg-slate-900/50">기능</th>
                  <th className="px-4 py-4 font-bold text-center bg-slate-900/50">Free</th>
                  <th className="px-4 py-4 font-bold text-center bg-emerald-500/10 border-x border-emerald-500/20">Pro</th>
                  <th className="px-4 py-4 font-bold text-center bg-slate-900/50">Team</th>
                </tr>
              </thead>
              <tbody>
                {[
                  { category: '기본', items: [
                    { name: '월간 분석', free: '10회', pro: '무제한', team: '무제한' },
                    { name: '포털 선택', free: '1개', pro: '6개', team: '6개' },
                    { name: '신뢰도', free: '🔴 50-70%', pro: '🟢 85%+', team: '🟢 85%+' },
                  ]},
                  { category: '분석 기능', items: [
                    { name: '검색 의도 분석', free: '❌', pro: '✅', team: '✅' },
                    { name: '경쟁사 분석', free: '❌', pro: '✅', team: '✅' },
                    { name: '12개월 트렌드', free: '❌', pro: '✅', team: '✅' },
                    { name: '뉴스/블로그 추적', free: '❌', pro: '✅', team: '✅' },
                  ]},
                  { category: '내보내기', items: [
                    { name: 'CSV 다운로드', free: '❌', pro: '✅', team: '✅' },
                    { name: 'PDF 리포트', free: '❌', pro: '✅', team: '✅' },
                    { name: '월별 자동 리포트', free: '❌', pro: '❌', team: '✅' },
                  ]},
                  { category: '팀 기능', items: [
                    { name: '팀 계정', free: '❌', pro: '❌', team: '최대 5개' },
                    { name: '공유 라이브러리', free: '❌', pro: '❌', team: '✅' },
                    { name: 'Slack 연동', free: '❌', pro: '❌', team: '✅' },
                  ]},
                  { category: '지원', items: [
                    { name: '커뮤니티 포럼', free: '✅', pro: '✅', team: '✅' },
                    { name: '이메일 지원', free: '❌', pro: '✅', team: '✅ 우선' },
                    { name: '전화 지원', free: '❌', pro: '❌', team: '✅' },
                  ]},
                ].map((section) => (
                  <React.Fragment key={section.category}>
                    <tr className="border-b border-slate-700">
                      <td colSpan={4} className="px-4 py-4 font-bold text-emerald-400 bg-slate-900/30">
                        {section.category}
                      </td>
                    </tr>
                    {section.items.map((item) => (
                      <tr key={item.name} className="border-b border-slate-700 hover:bg-slate-900/20">
                        <td className="px-4 py-4 font-medium text-white">{item.name}</td>
                        <td className="px-4 py-4 text-center text-slate-400">{item.free}</td>
                        <td className="px-4 py-4 text-center bg-emerald-500/5 text-white font-semibold">{item.pro}</td>
                        <td className="px-4 py-4 text-center text-slate-400">{item.team}</td>
                      </tr>
                    ))}
                  </React.Fragment>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        {/* FAQ */}
        <section className="max-w-3xl mx-auto px-4 py-20">
          <h2 className="text-3xl font-bold text-center mb-12">자주 묻는 질문</h2>

          <div className="space-y-6">
            {FAQ.map((item, idx) => (
              <details
                key={idx}
                className="group border border-slate-700 rounded-lg p-6 cursor-pointer hover:border-emerald-500/50 transition"
              >
                <summary className="flex justify-between items-center font-bold text-white">
                  {item.q}
                  <span className="group-open:rotate-180 transition duration-200">▼</span>
                </summary>
                <p className="text-slate-400 mt-4">{item.a}</p>
              </details>
            ))}
          </div>
        </section>

        {/* CTA */}
        <section className="max-w-4xl mx-auto px-4 py-20 text-center">
          <h2 className="text-3xl font-bold mb-6">
            무료로 시작해보세요.<br />
            신용카드 등록 필요 없습니다.
          </h2>
          <p className="text-slate-400 mb-8">
            2분 안에 가입하고 10회 무료 분석을 즉시 시작하세요.
          </p>
          <a
            href="/"
            className="inline-block px-8 py-4 bg-emerald-500 hover:bg-emerald-600 text-black font-bold rounded-lg transition duration-200"
          >
            🚀 KeyPoint Pro 시작하기
          </a>
        </section>

        {/* 푸터 */}
        <footer className="border-t border-slate-700 py-12">
          <div className="max-w-6xl mx-auto px-4 text-center text-slate-500 text-sm">
            <p>© 2026 KeyPoint Pro. All rights reserved.</p>
            <div className="mt-4 space-x-4">
              <a href="#" className="hover:text-white transition">개인정보처리방침</a>
              <span>·</span>
              <a href="#" className="hover:text-white transition">이용약관</a>
              <span>·</span>
              <a href="#" className="hover:text-white transition">연락처</a>
            </div>
          </div>
        </footer>
      </main>
    </>
  )
}
