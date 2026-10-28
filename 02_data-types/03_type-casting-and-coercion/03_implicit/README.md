# Implicit Type Coercion (Ép kiểu ngầm định) — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

**Implicit coercion** xảy ra khi **engine tự ép kiểu** mà bạn không gõ bất kỳ hàm chuyển đổi nào. Nó được kích hoạt trong bốn bối cảnh chính, và mỗi bối cảnh có **luật coercion riêng** — nắm vững luật giúp bạn **đoán chính xác kết quả** của bất kỳ biểu thức JS nào.

### 4 bối cảnh kích hoạt implicit coercion

#### 1. Toán tử cộng `+` — có string → nối, không có → số học

```js
"5" + 3;        // "53"  — có string → CONCATENATE
1 + true;       // 2     — không có string → coerce both to number (true → 1)
"a" + true;     // "atrue" — có string → concatenate
5 + " apples";  // "5 apples"
"" + 1 + 2;     // "12"   — left-to-right: ""+1="1", then "1"+2="12"
1 + 2 + "";     // "3"    — left-to-right: 1+2=3, then 3+""="3"
```

**Quy tắc:** `+` kiểm tra **operand bên trái trước** — nếu trái là string, concatenate; ngược lại, coerce cả hai sang number.

#### 2. Các toán tử số học `-`, `*`, `/`, `%` — LUÔN ép sang number

```js
"5" - 3;        // 2     — luôn coerce to number
"5" * 2;        // 10
"10" / 2;       // 5
"abc" - 1;      // NaN   — coerce failed
true - false;   // 1     — true→1, false→0
null - 0;       // 0     — null→0
undefined - 1;  // NaN   — undefined→NaN
```

#### 3. `==` (loose equality) — ép kiểu trước so sánh

```js
null == undefined;   // true  — special rule: null và undefined bằng nhau
0 == false;          // true  — false coerced to 0
"" == 0;             // true  — "" coerced to 0
"5" == 5;            // true  — "5" coerced to 5
true == 1;           // true  — true coerced to 1
null == 0;           // false — null only equals undefined
NaN == NaN;          // false — NaN NEVER equals anything, even itself
```

> ⚠️ `==` có **12 luật so sánh** trong ECMAScript spec — gần như không thể nhớ hết. Luật đơn giản nhất: **luôn dùng `===`** trừ khi chủ đích dùng `value == null` để bắt cả null và undefined.

#### 4. Ngữ cảnh điều kiện (`if`, `&&`, `||`, `!`) — quy về boolean

Mọi giá trị đều bị ** coerced thành boolean** trong các ngữ cảnh logic:

```js
if ("") { /* không chạy */ }      // "" → false (falsy)
if ("hello") { /* chạy */ }       // "hello" → true (truthy)
if (0) { /* không chạy */ }       // 0 → false
if (42) { /* chạy */ }            // 42 → true
if (null) { /* không chạy */ }    // null → false
if (undefined) { /* không chạy */ } // undefined → false
if (NaN) { /* không chạy */ }     // NaN → false
if ([]) { /* chạy */ }            // [] → true (mảng rỗng vẫn truthy!)
if ({}) { /* chạy */ }            // {} → true (object rỗng vẫn truthy!)
if (function(){}) { /* chạy */ }  // function → true
```

### Bảng truthy/falsy (thuộc lòng để đọc coercion đúng)

| Nhóm | Giá trị | Ví dụ |
|------|---------|-------|
| **Falsy (đúng 8 giá trị)** | `false`, `0`, `-0`, `0n`, `""`, `null`, `undefined`, `NaN` | `Boolean(false) === false` |
| **Truthy (mọi thứ còn lại)** | mọi số khác 0, mọi string khác rỗng, `[]`, `{}`, `function(){}`, `Symbol()`, `new Date()` | `Boolean([]) === true` |

> **Mẹo nhớ 8 falsy:** "**F**alse, **Z**ero, **N**aN, **N**ull, **U**ndefined, **E**mpty string" → acronym **"FZNNUE"** → đọc trại trong đầu.

```js
// Tự kiểm chứng
console.log(Boolean(""));       // false
console.log(Boolean("0"));      // true  ← string "0" KHÔNG rỗng!
console.log(Boolean([]));       // true  ← mảng rỗng vẫn truthy!
console.log(Boolean({}));       // true  ← object rỗng vẫn truthy!
console.log(Boolean("false"));  // true  ← string chứa ký tự là truthy
console.log(Boolean(0n));       // false
```

## 📐 Cấu trúc nhóm

```
02_data-types/03_type-casting-and-coercion/03_implicit/
├── README.md         ← bài này
└── app.js            ← demo implicit coercion
    └── index.html
```

## ✅ Điểm mạnh — Tại sao nên hiểu implicit coercion

