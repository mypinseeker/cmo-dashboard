'use client'
export default function ExperienceCards() {
  return (
    <div className="flex flex-col gap-3 h-full text-sm">
      <div>
        <p className="text-xs text-gray-400">体验评分</p>
        <p className="text-3xl font-bold text-white">4.2<span className="text-base text-gray-500">/5.0</span></p>
        <p className="text-xs text-green-400">▲ +0.2 MoM</p>
      </div>
      <div className="border-t border-gray-800 pt-2">
        <p className="text-xs text-gray-400 mb-1">vs Claro</p>
        <p className="text-sm text-yellow-400">差距 -8%</p>
        <p className="text-xs text-green-400">趋势：缩小 ▼</p>
      </div>
      <div className="border-t border-gray-800 pt-2">
        <p className="text-xs text-gray-400 mb-1">覆盖质量</p>
        <p className="text-sm text-white">边缘用户 20%</p>
        <p className="text-xs text-gray-500">2.5M 人弱信号</p>
      </div>
      <div className="border-t border-gray-800 pt-2">
        <p className="text-xs text-gray-400">告警城市</p>
        <a href="/drilldown/alerts" className="text-2xl font-bold text-red-400 hover:underline cursor-pointer">3 →</a>
      </div>
    </div>
  )
}
