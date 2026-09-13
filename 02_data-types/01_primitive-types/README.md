# Primitive Types (Kiểu nguyên thủy) — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

**Primitive (nguyên thủy)** là giá trị **không phải object** và **không có phương thức** riêng — chúng là "nguyên tử" dữ liệu của JavaScript. Có **7 kiểu nguyên thủy** được định nghĩa trong ECMAScript spec:

1. **`string`** — chuỗi ký tự: `"Sơn"`, `'a'`, `` `template ${x}` ``.
2. **`number`** — số dấu phẩy động IEEE-754: `42`, `3.14`, các giá trị đặc biệt `NaN`, `Infinity`, `-Infinity`.
3. **`bigint`** — số nguyên lớn không giới hạn: `9007199254740993n`.
4. **`boolean`** — `true` / `false`.
5. **`undefined`** — *chưa được gán giá trị* (engine tự đặt khi khai báo biến không gán, hoặc hàm không return).
6. **`symbol`** — giá trị duy nhất, bất biến, dùng làm khóa object — xem `05_symbol/`.
7. **`null`** — *cố ý rỗng* (lập trình viên đặt). Lưu ý: `typeof null` trả `"object"` — **bug lịch sử** không sửa được vì sẽ phá hàng tỉ trang web.

### Bản chất của primitive — 4 đặc tính quan trọng

| Đặc tính | Mô tả | Ví dụ |
|----------|-------|-------|
| **So sánh theo giá trị** | `===` so sánh nội dung, không phải tham chiếu | `"a" === "a"` → `true`, `1 === 1` → `true` |
| **Tại một thời điểm chỉ chứa một giá trị** | Không có "phương thức" đi kèm | `5.toFixed(2)` là syntax error (cần `(5).toFixed(2)`) |
| **Bất biến (immutable)** | Không "sửa" được; mọi thao tác tạo giá trị mới | `"abc".toUpperCase()` → `"ABC"`, chuỗi gốc không đổi |
| **Gán theo value copy** | `let b = a` sao chép giá trị vào ô nhớ mới | `a = 2; b vẫn là 1` |

### Boxing — tại sao primitive lại "có" phương thức?

Khi bạn gọi `"abc".toUpperCase()`, engine thực hiện cơ chế **auto-boxing**:

1. Tạo một **wrapper object** tạm thời: `new String("abc")`.
2. Gọi phương thức trên wrapper: `"abc".toUpperCase()`.
3. Vứt bỏ wrapper object — GC thu hồi.

```js
// Về mặt ngôn ngữ, đây là:
let temp = new String("abc");
temp.toUpperCase();     // "ABC"
// temp bị discard

// Bạn KHÔNG nên dùng new String() — tạo object wrapper rõ ràng:
typeof new String("abc"); // "object" ❌
typeof "abc";              // "string" ✅
```

### Primitive vs Reference — bảng so sánh nền tảng

| Đặc điểm | Primitive (7 kiểu) | Reference (object, array, function) |
|----------|-------------------|-------------------------------------|
| **Gán** | Copy giá trị | Copy tham chiếu (address) |
| **So sánh** | So sánh nội dung (`===`) | So sánh tham chiếu (cùng object?) |
| **Mutable** | Bất biến | Thay đổi được |
| **Memory** | Stack (trực tiếp) | Heap (tham chiếu qua stack pointer) |
| **Example** | `let a = 1; let b = a;` | `let a = {x:1}; let b = a;` |

## 📐 Cấu trúc nhóm

```
02_data-types/01_primitive-types/
├── README.md                 ← bài tổng quan này
├── 01_string/                ← string type details
├── 02_number/                ← number type details
├── 03_value-vs-reference/    ← value vs reference comparison
├── 04_bigint/                ← bigint type details
├── 05_symbol/                ← symbol type details
└── 06_null-undefined-boolean/← null, undefined, boolean details
```

