# Service Worker & Web Worker — chạy ngầm, không chặn UI — [Level: Advanced]

## 🔑 Khái niệm cốt lõi

**Service Worker** và **Web Worker** đều là các script chạy **ở background**, tách khỏi trang web — giúp thực hiện việc không cần đến tương tác trực tiếp với User UI, giảm tải cho luồng chính (main thread).

### Service Worker (Proxy layer)

Là **proxy** giữa trình duyệt và mạng — có thể chặn request và trả dữ liệu từ **cache**. Dùng để xây dựng **PWA (Progressive Web App)** với offline support.

Đặc điểm:
- Không truy cập DOM — giao tiếp qua `postMessage`.
- Lifecycle: `install` → `activate` → `fetch` (active).
- Chỉ hoạt động trên **HTTPS** (hoặc `localhost` cho development).
- Register tại root scope hoặc subdirectory — quyết định URL range nó quản lý.
- Có thể cached assets, push notifications, background sync.

### Web Worker (Computation thread)

Chạy tính toán nặng trên **thread riêng**, không chặn UI main thread. Giao tiếp qua `postMessage()` / `onmessage`.

Đặc điểm:
- Không truy cập DOM.
- Parallel execution — nhiều worker cùng lúc.
- Perfect cho: crypto, image processing, large data computation.

## 📐 Cấu trúc / Cú pháp

### Service Worker registration

```js
// Trong main thread (page script)
if ("serviceWorker" in navigator) {
  navigator.serviceWorker
    .register("/service_worker.js", { scope: "/" })
    .then((reg) => console.log("SW registered", reg.scope))
    .catch((err) => console.error("SW registration failed", err));
}
```

### Service Worker script (service_worker.js)

```js
const CACHE_NAME = "my-app-v1";
const ASSETS = [
  "/",
  "/index.html",
  "/app.js",
  "/style.css",
  "/images/logo.png"
];

// Install — cache assets
self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS))
  );
  self.skipWaiting(); // activate ngay
});

// Activate — clean old caches
self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys
          .filter((key) => key !== CACHE_NAME)
          .map((key) => caches.delete(key))
      )
    )
  );
  self.clients.claim(); // control all pages immediately
});

// Fetch — serve from cache, fallback to network
self.addEventListener("fetch", (event) => {
  event.respondWith(
    caches.match(event.request).then((cached) => {
      return cached || fetch(event.request);
    })
  );
});
```

### Web Worker

```js
// Main thread
const worker = new Worker("worker.js");
worker.postMessage({ task: "calculate", data: [1, 2, 3] });
worker.onmessage = (e) => console.log("Result:", e.data);
worker.onerror = (e) => console.error("Worker error:", e.message);

// worker.js
self.onmessage = (e) => {
  const { task, data } = e.data;
  if (task === "calculate") {
    const result = data.reduce((a, b) => a + b, 0);
    self.postMessage(result);
  }
};
```

## ✅ Điểm mạnh — Tại sao nên dùng

1. **Web app chạy offline** — cached resources load từ local.
2. **Push notifications** — thông báo ngay cả khi app đóng.
3. **Background sync** — đồng bộ data khi network available.
4. **Tính toán nặng không đơ UI** — Web Worker tách khỏi main thread.
5. **Fast repeat visits** — cached assets load instant.
6. **Intercept network requests** — mock API, modify response.

## ⚠️ Bẫy thường gặp & Hạn chế

### Bẫy 1: Chỉ hoạt động trên HTTPS (trừ localhost)

```js
// Local development:
navigator.serviceWorker.register("/sw.js"); // ✅ localhost OK

// Production:
navigator.serviceWorker.register("https://example.com/sw.js"); // ✅ HTTPS required
// http://example.com/sw.js // ❌ fails
```

### Bẫy 2: Không truy cập DOM được

```js
// service_worker.js
document.getElementById("app"); // ❌ ReferenceError — no DOM in SW
self.clients.matchAll(); // ✅ correct API
```

### Bẫy 3: Register path determines scope

```js
// Register tại / → SW control toàn bộ site
navigator.serviceWorker.register("/sw.js");

// Register tại /app/ → SW chỉ control /app/ subdirectory
navigator.serviceWorker.register("/app/sw.js");
```

### Bẫy 4: Lifecycle complexity — install → activate không tự động

```js
// SW cũ vẫn active cho đến khi:
// 1. Tất cả clients đóng
// 2. Gọi self.skipWaiting() trong install
// 3. Gọi self.clients.claim() trong activate
```

### Bẫy 5: Cache không tự invalidate — phải quản lý version

```js
const CACHE_NAME = "my-app-v2"; // tăng version khi đổi assets
// Old cache "my-app-v1" sẽ tồn tại mãi nếu không delete trong activate
```

### Bẫy 6: Worker không share memory với main thread

```js
// Main thread
const ab = new ArrayBuffer(1);
worker.postMessage(ab); // copies data, không reference shared

// SharedArrayBuffer cần Atomics — requires cross-origin isolation headers
```

## 💡 Khi nào dùng — Tình huống thực tế

1. **PWA muốn chạy offline** — blog, docs, mua hàng, app không cần internet.
2. **Push notification** — thông báo tin tức, alert quan trọng.
3. **Background sync** — gửi form data khi online, dù user đã đóng tab.
4. **Tính toán nặng** — xử lý ảnh, video, crypto, large dataset.
5. **API mocking** — intercept request trong development.
6. **Performance optimization** — pre-fetch resources, cache strategy.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Basic Service Worker registration

