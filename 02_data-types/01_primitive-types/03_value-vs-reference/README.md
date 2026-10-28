# Value Types và Reference Types — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

JavaScript chia thành hai nhóm theo **cách lưu và gán giá trị** trong bộ nhớ. Hiểu sự khác biệt này là **nền tảng quan trọng nhất** để tránh vô số bug về state, clone, và mutation.

### 1. Value Type (kiểu tham trị) — Primitive

Mỗi lần gán hoặc truyền vào hàm, giá trị được **sao chép vào ô nhớ mới hoàn toàn**. Biến `b = a` tạo bản sao độc lập — thay đổi `a` sau đó không ảnh hưởng `b`.

```js
let a = 1;
let b = a;    // sao chép GIÁ TRỊ (1) vào ô nhớ mới
a = 2;
console.log(b); // 1 — b vẫn là 1, không đổi theo a
```

- Tất cả primitive đều là value type: `string`, `number`, `boolean`, `bigint`, `symbol`, `undefined`, `null`.
-primitive được lưu trên **stack memory** — truy cập nhanh, giải phóng ngay khi ra khỏi scope.

### 2. Reference Type (kiểu tham chiếu) — Object, Array, Function

Biến chỉ lưu **tham chiếu (địa chỉ bộ nhớ)** trỏ đến object trong **heap**. Khi `b = a`, cả hai biến trỏ cùng một object — sửa `a` sẽ thấy kết quả ở `b`.

```js
let a = { name: "Mercedes" };
let b = a;       // cả hai trỏ CÙNG MỘT object trong heap
a.name = "BMW";
console.log(b);  // { name: "BMW" } — b cũng đổi theo!
console.log(b === a); // true — cùng tham chiếu (cùng địa chỉ)
```

- Object, array, function được lưu trên **heap memory** — shared reference, GC quản lý.
- `const` với object **chỉ khóa tham chiếu**, không khóa nội dung — vẫn sửa được thuộc tính!

```js
const arr = [1, 2, 3];
const arr2 = arr;      // arr2 trỏ cùng mảng
arr2.push(4);
console.log(arr);      // [1, 2, 3, 4] — arr cũng đổi!
// arr = [];           // ❌ TypeError — không gán lại được tham chiếu
```

### Truyền vào hàm — value copy vs reference copy

```js
// Primitive: truyền theo giá trị — hàm không thể sửa biến ngoài
function swapValue(a, b) {
  let temp = a;
  a = b;
  b = temp;
}
let x = 1, y = 2;
swapValue(x, y);
console.log(x, y); // 1 2 — không đổi!

// Object: truyền theo tham chiếu — hàm có thể sửa nội dung
function updateName(obj) {
  obj.name = 'Mercedes';
}
const f = { name: 'BMW' };
updateName(f);
console.log(f.name); // 'Mercedes' — đổi thật!
```

### `const` với object — hiểu đúng bản chất

```js
const bird = { species: "Kestrel" };

// ✅ OK — sửa thuộc tính bên trong object (mutation)
bird.species = "Striated Caracara";
bird.color = "brown";

// ✅ OK — thêm property mới
console.log(bird); // { species: 'Striated Caracara', color: 'brown' }

// ❌ TypeError — không gán lại được THAM CHIẾU
// bird = {};
// bird = { species: "Eagle" };
```

## 📐 Cấu trúc nhóm

```
02_data-types/01_primitive-types/03_value-vs-reference/
├── README.md         ← bài này
└── app.js            ← demo value vs reference
    └── index.html
```

## ✅ Điểm mạnh — Tại sao hiểu value vs reference quan trọng

| # | Điểm mạnh | Lý do |
|---|-----------|-------|
| 1 | **Primitive an toàn khi truyền vào hàm** | Không lo bị thay đổi ngoài ý muốn — pure function dễ reasoning |
| 2 | **Object/shared data dùng tham chiếu** | Tiết kiệm bộ nhớ, thay đổi đồng bộ giữa các biến |
| 3 | **Hiểu `const` đúng nghĩa** | `const` khóa tham chiếu, không khóa nội dung — tránh hiểu lầm |
| 4 | **Biết khi nào cần deep copy** | `structuredClone`, `JSON.parse/stringify`, hoặc library |
| 5 | **Debug state bug dễ hơn** | Nhận ra nguyên nhân "sửa copy làm đổi gốc" |
| 6 | **React/Redux state management** | Immutable pattern dựa trên hiểu value vs reference |

