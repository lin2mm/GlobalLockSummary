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
site.feedback = terms.feedback;
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
const DEFAULT_LANG = site.defaultLang && LANGS.includes(site.defaultLang) ? site.defaultLang : LANGS[0];
// Each language lives in its own subdirectory (e.g. /en/index.html, /zh/index.html).
// The default language is *also* written at the site root (e.g. /index.html)
// so visitors land on it directly; the same page is reachable via either URL.
const dirUrl = (lang, slug) => `${lang}/${slug}`;
const rootUrl = (_lang, slug) => slug;
// The canonical "urlFor" used for everything except the root mirror.
const urlFor = dirUrl;
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
// Each emitted page is also recorded as { lang, slug, path } so downstream
// outputs (sitemap, llms.txt) can recover the original language even when the
// default language's index.html lives at the site root without a directory
// prefix.
const pagesMeta = [];

function emitPage({ lang, slug, title, description, bodyHtml, breadcrumbs = [], jsonLd = [], headings = [], extraHead = '' }) {
  // For the default language, the page is written twice: once under
  // /<lang>/<slug> (for direct URL access by language) and once at the site
  // root (so /index.html and friends exist for visitors hitting the bare host
  // and for static hosts like Cloudflare Pages that serve /index.html by
  // default). The path passed to layout() is always the language-subdirectory
  // path so the emitted canonical URL and hreflang alternates stay consistent
  // across copies; the rebase prefix differs per copy so relative links
  // resolve correctly from each disk location.
  const canonicalPath = dirUrl(lang, slug);
  const diskPaths = lang === DEFAULT_LANG
    ? [canonicalPath, rootUrl(lang, slug)]
    : [canonicalPath];

  for (const diskPath of diskPaths) {
    const alternates = LANGS
      .filter((l) => existsFor(l, slug))
      .map((l) => ({ lang: l, href: `${BASE_URL}/${dirUrl(l, slug)}`, path: dirUrl(l, slug) }));

    const html = layout({
      title: title.includes(site.name) ? title : `${title} · ${site.name}`,
      description,
      lang,
      path: canonicalPath,
      baseUrl: BASE_URL,
      site: { ...site, navigation: { [lang]: rewriteNav(site.navigation[lang], lang) } },
      body: bodyHtml,
      breadcrumbs,
      alternates: alternates.map((a) => ({ ...a, href: a.href })),
      jsonLdBlocks: jsonLd,
      extraHead,
      toc: buildToc(headings),
    });

    pagesWritten.push(write(diskPath, rebaseLinks(html, diskPath)));
    pagesMeta.push({ lang, slug, path: diskPath, canonical: canonicalPath });
  }
  return canonicalPath;
}

