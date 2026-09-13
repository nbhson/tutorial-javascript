# Number (Kiểu số) — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

**Number** là kiểu primitive biểu diễn **mọi loại số** trong JavaScript: nguyên, thực, dương, âm, dương vô cực (`Infinity`), không xác định số (`NaN`), và các giá trị đặc biệt như `Number.EPSILON`. JavaScript dùng chuẩn **IEEE-754 double-precision floating-point** (64-bit) — nên có giới hạn: số nguyên an toàn lớn nhất là `Number.MAX_SAFE_INTEGER` = `9007199254740991` (2⁵³ − 1).

### Tạo giá trị number

```js
var PI = 3.14;                       // literal — số thập phân
var bigIntLiteral = 9007199254740991n; // BigInt literal (ES2020)
const a = new Number(23);            // object wrapper — KHÔNG NÊN DÙNG
typeof PI;                           // "number"
typeof a;                            // "object" ❌
```

> **Lưu ý:** `typeof NaN` trả `"number"` — "Not-a-Number" là giá trị đặc biệt thuộc kiểu number, không phải kiểu khác.

### Các giá trị đặc biệt của Number

| Giá trị | Ý nghĩa | Cách kiểm tra |
|---------|---------|---------------|
| `Infinity` | Dương vô cực (`1 / 0`) | `Number.isFinite(x)` → false |
| `-Infinity` | Âm vô cực (`-1 / 0`) | `Number.isFinite(x)` → false |
| `NaN` | Not-a-Number (`0/0`, `parseInt("abc")`) | `Number.isNaN(x)` → true |
| `-0` | Âm không (khác `+0` về mặt bit) | `Object.is(0, -0)` → false |
| `Number.EPSILON` | Độ chính xác nhỏ nhất (~2.2e-16) | So sánh số thực: `Math.abs(a-b) < Number.EPSILON` |

```js
console.log(1 / 0);            // Infinity
console.log(-1 / 0);           // -Infinity
console.log(0 / 0);            // NaN
console.log(Number.NaN);       // NaN
console.log(typeof NaN);       // "number" (đặc biệt!)
console.log(NaN === NaN);      // false ← NaN không bằng chính nó!
console.log(Number.isNaN(NaN)); // true — dùng cái này thay vì isNaN()
```

### Kiểm tra giá trị đặc biệt

```js
// isNaN() global — ép kiểu trước kiểm tra (dễ gây nhầm)
console.log(isNaN(20 / 'AC'));  // true (chia cho chuỗi → NaN)
console.log(isNaN('hello'));    // true (ép 'hello' → NaN)

// Number.isNaN() — chính xác hơn, không ép kiểu
console.log(Number.isNaN('hello')); // false — 'hello' không phải NaN
console.log(Number.isNaN(NaN));     // true

// isFinite() — kiểm tra có phải finite number không
console.log(isFinite(Infinity));    // false
console.log(isFinite(NaN));         // false
console.log(isFinite(42));          // true

// Number.isFinite() — strict version, không ép kiểu
console.log(Number.isFinite('42')); // false — string '42' không phải number
console.log(Number.isFinite(42));   // true
```

### Các hàm số học quan trọng trên `Math`

| Thuộc tính/Hàm | Ý nghĩa | Ví dụ |
|----------------|---------|-------|
| `Math.PI` | số π ≈ 3.14159... | `Math.PI` → 3.141592653589793 |
| `Math.E` | số e ≈ 2.71828... | `Math.E` → 2.718281828459045 |
| `Math.round(x)` | làm tròn (bỏ 0.5 trở lên thành 1) | `Math.round(3.5)` → 4 |
| `Math.ceil(x)` | làm tròn lên | `Math.ceil(3.1)` → 4 |
| `Math.floor(x)` | làm tròn xuống | `Math.floor(3.9)` → 3 |
| `Math.abs(x)` | giá trị tuyệt đối | `Math.abs(-15.41)` → 15.41 |
| `Math.min(a, b, ...)` | nhỏ nhất trong các đối số | `Math.min(5, 9, 4)` → 4 |
| `Math.max(a, b, ...)` | lớn nhất trong các đối số | `Math.max(5, 9, 4)` → 9 |
| `Math.random()` | số ngẫu nhiên `>= 0` và `< 1` | `Math.random()` → 0.738... |
| `Math.pow(x, y)` / `x ** y` | lũy thừa | `Math.pow(2, 3)` → 8 |
| `Math.sqrt(x)` | căn bậc hai | `Math.sqrt(16)` → 4 |
| `Math.trunc(x)` | bỏ phần thập phân | `Math.trunc(3.9)` → 3 |
| `Math.sign(x)` | dấu: 1, -1, 0, -0, NaN | `Math.sign(-5)` → -1 |

