# Arrays — Mảng Trong JavaScript

> Arrays là cấu trúc dữ liệu phổ biến nhất: danh sách có thứ tự, truy cập bằng số nguyên index.

## 🔑 Khái niệm cốt lõi

Array trong JavaScript là **dynamic, sparse, ordered collection** — có thể chứa bất kỳ type nào, grow/shrink tự động.

```js
const arr = [1, 'hello', true, null, { x: 1 }, [2, 3]];
arr[0];       // 1
arr.length;   // 6
```

### Array vs Arguments vs NodeList

| | Array | Arguments | NodeList |
|---|---|---|---|
| Type | Array | Object (array-like) | HTMLCollection |
| Methods | map/filter/reduce | Chỉ length/concat | Chỉ forEach (modern) |
| Spread | [...arr] | [...args] | [...nodes] |
| length | property | property | property |
| Index access | arr[0] | arguments[0] | nodes[0] |

### Array vs TypedArray

| | Array | TypedArray |
|---|---|---|
| Element type | Any | Fixed numeric type |
| Memory | Flexible | Contiguous, efficient |
| Use case | General purpose | Binary data, WebGL |
| Overhead | Higher | Lower (~8x less) |

## ✅ Điểm mạnh

- **Rich API:** 30+ built-in methods (map, filter, reduce, sort, find...)
- **Dynamic:** push/pop/unshift/shift tự động điều chỉnh length
- **Sparse:** index không liên tục vẫn hoạt động (hole = undefined)
- **Iterable:** for...of, spread, destructuring đều hoạt động
- **Memory:** contiguous block (native optimization)
- **Chainable:** `[...].map(...).filter(...).reduce(...)`

## ⚠️ Bẫy thường gặp

### Bẫy 1: mutating method trả về mới
```js
const arr = [3, 1, 2];
arr.sort();            // [1, 2, 3] — MUTATES original!
const sorted = arr.slice().sort(); // clone trước khi sort
arr.reverse();         // also mutates!
const reversed = [...arr].reverse();
```

### Bẫy 2: splice trả về phần tử bị xóa
```js
const arr = ['a', 'b', 'c', 'd'];
const removed = arr.splice(1, 2);
// removed = ['b', 'c'], arr = ['a', 'd']
```

### Bẫy 3: forEach không thể break
```js
[1, 2, 3, 4].forEach(x => {
  if (x === 3) return; // continue, không break!
});
// Dùng for...of hoặc findIndex thay thế
for (const x of [1, 2, 3, 4]) {
  if (x === 3) break;
}
```

### Bẫy 4: sparse array với delete
```js
const arr = [1, 2, 3];
delete arr[1];        // [1, empty, 3]
arr.length;           // 3 — length KHÔNG giảm
arr[1];               // undefined (hole, không phải explicitly set)
arr.forEach((v, i) => console.log(i, v)); // 0:1, 1:undefined(skips hole), 2:3
// Dùng undefined thay delete
arr[1] = undefined;   // [1, undefined, 3] — forEach vẫn gọi index 1
```

### Bẫy 5: map create holes
```js
const arr = [1, 2, 3];
const result = arr.map((v, i) => i === 1 ? undefined : v * 2);
// [2, undefined, 6] — có element tại index 1
const holey = arr.map((v, i) => i === 1 ? undefined : v * 2);
holey[1]; // undefined — nhưng vẫn là element, không phải hole
```

## 💡 Khi nào dùng Array

- Danh sách có thứ tự, truy cập index
- Dữ liệu dạng table/grid
- Cần transform pipeline (map → filter → reduce)
- Stack/queue operations (push/pop/unshift/shift)
- Dữ liệu small-to-medium (< 10K items)

## 🎯 Ví dụ

### Transform pipeline
```js
const users = [{name: 'A', age: 25}, {name: 'B', age: 30}, {name: 'C', age: 22}];
const names = users
  .filter(u => u.age >= 25)
  .map(u => u.name.toUpperCase())
  .sort();
// ['A', 'B']
```

### Stack/Queue pattern
```js
// Stack (LIFO)
const stack = [];
stack.push(1); stack.push(2);
stack.pop(); // 2

// Queue (FIFO)
const queue = [];
queue.push(1); queue.push(2);
queue.shift(); // 1

// Deque (double-ended)
const deque = [];
deque.push(3);      // right
deque.unshift(1);   // left
deque.pop();        // 3 (right)
deque.shift();      // 1 (left)
```

### Flat map
```js
const matrix = [[1, 2], [3, 4], [5, 6]];
const flat = matrix.flat();           // [1,2,3,4,5,6]
const flatDeep = [[[1],[2]],[[3],[4]]].flat(2); // [1,2,3,4]
constflatMap = matrix.flatMap(row => row.map(x => x * 2)); // [2,4,6,8,10,12]
```

## 🔬 Performance

| Operation | Array | Map | Set |
|---|---|---|---|
| Insert at end | O(1) amortized | O(1) | O(1) |
| Lookup by index/key | O(1) | O(1) | O(1) |
| Lookup by value | O(n) | O(n)* | O(n) |
| Delete by key/index | O(n) | O(1) | O(1) |
| Memory overhead | Low | ~2x | ~1.5x |
| Iteration speed | Fast | Medium | Fast |

*Map lookup is O(1) average with hash table.

## 📊 Best Practices

1. **Default:** dùng Array cho danh sách có thứ tự
2. **Avoid sparse arrays:** dùng `undefined` thay `delete`
3. **Prefer immutable ops:** `slice`, `concat`, spread thay vì mutate
4. **Use findIndex** thay forEach khi cần break
5. **Clone trước mutate:** `[...arr].sort()` thay vì `arr.sort()`
6. **TypedArray** cho binary/large numeric data

## 🔗 Liên kết chéo
- Xem: `03_data-structures/01_arrays/01_array-basics` (methods chi tiết)
- Xem: `05_loops-and-iterations/01_loops` (for...of với array)
- Xem: `03_data-structures/02_keyed-collections` (Map/Set alternatives)
