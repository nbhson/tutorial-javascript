# Primitive Types (Kiểu nguyên thủy)

## 🔑 Khái niệm

**Primitive (nguyên thủy)** là giá trị **không phải object** và **không có phương thức** riêng — chúng là "nguyên tử" dữ liệu của JavaScript. Có **7 kiểu nguyên thủy**:

1. **string** — chuỗi ký tự: `"Sơn"`, `'a'`, `` `template ${x}` ``.
2. **number** — số dấu phẩy động: `42`, `3.14`, các giá trị đặc biệt `NaN`, `Infinity`, `-Infinity`.
3. **bigint** — số nguyên lớn: `9007199254740993n`.
4. **boolean** — `true` / `false`.
5. **undefined** — *chưa được gán giá trị* (engine tự đặt).
6. **symbol** — giá trị duy nhất, bất biến, dùng làm khóa object.
7. **null** — *cố ý rỗng* (lập trình viên đặt). Lưu ý: `typeof null` trả `"object"` — **bug lịch sử** không sửa được vì sẽ phá hàng tỉ trang web.

**Bản chất của primitive:**

- **So sánh theo giá trị**: `"a" === "a"` là `true`, `1 === 1` là `true`.
- **Tại một thời điểm chỉ chứa một giá trị** duy nhất.
- **Bất biến (immutable)**: không "sửa" được chuỗi/số; mọi thao tác đều tạo giá trị mới.
- Khi gán `let b = a` (a là primitive): JS **sao chép giá trị** vào ô nhớ mới → thay đổi `a` sau đó không ảnh hưởng `b` (xem chi tiết ở `03_value-vs-reference`).

**Vì sao chuỗi lại "có" nhiều phương thức?** Chuỗi là primitive, nhưng khi bạn gọi `"abc".toUpperCase()`, engine tạm time "bọc" nó trong một object wrapper tương ứng (String, Number, Boolean...) rồi gọi phương thức và vứt đi — đó là cơ chế **boxing**. Nhờ vậy primitive vẫn "tiện" như object.

## ✅ Điểm mạnh

- Giá trị nhỏ gọn, di chuyển nhanh (copy theo value, không dính dáng tham chiếu).
- So sánh trực quan và chính xác: `1 === 1`, `"a" === "a"`.
- Bất biến → an toàn khi truyền vào hàm (hàm sửa đổi cũng không phá giá trị gốc).
- Đủ 7 kiểu cho mọi nhu cầu cơ bản: chữ, số, đúng/sai, rỗng, khóa duy nhất.
- Kết hợp boxing → vẫn có đủ helper methods tiện lợi dù là primitive.

## ⚠️ Lưu ý / Hạn chế

- `typeof null === "object"` — phải nhớ riêng, đừng tin vào kết quả này.
- `number` theo chuẩn IEEE-754 → `0.1 + 0.2` có thể không bằng `0.3`.
- `typeof` không phân biệt được array với object thường (đều là `"object"`) — dùng `Array.isArray`.
- Dùng `new String(...)`, `new Number(...)` tạo ra **object**, không phải primitive → `typeof` thành `"object"`, đừng làm.

## 💡 Khi nào dùng

- Mọi dữ liệu đơn giản: tên, số tuổi, cờ đúng/sai → string / number / boolean.
- Số vượt `Number.MAX_SAFE_INTEGER` (ID, hash, timestamp nano) → bigint.
- Cần giá trị duy nhất làm khóa → symbol.
- Biểu đạt "chưa có" → `undefined` cho engine, `null` cho quyết định của bạn.

## 🎯 Ví dụ minh họa

```js
let a = 1;
let b = a;       // sao chép GIÁ TRỊ
a = 2;
console.log(b);  // 1 — b không hề thay đổi

// primitive so sánh theo giá trị
console.log(1 === 1);         // true
console.log("x" === "x");     // true

// boxing: chuỗi primitive vẫn gọi được phương thức
console.log("son".toUpperCase()); // "SON"
```

## 📚 Tham khảo / Bài tập

- Nhóm này có 6 bài con, mỗi bài kèm file thực hành:
  - `01_string/` (`1_chuoi.js`, `2_lam-viec-voi-chuoi.js`)
  - `02_number/` (`number.js`)
  - `03_value-vs-reference/` (`app.js`)
  - `04_bigint/` (`app.js`)
  - `05_symbol/` (`app.js`)
  - `06_null-undefined-boolean/` (`app.js`)
- Chạy từng file bằng `node <tên-file>.js` (hoặc mở `index.html` tương ứng trong trình duyệt).
- Tự thử: gõ `typeof undefined`, `typeof null`, `typeof 10n`, `typeof Symbol()` vào Console để ghi nhớ 7 primitive.