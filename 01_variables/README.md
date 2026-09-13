# 01. Biến (Variables)

## 🔑 Khái niệm

Biến (**variable**) là một "chiếc hộp" có tên dùng để **lưu trữ giá trị** trong chương trình: số, chuỗi, mảng, object... Thay vì viết đi viết lại một giá trị, bạn gán nó vào biến và dùng tên biến ở mọi nơi.

```js
let tuoi = 20;
console.log(tuoi); // 20
tuoi = 21;         // gán lại giá trị (assignment)
```

Lưu ý quan trọng: **biến không phải là giá trị** — nó là chỗ đứng (container) chứa giá trị. Nhóm này dạy bạn trả lời 4 câu hỏi cốt lõi:

1. **Khai báo** như thế nào? (`var`, `let`, `const` — nên ưu tiên `let`/`const`.)
2. **Hoisting** hoạt động ra sao? (vì sao `var` in ra `undefined` còn `let`/`const` báo `ReferenceError`.)
3. **Scope (phạm vi)** ảnh hưởng thế nào? (global, block scope, function scope.)
4. **Đặt tên** thế nào cho chuẩn? (camelCase, tránh keyword, mô tả đúng ý nghĩa.)

Bởi JavaScript là **ngôn ngữ kiểu động** (dynamic typing), một biến có thể đổi kiểu khi chạy. Việc khai báo đúng cách là nền tảng để tránh vô số bug về sau.

## ✅ Điểm mạnh

- Code rõ ràng hơn: tên biến mô tả đúng dữ liệu nó chứa.
- `const`/`let` có **block scope**, thay thế `var` rối rắm của phiên bản cũ.
- Hiểu hoisting + TDZ → tránh được các lỗi ReferenceError khó hiểu.
- Nắm scope → viết được hàm không bị "ô nhiễm" biến toàn cục.
- Tái sử dụng giá trị, dễ bảo trì, dễ gỡ lỗi (log tên biến rõ nghĩa).

## ⚠️ Lưu ý / Hạn chế

- Dùng `var` trong code hiện đại là tín hiệu xấu; nó có function scope và nhảy ra khỏi block.
- Truy cập biến `let`/`const` trước dòng khai báo → `ReferenceError` (temporal dead zone).
- `const` chỉ khóa *tham chiếu*: object/array bên trong `const` **vẫn thay đổi** nội dung được.
- Không gán được cho biến chưa khai báo khi có `"use strict"` → `num = 5` sẽ lỗi.

## 💡 Khi nào dùng

- Bất kỳ lúc nào cần lưu và tái sử dụng một giá trị trong chương trình.
- Đếm số lần lặp, đếm số lần click, lưu trạng thái người dùng.
- Lưu cấu hình (config) không đổi → dùng `const` để "đóng băng" tham chiếu.
- Lưu kết quả DOM query (`const button = document.querySelector(...)`) để dùng nhiều lần.

## 🎯 Ví dụ minh họa

```js
// Khai báo + khởi tạo rồi gán lại
let count = 0;
count += 1;
console.log(count); // 1

// const — không gán lại được biến
const PI = 3.14;
// PI = 4; // TypeError: Assignment to constant variable

// const với object: thay đổi THUỘC TÍNH được, gán lại BIẾN thì không
const user = { name: "Nam" };
user.name = "Hoa"; // OK
console.log(user.name); // Hoa
```

## 📚 Tham khảo / Bài tập

- Nhóm này gồm 4 bài con: `01_declarations/`, `02_hoisting/`, `03_scopes/`, `04_naming-and-practices/`.
- Chạy thử `01_declarations/app.js` và `01_declarations/01_let-and-const/app.js` bằng Node (`node app.js`) hoặc mở `index.html` trên trình duyệt để xem console.
- Tự thử: khai báo một biến `var` bên trong `if`, thử truy cập bên ngoài; làm lại với `let` và quan sát lỗi.