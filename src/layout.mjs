/**
 * Page shell: <head> metadata, navigation, breadcrumbs, JSON-LD, footer.
 * Everything an AI crawler or a search engine needs lives here.
 */

const SITE_URL = 'https://globallocksummary.org'; // replaced when a domain is bound; Pages URL used until then

function esc(value) {
  return String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function jsonLd(obj) {
  return `<script type="application/ld+json">${JSON.stringify(obj, null, 2)}</script>`;
}

/**
 * @param {object} opts
 * @param {string} opts.title
 * @param {string} opts.description
 * @param {string} opts.lang         BCP-47, e.g. "en" or "zh"
 * @param {string} opts.path         URL path relative to site root, e.g. "identify.html"
 * @param {string} opts.baseUrl      Absolute base URL for this deployment
 * @param {object} opts.site         Site config from content/site.json
 * @param {string} opts.body         Already-rendered inner HTML
 * @param {Array}  [opts.breadcrumbs]
 * @param {Array}  [opts.alternates]  [{lang, path}] for hreflang
 * @param {Array}  [opts.jsonLdBlocks]
 * @param {string} [opts.extraHead]
 * @param {string} [opts.toc]
 */
export function layout(opts) {
  const {
    title, description, lang = 'en', path, baseUrl, site, body,
    breadcrumbs = [], alternates = [], jsonLdBlocks = [], extraHead = '', toc = '',
  } = opts;

  const url = `${baseUrl}/${path}`.replace(/([^:])\/{2,}/g, '$1/');
  const nav = (site.navigation[lang] || site.navigation.en || []).map((item) => {
    const href = item.href.split('#')[0].replace(/^\/+/, '');
    const active = href === path || (path.endsWith('/') && `${href}index.html` === path)
      ? ' aria-current="page"' : '';
    const icon = item.iconSvg ? `<span class="nav__icon-wrap" style="display: inline-flex; align-items: center; justify-content: center; margin-right: 6px; opacity: 0.85;">${item.iconSvg}</span>` : '';
    
    if (item.subItems && item.subItems.length > 0) {
      const subMenuHtml = item.subItems.map(sub => 
        `<a class="nav__sub-link" href="${esc(sub.href)}" style="display: block; padding: 7px 14px; font-size: 0.82rem; color: #334155; text-decoration: none; border-bottom: 1px solid #f1f5f9; white-space: nowrap; transition: background 0.15s;">${esc(sub.label)}</a>`
      ).join('');

      return `<div class="nav__dropdown" style="position: relative; display: inline-flex; align-items: center;">
        <a class="nav__link" href="${esc(item.href)}"${active} style="display: inline-flex; align-items: center;">
          ${icon}<span>${esc(item.label)}</span>
          <span style="font-size: 0.65rem; margin-left: 4px; opacity: 0.6;">▼</span>
        </a>
        <div class="nav__dropdown-menu" style="position: absolute; top: 100%; left: 0; min-width: 220px; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); display: none; z-index: 1000; padding: 4px 0;">
          ${subMenuHtml}
        </div>
      </div>`;
    }

    return `<a class="nav__link" href="${esc(item.href)}"${active} style="display: inline-flex; align-items: center;">${icon}<span>${esc(item.label)}</span></a>`;
  }).join('\n          ');

  const product = site.product && site.product.url
    ? {
        url: site.product.url,
        label: site.product.label?.[lang] || site.product.label?.en || '',
        note: site.product.note?.[lang] || site.product.note?.en || '',
      }
    : null;

  const feedbackTerms = site.feedback || {};
  const feedbackI18n = {
    title: feedbackTerms.title?.[lang] || feedbackTerms.title?.en || 'Engineer feedback',
    hint: feedbackTerms.hint?.[lang] || feedbackTerms.hint?.en || '',
    category: feedbackTerms.category?.[lang] || feedbackTerms.category?.en || 'Feedback type',
    categories: Object.fromEntries(Object.entries(feedbackTerms.categories || {}).map(([key, value]) => [key, value[lang] || value.en || key])),
    message: feedbackTerms.message?.[lang] || feedbackTerms.message?.en || 'Message',
    messagePlaceholder: feedbackTerms.messagePlaceholder?.[lang] || feedbackTerms.messagePlaceholder?.en || '',
    contact: feedbackTerms.contact?.[lang] || feedbackTerms.contact?.en || 'Contact (optional)',
    contactPlaceholder: feedbackTerms.contactPlaceholder?.[lang] || feedbackTerms.contactPlaceholder?.en || '',
    submit: feedbackTerms.submit?.[lang] || feedbackTerms.submit?.en || 'Submit feedback',
    submitting: feedbackTerms.submitting?.[lang] || feedbackTerms.submitting?.en || 'Submitting...',
    submitted: feedbackTerms.submitted?.[lang] || feedbackTerms.submitted?.en || 'Submitted! ID: ',
    submitFailed: feedbackTerms.submitFailed?.[lang] || feedbackTerms.submitFailed?.en || 'Submission failed. Please copy text.',
    tooShort: feedbackTerms.tooShort?.[lang] || feedbackTerms.tooShort?.en || 'Please enter at least 3 characters',
    openIssue: feedbackTerms.openIssue?.[lang] || feedbackTerms.openIssue?.en || 'Open GitHub issue',
    copy: feedbackTerms.copy?.[lang] || feedbackTerms.copy?.en || 'Copy feedback',
    copied: feedbackTerms.copied?.[lang] || feedbackTerms.copied?.en || 'Copied',
    note: feedbackTerms.note?.[lang] || feedbackTerms.note?.en || '',
  };
  const feedbackData = JSON.stringify(feedbackI18n).replace(/'/g, '&#39;');
  const feedback = `<section class="feedback feedback--ultra-clean" id="feedback" data-feedback
    data-page-title="${esc(title)}" data-page-path="${esc(path)}" data-issues-url="${esc(site.urls.issues)}"
    data-i18n='${feedbackData}'>
    <div class="feedback__ultra-form">
      <div class="feedback__input-cluster">
        <input type="text" class="feedback__direct-input" data-feedback-message placeholder="${lang === 'zh' ? '输入您的锁型需求或改装建议（支持直接输入，站内直达）...' : 'Type your suggestion or missing lock model...'}" aria-label="Feedback" />
        <button class="feedback__direct-submit" data-feedback-submit type="button">${lang === 'zh' ? '提交建议' : 'Submit Suggestion'}</button>
      </div>
      <div class="feedback__status-row">
        <span class="feedback__status-pill">⚡ ${lang === 'zh' ? '免登录 · 站内直达工程师' : 'Direct to Engineers'}</span>
        <button class="feedback__copy" data-feedback-copy type="button" style="display:none;">${esc(feedbackI18n.copy)}</button>
        <select data-feedback-category style="display:none;"></select>
        <input type="text" data-feedback-contact style="display:none;" />
        <a class="feedback__issue" data-feedback-issue href="${esc(site.urls.issues)}/new" target="_blank" rel="noopener" style="display:none;"></a>
        <span class="feedback__status" data-feedback-status aria-live="polite"></span>
      </div>
    </div>
  </section>`;

  const langLinks = alternates.map((alt) => {
    const label = site.languages[alt.lang]?.label || alt.lang;
    const isCurrent = alt.lang === lang;
    return `<a class="langswitch__link${isCurrent ? ' is-current' : ''}" href="${esc(alt.href)}" lang="${esc(alt.lang)}" hreflang="${esc(alt.lang)}"${isCurrent ? ' aria-current="true"' : ''}>${esc(label)}</a>`;
  }).join('\n          ');

  const crumbs = breadcrumbs.length
    ? `<nav class="breadcrumbs" aria-label="Breadcrumb"><ol>${breadcrumbs
        .map((c, idx) => (idx === breadcrumbs.length - 1
          ? `<li aria-current="page">${esc(c.label)}</li>`
          : `<li><a href="${esc(c.href)}">${esc(c.label)}</a></li>`))
        .join('')}</ol></nav>`
    : '';

  const ldBlocks = [{
    '@context': 'https://schema.org',
    '@type': 'WebSite',
    name: site.name,
    description: site.description[lang] || site.description.en,
    url,
    inLanguage: lang,
    license: site.license,
  }]
    .concat(jsonLdBlocks.filter(Boolean))
    .map(jsonLd)
    .join('\n  ');

  return `<!doctype html>
<html lang="${esc(lang)}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>${esc(title)}</title>
  <meta name="description" content="${esc(description)}">
  <link rel="canonical" href="${esc(url)}">
${alternates.map((a) => `  <link rel="alternate" hreflang="${esc(a.lang)}" href="${esc(a.href.startsWith('http') ? a.href : baseUrl + '/' + a.href)}">`).join('\n')}
  <meta property="og:type" content="website">
  <meta property="og:title" content="${esc(title)}">
  <meta property="og:description" content="${esc(description)}">
  <meta property="og:url" content="${esc(url)}">
  <meta property="og:site_name" content="${esc(site.name)}">
  <meta name="twitter:card" content="summary">
  <meta name="robots" content="index,follow,max-image-preview:large">
  <meta name="generator" content="GlobalLockSummary build">
  <link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="/assets/css/site.css">
  <link rel="alternate" type="application/json" title="Machine-readable lock catalog" href="/data/catalog.json">
  <link rel="sitemap" type="application/xml" href="/sitemap.xml">
  ${extraHead}
  ${ldBlocks}
</head>
<body>
  <a class="skip-link" href="#main">${esc(site.ui.skipToContent[lang] || 'Skip to content')}</a>
  <header class="site-header">
    <div class="wrap site-header__inner">
      <a class="brand" href="/${lang === 'en' ? '' : lang + '/'}">
        <svg class="brand__mark" viewBox="0 0 24 24" aria-hidden="true" focusable="false" style="width: 1.65rem; height: 1.65rem;">
          <defs>
            <linearGradient id="brandMarkGrad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#0284c7"/>
              <stop offset="100%" stop-color="#0f172a"/>
            </linearGradient>
          </defs>
          <!-- 硬化合金粗锁梁 (High-Contrast Bold Shackle) - 顶部负空间通透 -->
          <path d="M7 10V6.5C7 3.74 9.24 1.5 12 1.5C14.76 1.5 17 3.74 17 6.5V10" fill="none" stroke="#0284c7" stroke-width="2.6" stroke-linecap="round"/>
          <!-- 工业防撬切角锁身 (Precision Hex Chassis) -->
          <path d="M4 10.5C4 9.67 4.67 9 5.5 9H18.5C19.33 9 20 9.67 20 10.5V19.5C20 20.88 18.88 22 17.5 22H6.5C5.12 22 4 20.88 4 19.5V10.5Z" fill="url(#brandMarkGrad)"/>
          <!-- 极大光学负空间钥匙孔 (High-Visibility Classic Keyhole: Circle + Tapered Slot) 即使在12px下也清晰可辨 -->
          <circle cx="12" cy="14" r="2.2" fill="#ffffff"/>
          <path d="M10.9 14.5L10.2 19H13.8L13.1 14.5Z" fill="#ffffff"/>
        </svg>
        <span class="brand__text">${esc(site.name)}</span>
      </a>
            <div class="site-header__pulse-wrap" style="margin-left: auto; display: flex; align-items: center; gap: 8px;">
        <a href="/docs/AUTONOMOUS_OPTIMIZATION_LOOP.md" class="pulse-badge" title="${lang === 'zh' ? '自主巡航守护进程持续运行中 (点击查看实时运行日志)' : 'Autonomous Evolution Daemon Active (Click for live log)'}">
          <span class="pulse-dot"></span>
          <span class="pulse-text">${lang === 'zh' ? '自主进化守护中' : 'Daemon Active'}</span>
        </a>
      </div>
    <nav class="nav" aria-label="Main">
          ${nav}
      </nav>
      <div class="site-header__actions">
        ${product ? `<a class="product-link" href="${esc(product.url)}" rel="external noopener">${esc(product.label)}</a>` : ''}
        <a class="icon-link" href="/search.html" aria-label="${esc(site.ui.search[lang] || 'Search')}">${esc(site.ui.search[lang] || 'Search')}</a>
        <div class="langswitch">${langLinks}</div>
      </div>
    </div>
  </header>

  <main id="main" class="wrap page">
    ${crumbs}
    ${toc ? `<div class="page__grid"><article class="page__body">\n${body}\n</article><aside class="toc" aria-label="On this page"><p class="toc__title">${esc(site.ui.onThisPage[lang] || 'On this page')}</p><nav>${toc}</nav></aside></div>`
         : `<article class="page__body">\n${body}\n</article>`}
    ${feedback}
  </main>

  <footer class="site-footer">
    <div class="wrap site-footer__grid">
      <div>
        <p class="site-footer__title">${esc(site.name)}</p>
        <p class="site-footer__text">${esc(site.footer.tagline[lang] || site.footer.tagline.en)}</p>
      </div>
      <nav aria-label="${esc(site.footer.resourcesLabel[lang] || 'Resources')}">
        <p class="site-footer__title">${esc(site.footer.resourcesLabel[lang] || 'Resources')}</p>
        <ul class="site-footer__list">
          <li><a href="/data/catalog.json">catalog.json</a></li>
          <li><a href="/llms.txt">llms.txt</a></li>
          <li><a href="/sitemap.xml">sitemap.xml</a></li>
          <li><a href="${esc(site.urls.repository)}">${esc(site.footer.repository[lang] || 'Source on GitHub')}</a></li>
        </ul>
      </nav>
      <div>
        <p class="site-footer__title">${esc(site.footer.licenseLabel[lang] || 'License')}</p>
        <p class="site-footer__text">${esc(site.footer.licenseText[lang] || site.footer.licenseText.en)}</p>
      </div>
${product ? `      <div>
        <p class="site-footer__title">${esc(product.label)}</p>
        <p class="site-footer__text">${esc(product.note)}</p>
        <p class="site-footer__text"><a class="product-link product-link--footer" href="${esc(product.url)}" rel="external noopener">${esc(product.url.replace(/^https?:\/\//, '').replace(/\/$/, ''))}</a></p>
      </div>` : ''}
    </div>
    <div class="wrap site-footer__meta">
      <div class="footer__engineering-downloads" style="margin-bottom: 1.25rem; display: flex; gap: 10px; flex-wrap: wrap;">
        <a class="footer__download-chip" href="/docs/GLOBAL_LOCK_DATA_INDEX.xlsx" download style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 14px; background: rgba(37,99,235,0.08); border: 1px solid rgba(37,99,235,0.25); border-radius: 8px; color: #1d4ed8; font-size: 0.85rem; font-weight: 700; text-decoration: none;">
          📥 ${lang === 'zh' ? '下载 6工作表离线工程索引 (.xlsx)' : 'Download Master Engineering Index (.xlsx)'}
        </a>
        <a class="footer__download-chip" href="/data/catalog.json" download style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 14px; background: rgba(16,185,129,0.08); border: 1px solid rgba(16,185,129,0.25); border-radius: 8px; color: #047857; font-size: 0.85rem; font-weight: 700; text-decoration: none;">
          ⚙️ ${lang === 'zh' ? '全量机器可读 API (.json)' : 'Full Machine-Readable API (.json)'}
        </a>
      </div>
      <p>${esc(site.footer.disclaimer[lang] || site.footer.disclaimer.en)}</p>
    </div>
  </footer>
  <script src="/assets/js/site.js" defer></script>
  <script src="/assets/js/feedback.js" defer></script>
  <script src="/assets/js/gallery.js" defer></script>
</body>
</html>
`;
}

export function buildToc(headings, { minLevel = 2, maxLevel = 3 } = {}) {
  const items = headings.filter((h) => h.level >= minLevel && h.level <= maxLevel);
  if (items.length < 3) return '';
  return `<ul class="toc__list">${items
    .map((h) => `<li class="toc__item toc__item--h${h.level}"><a href="#${h.id}">${esc(h.text)}</a></li>`)
    .join('\n')}</ul>`;
}

export function faqJsonLd(faqItems) {
  if (!faqItems?.length) return null;
  return {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: faqItems.map((f) => ({
      '@type': 'Question',
      name: f.q,
      acceptedAnswer: { '@type': 'Answer', text: f.a },
    })),
  };
}

export function techArticleJsonLd({ headline, description, url, lang, dateModified }) {
  return {
    '@context': 'https://schema.org',
    '@type': 'TechArticle',
    headline,
    description,
    url,
    inLanguage: lang,
    dateModified,
    about: { '@type': 'Thing', name: 'Mechanical door locks and smart lock retrofit' },
    proficiencyLevel: 'Beginner to professional',
  };
}

export { SITE_URL };
