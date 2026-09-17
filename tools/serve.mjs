import http from 'http';
import fs from 'fs';
import path from 'path';

const PORT = 8080;
const ROOT = path.resolve('_site');
const LOGS_FILE = path.resolve('data/feedback_logs.json');

// Ensure data directory exists
if (!fs.existsSync(path.resolve('data'))) {
  fs.mkdirSync(path.resolve('data'), { recursive: true });
}
if (!fs.existsSync(LOGS_FILE)) {
  fs.writeFileSync(LOGS_FILE, JSON.stringify([], null, 2), 'utf8');
}

const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.mjs': 'application/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.webp': 'image/webp',
  '.ico': 'image/x-icon',
  '.md': 'text/markdown; charset=utf-8',
  '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
};

const server = http.createServer((req, res) => {
  // 1. API: Engineer feedback endpoint (Supports local preview & recording)
  if (req.method === 'POST' && req.url === '/api/feedback') {
    let body = '';
    req.on('data', chunk => { body += chunk; });
    req.on('end', () => {
      try {
        const payload = JSON.parse(body || '{}');
        const feedbackId = 'GLS-' + Date.now().toString(36).toUpperCase() + '-' + Math.random().toString(36).slice(2, 6).toUpperCase();
        const record = {
          id: feedbackId,
          timestamp: new Date().toISOString(),
          pageTitle: payload.pageTitle || '',
          pagePath: payload.pagePath || '',
          message: payload.message || '',
          contact: payload.contact || '',
          category: payload.category || 'other'
        };

        // Append to feedback_logs.json
        let logs = [];
        try { logs = JSON.parse(fs.readFileSync(LOGS_FILE, 'utf8')); } catch (_) { logs = []; }
        logs.unshift(record);
        fs.writeFileSync(LOGS_FILE, JSON.stringify(logs, null, 2), 'utf8');

        console.log(`\n📬 [收到新工程师建议] ID: ${feedbackId} | 来源页面: ${record.pagePath} (${record.pageTitle}) | 内容: ${record.message}`);

        res.writeHead(200, { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' });
        res.end(JSON.stringify({ ok: true, id: feedbackId, pagePath: record.pagePath, message: 'Feedback recorded' }));
      } catch (err) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'Invalid JSON body' }));
      }
    });
    return;
  }

  // 2. API: View feedback logs
  if (req.method === 'GET' && req.url === '/api/feedback-logs') {
    let logs = [];
    try { logs = JSON.parse(fs.readFileSync(LOGS_FILE, 'utf8')); } catch (_) { logs = []; }
    res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
    res.end(JSON.stringify(logs, null, 2));
    return;
  }

  // 3. Static routing & rewrite for /docs/
  let reqUrl = req.url.split('?')[0];

  // Map /(zh|en)/docs/ to /docs/
  const docMatch = reqUrl.match(/^\/(?:zh|en)\/docs\/(.*)$/);
  if (docMatch) {
    reqUrl = '/docs/' + docMatch[1];
  }

  // Map /docs/* directly to workspace docs/*
  if (reqUrl.startsWith('/docs/')) {
    const docRel = reqUrl.replace('/docs/', '');
    const docPath = path.resolve('docs', decodeURIComponent(docRel));
    if (fs.existsSync(docPath) && fs.statSync(docPath).isFile()) {
      const ext = path.extname(docPath).toLowerCase();
      res.writeHead(200, {
        'Content-Type': MIME_TYPES[ext] || 'application/octet-stream',
        'Cache-Control': 'no-cache',
      });
      fs.createReadStream(docPath).pipe(res);
      return;
    }
  }

  let filePath = path.join(ROOT, reqUrl === '/' ? 'index.html' : reqUrl);

  // If directory, try index.html
  if (fs.existsSync(filePath) && fs.statSync(filePath).isDirectory()) {
    filePath = path.join(filePath, 'index.html');
  }

  // Try appending .html
  if (!fs.existsSync(filePath) && fs.existsSync(filePath + '.html')) {
    filePath = filePath + '.html';
  }

  if (fs.existsSync(filePath) && fs.statSync(filePath).isFile()) {
    const ext = path.extname(filePath).toLowerCase();
    res.writeHead(200, {
      'Content-Type': MIME_TYPES[ext] || 'application/octet-stream',
      'Cache-Control': 'no-cache',
    });
    fs.createReadStream(filePath).pipe(res);
    return;
  }

  // 404 fallback
  const notFoundPath = path.join(ROOT, '404.html');
  if (fs.existsSync(notFoundPath)) {
    res.writeHead(404, { 'Content-Type': 'text/html; charset=utf-8' });
    fs.createReadStream(notFoundPath).pipe(res);
  } else {
    res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
    res.end('404 Not Found');
  }
});

server.listen(PORT, '0.0.0.0', () => {
  console.log(`Live Preview Server running at http://0.0.0.0:${PORT}`);
});
