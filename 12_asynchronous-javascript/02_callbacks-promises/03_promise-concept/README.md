# Promise — Khái niệm và 3 trạng thái (Pending / Fulfilled / Rejected)

## 🔑 Khái niệm

Promise sinh ra (từ ES6) để **giải quyết các vấn đề bất đồng bộ**. Trước promise, người ta dùng callback — và callback sinh ra **callback hell**, nên promise ra đời để thay thế.

Một promise được tạo bằng `new Promise(executor)` — **executor chạy ngay lập tức**, trước khi bạn nhận được biến promise, và nhận 2 hàm:

- `resolve(value)` → promise chuyển sang **fulfilled**; các `.then()` được gọi.
- `reject(error)` → promise chuyển sang **rejected**; `.catch()` được gọi.

Ba trạng thái:

1. **Pending** — không gọi `resolve`/`reject`.
2. **Fulfilled** — gọi `resolve()` → `.then()` chạy.
3. **Rejected** — gọi `reject()` → `.catch()` chạy.

Sau một trong hai, `.finally()` luôn chạy bất kể thành công hay thất bại. Lưu ý: nếu **không gọi** cả `resolve` và `reject`, promise rơi vào pending vĩnh viễn → **memory leak**.

Trong file demo: các tác vụ bất đồng bộ điển hình gồm `setTimeout`, `setInterval`, `fetch`, `XMLHttpRequest`, file reading, requestAnimationFrame.

## ✅ Điểm mạnh

- Tách rõ 3 trạng thái → dễ suy luận hành vi của code.
- `.then/.catch/.finally` xử lý lỗi tập trung, tránh callback lồng nhau.
- Executor chạy ngay giúp khởi tạo tác vụ đúng lúc.
- Nền tảng để ghép nối (`Promise.all`) và viết `async/await`.

## ⚠️ Lưu ý / Hạn chế

- Không gọi `resolve`/`reject` → treo vĩnh viễn (memory leak).
- Promise settle **một lần duy nhất**; gọi cả `resolve` rồi `reject` chỉ lần đầu có hiệu lực.
- Kết quả đến "muộn" so với cảm nhận — cần hiểu microtask để đoán thứ tự.
- Quên `.catch()` với `reject` → unhandled rejection.

## 💡 Khi nào dùng

- Wrapping các tác vụ không phải promise (callback API cũ) thành promise.
- Điều khiển luồng: thành công thì `.then`, thất bại thì `.catch`, luôn kết thúc bằng `.finally`.
- Khởi tạo tác vụ bất đồng bộ ngay lúc tạo promise.

## 🎯 Ví dụ minh họa

```js
var promise = new Promise((resolve, reject) => {
  // pending nếu không gọi gì
  reject("404"); // → rejected, .catch chạy
});

promise
  .then(function (result) {
    console.log("Success", result);   // chỉ chạy nếu resolve()
  })
  .catch(function (error) {
    console.log("Fail", error);       // → Fail 404
  })
  .finally(function () {
    console.log("Done");              // luôn chạy
  });
```

## 📚 Tham khảo / Bài tập

- Chạy `03_promise-concept/app.js` (qua `index.html` hoặc `node app.js`): xem `Fail 404` rồi `Done`.
- Tự thử: đổi dòng `reject("404")` thành `resolve([{ id: 1, course: "HTML" }])` và thấy `.then` nhận dữ liệu; rồi bỏ cả hai để quan sát promise treo ở pending.