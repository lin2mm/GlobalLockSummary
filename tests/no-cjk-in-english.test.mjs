import test from 'node:test';
import assert from 'node:assert/strict';
import { readdirSync, readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';

const EN_DIR = '_site/en';
const CJK_REGEX = /[\u4e00-\u9fff]/;

// 允许出现的特定上下文豁免：
// 1. 语言切换器链接：<a class="langswitch__link" ...>中文</a>
// 2. contribute.md 说明中包含 "中文" 这一语言称呼
// 3. 日本面板刻印与防犯旋钮的母语术语标注（如 フロント刻印, 防犯サムターン）
// 4. 双语大词典（glossary.html）的中英文对照表
const isExemptLine = (line, filePath) => {
  if (line.includes('class="langswitch__link"') && line.includes('中文')) return true;
  if (filePath.endsWith('glossary.html')) return true;
  if (filePath.endsWith('japan-engravings.html')) return true;
  if (filePath.endsWith('contribute.html') && line.includes('English and 中文')) return true;
  if (line.includes('フロント刻印') || line.includes('防犯サムターン')) return true;
  return false;
};

test('Anti-Leak Guard: Zero Unexpected CJK Characters in _site/en HTML Pages', () => {
  const leaks = [];

  const walk = (dir) => {
    for (const file of readdirSync(dir)) {
      const fullPath = join(dir, file);
      if (statSync(fullPath).isDirectory()) {
        walk(fullPath);
      } else if (file.endsWith('.html')) {
        const lines = readFileSync(fullPath, 'utf8').split('\n');
        for (let i = 0; i < lines.length; i++) {
          const line = lines[i];
          if (CJK_REGEX.test(line)) {
            if (!isExemptLine(line, fullPath)) {
              leaks.push({ file: fullPath, lineNo: i + 1, content: line.trim() });
            }
          }
        }
      }
    }
  };

  walk(EN_DIR);

  if (leaks.length > 0) {
    console.error(`Found ${leaks.length} unexpected CJK occurrences in English pages:`);
    for (const leak of leaks.slice(0, 10)) {
      console.error(`  ${leak.file}:${leak.lineNo} => ${leak.content.slice(0, 100)}`);
    }
  }

  assert.equal(leaks.length, 0, `English pages must be 100% free of unexpected CJK characters, but found ${leaks.length}`);
});
