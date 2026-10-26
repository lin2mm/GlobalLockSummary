# -*- coding: utf-8 -*-
import re

with open("build.mjs", "r", encoding="utf-8") as f:
    code = f.read()

# 检查分类逻辑代码实现
cluster_helper_js = """
function getSampleCluster(sample, lang) {
  const isZh = lang === 'zh';
  const t = ((sample.title && (sample.title[lang] || sample.title.en || sample.title.zh)) || sample.id).toLowerCase();
  
  if (t.includes('thumbturn') || t.includes('手扭') || t.includes('旋钮')) {
    return {
      id: 'cluster-thumbturn',
      name: isZh ? '内侧旋转手扭 (Thumbturn)' : 'Thumbturn Cylinders',
      tag: 'Thumbturn'
    };
  }
  if (t.includes('双锁芯') || t.includes('double cylinder') || t.includes('30/30') || t.includes('35/35') || t.includes('abus') || t.includes('evva') || t.includes('diamant') || t.includes('bluechip')) {
    return {
      id: 'cluster-double-cyl',
      name: isZh ? '双面槽型锁芯 (Double Cylinder)' : 'Double Keyed Cylinders',
      tag: isZh ? '双锁芯' : 'Double Cyl'
    };
  }
  if (t.includes('插芯锁体') || t.includes('mortice') || t.includes('mortise') || t.includes('onefit') || t.includes('bricard') || t.includes('electa') || t.includes('pado') || t.includes('la fonte') || t.includes('silvana') || t.includes('stam') || t.includes('gcc') || t.includes('union') || t.includes('chubb')) {
    return {
      id: 'cluster-mortise-case',
      name: isZh ? '欧标/窄体插芯锁体 (Mortise Case)' : 'Mortise Lock Cases',
      tag: isZh ? '插芯锁体' : 'Mortise Case'
    };
  }
  return {
    id: 'cluster-specialty',
    name: isZh ? '特种防盗与异形锁 (Specialty / High-Security)' : 'Specialty & High-Security',
    tag: isZh ? '特种锁' : 'Specialty'
  };
}
"""

# 在 lockPage 前插入 cluster_helper_js
if "function getSampleCluster(" not in code:
    code = code.replace("function lockPage(fam, lang) {", cluster_helper_js + "\nfunction lockPage(fam, lang) {")

with open("build.mjs", "w", encoding="utf-8") as f:
    f.write(code)

print("Injected getSampleCluster into build.mjs.")
