# Object.is() — SameValue Algorithm

## 🔑 Khái niệm cốt lõi

`Object.is(a, b)` (ES2015/ES6) thực hiện **SameValue** algorithm — giống `===` nhưng sửa 2 lỗi thiết kế:

1. **NaN** được coi là bằng chính nó (`NaN === NaN` → `false`, `Object.is(NaN, NaN)` → `true`)
2. **`-0` và `+0`** được phân biệt (`-0 === +0` → `true`, `Object.is(-0, +0)` → `false`)

### Thuật toán SameValue (ECMA-262 §7.2.13)

```
1. Nếu a是同 Type:
   a. Number:
      - both NaN → true
      - both +0 hoặc both -0 → true
      - same value → true
      - otherwise → false
   b. Khác Number cùng Type → same as ===
2. Nếu不同类型 → false
```

## 📐 Khác biệt `===` vs `Object.is`

| Trường hợp | `===` | `Object.is` | Ghi chú |
|---|---|---|---|
| `NaN === NaN` | false | **true** | Cùng giá trị special |
| `-0 === +0` | true | **false** | Khác dấu |
| `5 === 5` | true | true | Bình thường |
| `"a" === "a"` | true | true | Bình thường |
| `null === null` | true | true | Bình thường |
| `undefined === undefined` | true | true | Bình thường |
| `{} === {}` | false | false | Khác reference |

## ✅ Điểm mạnh

| Ưu điểm | Ứng dụng |
|---|---|
| Correct NaN comparison | Map key, Set member, algolia search |
| Distinguish ±0 | Financial calculations, physics simulations |
| No type coercion | Safer than `==`, clearer intent than `===` |
| Pure function | Không side effect, pure comparison |

## ⚠️ Bẫy thường gặp

### Bẫy 1: Hiệu năng
```js
// Object.is chậm hơn === ~2x do function call overhead
for (let i = 0; i < 1_000_000; i++) {
  Object.is(a, b); // ~2x slower than a === b
}
// Chỉ dùng khi cần SameValue semantics, không phải hot path
```

### Bẫy 2: Không so sánh được object cấu trúc
```js
Object.is({a: 1}, {a: 1})  // false — khác reference
Object.is([1,2], [1,2])   // false — khác reference
// Dùng deep equality library (lodash isEqual) cho structural comparison
```

### Bẫy 3: Không tự unwrap Promise
```js
const p1 = Promise.resolve(1);
const p2 = Promise.resolve(1);
Object.is(p1, p2) // false — 2 promise objects khác nhau
```

## 💡 Khi nào dùng

| Tình huống | Lý do |
|---|---|
| Làm key cho `Map` với NaN | `map.set(NaN, x)` cần SameValue |
| React state comparison | `Object.is` là default memoization |
| Financial/numerical apps | Phân biệt -0/+0 quan trọng |
| Deep equality replacement | Partial replace cho object comparison |

## 🎯 Ví dụ minh họa

### React dùng Object.is cho memoization
```js
// React internal:
function is(x, y) {
  if (x === y) return x !== 0 || 1 / x === 1 / y;
  return x !== x && y !== y; // NaN check
}

// Equivalent to Object.is in modern JS
```

### Map với NaN key
```js
const cache = new Map();
cache.set(NaN, "not-a-number");
cache.get(NaN); // "not-a-number" ← hoạt động vì Map dùng SameValue

// Nếu dùng ===:
const obj = {};
obj[NaN] = "value";
obj[NaN]; // "value" (JavaScript coerces NaN key to "NaN" string)
```

### Phân biệt -0 và +0 trong tính toán
```js
function normalizeAngle(angle) {
  // Trong graphics, -0 và +0 góc khác nhau
  return Object.is(angle, -0) ? 360 : angle;
}

function signedZero(x) {
  return Object.is(x, -0) ? "-0" : String(x);
}
console.log(signedZero(0));   // "0"
console.log(signedZero(-0));  // "-0"
```

## 🔬 So sánh alternatives

| Method | NaN | ±0 | Objects | Performance |
|---|---|---|---|---|
| `===` | ✗ | ✗ | ref | fastest |
| `Object.is` | ✓ | ✓ | ref | ~2x slower |
| `lodash.isEqual` | ✓ | ✓ | deep | ~100x slower |
| JSON.stringify | ✓ | ✗ | structural | slow + order-dependent |

## 📊 Best Practices

1. **Default:** dùng `===` cho 99% trường hợp
2. **Map/Set keys:** `Object.is` hoặc mặc định (Map/Set tự dùng SameValue)
3. **React hooks:** `Object.is` đã được React dùng nội bộ
4. **Financial code:** `Object.is` cho precise zero handling
5. **Structural comparison:** dùng thư viện (lodash, deep-equal)

## 🔗 Liên kết chéo
- Xem thêm: `04_equality-comparisons/01_loose-strict` (== vs ===)
- Xem thêm: `04_equality-comparisons/03_samevaluezero` (SameValueZero)
- Xem thêm: `03_data-structures/02_keyed-collections` (Map/Set internals)
