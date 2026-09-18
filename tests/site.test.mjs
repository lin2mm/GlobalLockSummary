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
import vm from 'node:vm';
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

let feedbackPages = 0;
for (const file of defaultFiles) {
  const html = read(file);
  if (html.includes('id="feedback"') && html.includes('/assets/js/feedback.js')) feedbackPages++;
}
check('every page has the engineer feedback widget', feedbackPages === defaultFiles.length, `${feedbackPages}/${defaultFiles.length}`);

/* Run the browser script against a tiny DOM stub, without uploading anything. */
const feedbackSource = read(join(ROOT, 'assets/js/feedback.js'));
const feedbackDocument = { addEventListener() {}, querySelectorAll() { return []; } };
const feedbackContext = { document: feedbackDocument, window: {}, location: { pathname: '/locks/example.html' }, navigator: {} };
vm.runInNewContext(feedbackSource, feedbackContext);
const feedbackApi = feedbackContext.window.GlobalLockFeedback;
const nodes = {};
function node(name) {
  return {
    name, attrs: {}, value: '', href: '', textContent: '', children: [], listeners: {},
    getAttribute(key) { return this.attrs[key] || null; },
    setAttribute(key, value) { this.attrs[key] = value; },
    appendChild(child) { this.children.push(child); },
    addEventListener(event, fn) { this.listeners[event] = fn; },
  };
}
const root = node('root');
root.attrs = {
  'data-page-title': 'Example lock', 'data-page-path': 'locks/example.html',
  'data-issues-url': 'https://github.com/example/repo/issues',
  'data-i18n': JSON.stringify({ copied: 'Copied', categories: { correction: 'Correction', other: 'Other' } }),
};
nodes.category = node('category'); nodes.message = node('message'); nodes.issue = node('issue');
nodes.copy = node('copy'); nodes.status = node('status');
root.querySelector = (selector) => ({
  '[data-feedback-category]': nodes.category, '[data-feedback-message]': nodes.message,
  '[data-feedback-issue]': nodes.issue, '[data-feedback-copy]': nodes.copy,
  '[data-feedback-status]': nodes.status,
}[selector]);
feedbackDocument.createElement = () => node('option');
feedbackApi.init(root);
nodes.category.value = 'correction'; nodes.message.value = 'Backset is wrong'; nodes.category.listeners.change(); nodes.message.listeners.input();
check('feedback script runs with a DOM stub and builds the issue URL', nodes.issue.href.includes('/issues/new?title=') && nodes.issue.href.includes(encodeURIComponent('Backset is wrong')) && nodes.issue.href.includes(encodeURIComponent('locks/example.html')));

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
// When the default language lives at the site root, the root mirror contains
// the default-language pages too — those are checked separately. Here we only
// verify that every English page under /en/ has a Chinese counterpart under /zh/.
const enPages = defaultFiles
  .filter((f) => f.includes(`${SITE}/en/`))
  .map((f) => f.slice(SITE.length + 1).replace(/^en\//, ''))
  .filter((p) => p !== '404.html');
const missingZh = enPages.filter((p) => !existsSync(join(SITE, 'zh', p)));
check('every English page has a Chinese counterpart under /zh/', missingZh.length === 0, missingZh.slice(0, 5).join(', '));

// The default-language mirror at the site root must contain exactly the same
// pages as the default-language subdirectory (/zh/ in this config). Anything
// else at the root is a bug — the root should never serve non-default content.
const rootMirror = defaultFiles
  .filter((f) => {
    const rel = f.slice(SITE.length + 1);
    if (rel.includes('/')) return false; // subdirectories are not part of the root mirror
    return existsSync(join(SITE, 'zh', rel));
  })
  .map((f) => f.slice(SITE.length + 1));
const expectedRootMirror = defaultFiles
  .filter((f) => f.includes(`${SITE}/zh/`) && !f.slice(SITE.length + 1).replace(/^zh\//, '').includes('/'))
  .map((f) => f.slice(SITE.length + 1).replace(/^zh\//, ''));
const extra = rootMirror.filter((p) => !expectedRootMirror.includes(p));
const missing = expectedRootMirror.filter((p) => !rootMirror.includes(p));
check('default-language mirror at the site root matches /zh/ exactly',
  extra.length === 0 && missing.length === 0,
  `extra=${extra.slice(0, 3).join(',')} missing=${missing.slice(0, 3).join(',')}`);

/* ---------- product site configured ---------- */

const PRODUCT = 'https://example-lock.test/retrofit';
build({ PRODUCT_URL: PRODUCT });

// The root /index.html and /identify.html serve the default language
// (Chinese in this config), while /en/ serves English. The labels below must
// track content/site.json#defaultLang — change them together.
const DEFAULT_LABEL = '后装智能锁';
const EN_LABEL = 'Retrofit Smart Lock';

for (const page of ['index.html', 'zh/index.html']) {
  const html = read(join(SITE, page));
  // The root /index.html serves the default language, so it uses DEFAULT_LABEL.
  // /zh/index.html is an explicit copy of the same content under /zh/.
  const expectedLabel = DEFAULT_LABEL;

  check(`${page}: product link in the header`, html.includes(`<a class="product-link" href="${PRODUCT}"`), expectedLabel);
  check(`${page}: product link uses the localised label`, html.includes(`>${expectedLabel}</a>`));
  check(`${page}: product link in the footer`, html.includes('product-link--footer'));
}

const wizardHtml = read(join(SITE, 'identify.html'));
check('identify.html: wizard receives the product URL', wizardHtml.includes(`data-product-url="${PRODUCT}"`));
check('identify.html: wizard receives the localised label', wizardHtml.includes(`data-product-label="${DEFAULT_LABEL}"`));

const wizardZh = read(join(SITE, 'zh/identify.html'));
check('zh/identify.html: wizard receives the localised label', wizardZh.includes(`data-product-label="${DEFAULT_LABEL}"`));

const wizardEn = read(join(SITE, 'en/identify.html'));
check('en/identify.html: wizard receives the English label', wizardEn.includes(`data-product-label="${EN_LABEL}"`));

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


/* ---------- gallery wall & images test ---------- */
const galleryJsonPath = join(ROOT, 'content/catalog/gallery.json');
check('gallery.json exists', existsSync(galleryJsonPath));
if (existsSync(galleryJsonPath)) {
  const galleryItems = JSON.parse(read(galleryJsonPath));
  check('gallery has 38 candidate items across 5 blocks', galleryItems.length === 38, `count=${galleryItems.length}`);
  
  let missingImgs = 0;
  for (const item of galleryItems) {
    const relImg = item.image.replace(/^\//, '');
    if (!existsSync(join(SITE, relImg))) {
      missingImgs++;
    }
  }
  check('all 38 gallery images exist in _site/', missingImgs === 0, `missing=${missingImgs}`);

  const rootIndex = read(join(SITE, 'index.html'));
  check('root index.html renders pure gallery portal grid with 5 major area images', rootIndex.includes('gallery-portal-grid') && rootIndex.includes('gallery-portal-card'));
  check('root index.html links to regional category pages', rootIndex.includes('/categories/na.html') && rootIndex.includes('/categories/latam.html'));

  const naCategory = read(join(SITE, 'zh/categories/na.html'));
  check('regional category renders block hero and lock cards', naCategory.includes('block-hero') && naCategory.includes('hero-na-deadbolt.jpg') && naCategory.includes('gallery-card'));

  const identifyZh = read(join(SITE, 'identify.html'));
  check('identify.html wizard links directly to Japan engraving directory', identifyZh.includes('japan-engravings.html'));
  
  const fieldIssuesZh = read(join(SITE, 'field-issues.html'));
  check('field-issues.html renders crawled real-world complaints', fieldIssuesZh.includes('Motor Blocked') && fieldIssuesZh.includes('Reddit') && fieldIssuesZh.includes('HDB'));

  const indigenousZh = read(join(SITE, 'indigenous-guides.html'));
  check('indigenous-guides.html renders terminology and authentic photos', indigenousZh.includes('Dornmaß') && indigenousZh.includes('de-dornmass-pz.png') && indigenousZh.includes('Gefahrenfunktion') && indigenousZh.includes('フロント刻印'));

  const jpEngravingsZh = read(join(SITE, 'japan-engravings.html'));
  check('japan-engravings.html renders MIWA and GOAL matrix', jpEngravingsZh.includes('MIWA') && jpEngravingsZh.includes('13LA') && jpEngravingsZh.includes('template-miwa-la.jpg'));

  const adaptersZh = read(join(SITE, 'adapters.html'));
  check('adapters.html renders 7mm to 8mm and BOM specs', adaptersZh.includes('7mm') && adaptersZh.includes('adapter-7to8mm.png'));

  const templatesZh = read(join(SITE, 'drilling-templates.html'));
  check('drilling-templates.html renders 1:1 drilling parameters', templatesZh.includes('54mm') && templatesZh.includes('template-schlage-b60.png'));

  const bestsellersZh = read(join(SITE, 'bestseller-matrix.html'));
  check('bestseller-matrix.html renders top selling locks comparison', bestsellersZh.includes('Kwikset') && bestsellersZh.includes('bestseller-deadbolt.jpg'));

  const retrofitZh = read(join(SITE, 'retrofit.html'));
  check('retrofit.html covers real-world failure cases & complaints', retrofitZh.includes('Nuki') && retrofitZh.includes('Motor Blocked'));
  check('root index.html includes in-site direct feedback button', rootIndex.includes('data-feedback-submit'));

  const enIndex = read(join(SITE, 'en/index.html'));
  check('en index.html renders pure gallery portal', enIndex.includes('gallery-portal-grid') && enIndex.includes('gallery-portal-card'));
}


// Check that nav link for catalog dynamically includes lock count
const zhIndexPage = read(join(SITE, 'zh/index.html'));
const galleryCount = JSON.parse(read(join(ROOT, 'content/catalog/gallery.json'))).length;
check(`Catalog nav link includes dynamic count (${galleryCount})`, zhIndexPage.includes(`(${galleryCount})`));

console.log(`OK  ${passed} checks passed`);
