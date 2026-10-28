# Built-in Objects — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

JavaScript đi kèm với hàng tá **built-in objects** (đối tượng có sẵn) được engine tích hợp sẵn — bạn không cần viết lại. Chúng cung cấp functionality cốt lõi cho mọi program: số học, thời gian, regex, error handling, serialization...

### Danh sách các built-in object quan trọng

| Đối tượng | Loại | Ghi chú |
|-----------|------|---------|
| **`Object`** | Constructor | Base class của mọi object — `Object.create()`, `Object.keys()` |
| **`Function`** | Constructor | Base class của mọi function — `fn.call()`, `fn.apply()`, `fn.bind()` |
| **`Array`** | Constructor | List ordered — `push`, `pop`, `map`, `filter`, `reduce` |
| **`String`** | Wrapper | Cho primitive string — `toUpperCase`, `split`, `includes` |
| **`Number`** | Wrapper | Cho primitive number — `toFixed`, `toExponential` |
| **`Boolean`** | Wrapper | Cho primitive boolean — `toString`, `valueOf` |
| **`Math`** | Namespace object | **KHÔNG có constructor** — chỉ access properties/methods via `Math.xxx` |
| **`Date`** | Constructor | Thời gian — `new Date()`, `toISOString()`, `getTime()` |
| **`RegExp`** | Constructor | Pattern matching — `/pattern/flags`, `test()`, `match()` |
| **`Error`** | Constructor | Exception types — `TypeError`, `ReferenceError`, `SyntaxError`... |
| **`JSON`** | Namespace object | Parse/stringify — `JSON.parse()`, `JSON.stringify()` |
| **`Map`** | Constructor | Key-value with any key type — `set()`, `get()`, `has()`, `size` |
| **`Set`** | Constructor | Unique values collection — `add()`, `has()`, `delete()` |
| **`Promise`** | Constructor | Async operation — `.then()`, `.catch()`, `async/await` |
| **`Symbol`** | Primitive factory | Unique values — `Symbol()`, `Symbol.iterator` |
| **`BigInt`** | Primitive factory | Large integers — `BigInt()`, `123n` literal |
| **`Proxy`** | Constructor | Intercept object operations — `new Proxy(target, handler)` |
| **`Reflect`** | Namespace object | Reflection API — `Reflect.get()`, `Reflect.apply()` |

> **`Math` là duy nhất trong nhóm này:** nó **không có constructor** (`new Math()` sẽ lỗi), chỉ là "namespace" chứa hàm/hằng số. Tất cả các đối tượng còn lại đều có constructor function — có thể `new Math()` là lỗi, `new Date()` là OK.

### Nhóm này gồm 4 bài nhỏ

Mỗi bài tập trung vào một built-in object quan trọng nhất:
- `01_math/` — Math API: hằng số, hàm số học.
- `02_date/` — Date API: tạo, định dạng, tính toán thời gian.
- `03_regexp/` — RegExp API: pattern matching, validation.
- `04_error/` — Error API: throw, catch, error types.

## 📐 Cấu trúc nhóm

```
02_data-types/04_builtin-objects/
├── README.md                          ← bài tổng quan này
├── 01_math/
│   ├── README.md
│   ├── app.js
│   └── index.html
├── 02_date/
│   ├── README.md
│   ├── app.js
│   └── index.html
├── 03_regexp/
│   ├── README.md
│   ├── app.js
│   └── index.html
└── 04_error/
    ├── README.md
    ├── app.js
    └── index.html
```

## ✅ Điểm mạnh — Tại sao dùng built-in objects

