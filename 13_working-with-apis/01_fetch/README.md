# Fetch API

## 🔑 Khái niệm

**Fetch API** là cách hiện đại để gọi HTTP từ JavaScript. `fetch(url, options)` nhận URL (+ tùy chọn `method`, `headers`, `body`...) và trả về một **Promise** — kết quả là object `Response`.

Luồng xử lý chuẩn:

```js
fetch(url)            // → Promise<Response>
  .then((res) => res.json()) // parse thân dữ liệu (cũng là promise)
  .then((data) => ...)       // dùng dữ liệu
  .catch((err) => ...);      // bắt lỗi mạng
```

`res.json()` đọc toàn bộ thân response và chuyển thành object từ JSON. Các bước nối tiếp nhau qua promise chain — cùng pattern như khi gọi `Promise.all`.

> ⚠️ **Quan trọng:** `fetch` chỉ trả lỗi khi **mạng hỏng**. HTTP lỗi (404, 500) vẫn resolve bình thường — bạn phải tự kiểm tra `res.ok` / `res.status`.

## ✅ Điểm mạnh

- Promise-based → kết hợp tốt với async/await, `Promise.all`.
- Cú pháp ngắn gọn, dễ đọc so với XMLHttpRequest.
- Hỗ trợ mọi phương thức HTTP (GET, POST, PUT, PATCH, DELETE) qua `options`.
- Được hỗ trợ rộng rãi trên browser và Node.js hiện đại.
- Dễ lấy nhiều nguồn cùng lúc bằng `Promise.all([...])`.

## ⚠️ Lưu ý / Hạn chế

- Không tự xử lý lỗi HTTP: phải check `res.ok` rồi `throw`.
- Phải chờ `res.json()` (chính nó là promise) trước khi dùng dữ liệu.
- Trình duyệt cũ không hỗ trợ (có polyfill).
- Default không gửi cookie trên cross-origin (cần `credentials`).

## 💡 Khi nào dùng

- Tải danh sách / chi tiết dữ liệu từ REST API.
- Gửi dữ liệu lên server (POST/PUT/PATCH/DELETE).
- Gọi nhiều endpoint song song và gộp kết quả.

## 🎯 Ví dụ minh họa

```js
const postApi = "https://jsonplaceholder.typicode.com/posts";
const todoApi = "https://jsonplaceholder.typicode.com/todos";

fetch(postApi)
  .then((res) => res.json())
  .then((posts) => console.log("posts:", posts.length))   // 100
  .catch((err) => console.error(err));

// Fetch nhiều nguồn song song
Promise.all([
  fetch(postApi).then((res) => res.json()),
  fetch(todoApi).then((res) => res.json()),
])
  .then(([posts, todos]) => console.log(posts.concat(todos).length)); // 300
```

## 📚 Tham khảo / Bài tập

- Chạy `01_fetch/app.js` qua `index.html` hoặc `node app.js`: file demo 2 ví dụ — fetch đơn (đang comment) và **multi-fetch bằng `Promise.all`** gộp `posts` + `todos`.
- Tự thử: bỏ comment ví dụ 1 để xem fetch đơn; thêm `console.log(posts[0])` để xem cấu trúc dữ liệu; sau đó viết lại bằng `async/await`.