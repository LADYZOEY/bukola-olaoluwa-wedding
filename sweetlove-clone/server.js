const http = require('http');
const https = require('https');
const fs = require('fs');
const path = require('path');

// Configuration
const PORT = process.env.PORT || 3001;
const PUBLIC_DIR = __dirname;
const UPSTREAM_HOST = "sweetlove-theme.thedigitalinvite.com";

const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.mjs': 'application/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif': 'image/gif',
  '.svg': 'image/svg+xml',
  '.webp': 'image/webp',
  '.avif': 'image/avif',
  '.ico': 'image/x-icon',
  '.woff': 'font/woff',
  '.woff2': 'font/woff2',
  '.ttf': 'font/ttf',
  '.mp4': 'video/mp4',
  '.webm': 'video/webm',
  '.mp3': 'audio/mpeg',
  '.wav': 'audio/wav',
};

const server = http.createServer((req, res) => {
  const parsedUrl = new URL(req.url, `http://localhost:${PORT}`);
  let pathname = decodeURIComponent(parsedUrl.pathname);

  if (pathname === '/api/log-error') {
    let body = '';
    req.on('data', chunk => { body += chunk; });
    req.on('end', () => {
      console.log('>>> [BROWSER ERROR] <<<', body);
      try { fs.appendFileSync(path.join(__dirname, 'browser_errors.log'), new Date().toISOString() + ' ' + body + '\n'); } catch (e) {}
      res.writeHead(200, { 'Content-Type': 'text/plain', 'Access-Control-Allow-Origin': '*' });
      res.end('ok');
    });
    return;
  }

  // Default to index.html for root
  if (pathname === '/' || pathname === '') {
    pathname = '/index.html';
  }

  const localFilePath = path.join(PUBLIC_DIR, pathname);

  // 1. Direct local file match
  if (fs.existsSync(localFilePath) && fs.statSync(localFilePath).isFile()) {
    return serveLocal(localFilePath, req, res);
  }

  // 2. Direct local file with .html extension
  if (fs.existsSync(localFilePath + '.html') && fs.statSync(localFilePath + '.html').isFile()) {
    return serveLocal(localFilePath + '.html', req, res);
  }

  // 3. Directory with index.html
  const nestedIndex = path.join(localFilePath, 'index.html');
  if (fs.existsSync(nestedIndex) && fs.statSync(nestedIndex).isFile()) {
    return serveLocal(nestedIndex, req, res);
  }

  // 4. On-demand proxy for assets, fonts, modules, bundles, or media
  if (
    pathname.startsWith('/_next/') ||
    pathname.startsWith('/assets/') ||
    pathname.startsWith('/lovable-uploads/') ||
    pathname.startsWith('/__l5e/') ||
    pathname.endsWith('.woff2') ||
    pathname.endsWith('.woff') ||
    pathname.endsWith('.mjs') ||
    pathname.endsWith('.js') ||
    pathname.endsWith('.css') ||
    pathname.endsWith('.png') ||
    pathname.endsWith('.jpg') ||
    pathname.endsWith('.jpeg') ||
    pathname.endsWith('.svg') ||
    pathname.endsWith('.webp') ||
    pathname.endsWith('.mp4') ||
    pathname.endsWith('.webm') ||
    pathname.endsWith('.mp3') ||
    pathname.endsWith('.wav') ||
    pathname === '/favicon.ico' ||
    pathname === '/~flock.js'
  ) {
    return proxyAndCache(pathname, parsedUrl.search, localFilePath, req, res);
  }

  // 5. Fallback to root index.html (SPA routes)
  const rootIndex = path.join(PUBLIC_DIR, 'index.html');
  if (fs.existsSync(rootIndex)) {
    return serveLocal(rootIndex, req, res);
  }

  res.writeHead(404, { 'Content-Type': 'text/plain' });
  res.end('404 Not Found');
});

function serveLocal(filePath, req, res) {
  const ext = path.extname(filePath).toLowerCase();
  const contentType = MIME_TYPES[ext] || 'application/octet-stream';
  const stat = fs.statSync(filePath);
  const totalSize = stat.size;

  // Handle HTTP Range requests for video/audio streaming
  const range = req.headers.range;
  if (range && (contentType.startsWith('video/') || contentType.startsWith('audio/'))) {
    const parts = range.replace(/bytes=/, "").split("-");
    const start = parseInt(parts[0], 10);
    const end = parts[1] ? parseInt(parts[1], 10) : totalSize - 1;

    if (start >= totalSize || end >= totalSize) {
      res.writeHead(416, {
        'Content-Range': `bytes */${totalSize}`,
        'Access-Control-Allow-Origin': '*'
      });
      return res.end();
    }

    const chunksize = (end - start) + 1;
    const fileStream = fs.createReadStream(filePath, { start, end });
    res.writeHead(206, {
      'Content-Range': `bytes ${start}-${end}/${totalSize}`,
      'Accept-Ranges': 'bytes',
      'Content-Length': chunksize,
      'Content-Type': contentType,
      'Access-Control-Allow-Origin': '*',
    });
    fileStream.pipe(res);
    return;
  }

  res.writeHead(200, {
    'Content-Type': contentType,
    'Content-Length': totalSize,
    'Accept-Ranges': 'bytes',
    'Access-Control-Allow-Origin': '*',
    'Cache-Control': 'no-cache, no-store, must-revalidate',
  });
  fs.createReadStream(filePath).pipe(res);
}

function proxyAndCache(pathname, search, localFilePath, req, clientRes) {
  const upstreamPath = pathname + (search || '');
  const headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    'Accept': '*/*',
    'Referer': `https://${UPSTREAM_HOST}/`,
  };

  if (req.headers.range) {
    headers['range'] = req.headers.range;
  }

  const options = {
    hostname: UPSTREAM_HOST,
    port: 443,
    path: upstreamPath,
    method: 'GET',
    headers: headers,
  };

  const proxyReq = https.request(options, (upstreamRes) => {
    // Only cache successful 200 responses to avoid caching 404s
    if (upstreamRes.statusCode === 200 && !req.headers.range) {
      try {
        fs.mkdirSync(path.dirname(localFilePath), { recursive: true });
        const fileStream = fs.createWriteStream(localFilePath);
        upstreamRes.pipe(fileStream);
      } catch (err) {
        // Cache write errors do not block serving
      }
    }

    const resHeaders = { ...upstreamRes.headers };
    // Strip security policies that break local execution
    delete resHeaders['content-security-policy'];
    delete resHeaders['x-frame-options'];
    resHeaders['access-control-allow-origin'] = '*';

    // Enforce correct JS mime type
    const ext = path.extname(localFilePath).toLowerCase();
    if (MIME_TYPES[ext]) {
      resHeaders['content-type'] = MIME_TYPES[ext];
    }

    clientRes.writeHead(upstreamRes.statusCode, resHeaders);
    upstreamRes.pipe(clientRes);
  });

  proxyReq.on('error', (err) => {
    console.error('[PROXY ERROR]', upstreamPath, err.message);
    if (!clientRes.headersSent) {
      clientRes.writeHead(502, { 'Content-Type': 'text/plain' });
      clientRes.end('502 Bad Gateway');
    }
  });

  proxyReq.end();
}

server.listen(PORT, () => {
  console.log(`Clone server running at http://localhost:${PORT}`);
});
