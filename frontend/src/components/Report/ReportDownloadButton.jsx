import { useState } from 'react'
import { downloadReport } from '../../api/client'
import { Download, Loader2 } from 'lucide-react'

export function ReportDownloadButton({ analysisData }) {
  const [loading, setLoading] = useState(false)

  const handle = async () => {
    setLoading(true)
    try {
      const { data } = await downloadReport(analysisData)
      const url = URL.createObjectURL(new Blob([data], { type: 'application/pdf' }))
      const a = document.createElement('a')
      a.href = url
      a.download = 'product-strategy-report.pdf'
      a.click()
      URL.revokeObjectURL(url)
    } catch (err) {
      console.error('PDF download failed:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <button
      onClick={handle}
      disabled={loading}
      className="flex items-center gap-2 px-4 py-2 rounded-xl bg-[#0f3460] hover:bg-[#1a4a8a] text-white text-sm font-medium transition-all disabled:opacity-50 border border-blue-700/30"
    >
      {loading ? <Loader2 size={14} className="animate-spin" /> : <Download size={14} />}
      {loading ? 'Generating PDF…' : 'Download Report'}
    </button>
  )
}
