# Keyed Collections — Map, Set, WeakMap, WeakSet

> Bộ 4 cấu trúc key-value/unique-value trong JS: Map, WeakMap, Set, WeakSet

## Khái niệm cốt lõi

| Collection | Key Type | Duplicate | Weak refs | Iterate | Size |
|---|---|---|---|---|---|
| **Map** | Any | Unique keys | No | keys/values/entries | .size |
| **WeakMap** | Object only | Unique keys | Yes (GC-friendly) | No | No .size |
| **Set** | Any | Unique values | No | values/entries | .size |
| **WeakSet** | Object only | Unique values | Yes (GC-friendly) | No | No .size |

Bộ tứ này chia làm 2 cặp: **Map/WeakMap** (key → value) và **Set/WeakSet** (giá trị duy nhất). Tiền tố "Weak" nghĩa là *không giữ chặt* key/value — khi không còn ai tham chiếu nữa, garbage collector (GC) tự dọn entry. Đổi lại, Weak không iterate được và không có `.size`.

### Map vs Object — Sự khác biệt quan trọng

| | Object | Map |
|---|---|---|
| Key type | String/Symbol only | Any (object, number, etc.) |
| Order | insertion (ES2015+) | insertion guaranteed |
| Size | Manual (.length not avail) | .size property |
| Performance | O(1) avg | O(1) avg (optimized) |
| Iteration | Object.keys/entries | for...of directly |
| Enumerable | Yes (affects for..in) | No (invisible to for..in) |
| Default keys | inherits from Object.prototype | None |

Chi tiết về thứ tự key đáng nhớ: với **Object**, các key dạng số nguyên (integer-like) được sắp xếp tăng dần trước, sau đó mới đến key string theo thứ tự chèn. Với **Map**, mọi key (kể cả số) đều giữ đúng thứ tự chèn. Nếu code của bạn phụ thuộc thứ tự lặp, Map an toàn hơn.

```js
const obj = { 10: "a", 2: "b", 1: "c" };
Object.keys(obj);          // ["1", "2", "10"] — integer-like keys được sort!

const map = new Map([[10, "a"], [2, "b"], [1, "c"]]);
[...map.keys()];           // [10, 2, 1] — giữ đúng thứ tự chèn
```

### So sánh thuật toán so sánh key

- **Object**: key bị ép thành string, so sánh string.
- **Map/Set**: dùng **SameValueZero** — gần giống `===` nhưng `NaN` bằng `NaN` và `-0` trùng `+0`. Chi tiết thuật toán xem `04_equality-comparisons/03_samevaluezero`.

## Điểm mạnh

- Map: any key type, fast get/set, size tracking
- Set: O(1) membership test, auto-dedup
- WeakMap/WeakSet: no memory leaks, attach metadata safely
- All preserve insertion order

## Bẫy thường gặp

- Map key object reference, không structural equality
- Set.add returns the Set (chainable)
- WeakMap keys cannot be iterated — chỉ qua known references
- Set so sánh NaN bằng SameValue (NaN === NaN trong Set context — 2 lần add NaN chỉ ra 1 entry)
- Dùng Map khi Object đủ → thừa overhead; dùng Object khi key cần là object → bug âm thầm

## Memory leak kinh điển — lý do WeakMap tồn tại

```js
// ❌ LEAK: Map giữ strong reference tới DOM node
const cache = new Map();
function attach(el) {
  cache.set(el, { lastClick: Date.now() });
}
document.querySelectorAll(".btn").forEach(attach);
// User điều hướng SPA: các node bị remove khỏi DOM,
// NHƯNG Map vẫn giữ reference → GC không thể thu hồi → memory tăng mãi.

// ✅ WeakMap: node bị remove + không còn biến nào tham chiếu → entry tự biến mất
const cache2 = new WeakMap();
function attach2(el) {
  cache2.set(el, { lastClick: Date.now() });
}
// Không cần hàm cleanup — GC tự lo.
```

Cách kiểm chứng: mở DevTools → tab Memory → chụp heap snapshot trước/sau khi remove node. Với Map bạn sẽ thấy array của node còn trong heap; với WeakMap thì không.

## Khi nào dùng

- Map: cache, counter, config with object keys
- Set: dedup array, membership testing
- WeakMap: private data, DOM node metadata
- WeakSet: track visited objects (cycle detection)

## Ví dụ

