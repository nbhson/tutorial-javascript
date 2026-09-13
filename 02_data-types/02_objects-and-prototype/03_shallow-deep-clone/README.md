# Shallow vs Deep Clone (Copy nông vs Copy sâu) — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

Khi "copy" một object/array, JavaScript chỉ gán **tham chiếu** nếu bạn viết `const person2 = person1`. Muốn thật sự có một bản sao độc lập, bạn cần **clone**. Có hai mức: **shallow copy** (chỉ copy tầng đầu) và **deep copy** (copy tất cả tầng lồng nhau).

### Tại sao cần clone?

Trong JavaScript, object/array là **reference type** — khi gán hoặc truyền vào hàm, ta chỉ copy **địa chỉ bộ nhớ** trỏ đến object trên heap. Nếu không clone, sửa đổi trên "bản sao" sẽ ảnh hưởng trực tiếp đến object gốc. Đây là nguyên nhân phổ biến nhất của bug "sửa dữ liệu này làm đổi luôn dữ liệu kia" trong state management, form editing, và data transformation.

### 1. Shallow copy (copy nông) — chỉ copy tầng đầu tiên

Mọi object/mảng lồng nhau **vẫn chia sẻ tham chiếu** với bản gốc:

```js
const person1 = {
  name: "Sơn",
  age: 22,
  networks: { facebook: "http://facebook.com" },  // nested object!
};

// Các cách shallow copy:
const a = { ...person1 };              // spread — ES6
const b = Object.assign({}, person1);  // Object.assign — ES6

// Đổi networks.facebook → các bản clone cũng đổi theo (vì cùng tham chiếu!)
person1.networks.facebook = "http://facebook.com/nbhson43";
console.log(a.networks.facebook);  // "http://facebook.com/nbhson43" ← DÍNH!
console.log(b.networks.facebook);  // "http://facebook.com/nbhson43" ← DÍNH!
```

> **Lưu ý `Object.assign`**: đối số **đầu tiên** là object đích — nếu bạn ghi `Object.assign(person1, {...})` thì chính `person1` bị sửa. **Luôn đặt object đích rỗng `{}`** làm tham số đầu.

### 2. Deep copy (copy sâu) — tạo bản sao hoàn toàn độc lập

Mọi tầng đều được nhân bản — sửa bản copy không ảnh hưởng gốc:

```js
// Cách truyền thống: JSON serialize/deserialize
const person2 = JSON.parse(JSON.stringify(person1));
// ⚠️ JSON clone có yếu điểm:
//   - NaN → null
//   - Date → string ISO
//   - undefined/function → BỊ MẤT (skip trong JSON)
//   - Symbol keys → BỊ MẤT
```

### 3. `structuredClone()` — giải pháp hiện đại (ES2022)

```js
const obj = {
  firstName: "David",
  moreInfo: {
    age: 18,
    countries: { anGiang: true, hoChiMinh: true },
    birthday: new Date(),   // Date giữ nguyên là Date ✓
    love: NaN,              // NaN giữ nguyên ✓
    tags: ["a", "b"],       // Array deep copied ✓
    metadata: new Map([["key", "value"]]),  // Map deep copied ✓
  },
};

const objCopy = structuredClone(obj);
objCopy.moreInfo.age = 25;
objCopy.moreInfo.countries.hoChiMinh = false;

console.log(obj.moreInfo.age);            // 18 — gốc KHÔNG đổi ✓
console.log(objCopy.moreInfo.birthday instanceof Date); // true ✓
console.log(objCopy.moreInfo.love);       // NaN ✓ (không bị convert to null)
```

> `structuredClone()` hỗ trợ: **Array, Object, Date, RegExp, Map, Set, ArrayBuffer, TypedArray, Blob, File, ImageData**. Không hỗ trợ: **function, Symbol, WeakMap, DOM nodes** (sẽ throw DataCloneError).

### Tóm tắt các cách copy

| Cách | Loại | Deep? | Giữ Date/NaN? | Giữ Function? | Syntax |
|------|------|-------|---------------|---------------|--------|
| `person2 = person1` | Reference | ❌ | — | — | ❌ Không phải clone |
| `{...obj}` | Shallow | ❌ | ✅ | ✅ | ES6 |
| `Object.assign({}, obj)` | Shallow | ❌ | ✅ | ✅ | ES6 |
| `JSON.parse(JSON.stringify(obj))` | Deep | ✅ | ❌ | ❌ | ES5 |
| `structuredClone(obj)` | Deep | ✅ | ✅ | ❌ | ES2022 |
| `lodash.cloneDeep(obj)` | Deep | ✅ | ✅ | ❌ | Library |

## 📐 Cấu trúc nhóm

```
02_data-types/02_objects-and-prototype/03_shallow-deep-clone/
├── README.md         ← bài này
└── app.js            ← demo shallow, JSON deep, structuredClone
    └── index.html
```

## ✅ Điểm mạnh — Tại sao nên hiểu clone

