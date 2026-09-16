/**
 * GlobalLockSummary build.
 *
 * Zero dependencies on purpose: `node build.mjs` reads `content/` and writes
 * plain, fully-rendered HTML to `_site/`. Static HTML (rather than a client-side
 * app) is a deliberate choice — crawlers, translators and archive bots must be
 * able to read every page without executing anything.
 *
 * Usage:
 *   node build.mjs            build once
 *   node build.mjs --watch    rebuild on change
 */

import { readFileSync, writeFileSync, mkdirSync, rmSync, cpSync, existsSync, readdirSync, watch } from 'node:fs';
import { join, dirname, relative, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { renderMarkdown, splitFrontMatter, slugify, escapeHtml } from './src/markdown.mjs';
import { layout, buildToc, faqJsonLd, techArticleJsonLd } from './src/layout.mjs';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)));
const CONTENT = join(ROOT, 'content');
const OUT = join(ROOT, '_site');
const BASE_URL = process.env.SITE_URL || 'https://lin2mm.github.io/GlobalLockSummary';
const BUILD_DATE = new Date().toISOString().slice(0, 10);

const readJson = (path) => JSON.parse(readFileSync(path, 'utf8'));
const t = (dict, key, lang) => dict?.[key]?.[lang] || dict?.[key]?.en || key;

/* ------------------------------------------------------------------ *
 * Load content
 * ------------------------------------------------------------------ */

const site = readJson(join(CONTENT, 'site.json'));
// The product-site link is optional. An env override exists so both states
// (published / not published) can be built and verified without editing data.
if (process.env.PRODUCT_URL && site.product) site.product.url = process.env.PRODUCT_URL;
const terms = readJson(join(CONTENT, 'i18n', 'terms.json'));
const architecturesDoc = readJson(join(CONTENT, 'catalog', 'retrofit-architectures.json'));
const standardsDoc = readJson(join(CONTENT, 'catalog', 'standards.json'));
const devicesDoc = readJson(join(CONTENT, 'catalog', 'smart-locks.json'));
const decisionTree = readJson(join(CONTENT, 'catalog', 'decision-tree.json'));

const FAMILIES_DIR = join(CONTENT, 'catalog', 'lock-families');
const families = readdirSync(FAMILIES_DIR)
  .filter((f) => f.endsWith('.json'))
  .map((f) => readJson(join(FAMILIES_DIR, f)))
  .sort((a, b) => a.id.localeCompare(b.id));

const familyById = Object.fromEntries(families.map((f) => [f.id, f]));
const archById = Object.fromEntries(architecturesDoc.architectures.map((a) => [a.id, a]));
const standardById = Object.fromEntries(standardsDoc.standards.map((s) => [s.id, s]));
const deviceById = Object.fromEntries(devicesDoc.devices.map((d) => [d.id, d]));

const LANGS = Object.keys(site.languages);
const dirFor = (lang) => site.languages[lang].dir;
const urlFor = (lang, slug) => {
  const d = dirFor(lang);
  return (d ? `${d}/` : '') + slug;
};
const hrefFor = (lang, slug) => `/${urlFor(lang, slug)}`;

/**
 * Depth prefix for a page path: "index.html" -> "", "locks/x.html" -> "../",
 * "zh/locks/x.html" -> "../../".
 */
export function prefixFor(path) {
  const depth = path.split('/').length - 1;
  return '../'.repeat(depth);
}

/**
 * GitHub Pages serves a project site from /<repo>/, not from the domain root, so
 * every root-relative href/src is rewritten to be relative to the page. This is
 * the single place that happens — templates keep using clean "/foo" paths, and
 * the same output works on a custom domain bound at the root.
 */
