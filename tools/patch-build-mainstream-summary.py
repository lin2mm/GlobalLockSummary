with open('build.mjs', 'r', encoding='utf-8') as f:
    text = f.read()

# 在分类画廊顶部增加权威的一句话说明横幅 (Mainstream Executive Summary Banner)
target = """          <div class="gallery-tier-filter" style="display: flex; gap: 8px; margin: 14px 0 0; flex-wrap: wrap; align-items: center;">"""

replacement = """          <!-- 顶部一句话直观说明主流几款、小众几款及其研发指导 -->
          <div class="mainstream-summary-banner" style="margin-top: 14px; padding: 10px 14px; background: #f0fdf4; border: 1px solid #bbf7d0; border-left: 4px solid #16a34a; border-radius: 6px; font-size: 0.85rem; color: #166534; line-height: 1.5;">
            <b>💡 ${isZh ? '出海研发选型导读' : 'Market Breakdown'}:</b> 
            ${isZh 
              ? `本板块共收录 <b>${block.items.length}</b> 款门锁样本，其中 <b>★ 主流基准锁占 ${block.items.filter(i => i.tierClass === 'Mainstream').length} 款</b>（深蓝高亮·覆盖当地 ≥80% 存量），<b>🔍 小众/特殊结构占 ${block.items.filter(i => i.tierClass !== 'Mainstream').length} 款</b>（浅灰淡色·特殊老房与长尾）。大货开模与现货配件优先保障主流锁型。`
              : `This division catalogs <b>${block.items.length}</b> lock models: <b>★ ${block.items.filter(i => i.tierClass === 'Mainstream').length} Mainstream Baselines</b> (bold blue outline, covering ≥80% market share) and <b>🔍 ${block.items.filter(i => i.tierClass !== 'Mainstream').length} Niche / Specialty Models</b> (muted tone, vintage & long-tail). Standardize tooling on mainstream locks.`
            }
          </div>

          <div class="gallery-tier-filter" style="display: flex; gap: 8px; margin: 12px 0 0; flex-wrap: wrap; align-items: center;">"""

if target in text:
    text = text.replace(target, replacement, 1)
    print("Injected Mainstream Summary Banner into category header!")
else:
    print("Target block not found in build.mjs!")

with open('build.mjs', 'w', encoding='utf-8') as f:
    f.write(text)

print("build.mjs successfully updated with Top Mainstream Summary Banner!")
