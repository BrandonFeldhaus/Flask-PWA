const CACHE_NAME = 'static-cache';

const FILES_TO_CACHE = [
  '/static/pages/offlinepages/offline.html',
  '/static/css/styles.css',
  '/static/pages/offlinepages/anotherpageOffline.html',
  '/static/pages/offlinepages/searchOffline.html'
];

const staticCacheName = 'pages-cache-v1';

///install event is the first event called for a service worker, it creates a cache and stores files
self.addEventListener('install', event => {
  console.log('Attempting to install service worker and cache static assets');
  event.waitUntil(
    caches.open(staticCacheName)
    .then(cache => {
      return cache.addAll(FILES_TO_CACHE);
    })
  );
});

/*
self.addEventListener('activate', (evt) => {
  console.log('[ServiceWorker] Activate');
  evt.waitUntil(
    caches.keys().then((keyList) => {
      return Promise.all(keyList.map((key) => {
        if (key !== CACHE_NAME) {
          console.log('[ServiceWorker] Removing old cache', key);
          return caches.delete(key);
        }
      }));
    })
  );
});
*/

/// Checks if there is wifi, if no wifi display offline page
self.addEventListener('fetch', (evt) => {
  if (evt.request.mode !== 'navigate') {
    return;
  }
  evt.respondWith(fetch(evt.request).catch(() => {
      return caches.open(staticCacheName).then((cache) => {
        return cache.match('/static/pages/offlinepages/offline.html');
      });
    })
  );
});


self.addEventListener('push', function(event) {
  console.log('[Service Worker] Push Received.');

  const title = 'OH NO, VULNERABILITY DETECTED';
  const options = {
    body: event.data.text(),
    icon: 'static/images/icon-64.png',
    vibrate: [50, 50, 50],
    sound: 'static/audio/notification-sound.mp3'
  };

  event.waitUntil(self.registration.showNotification(title, options));
});