# 危地马拉 Tigo FWA 投资回报率分析
## Guatemala Tigo FWA Business Case & ROI Assessment

> **背景**: Tigo Guatemala 固网（FBB）较薄弱，面临 Claro/Starlink 竞争，城区和郊区都出现新入网竞对用户。MBB 网络负荷偏高，FWA 需评估 ROI。
> **数据来源**: AI Think Tank + GSMA + Ericsson + 行业基准 + Millicom财报

---

## 1. 危地马拉 FBB 现状 — 为什么薄弱

### 1.1 数据对比

| 指标 | 危地马拉 | 哥伦比亚 | 行业基准 |
|---|---|---|---|
| 固网宽带渗透率 | **~5%** (约92万线/1870万人口) | 46% | 拉美平均 ~55% |
| Tigo 固网用户 | 720K | [待确认] | — |
| FBB 收入 | $470M (2024) | — | — |
| FBB 增长率 | **13.8% CAGR** | — | 高速增长 |
| 主要技术 | **Cable/HFC 为主** | Cable + 少量光纤 | FTTH 是趋势 |

### 1.2 Tigo 的困境

```
Tigo 固网弱的原因:
1. 历史投资侧重移动端（高 EBITDA 的移动业务优先）
2. 固网以 Cable/HFC 为主，没有大规模 FTTH 部署
3. 城区竞争加剧：Claro 推 FTTH + 5G FWA
4. 郊区新威胁：Starlink（2023年7月已进入危地马拉）
5. Millicom 刚宣布 $700M 光纤投资 — 但执行需要时间
```

### 1.3 竞争信号 — 城区和郊区都有新入网

| 区域 | 竞对动态 | 对 Tigo 的威胁 |
|---|---|---|
| **城区** (Guatemala City) | Claro FTTH 积极扩张，ISP Cablenet 竞争 | 高价值客户被抢 |
| **郊区** (Mixco, Villa Nueva) | Claro + 小型 ISP 扩展 | 新增长区域被截 |
| **农村** | Starlink 已覆盖（2023） | 卫星免基建，直接切入 |

---

## 2. FWA 方案评估

### 2.1 为什么考虑 FWA 而不是 FTTH

| 维度 | FTTH | 4G/5G FWA |
|---|---|---|
| 每用户成本 | $500-1,000 | **$300-800** |
| 部署速度 | 6-12 个月/区域 | **2-4 周/区域** |
| 时间价值 | 慢 → 市场被抢 | **快 → 抢先覆盖** |
| 技术限制 | 挖沟施工许可 | 利用现有基站 |
| 适合场景 | 城区高密度 | **郊区 + 新开发区** |

### 2.2 MBB 网络负荷约束

**关键约束**: Tigo MBB 网络负荷较高，FWA 会进一步增加负载。

| 参数 | 估算值 | 说明 |
|---|---|---|
| FWA 用户月均流量 | ~200 GB | 是移动用户的 **40 倍** |
| 每个 FWA 用户占用 PRB | 等效 3-5 个移动用户 | GSMA 数据 |
| 当前 PRB 利用率 | **估计 50-70%** (忙时) | [待实际测量确认] |
| FWA 可承载上限 | 每基站 15-30 个 FWA 用户 | 在不影响 MBB 质量的前提下 |

### 2.3 FWA 可行性判断框架

```
                 FWA 可行性 = f(三个条件)

条件1: 该区域 PRB 利用率 < 50%（有容量余量）
条件2: 该区域无 FTTH 覆盖（FWA 是唯一快速选择）
条件3: 该区域有固网需求但 Tigo 未覆盖（增量市场）

三个条件同时满足 → ✅ FWA 可行
任一条件不满足 → ⚠️ 需额外投资（扩容或选 FTTH）
```

---

## 3. 典型区域 ROI 测算

### 3.1 区域分类

| 类型 | 典型区域 | 人口密度 | MBB 负载 | FWA 可行性 |
|---|---|---|---|---|
| **A: 城区低负载** | Zone 10-15 (Guatemala City 新开发区) | 中 | 低 (PRB<40%) | ✅ 最佳 |
| **B: 郊区中负载** | Mixco, Villa Nueva, Petapa | 中高 | 中 (PRB 40-60%) | ✅ 可行（需监控） |
| **C: 城区高负载** | Zone 1-5 (Guatemala City 中心) | 高 | 高 (PRB>70%) | ❌ 需先扩容 |
| **D: 农村低负载** | Quetzaltenango 周边, Alta Verapaz | 低 | 低 (PRB<30%) | ✅ 可行但用户少 |

### 3.2 区域 A: 城区低负载区 — 最佳 ROI

