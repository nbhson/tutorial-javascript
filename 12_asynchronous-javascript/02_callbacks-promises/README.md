# Callbacks & Promises

## 🔑 Khái niệm

Đây là phần đi sâu vào hai công cụ xử lý bất đồng bộ phổ biến nhất:

- **Callback**: hàm được truyền vào hàm khác và gọi lại sau khi tác vụ hoàn thành. Là nền tảng, nhưng lồng nhau nhiều tầng sẽ thành **callback hell**.
- **Promise**: đối tượng đại diện cho kết quả của một tác vụ bất đồng bộ (đang chờ, thành công hoặc thất bại), với các bước `.then()/.catch()/.finally()`. Ra đời từ ES6 để giải quyết callback hell.
- **async/await**: cú pháp (ES2017) viết promise gọn như code đồng bộ, dễ đọc/dễ giữ lỗi.

Promise có 3 trạng thái:

- `pending` — tác vụ chưa xong.
- `fulfilled` — thành công, các `.then()` được gọi.
- `rejected` — thất bại, `.catch()` được gọi.

## ✅ Điểm mạnh

- Promise xử lý lỗi tập trung qua `.catch`, không phải truyền lỗi lồng nhau.
- Chain `.then()` cho phép nối các bước bất đồng bộ rõ ràng.
- `Promise.all/Promise.race...` chạy song song, kết hợp nhiều tác vụ.
- async/await làm code gần với suy nghĩ tuần tự, dễ debug.
- Giải quyết triệt để "callback hell"/"pyramid of doom".

## ⚠️ Lưu ý / Hạn chế

- Promise là **microtask** — thứ tự chạy trước setTimeout gây bất ngờ nếu quên.
- trong `.then()`, phải `return` giá trị/promise mới nối được chuỗi tiếp theo.
- Không gọi `resolve`/`reject` → promise treo vĩnh viễn (memory leak).
- `await` chỉ hợp lệ trong hàm `async`.
- Callback vẫn tồn tại trong các API thư viện cũ — cần biết cách wrap thành promise.

## 💡 Khi nào dùng

- Bất kỳ tác vụ bất đồng bộ nào: fetch, đọc file, database, timer.
- Xử lý theo chuỗi: lấy comment → lấy user từ comment → render.
- Chạy song song nhiều request: `Promise.all`.
- Giữ code dễ đọc trong quy trình nhiều bước phụ thuộc nhau.

## 🎯 Ví dụ minh họa

```js
// Promise cơ bản
const p = new Promise((resolve, reject) => {
  setTimeout(() => resolve("Success"), 1000);
});
p.then((msg) => console.log(msg))   // Success
 .catch((err) => console.log(err))
 .finally(() => console.log("Done"));

// Promise.all — chạy song song
Promise.all([fetch("/a"), fetch("/b")]).then(([a, b]) => {
  console.log("cả hai", a, b);
});
```

## 📚 Tham khảo / Bài tập

- Nhóm này gồm: `01_promise-theory`, `02_async-await`, `03_promise-concept`, `04_promise-chain`, `05_promise-static-methods`, `06_promise-example`, `07_callback-hell` — đọc theo thứ tự.
- Chạy lần lượt các `app.js` trong từng folder; folder `06_promise-example` có cả `index.html` để render UI thật.
- Tự thử: chạy demo ở `07_callback-hell` rồi so sánh với bản promise cùng file.