// Matches app/routers/threats.py _serialize()
export interface Threat {
  id: number
  source: string
  external_id: string
  title: string
  description: string
  indicators: string
  tags: string
  priority_score: number
  published_at: string | null
  pulled_at: string
}

export interface ThreatsResponse {
  count: number
  threats: Threat[]
}

// Matches app/routers/summary.py
export interface SummaryResponse {
  generated_by: 'gemini' | 'groq' | 'static'
  summary: string
  based_on_count: number
}

// Matches app/services/trends.py get_weekly_trend()
export interface TrendWeek {
  week_start: string
  otx: number
  kev: number
  total: number
}

export interface TrendsResponse {
  trend: TrendWeek[]
  excluded_null_count: number
}