export function rebaseLinks(html, path) {
  const prefix = prefixFor(path);
  if (!prefix) return html;
  return html.replace(/(href|src)="\/(?!\/)/g, `$1="${prefix}`);
}

/* ------------------------------------------------------------------ *
 * Output helpers
 * ------------------------------------------------------------------ */

function write(path, contents) {
  const full = join(OUT, path);
  mkdirSync(dirname(full), { recursive: true });
  writeFileSync(full, contents);
  return path;
}

const pagesWritten = [];

function emitPage({ lang, slug, title, description, bodyHtml, breadcrumbs = [], jsonLd = [], headings = [], extraHead = '' }) {
  const path = urlFor(lang, slug);
  const alternates = LANGS
    .filter((l) => existsFor(l, slug))
    .map((l) => ({ lang: l, href: `${BASE_URL}/${urlFor(l, slug)}`, path: urlFor(l, slug) }));

  const html = layout({
    title: title.includes(site.name) ? title : `${title} · ${site.name}`,
    description,
    lang,
    path,
    baseUrl: BASE_URL,
    // Navigation hrefs are root-relative so the site works from any sub-path.
    site: { ...site, navigation: { [lang]: rewriteNav(site.navigation[lang]) } },
    body: bodyHtml,
    breadcrumbs,
    alternates: alternates.map((a) => ({ ...a, href: a.href })),
    jsonLdBlocks: jsonLd,
    extraHead,
    toc: buildToc(headings),
  });

  pagesWritten.push(write(path, rebaseLinks(html, path)));
  return path;
}

/** Turn navigation hrefs into root-relative paths that work from any depth. */
function rewriteNav(nav) {
  return nav.map((item) => ({ ...item, href: item.href.startsWith('/') ? item.href : `/${item.href}` }));
}

/** Does this slug exist in this language? Used for hreflang alternates. */
const existing = new Set();
function existsFor(lang, slug) {
  return existing.has(`${lang}:${slug}`);
}
function register(lang, slug) {
  existing.add(`${lang}:${slug}`);
}

/* ------------------------------------------------------------------ *
 * Reusable HTML fragments
 * ------------------------------------------------------------------ */

function statusBadge(status, lang) {
  const label = t(terms.labels, status === 'verified' ? 'verified' : 'needs-review', lang);
  return `<span class="badge badge--${status}" title="${escapeHtml(label)}">${status === 'verified' ? '✓' : '⚠'} ${status === 'verified' ? (lang === 'zh' ? '已核对' : 'verified') : (lang === 'zh' ? '待核对' : 'needs review')}</span>`;
}

function measurementRows(list, lang) {
  return list
    .map((m) => {
      const label = t(terms.measurements, m.key, lang);
      const how = m.how?.[lang] || m.how?.en || '';
      return `<tr><th scope="row">${escapeHtml(label)}</th><td><code>${escapeHtml(localizedText(m.typical, lang))}</code></td><td>${escapeHtml(localizedText(m.tolerance, lang) || '—')}</td><td>${escapeHtml(how)}</td></tr>`;
    })
    .join('\n');
}

function linkList(ids, lang, kind) {
  const prefix = kind === 'standard' ? 'standards/' : 'locks/';
  const lookup = kind === 'standard' ? standardById : familyById;
  const labelOf = kind === 'standard'
    ? (id) => lookup[id]?.code || id
    : (id) => lookup[id]?.title?.[lang] || lookup[id]?.title?.en || id;
  return ids
    .filter((id) => lookup[id])
    .map((id) => `<a href="${hrefFor(lang, prefix + id + '.html')}">${escapeHtml(labelOf(id))}</a>`)
    .join(' · ') || '—';
}

function sourceList(sources, lang) {
  if (!sources?.length) return '';
  return `<section class="sources"><h2 id="sources">${escapeHtml(t(terms.labels, 'sources', lang))}</h2><ul>${sources
    .map((s) => `<li><a href="${escapeHtml(s.url)}" rel="external noopener">${escapeHtml(s.title)}</a></li>`)
    .join('\n')}</ul></section>`;
}

function faqBlock(faq, lang) {
  if (!faq?.length) return '';
  return `<section class="faq"><h2 id="questions">${escapeHtml(t(terms.labels, 'faq', lang))}</h2>${faq
    .map((f) => `<details><summary>${escapeHtml(f.q)}</summary><p>${escapeHtml(f.a)}</p></details>`)
    .join('\n')}</section>`;
}

function bilingualList(obj, lang, tag = 'ul') {
  const items = localized(obj, lang);
  if (!items.length) return '';
  return `<${tag}>${items.map((i) => `<li>${escapeHtml(i)}</li>`).join('')}</${tag}>`;
}

/**
 * Localised content arrives in two shapes across the catalog:
 *   { en: [...], zh: [...] }   — independent lists
 *   [ { en: '…', zh: '…' } ]   — paired items that must stay aligned
 * This returns a plain array of strings for the requested language.
 */
function localized(obj, lang) {
  if (!obj) return [];
  if (Array.isArray(obj)) {
    return obj.map((item) => (typeof item === 'string' ? item : item[lang] || item.en || '')).filter(Boolean);
  }
  return obj[lang] || obj.en || [];
}

/** Same as localized() but for a single string rather than a list. */
function localizedText(obj, lang) {
  if (!obj) return '';
  if (typeof obj === 'string') return obj;
  return obj[lang] || obj.en || '';
}

/* ------------------------------------------------------------------ *
 * Generated pages: lock families
 * ------------------------------------------------------------------ */

function lockIndexBody(lang) {
  const byRegion = new Map();
  for (const fam of families) {
    for (const region of fam.regions) {
      if (!byRegion.has(region)) byRegion.set(region, []);
      byRegion.get(region).push(fam);
    }
  }
  const intro = `<p>${escapeHtml(lang === 'zh'
    ? '本站收录的锁族。每一页给出：结构、必须测量的参数与公差、相关标准、可用的改造架构与已知阻碍。'
    : 'The lock families catalogued here. Each page gives anatomy, the parameters you must measure with their tolerances, related standards, the retrofit architectures that work, and the known blockers.')}</p>`;

  const table = `<div class="table-wrap"><table>
<thead><tr><th>${lang === 'zh' ? '锁族' : 'Lock family'}</th><th>${lang === 'zh' ? '常见地区' : 'Regions'}</th><th>${t(terms.labels, 'status', lang)}</th><th>${lang === 'zh' ? '改造架构' : 'Retrofit'}</th></tr></thead>
<tbody>
${families.map((f) => `<tr>
  <td><a href="${hrefFor(lang, 'locks/' + f.id + '.html')}">${escapeHtml(f.title[lang] || f.title.en)}</a></td>
  <td>${escapeHtml(f.regions.slice(0, 4).join(', '))}</td>
  <td>${statusBadge(f.status, lang)}</td>
  <td>${f.retrofit.architectures.length ? f.retrofit.architectures.map((a) => escapeHtml(t(terms.architecture, a, lang))).join(', ') : escapeHtml(lang === 'zh' ? '无干净方案' : 'no clean path')}</td>
</tr>`).join('\n')}
</tbody></table></div>`;

  const regionBlocks = [...byRegion.entries()].sort((a, b) => a[0].localeCompare(b[0])).map(([region, list]) => `
<section><h2 id="${slugify(region)}">${escapeHtml(region)}</h2><ul>${list.map((f) => `<li><a href="${hrefFor(lang, 'locks/' + f.id + '.html')}">${escapeHtml(f.title[lang] || f.title.en)}</a> — ${escapeHtml(f.summary[lang] || f.summary.en)}</li>`).join('')}</ul></section>`).join('\n');

  const headings = [{ level: 2, id: 'all', text: lang === 'zh' ? '全部锁族' : 'All lock families' },
    ...[...byRegion.keys()].sort((a, b) => a.localeCompare(b)).map((r) => ({ level: 2, id: slugify(r), text: r }))];

  return { html: `${intro}<h2 id="all">${lang === 'zh' ? '全部锁族' : 'All lock families'}</h2>${table}${regionBlocks}`, headings };
}

function lockPage(fam, lang) {
  const order = (fam.measureOrder || []).map((k) => t(terms.measurements, k, lang));
  const rows = measurementRows(fam.measurements, lang);
  const archList = fam.retrofit.architectures.length
    ? `<ul>${fam.retrofit.architectures.map((id) => {
        const a = archById[id];
        return `<li><a href="${hrefFor(lang, 'retrofit/' + id + '.html')}">${escapeHtml(t(terms.architecture, id, lang))}</a>${a ? ` — ${escapeHtml(a.principle[lang] || a.principle.en)}` : ''}</li>`;
      }).join('')}</ul>`
    : `<p class="warn">${escapeHtml(lang === 'zh' ? '本锁族没有干净的改造方案。见下方说明。' : 'There is no clean retrofit path for this family. See the note below.')}</p>`;

  const devices = devicesDoc.devices.filter((d) => d.fits.includes(fam.id));
  const deviceHtml = devices.length
    ? `<section><h2 id="devices">${lang === 'zh' ? '参考设备' : 'Reference devices'}</h2><p>${escapeHtml(lang === 'zh' ? '作为工程示例记录，不是推荐或销售。' : 'Recorded as engineering examples, not endorsements.')}</p><ul>${devices.map((d) => `<li><a href="${hrefFor(lang, 'devices/' + d.id + '.html')}">${escapeHtml(d.name)}</a> — ${escapeHtml(t(terms.architecture, d.architecture, lang))} ${statusBadge(d.status, lang)}</li>`).join('')}</ul></section>`
    : '';

  const html = `
<p class="lede">${escapeHtml(fam.summary[lang] || fam.summary.en)}</p>
<p class="meta">${statusBadge(fam.status, lang)} <span class="meta__sep">·</span> <strong>${escapeHtml(t(terms.labels, 'regions', lang))}:</strong> ${escapeHtml(fam.regions.join(', '))}</p>
${fam.aliases ? `<p><strong>${escapeHtml(t(terms.labels, 'aliases', lang))}:</strong> ${escapeHtml((fam.aliases[lang] || fam.aliases.en || []).join(' · '))}</p>` : ''}

<h2 id="anatomy">${escapeHtml(t(terms.labels, 'anatomy', lang))}</h2>
${bilingualList(fam.anatomy, lang)}

<h2 id="measurements">${escapeHtml(lang === 'zh' ? '必须测量的参数' : 'Parameters to measure')}</h2>
<p>${escapeHtml(t(terms.labels, 'measureInThisOrder', lang))}: <code>${escapeHtml(order.join(' → '))}</code></p>
<div class="table-wrap"><table>
<thead><tr><th>${lang === 'zh' ? '参数' : 'Parameter'}</th><th>${escapeHtml(t(terms.labels, 'typical', lang))}</th><th>${escapeHtml(t(terms.labels, 'tolerance', lang))}</th><th>${escapeHtml(t(terms.labels, 'howToMeasure', lang))}</th></tr></thead>
<tbody>${rows}</tbody></table></div>

<h2 id="retrofit">${escapeHtml(t(terms.labels, 'retrofitArchitectures', lang))}</h2>
${archList}
${fam.retrofit.notes ? `<p>${escapeHtml(fam.retrofit.notes[lang] || fam.retrofit.notes.en)}</p>` : ''}

<h2 id="standards">${escapeHtml(t(terms.labels, 'standards', lang))}</h2>
<p>${linkList(fam.standards, lang, 'standard')}</p>

${deviceHtml}
${faqBlock(fam.faq?.[lang] || fam.faq?.en, lang)}
${sourceList(fam.sources, lang)}

<p class="record-link"><a href="${escapeHtml(site.urls.repository)}/blob/main/content/catalog/lock-families/${escapeHtml(fam.id)}.json">${escapeHtml(t(terms.labels, 'openFile', lang))}</a></p>
`;

  const headings = [
    { level: 2, id: 'anatomy', text: t(terms.labels, 'anatomy', lang) },
    { level: 2, id: 'measurements', text: lang === 'zh' ? '必须测量的参数' : 'Parameters to measure' },
    { level: 2, id: 'retrofit', text: t(terms.labels, 'retrofitArchitectures', lang) },
    { level: 2, id: 'standards', text: t(terms.labels, 'standards', lang) },
    ...(devices.length ? [{ level: 2, id: 'devices', text: lang === 'zh' ? '参考设备' : 'Reference devices' }] : []),
    ...(fam.faq?.[lang]?.length || fam.faq?.en?.length ? [{ level: 2, id: 'questions', text: t(terms.labels, 'faq', lang) }] : []),
  ];

  const ld = [
    faqJsonLd(fam.faq?.[lang] || fam.faq?.en),
    {
      '@context': 'https://schema.org',
      '@type': 'Product',
      name: fam.title[lang] || fam.title.en,
      category: 'Door lock',
      description: fam.summary[lang] || fam.summary.en,
      additionalProperty: fam.measurements.map((m) => ({
        '@type': 'PropertyValue',
        name: t(terms.measurements, m.key, 'en'),
        value: m.typical,
      })),
    },
  ];

  return { html, headings, ld };
}

/* ------------------------------------------------------------------ *
 * Generated pages: standards
 * ------------------------------------------------------------------ */

function standardsIndexBody(lang) {
  const html = `
<p>${escapeHtml(lang === 'zh'
  ? '锁具标准决定的是尺寸、耐久与合规性。改造设计里最常见的错误，是机械上装得进去、却让门的认证失效。'
  : 'Lock standards decide dimensions, durability and compliance. The most common retrofit mistake is a lock that fits mechanically but invalidates the door\'s certification.')}</p>
<div class="table-wrap"><table>
<thead><tr><th>${lang === 'zh' ? '标准' : 'Standard'}</th><th>${lang === 'zh' ? '地区' : 'Origin'}</th><th>${lang === 'zh' ? '标题' : 'Title'}</th><th>${t(terms.labels, 'status', lang)}</th></tr></thead>
<tbody>
${standardsDoc.standards.map((s) => `<tr>
  <td><a href="${hrefFor(lang, 'standards/' + s.id + '.html')}"><code>${escapeHtml(s.code)}</code></a></td>
  <td>${escapeHtml(s.origin)}</td>
  <td>${escapeHtml(s.title[lang] || s.title.en)}</td>
  <td>${statusBadge(s.status, lang)}</td>
</tr>`).join('\n')}
</tbody></table></div>
<aside class="callout callout--warning"><p class="callout__title">${escapeHtml(lang === 'zh' ? '关于“待核对”条目' : 'About needs-review records')}</p><p>${escapeHtml(lang === 'zh'
  ? '标记为待核对的条目是故意发布的：知识库隐藏空白比标明空白更危险。请在引用前确认。'
  : 'Records marked needs-review are published deliberately: a knowledge base that hides its gaps is more dangerous than one that marks them. Verify before citing.')}</p></aside>`;
  return { html, headings: [] };
}

function standardPage(std, lang) {
  const html = `
<p class="meta">${statusBadge(std.status, lang)} <span class="meta__sep">·</span> <strong>${escapeHtml(lang === 'zh' ? '地区' : 'Origin')}:</strong> ${escapeHtml(std.origin)}</p>
<p class="lede">${escapeHtml(std.scope[lang] || std.scope.en)}</p>
<h2 id="decides">${escapeHtml(t(terms.labels, 'keyPoints', lang))}</h2>
${bilingualList(std.decides, lang)}
<h2 id="applies">${escapeHtml(t(terms.labels, 'appliesTo', lang))}</h2>
<p>${linkList(std.appliesTo, lang, 'family')}</p>
<h2 id="retrofit">${escapeHtml(lang === 'zh' ? '为什么改造设计者要关心' : 'Why a retrofit designer cares')}</h2>
<p>${escapeHtml(std.whyItMattersForRetrofit[lang] || std.whyItMattersForRetrofit.en)}</p>
${sourceList(std.sources, lang)}
<p class="record-link"><a href="${escapeHtml(site.urls.repository)}/issues">${escapeHtml(lang === 'zh' ? '指出错误或补充资料' : 'Report an error or add a source')}</a></p>`;

  return {
    html,
    headings: [
      { level: 2, id: 'decides', text: t(terms.labels, 'keyPoints', lang) },
      { level: 2, id: 'applies', text: t(terms.labels, 'appliesTo', lang) },
      { level: 2, id: 'retrofit', text: lang === 'zh' ? '为什么改造设计者要关心' : 'Why a retrofit designer cares' },
    ],
    ld: [{
      '@context': 'https://schema.org',
      '@type': 'DefinedTerm',
      name: std.code,
      description: std.scope[lang] || std.scope.en,
      termCode: std.code,
      inDefinedTermSet: { '@type': 'DefinedTermSet', name: 'Door lock standards' },
    }],
  };
}

/* ------------------------------------------------------------------ *
 * Generated pages: retrofit architectures and devices
 * ------------------------------------------------------------------ */

function architectureIndexBody(lang) {
  const html = `
<p>${escapeHtml(lang === 'zh'
  ? '七种把机械锁变成智能锁的方式。每一种对门的改动程度、对钥匙的保留方式、以及需要设计的适配件都不同。'
  : 'Seven ways to make a mechanical lock smart. They differ in how much they change the door, whether they keep the key, and which adapters have to be designed.')}</p>
<div class="table-wrap"><table>
<thead><tr><th>${lang === 'zh' ? '架构' : 'Architecture'}</th><th>${lang === 'zh' ? '不改门' : 'Door untouched'}</th><th>${lang === 'zh' ? '保留钥匙' : 'Keeps key'}</th><th>${lang === 'zh' ? '难度' : 'Difficulty'}</th><th>${lang === 'zh' ? '适用锁族' : 'Fits'}</th></tr></thead>
<tbody>
${architecturesDoc.architectures.map((a) => `<tr>
  <td><a href="${hrefFor(lang, 'retrofit/' + a.id + '.html')}">${escapeHtml(t(terms.architecture, a.id, lang))}</a></td>
  <td>${a.doorUntouched ? '✓' : '✗'}</td>
  <td>${a.keepsMechanicalKey ? '✓' : '✗'}</td>
  <td>${'●'.repeat(a.difficulty)}${'○'.repeat(4 - a.difficulty)}</td>
  <td>${escapeHtml(a.worksWith.map((id) => familyById[id]?.title?.[lang] || familyById[id]?.title?.en || id).join(', '))}</td>
</tr>`).join('\n')}
</tbody></table></div>`;
  return { html, headings: [] };
}

function architecturePage(arch, lang) {
  const targets = arch.targets.map((target) => `<tr>
      <th scope="row">${escapeHtml(target.label[lang] || target.label.en)}</th>
      <td><code>${escapeHtml(target.value)}</code></td>
      <td><span class="basis basis--${target.basis}">${escapeHtml(target.basis === 'standard'
        ? (lang === 'zh' ? '标准规定' : 'from standard')
        : (lang === 'zh' ? '工程经验' : 'practice'))}</span>${target.note ? `<br><small>${escapeHtml(target.note[lang] || target.note.en)}</small>` : ''}</td>
    </tr>`).join('\n');

  const html = `
<p class="lede">${escapeHtml(arch.principle[lang] || arch.principle.en)}</p>
<p class="meta"><strong>${lang === 'zh' ? '不改门' : 'Door untouched'}:</strong> ${arch.doorUntouched ? (lang === 'zh' ? '是' : 'yes') : (lang === 'zh' ? '否' : 'no')}
  <span class="meta__sep">·</span> <strong>${lang === 'zh' ? '保留机械钥匙' : 'Keeps mechanical key'}:</strong> ${arch.keepsMechanicalKey ? (lang === 'zh' ? '是' : 'yes') : (lang === 'zh' ? '否' : 'no')}
  <span class="meta__sep">·</span> <strong>${lang === 'zh' ? '难度' : 'Difficulty'}:</strong> ${'●'.repeat(arch.difficulty)}${'○'.repeat(4 - arch.difficulty)}</p>

<h2 id="fits">${escapeHtml(t(terms.labels, 'appliesTo', lang))}</h2>
<p>${linkList(arch.worksWith, lang, 'family')}</p>

<h2 id="measurements">${escapeHtml(lang === 'zh' ? '这种架构需要的测量值' : 'Measurements this architecture needs')}</h2>
<ul>${arch.requiredMeasurements.map((k) => `<li>${escapeHtml(t(terms.measurements, k, lang))}</li>`).join('')}</ul>

<h2 id="adapters">${escapeHtml(t(terms.labels, 'adapterInterfaces', lang))}</h2>
${bilingualList(arch.adapterInterfaces, lang)}

<h2 id="targets">${escapeHtml(lang === 'zh' ? '设计目标值' : 'Design targets')}</h2>
<p>${escapeHtml(lang === 'zh'
  ? '“标准规定”来自引用文件；“工程经验”是本站为改造设计给出的建议值，需要你自己验证。'
  : 'Targets marked "from standard" come from the cited document. Targets marked "practice" are our engineering guidance and must be verified for your design.')}</p>
<div class="table-wrap"><table>
<thead><tr><th>${lang === 'zh' ? '目标' : 'Target'}</th><th>${lang === 'zh' ? '数值' : 'Value'}</th><th>${lang === 'zh' ? '依据' : 'Basis'}</th></tr></thead>
<tbody>${targets}</tbody></table></div>

<h2 id="blockers">${escapeHtml(t(terms.labels, 'blockers', lang))}</h2>
${bilingualList(arch.blockers, lang)}

<h2 id="checklist">${escapeHtml(t(terms.labels, 'designChecklist', lang))}</h2>
${bilingualList(arch.designChecklist, lang)}

${arch.examples.length ? `<h2 id="examples">${lang === 'zh' ? '市售示例' : 'Examples on the market'}</h2><ul>${arch.examples.map((id) => {
    const d = deviceById[id];
    return `<li>${d ? `<a href="${hrefFor(lang, 'devices/' + id + '.html')}">${escapeHtml(d.name)}</a>` : escapeHtml(id)}</li>`;
  }).join('')}</ul>` : ''}

${sourceList(architecturesDoc.sources, lang)}
<p class="record-link"><a href="${escapeHtml(site.urls.repository)}/blob/main/content/catalog/retrofit-architectures.json">${escapeHtml(t(terms.labels, 'openFile', lang))}</a></p>`;

  return {
    html,
    headings: [
      { level: 2, id: 'fits', text: t(terms.labels, 'appliesTo', lang) },
      { level: 2, id: 'measurements', text: lang === 'zh' ? '这种架构需要的测量值' : 'Measurements this architecture needs' },
      { level: 2, id: 'adapters', text: t(terms.labels, 'adapterInterfaces', lang) },
      { level: 2, id: 'targets', text: lang === 'zh' ? '设计目标值' : 'Design targets' },
      { level: 2, id: 'blockers', text: t(terms.labels, 'blockers', lang) },
      { level: 2, id: 'checklist', text: t(terms.labels, 'designChecklist', lang) },
    ],
    ld: [{
      '@context': 'https://schema.org',
      '@type': 'HowTo',
      name: t(terms.architecture, arch.id, lang),
      description: arch.principle[lang] || arch.principle.en,
      step: localized(arch.designChecklist, lang).map((s, i) => ({
        '@type': 'HowToStep', position: i + 1, text: s,
      })),
    }],
  };
}

function deviceIndexBody(lang) {
  const html = `
<p>${escapeHtml(lang === 'zh'
  ? '这些设备作为工程参考记录：它们各自代表了哪一种改造架构、适配哪些锁族、以及有哪些硬约束。本站不销售、不推荐、不接受厂商投放。'
  : 'These devices are recorded as engineering references: which retrofit architecture each one represents, which lock families it fits, and what its hard constraints are. No sales, no recommendations, no vendor placement.')}</p>
<div class="table-wrap"><table>
<thead><tr><th>${lang === 'zh' ? '设备' : 'Device'}</th><th>${lang === 'zh' ? '架构' : 'Architecture'}</th><th>${lang === 'zh' ? '适用锁族' : 'Fits'}</th><th>${t(terms.labels, 'status', lang)}</th></tr></thead>
<tbody>
${devicesDoc.devices.map((d) => `<tr>
  <td><a href="${hrefFor(lang, 'devices/' + d.id + '.html')}">${escapeHtml(d.name)}</a></td>
  <td><a href="${hrefFor(lang, 'retrofit/' + d.architecture + '.html')}">${escapeHtml(t(terms.architecture, d.architecture, lang))}</a></td>
  <td>${escapeHtml(d.fits.map((id) => familyById[id]?.title?.[lang] || familyById[id]?.title?.en || id).join(', '))}</td>
  <td>${statusBadge(d.status, lang)}</td>
</tr>`).join('\n')}
</tbody></table></div>`;
  return { html, headings: [] };
}

function devicePage(dev, lang) {
  const html = `
<p class="lede">${escapeHtml(dev.vendor)} — ${escapeHtml(t(terms.architecture, dev.architecture, lang))}</p>
<p class="meta">${statusBadge(dev.status, lang)} <span class="meta__sep">·</span> ${escapeHtml(lang === 'zh' ? '核对日期' : 'Checked')}: ${escapeHtml(dev.checkedOn)}</p>
<h2 id="fits">${escapeHtml(t(terms.labels, 'appliesTo', lang))}</h2>
<p>${linkList(dev.fits, lang, 'family')}</p>
<h2 id="constraints">${escapeHtml(t(terms.labels, 'fitNotes', lang))}</h2>
${bilingualList(dev.keyConstraints, lang)}
<aside class="callout callout--note"><p class="callout__title">${escapeHtml(lang === 'zh' ? '这不是推荐' : 'Not a recommendation')}</p><p>${escapeHtml(lang === 'zh'
  ? '本条目记录的是工程事实：这台设备代表哪种架构、适配哪些锁族。请自行判断是否适合你的门。'
  : 'This record states engineering facts: which architecture the device represents and which lock families it fits. Judge suitability for your own door.')}</p></aside>
${sourceList(devicesDoc.sources, lang)}`;

  return {
    html,
    headings: [
      { level: 2, id: 'fits', text: t(terms.labels, 'appliesTo', lang) },
      { level: 2, id: 'constraints', text: t(terms.labels, 'fitNotes', lang) },
    ],
    ld: [],
  };
}

/* ------------------------------------------------------------------ *
 * Interactive widgets (inlined data, so pages work without fetching)
 * ------------------------------------------------------------------ */

function wizardFragment(lang) {
  const questions = decisionTree.questions.map((q) => ({
    id: q.id,
    prompt: q.prompt[lang] || q.prompt.en,
    hint: q.hint?.[lang] || q.hint?.en || '',
    options: q.options.map((o) => ({ id: o.id, label: o.label[lang] || o.label.en, add: o.add })),
  }));

  const catalog = families.map((f) => ({
    id: f.id,
    title: f.title[lang] || f.title.en,
    summary: f.summary[lang] || f.summary.en,
    status: f.status,
    regions: f.regions,
    url: urlFor(lang, `locks/${f.id}.html`),
    measureOrder: (f.measureOrder || []).map((k) => ({ key: k, label: t(terms.measurements, k, lang), typical: localizedText(f.measurements.find((m) => m.key === k)?.typical, lang) })),
    architectures: f.retrofit.architectures.map((a) => ({
      id: a, label: t(terms.architecture, a, lang), url: urlFor(lang, `retrofit/${a}.html`),
    })),
  }));

  return `<div class="wizard" id="wizard"
    data-lang="${lang}"
    data-root="${rootPrefix()}"
    data-product-url="${escapeHtml(site.product?.url || '')}"
    data-product-label="${escapeHtml(site.product?.label?.[lang] || site.product?.label?.en || '')}"
    data-i18n='${JSON.stringify({
      title: t(terms.wizard, 'title', lang),
      restart: t(terms.wizard, 'restart', lang),
      back: t(terms.wizard, 'back', lang),
      progress: t(terms.wizard, 'progress', lang),
      result: t(terms.wizard, 'result', lang),
      alternatives: t(terms.wizard, 'alternatives', lang),
      measureNext: t(terms.wizard, 'measureNext', lang),
      retrofitOptions: t(terms.wizard, 'retrofitOptions', lang),
      copyReport: t(terms.wizard, 'copyReport', lang),
      downloadReport: t(terms.wizard, 'downloadReport', lang),
      copied: t(terms.wizard, 'copied', lang),
      unknown: t(terms.wizard, 'unknown', lang),
      statusVerified: t(terms.labels, 'verified', lang),
      statusReview: t(terms.labels, 'needs-review', lang),
    }).replace(/'/g, '&#39;')}'
    data-questions='${JSON.stringify(questions).replace(/'/g, '&#39;')}'
    data-catalog='${JSON.stringify(catalog).replace(/'/g, '&#39;')}'>
  <noscript><p>${escapeHtml(lang === 'zh' ? '识别向导需要 JavaScript。也可以直接浏览锁型库。' : 'The identification wizard needs JavaScript. You can also browse the lock catalog directly.')}</p></noscript>
  <div class="wizard__inner"><p class="wizard__loading">${escapeHtml(lang === 'zh' ? '正在载入向导…' : 'Loading wizard…')}</p></div>
