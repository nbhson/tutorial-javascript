# Type Conversion vs Coercion — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

Cả hai đều là "chuyển đổi kiểu dữ liệu", nhưng khác nhau ở **ai là người chủ động làm**:

| Tiêu chí | **Conversion** (Explicit — Tường minh) | **Coercion** (Implicit — Ngầm định) |
|----------|----------------------------------------|--------------------------------------|
| **Ai thực hiện** | Lập trình viên (bạn chủ động gọi) | Engine (máy chạy JS tự động) |
| **Hình thức** | Gọi trực tiếp `String()`, `Number()`, `Boolean()`... | Xảy ra tự động trong phép tính/điều kiện |
| **Ví dụ** | `String(123)` → `"123"` | `"5" + 3` → `"53"` |
| **Đọc code** | Rõ ràng, dễ hiểu intent | Phải nắm quy tắc thì mới đoán được |
| **Rủi ro bug** | Thấp | Cao nếu không hiểu luật |

### Conversion (explicit) — bạn chủ động quyết định kiểu đích

```js
// Bạn GỌI hàm chuyển đổi — kết quả 100% đoán trước
String(123);           // "123"
Number("42");          // 42
Boolean(0);            // false
BigInt("9007199254740993"); // 9007199254740993n
parseInt("12px", 10);  // 12
```

### Coercion (implicit) — engine tự ép khi cần

Engine tự ép kiểu trong 4 bối cảnh chính:

1. **Toán tử `==` (loose equality)** — nếu hai vế khác kiểu, engine ép kiểu trước khi so sánh:
   ```js
   "5" == 5;    // true — engine ép "5" → 5 rồi so sánh
   null == undefined; // true — rule đặc biệt trong spec
   ```

2. **Toán tử `+` với có string** — `+` ưu tiên nối chuỗi nếu có ít nhất một operand là string:
   ```js
   1 + "2";     // "12" — string wins, concat
   "a" + true;  // "atrue"
   ```

3. **Toán tử số học `-`, `*`, `/`** — luôn ép sang number:
   ```js
   "5" - 3;     // 2
   "5" * 2;     // 10
   "abc" / 2;   // NaN
   ```

4. **Ngữ cảnh điều kiện (`if`, `&&`, `||`, `!`)** — mọi giá trị bị quy về boolean theo bảng truthy/falsy:
   ```js
   if ("") { /* không chạy */ }  // "" → false (falsy)
   if ([]) { /* chạy */ }        // [] → true  (truthy)
   ```

## 📐 Cấu trúc nhóm

```
02_data-types/03_type-casting-and-coercion/01_conversion-vs-coercion/
├── README.md         ← bài này
└── app.js            ← demo explicit vs implicit
    └── index.html
```

## ✅ Điểm mạnh — Tại sao nên phân biệt rõ

| # | Điểm mạnh | Lý do |
|---|-----------|-------|
| 1 | **Nắm được "quyền chủ động"** | Bạn kiểm soát kết quả khi dùng explicit, không bị bất ngờ bởi implicit |
| 2 | **Explicit giúp code tự giải thích** | Người đọc biết ngay dòng này đang đổi kiểu — dễ review |
| 3 | **Coercion khi hiểu luật giúp viết ngắn** | `if (username)` thay vì `if (username !== null && username !== undefined && username !== "")` |
| 4 | **Phân biệt rõ 2 khái niệm** | Trả lời được câu hỏi phỏng vấn kinh điển: "Conversion vs Coercion là gì?" |
| 5 | **Debug nhanh hơn** | Khi thấy `"abc" - 1` trả `NaN` → nhận ra engine đã coerce string → number (và thất bại) |

## ⚠️ Bẫy thường gặp & Hạn chế

| # | Bẫy | Ví dụ | Cách tránh |
|---|-----|-------|-----------|
| 1 | **Coercion làm code "kỳ lạ"** | `"5" + 3` khác `"5" - 3` dù cùng toán hạng | Hiểu rõ coercion rules theo toán tử |
| 2 | **`+` quyết định theo string presence** | Có string → concat, không có → add | Nhìn vào toán hạng đầu tiên để đoán |
| 3 | **`==` ép kiểu phức tạp** | `0 == false` → true, `"" == 0` → true | Dùng `===` trừ khi chủ đích dùng `==` |
| 4 | **Đọc code có coercion khó cho新人** | Junior dev khó đoán kết quả implicit | Thêm comment giải thích intent |

## 💡 Khi nào dùng — Tình huống thực tế

1. **Muốn kiểm soát hoàn toàn kiểu** → **explicit**: `Number(input)`, `String(id)`.
2. **Viết điều kiện "có giá trị trả về hay không"** → **implicit/truthy** có chủ đích: `if (data)`.
3. **Phân tích bug** — khi thấy `"abc" - 1` trả `NaN` → nhận ra engine coercion theo toán tử số học.
4. **Default value pattern** — `const name = user.name ?? "Khách"` — nullish coalescing, rõ intent hơn `||`.
5. **Loose equality chủ đích** — `if (value == null)` để bắt cả null lẫn undefined.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Explicit conversion — kiểm soát 100%

