# Cách chạy JavaScript trong trình duyệt — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

Để trình duyệt thực thi JavaScript, bạn phải **đưa mã JS vào trang HTML**. Có **3 cách chính** để làm điều này, và mỗi cách có ảnh hưởng khác nhau đến **hiệu suất tải trang** và **trật tự thực thi**.

### 3 cách chèn JavaScript vào HTML

#### Cách 1: Inline trong `<head>`

```html
<head>
  <script>
    alert("Đoạn script này chạy khi DOM chưa sẵn sàng!");
    // document.getElementById('main') → null!
  </script>
</head>
```

- Chạy **trước khi** nội dung `<body>` được render → **render-blocking**.
- Phù hợp để đặt sẵn hàm/biến dùng sau, hoặc các script analytics cần tải sớm.
- **Lưu ý quan trọng**: tại thời điểm này DOM của `<body>` chưa tồn tại, nên `document.getElementById(...)` sẽ trả về `null`.

#### Cách 2: Inline trong `<body>` (cuối cùng)

```html
<body>
  <h1>Nội dung trang web</h1>
  <script>
    // DOM đã sẵn sàng (vì script nằm sau nội dung)
    console.log(document.querySelector("h1").textContent);
  </script>
</body>
```

- Trình duyệt **tạm dừng render** tại điểm gặp `<script>` để thực thi rồi tiếp tục.
- Đặt cuối body giúp người dùng thấy nội dung trước, nhưng script lớn vẫn gây gián đoạn render.

#### Cách 3: File `.js` bên ngoài (best practice)

```html
<head>
  <script src="app.js" defer></script>
</head>
<!-- Hoặc cuối body -->
<body>
  ...
  <script src="app.js" defer></script>
</body>
```

- **Tách biệt**: cấu trúc (HTML), trình bày (CSS), hành vi (JS) — mỗi file một việc.
- **Browser caching**: file `.js` được cache sau lần tải đầu → lần sau tải nhanh hơn.
- **Dễ bảo trì**: sửa một file thay vì tìm trong hàng chục inline script.
- **Thuộc tính `defer`** (quan trọng nhất): tải song song background, **chỉ chạy sau khi** HTML được phân tích xong, và **giữ đúng thứ tự** xuất hiện.

### Thuộc tính `defer` vs `async` — khác nhau thế nào?

Cả hai chỉ áp dụng cho **external script** (có `src`):

| Thuộc tính | Tải song song? | Thực thi khi nào? | Giữ thứ tự? | Phù hợp cho |
|------------|---------------|-------------------|-------------|-------------|
| **`defer`** | Có | Sau khi HTML parse xong | **Có** — đúng thứ tự xuất hiện | Script phụ thuộc DOM, phụ thuộc thứ tự nhau |
| **`async`** | Có | Ngay khi tải xong (không chờ HTML) | **Không** — không đảm bảo | Script độc lập: analytics, quảng cáo, A/B test |

```html
<!-- defer: chạy sau khi DOM ready, đúng thứ tự -->
<script src="utils.js" defer></script>
<script src="app.js" defer></script>       <!-- app.js chạy sau utils.js -->

<!-- async: chạy ngay khi tải xong, thứ tự không đảm bảo -->
<script src="analytics.js" async></script>
<script src="ads.js" async></script>        <!-- ads.js có thể chạy trước analytics.js -->
```

### Render-blocking và impact đến performance

| Phương pháp | Render-blocking? | Browser caching? | Khuyến nghị |
|-------------|------------------|-------------------|--------------|
| Inline `<head>` | **Có** — chặn toàn trang | Không | ❌ Tránh trừ khi script cực nhỏ (< 1KB) |
| Inline cuối `<body>` | Có — chặn tại điểm chèn | Không | ⚠️ Chấp nhận được cho script nhỏ, nội bộ |
| File `.js` + `defer` | **Không** (nếu dùng defer) | **Có** | ✅ **Khuyến nghị** — best practice |
| File `.js` + `async` | **Không** (tải background) | **Có** | ✅ Cho script độc lập (analytics) |

### Quy trình load & execute một script với `defer`

```
1. Browser parse HTML → gặp <script src="app.js" defer>
2. Bắt đầu tải app.js song song với việc parse tiếp phần còn lại của HTML
3. Hoàn tất parse HTML (DOMContentLoaded event)
4. Chạy app.js — DOM đã sẵn sàng, script có thể truy cập elements
```

### DevTools — công cụ debug chính

- **Console (F12 → Console)**: xem `console.log`, lỗi runtime, test code trực tiếp.
- **Network (F12 → Network)**: xem file JS được tải từ đâu — `(memory cache)`, `(disk cache)`, hoặc từ server.
- **Sources (F12 → Sources)**: debug với breakpoint, step-through code.
- **Performance (F12 → Performance)**: profile, xem layout thrashing, long tasks.

#### Các lỗi phổ biến và cách sửa

