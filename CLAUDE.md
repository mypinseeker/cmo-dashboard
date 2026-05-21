# CMO Dashboard — 项目规则

## ⛔ QA 检查清单（每次修改推送前必须执行）

**触发条件**：任何代码修改完成后、git push 之前，必须按以下清单逐项检查。未通过 QA 不得推送。

---

### CHECK-1: 中英文翻译完整性 ❌ 最高优先级

**教训来源**：英文界面大量残留中文，用户多次反馈

| 检查项 | 方法 |
|---|---|
| **1a. HTML 静态中文必须有 data-i18n** | 扫描 HTML body 中所有中文字符，每个必须在 `data-i18n` 属性内或 `<!-- 注释 -->` 内 |
| **1b. JS 动态中文必须用 getTranslation()** | 扫描 `<script>` 块中所有中文字符串（排除 TRANSLATIONS 字典定义行、`//` 注释行、`currentLang==='zh'?` 三元表达式内的中文分支），剩余中文必须包裹在 `getTranslation()` 或 `currentLang` 三元表达式内 |
| **1b-extra. JS 数据对象中的中文** | ECharts series `name:`、legend `label:`、data `label:` 等用户可见字段，如果直接赋值中文字符串，必须用 `getTranslation()` 包裹。数据对象的 key（如 `"360p以下"`）可保留中文但显示时必须翻译 |
| **1c. TRANSLATIONS 字典必须覆盖** | 每个 `data-i18n="key"` 的 key 必须在 TRANSLATIONS 字典中有对应条目；每个 `getTranslation('key')` 的 key 也必须存在 |
| **1d. 下拉菜单 option** | `<select>` 的 `<option>` 文本必须在 `toggleLanguage()` 中有对应翻译逻辑 |
| **1e. 地图/图表动态内容** | Polygon tooltip、ECharts formatter、site popup 中的中文必须用 `getTranslation()` 或 `currentLang` 三元表达式 |

**自动化检查脚本（必须用 Python，不能用 grep）**：
```python
# 扫描 JS 代码块中未翻译的中文（排除注释、字典定义、三元表达式中文分支）
import re
with open('dashboard_v4.html') as f:
    content = f.read()
js_start = content.find('<script>', content.find('echarts.min.js'))
js_end = content.find('</script>', js_start)
js_lines = content[js_start:js_end].split('\n')
js_offset = content[:js_start].count('\n') + 1
for i, line in enumerate(js_lines):
    s = line.strip()
    if s.startswith('//') or s.startswith('*') or s.startswith('/*'): continue
    if re.search(r"'[^']*':\s*\{\s*zh:", s): continue
    if re.search(r"zh:\s*'|en:\s*'", s): continue
    line_no_gt = re.sub(r"getTranslation\('[^']*'\)", '', line)
    line_no_ternary = re.sub(r"currentLang\s*===\s*'zh'\s*\?\s*'[^']*'", '', line_no_gt)
    if re.findall(r'[\u4e00-\u9fff]+', line_no_ternary):
        print(f"L{js_offset+i}: {s[:120]}")
```
**标准**：上述脚本输出为 0 行（或仅剩 `//` 注释）才算通过

---

### CHECK-2: 布局对齐与空白 

**教训来源**：左栏/右栏底部大片空白、底部卡片遮挡侧栏、元素不对齐

| 检查项 | 方法 |
|---|---|
| **2a. 侧栏撑满** | 左右栏 flex 子元素必须有 `flex: N; min-height: 0`，不能有底部空白 |
| **2b. 底部行不遮挡侧栏** | `.bottom-row` 的 `grid-column` 必须是 `2`（仅中间列），不能是 `1 / -1` |
| **2c. overflow 正确** | 列容器 `overflow: hidden`，子卡片 `overflow-y: auto`（不能反过来，否则 flex 拉伸失效）|
| **2d. 目视检查** | 描述当前布局预期：左栏两卡片撑满、右栏三卡片撑满、底部四卡片在地图下方 |

---

### CHECK-3: 响应式适配

**教训来源**：固定像素值导致不同分辨率下错位

| 检查项 | 方法 |
|---|---|
| **3a. 禁止关键布局用固定 px** | grid-template-columns/rows、侧栏宽度、底栏高度必须用 CSS 变量 + `clamp()` |
| **3b. 字体用 CSS 变量** | 不允许在 `.card-title`、`.big-number`、`.app-name` 等 class 中硬编码 `font-size: Npx`，必须用 `var(--fs-*)` |
| **3c. 图表高度响应式** | ECharts 容器 height 必须用 `clamp(min, vh, max)`，不能固定 px |
| **3d. ECharts resize** | 必须有全局 resize handler，窗口变化时所有图表自动调整 |

---

### CHECK-4: HTML/CSS 结构完整性

**教训来源**：CSS 孤立片段、标签不匹配

