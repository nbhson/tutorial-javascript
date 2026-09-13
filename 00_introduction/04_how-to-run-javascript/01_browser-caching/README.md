# Browser Caching JavaScript: Nơi lưu trữ & cách hoạt động — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

**Browser caching** là cơ chế mà trình duyệt **lưu lại các tài nguyên** (file JS, CSS, ảnh, font…) ngay trên máy người dùng sau lần tải đầu tiên, để những lần truy cập sau **không cần tải lại từ server**. Đây là một trong những kỹ thuật **hiệu suất quan trọng nhất** cho web development — file tĩnh tải một lần, dùng mãi cho đến khi nội dung thay đổi.

### Tại sao caching quan trọng với JavaScript?

JavaScript thường là **file lớn nhất** trong trang web (bundle React, Vue, hoặc đa module). Nếu không có caching, mỗi lần người dùng reload trang sẽ phải tải lại toàn bộ — gây:
- **Chậm perceived performance**: trắng màn hình chờ tải script.
- **Tốn bandwidth**: cả người dùng lẫn server đều mất data không cần thiết.
- **Tăng server load**: mỗi request JS lại phải xử lý từ đầu.

Khi cache hoạt động đúng, trải nghiệm người dùng cải thiện đáng kể: trang reload gần như tức thì.

### Nơi JavaScript được cache — 3 loại cache

| Loại cache | Vị trí lưu | Tốc độ | Đặc điểm |
|-----------|-----------|--------|---------|
| **Memory cache** | RAM của trình duyệt | **Nhanh nhất** (~0ms) | Xóa khi đóng tab/trình duyệt; dùng cho trang đang active |
| **Disk cache** | Ổ cứng (localStorage-like) | Nhanh (~1–10ms) | Bền qua các phiên trình duyệt; dùng cho trang đã visit gần đây |
| **Service Worker cache** | Kho lưu trữ SW riêng | Nhanh (~0–5ms) | Cache có lập trình được; hỗ trợ **offline-first** PWA |

> **Lưu ý:** Service Worker cache là cơ chế lập trình được (code cache logic), khác với HTTP cache (browser tự quyết theo headers).

### Quy trình hoạt động của HTTP caching

```
Lần 1 (First visit):
  Browser → Server: GET /app.js
  Server → Browser: 200 OK + app.js content + Cache-Control: max-age=31536000
  Browser lưu app.js vào disk cache + memory cache

Lần 2 (Subsequent visit):
  Browser → Server: GET /app.js + If-Modified-Since / Cache-Control check
  Server → Browser: 304 Not Modified (hoặc 200 nếu cache invalid)
  Browser load app.js từ cache — không tải lại từ mạng ✓
```

### Cache headers quan trọng

```http
# Cache dài hạn (file tĩnh, hash-based)
Cache-Control: public, max-age=31536000       # 1 năm
Cache-Control: immutable                      # không bao giờ revalidate

# Cache ngắn hạn (file thay đổi thường xuyên)
Cache-Control: public, max-age=3600           # 1 giờ
Cache-Control: must-revalidate                # phải check server trước khi dùng cache

# Không cache (dữ liệu nhạy cảm, auth token)
Cache-Control: no-cache, no-store             # luôn tải mới từ server
Cache-Control: private                        # chỉ cache per-user (CDN không cache)

# Shared cache (CDN, proxy)
Cache-Control: public, max-age=60, s-maxage=3600  # browser 60s, CDN 1h
```

### Cache invalidation — 4 chiến lược

| Chiến lược | Cách hoạt động | Ví dụ |
|-----------|---------------|-------|
| **Time-based** | `max-age`/`Expires` header quyết định thời gian hợp lệ | `max-age=3600` → cache hết hạn sau 1 giờ |
| **Version/Hash** | Đổi tên file khi nội dung đổi | `app.md4h3kf.js` → `app.def456.js` — file cũ tự "biến mất" |
| **Must-revalidate** | Yêu cầu browser check server trước khi dùng cache | `Cache-Control: must-revalidate` |
| **Manual purge** | Xóa cache thủ công trên server/CDN | Cloudflare Purge, AWS CloudFront Invalidate |

