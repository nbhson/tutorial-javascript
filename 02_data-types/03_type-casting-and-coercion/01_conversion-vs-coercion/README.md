# Type Conversion vs Coercion

## 🔑 Khái niệm

Cả hai đều là "chuyển đổi kiểu dữ liệu", nhưng khác nhau ở **ai là người chủ động làm**:

| Tiêu chí | **Conversion** (Explicit) | **Coercion** (Implicit) |
|---|---|---|
| Ai thực hiện | Lập trình viên | Engine (máy chạy JS) |
| Hình thức | Gọi trực tiếp `String()`, `Number()`, `Boolean()`... | Xảy ra tự động trong phép tính/điều kiện |
| Ví dụ | `String(123)` → `"123"` | `"5" + 3` → `"53"` |
| Đọc code | Rõ ràng, dễ hiểu | Phải nắm quy tắc thì mới hiểu |
| Rủi ro bug | Thấp | Cao nếu không hiểu |

**Conversion (explicit):** bạn chủ động quyết định kiểu đích:
```js
String(123); // "123"
Number("42"); // 42
Boolean(0); // false
```

**Coercion (implicit):** engine tự "ép" khi gặp các tình huống như:
- Dùng **`==`** (loose equality): `"5" == 5` → engine chuyển `"5"` thành `5`.
- Toán tử **`+`** với có string: `1 + "2"` → `"12"` (ưu tiên nối chuỗi).
- Các toán tử số học `-`, `*`, `/`: `"5" - 3` → `2` (ưu tiên chuyển sang số).
- Ngữ cảnh điều kiện **`if (...)`**: giá trị bị quy về truthy/falsy.

```js
console.log("5" + 3); // "53"  (implicit — nối chuỗi)
console.log("5" - 3); // 2     (implicit — trừ số)
```

## ✅ Điểm mạnh

- Nắm được "quyền chủ động": bạn kiểm soát kết quả khi dùng explicit, không bị bất ngờ.
- Explicit giúp code tự giải thích, dễ review.
- Coercion (khi hiểu luật) giúp viết ngắn: `if (username)` thay vì `if (username !== null && username !== undefined && username !== "")`.
- Phân biệt rõ 2 khái niệm → trả lời được câu hỏi phỏng vấn kinh điển.

## ⚠️ Lưu ý / Hạn chế

- Coercion làm code online "kỳ lạ": `"5" + 3` khác `"5" - 3` dù cùng toán hạng.
- `+` quyết định theo sự hiện diện của string — còn `-`, `*`, `/` luôn ép số.
- `==` ép kiểu phức tạp; nếu không chắc, dùng `===`.
- Đọc code có coercion đòi hỏi kiến thức quy tắc, khó cho thành viên mới.

## 💡 Khi nào dùng

- Muốn kiểm soát hoàn toàn kiểu → **explicit**: `Number(input)`, `String(id)`.
- Viết điều kiện "có giá trị trả về hay không" → **implicit/truthy** một cách có chủ đích.
- Phân tích bug: khi thấy `"abc" - 1` trả `NaN` → biết engine coercion theo toán tử.

## 🎯 Ví dụ minh họa

```js
// Explicit conversion
console.log(String(123), typeof String(123)); // "123" string
console.log(Number("42"), typeof Number("42")); // 42 number
console.log(Boolean(0), Boolean(""), Boolean([])); // false false true

// Implicit coercion
console.log("5" + 3);       // "53"  — string thắng (nối chuỗi)
console.log("5" - 3);       // 2     — phép trừ luôn ép số
console.log(null == undefined); // true (chỉ với ==)
```

## 📚 Tham khảo / Bài tập

- Chạy `app.js` trong thư mục (`node app.js` hoặc mở `index.html`): in ra `String(123)`, `"5" + 3` (nối chuỗi), `"5" - 3` (ép số) — ví dụ gọn nhất phân biệt two loại.
- Chuyển tiếp sang `02_explicit/` (hàm ép kiểu chủ động) và `03_implicit/` (engine tự ép, 7 giá trị falsy).
- Tự thử: đưa 5 biểu thức `1 + "1"`, `"1" - 1`, `true + 1`, `null + 1`, `[] + 1` vào Console; đoán rồi kiểm chứng từng cái xem thuộc conversion hay coercion.
- Tài liệu: [javascript.info/type-conversions](https://javascript.info/type-conversions), [MDN — Equality](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Equality).