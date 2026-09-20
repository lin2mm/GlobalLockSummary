# -*- coding: utf-8 -*-
import re

with open("build.mjs", "r", encoding="utf-8") as f:
    code = f.read()

# 替换 sampleCards 与 gallerySectionHtml 生成部分
old_sample_loop = """  let gallerySectionHtml = '';
  if (matchedSamples.length > 0) {
    const sampleCards = matchedSamples.map((s) => {
      const sTitle = (s.title && (s.title[lang] || s.title.en || s.title.zh)) || s.id;
      const schematicPath = `/assets/img/diagrams/${s.id}_schematic.svg`;
      const hasSchematic = existsSync(join(ROOT, 'assets/img/diagrams', `${s.id}_schematic.svg`));

      return `
      <div class="lock-detail-sample">"""

new_sample_loop = """  let gallerySectionHtml = '';
  let clusterHeadings = [];
  if (matchedSamples.length > 0) {
    // 按类别组织样本
    const clustersMap = new Map();
    for (const s of matchedSamples) {
      const c = getSampleCluster(s, lang);
      if (!clustersMap.has(c.id)) {
        clustersMap.set(c.id, { id: c.id, name: c.name, tag: c.tag, items: [] });
      }
      clustersMap.get(c.id).items.push(s);
    }

    const clustersList = [...clustersMap.values()];
    const isMultiCluster = clustersList.length > 1;

    // 生成顶部快速分类跳链工规胶囊导航条
    let topClusterNavHtml = '';
    if (isMultiCluster) {
      const pills = clustersList.map(c => `
        <a href="#${c.id}" class="spec-cluster-pill" style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 12px; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; font-weight: 700; color: #0f172a; text-decoration: none; transition: all 0.2s ease;">
          <span style="font-size: 0.72rem; color: #64748b;">⌖</span>
          <span>${escapeHtml(c.name)}</span>
          <span style="font-size: 0.68rem; background: #f1f5f9; color: #475569; padding: 1px 5px; border-radius: 3px; border: 1px solid #e2e8f0;">${c.items.length}</span>
        </a>
      `).join('');

      topClusterNavHtml = `
      <div class="spec-cluster-bar" style="margin: 14px 0 24px; padding: 10px 14px; background: #f8fafc; border: 1px solid #cbd5e1; border-left: 3px solid #0B1D47; border-radius: 4px; display: flex; align-items: center; gap: 10px; flex-wrap: wrap;">
        <span style="font-size: 0.78rem; font-weight: 800; color: #0B1D47; text-transform: uppercase; letter-spacing: 0.04em;">
          📍 ${lang === 'zh' ? '实物型号直达分类' : 'Jump to Category'}:
        </span>
        <div style="display: flex; gap: 8px; flex-wrap: wrap; align-items: center;">
          ${pills}
        </div>
      </div>`;
    }

    // 渲染分类型卡片区
    let clusterSectionsHtml = '';
    for (const c of clustersList) {
      if (isMultiCluster) {
        clusterHeadings.push({ level: 3, id: c.id, text: c.name });
      }

      const cardsForCluster = c.items.map((s) => {
        const sTitle = (s.title && (s.title[lang] || s.title.en || s.title.zh)) || s.id;
        const schematicPath = `/assets/img/diagrams/${s.id}_schematic.svg`;
        const hasSchematic = existsSync(join(ROOT, 'assets/img/diagrams', `${s.id}_schematic.svg`));

        return `
        <div class="lock-detail-sample" id="${escapeHtml(s.id.toLowerCase())}">"""

if old_sample_loop in code:
    code = code.replace(old_sample_loop, new_sample_loop)
    print("Replaced old_sample_loop with new_sample_loop successfully.")
else:
    print("Could not find exact old_sample_loop.")

with open("build.mjs", "w", encoding="utf-8") as f:
    f.write(code)
