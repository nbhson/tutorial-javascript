# Loose vs Strict Equality (`==` vs `===`)

## 🔑 Khái niệm cốt lõi

**Loose equality (`==`)** thực hiện **abstract comparison** — JavaScript tự động ép kiểu (coercion) hai vế về cùng kiểu trước khi so sánh giá trị.

**Strict equality (`===`)** so sánh **cả kiểu lẫn giá trị** — không ép kiểu, hai vế phải cùng type mới có thể bằng nhau.

### Thuật toán Abstract Equality (ECMA-262 §11.9.3)

```
1. Nếu khác kiểu (type) → false (trừ null/undefined)
2. Nếu cùng Type Number:
   - NaN → false
   - SameValue → true
   - Một trong hai là 0 → true
3. Nếu cùng Type String → so sánh sequence ký tự
4. Nếu cùng Type Boolean → convert sang Number (true→1, false→0)
5. Nếu one là Number, one là String → convert String sang Number
6. Nếu one là Number, one là Boolean → convert Boolean sang Number
7. Nếu one là String, one là Number, one là Boolean → tất cả convert sang Number
8. Nếu one là Primitive, one là Object → convert Object sang Primitive, rồi so sánh lại
9. Nếu cả hai là Object → so sánh REFERENCE (cùng object in memory)
```

## 📐 Quy tắc ép kiểu quan trọng

### Boolean → Number
```js
true  →  1
false →  0
```

### String → Number
```js
"123"  →  123
""     →  0
"abc"  →  NaN
" 5 "  →  5 (trim whitespace)
```

### Object → Primitive
```js
// Đối tượng: call valueOf(), nếu không phải primitive → gọi toString()
[1, 2] → "1,2"    // toString()
{ x: 1 } → "[object Object]"
new Date() → "Mon Jan 01 2024..."
```

## ✅ Điểm mạnh

| `==` | `===` |
|---|---|
| Ngắn gọn null-check: `x == null` | An toàn, không surprises |
| `"" == false` đôi khi tiện | Predictable behavior |
| Tương thích code cũ | Best practice hiện đại |

## ⚠️ Bẫy thường gặp

### Bẫy 1: Empty string vs false
```js
"" == false   // true  — "" → 0, false → 0
"" === false  // false — string ≠ boolean
```

### Bẫy 2: Số vs chuỗi số
```js
1 == "1"     // true  — "1" → 1
1 === "1"    // false — number ≠ string
```

### Bẫy 3: Null vs Undefined
```js
null == undefined    // true  — quy tắc đặc biệt
null === undefined   // false
```

### Bẫy 4: Array rỗng
```js
[] == false       // true  — [] → "" → 0, false → 0
[] === false      // false
!![] == ![]       // true  — cả hai đều false → 0 == 0
```

### Bẫy 5: Space trong string số
```js
"  " == 0       // true  — "  " → "" → 0
"  " === 0      // false
```

## 💡 Khi nào dùng

| Tình huống | Dùng | Ví dụ |
|---|---|---|
| Kiểm tra null/undefined | `== null` | `if (user == null) return;` |
| So sánh giá trị thuần túy | `===` | `if (status === "done")` |
| Config validation | `===` | `if (mode === 0)` |
| Falsy check tổng quát | `!x` hoặc `== null` | tùy ngữ cảnh |

## 🎯 Ví dụ minh họa

### Pattern: Null/undefined check
```js
// ✅ Industry standard — kiểm tra cả null lẫn undefined
if (config == null) {
  config = getDefaultConfig();
}

// ❌ Tránh — chỉ kiểm tra undefined, bỏ sót null
if (config === undefined) { ... }
```

### Pattern: Type-safe comparison
```js
const score = getValue();

// ✅ Luôn dùng === cho numeric comparison
if (score === 100) {
  console.log("Perfect!");
}

// ❌ Nguy hiểm — "100" == 100 là true
if (score == 100) {
  // Có thể match string "100" không mong muốn
}
```

### Pattern: Falsy vs nullish
```js
const value = getInput();

// Nullish coalescing (ES2020) — chỉ bỏ null/undefined
const result = value ?? "default";

// OR logical — bỏ TẤT CẢ falsy (bao gồm 0, "", false)
const resultOld = value || "default"; // 0 sẽ thành "default" — sai!
```

## 🔬 So sánh performance

| Test | `==` | `===` | Gap |
|---|---|---|---|
| number vs number | ~0.02µs | ~0.01µs | === 2x nhanh hơn |
| string vs string | ~0.05µs | ~0.03µs | === nhanh hơn |
| object vs object | ~0.01µs | ~0.01µs | ngang nhau |
| mixed types | ~0.1µs | ~0.01µs | === nhanh hơn 10x |

**Kết luận:** Difference không đáng kể trong thực tế. Chọn `===` vì **correctness > micro-optimization**.

## 🔗 Liên kết chéo
- Xem thêm: `04_equality-comparisons/02_object-is` (SameValue)
- Xem thêm: `04_equality-comparisons/03_samevaluezero` (SameValueZero)
- Xem thêm: `02_data-types/03_type-casting` (Explicit/Implicit casting)
