import { useState, useEffect } from 'react'
import AgentProgressTracker from './AgentProgressTracker'
import InsightCard from './InsightCard'
import { ReportDownloadButton } from '../Report/ReportDownloadButton'
import { useAnalysis } from '../../hooks/useAnalysis'
import { TrendingUp, Target, Zap, BarChart3 } from 'lucide-react'

function MetricCard({ label, value, icon: Icon, color }) {
  return (
    <div className="bg-[#0f1929] border border-[#1f2d4e] rounded-xl p-4">
      <div className={`w-9 h-9 rounded-lg ${color} flex items-center justify-center mb-3`}>
        <Icon size={18} className="text-white" />
      </div>
      <div className="text-2xl font-bold text-white">{value}</div>
      <div className="text-gray-500 text-xs mt-0.5">{label}</div>
    </div>
  )
}

function SwotGrid({ swot }) {
  const { strengths = [], weaknesses = [], opportunities = [], threats = [] } = swot || {}
  const quad = (title, items, bg, textColor) => (
    <div className={`${bg} rounded-xl p-4`}>
      <h4 className={`font-bold text-sm mb-3 ${textColor}`}>{title}</h4>
      <ul className="space-y-1.5">
        {items.slice(0, 5).map((item, i) => (
          <li key={i} className="text-gray-300 text-xs flex gap-2">
            <span className={`${textColor} flex-shrink-0`}>•</span>{item}
          </li>
        ))}
      </ul>
    </div>
  )
  return (
    <div className="grid grid-cols-2 gap-3">
      {quad('STRENGTHS', strengths, 'bg-green-950/50 border border-green-800/30', 'text-green-400')}
      {quad('WEAKNESSES', weaknesses, 'bg-red-950/50 border border-red-800/30', 'text-red-400')}
      {quad('OPPORTUNITIES', opportunities, 'bg-blue-950/50 border border-blue-800/30', 'text-blue-400')}
      {quad('THREATS', threats, 'bg-yellow-950/50 border border-yellow-800/30', 'text-yellow-400')}
    </div>
  )
}

function PriorityBadge({ score }) {
  const s = parseFloat(score)
  if (s >= 7) return <span className="px-2 py-0.5 rounded-full text-xs bg-green-900/40 text-green-400 border border-green-700/30">High</span>
  if (s >= 4) return <span className="px-2 py-0.5 rounded-full text-xs bg-yellow-900/40 text-yellow-400 border border-yellow-700/30">Medium</span>
  return <span className="px-2 py-0.5 rounded-full text-xs bg-red-900/40 text-red-400 border border-red-700/30">Low</span>
}

