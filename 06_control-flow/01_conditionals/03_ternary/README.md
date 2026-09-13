# Toán tử ba ngôi (Ternary)

## 🔑 Khái niệm

Toán tử ba ngôi (ternary operator / conditional operator) là cách **viết gọn của `if...else`** trong một biểu thức, có 3 thành phần:

```
điều kiện ? giá_trị_nếu_đúng : giá_trị_nếu_sai
```

Nó là một *expression* — tức luôn **trả về một giá trị** — nên thường được dùng để gán cho biến hoặc làm đối số/giá trị trả về. Trong file `app.js`:

```js
let a = true ? "Success" : "Error"; // a = "Success"
```

Thay vì viết:

```js
let a;
if (true) {
  a = "Success";
} else {
  a = "Error";
}
```

## ✅ Điểm mạnh

- **Rất gọn**: chuyển 5-7 dòng `if/else` thành 1 dòng.
- Là một expression nên linh hoạt: gán biến, trả về từ hàm, điền trực tiếp vào template literal, tham số hàm.
- Dùng được với mọi giá trị truthy/falsy ở phần điều kiện.
- Dễ đọc khi mệnh đề đúng/sai là các giá trị/chuỗi ngắn.
- Thể hiện rõ "chọn một trong hai" — giúp người đọc hiểu ý đồ nhanh.

## ⚠️ Lưu ý / Hạn chế

- **Không dùng để chạy nhiều câu lệnh**: mục đích là trả về giá trị, không phải "thực thi hành động phức tạp".
- **Ternary lồng ternary rất khó đọc** — hãy chuyển sang `if...else` khi logic phức tạp.
- Dễ nhầm do thiếu dấu ngoặc khi kết hợp nhiều toán tử — đặt `()` rõ ràng nếu cần.
- Side effect trong nhánh ternary gây khó kiểm tra/bảo trì.
- Nếu cả hai nhánh cùng một công việc khá dài, ternary không còn "gọn" nữa mà chỉ là rối.

## 💡 Khi nào dùng

- Gán giá trị mặc định theo điều kiện: `let status = age >= 18 ? "người lớn" : "trẻ em";`
- Chọn văn bản/icon hiển thị theo trạng thái UI.
- Trả về giá trị khác nhau từ hàm một cách ngắn gọn.
- Xây chuỗi động (template literal) có nhánh điều kiện.
- Sửa/thẩm định biến một dòng thay cho `if` dài.

## 🎯 Ví dụ minh họa

```js
// app.js — ví dụ gốc trong thư mục
let a = true ? "Success" : "Error";
console.log(a); // Success

console.log("Sơn".length > 3 ? true : false); // true
console.log(100 % 2 === 0 ? "Chẵn" : "Lẻ");  // Chẵn
```

## 📚 Tham khảo / Bài tập

- Mở `index.html` trong trình duyệt và xem Console: biến `a = "Success"`.
- Chạy `app.js` bằng `node app.js` sau khi thêm `console.log(a);` để quan sát.
- Tự thử: viết `let mark = 7.5;` rồi `mark >= 8 ? "Giỏi" : "Khá"` và in ra; đổi giá trị để thấy nhánh đổi.
- Thử gán qua `/` , `+`, `-` giữa hai số chẵn/lẻ để làm quen với dạng `(x % 2 ? ... : ...)`.