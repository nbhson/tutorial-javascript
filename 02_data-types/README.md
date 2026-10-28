# 02. Kiểu dữ liệu (Data Types) — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

Mọi giá trị trong JavaScript đều thuộc một trong **8 kiểu dữ liệu** (7 primitive + 1 reference type group). Chúng được chia làm hai nhóm lớn:

### Kiểu nguyên thủy (Primitive types) — 7 kiểu

| Kiểu | Cú pháp | Ví dụ | Ghi chú |
|------|---------|-------|---------|
| **`string`** | `"text"`, `'text'`, `` `template` `` | `"Xin chào"`, `` `Hi ${name}` `` | Chuỗi ký tự bất biến |
| **`number`** | `42`, `3.14`, `NaN`, `Infinity` | `3.14159`, `-0`, `1e10` | IEEE-754 double precision |
| **`bigint`** | `9007199254740993n` | `123n`, `BigInt("999")` | Số nguyên không giới hạn |
| **`boolean`** | `true`, `false` | `true`, `false` | Đúng/sai |
| **`undefined`** | `let x;` | `x === undefined` | Engine tự đặt khi chưa gán |
| **`null`** | `null` | `user = null` | Lập trình viên đặt "rỗng có chủ đích" |
| **`symbol`** | `Symbol("desc")` | `Symbol.iterator` | Giá trị duy nhất, dùng làm key |

### Kiểu tham chiếu (Reference types) — object và các biến thể

- **`object`** — tập hợp key-value: `{ name: "Sơn", age: 23 }`
- **`array`** — object đặc biệt với index numeric: `[1, "a", true]` → `typeof [] === "object"`
- **`function`** — object đặc biệt có thể gọi: `function() {}` → `typeof fn === "function"`
- **Built-in objects**: `Date`, `RegExp`, `Map`, `Set`, `Promise`, `Error`...

### Hai quy luật nền tảng

1. **Primitive so sánh và được gán theo giá trị (value)**. Object so sánh và được gán theo **tham chiếu (reference)**. Xem chi tiết: `02_data-types/01_primitive-types/03_value-vs-reference/`.
2. **JavaScript có khả năng ép kiểu (coercion)** — tự chuyển đổi kiểu khi cần: `"1" + 1` → `"11"`, `"5" - 3` → `2`. Học kỹ ở: `02_data-types/03_type-casting-and-coercion/`.

### `typeof` operator — công cụ kiểm tra kiểu cơ bản

```js
console.log(typeof "text");     // "string"
console.log(typeof 42);         // "number"
console.log(typeof 10n);        // "bigint"
console.log(typeof true);       // "boolean"
console.log(typeof undefined);  // "undefined"
console.log(typeof null);       // "object"  ← BUG LỊCH SỬ!
console.log(typeof Symbol());   // "symbol"
console.log(typeof {});         // "object"
console.log(typeof []);         // "object"  (array vẫn là object)
console.log(typeof function(){}); // "function"
```

> **Lưu ý:** `typeof null === "object"` là bug lịch sử từ ES1. Nếu muốn kiểm tra null chính xác, dùng `value === null` thay vì `typeof`.

## 📐 Cấu trúc nhóm

```
02_data-types/
├── README.md                     ← bài tổng quan này
├── 01_primitive-types/
│   ├── README.md                 ← tổng quan 7 primitive
│   ├── 01_string/                ← string operations
│   ├── 02_number/                ← number, NaN, Infinity
│   ├── 03_value-vs-reference/    ← value vs reference assignment
│   ├── 04_bigint/                ← bigint large numbers
│   ├── 05_symbol/                ← symbol unique keys
│   └── 06_null-undefined-boolean/← null, undefined, boolean, truthy/falsy
├── 02_objects-and-prototype/
│   ├── README.md
│   ├── 01_object-basics/         ← object literal, constructor, prototype
│   ├── 02_functions-as-objects/  ← hàm cũng là object
│   └── 03_shallow-deep-clone/    ← copy object đúng cách
├── 03_type-casting-and-coercion/
│   ├── README.md
│   ├── 01_conversion-vs-coercion/← phân biệt conversion vs coercion
│   ├── 02_explicit/              ← ép kiểu tường minh
│   └── 03_implicit/              ← ép kiểu ngầm định
└── 04_builtin-objects/
    ├── README.md
    ├── 01_math/                  ← Math API
    ├── 02_date/                  ← Date API
    ├── 03_regexp/                ← RegExp API
    └── 04_error/                 ← Error API
```

## ✅ Điểm mạnh — Tại sao nên học kỹ

| # | Lợi ích | Lý do |
|---|---------|-------|
| 1 | **Nắm 7 primitive + object** | Đọc `typeof` đúng, hiểu mọi giá trị trong JS |
| 2 | **Hiểu tham trị/tham chiếu** | Tránh vô số bug clone/sửa dữ liệu — nguyên nhân số 1 của state bug |
| 3 | **Hiểu ép kiểu** | Đoán chính xác kết quả của `"5" + 3`, `1 == "1"`, `[] + []` |
| 4 | **Biết built-in objects** | Viết code ngắn, đúng chuẩn — không tự viết hàm thay cho `Math`, `Date`, `RegExp` |
| 5 | **Nền tảng vững cho topic nâng cao** | Asynchronous, class, module đều dựa trên hiểu biết data types |
| 6 | **Debug lỗi type-related** | `TypeError: Cannot read properties of undefined` — hiểu nguyên nhân từ data type |
| 7 | **Viết type-safe code (dù dynamic)** | `typeof`, `instanceof`, `Array.isArray` giúp validate trước khi xử lý |