export default function AnalysisDashboard({ sessionId, onComplete, analysisData, readonly }) {
  const { analyzing, data, error, analyze } = useAnalysis()
  const result = analysisData || data
  const [activeTab, setActiveTab] = useState('Overview')

  useEffect(() => {
    if (!readonly && sessionId) {
      analyze(sessionId).then(d => { if (d && onComplete) onComplete(d) })
    }
  }, [sessionId])

  const isRunning = analyzing && !result
  const agentResults = result?.agents || []

  if (!result) {
    return (
      <div className="max-w-2xl mx-auto py-8">
        <AgentProgressTracker agents={agentResults} isRunning={isRunning} />
        {error && (
          <div className="mt-6 text-center text-red-400 bg-red-900/20 border border-red-700/30 rounded-xl p-4">{error}</div>
        )}
      </div>
    )
  }

  const tabs = ['Overview', 'SWOT', 'Features', 'Opportunities', 'Roadmap', 'Agents']

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-bold text-white">Strategy Analysis Complete</h2>
        <ReportDownloadButton analysisData={result} />
      </div>

      <div className="grid grid-cols-4 gap-3">
        <MetricCard label="Opportunities" value={result.opportunities?.length || 0} icon={Zap} color="bg-[#e94560]" />
        <MetricCard label="Features Prioritized" value={result.feature_priorities?.length || 0} icon={Target} color="bg-[#0f3460]" />
        <MetricCard label="Strategic Insights" value={result.insights?.length || 0} icon={TrendingUp} color="bg-purple-900" />
        <MetricCard label="SWOT Items" value={Object.values(result.swot || {}).flat().length} icon={BarChart3} color="bg-green-900" />
      </div>

      <div className="flex gap-1 bg-[#0f1929] border border-[#1f2d4e] rounded-xl p-1">
        {tabs.map(t => (
          <button key={t} onClick={() => setActiveTab(t)}
            className={`flex-1 py-2 text-xs font-medium rounded-lg transition-all ${
              activeTab === t ? 'bg-[#e94560] text-white' : 'text-gray-400 hover:text-white'
            }`}>{t}</button>
        ))}
      </div>

      {activeTab === 'Overview' && (
        <div className="space-y-4">
          <div className="bg-[#0f1929] border border-[#1f2d4e] rounded-xl p-5">
            <h3 className="text-white font-semibold mb-3 text-sm">Executive Summary</h3>
            <p className="text-gray-300 text-sm leading-relaxed">{result.executive_summary}</p>
          </div>
          <div className="space-y-2">
            <h3 className="text-white font-semibold text-sm">Strategic Insights</h3>
            {result.insights?.slice(0, 10).map((ins, i) => <InsightCard key={i} number={i + 1} text={ins} />)}
          </div>
        </div>
      )}

      {activeTab === 'SWOT' && (
        <div className="space-y-4">
          <h3 className="text-white font-semibold text-sm">SWOT Analysis</h3>
          <SwotGrid swot={result.swot} />
        </div>
      )}

      {activeTab === 'Features' && (
        <div>
          <h3 className="text-white font-semibold text-sm mb-3">Feature Prioritization</h3>
          <div className="bg-[#0f1929] border border-[#1f2d4e] rounded-xl overflow-hidden">
            <table className="w-full text-sm">
              <thead className="bg-[#1a1a2e]">
                <tr>
                  {['Feature', 'Impact', 'Effort', 'Priority Score', 'Level'].map(h => (
                    <th key={h} className="px-4 py-3 text-left text-gray-400 text-xs font-medium">{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {(result.feature_priorities || []).slice(0, 10).map((f, i) => (
                  <tr key={i} className="border-t border-[#1f2d4e] hover:bg-white/[0.02]">
                    <td className="px-4 py-3 text-white font-medium">{f.name}</td>
                    <td className="px-4 py-3 text-gray-300">{f.impact}/10</td>
                    <td className="px-4 py-3 text-gray-300">{f.effort}/10</td>
                    <td className="px-4 py-3 text-white font-semibold">{parseFloat(f.priority_score).toFixed(2)}</td>
                    <td className="px-4 py-3"><PriorityBadge score={f.priority_score} /></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {activeTab === 'Opportunities' && (
        <div className="grid gap-4">
          {(result.opportunities || []).slice(0, 8).map((opp, i) => (
            <div key={i} className="bg-[#0f1929] border border-[#1f2d4e] rounded-xl p-5 flex gap-4">
              <div className="flex-shrink-0">
                <div className="w-12 h-12 rounded-xl bg-[#1a1a2e] border border-[#1f2d4e] flex flex-col items-center justify-center">
                  <span className="text-[#e94560] font-bold text-lg leading-none">{opp.score}</span>
                  <span className="text-gray-600 text-[9px]">/10</span>
                </div>
              </div>
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <h4 className="text-white font-semibold text-sm">{opp.title}</h4>
                  <span className="px-2 py-0.5 rounded-full text-[10px] bg-[#e94560]/15 text-[#e94560] border border-[#e94560]/30">{opp.category}</span>
                </div>
                <p className="text-gray-400 text-xs leading-relaxed">{opp.description}</p>
              </div>
            </div>
          ))}
        </div>
      )}

      {activeTab === 'Roadmap' && (
        <div className="space-y-4">
          {(result.roadmap || []).map((phase, i) => (
            <div key={i} className="bg-[#0f1929] border border-[#1f2d4e] rounded-xl p-5">
              <div className="flex items-center gap-3 mb-3">
                <div className="w-2 h-2 rounded-full bg-[#e94560]" />
                <h4 className="text-white font-semibold text-sm">{phase.quarter}</h4>
                <span className="text-gray-500 text-xs bg-[#1a1a2e] px-2 py-0.5 rounded-full">{phase.theme}</span>
              </div>
              <div className="flex flex-wrap gap-2">
                {(phase.features || []).map((f, j) => (
                  <span key={j} className="px-3 py-1 rounded-full text-xs bg-[#0f3460]/50 text-blue-300 border border-blue-800/30">{f}</span>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}

      {activeTab === 'Agents' && (
        <div className="space-y-2">
          {(result.agents || []).map((agent, i) => (
            <details key={i} className="bg-[#0f1929] border border-[#1f2d4e] rounded-xl">
              <summary className="px-4 py-3 cursor-pointer text-sm font-medium text-white flex items-center justify-between list-none">
                <span>{agent.agent_name}</span>
                <span className={`text-xs px-2 py-0.5 rounded-full ${
                  agent.status === 'completed' ? 'bg-green-900/40 text-green-400' : 'bg-red-900/40 text-red-400'
                }`}>{agent.status}</span>
              </summary>
              <div className="px-4 pb-4">
                <pre className="text-xs text-gray-400 overflow-auto max-h-48 bg-[#0d0d1a] rounded-lg p-3 whitespace-pre-wrap">
                  {JSON.stringify(agent.output, null, 2)}
                </pre>
              </div>
            </details>
          ))}
        </div>
      )}
    </div>
  )
}
