# Hàm có sẵn (Built-in Functions)

## 🔑 Khái niệm

Built-in functions là **các hàm do JavaScript (hoặc môi trường chạy) cung cấp sẵn**, ta không phải tự viết mà chỉ cần gọi ra dùng. Trong file `app.js`, tác giả liệt kê một số hàm quen thuộc trong môi trường **trình duyệt**:

| Hàm | Công dụng |
|---|---|
| `alert(message)` | hiện hộp thoại thông báo |
| `confirm(question)` | hỏi Có/Không, trả về `true`/`false` |
| `prompt(label)` | ô nhập liệu, trả về chuỗi người dùng nhập |
| `console.log()` | in ra console (DevTools) |
| `setTimeout(fn, ms)` / `clearTimeout()` | chạy hàm sau `ms` mili-giây |
| `setInterval(fn, ms)` / `clearInterval()` | chạy hàm lặp lại đều đặn |

Chú ý: nhóm này khác với **Built-in Object** (như `Math`, `JSON`, `Date`) — đó là "đối tượng có sẵn", còn đây là "hàm có sẵn". Trong `app.js`, tác giả chỉ demo các hàm tương tác trình duyệt ở trên; còn nhóm hàm chuyển kiểu/chuyển mã hay gặp khác như `parseInt`, `parseFloat`, `isNaN`, `isFinite`, `encodeURI`, `eval` cũng là built-in (riêng `eval` hiện khuyến cáo tránh vì chạy mã nguy hiểm).

## ✅ Điểm mạnh

- Tiết kiệm thời gian: không phải tự dựng các chức năng hệ thống.
- `setTimeout`/`setInterval` giúp làm quen với **bất đồng bộ** — nền tảng của JS.
- `confirm`/`prompt` giúp tương tác người dùng mà không cần xây UI phức tạp.
- Chạy demo trong trình duyệt thấy kết quả ngay và trực quan.
- Liệt kê rõ từng hàm kèm tác vụ, dễ học từng cái.

## ⚠️ Lưu ý / Hạn chế

- `alert`, `confirm`, `prompt` **chỉ chạy trong trình duyệt** — dùng trong Node.js sẽ lỗi (`ReferenceError: alert is not defined`).
- `alert`/`confirm` **chặn** luồng chạy (blocking) — không nên lạm dụng trong sản phẩm thật.
- `setTimeout(fn, ms)` thời gian thực thi không chính xác tuyệt đối (bị độ trễ, phụ thuộc event loop).
- `eval` chạy mã động cực kỳ nguy hiểm (code injection) và chậm — hạn chế tối đa.
- `isNaN("abc")` cũng trả `true` do ép kiểu — nếu muốn kiểm tra chặt, dùng `Number.isNaN`.

## 💡 Khi nào dùng

- Gửi thông báo/tương tác đơn giản với người dùng (bản demo, prototype).
- Hẹn giờ chạy tác vụ một lần (`setTimeout`) hoặc định kỳ (`setInterval`).
- Parse số từ chuỗi input: `parseInt`, `parseFloat`.
- Kiểm tra số hữu hạn/an toàn với `isFinite`, `Number.isNaN` (bản chặt).
- Mã hóa URL khi truyền tham số: `encodeURI`.

## 🎯 Ví dụ minh họa

```js
// Nội dung app.js trong thư mục (chạy trong trình duyệt)
alert("Xin chào đến với website!");
confirm("Xác nhận đã đủ 18 tuổi?");   // true / false
prompt("Nhập tên của bạn:");          // trả về chuỗi nhập vào

setTimeout(() => console.log("setTimeout"), 1000);   // sau 1s in setTimeout
setInterval(() => console.log("setInterval"), 1000); // mỗi 1s in setInterval

// Hàm chuyển kiểu thường dùng khi xử lý input
console.log(parseInt("42px"));    // 42
console.log(parseFloat("3.14"));  // 3.14
```

## 📚 Tham khảo / Bài tập

- Thư mục này **chỉ có `app.js`** (không có `index.html`) — vì `alert`/`confirm`/`prompt` cần trình duyệt, hãy dán nội dung `app.js` vào Console (`F12`) của trình duyệt để xem các hộp thoại hiện ra.
- Xem Console sau khi đóng các hộp thoại: `setTimeout` in 1 lần sau 1 giây, `setInterval` in lặp lại mỗi giây.
- Tự thử: dùng `clearInterval` với một biến đếm để dừng sau 5 lần in.
- Tự thử: so sánh `isNaN("abc")` (true) với `Number.isNaN("abc")` (false) để thấy sự khác biệt ép kiểu.