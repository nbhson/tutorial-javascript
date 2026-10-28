# Set — Tập Hợp Giá Trị Duy Nhất

> Set: collection các giá trị duy nhất, không lặp. O(1) has(), tự động dedupe.

## Khái niệm cốt lõi

```js
const set = new Set([1, 2, 2, 3]);
set.size; // 3
set.add(4);
set.has(2); // true
set.delete(2);
[...set]; // [1, 3, 4]
```

Set trả lời đúng một câu hỏi: **"giá trị này đã xuất hiện chưa?"** — với chi phí O(1) thay vì O(n) như `Array.includes()`. Với mảng vài nghìn phần tử được kiểm tra membership liên tục, Set có thể nhanh hơn hàng chục lần.

### SameValueZero comparison rules

- `NaN` trong Set: chỉ 1 lần (SameValueZero coi NaN bằng NaN)
- `-0` và `+0`: cùng 1 entry (SameValueZero: -0 === +0)
- Object: so sánh reference, không structural equality
- Primitive: so sánh value + type

```js
const s = new Set();
s.add(NaN);
s.add(NaN);
s.size; // 1 — NaN "bằng" NaN trong Set (khác với ===!)

s.add(-0);
s.add(+0);
s.size; // vẫn 1 — -0 và +0 trùng nhau trong SameValueZero

s.add({ id: 1 });
s.add({ id: 1 });
s.size; // 3 — 2 object khác reference = 2 entry
```

### Set API

| Method | Trả về | Mô tả |
|---|---|---|
| `add(value)` | Set (chainable) | Thêm value |
| `delete(value)` | boolean | Xóa, return true nếu tồn tại |
| `has(value)` | boolean | Kiểm tra membership |
| `clear()` | — | Xóa tất cả |
| `size` | number | Số elements |
| `values()` | Iterator | Giá trị theo insertion order |
| `entries()` | Iterator | [value, value] pairs |
| `forEach(cb)` | — | Callback(value, value, set) |

### Thứ tự lặp

Set duyệt theo **thứ tự chèn** (insertion order) — được đặc tả, không phải chi tiết cài đặt. Element bị xóa rồi thêm lại sẽ đứng cuối. Vì Set không có index, "thứ tự" là thứ tự duy nhất bạn có thể dựa vào.

```js
const s = new Set(["b", "a", "c"]);
s.delete("b");
s.add("b");
[...s]; // ["a", "c", "b"] — "b" xuống cuối vì re-add
```

## Điểm mạnh

- Auto-deduplication — không cần manual filter
- O(1) has() lookup — nhanh hơn Array.indexOf O(n)
- Iteration theo insertion order
- Set operations: union, intersection, difference
- Memory efficient cho large unique datasets

## Bẫy thường gặp

- Object keys so sánh reference, không value
- Không sort được trực tiếp — cần `[...set].sort()`
- Set không có index access
- Thêm object cùng structure nhưng khác reference -> 2 entries
- `new Set(2)` — TypeError; constructor chỉ nhận iterable (dùng `new Set([2])`)
- Set không có method "lấy phần tử bất kỳ" — luôn phải spread ra array nếu cần index

```js
// ❌ Bẫy so sánh theo reference
new Set([{ id: 1 }]).has({ id: 1 }); // false!

// ✅ Kiểm tra theo giá trị: dùng key primitive
new Set(["1"]).has("1"); // true
// hoặc map sang key primitive trước
const byId = new Set(users.map((u) => u.id));
byId.has(1); // true
```

## Khi nào dùng

- Deduplicate array nhanh gọn
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

// Graph BFS với Set visited
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

## Ví dụ 2: So sánh hiệu năng has() — Set vs Array

```js
const n = 100_000;
const arr = Array.from({ length: n }, (_, i) => i);
const set = new Set(arr);
const target = n - 1;

console.time("array includes");
arr.includes(target); // O(n) — duyệt gần hết mảng
console.timeEnd("array includes");

console.time("set has");
set.has(target); // O(1) — hash lookup
console.timeEnd("set has");
// Trên máy phổ thông: array ~vài ms, set ~vài microsecond (hàng trăm lần nhanh hơn)
```

Quy tắc thực chiến: nếu membership test nằm trong vòng lặp (kể cả nested loop nhỏ), chuyển sang Set. `includes()` chỉ phù hợp test một lần trên mảng nhỏ.