| # | Điểm mạnh | Lý do |
|---|-----------|-------|
| 1 | **Hiểu shallow/deep** | Biết được "bản sao đó có tách khỏi gốc hay không" — tránh bug mutation |
| 2 | **`structuredClone` an toàn** | Deep copy chính xác với Date, NaN, Map/Set — không mất data |
| 3 | **Shallow copy nhanh** | Đủ dùng cho object "một tầng" (config, props) — performance tốt |
| 4 | **React/Redux pattern** | Immutable state update: `{...state, key: newVal}` — bắt buộc shallow copy |
| 5 | **Tránh mutation bugs** | Clone trước khi pass vào third-party function, không lo "bị sửa" |
| 6 | **Form state snapshot** | Lưu "before" state để compare/cancel edit — cần deep copy |

## ⚠️ Bẫy thường gặp & Hạn chế

| # | Bẫy | Ví dụ | Cách tránh |
|---|-----|-------|-----------|
| 1 | **`const b = a` không phải clone** | Chỉ thêm một "biệt danh" trỏ cùng vùng nhớ | Dùng spread hoặc structuredClone |
| 2 | **Shallow copy không tách nested** | `person1.networks` vẫn shared | Dùng `structuredClone` cho nested |
| 3 | **JSON clone phá giá trị đặc biệt** | `NaN → null`, `Date → string`, `function → mất` | Dùng `structuredClone` thay thế |
| 4 | **`structuredClone` throw on function/DOM** | `structuredClone({ fn: () => {} })` → DataCloneError | Xử lý function/DOM separately trước clone |
| 5 | **Circular reference** | `obj.self = obj; JSON.stringify(obj)` → TypeError | `structuredClone` xử lý được circular refs |
| 6 | **Performance cost deep clone** | Large nested object → slow | Chỉ deep clone khi cần; shallow cho flat data |
| 7 | **Map/Set key by reference** | Shallow copy `new Map(oldMap)` — keys vẫn shared | Deep clone Map entries manually if needed |

## 💡 Khi nào dùng — Tình huống thực tế

1. **Sửa dữ liệu form mà không muốn động đến giá trị gốc** → deep copy `structuredClone(formData)`.
2. **React state update** → `{...state, updatedKey}` — immutable shallow update.
3. **Lưu "snapshot" cấu hình trước khi thay đổi** → `const backup = structuredClone(config)`.
4. **Pass object vào third-party function** → clone trước để không bị unexpected mutation.
5. **Unit test fixtures** → deep copy test data để mỗi test case độc lập.
6. **Redux action payload** → immutable update: `[{...item, status: 'done'}]`.
7. **Object đơn tầng** → `{...obj}` nhanh và đủ; nested hoặc chứa Date/NaN → `structuredClone`.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Reference assignment — NOT cloning

```js
const original = { name: "Sơn", scores: [90, 85, 92] };
const alias = original;     // KHÔNG phải clone — chỉ thêm reference

alias.name = "Nam";
console.log(original.name); // "Nam" — GỐC CŨNG ĐỔI!
console.log(original === alias); // true — cùng object

// Deep modify through alias
alias.scores.push(88);
console.log(original.scores); // [90, 85, 92, 88] — shared nested array!
```

### Ví dụ 2: Shallow copy — nested objects still shared

```js
const original = {
  name: "Sơn",
  address: { city: "SG", district: "Q1" },
  scores: [90, 85, 92],
};

// Spread shallow copy
const shallow1 = { ...original };
// Object.assign shallow copy
const shallow2 = Object.assign({}, original);

// Change top-level property — no effect on original
shallow1.name = "Nam";
console.log(original.name);      // "Sơn" ✓ — top level independent

// Change nested property — SHARED reference!
shallow1.address.city = "HN";
console.log(original.address.city); // "HN" ❌ — GỐC BỊ ĐỔI!

// Shallow copy của array nested — also shared
const arrCopy = [...original.scores];
arrCopy.push(88);
console.log(original.scores.length); // 4 — original also changed!

// Solution: clone nested manually
const manualDeep = {
  ...original,
  address: { ...original.address },   // deep copy nested object
  scores: [...original.scores],        // deep copy nested array
};
```

### Ví dụ 3: JSON deep copy — simple but with pitfalls

```js
const data = {
  name: "Sơn",
  address: { city: "SG" },
  scores: [90, 85],
  created: new Date(),     // Date!
  score: NaN,              // NaN!
  callback: function() {}, // Function!
  temp: undefined,         // Undefined!
};

const jsonCopy = JSON.parse(JSON.stringify(data));

console.log(jsonCopy.address.city); // "SG" — nested deep copied ✓
console.log(jsonCopy.created);      // "2025-..." — Date becomes STRING ❌
console.log(jsonCopy.score);        // null — NaN becomes null ❌
console.log(jsonCopy.callback);     // undefined — function lost ❌
console.log(jsonCopy.temp);         // undefined — property removed from object ❌
```

### Ví dụ 4: `structuredClone` — the modern solution

