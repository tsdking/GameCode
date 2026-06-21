# 墨多多汉字冒险

> 一个面向小学 3-4 年级学生的笔顺纠正游戏。单文件 HTML5，可直接部署到 GitHub Pages / Cloudflare Pages。

## 项目特点

- **15 个关卡**：覆盖横/竖/撇/捺/点/折、左右/上下/包围/复合结构、高频易错字
- **专业笔顺动画**：基于 [Hanzi Writer](https://chanind.github.io/hanzi-writer/) 的汉字描红与动画
- **8 方向笔顺识别**：自定义 Canvas 描红 + 方向匹配算法
- **多巴胺奖励**：canvas-confetti 庆祝特效、绿宝石飘动动画、星级结算
- **量化进度**：Chart.js 每日正确率折线图、逐字掌握度条形图
- **纸笔过渡**：结算页家长确认机制，连接电子练习与真实书写
- **离线可用**：核心汉字数据全部内嵌，无需后端

## 技术栈

- HTML5 + CSS3 + Vanilla JS
- Canvas 2D API
- [Hanzi Writer](https://github.com/chanind/hanzi-writer)（jsDelivr CDN）
- [canvas-confetti](https://github.com/catdad/canvas-confetti)（jsDelivr CDN）
- [Chart.js](https://www.chartjs.org/)（jsDelivr CDN）
- localStorage 存档

## 本地运行

```bash
python3 -m http.server 8080
# 打开 http://localhost:8080/index.html
```

或直接双击 `index.html` 用浏览器打开。

## 部署到 GitHub Pages

1. Fork 本仓库（或直接把 `index.html` 推到 GitHub 仓库）。
2. 进入仓库 **Settings → Pages**。
3. Source 选择 **Deploy from a branch**，Branch 选择 **main / root**。
4. 等待片刻，访问 `https://你的用户名.github.io/仓库名/`。

## 部署到 Cloudflare Pages

1. 登录 [Cloudflare Pages](https://pages.cloudflare.com/)。
2. 创建新项目，连接 GitHub 仓库。
3. 构建设置：
   - Framework preset: **None**
   - Build command: （留空）
   - Build output directory: `/`
4. 保存并部署。

## 存档说明

游戏进度保存在浏览器 `localStorage` 中，键名为 `moduoduo_save_v3`。家长后台提供“导出存档”功能，可备份为 JSON 文件。

## 目标用户

- 小学 3-4 年级学生
- 已经会写字，但存在固定错误笔顺或结构问题
- 家长可陪同 15-20 分钟/天

## 数据来源

汉字笔顺数据来自 [hanzi-writer-data](https://www.npmjs.com/package/hanzi-writer-data)，按 CC BY-SA 4.0 授权。