## Ví dụ 3: Set algebra — ES2024 built-in methods

Từ 2024, các phép toán tập hợp có sẵn (Chrome 122+, Firefox 127+, Safari 17+ — Baseline 2024), thay cho pattern spread/filter:

```js
const frontend = new Set(["HTML", "CSS", "JS", "React"]);
const backend = new Set(["JS", "Node", "React", "SQL"]);

frontend.union(backend);                  // Set {"HTML","CSS","JS","Node","React","SQL"}
frontend.intersection(backend);           // Set {"React"}
frontend.difference(backend);             // Set {"HTML","CSS"}
frontend.symmetricDifference(backend);    // Set {"HTML","CSS","JS","Node","SQL"}
frontend.isSubsetOf(backend);             // false
frontend.isDisjointFrom(backend);         // false

// Fallback cho môi trường cũ:
const unionFallback = new Set([...frontend, ...backend]);
```

Lợi ích so với spread/filter: gọn hơn, ý đồ rõ ràng hơn, và các method nhận bất kỳ iterable nào chứ không chỉ Set.

## Ví dụ 4: Real-world use cases

```js
// 1. Tìm phần tử chung giữa 2 danh sách (khách hàng mua cả 2 sản phẩm)
const buyersA = new Set(orderA.map((o) => o.userId));
const both = [...buyersA].filter((id) => buyerBSet.has(id));

// 2. Theo dõi các tab/category user đã xem (tránh đẩy lại gợi ý)
const viewedIds = new Set();
productList.forEach((p) => {
  if (!viewedIds.has(p.id)) {
    showNew(p);
    viewedIds.add(p.id);
  }
});

// 3. Kiểm tra quyền nhanh — O(1) thay vì includes O(n)
const adminPermissions = new Set(["read", "write", "delete", "manage"]);
function can(user, action) {
  return adminPermissions.has(action);
}

// 4. So sánh 2 mảng có cùng phần tử (không quan tâm thứ tự/lặp)
function sameContents(x, y) {
  return x.length === y.length && new Set(x).size === new Set(y).size
    && [...new Set(x)].every((v) => y.includes(v));
}
```

## Ví dụ 5: Chuyển đổi Set ↔ các cấu trúc khác

```js
// Set → Array
const arr = [...set];
const arr2 = Array.from(set);

// Array → Set
const set2 = new Set(arr);

// Set → JSON: phải qua array
const json = JSON.stringify([...set]);

// Dedupe object theo key — pattern phổ biến
const users = [{ id: 1, name: "A" }, { id: 1, name: "A2" }, { id: 2, name: "B" }];
const seen = new Set();
const uniqueUsers = users.filter((u) => {
  if (seen.has(u.id)) return false; // key primitive (id) — so sánh đúng
  seen.add(u.id);
  return true;
}); // [{ id: 1, name: "A" }, { id: 2, name: "B" }]
```

## Set vs Array — khi nào cái nào?

| Nhu cầu | Chọn |
|---|---|
| Danh sách có thứ tự, truy cập theo index | Array |
| Kiểm tra tồn tại lặp lại nhiều lần | Set |
| Loại bỏ trùng lặp | Set (1 dòng) |
| Cần `.map`, `.filter`, `.reduce` trực tiếp | Array (Set phải spread trước) |
| Đếm số phần tử duy nhất | Set `.size` |
| Stack/queue, thứ tự xử lý | Array (`push`/`shift`) |

## Checklist tự kiểm tra

- [ ] Biết Set so sánh bằng SameValueZero (NaN bằng NaN, -0 trùng +0)
- [ ] Hiểu object trong Set so sánh theo reference
- [ ] Viết được dedupe array 1 dòng và dedupe object theo key
- [ ] Biết các method set algebra của ES2024 (union, intersection, difference...)
- [ ] Biết khi nào has() của Set nhanh hơn hẳn includes() của Array

## Liên kết chéo

- Xem: `03_data-structures/02_keyed-collections/01_map` (Map key uniqueness)
- Xem: `04_equality-comparisons/03_samevaluezero` (SameValueZero algorithm)
- Xem: `03_data-structures/02_keyed-collections/04_weakset` (WeakSet)
- Xem: `03_data-structures/02_keyed-collections/02_weakmap` (họ weak collection)
- Tài liệu: [MDN — Set](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set)
