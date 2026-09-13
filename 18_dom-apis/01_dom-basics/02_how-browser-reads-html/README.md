# Trình duyệt đọc HTML như thế nào (Rendering Pipeline) — [Level: Beginner → Intermediate]

## 🔑 Khái niệm cốt lõi

Khi bạn nhập URL, trình duyệt trải qua chuỗi bước để vẽ trang lên màn hình. Hiểu pipeline này là chìa khóa để **debug performance** và **tối ưu đúng chỗ**.

### 10 Bước rendering pipeline

1. **Request**: trình duyệt tạo HTTP request tới server (GET, header...).
2. **Server xử lý**: tìm tài nguyên, xác thực, trả **Response** kèm HTML/CSS/JS.
3. **Download**: trình duyệt tải về các tài nguyên (tuần tự/song song tùy browser optimization).
4. **HTML Parsing**: đọc từng ký tự HTML → chuyển thành **nodes** (mỗi thẻ là một node với attribute).
5. **DOM Tree Construction**: sắp xếp nodes thành **cây DOM** theo hệ phân cấp cha/con. Cây này đại diện trang web và được **phơi bày cho JS** qua API — "Cái nhận về từ mạng là chuỗi text; trình duyệt parse nó thành mô hình dữ liệu mà máy hiểu".
6. **CSSOM Construction**: các file CSS được tạo thành **CSS Object Model** — cây quy tắc CSS tương tự DOM.
7. **Render Tree**: gộp DOM + CSSOM — chỉ giữ phần tử cần hiển thị (bỏ `display:none`, `hidden`).
8. **Layout (Reflow)**: đặt vị trí và kích thước từng phần tử trên trang — tính toán geometry.
9. **Paint**: vẽ từng pixel lên màn hình — color, border, shadow, text.
10. **Composite**: sắp xếp các layer theo z-order, combine thành final image gửi đến screen.

### JavaScript Execution — điểm quan trọng
Nếu gặp `<script>` trong HTML:
- **Blocking script** (`<script src="...">` không có defer/async): parser **dừng** lại, tải và execute script, rồi mới tiếp tục parse.
- **Defer** (`<script defer src="...">`): tải song song với parse, execute **SAU** khi DOM xong.
- **Async** (`<script async src="...">`): tải song song, execute **NGAY** khi download xong (có thể trước DOM xong).

### Tại sao sửa DOM lại "đắt"?
Mỗi lần JS đổi DOM/CSSOM, trình duyệt có thể phải:
1. **Reflow (Layout)** — tính lại vị trí/kích thước các element.
2. **Repaint (Paint)** — vẽ lại pixel.
3. **Composite** — sắp xếp lại layers.

Reflow là昂贵 nhất — một thay đổi nhỏ có thể trigger reflow cả subtree.

## 📐 Cấu trúc / Cú pháp

### Script loading strategies
```html
<!-- Blocking — parser dừng lại -->
<script src="heavy.js"></script>

<!-- Deferred — tải song song, chạy SAU DOM parse -->
<script defer src="app.js"></script>

<!-- Async — tải song song, chạy NGAY khi xong (không đảm bảo order) -->
<script async src="analytics.js"></script>

<!-- Inline deferred -->
<script>
  // inline script chạy ngay tại vị trí này (blocking)
  console.log('inline');
</script>
```

### Event timing trong pipeline
```js
// DOMContentLoaded — DOM parse xong, CSSOM có thể chưa xong
document.addEventListener('DOMContentLoaded', () => {
  console.log('DOM ready — elements available');
});

// load — mọi tài nguyên (ảnh, CSS, iframe) load xong
window.addEventListener('load', () => {
  console.log('All resources loaded — images have dimensions');
});
```

### Performance API — measure pipeline
```js
// Navigation timing API
const perf = performance.getEntriesByType('navigation')[0];
console.log({
  dnsLookup: perf.domainLookupEnd - perf.domainLookupStart,
  tcpConnect: perf.connectEnd - perf.connectStart,
  ttfb: perf.responseStart - perf.requestStart, // time to first byte
  domParse: perf.domContentLoadedEventEnd - perf.navigationStart,
  loadComplete: perf.loadEventEnd - perf.navigationStart
});
```

