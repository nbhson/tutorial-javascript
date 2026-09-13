# setTimeout / setInterval — hẹn giờ trong JavaScript

## 🔑 Khái niệm

`setTimeout` và `setInterval` là hai hàm hẹn giờ (timer) thuộc **Web APIs** — kết quả của chúng rơi vào **Macrotask Queue**:

| Hàm | Cách hoạt động | Dừng lại |
|-----|----------------|----------|
| `setTimeout(fn, ms)` | chạy `fn` **một lần** sau ít nhất `ms` ms | `clearTimeout(id)` |
| `setInterval(fn, ms)` | chạy `fn` **lặp lại mỗi** `ms` ms | `clearInterval(id)` |

Quan trọng: thời gian chỉ là **tối thiểu**. Callback chỉ chạy khi **Call Stack trống** — nên `setTimeout(fn, 0)` vẫn chạy sau toàn bộ code đồng bộ (macro/microtask phía sau ưu tiên).

Vì `setTimeout`/`setInterval` là **macrotask**, chúng luôn chạy **sau** mọi microtask (promise) đang chờ cùng lúc.

## ✅ Điểm mạnh

- Trì hoãn/định kỳ tác vụ mà không chặn luồng chính.
- Dùng `setTimeout` chạy trễ sau khi sự kiện hiện tại xử lý xong.
- `setInterval` tiện cho đồng hồ, đếm ngược, polling nhẹ.
- Kết hợp với `clearInterval` kiểm soát vòng lặp chính xác.

## ⚠️ Lưu ý / Hạn chế

- Không đảm bảo độ chính xác thời gian (tối thiểu, không tuyệt đối).
- `setInterval` **chạy mãi mãi** nếu không `clearInterval` → tốn tài nguyên, giật UI.
- Callback phải chờ stack trống — gọi API nặng ở interval có thể "dồn chồng" nhau.
- `setTimeout(0)` chạy sau tất cả sync và sau các microtask đang đợi.

## 💡 Khi nào dùng

- Debounce tìm kiếm, autocomplete (setTimeout + clearTimeout).
- Animation, đếm ngược, đồng hồ (setInterval + clearInterval).
- Xếp tác vụ chạy sau khi render (setTimeout 0).

## 🎯 Ví dụ minh họa

```js
console.log(1);
setTimeout(() => console.log("timeout 0"), 0); // macrotask → chạy sau
console.log(3);
// Output: 1 → 3 → timeout 0

// setInterval: chạy lặp, tự dừng ở lần thứ 2
let n = 0;
const id = setInterval(() => {
  console.log("interval", ++n);
  if (n >= 2) clearInterval(id); // dừng vòng lặp
}, 10);
// interval 1 → interval 2 (rồi dừng)
```

## 📚 Tham khảo / Bài tập

- Chạy `03_settimeout-setinterval/app.js` (qua `index.html` hoặc `node app.js`): xem thứ tự `1 → 3 → timeout 0` và vòng lặp interval tự dừng sau 2 lần.
- Tự thử: bỏ dòng `clearInterval(id)` và thấy interval chạy vô hạn; thêm `Promise.resolve().then(() => console.log("promise"))` để quan sát microtask chạy trước timer.