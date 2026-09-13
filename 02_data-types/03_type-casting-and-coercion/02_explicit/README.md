# Explicit Type Casting (Ép kiểu tường minh) — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

**Explicit type casting** là việc lập trình viên **chủ động** chuyển một giá trị từ kiểu này sang kiểu khác bằng các hàm quy đổi chuẩn của JavaScript. Đây là cách được khuyến nghị nhất trong production vì **code tự mô tả ý định** và không phụ thuộc quy tắc ngầm của engine.

### Bộ 6 hàm quy đổi chính

| Hàm | Ví dụ | Kết quả | Ghi chú |
|-----|-------|---------|---------|
| **`String(x)`** | `String(123)` | `"123"` | `String(null)` → `"null"`, `String(undefined)` → `"undefined"` |
| **`Number(x)`** | `Number("42")` | `42` | `Number("  ")` → `0`; `Number("abc")` → `NaN` |
| **`Boolean(x)`** | `Boolean(0)` | `false` | `Boolean([])` → `true`; `Boolean({})` → `true` |
| **`BigInt(x)`** | `BigInt("123")` | `123n` | Chỉ chuyển số nguyên, không chuyển float |
| **`Symbol(desc)`** | `Symbol("id")` | `Symbol(id)` | Tạo unique symbol — không phải ép kiểu |
| **`parseInt/parseFloat`** | `parseInt("12px")` | `12` | Đọc số từ đầu chuỗi, dừng tại ký tự không phải số |

### Bảng kết quả quan trọng — nhớ kỹ

```js
// String conversions
String(123);              // "123"
String(null);             // "null"
String(undefined);        // "undefined"
String(true);             // "true"
String([1, 2]);           // "1,2" — array joined by comma
String({ a: 1 });         // "[object Object]"

// Number conversions — CAREFUL with edge cases
Number("42");             // 42
Number("  ");             // 0     ← chuỗi toàn khoảng trắng → 0!
Number("");               // 0     ← chuỗi rỗng → 0!
Number("abc");            // NaN   ← không phải số → NaN
Number(true);             // 1     ← boolean → 1/0
Number(false);            // 0
Number(null);             // 0     ← null → 0
Number(undefined);        // NaN   ← undefined → NaN
Number("10px");           // NaN   ← có suffix → NaN (khác parseInt!)
Number(new Date());       // timestamp number
Number("1.5e2");          // 150   ← scientific notation supported

// Boolean conversions — 8 falsy values
Boolean(0);               // false
Boolean(-0);              // false
Boolean(0n);              // false
Boolean("");              // false
Boolean(null);            // false
Boolean(undefined);       // false
Boolean(NaN);             // false
Boolean(false);           // false

// TRUE for everything else:
Boolean(1);               // true
Boolean("0");             // true  ← chuỗi "0" KHÔNG rỗng!
Boolean("false");         // true  ← chuỗi "false" vẫn truthy!
Boolean([]);              // true  ← mảng rỗng vẫn truthy!
Boolean({});              // true  ← object rỗng vẫn truthy!
Boolean(function(){});    // true
Boolean(new Date());      // true

// BigInt conversions
BigInt("123");            // 123n
BigInt(123);              // 123n
BigInt("12.3");           // ❌ SyntaxError — không chấp nhận float string
BigInt("abc");            // ❌ SyntaxError

// parseInt vs Number — khác nhau quan trọng
parseInt("12px", 10);     // 12   — trích số từ đầu chuỗi
parseInt("12.5px", 10);   // 12   — trích integer, bỏ decimal
parseInt("abc123", 10);   // NaN  — không bắt đầu bằng số
parseInt("  42  ", 10);   // 42   — bỏ whitespace hai đầu
Number("12px");           // NaN  — phải là số nguyên, có suffix → NaN

// parseFloat
parseFloat("12.5px");     // 12.5 — trích số thập phân từ đầu chuỗi
parseFloat("12.5.6px");   // 12.5 — dừng tại ký tự không hợp lệ
```

### Các trường hợp "kỳ lạ" bạn phải nhớ

```js
Number("42");      // 42
Number("  ");      // 0     ← chuỗi toàn khoảng trắng → 0
Number("abc");     // NaN   ← không phải số → NaN
Number(true);      // 1     ← boolean → 1/0
String(null);      // "null"
String(undefined); // "undefined"
Boolean(0);        // false
Boolean("");       // false
Boolean([]);       // true  ← mảng rỗng vẫn truthy!
```

## 📐 Cấu trúc nhóm

```
02_data-types/03_type-casting-and-coercion/02_explicit/
├── README.md         ← bài này
└── app.js            ← demo explicit conversions
    └── index.html
```