**场景**: Guatemala City Zone 10-15 新开发住宅区

| 参数 | 值 | 说明 |
|---|---|---|
| 目标区域基站数 | 20 站 | 现有基站，无需新建 |
| 每站 FWA 用户 | 25 户 | PRB<40%，容量充足 |
| 总 FWA 用户 | **500 户** | 20 站 × 25 户 |
| FWA CPE 成本 | $150/台 | 华为 5G CPE Pro 批量价 |
| 安装成本 | $30/户 | 自安装为主，少量技术支持 |
| 基站改造成本 | $0 | 软件升级即可（已有 4G/5G） |
| **总投资** | **$90,000** | 500 × ($150 + $30) |
| | | |
| 月 ARPU | **Q200 (~$25)** | 参考 Tigo 当前 FBB 定价 |
| 月收入 | $12,500 | 500 × $25 |
| 年收入 | **$150,000** | |
| | | |
| **投资回报期** | **7.2 个月** | $90K / ($12.5K/月) |
| **3 年 ROI** | **400%** | ($450K 收入 - $90K 投资) / $90K |

### 3.3 区域 B: 郊区中负载区 — 可行但需监控

**场景**: Mixco / Villa Nueva 居民区

| 参数 | 值 | 说明 |
|---|---|---|
| 目标区域基站数 | 30 站 | 现有基站 |
| 每站 FWA 用户 | 15 户 | PRB 40-60%，需限制数量 |
| 总 FWA 用户 | **450 户** | |
| 总投资 | **$81,000** | 450 × $180 |
| 月 ARPU | **Q150 (~$19)** | 郊区定价略低 |
| 月收入 | $8,550 | |
| **投资回报期** | **9.5 个月** | |
| **3 年 ROI** | **280%** | |

⚠️ **风险**: 部分基站 PRB 可能在忙时超 70%，需要：
- 设置 FWA 用户优先级低于 MBB
- 忙时限速（如 10Mbps 降至 5Mbps）
- 每月监控 PRB 利用率，超 70% 的站停止新增 FWA

### 3.4 区域 C: 城区高负载区 — 不建议 FWA

**场景**: Guatemala City Zone 1-5 商业中心

| 参数 | 值 | 说明 |
|---|---|---|
| PRB 利用率 | >70% | 已接近满负荷 |
| FWA 影响 | 每增 10 个 FWA 用户 → MBB 速率降 15-20% | 不可接受 |
| **结论** | ❌ **不做 FWA** | 这里应该投 FTTH |

> 高负载区做 FWA = 牺牲 11.7M 移动用户体验去服务几百个 FWA 用户，得不偿失

### 3.5 区域 D: 农村低负载区 — 可行但规模小

**场景**: Quetzaltenango 周边乡镇

| 参数 | 值 | 说明 |
|---|---|---|
| 目标基站数 | 15 站 | 农村站，PRB<30% |
| 每站 FWA 用户 | 20 户 | 容量充裕 |
| 总 FWA 用户 | **300 户** | |
| 总投资 | **$54,000** | |
| 月 ARPU | **Q100 (~$13)** | 农村定价更低 |
| 月收入 | $3,900 | |
| **投资回报期** | **13.8 个月** | |
| **3 年 ROI** | **143%** | |

⚠️ **挑战**: 
- 用户密度低 → 获客成本高
- 与 Starlink 直接竞争（Starlink 不需要基站）
- 但 Tigo 有价格优势（$13 vs Starlink $50+/月）

---

## 4. FWA 部署总体方案

### 4.1 分区策略

```
         危地马拉 Tigo FWA 部署策略
         
  ┌─────────────────────────────────────────┐
  │  优先区域 A: 城区低负载                  │
  │  500 户 | $90K 投资 | 7 个月回本          │
  │  ✅ 立即启动 (Q3 2026)                   │
  ├─────────────────────────────────────────┤
  │  第二波 B: 郊区中负载                    │
  │  450 户 | $81K 投资 | 10 个月回本         │
  │  ✅ Q4 2026 启动（PRB 监控到位后）        │
  ├─────────────────────────────────────────┤
  │  第三波 D: 农村低负载                    │
  │  300 户 | $54K 投资 | 14 个月回本         │
  │  ⚠️ 2027 H1（评估 Starlink 竞争后决定）  │
  ├─────────────────────────────────────────┤
  │  不做 C: 城区高负载                      │
  │  ❌ 投 FTTH，不要投 FWA                  │
  └─────────────────────────────────────────┘
```

### 4.2 总投资回报汇总

