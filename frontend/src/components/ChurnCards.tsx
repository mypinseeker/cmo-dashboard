'use client'
export default function ChurnCards() {
  return (
    <div className="flex flex-col gap-3 h-full text-sm">
      <div>
        <p className="text-xs text-gray-400">月度流失</p>
        <p className="text-xl font-bold text-white">15.2K</p>
        <p className="text-xs text-red-400">▲ +8% MoM</p>
        <p className="text-xs text-gray-500">网络因素 62%</p>
      </div>
      <div className="border-t border-gray-800 pt-2">
        <p className="text-xs text-gray-400 mb-1">Ookla 对比</p>
        <div className="text-xs space-y-1">
          <div className="flex justify-between"><span className="text-cyan-400">Tigo</span><span>38 Mbps</span></div>
          <div className="flex justify-between"><span className="text-orange-400">Claro</span><span>42 Mbps</span></div>
          <div className="flex justify-between"><span className="text-purple-400">Movistar</span><span>28 Mbps</span></div>
        </div>
      </div>
    </div>
  )
}
