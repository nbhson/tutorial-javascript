# Xử lý ngoại lệ (Exceptional Handling)

## 🔑 Khái niệm

Xử lý ngoại lệ là kỹ thuật **kiểm soát lỗi** để chương trình không "chết" giữa chừng khi có lỗi xảy ra. Trong JavaScript:

- **`throw`** — chủ động *ném ra* một tín hiệu lỗi. Khác với nhiều ngôn ngữ khác, bạn có thể `throw` **bất cứ giá trị nào**: chuỗi, số, object, hay `new Error("...")`.
- **`try...catch`** — *bắt* lỗi bị ném trong khối `try` và xử lý ở khối `catch`.
- **`finally`** — luôn chạy dù có lỗi hay không, thường dùng để dọn dẹp (đóng kết nối, xóa loading...).
- **Error Objects** (`Error`, `TypeError`, `ReferenceError`, `SyntaxError`, `RangeError`, `URIError`) — các loại lỗi chuẩn kèm `name` và `message` để biết lỗi gì đã xảy ra.

Khi lỗi không được bắt, chương trình sẽ dừng lại và in stack trace ra console — đúng cái cảnh "màn hình đỏ" mà ai lập trình lâu ngày cũng từng gặp.

## ✅ Điểm mạnh

- **Chương trình không chết oan**: lỗi được kiểm soát và thông báo thân thiện thay vì treo app.
- **Tách biệt logic và xử lý lỗi**: code chính gọn, phần lỗi gom vào `catch`.
- **`finally` đảm bảo dọn dẹp** trong mọi trường hợp — kể cả khi có `return` hoặc `throw` trong `try`.
- **Throw được mọi giá trị** → linh hoạt trong việc truyền thông tin lỗi tùy ngữ cảnh.
- Error objects chuẩn giúp phân biệt loại lỗi bằng `instanceof`, `name` hoặc `message`.
- `catch` không bắt buộc có tham số (ES2019) khi bạn chỉ cần `finally`.

## ⚠️ Lưu ý / Hạn chế

- Nên `throw new Error(...)` thay vì `throw "chuỗi"` hay `throw {code: 400}` — lỗi dạng object có kèm `stack` trace giúp debug.
- `try...catch` chỉ bắt được lỗi **đồng bộ** trong cùng khối; lỗi trong callback/promise/`setTimeout` không bị bắt trực tiếp (cần `.catch()` hoặc `async/await`).
- `finally` luôn chạy, nhưng nếu `finally` bản thân ném lỗi, nó sẽ **che lấp** lỗi gốc từ `try`.
- Lạm dụng `try...catch` để "nuốt" lỗi (bỏ `console.error`) sẽ làm việc debug sau này khó khăn hơn rất nhiều.

## 💡 Khi nào dùng

- Thẩm định dữ liệu đầu vào (chia cho 0, nhập sai định dạng, JSON lỗi cú pháp).
- Gọi API / đọc file — mạng không ổn định, cần bắt và thông báo trọng tải.
- Phân tích cú pháp: `JSON.parse`, `eval` — dễ ném lỗi với input không hợp lệ.
- Code thư viện/helper: `throw` lỗi rõ ràng cho người dùng hàm biết đã truyền sai tham số.
- Dọn dẹp tài nguyên bắt buộc: đóng modal, xóa spinner, ngắt kết nối — đặt ở `finally`.

## 🎯 Ví dụ minh họa

```js
function div(a, b) {
  if (b === 0) throw new Error("divide by zero");
  return a / b;
}

try {
  div(1, 0);
} catch (e) {
  console.log(e.message); // divide by zero
} finally {
  console.log("luôn chạy"); // dù thành công hay thất bại
}
```

## 📚 Tham khảo / Bài tập

- `01_throw/` — cách dùng `throw` đúng chuẩn với Error object (`app.js`).
- `02_try-catch-finally/` — thứ tự hoạt động của `try/catch/finally`, kể cả finally trong finally (`app.js`).
- `03_error-objects/` — phân biệt `TypeError`, `SyntaxError`, `RangeError` bằng `name` và `instanceof` (`app.js`).
- Tự thử với từng file (mỗi thư mục có `index.html` để mở trên trình duyệt hoặc chạy `node app.js`).