## ✅ Điểm mạnh — Tại sao primitive quan trọng

| # | Điểm mạnh | Lý do |
|---|-----------|-------|
| 1 | **Nhỏ gọn, di chuyển nhanh** | Copy theo value, không dính dáng tham chiếu — predictable behavior |
| 2 | **So sánh trực quan và chính xác** | `1 === 1`, `"a" === "a"` — dễ đoán kết quả |
| 3 | **Bất biến → an toàn** | Truyền vào hàm, hàm sửa đổi cũng không phá giá trị gốc |
| 4 | **Đủ 7 kiểu cho nhu cầu cơ bản** | Chữ, số, đúng/sai, rỗng, khóa duy nhất — cover mọi use case |
| 5 | **Boxing tự động** | Vẫn có đủ helper methods tiện lợi dù là primitive |
| 6 | **Performance cao** | Primitive lưu trên stack, truy cập nhanh hơn heap object |

## ⚠️ Bẫy thường gặp & Hạn chế

| # | Bẫy | Ví dụ | Cách tránh |
|---|-----|-------|-----------|
| 1 | **`typeof null === "object"`** | Bug lịch sử từ ES1 | Dùng `value === null` thay `typeof` |
| 2 | **`number` IEEE-754 sai số** | `0.1 + 0.2 !== 0.3` | So sánh với epsilon: `Math.abs(a-b) < Number.EPSILON` |
| 3 | **`typeof` không phân biệt array/object** | `typeof [] === "object"`, `typeof {} === "object"` | Dùng `Array.isArray(arr)` |
| 4 | **`new String/Number/Boolean` tạo object** | `typeof new String("x")` → `"object"` | Dùng hàm chuyển đổi `String(x)` thay `new String(x)` |
| 5 | **Primitive bất biến — hiểu nhầm mutable** | `let s = "hello"; s[0] = "H"; console.log(s)` → `"hello"` (không đổi) | Hiểu rằng string là immutable, mọi method trả về string mới |
| 6 | **`(5).toFixed(2)` cần parentheses** | `5.toFixed(2)` → SyntaxError | `(5).toFixed(2)` hoặc `Number(5).toFixed(2)` |

## 💡 Khi nào dùng — Tình huống thực tế

1. **Mọi dữ liệu đơn giản**: tên, số tuổi, cờ đúng/sai → `string` / `number` / `boolean`.
2. **Số vượt `Number.MAX_SAFE_INTEGER`** (ID, hash, timestamp nano) → `bigint`.
3. **Cần giá trị duy nhất làm khóa** → `symbol` — tránh collision với key string.
4. **Biểu đạt "chưa có"** → `undefined` (engine tự đặt), `null` (lập trình viên đặt có chủ đích).
5. **Tạo constant configuration** → `const` + primitive value — immutable reference.
6. **Key trong Map/Set** → `symbol` đảm bảo uniqueness, không bị override.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: 7 primitive types — typeof check

```js
console.log(typeof "hello");        // "string"
console.log(typeof 42);             // "number"
console.log(typeof 10n);            // "bigint"
console.log(typeof true);           // "boolean"
console.log(typeof undefined);      // "undefined"
console.log(typeof null);           // "object" ← BUG LỊCH SỬ
console.log(typeof Symbol("id"));   // "symbol"
```

### Ví dụ 2: Value copy — primitive assignment

```js
let a = 1;
let b = a;       // sao chép GIÁ TRỊ (1) vào ô nhớ mới
a = 2;           // đổi a, b vẫn nguyên
console.log(b);  // 1 — b không hề thay đổi

// So sánh với object (reference copy):
let objA = { x: 1 };
let objB = objA;      // copy THAM CHIẾU (cùng object trong heap)
objA.x = 99;
console.log(objB.x);  // 99 — objB cũng đổi theo!
```

### Ví dụ 3: Primitive so sánh theo giá trị

