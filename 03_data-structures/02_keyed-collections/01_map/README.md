# Map — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

**`Map`** là cấu trúc dữ liệu **key-value** trong đó khóa có thể là **bất kỳ kiểu nào** — object, function, primitive, Symbol — không bị ép thành chuỗi như object thường. Map giữ **thứ tự chèn** và có property `size` dễ lấy.

### So sánh Map vs Object thông thường

| Đặc điểm | Object `{}` | `Map` |
|----------|------------|-------|
| Khóa | Chỉ string/Symbol | **Bất kỳ** (object, number, function...) |
| Thứ tự chèn | Không đảm bảo (trừ key number sorted) | **Giữ nguyên thứ tự chèn** |
| `size` | Phải đếm tay `Object.keys(obj).length` | `map.size` — built-in |
| Performace thêm/xóa key động | Tốt cho static structure | Tốt cho frequent add/remove |
| Iteration | `for...in`, `Object.keys()` | `for...of`, `map.forEach()` |
| Default prototype | Có (`Object.prototype`) | Không có prototype default |

### Cú pháp cơ bản

```js
const m = new Map();

// set(key, value) — thêm hoặc cập nhật
m.set("name", "Sơn");
m.set(42, "the answer");
m.set(true, "boolean");
m.set({ id: 1 }, "object key");
m.set(Symbol("id"), "symbol key");

// get(key) — truy xuất
console.log(m.get("name"));           // "Sơn"
console.log(m.get(42));               // "the answer"
console.log(m.get({ id: 1 }));        // undefined! — different object reference
console.log(m.get(Symbol("id")));     // undefined! — different symbol instance

// has(key) — kiểm tra tồn tại
console.log(m.has("name"));           // true

// delete(key) — xóa
m.delete(42);
console.log(m.has(42));               // false

// size — số lượng entries
console.log(m.size);                  // 4

// clear() — xóa tất cả
m.clear();
console.log(m.size);                  // 0
```

### ⚠️ Bẫy: Map khóa object so sánh theo THAM CHIẾU

```js
const key1 = { id: 1 };
const key2 = { id: 1 }; // Same content, DIFFERENT object reference

m.set(key1, "value1");
console.log(m.get(key1));   // "value1" ✓
console.log(m.get(key2));   // undefined ✗ — khác object reference!
```

### Iteration — 3 cách

```js
const m = new Map();
m.set("a", 1);
m.set("b", 2);

// 1. for...of trên entries
for (const [key, value] of m) {
  console.log(key, value); // "a" 1, "b" 2
}

// 2. forEach
m.forEach((value, key) => {
  console.log(key, value); // "a" 1, "b" 2
});

// 3. Explicit iterators
console.log([...m.keys()]);   // ["a", "b"]
console.log([...m.values()]); // [1, 2]
console.log([...m.entries()]); // [["a", 1], ["b", 2]]
```

### Convert Map ↔ Object

```js
// Map → Object
const obj = Object.fromEntries(m);

// Object → Map
const mapFromObj = new Map(Object.entries({ a: 1, b: 2 }));

// Map → JSON (với convert)
const json = JSON.stringify(Object.fromEntries(m));

// JSON → Map
const m2 = new Map(Object.entries(JSON.parse(json)));
```

## 📐 Cấu trúc nhóm

```
03_data-structures/02_keyed-collections/01_map/
├── README.md         ← bài này
└── app.js            ← demo Map usage
    └── index.html
```

## ✅ Điểm mạnh

- Khóa là object/function được phép — không bị ép thành chuỗi.
- Giữ thứ tự chèn và `size` dễ lấy hơn object.
- O(1) lookup — nhanh hơn `for...in` duyệt object.
- Không có prototype default — an toàn khỏi prototype pollution.
- Iterable protocol — `for...of`, spread, destructuring work naturally.

## ⚠️ Bẫy thường gặp

| # | Bẫy | Ví dụ | Cách tránh |
|---|-----|-------|-----------|
| 1 | **Khóa object so sánh theo reference** | `m.get({id:1})` sau `m.set({id:1}, v)` → undefined | Dùng cùng instance làm key |
| 2 | **Không JSON-serializable** | `JSON.stringify(new Map())` → `{}` | Dùng `Object.fromEntries(map)` |
| 3 | **Lạm dụng Map khi Object đủ** | Map overhead cao hơn object plain | Dùng Map chỉ khi cần object key hoặc size |
| 4 | **`forEach` không thể `break`** | Giống array forEach | Dùng `for...of` khi cần early exit |

## 💡 Khi nào dùng

- Liên kết khóa–giá trị phức tạp, thứ tự quan trọng, cần `size` → `Map`.
- Cache metadata kèm object mà muốn GC xử lý → `WeakMap`.
- Cần danh sách phần tử không trùng → `Set`.
- Đánh dấu "đã xử lý" cho object → `WeakSet`.

## 🎯 Ví dụ minh họa

### Ví dụ 1: Basic usage

```js
const m = new Map();
m.set("a", 1);
m.set({ id: 1 }, "obj");
console.log(m.get("a"), m.size); // 1 2
for (const [k, v] of m) console.log(k, v);
```

### Ví dụ 2: Frequency counter pattern

```js
function wordFrequency(text) {
  const freq = new Map();
  for (const word of text.toLowerCase().split(/\s+/)) {
    freq.set(word, (freq.get(word) || 0) + 1);
  }
  return freq;
}

const text = "the quick brown fox jumps over the lazy dog the";
const freq = wordFrequency(text);
console.log(freq.get("the"));  // 3
console.log(freq.get("fox"));  // 1
```

### Ví dụ 3: Iterator with early exit

```js
const scores = new Map([
  ["Alice", 85],
  ["Bob", 92],
  ["Carol", 78],
  ["Dave", 95],
]);

// forEach — không break được
scores.forEach((score, name) => {
  if (score < 80) console.log(`${name}: fail`);
  // không thể break!
});

// for...of — break được
for (const [name, score] of scores) {
  if (score >= 90) {
    console.log(`${name}: pass (first above 90)`);
    break;
  }
}
// Dave: pass (first above 90)
```

### Ví dụ 4: Real-world use — request cache

```js
const apiCache = new Map();

async function fetchWithCache(url) {
  if (apiCache.has(url)) {
    console.log(`Cache hit: ${url}`);
    return apiCache.get(url);
  }
  const data = await fetch(url).then(r => r.json());
  apiCache.set(url, data);
  console.log(`Cache miss, stored: ${url}`);
  return data;
}

// Cache tự grow — trong production cần TTL/eviction policy
```

## 🔗 Liên kết chéo

- Xem thêm: `03_data-structures/02_keyed-collections/` — overview Map/Set/WeakMap/WeakSet
- Xem thêm: `03_data-structures/02_keyed-collections/02_weakmap/` — WeakMap counterpart
- Tài liệu: [MDN — Map](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map)
