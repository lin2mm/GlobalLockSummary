# -*- coding: utf-8 -*-
with open("build.mjs", "r", encoding="utf-8") as f:
    code = f.read()

# 替换 gallerySectionHtml 的模板字符串
old_gallery_section = """    gallerySectionHtml = `
<h2 id="installation-samples">${lang === 'zh' ? '实物安装与改造图谱' : 'Installation Photos & Retrofit Diagrams'}</h2>
<p class="lede">${lang === 'zh' ? '以下为该锁族在实际门上的实物安装案例、传动原理示意图与智能化改造常见问题分析：' : 'Field installation examples, drive schematics, and common retrofit failure modes for this lock family:'}</p>
<div class="lock-detail-samples">
  ${sampleCards}
</div>
${fieldCasesHtml}
`;"""

new_gallery_section = """    gallerySectionHtml = `
<h2 id="installation-samples">${lang === 'zh' ? '实物安装与改造图谱' : 'Installation Photos & Retrofit Diagrams'}</h2>
<p class="lede">${lang === 'zh' ? '以下为该锁族在实际门上的实物安装案例、传动原理示意图与智能化改造常见问题分析：' : 'Field installation examples, drive schematics, and common retrofit failure modes for this lock family:'}</p>
${topClusterNavHtml}
${clusterSectionsHtml}
${fieldCasesHtml}
`;"""

if old_gallery_section in code:
    code = code.replace(old_gallery_section, new_gallery_section)
    print("Replaced old_gallery_section successfully.")
else:
    print("Could not find exact old_gallery_section.")

# 更新 headings 数组，将 clusterHeadings 注入
old_headings = """  const headings = [
    ...(matchedSamples.length ? [{ level: 2, id: 'installation-samples', text: lang === 'zh' ? '实物安装与改造图谱' : 'Installation Photos & Retrofit Diagrams' }] : []),"""

new_headings = """  const headings = [
    ...(matchedSamples.length ? [{ level: 2, id: 'installation-samples', text: lang === 'zh' ? '实物安装与改造图谱' : 'Installation Photos & Retrofit Diagrams' }] : []),
    ...clusterHeadings,"""

if old_headings in code:
    code = code.replace(old_headings, new_headings)
    print("Injected clusterHeadings into headings array successfully.")
else:
    print("Could not find exact old_headings.")

with open("build.mjs", "w", encoding="utf-8") as f:
    f.write(code)