## ⚠️ Bẫy thường gặp & Hạn chế

| # | Bẫy | Ví dụ | Cách tránh |
|---|-----|-------|-----------|
| 1 | **`typeof null === "object"`** | Bug lịch sử không sửa được | Dùng `=== null` thay vì `typeof` để kiểm tra null |
| 2 | **`number` không chính xác tuyệt đối** | `0.1 + 0.2 !== 0.3` — IEEE-754 floating point | So sánh với epsilon: `Math.abs(a - b) < Number.EPSILON` |
| 3 | **Object so sánh theo tham chiếu** | `{} === {}` → `false` (2 object khác nhau) | Dùng `JSON.stringify` hoặc deep equal library |
| 4 | **`typeof [] === "object"`** | Array là object đặc biệt, không phải type riêng | Dùng `Array.isArray(arr)` để kiểm tra |
| 5 | **Ép kiểu ngầm định gây bug** | `"9" > "10"` → `true` (so sánh chuỗi ký tự đầu) | Dùng `===` thay `==`, ép kiểu tường minh `Number()` |
| 6 | **`new String()` tạo object, không primitive** | `typeof new String("x")` → `"object"` | Dùng `String(x)` thay `new String(x)` |
| 7 | **`NaN !== NaN`** | NaN không bằng chính nó | Dùng `Number.isNaN(value)` thay `value === NaN` |

## 💡 Khi nào dùng — Tình huống thực tế

1. **Kiểm tra kiểu dữ liệu của biến** → `typeof` / `Array.isArray()` / `instanceof Constructor`.
2. **Tính toán số an toàn** → `number`; số cực lớn (ID, timestamp nano) → `bigint`.
3. **Khóa duy nhất/hidden trong object** → `symbol` — tránh collision với key string.
4. **Biểu diễn "chưa có gì"** → `undefined` (engine tự đặt), `null` (lập trình viên đặt có chủ đích).
5. **Thao tác thời gian** → `Date` built-in object, `toISOString()`, `getTime()`.
6. **Validate format** → `RegExp.test()` cho email, phone, zip code.
7. **Xử lý lỗi runtime** → `try/catch` + `Error` subclasses (`TypeError`, `ReferenceError`...).

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: 8 kiểu dữ liệu với typeof

```js
// Primitive types
console.log(typeof "text");        // "string"
console.log(typeof 42);            // "number"
console.log(typeof 10n);           // "bigint"
console.log(typeof true);          // "boolean"
console.log(typeof undefined);     // "undefined"
console.log(typeof null);          // "object" ← BUG LỊCH SỬ
console.log(typeof Symbol());      // "symbol"

// Reference types
console.log(typeof {});            // "object"
console.log(typeof []);            // "object" (array vẫn là object)
console.log(typeof function(){});  // "function"
```

### Ví dụ 2: Value vs Reference — sự khác biệt quan trọng nhất

```js
// Primitive — copy by value
let a = 1;
let b = a;        // sao chép GIÁ TRỊ
a = 2;
console.log(b);   // 1 — b không hề thay đổi

// Object — copy by reference
let obj1 = { x: 1 };
let obj2 = obj1;  // cả hai trỏ CÙNG MỘT object
obj1.x = 99;
console.log(obj2.x);  // 99 — obj2 cũng đổi theo!
```

### Ví dụ 3: Ép kiểu ngầm định (coercion)

```js
console.log("5" + 3);       // "53"  — string wins, concat
console.log("5" - 3);       // 2     — arithmetic, coerce to number
console.log(null + 1);      // 1     — null → 0
console.log(undefined + 1); // NaN   — undefined → NaN
console.log(true + 1);      // 2     — true → 1
console.log(false - 1);     // -1    — false → 0
```

### Ví dụ 4: Truthy/Falsy — 8 giá trị falsy

```js
// 8 falsy values (đúng 8, không phải 7!)
console.log(Boolean(false));       // false
console.log(Boolean(0));           // false
console.log(Boolean(-0));          // false
console.log(Boolean(0n));          // false
console.log(Boolean(""));          // false
console.log(Boolean(null));        // false
console.log(Boolean(undefined));   // false
console.log(Boolean(NaN));         // false

// Mọi thứ khác là truthy
console.log(Boolean(1));           // true
console.log(Boolean("0"));         // true — chuỗi "0" KHÔNG rỗng!
console.log(Boolean([]));          // true — mảng rỗng vẫn truthy!
console.log(Boolean({}));          // true — object rỗng vẫn truthy!
```

### Ví dụ 5: Kiểm tra kiểu an toàn

