# -*- coding: utf-8 -*-
import re

with open("build.mjs", "r", encoding="utf-8") as f:
    code = f.read()

# 检查 sampleCards.map 的闭合处
# 原先是：
#       </div>`;
#     }).join('\n');
#
#     // Ingest all matching field cases from installation-cases.json for high-immersion jobsite experience

old_close = """        ` : ''}
      </div>`;
    }).join('\\n');

    // Ingest all matching field cases from installation-cases.json for high-immersion jobsite experience"""

new_close = """        ` : ''}
      </div>`;
      }).join('\\n');

      if (isMultiCluster) {
        clusterSectionsHtml += `
        <div class="lock-cluster-group" id="${c.id}" style="margin-top: 24px; padding-top: 12px; border-top: 1px dashed #cbd5e1;">
          <h3 style="margin: 0 0 14px; font-size: 1.05rem; font-weight: 800; color: #0B1D47; display: flex; align-items: center; justify-content: space-between;">
            <span>⌖ ${escapeHtml(c.name)}</span>
            <span style="font-size: 0.72rem; font-weight: 600; color: #64748b; background: #f1f5f9; padding: 2px 8px; border-radius: 4px; border: 1px solid #e2e8f0;">${c.items.length} ${lang === 'zh' ? '款典型型号' : 'models'}</span>
          </h3>
          <div class="lock-detail-samples">
            ${cardsForCluster}
          </div>
        </div>`;
      } else {
        clusterSectionsHtml += `
        <div class="lock-detail-samples">
          ${cardsForCluster}
        </div>`;
      }
    }

    // Ingest all matching field cases from installation-cases.json for high-immersion jobsite experience"""

if old_close in code:
    code = code.replace(old_close, new_close)
    print("Replaced old_close successfully.")
else:
    print("Could not find exact old_close, checking with normalized newlines...")
    # 尝试正则替换
    pattern = r'(\s*\`\s*\:\s*\'\'\}\s*<\/div>\`;\s*\}\)\.join\(\'\\n\'\);\s*\/\/\s*Ingest all matching field cases)'
    if re.search(pattern, code):
        print("Found regex match for old_close!")

with open("build.mjs", "w", encoding="utf-8") as f:
    f.write(code)
