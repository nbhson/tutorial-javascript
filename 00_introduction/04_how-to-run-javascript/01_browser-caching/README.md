# Browser Caching JavaScript: Nơi lưu trữ & cách hoạt động

## 🔑 Khái niệm

**Browser caching** là việc trình duyệt **lưu lại** các tài nguyên (file JS, CSS, ảnh...) ngay trên máy người dùng sau lần tải đầu tiên, để những lần sau **không cần tải lại từ server**. Đây là lý do quan trọng nhất khiến việc đặt JavaScript ra file `.js` riêng giúp website nhanh hơn: file tĩnh tải một lần, dùng mãi cho đến khi thay đổi.

**Nơi JavaScript được cache:**

- **Memory cache** — lưu trong RAM, truy cập nhanh nhất nhưng dễ bị xóa khi đóng tab/trình duyệt.
- **Disk cache** — lưu trên ổ cứng, bền hơn qua các phiên/trình duyệt khởi động lại.
- **Service Worker cache** — cache có thể lập trình được, cung cấp khả năng chạy **offline**.

**Quy trình hoạt động:**

1. **Lần đầu**: trình duyệt tải JS từ server, lưu vào cache kèm metadata (URL, headers, thời gian), rồi thực thi.
2. **Lần sau**: trình duyệt kiểm tra cache — nếu còn "hợp lệ" theo `Cache-Control`, nó **load từ cache** thay vì gọi server.

**Cache headers quan trọng:**

```http
# Tĩnh, không đổi (1 năm)
Cache-Control: public, max-age=31536000

# Ngắn hạn (1 giờ)
Cache-Control: public, max-age=3600

# Cấm cache (nhạy cảm/dữ liệu người dùng)
Cache-Control: no-cache, no-store
```

**Cache invalidation** — quá trình làm cache "hết hiệu lực" để trình duyệt tải bản mới. Bốn cách phổ biến:

1. **Time-based**: để cache hết hạn sau `max-age`/`expires`.
2. **Versioning/Hashing**: đổi tên file khi nội dung đổi (`main.abc123.js` → `main.def456.js`) → file cũ tự "biến mất", trình duyệt buộc tải file mới.
3. **Must-revalidate / no-cache**: yêu cầu tải lại nếu dữ liệu thay đổi.
4. **Manual purge**: xóa cache thủ công trên server/CDN.

**Cách nhận biết file đã cache** — DevTools → tab **Network**, cột **Size**:

- `(memory cache)` — load từ RAM.
- `(disk cache)` — load từ ổ cứng.
- `(from ServiceWorker)` — load từ service worker.
- Thời gian load `0–1ms` gần như chắc chắn là từ cache; `>100ms` là tải lại từ server.

## ✅ Điểm mạnh

- **Tăng tốc tải trang** rõ rệt: bỏ qua độ trễ mạng ở các lần truy cập sau.
- **Giảm băng thông** của người dùng lẫn chi phí server/CDN.
- **Cải thiện UX** tinh thần "tốc độ" và độ ổn định.
- Kết hợp với build tool (Vite, Angular CLI...) → **tự động invalidation** bằng hash, không cần xóa cache tay.

## ⚠️ Lưu ý / Hạn chế

- **Cache quá "chắc"** khiến người dùng mắc kẹt với phiên bản cũ của app — phải dùng `versioning/hashing` hoặc `no-cache` cho `index.html`.
- Cache **không áp dụng** cho inline script — đó là lý do script ngoài file luôn được khuyến khích.
- `no-store` giúp tránh lưu dữ liệu nhạy cảm nhưng sẽ tốn tải lại nhiều lần.
- Cache đầu tiên (first load) vẫn chậm; caching chỉ phát huy ở các lần sau.

## 💡 Khi nào dùng

- File JS/CSS/ảnh **tĩnh, không đổi** → cache dài hạn (1 năm) kèm hashing khi build.
- `index.html` → **luôn tải mới** (dùng `no-cache`) để dẫn đến các file bản mới.
- Ứng dụng cần chạy offline → Service Worker cache.
- Website nhiều trang dùng chung một bundle `app.js` → hưởng lợi lớn nhất từ caching.

## 🎯 Ví dụ minh họa

```html
<!-- index.html — index luôn mới, file JS có hash để "tự hủy cache" khi đổi -->
<head>
  <script src="app.md4h3kf.js" defer></script>
</head>
```

```js
// app.js (thư mục 01_browser-caching)
console.log("APP");
console.log("APP 2");
console.log("APP 3");
```

## 📚 Tham khảo / Bài tập

- **Quan sát cache thực tế**: mở `index.html` (cùng thư mục) trong trình duyệt, bật DevTools → Network, reload (*⇧⌘R* hoặc *Ctrl+Shift+R* để bỏ qua cache một lần) và so sánh cột Size: lần đầu `app.js` tải từ localhost, lần sau hiện `(disk cache)`/`(memory cache)`.
- Tự thử: 1) sửa nội dung `app.js` rồi reload — nếu vẫn thấy bản cũ trong cache, thử *Hard Reload*; 2) mở tab **Application → Storage → Cache Storage** hoặc **Clear storage** để xem và xóa cache; 3) thêm `Cache-Control` header (cần server nhỏ như `python -m http.server`) và quan sát thay đổi.
- Tài liệu: [MDN — HTTP Caching](https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching).