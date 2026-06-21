# 《墨多多汉字冒险》v2 升级实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将现有第1关原型升级为面向小学三年级以上、以纠正错误笔顺/结构为目标的完整多关游戏，增强多巴胺奖励动画、量化进度图表，并适配 GitHub/Cloudflare 静态部署。

**Architecture：** 保持单文件 HTML 部署形态，通过 jsDelivr（国内可访问）加载 Hanzi Writer、Chart.js、canvas-confetti 等专业库，内嵌核心关卡字符数据以保证首屏可用；游戏状态、逐字统计、打卡记录全部持久化到 localStorage。

**Tech Stack：** HTML5 + CSS3 + Vanilla JS，Canvas 2D，Hanzi Writer（笔顺动画），Chart.js（进度图表），canvas-confetti（奖励特效），Web Audio API（音效），localStorage（存档）。

---

## 0. 需求对齐与范围边界

### 0.1 回顾原产品方案文档
- 核心用户：10岁左右、写字慢、笔顺错误、抵触练字的小学生。
- 核心目标：30天重建20个高频字的正确笔顺。
- 三阶段：游戏化兴趣期 → 双轨融合期 → 纸笔独立期。
- 单关结构：开场 → 热身 → 新字教学 → 挑战字 → Boss战 → 结算。
- 笔顺识别：8方向简化算法，允许顺序错位1位容错。
- 奖励：绿宝石、星级、皮肤券、纸笔复刻奖励。
- 家长后台：进度、薄弱字、纸笔记录。

### 0.2 本次升级新增需求
1. **可使用国内可访问的 CDN 资源**优化动画与图表。
2. **奖励动画要刺激多巴胺**：庆祝特效、绿宝石弹窗、升级光效。
3. **练习结果量化可见**：正确率趋势图、逐字掌握度图、Boss战历史。
4. **字数量和难度提升**：覆盖三到四年级高频易错字，不只写“一、二、三”。
5. **目标用户是“纠正错误笔顺/结构”**，不是零基础。
6. **最终部署到 GitHub / Cloudflare Pages**，保持单文件或极简化结构。

### 0.3 范围决策
- 实现 **15 个关卡**（按原方案文档第1-15关），每关4-5个字，共约60个唯一汉字。
- 第1-5关完整可玩；第6-15关数据、对话、BOSS战逻辑全部实现，UI上标注为“已解锁/复习”。
- 保留并强化纸笔过渡闭环（家长确认 + 绿宝石奖励）。
- 家长后台增加 Chart.js 图表。
- 不实现后端、账号系统、语音合成、皮肤商城兑换实物（保留绿宝石计数与兑换入口提示）。

---

## 1. 数据准备：字符笔顺数据

### Task 1.1：确定15关字表
**Files:**
- Create: `scripts/char_list.json`（临时数据脚本输出）

**字表（严格按原方案文档）：**

| 关卡 | 主题 | 字 |
|------|------|-----|
| 1 | 横画基准 | 一、二、三、工、王 |
| 2 | 竖画支撑 | 十、木、本、禾、未 |
| 3 | 撇捺平衡 | 人、八、入、大、天 |
| 4 | 点定位 | 方、主、玉、太、犬 |
| 5 | 折笔入门 | 了、子、字、学、孩 |
| 6 | 左右结构 | 的、他、你、们、什 |
| 7 | 上下结构 | 是、早、星、旦、晶 |
| 8 | 包围结构 | 国、回、同、问、间 |
| 9 | 复合结构 | 我、说、话、语、讲 |
| 10 | 综合巩固 | 这、那、都、里、高 |
| 11 | 为火类 | 为、火、办、伙、秋 |
| 12 | 方万类 | 方、万、历、厉、迈 |
| 13 | 以比类 | 以、比、北、此、化 |
| 14 | 车东类 | 车、东、乐、划、戈 |
| 15 | 终极综合 | 全部20核心字随机混合 |

- [ ] **Step 1:** 按上表生成 `scripts/char_list.json`。

```json
{
  "levels": [
    {"id":1,"title":"横画基准","chars":["一","二","三","工","王"],"theme":"新手村·墨多多训练营"},
    ...
  ]
}
```

- [ ] **Step 2:** 检查是否有生僻字无法从 Hanzi Writer 数据获取。

---

### Task 1.2：获取并内嵌 Hanzi Writer 字符数据
**Files:**
- Create: `scripts/fetch_hanzi_data.py`
- Modify: `index.html`（内嵌 `HANZI_DATA`）