| # | Điểm mạnh | Lý do |
|---|-----------|-------|
| 1 | **Tái sử dụng code chuẩn** | Không tự viết `sin()`, `random()`, `parseISO()` — engine tối ưu sẵn |
| 2 | **Math API mạnh mẽ** |PI, round, abs, random... giải quyết đúng việc thường gặp |
| 3 | **Date chuẩn hóa toàn cầu** | Timestamp ms, ISO string — so sánh/trừ ngày bằng số rất an toàn |
| 4 | **RegExp & Error được tối ưu nguyên bản** | Nhanh hơn thư viện bên ngoài, tích hợp engine |
| 5 | **Hiểu built-in → đọc code hiện đại** | Mọi codebase đều dùng Date, RegExp, Error, JSON |

## ⚠️ Bẫy thường gặp & Hạn chế

| # | Bẫy | Ví dụ | Cách tránh |
|---|-----|-------|-----------|
| 1 | **`new String(1)` tạo object, không primitive** | `typeof new String(1)` → `"object"` | Dùng `String(1)` thay `new String(1)` |
| 2 | **Date tháng bắt đầu từ 0** | `new Date(2024, 1, 1)` → tháng 2, không phải tháng 1! | Nhớ `month = actualMonth - 1` |
| 3 | **RegExp slash syntax dễ nhầm** | `/ab+c/g` vs `new RegExp("ab+c", "g")` — cần escape khác nhau | Dùng regex literal cho static patterns |
| 4 | **Math không có constructor** | `new Math()` → TypeError | Dùng `Math.PI`, `Math.max()` thay |
| 5 | **Date mutable** | `d.setDate(d.getDate() + 1)` sửa object gốc | Clone trước: `new Date(d.getTime())` |
| 6 | **Error properties differ by type** | `e.name`, `e.message`, `e.stack` — không phải lỗi nào cũng có đủ | Dùng `instanceof` check types |

## 💡 Khi nào dùng — Tình huống thực tế

1. **Tính toán, làm tròn, giá trị tuyệt đối, random trong khoảng** → `Math`.
2. **Hiển thị/lưu lại thời gian** → `Date` + `toISOString()` / `toLocaleDateString()`.
3. **Validate email, tìm text mẫu, replace theo pattern** → `RegExp`.
4. **Bắt và xử lý lỗi runtime** → `try/catch` + `Error` subclasses.
5. **Chuyển object ↔ JSON** → `JSON.parse()` / `JSON.stringify()`.
6. **Map/Set cho key-value hoặc unique collection** → `Map`, `Set`.
7. **Proxy cho intercepting operations** — logging, validation, lazy loading.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Math namespace — no constructor

```js
// Math là object, KHÔNG có constructor
// new Math(); // ❌ TypeError: Do not construct Math

console.log(Math.PI);              // 3.141592653589793
console.log(Math.E);               // 2.718281828459045
console.log(Math.sqrt(144));       // 12
console.log(Math.pow(2, 10));      // 1024
console.log(2 ** 10);              // 1024  — ES7 exponentiation
console.log(Math.random());        // 0 ≤ r < 1
console.log(Math.round(3.6));      // 4
console.log(Math.ceil(3.1));       // 4
console.log(Math.floor(3.9));      // 3
console.log(Math.abs(-15.41));     // 15.41
console.log(Math.max(1, 5, 3));    // 5
console.log(Math.min(...[8, 3, 5])); // 3  — spread array
```

### Ví dụ 2: Date — timestamp and formatting

```js
const now = new Date();
console.log(now.toISOString());       // "2025-08-30T07:00:00.000Z"
console.log(now.getTime());           // 1725012345678
console.log(Date.now());              // ~same as getTime() — faster (no object)

// Create from various inputs
const fromString = new Date("2024-01-01T00:00:00Z");
const fromParts = new Date(2024, 0, 1, 12, 30, 0);  // month 0 = January!
const fromTimestamp = new Date(1704067200000);

// ⚠️ IMPORTANT: month is 0-indexed!
console.log(fromParts.toLocaleDateString("vi-VN")); // "1/1/2024"

// Calculate difference in days
const start = new Date("2024-01-01");
const end = new Date("2024-01-03");
const daysDiff = (end.getTime() - start.getTime()) / 86400000;
console.log(daysDiff); // 2

// Format for display
console.log(now.toLocaleDateString("vi-VN"));    // "30/8/2025"
console.log(now.toLocaleTimeString("vi-VN"));    // "14:00:00"
console.log(now.toLocaleString("vi-VN"));        // "30/8/2025, 14:00:00"
```

