import ReactMarkdown from 'react-markdown'
import { Brain, User } from 'lucide-react'

export default function ChatMessage({ message }) {
  const isUser = message.role === 'user'
  return (
    <div className={`flex gap-3 ${isUser ? 'flex-row-reverse' : ''}`}>
      <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
        isUser ? 'bg-[#e94560]' : 'bg-[#0f3460]'
      }`}>
        {isUser ? <User size={14} className="text-white" /> : <Brain size={14} className="text-white" />}
      </div>
      <div className={`max-w-[75%] flex flex-col gap-1 ${isUser ? 'items-end' : 'items-start'}`}>
        <div className={`rounded-2xl px-4 py-3 text-sm leading-relaxed ${
          isUser
            ? 'bg-[#e94560] text-white rounded-tr-sm'
            : 'bg-[#0f1929] border border-[#1f2d4e] text-gray-200 rounded-tl-sm'
        }`}>
          {isUser ? message.content : (
            <ReactMarkdown components={{
              p: ({ children }) => <p className="mb-2 last:mb-0">{children}</p>,
              ul: ({ children }) => <ul className="list-disc pl-4 mb-2">{children}</ul>,
              ol: ({ children }) => <ol className="list-decimal pl-4 mb-2">{children}</ol>,
              li: ({ children }) => <li className="mb-0.5">{children}</li>,
              strong: ({ children }) => <strong className="text-white font-semibold">{children}</strong>,
              code: ({ children }) => <code className="bg-[#1a1a2e] px-1.5 py-0.5 rounded text-[#e94560] text-xs">{children}</code>,
            }}>{message.content}</ReactMarkdown>
          )}
        </div>
        {message.sources?.length > 0 && (
          <div className="flex gap-1 flex-wrap">
            {message.sources.map((s, i) => (
              <span key={i} className="text-[10px] text-gray-500 bg-[#0f1929] border border-[#1f2d4e] px-2 py-0.5 rounded-full">{s}</span>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