| 检查项 | 方法 |
|---|---|
| **4a. 标签配对** | `<div>` == `</div>`、`<span>` == `</span>`、`<script>` == `</script>`、`<style>` == `</style>` |
| **4b. CSS 大括号配对** | `<style>` 内 `{` 数量 == `}` 数量 |
| **4c. 无孤立 CSS 片段** | 不允许出现 `property: value; }` 前面没有选择器 `{` 的情况 |

**自动化检查脚本**：
```python
import re
with open('dashboard_v4.html') as f:
    content = f.read()
for tag in ['div','span','script','style']:
    o = len(re.findall(rf'<{tag}[\s>]', content))
    c = len(re.findall(rf'</{tag}>', content))
    assert o == c, f'{tag} mismatch: {o} vs {c}'
```

---

### CHECK-5: JavaScript 运行时安全

**教训来源**：引用不存在的 DOM 元素导致图表初始化失败

| 检查项 | 方法 |
|---|---|
| **5a. getElementById 有对应元素** | JS 中每个 `getElementById('xxx')` 的 xxx 必须在 HTML 中存在 |
| **5b. 空值保护** | 所有 `echarts.init(el)` 前必须有 `if (!el) return` 守卫 |
| **5c. 变量名一致** | 全局变量（如 SITES_DATA vs SITES）不能有命名不一致 |
| **5d. 变量声明顺序 (TDZ)** | `const`/`let` 声明的全局变量，必须在第一次引用之前完成声明。函数体内的引用虽然是延迟执行，但如果函数可能在声明前被调用（如 onclick 触发），则仍然会触发暂时性死区 (TDZ) ReferenceError |
| **5e. 无重复声明** | 同一个 `const`/`let` 变量名只能声明一次，不允许在不同位置重复声明 |
| **5f. onclick 引用检查** | HTML 中每个 `onclick="funcName()"` 的 funcName 必须在 JS 中有 `function funcName` 定义 |
| **5g. 数据键名一致性** | 同一个实体（城市/区域/指标）在不同数据结构中必须用完全相同的字符串。禁止混用带重音和不带重音的拼写（如 `Medellín` vs `Medellin`），统一用不带重音的 ASCII 拼写 |

**自动化检查脚本（TDZ + 重复声明）**：
```python
import re
with open('dashboard_v4.html') as f:
    content = f.read()
js_start = content.find('<script>\n', content.find('echarts.min.js'))
js_end = content.find('</script>', js_start)
js = content[js_start:js_end]
js_offset = content[:js_start].count('\n') + 1
# 收集所有 const/let 声明位置
decls = {}
for i, line in enumerate(js.split('\n')):
    for name in re.findall(r'\b(?:const|let)\s+(\w+)\s*=', line):
        if name not in decls: decls[name] = js_offset + i
# 检查关键变量是否在声明前被引用
key_vars = ['MR_HEATMAP','covHeatLayer','TERMINAL_HEATMAPS',
            'EXPERIENCE_METRICS','COMPETITOR_DATA','COVERAGE_DATA']
for var in key_vars:
    if var not in decls: continue
    for i, line in enumerate(js.split('\n')):
        ln = js_offset + i
        if ln == decls[var]: continue
        if line.strip().startswith('//'): continue
        if re.search(rf'\b(?:const|let|var)\s+{var}\b', line): continue
        if re.search(rf'\b{var}\b', line) and ln < decls[var]:
            print(f'TDZ: {var} used at L{ln}, declared at L{decls[var]}')
            break
# 检查重复声明
for var in key_vars:
    count = len(re.findall(rf'\b(?:const|let)\s+{var}\b', js))
    if count > 1: print(f'DUPLICATE: {var} declared {count} times')
```
**标准**：上述脚本输出为空才算通过

---

### CHECK-6: 底部 APP 卡片专项

**教训来源**：多次迭代底部卡片布局（上下布局→左右布局、饼图太大挤掉文字、重复数字、字体怪异）

| 检查项 | 方法 |
|---|---|
| **6a. 左右布局** | 饼图在左，指标在右，`display:flex; align-items:center` |
| **6b. 饼图尺寸响应式** | 宽度用 `clamp(60px, 5.5vw, 90px)`，不能固定 px |
| **6c. 无重复数字** | 同一个数据点不要在卡片上出现两次 |
| **6d. 字体统一** | 使用 `.btm-name`/`.btm-row`/`.btm-label`/`.btm-val` 等 CSS class，不用 inline font-size |

---

## 执行流程

```
代码修改完成
    ↓
QA CHECK-1~6 逐项检查
    ↓
全部 ✅ → git add + commit + push
    ↓
任一 ❌ → 修复后重新检查，直到全绿
```

**违规**：未执行 QA 直接 push = 违规。QA 发现 Critical 问题但仍然 push = 违规。
