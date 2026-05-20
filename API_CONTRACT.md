# CMO Dashboard - Frontend API Contract

## Overview
All components are integrated with real API data support while maintaining mock data fallback. When the backend API is unavailable, components automatically display mock data without errors.

## API Base URL
```
http://localhost:8000
```

## Endpoints & Field Mappings

### 1. `/api/overview` (UserCards Component)
**Response Fields:**
```json
{
  "total_users_estimate": <number>,  // in users (e.g., 12500000)
  "mom_change_pct": <number>,        // % change (e.g., 2.3)
  "daily_net_new": <number>,         // net new users/day (e.g., 28000)
  "daily_new": <number>,             // new users/day (e.g., 45000)
  "daily_churn": <number>,           // churned users/day (e.g., 17000)
  "worst_churn_city": <string>,      // city name (e.g., "Barranquilla")
  "worst_churn_rate": <number>       // churn rate % (e.g., 2.1)
}
```

**Component Rendering:**
- total_users_estimate (÷1M, 1 decimal) → "12.5M"
- mom_change_pct → "+2.3%"
- daily_net_new (÷1000) → "+28K"
- daily_new (÷1000) → "+45K"
- daily_churn (÷1000, negative) → "-17K"
- worst_churn_city → link href & display
- worst_churn_rate → "2.1%"

### 2. `/api/experience` (ExperienceCards Component)
**Response Fields:**
```json
{
  "experience_score": <number>,       // 0-5 scale (e.g., 4.2)
  "mom_change": <number>,             // score change (e.g., 0.2)
  "vs_claro_gap": <number>,           // % gap (e.g., -8)
  "edge_user_pct": <string>,          // % string (e.g., "20%")
  "weak_signal_users_m": <number>,    // users in millions (e.g., 2.5)
  "alert_cities": <number>            // count (e.g., 3)
}
```

**Component Rendering:**
- experience_score (1 decimal) → "4.2"
- mom_change → "+0.2"
- vs_claro_gap → "-8%"
- edge_user_pct → "20%"
- weak_signal_users_m (formatted) → "2.5M"
- alert_cities → "3"

### 3. `/api/churn` (ChurnCards Component)
**Response Fields:**
```json
{
  "monthly_churn": <number>,          // count (e.g., 15200)
  "mom_change_pct": <number>,         // % change (e.g., 8)
  "network_factor_pct": <string>,     // % string (e.g., "62%")
  "tigo_speed_mbps": <number>,        // Mbps (e.g., 38)
  "claro_speed_mbps": <number>,       // Mbps (e.g., 42)
  "movistar_speed_mbps": <number>     // Mbps (e.g., 28)
}
```

**Component Rendering:**
- monthly_churn (÷1000, 1 decimal) → "15.2K"
- mom_change_pct → "+8%"
- network_factor_pct → "62%"
- tigo_speed_mbps → "38 Mbps"
- claro_speed_mbps → "42 Mbps"
- movistar_speed_mbps → "28 Mbps"

### 4. `/api/terminals` (TerminalCards Component)
**Response Fields:**
```json
{
  "premium_users": <number>,          // count (e.g., 4500000)
  "premium_pct": <string>,            // % string (e.g., "36%")
  "premium_revenue_pct": <string>,    // % string (e.g., "68%")
  "uncovered_pop": <number>,          // count (e.g., 11500000)
  "high_potential": <number>,         // count (e.g., 4200000)
  "yearly_revenue": <number>          // millions (e.g., 180)
}
```

**Component Rendering:**
- premium_users (÷1M, 1 decimal) → "4.5M"
- premium_pct → "36%"
- premium_revenue_pct → "68%"
- uncovered_pop (÷1M, 1 decimal) → "11.5M"
- high_potential (÷1M, 1 decimal) → "4.2M"
- yearly_revenue → "$180M/年"

## Error Handling
- All API calls wrap in try-catch
- Network failures return `null`
- Component detects null and uses pre-defined MOCK_DATA
- Console warnings logged for debugging (check browser DevTools)

## Testing the Integration

### When API is DOWN (current state):
```bash
npm run dev
# Components display mock data automatically
```

### When API is UP:
```bash
# Start backend on http://localhost:8000
npm run dev
# Components fetch from API and display real data
# No code changes needed
```

## Implementation Details

### src/lib/api.ts
```typescript
export async function fetchAPI(endpoint: string) {
  try {
    const res = await fetch(`${API_BASE}${endpoint}`, { cache: 'no-store' })
    if (!res.ok) throw new Error(`${res.status}`)
    return await res.json()
  } catch (error) {
    console.warn(`Failed to fetch ${endpoint}:`, error)
    return null  // Signals component to use fallback
  }
}
```

### Component Pattern
```typescript
const MOCK_DATA = { /* fallback values */ }

export default function ComponentName() {
  const [data, setData] = useState(MOCK_DATA)
  
  useEffect(() => {
    async function load() {
      const response = await fetchAPI('/api/endpoint')
      if (response) {
        setData({ /* transform response */ })
      }
    }
    load()
  }, [])
  
  return ( /* render using data */ )
}
```

## Validation Checklist
- [x] All components have MOCK_DATA constants
- [x] All components use useState with MOCK_DATA initial value
- [x] All components call fetchAPI in useEffect on mount
- [x] fetchAPI returns null on errors, never throws
- [x] Components handle null gracefully with fallback
- [x] .env.local configured with API_BASE
- [x] npm run build passes without errors
- [x] No TypeScript errors

## Notes
- Cache disabled (`cache: 'no-store'`) to ensure fresh data on each request
- Field mapping handles both presence and absence of fields gracefully
- All number formatting (M, K, %, Mbps) done client-side
- Components remain fully functional even if backend is completely unavailable