| # | Điểm mạnh | Lý do |
|---|-----------|-------|
| 1 | **Viết ngắn gọn** | `if (username)` thay chuỗi kiểm tra dài lê thê |
| 2 | **Tận dụng truthy/falsy** | Kiểm tra nhanh "có giá trị hay không" — rất phổ biến trong codebase |
| 3 | **Coercion số học tiện** | Xử lý string-form data tiện lợi khi format known |
| 4 | **Đọc code đời thực** | Hiểu được vô số code viết theo pattern truthy/falsy |
| 5 | **Debug nhanh** | Nhận ra tại sao `if (arr)` luôn chạy với mảng rỗng |

## ⚠️ Bẫy thường gặp & Hạn chế

| # | Bẫy | Ví dụ | Cách tránh |
|---|-----|-------|-----------|
| 1 | **Kết quả dễ gây sốc** | `[] + []` → `""`, `{} + []` → `0` — hiểu rõ quy tắc coerce | Kiểm chứng trong console trước khi tin |
| 2 | **`0 == false`, `"" == 0` đều true** | Loophole trong `==` — nhiều người không đoán được | Dùng `===` trừ khi chủ đích |
| 3 | **`NaN` không bằng chính nó** | `NaN == NaN` → false — unique property | Dùng `Number.isNaN()` |
| 4 | **`if ([])` luôn chạy** | Mảng rỗng là truthy — hiểu sai `if (arr)` | Dùng `arr.length > 0` thay |
| 5 | **Coercion trong production gây bug** | "5" + 3 = "53" — unintended concat | Explicit conversion `Number("5") + 3` |

## 💡 Khi nào dùng — Tình huống thực tế

1. **Điều kiện nhanh theo độ "có dữ liệu"** — `if (data && data.length > 0)`.
2. **Default value dựa trên truthy** — `const name = user.name \|\| "Khách"`.
3. **Cố tình so sánh có chủ đích** — `== null` để bắt cả `null` lẫn `undefined` (thủ thuật hay).
4. **Logic muốn "number hoặc string đều OK"** — `if (value)` nhận cả hai.
5. **Short-circuit evaluation** — `const result = condition && expensiveFunction()` — avoid calling if condition falsy.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: `+` operator — concat vs arithmetic

```js
// Có string → concat, không có → arithmetic
console.log("5" + 3);     // "53"  — concat
console.log(5 + "3");     // "53"  — concat
console.log("5" - 3);     // 2     — arithmetic
console.log("5" * 2);     // 10    — arithmetic
console.log("5" / 1);     // 5     — arithmetic

// Left-to-right associativity matters
console.log(1 + 2 + "3"); // "33"  — (1+2)="3", then "3"+"3"="33"
console.log("1" + 2 + 3); // "123" — "1"+2="12", "12"+3="123"
console.log(true + true); // 2     — both coerced to number: 1+1=2
console.log("a" + true);  // "atrue" — string concat
```

### Ví dụ 2: `==` vs `===` — sự khác biệt lớn nhất

```js
console.log("5" == 5);    // true  — == coerces "5" → 5, then compares
console.log("5" === 5);   // false — === no coercion, different types

console.log(0 == false);  // true  — 0 coerced same as false
console.log(0 === false); // false — number vs boolean

console.log("" == 0);     // true  — "" → 0
console.log("" === 0);    // false — string vs number

console.log(null == undefined); // true  — special rule in spec
console.log(null === undefined); // false — different types

console.log(NaN == NaN);  // false — NaN never equals anything
console.log(NaN === NaN); // false
console.log(Object.is(NaN, NaN)); // true — the ONLY way to detect NaN equality
```

### Ví dụ 3: Truthy/Falsy trong thực tế

```js
// Falsy values (8 total)
const falsyValues = [false, 0, -0, 0n, "", null, undefined, NaN];
for (const v of falsyValues) {
  console.log(`${String(v).padEnd(12)} → Boolean: ${Boolean(v)}`);
}
// false          → Boolean: false
// 0              → Boolean: false
// -0             → Boolean: false
// 0n             → Boolean: false
// ""             → Boolean: false
// null           → Boolean: false
// undefined      → Boolean: false
// NaN            → Boolean: false

// Truthy values — counter-intuitive ones
console.log(Boolean([]));     // true  — empty array is TRUTHY!
console.log(Boolean({}));     // true  — empty object is TRUTHY!
console.log(Boolean("0"));    // true  — string "0" is TRUTHY (not empty)!
console.log(Boolean(" "));    // true  — space string is TRUTHY
console.log(Boolean(function() {})); // true
```

### Ví dụ 4: Bẫy kinh điển — kết quả không đoán trước

