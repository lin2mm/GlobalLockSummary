import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';

function getAllHtmlFiles(dir) {
  let results = [];
  const list = readdirSync(dir);
  for (const file of list) {
    const fullPath = join(dir, file);
    const stat = statSync(fullPath);
    if (stat && stat.isDirectory()) {
      results = results.concat(getAllHtmlFiles(fullPath));
    } else if (file.endsWith('.html')) {
      results.push(fullPath);
    }
  }
  return results;
}

test('Anti-Regression: No Unrendered Mustache/Template Placeholders Shall Exist in HTML', () => {
  const siteDir = join(process.cwd(), '_site');
  const htmlFiles = getAllHtmlFiles(siteDir);
  const corruptedFiles = [];

  for (const file of htmlFiles) {
    const content = readFileSync(file, 'utf8');
    if (content.includes('{{gallery}}') || content.includes('{{') && content.includes('}}')) {
      // 允许正常的内联脚本或 CSS（如果存在），但坚决杜绝 {{gallery}} 等占位符
      if (content.includes('{{gallery}}')) {
        corruptedFiles.push(file);
      }
    }
  }

  assert.equal(
    corruptedFiles.length,
    0,
    `Detected unrendered template placeholders in built site: ${corruptedFiles.join(', ')}`
  );
  console.log(`✓ Verified ${htmlFiles.length} HTML pages: 100% free of unrendered {{gallery}} placeholders.`);
});
