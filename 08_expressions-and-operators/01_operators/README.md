# Toán tử cơ bản (Operators — Basics)

## 🔑 Khái niệm

Thư mục này chứa 6 file demo các toán tử nền tảng mà bạn dùng hằng ngày:

| File | Nhóm | Toán tử chính |
|---|---|---|
| `1_toan-tu-so-hoc.js` | Số học (Arithmetic) | `+ - * ** / % ++ --` |
| `2_toan-tu-chuoi.js` | Chuỗi (String) | `+` nối chuỗi |
| `3_toan-tu-gan.js` | Gán (Assignment) | `= += -= *= /= **=` |
| `4_toan-tu-so-sanh.js` | So sánh (Comparison) | `== != > < >= <= === !==` |
| `5_toan-tu-logical.js` | Logic (Logical) | `&&` `\|\|` `!` |
| `6_toan-tu-prefix-postfix.js` | Tăng/giảm | `++ --` (tiền tố / hậu tố) |

Hai kiến thức quan trọng nhất cần nắm từ nhóm này:

1. **`==` vs `===`**: `==` ép kiểu trước khi so sánh (`3 == "3"` → `true`), còn `===` so sánh nghiêm ngặt cả kiểu lẫn giá trị (`3 === "3"` → `false`). Nên dùng `===`.
2. **Prefix vs Postfix**: `n++` trả về **giá trị cũ** rồi mới tăng; `++n` tăng trước rồi **trả về giá trị mới**.

Bên cạnh đó, file `4_toan-tu-so-sanh.js` liệt kê 7 giá trị falsy quan trọng: `0`, `NaN`, `""`, `''`, `false`, `null`, `undefined`.

## ✅ Điểm mạnh

- Bao phủ trọn bộ toán tử cơ bản cần cho mọi dự án JavaScript.
- Mỗi file nhỏ, gọn, chú thích tiếng Việt rõ ràng về ý nghĩa từng ký hiệu.
- Có ví dụ thực tế về ép kiểu (`a + b` với `b` là chuỗi kết quả `"15"`, `a - b` ra số `-4`).
- Ghi rõ 7 falsy value — kiến thức chống ngộ nhận khi dùng `if`.
- Nhấn mạnh `===` và sự khác nhau giữa string và String object.
- Chạy độc lập được từng file bằng `node`.

## ⚠️ Lưu ý / Hạn chế

- `+` có hai nghĩa: cộng số hoặc nối chuỗi, phụ thuộc kiểu toán hạng (`1 + '5'` → `"15"`).
- Với `- * /`, chuỗi số sẽ được ép thành số (`'5' * 2` → `10`).
- `==` với `null`/`undefined` và với kiểu object (`"" == new String("")`) dễ gây kết quả bất ngờ — dùng `===` để an toàn.
- Quên thứ tự `a++`/`++a` khi kẹp trong biểu thức lớn sẽ cho kết quả sai mà khó tìm.
- `==` có những cặp "lạ" như `true == "1"` → `true` — rất dễ hiểu nhầm nếu chỉ đọc lướt.

## 💡 Khi nào dùng

- So sánh giá trị trong mọi điều kiện `if`/`while`/`switch` — luôn ưu tiên `===`/`!==`.
- Tính toán số học, lũy thừa (`**`), chia lấy dư (`%`) để kiểm tra chẵn/lẻ.
- Cộng dồn dữ liệu với `+=`, `*=`, tăng đếm trong vòng lặp bằng `++`.
- Nối chuỗi tên, địa chỉ, chuỗi thông báo.
- Kiểm tra truthy/falsy để quyết định nhánh code.

## 🎯 Ví dụ minh họa

```js
// 1_toan-tu-so-hoc.js
var a = 1, b = "5";
console.log(a + b); // "15"  — nối chuỗi vì có string
console.log(a - b); // -4    — ép "5" thành số
console.log(3 ** 2); // 9

// 4_toan-tu-so-sanh.js
console.log(3 == "3");  // true
console.log(3 === "3"); // false
console.log(undefined == null);  // true
console.log(undefined === null); // false

// 6_toan-tu-prefix-postfix.js
var a = 69;
var b = a++;
console.log(a, b); // 70 69 — a tăng lên 70, b nhận giá trị cũ 69
```

## 📚 Tham khảo / Bài tập

- `node 1_toan-tu-so-hoc.js` — thử thêm `1 + "1"`, `"3" * "2"`, `10 % 3`.
- `node 2_toan-tu-chuoi.js` — thử thêm ký tự unicode và \n (xuống dòng).
- `node 3_toan-tu-gan.js` — thêm vài dòng tính `x **= 2`, `x /= 2`.
- `node 4_toan-tu-so-sanh.js` — tự kiểm tra `null == 0`, `[] == ""`, `[1] == 1` và thấy kết quả "bất ngờ" của `==`.
- `node 5_toan-tu-logical.js` — viết thử `console.log(3 && 0)`, `console.log(0 || "mặc định")`, `console.log(!null)`.
- `node 6_toan-tu-prefix-postfix.js` — đổi `number++` thành `++number` và xem kết quả đổi từ `12` thành `13`.