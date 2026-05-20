# ITERATION PLAN: CMO Dashboard Demo — Phase 1 数据模拟 + 后端

> **关联 PRD**: PRD-CMOD-001 (状态: ✅ Approved)
> **Date**: 2026-05-19
> **Base Commit**: `b9c2c43`

---

## 0. 全局开发计划

| Phase | 目标 | 天数 |
|:---|:---|:---|
| **1 数据模拟 + 后端** | 8 类模拟数据 + 计算引擎 + API | 4-5 天 |
| 2 前端大屏 | 5 个 Tab + 下钻 + 地图 | 5-7 天 |
| 3 联调部署 | 前后端联调 + Vercel 部署 | 2-3 天 |

**本计划覆盖 Phase 1。** 以下任务按依赖关系分批，可并行的标注。

---

## 1. 任务清单

### 批次 A：基础数据生成（并行，3 个 Agent 同时）

#### T-01: 公参数据生成
- **优先级**: P0
- **依赖**: 无
- **并行**: 可与 T-02、T-03 并行
- **涉及文件**: `data/generators/gen_sites.py`, `data/sites.json`
- **验收标准**:
  - 5 城市 ~400 站点，真实经纬度范围
  - Bogotá(4.55~4.75, -74.15~-74.00), Medellín(6.18~6.30, -75.62~-75.52), Cali(3.38~3.48, -76.56~-76.48), Barranquilla(10.95~11.02, -74.82~-74.76), Cartagena(10.38~10.44, -75.55~-75.49)
  - 每站含: site_id, name, lat, lon, city, department, region, site_type, bands, technology, vendor, status
  - 输出 JSON，可被后续脚本引用

#### T-02: 无线 + 网络 KPI 数据生成
- **优先级**: P0
- **依赖**: T-01（需要站点列表）
- **并行**: T-01 完成后立即启动，与 T-03 并行
- **涉及文件**: `data/generators/gen_kpi.py`, `data/radio_kpi.json`, `data/network_kpi.json`
- **验收标准**:
  - 400 站 × 24h × 30 天 = ~288K 条
  - 日内波动模式：早 6 点低谷 → 中午高峰 → 下午回落 → 晚 8-10 点最高峰 → 凌晨低谷
  - 周末 vs 工作日差异
  - 5-8 个站点模拟体验恶化趋势（PRB 持续上升）
  - Barranquilla/Cartagena 整体体验低于 Bogotá/Medellín

#### T-03: Ookla 测速数据生成
- **优先级**: P0
- **依赖**: T-01（需要站点位置做距离关联）
- **并行**: T-01 完成后立即启动，与 T-02 并行
- **涉及文件**: `data/generators/gen_ookla.py`, `data/ookla.json`
- **验收标准**:
  - 三家运营商（Tigo/Claro/Movistar），2 季度（Q4'25 + Q1'26），~8K 条/季度
  - 每条含: test_id, timestamp, lat, lon, city, operator, technology, download_mbps, upload_mbps, latency_ms, jitter_ms, signal_strength_dbm(-70~-150), device_model, period
  - 城市级竞争差异: Tigo 在 Bogotá/Medellín 强，Barranquilla/Cartagena 弱；Claro 整体略强
  - 信号强度与距离最近站点正相关
  - RSRP 按 10dB 分档分布合理

---

### 批次 B：业务数据生成（并行，与批次 A 的 T-02/T-03 同时或紧随其后）

#### T-04: 探针 DPI 数据生成
- **优先级**: P0
- **依赖**: T-01
- **并行**: 可与 T-02、T-03、T-05 并行
- **涉及文件**: `data/generators/gen_dpi.py`, `data/dpi.json`
- **验收标准**:
  - 400 站 × 24h × 30 天，每条含 APP 流量分布 + 视频体验
  - APP 分布: YouTube/Netflix/TikTok/WhatsApp/Instagram/Gaming/Other
  - 视频体验: YouTube 和 Netflix 各自的 HD 占比、卡顿率、首次缓冲
  - 高峰期（18-22 点）HD 占比从 55% 降至 25%，卡顿率从 0.8% 升至 4.5%
  - 与 PRB 利用率关联（PRB>80% 时视频降质）