### Ví dụ 3: RegExp — pattern matching

```js
// Regex literal (recommended for static patterns)
const re = /ab+c/g;

console.log(re.test("abbbc"));         // true
console.log("abc".match(re));          // ["abc"] — global returns all matches
console.log("abbbcabc".match(/ab+c/g)); // ["abbbc", "abc"]

// Replace
console.log("abbbc".replace(/b+/, "X")); // "aXc"
console.log("a2 b4 c8".replace(/\d/g, "X")); // "aX bX cX"

// Common patterns
const emailRe = /^[\w.-]+@[\w.-]+\.\w+$/;
console.log(emailRe.test("nam@example.com")); // true
console.log(emailRe.test("invalid"));          // false

const vnPhoneRe = /^0[3-9]\d{8}$/;
console.log(vnPhoneRe.test("0901234567")); // true
```

### Ví dụ 4: Error — throw and catch

```js
// Different error types
try {
  throw new TypeError("bad type");
} catch (e) {
  console.log(e.name);      // "TypeError" — error type name
  console.log(e.message);   // "bad type" — custom message
  console.log(e.stack);     // stack trace — where error occurred
}

// Error types and when they occur
try { null.x; } catch (e) { console.log(e.name); }       // TypeError

try { undefinedVar; } catch (e) { console.log(e.name); }  // ReferenceError

try { eval("return;"); } catch (e) { console.log(e.name); } // SyntaxError (in some contexts)

try { new Array(1e10); } catch (e) { console.log(e.name); } // RangeError

// Check error type with instanceof
try {
  null.x;
} catch (e) {
  console.log(e instanceof TypeError); // true
}
```

## 🔬 So sánh với alternatives

| Đối tượng | Thay thế thư viện | Ưu điểm built-in | Nhược điểm |
|-----------|------------------|-----------------|------------|
| **Math** | math.js, numerical | Fast, no dependency | Less advanced (no matrices) |
| **Date** | date-fns, dayjs, luxon | Built-in, no install | API clunky (0-indexed months) |
| **RegExp** | — | Optimized natively | Complex syntax, easy to write wrong |
| **Error** | custom error classes | Standardized, stack trace | Limited customization |

## 📊 Performance & Best Practices

- **Dùng `Date.now()`** thay `new Date().getTime()` — faster, no object allocation.
- **Dùng regex literal** `/pattern/flags` thay `new RegExp(string, flags)` — cleaner, no double-escaping.
- **Always specify radix in `parseInt`** — `parseInt(str, 10)` tránh octal interpretation.
- **Clone Date before mutating** — `const copy = new Date(d.getTime())` để tránh mutate original.
- **Use specific Error subclasses** — `TypeError` thay vì generic `Error` — easier debugging.
- **Check `instanceof Error`** trong catch — handle different error types differently.
- **Use `JSON.parse` with reviver** — transform data during deserialization.

## 🔗 Liên kết chéo

- Xem thêm: `02_data-types/04_builtin-objects/01_math/` — Math API chi tiết
- Xem thêm: `02_data-types/04_builtin-objects/02_date/` — Date API chi tiết
- Xem thêm: `02_data-types/04_builtin-objects/03_regexp/` — RegExp API chi tiết
- Xem thêm: `02_data-types/04_builtin-objects/04_error/` — Error API chi tiết
- Xem thêm: `07_exceptional-handling/` — try/catch/finally deep dive
- Tài liệu: [MDN — Built-in objects](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects), [ECMAScript Spec — Built-in objects](https://tc39.es/ecma262/#sec-built-in-object-types)
