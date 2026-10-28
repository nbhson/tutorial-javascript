# Object.is() — SameValue Algorithm

## 🔑 Khái niệm cốt lõi

`Object.is(a, b)` (ES2015/ES6) thực hiện **SameValue** algorithm — giống `===` nhưng sửa 2 lỗi thiết kế:

1. **NaN** được coi là bằng chính nó (`NaN === NaN` → `false`, `Object.is(NaN, NaN)` → `true`)
2. **`-0` và `+0`** được phân biệt (`-0 === +0` → `true`, `Object.is(-0, +0)` → `false`)

### Thuật toán SameValue (ECMA-262 §7.2.13)

```
1. Nếu a cùng kiểu (Type):
   a. Number:
      - both NaN → true
      - both +0 hoặc both -0 → true
      - same value → true
      - otherwise → false
   b. Khác Number cùng Type → same as ===
2. Nếu khác kiểu (type) → false
```

Tóm lại, toàn bộ khác biệt giữa `Object.is` và `===` nằm trong **2 dòng** xử lý Number: NaN và ±0. Mọi kiểu khác (string, boolean, null, undefined, object) hành xử y hệt `===`.

### Polyfill — tự viết Object.is() bằng ===

Đây là câu hỏi phỏng vấn kinh điển, và cũng là polyfill chính thức trong spec (ECMA-262 Annex B):

```js
if (!Object.is) {
  Object.is = function (x, y) {
    // Trường hợp giống === :
    if (x === y) {
      // Lưu ý đặc biệt duy nhất: 0 === -0 nhưng Object.is(-0, 0) phải là false.
      // Mẹo: 1/0 = +Infinity, 1/-0 = -Infinity → phân biệt được hai dấu zero
      return x !== 0 || 1 / x === 1 / y;
    }
    // Trường hợp khác === : NaN !== NaN, nhưng Object.is(NaN, NaN) = true
    // (x !== x chỉ đúng khi x là NaN — đây là cách nhận diện NaN duy nhất trước Number.isNaN)
    return x !== x && y !== y;
  };
}
```

Cả hai dòng "ma thuật" đều đáng hiểu kỹ:

- `x !== 0 || 1/x === 1/y` — khi `x === y` đã true, chỉ còn cần chặn trường hợp cả hai là 0 khác dấu. Nếu `x` là `+0` thì `1/x = Infinity`, `-0` thì `1/x = -Infinity` → so sánh hai kết quả này phân biệt được dấu.
- `x !== x && y !== y` — NaN là giá trị duy nhất không bằng chính nó, nên phép kiểm tra "không tự bằng chính mình" chính là NaN detector.

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
| `Object.is(NaN, NaN)` trong Map/Set | — | luôn true | Map/Set dùng SameValueZero (khác SameValue ở ±0!) |

Chú ý dòng cuối: **Map/Set dùng SameValueZero**, không phải SameValue — SameValueZero coi `-0 === +0` (cùng entry), còn `Object.is` phân biệt. Đây là sự khác biệt tinh tế giữa 3 thuật toán, chi tiết đầy đủ ở `04_equality-comparisons/03_samevaluezero`.

### Nguồn gốc của -0 trong thực tế

`-0` không phải lý thuyết suông — nó sinh ra từ phép tính thông thường:

```js
Math.round(-0.4);   // -0
Math.round(-0.5);   // -0
-1 * 0;             // -0
0 * -Infinity;      // -0
-0;                 // -0 (literal)
Object.freeze([-0])[0]; // -0
Math.min(-0, -1) + 1;   // -0
JSON.parse("-0");       // -0 (JSON hỗ trợ -0!)

// Nhưng các phép "làm mờ dấu" dễ khiến bạn không nhận ra:
-0 + 0;              // 0  — cộng thêm thì mất dấu
-0 * 1;              // -0 — nhân vẫn giữ dấu
Math.abs(-0);        // 0
-0 === 0;            // true — === che mất khác biệt
Object.is(-0, 0);    // false — chỉ Object.is thấy được
```

## ✅ Điểm mạnh

| Ưu điểm | Ứng dụng |
|---|---|
| Correct NaN comparison | Map key, Set member, so sánh kết quả phép tính |
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

### Bẫy 4: Kỳ vọng sai về Set/Map

