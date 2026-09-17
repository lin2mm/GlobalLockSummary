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
      site: { ...site, navigation: { [lang]: rewriteNav(site.navigation[lang]) } },
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
        <div class="lock-detail-sample__tier3-header" style="background: #0f172a; color: #38bdf8; padding: 6px 12px; border-radius: 6px 6px 0 0; font-size: 0.8rem; font-weight: 700; display: flex; justify-content: space-between; align-items: center; margin-bottom: -1px;">
          <span>🔧 ${lang === 'zh' ? '第三层：真实安装案例与 1:1 改装打样图谱' : 'Tier 3: Real Field Installation Case & 1:1 Retrofit Blueprint'}</span>
          <span style="color: #cbd5e1; font-weight: normal; font-size: 0.72rem;">${lang === 'zh' ? '门上实态 + 原厂图纸对照' : 'Field Case + Factory Drawing'}</span>
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
        <div class="lock-detail-sample__steps-box" style="margin: 16px 0; padding: 14px 18px; background: #f8fafc; border-left: 4px solid #0284c7; border-radius: 4px;">
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
            <div style="background: #f1f5f9; padding: 5px 8px; border-radius: 4px; font-size: 0.72rem; color: #334155; border-left: 3px solid #0284c7;">
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
          <a class="block-hero__btn" style="font-size: 0.8rem; padding: 6px 12px; background: #0284c7; color: #fff;" href="${lang === 'zh' ? '/zh/install-gallery.html' : '/en/install-gallery.html'}">
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

  return [
    {
      code: 'na',
      title: isZh ? '🇺🇸 北美标准板块 (Americas — ANSI / BHMA)' : '🇺🇸 North America (Americas — ANSI / BHMA)',
      shortTitle: isZh ? '北美标准板块' : 'North America',
      subtitle: isZh ? '全球存量最大的智能锁加装市场 · 标准 54mm 大孔位、单插销死锁 (Deadbolt) 与 60/70mm 标准背距' : 'World largest retrofit market · Standard 54mm bore, deadbolt & 60/70mm backset',
      hero: {
        title: isZh ? '核心改装基准：美标单缸插销死锁 (ANSI Deadbolt / Schlage B60)' : 'Core Retrofit Baseline: ANSI Single-Cylinder Deadbolt (Schlage B60)',
        desc: isZh ? 'August 与 SwitchBot 的全球基本盘。标准扁平尾轴（Tailpiece）直接啮合；改造核心难点在于门扇下沉与密封条导致插销与扣板卡阻。' : 'Core baseline for August & SwitchBot. Flat tailpiece interface; key challenge is sag binding.',
        image: '/assets/img/hero/hero-na-deadbolt.png',
        familyId: 'us-deadbolt',
        tag: isZh ? '⭐ 极强相关 · 改装第一基准' : '⭐ Core Retrofit Baseline'
      },
      items: items.filter(i => i.block === 'na')
    },
    {
      code: 'europe5',
      title: isZh ? '🇪🇺 欧陆五国板块 (Continental Europe — DIN / EN)' : '🇪🇺 Continental Europe (DIN / EN)',
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
      title: isZh ? '🇦🇺🇬🇧 澳洲与英国板块 (Pacific & UK — AS / BS)' : '🇦🇺🇬🇧 Australia, NZ & UK (Pacific & UK — AS / BS)',
      shortTitle: isZh ? '澳洲与英国板块' : 'Australia, NZ & UK',
      subtitle: isZh ? '英联邦经典五金体系 · 澳式外装夜锁 (Lockwood 001/002)、双扣死锁 (355)、英标 5 拨杆防盗锁 (BS 3621)' : 'Commonwealth hardware · Lockwood deadlatches, 355 deadlocks & UK 5-lever mortice sets',
      hero: {
        title: isZh ? '核心改装基准：澳式外装夜锁与双扣锁 (Lockwood 001 / 355)' : 'Core Retrofit Baseline: Australian Deadlatch & Deadlock (Lockwood 001 / 355)',
        desc: isZh ? '大洋洲存量最大防盗锁。内侧带旋转大旋钮；死穴在于辅助锁舌（Auxiliary Latch）必须完全压入扣板，否则旋钮转动主舌并未死锁。' : 'Australia major lock. Large interior turn; auxiliary latch must fully compress for deadlatch.',
        image: '/assets/img/hero/hero-anz-lockwood001.jpg',
        familyId: 'au-deadlatch',
        tag: isZh ? '⭐ 强相关 · 澳标第一基准' : '⭐ Core ANZ Baseline'
      },
      items: items.filter(i => i.block === 'uk-anz')
    },
    {
      code: 'sea',
      title: isZh ? '🇸🇬 东南亚与东亚板块 (Asia-Pacific — 铁闸与推拉锁)' : '🇸🇬 Southeast Asia & East Asia (Asia-Pacific)',
      shortTitle: isZh ? '东南亚与东亚板块' : 'Southeast Asia & East Asia',
      subtitle: isZh ? '极端净距与数字存量市场 · 新加坡 HDB 金属双门铁闸碰撞风险 (<80mm) 与早期推拉整锁边界样本' : 'Extreme clearances & digital stock · Singapore HDB gate clash (<80mm) & push-pull mortise',
      hero: {
        title: isZh ? '核心改装基准：新加坡 HDB 金属防盗双门铁闸锁' : 'Core Retrofit Baseline: Singapore HDB Metal Security Gate Lock',
        desc: isZh ? '东南亚代表性双门结构。外铁闸与内木门净距普遍小于 80mm，智能锁厚度超过 35mm 即发生把手致命撞击。' : 'Key SE Asia structure. Gap under 80mm; lock thickness >35mm causes severe gate handle collision.',
        image: '/assets/img/hero/hero-sea-hdb.jpg',
        familyId: 'sg-metal-gate-lock',
        tag: isZh ? '⚠️ 极限净距边界基准' : '⚠️ Extreme Clearance'
      },
      items: items.filter(i => i.block === 'sea')
    },
    {
      code: 'latam',
      title: isZh ? '🌎 拉美新兴板块 (Latin America — ABNT / ODIS)' : '🌎 Latin America & Emerging (ABNT / ODIS)',
      shortTitle: isZh ? '拉美新兴板块' : 'Latin America',
      subtitle: isZh ? '拉美大容量新兴五金体系 · 巴西 ABNT 窄背距插芯锁 (40/45mm)、薄门扇 (30mm) 与安第斯重型外装双钩锁' : 'Emerging market hardware · Brazil ABNT narrow backset (40/45mm) & heavy-duty rim locks',
      hero: {
        title: isZh ? '核心改装基准：巴西 ABNT NBR 14913 极窄背距插芯锁' : 'Core Retrofit Baseline: Brazil ABNT Narrow Mortise (La Fonte / Silvana)',
        desc: isZh ? '拉美大容量存量。背距仅 40/45mm，门扇厚仅 30mm，电机回转半径稍大即撞击门框防风条。' : 'Latin America high volume. Backset 40/45mm; thin 30mm door; motor radius must be strictly bounded.',
        image: '/assets/img/hero/hero-latam-abnt.webp',
        familyId: 'euro-cylinder-mortise',
        tag: isZh ? '⚠️ 窄背距与薄门基准' : '⚠️ Narrow Backset'
      },
      items: items.filter(i => i.block === 'latam')
    }
  ];
}

