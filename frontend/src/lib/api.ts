const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export async function fetchAPI(endpoint: string) {
  try {
    const res = await fetch(`${API_BASE}${endpoint}`, { cache: 'no-store' })
    if (!res.ok) throw new Error(`${res.status}`)
    return await res.json()
  } catch (error) {
    console.warn(`Failed to fetch ${endpoint}:`, error)
    return null  // Return null on failure, component uses fallback
  }
}
