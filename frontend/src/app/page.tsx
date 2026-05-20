import dynamic from 'next/dynamic'
import UserCards from '@/components/UserCards'
import ExperienceCards from '@/components/ExperienceCards'
import TerminalCards from '@/components/TerminalCards'
import ChurnCards from '@/components/ChurnCards'
import AppExperience from '@/components/AppExperience'

const DashboardMap = dynamic(() => import('@/components/DashboardMap'), { ssr: false })

export default function Dashboard() {
  return (
    <div className="h-screen flex flex-col p-2 gap-2">
      <header className="flex justify-between items-center px-4 py-1.5 bg-gray-900 rounded border border-gray-800">
        <h1 className="text-lg font-bold text-cyan-400">Tigo Colombia CMO Dashboard</h1>
        <span className="text-gray-400 text-sm">2026-05-19</span>
      </header>

      <div className="flex-1 flex gap-2 min-h-0">
        <div className="w-60 flex flex-col gap-2">
          <div className="bg-gray-900 rounded p-3 flex-1 border border-gray-800 overflow-auto">
            <UserCards />
          </div>
          <div className="bg-gray-900 rounded p-3 flex-1 border border-gray-800 overflow-auto">
            <TerminalCards />
          </div>
        </div>

        <div className="flex-1 bg-gray-900 rounded border border-gray-800 overflow-hidden">
          <DashboardMap />
        </div>

        <div className="w-60 flex flex-col gap-2">
          <div className="bg-gray-900 rounded p-3 flex-1 border border-gray-800 overflow-auto">
            <ExperienceCards />
          </div>
          <div className="bg-gray-900 rounded p-3 flex-1 border border-gray-800 overflow-auto">
            <ChurnCards />
          </div>
        </div>
      </div>

      <div className="h-32">
        <AppExperience />
      </div>
    </div>
  )
}
