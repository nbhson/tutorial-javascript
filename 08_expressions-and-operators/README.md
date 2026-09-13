# Biểu thức và Toán tử (Expressions & Operators)

## 🔑 Khái niệm

Một **expression** (biểu thức) là bất kỳ đoạn code nào **trả về một giá trị** — ví dụ `5 + 3`, `a > b`, `x = 10`. Một **operator** (toán tử) là ký hiệu thực hiện thao tác lên các *operand* (toán hạng) để tạo ra giá trị đó. JavaScript có rất nhiều nhóm toán tử, và đây là lộ trình học đầy đủ theo roadmap.sh:

| Thư mục | Nhóm toán tử | Ví dụ |
|---|---|---|
| `01_operators/` | Cơ bản: số học, chuỗi, gán, so sánh, logical, prefix/postfix | `+`, `**`, `=`, `===`, `&&`, `++` |
| `02_bitwise/` | Bitwise — thao tác trên từng bit | `&`, `|`, `^`, `~`, `<<`, `>>`, `>>>` |
| `03_bigint-operators/` | Toán tử trên số BigInt | `10n + 5n`, `2n ** 10n` |
| `04_comma/` | Dấu phẩy — trả về toán hạng cuối | `(1, 2, 3) → 3` |
| `05_unary/` | Toán tử một ngôi | `typeof`, `void`, `delete`, `+`, `-`, `!` |
| `06_string-operators/` | Nối chuỗi | `+`, `+=`, `.concat()` |

## ✅ Điểm mạnh

- **Phủ đầy đủ lộ trình roadmap.sh** — từ cơ bản đến các toán tử ít dùng nhưng vẫn cần biết.
- Mỗi nhóm có thư mục riêng với ví dụ chạy được ngay, dễ tìm lại khi cần.
- Ví dụ minh họa tính toán thực tế (so sánh `3 == "3"` vs `3 === "3"`, bit flags, BigInt).
- Biết đủ nhóm toán tử giúp đọc code của người khác (npm, thư viện) không lúng túng.
- Là nền tảng hiểu rõ "biểu thức" — khái niệm xuyên suốt mọi part sau này (ternary, short-circuit, template...).

## ⚠️ Lưu ý / Hạn chế

- Một số toán tử ít dùng đến trong công việc thường ngày (bitwise, comma, BigInt) — dễ quên, nhưng cần biết mặt để đọc hiểu.
- `==` dễ gây lỗi ngầm do tự ép kiểu — ưu tiên `===` / `!==`.
- Prefix (`++i`) và postfix (`i++`) cho kết quả **khác nhau khi nằm trong biểu thức** — nhầm lẫn rất phổ biến.
- BigInt không trộn được với Number trong cùng phép toán (lỗi `TypeError`).
- Một số toán tử (như bitwise) chỉ hoạt động trên số 32-bit, kết quả có thể gây bất ngờ với số lớn.

## 💡 Khi nào dùng

- Tính toán, so sánh, gán giá trị — diễn ra trong gần như mọi dòng code.
- Viết điều kiện phức tạp với `&&`, `||`, `!` (đặc biệt với short-circuit để đặt giá trị mặc định).
- Xử lý quyền, cờ trạng thái (permissions) với phép toán bitwise.
- Làm việc với số nguyên siêu lớn vượt quá `Number.MAX_SAFE_INTEGER` → BigInt.
- Kiểm tra kiểu với `typeof`, trả về `undefined` bằng `void` (vd: THJS `void 0`), xóa thuộc tính bằng `delete`.

## 🎯 Ví dụ minh họa

```js
console.log(3 == "3");  // true  — ép kiểu
console.log(3 === "3"); // false — nghiêm ngặt

let n = 6;
console.log(n++ + --n); // 6 + 6 = 12 (hậu tố trả giá trị cũ, tiền tố trả giá trị mới)

console.log(5 & 1);     // 1 — bitwise AND
console.log(10n + 5n);  // 15n — BigInt
console.log(typeof 123); // number
```

## 📚 Tham khảo / Bài tập

- Bắt đầu từ `01_operators/` với 6 file `1_toan-tu-so-hoc.js` → `6_toan-tu-prefix-postfix.js`.
- Tiếp tục khám phá từng nhóm nâng cao: `02_bitwise/app.js`, `03_bigint-operators/app.js`, `04_comma/app.js`, `05_unary/app.js`, `06_string-operators/app.js`.
- Mỗi thư mục đều có `index.html` — mở trên trình duyệt hoặc chạy `node app.js`.
- Tự thử: đoán kết quả của `2 + "2"`, `"5" * "2"`, `++n` vs `n++` trước khi chạy để kiểm chứng.