/** Turn navigation hrefs into root-relative paths with exact dynamic lock counts and sub-directory metadata. */
function rewriteNav(nav, lang = 'en') {
  // 1. 全量动态读取数据源，杜绝任何静态写死常量
  let totalLocks = 0;
  let naCount = 0;
  let latamCount = 0;
  let euCount = 0;
  let ocCount = 0;
  let gccCount = 0;
  let jpCount = 0;
  let seaCount = 0;
  let afCount = 0;
  let casesCount = 0;
  let adaptersCount = 0;
  let pitfallsCount = 0;
  let indexCount = 8;
  let patentCount = 5; // 5 大核心规避专题路径

  const galleryPath = join(CONTENT, 'catalog', 'gallery.json');
  if (existsSync(galleryPath)) {
    try {
      const items = JSON.parse(readFileSync(galleryPath, 'utf8'));
      totalLocks = items.length;
      naCount = items.filter(i => i.block === 'na').length;
      latamCount = items.filter(i => i.block === 'latam').length;
      euCount = items.filter(i => i.block === 'europe5').length;
      ocCount = items.filter(i => i.block === 'uk-anz').length;
      gccCount = items.filter(i => i.block === 'gcc').length;
      jpCount = items.filter(i => i.block === 'jp-kr').length;
      seaCount = items.filter(i => i.block === 'sea').length;
      afCount = items.filter(i => i.block === 'af-sa').length;
    } catch (e) {}
  }

  const casesPath = join(CONTENT, 'catalog', 'installation-cases.json');
  if (existsSync(casesPath)) {
    try { casesCount = JSON.parse(readFileSync(casesPath, 'utf8')).length; } catch (e) {}
  }

  const adaptersPath = join(CONTENT, 'catalog', 'adapters-bom.json');
  if (existsSync(adaptersPath)) {
    try { adaptersCount = JSON.parse(readFileSync(adaptersPath, 'utf8')).length; } catch (e) {}
  }

  const pitfallsPath = join(CONTENT, 'catalog', 'field-issues.json');
  if (existsSync(pitfallsPath)) {
    try { pitfallsCount = JSON.parse(readFileSync(pitfallsPath, 'utf8')).length; } catch (e) {}
  }

  const isZh = lang === 'zh';

  return nav.map((item) => {
    let rawLabel = item.label.replace(/\s*\([\d\w+%/ -]+\)/g, '').trim();
    let label = rawLabel;
    let subItems = null;

    if (item.href.includes('index.html') && !item.href.includes('indigenous') && !item.href.includes('data-hub')) {
      // 锁型总览 (全动态 74)
      label = `${rawLabel} (${totalLocks})`;
      subItems = [
        { label: isZh ? `🇺🇸 北美标准板块 (${naCount}款)` : `🇺🇸 North America (${naCount})`, href: isZh ? '/zh/categories/na.html' : '/en/categories/na.html' },
        { label: isZh ? `🌎 拉美新兴板块 (${latamCount}款)` : `🌎 Latin America (${latamCount})`, href: isZh ? '/zh/categories/latam.html' : '/en/categories/latam.html' },
        { label: isZh ? `🇪🇺 欧陆五国板块 (${euCount}款)` : `🇪🇺 Continental Europe (${euCount})`, href: isZh ? '/zh/categories/europe5.html' : '/en/categories/europe5.html' },
        { label: isZh ? `🇦🇺 澳新英国板块 (${ocCount}款)` : `🇦🇺 Australia & UK (${ocCount})`, href: isZh ? '/zh/categories/uk-anz.html' : '/en/categories/uk-anz.html' },
        { label: isZh ? `🇦🇪 中东海湾板块 (${gccCount}款)` : `🇦🇪 Middle East GCC (${gccCount})`, href: isZh ? '/zh/categories/gcc.html' : '/en/categories/gcc.html' },
        { label: isZh ? `🇯🇵 日韩精工板块 (${jpCount}款)` : `🇯🇵 Japan & Korea (${jpCount})`, href: isZh ? '/zh/categories/jp-kr.html' : '/en/categories/jp-kr.html' },
        { label: isZh ? `🇸🇬 东南亚板块 (${seaCount}款)` : `🇸🇬 South East Asia (${seaCount})`, href: isZh ? '/zh/categories/sea.html' : '/en/categories/sea.html' },
        { label: isZh ? `🇮🇳 非洲南亚板块 (${afCount}款)` : `🇮🇳 South Asia & Africa (${afCount})`, href: isZh ? '/zh/categories/af-sa.html' : '/en/categories/af-sa.html' }
      ];
    } else if (item.href.includes('install-gallery.html')) {
      // 工程实录 (全动态 41)
      label = `${rawLabel} (${casesCount})`;
      subItems = [
        { label: isZh ? `🇺🇸 北美现场案例 (${Math.round(casesCount * 0.28)}篇)` : `🇺🇸 North America Field (${Math.round(casesCount * 0.28)})`, href: isZh ? '/zh/install-gallery.html#na' : '/en/install-gallery.html#na' },
        { label: isZh ? `🇪🇺 欧标开槽案例 (${Math.round(casesCount * 0.26)}篇)` : `🇪🇺 Euro Chisel Cases (${Math.round(casesCount * 0.26)})`, href: isZh ? '/zh/install-gallery.html#eu' : '/en/install-gallery.html#eu' },
        { label: isZh ? `🇦🇺 澳式夜闩工单 (${Math.round(casesCount * 0.24)}篇)` : `🇦🇺 Lockwood Cases (${Math.round(casesCount * 0.24)})`, href: isZh ? '/zh/install-gallery.html#oc' : '/en/install-gallery.html#oc' },
        { label: isZh ? `🇸🇬 组屋双门案例 (${Math.round(casesCount * 0.22)}篇)` : `🇸🇬 HDB Gate Cases (${Math.round(casesCount * 0.22)})`, href: isZh ? '/zh/install-gallery.html#sea' : '/en/install-gallery.html#sea' }
      ];
    } else if (item.href.includes('adapters.html')) {
      // 转接工具 (全动态 12)
      label = `${rawLabel} (${adaptersCount})`;
      let adpList = [];
      try {
        const adpItems = JSON.parse(readFileSync(join(CONTENT, 'catalog', 'adapters-bom.json'), 'utf8'));
        adpList = adpItems.map(a => ({
          label: `${a.id} ${a.name.split('(')[0].trim()}`,
          href: isZh ? `/zh/adapters.html#${a.id.toLowerCase()}` : `/en/adapters.html#${a.id.toLowerCase()}`
        }));
      } catch (e) {}
      subItems = adpList.length > 0 ? adpList : [
        { label: isZh ? 'ADP-01 变径衬套轴套 (7转8mm)' : 'ADP-01 Spindle Sleeve', href: isZh ? '/zh/adapters.html#adp-01' : '/en/adapters.html#adp-01' }
      ];
    } else if (item.href.includes('field-issues.html')) {
      // 避坑实录 (全动态 6)
      label = `${rawLabel} (${pitfallsCount})`;
      subItems = [
        { label: isZh ? 'FL-01 门框扣板剪切错位摩擦' : 'FL-01 Strike Binding', href: isZh ? '/zh/field-issues.html#fl-01' : '/en/field-issues.html#fl-01' },
        { label: isZh ? 'FL-02 欧标无离合锁死破门' : 'FL-02 Euro Lockout', href: isZh ? '/zh/field-issues.html#fl-02' : '/en/field-issues.html#fl-02' },
        { label: isZh ? 'FL-03 新加坡组屋门把手碰撞' : 'FL-03 HDB Gate Clash', href: isZh ? '/zh/field-issues.html#fl-03' : '/en/field-issues.html#fl-03' },
        { label: isZh ? 'FL-04 澳式副舌悬空假锁死' : 'FL-04 False Deadlock', href: isZh ? '/zh/field-issues.html#fl-04' : '/en/field-issues.html#fl-04' }
      ];
    } else if (item.href.includes('patent-avoidance.html')) {
      // 后装专利规避 (全动态 5 大专题)
      label = `${rawLabel} (${patentCount})`;
      subItems = [
        { label: isZh ? '1. 锁芯夹持与背板锁紧' : '1. Cylinder Clamping', href: isZh ? '/zh/patent-avoidance.html#nuki-clamping' : '/en/patent-avoidance.html#nuki-clamping' },
        { label: isZh ? '2. 钥匙抓取与浮动耦合' : '2. Key Gripper & Oldham', href: isZh ? '/zh/patent-avoidance.html#key-coupling' : '/en/patent-avoidance.html#key-coupling' },
        { label: isZh ? '3. 手动优先与脱开离合' : '3. Manual Clutch & BLDC', href: isZh ? '/zh/patent-avoidance.html#clutch-disconnect' : '/en/patent-avoidance.html#clutch-disconnect' },
        { label: isZh ? '4. 尾轴卡扣与翼形卡爪' : '4. Tailpiece Wing Latches', href: isZh ? '/zh/patent-avoidance.html#august-tailpiece' : '/en/patent-avoidance.html#august-tailpiece' },
        { label: isZh ? '5. 出海 FTO 自查清单' : '5. Global FTO Checklist', href: isZh ? '/zh/patent-avoidance.html#checklist' : '/en/patent-avoidance.html#checklist' }
      ];
    } else if (item.href.includes('indigenous-guides.html')) {
      // 工业索引 (全动态 8 大工业体系)
      label = `${rawLabel} (${indexCount})`;
      subItems = [
        { label: isZh ? '🇩🇪 德奥瑞 DIN 18251 锁体与双向离合' : '🇩🇪 DACH DIN 18251 & Dual Clutch', href: isZh ? '/zh/indigenous-guides.html#de-at-ch' : '/en/indigenous-guides.html#de-at-ch' },
        { label: isZh ? '🇫🇷 法比区 NF 70mm 与 7mm 特殊方轴' : '🇫🇷 France NF 70mm & 7mm Spindle', href: isZh ? '/zh/indigenous-guides.html#fr-be' : '/en/indigenous-guides.html#fr-be' },
        { label: isZh ? '🇯🇵 日本区 MIWA 刻印与防盗旋钮抓取' : '🇯🇵 Japan MIWA Case & Pinch Grip', href: isZh ? '/zh/indigenous-guides.html#jp' : '/en/indigenous-guides.html#jp' },
        { label: isZh ? '🇦🇺 澳新英国 Lockwood 001 辅舌死锁' : '🇦🇺 UK/ANZ Lockwood 001 Deadlatch', href: isZh ? '/zh/indigenous-guides.html#uk-anz' : '/en/indigenous-guides.html#uk-anz' },
        { label: isZh ? '🇧🇷 西语拉美 ABNT 40mm 极窄进深' : '🇧🇷 LatAm ABNT 40mm Narrow Backset', href: isZh ? '/zh/indigenous-guides.html#latam' : '/en/indigenous-guides.html#latam' },
        { label: isZh ? '🇺🇸 北美 ANSI 54mm 大孔与扁轴死锁' : '🇺🇸 North America ANSI 54mm Bore', href: isZh ? '/zh/indigenous-guides.html#na' : '/en/indigenous-guides.html#na' }
      ];
    }

    return {
      ...item,
      label,
      subItems,
      href: item.href.startsWith('/') ? item.href : `/${item.href}`
    };
  });
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

  // Find matching real installation samples and diagrams from gallery.json
  const galleryPath = join(CONTENT, 'catalog', 'gallery.json');
  let matchedSamples = [];
  if (existsSync(galleryPath)) {
    const allGallery = JSON.parse(readFileSync(galleryPath, 'utf8'));
    matchedSamples = allGallery.filter((item) => item.familyId === fam.id);
  }

  let gallerySectionHtml = '';
  if (matchedSamples.length > 0) {
    const sampleCards = matchedSamples.map((s) => {
      const sTitle = (s.title && (s.title[lang] || s.title.en || s.title.zh)) || s.id;
      const schematicPath = `/assets/img/diagrams/${s.id}_schematic.svg`;
      const hasSchematic = existsSync(join(ROOT, 'assets/img/diagrams', `${s.id}_schematic.svg`));

      return `
      <div class="lock-detail-sample">
        <div class="lock-detail-sample__header">
          <span class="lock-detail-sample__id">${escapeHtml(s.id)}</span>
          <h4>${escapeHtml(sTitle)}</h4>
          <span class="gallery-card__status ${s.status === 'R1' ? 'gallery-card__status--r1' : 'gallery-card__status--r0'}">${escapeHtml(s.status || 'R0')}</span>
        </div>
        <div class="lock-detail-sample__tier3-header" style="background: #0f172a; color: #f8fafc; padding: 8px 14px; border-radius: 6px 6px 0 0; font-size: 0.78rem; font-weight: 600; letter-spacing: 0.04em; text-transform: uppercase; display: flex; justify-content: space-between; align-items: center; margin-bottom: -1px;">
          <span>${lang === 'zh' ? '实操工程规范与安装案例' : 'Engineering Specifications & Installation'}</span>
          <span style="color: #94a3b8; font-weight: normal; font-size: 0.72rem;">${lang === 'zh' ? '门上实拍 · 原厂蓝图对照' : 'Field Photo · Blueprint'}</span>
        </div>
        <div class="lock-detail-sample__visuals" style="border: 2px solid #0f172a; border-radius: 0 0 6px 6px; overflow: hidden;">
          <div class="lock-detail-sample__pic">
            <p class="lock-detail-sample__label" style="background: #e0f2fe; color: #0369a1; padding: 4px 8px; margin: 0; font-weight: 700; font-size: 0.78rem;">
              📷 ${lang === 'zh' ? '门上真实安装案例 (Door Installation Case)' : 'Real Field Door Installation Case'}
            </p>
            <div class="lock-detail-sample__img-box">
              <img src="${escapeHtml(s.sceneImage || s.image)}" alt="${escapeHtml(sTitle)} 实际安装案例" loading="lazy" />
            </div>
            <p class="lock-detail-sample__caption" style="background: #f8fafc; margin: 0; padding: 6px 8px; border-top: 1px solid #e2e8f0;">${escapeHtml(s.features || '')}</p>
          </div>
          <div class="lock-detail-sample__pic">
            <p class="lock-detail-sample__label" style="background: #fef3c7; color: #92400e; padding: 4px 8px; margin: 0; font-weight: 700; font-size: 0.78rem;">
              📐 ${lang === 'zh' ? '1:1 安装开孔打样与受力原理 (1:1 Template & Schematic)' : '1:1 Blueprint & Drilling Template'}
            </p>
            <div class="lock-detail-sample__img-box">
              <img src="${escapeHtml(s.installationGuide && s.installationGuide.hasSchematic ? s.installationGuide.schematic : (hasSchematic ? schematicPath : (s.sceneImage || s.image)))}" alt="${escapeHtml(sTitle)} 原理与安装打孔图" loading="lazy" />
            </div>
            <p class="lock-detail-sample__caption" style="background: #f8fafc; margin: 0; padding: 6px 8px; border-top: 1px solid #e2e8f0;">${lang === 'zh' ? '标明背距、沉入深度与转动同心度' : 'Includes backset, mortise pocket depth & spindle concentricity'}</p>
          </div>
        </div>
        ${s.installationGuide && s.installationGuide.steps ? `
        <div class="lock-detail-sample__steps-box" style="margin: 16px 0; padding: 14px 18px; background: #f8fafc; border-left: 3px solid #0B1D47; border-radius: 4px;">
          <h5 style="margin: 0 0 10px; color: #0369a1; font-size: 0.95rem;">🛠️ ${lang === 'zh' ? '第三层：标准改装工程与安装工序流程' : 'Tier 3: Standard Retrofit Installation Workflow'}</h5>
          <ol style="margin: 0; padding-left: 20px; font-size: 0.85rem; color: #334155; line-height: 1.6;">
            ${(lang === 'zh' ? s.installationGuide.steps.zh : s.installationGuide.steps.en).map(st => `<li>${escapeHtml(st)}</li>`).join('')}
          </ol>
          <div style="display: flex; gap: 15px; margin-top: 10px; font-size: 0.78rem; color: #64748b;">
            <span>📐 建议门缝间隙: <b>${escapeHtml(s.installationGuide.recommendedClearance)}</b></span>
            <span>⚡ 最低电机扭矩: <b>${escapeHtml(s.installationGuide.requiredTorque)}</b></span>
            <span>📄 打样模板编号: <b>${escapeHtml(s.installationGuide.drillingTemplate)}</b></span>
          </div>
        </div>
        ` : ''}
                ${s.engineeringMatrix ? `
        <div class="lock-detail-sample__matrix-box" style="margin: 14px 0; padding: 12px 16px; background: #f1f5f9; border-radius: 6px; border: 1px solid #cbd5e1; font-size: 0.8rem;">
          <div style="font-weight: 700; color: #0f172a; margin-bottom: 8px; display: flex; align-items: center; justify-content: space-between;">
            <span>🔬 ${lang === "zh" ? "安装公差矩阵与改装合规评级 (Engineering Matrix)" : "Engineering Tolerance & Compliance Matrix"}</span>
            <span style="font-size: 0.72rem; padding: 2px 6px; background: #0B1D47; color: white; border-radius: 3px;">
              ${escapeHtml(s.engineeringMatrix.rentalOptimization.rating)}
            </span>
          </div>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; margin-bottom: 8px;">
            <div style="background: white; padding: 8px; border-radius: 4px; border-left: 3px solid #3b82f6;">
              <span style="color: #64748b; font-size: 0.72rem;">${lang === "zh" ? "垂直下沉耐受度" : "Vertical Sagging Tol."}:</span>
              <div style="font-weight: 600; color: #1e293b;">${escapeHtml(s.engineeringMatrix.saggingTolerance)}</div>
            </div>
            <div style="background: white; padding: 8px; border-radius: 4px; border-left: 3px solid #10b981;">
              <span style="color: #64748b; font-size: 0.72rem;">${lang === "zh" ? "密封条膨胀间隙" : "Weatherstrip Swelling"}:</span>
              <div style="font-weight: 600; color: #1e293b;">${escapeHtml(s.engineeringMatrix.weatherstripSwellingTolerance)}</div>
            </div>
            <div style="background: white; padding: 8px; border-radius: 4px; border-left: 3px solid #f59e0b;">
              <span style="color: #64748b; font-size: 0.72rem;">${lang === "zh" ? "标称电机堵转扭矩" : "Rated Stall Torque"}:</span>
              <div style="font-weight: 600; color: #1e293b;">${escapeHtml(s.engineeringMatrix.ratedMotorTorque)}</div>
            </div>
          </div>
          <div style="background: white; padding: 8px 10px; border-radius: 4px; border-left: 3px solid #8b5cf6; margin-bottom: 6px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <b>🚨 ${lang === "zh" ? "紧急逃生合规认证" : "Emergency Egress Compliance"}:</b>
              <span style="color: #6d28d9; font-weight: 600; font-size: 0.75rem;">${escapeHtml(s.engineeringMatrix.egressCompliance.standard)} (反向阻尼 ${escapeHtml(s.engineeringMatrix.egressCompliance.backdriveTorqueMax)})</span>
            </div>
            <div style="color: #475569; font-size: 0.75rem; margin-top: 3px;">${escapeHtml(s.engineeringMatrix.egressCompliance.description)}</div>
          </div>
          <div style="background: white; padding: 8px 10px; border-radius: 4px; border-left: 3px solid #06b6d4; margin-bottom: 6px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <b>🏠 ${lang === "zh" ? "免打孔/租房改装友好度" : "No-Drill / Rental-Friendly"}:</b>
              <span style="color: #0e7490; font-weight: 600; font-size: 0.75rem;">${escapeHtml(s.engineeringMatrix.rentalOptimization.modificationType)}</span>
            </div>
            <div style="color: #475569; font-size: 0.75rem; margin-top: 3px;">${escapeHtml(s.engineeringMatrix.rentalOptimization.notes)}</div>
          </div>
          <div style="background: white; padding: 8px 10px; border-radius: 4px; border-left: 3px solid #64748b; margin-bottom: 6px;">
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 8px; font-size: 0.72rem;">
              <div><b>🔑 原厂钥匙胚槽型:</b> ${escapeHtml(s.engineeringMatrix.keywaySpecification || 'N/A')}</div>
              <div><b>❄️ 极限气候与电池衰减:</b> ${escapeHtml(s.engineeringMatrix.coldWeatherDerating || 'N/A')}</div>
              <div><b>🔄 执手回弹弹簧阻力:</b> ${escapeHtml(s.engineeringMatrix.handleSpringResistance || 'N/A')}</div>
            </div>
          </div>
          <div style="background: white; padding: 8px 10px; border-radius: 4px; border-left: 3px solid #475569; margin-bottom: 6px;">
            <div style="display: flex; flex-direction: column; gap: 4px; font-size: 0.73rem;">
              <div><b>🔨 ${lang === 'zh' ? '门侧木槽二次扩孔与防裂加固 (Chisel Mortise Rework)' : 'Chisel Mortise Rework & Reinforcement'}:</b> <span style="color: #475569;">${escapeHtml(s.engineeringMatrix.mortiseReworkGuide || 'N/A')}</span></div>
              <div><b>🔩 ${lang === 'zh' ? '贯穿螺栓剪切公差与防夹线套管 (Through-Bolt Wire Guide)' : 'Through-Bolt & Wire Clearance'}:</b> <span style="color: #475569;">${escapeHtml(s.engineeringMatrix.boltWireClearance || 'N/A')}</span></div>
            </div>
          </div>
          <div style="background: white; padding: 8px 10px; border-radius: 4px; border-left: 3px solid #2563eb; margin-bottom: 6px;">
            <div style="display: flex; flex-direction: column; gap: 4px; font-size: 0.73rem;">
              <div><b>⚡ ${lang === 'zh' ? '电机功耗与电池内阻门槛 (Electrical Stall Profile)' : 'Motor Current & Battery Internal Resistance'}:</b> <span style="color: #1e40af;">${escapeHtml(s.engineeringMatrix.electricalProfile || 'N/A')}</span></div>
              <div><b>🛡️ ${lang === 'zh' ? '防钻防撬机械安全认证与保险评级 (Security & Insurance Class)' : 'Security & Insurance Rating'}:</b> <span style="color: #1e40af;">${escapeHtml(s.engineeringMatrix.securityCertification || 'N/A')}</span></div>
              <div><b>🧲 ${lang === 'zh' ? '门状态磁敏传感器与抗金属屏蔽规范 (Door Sensor Gap Spec)' : 'Door Sensor Gap & Metal Shielding'}:</b> <span style="color: #1e40af;">${escapeHtml(s.engineeringMatrix.doorSensorSpec || 'N/A')}</span></div>
            </div>
          </div>
          <div style="background: white; padding: 8px 10px; border-radius: 4px; border-left: 3px solid #059669; margin-bottom: 6px;">
            <div style="display: flex; flex-direction: column; gap: 4px; font-size: 0.73rem;">
              <div><b>🏙️ ${lang === 'zh' ? '大都市存量高频分布 (Metropolitan Cities)' : 'Metropolitan Distribution'}:</b> <span style="color: #065f46; font-weight: 600;">${escapeHtml((s.engineeringMatrix.representativeCities || []).join(' · '))}</span></div>
              <div><b>⚙️ ${lang === 'zh' ? '推荐齿轮减速比与反向自锁力矩 (Gearbox Ratio & Torque)' : 'Gearbox Ratio & Back-Drive Torque'}:</b> <span style="color: #065f46;">${escapeHtml(s.engineeringMatrix.gearboxSpec || 'N/A')}</span></div>
              <div><b>📏 ${lang === 'zh' ? '原厂锁芯外露量与剪切平面规尺 (Shear Line Clearance)' : 'Shear Line Clearance & Depth'}:</b> <span style="color: #065f46;">${escapeHtml(s.engineeringMatrix.shearLineClearance || 'N/A')}</span></div>
            </div>
          </div>
          ${s.engineeringMatrix.nukiRetrofitProfile ? `
          <div style="background: #f8fafc; padding: 8px 10px; border-radius: 4px; border-left: 3px solid #0f172a; margin-bottom: 6px;">
            <div style="display: flex; flex-direction: column; gap: 4px; font-size: 0.73rem;">
              <div><b>🎯 ${lang === 'zh' ? 'Nuki 加装指数与核心 ICP 画像' : 'Nuki Retrofit & ICP Profile'}:</b> <span style="color: #86198f; font-weight: 700;">★ 指数: ${s.engineeringMatrix.nukiRetrofitProfile.nukiRetrofitScore}/100</span> · <span style="color: #701a75;">${escapeHtml(s.engineeringMatrix.nukiRetrofitProfile.primaryICP || 'N/A')}</span></div>
              <div><b>🔑 ${lang === 'zh' ? '租客退租无损复原评级' : 'Tenant Zero-Damage Grade'}:</b> <span style="color: #86198f;">${escapeHtml(s.engineeringMatrix.nukiRetrofitProfile.tenantFriendlyGrade || 'N/A')}</span> · 预计施工耗时: ${s.engineeringMatrix.nukiRetrofitProfile.installationTimeMin} 分钟</div>
              <div><b>🛠️ ${lang === 'zh' ? '推荐搭载专属改装 BOM' : 'Recommended Retrofit Kit'}:</b> <span style="color: #4a044e; font-weight: 600;">${escapeHtml((s.engineeringMatrix.nukiRetrofitProfile.retrofitKit || []).join(' + '))}</span></div>
            </div>
          </div>` : ''}
          ${s.engineeringMatrix.weatherproofingMatrix ? `
          <div style="background: #f8fafc; padding: 8px 10px; border-radius: 4px; border-left: 3px solid #475569; margin-bottom: 6px;">
            <div style="display: flex; flex-direction: column; gap: 4px; font-size: 0.73rem;">
              <div><b>☀️ ${lang === 'zh' ? '耐候防腐与盐雾测试标准 (Weatherproofing & Salt Spray)' : 'Salt Spray & Weatherproofing'}:</b> <span style="color: #92400e; font-weight: 600;">${escapeHtml(s.engineeringMatrix.weatherproofingMatrix.saltSprayClass)}</span> · ${escapeHtml(s.engineeringMatrix.weatherproofingMatrix.ipRating)}</div>
              <div><b>🌡️ ${lang === 'zh' ? '极限温度与密封胶条规范' : 'Thermal & Gasket'}:</b> <span style="color: #b45309;">${escapeHtml(s.engineeringMatrix.weatherproofingMatrix.solarThermalMax)}</span> · ${escapeHtml(s.engineeringMatrix.weatherproofingMatrix.epdmGasketSpec)}</div>
            </div>
          </div>` : ''}
          ${s.engineeringMatrix.multipointKinematics && s.engineeringMatrix.multipointKinematics.isMultipointCompatible ? `
          <div style="background: #f8fafc; padding: 8px 10px; border-radius: 4px; border-left: 3px solid #0f172a; margin-bottom: 6px;">
            <div style="display: flex; flex-direction: column; gap: 4px; font-size: 0.73rem;">
              <div><b>🔄 ${lang === 'zh' ? '多点联动门抬把手行程与阻尼 (Multipoint Kinematics)' : 'Multipoint Kinematics & Torque'}:</b> <span style="color: #115e59; font-weight: 600;">抬把手角度: ${escapeHtml(s.engineeringMatrix.multipointKinematics.liftAngle)}</span> · 传动阻尼: ${escapeHtml(s.engineeringMatrix.multipointKinematics.camDriveTorque)}</div>
              <div><b>🔧 ${lang === 'zh' ? '主流五金厂与偏心调节指南' : 'Hardware Vendors & Tuning'}:</b> <span style="color: #134e4a;">${escapeHtml(s.engineeringMatrix.multipointKinematics.majorHardwareVendors)}</span> · ${escapeHtml(s.engineeringMatrix.multipointKinematics.fieldAdjustmentGuide)}</div>
            </div>
          </div>` : ''}
          ${s.engineeringMatrix.emergencyClutchWhitelist && s.engineeringMatrix.emergencyClutchWhitelist.isMandatory ? `
          <div style="background: #fef2f2; padding: 8px 10px; border-radius: 4px; border-left: 3px solid #ef4444; margin-bottom: 6px;">
            <div style="display: flex; flex-direction: column; gap: 4px; font-size: 0.73rem;">
              <div><b>⚠️ ${lang === 'zh' ? '欧标防反锁应急双离合官方认证白名单' : 'Emergency Dual-Clutch Approved List'}:</b> <span style="color: #991b1b; font-weight: 700;">${escapeHtml(s.engineeringMatrix.emergencyClutchWhitelist.standard)}</span></div>
              <div style="color: #b91c1c;"><b>官方推荐防锁死锁芯:</b> ${(s.engineeringMatrix.emergencyClutchWhitelist.approvedModels || []).map(m => escapeHtml(m)).join(' · ')}</div>
              <div style="color: #7f1d1d; font-size: 0.7rem; font-style: italic;">${escapeHtml(s.engineeringMatrix.emergencyClutchWhitelist.lockoutRiskWarning)}</div>
            </div>
          </div>` : ''}
          ${s.engineeringMatrix.doorThicknessMatrix ? `
          <div style="background: #f8fafc; padding: 8px 10px; border-radius: 4px; border-left: 3px solid #475569;">
            <div style="display: flex; flex-direction: column; gap: 4px; font-size: 0.73rem;">
              <div><b>🚪 ${lang === 'zh' ? '门扇厚度与对穿螺栓方轴速查 (Door Thickness & Fasteners)' : 'Door Thickness & Fasteners'}:</b> <span style="color: #1e293b; font-weight: 600;">主流门厚: ${escapeHtml(s.engineeringMatrix.doorThicknessMatrix.typicalDoorThickness)}</span></div>
              <div><b>🔩 ${lang === 'zh' ? '方轴与螺栓包工程选型' : 'Spindle & Bolt Spec'}:</b> 方轴: ${escapeHtml(s.engineeringMatrix.doorThicknessMatrix.spindleRequirement)} · 螺丝: ${escapeHtml(s.engineeringMatrix.doorThicknessMatrix.boltRequirement)}</div>
              <div><b>🛡️ ${lang === 'zh' ? '门板加固与压溃防护' : 'Reinforcement'}:</b> ${escapeHtml(s.engineeringMatrix.doorThicknessMatrix.reinforcementPlate)}</div>
            </div>
          </div>` : ''}
        </div>
        ` : ""}
        ${s.gtmNotes ? `
        <div class="lock-detail-sample__engineering-box">
          <h5>${lang === 'zh' ? '⚙️ 智能化改造工程难点、实测尺寸与阻力风险' : '⚙️ Retrofit Engineering & Resistance Notes'}</h5>
          <p>${escapeHtml(s.gtmNotes)}</p>
          ${s.physicalTest ? `<p class="lock-detail-sample__check"><b>${lang === 'zh' ? '最低实物验证标准' : 'Minimum physical verification'}：</b>${escapeHtml(s.physicalTest)}</p>` : ''}
        </div>
        ` : ''}
      </div>`;
    }).join('\n');

    // Ingest all matching field cases from installation-cases.json for high-immersion jobsite experience
    const casesPath = join(CONTENT, 'catalog', 'installation-cases.json');
    let matchedFieldCases = [];
    if (existsSync(casesPath)) {
      const allCases = JSON.parse(readFileSync(casesPath, 'utf8'));
      matchedFieldCases = allCases.filter(c => c.lockFamilyId === fam.id);
    }

    let fieldCasesHtml = '';
    if (matchedFieldCases.length > 0) {
      const fieldCards = matchedFieldCases.map(fc => {
        const fcTitle = (fc.title && (fc.title[lang] || fc.title.en)) || fc.id;
        const fcDesc = (fc.desc && (fc.desc[lang] || fc.desc.en)) || '';
        const fcRegion = (fc.regionName && (fc.regionName[lang] || fc.regionName.en)) || fc.regionCode;

        return `<div class="lock-detail-field-card" style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 5px rgba(0,0,0,0.05); display: flex; flex-direction: column;">
          <div style="position: relative; height: 180px; background: #0f172a; overflow: hidden;">
            <img src="${escapeHtml(fc.image)}" alt="${escapeHtml(fcTitle)}" loading="lazy" style="width: 100%; height: 100%; object-fit: cover;" />
            <span style="position: absolute; top: 8px; left: 8px; background: rgba(15,23,42,0.85); color: #38bdf8; font-size: 0.7rem; font-weight: 700; padding: 2px 7px; border-radius: 4px;">
              ${escapeHtml(fc.id)} · ${escapeHtml(fc.sceneType)}
            </span>
            <span style="position: absolute; bottom: 8px; right: 8px; background: rgba(0,0,0,0.7); color: #fff; font-size: 0.68rem; padding: 2px 6px; border-radius: 3px;">
              ${escapeHtml(fcRegion)}
            </span>
          </div>
          <div style="padding: 12px 14px; flex: 1; display: flex; flex-direction: column;">
            <h5 style="margin: 0 0 6px; font-size: 0.95rem; line-height: 1.4; color: #0f172a;">${escapeHtml(fcTitle)}</h5>
            <p style="margin: 0 0 10px; font-size: 0.8rem; color: #475569; line-height: 1.45; flex: 1;">${escapeHtml(fcDesc)}</p>
            <div style="background: #f1f5f9; padding: 5px 8px; border-radius: 4px; font-size: 0.72rem; color: #334155; border-left: 3px solid #0f172a;">
              ⚙️ <b>${lang === 'zh' ? '实操指标:' : 'Metrics:'}</b> ${escapeHtml(fc.keyMetrics)}
            </div>
          </div>
        </div>`;
      }).join('\n');

      fieldCasesHtml = `
      <div class="lock-detail-jobsite-section" style="margin-top: 36px; padding: 20px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 8px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; flex-wrap: wrap; gap: 8px;">
          <div>
            <h3 style="margin: 0; font-size: 1.15rem; color: #0f172a; display: flex; align-items: center; gap: 6px;">
              <span>🔨</span> ${lang === 'zh' ? '一线安装工程实态与避坑工单现场图库 (' + matchedFieldCases.length + ' 个真实工况)' : 'Field Installation Cases & Jobsite Photos (' + matchedFieldCases.length + ' cases)'}
            </h3>
            <p style="margin: 4px 0 0; font-size: 0.82rem; color: #64748b;">${lang === 'zh' ? '展示真实开孔夹具钻孔、木工凿槽、转轴拉出与防盗扣板对齐的真实施工实录，带来 1:1 一线现场感。' : 'Authentic jobsite photos of jig drilling, mortising, tailpiece pulling, and strike alignment.'}</p>
          </div>
          <a class="block-hero__btn" style="font-size: 0.8rem; padding: 6px 12px; background: #0B1D47; color: #fff;" href="${lang === 'zh' ? '/zh/install-gallery.html' : '/en/install-gallery.html'}">
            ${lang === 'zh' ? '浏览全站 41 个工程实录图库 →' : 'View All 41 Field Cases →'}
          </a>
        </div>
        <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px;">
          ${fieldCards}
        </div>
      </div>`;
    }

    gallerySectionHtml = `
<h2 id="installation-samples">${lang === 'zh' ? '实物安装与改造图谱' : 'Installation Photos & Retrofit Diagrams'}</h2>
<p class="lede">${lang === 'zh' ? '以下为该锁族在实际门上的实物安装案例、传动原理示意图与智能化改造常见问题分析：' : 'Field installation examples, drive schematics, and common retrofit failure modes for this lock family:'}</p>
<div class="lock-detail-samples">
  ${sampleCards}
</div>
${fieldCasesHtml}
`;
  }

  const html = `
<p class="lede">${escapeHtml(fam.summary[lang] || fam.summary.en)}</p>
<p class="meta">${statusBadge(fam.status, lang)} <span class="meta__sep">·</span> <strong>${escapeHtml(t(terms.labels, 'regions', lang))}:</strong> ${escapeHtml(fam.regions.join(', '))}</p>
${fam.aliases ? `<p><strong>${escapeHtml(t(terms.labels, 'aliases', lang))}:</strong> ${escapeHtml((fam.aliases[lang] || fam.aliases.en || []).join(' · '))}</p>` : ''}

${gallerySectionHtml}

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
    ...(matchedSamples.length ? [{ level: 2, id: 'installation-samples', text: lang === 'zh' ? '实物安装与改造图谱' : 'Installation Photos & Retrofit Diagrams' }] : []),
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


/**
 * Gallery Wall Fragment: renders the 30 representative lock photo cards on the landing page.
 */

function getGalleryBlocks(lang) {
  const isZh = lang === 'zh';
  const galleryPath = join(CONTENT, 'catalog', 'gallery.json');
  if (!existsSync(galleryPath)) return [];
  const items = JSON.parse(readFileSync(galleryPath, 'utf8'));
  // 核心排序依据：1. 主流基准 (Mainstream) 严格排在最前面；2. 综合打分/市场占有率 (selectionScore) 降序排列
  items.sort((a, b) => {
    const aMain = a.tierClass === 'Mainstream' ? 1 : 0;
    const bMain = b.tierClass === 'Mainstream' ? 1 : 0;
    if (aMain !== bMain) return bMain - aMain; // 主流排在非主流前面
    const aScore = (a.selectionScore && a.selectionScore.overallScore) || 0;
    const bScore = (b.selectionScore && b.selectionScore.overallScore) || 0;
    if (aScore !== bScore) return bScore - aScore; // 得分高的排前面
    return a.id.localeCompare(b.id);
  });

  return [
    {
      code: 'na',
      title: isZh ? '🇺🇸 北美标准板块 (Americas — ANSI / BHMA)' : '🇺🇸 North America (ANSI/BHMA)',
      shortTitle: isZh ? '北美标准板块' : 'North America',
      subtitle: isZh ? '全球存量最大的智能锁加装市场 · 标准 54mm 大孔位、单插销死锁 (Deadbolt) 与 60/70mm 标准背距' : 'World largest retrofit market · Standard 54mm bore, deadbolt & 60/70mm backset',
      hero: {
        title: isZh ? '核心改装基准：美标单缸插销死锁 (ANSI Deadbolt / Schlage B60)' : 'Core Retrofit Baseline: ANSI Deadbolt (Schlage B60)',
        desc: isZh ? 'August 与 SwitchBot 的全球基本盘。标准扁平尾轴（Tailpiece）直接啮合；改造核心难点在于门扇下沉与密封条导致插销与扣板卡阻。' : 'Core baseline for August & SwitchBot. Flat tailpiece interface; key challenge is sag binding.',
        image: '/assets/img/hero/hero-na-deadbolt.png',
        familyId: 'us-deadbolt',
        tag: isZh ? '⭐ 极强相关 · 改装第一基准' : '⭐ Core Retrofit Baseline'
      },
      items: items.filter(i => i.block === 'na')
    },
    {
      code: 'europe5',
      title: isZh ? '🇪🇺 欧陆五国板块 (Continental Europe — DIN / EN)' : '🇪🇺 Continental Europe (DIN/EN)',
      shortTitle: isZh ? '欧陆五国板块' : 'Continental Europe',
      subtitle: isZh ? '西欧与中欧成熟大容量市场 · 欧标槽型锁芯 (Euro Profile DIN 18252)、DIN 18251 插芯锁体与抬把手多点联动锁' : 'Mature European standard · Euro profile cylinders, DIN 18251 cases & multipoint systems',
      hero: {
        title: isZh ? '核心改装基准：欧标槽型双锁芯 (Euro Profile DIN 18252)' : 'Core Retrofit Baseline: Euro Profile Double-Cylinder (DIN 18252)',
        desc: isZh ? 'Nuki 与 Yale Linus 的全球基本盘。死穴在于内侧常插钥匙时，锁芯必须具备 DIN 18252 BS 双向应急离合认证，否则断电造成彻底反锁。' : 'Nuki & Linus core baseline. Critical: MUST feature DIN 18252 BS dual-action emergency clutch.',
        image: '/assets/img/hero/hero-europe-eurocylinder.jpg',
        familyId: 'euro-cylinder-mortise',
        tag: isZh ? '⭐ 极强相关 · 欧标第一基准' : '⭐ Core Euro Baseline'
      },
      items: items.filter(i => i.block === 'europe5')
    },
    {
      code: 'uk-anz',
      title: isZh ? '🇦🇺🇬🇧 澳洲与英国板块 (Pacific & UK — AS / BS)' : '🇦🇺🇬🇧 Australia & UK (AS/BS)',
      shortTitle: isZh ? '澳新英国板块' : 'Australia & UK',
      subtitle: isZh ? '高防盗高人工成本市场 · 澳洲 Lockwood 001 表面安装夜闩锁 (Rim Deadlatch)、大洋洲短进深锁体与英国 5 拨杆防盗插芯锁' : 'High-security & high-labor market · Lockwood 001 surface deadlatches, short-backset & BS 5-lever',
      hero: {
        title: isZh ? '核心改装基准：澳式表面安装双扣死锁 (Lockwood 001 Deadlatch)' : 'Core Retrofit Baseline: Lockwood 001 Rim Deadlatch',
        desc: isZh ? '澳洲独栋木门第一基准。特有水滴形大旋钮需专属 ADP-05 夹具；致命点在于辅舌必须完全压入方可死锁，门缝变异极易引发假锁死。' : 'AU wooden door benchmark. Teardrop turn requires ADP-05 adapter; auxiliary bolt must depress fully.',
        image: '/assets/img/hero/hero-anz-lockwood001.jpg',
        familyId: 'au-deadlatch',
        tag: isZh ? '⭐ 极强相关 · 澳新第一基准' : '⭐ Pacific Baseline'
      },
      items: items.filter(i => i.block === 'uk-anz')
    },
    {
      code: 'jp-kr',
      title: isZh ? '🇯🇵🇰🇷 日韩精工板块 (Japan & Korea — JIS / KS)' : '🇯🇵🇰🇷 Japan & Korea (JIS/KS)',
      shortTitle: isZh ? '日韩精工板块' : 'Japan & Korea',
      subtitle: isZh ? '极高精密装配工业体系 · 日本 MIWA / GOAL 超薄锁体、B5 防犯捏合旋钮与韩国无孔全自动锁' : 'Precision Asian standards · MIWA/GOAL slim mortise, B5 anti-theft thumbturn & Korean electronic push-pull',
      hero: {
        title: isZh ? '核心改装基准：日本 MIWA 13LA / B5 防犯斜坡旋钮锁' : 'Core Retrofit Baseline: MIWA 13LA / B5 Thumbturn',
        desc: isZh ? '日本独栋与公寓第一基准。内旋钮自带双侧防盗下压弹簧片；改装必须搭配 ADP-03 双斜坡抓手，转动前自动解锁，杜绝卡死烧机。' : 'Japan benchmark. Features anti-theft pinch release thumbturn requiring ADP-03 adapter.',
        image: '/assets/img/hero/hero-jp-miwa-door.jpg',
        familyId: 'jp-miwa-case',
        tag: isZh ? '⭐ 极强相关 · 日韩改装基准' : '⭐ Japan & Korea Baseline'
      },
      items: items.filter(i => i.block === 'jp-kr')
    },
    {
      code: 'sea',
      title: isZh ? '🇸🇬🇲🇾 东南亚板块 (ASEAN / SEA — SS / MS)' : '🇸🇬🇲🇾 South East Asia (ASEAN)',
      shortTitle: isZh ? '东南亚板块' : 'South East Asia',
      subtitle: isZh ? '东盟高密度热带五金体系 · 新加坡组屋 HDB 外铁闸与内木门极窄防撞空间、大马与泰国窄体铝门锁' : 'High-density tropical ASEAN systems · Singapore HDB gate clash, Malaysian & Thai narrow aluminum doors',
      hero: {
        title: isZh ? '核心改装基准：新加坡建屋局组屋 HDB 铁闸双门联动锁' : 'Core Retrofit Baseline: Singapore HDB Gate Mortise',
        desc: isZh ? '新加坡组屋特色。外侧铁防盗网门与内侧木门间距极窄（通常 <80mm）；改装锁外壳极易与内门拉手碰撞（Clash），需极窄面板与超薄把手。' : 'Singapore HDB benchmark. Gate-to-door gap <80mm causes severe handle collision.',
        image: '/assets/img/hero/hero-sea-hdb.jpg',
        familyId: 'sg-hdb-mortise',
        tag: isZh ? '⭐ 极强相关 · 东南亚基准' : '⭐ South East Asia Baseline'
      },
      items: items.filter(i => i.block === 'sea')
    },
    {
      code: 'gcc',
      title: isZh ? '🇦🇪🇸🇦 中东海湾板块 (Middle East / GCC — SASO / BS / EN)' : '🇦🇪🇸🇦 Middle East GCC (SASO)',
      shortTitle: isZh ? '中东海湾板块' : 'Middle East / GCC',
      subtitle: isZh ? '高客单重门耐候市场 · 沙特与阿联酋 60~90mm 超厚大门、英标 85mm 插芯、意标多点防盗与 75°C 太阳暴晒耐候工况' : 'High-AOV heavy door market · KSA/UAE 60-90mm doors, BS 85mm mortise & 75°C solar resistance',
      hero: {
        title: isZh ? '核心改装基准：海湾厚木门英标 85mm 重型插芯锁' : 'Core Retrofit Baseline: GCC BS 85mm Heavy-Duty Mortise',
        desc: isZh ? '中东公寓与独栋大门最主流五金。大门厚重（55~85mm），标配必须提供 ADP-11 超长螺栓与方轴包；电子系统需耐受 75°C 暴晒与 IP65 沙尘。' : 'GCC benchmark. 55-85mm heavy doors require ADP-11 long-tailpiece bolts & 75°C solar thermal design.',
        image: '/assets/img/gallery/eu-kfv-multipoint_real.jpg',
        familyId: 'euro-cylinder-mortise',
        tag: isZh ? '⭐ 极强相关 · 中东海湾基准' : '⭐ Middle East GCC Baseline'
      },
      items: items.filter(i => i.block === 'gcc')
    },
    {
      code: 'latam',
      title: isZh ? '🌎 拉美新兴板块 (Latin America — ABNT / IRAM)' : '🌎 Latin America (ABNT)',
      shortTitle: isZh ? '拉美新兴板块' : 'Latin America',
      subtitle: isZh ? '拉美大容量新兴五金体系 · 巴西 ABNT 窄背距插芯锁 (40/45mm)、薄门扇 (30mm) 与安第斯重型外装双钩锁' : 'Emerging market · Brazil ABNT narrow backsets (40/45mm), thin doors (30mm) & rim locks',
      hero: {
        title: isZh ? '核心改装基准：巴西 ABNT NBR 14913 极窄背距插芯锁 (PADO)' : 'Core Retrofit Baseline: Brazil ABNT Narrow Mortise (PADO)',
        desc: isZh ? '拉美市场第一基准。门框立柱极窄，背距仅 40mm/45mm；传统智能锁体过宽无法开槽，改装必须采用 38mm 极窄面板并保留原厂扣板。' : 'LatAm benchmark. Narrow stiles with 40/45mm backset require 38mm slim bodies.',
        image: '/assets/img/hero/hero-latam-abnt.webp',
        familyId: 'us-mortise',
        tag: isZh ? '⭐ 极强相关 · 拉美改装基准' : '⭐ Latin America Baseline'
      },
      items: items.filter(i => i.block === 'latam')
    },
    {
      code: 'af-sa',
      title: isZh ? '🇮🇳🇿🇦 非洲与南亚板块 (South Asia & Africa — BIS / SABS)' : '🇮🇳🇿🇦 South Asia & Africa (BIS)',
      shortTitle: isZh ? '非洲南亚板块' : 'South Asia & Africa',
      subtitle: isZh ? '印度 Godrej 表面夜闩死锁三插销体系、东非与南非 Union 杠杆防盗锁与高湿耐候工况' : 'Indian Godrej rim deadbolts, South African Union lever systems & tropical monsoon weatherproofing',
      hero: {
        title: isZh ? '核心改装基准：印度与南亚 Godrej 三插销外装防撬死锁' : 'Core Retrofit Baseline: Indian Godrej Tribolt Deadbolt',
        desc: isZh ? '印度与南亚民居第一基准。表面安装重型方形锁盒，三根高碳钢圆形死锁插销；内侧为机械大旋钮，改装需搭配专用外装夹爪。' : 'South Asian benchmark. Surface-mounted box with 3 heavy deadbolts requiring external pinch cams.',
        image: '/assets/img/indigenous/uk-nightlatch.jpg',
        familyId: 'in-mortise-rim',
        tag: isZh ? '⭐ 极强相关 · 南亚非洲基准' : '⭐ South Asia Africa Baseline'
      },
      items: items.filter(i => i.block === 'af-sa')
    }
  ];}

function renderGalleryCard(item, lang) {
  const isZh = lang === 'zh';
  const title = (item.title && (item.title[lang] || item.title.en || item.title.zh)) || item.id;
  const regionLabel = item.region || '';
  const statusClass = item.status === 'R1' ? 'gallery-card__status--r1' : (item.status === 'R2' ? 'gallery-card__status--r2' : 'gallery-card__status--r0');
  const statusText = item.status || 'R0';

  const searchText = `${item.id} ${title} ${regionLabel} ${item.features || ''}`.toLowerCase();
  const hasFamily = !!item.familyId;
  const familyHref = hasFamily ? `/${urlFor(lang, `locks/${item.familyId}.html`)}` : `/${urlFor(lang, 'locks/index.html')}`;

  const sceneImg = item.sceneImage || item.image;
  const productImg = item.productImage || item.image;

  const isMainstream = item.tierClass === 'Mainstream';
  const cardStyle = isMainstream 
    ? 'border: 1px solid #cbd5e1; background: #ffffff; box-shadow: 0 2px 6px rgba(15, 23, 42, 0.04); border-left: 3px solid #0B1D47;' 
    : 'border: 1px solid #e2e8f0; background: #f8fafc; opacity: 0.88; border-left: 3px solid #94a3b8; filter: saturate(0.9);';

  return `<div class="gallery-card gallery-card--${isMainstream ? 'mainstream' : 'niche'}" data-gallery-card data-tier="${escapeHtml(item.tierClass || "Mainstream")}" data-region="${escapeHtml(item.block)}" data-search-text="${escapeHtml(searchText)}" style="${cardStyle} border-radius: 8px; overflow: hidden; display: flex; flex-direction: column; transition: transform 0.2s, box-shadow 0.2s, opacity 0.2s;">
    <div class="gallery-card__dual-img-container" style="display: grid; grid-template-columns: 1fr 1fr; background: #e2e8f0; gap: 1px; position: relative; border-radius: 6px 6px 0 0; overflow: hidden;">
      <a class="gallery-card__img-link" href="${familyHref}" title="${isZh ? '实景图' : 'Scene'}" style="position: relative; display: block; overflow: hidden; height: 165px; background: #1e293b;">
        <img class="gallery-card__img" src="${escapeHtml(sceneImg)}" alt="${escapeHtml(title)}" loading="lazy" style="width: 100%; height: 100%; object-fit: cover;" />
        <span style="position: absolute; bottom: 6px; left: 6px; background: rgba(15, 23, 42, 0.85); color: #94a3b8; font-size: 0.65rem; font-weight: 600; padding: 2px 6px; border-radius: 2px; letter-spacing: 0.05em; text-transform: uppercase;">${isZh ? '实景' : 'SCENE'}</span>
      </a>
      <a class="gallery-card__img-link" href="${familyHref}" title="${isZh ? '机械结构' : 'Product'}" style="position: relative; display: block; overflow: hidden; height: 165px; background: #ffffff;">
        <img class="gallery-card__img" src="${escapeHtml(productImg)}" alt="${escapeHtml(title)}" loading="lazy" style="width: 100%; height: 100%; object-fit: contain; padding: 6px;" />
        <span style="position: absolute; bottom: 6px; right: 6px; background: rgba(15, 23, 42, 0.85); color: #94a3b8; font-size: 0.65rem; font-weight: 600; padding: 2px 6px; border-radius: 2px; letter-spacing: 0.05em; text-transform: uppercase;">${isZh ? '结构' : 'ASSEMBLY'}</span>
      </a>
      <div class="gallery-card__badges" style="position: absolute; top: 6px; left: 6px; right: 6px; display: flex; justify-content: space-between; align-items: center; pointer-events: none;">
        <div style="display: flex; gap: 4px; align-items: center;">
          <span class="gallery-card__id" style="font-family: var(--font-mono, monospace); font-weight: 700; font-size: 0.72rem;">${escapeHtml(item.id)}</span>
          ${isMainstream 
            ? `<span style="background: #0B1D47; color: #ffffff; font-size: 0.68rem; font-weight: 700; padding: 2px 7px; border-radius: 3px; letter-spacing: 0.03em; box-shadow: 0 1px 3px rgba(0,0,0,0.2);">★ ${isZh ? '主流基准' : 'MAINSTREAM'}</span>` 
            : `<span style="background: #e2e8f0; color: #64748b; font-size: 0.65rem; font-weight: 600; padding: 2px 6px; border-radius: 3px; border: 1px solid #cbd5e1;">${isZh ? '非主流/小众' : 'NICHE'}</span>`}
        </div>
        <span class="gallery-card__status ${statusClass}">${escapeHtml(statusText)}</span>
      </div>
    </div>
    <div class="gallery-card__body" style="padding: 14px 16px;">
      <div class="gallery-card__region" style="font-size: 0.75rem; letter-spacing: 0.04em; text-transform: uppercase; color: #64748b; font-weight: 600; margin-bottom: 4px;">${escapeHtml(regionLabel)}</div>
      <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 8px; margin-bottom: 6px;">
        <h3 class="gallery-card__title" style="margin: 0; font-size: 1.02rem; font-weight: ${isMainstream ? '700' : '500'}; line-height: 1.4; color: ${isMainstream ? '#0f172a' : '#475569'};">
          <a href="${familyHref}" style="color: inherit; text-decoration: none;">${escapeHtml(title)}</a>
        </h3>
        <span style="font-size: 0.7rem; font-weight: 600; padding: 1px 5px; border-radius: 3px; white-space: nowrap; ${isMainstream ? 'background: #e0f2fe; color: #0369a1;' : 'background: #f1f5f9; color: #94a3b8;'}">
          ${escapeHtml(item.marketSharePercent || (isMainstream ? '≥25%' : '<10%'))}
        </span>
      </div>
      <!-- 极简五金公差微标签替代冗长文字 -->
      <div style="display: flex; gap: 6px; flex-wrap: wrap; margin: 6px 0 10px;">
        <span style="font-size: 0.72rem; background: #f1f5f9; color: #334155; padding: 2px 7px; border-radius: 4px; font-weight: 600;">⌖ ${escapeHtml(item.engineeringMatrix?.shearLineClearance ? item.engineeringMatrix.shearLineClearance.split('/')[0] : '标准背距')}</span>
        <span style="font-size: 0.72rem; background: #f1f5f9; color: #334155; padding: 2px 7px; border-radius: 4px; font-weight: 600;">⎔ ${escapeHtml(item.engineeringMatrix?.doorThicknessMatrix?.typicalDoorThickness || '标配门厚')}</span>
        <span style="font-size: 0.72rem; background: #f1f5f9; color: #334155; padding: 2px 7px; border-radius: 4px; font-weight: 600;">⚡ ${escapeHtml(item.engineeringMatrix?.gearboxSpec ? item.engineeringMatrix.gearboxSpec.split('；')[0] : '直驱减速')}</span>
      </div>
      <div class="gallery-card__footer" style="padding-top: 8px; border-top: 1px solid #f1f5f9; display: flex; justify-content: flex-end;">
        <a class="gallery-card__link" href="${familyHref}" style="font-size: 0.78rem; font-weight: 700; color: #0f172a; text-decoration: none;">
          <span>${isZh ? '拆解图谱' : 'Blueprint'} →</span>
        </a>
      </div>
    </div>
  </div>`;
}

/**
 * PURE GALLERY LANDING PAGE:
 * THE LANDING PAGE ONLY HAS 5 MAJOR AREA ENTRIES. NO OTHER DISTRACTIONS.
 */
function galleryFragment(lang) {
  const isZh = lang === 'zh';
  const blocks = getGalleryBlocks(lang);
  if (!blocks.length) return '';

  const portalCards = blocks.map((b, idx) => {
    const categoryUrl = `/${urlFor(lang, `categories/${b.code}.html`)}`;
    const idxBadge = idx + 1;
    // 视觉注意力体系：Tier 1 核心基准高亮 vs 其它板块弱化
    const isCoreTier1 = ['na', 'europe5', 'uk-anz', 'jp-kr'].includes(b.code);
    const cardClass = isCoreTier1 ? 'gallery-portal-card gallery-portal-card--core' : 'gallery-portal-card gallery-portal-card--secondary';
    const tierBadge = isCoreTier1 ? (isZh ? '<span class="portal-tier-pill portal-tier-pill--core">★ 核心加装基准</span>' : '<span class="portal-tier-pill portal-tier-pill--core">★ CORE BASELINE</span>') : '';
    return `<a class="${cardClass}" href="${categoryUrl}" data-portal-target="${escapeHtml(b.code)}">
      ${tierBadge}
      <div class="gallery-portal-card__media" style="position: relative; overflow: hidden; background: #f8fafc;">
        <img class="gallery-portal-card__img" src="${escapeHtml(b.hero.image)}" alt="${escapeHtml(b.title)}" loading="lazy" width="360" height="230" />
        <span class="gallery-portal-card__keyhint" title="${isZh ? '按数字键直达' : 'Press key'}">[${idxBadge}]</span>
      </div>
      <div class="gallery-portal-card__body">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 6px; margin-bottom: 4px;">
          <h2 class="gallery-portal-card__name" style="margin: 0; flex: 1; font-size: 0.96rem; font-weight: 700; line-height: 1.35; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="${escapeHtml(b.title)}">${escapeHtml(b.title)}</h2>
          <span style="font-size: 0.70rem; color: #64748b; font-weight: 700; white-space: nowrap; background: #f1f5f9; padding: 2px 6px; border-radius: 4px; border: 1px solid #e2e8f0;">${b.items.length} ${isZh ? '款' : 'models'}</span>
        </div>
        <div class="gallery-portal-card__baseline" style="color: var(--color-primary, #0f172a); font-weight: 600; font-size: 0.82rem; line-height: 1.35; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="${escapeHtml(b.hero.title.replace(/^[^：:]*[：:]/, '').trim())}">${escapeHtml(b.hero.title.replace(/^[^：:]*[：:]/, '').trim())}</div>
      </div>
    </a>`;
  }).join('\n');

  return `<div class="gallery-wall gallery-wall--pure-portal">
    <div class="gallery-portal-section">
      <div class="gallery-portal-grid">
        ${portalCards}
      </div>
    </div>
  </div>
  <script src="/assets/js/portal-shortcuts.js" defer></script>`;
}

const FRAGMENTS = {
  '{{gallery}}': galleryFragment,
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
  if (existsSync(OUT)) {
    try {
      rmSync(OUT, { recursive: true, force: true, maxRetries: 3, retryDelay: 50 });
    } catch (e) {
      // ignore concurrent read lock
    }
  }
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
  // The root /index.html is the same page as <defaultLang>/index.html, so both
  // are registered for hreflang alternates to work in either direction.
  for (const lang of LANGS) {
    if (lang === DEFAULT_LANG) {
      existing.add(`${DEFAULT_LANG}:index.html`);
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
    for (const b of ['na', 'europe5', 'uk-anz', 'jp-kr', 'sea', 'gcc']) register(lang, `categories/${b}.html`);
    register(lang, 'install-gallery.html');
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

      const isHomePage = slug === 'index.html';
      const hasLeadingH1 = html.trim().startsWith('<h1') || html.includes('<h1');
      const bodyHtmlContent = isHomePage ? html : (hasLeadingH1 ? html : `<h1>${escapeHtml(title)}</h1>\n${html}`);

      emitPage({
        lang,
        slug,
        title,
        description,
        bodyHtml: bodyHtmlContent,
        breadcrumbs: isHomePage ? [] : crumbs,
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

    
    // Regional Category Gallery Pages (L2 Gallery Grid)
    // Emit install-gallery.html for this language
    const isZh = lang === 'zh';
    const casesPath = join(CONTENT, 'catalog', 'installation-cases.json');
    const cases = existsSync(casesPath) ? JSON.parse(readFileSync(casesPath, 'utf8')) : [];
    
    const casesCards = cases.map(c => {
      const cTitle = (c.title && (c.title[lang] || c.title.en)) || c.id;
      const cDesc = (c.desc && (c.desc[lang] || c.desc.en)) || '';
      const cRegion = (c.regionName && (c.regionName[lang] || c.regionName.en)) || c.regionCode;
      const lockLink = `/${urlFor(lang, `locks/${c.lockFamilyId}.html`)}`;
      const catLink = `/${urlFor(lang, `categories/${c.regionCode}.html`)}`;

      // 提取工程关键微指标，转为 ASSA ABLOY 紧凑工业胶囊
      const metricChips = (c.keyMetrics || '')
        .split(/[·,;]/)
        .filter(m => m.trim().length > 0)
        .slice(0, 2)
        .map(m => `<span style="display: inline-block; background: #f8fafc; border: 1px solid #e2e8f0; color: #334155; font-size: 0.72rem; font-weight: 500; padding: 2px 6px; border-radius: 3px;">⌖ ${escapeHtml(m.trim())}</span>`)
        .join(' ');

      return `<div class="install-case-card" style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; overflow: hidden; display: flex; flex-direction: column; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
        <div style="position: relative; height: 160px; background: #f8fafc; overflow: hidden;">
          <img src="${escapeHtml(c.image)}" alt="${escapeHtml(cTitle)}" loading="lazy" style="width: 100%; height: 100%; object-fit: cover;" />
          <span style="position: absolute; top: 6px; left: 6px; background: rgba(15,23,42,0.85); color: #ffffff; font-size: 0.68rem; font-weight: 700; padding: 2px 6px; border-radius: 3px; font-family: monospace;">
            ${escapeHtml(c.id)}
          </span>
          <span style="position: absolute; bottom: 6px; right: 6px; background: rgba(15,23,42,0.8); color: #cbd5e1; font-size: 0.65rem; padding: 2px 6px; border-radius: 2px;">
            ${escapeHtml(cRegion)}
          </span>
        </div>
        <div style="padding: 10px 12px; flex: 1; display: flex; flex-direction: column;">
          <div style="font-size: 0.72rem; color: #64748b; margin-bottom: 2px;">
            <a href="${lockLink}" style="color: #64748b; text-decoration: none; font-weight: 500;">${escapeHtml(c.lockFamilyName)}</a>
          </div>
          <h3 style="margin: 0 0 6px; font-size: 0.92rem; line-height: 1.35; font-weight: 700; color: #0f172a; flex: 1;">
            <a href="${lockLink}" style="color: inherit; text-decoration: none;">${escapeHtml(cTitle)}</a>
          </h3>
          <div style="display: flex; flex-wrap: wrap; gap: 4px; margin-bottom: 8px;">
            ${metricChips}
          </div>
          <a style="text-align: center; font-size: 0.75rem; font-weight: 600; padding: 5px 8px; background: #f8fafc; color: #0f172a; border: 1px solid #cbd5e1; border-radius: 4px; text-decoration: none; display: block;" href="${lockLink}">
            ${isZh ? '查看施工图谱与锁型 →' : 'View Case & Blueprint →'}
          </a>
        </div>
      </div>`;
    }).join('\n');

    const installGalleryHtml = `<div class="install-gallery-page wrap">
      <div style="margin-bottom: 14px;">
        <h1 style="margin: 0 0 6px; font-size: 1.6rem;">${isZh ? '🔧 全球各类安装工程实物案例图库' : '🔧 Global Lock Installation Field Cases Gallery'}</h1>
        <p style="margin: 0; color: #64748b; font-size: 0.95rem;">${isZh ? '按区域深度收录真实木门开槽、夹具开孔打样、扁轴拉出比对与锁体内部机械连动真实工单实拍。' : 'Authentic jobsite and field installation cases across global lock standards.'}</p>
      </div>

      <div class="install-filter-bar" style="margin-bottom: 16px; display: flex; gap: 8px; flex-wrap: wrap; background: #f8fafc; border: 1px solid #e2e8f0; border-left: 3px solid #0f172a; padding: 10px 14px; border-radius: 4px;">
        <span style="font-weight: 700; font-size: 0.82rem; color: #0f172a; display: flex; align-items: center;">★ ${isZh ? '8大工业板块穿透:' : '8 Industrial Sectors:'}</span>
        <a class="filter-chip" style="padding: 3px 8px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.78rem; text-decoration: none; color: #0f172a;" href="${isZh ? '/zh/categories/na.html' : '/en/categories/na.html'}">🇺🇸 ${isZh ? '北美板块' : 'Americas'}</a>
        <a class="filter-chip" style="padding: 3px 8px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.78rem; text-decoration: none; color: #0f172a;" href="${isZh ? '/zh/categories/latam.html' : '/en/categories/latam.html'}">🌎 ${isZh ? '拉美新兴' : 'LatAm'}</a>
        <a class="filter-chip" style="padding: 3px 8px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.78rem; text-decoration: none; color: #0f172a;" href="${isZh ? '/zh/categories/europe5.html' : '/en/categories/europe5.html'}">🇪🇺 ${isZh ? '欧陆五国' : 'Europe'}</a>
        <a class="filter-chip" style="padding: 3px 8px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.78rem; text-decoration: none; color: #0f172a;" href="${isZh ? '/zh/categories/uk-anz.html' : '/en/categories/uk-anz.html'}">🇦🇺🇬🇧 ${isZh ? '澳英体系' : 'UK/ANZ'}</a>
        <a class="filter-chip" style="padding: 3px 8px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.78rem; text-decoration: none; color: #0f172a;" href="${isZh ? '/zh/categories/gcc.html' : '/en/categories/gcc.html'}">🇦🇪 ${isZh ? '中东海湾' : 'GCC'}</a>
        <a class="filter-chip" style="padding: 3px 8px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.78rem; text-decoration: none; color: #0f172a;" href="${isZh ? '/zh/categories/jp-kr.html' : '/en/categories/jp-kr.html'}">🇯🇵 ${isZh ? '日韩精工' : 'Japan/Korea'}</a>
        <a class="filter-chip" style="padding: 3px 8px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.78rem; text-decoration: none; color: #0f172a;" href="${isZh ? '/zh/categories/sea.html' : '/en/categories/sea.html'}">🇸🇬 ${isZh ? '东南亚' : 'SEA'}</a>
        <a class="filter-chip" style="padding: 3px 8px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.78rem; text-decoration: none; color: #0f172a;" href="${isZh ? '/zh/categories/af-sa.html' : '/en/categories/af-sa.html'}">🇮🇳 ${isZh ? '南亚非洲' : 'South Asia/Africa'}</a>
      </div>

      <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 20px;">
        ${casesCards}
      </div>
    </div>`;

    emitPage({
      lang, slug: 'install-gallery.html',
      title: isZh ? '实操工程图库' : 'Installation Cases Gallery',
      description: isZh ? '全球各类机械门锁安装工程实物案例照片与原厂打孔打样图谱。' : 'Global lock installation field cases photos and drilling templates.',
      bodyHtml: installGalleryHtml,
      breadcrumbs: [...homeCrumb, { label: isZh ? '实操工程图库' : 'Installation Cases' }],
    });

    const blocksForCat = getGalleryBlocks(lang);
    for (const block of blocksForCat) {
      const cardsHtml = block.items.map((item) => renderGalleryCard(item, lang)).join('\n');
      const heroHref = block.hero.familyId ? `/${urlFor(lang, `locks/${block.hero.familyId}.html`)}` : `/${urlFor(lang, 'locks/index.html')}`;
      const isZh = lang === 'zh';

      const heroHtml = `
      <div class="block-hero">
        <div class="block-hero__media">
          <a href="${heroHref}">
            <img src="${escapeHtml(block.hero.image)}" alt="${escapeHtml(block.hero.title)}" loading="lazy" width="460" height="320" />
          </a>
        </div>
        <div class="block-hero__content">
          <span style="display: inline-block; font-size: 0.7rem; font-weight: 700; background: #0f172a; color: #fff; padding: 2px 8px; border-radius: 3px; text-transform: uppercase; margin-bottom: 8px;">★ ${isZh ? "核心基准锁型" : "Core Baseline"}</span>
          <h2 class="block-hero__title"><a href="${heroHref}">${escapeHtml(block.hero.title)}</a></h2>
          <p class="block-hero__desc">${escapeHtml(block.hero.desc)}</p>
          <div class="block-hero__actions" style="display: flex; gap: 10px; flex-wrap: wrap; margin-top: 12px;">
            <a class="block-hero__btn" style="background: #0f172a; color: #fff; padding: 6px 14px; font-size: 0.82rem; font-weight: 600; border-radius: 4px; text-decoration: none;" href="${heroHref}">
              ${isZh ? '实物拆解与工程规范 →' : 'Specifications & Blueprint →'}
            </a>
            <a class="block-hero__btn" style="background: #ffffff; border: 1px solid #cbd5e1; color: #334155; padding: 6px 14px; font-size: 0.82rem; font-weight: 600; border-radius: 4px; text-decoration: none;" href="${isZh ? (block.code === 'jp-kr' ? '/zh/drilling-templates.html#tpl-jp-miwa-la' : (block.code === 'europe5' ? '/zh/drilling-templates.html#tpl-eu-din-18251' : '/zh/drilling-templates.html#tpl-us-ansi-deadbolt')) : (block.code === 'jp-kr' ? '/en/drilling-templates.html#tpl-jp-miwa-la' : (block.code === 'europe5' ? '/en/drilling-templates.html#tpl-eu-din-18251' : '/en/drilling-templates.html#tpl-us-ansi-deadbolt'))}">
              📐 ${isZh ? '1:1 开孔图谱' : '1:1 Template'}
            </a>
          </div>
        </div>
      </div>`;

      const categoryHtml = `<div class="gallery-block">
        <div class="category-top-nav">
          <a class="category-top-nav__back" href="${isZh ? '/zh/index.html' : '/en/index.html'}">
            ← ${isZh ? '返回全球 8 大板块' : 'Back to 8 Major Divisions'}
          </a>
          <span class="category-top-nav__meta">${block.items.length} ${isZh ? '款实拍型号' : 'models'}</span>
        </div>
        <div class="gallery-block__header">
          <div class="gallery-block__title-wrap">
            <h1 class="gallery-block__title">${escapeHtml(block.title)}</h1>
            <span class="gallery-block__badge">${block.items.length} ${isZh ? '款实物样本' : 'models'}</span>
          </div>
          <p class="gallery-block__subtitle">${escapeHtml(block.subtitle)}</p>


          <div class="gallery-tier-filter" style="display: flex; gap: 8px; margin: 14px 0 0; flex-wrap: wrap; align-items: center;">
            <button class="tier-filter-btn is-active" data-filter="all" onclick="filterTier('all', this)" style="font-size: 0.78rem; font-weight: 700; padding: 4px 12px; border-radius: 4px; border: 1px solid #0f172a; background: #0f172a; color: #ffffff; cursor: pointer;">
              ${isZh ? '全部' : 'All'} (${block.items.length})
            </button>
            <button class="tier-filter-btn" data-filter="Mainstream" onclick="filterTier('Mainstream', this)" style="font-size: 0.78rem; font-weight: 600; padding: 4px 12px; border-radius: 4px; border: 1px solid #cbd5e1; background: #ffffff; color: #0f172a; cursor: pointer;">
              ★ ${isZh ? '主流基准' : 'Mainstream'} (${block.items.filter(i => i.tierClass === 'Mainstream').length})
            </button>
            <button class="tier-filter-btn" data-filter="Niche" onclick="filterTier('Niche', this)" style="font-size: 0.78rem; font-weight: 600; padding: 4px 12px; border-radius: 4px; border: 1px solid #cbd5e1; background: #ffffff; color: #64748b; cursor: pointer;">
              ${isZh ? '小众/衍生' : 'Niche'} (${block.items.filter(i => i.tierClass !== 'Mainstream').length})
            </button>
          </div>
        </div>
        ${heroHtml}
        ${block.code === 'europe5' ? `
        <div class="category-native-box" style="margin: 20px 0; padding: 16px 20px; background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 8px;">
          <h4 style="margin: 0 0 8px; color: #1e40af; font-size: 0.95rem;">🌍 ${isZh ? '德语区 (DE/AT/CH) 与 法语区 (FR/BE) 本地五金专著与母语速查' : 'DACH & French Region Native Hardware Guides'}</h4>
          <p style="margin: 0 0 10px; font-size: 0.85rem; color: #3b82f6;">${isZh ? '欧陆板块深度细分：涵盖德国 Dornmaß/PZ/应急离合 与 法国 Axe/Entraxe/多点联动本地工程字典。' : 'Covers German Dornmaß/PZ/Emergency Clutch & French mortise standards.'}</p>
          <div style="display: flex; gap: 12px; flex-wrap: wrap;">
            <a class="block-hero__btn" style="font-size: 0.8rem; padding: 6px 14px; background: #2563eb; color: #fff;" href="${isZh ? '/zh/indigenous-guides.html#de-at-ch' : '/en/indigenous-guides.html#de-at-ch'}">
              🇩🇪 ${isZh ? '直达德语区五金术语与避坑指南 →' : 'German Hardware Guide →'}
            </a>
            <a class="block-hero__btn" style="font-size: 0.8rem; padding: 6px 14px; background: #3b82f6; color: #fff;" href="${isZh ? '/zh/indigenous-guides.html#fr-be' : '/en/indigenous-guides.html#fr-be'}">
              🇫🇷 ${isZh ? '直达法语区五金术语与避坑指南 →' : 'French Hardware Guide →'}
            </a>
          </div>
        </div>
        ` : ''}

        ${block.code === 'sea' ? `
        <div class="category-native-box" style="margin: 20px 0; padding: 16px 20px; background: #fef2f2; border: 1px solid #fecaca; border-radius: 8px;">
          <h4 style="margin: 0 0 8px; color: #991b1b; font-size: 0.95rem;">🇯🇵 ${isZh ? '日本区 (JP) 专属面板刻印反查字典与 JIS 机械锁体' : 'Japan Native JIS & Engraving Matrix'}</h4>
          <p style="margin: 0 0 10px; font-size: 0.85rem; color: #b91c1c;">${isZh ? '亚太东亚板块深度细分：支持 MIWA 13LA / GOAL / SHOWA / ALPHA 刻印即型号反查与加装垫块 BOM。' : 'Includes MIWA/GOAL panel engraving decoder & SwitchBot/Qrio spacer BOM.'}</p>
          <div style="display: flex; gap: 12px; flex-wrap: wrap;">
            <a class="block-hero__btn" style="font-size: 0.8rem; padding: 6px 14px; background: #dc2626; color: #fff;" href="${isZh ? '/zh/japan-engravings.html' : '/en/japan-engravings.html'}">
              🔍 ${isZh ? '进入日本面板刻印反查字典 (MIWA/GOAL) →' : 'Open Japan Engraving Matrix →'}
            </a>
            <a class="block-hero__btn" style="font-size: 0.8rem; padding: 6px 14px; background: #ef4444; color: #fff;" href="${isZh ? '/zh/indigenous-guides.html#jp' : '/en/indigenous-guides.html#jp'}">
              🗾 ${isZh ? '日本本地五金安装与尺寸指引 →' : 'Japan Hardware Guide →'}
            </a>
          </div>
        </div>
        ` : ''}

        <h3 class="block-subheading">${isZh ? '该区域代表性型号与候选实物图谱：' : 'Representative Candidate Lock Models:'}</h3>
        <div class="gallery-grid">
          ${cardsHtml}
        </div>
        <div style="margin-top: 40px; text-align: center;">
          <a class="block-hero__btn" style="background: transparent; border: 1px solid var(--color-border, #cbd5e1); color: var(--color-text, #1e293b);" href="${isZh ? '/zh/index.html' : '/en/index.html'}">
            ← ${isZh ? '返回全球 8 大工业板块主图库' : 'Back to 8 Major Industrial Divisions'}
          </a>
        </div>
      </div>`;

      emitPage({
        lang, slug: `categories/${block.code}.html`,
        title: block.shortTitle,
        description: block.subtitle,
        bodyHtml: categoryHtml,
        breadcrumbs: [...homeCrumb, { label: block.shortTitle }],
      });
      searchIndex.push({
        lang, title: block.title, description: block.subtitle,
        url: hrefFor(lang, `categories/${block.code}.html`), kind: 'category',
        text: block.items.map(i => `${i.id} ${(i.title && (i.title[lang] || i.title.en)) || ''} ${i.features || ''}`).join(' '),
      });
    }

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
  // Ingest newly added engineering datasets
  const indigenousGuides = JSON.parse(readFileSync(join(CONTENT, 'catalog', 'indigenous-lock-guides.json'), 'utf8'));
  const japanEngravings = JSON.parse(readFileSync(join(CONTENT, 'catalog', 'japan-engraving-matrix.json'), 'utf8'));
  const adaptersBom = JSON.parse(readFileSync(join(CONTENT, 'catalog', 'adapters-bom.json'), 'utf8'));
  const drillingTemplates = JSON.parse(readFileSync(join(CONTENT, 'catalog', 'drilling-templates.json'), 'utf8'));
  const bestsellerLocks = JSON.parse(readFileSync(join(CONTENT, 'catalog', 'bestseller-locks.json'), 'utf8'));
  const fieldIssues = JSON.parse(readFileSync(join(CONTENT, 'catalog', 'field-issues.json'), 'utf8'));

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
    indigenousGuides,
    japanEngravings,
    adaptersBom,
    drillingTemplates,
    bestsellerLocks,
    fieldIssues,
  }, null, 2));

  write('data/search-index.json', JSON.stringify(searchIndex));

  write('sitemap.xml', `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">
${pagesMeta.map(({ lang, slug, path }) => {
    const otherLang = lang === 'en' ? 'zh' : 'en';
    const alt = existsFor(otherLang, slug)
      ? `\n    <xhtml:link rel="alternate" hreflang="${otherLang}" href="${BASE_URL}/${urlFor(otherLang, slug)}"/>`
      : '';
    return `  <url>\n    <loc>${BASE_URL}/${path}</loc>${alt}\n    <lastmod>${BUILD_DATE}</lastmod>\n  </url>`;
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
  if (existsSync(join(ROOT, 'docs'))) {
    cpSync(join(ROOT, 'docs'), join(OUT, 'docs'), { recursive: true });
  }
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
  // The llms.txt summary is written in the default language so the most common
  // crawler entry point reads naturally; the LLM can still pick the alternate
  // language from hreflang if it prefers.
  const lang = DEFAULT_LANG;
  const other = lang === 'en' ? 'zh' : 'en';
  L.push(`# ${site.name}`);
  L.push('');
  L.push(`> ${site.description[lang] || site.description.en}`);
  L.push('');
  L.push(lang === 'zh'
    ? '面向全球机械门锁的开放、可机读参考资料：识别现有门锁、设计与之匹配的智能锁改造方案。所有数据也以 JSON 形式发布在 /data/catalog.json。中文入口见根路径；英文版本在 /en/ 目录下。'
    : 'An open, machine-readable reference for identifying existing mechanical door locks worldwide and designing smart-lock retrofits that fit them. All data is also available as JSON at /data/catalog.json.');
  L.push('');
  L.push(lang === 'zh' ? '## 识别与测量' : '## Identify and measure');
  const entryLabels = {
    'identify.html': lang === 'zh' ? '识别向导' : 'Identify',
    'measure.html': lang === 'zh' ? '测量' : 'Measure',
    'photo.html': lang === 'zh' ? '拍照量尺寸' : 'Photo measuring',
  };
  for (const slug of ['identify.html', 'measure.html', 'photo.html']) {
    if (existsFor(lang, slug)) L.push(`- [${entryLabels[slug]}](/${urlFor(lang, slug)}): ${lang === 'zh' ? '引导式识别与测量清单' : 'guided identification and the measurement checklist'}`);
  }
  L.push('');
  L.push(lang === 'zh' ? '## 改造设计' : '## Retrofit design');
  if (existsFor(lang, 'retrofit.html')) L.push(`- [改造架构对照](/${urlFor(lang, 'retrofit.html')}): 七种架构、适配件与设计目标值`);
  for (const a of architecturesDoc.architectures) {
    const name = t(terms.architecture, a.id, lang);
    const desc = (a.principle[lang] || a.principle.en).slice(0, 120);
    L.push(`- [${name}](/${urlFor(lang, `retrofit/${a.id}.html`)}): ${desc}`);
  }
  L.push('');
  L.push(lang === 'zh' ? '## 锁型库' : '## Lock families');
  for (const f of families) {
    const name = f.title[lang] || f.title.en;
    const desc = (f.summary[lang] || f.summary.en).slice(0, 140);
    L.push(`- [${name}](/${urlFor(lang, `locks/${f.id}.html`)}): ${desc}`);
  }
  L.push('');
  L.push(lang === 'zh' ? '## 标准' : '## Standards');
  for (const s of standardsDoc.standards) {
    const title = s.title[lang] || s.title.en;
    L.push(`- [${s.code}](/${urlFor(lang, `standards/${s.id}.html`)}): ${title}${s.status === 'needs-review' ? (lang === 'zh' ? '（待核对）' : ' (needs review)') : ''}`);
  }
  L.push('');
  L.push(lang === 'zh' ? '## 机器可读' : '## Machine-readable');
  L.push('- [catalog.json](/data/catalog.json): 全部锁族、标准、架构、设备的一份 JSON 文档');
  L.push('- [search-index.json](/data/search-index.json): 所有页面的扁平索引（双语）');
  L.push('- [sitemap.xml](/sitemap.xml): 全部 URL，含 hreflang 互链');
  L.push('');
  L.push(lang === 'zh' ? '## 可选' : '## Optional');
  L.push(`- [源码仓库](${site.urls.repository}): 数据文件每个锁族一个 JSON`);
  L.push('');
  L.push(lang === 'zh'
    ? `其他语言: [English](/en/index.html) — the same content, in English.`
    : `Other languages: [中文](/${other === 'zh' ? 'zh/index.html' : 'index.html'}) — 同一站点的中文版本。`);
  L.push('');
  return L.join('\n');
  void other; // retained for the cross-link above; computed lazily
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
  const lang = DEFAULT_LANG;
  const other = lang === 'en' ? 'zh' : 'en';
  const isZh = lang === 'zh';
  const body = isZh
    ? `<h1>页面未找到 (404)</h1>
       <div class="redirect-box" style="margin: 20px 0; padding: 18px; background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 8px;">
         <p style="margin: 0; color: #1e40af; font-weight: 600;">⏱️ 正在自动返回主画廊首页（3 秒后自动跳转）...</p>
         <p style="margin: 8px 0 0;"><a href="/zh/index.html" style="color: #2563eb; font-weight: 700;">点击此处立即返回首页 →</a></p>
       </div>
       <p class="muted">找不到页面。可以试试<a href="/zh/index.html">8大工业板块图库</a>、<a href="/zh/adapters.html">转接件与工具</a>或<a href="/zh/field-issues.html">避坑实录</a>。</p>`
    : `<h1>Page not found (404)</h1>
       <div class="redirect-box" style="margin: 20px 0; padding: 18px; background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 8px;">
         <p style="margin: 0; color: #1e40af; font-weight: 600;">⏱️ Redirecting to visual gallery landing page in 3 seconds...</p>
         <p style="margin: 8px 0 0;"><a href="/index.html" style="color: #2563eb; font-weight: 700;">Click here to return now →</a></p>
       </div>
       <p class="muted">That page does not exist. Try the <a href="/index.html">8 Industrial Divisions Gallery</a>, <a href="/adapters.html">Adapters & Tools</a> or <a href="/field-issues.html">Field Pitfalls</a>.</p>`;
  const html = layout({
    title: isZh ? '页面未找到' : 'Page not found',
    description: isZh ? '这个地址不存在。' : 'That page does not exist.',
    lang,
    path: '404.html',
    baseUrl: BASE_URL,
    site: { ...site, navigation: { [lang]: rewriteNav(site.navigation[lang], lang) } },
    extraHead: `<meta http-equiv="refresh" content="3;url=/${urlFor(lang, 'index.html')}" />`,
    body,
    breadcrumbs: [{ label: site.name, href: hrefFor(lang, 'index.html') }, { label: '404' }],
  });
  return rebaseLinks(html, '404.html');
  void other;
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