## ⚠️ Bẫy thường gặp & Hạn chế

| # | Bẫy | Ví dụ | Cách tránh |
|---|-----|-------|-----------|
| 1 | **`let b = a` với object không tạo bản sao** | `a.x = 1; b.x` cũng là 1 | Dùng `{...a}` hoặc `structuredClone(a)` để copy |
| 2 | **`const` object vẫn mutate được** | `const obj = {}; obj.x = 1;` — OK | Dùng `Object.freeze(obj)` nếu cần immutable |
| 3 | **`===` so sánh object theo tham chiếu** | `{} === {}` → `false` | Dùng deep equal library hoặc `JSON.stringify` compare |
| 4 | **Shallow copy `{...obj}` chỉ copy một lớp** | Nested object vẫn shared | Dùng `structuredClone` cho deep copy |
| 5 | **`JSON.parse(JSON.stringify(obj))` mất giá trị đặc biệt** | `undefined` → bỏ qua, `Date` → string, `NaN` → `null` | Dùng `structuredClone` thay thế |
| 6 | **Array push/pop trên const array** | `const arr = []; arr.push(1);` — OK | Hiểu `const` khóa reference, không contents |

## 💡 Khi nào dùng — Tình huống thực tế

1. **Primitive** — lưu ID, số, chuỗi — muốn mỗi biến tự trị, thay đổi không "lây".
2. **Object** — lưu cấu trúc dữ liệu phức tạp (user, product, config) — muốn share chung.
3. **Khi cần giữ nguyên object gốc** → copy sâu (`structuredClone`, `JSON.parse/stringify`, hoặc lodash `cloneDeep`).
4. **Truyền object vào hàm** — cẩn thận accidental mutation; tạo bản sao trước khi xử lý nếu cần giữ gốc.
5. **React state update** — immutable pattern: `setState({...state, key: newValue})` thay vì mutate directly.
6. **Memoization cache** — dùng object làm cache, hiểu rằng cache shared giữa calls.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Primitive — value copy

```js
// Primitive: value copy
let x = "hello";
let y = x;         // sao chép GIÁ TRỊ "hello"
x = "world";
console.log(y);    // "hello" — không đổi, y có bản sao riêng

let a = 42;
let b = a;
a = 100;
console.log(b);    // 42 — b giữ nguyên giá trị ban đầu
```

### Ví dụ 2: Object — reference copy

```js
// Object: reference copy
let obj1 = { a: 1, b: 2 };
let obj2 = obj1;         // cả hai trỏ CÙNG object trong heap
obj1.a = 99;             // sửa obj1
console.log(obj2.a);     // 99 — obj2 cũng đổi theo!
console.log(obj1 === obj2); // true — cùng reference

// Object.freeze — shallow immutable
const frozen = Object.freeze({ x: 1, y: 2 });
frozen.x = 99;            // silently fails (hoặc TypeError in strict mode)
console.log(frozen.x);    // 1 — không đổi
```

### Ví dụ 3: Array — reference copy

```js
const arr = [1, 2, 3];
const arr2 = arr;        // reference copy
arr2.push(4);
console.log(arr);        // [1, 2, 3, 4] — arr cũng đổi!

// Copy array an toàn
const arrCopy = [...arr];    // shallow copy
arrCopy.push(5);
console.log(arr);            // [1, 2, 3, 4] — arr gốc không đổi

const arrCopy2 = arr.slice(); // shallow copy cách 2
const arrCopy3 = arr.concat(); // shallow copy cách 3
```

### Ví dụ 4: Shallow vs Deep copy

```js
const original = {
  name: "Sơn",
  address: { city: "SG", district: "Q1" },
  scores: [90, 85, 92]
};

// Shallow copy — chỉ copy tầng đầu
const shallow = { ...original };
shallow.name = "Nam";
shallow.address.city = "HN";   // ❌ address shared!
console.log(original.address.city); // "HN" — gốc bị đổi!

// Deep copy — structuredClone (ES2022)
const deep = structuredClone(original);
deep.address.city = "DN";
console.log(original.address.city); // "SG" — gốc không đổi ✓

// Deep copy — JSON (cẩn thận với Date, NaN, undefined)
const jsonCopy = JSON.parse(JSON.stringify(original));
jsonCopy.address.city = "CT";
console.log(original.address.city); // "SG" — cũng OK nhưng mất Date/undefined/function
```

