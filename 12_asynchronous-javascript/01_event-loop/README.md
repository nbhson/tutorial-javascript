# Event Loop trong Asynchronous JavaScript

## 🔑 Khái niệm

**Event Loop** là cơ chế cho phép JS (đơn luồng) xử lý các tác vụ bất đồng bộ. Nó liên tục **quan sát Call Stack và các hàng đợi**, và chỉ khi **Call Stack trống** mới đưa callback từ hàng đợi vào stack để thực thi. Tóm tắt chu trình:

```
1. Call Stack chạy code đồng bộ.
2. Gặp tác vụ bất đồng bộ (setTimeout, fetch...) → đẩy sang Web APIs.
3. Web APIs xử lý xong → bỏ callback vào hàng đợi (queue).
4. Event Loop: nếu Call Stack trống → lấy callback theo FIFO vào stack.
5. Lặp lại.
```

Có **hai hàng đợi** với thứ tự ưu tiên:

- **Microtask Queue** (ưu tiên cao): `Promise.then()`, `queueMicrotask()`, `MutationObserver`.
- **Macrotask Queue** (ưu tiên thấp): `setTimeout`, `setInterval`, I/O...

Thứ tự thực thi chuẩn: **sync → microtask → macrotask**.

## ✅ Điểm mạnh

- Giải thích được mọi output "bất ngờ" của code bất đồng bộ.
- Khiến JS nhanh và responsive bất chấp đơn luồng.
- Microtask ưu tiên cao giúp Promise settle ngay khi stack trống.
- Dự đoán chính xác thứ tự log giữa promise và setTimeout.

## ⚠️ Lưu ý / Hạn chế

- Callback **không chạy đúng lúc** đúng hạn (thời gian chỉ là tối thiểu).
- Lạm dụng quá nhiều microtask có thể "bỏ đói" macrotask.
- Task nặng trong call stack vẫn chặn mọi thứ — bất đồng bộ không làm code nhanh hơn.
- Cần nhớ cả stack, heap, web APIs, hai queue mới hiểu trọn bức tranh.

## 💡 Khi nào dùng

- Debug thứ tự thực thi của promise so với setTimeout.
- Tối ưu: đẩy tác vụ nặng, tác vụ bất đồng bộ ra khỏi luồng chính.
- Hiểu vì sao async/await lại "treo" hàm mà không chặn chương trình.

## 🎯 Ví dụ minh họa

```js
console.log("1. Start");

setTimeout(() => console.log("2. Timeout"), 0);      // macrotask
Promise.resolve().then(() => console.log("3. Promise")); // microtask
queueMicrotask(() => console.log("4. queueMicrotask"));  // microtask

console.log("5. End");

// 1. Start → 5. End → 3. Promise → 4. queueMicrotask → 2. Timeout
```

## 📚 Tham khảo / Bài tập

- Nhóm này gồm: `00_js-runtime-deep-dive`, `01_introduce-sync-async`, `02_event-loop` (kèm gif minh họa), `03_settimeout-setinterval` — đọc lần lượt.
- Chạy thử `app.js`/`example.js` trong từng folder, quan sát thứ tự in ra.
- Tự thử: thêm 1 promise khác và đổi thứ tự khai báo — đoán thứ tự output trước khi chạy.