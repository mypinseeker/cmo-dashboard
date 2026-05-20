'use client'
import dynamic from 'next/dynamic'

const MapInner = dynamic(() => import('./MapInner'), { ssr: false, loading: () => <div className="h-full flex items-center justify-center text-gray-500">地图加载中...</div> })

export default function DashboardMap() {
  return <MapInner />
}
