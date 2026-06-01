import { useState } from 'react'
import { runAnalysis } from '../api/client'

export function useAnalysis() {
  const [analyzing, setAnalyzing] = useState(false)
  const [data, setData] = useState(null)
  const [error, setError] = useState(null)

  const analyze = async (sessionId) => {
    setAnalyzing(true)
    setError(null)
    try {
      const { data: result } = await runAnalysis(sessionId)
      setData(result)
      return result
    } catch (err) {
      setError(err.response?.data?.detail || 'Analysis failed')
      return null
    } finally {
      setAnalyzing(false)
    }
  }

  return { analyzing, data, error, analyze }
}
