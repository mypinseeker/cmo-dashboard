'use client'

function AppCard({ name, color, metrics }: { name: string; color: string; metrics: { label: string; value: string; status: string }[] }) {
  const statusColor = (s: string) => s === 'good' ? 'text-green-400' : s === 'warn' ? 'text-yellow-400' : 'text-red-400'
  return (
    <div className="bg-gray-900 rounded p-3 flex-1 border border-gray-800">
      <h3 className="text-xs font-semibold mb-2" style={{ color }}>{name}</h3>
      <div className="space-y-1">
        {metrics.map((m, i) => (
          <div key={i} className="flex justify-between text-xs">
            <span className="text-gray-400">{m.label}</span>
            <span className={`font-semibold ${statusColor(m.status)}`}>{m.value}</span>
          </div>
        ))}
      </div>
    </div>
  )
}

export default function AppExperience() {
  return (
    <div className="flex gap-2 h-full">
      <AppCard name="YouTube" color="#ff0000" metrics={[
        { label: 'HD 占比', value: '33% ▼', status: 'warn' },
        { label: '卡顿率', value: '2.8% ▲', status: 'warn' },
        { label: '缓冲', value: '1.2s', status: 'warn' },
      ]} />
      <AppCard name="Netflix" color="#e50914" metrics={[
        { label: 'HD 占比', value: '43% ▲', status: 'good' },
        { label: '卡顿率', value: '1.5% ▼', status: 'good' },
        { label: '缓冲', value: '0.95s', status: 'good' },
      ]} />
      <AppCard name="TikTok" color="#00f2ea" metrics={[
        { label: '成功率', value: '98.5% ▲', status: 'good' },
        { label: '上传', value: '6.2Mbps ▲', status: 'good' },
        { label: '日活', value: '580K', status: 'good' },
      ]} />
      <div className="bg-gray-900 rounded p-3 flex-1 border border-gray-800">
        <h3 className="text-xs font-semibold text-gray-300 mb-2">流量分布</h3>
        <div className="space-y-1.5">
          {[{n:'视频',p:32,c:'#ef4444'},{n:'社交',p:28,c:'#3b82f6'},{n:'消息',p:18,c:'#10b981'},{n:'游戏',p:8,c:'#f59e0b'},{n:'其他',p:14,c:'#6b7280'}].map(c => (
            <div key={c.n} className="flex items-center gap-2 text-xs">
              <span className="text-gray-400 w-8">{c.n}</span>
              <div className="flex-1 bg-gray-800 rounded-full h-1.5">
                <div className="h-1.5 rounded-full" style={{width:`${c.p}%`,backgroundColor:c.c}} />
              </div>
              <span className="text-gray-300 w-7 text-right">{c.p}%</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
