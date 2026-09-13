# Event Loop — cơ chế lõi của async JavaScript

## 🔑 Khái niệm

JS là ngôn ngữ **đơn luồng**: chỉ một nhiệm vụ thực thi tại một thời điểm. Để không bị chặn bởi các tác vụ lâu (timer, request mạng), trình duyệt cung cấp **Web APIs** — các API bất đồng bộ, non-blocking (DOM API, HTTP request, `setTimeout`...).

Hành trình của một callback:

1. Hàm được gọi → đẩy vào **Call Stack** (LIFO). Hàm xong thì lấy ra.
2. Gặp `setTimeout`/`fetch` → callback được đưa sang **Web APIs**, nơi có đồng hồ riêng chờ cho tới khi đủ thời gian.
3. Hết thời gian → callback **không vào thẳng Call Stack** mà nằm ở **Callback Queue** (FIFO) chờ lượt.
4. **Event Loop** chỉ có một việc: khi **Call Stack trống** thì lấy callback từ Queue đưa vào Stack để chạy.

Vì vậy `setTimeout(fn, 0)` **không** chạy ngay sau khi hết 0ms — nó phải chờ stack trống. Càng xếp nhiều setTimeout/setInterval thì càng chờ lâu.

## ✅ Điểm mạnh

- Giải thích chính xác mọi thứ tự log bất ngờ (stack, web API, queue).
- Hiểu vì sao setTimeout 0 vẫn chạy sau code đồng bộ.
- Nền tảng để dùng đúng promise (microtask) và timer (macrotask).
- Trình bày trực quan bằng các file gif minh họa trong folder.

## ⚠️ Lưu ý / Hạn chế

- Thời gian trong `setTimeout` chỉ là **tối thiểu**, không đảm bảo chính xác.
- Stack trống nhưng Queue có nhiều callback → thứ tự FIFO quyết định.
- Task nặng trong stack chặn mọi callback dù đã sẵn sàng trong queue.
- Microtask (promise) được ưu tiên trước macrotask (timer) — thường "nhảy hàng".

## 💡 Khi nào dùng

- Chạy trễ một đoạn code sau khi sự kiện hiện tại xử lý xong (`setTimeout(0)`).
- Gộp nhiều thao tác DOM tốn kém lại chờ lượt.
- Đồng bộ hóa giữa các tác vụ bất đồng bộ độc lập.

## 🎯 Ví dụ minh họa

```js
const foo = () => console.log("First");
const bar = () => setTimeout(() => console.log("Second"), 0);
const baz = () => console.log("Third");

bar(); // callback → Web API (timer 0ms) → queue
foo(); // First
baz(); // Third
// stack trống → Event Loop lấy callback
// Second   ← in cuối cùng
```

## 📚 Tham khảo / Bài tập

- Mở `02_event-loop/` và xem các file gif (Stack, Web API, Queue, Event Loop) minh họa từng bước; `app.js`/`index.html` chuẩn bị sẵn để bạn chạy thử.
- Tự thử: thêm `Promise.resolve().then(() => console.log("Micro"))` vào đoạn trên và dự đoán thứ tự — bạn sẽ thấy microtask chạy trước "Second".