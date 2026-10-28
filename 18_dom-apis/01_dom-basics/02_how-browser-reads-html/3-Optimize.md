# Tối ưu tốc độ tải trang — CSS & JS Delivery

> Bài này trả lời: làm sao để trình duyệt parse HTML và hiển thị nội dung **nhanh nhất có thể**. Nối tiếp bài `1-How-Browser-Reads-HTML` (browser parse HTML thế nào) và `2-Node` (cây node được tạo ra).

## Bối cảnh: render blocking là gì

Từ bài trước bạn đã biết: browser đọc HTML tuần tự từ trên xuống, gặp tag thì tạo node. Nhưng có 2 loại tài nguyên **chặn quá trình này**:

1. **CSS bên ngoài** — trình duyệt không render bất cứ thứ gì cho đến khi tải và xử lý xong toàn bộ CSS (nếu không, người dùng sẽ thấy trang "nháy" không style).
2. **JavaScript** — script có thể thay đổi DOM qua `document.write()` hoặc thao tác DOM khác, nên parser phải **dừng** cho đến khi script tải xong và chạy xong (trừ khi bạn báo hiệu khác — xem phần async/defer).

Mục tiêu tối ưu hóa: **giảm khối lượng dữ liệu cần thiết để hiển thị nội dung đầu tiên** (HTML markup, images, CSS, JavaScript). Một số cách làm:

- Cấu trúc HTML để tải nội dung quan trọng trong màn hình đầu tiên trước tiên:
  - Tải nội dung chính của trang trước. Cấu trúc trang sao cho phản hồi ban đầu từ máy chủ gửi dữ liệu cần thiết để hiển thị ngay phần quan trọng, và trì hoãn phần còn lại.
  - Điều này có thể nghĩa là bạn phải chia CSS thành hai phần: phần nội tuyến **chịu trách nhiệm tạo kiểu cho phần hiển thị đầu tiên** và phần **có thể trì hoãn**.
- Giảm lượng dữ liệu được sử dụng bởi tài nguyên:
  - Minify HTML, CSS, JS
  - Cân nhắc dùng CSS thay vì hình ảnh khi có thể (gradient, border, icon SVG)
  - Bật nén (gzip/brotli) trên server

## Tối ưu CSS Delivery

**Tổng quan**: Trước khi trình duyệt có thể hiển thị nội dung, nó phải xử lý tất cả thông tin về kiểu dáng và bố cục cho trang hiện tại. Do đó, trình duyệt sẽ chặn hiển thị cho đến khi các bảng định kiểu bên ngoài được tải xuống và xử lý — điều này có thể yêu cầu nhiều lần round-trip và trì hoãn thời gian hiển thị lần đầu (First Paint / LCP).

**Khuyến nghị**

- Nếu tài nguyên CSS bên ngoài nhỏ, bạn có thể chèn trực tiếp vào tài liệu HTML (inline):
  ```html
  <style>/* CSS critical — vài KB đầu */</style>
  ```
- Lưu ý rằng nếu tệp CSS lớn, việc nội tuyến toàn bộ có thể khiến PageSpeed Insights cảnh báo phần head quá lớn.
- Với CSS lớn: xác định và **nội tuyến chỉ phần CSS cần cho màn hình đầu tiên** (critical CSS), trì hoãn phần còn lại:
  ```html
  <link rel="preload" href="styles.css" as="style" onload="this.rel='stylesheet'">
  <noscript><link rel="stylesheet" href="styles.css"></noscript>
  ```
- Don't inline large data URIs — data URI làm phình HTML, mất khả năng cache riêng của CSS.
- Don't inline CSS attributes (style="...") rải rác trong markup — khó cache, khó maintain.

Mẹo thực chiến: dùng tool như `critters` (build-time) hoặc Lighthouse để tìm critical CSS thay vì tự đoán.

## Tối ưu JS Delivery

**Tổng quan**: Bất kỳ tập script nào cũng có thể chèn HTML của riêng nó qua `document.write()` hoặc thao tác DOM. Điều này ngụ ý parser phải **đợi** script tải xuống và thực thi trước khi parse tiếp phần còn lại một cách an toàn. *Câu hỏi lớn: bạn nên đặt thẻ script ở đâu và tại sao?*

**Khuyến nghị**: Cách tiếp cận cũ là đặt thẻ `script` ở **cuối body** — đảm bảo parser không bị chặn cho tới cuối.