## ✅ Điểm mạnh (khi hiểu pipeline)

1. **Biết vì sao sửa DOM lại "đắt"** — mỗi lần JS đổi DOM/CSSOM có thể kích hoạt layout + paint lại.
2. **Tối ưu đúng chỗ** — batch thay đổi, hạn chế reflow, dùng `content-visibility`... trở nên có căn cứ.
3. **Hiểu thứ tự load** — `<script>` (chặn parsing) vs `defer`/`async` — quyết định đúng khi tối ưu FCP.
4. **Nối logic với sự kiện** — vì sao phải đợi `DOMContentLoaded`/`load` trước khi DOM manipulation.
5. **Đọc được CDP/Lighthouse reports** — "render-blocking resources", "layout shift" giờ có ý nghĩa cụ thể.
6. **Debug FOUC (Flash of Unstyled Content)** — hiểu CSSOM delay so với DOM.
7. **Optimize Critical Rendering Path** — minimize blocking resources, inline critical CSS.

## ⚠️ Lưu ý / Hạn chế

1. **Render Tree ≠ DOM Tree** — Render Tree chỉ chứa phần tử hiển thị; phần `display:none` có trong DOM nhưng không vào render.
2. **JS đang parse bị chặn** — `<script>` ở giữa trang làm **dừng HTML parser** — tài nguyên nặng làm chậm trang.
3. **Cây DOM đầy đủ node text (xuống dòng)** — dễ làm bạn đếm sai `childNodes`.
4. **Canvas/SVG/quy trình "server-side rendering" không đi theo toàn bộ chuỗi này** theo cách giống hệt.
5. **Chrome DevTools Performance panel** — record có thể ảnh hưởng kết quả do overhead recording.
6. **Pipeline khác nhau giữa browser** — Firefox (Gecko), Safari (WebKit) có implementation detail khác.

## 💡 Khi nào dùng — Tình huống thực tến

1. **Tối ưu tốc độ tải trang** — sắp xếp nơi đặt `<script>`, nén ảnh, giảm CSS render-blocking.
2. **Giải thích hiện tượng "trang nhấp nháy"** — FOUC do CSSOM tới sau DOM.
3. **Debug layout/paint** — dùng Performance panel xem các "Layout/Paint" tasks trong một thao tác.
4. **Trước khi bàn đến CSR vs SSR** — nắm pipeline là tiền đề hiểu vì sao SSR thân thiện với SEO.
5. **Trong phỏng vấn frontend** — câu "browser renders HTML như thế nào" cực kỳ kinh điển.
6. **Optimize Core Web Vitals** — LCP, FID, CLS đều liên quan đến rendering pipeline.
7. **Debug "white screen of death"** — script error block rendering → hiểu pipeline để tìm root cause.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Script placement impact
```html
<!DOCTYPE html>
<html>
<head>
  <!-- ❌ BAD: script chặn parse -->
  <script src="heavy.js"></script>
  
  <!-- ✅ GOOD: defer — tải song song, chạy sau DOM -->
  <script defer src="app.js"></script>
  
  <!-- ✅ GOOD: async — tải song song, chạy ngay khi xong (cho analytics) -->
  <script async src="analytics.js"></script>
</head>
<body>
  <h1>Content</h1>
  <p>More content...</p>
</body>
</html>
```

### Ví dụ 2: Event timing trong pipeline
```html
<script>
  // Inline script — chạy ngay tại đây (blocking)
  console.log('1. Inline script');
  
  document.addEventListener('DOMContentLoaded', () => {
    console.log('2. DOMContentLoaded — DOM parse xong');
  });
  
  window.addEventListener('load', () => {
    console.log('3. Load — mọi tài nguyên xong');
  });
</script>
```

### Ví dụ 3: Batch DOM changes để tránh nhiều reflow
```js
// ❌ BAD — mỗi lần append触发 reflow
const ul = document.querySelector('ul');
for (let i = 0; i < 1000; i++) {
  const li = document.createElement('li');
  li.textContent = `Item ${i}`;
  ul.appendChild(li); // 1000 lần reflow
}

// ✅ GOOD — DocumentFragment, 1 reflow
const fragment = document.createDocumentFragment();
for (let i = 0; i < 1000; i++) {
  const li = document.createElement('li');
  li.textContent = `Item ${i}`;
  fragment.appendChild(li);
}
ul.appendChild(fragment); // 1 lần reflow
```