```js
const obj = {
  name: "Sơn",
  address: { city: "SG", geo: { lat: 10.7, lng: 106.6 } },
  scores: [90, 85, 92],
  birthday: new Date("2000-01-01"),
  tags: new Set(["js", "web"]),
  metadata: new Map([["version", 1]]),
  data: new Uint8Array([1, 2, 3]),
};

const deep = structuredClone(obj);

// Modify everything in copy — original unaffected
deep.address.city = "HN";
deep.scores.push(88);
deep.birthday.setFullYear(2025);
deep.tags.add("deep");

console.log(obj.address.city);       // "SG" ✓
console.log(obj.scores.length);      // 3 ✓
console.log(obj.birthday.getFullYear()); // 2000 ✓
console.log(obj.tags.has("deep"));   // false ✓
console.log(deep.birthday instanceof Date);  // true ✓ — Date preserved!

// Circular reference — structuredClone handles, JSON doesn't!
const circular = { name: "test" };
circular.self = circular;
// JSON.stringify(circular); // ❌ TypeError: Converting circular structure to JSON
const circularCopy = structuredClone(circular); // ✅ works
console.log(circularCopy.self === circularCopy); // false — proper deep copy
```

### Ví dụ 5: Lodash cloneDeep — library approach

```js
// npm install lodash
// import _ from "lodash";

const complex = {
  name: "Sơn",
  address: { city: "SG" },
  callback: function () { return "hi"; },  // function preserved!
  createdAt: new Date(),
};

const cloned = _.cloneDeep(complex);
cloned.address.city = "HN";

console.log(complex.address.city);    // "SG" — original unchanged ✓
console.log(typeof cloned.callback);  // "function" — function preserved ✓
console.log(cloned.callback());       // "hi" — still works ✓
console.log(cloned.createdAt instanceof Date); // true ✓
```

### Ví dụ 6: Performance comparison — khi nào dùng cách nào

```js
const obj = { a: 1, b: { c: 2, d: { e: 3 } } };

// Test performance for 1M iterations
const iterations = 1000000;

// Shallow copy — fastest for flat objects
let start = performance.now();
for (let i = 0; i < iterations; i++) {
  const copy = { ...obj };
}
console.log(`Spread: ${(performance.now() - start).toFixed(1)}ms`);

// JSON deep copy — slower, data loss risk
start = performance.now();
for (let i = 0; i < iterations; i++) {
  const copy = JSON.parse(JSON.stringify(obj));
}
console.log(`JSON: ${(performance.now() - start).toFixed(1)}ms`);

// structuredClone — moderate, accurate
start = performance.now();
for (let i = 0; i < iterations; i++) {
  const copy = structuredClone(obj);
}
console.log(`structuredClone: ${(performance.now() - start).toFixed(1)}ms`);

// Conclusion:
// - Flat object → spread {...obj} (fastest)
// - Nested with Date/Map → structuredClone
// - Complex with functions → lodash cloneDeep
```

## 🔬 So sánh với alternatives

| Phương án | Ưu điểm | Nhược điểm | Phù hợp khi |
|-----------|---------|------------|-------------|
| **Shallow `{...obj}`** | Nhanh nhất, simple syntax | Nested shared, not truly independent | Flat config objects, React state |
| **`Object.assign({}, obj)`** | Shallow copy, ES6, merge support | Same as spread | Merge multiple objects |
| **`JSON.parse/stringify`** | Deep copy, ubiquitous | Date→string, NaN→null, function lost | Simple data, no special types |
| **`structuredClone()`** | Deep, preserves Date/NaN/Map/Set | No functions/DOM, needs modern browser | Modern apps, complex nested data |
| **Lodash `cloneDeep`** | Most robust, handles functions | Extra dependency | Legacy projects, complex objects |

## 📊 Performance & Best Practices

- **Object phẳng (1 tầng)** → `{...obj}` hoặc `Object.assign({}, obj)` — fastest, simplest.
- **Nested object chứa Date/NaN/Map/Set** → `structuredClone()` — accurate deep copy.
- **JSON-safe data only** → `JSON.parse(JSON.stringify(obj))` — simple deep copy fallback.
- **Project có lodash** → `_.cloneDeep(obj)` — most robust, handles edge cases.
- **React state** → always immutable: `{...state, updatedKey}` or spread copy before modify.
- **Large deeply nested** → consider **structural sharing** (Immer.js) instead of full deep clone.
- **Avoid circular refs** in plain data — `structuredClone` handles them but indicates design issue.
- **Performance profiling** → clone in hot loops = expensive; cache and reuse where possible.

## 🔗 Liên kết chéo

- Xem thêm: `02_data-types/02_objects-and-prototype/01_object-basics/` — object literal, constructor
- Xem thêm: `02_data-types/01_primitive-types/03_value-vs-reference/` — value vs reference foundation
- Xem thêm: `03_data-structures/01_arrays/` — array copy: `[...arr]` vs `structuredClone`
- Xem thêm: `20_modern-javascript/02_destructuring-spread-rest/` — spread syntax chi tiết
- Tài liệu: [MDN — structuredClone](https://developer.mozilla.org/en-US/docs/Web/API/structuredClone), [MDN — Object.assign](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/assign)
