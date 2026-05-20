'use client'
export default function TerminalCards() {
  return (
    <div className="flex flex-col gap-3 h-full text-sm">
      <div>
        <p className="text-xs text-gray-400">高价值用户</p>
        <p className="text-xl font-bold text-white">4.5M <span className="text-xs text-gray-500">(36%)</span></p>
        <p className="text-xs text-gray-500">贡献收入 68%</p>
      </div>
      <div className="border-t border-gray-800 pt-2">
        <p className="text-xs text-gray-400">未覆盖人口</p>
        <p className="text-xl font-bold text-yellow-400">11.5M</p>
        <p className="text-xs text-gray-500">高潜力 4.2M · $180M/年</p>
      </div>
    </div>
  )
}
