# SameValueZero — Algorithm Cho Map/Set

## 🔑 Khái niệm cốt lõi

**SameValueZero** là thuật toán so sánh được JavaScript engine dùng nội bộ cho:
- `Map.prototype.set/get/delete`
- `Set.prototype.add.has.delete`
- `Array.prototype.indexOf`
- `Array.prototype.lastIndexOf`

Khác với SameValue (`Object.is`): **SameValueZero coi `-0 === +0` là `true`** (trỞ lại như `===`).

### Thuật toán SameValueZero (ECMA-262 §7.2.14)

```
1. Nếu x cùng kiểu (Type) và y cùng kiểu (Type):
   a. Number:
      - x là NaN và y là NaN → true
      - x là +0 và y là -0, HOẶC x là -0 và y là +0 → true  ← KHÁC SameValue
      - x === y → true
      - otherwise → false
   b. Khác Number → same as SameValue
2. Nếu khác kiểu (type) → false
```

## 📐 So sánh 3 thuật toán

| Trường hợp | SameValue (`===`) | SameValueZero | Object.is |
|---|---|---|---|
| `NaN` vs `NaN` | false | **true** | true |
| `-0` vs `+0` | **true** | **true** | false |
| `5` vs `5` | true | true | true |
| `"a"` vs `"a"` | true | true | true |
| `{}` vs `{}` | false | false | false |

## ✅ Điểm mạnh

| Ưu điểm | Ứng dụng thực tế |
|---|---|
| `indexOf(NaN)` tìm được NaN | Debug, validation arrays |
| Map/Set handle NaN key | Cache, lookup tables |
| `-0 === +0` trong collection | Tránh duplicate trong Set |
| Internal engine use | Không cần implement manual |

## ⚠️ Bẫy thường gặp

### Bẫy 1: indexOf không tìm được NaN
```js
const arr = [1, NaN, 3];
arr.indexOf(NaN);     // -1  ← SameValueZero fails for NaN!
arr.findIndex(x => Object.is(x, NaN)); // 1  ← correct
```
**Thực tế:** `indexOf` dùng SameValueZero, nên NaN không tìm được. Dùng `findIndex` + `Object.is` thay thế.

### Bẫy 2: Map key NaN hoạt động
```js
const map = new Map();
map.set(NaN, "value");
map.get(NaN); // "value" ← Map dùng SameValue, tìm được NaN
```

### Bẫy 3: Set chứa NaN multiple lần?
```js
const set = new Set();
set.add(NaN);
set.add(NaN);
set.size; // 1 — cùng key NaN, không duplicate
```

### Bẫy 4: -0 và +0 trong Set
```js
const set = new Set();
set.add(-0);
set.add(+0);
set.size; // 1 — SameValueZero coi -0 === +0
```

## 💡 Khi nào dùng

| Tình huống | Giải pháp |
|---|---|
| Tìm NaN trong array | `findIndex(x => Object.is(x, NaN))` |
| Check existence in Map/Set | `.has(key)` — internal SameValue/SameValueZero |
| Duplicate removal | `new Set(arr)` — tự handle SameValueZero |
| Precise numeric comparison | `Object.is(a, b)` |

## 🎯 Ví dụ minh họa

### Tìm NaN trong array (pattern thường gặp)
```js
function findNaNIndex(arr) {
  return arr.findIndex(val => val !== val); // NaN !== NaN là true
}

// Hoặc dùng Object.is
function findNaNIndexV2(arr) {
  return arr.findIndex(val => Object.is(val, NaN));
}

const data = [1, 2, NaN, 4, NaN];
console.log(findNaNIndex(data));  // 2
console.log(findNaNIndexV2(data)); // 2
```

### Map với nhiều loại key
```js
const cache = new Map();

// Các key đều khác nhau
cache.set("str", "string");
cache.set(123, "number");
cache.set(NaN, "not-a-number");
cache.set(null, "null-value");
cache.set(undefined, "undefined-value");
cache.set(-0, "negative-zero");
cache.set(+0, "positive-zero"); // ghi đè -0 vì SameValueZero

console.log(cache.size); // 6 (NaN, -0, +0 hợp nhất thành 1)
```

### Set deduplication với đối tượng
```js
const seen = new Set();
const items = [{id: 1}, {id: 2}, {id: 1}, {id: 2}];

// Object reference-based dedup
items.forEach(item => seen.add(JSON.stringify(item)));
console.log(seen.size); // 2
```

## 🔬 Performance

| Operation | Time Complexity | Notes |
|---|---|---|
| Map.set/get | O(1) avg | Hash-based, SameValue comparison |
| Set.add/has | O(1) avg | Hash-based, SameValueZero comparison |
| indexOf | O(n) | Linear scan, SameValueZero |
| findIndex(Object.is) | O(n) | Linear scan, SameValue |

## 📊 Best Practices

1. **Array search:** dùng `findIndex` + `Object.is` thay `indexOf` cho NaN
2. **Map keys:** thoải mái dùng NaN, -0, +0 — engine handle đúng
3. **Set dedup:** `-0` và `+0` tự hợp nhất (SameValueZero)
4. **Object comparison:** `===` chỉ so sánh reference, cần deep equal library
5. **Hot path:** dùng `===` thay `Object.is` khi không cần NaN/±0 precision

## 🔗 Liên kết chéo
- Xem thêm: `04_equality-comparisons/01_loose-strict` (== vs ===)
- Xem thêm: `04_equality-comparisons/02_object-is` (SameValue)
- Xem thêm: `03_data-structures/02_keyed-collections` (Map/Set internals)
