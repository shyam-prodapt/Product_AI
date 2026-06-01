import { LayoutDashboard, MessageSquare } from 'lucide-react'

const tabs = [
  { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { id: 'chat', label: 'Ask AI', icon: MessageSquare },
]

export default function Sidebar({ activeTab, onTabChange }) {
  return (
    <aside className="w-52 bg-[#0d0d1a] border-r border-[#1f2d4e] flex flex-col py-6 px-3 gap-1">
      {tabs.map(({ id, label, icon: Icon }) => (
        <button
          key={id}
          onClick={() => onTabChange(id)}
          className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all ${
            activeTab === id
              ? 'bg-[#e94560]/15 text-[#e94560] border border-[#e94560]/30'
              : 'text-gray-400 hover:text-white hover:bg-white/5'
          }`}
        >
          <Icon size={16} />
          {label}
        </button>
      ))}
    </aside>
  )
}
