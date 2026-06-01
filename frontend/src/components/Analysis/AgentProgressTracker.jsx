import { Users, TrendingUp, Swords, ListChecks, Lightbulb, Grid2X2, FileText, CheckCircle, XCircle, Loader2, Clock } from 'lucide-react'

const AGENT_META = {
  'Customer Feedback Agent': { icon: Users, color: 'text-pink-400' },
  'Market Research Agent': { icon: TrendingUp, color: 'text-blue-400' },
  'Competitor Analysis Agent': { icon: Swords, color: 'text-orange-400' },
  'Feature Prioritization Agent': { icon: ListChecks, color: 'text-purple-400' },
  'Opportunity Agent': { icon: Lightbulb, color: 'text-yellow-400' },
  'SWOT Analysis Agent': { icon: Grid2X2, color: 'text-green-400' },
  'Executive Report Agent': { icon: FileText, color: 'text-cyan-400' },
}

const AGENT_NAMES = Object.keys(AGENT_META)

export default function AgentProgressTracker({ agents = [], isRunning }) {
  const completedCount = agents.filter(a => a.status === 'completed').length
  const total = AGENT_NAMES.length

  const getStatus = (name) => {
    const agent = agents.find(a => a.agent_name === name)
    if (!agent) return isRunning ? 'running' : 'pending'
    return agent.status
  }

  return (
    <div className="max-w-2xl mx-auto">
      <div className="text-center mb-8">
        <h2 className="text-2xl font-bold text-white mb-2">Running Multi-Agent Analysis</h2>
        <p className="text-gray-400 text-sm">7 AI agents working in parallel to analyze your documents</p>
        <div className="mt-4 flex items-center justify-center gap-3">
          <div className="text-[#e94560] font-bold text-3xl">{completedCount}</div>
          <div className="text-gray-500 text-lg">/ {total} agents complete</div>
        </div>
        <div className="mt-3 h-2 bg-[#1f2d4e] rounded-full overflow-hidden max-w-sm mx-auto">
          <div
            className="h-full bg-gradient-to-r from-[#e94560] to-[#0f3460] rounded-full transition-all duration-500"
            style={{ width: `${(completedCount / total) * 100}%` }}
          />
        </div>
      </div>

      <div className="grid gap-3">
        {AGENT_NAMES.map(name => {
          const meta = AGENT_META[name]
          const Icon = meta.icon
          const status = getStatus(name)
          const agent = agents.find(a => a.agent_name === name)

          return (
            <div key={name} className={`bg-[#0f1929] border rounded-xl px-4 py-3.5 flex items-center gap-4 transition-all ${
              status === 'running' ? 'border-blue-500/50' :
              status === 'completed' ? 'border-green-500/30' :
              status === 'failed' ? 'border-red-500/30' :
              'border-[#1f2d4e]'
            }`}>
              <div className="w-9 h-9 rounded-lg bg-[#1a1a2e] flex items-center justify-center flex-shrink-0">
                <Icon size={18} className={meta.color} />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-white text-sm font-medium">{name}</p>
                {agent?.duration_ms && (
                  <p className="text-gray-500 text-xs flex items-center gap-1">
                    <Clock size={10} />{(agent.duration_ms / 1000).toFixed(1)}s
                  </p>
                )}
              </div>
              <div className="flex-shrink-0">
                {status === 'completed' && <CheckCircle size={18} className="text-green-400" />}
                {status === 'failed' && <XCircle size={18} className="text-red-400" />}
                {status === 'running' && <Loader2 size={18} className="text-blue-400 animate-spin" />}
                {status === 'pending' && <div className="w-4 h-4 rounded-full border-2 border-gray-600" />}
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
