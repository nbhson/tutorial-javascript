# JavaScript Runtime — Đi sâu vào bộ máy của JS

## 🔑 Khái niệm

**JavaScript Runtime** là môi trường thực thi JS, gồm các thành phần phối hợp với nhau để chạy code:

```
┌────────────────────────────────────────────────────┐
│ JavaScript Runtime                                 │
│  ┌───────────────┐   ┌───────────────┐            │
│  │  Call Stack   │   │     Heap      │            │
│  │  (LIFO)       │   │  (bộ nhớ động)│            │
│  └───────────────┘   └───────────────┘            │
│  ┌──────────────────────────────────────────────┐  │
│  │            Event Loop                        │  │
│  └──────────────────────────────────────────────┘  │
│  ┌───────────────┐   ┌───────────────────┐        │
│  │ Callback Queue│   │    Web APIs       │        │
│  │ (macrotask)   │   │ setTimeout/fetch..│        │
│  │ Microtask Q.  │   └───────────────────┘        │
│  └───────────────┘                                │
└────────────────────────────────────────────────────┘
```

Các thành phần chính:

- **Call Stack**: ngăn xếp LIFO chứa các hàm đang chạy; đẩy vào khi gọi, lấy ra khi return.
- **Heap**: vùng nhớ lưu object, array, function (quản lý bởi Garbage Collector).
- **Web APIs**: đồng hồ timer, fetch, DOM... do trình duyệt cung cấp, chạy ngoài luồng chính.
- **Event Loop**: đồng bộ Call Stack với các hàng đợi; chạy callback khi stack trống.
- **Task Queue (macrotask)** và **Microtask Queue**: nơi callback chờ lượt; microtask ưu tiên hơn.

## ✅ Điểm mạnh

- Nhìn thấy bức tranh toàn cảnh từ lúc code chạy đến lúc trả kết quả.
- Giải thích chính xác các lỗi `RangeError: Maximum call stack size exceeded` (stack overflow).
- Hiểu hoisting, scope chain, closure, this binding trong bối cảnh runtime thật.
- Phân biệt rõ thứ tự chạy của sync, microtask, macrotask — nền tảng debug bất đồng bộ.

## ⚠️ Lưu ý / Hạn chế

- V8/Node và trình duyệt có runtime khác nhau (Node không có DOM API).
- Stack overflow khi đệ quy vô hạn — không có golang-style stack tăng vô hạn.
- Biến global khai báo thiếu `var/let/const` gây memory leak.
- `setInterval` không được `clear` chạy mãi mãi → tốn tài nguyên.

## 💡 Khi nào dùng

- Giải thích/output thứ tự console.log trong code không đồng bộ.
- Chẩn đoán lỗi treo, memory leak, stack overflow.
- Tối ưu performance (tránh object "chết" trong bộ nhớ, debounce DOM access...).

## 🎯 Ví dụ minh họa

```js
// Thứ tự thực thi: sync → microtask → macrotask
setTimeout(() => console.log("4. Timeout"), 0);          // macrotask

Promise.resolve().then(() => console.log("3. Promise")); // microtask

for (let i = 0; i < 3; i++) console.log("1. For loop"); // sync

console.log("2. Start");
// Output: 1. For loop ×3 → 2. Start → 3. Promise → 4. Timeout
```

## 📚 Tham khảo / Bài tập

- Chạy `00_js-runtime-deep-dive/example.js` bằng `node example.js`: xem thứ tự `1. For loop` → `2. Start` → `3. Promise` → `4. Timeout` (promise chạy trước setTimeout dù khai báo sau).
- Xem file ảnh `Screenshot 2025-11-06 at 21.50.48.png` minh họa kiến trúc runtime.
- Tự thử: thêm `queueMicrotask(() => ...)` và một `setInterval` — dự đoán thứ tự in ra.