```js
console.log(Math.PI);            // 3.141592653589793
console.log(Math.round(3.4));    // 3
console.log(Math.ceil(3.1));     // 4
console.log(Math.floor(3.9));    // 3
console.log(Math.abs(-15.41));   // 15.41
console.log(Math.min(5, 9, 4, 8.7, 1));  // 1
console.log(Math.max(5, 9, 4, 8.7, 1));  // 9
console.log(Math.random());      // >= 0, < 1
console.log(2 ** 10);            // 1024
console.log(Math.sqrt(144));     // 12
```

### Chuyển số thành chuỗi

```js
console.log((22).toString());    // "22" — cần parentheses vì 22.toString() parse lỗi
console.log((22).toFixed(2));    // "22.00" — dừng lại 2 chữ số thập phân (trả về string)
console.log((3.14159).toFixed(1)); // "3.1"
console.log((42).toExponential()); // "4.2e+1"
console.log((1234).toPrecision(3)); // "1.23e+3"

// String() và toString() khác nhau ở null/undefined
console.log(String(null));       // "null"
// null.toString();             // ❌ TypeError: Cannot read properties of null
```

### NaN — giá trị "dị" cần hiểu rõ

```js
// NaN không bằng chính nó — property duy nhất trong IEEE-754
console.log(NaN === NaN);           // false
console.log(NaN == NaN);            // false
console.log(Object.is(NaN, NaN));   // true — cách kiểm tra chính xác

// NaN truyền propagation — mọi phép toán với NaN đều NaN
console.log(NaN + 1);              // NaN
console.log(NaN * 0);              // NaN
console.log(Math.sqrt(-1));        // NaN

// Kiểm tra NaN đúng cách
console.log(Number.isNaN(NaN));    // true
console.log(Number.isNaN('abc'));  // false — 'abc' không phải NaN (khác với global isNaN)
console.log(isNaN('abc'));         // true — global isNaN ép 'abc' → NaN trước khi check
```

## ✅ Điểm mạnh — Tại sao nên dùng number

| # | Điểm mạnh | Lý do |
|---|-----------|-------|
| 1 | **Chi phối hầu hết phép tính** | API, function luôn dùng number — không thể tránh |
| 2 | **`Math` API mạnh mẽ** | Đủ dùng cho phép tính cơ bản đến phức tạp |
| 3 | **`isNaN` / `Number.isNaN`** | Kiểm tra phép tính thất bại (chia cho 0, PARSE thất bại) |
| 4 | **`toString()` + `toFixed()` linh hoạt** | Hiển thị số theo dạng văn bản, format tiền tệ |
| 5 | **Number literal ngắn gọn** | Dễ đọc, dễ viết — `42`, `3.14`, `1e10` |

## ⚠️ Bẫy thường gặp & Hạn chế