```js
// Nhầm tưởng: "Map dùng Object.is nên -0 và +0 là 2 key"
const m = new Map();
m.set(0, "zero");
m.has(-0); // true — Map dùng SameValueZero: -0 và +0 là CÙNG key!
// Object.is phân biệt ±0, SameValueZero thì không — khác nhau đúng một điểm này.
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

Đây chính là lý do `Object.is` được nhắc trong tài liệu React: `useMemo`, `memo`, `useEffect` dependency so sánh bằng hàm `is` này. Hệ quả thực tế:

```js
function Component() {
  const [count, setCount] = useState(0);
  // Nếu setState bằng -0 rồi +0, React (với Object.is) coi là THAY ĐỔI → re-render.
  // Nếu là 0 → 0, Object.is(0, 0) = true → không re-render.
  setCount(-0);
  setCount(0); // vẫn re-render vì Object.is(-0, 0) === false
}
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

Ứng dụng thực tế của việc phân biệt ±0: định dạng số tài chính (hiển thị `-$0.00` cho khoản nợ bằng 0), phát hiện hướng di chuyển (vận tốc -0 nghĩa là đang giảm tốc), vẽ biểu đồ (góc quay -0° và 0° khác chiều animation).

### Kiểm tra -0/NaN một cách tường minh

```js
// Tại sao phải Object.is mà không dùng ===?
console.log(-0 === 0);            // true — vô dụng để phát hiện -0
console.log(Object.is(-0, -0));   // true
console.log(Object.is(-0, 0));    // false ← cách duy nhất để phát hiện -0

// Kiểm tra NaN:
console.log(NaN === NaN);         // false — vô dụng
console.log(NaN !== NaN);         // true — mẹo cũ
console.log(Object.is(NaN, NaN)); // true
console.log(Number.isNaN(NaN));   // true — cách ưa dùng ngày nay

// Lưu ý global isNaN vs Number.isNaN:
console.log(isNaN("hello"));        // true! — ép kiểu "NaN" → NaN trước
console.log(Number.isNaN("hello")); // false — không ép kiểu, đúng nghĩa hơn
```

## 🔬 So sánh các thuật toán so sánh

| Method | NaN | ±0 | Objects | Performance |
|---|---|---|---|---|
| `==` | false | true | ép kiểu rồi ref | fastest + coercion |
| `===` | ✗ false | ✗ true (trùng) | ref | fastest |
| `Object.is` (SameValue) | ✓ true | ✓ false (phân biệt) | ref | ~2x slower |
| SameValueZero (Map/Set/includes) | ✓ true | ✗ true (trùng) | ref | fast |
| `lodash.isEqual` | ✓ | ✓ | deep | ~100x slower |
| JSON.stringify | ✓ | ✗ | structural | slow + order-dependent |

Bảng tóm tắt cả 3 thuật toán của spec:

| | NaN vs NaN | +0 vs -0 | Nơi dùng |
|---|---|---|---|
| IsLooselyEqual (`==`) | false | true | đã deprecated về mặt thực hành |
| IsStrictlyEqual (`===`) | false | true | default |
| SameValue (`Object.is`) | true | false | hiếm, React |
| SameValueZero (Map/Set/`includes`) | true | true | Map, Set, `Array.prototype.includes` |

## 📊 Best Practices

1. **Default:** dùng `===` cho 99% trường hợp
2. **Map/Set keys:** `Object.is` hoặc mặc định (Map/Set tự dùng SameValue)
3. **React hooks:** `Object.is` đã được React dùng nội bộ
4. **Financial code:** `Object.is` cho precise zero handling
5. **Structural comparison:** dùng thư viện (lodash, deep-equal)
6. **Kiểm tra NaN:** ưu tiên `Number.isNaN()` — đọc rõ ý đồ hơn `Object.is(x, NaN)`
7. **Đừng dùng Object.is thay `===` "cho chắc"**: chậm hơn và ngữ cảnh ±0 hiếm khi quan trọng

## 🔗 Liên kết chéo

- Xem thêm: `04_equality-comparisons/01_loose-strict` (== vs ===)
- Xem thêm: `04_equality-comparisons/03_samevaluezero` (SameValueZero)
- Xem thêm: `03_data-structures/02_keyed-collections` (Map/Set internals)
- Tài liệu: [MDN — Object.is](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/is)
