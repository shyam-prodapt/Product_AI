import { useState } from 'react'
import { sendChatMessage } from '../api/client'

export function useChat(sessionId) {
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)

  const send = async (text) => {
    const userMsg = { role: 'user', content: text }
    setMessages(prev => [...prev, userMsg])
    setLoading(true)
    try {
      const history = messages.map(m => ({ role: m.role, content: m.content }))
      const { data } = await sendChatMessage(sessionId, text, history)
      setMessages(prev => [
        ...prev,
        { role: 'assistant', content: data.response, sources: data.sources },
      ])
    } catch (err) {
      setMessages(prev => [
        ...prev,
        { role: 'assistant', content: 'Error: ' + (err.message || 'Request failed'), sources: [] },
      ])
    } finally {
      setLoading(false)
    }
  }

  return { messages, loading, send }
}