</div>
<script src="/assets/js/scoring.js" defer></script>
<script src="/assets/js/identify.js" defer></script>`;
}

function photoFragment(lang) {
  return `<div class="photo" id="photo"
    data-lang="${lang}"
    data-i18n='${JSON.stringify({
      title: t(terms.photo, 'title', lang),
      drop: t(terms.photo, 'drop', lang),
      hint: t(terms.photo, 'hint', lang),
      setReference: t(terms.photo, 'setReference', lang),
      measure: t(terms.photo, 'measure', lang),
      referenceLength: t(terms.photo, 'referenceLength', lang),
      result: t(terms.photo, 'result', lang),
      reset: t(terms.photo, 'reset', lang),
      noSupport: t(terms.photo, 'noSupport', lang),
    }).replace(/'/g, '&#39;')}'>
  <noscript><p>${escapeHtml(lang === 'zh' ? '拍照量尺寸需要 JavaScript。请使用下面的打印版测量指南。' : 'Photo measuring needs JavaScript. Use the printable guide below instead.')}</p></noscript>
  <p class="photo__loading">${escapeHtml(lang === 'zh' ? '正在载入工具…' : 'Loading tool…')}</p>
</div>
<script src="/assets/js/photo.js" defer></script>`;
}

function searchFragment(lang) {
  return `<div class="search" id="search"
    data-lang="${lang}"
    data-root="${rootPrefix()}"
    data-i18n='${JSON.stringify({
      placeholder: t(site.ui, 'searchPlaceholder', lang),
      noResults: t(site.ui, 'noResults', lang),
      search: t(site.ui, 'search', lang),
    }).replace(/'/g, '&#39;')}'>
  <noscript><p>${escapeHtml(lang === 'zh' ? '搜索需要 JavaScript。可以改用锁型库与标准索引页。' : 'Search needs JavaScript. Use the catalog and standards index pages instead.')}</p></noscript>
</div>
<script src="/assets/js/search.js" defer></script>`;
}

const FRAGMENTS = {
  '{{wizard}}': wizardFragment,
  '{{photo}}': photoFragment,
  '{{search}}': searchFragment,
};

/**
 * Set by the markdown loop before a page body is rendered, so widget fragments
 * can emit correct relative paths without knowing where they will be placed.
 */
let currentPagePath = 'index.html';
const rootPrefix = () => prefixFor(currentPagePath);

/* ------------------------------------------------------------------ *
 * Build
 * ------------------------------------------------------------------ */

function build() {
  const started = Date.now();
  if (existsSync(OUT)) rmSync(OUT, { recursive: true, force: true });
  mkdirSync(OUT, { recursive: true });

  const searchIndex = [];

  // 1. Markdown pages ------------------------------------------------
  for (const lang of LANGS) {
    const dir = join(CONTENT, 'pages', lang);
    if (!existsSync(dir)) continue;
    for (const file of readdirSync(dir).filter((f) => f.endsWith('.md'))) {
      const source = readFileSync(join(dir, file), 'utf8');
      const { data, body } = splitFrontMatter(source);
      const slug = data.slug || (file.replace(/\.md$/, '') === 'index' ? 'index.html' : file.replace(/\.md$/, '') + '.html');
      register(lang, slug);
    }
  }
  // Register generated pages so hreflang alternates resolve.
  for (const lang of LANGS) {
    register(lang, 'locks/index.html');
    register(lang, 'standards/index.html');
    register(lang, 'retrofit/index.html');
    register(lang, 'devices/index.html');
    register(lang, 'search.html');
    for (const f of families) register(lang, `locks/${f.id}.html`);
    for (const s of standardsDoc.standards) register(lang, `standards/${s.id}.html`);
    for (const a of architecturesDoc.architectures) register(lang, `retrofit/${a.id}.html`);
    for (const d of devicesDoc.devices) register(lang, `devices/${d.id}.html`);
  }

  for (const lang of LANGS) {
    const dir = join(CONTENT, 'pages', lang);
    if (!existsSync(dir)) continue;
    for (const file of readdirSync(dir).filter((f) => f.endsWith('.md'))) {
      const source = readFileSync(join(dir, file), 'utf8');
      const { data, body } = splitFrontMatter(source);
      const slug = data.slug || (file.replace(/\.md$/, '') === 'index' ? 'index.html' : file.replace(/\.md$/, '') + '.html');
      currentPagePath = urlFor(lang, slug);

      let rendered = renderMarkdown(body);
      let html = rendered.html;
      for (const [token, fn] of Object.entries(FRAGMENTS)) {
        if (html.includes(token)) html = html.replace(new RegExp(token.replace(/[{}]/g, '\\$&'), 'g'), fn(lang));
      }

      const title = data.title || file.replace(/\.md$/, '');
      const description = data.description || site.description[lang];
      const crumbs = [{ label: site.name, href: hrefFor(lang, 'index.html') }];
      if (slug !== 'index.html') crumbs.push({ label: title });

      const faq = data.faq
        ? null
        : extractFaqFromMarkdown(body, lang);

      emitPage({
        lang,
        slug,
        title,
        description,
        bodyHtml: `<h1>${escapeHtml(title)}</h1>\n${html}`,
        breadcrumbs: crumbs,
        headings: rendered.headings,
        jsonLd: [
          techArticleJsonLd({ headline: title, description, url: `${BASE_URL}/${urlFor(lang, slug)}`, lang, dateModified: BUILD_DATE }),
          faq,
        ].filter(Boolean),
      });

      searchIndex.push({
        lang, title, description,
        url: hrefFor(lang, slug),
        kind: 'page',
        text: body.replace(/[#*`|>]/g, ' ').slice(0, 4000),
      });
    }
  }

  // 2. Generated catalog pages ---------------------------------------
  for (const lang of LANGS) {
    const homeCrumb = [{ label: site.name, href: hrefFor(lang, 'index.html') }];

    const li = lockIndexBody(lang);
    emitPage({
      lang, slug: 'locks/index.html',
      title: lang === 'zh' ? '锁型库' : 'Lock families',
      description: lang === 'zh'
        ? '全球机械门锁锁族目录：结构、必测参数与公差、相关标准与可用改造架构。'
        : 'Catalog of the world\'s mechanical door lock families: anatomy, required measurements with tolerances, standards and retrofit architectures.',
      bodyHtml: `<h1>${lang === 'zh' ? '锁型库' : 'Lock families'}</h1>\n${li.html}`,
      breadcrumbs: [...homeCrumb, { label: lang === 'zh' ? '锁型库' : 'Lock families' }],
      headings: li.headings,
      jsonLd: [{ '@context': 'https://schema.org', '@type': 'ItemList', name: 'Lock families', numberOfItems: families.length, itemListElement: families.map((f, i) => ({ '@type': 'ListItem', position: i + 1, name: f.title[lang] || f.title.en, url: `${BASE_URL}/${urlFor(lang, 'locks/' + f.id + '.html')}` })) }],
    });

    for (const fam of families) {
      const p = lockPage(fam, lang);
      emitPage({
        lang, slug: `locks/${fam.id}.html`,
        title: fam.title[lang] || fam.title.en,
        description: (fam.summary[lang] || fam.summary.en).slice(0, 200),
        bodyHtml: `<h1>${escapeHtml(fam.title[lang] || fam.title.en)}</h1>\n${p.html}`,
        breadcrumbs: [...homeCrumb, { label: lang === 'zh' ? '锁型库' : 'Lock families', href: hrefFor(lang, 'locks/index.html') }, { label: fam.title[lang] || fam.title.en }],
        headings: p.headings,
        jsonLd: p.ld,
      });
      searchIndex.push({
        lang, title: fam.title[lang] || fam.title.en,
        description: fam.summary[lang] || fam.summary.en,
        url: hrefFor(lang, `locks/${fam.id}.html`), kind: 'lock',
        text: [fam.aliases?.[lang]?.join(' '), fam.regions.join(' '), fam.measurements.map((m) => `${t(terms.measurements, m.key, lang)} ${m.typical}`).join(' ')].join(' '),
      });
    }

    const si = standardsIndexBody(lang);
    emitPage({
      lang, slug: 'standards/index.html',
      title: lang === 'zh' ? '锁具标准索引' : 'Lock standards index',
      description: lang === 'zh' ? 'DIN、EN、BS、TS、ANSI/BHMA 与亚洲标准索引，说明每项标准实际决定什么。' : 'Index of DIN, EN, BS, TS, ANSI/BHMA and Asian lock standards, and what each one actually decides.',
      bodyHtml: `<h1>${lang === 'zh' ? '锁具标准索引' : 'Lock standards index'}</h1>\n${si.html}`,
      breadcrumbs: [...homeCrumb, { label: lang === 'zh' ? '标准' : 'Standards' }],
      headings: si.headings,
    });

    for (const std of standardsDoc.standards) {
      const p = standardPage(std, lang);
      emitPage({
        lang, slug: `standards/${std.id}.html`,
        title: std.code,
        description: (std.scope[lang] || std.scope.en).slice(0, 200),
        bodyHtml: `<h1><code>${escapeHtml(std.code)}</code> ${escapeHtml(std.title[lang] || std.title.en)}</h1>\n${p.html}`,
        breadcrumbs: [...homeCrumb, { label: lang === 'zh' ? '标准' : 'Standards', href: hrefFor(lang, 'standards/index.html') }, { label: std.code }],
        headings: p.headings,
        jsonLd: p.ld,
      });
      searchIndex.push({
        lang, title: `${std.code} — ${std.title[lang] || std.title.en}`,
        description: std.scope[lang] || std.scope.en,
        url: hrefFor(lang, `standards/${std.id}.html`), kind: 'standard',
        text: (std.decides[lang] || std.decides.en).join(' '),
      });
    }

    const ai = architectureIndexBody(lang);
    emitPage({
      lang, slug: 'retrofit/index.html',
      title: lang === 'zh' ? '改造架构对照' : 'Retrofit architectures',
      description: lang === 'zh' ? '七种把机械锁智能化的架构：对门的改动、是否保留钥匙、需要设计的适配件与设计目标值。' : 'Seven architectures for making a mechanical lock smart: what changes on the door, whether the key survives, the adapters to design, and the design targets.',
      bodyHtml: `<h1>${lang === 'zh' ? '改造架构对照' : 'Retrofit architectures'}</h1>\n${ai.html}`,
      breadcrumbs: [...homeCrumb, { label: lang === 'zh' ? '改造' : 'Retrofit' }],
      headings: ai.headings,
    });

    for (const arch of architecturesDoc.architectures) {
      const p = architecturePage(arch, lang);
      const name = t(terms.architecture, arch.id, lang);
      emitPage({
        lang, slug: `retrofit/${arch.id}.html`,
        title: name,
        description: (arch.principle[lang] || arch.principle.en).slice(0, 200),
        bodyHtml: `<h1>${escapeHtml(name)}</h1>\n${p.html}`,
        breadcrumbs: [...homeCrumb, { label: lang === 'zh' ? '改造' : 'Retrofit', href: hrefFor(lang, 'retrofit/index.html') }, { label: name }],
        headings: p.headings,
        jsonLd: p.ld,
      });
      searchIndex.push({
        lang, title: name,
        description: arch.principle[lang] || arch.principle.en,
        url: hrefFor(lang, `retrofit/${arch.id}.html`), kind: 'architecture',
        text: localized(arch.adapterInterfaces, lang).join(' '),
      });
    }

    const di = deviceIndexBody(lang);
    emitPage({
      lang, slug: 'devices/index.html',
      title: lang === 'zh' ? '参考设备' : 'Reference devices',
      description: lang === 'zh' ? '改造型智能锁的工程参考记录：代表哪种架构、适配哪些锁族、有哪些硬约束。' : 'Engineering references for retrofit smart locks: which architecture each represents, which families it fits, and its hard constraints.',
      bodyHtml: `<h1>${lang === 'zh' ? '参考设备' : 'Reference devices'}</h1>\n${di.html}`,
      breadcrumbs: [...homeCrumb, { label: lang === 'zh' ? '设备' : 'Devices' }],
      headings: di.headings,
    });

    for (const dev of devicesDoc.devices) {
      const p = devicePage(dev, lang);
      emitPage({
        lang, slug: `devices/${dev.id}.html`,
        title: dev.name,
        description: `${dev.vendor} — ${t(terms.architecture, dev.architecture, lang)}`,
        bodyHtml: `<h1>${escapeHtml(dev.name)}</h1>\n${p.html}`,
        breadcrumbs: [...homeCrumb, { label: lang === 'zh' ? '设备' : 'Devices', href: hrefFor(lang, 'devices/index.html') }, { label: dev.name }],
        headings: p.headings,
        jsonLd: p.ld,
      });
      searchIndex.push({
        lang, title: dev.name, description: dev.vendor,
        url: hrefFor(lang, `devices/${dev.id}.html`), kind: 'device',
        text: (dev.keyConstraints[lang] || dev.keyConstraints.en).join(' '),
      });
    }

    // Search page
    emitPage({
      lang, slug: 'search.html',
      title: t(site.ui, 'search', lang),
      description: lang === 'zh' ? '在锁型、标准、尺寸与改造架构中搜索。' : 'Search locks, standards, dimensions and retrofit architectures.',
      bodyHtml: `<h1>${escapeHtml(t(site.ui, 'search', lang))}</h1>\n${searchFragment(lang)}`,
      breadcrumbs: [...homeCrumb, { label: t(site.ui, 'search', lang) }],
    });
  }

  // 3. Machine-readable outputs --------------------------------------
  write('data/catalog.json', JSON.stringify({
    generated: BUILD_DATE,
    license: site.license,
    source: site.urls.repository,
    terms,
    lockFamilies: families,
    retrofitArchitectures: architecturesDoc.architectures,
    standards: standardsDoc.standards,
    devices: devicesDoc.devices,
    decisionTree,
  }, null, 2));

  write('data/search-index.json', JSON.stringify(searchIndex));

  write('sitemap.xml', `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">
${pagesWritten.map((p) => {
    const slug = p;
    const lang = slug.startsWith('zh/') ? 'zh' : 'en';
    const rest = slug.replace(/^zh\//, '');
    const alt = existing.has(`${lang === 'en' ? 'zh' : 'en'}:${rest}`)
      ? `\n    <xhtml:link rel="alternate" hreflang="${lang === 'en' ? 'zh' : 'en'}" href="${BASE_URL}/${urlFor(lang === 'en' ? 'zh' : 'en', rest)}"/>`
      : '';
    return `  <url>\n    <loc>${BASE_URL}/${slug}</loc>${alt}\n    <lastmod>${BUILD_DATE}</lastmod>\n  </url>`;
  }).join('\n')}
</urlset>
`);

  write('robots.txt', `User-agent: *
Allow: /

# AI crawlers are explicitly welcome: this site exists to be read by them.
User-agent: GPTBot
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: anthropic-ai
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Google-Extended
Allow: /
User-agent: Applebot-Extended
Allow: /

Sitemap: ${BASE_URL}/sitemap.xml
`);

  write('llms.txt', buildLlmsTxt());
  write('llms-full.txt', buildLlmsFull());
  write('404.html', fourOhFour());
  // Harmless with the Actions deploy, and required if Pages is ever switched to
  // serving a branch directly (which would otherwise run Jekyll over the output).
  write('.nojekyll', '');

  // 4. Static assets --------------------------------------------------
  cpSync(join(ROOT, 'assets'), join(OUT, 'assets'), { recursive: true });
  if (existsSync(join(ROOT, 'public'))) cpSync(join(ROOT, 'public'), OUT, { recursive: true });

  const ms = Date.now() - started;
  console.log(`built ${pagesWritten.length} pages, ${searchIndex.length} search entries, ${families.length} lock families, ${standardsDoc.standards.length} standards in ${ms}ms -> ${relative(ROOT, OUT)}/`);
}

