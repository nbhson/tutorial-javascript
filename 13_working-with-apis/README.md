# Làm việc với APIs (Working with APIs)

## 🔑 Khái niệm

**API (Application Programming Interface)** là "cổng giao tiếp" giữa các phần mềm. Trong phát triển web, chúng ta thường dùng **REST API**: gửi HTTP request tới server để **tạo / đọc / sửa / xóa** dữ liệu theo các phương thức:

| Phương thức | Mục đích | Ví dụ |
|-------------|----------|-------|
| `GET` | Đọc dữ liệu (Read) | lấy danh sách khóa học |
| `POST` | Tạo mới (Create) | thêm khóa học |
| `PUT` / `PATCH` | Cập nhật (Update) | sửa toàn bộ / sửa một phần |
| `DELETE` | Xóa (Delete) | xóa khóa học |

Để gọi API từ JS có các công cụ chính:

- **`fetch()`** — hiện đại, dựa trên Promise, cú pháp gọn.
- **`XMLHttpRequest` (XHR)** — tiền thân của fetch, dựa trên callback.
- **JSON Server** — giả lập REST server bằng file JSON để phát triển/prototype.
- **Postman / Thunder Client** — kiểm thử API bằng giao diện mà không cần viết code.

## ✅ Điểm mạnh

- Tách frontend và backend: chỉ trao đổi dữ liệu qua HTTP.
- `fetch` + Promise/async-await giúp code gọi API ngắn gọn, dễ lỗi rất rõ ràng.
- JSON Server cho phép làm CRUD đầy đủ mà không cần backend thật.
- Postman kiểm thử nhanh trước khi viết code — tiết kiệm thời gian.
- Service/Worker giúp nâng cao trải nghiệm offline, background sync.

## ⚠️ Lưu ý / Hạn chế

- `fetch` không throw khi server trả lỗi HTTP — phải tự kiểm tra `res.ok`.
- XHR nhiều callback, ít gọn — chỉ nên dùng khi cần tương thích cũ hoặc theo dõi tiến trình.
- JSON Server chỉ là **giả lập** — không đủ cho production thật.
- CORS: gọi API khác origin cần server cho phép.
- Cache, retry, abort request cần xử lý tay.

## 💡 Khi nào dùng

- Mọi ứng dụng cần dữ liệu động từ server: blog, shop, admin panel...
- Prototype nhanh giao diện với JSON Server trước khi có backend.
- Kiểm tra server/API của đồng nghiệp bằng Postman.
- Build PWA có offline trải nghiệm bằng Service Worker.

## 🎯 Ví dụ minh họa

```js
// GET tiêu chuẩn bằng fetch
fetch("https://jsonplaceholder.typicode.com/posts")
  .then((res) => res.json())
  .then((posts) => console.log(posts.length)) // 100
  .catch((err) => console.error(err));
```

## 📚 Tham khảo / Bài tập

- Nhóm này gồm: `01_fetch`, `02_xmlhttprequest`, `03_json-server`, `04_postman`, `05_crud`, `06_service-worker` — đọc theo thứ tự.
- Mỗi folder có `app.js` (+ `index.html`, `server.json` ở các folder dùng json-server).
- Tự thử: sau khi học, viết một trang quản lý khóa học đầy đủ GET/POST/DELETE tự tay.