### Ví dụ 5: Truyền vào hàm — value vs reference

```js
// Primitive parameter — copy by value
function increment(n) {
  n = n + 1;
  console.log("inside:", n); // 11
}
let num = 10;
increment(num);
console.log("outside:", num); // 10 — không đổi!

// Object parameter — copy by reference (mutation possible)
function updateAge(user) {
  user.age = 26;
  console.log("inside:", user.age); // 26
}
const person = { name: "Hoa", age: 25 };
updateAge(person);
console.log("outside:", person.age); // 26 — đổi thật!

// Safe: truyền bản sao vào hàm mutate
function safeUpdate(user) {
  const copy = { ...user };    // shallow copy
  copy.age = 26;
  return copy;                 // return new object
}
const updated = safeUpdate(person);
console.log(person.age);     // 25 — gốc không đổi
console.log(updated.age);    // 26 — copy đã đổi
```

### Ví dụ 6: const với object — tham chiếu cố định, nội dung thay đổi

```js
const config = { host: "localhost", port: 3000 };

// ✅ Sửa property được
config.host = "production";
config.timeout = 5000;       // thêm property mới
console.log(config);          // { host: 'production', port: 3000, timeout: 5000 }

// ❌ Không gán lại được reference
// config = { host: "staging" }; // TypeError

// Object.freeze — shallow freeze
const frozenConfig = Object.freeze({ host: "localhost", port: 3000 });
frozenConfig.host = "production"; // silently fails
console.log(frozenConfig.host);   // "localhost"
```

## 🔬 So sánh với alternatives

| Phương án | Ưu điểm | Nhược điểm | Phù hợp khi |
|-----------|---------|------------|-------------|
| **Native shallow copy (`{...obj}`, `[...arr]`)** | Nhanh, built-in, syntax gọn | Chỉ copy tầng 1 — nested vẫn shared | Object phẳng, không có nested |
| **`structuredClone()` (ES2022)** | Deep copy chính xác, giữ Date/NaN/Map/Set | Browser cũ không support | Modern apps, complex nested data |
| **`JSON.parse(JSON.stringify(obj))`** | Deep copy đơn giản, ubiquitous | Mất function/undefined/Date→string, NaN→null | Simple data, no special types |
| **Lodash `_.cloneDeep`** | Deep copy robust, edge cases handled | Extra dependency (~7KB gzipped) | Legacy projects, complex objects |
| **Immutable libraries (Immer, Immutable.js)** | Structural sharing, performant | Learning curve, API khác biệt | Redux state management |

## 📊 Performance & Best Practices

- **Mặc định dùng shallow copy `{...obj}`** cho object phẳng — nhanh và đủ.
- **Dùng `structuredClone()`** cho nested object hoặc object chứa Date/Map/Set — chính xác nhất.
- **Tránh `JSON.parse/stringify`** cho object chứa `undefined`, `function`, `Date` — dữ liệu bị biến đổi.
- **Dùng `Object.freeze()`** cho config/constants — shallow immutable, phòng mutate ngoài ý muốn.
- **React state: immutable update pattern** — `setState({...state, key: newVal})` thay vì mutate directly.
- **Truyền bản sao vào hàm mutate** — nếu hàm cần sửa object, copy trước rồi truyền vào, return lại.
- **Kiểm tra `Array.isArray()`** trước khi spread/array copy — `typeof [] === "object"`.

## 🔗 Liên kết chéo

- Xem thêm: `02_data-types/01_primitive-types/` — 7 primitive types (value types)
- Xem thêm: `02_data-types/02_objects-and-prototype/` — object reference types
- Xem thêm: `02_data-types/02_objects-and-prototype/03_shallow-deep-clone/` — clone strategies chi tiết
- Xem thêm: `03_data-structures/01_arrays/` — array mutation methods (push, splice...)
- Xem thêm: `17_memory-management/01_memory-lifecycle-gc/` — GC và reference counting
- Tài liệu: [MDN — Comparison operators](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Equality_comparisons_and_sameness), [javascript.info/reference-type](https://javascript.info/reference-type)