```js
// String conversion
console.log(String(123), typeof String(123));   // "123" string
console.log(String(null), typeof String(null)); // "null" string

// Number conversion
console.log(Number("42"), typeof Number("42")); // 42 number
console.log(Number("  "), typeof Number("  ")); // 0    number — whitespace → 0!
console.log(Number("abc"), typeof Number("abc"));// NaN  number — not a number!

// Boolean conversion
console.log(Boolean(0), typeof Boolean(0));    // false boolean
console.log(Boolean(""), typeof Boolean(""));  // false boolean
console.log(Boolean([]), typeof Boolean([]));   // true  boolean — array rỗng vẫn truthy!
console.log(Boolean("0"), typeof Boolean("0")); // true  boolean — string "0" không rỗng!
```

### Ví dụ 2: Implicit coercion — engine tự động

```js
// + operator: có string → concat, không có → add
console.log("5" + 3);         // "53" — string wins (concat)
console.log(5 + "3");         // "53" — same, concat
console.log("5" - 3);         // 2    — subtraction always coerces to number
console.log("5" * 2);         // 10   — multiplication always coerces to number
console.log(true + 1);        // 2    — true coerced to 1 (number context)
console.log(false - 1);       // -1   — false coerced to 0

// == operator: coerces both sides
console.log("5" == 5);        // true  — "5" coerced to 5
console.log(null == undefined); // true — special rule in spec
console.log(0 == false);      // true  — 0 == false (both become 0)
console.log("" == 0);         // true  — "" → 0
```

### Ví dụ 3: Truthy/Falsy context — implicit boolean coercion

```js
// if (...) automatically coerces to boolean
if ("") console.log("truthy"); else console.log("falsy empty string");
// → "falsy empty string"

if ([]) console.log("truthy"); else console.log("falsy");
// → "truthy" (mảng rỗng vẫn truthy!)

if ({}) console.log("truthy"); else console.log("falsy");
// → "truthy" (object rỗng vẫn truthy!)

if (0) console.log("truthy"); else console.log("falsy zero");
// → "falsy zero"

// Logical operators
console.log("hello" || "world");       // "hello" — first truthy short-circuits
console.log("" || "world");            // "world" — "" is falsy, returns second
console.log("hello" && "world");       // "world" — first truthy, returns second
console.log("" && "world");            // "" — first falsy, short-circuits
console.log(!undefined);               // true   — ! coerces to boolean, then negates
```

### Ví dụ 4: Phân biệt rõ ràng — cùng giá trị, kết quả khác nhau

```js
const value = "5";

// Explicit: bạn gọi Number() → kết quả 5
const explicit = Number(value);
console.log(explicit);         // 5 — number type
console.log(typeof explicit);  // "number"

// Implicit: engine tự ép trong phép - → kết quả 5
const implicit = value - 0;   // coerce "5" to 5
console.log(implicit);         // 5 — number type
console.log(typeof implicit);  // "number"

// Cùng kết quả số, nhưng:
// Explicit: readable, predictable, intent clear
// Implicit: magical, hard to trace, easy to miss in review
```

### Ví dụ 5: Debug coercion bug — case study thực tế

```js
// Bug report: form returns NaN even when user enters "42"
function calculateTotal(price, quantity) {
  const total = price * quantity;  // implicit coercion happens here
  return total;
}

// Scenario 1: Both strings — works (coerced to numbers)
console.log(calculateTotal("10", "5"));   // 50 ✓

// Scenario 2: One string, one NaN — fails silently
console.log(calculateTotal("10", NaN));    // NaN ✗

// Scenario 3: String with non-numeric — fails silently
console.log(calculateTotal("10", "abc"));  // NaN ✗

// Fix: explicit conversion + validation
function calculateTotalFixed(price, quantity) {
  const p = Number(price);
  const q = Number(quantity);

  if (Number.isNaN(p) || Number.isNaN(q)) {
    throw new Error(`Invalid inputs: price=${price}, qty=${quantity}`);
  }
  return p * q;
}

console.log(calculateTotalFixed("10", "5"));     // 50 ✓
console.log(calculateTotalFixed("10", "abc"));   // throws Error ✓
```

## 🔬 So sánh với alternatives

| Phương án | Ưu điểm | Nhược điểm |
|-----------|---------|------------|
| **Always explicit** | Predictable, self-documenting | More verbose |
| **Rely on coercion** | Concise, idiomatic JS | Hard to predict, debugging painful |
| **TypeScript** | Compile-time safety, no runtime coercion surprises | Build step, learning curve |
| **Runtime type guards** | Explicit at point of use | Boilerplate code |

## 📊 Performance & Best Practices

- **Trong production, ưu tiên explicit** — `Number(value)` thay vì `+value` — rõ intent, dễ debug.
- **Hiểu coercion rules** — biết `+` concat khi có string, `-` luôn coerce to number.
- **Luôn dùng `===`** trừ khi có lý do chính đáng dùng `==`.
- **Kiểm tra trước khi coerce** — `typeof input === "string" && /^\d+$/.test(input)` trước `Number()`.
- **Sử dụng ESLint `no-coercion`** — warn khi implicit coercion detected.
- **Document expected types** — JSDoc `@param {number} price` giúp reader hiểu intent.

## 🔗 Liên kết chéo

- Xem thêm: `02_data-types/03_type-casting-and-coercion/02_explicit/` — explicit conversion functions detail
- Xem thêm: `02_data-types/03_type-casting-and-coercion/03_implicit/` — implicit coercion rules deep dive
- Xem thêm: `02_data-types/01_primitive-types/06_null-undefined-boolean/` — truthy/falsy 8 values
- Xem thêm: `04_equality-comparisons/` — `==` vs `===` behavior
- Tài liệu: [MDN — Abstract Equality](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Equality), [javascript.info/type-conversions](https://javascript.info/type-conversions)
