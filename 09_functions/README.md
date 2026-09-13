# Hàm (Functions)

## 🔑 Khái niệm

Hàm (function) là **khối code có tên**, nhận tham số đầu vào, thực thi logic, và trả về kết quả — giúp tái sử dụng và chia nhỏ chương trình. Trong JavaScript, hàm là **first-class citizens**: có thể gán cho biến, truyền làm đối số, trả về từ hàm khác.

Lộ trình học hàm trong repo này chia làm hai nhóm lớn:

### 01_parameters-and-arrow — cách tạo và dùng hàm
- `01_callbacks/` — callback: hàm truyền làm đối số (`forEach`, `filter`, `some`, `every`, `map`).
- `02_builtin-functions/` — các hàm có sẵn của ngôn ngữ (`alert`, `setTimeout`, `setInterval`...).
- `03_arrow-functions/` — cú pháp mũi tên `() => {}` và sự khác biệt với function thường (`this`).
- `04_recursion/` — đệ quy: hàm gọi chính nó (`factorial`, `fibonacci`).
- `05_arguments-object/` — object `arguments` ẩn giấu bên trong hàm thường.
- `06_function-parameters/` — tham số: default value, rest `...args`.

### 02_scope-closure-strict-mode — vòng đời và phạm vi của hàm
- `01_strict-mode/` — chế độ nghiêm ngặt `"use strict"` bật kiểm tra gắt gao.
- `02_iife/` — hàm được gọi ngay lập tức (IIFE) và tính private.
- `03_closure/` — hàm nhớ được biến của phạm vi bên ngoài.
- `04_non-blocking-io/` — cách JavaScript xử lý bất đồng bộ, không chặn luồng.
- `05_function-stack/` — call stack (ngăn xếp gọi hàm) và scope chain.

## ✅ Điểm mạnh

- **Tái sử dụng code**: viết một lần, gọi nhiều nơi — giảm trùng lặp.
- **Chia nhỏ logic**: hàm nhỏ giúp test, sửa, đọc hiểu dễ hơn.
- Bóc tách rõ ràng giữa "khai báo", "biểu thức gán", và "arrow" — so sánh trực tiếp từng cách.
- Kèm ví dụ chạy ngay được trong từng thư mục con (phần lớn có `app.js` + `index.html`).
- Đi theo đúng lộ trình roadmap.sh: từ callback → closure → bất đồng bộ.
- Hệ thống luôn bổ sung các kiến thức nền (strict mode, call stack) giúp hiểu "tại sao" chứ không chỉ "làm gì".

## ⚠️ Lưu ý / Hạn chế

- Function declaration **hoisted** (dùng được trước khi khai báo), còn function expression và arrow thì **không**.
- Arrow function **không có `this`, `arguments` riêng, không dùng làm constructor** — đọc kỹ `03_arrow-functions` trước khi áp dụng.
- Callback dễ dẫn tới "callback hell" (lồng nhau quá sâu) nếu không tổ chức tốt.
- Đệ quy cần **base case** rõ ràng, nếu không sẽ tràn bộ nhớ (stack overflow).
- Top-level `03_this-and-binding` trong roadmap.sh chưa có thư mục trong repo này — kiến thức `this` được đề cập sơ bộ trong `03_arrow-functions` và `01_strict-mode`.

## 💡 Khi nào dùng

- Đóng gói các thao tác lặp lại: format dữ liệu, tính toán, gọi API.
- Xử lý danh sách bằng callback/map/filter thay vì viết vòng lặp tay.
- Tổ chức ứng dụng theo hướng hàm nhỏ ghép lại (functional).
- Hiểu đệ quy cho các bài toán chia nhỏ (duyệt cây, thư mục, JSON lồng nhau).
- Làm quen với closure cho các pattern như counter, module, hooks.

## 🎯 Ví dụ minh họa

```js
// Callback gọi lại
function welcome(name) {
  console.log("Xin chào " + name);
}
setTimeout(() => welcome("Sơn"), 1000); // sau 1s in "Xin chào Sơn"

// Map với arrow
const nums = [1, 2, 3].map(n => n * 2);
console.log(nums); // [2, 4, 6]
```

## 📚 Tham khảo / Bài tập

- Bắt đầu với `01_parameters-and-arrow/01_callbacks/` và 6 file từ `1_call-back.js` đến `6_map.js`.
- Làm quen hàm có sẵn qua `02_builtin-functions/app.js`.
- So sánh `03_arrow-functions/app.js` để thấy khác biệt so với hàm thường.
- Về đệ quy và tham số, xem `04_recursion/app.js`, `05_arguments-object/app.js`, `06_function-parameters/app.js`.
- Về phạm vi: đọc `02_scope-closure-strict-mode/` từ `01_strict-mode/app.js` → `05_function-stack/app.js`.
- Tự thử: viết hàm `calculate(a, b, operator)` trả về phép tính tương ứng, dùng default + rest khi hợp lý.