import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync, statSync, existsSync } from 'node:fs';
import { join } from 'node:path';

function getAllFiles(dir, fileList = []) {
  if (!existsSync(dir)) return fileList;
  const files = readdirSync(dir);
  for (const file of files) {
    const fullPath = join(dir, file);
    if (statSync(fullPath).isDirectory()) {
      getAllFiles(fullPath, fileList);
    } else {
      fileList.push(fullPath);
    }
  }
  return fileList;
}

test('Privacy Guard: Guard exists in build.mjs and executes after all asset copies', () => {
  const buildScript = readFileSync(join(process.cwd(), 'build.mjs'), 'utf8');

  // 1. Verify PRIVATE_PUBLISH_PATHS constant definition
  assert.ok(
    buildScript.includes("PRIVATE_PUBLISH_PATHS = ['docs', join('assets', 'downloads')]") ||
    buildScript.includes('PRIVATE_PUBLISH_PATHS = ["docs", join("assets", "downloads")]') ||
    buildScript.includes("PRIVATE_PUBLISH_PATHS = ['docs', join('assets', 'downloads')];"),
    'build.mjs must define PRIVATE_PUBLISH_PATHS containing docs and assets/downloads'
  );

  // 2. Verify guard execution order: must execute after cpSync calls
  const lastCpSyncIndex = buildScript.lastIndexOf('cpSync(');
  const guardLoopIndex = buildScript.indexOf('for (const relPath of PRIVATE_PUBLISH_PATHS)');
  assert.ok(
    guardLoopIndex > lastCpSyncIndex,
    'Privacy guard loop must be executed after all cpSync / asset copying logic in build()'
  );

  // 3. Verify guard throws on failure
  assert.ok(
    buildScript.includes('throw new Error(') && buildScript.includes('Failed to remove private path'),
    'Privacy guard must throw an error if private paths cannot be removed from build output'
  );
});

test('Privacy Guard: No docs/ or assets/downloads/ directory exists in _site', () => {
  const siteDir = join(process.cwd(), '_site');
  const siteDocs = join(siteDir, 'docs');
  const siteDownloads = join(siteDir, 'assets', 'downloads');

  assert.equal(
    existsSync(siteDocs),
    false,
    '_site/docs must NOT exist in published site'
  );

  assert.equal(
    existsSync(siteDownloads),
    false,
    '_site/assets/downloads must NOT exist in published site'
  );
});

test('Privacy Guard: No public references to /docs/ or /assets/downloads/ in generated HTML, JSON, XML, TXT', () => {
  const siteDir = join(process.cwd(), '_site');
  const allFiles = getAllFiles(siteDir);
  const textExtensions = ['.html', '.json', '.xml', '.txt'];
  const violations = [];

  for (const file of allFiles) {
    if (!textExtensions.some(ext => file.endsWith(ext))) continue;

    const content = readFileSync(file, 'utf8');
    const relPath = file.slice(siteDir.length + 1);

    // Look for published hyperlinks or references to /docs/ or /assets/downloads/
    // Exclude github.com/.../docs/ links which point to internal GitHub repository
    const lines = content.split('\n');
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      if (
        (line.includes('/docs/') || line.includes('/assets/downloads/')) &&
        !line.includes('github.com')
      ) {
        violations.push(`${relPath}:${i + 1}: ${line.trim().slice(0, 100)}`);
      }
    }
  }

  assert.equal(
    violations.length,
    0,
    `Found private path references in published files:\n${violations.join('\n')}`
  );
});

test('Privacy Guard: Source docs/ and assets/downloads/ directories remain intact in workspace', () => {
  const sourceDocs = join(process.cwd(), 'docs');
  const sourceDownloads = join(process.cwd(), 'assets', 'downloads');

  assert.ok(
    existsSync(sourceDocs) && statSync(sourceDocs).isDirectory(),
    'Source docs/ directory must remain intact'
  );
  assert.ok(
    existsSync(sourceDownloads) && statSync(sourceDownloads).isDirectory(),
    'Source assets/downloads/ directory must remain intact'
  );

  const docsFiles = getAllFiles(sourceDocs);
  assert.ok(
    docsFiles.length > 0,
    'Source docs/ must not be empty or deleted'
  );

  const downloadFiles = getAllFiles(sourceDownloads);
  assert.ok(
    downloadFiles.length > 0,
    'Source assets/downloads/ must not be empty or deleted'
  );
});