```js
// These are famous coercion surprises:
console.log([] + []);         // ""     — both [] → "" (toString), then "" + "" = ""
console.log({} + []);         // 0      — {} parsed as empty block, [] → 0
console.log([] + {});         // "[object Object]" — [] → "", {} → "[object Object]"
console.log({} + {});         // "[object Object]" — {} block + {} → "[object Object]"
console.log("9" > "10");      // true   — string comparison: '9' > '1' (first char)
console.log([1] == "1");      // true   — [1] → "1", then "1" == "1"
console.log([1] === "1");     // false  — array vs string, different types
console.log(![]);             // true   — [] is truthy, ![] → false
console.log(!![]);            // true   — double negation restores truthiness
```

### Ví dụ 5: Ứng dụng thực tế — default value pattern

```js
// Pattern 1: || — thay thế MỌI falsy value
const name1 = "" || "Khách";           // "Khách"
const name2 = 0 || 42;                 // 42 — 0 là falsy!
const name3 = false || true;           // true
const name4 = null || "default";       // "default"

// Pattern 2: ?? — chỉ thay thế NULLISH (null/undefined) — GIỮ 0, "", false
const num1 = 0 ?? 10;                  // 0 — 0 được giữ (không phải nullish)
const str1 = "" ?? "default";          // "" — empty string được giữ
const bool1 = false ?? true;           // false — false được giữ
const val1 = null ?? "default";        // "default" — null replaced
const val2 = undefined ?? "default";   // "default" — undefined replaced

// Khi nào dùng cái nào?
// || khi muốn default cho MỌI falsy (aggressive)
// ?? khi muốn default CHỈ cho null/undefined (conservative, safer)
```

### Ví dụ 6: Coercion trong điều kiện — pattern phổ biến

```js
const user = { name: "Sơn", scores: [] };

// B1: Kiểm tra user tồn tại (không nullish)
if (user) {                    // true — object là truthy
  console.log("User exists");
}

// B2: Kiểm tra scores có phần tử (KHÔNG dùng if (user.scores))
// ❌ if (user.scores) → [] vẫn truthy!
if (user.scores && user.scores.length > 0) {
  console.log("Has scores");
} else {
  console.log("No scores — [] is truthy but empty!");
}

// B3: Kiểm tra username (tránh "0" being falsy by mistake)
const displayName = user.name || "Anonymous";
console.log(displayName);      // "Sơn"

// B4: Kiểm tra có ID hay không (dùng ??)
const userId = user.id ?? "guest"; // giữ 0, false, "" — chỉ thay nullish
```

## 🔬 So sánh với alternatives

| Phương án | Ưu điểm | Nhược điểm |
|-----------|---------|------------|
| **Implicit coercion** | Code ngắn, tự nhiên | Dễ gây bug, khó đọc, khó debug |
| **Explicit conversion** | Dự đoán được, self-documenting | Verbose hơn |
| **TypeScript strict mode** | Compile-time, no runtime surprise | Build step, config |
| **Runtime type guards** | Precise control | Boilerplate code |

## 📊 Performance & Best Practices

- **Production: dùng `===` thay `==`** — trừ khi chủ đích dùng `value == null` để bắt cả null và undefined.
- **Dùng `??` thay `||` khi muốn default chỉ cho nullish** — giữ giá trị 0, "", false hợp lệ.
- **Kiểm tra `if (arr.length > 0)` thay `if (arr)`** — tránh bẫy mảng rỗng là truthy.
- **Kiểm tra `if (obj.key !== undefined && obj.key !== null)`** thay `if (obj.key)` — tránh 0, "", false bị typefalsy.
- **Debug coercion issue** — mở DevTools Console, chạy từng expression, đọc kết quả thực tế.
- **Tránh relies vào coercion trong logic quan trọng** — dùng explicit chuyển đổi để rõ intent.
- **ESLint `eqeqeq`** — enforce `===` instead of `==`.
- **ESLint `no-coercion`** (cần plugin) — warn khi implicit coercion detected.

## 🔗 Liên kết chéo

- Xem thêm: `02_data-types/03_type-casting-and-coercion/01_conversion-vs-coercion/` — phân biệt explicit vs implicit
- Xem thêm: `02_data-types/03_type-casting-and-coercion/02_explicit/` — explicit conversion functions
- Xem thêm: `02_data-types/01_primitive-types/06_null-undefined-boolean/` — truthy/falsy 8 values
- Xem thêm: `04_equality-comparisons/` — `==` vs `===` vs `Object.is`
- Tài liệu: [MDN — Type coercion](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators), [javascript.info/type-conversions](https://javascript.info/type-conversions), [Dmitry Soshnikov — ECMAScript Coercion](http://dmitrysoshnikov.com/ecmascript/chapter-2/abstract-operations/)
