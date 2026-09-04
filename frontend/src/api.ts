import type { ThreatsResponse, SummaryResponse, TrendsResponse } from './types'

const BASE_URL = 'http://localhost:8000'

async function fetchJson<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`)
  if (!res.ok) {
    throw new Error(`${path} failed: ${res.status} ${res.statusText}`)
  }
  return res.json()
}

export function getThreats(): Promise<ThreatsResponse> {
  return fetchJson<ThreatsResponse>('/threats')
}

export function getSummary(): Promise<SummaryResponse> {
  return fetchJson<SummaryResponse>('/summary')
}

export function getTrends(): Promise<TrendsResponse> {
  return fetchJson<TrendsResponse>('/trends')
}
