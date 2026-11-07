
const CACHE_NAME = "message-encryptor-v1";

const BASE_URL = new URL("./", self.registration.scope);
const INDEX_URL = new URL("index.html", BASE_URL).href;

const APP_FILES = [
  BASE_URL.href,
  INDEX_URL,
  new URL("manifest.json", BASE_URL).href,
  new URL("icons/icon-192.png", BASE_URL).href,
  new URL("icons/icon-512.png", BASE_URL).href
];

// نصب و ذخیره فایل‌های اصلی برنامه
self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(APP_FILES))
      .then(() => self.skipWaiting())
  );
});

// فعال‌سازی نسخه جدید و پاک‌کردن کش قدیمی
self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) =>
        Promise.all(
          keys
            .filter((key) => key !== CACHE_NAME)
            .map((key) => caches.delete(key))
        )
      )
      .then(() => self.clients.claim())
  );
});

// مدیریت درخواست‌ها
self.addEventListener("fetch", (event) => {
  const request = event.request;

  if (request.method !== "GET") return;

  const url = new URL(request.url);

  // فقط درخواست‌های مربوط به سایت خودمان
  if (url.origin !== self.location.origin) return;

  if (request.mode === "navigate") {
    event.respondWith(
      fetch(request)
        .then((response) => {
          if (response.ok) {
            const copy = response.clone();
            caches.open(CACHE_NAME)
              .then((cache) => cache.put(INDEX_URL, copy));
          }
          return response;
        })
        .catch(async () => {
          return (await caches.match(INDEX_URL)) ||
                 (await caches.match(BASE_URL));
        })
    );
    return;
  }

  // ابتدا نسخه ذخیره‌شده، سپس اینترنت
  event.respondWith(
    caches.match(request).then((cached) => {
      return cached || fetch(request).then((response) => {
        if (response.ok) {
          const copy = response.clone();
          caches.open(CACHE_NAME)
            .then((cache) => cache.put(request, copy));
        }
        return response;
      });
    })
  );
});
