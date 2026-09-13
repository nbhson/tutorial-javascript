# JSON Server — Giả lập REST API

## 🔑 Khái niệm

**JSON Server** là một công cụ chạy bằng Node.js, biến một **file JSON** thành một **REST API giả lập** (fake REST server) — phục vụ mục đích **prototyping / phát triển frontend** mà không cần backend thật.

Cách dùng:

```bash
npm i -g json-server        # cài global (hoặc npx json-server --watch server.json)
json-server --watch server.json --port 3000
```

Với file `server.json`:

```json
{
  "coures": [
    { "name": "HTML", "description": "Free", "id": 1 },
    { "name": "CSS", "description": "Free", "id": 2 }
  ]
}
```

Sau khi chạy, mỗi khóa cấp cao trong JSON trở thành một **resource**:

- `GET http://localhost:3000/coures` → toàn bộ mảng.
- `GET http://localhost:3000/coures/1` → phần tử theo id.
- `POST /coures`, `PUT /coures/1`, `PATCH /coures/1`, `DELETE /coures/1` → CRUD tự động.

## ✅ Điểm mạnh

- Tạo full-CRUD API chỉ trong vài giây, không viết backend.
- Dữ liệu trong `server.json` thay đổi trực quan được.
- Hỗ trợ filter, sort, paginate (`?_limit=2`, `?_sort=name`...).
- Lý tưởng để học fetch/CRUD trước khi gặp backend thật.
- Chạy localhost, không tốn chi phí cloud.

## ⚠️ Lưu ý / Hạn chế

- Chỉ là **giả lập** — dữ liệu lưu file, không chạy được ở production.
- Mỗi resource cần một khóa ở cấp cao nhất của JSON (ví dụ `"coures"`).
- Tự generate id nếu bạn không cung cấp — cần để ý khi POST.
- Tên resource phải khớp URL trong code (folder dùng `coures`, đừng gõ `courses`).

## 💡 Khi nào dùng

- Học CRUD: GET/POST/PUT/PATCH/DELETE bằng fetch.
- Dựng prototype UI trước khi backend chính thức có.
- Demo tính năng frontend khi chưa có server.

## 🎯 Ví dụ minh họa

```bash
# Chạy server từ folder 03_json-server
npx json-server --watch server.json --port 3000
```

```js
var postApi = "http://localhost:3000/coures";

fetch(postApi)
  .then((res) => res.json())
  .then((courses) => console.log(courses)) // [{name:"HTML",...}, ...]
  .catch((err) => console.error(err));
```

## 📚 Tham khảo / Bài tập

- File `server.json` trong folder chứa resource `coures` với 3 khóa học HTML/CSS/Javascript.
- Cài và chạy `json-server --watch server.json`, mở `03_json-server/index.html` (gọi `app.js` fetch `http://localhost:3000/coures`) — nhớ cài server trước.
- Tự thử: thêm khóa học mới bằng `POST`, thử truy cập `http://localhost:3000/coures/1` và `?name=HTML` để thấy filter hoạt động.