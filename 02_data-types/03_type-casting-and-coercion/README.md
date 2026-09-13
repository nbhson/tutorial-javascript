# Type Casting & Coercion (Ép kiểu tường minh và ngầm định) — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

JavaScript là ngôn ngữ **kiểu động (dynamic typing)** — kiểu của biến được xác định tại runtime, và cùng một biến có thể đổi kiểu. Hệ quả tất yếu: JavaScript **tự động chuyển đổi kiểu dữ liệu** khi cần, gọi chung là **type conversion**. Có hai "hình thức":

1. **Conversion (explicit — tường minh):** lập trình viên **chủ động** gọi `String()`, `Number()`, `Boolean()`... để quy đổi kiểu:
   ```js
   String(123);  // "123"
   Number("42"); // 42
   Boolean(0);   // false
   ```

2. **Coercion (implicit — ngầm định):** **engine tự ép kiểu** trong các phép toán/bối cảnh mà không ai chủ động chuyển:
   ```js
   "5" + 3;         // "53"  — ưu tiên nối chuỗi
   "5" - 3;         // 2     — ưu tiên số học
   null == undefined; // true — loose equality tự "thả"
   if ("") { /* falsy */ }
   ```

**Tại sao phải nắm vững?** `"5" + 3` cho `"53"` còn `"5" - 3` cho `2` — cùng toán hạng, kết quả khác hoàn toàn tùy theo toán tử. Nắm vững quy tắc này tránh vô số bug "khó hiểu" nhất của JavaScript.

### General về truthy/falsy (dùng trong `if`, `&&`, `||`, `!`)

- **Falsy (đúng 8 giá trị):** `false`, `0`, `-0`, `0n`, `""` (chuỗi rỗng), `null`, `undefined`, `NaN`.
- **Truthy:** mọi thứ còn lại — bao gồm `[]`, `{}`, `"0"`, `"false"`, `Infinity`, `Symbol()`, `function(){}`.

> Xem chi tiết truthy/falsy ở `02_data-types/01_primitive-types/06_null-undefined-boolean/`.

## 📐 Cấu trúc nhóm

```
02_data-types/03_type-casting-and-coercion/
├── README.md                      ← bài tổng quan này
├── 01_conversion-vs-coercion/     ← phân biệt conversion vs coercion
├── 02_explicit/                   ← explicit type casting
└── 03_implicit/                   ← implicit coercion rules
```

## ✅ Điểm mạnh — Tại sao nên học topic này

| # | Lợi ích | Lý do |
|---|---------|-------|
| 1 | **Code gọn, linh hoạt** | Không cần khai báo kiểu, dữ liệu "tự thích nghi" theo ngữ cảnh |
| 2 | **Coercion đôi lúc tiện** | Nối chuỗi với số, kiểm tra truthy/falsy nhanh — viết code ngắn hơn |
| 3 | **Duck typing** | Chỉ cần đối tượng "đi như vịt" thì dùng được — flexible API design |
| 4 | **Rapid prototyping** | Không bị ràng buộc kiểu ở giai đoạn đầu — phát triển nhanh |

## ⚠️ Bẫy thường gặp & Hạn chế

| # | Bẫy | Ví dụ | Cách tránh |
|---|-----|-------|-----------|
| 1 | **Ép kiểu ngầm gây bug** | `[] + []` → `""`, `{} + []` → `0` — kết quả không đoán trước | Ưu tiên explicit conversion trong production |
| 2 | **`Number("abc")` → NaN, không lỗi** | Ép số thất bại im lặng, downstream tính toán lỗi | Kiểm tra `isNaN()` sau khi chuyển |
| 3 | **`Number("  ")` → 0** | Chuỗi chỉ whitespace thành 0 — khó debug | Dùng `parseInt()` hoặc regex validation trước |
| 4 | **`null == undefined` → true** | Loose equality bắt cả null và undefined | Dùng `===` hoặc `value != null` pattern |
| 5 | **Dùng `==` dễ sai** | `"5" == 5`, `0 == false`, `"" == 0` — tất cả true | Luôn dùng `===` trừ khi chủ đích dùng `==` |
| 6 | **JSON serialization mất data** | `undefined`, `function` → bị bỏ qua | Chuyển kiểu trước khi `JSON.stringify` |

## 💡 Khi nào dùng — Tình huống thực tế

1. **Đọc input từ form/API (luôn là string) và cần tính toán** → `Number(input.value)`.
2. **Gửi dữ liệu lên server** → chuyển object về chuỗi JSON, số về string: `JSON.stringify(data)`.
3. **Kiểm tra một giá trị "có đáng tin" hay không** → rely truthy/falsy trong điều kiện `if (data)`.
4. **Khi cần so sánh lỏng thật sự có chủ đích** → `== null` để bắt cả null lẫn undefined.
5. **Parse CSS value có đơn vị** → `parseInt(style.width)` → `100` từ `"100px"`.
6. **Validate user input** → `Number.isFinite(Number(input))` trước khi xử lý.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Explicit vs Implicit — khác nhau ở "ai quyết định"

```js
// ── Explicit Conversion — bạn chủ động gọi hàm ──
console.log(String(123));      // "123" — number → string
console.log(Number("42"));     // 42 — string → number
console.log(Boolean(0));       // false — number → boolean
console.log(Boolean(""));      // false — empty string → false
console.log(Boolean([]));      // true — array rỗng vẫn truthy!

// ── Implicit Coercion — engine tự ép kiểu ──
console.log("5" + 3);          // "53"  — + có string → nối chuỗi
console.log("5" - 3);          // 2     — - luôn ép number
console.log("5" * 2);          // 10    — * luôn ép number
console.log(null == undefined); // true  — == loosely compare
```

