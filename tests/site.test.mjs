/**
 * Build-output tests: things that are easy to break without noticing.
 *
 *  - no empty href/src anywhere (an unconfigured optional link must not render
 *    as an empty anchor)
 *  - every internal link and in-page anchor resolves
 *  - the optional product-site link appears only when configured, in both
 *    languages, in the header, the footer and the wizard
 *
 *   npm test
 */

import { execFileSync } from 'node:child_process';
import { readFileSync, readdirSync, statSync, existsSync } from 'node:fs';
import { join, dirname, normalize, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const SITE = join(ROOT, '_site');

let passed = 0;
const failures = [];
function check(name, condition, detail) {
  if (condition) { passed++; return; }
  failures.push(`${name}${detail ? ` — ${detail}` : ''}`);
}

function build(env = {}) {
  execFileSync(process.execPath, ['build.mjs'], {
    cwd: ROOT,
    stdio: 'pipe',
    env: { ...process.env, ...env },
  });
}

function htmlFiles(dir = SITE, acc = []) {
  for (const entry of readdirSync(dir)) {
    const full = join(dir, entry);
    if (statSync(full).isDirectory()) htmlFiles(full, acc);
    else if (entry.endsWith('.html')) acc.push(full);
  }
  return acc;
}

const read = (p) => readFileSync(p, 'utf8');

/* ---------- default build: no product site configured ---------- */

build();
const defaultFiles = htmlFiles();
check('the default build produces pages', defaultFiles.length > 100, `${defaultFiles.length} pages`);

let emptyAttrs = 0;
let productInDefault = 0;
for (const file of defaultFiles) {
  const html = read(file);
  emptyAttrs += (html.match(/(?:href|src)=""/g) || []).length;
  productInDefault += (html.match(/product-link/g) || []).length;
}
check('no empty href or src attributes when the product site is unconfigured', emptyAttrs === 0, `${emptyAttrs} found`);
check('no product link renders when the product site is unconfigured', productInDefault === 0, `${productInDefault} found`);

/* ---------- link and anchor integrity ---------- */

let broken = [];
let missingAnchors = [];
for (const file of defaultFiles) {
  const html = read(file);
  const rel = file.slice(ROOT.length + 1);
  for (const m of html.matchAll(/(?:href|src)="([^"#]+)(?:#[^"]*)?"/g)) {
    const url = m[1];
    if (/^(https?:|mailto:|data:|javascript:)/.test(url)) continue;
    const target = normalize(join(dirname(file), url));
    if (!existsSync(target)) broken.push(`${rel} -> ${url}`);
  }
  const ids = new Set([...html.matchAll(/\sid="([^"]+)"/g)].map((m) => m[1]));
  for (const m of html.matchAll(/href="#([^"]+)"/g)) {
    if (!ids.has(m[1])) missingAnchors.push(`${rel} -> #${m[1]}`);
  }
}
check('every internal link resolves', broken.length === 0, broken.slice(0, 5).join(', '));
check('every in-page anchor resolves', missingAnchors.length === 0, missingAnchors.slice(0, 5).join(', '));

/* ---------- both languages present for every English page ---------- */

// 404.html is deliberately a single page carrying both languages' links.
const enPages = defaultFiles
  .filter((f) => !f.includes(`${SITE}/zh/`))
  .map((f) => f.slice(SITE.length + 1))
  .filter((p) => p !== '404.html');
const missingZh = enPages.filter((p) => !existsSync(join(SITE, 'zh', p)));
check('every page has a Chinese counterpart', missingZh.length === 0, missingZh.slice(0, 5).join(', '));

/* ---------- product site configured ---------- */

const PRODUCT = 'https://example-lock.test/retrofit';
build({ PRODUCT_URL: PRODUCT });

for (const page of ['index.html', 'zh/index.html']) {
  const html = read(join(SITE, page));
  const isZh = page.startsWith('zh/');
  const expectedLabel = isZh ? '智能改造产品' : 'Retrofit hardware';

  check(`${page}: product link in the header`, html.includes(`<a class="product-link" href="${PRODUCT}"`), expectedLabel);
  check(`${page}: product link uses the localised label`, html.includes(`>${expectedLabel}</a>`));
  check(`${page}: product link in the footer`, html.includes('product-link--footer'));
}

const wizardHtml = read(join(SITE, 'identify.html'));
check('identify.html: wizard receives the product URL', wizardHtml.includes(`data-product-url="${PRODUCT}"`));
check('identify.html: wizard receives the product label', wizardHtml.includes('data-product-label="Retrofit hardware"'));

const wizardZh = read(join(SITE, 'zh/identify.html'));
check('zh/identify.html: wizard receives the localised label', wizardZh.includes('data-product-label="智能改造产品"'));

/* ---------- restore the normal build so _site is left clean ---------- */

build();
const restored = read(join(SITE, 'index.html'));
check('the default build is restored afterwards', !restored.includes('product-link'));

/* ---------- report ---------- */

if (failures.length) {
  for (const f of failures) console.error(`FAIL  ${f}`);
  console.error(`\n${failures.length} failed, ${passed} passed`);
  process.exit(1);
}
console.log(`site output: ${defaultFiles.length} pages checked, all links and anchors resolve`);
console.log(`OK  ${passed} checks passed`);
