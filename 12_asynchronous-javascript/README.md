# Lập trình Bất đồng bộ (Asynchronous JavaScript)

## 🔑 Khái niệm

**JavaScript là ngôn ngữ đơn luồng (single-threaded)**: engine chỉ xử lý một câu lệnh tại một thời điểm trong một luồng duy nhất. Điều này khiến mọi tác vụ chạy lâu (gọi API, đọc file, chờ timer...) có thể **chặn (block)** toàn bộ chương trình nếu thực hiện đồng bộ.

**Lập trình bất đồng bộ (asynchronous)** giải quyết vấn đề đó: chương trình có thể **bắt đầu** một tác vụ dài và **tiếp tục đáp ứng các sự kiện khác** ngay lập tức, thay vì đứng chờ; khi tác vụ hoàn thành thì kết quả được thông báo lại. JavaScript hiện thực điều này bằng **Event Loop + Call Stack + Web APIs + hàng đợi (queue)**.

Các kỹ thuật bất đồng bộ chính trong JS:

1. **Callbacks** — truyền hàm xử lý sau khi tác vụ xong (nền tảng, nhưng dễ thành callback hell).
2. **Promises (ES6)** — đối tượng đại diện kết quả tương lai, giải quyết callback hell.
3. **async/await (ES2017)** — cú pháp viết code bất đồng bộ nhìn như đồng bộ.

## ✅ Điểm mạnh

- Không chặn luồng chính (main thread): trang web luôn phản hồi trong lúc tải dữ liệu.
- Xử lý song song các tác vụ độc lập (fetch nhiều API cùng lúc bằng `Promise.all`).
- Cải thiện trải nghiệm người dùng (UI mượt, không bị "đứng hình").
- Promises + async/await giúp code dễ đọc, dễ debug hơn callback nối chồng.
- Mọi tác vụ I/O mạng, timer, DOM event đều tận dụng được.

## ⚠️ Lưu ý / Hạn chế

- Thứ tự thực thi không theo thứ tự khai báo — dễ nhầm nếu không hiểu Event Loop.
- Promise là **microtask**, chạy trước `setTimeout`/`setInterval` (macrotask) — thứ tự output thường bất ngờ.
- Callback lồng sâu ("pyramid of doom") khó đọc, khó gỡ lỗi nếu không dùng Promise.
- `await` chỉ hợp lệ bên trong hàm `async`.
- Bất đồng bộ thêm độ phức tạp: cần nắm call stack, task queue, microtask queue.

## 💡 Khi nào dùng

- Gọi REST API, tải dữ liệu từ server (fetch, XHR).
- Đặt lịch tác vụ: `setTimeout`, `setInterval`.
- Lắng nghe sự kiện người dùng (click, scroll...) mà không chặn.
- Xử lý file, stream, realtime (WebSocket), animation.
- Mọi tác vụ cần "chờ" kết quả ngoài luồng mà không muốn đứng im chờ.

## 🎯 Ví dụ minh họa

```js
console.log("1. Start");

setTimeout(() => {
  console.log("2. Timeout");     // macrotask → chạy cuối
}, 0);

Promise.resolve()
  .then(() => console.log("3. Promise")); // microtask → chạy sau sync

console.log("4. End");

// Output: 1. Start → 4. End → 3. Promise → 2. Timeout
```

## 📚 Tham khảo / Bài tập

- Nhóm chia 2 phần: `01_event-loop` (runtime, sync/async, event loop, setTimeout) và `02_callbacks-promises` (promise theory, async/await, chain, static methods, callback hell).
- Chạy thử các file `app.js` trong từng sub-folder theo thứ tự.
- Tự thử: viết lại đoạn trên với thêm 2 `setTimeout(0)` và 1 `Promise.resolve().then()` — đoán trước thứ tự output trước khi chạy.