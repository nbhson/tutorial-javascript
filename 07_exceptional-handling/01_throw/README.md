# throw — Ném ngoại lệ

## 🔑 Khái niệm

`throw` là từ khóa dùng để **chủ động phát ra một lỗi** khi gặp tình huống bất thường mà bạn muốn dừng luồng chạy lại. Khi gặp `throw`, chương trình lập tức thoát khỏi luồng bình thường và: nếu có `try...catch` bao quanh thì rơi vào `catch`, còn không thì dừng hẳn và in lỗi ra console.

Điểm quan trọng nhất: **bạn có thể `throw` bất cứ giá trị nào** — không chỉ riêng lỗi.

```js
throw new Error("oops");   // ✅ nên dùng — có đầy đủ name, message, stack
throw "string";            // tránh — vẫn chạy được nhưng mất thông tin
throw { code: 400 };       // tránh — mất thông điệp và stack trace
```

Thư mục này minh họa bằng `app.js`: hàm `div` ném lỗi `"divide by zero"` khi mẫu số bằng `0`.

## ✅ Điểm mạnh

- **Dừng sớm, fail-fast**: phát hiện dữ liệu sai thì báo ngay thay vì để lỗi lan xa khó truy vết.
- Có thể truyền thông tin phong phú qua Error object: `message` để đọc, `stack` để debug, `name` để giám sát.
- Kết hợp tự nhiên với `try...catch` và `finally`.
- Không giới hạn kiểu throw — linh hoạt khi cần giao tiếp giữa các phần hệ thống.
- Giúp viết helper/an toàn: người dùng hàm nhận được lỗi rõ ràng khi truyền sai tham số.
- Là nền tảng để xây hệ thống lỗi nghiệp vụ (business error) trong dự án thực.

## ⚠️ Lưu ý / Hạn chế

- `throw "string"` / `throw {code}` bị "lạc" thông tin: không có `stack`, khó biết lỗi từ đâu ra — tránh trong code thật.
- Ném ngầm một giá trị không phải Error khiến `catch(e)` khó nhận biết loại lỗi.
- `throw` luôn dừng hàm hiện tại — code phía sau `throw` trong cùng khối không bao giờ chạy.
- Lỗi `throw` không được bắt sẽ làm chương trình chết — luôn đi kèm `try...catch` ở tầng phù hợp.

## 💡 Khi nào dùng

- Kiểm tra dữ liệu đầu vào: chia cho 0, tham số thiếu, định dạng sai.
- Xác thực nghiệp vụ: tài khoản không đủ tiền, sản phẩm hết hàng.
- Ném lỗi lập trình viên gọi sai API của hàm thư viện.
- Khi cần đưa chương trình về trạng thái báo lỗi rõ ràng thay vì lỗi mơ hồ.

## 🎯 Ví dụ minh họa

```js
// Nội dung app.js trong thư mục
function div(a, b) {
  if (b === 0) throw new Error("divide by zero");
  return a / b;
}

try {
  div(1, 0);
} catch (e) {
  console.log(e.message); // "divide by zero"
}
```

## 📚 Tham khảo / Bài tập

- Mở `index.html` trên trình duyệt (Console) hoặc chạy `node app.js` để thấy `"divide by zero"`.
- Tự thử: bỏ khối `try...catch` và cho hàm `div(1, 0)` chạy gốc — quan sát lỗi in thẳng ra console.
- Thử `throw "lỗi chuỗi"` rồi bắt bằng `catch` — so sánh thông tin nhận được so với `new Error`.
- Tự viết hàm `checkAge(age)` ném lỗi `"Chưa đủ 18 tuổi"` khi `age < 18`.