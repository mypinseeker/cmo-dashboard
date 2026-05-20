# CMO Dashboard Frontend - Quick Start Guide

## Startup

```bash
cd frontend
npm run dev
```

Open http://localhost:3000 in browser.

## Commands

- `npm run dev` - Start development server (http://localhost:3000)
- `npm run build` - Create production build
- `npm start` - Run production server
- `npm run lint` - Check code quality

## Directory Structure

```
src/
├── app/
│   ├── layout.tsx    - Root layout with dark theme
│   ├── page.tsx      - Dashboard skeleton (left/center/right + footer)
│   └── globals.css   - Tailwind directives & utilities
└── lib/
    └── api.ts        - API client (fetchAPI helper)
```

## Configuration

**Environment Variables** (`.env.local`)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Color Scheme**
- Background: `gray-950` (#0a0a0a)
- Cards: `gray-900` (#111827)
- Text: white, `gray-400`, `gray-500`
- Accent: `cyan-400` (#06b6d4)

## Dependencies

- **Maps**: Leaflet 1.9.4 + react-leaflet 5.0.0
- **Charts**: ECharts 6.1.0 + echarts-for-react 3.0.6
- **Styling**: Tailwind CSS 3.4.1
- **Framework**: Next.js 14.2.35 + React 18

## Layout Overview

```
┌─────────────────────────────────────────────┐
│  Tigo Colombia CMO Dashboard    2026-05-20  │  Header
├────────┬─────────────────────┬──────────────┤
│        │                     │              │
│ Left   │    Central Map      │   Right      │  Main
│ Cards  │                     │   Cards      │
│        │                     │              │
├────────┴─────────────────────┴──────────────┤
│  YouTube  │ Netflix │ TikTok │ Flow Chart   │  Footer
└────────────────────────────────────────────┘
```

## Next Steps

1. Build Leaflet map component
2. Build ECharts card components  
3. Connect to backend API (`/api/` endpoints)
4. Add real-time data updates
5. Implement error handling & loading states

---
**Status**: F-01 Skeleton Complete
**Created**: 2026-05-20