```js
function checkType(val) {
  if (val === null) return "null";
  if (Array.isArray(val)) return "array";
  if (typeof val === "bigint") return "bigint";
  if (typeof val === "symbol") return "symbol";
  return typeof val;
}

console.log(checkType(null));       // "null"
console.log(checkType([1, 2]));     // "array"
console.log(checkType(10n));        // "bigint"
console.log(checkType(Symbol()));   // "symbol"
console.log(checkType("hi"));       // "string"
```

## 🔬 So sánh với alternatives

| Phương án | Ưu điểm | Nhược điểm |
|-----------|---------|------------|
| **`typeof`** | Nhanh, đơn giản, built-in | `typeof null === "object"`, không phân biệt object/array/function chi tiết |
| **`instanceof`** | Kiểm tra prototype chain | Không hoạt động qua iframe, chỉ kiểm tra constructor |
| **`Array.isArray()`** | Chính xác cho array | Chỉ check array, không dùng cho object general |
| **`Object.prototype.toString.call()`** | Chính xác nhất (`[object Array]`, `[object Date]`) |Verbose, ít dùng trong code hiện đại |
| **TypeScript `typeof`/`is`** | Compile-time type checking | Cần transpile, thêm complexity |

## 📊 Performance & Best Practices

- **Dùng `Array.isArray()`** thay `typeof arr === "object"` để kiểm tra array — chính xác hơn.
- **Dùng `=== null`** thay `typeof x === "object"` để kiểm tra null — tránh bug `typeof null`.
- **Dùng `Number.isNaN()`** thay `isNaN()` — `isNaN("abc")` là `true` (ép kiểu), `Number.isNaN("abc")` là `false`.
- **Ưu tiên ép kiểu tường minh** (`Number()`, `String()`, `Boolean()`) thay vì relies coercion ngầm.
- **Dùng `Object.freeze()`** cho constant objects — shallow immutable, ngăn mutate ngoài ý muốn.
- **Avoid `new String/Number/Boolean`** — tạo object wrapper, `typeof` sẽ là `"object"`.
- **So sánh số thực với epsilon** — `Math.abs(a - b) < Number.EPSILON` thay vì `a === b`.

## 🔗 Liên kết chéo

- Xem thêm: `02_data-types/01_primitive-types/` — 7 primitive types chi tiết
- Xem thêm: `02_data-types/01_primitive-types/01_string/` — string operations
- Xem thêm: `02_data-types/01_primitive-types/02_number/` — number, NaN, Infinity
- Xem thêm: `02_data-types/01_primitive-types/03_value-vs-reference/` — value vs reference
- Xem thêm: `02_data-types/01_primitive-types/04_bigint/` — bigint large integers
- Xem thêm: `02_data-types/01_primitive-types/05_symbol/` — symbol unique keys
- Xem thêm: `02_data-types/01_primitive-types/06_null-undefined-boolean/` — null, undefined, boolean
- Xem thêm: `02_data-types/02_objects-and-prototype/` — object basics, prototype
- Xem thêm: `02_data-types/03_type-casting-and-coercion/` — ép kiểu tường minh/ngầm
- Xem thêm: `04_equality-comparisons/` — `==` vs `===` vs `Object.is`
- Tài liệu: [MDN — Data types](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures), [javascript.info/types](https://javascript.info/types)

## 🆕 ES2025 & Iterables hiện đại

Một số tính năng mới liên quan đến kiểu dữ liệu / built-in objects (tổng hợp chi tiết: `22_es2025-features/README.md`):

### Iterator Helpers — ES2025 (Chrome 122+, Firefox 131+, Safari 18.4+)

Method functional **lazy** trực tiếp trên `Iterator.prototype` — chi tiết đầy đủ ở `15_iterators-and-generators/`.

```js
// Chuỗi vô hạn vẫn an toàn nhờ lazy evaluation
function* naturalNumbers() { let n = 0; while (true) yield n; }

const result = naturalNumbers()
  .filter(n => n % 2 === 0)
  .map(n => n * n)
  .take(5)
  .toArray();
console.log(result); // [0, 4, 16, 36, 64]
```

> 📖 MDN: [Iterator](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Iterator)

### Set Methods — phép toán tập hợp (Chrome 122+, Firefox 127+, Safari 17+)

```js
const a = new Set([1, 2, 3]);
const b = new Set([3, 4, 5]);

a.union(b);            // Set {1, 2, 3, 4, 5}
a.intersection(b);      // Set {3}
a.difference(b);        // Set {1, 2}
a.symmetricDifference(b); // Set {1, 2, 4, 5}
a.isSubsetOf(b);        // false
a.isSupersetOf(b);      // false
a.isDisjointFrom(b);    // false
```

> 📖 MDN: [Set](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set)

### RegExp.escape() (Chrome 123+, Firefox 127+)

Escape chuỗi an toàn trước khi nhúng vào `new RegExp()` — chi tiết ở `02_data-types/04_builtin-objects/03_regexp/`.

```js
const userInput = "C++ (2025)";
const re = new RegExp(RegExp.escape(userInput)); // escape toàn bộ syntax chars
console.log(re.test("C++ (2026)")); // false — match literal chính xác
```
