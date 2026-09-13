# Number (Kiểu số)

## 🔑 Khái niệm

**Number** là kiểu primitive biểu diễn **mọi loại số** trong JavaScript: nguyên, thực, dương, âm, dương vô cực (`Infinity`), không xác định số (`NaN`), và các giá trị đặc biệt như `Number.EPSILON`. JavaScript dùng chuẩn **IEEE-754 double-precision floating-point** (64-bit) — nên có giới hạn: số nguyên an toàn lớn nhất là `Number.MAX_SAFE_INTEGER` = `9007199254740991` (2⁵³ − 1).

**Tạo giá trị number:**

```js
var PI = 3.14;                       // literal
const a = new Number(23);            // object wrapper — KHÔNG nên dùng
typeof PI;                           // "number"
typeof a;                            // "object"
```

> **Lưu ý:** `typeof NaN` trả `"number"` — “Not-a-Number” là giá trị đặc biệt, không phải kiểu khác.

**Kiểm tra giá trị đặc biệt:**

```js
console.log(isNaN(20 / 'AC')); // true (chia cho chuỗi → NaN)
console.log(isNaN('hello'));   // true
console.log(Number.isNaN('hello')); // false — chính xác hơn typeof cho NaN
```

**Các hàm số học quan trọng trên `Math`:**

| Thuộc tính/Hàm | Ý nghĩa |
|---|---|
| `Math.PI` | số π = 3.14159... |
| `Math.round(x)` | làm tròn |
| `Math.ceil(x)` | làm tròn lên |
| `Math.floor(x)` | làm tròn xuống |
| `Math.abs(x)` | giá trị tuyệt đối |
| `Math.min(a, b, ...)` / `Math.max(...)` | nhỏ nhất / lớn nhất trong các giá trị |
| `Math.random()` | số ngẫu nhiên `>= 0` và `< 1` |

**Chuyển số thành chuỗi:**

```js
console.log((22).toString());   // "22"
console.log((22).toFixed(2));   // "22.00" — dừng lại, trả về string
```

**NaN — giá trị "dị":**

```js
typeof NaN;        // "number"
NaN === NaN;       // false ← NaN không bằng chính nó!
Number.isNaN(NaN); // true (dùng cái này thay vì isNaN())
```

## ✅ Điểm mạnh

- Chi phối hầu hết phép tính trong JS, API function luôn dùng number.
- `Math` API mạnh mẽ, đủ dùng cho phép tính cơ bản đến phức tạp.
- `isNaN` / `Number.isNaN` giúp kiểm tra phép tính thất bại (chia cho 0, PARSE thất bại...).
- `toString()` + `toFixed()` linh hoạt hiển thị số theo dạng văn bản.
- Number literal ngắn gọn, dễ đọc.

## ⚠️ Lưu ý / Hạn chế

- **`0.1 + 0.2 !== 0.3`** do sai số IEEE-754; so sánh số thực cần `Math.abs(a - b) < ε`.
- `new Number(23)` tạo object (typeof `"object"`) — không dùng.
- `NaN === NaN` trả **false**; dùng `Number.isNaN()` thay vì `isNaN()` để tránh sai (vd. `isNaN("x")` là `true` dù `"x"` không phải `NaN`).
- `Math.random()` chỉ tạo số nguyên dương duy nhất khi kết hợp `Math.floor(Math.random() * n)`.
- Nhỏ/nhỏ không gọi được `(3).toString()` — cần括号: `String(3)` để an toàn hơn.

## 💡 Khi nào dùng

- Tính toán hiển thị: `toFixed(2)` cho giá tiền.
- Làm tròn, giá trị tuyệt đối, kiểm tramax/min (`Math.round`, `Math.ceil`, `Math.floor`, `Math.min`, `Math.max`).
- Lấy số ngẫu nhiên trong khoảng `[min, max]`: `Math.floor(Math.random() * (max - min + 1)) + min`.
- Kiểm tra `NaN` trên kết quả phép toán: dùng `Number.isNaN()`.

## 🎯 Ví dụ minh họa

```js
var PI = 3.14;
console.log(typeof PI, Math.PI);          // number  3.14159...
console.log((22).toString());             // "22"
console.log(Math.round(3.4));             // 3
console.log(Math.ceil(3.1));              // 4
console.log(Math.floor(3.9));             // 3
console.log(Math.abs(-15.41));            // 15.41
console.log(Math.min(5, 9, 4, 8.7, 1));  // 1
console.log(Math.max(5, 9, 4, 8.7, 1));  // 9
console.log(Math.random());               // >= 0, < 1
```

## 📚 Tham khảo / Bài tập

- Chạy `number.js` bằng `node` hoặc mở `index.html` trong thư mục này để xem kết quả trực tiếp; mở thêm `Number.docx` để đọc tài liệu tham khảo.
- Tự thử: 1) xác minh `0.1 + 0.2 === 0.3` in ra `false`; 2) viết hàm `randomBetween(min, max)` trả số nguyên ngẫu nhiên trong khoảng `[min, max]`; 3) dùng `Number.isNaN` kiểm tra kết quả `parseInt("abc")` và so sánh với `isNaN`.
- Tài liệu: [MDN — Number](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number), [MDN — Math](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math).