### Cách nhận biết file đã được cache — DevTools Network

Mở **DevTools (F12) → Tab Network** → Reload trang → Xem cột **Size**:

| Giá trị Size | Nghĩa | Thời gian |
|-------------|-------|-----------|
| `(memory cache)` | Load từ RAM — nhanh nhất | ~0 ms |
| `(disk cache)` | Load từ ổ cứng | ~1–10 ms |
| `(from ServiceWorker)` | Load từ SW cache | ~0–5 ms |
| `1.2 kB (gzip)` | Tải mới từ server | ~50–500 ms |

> **Mẹo:** reload lần 2 sẽ thấy `(disk cache)` hoặc `(memory cache)` — đây là dấu hiệu cache hoạt động đúng.

## 📐 Cấu trúc nhóm

```
04_how-to-run-javascript/
└── 01_browser-caching/
    ├── README.md                 ← bài này
    ├── index.html                # trang HTML demo
    └── app.js                    # file JS để quan sát cache behavior
```

## ✅ Điểm mạnh — Tại sao nên hiểu browser caching

| # | Điểm mạnh | Lý do |
|---|-----------|-------|
| 1 | **Tăng tốc tải trang rõ rệt** | Bỏ qua độ trễ mạng ở các lần truy cập sau — LCP cải thiện đáng kể |
| 2 | **Giảm băng thông** | Người dùng tiết kiệm data, server/CDN giảm load |
| 3 | **Cải thiện UX tinh thần** | "Tốc độ" và độ ổn định — user quay lại nhiều hơn |
| 4 | **Tích hợp build tool** | Vite, Webpack, Angular CLI tự động invalidation bằng hash |
| 5 | **Nền tảng PWA** | Service Worker cache + manifest = offline-first experience |
| 6 | **Hiệu quả SEO** | Google dùng Core Web Vitals (LCP, FID, CLS) làm ranking factor |
| 7 | **Tiết kiệm chi phí hosting** | Giảm bandwidth bill, giảm request count lên origin server |
| 8 | **Hiểu được DevTools** | Đọc được Network panel, chẩn đoán performance issue |

## ⚠️ Bẫy thường gặp & Hạn chế

| # | Bẫy | Ví dụ | Cách tránh |
|---|-----|-------|-----------|
| 1 | **Cache quá "chắc" — user mắc kẹt phiên bản cũ** | Sửa `app.js` nhưng user vẫn tải bản cũ từ cache | Versioning/hash: `app.md4h3kf.js` |
| 2 | **Cache không áp dụng cho inline script** | `<script>console.log('hello')</script>` không cache được | Tách ra file `.js` riêng |
| 3 | **`no-store` gây tải lại nhiều lần** | Mỗi lần reload đều tải lại từ server | Dùng `no-store` chỉ cho dữ liệu nhạy cảm |
| 4 | **First load vẫn chậm** | Cache chỉ phát huy ở lần truy cập thứ 2 trở đi | Dùng preload/prefetch cho lần đầu |
| 5 | **Cache header sai → stale content** | `max-age=0` với file static lớn — load lại every time | Set `max-age` hợp lý cho từng tài nguyên |
| 6 | **Service Worker cache override HTTP cache** | SW logic can thiệp vào cache strategy | Hiểu rõ SW cache API, test kỹ |
| 7 | **CDN cache không invalidate đúng cách** | Cloudflare cache giữ file cũ sau deploy | Configure cache purge API, hoặc hash-based filename |
| 8 | **Hard Reload không phải lúc nào cũng clear cache** | ⇧⌘R bỏ qua một số cache entries | Clear storage trong Application tab |

## 💡 Khi nào dùng — Tình huống thực tế

