# Tigo Network Dashboard — Iteration Plan
## From CMO Dashboard → Tigo Network Dashboard

> **Base**: `dashboard_v4.html` (current CMO Dashboard)
> **Output**: `tigo_network_dashboard.html` (new file, preserves original)
> **Repo**: `cmo-dashboard`

---

## Sprint Overview

| Sprint | Task | Effort | Dependency |
|--------|------|--------|------------|
| **S1** | Scaffolding: new file + 3 tabs + rename | 1h | — |
| **S2** | Grid Coverage: data generation + grid rendering | 2h | S1 |
| **S3** | Grid Coverage: heatmap mode + controls | 1h | S2 |
| **S4** | 3D Building: data + cross-section view | 2h | S1 |
| **S5** | 3D Building: CSS 3D isometric view | 2h | S4 |
| **S6** | Map integration: building markers + popup | 1h | S3+S5 |
| **S7** | Polish: i18n + responsive + testing | 1h | S6 |
| **Total** | | **~10h** | |

---

## S1: Scaffolding (1h)

**Goal**: New HTML file with 3-tab navigation, existing dashboard intact.

### Tasks
- [ ] Copy `dashboard_v4.html` → `tigo_network_dashboard.html`
- [ ] Rename all "CMO" → "Network" (title, header logo, i18n entries)
- [ ] Add top-level 3-tab navigation in header:
  ```
  [National Overview]  [Grid Coverage]  [3D Building]
  ```
- [ ] Create 3 container divs: `#view-national`, `#view-grid`, `#view-building`
- [ ] Write `switchMainView(view)` function (show/hide containers)
- [ ] Verify national view still works after restructuring

### Acceptance
- Tab switching works
- National view renders identically to current dashboard
- Grid and Building tabs show placeholder content

---

## S2: Grid Coverage — Data + Grid Mode (2h)

**Goal**: 50m×50m grid over Medellín with color-coded cells.

### Area
- Center: Medellín El Poblado (6.21, -75.575)
- 1km² area: 20×20 = 400 cells

### Tasks
- [ ] Generate mock grid data with 3 virtual cell tower seeds:
  - Tower 1: (6.2149, -75.5757) — near Building 2
  - Tower 2: (6.2080, -75.5780) — south
  - Tower 3: (6.2200, -75.5700) — northeast
  - Distance-based falloff + random noise
- [ ] Each cell: `{ row, col, lat, lon, dl, ul, rsrp }`
- [ ] Create Leaflet map in `#view-grid`, zoom 16, CartoDB dark tiles
- [ ] Render 400 `L.rectangle` with color encoding:
  | Metric | Green | Yellow | Red |
  |--------|-------|--------|-----|
  | DL | ≥50 Mbps | 10-50 | <10 |
  | UL | ≥10 Mbps | 3-10 | <3 |
  | RSRP | ≥-90 dBm | -90 to -105 | <-105 |
- [ ] Metric tab buttons: `[DL] [UL] [RSRP]`
- [ ] Cell click/hover popup: show all 3 metrics
- [ ] Right panel: statistics (avg, min, max, distribution %)
- [ ] Color legend

### Acceptance
- 400 colored rectangles visible on map
- Tab switch changes colors
- Popup shows data on click

---

## S3: Grid Coverage — Heatmap + Controls (1h)

**Goal**: Toggle between grid view and heatmap view.

### Tasks
- [ ] Implement heatmap using `L.heatLayer` (already loaded)
- [ ] View mode toggle buttons: `[Grid ✓] [Heatmap]`
- [ ] Grid mode = default
- [ ] Switching clears previous layer before adding new one
- [ ] Heatmap config: `radius:25, blur:15, maxZoom:18`
- [ ] Statistics panel updates in both modes

### Acceptance
- Toggle between grid and heatmap works smoothly
- No layer conflicts
- Heatmap shows same spatial pattern as grid

---

## S4: 3D Building — Data + Cross-Section (2h)

**Goal**: Per-floor coverage data and ECharts bar chart for 3 buildings.

### Buildings (from `data/3Dbuildingaddress`)

| ID | Address | Lat | Lon | Floors | Type |
|----|---------|-----|-----|--------|------|
| A | Cl. 17A Sur #48-35, El Poblado | 6.1891 | -75.5811 | 18 | Residential tower |
| B | Cl. 14 #50-88, El Poblado | 6.2149 | -75.5757 | 22 | Office tower |
| C | Cra. 45 #31-280, La Candelaria | 6.2440 | -75.5671 | 15 | Mixed-use |

