/**
 * Minimal, dependency-free Markdown renderer.
 *
 * Deliberately small: it supports the subset of Markdown used by the content in
 * `content/pages` (headings, tables, nested lists, code fences, callouts, links)
 * and nothing else. The point is to keep the build auditable — anyone reading
 * this file can see exactly how the published HTML is produced.
 */

export function slugify(input) {
  return String(input)
    .normalize('NFKD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .replace(/[^\p{L}\p{N}]+/gu, '-')
    .replace(/^-+|-+$/g, '')
    .slice(0, 80);
}

export function escapeHtml(text) {
  return String(text)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

/** Split front matter (`---` delimited) from the Markdown body. */
export function splitFrontMatter(source) {
  const match = /^---\r?\n([\s\S]*?)\r?\n---\r?\n?/.exec(source);
  if (!match) return { data: {}, body: source };
  return { data: parseSimpleYaml(match[1]), body: source.slice(match[0].length) };
}

/**
 * Tiny YAML subset: `key: value`, `key: [a, b]`, and two-space-indented list
 * items. Enough for front matter without pulling in a parser dependency.
 */
export function parseSimpleYaml(text) {
  const out = {};
  const lines = text.split(/\r?\n/);
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (!line.trim() || line.trim().startsWith('#')) continue;
    const m = /^([A-Za-z0-9_-]+):\s*(.*)$/.exec(line);
    if (!m) continue;
    const [, key, raw] = m;
    if (raw === '') {
      const items = [];
      while (i + 1 < lines.length && /^\s*-\s+/.test(lines[i + 1])) {
        items.push(unquote(lines[++i].replace(/^\s*-\s+/, '')));
      }
      out[key] = items;
    } else if (raw.startsWith('[') && raw.endsWith(']')) {
      out[key] = raw
        .slice(1, -1)
        .split(',')
        .map((s) => unquote(s.trim()))
        .filter(Boolean);
    } else {
      out[key] = unquote(raw);
    }
  }
  return out;
}

function unquote(value) {
  const v = value.trim();
  if ((v.startsWith('"') && v.endsWith('"')) || (v.startsWith("'") && v.endsWith("'"))) {
    return v.slice(1, -1);
  }
  return v;
}

/** Inline Markdown: code, bold, italic, links, images, line breaks. */
function inline(text, { headings = [] } = {}) {
  let html = escapeHtml(text);

  // Protect inline code from further processing.
  const codeSpans = [];
  html = html.replace(/`([^`]+)`/g, (_, code) => {
    codeSpans.push(code);
    return `\u0000CODE${codeSpans.length - 1}\u0000`;
  });

  html = html.replace(/!\[([^\]]*)\]\(([^)\s]+)(?:\s+&quot;([^&]*)&quot;)?\)/g,
    (_, alt, src, title) => `<img src="${src}" alt="${alt}"${title ? ` title="${title}"` : ''} loading="lazy">`);

  html = html.replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, (_, label, href) => {
    const external = /^https?:\/\//.test(href);
    return `<a href="${href}"${external ? ' rel="external noopener"' : ''}>${label}</a>`;
  });

  html = html
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    .replace(/(^|[\s(])\*([^*\n]+)\*/g, '$1<em>$2</em>')
    .replace(/~~([^~]+)~~/g, '<del>$1</del>');

  html = html.replace(/\u0000CODE(\d+)\u0000/g, (_, i) => `<code>${codeSpans[Number(i)]}</code>`);

  void headings;
  return html;
}

function tableCell(text) {
  return inline(text.trim());
}

/**
 * Render Markdown to HTML.
 * @returns {{html: string, headings: Array<{level: number, id: string, text: string}>}}
 */
export function renderMarkdown(markdown) {
  const lines = String(markdown).replace(/\r\n/g, '\n').split('\n');
  const out = [];
  const headings = [];
  const usedIds = new Set();
  let i = 0;

  const uniqueId = (base) => {
    let id = base || 'section';
    let n = 2;
    while (usedIds.has(id)) id = `${base}-${n++}`;
    usedIds.add(id);
    return id;
  };

  while (i < lines.length) {
    const line = lines[i];

    if (!line.trim()) { i++; continue; }

    // Fenced code block
    const fence = /^```(\S*)\s*$/.exec(line);
    if (fence) {
      const lang = fence[1];
      const buf = [];
      i++;
      while (i < lines.length && !/^```\s*$/.test(lines[i])) buf.push(lines[i++]);
      i++; // closing fence
      out.push(`<pre${lang ? ` class="language-${escapeHtml(lang)}"` : ''}><code>${escapeHtml(buf.join('\n'))}</code></pre>`);
      continue;
    }

    // Heading
    const heading = /^(#{1,6})\s+(.*)$/.exec(line);
    if (heading) {
      const level = heading[1].length;
      const text = heading[2].trim();
      const id = uniqueId(slugify(text));
      headings.push({ level, id, text });
      out.push(`<h${level} id="${id}">${inline(text)}</h${level}>`);
      i++;
      continue;
    }

    // Horizontal rule
    if (/^\s*(-{3,}|\*{3,}|_{3,})\s*$/.test(line)) {
      out.push('<hr>');
      i++;
      continue;
    }

    // Raw HTML block (used for <details>, <figure>, custom partials)
    if (/^\s*</.test(line)) {
      const buf = [];
      while (i < lines.length && lines[i].trim() !== '') buf.push(lines[i++]);
      out.push(buf.join('\n'));
      continue;
    }

    // Blockquote, including > [!NOTE] / > [!WARNING] callouts
    if (/^\s*>/.test(line)) {
      const buf = [];
      while (i < lines.length && /^\s*>/.test(lines[i])) {
        buf.push(lines[i].replace(/^\s*>\s?/, ''));
        i++;
      }
      const callout = /^\[!(\w+)\]\s*(.*)$/.exec(buf[0] || '');
      if (callout) {
        const kind = callout[1].toLowerCase();
        const title = callout[2] || kind.toUpperCase();
        const inner = renderMarkdown(buf.slice(1).join('\n')).html;
        out.push(`<aside class="callout callout--${kind}"><p class="callout__title">${escapeHtml(title)}</p>${inner}</aside>`);
      } else {
        out.push(`<blockquote>${renderMarkdown(buf.join('\n')).html}</blockquote>`);
      }
      continue;
    }

    // Table (header row followed by a delimiter row)
    if (line.includes('|') && /^\s*\|?[\s:|-]+\|[\s:|-]*$/.test(lines[i + 1] || '')) {
      const splitRow = (row) => row.trim().replace(/^\|/, '').replace(/\|$/, '').split('|');
      const header = splitRow(line);
      i += 2;
      const rows = [];
      while (i < lines.length && lines[i].includes('|') && lines[i].trim()) {
        rows.push(splitRow(lines[i]));
        i++;
      }
      const thead = header.map((c) => `<th>${tableCell(c)}</th>`).join('');
      const tbody = rows.map((r) => `<tr>${header.map((_, c) => `<td>${tableCell(r[c] ?? '')}</td>`).join('')}</tr>`).join('\n');
      out.push(`<div class="table-wrap"><table><thead><tr>${thead}</tr></thead><tbody>\n${tbody}\n</tbody></table></div>`);
      continue;
    }

    // Lists (nested by indentation, ordered or unordered)
    if (/^\s*([-*+]|\d+[.)])\s+/.test(line)) {
      const start = i;
      const buf = [];
      while (i < lines.length && (/^\s*([-*+]|\d+[.)])\s+/.test(lines[i]) || (/^\s+\S/.test(lines[i]) && buf.length))) {
        buf.push(lines[i]);
        i++;
      }
      out.push(renderList(buf));
      void start;
      continue;
    }

    // Paragraph
    const para = [];
    while (i < lines.length && lines[i].trim() && !/^(#{1,6}\s|\s*>|\s*([-*+]|\d+[.)])\s|```|\s*<)/.test(lines[i])) {
      para.push(lines[i]);
      i++;
    }
    if (para.length) out.push(`<p>${inline(para.join(' '))}</p>`);
  }

  return { html: out.join('\n'), headings };
}