1. **File JS/CSS/ảnh tĩnh, không đổi** → cache dài hạn (1 năm) kèm hashing khi build.
2. **`index.html` luôn tải mới** → `Cache-Control: no-cache` để browser luôn check bản mới của HTML (vì HTML dẫn đến các file versioned).
3. **Ứng dụng PWA cần offline** → Service Worker cache chiến lược (stale-while-revalidate, cache-first, network-first).
4. **Website nhiều trang dùng chung bundle `app.js`** → hưởng lợi lớn nhất từ caching — tải một lần, dùng cho mọi trang.
5. **API response cache** — `Cache-Control` header cho API endpoint, CDN cache response.
6. **Static asset trên CDN** — CloudFront, Cloudflare cache assets, purge khi deploy mới.
7. **Developer experience** — disable cache trong DevTools (checkbox "Disable cache" khi DevTools mở) để test fresh load.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Demo cơ bản — quan sát cache trong DevTools

```html
<!-- index.html — thư mục 01_browser-caching -->
<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <title>Browser Caching Demo</title>
  <script src="app.js" defer></script>
</head>
<body>
  <h1>Browser Caching Demo</h1>
  <p>Mở DevTools → Network tab → Reload để quan sát cache behavior.</p>
  <p>Lần 1: app.js load từ localhost (~bytes)</p>
  <p>Lần 2: app.js load từ (memory cache) hoặc (disk cache) — ~0ms</p>
</body>
</html>
```

```js
// app.js — file JS riêng biệt
console.log("APP loaded from cache or network");
console.log("APP 2");
console.log("APP 3");

// Lần reload thứ nhất: Network tab thấy app.js với size ~100B, từ localhost
// Lần reload thứ hai: Network tab thấy app.js với size "(memory cache)" hoặc "(disk cache)"
// Thời gian: ~0ms thay vì ~50ms
```

**Hướng dẫn quan sát:**
1. Mở `index.html` trong trình duyệt.
2. Bật **DevTools (F12)** → tab **Network**.
3. Tick checkbox **"Disable cache"** → OFF (để cache hoạt động).
4. **Reload trang** (F5 hoặc ⇧⌘R) — lần đầu: app.js tải từ localhost.
5. **Reload lần 2** — app.js hiện `(disk cache)` hoặc `(memory cache)` trong cột Size.
6. So sánh thời gian: lần 1 ~50ms, lần 2 ~0ms.

### Ví dụ 2: Versioning/Hashing — cache invalidation chiến lược

```html
<!-- Cách 1: Hash-based filename (build tool tự làm) -->
<head>
  <script src="app.md4h3kf8.js" defer></script>
  <link rel="stylesheet" href="styles.a1b2c3d4.css">
</head>

<!-- Cách 2: Query string (ít được khuyến nghị — một số CDN không cache query string) -->
<head>
  <script src="app.js?v=2.1.3" defer></script>
</head>
```

```js
// Với hash-based: khi nội dung app.js đổi, build tool tạo tên file mới
// app.md4h3kf8.js → app.xyz987ab.js
// Browser tải file mới vì tên khác nhau — file cũ tự "biến mất" khỏi cache
```

### Ví dụ 3: Cache-Control headers — cấu hình server

```http
# nginx config
location ~* \.(js|css|png|jpg|svg|woff2)$ {
  expires 1y;                           # max-age=31536000
  add_header Cache-Control "public, immutable";
}

location /index.html {
  expires -1;                           # no-cache
  add_header Cache-Control "no-cache, must-revalidate";
}
```

```http
# Express.js (Node)
app.use(express.static('public', {
  maxAge: '1y',                         # 1 year cache
  immutable: true
}));

app.get('/api/data', (req, res) => {
  res.set('Cache-Control', 'no-store'); // API response: never cache
  res.json({ data: '...' });
});
```

### Ví dụ 4: Service Worker cache — lập trình cache