- [ ] **Step 1:** 编写脚本从 `https://cdn.jsdelivr.net/npm/hanzi-writer-data@latest/{char}.json` 拉取全部唯一字符数据。

```python
import json, urllib.request, os
chars = [...]  # 60个唯一字
os.makedirs('data', exist_ok=True)
data = {}
for c in chars:
    url = f'https://cdn.jsdelivr.net/npm/hanzi-writer-data@latest/{c}.json'
    data[c] = json.loads(urllib.request.urlopen(url).read())
with open('data/hanzi_data.json','w',encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False)
```

- [ ] **Step 2:** 运行脚本生成 `data/hanzi_data.json`。
- [ ] **Step 3:** 验证每个字符数据完整（有 strokes 和 medians）。
- [ ] **Step 4:** 将 `data/hanzi_data.json` 内容压缩后写入 `index.html` 的 `<script>const HANZI_DATA = {...};</script>`。

**Test:**
```bash
python3 scripts/fetch_hanzi_data.py
wc -c data/hanzi_data.json
```
Expected: 文件大小 < 150KB，所有60字均成功拉取。

---

## 2. 依赖库选型与加载

### Task 2.1：CDN 选型
**Files:**
- Modify: `index.html`（`<head>` 与 `<script>` 区域）

| 用途 | 库 | CDN | 国内可用性 |
|------|-----|-----|-----------|
| 笔顺动画 | Hanzi Writer 3.3.0 | `https://cdn.jsdelivr.net/npm/hanzi-writer@3.3.0/dist/hanzi-writer.min.js` | 高（jsDelivr 有国内节点） |
| 庆祝特效 | canvas-confetti 1.9.3 | `https://cdn.jsdelivr.net/npm/canvas-confetti@1.9.3/dist/confetti.browser.min.js` | 高 |
| 进度图表 | Chart.js 4.4.1 | `https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js` | 高 |

- [ ] **Step 1:** 在 `index.html` 中通过 `<script src="...">` 引入上述三个库，放在 `<body>` 末尾、游戏逻辑之前。

```html
<script src="https://cdn.jsdelivr.net/npm/hanzi-writer@3.3.0/dist/hanzi-writer.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.9.3/dist/confetti.browser.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
```

- [ ] **Step 2:** 添加 CDN 加载失败回退：若 `window.HanziWriter` 不存在，显示提示“请检查网络连接”。

**Test:**
```bash
# 启动本地服务器，断网刷新，观察是否出现网络提示
python3 -m http.server 8080
```
Expected: 断网时页面不白屏，有中文提示。

---

## 3. 游戏架构重构

### Task 3.1：模块化单文件代码结构
**Files:**
- Modify: `index.html`

将现有巨大 `<script>` 拆分为清晰区块（仍在一个文件中）：

```html
<script>
// ===== 配置层 =====
const CONFIG = {...};

// ===== 数据层 =====
const LEVELS = [...];
const NPC = {...};
const DIALOGUES = {...};

// ===== 工具层 =====
const utils = {...};
const audio = {...};

// ===== 核心引擎 =====
class StrokeEngine {...}
class Validator {...}
class HanziRenderer {...}
class RewardSystem {...}
class ChartManager {...}

// ===== 游戏状态机 =====
const game = {...};

// ===== 初始化 =====
document.addEventListener('DOMContentLoaded', () => game.init());
</script>
```

- [ ] **Step 1:** 创建 `CONFIG` 对象，集中管理常量（关卡数、BOSS时间、星级阈值、宝石奖励等）。
- [ ] **Step 2:** 将 `LEVELS`、`NPC`、`DIALOGUES` 提取为独立数据对象。
- [ ] **Step 3:** 创建 `RewardSystem` 类，封装所有奖励动画与音效。
- [ ] **Step 4:** 创建 `ChartManager` 类，封装 Chart.js 初始化与更新。

---

### Task 3.2：增强存档模型
**Files:**
- Modify: `index.html`

```javascript
function defaultSave() {
  return {
    version: 3,
    gems: 0,
    currentLevel: 1,
    clearedLevels: [],
    levelStars: {},
    charStats: {},        // {字: {correct, wrong, lastPractice, streak}}
    dailyStats: {},       // {日期: {practiced, correct, wrong, paperDone}}
    paperRecord: [],
    firstPlay: true,
    soundOn: true,
    streakDays: 0,
    lastPlayDate: null,
    achievements: []
  };
}
```

- [ ] **Step 1:** 升级 `defaultSave` 与 `loadSave`（兼容旧版 v2 存档迁移：若读到 v2 则补全新字段）。
- [ ] **Step 2:** 每次练习/BOSS战后写入 `dailyStats`。
- [ ] **Step 3:** 登录时计算连续打卡天数 `streakDays`。

