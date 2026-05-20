# CMO Network Intelligence Dashboard

为运营商 CMO 提供的网络智能决策大屏，整合公参、无线KPI、网络KPI、探针DPI、Ookla测速、用户流失六层数据，从用户、体验、业务、终端、潜力五个维度支撑决策。

## 目标客户

Tigo Colombia (Millicom)

## 技术栈

- **前端**: Next.js 14 + TypeScript + Tailwind CSS + Leaflet + ECharts
- **后端**: FastAPI + Python
- **数据**: 模拟数据（JSON），可替换为真实数据源

## 快速启动

### 后端

```bash
# 安装依赖
pip install fastapi uvicorn httpx

# 生成模拟数据（如果 data/ 下 JSON 不存在）
python3 data/generators/gen_sites.py
python3 data/generators/gen_kpi.py
python3 data/generators/gen_ookla.py
python3 data/generators/gen_dpi.py
python3 data/generators/gen_churn.py
python3 data/generators/gen_coverage.py
python3 data/generators/gen_terminals.py
python3 data/generators/gen_population.py

# 运行计算引擎（预计算各类指标）
python3 backend/engines/experience_score.py
python3 backend/engines/churn_attribution.py
python3 backend/engines/competitiveness.py
python3 backend/engines/potential_score.py

# 启动 API 服务
uvicorn backend.main:app --reload
# API 访问地址: http://localhost:8000
```

### 前端

```bash
cd frontend
npm install
npm run dev
# 访问 http://localhost:3000
```

## 大屏布局

```
┌──────────────────────────────────────────────┐
│  左上：用户  │  中央：地图  │  右上：体验     │
│  左下：终端  │  (站点着色)  │  右下：流失     │
├──────────────┴──────────────┴────────────────┤
│  底部：YouTube | Netflix | TikTok | 流量分布  │
└──────────────────────────────────────────────┘
```

## 五个分析维度

| 维度 | 内容 | 关键指标 |
|------|------|---------|
| **用户** | 全网趋势→城市下钻→流失归因 | 在网用户、日净增、流失最高城市 |
| **体验** | 纵向跟自己比→横向跟对手比→覆盖质量 | 体验评分、对标Claro、覆盖质量 |
| **业务** | APP流量→视频体验→时间/空间分析 | YouTube/Netflix/TikTok体验 |
| **终端** | 高价值用户→体验→覆盖→竞对对标 | 终端分布、高价值用户覆盖 |
| **潜力** | 人口×Ookla竞对→未覆盖区域→投资建议 | 潜力评分、投资优先级 |

## 数据规模（模拟）

| 数据 | 量级 |
|------|------|
| 站点 | 400 站（5城市+农村） |
| 无线+网络KPI | 152K 条 |
| Ookla 测速 | 22K 条（3家运营商） |
| 探针 DPI | 76K 条 |
| 流失用户 | 15K 条 |
| 人口栅格 | 1,300 个 |

## API 端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/overview` | GET | 总览 KPI（全网在网用户、日净增、流失最高城市） |
| `/api/sites` | GET | 站点列表（支持城市过滤） |
| `/api/ookla` | GET | Ookla 竞对数据（支持运营商、城市过滤） |
| `/api/coverage` | GET | 覆盖质量指标 |
| `/api/terminals` | GET | 终端分布数据 |
| `/api/churn` | GET | 流失分析数据 |
| `/api/potential` | GET | 潜力评分数据 |
| `/api/competitiveness` | GET | 竞争力对标 |
| `/api/experience` | GET | 体验评分数据 |
| `/api/drilldown/{city}` | GET | 城市下钻（含六维自动诊断） |

## 项目文档

- **PRD**: `PRD.md` - 产品需求文档
- **架构设计**: `ARCHITECTURE.md` - 系统设计与数据流
- **迭代计划**: `ITERATION_PLAN.md` - 开发阶段规划
- **Phase 2 计划**: `PHASE2_PLAN.md` - 前端大屏实现方案
- **前端进度**: `FRONTEND_STATUS.md` - 实时开发状态

## 测试

### 后端测试

```bash
cd backend
python -m pytest tests/ -v
# 预期: 24 个测试全通过
```

### 前端 Build

```bash
cd frontend
npm run build
# 预期: 零错误
```

## 目录结构

```
cmo-dashboard/
├── backend/                    # FastAPI 后端
│   ├── main.py                # API 入口
│   ├── engines/               # 计算引擎（体验评分/流失归因等）
│   ├── tests/                 # 单元测试
│   └── config.py              # 配置
├── frontend/                  # Next.js 前端
│   ├── src/
│   │   ├── app/              # 页面
│   │   ├── components/       # React 组件
│   │   └── lib/              # 工具函数
│   └── public/               # 静态资源
├── data/                      # 模拟数据
│   ├── generators/           # 数据生成脚本
│   ├── *.json                # 生成的数据集
└── docs/                      # 文档
```

## 核心功能

### Phase 1: 数据与计算
- 8 类模拟数据生成器（公参、无线KPI、网络KPI、Ookla、探针DPI、流失、覆盖、终端、人口）
- 4 个计算引擎（体验评分、流失归因、竞争力评分、潜力评分）
- 完整的 FastAPI 后端，支持 11 个数据接口

### Phase 2: 前端大屏
- 暗色主题的现代化大屏设计
- 交互式 Leaflet 地图（站点着色展示覆盖质量）
- 5 个核心卡片（用户、体验、终端、流失、竞对）
- 4 个 APP 体验监控（YouTube、Netflix、TikTok、流量分布）
- 城市下钻页面，支持 6 维自动诊断
- 实时数据同步，支持多粒度筛选

## 开发规范

- **语言**: TypeScript（前后端）
- **代码风格**: Prettier + ESLint
- **提交规范**: Conventional Commits
- **版本管理**: 语义化版本控制

## 贡献

欢迎通过 Issue 和 PR 贡献！请确保：
1. 通过所有测试
2. 遵循代码风格
3. 更新相关文档

## 许可证

Proprietary - Millicom/Tigo Colombia