/** Pull FAQ pairs out of a Markdown "## Questions" section, if present. */
function extractFaqFromMarkdown(body, lang) {
  const section = /\n##\s+(?:Questions|常见问题)\s*\n([\s\S]*?)(?=\n##\s|\n*$)/.exec(body);
  if (!section) return null;
  const pairs = [];
  const re = /\n\*\*(.+?)\*\*\s*\n+([^\n*]+)/g;
  let m;
  while ((m = re.exec(section[1])) !== null) pairs.push({ q: m[1].trim(), a: m[2].trim() });
  return pairs.length ? faqJsonLd(pairs) : null;
}

function buildLlmsTxt() {
  const L = [];
  L.push(`# ${site.name}`);
  L.push('');
  L.push(`> ${site.description.en}`);
  L.push('');
  L.push('An open, machine-readable reference for identifying existing mechanical door locks worldwide and designing smart-lock retrofits that fit them. All data is also available as JSON at /data/catalog.json.');
  L.push('');
  L.push('## Identify and measure');
  for (const slug of ['identify.html', 'measure.html', 'photo.html']) {
    if (existing.has(`en:${slug}`)) L.push(`- [${slug.replace('.html', '')}](/${slug}): guided identification and the measurement checklist`);
  }
  L.push('');
  L.push('## Retrofit design');
  for (const slug of ['retrofit.html']) if (existing.has(`en:${slug}`)) L.push(`- [Retrofit architectures](/${slug}): the seven architectures, adapters and design targets`);
  for (const a of architecturesDoc.architectures) L.push(`- [${a.id}](/retrofit/${a.id}.html): ${a.principle.en.slice(0, 120)}`);
  L.push('');
  L.push('## Lock families');
  for (const f of families) L.push(`- [${f.title.en}](/locks/${f.id}.html): ${f.summary.en.slice(0, 140)}`);
  L.push('');
  L.push('## Standards');
  for (const s of standardsDoc.standards) L.push(`- [${s.code}](/standards/${s.id}.html): ${s.title.en}${s.status === 'needs-review' ? ' (needs review)' : ''}`);
  L.push('');
  L.push('## Machine-readable');
  L.push('- [catalog.json](/data/catalog.json): every lock family, standard, architecture and device in one JSON document');
  L.push('- [search-index.json](/data/search-index.json): flat index of all pages in both languages');
  L.push('- [sitemap.xml](/sitemap.xml): all URLs with hreflang alternates');
  L.push('');
  L.push('## Optional');
  L.push(`- [Source repository](${site.urls.repository}): data files are one JSON record per lock family`);
  L.push('');
  return L.join('\n');
}