```js
// index.html
if ("serviceWorker" in navigator) {
  navigator.serviceWorker
    .register("/service_worker.js")
    .then((reg) => console.log("SW registered", reg.scope))
    .catch((err) => console.error("SW failed", err));
} else {
  console.log("Service Worker not supported");
}
```

### Ví dụ 2: Complete SW with cache strategy

```js
// service_worker.js
const CACHE_NAME = "blog-v1";
const OFFLINE_URL = "/offline.html";

const PRECACHE_ASSETS = [
  "/",
  "/index.html",
  "/style.css",
  "/app.js",
  "/offline.html"
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(PRECACHE_ASSETS);
    }).then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k))
      )
    ).then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (event) => {
  // Cache-first strategy
  event.respondWith(
    caches.match(event.request).then((cached) => {
      if (cached) return cached;
      
      return fetch(event.request).then((response) => {
        if (!response || response.status !== 200 || response.type !== "basic") {
          return response;
        }
        
        const responseClone = response.clone();
        caches.open(CACHE_NAME).then((cache) => {
          cache.put(event.request, responseClone);
        });
        
        return response;
      }).catch(() => caches.match(OFFLINE_URL));
    })
  );
});
```

### Ví dụ 3: Web Worker — heavy computation

```js
// main.js
const worker = new Worker("worker.js");

worker.postMessage({ operation: "sum", numbers: Array(1000000).fill(1) });
worker.onmessage = (e) => {
  console.log("Sum:", e.data);
  document.getElementById("result").textContent = e.data;
};

// worker.js
self.onmessage = (e) => {
  const { operation, numbers } = e.data;
  let result;
  
  if (operation === "sum") {
    result = numbers.reduce((a, b) => a + b, 0);
  } else if (operation === "fibonacci") {
    result = fibonacci(e.data.n);
  }
  
  self.postMessage(result);
};

function fibonacci(n) {
  if (n <= 1) return n;
  let a = 0, b = 1;
  for (let i = 2; i <= n; i++) {
    [a, b] = [b, a + b];
  }
  return b;
}
```

### Ví dụ 4: Service Worker + Fetch integration

```js
// main.js — fetch data, SW cache it
async function loadData() {
  const res = await fetch("/api/posts");
  const posts = await res.json();
  renderPosts(posts);
}

// Lần sau (offline): SW serve từ cache, không cần network
```

### Ví dụ 5: Background Sync

```js
// main.js
if ("serviceWorker" in navigator && "SyncManager" in window) {
  navigator.serviceWorker.ready.then((reg) => {
    reg.sync.register("sync-posts");
  });
}

// service_worker.js
self.addEventListener("sync", (event) => {
  if (event.tag === "sync-posts") {
    event.waitUntil(syncPosts());
  }
});

async function syncPosts() {
  const pending = await getPendingPosts();
  for (const post of pending) {
    await fetch("/api/posts", {
      method: "POST",
      body: JSON.stringify(post)
    });
  }
}
```

### Ví dụ 6: Push Notification

```js
// service_worker.js
self.addEventListener("push", (event) => {
  const data = event.data ? event.data.json() : {};
  event.waitUntil(
    self.registration.showNotification(data.title || "New update", {
      body: data.body || "Check it out!",
      icon: "/icon.png",
      badge: "/badge.png"
    })
  );
});

self.addEventListener("notificationclick", (event) => {
  event.notification.close();
  event.waitUntil(
    clients.openWindow("https://example.com")
  );
});
```

### Ví dụ 7: Multiple Workers parallel computation

```js
// Split work across 4 workers
const workers = Array.from({ length: 4 }, () => new Worker("worker.js"));
const chunks = splitArray(data, 4);

chunks.forEach((chunk, i) => {
  workers[i].postMessage({ operation: "process", data: chunk });
});

workers.forEach((w, i) => {
  w.onmessage = (e) => {
    results[i] = e.data;
    if (i === 3) mergeResults(results);
  };
});
```

## 🔬 So sánh với alternatives

| Feature | Service Worker | Web Worker | Thread (C++) | WebAssembly |
|---------|---------------|------------|--------------|-------------|
| Offline cache | ✅ | ❌ | ❌ | ❌ |
| Push notifications | ✅ | ❌ | ❌ | ❌ |
| Heavy computation | ⚠️ Limited | ✅ | ✅ | ✅ |
| DOM access | ❌ | ❌ | ❌ | ❌ |
| Browser support | Modern | Modern | N/A | Modern |

## 📊 Performance & Best Practices

- **Cache strategically** — precache critical assets, runtime cache for API responses.
- **Version caches** — `CACHE_NAME = "app-v2"` để invalidate old cache.
- **Use `skipWaiting()` và `clients.claim()`** — SW active ngay sau update.
- **Keep SW script small** — giảm download time, parsing time.
- **Web Worker cho computation > 50ms** — tránh block main thread.
- **Terminate worker khi finish** — `worker.terminate()` giải phóng memory.
- **Test offline** — DevTools → Network → Offline checkbox.
- **HTTPS required** — production must be HTTPS, localhost OK for dev.

## 🔗 Liên kết chéo

- **Xem thêm:** `13_working-with-apis/01_fetch` — fetch + SW cache integration
- **Xem thêm:** `12_asynchronous-javascript/01_event-loop/00_js-runtime-deep-dive` — runtime architecture
- **Xem thêm:** `17_memory-management/01_memory-lifecycle-gc/02_memory-leaks` — worker memory management
- **Xem thêm:** `18_dom-apis/README` — DOM không truy cập được từ worker
- **MDN**: "Using Service Workers", "Web Workers"
