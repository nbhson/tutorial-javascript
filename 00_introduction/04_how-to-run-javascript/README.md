# Cách chạy JavaScript trong trình duyệt

## 🔑 Khái niệm

Để trình duyệt thực thi JavaScript, bạn phải đưa mã JS vào trang HTML. Có **3 cách chính**:

1. **Inline trong `<head>`** — thẻ `<script>` nằm trong phần `<head>`:

```html
<head>
  <script>
    alert("Hôm nay là " + new Date());
  </script>
</head>
```

   → Chạy **trước khi** nội dung `<body>` được render (render-blocking). Phù hợp để đặt sẵn hàm/biến dùng sau, hoặc các script analytics cần tải sớm. **Lưu ý:** tại thời điểm này DOM của `<body>` chưa tồn tại, nên `document.getElementById(...)` sẽ trả về `null`.

2. **Inline trong `<body>`** — đặt thẻ `<script>` ở cuối body, ngay trước `</body>`:

```html
<body>
  ...nội dung...
  <script>
    document.body.innerHTML = "<h1>" + new Date() + "</h1>";
  </script>
</body>
```

   → Trình duyệt **tạm dừng render** tại điểm gặp `<script>` để thực thi rồi tiếp tục. Đặt cuối body giúp người dùng thấy nội dung trước, nhưng script lớn vẫn gây gián đoạn.

3. **File `.js` bên ngoài** (best practice) — dùng thuộc tính `src`:

```html
<body>
  <script src="js/script.js" defer></script>
</body>
```

   → Tách biệt cấu trúc (HTML), trình bày (CSS), hành vi (JS). Một file dùng được cho nhiều trang, dễ bảo trì, và quan trọng nhất là được **browser caching**.

**Thuộc tính `defer` vs `async` (chỉ dùng với script bên ngoài):**

- `defer`: tải song song background, **chỉ chạy sau khi** HTML được phân tích xong, và **giữ đúng thứ tự** xuất hiện. → chọn cho script phụ thuộc thứ tự.
- `async`: tải song song background nhưng **chạy ngay khi tải xong**, thứ tự không đảm bảo. → hợp cho script độc lập (analytics, quảng cáo).

**Hiệu suất tóm tắt:**

| Phương pháp | Render-blocking? | Caching? | Khuyến nghị |
|-------------|------------------|----------|--------------|
| Inline `<head>` | Có (toàn trang) | Không | Tránh trừ khi script cực nhỏ |
| Inline cuối `<body>` | Có (từng điểm) | Không | Chấp nhận được cho script nhỏ |
| File `.js` + `defer` | Không (nếu dùng defer) | Có | **Khuyến nghị** |

**Cách chạy nhanh nhất để luyện tập:** mở *Developer Tools* (F12) → tab *Console*, gõ JavaScript trực tiếp — không cần file nào. Debug lỗi phổ biến: "Cannot read properties of null" (script chạy trước DOM) → đưa script xuống cuối body + `defer`; "Uncaught SyntaxError" → thiếu ngoặc `()`, `{}`, `""`; script tải lỗi 404 → kiểm tra tab *Network* và đường dẫn `src`.

## ✅ Điểm mạnh

- Chạy thử tức thì bằng Console mà không cần dựng project.
- File `.js` tách biệt giúp code sạch, dễ bảo trì, dễ tái sử dụng nhiều trang.
- `defer` cho phép tải không blocking → trang hiển thị nhanh, "perceived performance" tốt.
- Browser caching giảm băng thông và thời gian tải ở các lần truy cập sau.
- DevTools là công cụ debug đủ mạnh để truy tìm hầu hết lỗi thường gặp.

## ⚠️ Lưu ý / Hạn chế

- Script trong `<head>` chạy khi chưa có DOM → gọi DOM sẽ lỗi `null`.
- Không đặt script block trong `<head>` nếu không cần thiết — nó **chặn render** cả trang.
- `async` không giữ thứ tự thực thi giữa các script — đừng dùng cho script đặt trước script phụ thuộc nó.
- Nhiều thẻ `<script>` được tải **tuần tự** (trừ khi có `defer`/`async`), kéo dài thời gian hoàn tất.

## 💡 Khi nào dùng

- Xác thực form ngay khi gõ hoặc khi submit (dừng submit nếu sai).
- Dark mode toggle: thêm/bớt class bằng JavaScript + CSS.
- Cập nhật nội dung động (hiển thị ngày giờ, đồng hồ, giỏ hàng) mà không reload trang.
- Đặt script analytics / quảng cáo (dùng `async`).

## 🎯 Ví dụ minh họa

```html
<!-- index.html — cách chuẩn hiện đại -->
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>Chạy JS</title>
  </head>
  <body>
    <button id="toggle">Đổi chế độ tối</button>
    <h1 id="title">Xin chào</h1>
    <script src="app.js" defer></script>
  </body>
</html>
```

```js
// app.js
console.log("Script ngoài file, chạy sau khi DOM sẵn sàng").

const btn = document.getElementById("toggle");
btn.addEventListener("click", () =>
  document.body.classList.toggle("dark")
);
```

## 📚 Tham khảo / Bài tập

- Bài con `01_browser-caching/` gồm `index.html` + `app.js` (trong đó `app.js` chỉ in `console.log('APP')`...) để thực hành cache: mở file lên trình duyệt, vào DevTools → Network, reload để thấy file được load từ `(disk cache)` / `(memory cache)`.
- Tự thử: 1) di chuyển thẻ `<script>` lên `<head>` không có `defer` và quan sát khác biệt; 2) thêm `defer` vào rồi so sánh; 3) viết một script ngoài file đổi màu nền khi click và dùng F12 → Console tìm lỗi khi cần.
- Tài liệu gốc tham khảo: [DigitalOcean — How To Add JavaScript to HTML](https://www.digitalocean.com/community/tutorials/how-to-add-javascript-to-html).