'use client'
import { useEffect, useState } from 'react'
import { fetchAPI } from '@/lib/api'

const MOCK_DATA = {
  totalUsers: '12.5M',
  momChange: '+2.3%',
  dailyNetNew: '+28K',
  dailyNew: '+45K',
  dailyChurn: '-17K',
  worstCity: 'Barranquilla',
  worstChurnRate: '2.1%'
}

export default function UserCards() {
  const [data, setData] = useState(MOCK_DATA)

  useEffect(() => {
    async function load() {
      const overview = await fetchAPI('/api/overview')
      if (overview) {
        setData({
          totalUsers: (overview.total_users_estimate / 1000000).toFixed(1) + 'M',
          momChange: overview.mom_change_pct ? `+${overview.mom_change_pct}%` : '+2.3%',
          dailyNetNew: overview.daily_net_new ? `+${(overview.daily_net_new / 1000).toFixed(0)}K` : '+28K',
          dailyNew: overview.daily_new ? `+${(overview.daily_new / 1000).toFixed(0)}K` : '+45K',
          dailyChurn: overview.daily_churn ? `-${(overview.daily_churn / 1000).toFixed(0)}K` : '-17K',
          worstCity: overview.worst_churn_city || 'Barranquilla',
          worstChurnRate: overview.worst_churn_rate ? `${overview.worst_churn_rate}%` : '2.1%'
        })
      }
    }
    load()
  }, [])

  return (
    <div className="flex flex-col gap-3 h-full text-sm">
      <div>
        <p className="text-xs text-gray-400">在网用户</p>
        <p className="text-3xl font-bold text-white">{data.totalUsers}</p>
        <p className="text-xs text-green-400">▲ {data.momChange} MoM</p>
      </div>
      <div className="border-t border-gray-800 pt-2">
        <p className="text-xs text-gray-400 mb-1">日变化</p>
        <div className="grid grid-cols-3 gap-1 text-xs">
          <div><p className="text-gray-500">净增</p><p className="text-green-400 font-bold">{data.dailyNetNew}</p></div>
          <div><p className="text-gray-500">新增</p><p className="text-blue-400 font-bold">{data.dailyNew}</p></div>
          <div><p className="text-gray-500">流失</p><p className="text-red-400 font-bold">{data.dailyChurn}</p></div>
        </div>
      </div>
      <div className="border-t border-gray-800 pt-2">
        <p className="text-xs text-gray-400 mb-1">流失最高</p>
        <a href={`/drilldown/${data.worstCity}`} className="text-sm text-red-400 hover:underline cursor-pointer">{data.worstCity} →</a>
        <p className="text-xs text-gray-500">离网率 {data.worstChurnRate}</p>
      </div>
    </div>
  )
}
