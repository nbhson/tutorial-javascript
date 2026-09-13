# `this` đứng một mình (global scope)

## 🔑 Khái niệm

Ở **global scope** (ngoài mọi function), `this` trỏ tới object toàn cục:

- **Browser:** `this === window` (và `window === globalThis`).
- **Node.js:** `this` ở module thường là `module.exports`, nhưng `globalThis` luôn là object global.

Khi gọi một hàm **trần** (không phải method, không bind, không `new`) trong non-strict mode, `this` bên trong hàm cũng rơi về global (default binding). Đây là "con số 0" của 4 quy tắc binding: nếu không thuộc quy tắc nào khác thì `this` là global/`undefined`.

## ✅ Điểm mạnh

- Nắm được hành vi mặc định của `this` từ đó suy ra được giá trị của mọi trường hợp khác.
- Dùng `globalThis` để truy cập object toàn cục mà không phụ thuộc browser/Node.
- Kiểm tra nhanh môi trường chạy (browser vs Node) qua loại object global.

## ⚠️ Lưu ý / Hạn chế

- `this === globalThis` chỉ là `true` ở global scope của browser; ở Node module top-level thì không.
- Gán/đọc biến global qua `this` dễ gây lỗi cùng tên biến (naming clash).
- Trong strict mode, gọi hàm trần trả về `undefined`, nên đừng trông chờ `window`.
- `window` không tồn tại trong Node — luôn kiểm tra môi trường trước khi dùng.

## 💡 Khi nào dùng

- Viết code chạy đa môi trường (browser + Node) cần object toàn cục: dùng `globalThis`.
- Debug: xác định môi trường đang chạy script.
- Làm nền để hiểu quy tắc default binding trong event handler và hàm trần.

## 🎯 Ví dụ minh họa

```js
// ở global scope của browser
console.log(this === globalThis); // → true

// Kiểm tra môi trường
console.log(
  typeof window !== "undefined" ? "browser window" : "node global"
); // browser window (chạy trong trình duyệt)
```

## 📚 Tham khảo / Bài tập

- Chạy `03_alone/app.js` (qua `index.html` trong trình duyệt): xem `this === globalThis` in ra `true`.
- Tự thử: mở cùng file bằng `node app.js` — so sánh kết quả giữa browser và Node; sau đó thêm `"use strict"` để thấy `this` trong hàm trở thành `undefined`.