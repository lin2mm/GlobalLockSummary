---
title: 贡献
description: 如何为 GlobalLockSummary 增加锁族、标准或更正——一个锁一个 JSON 记录、数据结构，以及什么样的记录才算可核对。
---

这个目录是靠量过真实锁的人把结果写下来而增长的。最有价值的贡献不是大贡献——而是来自一个我们尚未覆盖的国家的一个锁族，带着数字和照片。

## 最快的贡献方式

提交一个 issue，包含：

1. 国家与城市
2. 门是什么（木门、uPVC、金属铁闸、玻璃）
3. 背距、中心距、面板尺寸、门厚
4. 一张门边照片，画面里有尺子
5. 这扇门是否耐火

这些足够维护者创建记录。如果你更愿意自己写记录，说明在下面。

## 仓库结构

```text
content/
  site.json                 站点名称、导航、语言、页脚文字
  i18n/terms.json           共享双语术语——一个术语只加一次
  pages/<lang>/*.md         长文页面，每种语言一个目录
  catalog/
    lock-families/*.json    一个锁族一个文件
    standards.json          所有标准在一个文件里
    retrofit-architectures.json
    smart-locks.json        参考设备
    decision-tree.json      识别向导的问题
```

新增一个锁族就是新增一个 JSON 文件。其他地方都不用改——索引页、搜索索引、sitemap 与 `llms.txt` 都会由它重新生成。

## 锁族数据结构

```json
{
  "id": "kebab-case-unique-id",
  "status": "verified | needs-review",
  "regions": ["Country", "..."],
  "title": { "en": "...", "zh": "..." },
  "summary": { "en": "...", "zh": "..." },
  "anatomy": { "en": ["..."], "zh": ["..."] },
  "measurements": [
    {
      "key": "backset",
      "typical": "55 mm, 60 mm",
      "tolerance": "±1 mm",
      "how": { "en": "Door edge to keyhole centre.", "zh": "..." }
    }
  ],
  "measureOrder": ["backset", "centreDistance"],
  "standards": ["din-18251"],
  "retrofit": { "architectures": ["motor-on-thumbturn"], "notes": { "en": "...", "zh": "..." } },
  "faq": { "en": [{ "q": "...", "a": "..." }], "zh": [] },
  "sources": [{ "title": "...", "url": "https://..." }]
}
```

`measurements` 里的 `key` 必须存在于 `content/i18n/terms.json` 的 `measurements` 下——这就是标签只翻译一次而不是每条记录翻译一次的原因。使用了不存在的 key，`npm run check` 会让构建失败。

## 状态标记不可省略

- **已核对（verified）** —— 数值已对照公开资料交叉核对，来源列在 `sources` 里。数据表、标准文件与厂商规格算；论坛帖子不算。
- **待核对（needs-review）** —— 其他一切，包括你自己量过但没人确认的内容。这类记录会带明显警告发布，这比记录根本不存在要好得多。

没有链接就不要标记为已核对。本站的全部价值就在于读者能去核对。

## 同时为两类读者写作

每条记录都会被房主和机械工程师读到，而且通常是这个顺序。摘要用平实语言，测量数据保持精确。如果某个数字重要，就给出公差——没有公差的尺寸不是规格。

## 翻译

内容目前是双语（英文与中文）。结构是为扩展设计的：数据存在带各语言字段的 JSON 里，共享词汇存在 `terms.json`，因此将来的机器翻译可以处理术语而不是散文。

如果你要新增一种语言，创建 `content/pages/<lang>/`，并在 `content/site.json` 的 `languages`、`navigation` 与 UI 文案里加上该语言。构建脚本不需要任何改动。

## 本地运行

```bash
node build.mjs            # 构建到 _site/
node build.mjs --watch    # 变更时自动重建
node serve.mjs            # 在 http://localhost:8080 提供 _site/
npm run check             # 语法检查 + 目录数据引用完整性检查
```

无需安装任何依赖。Node 20 或更新版本。

## 当前最需要的内容

1. **非洲、南美、印度、中东** —— 目前一个锁族都没有
2. **澳大利亚** —— 标准编号待确认
3. **日本** —— 锁体尺寸与适用的 JIS 引用
4. **带尺子的照片** —— 每个锁族都需要，识别向导才能展示
5. **适配件拆解数据** —— 实测的夹持范围与旋钮形状，这些没有厂商会公布