### Data Model
```javascript
{
  id: 'A',
  name: 'Torre El Poblado Sur',
  address: 'Cl. 17A Sur #48-35',
  lat: 6.1891, lon: -75.5811,
  floors: 18,
  type: 'Residential',
  floorData: [
    { floor: 1, rsrp: -72, dl: 85, ul: 18 },  // ground: good
    { floor: 2, rsrp: -74, dl: 80, ul: 17 },
    ...
    { floor: 18, rsrp: -108, dl: 8, ul: 2 },   // top: poor
  ]
}
```

### Floor Data Generation
- RSRP degrades ~1.5 dBm per floor (building penetration loss)
- DL/UL proportional to RSRP
- Add random jitter ±3 dBm
- Ground floor boosted (street-level reflection)

### Tasks
- [ ] Define 3 building data objects with per-floor metrics
- [ ] Write `generateFloorData(floors, baseTowerDist)` function
- [ ] Build cross-section view using ECharts horizontal bar chart:
  - Y axis = floor number (1 → N)
  - X axis = metric value
  - Bar color = green/yellow/red threshold
- [ ] Building selector: 3 clickable cards (left panel)
- [ ] Metric selector: `[RSRP] [DL] [UL]`
- [ ] Floor hover: highlight bar + show detail in right panel

### Acceptance
- 3 buildings selectable
- Bar chart shows floor-by-floor data with correct colors
- Metric switching works
- Hover shows per-floor detail

---

## S5: 3D Building — CSS Isometric View (2h)

**Goal**: 3D stacked-floor visualization using CSS transforms.

### Rendering Approach
```css
.building-3d {
  transform: rotateX(55deg) rotateZ(-45deg);
  transform-style: preserve-3d;
}
.floor-slab {
  width: 140px;
  height: 90px;
  margin-bottom: 3px;
  background: var(--floor-color);
  border: 1px solid rgba(255,255,255,0.15);
  box-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}
```

### Tasks
- [ ] Create `.building-3d` container with CSS 3D perspective
- [ ] Render N floor slabs, stacked vertically with `translateZ`
- [ ] Color each slab based on metric + threshold
- [ ] Hover effect: highlight slab + tooltip (floor#, RSRP, DL, UL)
- [ ] Click: pin selection, update detail panel
- [ ] View toggle: `[3D Isometric] [Cross-Section]`
- [ ] Building switch animation (fade/slide)
- [ ] Floor number labels on side

### Acceptance
- 3D building renders correctly in Chrome/Firefox
- Color gradient visible from green (bottom) to red (top)
- Hover/click interaction works
- Toggle between 3D and cross-section is smooth

---

## S6: Map Integration — Building Markers + Popup (1h)

**Goal**: Building icons on the grid map, click to open 3D sim popup.

### Tasks
- [ ] Add 3 custom Leaflet markers on grid coverage map at building coordinates
- [ ] Marker icon: building silhouette (CSS-drawn or SVG, no external images)
- [ ] Click marker → open Leaflet popup with:
  - Building name + address
  - Mini 3D isometric preview (inline CSS, simplified 5-floor version)
  - "Open Full Simulation" button → switches to Building tab
- [ ] Or: click marker → modal overlay with full 3D view
- [ ] Markers visible in both grid and heatmap modes

### Acceptance
- 3 building markers visible on grid map
- Click opens popup with mini 3D preview
- Can navigate to full Building tab from popup

---

## S7: Polish + Integration (1h)

**Goal**: Production-ready dashboard.

### Tasks
- [ ] Add i18n entries for all new strings (zh/en)
- [ ] Test responsive: min-width 1200px
- [ ] Demo mode / storyline integration (if applicable)
- [ ] Cross-browser: Chrome, Firefox, Safari
- [ ] Performance: 400 rectangles + heatmap smooth at zoom 16
- [ ] Code cleanup: remove debug logs
- [ ] Update `CLAUDE.md` with new dashboard reference
- [ ] Git commit + push

### Acceptance
- All text bilingual
- No console errors
- Smooth interactions
- Pushed to repo

---

## Technical Notes

### Libraries (all already loaded, zero new deps)
- Leaflet 1.9.4 — grid map, heatmap
- leaflet.heat 0.2.0 — heatmap mode
- ECharts 5 — cross-section charts, statistics
- CSS 3D transforms — isometric building view

### File Structure
```
cmo-dashboard/
├── dashboard_v4.html            ← preserved (CMO Dashboard)
├── tigo_network_dashboard.html  ← NEW (Tigo Network Dashboard)
├── data/
│   ├── 3Dbuildingaddress        ← building addresses (exists)
│   ├── coverage.json            ← existing coverage data
│   └── ...
```

### Building Coordinates (geocoded)
```
A: 6.1891, -75.5811  (Cl. 17A Sur #48-35, El Poblado)
B: 6.2149, -75.5757  (Cl. 14 #50-88, El Poblado)
C: 6.2440, -75.5671  (Cra. 45 #31-280, La Candelaria)
```