function renderGalleryCard(item, lang) {
  const isZh = lang === 'zh';
  const title = (item.title && (item.title[lang] || item.title.en || item.title.zh)) || item.id;
  const regionLabel = item.region || '';
  const statusClass = item.status === 'R1' ? 'gallery-card__status--r1' : (item.status === 'R2' ? 'gallery-card__status--r2' : 'gallery-card__status--r0');
  const statusText = item.status || 'R0';
  const statusTip = item.status === 'R1' 
    ? (isZh ? 'R1 优先推荐测试' : 'R1 Feasible')
    : (item.status === 'R2' ? (isZh ? 'R2 需实测再宣传' : 'R2 Test First') : (isZh ? 'R0 边界样本 / 特殊锁体' : 'R0 Boundary'));

  const searchText = `${item.id} ${title} ${regionLabel} ${item.features || ''}`.toLowerCase();
  const hasFamily = !!item.familyId;
  const familyHref = hasFamily ? `/${urlFor(lang, `locks/${item.familyId}.html`)}` : `/${urlFor(lang, 'locks/index.html')}`;

  const sceneImg = item.sceneImage || item.image;
  const productImg = item.productImage || item.image;
  const score = item.selectionScore ? item.selectionScore.overallScore : 88;
  const ctrWeight = item.selectionScore ? item.selectionScore.estimatedCtrWeight : '0.88';

  return `<div class="gallery-card" data-gallery-card data-region="${escapeHtml(item.block)}" data-search-text="${escapeHtml(searchText)}">
    <div class="gallery-card__dual-views">
      <div class="gallery-card__view-tab" style="display: flex; justify-content: space-between; font-size: 0.72rem; padding: 5px 8px; background: #0f172a; color: #f8fafc; border-bottom: 1px solid #334155; font-weight: 600;">
        <span style="color: #38bdf8;">🏷️ ${isZh ? '第二层：类别画廊' : 'Tier 2: Category Gallery'}</span>
        <span style="color: #94a3b8;">${isZh ? '门上实景与机械总成对照' : 'Scene + Product Dual View'}</span>
      </div>
      <div class="gallery-card__dual-img-container" style="display: grid; grid-template-columns: 1fr 1fr; background: #f1f5f9; gap: 2px; position: relative;">
        <a class="gallery-card__img-link" href="${familyHref}" title="${isZh ? '门上场景实景图' : 'Scene View'}" style="position: relative; display: block; overflow: hidden; height: 160px; background: #000;">
          <img class="gallery-card__img" src="${escapeHtml(sceneImg)}" alt="${escapeHtml(title)} 门上场景" loading="lazy" style="width: 100%; height: 100%; object-fit: cover;" />
          <span style="position: absolute; bottom: 4px; left: 4px; background: rgba(15, 23, 42, 0.85); color: #fff; font-size: 0.65rem; padding: 2px 5px; border-radius: 3px;">🏠 ${isZh ? '场景图' : 'Scene'}</span>
        </a>
        <a class="gallery-card__img-link" href="${familyHref}" title="${isZh ? '锁体产品剖面/原理图' : 'Product Blueprint View'}" style="position: relative; display: block; overflow: hidden; height: 160px; background: #fff;">
          <img class="gallery-card__img" src="${escapeHtml(productImg)}" alt="${escapeHtml(title)} 锁体产品剖面" loading="lazy" style="width: 100%; height: 100%; object-fit: contain; padding: 4px;" />
          <span style="position: absolute; bottom: 4px; right: 4px; background: rgba(2, 132, 199, 0.85); color: #fff; font-size: 0.65rem; padding: 2px 5px; border-radius: 3px;">📐 ${isZh ? '产品图' : 'Product'}</span>
        </a>
        <div class="gallery-card__badges" style="position: absolute; top: 6px; left: 6px; right: 6px; display: flex; justify-content: space-between; pointer-events: none;">
          <span class="gallery-card__id">${escapeHtml(item.id)}</span>
          <span class="gallery-card__score" style="background: #fef08a; color: #854d0e; padding: 2px 6px; border-radius: 4px; font-weight: 700; font-size: 0.72rem; box-shadow: 0 1px 3px rgba(0,0,0,0.2);">⭐ ${score}分</span>
          <span class="gallery-card__status ${statusClass}" title="${escapeHtml(statusTip)}">${escapeHtml(statusText)}</span>
        </div>
      </div>
    </div>
    <div class="gallery-card__body">
      <div class="gallery-card__region-row" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
        <span class="gallery-card__region">${escapeHtml(regionLabel)}</span>
        <span class="gallery-card__ctr-tag" style="font-size: 0.7rem; color: #ea580c; font-weight: 700;">🔥 检索权重 ${ctrWeight}</span>
      </div>
      <h3 class="gallery-card__title">
        <a href="${familyHref}">${escapeHtml(title)}</a>
      </h3>
      <p class="gallery-card__desc" style="font-size: 0.8rem; color: #64748b; line-height: 1.4; margin: 4px 0 8px;">${escapeHtml(item.features || '')}</p>
      <div class="gallery-card__footer">
        <a class="gallery-card__link" href="${familyHref}">
          <span>${isZh ? '进入第三层：安装工序与开孔打样' : 'Tier 3: Installation & Templates'}</span>
          <span class="gallery-card__arrow">→</span>
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
    return `<a class="gallery-portal-card" href="${categoryUrl}" data-portal-target="${escapeHtml(b.code)}">
      <div class="gallery-portal-card__tier-tag" style="background: #0f172a; color: #38bdf8; font-size: 0.72rem; font-weight: 700; padding: 4px 10px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #334155;">
        <span>🌐 ${isZh ? '第一层：工业板块主入口' : 'Tier 1: Major Division Entry'}</span>
        <span style="color: #cbd5e1; font-weight: normal;">${isZh ? '主流场景实景' : 'Scene HD'}</span>
      </div>
      <div class="gallery-portal-card__media" style="position: relative;">
        <img class="gallery-portal-card__img" src="${escapeHtml(b.hero.image)}" alt="${escapeHtml(b.title)}" loading="lazy" width="360" height="220" />
        <span class="gallery-portal-card__badge">${b.items.length} ${isZh ? '款实拍样本' : 'models'}</span>
        <span class="gallery-portal-card__keyhint" title="${isZh ? '按键盘数字键快速直达' : 'Press key to navigate'}">[${idxBadge}]</span>
        <span class="gallery-portal-card__scene-badge" style="position: absolute; bottom: 8px; left: 8px; background: rgba(15, 23, 42, 0.85); color: #f8fafc; font-size: 0.7rem; padding: 3px 8px; border-radius: 4px; backdrop-filter: blur(4px);">
          📷 ${isZh ? '本国第一主流门锁实景图' : 'National Standard Door Scene'}
        </span>
      </div>
      <div class="gallery-portal-card__body">
        <h2 class="gallery-portal-card__name">${escapeHtml(b.title)}</h2>
        <div class="gallery-portal-card__baseline" style="color: #0369a1; font-weight: 600;">🔑 ${escapeHtml(b.hero.title.replace(/^[^：:]*[：:]/, ''))}</div>
        <div class="gallery-portal-card__action">
          <span class="portal-icon portal-icon--locked">🔒</span>
          <span class="portal-icon portal-icon--unlocked">🔓</span>
          <span>${isZh ? '进入第二层：场景与产品图库' : 'Tier 2: Scene + Product Gallery'} →</span>
        </div>
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
    for (const b of ['na', 'europe5', 'uk-anz', 'sea', 'latam']) register(lang, `categories/${b}.html`);
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
      const bodyHtmlContent = isHomePage ? html : `<h1>${escapeHtml(title)}</h1>\n${html}`;

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

      return `<div class="install-case-card" style="background: var(--color-surface, #fff); border: 1px solid var(--color-border, #cbd5e1); border-radius: 8px; overflow: hidden; display: flex; flex-direction: column; box-shadow: 0 2px 6px rgba(0,0,0,0.04);">
        <div style="position: relative; height: 220px; background: #000; overflow: hidden;">
          <img src="${escapeHtml(c.image)}" alt="${escapeHtml(cTitle)}" loading="lazy" style="width: 100%; height: 100%; object-fit: cover;" />
          <span style="position: absolute; top: 8px; left: 8px; background: rgba(15,23,42,0.85); color: #38bdf8; font-size: 0.72rem; font-weight: 700; padding: 3px 8px; border-radius: 4px;">
            ${escapeHtml(c.id)} · ${escapeHtml(c.sceneType)}
          </span>
          <span style="position: absolute; bottom: 8px; right: 8px; background: rgba(0,0,0,0.7); color: #fff; font-size: 0.7rem; padding: 2px 6px; border-radius: 3px;">
            ${escapeHtml(cRegion)}
          </span>
        </div>
        <div style="padding: 16px; flex: 1; display: flex; flex-direction: column;">
          <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: #64748b; margin-bottom: 6px;">
            <span>${isZh ? '所属锁族:' : 'Family:'} <a href="${lockLink}" style="font-weight: 700; color: #0284c7;">${escapeHtml(c.lockFamilyName)}</a></span>
            <span><a href="${catLink}" style="color: #64748b;">${escapeHtml(cRegion)} ${isZh ? '图库' : 'Gallery'} →</a></span>
          </div>
          <h3 style="margin: 0 0 8px; font-size: 1.05rem; line-height: 1.4;">${escapeHtml(cTitle)}</h3>
          <p style="font-size: 0.85rem; color: #475569; line-height: 1.5; margin: 0 0 12px; flex: 1;">${escapeHtml(cDesc)}</p>
          <div style="background: #f8fafc; border-left: 3px solid #0284c7; padding: 6px 10px; font-size: 0.78rem; color: #334155; margin-bottom: 12px;">
            ⚙️ <b>${isZh ? '工程关键指标:' : 'Key Metrics:'}</b> ${escapeHtml(c.keyMetrics)}
          </div>
          <div style="display: flex; gap: 8px;">
            <a class="block-hero__btn" style="flex: 1; text-align: center; font-size: 0.8rem; padding: 6px 10px;" href="${lockLink}">
              ${isZh ? '进入所属锁型详情 →' : 'View Lock Details →'}
            </a>
            <a class="block-hero__btn" style="background: transparent; border: 1px solid #cbd5e1; color: #1e293b; font-size: 0.8rem; padding: 6px 10px;" href="${catLink}">
              ${isZh ? '本区域图库' : 'Regional Gallery'}
            </a>
          </div>
        </div>
      </div>`;
    }).join('\n');

    const installGalleryHtml = `<div class="install-gallery-page wrap">
      <div style="margin-bottom: 24px;">
        <h1 style="margin: 0 0 8px;">${isZh ? '🔧 全球各类安装工程实物案例图库' : '🔧 Global Lock Installation Field Cases Gallery'}</h1>
        <p style="margin: 0; color: #64748b; font-size: 0.95rem;">${isZh ? '按区域深度收录真实木门开槽、夹具开孔打样、扁轴拉出比对与锁体内部机械连动真实工单实拍。' : 'Authentic jobsite and field installation cases across global lock standards.'}</p>
      </div>

      <div class="install-filter-bar" style="margin-bottom: 20px; display: flex; gap: 8px; flex-wrap: wrap; background: #f1f5f9; padding: 10px 14px; border-radius: 8px;">
        <span style="font-weight: 700; font-size: 0.85rem; color: #334155; display: flex; align-items: center;">📍 ${isZh ? '区域快速穿透:' : 'Quick Navigation:'}</span>
        <a class="filter-chip" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;" href="${isZh ? '/zh/categories/na.html' : '/en/categories/na.html'}">🇺🇸 ${isZh ? '北美板块 (6款)' : 'North America (6)'}</a>
        <a class="filter-chip" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;" href="${isZh ? '/zh/categories/europe5.html' : '/en/categories/europe5.html'}">🇪🇺 ${isZh ? '欧陆五国 (8款)' : 'Continental Europe (8)'}</a>
        <a class="filter-chip" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;" href="${isZh ? '/zh/categories/uk-anz.html' : '/en/categories/uk-anz.html'}">🇦🇺🇬🇧 ${isZh ? '澳英板块 (10款)' : 'Australia & UK (10)'}</a>
        <a class="filter-chip" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;" href="${isZh ? '/zh/categories/sea.html' : '/en/categories/sea.html'}">🇸🇬 ${isZh ? '东南亚/东亚 (10款)' : 'Southeast Asia (10)'}</a>
        <a class="filter-chip" style="padding: 4px 10px; background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.8rem; text-decoration: none; color: #1e293b;" href="${isZh ? '/zh/categories/latam.html' : '/en/categories/latam.html'}">🌎 ${isZh ? '拉美新兴 (4款)' : 'Latin America (4)'}</a>
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
          <span class="block-hero__tag">${escapeHtml(block.hero.tag)}</span>
          <h2 class="block-hero__title"><a href="${heroHref}">${escapeHtml(block.hero.title)}</a></h2>
          <p class="block-hero__desc">${escapeHtml(block.hero.desc)}</p>
          <div class="block-hero__actions" style="display: flex; gap: 10px; flex-wrap: wrap; margin-top: 12px;">
            <a class="block-hero__btn" href="${heroHref}">${isZh ? '进入该基准锁实物拆解与工程规范 →' : 'Enter Core Baseline Specs & Photos →'}</a>
            <a class="block-hero__btn" style="background: transparent; border: 1px solid var(--color-border, #cbd5e1); color: var(--color-text, #1e293b);" href="${isZh ? '/zh/drilling-templates.html' : '/en/drilling-templates.html'}">
              📐 ${isZh ? '获取 1:1 开孔打样工程模板' : '1:1 Drilling Templates'}
            </a>
          </div>
        </div>
      </div>`;

      const categoryHtml = `<div class="gallery-block">
        <div class="category-top-nav">
          <a class="category-top-nav__back" href="${isZh ? '/zh/index.html' : '/en/index.html'}">
            ← ${isZh ? '返回全球 5 大板块' : 'Back to 5 Major Divisions'}
          </a>
          <span class="category-top-nav__meta">${block.items.length} ${isZh ? '款实拍型号' : 'models'}</span>
        </div>
        <div class="gallery-block__header">
          <div class="gallery-block__title-wrap">
            <h1 class="gallery-block__title">${escapeHtml(block.title)}</h1>
            <span class="gallery-block__badge">${block.items.length} ${isZh ? '类实物样本' : 'models'}</span>
          </div>
          <p class="gallery-block__subtitle">${escapeHtml(block.subtitle)}</p>
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
            ← ${isZh ? '返回全球 5 大板块主图库' : 'Back to 5 Major Area Gallery'}
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
       <p class="muted">找不到页面。可以试试<a href="/zh/index.html">5大板块图库</a>、<a href="/zh/adapters.html">转接件与工具</a>或<a href="/zh/field-issues.html">避坑实录</a>。</p>`
    : `<h1>Page not found (404)</h1>
       <div class="redirect-box" style="margin: 20px 0; padding: 18px; background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 8px;">
         <p style="margin: 0; color: #1e40af; font-weight: 600;">⏱️ Redirecting to visual gallery landing page in 3 seconds...</p>
         <p style="margin: 8px 0 0;"><a href="/index.html" style="color: #2563eb; font-weight: 700;">Click here to return now →</a></p>
       </div>
       <p class="muted">That page does not exist. Try the <a href="/index.html">5 Divisions Gallery</a>, <a href="/adapters.html">Adapters & Tools</a> or <a href="/field-issues.html">Field Pitfalls</a>.</p>`;
  const html = layout({
    title: isZh ? '页面未找到' : 'Page not found',
    description: isZh ? '这个地址不存在。' : 'That page does not exist.',
    lang,
    path: '404.html',
    baseUrl: BASE_URL,
    site: { ...site, navigation: { [lang]: rewriteNav(site.navigation[lang]) } },
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
