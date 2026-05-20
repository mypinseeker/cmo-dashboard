'use client'
import { useParams } from 'next/navigation'
import Link from 'next/link'

interface CityMetrics {
  users: string
  userTrend: string
  experience: number
  expTrend: string
  churnRate: string
  churnTrend: string
  vsClaro: string
  prb: number
  edgePct: number
  ytHD: number
  ytBuffer: number
  topIssue: string
  action: string
  sites: number
  alertSites: number
}

// Mock 城市数据
const CITY_DATA: Record<string, CityMetrics> = {
  Bogota: { users: '4.2M', userTrend: '+3.1%', experience: 4.3, expTrend: '+0.3', churnRate: '0.8%', churnTrend: '-0.1%', vsClaro: '-5%', prb: 55, edgePct: 15, ytHD: 38, ytBuffer: 2.2, topIssue: '部分站点晚高峰拥塞', action: '3 站点扩容', sites: 100, alertSites: 5 },
  Medellin: { users: '2.8M', userTrend: '+2.5%', experience: 3.9, expTrend: '+0.1', churnRate: '1.0%', churnTrend: '0%', vsClaro: '-10%', prb: 50, edgePct: 18, ytHD: 35, ytBuffer: 2.5, topIssue: '西部山区覆盖不足', action: '4 站点补盲', sites: 80, alertSites: 3 },
  Cali: { users: '1.9M', userTrend: '+1.8%', experience: 3.5, expTrend: '-0.1', churnRate: '1.3%', churnTrend: '+0.2%', vsClaro: '-12%', prb: 58, edgePct: 22, ytHD: 30, ytBuffer: 3.1, topIssue: '南部扩展区域覆盖缺口', action: '6 站点新建', sites: 70, alertSites: 8 },
  Barranquilla: { users: '1.1M', userTrend: '-1.2%', experience: 2.8, expTrend: '-0.5', churnRate: '2.1%', churnTrend: '+0.4%', vsClaro: '-22%', prb: 72, edgePct: 32, ytHD: 18, ytBuffer: 5.8, topIssue: 'PRB>90% 站点多、覆盖差、竞对领先', action: '8 站点扩容+补盲', sites: 60, alertSites: 15 },
  Cartagena: { users: '0.8M', userTrend: '-0.8%', experience: 3.1, expTrend: '-0.2', churnRate: '1.8%', churnTrend: '+0.3%', vsClaro: '-18%', prb: 68, edgePct: 28, ytHD: 22, ytBuffer: 4.5, topIssue: '旅游区域高峰拥塞', action: '5 站点扩容', sites: 50, alertSites: 10 },
}

function DiagnosisBar({ data }: { data: CityMetrics }) {
  const isSerious = parseFloat(data.userTrend) < 0 && data.experience < 3.5 && parseFloat(data.churnTrend) > 0
  const isCaution = data.experience < 4.0 || parseFloat(data.churnTrend) > 0
  const level = isSerious ? 'bg-red-900 border-red-700 text-red-300' : isCaution ? 'bg-yellow-900 border-yellow-700 text-yellow-300' : 'bg-green-900 border-green-700 text-green-300'
  const label = isSerious ? '🔴 高优先级：用户下降+体验恶化+流失上升+竞对领先' : isCaution ? '⚠️ 需关注：部分指标异常' : '✅ 健康：各项指标正常'

  return (
    <div className={`rounded p-2 text-xs border ${level}`}>
      {label} — {data.topIssue}
    </div>
  )
}

