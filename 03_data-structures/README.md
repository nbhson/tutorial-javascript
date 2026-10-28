# Data Structures — Cấu Trúc Dữ Liệu Trong JavaScript

> **roadmap.sh:** Arrays, Keyed Collections (Map/WeakMap/Set/WeakSet), Typed Arrays, JSON

## 🔑 Khái niệm cốt lõi

JavaScript có 4 nhóm cấu trúc dữ liệu chính, mỗi nhóm giải quyết bài toán khác nhau:

| Nhóm | Cấu trúc | Mục đích |
|---|---|---|
| **Array** | Array | Danh sách có thứ tự, truy cập index |
| **Keyed Collection** | Map, Set, WeakMap, WeakSet | Key-value với any key type, unique values |
| **Typed Array** | ArrayBuffer, Uint8Array, DataView | Binary data, xử lý byte-level |
| **Structured Data** | JSON | Serialization/deserialization |

### Array vs Map — Sự khác biệt quan trọng

| Tiêu chí | Array | Map |
|---|---|---|
| Key type | Number (index) | Any (string, object, symbol) |
| Order | Giữ thứ tự insertion | Giữ thứ tự insertion |
| Size | .length (property) | .size (property) |
| Iteration | for...of, forEach | for...of, forEach |
| Performance lookup | O(1) by index | O(1) average by key |
| Memory overhead | Thấp | Cao hơn (~2x) |

## 📐 Khi nào dùng cấu trúc nào

| Tình huống | Cấu trúc | Lý do |
|---|---|---|
| Danh sách có thứ tự, index truy cập | Array | Native, optimized |
| Lookup theo key phức tạp (object) | Map | Any key type |
| Unique values collection | Set | O(1) has(), auto-dedup |
| Cache với object key, thin memory | WeakMap | GC-friendly |
| Metadata attach to DOM nodes | WeakMap | Không leak memory |
| Binary data (image, audio) | TypedArray | Efficient memory layout |
| Exchange data giữa systems | JSON | Universal format |

## ✅ Điểm mạnh

| Cấu trúc | Ưu điểm chính |
|---|---|
| Array | Fast index access, rich API (map/filter/reduce) |
| Map | Any key type, preserves insertion order, O(1) get/set |
| Set | Fast membership test, automatic deduplication |
| WeakMap | Keys are weakly referenced — no memory leaks |
| TypedArray | Binary data manipulation, WebGL, crypto |
| JSON | Human-readable, universal, language-agnostic |

## ⚠️ Bẫy thường gặp

### Bẫy 1: Array không phải Map
```js
const arr = [];
arr['name'] = 'test';  // thêm property, KHÔNG phải element
arr.length;            // 0 — không tính property
Array.isArray(arr);    // true — vẫn là array
```

### Bẫy 2: Map vs Object key type
```js
const obj = {};
obj[1] = 'one';   // key là string "1"
obj[true] = 'yes'; // key là string "true"
// 1 === '1' → false, nhưng obj[1] === obj['1'] → true

const map = new Map();
map.set(1, 'one');
map.set('1', 'string-one');
map.get(1);      // 'one'
map.get('1');    // 'string-one' ← phân biệt được!
```

### Bẫy 3: WeakMap key phải là object
```js
const wm = new WeakMap();
wm.set('string', 'value'); // TypeError
wm.set(123, 'value');      // TypeError
wm.set(null, 'value');     // TypeError
// ONLY objects: {}, [], class instances, functions
```

### Bẫy 4: JSON không serialize được
```js
JSON.stringify(new Date());      // "2024-01-01T00:00:00.000Z"
JSON.stringify(/regex/);         // undefined (bỏ qua)
JSON.stringify(() => {});        // undefined
JSON.stringify(new Map());       // {} (mất data)
JSON.stringify(new Set([1,2]));  // []
```

## 💡 Khi nào dùng

### Array — khi cần:
- Danh sách có thứ tự, truy cập bằng index
- Dữ liệu dạng list/table
- Cần các methods: map, filter, reduce, sort

### Map — khi cần:
- Key là object/symbol (không phải string/number)
- Cần preserve insertion order + frequent get/set
- Counter/tally với object key
- Memoization cache

### Set — khi cần:
- Loại bỏ duplicate values
- Kiểm tra membership nhanh (O(1))
- Intersection/union/difference giữa collections

### WeakMap — khi cần:
- Attach metadata vào object mà không gây memory leak
- Private fields simulation
- Cache với object key, cho phép GC thu hồi

### TypedArray — khi cần:
- Xử lý binary data (ảnh, audio, websockets)
- Giao tiếp với WebGL/WebGPU
- Cryptographic operations
- Memory-efficient numeric arrays

### JSON — khi cần:
- Send/receive data qua network (API)
- Store configuration
- Log/debug data representation
- Exchange giữa languages

## 🎯 Ví dụ minh họa

### Array — basic operations
```js
const fruits = ['apple', 'banana', 'cherry'];
fruits.push('date');           // thêm cuối
fruits.unshift('apricot');     // thêm đầu
fruits.splice(1, 1);           // xóa 'banana'
const slice = fruits.slice(0, 2); // clone phần tử
const found = fruits.indexOf('cherry'); // tìm index
```

