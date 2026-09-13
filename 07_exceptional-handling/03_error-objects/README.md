# Error Objects — Các đối tượng lỗi chuẩn

## 🔑 Khái niệm

JavaScript cung cấp sẵn các "họ" lỗi chuẩn (built-in error types) để biểu thị từng kiểu lỗi. Tất cả đều kế thừa từ `Error` và có hai thuộc tính quan trọng: **`name`** (loại lỗi) và **`message`** (nội dung), ngoài ra còn có `stack` để truy vết.

Các loại phổ biến:

| Loại | Khi nào xuất hiện |
|---|---|
| `Error` | lỗi chung, hoặc do bạn `throw new Error(...)` |
| `TypeError` | gọi hàm/đọc thuộc tính sai kiểu — ví dụ `null.f()` |
| `ReferenceError` | truy cập biến chưa khai báo |
| `SyntaxError` | sai cú pháp (thường gặp khi `eval` chuỗi sai) |
| `RangeError` | số nằm ngoài phạm vi hợp lệ (mảng âm, vòng lặp quá sâu...) |
| `URIError` | dùng hàm URI (`decodeURI`) với chuỗi sai quy tắc |

Trong `app.js` có ba lần kiểm chứng điển hình:

1. `null.f()` → `TypeError` (`e.name === "TypeError"`, `instanceof TypeError` là `true`).
2. `eval("a b")` → `SyntaxError` (chuỗi không phải cú pháp hợp lệ).
3. `new RangeError("range").name` → `"RangeError"`.

## ✅ Điểm mạnh

- **Chuẩn hóa thông tin lỗi**: `name` + `message` + `stack`, ai cũng hiểu được.
- Phân loại lỗi bằng `instanceof` và `name` → viết `catch` theo từng loại lỗi cụ thể.
- Kế thừa từ `Error` nên dùng chung được với tất cả cấu trúc xử lý lỗi.
- Giúp debug nhanh: nhìn `name` biết ngay lỗi kiểu gì (gọi sai phương thức, biến thiếu, cú pháp sai...).
- Có thể tự tạo subclass của `Error` cho lỗi nghiệp vụ của dự án.

## ⚠️ Lưu ý / Hạn chế

- Nhầm lẫn hay gặp: `TypeError` là do **thao tác trên giá trị sai kiểu** (như `null.f()`, gọi số như hàm), chứ không phải "kiểu dữ liệu sai khi so sánh".
- Lỗi cú pháp của chương trình (file JS bị lẫn lộn cú pháp) không bắt được bằng `try...catch` — nó xảy ra lúc parse, không phải lúc chạy.
- Dùng `instanceof` để phân loại đáng tin hơn so với đọc chuỗi `message` (vì message có thể được tùy biến).
- Khi phải handle mọi kiểu lỗi, đừng chỉ dựa vào `TypeError` — có cả `EvalError`, `URIError`, lỗi custom...

## 💡 Khi nào dùng

- Bắt lỗi và hiển thị thông báo phù hợp theo từng loại lỗi.
- Debug ngay tại console: đọc `e.name`/`e.message`/`e.stack`.
- `JSON.parse` / `eval` — bắt `SyntaxError` để xử lý chuỗi đầu vào xấu.
- Viết guard cho thư viện: `throw new TypeError("tham số phải là number")`.
- Giám sát lỗi sản phẩm (Sentry, logging) dựa trên `name` và `stack`.

## 🎯 Ví dụ minh họa

```js
// Nội dung app.js trong thư mục
try {
  null.f();                                    // đọc thuộc tính của null
} catch (e) {
  console.log(e.name, e instanceof TypeError); // "TypeError" true
}

try {
  eval("a b");                                 // cú pháp sai
} catch (e) {
  console.log(e.name);                         // "SyntaxError"
}

console.log(new RangeError("range").name);     // "RangeError"
```

## 📚 Tham khảo / Bài tập

- Mở `index.html` trên trình duyệt (Console) hoặc chạy `node app.js` để xem kết quả: `TypeError true`, `SyntaxError`, `RangeError`.
- Tự thử: `console.log(undefVar)` (không khai báo `undefVar`) để thấy `ReferenceError`.
- Thử `new Array(-1)` để gặp `RangeError`, `decodeURIComponent("%")` để gặp `URIError`.
- Viết hàm phân loại lỗi bằng `instanceof` và in ra thông báo khác nhau cho `TypeError` / `RangeError` / `Error` chung.