const CACHE_NAME = '2d-agent-cache-v215';
const urlsToCache = [
  './',
  './index.html',
  './agent.html',
  './manifest.json'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        return cache.addAll(urlsToCache);
      })
  );
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  self.clients.claim();
});

// App-shell caching only: same-origin GET requests for our own files.
// Firebase Realtime Database (long-polling streams), gstatic and other
// cross-origin requests are NEVER intercepted, so the service worker can
// no longer break the live cloud connection inside installed PWAs.
self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);
  if (event.request.method !== 'GET' || url.origin !== self.location.origin) {
    return; // let the browser handle it normally
  }
  event.respondWith(
    fetch(event.request)
      .then(response => {
        // Network-first: always fetch the latest version from the server so
        // updates show up immediately. Only cache successful basic responses.
        if (response && response.status === 200 && response.type === 'basic') {
          const responseClone = response.clone();
          caches.open(CACHE_NAME).then(cache => {
            cache.put(event.request, responseClone).catch(() => {});
          });
        }
        return response;
      })
      .catch(() => caches.match(event.request))
  );
});
