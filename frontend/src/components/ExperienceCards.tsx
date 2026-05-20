'use client'
import { useEffect, useState } from 'react'
import { fetchAPI } from '@/lib/api'

const MOCK_DATA = {
  experienceScore: '4.2',
  momChange: '+0.2',
  vsCompetitorGap: '-8%',
  edgeUserPct: '20%',
  weakSignalUsers: '2.5M',
  alertCities: '3'
}

export default function ExperienceCards() {
  const [data, setData] = useState(MOCK_DATA)

  useEffect(() => {
    async function load() {
      const experience = await fetchAPI('/api/experience')
      if (experience) {
        setData({
          experienceScore: experience.experience_score?.toFixed(1) || '4.2',
          momChange: experience.mom_change ? `+${experience.mom_change}` : '+0.2',
          vsCompetitorGap: experience.vs_claro_gap ? `${experience.vs_claro_gap}%` : '-8%',
          edgeUserPct: experience.edge_user_pct || '20%',
          weakSignalUsers: experience.weak_signal_users_m ? `${experience.weak_signal_users_m}M` : '2.5M',
          alertCities: experience.alert_cities?.toString() || '3'
        })
      }
    }
    load()
  }, [])

  return (
    <div className="flex flex-col gap-3 h-full text-sm">
      <div>
        <p className="text-xs text-gray-400">体验评分</p>
        <p className="text-3xl font-bold text-white">{data.experienceScore}<span className="text-base text-gray-500">/5.0</span></p>
        <p className="text-xs text-green-400">▲ {data.momChange} MoM</p>
      </div>
      <div className="border-t border-gray-800 pt-2">
        <p className="text-xs text-gray-400 mb-1">vs Claro</p>
        <p className="text-sm text-yellow-400">差距 {data.vsCompetitorGap}</p>
        <p className="text-xs text-green-400">趋势：缩小 ▼</p>
      </div>
      <div className="border-t border-gray-800 pt-2">
        <p className="text-xs text-gray-400 mb-1">覆盖质量</p>
        <p className="text-sm text-white">边缘用户 {data.edgeUserPct}</p>
        <p className="text-xs text-gray-500">{data.weakSignalUsers} 人弱信号</p>
      </div>
      <div className="border-t border-gray-800 pt-2">
        <p className="text-xs text-gray-400">告警城市</p>
        <a href="/drilldown/alerts" className="text-2xl font-bold text-red-400 hover:underline cursor-pointer">{data.alertCities} →</a>
      </div>
    </div>
  )
}