## ✅ Điểm mạnh — Tại sao dùng explicit conversion

| # | Điểm mạnh | Lý do |
|---|-----------|-------|
| 1 | **Code rõ ràng, tự giải thích** | Người đọc biết ngay dòng này đang đổi kiểu — đọc code như đọc văn |
| 2 | **Không phụ thuộc quy tắc implicit** | Kết quả đoán trước được 100%, không surprise |
| 3 | **`parseInt("12px")` thực dụng** | Xử lý CSS value có đơn vị — rất phổ biến trong DOM manipulation |
| 4 | **An toàn hơn với dữ liệu ngoài** | Form input, API response luôn cần validate/convert before use |
| 5 | **Debug dễ hơn** | Khi có lỗi, bạn biết ngay chuyển đổi nào thất bại |
| 6 | **Self-documenting** | `Number(input)` nói rõ intent hơn `+input` |

## ⚠️ Bẫy thường gặp & Hạn chế

| # | Bẫy | Ví dụ | Cách tránh |
|---|-----|-------|-----------|
| 1 | **`Number("abc")` → NaN, không lỗi** | ép số thất bại im lặng — downstream tính toán sai | Kiểm tra `Number.isNaN(result)` sau khi convert |
| 2 | **`Number("  ")` → 0** | chuỗi whitespace thành 0 — gây hiểu lầm | Kiểm tra `trim()` trước, hoặc dùng `parseInt` |
| 3 | **`Boolean([])`/`Boolean({})` là `true`** | bẫy khi kiểm tra "mảng rỗng" | Dùng `Array.isArray(arr) && arr.length === 0` |
| 4 | **`parseInt` khác `Number`** | `parseInt("12px")` → 12, `Number("12px")` → NaN | Dùng `parseInt` cho CSS, `Number` cho pure number input |
| 5 | **`BigInt("12.3")` throw** | BigInt không chấp nhận float string | Dùng `Number()` cho float, `BigInt()` chỉ cho integer |
| 6 | **`String(undefined)` → `"undefined"`** | có thể gây bug nếu không expect | Check nullish before String() convert |

## 💡 Khi nào dùng — Tình huống thực tế

1. **Chuyển input form (luôn là string) sang số** — `Number(input.value)` để tính toán.
2. **Hiển thị giá trị động vào chuỗi** — `String(id)` cho template string interpolation.
3. **Chuẩn hóa dữ liệu đầu vào** — validate/convert trước khi lưu vào state hoặc gửi API.
4. **Đọc thuộc tính CSS** — `parseInt(style.width)` bỏ đơn vị `px` → số nguyên.
5. **Parse version string** — `parseInt("v2.3.1".match(/\d+/)[0])` → 2.
6. **Validate boolean flag** — `Boolean(parseInt(rawFlag))` để convert string "true"/"false".

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: 6 hàm conversion cơ bản

```js
// String
console.log(String(123), String(null), String(undefined));
// "123" "null" "undefined"

// Number — edge cases
console.log(Number("42"), Number("  "), Number("abc"), Number(true));
// 42 0 NaN 1

// Boolean
console.log(Boolean(0), Boolean(""), Boolean([]), Boolean({}), Boolean("0"));
// false false true true true

// BigInt
console.log(BigInt("123"));         // 123n
console.log(BigInt(123));           // 123n
// console.log(BigInt("12.3"));     // ❌ SyntaxError

// parseInt vs Number
console.log(parseInt("12px", 10));  // 12   — CSS parsing
console.log(Number("12px"));        // NaN  — pure number required
console.log(parseFloat("3.14rem")); // 3.14 — decimal CSS
```

### Ví dụ 2: parseInt vs Number vs parseFloat — so sánh chi tiết

```js
const testValues = ["42", "42px", "  42  ", "abc", "", "12.5", "12.5.6", "-3.14"];

for (const v of testValues) {
  console.log(
    `Input: "${v}"`,
    `| Number: ${Number(v)}`,
    `| parseInt: ${parseInt(v, 10)}`,
    `| parseFloat: ${parseFloat(v)}`
  );
}
/*
Input: "42"          | Number: 42         | parseInt: 42   | parseFloat: 42
Input: "42px"        | Number: NaN        | parseInt: 42   | parseFloat: 42
Input: "  42  "      | Number: 42         | parseInt: 42   | parseFloat: 42
Input: "abc"         | Number: NaN        | parseInt: NaN  | parseFloat: NaN
Input: ""            | Number: 0          | parseInt: NaN  | parseFloat: NaN
Input: "12.5"        | Number: 12.5       | parseInt: 12   | parseFloat: 12.5
Input: "12.5.6"      | Number: NaN        | parseInt: 12   | parseFloat: 12.5
Input: "-3.14"       | Number: -3.14      | parseInt: -3   | parseFloat: -3.14
*/
```

