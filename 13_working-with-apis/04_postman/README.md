# Postman — Kiểm thử API không cần viết code

## 🔑 Khái niệm

**Postman** là công cụ (GUI) để **gửi HTTP request và xem response** — bạn test API mà không cần viết code, rất hữu ích để kiểm tra server trước khi tích hợp vào frontend. Ngoài Postman, **Thunder Client** (extension VS Code) cũng làm việc tương tự.

Giao diện Postman bạn cần biết:

- **Method** (GET / POST / PUT / PATCH / DELETE).
- **URL** — ví dụ `http://localhost:3000/coures`.
- **Headers** — ví dụ `Content-Type: application/json`.
- **Body** — dữ liệu JSON cho POST/PUT/PATCH.
- **Send** → xem **Status code**, **JSON response**, thời gian.

Vì Postman chỉ "gõ tay", nó đi kèm với **JSON Server**: mở `server.json` làm REST fake ở local, rồi dùng Postman bắn request về đó để test CRUD.

## ✅ Điểm mạnh

- Kiểm thử server **không cần code** — nhanh, trực quan.
- Lưu lịch sử request, collections, môi trường biến để tái dùng.
- Xem rõ status code, header, body — hỗ trợ debug CORS/lỗi server.
- Làm tài liệu API (Export collection, đọc được OpenAPI/Swagger).
- Hoàn hảo phối hợp JSON Server để phát triển frontend độc lập.

## ⚠️ Lưu ý / Hạn chế

- Chỉ kiểm thử **thủ công** — chưa tự động hóa (cần Newman/scripts).
- Không thay thế frontend fet — chỉ kiểm tra "phía server OK trong mắt Postman".
- Phải nhớ đúng method/body — gõ sai sẽ ra lỗi gây hiểu lầm.
- Nếu server chưa chạy (JSON Server), mọi request đều connection refused.

## 💡 Khi nào dùng

- Kiểm tra một endpoint mới trước khi viết code gọi.
- Xem response shape để biết trường nào render trong UI.
- Trao đổi với backend: gửi request mẫu, minh chứng lỗi.
- Demo/tài liệu API cho team.

## 🎯 Ví dụ minh họa

Với JSON Server chạy ở `http://localhost:3000` và `server.json` chứa resource `coures`:

```
GET    http://localhost:3000/coures        → danh sách (200)
GET    http://localhost:3000/coures/1      → chi tiết id=1
POST   http://localhost:3000/coures        body: {"name":"React","description":"SE","id":6}
PUT    http://localhost:3000/coures/1      body: {..., "name":"HTML nâng cao"}
PATCH  http://localhost:3000/coures/1      body: {"description":"đã sửa"}
DELETE http://localhost:3000/coures/1
```

## 📚 Tham khảo / Bài tập

- Đọc `04_postman/app.js`: file chỉ chứa **comment nhắc lại CRUD** (Create=POST, Read=GET, Update=PUT/PATCH, Delete=DELETE) và ghi chú THUNDER CLIENT — hướng dẫn dùng tool để test.
- Mở `server.json` (resource `coures` với 5 khóa học) và `index.html`.
- Tự thử: chạy JSON Server, dùng **Thunder Client** (VS Code) hoặc Postman để POST thêm 1 khóa học, xóa khóa cũ, rồi mở lại `server.json` xem file đã bị thay đổi như thế nào.