| Lỗi | Nguyên nhân | Cách sửa |
|-----|------------|----------|
| `Cannot read properties of null` | Script chạy trước DOM | Đưa script xuống cuối body + dùng `defer` |
| `Uncaught SyntaxError` | Thiếu ngoặc `()`, `{}`, `""` | Kiểm tra dấu câu, dùng linter |
| `404 Not Found` | Đường dẫn `src` sai | Kiểm tra tab Network, path tương đối/absolute |
| Script chạy không theo thứ tự | Dùng `async` thay vì `defer` | Đổi `async` thành `defer` nếu cần giữ thứ tự |

## 📐 Cấu trúc nhóm

```
04_how-to-run-javascript/
├── README.md                 ← bài tổng quan này
└── 01_browser-caching/       ← cache hoạt động thế nào
    ├── index.html
    └── app.js
```

## ✅ Điểm mạnh — Tại sao nên học cách chạy JS đúng

| # | Điểm mạnh | Lý do |
|---|-----------|-------|
| 1 | **Chạy thử tức thì bằng Console** | Không cần dựng project — F12 là code được ngay |
| 2 | **File `.js` tách biệt** | Code sạch, dễ bảo trì, dễ tái sử dụng nhiều trang |
| 3 | **`defer` cho phép tải không blocking** | Trang hiển thị nhanh, "perceived performance" tốt |
| 4 | **Browser caching giảm băng thông** | File tĩnh tải một lần, dùng mãi cho đến khi thay đổi |
| 5 | **DevTools debug đủ mạnh** | Console, Network, Sources, Performance — đủ để truy tìm hầu hết lỗi |
| 6 | **Hiểu được call stack & execution context** | Nền tảng cho hoisting, closure, async programming |
| 7 | **Kiểm soát được thứ tự thực thi** | `defer` giữ thứ tự, `async` không — chọn đúng cho từng script |
| 8 | **Tối ưu được Core Web Vitals** | LCP, FID, CLS đều bị ảnh hưởng bởi script placement |

## ⚠️ Bẫy thường gặp & Hạn chế

| # | Bẫy | Ví dụ |
|---|-----|-------|
| 1 | **Script trong `<head>` chạy khi DOM chưa có** | `document.getElementById('main')` → `null` → `Cannot read properties of null` |
| 2 | **Không dùng `defer` cho script DOM-dependent** | Inline script trong head truy cập DOM → lỗi ngay lập tức |
| 3 | **Dùng `async` cho script có thứ tự phụ thuộc** | `analytics.js` tải xong trước `tracker.js` → tracker chạy khi analytics chưa sẵn sàng |
| 4 | **Nhiều `<script>` không defer/async tải tuần tự** | Kéo dài thời gian render-blocking, đặc biệt với script lớn |
| 5 | **Inline script không được cache** | Mỗi lần reload trang, browser phải parse lại nội dung inline — lãng phí bandwidth |
| 6 | **`defer` không hoạt động với `type="module"`** | Module script tự động defer — viết `defer` thêm là thừa (nhưng không lỗi) |
| 7 | **Hard Reload (⇧⌘R) không đảm bảo cache mới** | Nếu server không set cache header đúng, hard reload vẫn có thể lấy cached version |

## 💡 Khi nào dùng — Tình huống thực tế

1. **Xác thực form ngay khi gõ/submit** — inline cuối body hoặc external defer, vì cần truy cập DOM.
2. **Dark mode toggle** — thêm/bớt class bằng JavaScript + CSS listener, cần DOM sẵn sàng → `defer`.
3. **Cập nhật nội dung động** — hiển thị ngày giờ, đồng hồ, giỏ hàng mà không reload trang.
4. **Đặt script analytics/quảng cáo** — dùng `async` vì độc lập, không cần DOM, không cần thứ tự.
5. **Library lớn (React, Vue)** — dùng `defer` hoặc `type="module"` để không chặn render.
6. **Multi-page app với shared common JS** — tách thành file riêng, hưởng lợi browser caching across pages.
7. **A/B testing scripts** — `async` vì không phụ thuộc DOM và không cần thứ tự xác định.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Cách chuẩn hiện đại (defer + external file)

```html
<!-- index.html -->
<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <title>Chạy JS Đúng Cách</title>
  <!-- defer: tải song song, chạy sau DOM ready -->
  <script src="app.js" defer></script>
</head>
<body>
  <button id="toggle">Đổi chế độ tối</button>
  <h1 id="title">Xin chào thế giới</h1>
  <p id="info">Click button để toggle dark mode</p>
</body>
</html>
```

```js
// app.js
console.log("Script ngoài file, chạy sau khi DOM sẵn sàng ✓");

const btn = document.getElementById("toggle");
const title = document.getElementById("title");
const info = document.getElementById("info");

// Toggle dark mode
btn.addEventListener("click", () => {
  document.body.classList.toggle("dark");
  const isDark = document.body.classList.contains("dark");
  title.textContent = isDark ? "Chế độ tối" : "Chế độ sáng";
  info.textContent = isDark ? "Đã bật dark mode" : "Đã tắt dark mode";
});
```

### Ví dụ 2: So sánh defer vs async