| # | Bẫy | Ví dụ | Cách tránh |
|---|-----|-------|-----------|
| 1 | **`0.1 + 0.2 !== 0.3`** | Sai số IEEE-754 floating point | So sánh với epsilon: `Math.abs(a-b) < Number.EPSILON` |
| 2 | **`new Number(23)` tạo object** | `typeof new Number(23)` → `"object"` | Dùng literal `23` thay `new Number(23)` |
| 3 | **`NaN === NaN` là false** | Không thể dùng `===` kiểm tra NaN | Dùng `Number.isNaN(x)` |
| 4 | **`isNaN("x")` là true** | Global `isNaN` ép kiểu trước check | Dùng `Number.isNaN(x)` — strict, không ép kiểu |
| 5 | **`Math.random()` chỉ `[0, 1)`** | Không bao giờ bằng 1 | Kết hợp `Math.floor(Math.random() * n)` cho integer range |
| 6 | **`(3).toString()` cần parentheses** | `3..toString()` parse lỗi | `(3).toString()` hoặc `String(3)` |
| 7 | **Không an toàn cho tiền tệ** | Floating point precision loss | Dùng integer cents hoặc library như `decimal.js` |

## 💡 Khi nào dùng — Tình huống thực tế

1. **Tính toán hiển thị** — `toFixed(2)` cho giá tiền, phần trăm.
2. **Làm tròn, giá trị tuyệt đối, min/max** — `Math.round`, `Math.ceil`, `Math.floor`, `Math.min`, `Math.max`.
3. **Lấy số ngẫu nhiên trong khoảng** — `Math.floor(Math.random() * (max - min + 1)) + min`.
4. **Kiểm tra NaN trên kết quả phép toán** — dùng `Number.isNaN()` thay `isNaN()`.
5. **Đếm, index, loop counter** — số nguyên `0, 1, 2...`
6. **Timestamp** — `Date.now()` trả number ms từ epoch.
7. **Math/geometry calculations** — `Math.PI`, `Math.sqrt`, `Math.pow`, `Math.sin/cos/tan`.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Các hàm Math cơ bản

```js
var PI = 3.14;
console.log(typeof PI, Math.PI);          // number  3.141592653589793
console.log((22).toString());             // "22"
console.log(Math.round(3.4));             // 3 — làm tròn
console.log(Math.ceil(3.1));              // 4 — làm tròn lên
console.log(Math.floor(3.9));             // 3 — làm tròn xuống
console.log(Math.abs(-15.41));            // 15.41 — giá trị tuyệt đối
console.log(Math.min(5, 9, 4, 8.7, 1));   // 1 — nhỏ nhất
console.log(Math.max(5, 9, 4, 8.7, 1));   // 9 — lớn nhất
console.log(Math.random());               // >= 0, < 1 (random)
console.log(2 ** 10);                     // 1024 — lũy thừa
console.log(Math.sqrt(144));              // 12 — căn bậc hai
```

### Ví dụ 2: Random number trong khoảng [min, max]

```js
// Hàm sinh số nguyên ngẫu nhiên trong [min, max]
function randomInt(min, max) {
  // Math.random() → [0, 1)
  // * (max - min + 1) → [0, max-min+1)
  // Math.floor() → [0, max-min]
  // + min → [min, max]
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

console.log(randomInt(1, 100));  // số ngẫu nhiên từ 1 đến 100
console.log(randomInt(-10, 10)); // số ngẫu nhiên từ -10 đến 10

// Xác thực: chạy 1000 lần, tất cả phải trong range
let allInRange = true;
for (let i = 0; i < 1000; i++) {
  const r = randomInt(1, 10);
  if (r < 1 || r > 10) allInRange = false;
}
console.log('All in range:', allInRange); // true
```

### Ví dụ 3: Kiểm tra NaN và giá trị đặc biệt

```js
console.log(typeof NaN);         // "number"
console.log(NaN === NaN);        // false
console.log(Number.isNaN(NaN));  // true — đúng cách kiểm tra

console.log(isNaN('hello'));     // true — global isNaN ép kiểu (dễ gây nhầm)
console.log(Number.isNaN('hello')); // false — strict, không ép kiểu

console.log(isFinite(Infinity));      // false
console.log(Number.isFinite(42));     // true
console.log(Number.isFinite('42'));   // false — string không phải number

console.log(Object.is(0, -0));       // false — 0 và -0 khác nhau bitwise
console.log(0 === -0);               // true — === không phân biệt 0/-0
```

