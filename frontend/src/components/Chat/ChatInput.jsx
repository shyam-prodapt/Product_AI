import { useState } from 'react'
import { Send } from 'lucide-react'

export default function ChatInput({ onSend, disabled }) {
  const [value, setValue] = useState('')

  const handle = () => {
    const trimmed = value.trim()
    if (!trimmed || disabled) return
    onSend(trimmed)
    setValue('')
  }

  return (
    <div className="flex gap-2 bg-[#0f1929] border border-[#1f2d4e] rounded-2xl p-2">
      <input
        value={value}
        onChange={e => setValue(e.target.value)}
        onKeyDown={e => e.key === 'Enter' && !e.shiftKey && handle()}
        placeholder="Ask about your product strategy…"
        disabled={disabled}
        className="flex-1 bg-transparent text-white text-sm px-2 outline-none placeholder:text-gray-600 disabled:opacity-50"
      />
      <button
        onClick={handle}
        disabled={!value.trim() || disabled}
        className="w-9 h-9 rounded-xl bg-[#e94560] disabled:opacity-40 disabled:cursor-not-allowed flex items-center justify-center flex-shrink-0 hover:bg-[#ff6b80] transition-colors"
      >
        <Send size={14} className="text-white" />
      </button>
    </div>
  )
}