### Ví dụ 2: Toán tử quyết định hướng ép kiểu

```js
// + quyết định theo sự hiện diện của string
console.log(1 + "2");        // "12"  — có string → nối chuỗi
console.log("1" + 2 + 3);    // "123" — left-to-right: "1"+2="12", then "12"+3="123"

// Các toán tử số học LUÔN ép sang number
console.log("5" - 3);        // 2
console.log("5" * 2);        // 10
console.log("10" / 2);       // 5
console.log("10" % 3);       // 1

// Boolean context → truthy/falsy check
console.log(Boolean("hello")); // true — string không rỗng là truthy
console.log(Boolean(0));       // false
console.log(Boolean([]));      // true — array rỗng vẫn truthy!
console.log(Boolean({}));      // true — object rỗng vẫn truthy!
```

### Ví dụ 3: Bẫy kinh điển — kết quả không đoán trước

```js
console.log([] + []);         // ""     — both coerce to "" and concat
console.log({} + []);         // 0      — {} parsed as empty block, then +[] → 0
console.log([] + {});         // "[object Object]"
console.log({} + {});         // "[object Object]" — parse {} as block
console.log("9" > "10");      // true   — string comparison by character: '9' > '1'

// Loophole: == bắt cả null và undefined
const val = null;
if (val == null) console.log("null or undefined"); // "null or undefined"

// NaN propagation
console.log(NaN + 1);         // NaN
console.log("abc" - 1);       // NaN
```

### Ví dụ 4: Thực hành thực tế — validate form input

```js
function processUserInput(rawInput) {
  // Bước 1: Kiểm tra truthiness (implicit coercion trong if)
  if (!rawInput) {
    return { error: "Input cannot be empty" };
  }

  // Bước 2: Explicit conversion — trim và chuyển thành number
  const trimmed = String(rawInput).trim();
  const numeric = Number(trimmed);

  // Bước 3: Kiểm tra valid number
  if (Number.isNaN(numeric)) {
    return { error: "Input must be a valid number" };
  }

  // Bước 4: Validate range
  if (!Number.isFinite(numeric)) {
    return { error: "Input must be a finite number" };
  }

  return { value: numeric, raw: trimmed };
}

console.log(processUserInput("  42  "));
// { value: 42, raw: "42" }

console.log(processUserInput("abc"));
// { error: "Input must be a valid number" }

console.log(processUserInput(""));
// { error: "Input cannot be empty" }
```

### Ví dụ 5: Coercion với đối tượng — valueOf vs toString

```js
const obj = {
  valueOf() { return 42; },
  toString() { return "42"; },
};

// Arithmetic → prefer valueOf
console.log(obj + 1);         // 43 — obj.valueOf() = 42, then 42 + 1

// String context → prefer toString
console.log("Result: " + obj); // "Result: 42" — obj.toString() = "42"

// Object without proper conversion
const plainObj = { x: 1 };
console.log(plainObj + 1);    // "1[object Object]" — toString() called
```

## 🔬 So sánh với alternatives

| Phương án | Ưu điểm | Nhược điểm |
|-----------|---------|------------|
| **Explicit conversion** (`Number()`, `String()`) | Rõ ràng, dễ đọc, đoán trước kết quả |Verbose hơn |
| **Implicit coercion** (engine tự ép) | Code ngắn, tự nhiên trong điều kiện | Dễ gây bug, khó debug |
| **TypeScript strict types** | Compile-time type safety | Cần transpile, learning curve |
| **JSONSchema validation** | Schema-driven, self-documenting | Heavy setup for simple cases |
| **Manual type checking** (`typeof`, `instanceof`) | Control exactly what types accepted | Verbose, must check every input |

## 📊 Performance & Best Practices

- **Production: ưu tiên explicit conversion** — `Number(value)` thay vì đinh ninh `+value` luôn đúng ý bạn.
- **Luôn dùng `===`** trừ khi chủ định dùng `==` để bắt cả null và undefined (`value != null`).
- **Kiểm tra `Number.isNaN()` sau khi convert** — `Number("abc")` → `NaN`, không lỗi, downstream sẽ lỗi.
- **Dùng `parseInt(str, 10)`** thay implicit number convert cho string-parse — rõ intent, base 10 explicit.
- **Validate before coerce** — `if (typeof input === "string" && /^\d+$/.test(input))` trước khi `Number()`.
- **Avoid coercion in comparisons** — `"5" == 5` là true nhưng dễ gây hiểu lầm; dùng `===`.
- **Know the coercion table** — đọc MDN "Abstract Equality Comparison" để hiểu luật `==`.
- **Use ESLint `no-coercion` or `eqeqeq`** — enforce `===` instead of `==`.

## 🔗 Liên kết chéo

- Xem thêm: `02_data-types/03_type-casting-and-coercion/01_conversion-vs-coercion/` — phân biệt explicit vs implicit
- Xem thêm: `02_data-types/03_type-casting-and-coercion/02_explicit/` — hàm ép kiểu tường minh
- Xem thêm: `02_data-types/03_type-casting-and-coercion/03_implicit/` — quy tắc implicit coercion
- Xem thêm: `02_data-types/01_primitive-types/06_null-undefined-boolean/` — truthy/falsy 8 values
- Xem thêm: `04_equality-comparisons/` — `==` vs `===` vs `Object.is`
- Tài liệu: [MDN — Type coercion](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators), [javascript.info/type-conversions](https://javascript.info/type-conversions)
