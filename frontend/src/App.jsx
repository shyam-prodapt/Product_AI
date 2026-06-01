import { useState } from 'react'
import FileUploadZone from './components/Upload/FileUploadZone'
import AnalysisDashboard from './components/Analysis/AnalysisDashboard'
import ChatInterface from './components/Chat/ChatInterface'
import Header from './components/Layout/Header'
import Sidebar from './components/Layout/Sidebar'

const PHASES = { UPLOAD: 'upload', ANALYZING: 'analyzing', RESULTS: 'results' }

export default function App() {
  const [phase, setPhase] = useState(PHASES.UPLOAD)
  const [sessionId, setSessionId] = useState(null)
  const [analysisData, setAnalysisData] = useState(null)
  const [activeTab, setActiveTab] = useState('dashboard')

  return (
    <div className="min-h-screen bg-[#030712] text-white flex flex-col">
      <Header phase={phase} />
      <div className="flex flex-1 overflow-hidden">
        {phase === PHASES.RESULTS && (
          <Sidebar activeTab={activeTab} onTabChange={setActiveTab} />
        )}
        <main className="flex-1 overflow-auto p-6">
          {phase === PHASES.UPLOAD && (
            <FileUploadZone onComplete={(sid) => {
              setSessionId(sid)
              setPhase(PHASES.ANALYZING)
            }} />
          )}
          {(phase === PHASES.ANALYZING || (phase === PHASES.RESULTS && activeTab === 'dashboard')) && (
            <AnalysisDashboard
              sessionId={sessionId}
              onComplete={(data) => {
                setAnalysisData(data)
                setPhase(PHASES.RESULTS)
              }}
              analysisData={analysisData}
              readonly={phase === PHASES.RESULTS}
            />
          )}
          {phase === PHASES.RESULTS && activeTab === 'chat' && (
            <ChatInterface sessionId={sessionId} analysisData={analysisData} />
          )}
        </main>
      </div>
    </div>
  )
}
