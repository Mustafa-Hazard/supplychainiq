import { useEffect, useState } from 'react'
import { getSummary } from '../api'
import type { SummaryResponse } from '../types'

const TIER_STYLES: Record<SummaryResponse['generated_by'], string> = {
  gemini: 'text-[#8A8578] border-[#8A8578]/40',
  groq: 'text-[#EDEAE2] border-[#EDEAE2]/40',
  static: 'text-[#C97B4A] border-[#C97B4A]/40',
}

function SummaryPanel() {
  const [data, setData] = useState<SummaryResponse | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let ignore = false

    getSummary()
      .then((res) => {
        if (!ignore) setData(res)
      })
      .catch((e: Error) => {
        if (!ignore) setError(e.message)
      })
      .finally(() => {
        if (!ignore) setLoading(false)
      })

    return () => {
      ignore = true
    }
  }, [])

  return (
    <section className="border border-[#8A8578]/30 rounded-md p-6">
      <div className="flex items-baseline justify-between mb-4">
        <h2 className="font-condensed text-xl tracking-tight text-[#EDEAE2]">
          Daily Briefing
        </h2>
        {data && (
          <span
            className={`font-mono text-[10px] uppercase tracking-wider border rounded px-2 py-0.5 ${TIER_STYLES[data.generated_by]}`}
          >
            {data.generated_by}
          </span>
        )}
      </div>

      {loading && (
        <p className="font-mono text-sm text-[#8A8578]">loading briefing...</p>
      )}

      {error && (
        <p className="font-mono text-sm text-[#C97B4A]">
          failed to load summary: {error}
        </p>
      )}

      {data && (
        <>
          <p className="text-sm leading-relaxed text-[#EDEAE2]/90 whitespace-pre-line">
            {data.summary}
          </p>
          <p className="font-mono text-xs text-[#8A8578] mt-4">
            based on top {data.based_on_count} threats
          </p>
        </>
      )}
    </section>
  )
}

export default SummaryPanel