- **Cách này có vấn đề riêng**: browser không thể bắt đầu tải script cho tới khi toàn bộ tài liệu đã parse xong. Với site lớn, script/stylesheet nặng, việc bắt đầu tải script càng sớm càng tốt là rất quan trọng.
- Giải pháp tối ưu: trình duyệt bắt đầu **tải xuống script càng sớm càng tốt**, đồng thời vẫn parse tiếp phần còn lại của tài liệu.

> Cách tiếp cận hiện đại: các browser hỗ trợ thuộc tính `async` và `defer`. Các thuộc tính này báo cho browser biết rằng việc tiếp tục parse trong khi script đang được tải xuống là an toàn.

### So sánh 3 cách đặt script

```html
<!-- 1. Thường — CHẶN parser: tải xong → chạy → mới parse tiếp -->
<script src="app.js"></script>

<!-- 2. async — KHÔNG chặn parse, chạy NGAY khi tải xong, thứ tự KHÔNG đảm bảo -->
<script async src="analytics.js"></script>

<!-- 3. defer — KHÔNG chặn parse, chạy SAU khi parse xong, đúng thứ tự tài liệu -->
<script defer src="app.js"></script>
```

| | Thường | `async` | `defer` |
|---|---|---|---|
| Chặn parsing HTML | Có | Không | Không |
| Thời điểm thực thi | Ngay khi tải xong | Ngay khi tải xong | Sau khi DOM parse xong (trước `DOMContentLoaded`) |
| Thứ tự thực thi | Theo thứ tự tài liệu | **Không đảm bảo** | **Đúng thứ tự tài liệu** |
| Truy cập DOM an toàn? | Có (nếu cuối body) | Không đảm bảo | Có |
| Phù hợp | Script nhỏ phụ thuộc DOM | Analytics, tracking, script độc lập | App chính, script có phụ thuộc lẫn nhau |

### async

- Các tập script có thuộc tính `async` được thực thi không đồng bộ.
- Script được thực thi ngay khi tải xong.
- Điều này ngụ ý: có thể script 2 được tải và thực thi **trước** script 1.

```html
<script type="text/javascript" src="path/to/script1.js" async></script>
<script type="text/javascript" src="path/to/script2.js" async></script>
```

Vì thế: **đừng dùng `async` cho các script phụ thuộc lẫn nhau** (ví dụ script A định nghĩa global mà script B dùng). Nó phù hợp cho script độc lập — analytics, quảng cáo, widget xã hội.

### defer

- Các tập script có thuộc tính `defer` được thực thi **theo thứ tự** trong tài liệu (script 1 trước, script 2 sau), và không chặn browser.
- Script trì hoãn chỉ được thực thi sau khi toàn bộ tài liệu được parse (trước sự kiện `DOMContentLoaded`).
- Vì chạy sau khi DOM đã parse xong, script `defer` **truy cập DOM an toàn** mà không cần bọc trong `DOMContentLoaded`.

```html
<script type="text/javascript" src="path/to/script1.js" defer></script>
<script type="text/javascript" src="path/to/script2.js" defer></script>
```

Ghi chú về browser cũ: một số phiên bản IE cũ (≤9) có thể thực thi script `defer` sai thứ tự. Ngày nay (2026) đây chủ yếu là kiến thức lịch sử — `defer` và `async` được hỗ trợ đều khắp nơi từ lâu.

### type="module" — defer miễn phí

```html
<script type="module" src="app.js"></script>
```

ES modules mặc định hành xử giống `defer`: không chặn parse, thực thi sau khi tài liệu parse xong, đúng thứ tự. Đây là lựa chọn mặc định của code hiện đại (xem `16_modules/`).

## Ví dụ: đo lường trước — tối ưu sau

Đừng tối ưu mù quáng — đo bằng DevTools trước:

```js
// Navigation Timing — xem các mốc thời gian tải trang
window.addEventListener("load", () => {
  const nav = performance.getEntriesByType("navigation")[0];
  console.log("DNS lookup:", nav.domainLookupEnd - nav.domainLookupStart, "ms");
  console.log("TTFB:", nav.responseStart - nav.requestStart, "ms");
  console.log("DOM parse+execute:", nav.domContentLoadedEventEnd - nav.responseStart, "ms");
});

// Resource Timing — tài nguyên nào chậm nhất?
performance.getEntriesByType("resource")
  .sort((a, b) => b.duration - a.duration)
  .slice(0, 5)
  .forEach((r) => console.log(r.name.split("/").pop(), Math.round(r.duration), "ms"));
```

