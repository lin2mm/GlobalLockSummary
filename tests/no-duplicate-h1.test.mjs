import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';
import test from 'node:test';
import assert from 'node:assert/strict';

function getAllHtmlFiles(dir, fileList = []) {
  const files = readdirSync(dir);
  for (const file of files) {
    const fullPath = join(dir, file);
    if (statSync(fullPath).isDirectory()) {
      getAllHtmlFiles(fullPath, fileList);
    } else if (file.endsWith('.html')) {
      fileList.push(fullPath);
    }
  }
  return fileList;
}

test('Anti-Regression: No Page Shall Have Duplicate H1 Headings', () => {
  const allHtmls = getAllHtmlFiles('_site');
  let checked = 0;
  for (const htmlPath of allHtmls) {
    const content = readFileSync(htmlPath, 'utf8');
    const h1Matches = content.match(/<h1[\s>]/g) || [];
    assert.ok(
      h1Matches.length <= 1,
      `Violation in ${htmlPath}: Found ${h1Matches.length} <h1> tags! Must have at most 1 <h1>.`
    );
    checked++;
  }
  console.log(`✓ Verified ${checked} HTML pages: 100% free of duplicate <h1> headings.`);
});
