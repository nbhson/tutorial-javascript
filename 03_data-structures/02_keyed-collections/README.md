# Keyed Collections — Map, Set, WeakMap, WeakSet

> Bộ 4 cấu trúc key-value/unique-value trong JS: Map, WeakMap, Set, WeakSet

## Khái niệm cốt lõi

| Collection | Key Type | Duplicate | Weak refs | Iterate | Size |
|---|---|---|---|---|---|
| **Map** | Any | Unique keys | No | keys/values/entries | .size |
| **WeakMap** | Object only | Unique keys | Yes (GC-friendly) | No | No .size |
| **Set** | Any | Unique values | No | values/entries | .size |
| **WeakSet** | Object only | Unique values | Yes (GC-friendly) | No | No .size |

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

## Điểm mạnh

- Map: any key type, fast get/set, size tracking
- Set: O(1) membership test, auto-dedup
- WeakMap/WeakSet: no memory leaks, attach metadata safely
- All preserve insertion order

## Bẫy thường gặp

- Map key object reference, không structural equality
- Set.add returns the Set (chainable)
- WeakMap keys cannot be iterated — chỉ qua known references
- Set so sánh NaN bằng SameValue (NaN === NaN trong Set context)

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

## Liên kết chéo

- Xem: `02_data-types/02_objects-and-prototype` (prototype)
- Xem: `04_equality-comparisons/03_samevaluezero` (Map key algorithm)
- Xem: `17_memory-management/01_memory-lifecycle-gc` (GC principles)