```js
// Map
const m = new Map([[1, 'one'], [2, 'two']]);
m.set({id: 1}, 'object-key'); // object key works!
m.get(1); // 'one'

// Set
const s = new Set([1, 2, 2, 3]); // Set {1, 2, 3}
s.has(2); // true
s.add(4); // returns Set, chainable

// WeakMap
const wm = new WeakMap();
const obj = {};
wm.set(obj, 'data');
// obj bị GC -> wm entry tự động remove

// Set operations
const a = new Set([1, 2, 3]);
const b = new Set([2, 3, 4]);
const union = new Set([...a, ...b]);           // {1,2,3,4}
const intersect = new Set([...a].filter(x => b.has(x))); // {2,3}
const diff = new Set([...a].filter(x => !b.has(x)));     // {1}
```

### ES2024 — Set có sẵn các phép toán tập hợp

Từ 2024, Set có method built-in (Chrome 122+, Firefox 127+, Safari 17+), không cần spread/filter nữa:

```js
const a = new Set([1, 2, 3]);
const b = new Set([2, 3, 4]);

a.union(b);                 // Set {1,2,3,4}
a.intersection(b);          // Set {2,3}
a.difference(b);            // Set {1}
a.symmetricDifference(b);   // Set {1,4}
a.isSubsetOf(b);            // false
a.isDisjointFrom(b);        // false
```

## WeakRef & FinalizationRegistry — phần mở rộng của "weak" family

WeakMap/WeakSet không phải thứ duy nhất làm việc với weak reference. ES2021 bổ sung thêm 2 API cùng "họ" (xem chi tiết: `js-info/vi/14_misc/weakref-finalizationregistry/` trong mirror javascript.info):

```js
// WeakRef — giữ tham chiếu YẾU tới object, không chặn GC
let target = { heavy: new Array(1_000_000).fill("data") };
const ref = new WeakRef(target);
ref.deref();          // object (còn sống)
// ... target = null; GC chạy ...
ref.deref();          // undefined — object đã bị thu hồi

// FinalizationRegistry — nhận callback khi object bị GC
const registry = new FinalizationRegistry((heldValue) => {
  console.log(`Object ${heldValue} đã bị GC thu hồi`);
});
registry.register(target, "my-resource");
```

⚠️ **Cảnh báo quan trọng** khi dùng:

- GC timing không đoán được — callback có thể chạy rất muộn hoặc **không bao giờ chạy**. Không dùng cho logic nghiệp vụ (giải phóng DB connection, file handle...) mà phải cleanup thủ công.
- Lý do chính đáng để dùng WeakRef: cache lớn có thể tự tái tạo (memoize kết quả tính nặng, image cache), nơi việc mất cache chỉ tốn hiệu năng chứ không sai logic.
- FinalizationRegistry chủ yếu dùng cho **cleanup phụ** như xóa cache entry ngoại vi, log thống kê — không phải cơ chế dọn tài nguyên chính.

Với 99% nhu cầu gắn dữ liệu vào object/DOM node, **WeakMap là lựa chọn đúng** — đừng vội dùng WeakRef.

## Chọn cấu trúc nào? Cây quyết định

```
Cần ánh xạ key → value?
├── Key là string/symbol, cấu trúc tĩnh        → Object
└── Key động, object, cần thứ tự/size          → Map
    └── Key là object, KHÔNG muốn giữ node sống → WeakMap

Cần tập giá trị duy nhất?
├── Cần đếm/duyệt/serialize                    → Set
└── Chỉ cần "đã xử lý object chưa", tránh leak → WeakSet
```

## Trường hợp nào dùng Map KHI Object đủ

Rất nhiều người đặt `new Map()` cho mọi thứ — đây là sự thận trọng thái quá. Dùng Object khi:

- Key luôn là string hoặc Symbol
- Cấu trúc cố định (không thêm/bớt key động theo logic)
- Cần serialize qua `JSON.stringify` (Object serialize thành JSON tự nhiên, Map thì không)
- Key không cần thứ tự lặp đặc biệt (hoặc bạn không duyệt theo thứ tự)

Dùng Map khi thật sự cần: key là object, size động, duyệt theo thứ tự chèn.

## Bài trong nhóm

- `01_map/` — Map chi tiết (so sánh với Object, iteration, cache pattern)
- `02_weakmap/` — WeakMap chi tiết (private data, metadata, memory leak)
- `03_set/` — Set chi tiết (dedup, SameValueZero, set algebra, BFS)
- `04_weakset/` — WeakSet chi tiết (cycle detection, tracking không rò rỉ)

## Liên kết chéo

- Xem: `04_equality-comparisons/03_samevaluezero` (Map key algorithm)
- Xem: `17_memory-management/01_memory-lifecycle-gc` (GC principles)
- Xem: `04_equality-comparisons/02_object-is` (SameValue — nền của SameValueZero)
- js-info (mirror tiếng Việt): `js-info/vi/05_data-types/` — chương map-set, weakmap-weakset