function buildLlmsFull() {
  const L = [`# ${site.name} — full content dump`, '', `Generated: ${BUILD_DATE}`, '', site.description.en, ''];

  L.push('## Lock families', '');
  for (const f of families) {
    L.push(`### ${f.title.en}`, '', f.summary.en, '', `- Regions: ${f.regions.join(', ')}`, `- Status: ${f.status}`, `- Standards: ${f.standards.join(', ')}`, `- Retrofit architectures: ${f.retrofit.architectures.join(', ') || 'none'}`, '', 'Measurements:', '');
    for (const m of f.measurements) L.push(`- ${t(terms.measurements, m.key, 'en')}: ${m.typical} (tolerance: ${m.tolerance || '—'}) — ${m.how.en}`);
    L.push('', ...f.anatomy.en.map((a) => `- ${a}`), '');
    if (f.faq?.en) { L.push('Questions:', ''); for (const q of f.faq.en) L.push(`- ${q.q} — ${q.a}`); L.push(''); }
    for (const s of f.sources) L.push(`Source: ${s.title} ${s.url}`);
    L.push('');
  }

  L.push('## Standards', '');
  for (const s of standardsDoc.standards) {
    L.push(`### ${s.code} — ${s.title.en}`, '', `Status: ${s.status}`, `Origin: ${s.origin}`, '', s.scope.en, '', ...s.decides.en.map((d) => `- ${d}`), '', `Why it matters for retrofit: ${s.whyItMattersForRetrofit.en}`, '');
  }

  L.push('## Retrofit architectures', '');
  for (const a of architecturesDoc.architectures) {
    L.push(`### ${t(terms.architecture, a.id, 'en')}`, '', a.principle.en, '', `Door untouched: ${a.doorUntouched}. Keeps mechanical key: ${a.keepsMechanicalKey}. Difficulty: ${a.difficulty}/4.`, '', 'Design targets:', '');
    for (const target of a.targets) L.push(`- ${target.label.en}: ${target.value} [${target.basis}]${target.note ? ` — ${target.note.en}` : ''}`);
    L.push('', 'Adapter interfaces:', '', ...localized(a.adapterInterfaces, 'en').map((x) => `- ${x}`), '', 'Blockers:', '', ...a.blockers.en.map((x) => `- ${x}`), '');
  }

  L.push('## Reference devices', '');
  for (const d of devicesDoc.devices) {
    L.push(`### ${d.name} (${d.vendor})`, '', `Architecture: ${t(terms.architecture, d.architecture, 'en')}. Status: ${d.status}, checked ${d.checkedOn}.`, `Fits: ${d.fits.join(', ')}.`, '', ...d.keyConstraints.en.map((x) => `- ${x}`), '');
  }

  L.push('## Markdown pages', '');
  for (const lang of LANGS) {
    const dir = join(CONTENT, 'pages', lang);
    if (!existsSync(dir)) continue;
    for (const file of readdirSync(dir).filter((f) => f.endsWith('.md'))) {
      const { data, body } = splitFrontMatter(readFileSync(join(dir, file), 'utf8'));
      L.push(`### [${lang}] ${data.title || file}`, '', body.trim(), '');
    }
  }

  return L.join('\n');
}

