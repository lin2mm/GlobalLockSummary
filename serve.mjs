/**
 * Tiny static file server for local preview and the sandbox live preview.
 * No dependencies. Serves _site/ (run `node build.mjs` first).
 *
 *   node serve.mjs            http://0.0.0.0:8080
 *   PORT=3000 node serve.mjs
 */

import { createServer } from 'node:http';
import { readFile, stat } from 'node:fs/promises';
import { extname, join, normalize, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { dirname } from 'node:path';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '_site');
const PORT = Number(process.env.PORT || 8080);
const HOST = process.env.HOST || '0.0.0.0';

const TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.txt': 'text/plain; charset=utf-8',
  '.xml': 'application/xml; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.ico': 'image/x-icon',
  '.webmanifest': 'application/manifest+json',
};

const server = createServer(async (req, res) => {
  try {
    const url = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
    let pathname = decodeURIComponent(url.pathname);

    // Directory requests resolve to index.html, like GitHub Pages does.
    if (pathname.endsWith('/')) pathname += 'index.html';

    const filePath = normalize(join(ROOT, pathname));
    if (!filePath.startsWith(ROOT)) {
      res.writeHead(403).end('Forbidden');
      return;
    }

    let target = filePath;
    try {
      const info = await stat(target);
      if (info.isDirectory()) target = join(target, 'index.html');
    } catch {
      // Extension-less URLs (e.g. /identify) resolve to the .html file.
      try {
        await stat(`${filePath}.html`);
        target = `${filePath}.html`;
      } catch {
        target = join(ROOT, '404.html');
        res.statusCode = 404;
      }
    }

    const body = await readFile(target);
    const type = TYPES[extname(target)] || 'application/octet-stream';
    res.setHeader('Content-Type', type);
    res.setHeader('Cache-Control', 'no-cache');
    res.end(body);
  } catch (error) {
    res.writeHead(500, { 'Content-Type': 'text/plain; charset=utf-8' });
    res.end(`Internal error: ${error.message}`);
  }
});

server.listen(PORT, HOST, () => {
  console.log(`serving ${ROOT}`);
  console.log(`  local:   http://localhost:${PORT}/`);
  console.log(`  network: http://${HOST}:${PORT}/`);
});
