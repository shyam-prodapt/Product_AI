import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '',
  timeout: 180000,
})

export const uploadFiles = (formData, onProgress) =>
  api.post('/api/upload/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
    onUploadProgress: (e) => onProgress?.(Math.round((e.loaded / e.total) * 100)),
  })

export const runAnalysis = (sessionId) =>
  api.post('/api/analysis/run', { session_id: sessionId })

export const sendChatMessage = (sessionId, message, history) =>
  api.post('/api/chat/', { session_id: sessionId, message, history })

export const downloadReport = (analysisData) =>
  api.post('/api/report/download', analysisData, { responseType: 'blob' })
