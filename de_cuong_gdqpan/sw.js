/* ============================================================
   SERVICE WORKER - Quiz QP-AN
   Chiến lược:
   - Cache-first cho static assets (HTML, CSS, JS, icons)
   - Network-first cho navigation (để cập nhật nội dung mới)
============================================================ */

const CACHE_VERSION = 'quiz-qpan-v1.0.0';
const STATIC_CACHE = `${CACHE_VERSION}-static`;
const PAGES_CACHE = `${CACHE_VERSION}-pages`;

// Tài nguyên cần cache ngay khi cài
const PRECACHE_URLS = [
  './',
  './index.html',
  './manifest.json',
  './icons/icon-192.png',
  './icons/icon-512.png',
  './icons/icon-maskable-512.png',
  './gdqpan1/',
  './gdqpan1/index.html',
  './gdqpan1/gdqpan1.json',
  './gdqpan2/',
  './gdqpan2/index.html',
  './gdqpan2/gdqpan2.json'
];

/* ============================================================
   INSTALL
============================================================ */
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(STATIC_CACHE)
      .then(cache => {
        // addAll fail nếu 1 file 404 → dùng add riêng lẻ để không vỡ cả cache
        return Promise.allSettled(
          PRECACHE_URLS.map(url =>
            cache.add(url).catch(err => console.warn('Precache miss:', url, err.message))
          )
        );
      })
      .then(() => self.skipWaiting())
  );
});

/* ============================================================
   ACTIVATE - dọn cache cũ
============================================================ */
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys
          .filter(key => !key.startsWith(CACHE_VERSION))
          .map(key => caches.delete(key))
      )
    ).then(() => self.clients.claim())
  );
});

/* ============================================================
   FETCH
============================================================ */
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Bỏ qua request khác origin (Google Fonts, CDN...) — trình duyệt tự xử lý
  if (url.origin !== self.location.origin) return;

  // Bỏ qua request không phải GET
  if (request.method !== 'GET') return;

  // Navigation request (mở trang) → Network-first, fallback cache
  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request)
        .then(response => {
          // Cache lại bản mới
          const clone = response.clone();
          caches.open(PAGES_CACHE).then(cache => cache.put(request, clone));
          return response;
        })
        .catch(() => {
          // Offline → thử cache
          return caches.match(request).then(cached => {
            if (cached) return cached;
            // Fallback: trang chủ nếu có
            return caches.match('./index.html');
          });
        })
    );
    return;
  }

  // Static assets (CSS, JS, JSON, images, fonts nội bộ) → Cache-first
  event.respondWith(
    caches.match(request).then(cached => {
      if (cached) {
        // Cập nhật ngầm (stale-while-revalidate)
        fetch(request).then(response => {
          if (response.ok) {
            caches.open(STATIC_CACHE).then(cache => cache.put(request, response));
          }
        }).catch(() => {});
        return cached;
      }
      // Chưa có cache → fetch và cache lại
      return fetch(request).then(response => {
        if (!response || !response.ok) return response;
        const clone = response.clone();
        caches.open(STATIC_CACHE).then(cache => cache.put(request, clone));
        return response;
      }).catch(() => {
        // Không có cache & offline
        return new Response('Offline - Không thể tải tài nguyên này.', {
          status: 503,
          statusText: 'Service Unavailable',
          headers: { 'Content-Type': 'text/plain; charset=utf-8' }
        });
      });
    })
  );
});

/* ============================================================
   MESSAGE - cho phép skipWaiting từ client (tùy chọn)
============================================================ */
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});