```js
// service-worker.js — cache chiến lược lập trình được
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open('v1-static').then((cache) => {
      return cache.addAll([
        '/app.js',
        '/styles.css',
        '/logo.png'
      ]);
    })
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      // Cache-first: dùng cache nếu có, còn không thì fetch từ network
      return cachedResponse || fetch(event.request);
    })
  );
});
```

### Ví dụ 5: Đo lường hiệu quả cache

```js
// Measure load time difference with/without cache
const measureLoad = async () => {
  const start = performance.now();

  // Hard reload to bypass cache
  await fetch('/app.js', { cache: 'no-store' });
  const noCacheTime = performance.now() - start;

  // Normal load (uses cache on 2nd visit)
  const start2 = performance.now();
  await fetch('/app.js', { cache: 'default' });
  const withCacheTime = performance.now() - start2;

  console.log(`Không cache: ${noCacheTime.toFixed(1)}ms`);
  console.log(`Có cache:    ${withCacheTime.toFixed(1)}ms`);
  console.log(`T tiết kiệm: ${(noCacheTime - withCacheTime).toFixed(1)}ms`);
};
```

## 🔬 So sánh với alternatives

| Chiến lược | Ưu điểm | Nhược điểm | Phù hợp khi |
|-----------|---------|------------|-------------|
| **HTTP Cache-Control** | Đơn giản, browser tự quản | Không linh hoạt, hard invalidate phức tạp | Static assets, CDN cache |
| **Version/Hash filename** | Invalidate tự động, không cần purge | Build tool phải hỗ trợ, URL thay đổi | Modern build tools (Vite, Webpack) |
| **Service Worker cache** | Lập trình được, offline-first | Phức tạp hơn, cần register SW | PWA, app-like experience |
| **Query string versioning** | Đơn giản, không cần build tool | Một số CDN/proxy không cache query string | Quick fix, legacy projects |
| **Manual purge (CDN)** | Kiểm soát tuyệt đối | Thủ công, cần trigger purge API | Enterprise, multi-CDN setups |

## 📊 Performance & Best Practices

- **Đặt `Cache-Control: max-age=31536000, immutable`** cho static assets (JS, CSS, images) — cache 1 năm, không bao giờ revalidate.
- **Đặt `Cache-Control: no-cache`** cho `index.html` — luôn check server để lấy version mới (vì HTML dẫn đến file versioned).
- **Dùng hash-based filename** (`app.abc123.js`) — tự động invalidate khi nội dung đổi.
- **Configure CDN cache headers** — Cloudflare, AWS CloudFront cần set cache policy đúng.
- **Dùng DevTools Network panel** thường xuyên — kiểm tra `(memory cache)` vs `(disk cache)` vs bytes tải thực tế.
- **Disable cache trong DevTools** khi debug — tick "Disable cache" để test fresh load.
- **Balance giữa cache lifetime và update frequency** — file rarely changes → cache dài; file thường đổi → cache ngắn hoặc hash.
- **Test trên connection chậm** — dùng DevTools Network "Slow 3G" để đo impact của cache real-world.

## 🔗 Liên kết chéo

- Xem thêm: `00_introduction/04_how-to-run-javascript/` — cách chèn script vào HTML
- Xem thêm: `00_introduction/04_how-to-run-javascript/01_browser-caching/` — bài thực hành này
- Xem thêm: `17_memory-management/01_memory-lifecycle-gc/` — browser memory vs cache (khác nhau)
- Xem thêm: `19_browser-devtools/02_devtools-performance/` — measure cache impact via Performance tab
- Xem thêm: `13_working-with-apis/01_fetch/` — fetch với cache option (`cache: 'no-store'`)
- Tài liệu: [MDN — HTTP caching](https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching), [Web.dev — HTTP caching](https://web.dev/uses-passive-listeners/), [Cache API](https://developer.mozilla.org/en-US/docs/Web/API/Cache_API)
