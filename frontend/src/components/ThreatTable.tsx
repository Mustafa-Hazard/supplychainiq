import { useEffect, useMemo, useState } from 'react'
import { getThreats } from '../api'
import type { Threat } from '../types'

type SortKey = 'priority_score' | 'published_at'
type SortDir = 'asc' | 'desc'

function severityColor(score: number): string {
  if (score >= 7) return 'bg-[#C97B4A]'
  if (score >= 5) return 'bg-[#8A8578]'
  return 'bg-[#8A8578]/40'
}

function formatDate(iso: string | null): string {
  if (!iso) return '—'
  return iso.slice(0, 10)
}

function ThreatTable() {
  const [threats, setThreats] = useState<Threat[]>([])
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const [sortKey, setSortKey] = useState<SortKey>('priority_score')
  const [sortDir, setSortDir] = useState<SortDir>('desc')
  const [tagFilter, setTagFilter] = useState<string>('all')

  useEffect(() => {
    let ignore = false

    getThreats()
      .then((res) => {
        if (!ignore) setThreats(res.threats.slice(0, 50))
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

  const availableTags = useMemo(() => {
    const tags = new Set<string>()
    threats.forEach((t) => {
      if (t.tags) tags.add(t.tags)
    })
    return Array.from(tags).sort()
  }, [threats])

  const filtered = useMemo(() => {
    let rows = threats
    if (tagFilter === 'untagged') {
      rows = rows.filter((t) => !t.tags)
    } else if (tagFilter !== 'all') {
      rows = rows.filter((t) => t.tags === tagFilter)
    }

    return [...rows].sort((a, b) => {
      let cmp = 0
      if (sortKey === 'priority_score') {
        cmp = a.priority_score - b.priority_score
      } else {
        const aTime = a.published_at ? new Date(a.published_at).getTime() : 0
        const bTime = b.published_at ? new Date(b.published_at).getTime() : 0
        cmp = aTime - bTime
      }
      return sortDir === 'asc' ? cmp : -cmp
    })
  }, [threats, tagFilter, sortKey, sortDir])

  function toggleSort(key: SortKey) {
    if (sortKey === key) {
      setSortDir(sortDir === 'asc' ? 'desc' : 'asc')
    } else {
      setSortKey(key)
      setSortDir('desc')
    }
  }

  function sortIndicator(key: SortKey) {
    if (sortKey !== key) return ''
    return sortDir === 'asc' ? ' ↑' : ' ↓'
  }

  return (
    <section className="border border-[#8A8578]/30 rounded-md p-6">
      <div className="flex items-baseline justify-between mb-4">
        <h2 className="font-condensed text-xl tracking-tight text-[#EDEAE2]">
          Top Threats
        </h2>
        <div className="flex items-center gap-3">
          {threats.length > 0 && (
            <span className="font-mono text-xs text-[#8A8578]">
              showing top {filtered.length} of {threats.length}
            </span>
          )}
          <select
            value={tagFilter}
            onChange={(e) => setTagFilter(e.target.value)}
            className="font-mono text-xs bg-transparent border border-[#8A8578]/40 rounded px-2 py-1 text-[#EDEAE2]"
          >
            <option value="all" className="bg-[#1A1815] text-[#EDEAE2]">all tags</option>
            <option value="untagged" className="bg-[#1A1815] text-[#EDEAE2]">untagged</option>
            {availableTags.map((tag) => (
              <option key={tag} value={tag} className="bg-[#1A1815] text-[#EDEAE2]">
                {tag}
              </option>
            ))}
          </select>
        </div>
      </div>

      {loading && (
        <p className="font-mono text-sm text-[#8A8578]">loading threats...</p>
      )}

      {error && (
        <p className="font-mono text-sm text-[#C97B4A]">
          failed to load threats: {error}
        </p>
      )}

      {!loading && !error && (
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-[#8A8578]/30 text-left">
              <th
                className="font-mono text-xs text-[#8A8578] font-normal py-2 pr-4 cursor-pointer select-none"
                onClick={() => toggleSort('priority_score')}
              >
                priority{sortIndicator('priority_score')}
              </th>
              <th className="font-mono text-xs text-[#8A8578] font-normal py-2 pr-4">
                title
              </th>
              <th className="font-mono text-xs text-[#8A8578] font-normal py-2 pr-4">
                source
              </th>
              <th className="font-mono text-xs text-[#8A8578] font-normal py-2 pr-4">
                tag
              </th>
              <th
                className="font-mono text-xs text-[#8A8578] font-normal py-2 cursor-pointer select-none"
                onClick={() => toggleSort('published_at')}
              >
                published{sortIndicator('published_at')}
              </th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((t) => (
              <tr key={t.id} className="border-b border-[#8A8578]/10">
                <td className="py-2 pr-4">
                  <span className="flex items-center gap-2 font-mono text-xs text-[#EDEAE2]">
                    <span
                      className={`w-2 h-2 rounded-full ${severityColor(t.priority_score)}`}
                    />
                    {t.priority_score.toFixed(2)}
                  </span>
                </td>
                <td className="py-2 pr-4 text-[#EDEAE2]/90 max-w-[400px] truncate">
                  {t.title}
                </td>
                <td className="py-2 pr-4 font-mono text-xs text-[#8A8578]">
                  {t.source}
                </td>
                <td className="py-2 pr-4">
                  {t.tags ? (
                    <span className="font-mono text-[10px] uppercase tracking-wider border border-[#8A8578]/40 rounded px-2 py-0.5 text-[#8A8578]">
                      {t.tags}
                    </span>
                  ) : (
                    <span className="font-mono text-[10px] text-[#8A8578]/50">
                      untagged
                    </span>
                  )}
                </td>
                <td className="py-2 font-mono text-xs text-[#8A8578]">
                  {formatDate(t.published_at)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </section>
  )
}

export default ThreatTable