### Map — với object keys
```js
const userScores = new Map();
userScores.set({ id: 1, name: 'Alice' }, 95);
userScores.set({ id: 2, name: 'Bob' }, 87);

const alice = { id: 1, name: 'Alice' };
userScores.get(alice); // 95
```

### Set — deduplication
```js
const raw = [1, 2, 2, 3, 3, 3, 4];
const unique = [...new Set(raw)]; // [1, 2, 3, 4]

const a = new Set([1, 2, 3, 4]);
const b = new Set([3, 4, 5, 6]);
const intersect = new Set([...a].filter(x => b.has(x))); // {3, 4}
```

### TypedArray — binary ops
```js
const buf = new ArrayBuffer(16);
const view = new DataView(buf);
view.setInt32(0, 42, true);
view.setFloat32(4, 3.14);
console.log(view.getInt32(0)); // 42
```

### JSON — serialization
```js
const data = { name: 'A', scores: [90, 85, 92] };
const json = JSON.stringify(data, null, 2);
const parsed = JSON.parse(json);
```

## 🔬 Performance Comparison

| Operation | Array | Map | Set | Object |
|---|---|---|---|---|
| Insert at end | O(1) | O(1) | O(1) | O(1) |
| Lookup by index/key | O(1) | O(1) | O(1) | O(1) |
| Lookup by value | O(n) | O(n)* | O(n) | O(n) |
| Delete by key | O(n) | O(1) | O(1) | O(1) |
| Memory overhead | Low | ~2x | ~1.5x | Low |

*Map lookup O(1) average with hash table, worst case O(n) with collisions.

## 📊 Best Practices

1. **Default:** dùng Array cho danh sách có thứ tự
2. **Object key:** dùng Map thay Object cho frequent get/set
3. **Dedup:** dùng Set, không filter/splice thủ công
4. **Private data:** dùng WeakMap, không property trực tiếp
5. **Binary:** dùng TypedArray, không ArrayBuffer raw
6. **API exchange:** JSON.stringify + JSON.parse, handle edges

## 🔗 Liên kết chéo
- Xem thêm: `03_data-structures/01_arrays` (Array chi tiết)
- Xem thêm: `03_data-structures/02_keyed-collections` (Map/Set/WeakMap/WeakSet)
- Xem thêm: `03_data-structures/03_typed-arrays` (Binary data)
- Xem thêm: `03_data-structures/04_json` (Serialization)

## 🆕 ES2025+ — Grouping & Set Methods

### Object.groupBy() / Map.groupBy() — nhóm dữ liệu một dòng

**Browser support:** Chrome 117+, Firefox 119+, Safari 17.4+, Node 21+ (ES2024).

```js
const inventory = [
  { name: 'asparagus', type: 'veg', qty: 5 },
  { name: 'bananas',   type: 'fruit', qty: 0 },
  { name: 'goat',      type: 'meat', qty: 23 },
];

// ❌ Trước: reduce thủ công
const old = inventory.reduce((acc, item) => {
  (acc[item.type] ??= []).push(item);
  return acc;
}, {});

// ✅ Object.groupBy — key bị coerce thành string
const byType = Object.groupBy(inventory, ({ type }) => type);
// { veg: [...], fruit: [...], meat: [...] }

// ✅ Map.groupBy — key giữ nguyên kiểu (object, number, NaN...)
const byQty = Map.groupBy(inventory, ({ qty }) => (qty > 0 ? 'inStock' : 'soldOut'));
console.log(byQty.get('inStock')); // các item còn hàng
```

> 📖 MDN: [Object.groupBy()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/groupBy) · [Map.groupBy()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map/groupBy)

### Set Methods — phép toán tập hợp native

**Browser support:** Chrome 122+, Firefox 127+, Safari 17+, Node 22+ (Baseline 2024).

```js
const a = new Set([1, 2, 3, 4]);
const b = new Set([3, 4, 5, 6]);

// ❌ Trước: viết tay
const intersectOld = new Set([...a].filter(x => b.has(x))); // {3, 4}

// ✅ ES2025: 7 method chuẩn toán học trên Set.prototype
console.log(a.union(b));                  // Set {1, 2, 3, 4, 5, 6}  (A ∪ B)
console.log(a.intersection(b));           // Set {3, 4}              (A ∩ B)
console.log(a.difference(b));             // Set {1, 2}              (A \ B)
console.log(a.symmetricDifference(b));    // Set {1, 2, 5, 6}        (A △ B)
console.log(a.isSubsetOf(b));             // false                   (A ⊆ B?)
console.log(a.isSupersetOf(b));           // false                   (A ⊇ B)
console.log(a.isDisjointFrom(new Set([9, 10]))); // true             (rời nhau)
```

| Method | Trả về | Dùng khi |
|---|---|---|
| `union()` | Set mới | Gộp 2 tập, loại trùng |
| `intersection()` | Set mới | Tìm phần chung |
| `difference()` | Set mới | Loại phần thuộc set khác |
| `symmetricDifference()` | Set mới | Phần tử chỉ thuộc 1 trong 2 tập |
| `isSubsetOf()` / `isSupersetOf()` | boolean | Kiểm tra quan hệ bao hàm |
| `isDisjointFrom()` | boolean | Kiểm tra 2 tập không giao nhau |

> 📖 MDN: [Set](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set) · [union()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set/union) · [intersection()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set/intersection) · [difference()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set/difference)
>
> Tổng hợp đầy đủ: `22_es2025-features/README.md`
