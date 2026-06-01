export default function InsightCard({ number, text }) {
  return (
    <div className="flex gap-3 bg-[#0f1929] border border-[#1f2d4e] rounded-xl p-4">
      <div className="w-6 h-6 rounded-full bg-[#e94560]/20 text-[#e94560] text-xs font-bold flex items-center justify-center flex-shrink-0 mt-0.5">
        {number}
      </div>
      <p className="text-gray-300 text-sm leading-relaxed">{text}</p>
    </div>
  )
}