---

## 4. 关卡与内容系统

### Task 4.1：构建15关数据
**Files:**
- Modify: `index.html` 中 `LEVELS` 数据对象

每关结构：
```javascript
{
  id: 1,
  theme: '新手村·墨多多训练营',
  title: '横画基准',
  intro: '墨多多开场台词...',
  chars: ['一','二','三','工','王'],
  newChars: ['二','三','工','王'],  // 热身除外
  warmUp: ['一'],
  challenge: ['工','王'],
  bossPool: ['一','二','三','工','王'],
  bossCount: 5,
  bossTime: 15000,
  dialogues: {
    intro: [...],
    warmup: {...},
    teaching: {...},
    challenge: {...},
    beforeBoss: [...]
  }
}
```

- [ ] **Step 1:** 为15关编写 `LEVELS` 数组，每关包含完整对话与字表。
- [ ] **Step 2:** 对话严格参考原方案文档第七章“关卡与对话脚本”。
- [ ] **Step 3:** 为每个字补充 `hint`（教学提示）、`commonErrors`（常见错误）、`structure`（结构类型：独体/左右/上下/包围/半包围）。

---

### Task 4.2：通用关卡流程引擎
**Files:**
- Modify: `index.html`

流程状态机：
```
enterLevel(id)
  → showLevelIntro()      // 关卡开场对话
  → warmUp()              // 1-2个已学/简单字教学
  → teachNewChars()       // 2-3个新字教学
  → challengeChars()      // 1-2个挑战/辨析字
  → startPractice()       // 逐字描红练习
  → startBoss()           // Boss战
  → showResult()          // 结算
```

- [ ] **Step 1:** 重构 `enterLevel` 为状态机驱动，支持任意关卡。
- [ ] **Step 2:** 教学页根据阶段显示不同对话（intro/warmup/teaching/challenge）。
- [ ] **Step 3:** 练习页按关卡顺序逐个练习当前关卡所有字。
- [ ] **Step 4:** Boss战从 `bossPool` 中按算法生成序列（必含新字 + 易错字 + 随机字）。

---

## 5. 奖励系统：多巴胺动画

### Task 5.1：绿宝石获得动画
**Files:**
- Modify: `index.html` CSS + JS

- [ ] **Step 1:** 绿宝石 +N 时，从获得位置飘出一个绿色菱形到顶部 gem-bar。
- [ ] **Step 2:** 使用 `canvas-confetti` 在点击/正确时触发小范围金色粒子。
- [ ] **Step 3:** 8-bit “叮”音效配合动画。

```javascript
function showGemReward(amount, sourceElement) {
  const el = document.createElement('div');
  el.className = 'floating-gem';
  el.textContent = `+${amount}`;
  document.body.appendChild(el);
  // animate to gem-bar
  el.animate([...], {duration: 800, easing: 'ease-out'});
  confetti({particleCount: 15, spread: 40, origin: {...}, colors: ['#55AA55']});
}
```

---

### Task 5.2：星级结算动画
**Files:**
- Modify: `index.html`

- [ ] **Step 1:** 结算页根据星级依次点亮星星，每个星星弹出并旋转。
- [ ] **Step 2:** 3星时触发全屏 confetti 庆祝 + “传奇！”称号发光。
- [ ] **Step 3:** 1-2星时显示鼓励动画，不倒笔怪出现但给出具体改进建议。

---

### Task 5.3：升级/解锁动画
**Files:**
- Modify: `index.html`

- [ ] **Step 1:** 首次通关关卡时，地图页对应章节播放解锁光效。
- [ ] **Step 2:** 解锁下一章时显示墨多多提示弹窗。

---

## 6. 练习结果量化图表

### Task 6.1：每日正确率折线图
**Files:**
- Modify: `index.html` 家长后台

- [ ] **Step 1:** 在家长后台添加 `<canvas id="chart-daily">`。
- [ ] **Step 2:** 使用 Chart.js 绘制最近7天每日正确率折线。
- [ ] **Step 3:** 数据来自 `state.dailyStats`。

```javascript
new Chart(ctx, {
  type: 'line',
  data: { labels: dates, datasets: [{ label: '正确率%', data: rates, borderColor: '#55AA55' }] },
  options: { responsive: true, scales: { y: { min: 0, max: 100 } } }
});
```

---

### Task 6.2：逐字掌握度雷达/条形图
**Files:**
- Modify: `index.html` 家长后台

