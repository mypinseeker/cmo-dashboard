'use client'
import { useEffect, useState } from 'react'
import { fetchAPI } from '@/lib/api'

const MOCK_DATA = {
  premiumUsers: '4.5M',
  premiumPct: '36%',
  premiumRevenuePct: '68%',
  uncoveredPop: '11.5M',
  highPotential: '4.2M',
  yearlyRevenue: '$180M'
}

export default function TerminalCards() {
  const [data, setData] = useState(MOCK_DATA)

  useEffect(() => {
    async function load() {
      const terminals = await fetchAPI('/api/terminals')
      if (terminals) {
        setData({
          premiumUsers: terminals.premium_users ? `${(terminals.premium_users / 1000000).toFixed(1)}M` : '4.5M',
          premiumPct: terminals.premium_pct || '36%',
          premiumRevenuePct: terminals.premium_revenue_pct || '68%',
          uncoveredPop: terminals.uncovered_pop ? `${(terminals.uncovered_pop / 1000000).toFixed(1)}M` : '11.5M',
          highPotential: terminals.high_potential ? `${(terminals.high_potential / 1000000).toFixed(1)}M` : '4.2M',
          yearlyRevenue: terminals.yearly_revenue ? `$${terminals.yearly_revenue}M` : '$180M'
        })
      }
    }
    load()
  }, [])

  return (
    <div className="flex flex-col gap-3 h-full text-sm">
      <div>
        <p className="text-xs text-gray-400">高价值用户</p>
        <p className="text-xl font-bold text-white">{data.premiumUsers} <span className="text-xs text-gray-500">({data.premiumPct})</span></p>
        <p className="text-xs text-gray-500">贡献收入 {data.premiumRevenuePct}</p>
      </div>
      <div className="border-t border-gray-800 pt-2">
        <p className="text-xs text-gray-400">未覆盖人口</p>
        <p className="text-xl font-bold text-yellow-400">{data.uncoveredPop}</p>
        <p className="text-xs text-gray-500">高潜力 {data.highPotential} · {data.yearlyRevenue}/年</p>
      </div>
    </div>
  )
}