function renderList(rawLines) {
  const items = [];
  const detect = (l) => {
    const m = /^(\s*)([-*+]|\d+[.)])\s+(.*)$/.exec(l);
    if (!m) return null;
    return { indent: m[1].replace(/\t/g, '  ').length, marker: m[2], text: m[3] };
  };

  const first = detect(rawLines[0]);
  if (!first) return `<p>${inline(rawLines.join(' '))}</p>`;
  const ordered = /\d/.test(first.marker);
  const baseIndent = first.indent;

  let idx = 0;
  while (idx < rawLines.length) {
    const parsed = detect(rawLines[idx]);
    if (parsed && parsed.indent <= baseIndent) {
      items.push({ text: parsed.text, children: [] });
      idx++;
    } else if (items.length) {
      // Collect the continuation / nested block belonging to the last item.
      const chunk = [];
      while (idx < rawLines.length) {
        const p = detect(rawLines[idx]);
        if (p && p.indent <= baseIndent) break;
        chunk.push(rawLines[idx].replace(new RegExp(`^\\s{0,${baseIndent + 2}}`), ''));
        idx++;
      }
      if (chunk.length) items[items.length - 1].children.push(chunk.join('\n'));
    } else {
      idx++;
    }
  }

  const body = items
    .map((item) => {
      const inner = item.children.length ? item.children.map(renderList).join('\n') : '';
      return `<li>${inline(item.text)}${inner}</li>`;
    })
    .join('\n');

  return ordered ? `<ol>\n${body}\n</ol>` : `<ul>\n${body}\n</ul>`;
}