```html
<!DOCTYPE html>
<html>
<head>
  <!-- Script A: defer — chạy sau DOM ready, đúng thứ tự -->
  <script src="a.js" defer></script>
  <!-- Script B: defer — chạy sau A, đúng thứ tự -->
  <script src="b.js" defer></script>
  <!-- Script C: async — chạy ngay khi tải xong, có thể trước A hoặc B -->
  <script src="c.js" async></script>
</head>
<body>
  <h1>Test defer vs async</h1>
  <!-- Mở Console để xem thứ tự log -->
</body>
</html>
```

```js
// a.js
console.log("A chạy sau DOM ready");

// b.js
console.log("B chạy sau A (defer giữ thứ tự)");

// c.js
console.log("C chạy khi tải xong — thứ tự không đảm bảo!");
```

### Ví dụ 3: Inline script cuối body (acceptable cho script nhỏ)

```html
<body>
  <h1>Nội dung trang</h1>
  <p>Văn bản giới thiệu...</p>

  <!-- Script nhỏ, inline — DOM đã sẵn sàng vì nằm cuối body -->
  <script>
    const mainHeading = document.querySelector("h1");
    mainHeading.style.color = "blue";
    console.log("Inline script cuối body: DOM sẵn sàng ✓");
  </script>
</body>
```

### Ví dụ 4: Quan sát browser caching trong DevTools

```js
// app.js — thư mục 01_browser-caching
console.log("APP");
console.log("APP 2");
console.log("APP 3");

// Lần reload đầu tiên: Network tab hiện app.js với size ~100B, từ "localhost"
// Lần reload thứ hai: Network tab hiện app.js với size "(memory cache)" hoặc "(disk cache)"
// Thời gian load: ~0ms thay vì ~50ms
```

### Ví dụ 5: Error handling — debug script lỗi

```js
// Ví dụ về lỗi phổ biến và cách sửa
try {
  // Lỗi: document.getElementById chưa tồn tại vì script chạy trước DOM
  const el = document.getElementById("missing");
  console.log(el.textContent); // TypeError: Cannot read properties of null
} catch (err) {
  console.error("Lỗi:", err.message);
}

// Cách sửa: đặt script sau DOM hoặc dùng defer
// Hoặc đợi DOM ready:
document.addEventListener("DOMContentLoaded", () => {
  const el = document.getElementById("missing");
  console.log(el ? el.textContent : "Element not found");
});
```

## 🔬 So sánh với alternatives

| Phương pháp | Ưu điểm | Nhược điểm | Phù hợp khi |
|------------|---------|------------|-------------|
| **External + defer** | Cache được, không blocking, giữ thứ tự | Cần server/phần mềm serve file | Đa số trường hợp — best practice |
| **External + async** | Tải không blocking, độc lập | Không giữ thứ tự, không đảm bảo DOM ready | Analytics, quảng cáo, A/B test |
| **Inline trong body** | Đơn giản, không cần file | Không cache được, tăng HTML size | Script nhỏ (< 1KB), prototype |
| **Inline trong head** | Nhanh chóng, accessible sớm | Render-blocking, không cache được | Analytics tracking code (cần sớm) |
| **Module script** | Tự động defer, isolated scope | Hỗ trợ browser cũ kém hơn | Project hiện đại, dùng import/export |

## 📊 Performance & Best Practices

- **Luôn đặt `<script>` ở cuối `<body>`** hoặc dùng `defer` — tránh render-blocking, cải thiện LCP.
- **Tách JS ra file riêng** — tận dụng browser caching, giảm HTML bundle size.
- **Dùng `defer` cho script DOM-dependent** — đảm bảo DOM sẵn sàng khi script chạy.
- **Dùng `async` cho script độc lập** — analytics, ads, tracking — không cần thứ tự.
- **Kiểm tra Network tab** — xác nhận file JS được load từ cache `(disk cache)`/`(memory cache)` thay vì từ server.
- **Hard Reload (⇧⌘R) để test cache** — bỏ qua cache tạm thời, tải lại từ server.
- **Dùng `<script type="module">`** — tự động defer, scope isolated, phù hợp project hiện đại.
- **Giảm số lượng script** — mỗi `<script>` là một network request (trừ khi cache); combine và minify để tối ưu.

## 🔗 Liên kết chéo

- Xem thêm: `00_introduction/04_how-to-run-javascript/01_browser-caching/` — browser cache hoạt động thế nào
- Xem thêm: `01_variables/02_hoisting/` — function declaration hoisted, script placement ảnh hưởng hoisting context
- Xem thêm: `09_functions/02_scope-closure-strict-mode/04_non-blocking-io/` — event loop và non-blocking I/O
- Xem thêm: `12_asynchronous-javascript/01_event-loop/` — event loop, call stack, task queue
- Xem thêm: `19_browser-devtools/02_devtools-performance/` — profile và optimize performance
- Xem thêm: `18_dom-apis/01_dom-basics/` — DOM API và truy cập element từ JS
- Tài liệu: [MDN — Insert JavaScript into HTML](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/script), [Web.dev — Remove render-blocking JS](https://web.dev/use-defer-script/)
