# Equality Comparisons — So Sánh Bằng Nhau

> **roadmap.sh:** `==` vs `===`, `Object.is`, SameValue, SameValueZero

## 🔑 Khái niệm cốt lõi

JavaScript có **3 cơ chế so sánh bằng** khác nhau, mỗi cái phù hợp cho ngữ cảnh riêng:

| Operator | Tên kỹ thuật | Hành vi |
|---|---|---|
| `==` | Abstract Comparison (Loose) | Ép kiểu (coercion) trước khi so sánh |
| `===` | Strict Equality | So sánh kiểu + giá trị, không ép kiểu |
| `Object.is(a, b)` | SameValue | Giống `===` nhưng xử lý đúng `NaN` và `-0` |

**ES2016 (ES7)** thêm `Object.is()` để giải quyết 2 lỗi thiết kế của `===`:
1. `NaN === NaN` trả về `false` (mặc dù cùng giá trị)
2. `-0 === +0` trả về `true` (mặc dù khác dấu)

`Object.is(NaN, NaN)` → `true`, `Object.is(-0, +0)` → `false`.

## 📐 Bảng ép kiểu của `==` (Abstract Equality)

| Trường hợp | Kết quả |
|---|---|
| `null == undefined` | `true` |
| `null == null` | `true` |
| `undefined == undefined` | `true` |
| `NaN == anything` | `false` (kể cả chính nó) |
| `string == number` | Convert string sang number |
| `boolean == anything` | Convert boolean sang number (true→1, false→0) |
| `string == object` | Convert object thành primitive, rồi so sánh |
| `number == object` | Convert object thành primitive, rồi so sánh |

**Primitive conversion rule:** object → `valueOf()` → `toString()` → so sánh kết quả.

## ✅ Điểm mạnh

| Ưu điểm | Lý do |
|---|---|
| `===` tránh bug coercion | Không surprises từ `"" == false` → `true` |
| `Object.is` chính xác tuyệt đối | Xử lý đúng NaN, -0, +0 |
| `==` hữu ích cho null check | `x == null` kiểm tra cả null lẫn undefined |
| SameValueZero dùng trong Map/Set | `[NaN]` tồn tại trong Set, indexOf tìm NaN |

## ⚠️ Bẫy thường gặp

### Bẫy 1: `"" == false` là `true`
```js
"" == false  // true — string "" → 0, boolean false → 0, 0 == 0
"" === false // false — khác kiểu (string ≠ boolean)
```

### Bẫy 2: `[] == ![]` là `true`
```js
[] == ![]
// ![] → false → 0
// [] == 0 → [] → "" → 0 → 0 == 0 → true
[] === ![] // false
```

### Bẫy 3: `NaN` không bằng chính nó
```js
NaN === NaN   // false
NaN == NaN    // false
Object.is(NaN, NaN) // true — cách đúng
```

### Bẫy 4: `-0` và `+0`
```js
-0 === +0     // true
Object.is(-0, +0) // false
1 / -0 === 1 / +0 // true (cùng NaN-ish)
1 / -0 < 0    // true — phân biệt được qua phép chia
```

### Bẫy 5: Object reference luôn khác
```js
({} === {})    // false — 2 object riêng biệt
([] === [])    // false
([1] === [1])  // false — mỗi lần tạo là object mới
```

## 💡 Khi nào dùng

| Tình huống | Toán tử | Lý do |
|---|---|---|
| So sánh giá trị thuần túy | `===` | Tránh coercion bất ngờ |
| Kiểm tra null/undefined | `== null` | Đúng cho cả null VÀ undefined |
| Key trong Map/Set | `Object.is` | NaN là key hợp lệ |
| Array.indexOf | internal SameValueZero | Tìm NaN trong mảng |
| Config/default values | `??` thay `||` | Giữ nguyên 0, "", false |

## 🎯 Ví dụ minh họa

### 1. Null check thông dụng
```js
function process(user) {
  if (user == null) {  // đúng cho null VÀ undefined
    throw new Error("User required");
  }
  return user.name;
}
```

### 2. so sánh Object chính xác
```js
const objA = { x: NaN };
const objB = { x: NaN };
console.log(Object.is(objA.x, objB.x)); // true — NaN === NaN đúng

// Dùng làm key trong Map
const map = new Map();
map.set(NaN, "found");
console.log(map.get(NaN)); // "found"
```

### 3. SameValueZero trong Array
```js
const arr = [1, NaN, 3];
console.log(arr.indexOf(NaN)); // -1 (SameValueZero fails for NaN)
console.log(arr.findIndex(x => Object.is(x, NaN))); // 1 (đúng)
```

### 4. Phân biệt -0 và +0
```js
function sign(x) {
  return Object.is(x, -0) ? "-0" : String(x);
}
sign(-0); // "-0"
sign(0);  // "0"
```

## 🔬 So sánh

| Tiêu chí | `==` | `===` | `Object.is` |
|---|---|---|---|
| Ép kiểu | Có | Không | Không |
| NaN === NaN | false | false | **true** |
| -0 === +0 | true | true | **false** |
| undefined == null | **true** | false | false |
| performance | Nhanh nhất | Nhanh | Chậm hơn ~2x |

## 📊 Performance

- `===` nhanh hơn `Object.is` ~2 lần (không có overhead function call)
- `==` nhanh nhất nhưng không đáng kể so với logic business
- **Không optimize premature** — chọn đúng operator quan trọng hơn speed

## 🔗 Liên kết chéo
- Xem thêm: `01_variables/03_scopes` (typeof trong scope)
- Xem thêm: `02_data-types/01_primitive-types` (kiểu dữ liệu so sánh)
- Xem thêm: `03_data-structures/02_keyed-collections` (Map/Set dùng SameValueZero)
- Xem thêm: `20_modern-javascript/03_optional-chaining-nullish/02_nullish-coalescing` (?? vs ||)