```js
console.log(1 === 1);              // true — same value
console.log("x" === "x");          // true — same string content
console.log(true === true);        // true
console.log(null === null);        // true
console.log(undefined === undefined); // true

// Object so sánh theo tham chiếu
console.log({} === {});            // false — 2 objects khác nhau
console.log([] === []);            // false — 2 arrays khác nhau
```

### Ví dụ 4: Boxing — primitive "có" phương thức

```js
// String boxing: engine tạm tạo String object, gọi method, discard
console.log("son".toUpperCase());  // "SON" — primitive string có method
console.log(("son").length);       // 3

// Number boxing
console.log((42.7).toFixed(1));    // "42.7" — primitive number có method

// Boolean boxing
console.log(true.toString());      // "true" — primitive boolean có method

// ⚠️ Nhưng KHÔNG dùng new String/Number/Boolean
console.log(typeof new String("x")); // "object" ❌
console.log(typeof String("x"));     // "string" ✅
```

### Ví dụ 5: Null vs Undefined — hai trạng thái "không có"

```js
let unassigned;           // undefined — engine tự đặt
console.log(unassigned);  // undefined
console.log(typeof unassigned); // "undefined"

let intentionallyEmpty = null;  // null — lập trình viên đặt có chủ đích
console.log(intentionallyEmpty); // null
console.log(typeof intentionallyEmpty); // "object" (bug lịch sử)

// So sánh
console.log(null == undefined);    // true  (loose equality: cùng "không có giá trị")
console.log(null === undefined);   // false (strict: khác kiểu)
```

## 🔬 So sánh với alternatives

| Phương án | Ưu điểm | Nhược điểm |
|-----------|---------|------------|
| **Primitive types (native)** | Performance cao, memory nhỏ, built-in | Immutable — không mutate được trực tiếp |
| **Wrapper objects** (`new String`) | Có thể thêm property | typeof = "object", memory overhead, anti-pattern |
| **TypeScript primitive types** | Type safety compile-time | Cần transpile, thêm config |
| **Rust primitives** | Memory safe, zero-cost abstractions | Learning curve cao, syntax khác |
| **Python primitives** | Dynamic typing tương tự | Different semantics (all objects in Python) |

## 📊 Performance & Best Practices

- **Ưu tiên primitive** cho dữ liệu đơn giản — performance cao hơn, memory nhỏ hơn object wrapper.
- **Tránh `new String/Number/Boolean`** — tạo object overhead, typeof sai, confusion.
- **Dùng `const` + primitive** cho constants — immutable reference + compiler hint.
- **Hiểu boxing behavior** — `"abc".length` hoạt động vì auto-boxing, nhưng không nên dựa vào việc thêm property cho primitive.
- **So sánh primitive với `===`** — chính xác, không có coercion surprise.
- **Dùng `typeof` + check null separately** — `typeof x === "string" && x !== null` pattern cho validation.
- **BigInt cho cryptographic/ID** — khi số vượt `Number.MAX_SAFE_INTEGER`, dùng `bigint` thay vì `number` để tránh precision loss.

## 🔗 Liên kết chéo

- Xem thêm: `02_data-types/01_primitive-types/01_string/` — string operations chi tiết
- Xem thêm: `02_data-types/01_primitive-types/02_number/` — number, NaN, Infinity
- Xem thêm: `02_data-types/01_primitive-types/03_value-vs-reference/` — value vs reference deep dive
- Xem thêm: `02_data-types/01_primitive-types/04_bigint/` — bigint large integers
- Xem thêm: `02_data-types/01_primitive-types/05_symbol/` — symbol unique keys
- Xem thêm: `02_data-types/01_primitive-types/06_null-undefined-boolean/` — null, undefined, boolean
- Xem thêm: `02_data-types/03_type-casting-and-coercion/` — ép kiểu primitive
- Tài liệu: [MDN — Primitive](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Primitive_values), [javascript.info/primitives](https://javascript.info/primitives)
