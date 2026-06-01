import { useState } from 'react'
import { uploadFiles } from '../api/client'

export function useFileUpload() {
  const [uploading, setUploading] = useState(false)
  const [progress, setProgress] = useState(0)
  const [error, setError] = useState(null)

  const upload = async (fileList) => {
    setUploading(true)
    setError(null)
    setProgress(0)
    const formData = new FormData()
    for (const file of fileList) formData.append('files', file)
    try {
      const { data } = await uploadFiles(formData, setProgress)
      return data.session_id
    } catch (err) {
      setError(err.response?.data?.detail || 'Upload failed')
      return null
    } finally {
      setUploading(false)
    }
  }

  return { uploading, progress, error, upload }
}
