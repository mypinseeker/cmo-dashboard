'use client'
export default function UserCards() {
  return (
    <div className="flex flex-col gap-3 h-full text-sm">
      <div>
        <p className="text-xs text-gray-400">在网用户</p>
        <p className="text-3xl font-bold text-white">12.5M</p>
        <p className="text-xs text-green-400">▲ +2.3% MoM</p>
      </div>
      <div className="border-t border-gray-800 pt-2">
        <p className="text-xs text-gray-400 mb-1">日变化</p>
        <div className="grid grid-cols-3 gap-1 text-xs">
          <div><p className="text-gray-500">净增</p><p className="text-green-400 font-bold">+28K</p></div>
          <div><p className="text-gray-500">新增</p><p className="text-blue-400 font-bold">+45K</p></div>
          <div><p className="text-gray-500">流失</p><p className="text-red-400 font-bold">-17K</p></div>
        </div>
      </div>
      <div className="border-t border-gray-800 pt-2">
        <p className="text-xs text-gray-400 mb-1">流失最高</p>
        <a href="/drilldown/Barranquilla" className="text-sm text-red-400 hover:underline cursor-pointer">Barranquilla →</a>
        <p className="text-xs text-gray-500">离网率 2.1%</p>
      </div>
    </div>
  )
}
