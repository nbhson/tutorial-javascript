# Set — Tap Hop Gia Tri Duy Nhat

> Set: collection cac gia tri duy nhat, khong lap. O(1) has(), tu dong dedupe.

## Khái niệm cốt lõi

```js
const set = new Set([1, 2, 2, 3]);
set.size; // 3
set.add(4);
set.has(2); // true
set.delete(2);
[...set]; // [1, 3, 4]
```

### SameValueZero comparison rules

- `NaN` trong Set: chi 1 lan (SameValueZero coi NaN bang NaN)
- `-0` va `+0`: cung 1 entry (SameValueZero: -0 === +0)
- Object: so sanh reference, khong structural equality
- Primitive: so sanh value + type

### Set API

| Method | Tra ve | Mo ta |
|---|---|---|
| `add(value)` | Set (chainable) | Them value |
| `delete(value)` | boolean | Xoa, return true neu ton tai |
| `has(value)` | boolean | Kiem tra membership |
| `clear()` | — | Xoa tat ca |
| `size` | number | So elements |
| `values()` | Iterator | Gia tri theo insertion order |
| `entries()` | Iterator | [value, value] pairs |
| `forEach(cb)` | — | Callback(value, value, set) |

## Điểm mạnh

- Auto-deduplication — khong can manual filter
- O(1) has() lookup — nhanh hon Array.indexOf O(n)
- Iteration theo insertion order
- Set operations: union, intersection, difference
- Memory efficient cho large unique datasets

## Bẫy thường gặp

- Object keys so sanh reference, khong value
- Khong sort duoc truc tiep — can [...set].sort()
- Set khong co index access
- Them object cung structure nhung khac reference -> 2 entries

## Khi nao dung

- Deduplicate array nhanh gon
- Track visited nodes (graph traversal BFS/DFS)
- Membership testing O(1)
- Unique tag/collection system
- Implement set algebra (union/intersection/diff)

## Ví dụ

```js
// Dedupe
const raw = [1, 2, 2, 3, 3, 3, 4];
const unique = [...new Set(raw)]; // [1, 2, 3, 4]

// Set operations
const a = new Set([1, 2, 3, 4]);
const b = new Set([2, 3, 4, 5]);
const union = new Set([...a, ...b]);              // {1,2,3,4,5}
const intersect = new Set([...a].filter(x => b.has(x))); // {2,3,4}
const diff = new Set([...a].filter(x => !b.has(x)));     // {1}

// Graph BFS voi Set visited
function bfs(graph, start) {
  const visited = new Set();
  const queue = [start];
  while (queue.length) {
    const node = queue.shift();
    if (visited.has(node)) continue;
    visited.add(node);
    queue.push(...(graph[node] || []));
  }
  return visited;
}

// Unique words in text
const text = "hello world hello JavaScript world";
const uniqueWords = [...new Set(text.split(' '))]; // ["hello","world","JavaScript"]
```

## Liên kết chéo

- Xem: `03_data-structures/02_keyed-collections/01_map` (Map key uniqueness)
- Xem: `04_equality-comparisons/03_samevaluezero` (SameValueZero algorithm)
- Xem: `03_data-structures/02_keyed-collections/04_weakset` (WeakSet)