function fourOhFour() {
  const html = layout({
    title: 'Page not found',
    description: 'That page does not exist. Try the lock catalog or the identification wizard.',
    lang: 'en',
    path: '404.html',
    baseUrl: BASE_URL,
    site: { ...site, navigation: { en: rewriteNav(site.navigation.en) } },
    body: `<h1>Page not found</h1><p>That page does not exist. Try the <a href="/locks/index.html">lock catalog</a>, the <a href="/standards/index.html">standards index</a> or the <a href="/identify.html">identification wizard</a>.</p><p class="muted">找不到页面。可以试试<a href="/zh/locks/index.html">锁型库</a>、<a href="/zh/standards/index.html">标准索引</a>或<a href="/zh/identify.html">识别向导</a>。</p>`,
    breadcrumbs: [{ label: site.name, href: '/index.html' }, { label: '404' }],
  });
  return rebaseLinks(html, '404.html');
}

/* ------------------------------------------------------------------ *
 * Watch mode
 * ------------------------------------------------------------------ */

build();

if (process.argv.includes('--watch')) {
  console.log('watching content/ and assets/ …');
  let timer = null;
  const onChange = () => {
    clearTimeout(timer);
    timer = setTimeout(() => {
      try { build(); } catch (err) { console.error(err); }
    }, 150);
  };
  for (const dir of ['content', 'assets', 'src']) {
    watch(join(ROOT, dir), { recursive: true }, onChange);
  }
}
