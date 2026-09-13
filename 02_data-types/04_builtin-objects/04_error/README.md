# Built-in: Error (Xử lý lỗi)

## 🔑 Khái niệm

**`Error`** là built-in object đại diện cho một lỗi trong JavaScript. Ngoài `Error`, JS còn các biến thể nghiệp hơn: `TypeError`, `ReferenceError`, `SyntaxError`, `RangeError`, `URIError`, `EvalError`... — mỗi loại mô tả một loại sai khác nhau.

**Khởi tạo và ném lỗi:**

```js
new Error("thông điệp");
throw new TypeError("bad");
```

**Bắt lỗi bằng try/catch:**

```js
try {
  throw new TypeError("bad");
} catch (e) {
  console.log(e.name);    // "TypeError" — tên loại lỗi
  console.log(e.message); // "bad"      — thông điệp mô tả
  console.log(e.stack);   // toàn bộ stack trace (nơi lỗi xảy ra)
}
```

Kết quả chạy:

```
TypeError
bad
TypeError: bad
    at Object.<anonymous> (file:line)
    ...stack...
```

**Ba thuộc tính chính của Error:**

| Thuộc tính | Ý nghĩa |
|---|---|
| `name` | tên loại lỗi: `"TypeError"`, `"ReferenceError"`, `"Error"`... |
| `message` | thông điệp bạn tự viết khi tạo |
| `stack` | chuỗi trace chỉ chính xác **ở đâu** và **gọi qua đâu** để lỗi xuất hiện |

**Khi nào dùng loại nào:**

- `TypeError` — thao tác sai kiểu (gọi hàm không tồn tại, `null.prop`).
- `ReferenceError` — truy cập biến chưa khai báo.
- `SyntaxError` — sai cú pháp (thường do engine bắt khi parse).
- `RangeError` — giá trị ngoài khoảng hợp lệ (vd. mảng quá lớn).
- `Error` — lỗi chung tự định nghĩa.

## ✅ Điểm mạnh

- Kiểm soát flow: bắt được lỗi và phản hồi đúng thay vì app "chết".
- `name`/`message`/`stack` giúp debug nhanh và chính xác.
- Phân loại lỗi theo loại → xử lý chi nhánh phù hợp:
  ```js
  if (e instanceof TypeError) { ... } else { ... }
  ```
- `throw` truyền dữ liệu lỗi xuyên qua nhiều tầng gọi hàm.
- Không bắt được lỗi `SyntaxError` trong cùng file (engine bắt lúc parse).

## ⚠️ Lưu ý / Hạn chế

- Quên `try/catch` → lỗi **"crash"** chương trình (Node ngắt, trình duyệt in đỏ).
- `throw "chuỗi"` vẫn chạy được, nhưng `e` sẽ **không có** `message`/`stack` — hãy luôn `throw new Error(...)` để các thuộc tính đó tồn tại.
- Lỗi trong **async** (callback/Promise) không bị `try/catch` sync bắt — phải dùng `.catch`/`try{await}`.
- Đừng lờ lờ `catch {}` (rỗng) — vô tình nuốt lỗi.

## 💡 Khi nào dùng

- Validate đầu vào và ném lỗi `TypeError`/`RangeError` khi không hợp lệ.
- Bọc các thao tác dễ lỗi (đọc API, parse JSON) trong try/catch.
- Xử lý lỗi phân lớp theo loại (re-throw nếu không thuộc quyền xử lý của hàm).
- Log `e.stack` khi cần trace lỗi production.

## 🎯 Ví dụ minh họa

```js
try {
  throw new TypeError("bad");
} catch (e) {
  console.log(e.name, e.message, e.stack.slice(0, 80));
}
// TypeError bad TypeError: bad
//    at Object.<anonymous> ( ... )

// Phân loại lỗi
try {
  null.x;                     // TypeError
} catch (e) {
  console.log(e instanceof TypeError); // true
}
```

## 📚 Tham khảo / Bài tập

- Chạy `app.js` trong thư mục (`node app.js` hoặc mở `index.html`): ném `TypeError("bad")`, bắt và in `name`, `message`, `stack` — quan sát toàn bộ stack trace.
- Tự thử: 1) viết hàm `divide(a, b)` ném `RangeError` nếu `b === 0`; 2) kết hợp `JSON.parse` trong try/catch và in `e.name` khi chuỗi sai; 3) bỏ `catch` xem chương trình "crash" thế nào rồi thử lại với `try/catch`.
- Tài liệu: [MDN — Error](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error), [javascript.info/try-catch](https://javascript.info/try-catch).