### Ví dụ 4: Avoid layout thrashing
```js
const boxes = document.querySelectorAll('.box');

// ❌ BAD — read then write in same loop → layout thrashing
boxes.forEach(box => {
  const height = box.offsetHeight; // read → trigger layout
  box.style.height = (height * 2) + 'px'; // write → trigger layout
});

// ✅ GOOD — batch reads then batch writes
const heights = [...boxes].map(box => box.offsetHeight); // all reads first
boxes.forEach((box, i) => {
  box.style.height = (heights[i] * 2) + 'px'; // then all writes
});
```

### Ví dụ 5: Critical CSS inline
```html
<head>
  <!-- Inline critical CSS — above-the-fold styles -->
  <style>
    .hero { height: 400px; background: blue; }
    .nav { position: fixed; top: 0; width: 100%; }
  </style>
  <!-- Non-critical CSS — load async -->
  <link rel="preload" href="styles.css" as="style" onload="this.rel='stylesheet'">
  <noscript><link rel="stylesheet" href="styles.css"></noscript>
</head>
```

### Ví dụ 6: Measure rendering performance
```js
// Performance API — measure task duration
performance.mark('start-render');

// ... DOM operations ...

performance.mark('end-render');
performance.measure('render-duration', 'start-render', 'end-render');

const measures = performance.getEntriesByName('render-duration');
console.log(`Render took: ${measures[0].duration.toFixed(2)}ms`);

// Long task detection (>50ms)
const entries = performance.getEntriesByType('longtask');
entries.forEach(entry => {
  console.log(`Long task: ${entry.duration.toFixed(2)}ms at ${entry.startTime}`);
});
```

### Ví dụ 7: Understanding FOUC
```css
/* CSS loaded after DOM parse → FOUC: content hiện rồi mới style */
body { opacity: 0; }
body.loaded { opacity: 1; }
```
```js
// Hide content until CSS loaded
document.addEventListener('DOMContentLoaded', () => {
  document.body.style.opacity = '0';
});
window.addEventListener('load', () => {
  document.body.classList.add('loaded'); // CSS transition fade in
});
```

## 🔬 So sánh với alternatives

| Approach | Kiểm soát | Complexity | Performance |
|---|---|---|---|
| **Understanding pipeline** | High | Medium | Optimal |
| **Blind DOM manipulation** | Low | Low | Poor (reflows) |
| **Framework Virtual DOM** | Medium | High | Good (batched) |
| **Server-side rendering** | High | High | Best FCP |
| **Static HTML** | N/A | Low | Best possible |

## 📊 Performance & Best Practices

- **Place scripts at bottom** hoặc dùng `defer` — tránh chặn HTML parsing.
- **Batch DOM writes** — gộp nhiều changes thành 1 reflow cycle.
- **Read before write** — avoid layout thrashing (read all offsets first, then write).
- **Use `requestAnimationFrame`** cho animation — sync với browser paint cycle.
- **Minimize reflow scope** — thay đổi element level thấp nhất có thể (leaf nodes).
- **CSS over JS animation** — GPU-accelerated CSS transforms (`translate`, `scale`) nhanh hơn JS style changes.
- **Content-visibility** — `content-visibility: auto` skip rendering off-screen content.
- **Measure before optimizing** — dùng DevTools Performance panel để identify real bottlenecks.

## 🔗 Liên kết chéo

- Xem thêm: `18_dom-apis/01_dom-basics/01_f8-basic-dom/1_dom-api/` — DOM basics.
- Xem thêm: `18_dom-apis/01_dom-basics/01_f8-basic-dom/12_EventListener/` — DOMContentLoaded timing.
- Xem thêm: `17_memory-management/` — memory implications của DOM operations.
- Xem thêm: `19_browser-devtools/02_devtools-performance/` — performance profiling.
- Ảnh minh họa: `DOM.png`, `HTML-Parsing.png`, `Painting-Phase-1.png`, `node-structure-in-dom.png`.
- Tài liệu thêm: [web.dev/articles/critical-rendering-path](https://web.dev/articles/critical-rendering-path/render-tree-construction).