| 波次 | 区域 | 用户数 | 投资 | 年收入 | 回本期 | 3年ROI |
|---|---|---|---|---|---|---|
| Wave 1 | 城区低负载 | 500 | $90K | $150K | 7月 | 400% |
| Wave 2 | 郊区中负载 | 450 | $81K | $103K | 10月 | 280% |
| Wave 3 | 农村低负载 | 300 | $54K | $47K | 14月 | 143% |
| **合计** | — | **1,250** | **$225K** | **$300K** | **9月(加权)** | **300%(加权)** |

### 4.3 与 FTTH 对比

| 方案 | 投资 | 覆盖用户 | 回本期 | 部署周期 |
|---|---|---|---|---|
| **FWA (1,250户)** | **$225K** | 1,250 | **9个月** | **2-4周/区域** |
| FTTH (同等户数) | $625K-1.25M | 1,250 | 24-36个月 | 6-12月/区域 |

> **FWA 的核心价值不是替代 FTTH，而是在 FTTH 建设期间快速抢占市场，防止 Claro 和 Starlink 截流。**

---

## 5. 关键风险与缓解

| 风险 | 严重度 | 缓解措施 |
|---|---|---|
| **MBB 体验劣化** | 🔴 高 | 设置 PRB 阈值（70%），超限自动限制 FWA 新增 |
| **ARPU 过低无法覆盖流量成本** | 🟠 中 | 设最低套餐 Q100，限流量 200GB/月 |
| **Starlink 价格竞争** | 🟡 低 | Tigo 价格已是 Starlink 的 1/3，有优势 |
| **Claro 抢先部署 FWA** | 🟠 中 | Wave 1 立即启动，抢先占位 |
| **CPE 退货/流失** | 🟡 低 | 12月合约锁定 + CPE 押金 |

---

## 6. 给 CEO 的建议

### 6.1 决策要点

1. **FWA 不是做不做的问题，而是做多少的问题** — Claro 和 Starlink 已经在抢客户
2. **$225K 投资可覆盖 1,250 户，9 个月回本** — 极低风险
3. **但必须避开高负载区** — 牺牲 11.7M 移动用户体验是不可接受的
4. **FWA 是过渡方案** — 长期仍需 FTTH，Millicom 的 $700M 光纤投资是正确方向

### 6.2 需要 CEO 确认的数据

| 数据 | 为什么需要 | 谁有 |
|---|---|---|
| 各区域 PRB 利用率 | 确认哪些区域有 FWA 容量 | 网络运维 |
| 固网用户分布热力图 | 确认哪些区域需求最大 | 市场部 |
| Claro/Starlink 新增用户区域 | 确认哪些区域正在流失 | 竞争情报 |
| 当前 CPE 采购价格 | 精确测算 ROI | 采购部 |

### 6.3 华为可以做什么

| 支持项 | 内容 |
|---|---|
| **免费网络评估** | 华为工程师分析全网 PRB 利用率，标出 FWA 可行区域 |
| **CPE 批量优惠** | 华为 5G CPE Pro 批量价 $150/台（含 12 月保修） |
| **FWA 策略规划** | 基于 CTO Dashboard 栅格数据，精确选址 |
| **容量保护方案** | FWA QoS 策略设计，确保 MBB 体验不劣化 |
| **3 个月试点** | 选 1 个 Wave 1 区域做 POC，用数据说话 |

---

## 数据来源

- [Millicom Q1 2026 SEC Filing](https://www.stocktitan.net/sec-filings/TIGO/6-k-millicom-international-cellular-sa-current-report-foreign-issuer-d312ee543841.html)
- [Guatemala Telecom Intelligence 2025](https://www.globenewswire.com/news-release/2025/04/21/3064515/28124/en/Guatemala-Telecom-Operators-Country-Intelligence-Report-2025.html)
- [Digital 2026 Guatemala - DataReportal](https://datareportal.com/reports/digital-2026-guatemala)
- [Guatemala MNP Decreto 14-2025](https://www.guatemalaportal.com/guatemala-approves-decreto-14-2025-keep-your-number-when-switching-carriers/)
- [GSMA FWA Economic Potential](https://www.gsma.com/solutions-and-impact/technologies/networks/5g/fixed-wireless-access-economic-potential-and-best-practices/)
- [Ericsson FWA Growth Opportunity](https://www.ericsson.com/en/reports-and-papers/mobility-report/articles/realizing-the-5g-fwa-growth-opportunity)
- [Starlink Guatemala](https://worldpossible.org/products/starlink-in-guatemala)
- FWA CAPEX $300-800/subscriber: GSMA + Infovista industry benchmarks
- FWA 用户流量 40x: GSMA Connected Society report