### Ví dụ 4: Floating point precision — bẫy kinh điển

```js
// Sai số IEEE-754
console.log(0.1 + 0.2);            // 0.30000000000000004 !== 0.3
console.log(0.1 + 0.2 === 0.3);    // false — so sánh trực tiếp sai!

// Cách so sánh an toàn: dùng epsilon
function nearEqual(a, b, epsilon = Number.EPSILON) {
  return Math.abs(a - b) < epsilon;
}
console.log(nearEqual(0.1 + 0.2, 0.3)); // true — so sánh với epsilon

// Với tiền tệ: dùng integer cents thay decimal dollars
const price1 = 1.99;
const price2 = 2.99;
console.log((price1 + price2).toFixed(2)); // "4.98" — hiển thị OK
console.log(price1 + price2 === 4.98);     // false — so sánh float sai
// Giải pháp: làm việc với cents
const cents1 = 199;
const cents2 = 299;
console.log((cents1 + cents2) / 100);      // 4.98 — chính xác
```

### Ví dụ 5: Chuyển số thành chuỗi có định dạng

```js
const num = 42.6789;

console.log(num.toString());           // "42.6789"
console.log(num.toFixed(2));           // "42.68" — làm tròn 2 chữ số
console.log(num.toExponential());      // "4.26789e+1"
console.log(num.toPrecision(4));       // "42.68" — 4 significant digits

// String() an toàn cho mọi giá trị
console.log(String(42));               // "42"
console.log(String(null));             // "null"
console.log(String(undefined));        // "undefined"

// parseInt/parseFloat — trích số từ chuỗi
console.log(parseInt("42px", 10));     // 42 — base 10 rõ ràng
console.log(parseFloat("3.14rem"));    // 3.14
console.log(parseInt("abc123"));       // NaN — không bắt đầu bằng số
console.log(parseInt("12abc"));        // 12 — dừng tại ký tự không phải số
```

## 🔬 So sánh với alternatives

| Phương án | Ưu điểm | Nhược điểm | Phù hợp khi |
|-----------|---------|------------|-------------|
| **Native Number** | Built-in, fast, no dependency | Floating point precision loss | General math, non-financial |
| **BigInt** | Exact integer arithmetic, arbitrary size | Slower, can't mix with Number | Cryptography, large IDs |
| **decimal.js / big.js** | Arbitrary precision decimal | Extra dependency, API学习 | Financial calculations |
| **Integer cents** | Exact for currency, simple | Must convert back/forth | Small-scale money handling |
| **Math.js** | Full math library (matrix, unit, complex) | Heavy dependency | Scientific computing |

## 📊 Performance & Best Practices

- **Dùng `Number.isNaN()`** thay `isNaN()` — không ép kiểu, chính xác hơn.
- **Dùng `Math.abs(a-b) < epsilon`** thay `a === b` cho float comparison.
- **Dùng `Number()` hoặc `parseInt(str, 10)`** thay implicit coercion — explicit hơn, dễ debug.
- **Tránh `new Number()`** — tạo object wrapper, typeof = "object", performance overhead.
- **Base 10 cho `parseInt`** — luôn viết `parseInt(str, 10)` tránh octal interpretation trong old browsers.
- **Tiền tệ dùng integer** — làm việc với cents (integer) thay dollars (float) để tránh precision loss.
- **`Math.random()` không an toàn cho mật mã** — dùng `crypto.getRandomValues()` thay thế khi cần cryptographic security.

## 🔗 Liên kết chéo

- Xem thêm: `02_data-types/01_primitive-types/` — overview primitive types
- Xem thêm: `02_data-types/01_primitive-types/04_bigint/` — bigint khi number không đủ lớn
- Xem thêm: `02_data-types/03_type-casting-and-coercion/02_explicit/` — Number() explicit conversion
- Xem thêm: `02_data-types/04_builtin-objects/01_math/` — Math API deep dive
- Xem thêm: `08_expressions-and-operators/01_operators/` — arithmetic operators
- Tài liệu: [MDN — Number](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number), [MDN — Math](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math)