#### T-05: IMSI 流失数据 + MR 覆盖数据 + 终端数据 + 人口栅格
- **优先级**: P0
- **依赖**: T-01、T-02（需要站点和 KPI 做关联）
- **并行**: T-01/T-02 完成后启动
- **涉及文件**: `data/generators/gen_churn.py`, `data/generators/gen_coverage.py`, `data/generators/gen_terminals.py`, `data/generators/gen_population.py`, `data/churn.json`, `data/coverage.json`, `data/terminals.json`, `data/population.json`
- **验收标准**:
  - IMSI 流失: ~15K 离网用户/月，含活动区域、体验评分、ARPU、终端级别；体验差区域流失率 3.5%，体验好区域 0.5%
  - MR 覆盖: 每站点 RSRP 分层（核心≥-85 / 中间-85~-105 / 边缘<-105），Bogotá 边缘 15%，Barranquilla 边缘 32%
  - 终端: 4 级分布（旗舰 15% / 高端 21% / 中端 35% / 入门 29%），含 ARPU、速率倍数、边缘占比
  - 人口栅格: 5 城市 ~5K 个 500m×500m 栅格，含人口密度

---

### 批次 C：计算引擎 + API（依赖批次 A+B 数据）

#### T-06: 计算引擎
- **优先级**: P0
- **依赖**: T-01 ~ T-05 全部完成
- **涉及文件**: `backend/engines/experience_score.py`, `backend/engines/churn_attribution.py`, `backend/engines/competitiveness.py`, `backend/engines/potential_score.py`
- **验收标准**:
  - 体验评分: 五维加权（下行30%+时延25%+PRB20%+接通率15%+掉线率10%），输出 0-5 分
  - 流失归因: 离网用户体验 vs 全网对比 → 自动判定网络因素占比
  - 竞争力: Tigo 速率 / max(竞对) 按栅格计算
  - 潜力评分: 人口35%+覆盖缺口30%+竞对活跃20%+收入15%
  - 单元测试 ≥15 个

#### T-07: FastAPI 后端 API
- **优先级**: P0
- **依赖**: T-06
- **涉及文件**: `backend/main.py`, `backend/api/`
- **验收标准**:
  - `GET /api/overview` — 总览 KPI 卡片数据
  - `GET /api/users?city=&period=` — 用户趋势
  - `GET /api/experience?city=&period=` — 体验趋势 + 竞对对比
  - `GET /api/coverage?city=` — 覆盖质量分布
  - `GET /api/apps?city=&hour=` — 业务/APP 数据
  - `GET /api/terminals?city=` — 终端分布
  - `GET /api/churn?city=` — 流失分析
  - `GET /api/potential?city=` — 潜力分析
  - `GET /api/ookla?city=&operator=&period=` — Ookla 竞对数据
  - `GET /api/sites` — 站点列表
  - `GET /api/drilldown/{city}` — 城市下钻聚合数据
  - 所有端点返回 JSON，格式与前端约定一致
  - 单元测试 ≥10 个

---

## 2. 并行策略

```
批次 A（3 个 Agent 并行）
│
├── Agent A: T-01 公参数据（先跑，2h）
│   完成后 →
│   ├── Agent B: T-02 无线+网络 KPI（4h）
│   └── Agent C: T-03 Ookla 数据（4h）
│
├── 同时 Agent D: T-04 探针 DPI（依赖 T-01，4h）
│
└── T-01+T-02 完成后 → Agent E: T-05 流失+覆盖+终端+人口（3h）

批次 C（串行）
│
├── T-06 计算引擎（依赖全部数据，4h）
└── T-07 API（依赖 T-06，4h）
```

---

## 3. QA 门禁

| 检查项 | 命令 | 预期 |
|:---|:---|:---|
| 测试通过 | `pytest backend/tests/ -v` | 0 failures |
| Lint | `ruff check backend/ data/` | 0 errors |
| 数据完整性 | `python data/validate.py` | 所有 JSON 格式正确、数量达标 |
| API 可用 | `uvicorn backend.main:app` + curl 测试 | 所有端点返回 200 |

---

## 4. 交付清单

| 交付物 | 状态 |
|:---|:---|
| 8 类模拟数据 JSON | ⬜ |
| 4 个计算引擎 | ⬜ |
| 11 个 API 端点 | ⬜ |
| 测试 ≥25 个全通过 | ⬜ |
| 数据验证脚本 | ⬜ |
