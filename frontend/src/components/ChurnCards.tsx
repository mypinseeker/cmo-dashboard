'use client'
import { useEffect, useState } from 'react'
import { fetchAPI } from '@/lib/api'

const MOCK_DATA = {
  monthlyChurn: '15.2K',
  momChange: '+8%',
  networkFactorPct: '62%',
  tigoMbps: '38',
  claroMbps: '42',
  movistarMbps: '28'
}

export default function ChurnCards() {
  const [data, setData] = useState(MOCK_DATA)

  useEffect(() => {
    async function load() {
      const churn = await fetchAPI('/api/churn')
      if (churn) {
        setData({
          monthlyChurn: churn.monthly_churn ? `${(churn.monthly_churn / 1000).toFixed(1)}K` : '15.2K',
          momChange: churn.mom_change_pct ? `+${churn.mom_change_pct}%` : '+8%',
          networkFactorPct: churn.network_factor_pct || '62%',
          tigoMbps: churn.tigo_speed_mbps?.toString() || '38',
          claroMbps: churn.claro_speed_mbps?.toString() || '42',
          movistarMbps: churn.movistar_speed_mbps?.toString() || '28'
        })
      }
    }
    load()
  }, [])

  return (
    <div className="flex flex-col gap-3 h-full text-sm">
      <div>
        <p className="text-xs text-gray-400">月度流失</p>
        <p className="text-xl font-bold text-white">{data.monthlyChurn}</p>
        <p className="text-xs text-red-400">▲ {data.momChange} MoM</p>
        <p className="text-xs text-gray-500">网络因素 {data.networkFactorPct}</p>
      </div>
      <div className="border-t border-gray-800 pt-2">
        <p className="text-xs text-gray-400 mb-1">Ookla 对比</p>
        <div className="text-xs space-y-1">
          <div className="flex justify-between"><span className="text-cyan-400">Tigo</span><span>{data.tigoMbps} Mbps</span></div>
          <div className="flex justify-between"><span className="text-orange-400">Claro</span><span>{data.claroMbps} Mbps</span></div>
          <div className="flex justify-between"><span className="text-purple-400">Movistar</span><span>{data.movistarMbps} Mbps</span></div>
        </div>
      </div>
    </div>
  )
}
