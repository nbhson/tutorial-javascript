# CRUD hoàn chỉnh với Fetch + JSON Server

## 🔑 Khái niệm

**CRUD** viết tắt của bốn thao tác dữ liệu cơ bản, ánh xạ trực tiếp sang HTTP REST:

| Thao tác | HTTP | Trong ví dụ |
|----------|------|-------------|
| **Create** | `POST` | `addCourses()` — thêm khóa học |
| **Read** | `GET` | `getCourses()` — lấy danh sách |
| **Update** | `PUT` / `PATCH` | (chưa demo trong file, là bài tập của bạn) |
| **Delete** | `DELETE` | `deleteCourse(id)` — xóa khóa học |

Đây là một ứng dụng nhỏ hoàn chỉnh (form nhập `name`, `description`; danh sách khóa học có nút **Xóa**) kết nối với **JSON Server** ở `http://localhost:3000/coures`. Cách tổ chức trong `app.js`:

- `start()` — khởi chạy: load danh sách + gắn sự kiện form.
- `getCourses(callback)` — GET + `callback` render.
- `addCourses(data, callback)` — POST với `Content-Type: application/json` và `body: JSON.stringify(data)`.
- `deleteCourse(id)` — DELETE `courseAPI + "/" + id`, xóa luôn element khỏi DOM.

## ✅ Điểm mạnh

- Mẫu chuẩn cho mọi app quản lý danh sách (to-do, blog, khóa học...).
- Ví dụ điển hình về `headers` và `JSON.stringify` cho POST/DELETE.
- Cập nhật DOM ngay sau khi server phản hồi — luồng dữ liệu thực tế.
- Dễ mở rộng: thêm Update (PUT/PATCH) chỉ vài dòng.

## ⚠️ Lưu ý / Hạn chế

- File demo logic **chỉ có hôm sẵn Create/Read/Delete** — Update (PUT/PATCH) chưa được code.
- `server.json` cần có resource `coures` đúng tên; `app.js` dùng URL phải khớp.
- Các ô input đọc bằng `document.querySelector('input[name="name"]')` — phải trùng `name` trong HTML.
- Chưa có xử lý lỗi chi tiết (nếu server chưa chạy, mọi fetch đều reject).
- Đặt hàng: chạy JSON Server rồi mới mở `index.html`.

## 💡 Khi nào dùng

- App quản lý danh sách dữ liệu kết nối REST backend.
- Học cách dùng POST/DELETE với fetch + JSON thực tế.
- Làm nền tảng trước khi học framework (React/Vue) có sidebar state.

## 🎯 Ví dụ minh họa

```js
var courseAPI = "http://localhost:3000/coures";

// READ
function getCourses(callback) {
  fetch(courseAPI).then((res) => res.json()).then(callback);
}

// CREATE
function addCourses(data, callback) {
  fetch(courseAPI, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  })
    .then((res) => res.json())
    .then(callback);
}

// DELETE
function deleteCourse(id) {
  fetch(courseAPI + "/" + id, {
    method: "DELETE",
    headers: { "Content-Type": "application/json" },
  }).then(() => console.log("deleted", id));
}

getCourses((courses) => console.log(courses)); // danh sách từ server
```

## 📚 Tham khảo / Bài tập

- Chạy `json-server --watch server.json` trong folder `05_crud`, mở `index.html` — form "Create" thêm khóa học, nút "Xóa" xóa khóa học, danh sách render vào `#list-course`.
- Đọc kỹ `app.js` (toàn bộ luồng `start → getCourses → handleFormAdd → addCourses → deleteCourse`) và `index.html` (form + `#list-course`).
- Tự thử: **viết thêm `updateCourse(id, data)`** dùng phương thức `PUT` hoặc `PATCH`, và đổi `deleteCourse` từ xóa element thành gọi lại `getCourses(renderCourse)` để đồng bộ DOM với server.