# Changelog

All notable changes to the CMO Network Intelligence Dashboard project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Phase 3: 数据实时同步与生产环保
- 实时 WebSocket 推送
- 认证与权限管理
- 多租户支持

---

## [0.2.0] - 2026-05-20

### Added - Phase 2: 前端大屏完成

#### 前端组件
- Next.js 14 暗色主题大屏骨架
- Leaflet 地图集成（CartoDB 暗色瓦片）
- 站点着色引擎（基于覆盖质量评分）
- 城市边界 GeoJSON 加载

#### 卡片与可视化
- **用户卡片**: 全网在网用户、日净增、流失最高城市（3 家竞对对标）
- **体验卡片**: 体验评分（5.2/10 示例）、对标Claro、覆盖质量等级、告警指示
- **终端卡片**: 高价值用户分布、设备类型占比
- **流失竞对卡片**: 流失最高城市、竞对对标、归因分析
- **APP 体验带**: YouTube/Netflix/TikTok 实时体验监控、流量分布柱状图

#### 下钻与诊断
- 城市详情页面（支持5城市+农村下钻）
- 自动诊断：基于体验评分自动提示问题
- 六维流失归因：网络质量、覆盖、竞对、品牌、价格、其他
- 竞对对标表（Claro vs Tigo）

#### 页面与路由
- Dashboard 首页（`/`）
- 城市下钻页面（`/city/[city_name]`）
- 自动路由与 TypeScript 类型安全

### Backend Changes
- 11 个 API 端点完全实现
- 数据缓存优化
- 错误处理与日志完善

### Testing
- 前端：组件渲染测试（Vitest）
- 后端：24 个单元测试全通过（pytest）
- Build 验证：Next.js build 零错误

### Documentation
- PHASE2_PLAN.md：前端详细实现方案
- FRONTEND_STATUS.md：实时开发进度
- 组件 JSDoc 注释完整

### Fixed
- 地图展示性能优化
- 暗色主题配色一致性

---

## [0.1.0] - 2026-05-19

### Added - Phase 1: 数据与后端完成

#### 数据生成
- **gen_sites.py**: 400 个基站（5城市+农村分布）
  - Bogotá, Cali, Medellín, Barranquilla, Cartagena
  - 各站点包含坐标、覆盖半径、设备类型
  
- **gen_kpi.py**: 152K 条无线+网络KPI
  - 指标：SINR、CQI、PDCP、RLC、MAC 吞吐量等
  - 按时间序列、站点、城市组织
  
- **gen_ookla.py**: 22K 条 Ookla 测速数据
  - 3 家运营商：Tigo、Claro、Movistar
  - 下载速率、上传速率、延迟、抖动
  
- **gen_dpi.py**: 76K 条探针 DPI 数据
  - YouTube、Netflix、TikTok、WhatsApp、其他
  - 体验质量等级分布
  
- **gen_churn.py**: 15K 条用户流失数据
  - 流失归因：网络质量、覆盖、竞对、品牌、价格
  - 按城市、时间分组
  
- **gen_coverage.py**: 覆盖质量指标
  - 信号强度、SINR、覆盖率、边缘覆盖
  
- **gen_terminals.py**: 终端分布
  - 高价值用户比例、设备类型占比
  
- **gen_population.py**: 人口栅格（1,300 个）
  - 经纬度、人口数、城市标签

#### 计算引擎
- **experience_score.py**: 体验评分引擎
  - 聚合 KPI + DPI，输出 0-10 分
  - 自动生成告警
  
- **churn_attribution.py**: 流失归因引擎
  - 多维分析流失原因
  - 支持城市级下钻
  
- **competitiveness.py**: 竞争力对标
  - Tigo vs Claro vs Movistar
  - 多维度对比矩阵
  
- **potential_score.py**: 潜力评分
  - 人口 × Ookla 竞对速率 × 未覆盖
  - 输出投资优先级

#### FastAPI 后端
- **main.py**: 11 个 API 端点
  - `/api/overview`: 总览 KPI
  - `/api/sites`: 站点列表
  - `/api/ookla`: Ookla 数据
  - `/api/coverage`: 覆盖质量
  - `/api/terminals`: 终端分布
  - `/api/churn`: 流失分析
  - `/api/potential`: 潜力评分
  - `/api/competitiveness`: 竞争力
  - `/api/experience`: 体验数据
  - `/api/drilldown/{city}`: 城市下钻
  - `/health`: 健康检查

#### Testing
- 24 个单元测试（pytest）
  - 数据生成验证
  - 引擎计算正确性
  - API 端点测试
  - 数据格式验证
- 所有测试通过 ✓

#### Documentation
- PRD.md: 完整产品需求
- ARCHITECTURE.md: 系统设计（81KB）
- ITERATION_PLAN.md: 开发计划
- 后端代码注释完整

### Technical Details
- **数据量**: ~300K 记录
- **响应时间**: API 平均 <50ms
- **测试覆盖**: 84% 代码覆盖率
- **Python 版本**: 3.9+
- **依赖**: fastapi, uvicorn, httpx, pandas, numpy

---

## [0.0.0] - 2026-05-18

### Initial Setup
- 项目初始化
- Git 仓库创建
- 开发环境配置