## Resource Hints — nói với browser trước

Browser có thể làm việc hiệu quả hơn nếu bạn **nói trước** cho nó biết sắp cần gì:

```html
<!-- preload: tải sớm, ưu tiên cao — dùng cho font, CSS critical, JS entry -->
<link rel="preload" href="/fonts/main.woff2" as="font" crossorigin>
<link rel="preload" href="/css/critical.css" as="style">

<!-- prefetch: tải khi rảnh — dùng cho tài nguyên trang kế tiếp -->
<link rel="prefetch" href="/page2.js">

<!-- preconnect: thiết lập kết nối TCP/TLS sớm — dùng cho domain bên thứ 3 -->
<link rel="preconnect" href="https://cdn.example.com">
```

Quy tắc chọn nhanh: `preload` cho thứ bạn cần **ngay lần này** (font hiển thị text), `prefetch` cho thứ **lần sau** (trang kế), `preconnect` cho tài nguyên bên thứ 3 (CDN, API).

## Image lazy loading và modern formats

```html
<!-- lazy loading native — trình duyệt tự hoãn cho đến khi gần viewport -->
<img src="photo.jpg" loading="lazy" alt="...">

<!-- fetchpriority: cho trình duyệt biết ưu tiên -->
<img src="hero.webp" fetchpriority="high" alt="..."> <!-- LCP image — ưu tiên cao nhất -->

<!-- picture: serve format phù hợp browser -->
<picture>
  <source srcset="image.avif" type="image/avif">
  <source srcset="image.webp" type="image/webp">
  <img src="image.jpg" alt="...">
</picture>
```

**Thứ tự ưu tiên LCP (Largest Contentful Paint):**

1. Đặt `fetchpriority="high"` trên ảnh hero (LCP element)
2. `preload` ảnh này nếu nó nằm trong `<head>` style CSS
3. `loading="eager"` (mặc định) cho LCP, `loading="lazy"` cho các ảnh dưới fold
4. Chuyển sang WebP/AVIF để giảm size mà không giảm chất lượng

## HTTP/2 và bundle strategy cũ

Với HTTP/2 (hầu hết server hiện đại), việc gộp nhiều file CSS/JS thành 1 bundle lớn **đôi khi chậm hơn** việc tải nhiều file nhỏ (vì bundle lớn bị head-of-line blocking). Khuyến nghị hiện đại:

- Để build tool (Vite, Webpack) quyết định bundle strategy (chúng tự split code thông minh)
- Vite mặc định dùng native ESM, chia chunk theo dynamic import — không cần manual bundle
- Mục tiêu: **code splitting theo route/feature** — mỗi trang chỉ tải code nó cần

## Quy trình tối ưu thực chiến

```
1. Lighthouse → identify LCP, CLS, FID (Core Web Vitals)
   ↓
2. Đo TTFB (server response time) → nếu > 600ms: tối ưu server/database trước
   ↓
3. Sửa render-blocking resources (preload, inline critical CSS, async/defer JS)
   ↓
4. Optimize images (lazy load, modern format, srcset)
   ↓
5. Bật nén (brotli/gzip) → kiểm tra bằng DevTools → Network → transferred size
   ↓
6. Đo lại Lighthouse → so sánh score
```

## Checklist tự kiểm tra

- [ ] Giải thích được vì sao CSS chặn render và JS chặn parse
- [ ] Phân biệt `async` vs `defer` (thời điểm chạy, thứ tự, an toàn DOM)
- [ ] Biết `type="module"` mặc định như `defer`
- [ ] Biết khái niệm critical CSS và preload
- [ ] Dùng được Performance/Lighthouse để đo thay vì đoán
- [ ] Biết khi nào dùng preload vs prefetch vs preconnect
- [ ] Thêm được `fetchpriority="high"` vào ảnh LCP

## References

- Tổng quan tối ưu page speed: https://gist.github.com/nishantmendiratta/db09531f80803465da36f0d43c3e58ac
- MDN — script async/defer: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/script
- web.dev — Render-blocking CSS: https://web.dev/articles/render-blocking-css
- web.dev — Optimize LCP: https://web.dev/articles/optimize-lcp
- web.dev — Resource Hints: https://web.dev/articles/prefetch-seo-audit
