import { useEffect, useRef } from 'react'
import ChatMessage from './ChatMessage'
import ChatInput from './ChatInput'
import { useChat } from '../../hooks/useChat'
import { Loader2, Sparkles } from 'lucide-react'

const SUGGESTED = [
  "What are the top 3 products by revenue?",
  "Which region has the best performance?",
  "What are the main customer pain points?",
  "Which features should we prioritize next?",
  "What is the overall market opportunity?",
]

export default function ChatInterface({ sessionId }) {
  const { messages, loading, send } = useChat(sessionId)
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  return (
    <div className="max-w-3xl mx-auto flex flex-col h-[calc(100vh-120px)]">
      <div className="mb-4">
        <h2 className="text-xl font-bold text-white">Ask the Strategy AI</h2>
        <p className="text-gray-500 text-sm">Ask questions grounded in your uploaded documents</p>
      </div>

      <div className="flex-1 overflow-y-auto space-y-4 pb-4">
        {messages.length === 0 && (
          <div className="space-y-3">
            <p className="text-gray-500 text-xs font-medium uppercase tracking-wider">Suggested questions</p>
            {SUGGESTED.map((q, i) => (
              <button key={i} onClick={() => send(q)}
                className="flex items-center gap-2 text-left w-full bg-[#0f1929] border border-[#1f2d4e] hover:border-[#e94560]/30 rounded-xl px-4 py-3 text-sm text-gray-300 hover:text-white transition-all">
                <Sparkles size={13} className="text-[#e94560] flex-shrink-0" />
                {q}
              </button>
            ))}
          </div>
        )}
        {messages.map((msg, i) => <ChatMessage key={i} message={msg} />)}
        {loading && (
          <div className="flex gap-3">
            <div className="w-8 h-8 rounded-full bg-[#0f3460] flex items-center justify-center flex-shrink-0">
              <Loader2 size={14} className="text-white animate-spin" />
            </div>
            <div className="bg-[#0f1929] border border-[#1f2d4e] rounded-2xl rounded-tl-sm px-4 py-3">
              <div className="flex gap-1">
                {[0, 1, 2].map(i => (
                  <div key={i} className="w-1.5 h-1.5 rounded-full bg-gray-500 animate-bounce" style={{ animationDelay: `${i * 0.15}s` }} />
                ))}
              </div>
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      <ChatInput onSend={send} disabled={loading} />
    </div>
  )
}
