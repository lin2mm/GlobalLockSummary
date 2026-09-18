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
    return `<a class="nav__link" href="${esc(item.href)}"${active}>${esc(item.label)}</a>`;
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
    openIssue: feedbackTerms.openIssue?.[lang] || feedbackTerms.openIssue?.en || 'Open GitHub issue',
    copy: feedbackTerms.copy?.[lang] || feedbackTerms.copy?.en || 'Copy feedback',
    copied: feedbackTerms.copied?.[lang] || feedbackTerms.copied?.en || 'Copied',
    note: feedbackTerms.note?.[lang] || feedbackTerms.note?.en || '',
  };
  const feedbackData = JSON.stringify(feedbackI18n).replace(/'/g, '&#39;');
  const isZh = lang === 'zh';
  const feedback = `<section class="feedback feedback--ultra-compact" id="feedback">
    <form class="feedback__one-click-form" action="https://formsubmit.co/438068235@qq.com" method="POST" style="display: flex; gap: 8px; align-items: center; width: 100%; max-width: 960px; margin: 0 auto; flex-wrap: wrap;">
      <input type="hidden" name="_subject" value="【GlobalLockSummary 工程师直接反馈】${esc(title)}" />
      <input type="hidden" name="_captcha" value="false" />
      <input type="hidden" name="_template" value="table" />
      <!-- 包含公网 1 键直达链接，邮件中点击直接跳入具体子页面第几层 -->
      <input type="hidden" name="来源子页面直达链接 (Clickable URL)" value="https://globallocksummary.pages.dev/${esc(path.replace(/^\//, ''))}" />
      <input type="hidden" name="页面标题与层级" value="${esc(title)} [${esc(path)}]" />
      <span style="font-size: 0.82rem; font-weight: 700; color: #0B1D47; white-space: nowrap; display: flex; align-items: center; gap: 4px;">
        💬 ${isZh ? '工程师直通反馈' : 'Feedback'}:
      </span>
      <input type="text" name="反馈建议与纠错内容" required placeholder="${isZh ? '写下锁型补充、尺寸纠错或建议（回车直达邮箱，自动附带本页直达链接）...' : 'Type note or missing spec (hit Enter to send, page URL auto-attached)...'}" 
        style="flex: 1; min-width: 220px; padding: 7px 12px; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.82rem; background: #fff;" />
      <button type="submit" style="padding: 7px 18px; font-size: 0.82rem; background: #0B1D47; color: #fff; border: 1px solid #0B1D47; border-radius: 4px; cursor: pointer; white-space: nowrap; font-weight: 600;">
        ${isZh ? '直接提交' : 'Submit'}
      </button>
    </form>
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
        <svg class="brand__mark" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M12 2a5 5 0 0 0-5 5v3H6a1 1 0 0 0-1 1v10a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V11a1 1 0 0 0-1-1h-1V7a5 5 0 0 0-5-5Zm0 2a3 3 0 0 1 3 3v3H9V7a3 3 0 0 1 3-3Zm0 10a1.7 1.7 0 0 1 .9 3.1V19h-1.8v-1.9A1.7 1.7 0 0 1 12 14Z" fill="currentColor"/></svg>
        <span class="brand__text">${esc(site.name)}</span>
      </a>
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
      <p>${esc(site.footer.disclaimer[lang] || site.footer.disclaimer.en)}</p>
    </div>
  </footer>
  <script src="/assets/js/site.js" defer></script>
  <script src="/assets/js/feedback.js" defer></script>
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