export default function DrilldownPage() {
  const params = useParams()
  const city = params.city as string
  const data = CITY_DATA[city]

  if (!data) {
    return (
      <div className="h-screen bg-gray-950 text-white flex items-center justify-center">
        <div>
          <p className="text-xl mb-4">城市 &quot;{city}&quot; 暂无数据</p>
          <Link href="/" className="text-cyan-400 hover:underline">← 返回大屏</Link>
        </div>
      </div>
    )
  }

  const expColor = data.experience >= 4.0 ? 'text-green-400' : data.experience >= 3.0 ? 'text-yellow-400' : 'text-red-400'
  const userColor = data.userTrend.startsWith('-') ? 'text-red-400' : 'text-green-400'

  return (
    <div className="min-h-screen bg-gray-950 text-white p-4">
      {/* 顶部 */}
      <div className="flex justify-between items-center mb-3">
        <div className="flex items-center gap-3">
          <Link href="/" className="text-gray-400 hover:text-cyan-400 text-sm">← 返回大屏</Link>
          <h1 className="text-xl font-bold text-cyan-400">📍 {city}</h1>
        </div>
        <span className="text-gray-500 text-sm">2026-05-19</span>
      </div>

      {/* 诊断条 */}
      <DiagnosisBar data={data} />

      {/* 4 张 KPI 卡片 */}
      <div className="grid grid-cols-4 gap-3 mt-3">
        <div className="bg-gray-900 rounded p-4 border border-gray-800">
          <p className="text-xs text-gray-400">用户数</p>
          <p className="text-2xl font-bold">{data.users}</p>
          <p className={`text-xs ${userColor}`}>{data.userTrend} MoM</p>
        </div>
        <div className="bg-gray-900 rounded p-4 border border-gray-800">
          <p className="text-xs text-gray-400">体验评分</p>
          <p className={`text-2xl font-bold ${expColor}`}>{data.experience}</p>
          <p className={`text-xs ${parseFloat(data.expTrend) >= 0 ? 'text-green-400' : 'text-red-400'}`}>{data.expTrend} MoM</p>
        </div>
        <div className="bg-gray-900 rounded p-4 border border-gray-800">
          <p className="text-xs text-gray-400">离网率</p>
          <p className="text-2xl font-bold text-white">{data.churnRate}</p>
          <p className={`text-xs ${parseFloat(data.churnTrend) > 0 ? 'text-red-400' : 'text-green-400'}`}>{data.churnTrend} MoM</p>
        </div>
        <div className="bg-gray-900 rounded p-4 border border-gray-800">
          <p className="text-xs text-gray-400">vs Claro</p>
          <p className="text-2xl font-bold text-yellow-400">{data.vsClaro}</p>
          <p className="text-xs text-gray-500">速率差距</p>
        </div>
      </div>

      {/* 六维归因 */}
      <div className="grid grid-cols-2 gap-3 mt-3">
        {/* 左侧：网络+覆盖+探针 */}
        <div className="bg-gray-900 rounded p-4 border border-gray-800">
          <h3 className="text-sm font-semibold text-gray-300 mb-3">原因分析</h3>

          <div className="space-y-3 text-xs">
            <div>
              <p className="text-gray-400 mb-1">网络层面</p>
              <div className="grid grid-cols-2 gap-2">
                <div><span className="text-gray-500">PRB 均值：</span><span className={data.prb > 70 ? 'text-red-400' : data.prb > 60 ? 'text-yellow-400' : 'text-green-400'}>{data.prb}%</span></div>
                <div><span className="text-gray-500">告警站点：</span><span className="text-red-400">{data.alertSites} / {data.sites}</span></div>
              </div>
            </div>

            <div className="border-t border-gray-800 pt-2">
              <p className="text-gray-400 mb-1">覆盖质量</p>
              <div className="grid grid-cols-2 gap-2">
                <div><span className="text-gray-500">边缘占比：</span><span className={data.edgePct > 25 ? 'text-red-400' : data.edgePct > 20 ? 'text-yellow-400' : 'text-green-400'}>{data.edgePct}%</span></div>
              </div>
            </div>

            <div className="border-t border-gray-800 pt-2">
              <p className="text-gray-400 mb-1">用户感知（探针）</p>
              <div className="grid grid-cols-2 gap-2">
                <div><span className="text-gray-500">YouTube HD：</span><span className={data.ytHD < 25 ? 'text-red-400' : data.ytHD < 35 ? 'text-yellow-400' : 'text-green-400'}>{data.ytHD}%</span></div>
                <div><span className="text-gray-500">卡顿率：</span><span className={data.ytBuffer > 4 ? 'text-red-400' : data.ytBuffer > 2.5 ? 'text-yellow-400' : 'text-green-400'}>{data.ytBuffer}%</span></div>
              </div>
            </div>
          </div>
        </div>

        {/* 右侧：竞对+流失+终端 */}
        <div className="bg-gray-900 rounded p-4 border border-gray-800">
          <h3 className="text-sm font-semibold text-gray-300 mb-3">竞对与流失</h3>

          <div className="space-y-3 text-xs">
            <div>
              <p className="text-gray-400 mb-1">Ookla 竞对对比</p>
              <p className="text-white">Tigo vs Claro 速率差距：<span className="text-yellow-400">{data.vsClaro}</span></p>
            </div>

            <div className="border-t border-gray-800 pt-2">
              <p className="text-gray-400 mb-1">流失归因</p>
              <p className="text-white">离网率 <span className={parseFloat(data.churnRate) > 1.5 ? 'text-red-400' : 'text-yellow-400'}>{data.churnRate}</span>（全网 1.2%）</p>
              <p className="text-gray-500">网络因素占比：约 {data.edgePct > 25 ? '78%' : '45%'}</p>
            </div>

            <div className="border-t border-gray-800 pt-2">
              <p className="text-gray-400 mb-1">建议行动</p>
              <p className="text-cyan-400 font-semibold">{data.action}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