- [ ] **Step 1:** 添加 `<canvas id="chart-chars">`。
- [ ] **Step 2:** 用水平条形图展示每个字的正确率，颜色按掌握度分段（绿/黄/红）。
- [ ] **Step 3:** 可切换“当前关卡”与“全部已学字”。

---

### Task 6.3：结算页本次战斗统计
**Files:**
- Modify: `index.html` 结算页

- [ ] **Step 1:** 结算页显示本次 Boss 战每字耗时/正确性小条形图。
- [ ] **Step 2:** 列出“最棒的字”和“需要加强的字”。

---

## 7. 笔顺识别算法增强

### Task 7.1：8方向 + 笔画数量 + 顺序容错
**Files:**
- Modify: `index.html` `Validator` 类

- [ ] **Step 1:** 保持8方向识别。
- [ ] **Step 2:** 笔画数量错误时明确提示“多写了一笔/少写了一笔”。
- [ ] **Step 3:** 允许相邻两笔顺序错位1位（容错），但扣1星。
- [ ] **Step 4:** 复杂字增加“结构类型”检查提示（如左右结构先左后右）。

```javascript
validate(character, userDirs) {
  const std = CHAR_DATA[character];
  if (userDirs.length !== std.directions.length) {
    return {correct:false, reason: `需要${std.directions.length}笔，你写了${userDirs.length}笔`};
  }
  // 完全匹配 → 3星
  // 错位1位 → 2星
  // 方向错1笔 → 1星
  // 错2笔+ → 0星
}
```

---

## 8. UI/UX 升级

### Task 8.1：响应式再优化
**Files:**
- Modify: `index.html` CSS

- [ ] **Step 1:** 使用 CSS Grid/Flexbox + `clamp()` + `min()`/`max()` 实现任意屏幕适配。
- [ ] **Step 2:** 横屏时自动调整为左右布局（对话左 / 书写区右）。
- [ ] **Step 3:** 确保按钮最小 44×44pt，适合儿童手指。

---

### Task 8.2：深色/护眼模式
**Files:**
- Modify: `index.html` CSS

- [ ] **Step 1:** 增加米黄色书写区背景，降低白屏刺眼感。
- [ ] **Step 2:** 所有颜色使用 CSS 变量，便于后续主题切换。

---

## 9. 部署优化

### Task 9.1：GitHub/Cloudflare Pages 就绪
**Files:**
- Create: `README.md`
- Create: `.github/workflows/static.yml`（可选）

- [ ] **Step 1:** 在 `README.md` 中说明：这是一个纯静态单文件，可直接部署到 GitHub Pages / Cloudflare Pages。
- [ ] **Step 2:** 提供一键部署说明：Fork → Settings → Pages → 选择 main 分支 root。
- [ ] **Step 3:** 确保所有 CDN 链接使用 HTTPS。

---

## 10. 测试清单

### Task 10.1：功能测试
- [ ] 15关均可从地图进入。
- [ ] 每关教学、练习、Boss战、结算流程完整。
- [ ] 笔顺正确时通过，错误时提示并撤销。
- [ ] Boss战计时、提交、跳过正常。
- [ ] 绿宝石、星级、纸笔打卡正确累计。
- [ ] 家长后台图表正确渲染。
- [ ] 存档导出/导入/清除正常。

### Task 10.2：兼容性测试
- [ ] Chrome / Safari / Edge 最新版。
- [ ] iOS Safari（touch事件）。
- [ ] Android Chrome。
- [ ] 离线模式（已内嵌数据）下首屏可用。

### Task 10.3：性能测试
- [ ] 首屏加载 < 3s（4G）。
- [ ] 单文件大小 < 500KB。
- [ ] 15关切换无内存泄漏。

---

## 11. 风险与对策

| 风险 | 对策 |
|------|------|
| jsDelivr 在国内偶尔不稳定 | 内嵌核心关卡数据；库文件使用 `integrity` 或本地 fallback |
| 60字数据文件过大 | 仅内嵌前5关核心数据，高级关卡按需从 CDN 拉取 |
| 复杂字识别误判 | 明确提示“方向/数量/顺序”三类错误，降低挫败感 |
| 儿童误触家长后台 | 家长后台增加简单验证题（如 3+5=？） |

---

## 12. 执行顺序建议

1. 准备字符数据（Task 1-2）
2. 搭建 CDN 依赖与单文件骨架（Task 2-3）
3. 实现15关数据与通用流程引擎（Task 4）
4. 强化奖励动画（Task 5）
5. 添加图表与家长后台（Task 6）
6. 优化笔顺识别与UI（Task 7-8）
7. 部署文档与测试（Task 9-10）
