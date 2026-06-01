import { useCallback, useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, FileText, X, Loader2, CheckCircle, AlertCircle } from 'lucide-react'
import { useFileUpload } from '../../hooks/useFileUpload'

const FILE_ICONS = { pdf: '📄', csv: '📊', docx: '📝', txt: '📃' }
const fmt = (b) => b > 1024 * 1024 ? `${(b / 1024 / 1024).toFixed(1)} MB` : `${(b / 1024).toFixed(0)} KB`

export default function FileUploadZone({ onComplete }) {
  const [selectedFiles, setSelectedFiles] = useState([])
  const { uploading, progress, error, upload } = useFileUpload()

  const onDrop = useCallback((accepted) => {
    setSelectedFiles(prev => {
      const names = new Set(prev.map(f => f.name))
      return [...prev, ...accepted.filter(f => !names.has(f.name))]
    })
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'text/csv': ['.csv'],
      'text/plain': ['.txt'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
    },
    maxSize: 50 * 1024 * 1024,
  })

  const remove = (name) => setSelectedFiles(prev => prev.filter(f => f.name !== name))

  const handleUpload = async () => {
    if (!selectedFiles.length) return
    const sessionId = await upload(selectedFiles)
    if (sessionId) onComplete(sessionId)
  }

  return (
    <div className="max-w-2xl mx-auto mt-16 px-4">
      <div className="text-center mb-10">
        <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-[#e94560]/15 border border-[#e94560]/30 mb-4">
          <Upload size={26} className="text-[#e94560]" />
        </div>
        <h2 className="text-2xl font-bold text-white mb-2">Upload Business Documents</h2>
        <p className="text-gray-400 text-sm">Upload CSV, PDF, DOCX, or TXT files for AI-powered strategy analysis</p>
      </div>

      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-2xl p-10 text-center cursor-pointer transition-all ${
          isDragActive
            ? 'border-[#e94560] bg-[#e94560]/5'
            : 'border-[#1f2d4e] hover:border-[#e94560]/50 hover:bg-white/[0.02]'
        }`}
      >
        <input {...getInputProps()} />
        <FileText size={36} className="mx-auto mb-3 text-gray-500" />
        <p className="text-white font-medium mb-1">
          {isDragActive ? 'Drop files here…' : 'Drag & drop files here'}
        </p>
        <p className="text-gray-500 text-sm">or click to browse • PDF, CSV, DOCX, TXT • Max 50MB</p>
      </div>

      {selectedFiles.length > 0 && (
        <div className="mt-4 space-y-2">
          {selectedFiles.map(file => {
            const ext = file.name.split('.').pop().toLowerCase()
            return (
              <div key={file.name} className="flex items-center justify-between bg-[#0f1929] border border-[#1f2d4e] rounded-xl px-4 py-3">
                <div className="flex items-center gap-3">
                  <span className="text-xl">{FILE_ICONS[ext] || '📁'}</span>
                  <div>
                    <p className="text-white text-sm font-medium">{file.name}</p>
                    <p className="text-gray-500 text-xs">{fmt(file.size)}</p>
                  </div>
                </div>
                {!uploading && (
                  <button onClick={() => remove(file.name)} className="text-gray-500 hover:text-[#e94560] transition-colors">
                    <X size={16} />
                  </button>
                )}
              </div>
            )
          })}
        </div>
      )}

      {error && (
        <div className="mt-3 flex items-center gap-2 text-red-400 text-sm bg-red-900/20 border border-red-700/30 rounded-xl px-4 py-3">
          <AlertCircle size={15} /> {error}
        </div>
      )}

      {uploading && (
        <div className="mt-4">
          <div className="flex justify-between text-xs text-gray-400 mb-1.5">
            <span>Uploading & indexing…</span><span>{progress}%</span>
          </div>
          <div className="h-1.5 bg-[#1f2d4e] rounded-full overflow-hidden">
            <div className="h-full bg-[#e94560] rounded-full transition-all duration-300" style={{ width: `${progress}%` }} />
          </div>
        </div>
      )}

      <button
        onClick={handleUpload}
        disabled={!selectedFiles.length || uploading}
        className="mt-6 w-full py-3.5 rounded-xl font-semibold text-sm transition-all flex items-center justify-center gap-2 disabled:opacity-40 disabled:cursor-not-allowed bg-[#e94560] hover:bg-[#ff6b80] text-white"
      >
        {uploading
          ? <><Loader2 size={16} className="animate-spin" /> Processing…</>
          : <><CheckCircle size={16} /> Analyze Documents</>
        }
      </button>
    </div>
  )
}
