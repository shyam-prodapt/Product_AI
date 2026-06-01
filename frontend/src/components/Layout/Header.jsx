import { Brain, Cpu, CheckCircle } from 'lucide-react'

const PHASE_LABELS = {
  upload: 'Upload Documents',
  analyzing: 'Running Analysis',
  results: 'Strategy Ready',
}

export default function Header({ phase }) {
  return (
    <header className="bg-[#0d0d1a] border-b border-[#1f2d4e] px-6 py-4 flex items-center justify-between">
      <div className="flex items-center gap-3">
        <div className="w-9 h-9 rounded-lg bg-[#e94560] flex items-center justify-center">
          <Brain size={20} className="text-white" />
        </div>
        <div>
          <h1 className="text-white font-bold text-lg leading-tight">Product Strategy AI</h1>
          <p className="text-gray-400 text-xs">Multi-Agent Intelligence Platform</p>
        </div>
      </div>
      <div className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium ${
        phase === 'results'
          ? 'bg-green-900/40 text-green-400 border border-green-700/50'
          : phase === 'analyzing'
          ? 'bg-blue-900/40 text-blue-400 border border-blue-700/50'
          : 'bg-gray-800 text-gray-400 border border-gray-700/50'
      }`}>
        {phase === 'results' && <CheckCircle size={12} />}
        {phase === 'analyzing' && <Cpu size={12} className="animate-pulse" />}
        {PHASE_LABELS[phase]}
      </div>
    </header>
  )
}