### Ví dụ 3: Validate form input — real-world pattern

```js
function parseAge(input) {
  // Bước 1: Check nullish
  if (input == null) return null;

  // Bước 2: Trim và convert to number
  const num = Number(String(input).trim());

  // Bước 3: Check valid number
  if (Number.isNaN(num)) return null;

  // Bước 4: Check integer and range
  if (!Number.isInteger(num)) return null;
  if (num < 0 || num > 150) return null;

  return num;
}

console.log(parseAge("25"));       // 25 ✓
console.log(parseAge("  30  "));   // 30 ✓
console.log(parseAge("abc"));      // null — invalid
console.log(parseAge(null));       // null — nullish
console.log(parseAge("25.5"));     // null — not integer
console.log(parseAge("-5"));       // null — out of range
```

### Ví dụ 4: CSS parsing — parseInt real use case

```js
// Giả sử có element với style inline
const box = document.getElementById("box");
const style = getComputedStyle(box);

// CSS property luôn là string, có đơn vị
const widthStr = style.width;    // "200px"
const heightStr = style.height;  // "150px"

//parseInt extract number, bỏ px
const width = parseInt(widthStr, 10);   // 200
const height = parseInt(heightStr, 10); // 150

console.log(width * height);            // 30000 — square pixels

// parseFloat cho decimal values (transform, opacity...)
const opacity = parseFloat(style.opacity); // "0.75" → 0.75
const scale = parseFloat(style.transform); // "scale(1.5)" → 1.5
```

### Ví dụ 5: Error handling khi convert thất bại

```js
function safeNumber(value, fallback = 0) {
  const num = Number(value);
  // Check if conversion produced NaN — then return fallback
  return Number.isNaN(num) ? fallback : num;
}

function safeInt(value, fallback = 0) {
  const num = parseInt(String(value), 10);
  return Number.isNaN(num) ? fallback : num;
}

console.log(safeNumber("42"));     // 42
console.log(safeNumber("abc"));    // 0 (fallback)
console.log(safeNumber(null));     // 0 (fallback)
console.log(safeInt("10px"));      // 10
console.log(safeInt("invalid"));   // 0 (fallback)
```

## 🔬 So sánh với alternatives

| Phương án | Ưu điểm | Nhược điểm | Phù hợp khi |
|-----------|---------|------------|-------------|
| **`Number()`** | Handles all types, handles scientific notation | NaN on any non-numeric string | Pure numeric conversion |
| **`parseInt(str, radix)`** | Extracts leading number from string | Ignores decimals, base confusion risk | CSS, version parsing |
| **`parseFloat(str)`** | Extracts decimal number | No radix control, similar to parseInt | Decimal values from strings |
| **Unary `+str`** | Shortest syntax | Same rules as `Number()`, less readable | Quick snippets, not production code |
| **Template literal `` `${x}` ``** | Convert to string, clean | Only for string output | String interpolation |

## 📊 Performance & Best Practices

- **Mặc định dùng `Number()`** cho pure numeric conversion — handles edge cases well.
- **Dùng `parseInt(str, 10)`** cho string parse với base 10 explicit — avoid octal in old browsers.
- **Dùng `parseFloat()`** cho decimal values from CSS or mixed strings.
- **Check `Number.isNaN()`** sau khi convert — phát hiện thất bại im lặng.
- **Prefer explicit over implicit** — `Number(input)` đọc rõ hơn `+input`.
- **Avoid `new String/Number/Boolean`** — tạo object wrapper, `typeof` sai.
- **Validate input before convert** — regex check `^\d+$` before `Number()` for strict integer validation.
- **Use TypeScript `as number`** trong project TS — compile-time type assertion.

## 🔗 Liên kết chéo

- Xem thêm: `02_data-types/03_type-casting-and-coercion/01_conversion-vs-coercion/` — phân biệt explicit vs implicit
- Xem thêm: `02_data-types/03_type-casting-and-coercion/03_implicit/` — implicit coercion rules
- Xem thêm: `02_data-types/01_primitive-types/02_number/` — number NaN, Infinity
- Xem thêm: `02_data-types/01_primitive-types/04_bigint/` — BigInt conversion
- Tài liệu: [MDN — Number()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/Number), [javascript.info/type-conversions](https://javascript.info/type-conversions)
