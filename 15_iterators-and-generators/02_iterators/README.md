# Iterator (Symbol.iterator) — [Level: Intermediate]

## 🔑 Khái niệm cốt lõi

**Iterator** là một object interface chuẩn trong JavaScript, được định nghĩa bởi **Iterator Protocol** (ECMAScript specification). Theo protocol này, một object được coi là **iterator** khi nó có phương thức `next()` trả về object `{ value, done }`:

- `value`: phần tử hiện tại đang duyệt (hoặc `undefined` nếu đã hết).
- `done`: boolean — `false` nghĩa là còn phần tử, `true` nghĩa là đã duyệt hết.

Một object **iterable** (khả năng lặp) là object có property `Symbol.iterator` — một Symbol built-in của ngôn ngữ — trả về một iterator object. Khi object là iterable, nó có thể dùng được trong `for...of`, spread `...`, `Array.from()`, destructuring assignment, `yield*`, v.v.

JavaScript có nhiều kiểu built-in iterable sẵn:
- `Array`, `String`, `Map`, `Set`, `arguments`, `NodeList`, `DOMTokenList`

Tuy nhiên, bạn hoàn toàn có thể làm cho **class/object tùy chỉnh** trở thành iterable bằng cách thêm `Symbol.iterator` — đây là sức mạnh thực sự của Iterator Protocol.

Iterator là **một chiều** (one-pass): sau khi `done === true`, iterator không thể quay lại đầu. Muốn duyệt lại phải gọi lại `Symbol.iterator()` để nhận iterator mới. Đây là thiết kế có chủ đích — iterator đại diện cho một "con trỏ" đang di chuyển, không phải bản sao dữ liệu.

Trong ví dụ `02_iterators/app.js`, một object thường được biến thành iterable bằng cách định nghĩa generator shorthand `*[Symbol.iterator]() { yield 1; yield 2; yield 3; }`. Sau đó vừa dùng được với `for...of`, vừa có thể gọi tay `it.next()` để kiểm soát từng bước.

**Phân biệt nhanh ba khái niệm:**
- **Iterator** = object có `next()` (mức thấp, có thể viết tay).
- **Iterable** = object có `Symbol.iterator` (dùng được trong `for...of`).
- **Generator** = `function*` dùng `yield`; gọi generator là có ngay một iterator mà không cần viết `next()` thủ công.

## 📐 Cấu trúc / Cú pháp

### Iterator Protocol — chuẩn ECMAScript

```js
const iterator = {
  next() {
    // Must return { value: any, done: boolean }
    return { value: /* some value */, done: false };
  }
};
```

### Iterable Protocol — để dùng trong `for...of`

```js
const iterable = {
  [Symbol.iterator]() {
    let count = 0;
    return {
      next() {
        count++;
        return count <= 3
          ? { value: count, done: false }
          : { value: undefined, done: true };
      }
    };
  }
};

// Dùng được ngay:
for (const n of iterable) console.log(n); // 1, 2, 3
console.log([...iterable]);               // [1, 2, 3]
```

### Generator shorthand (loophole tiện lợi)

```js
const obj = {
  *[Symbol.iterator]() {   // * ở trước Symbol.iterator = generator method
    yield 1;
    yield 2;
    yield 3;
  }
};
```

### Bảng so sánh Iterator vs Iterable

| Thuộc tính | Iterator | Iterable |
|---|---|---|
| Có `next()` | ✅ Bắt buộc | ❌ Không cần |
| Có `Symbol.iterator` | ❌ Không cần | ✅ Bắt buộc |
| Dùng trong `for...of` | ❌ Không trực tiếp | ✅ Có |
| Trả về từ `Symbol.iterator` | — | ✅ Phải là Iterator |
| Ví dụ | `array[Symbol.iterator]()` | `array`, `string`, `map` |

## ✅ Điểm mạnh — Tại sao nên dùng

1. **Chuẩn chung của ngôn ngữ** — iterable "cắm" được vào mọi cú pháp duyệt có sẵn của JS (`for...of`, spread, `Array.from`, destructuring).
2. **Tách biệt cấu trúc dữ liệu khỏi cách duyệt** — bạn định nghĩa logic `next()`, code dùng chỉ cần `for...of`. Không ghép nối.
3. **Lazy evaluation** — chỉ sinh giá trị tiếp theo khi được yêu cầu, tiết kiệm bộ nhớ đáng kể.
4. **Hỗ trợ cấu trúc tùy chỉnh** — linked list, tree, graph, Range, stream đều có thể trở thành iterable.
5. **Kiểm soát từng bước** — gọi tay `next()` để dừng/giữa chừng/kiểm tra trạng thái mà không cần vòng lặp liền mạch.
6. **Tích hợp với generator** — `yield*` delegate sang iterable khác, pipeline data smooth.
7. **Tương thích TypeScript** — type `Iterable<T>` và `Iterator<T>` có sẵn trong lib.dom và ES libs.
8. **Foundation cho ecosystem** — nhiều thư viện (RxJS, D3, Lodash fp) đều dựa trên iterable protocol.
9. **No runtime overhead** — pure JS native, không cần polyfill trong browser hiện đại.
10. **Debug-friendly** — có thể inspect iterator state (value, done) tại mọi thời điểm qua Console.

## ⚠️ Bẫy thường gặp & Hạn chế

### Bẫy 1: Iterator "dùng một lần" — phải lấy lại
```js
const arr = [1, 2, 3];
const it = arr[Symbol.iterator]();
console.log([...it]); // [1, 2, 3]
console.log([...it]); // []  ← iterator đã done, phải lấy lại
const it2 = arr[Symbol.iterator]();
console.log([...it2]); // [1, 2, 3] ✅
```

### Bẫy 2: Thiếu `Symbol.iterator` → "not iterable"
```js
const obj = { first: 1, second: 2 };
// obj[Symbol.iterator] là undefined
for (const v of obj) {
  // ❌ TypeError: obj is not iterable
}
// Fix: thêm Symbol.iterator
obj[Symbol.iterator] = function*() { yield* Object.values(this); };
```

### Bẫy 3: Gọi `next()` sau khi `done` vẫn hợp lệ (không lỗi nhưng vô nghĩa)
```js
function* gen() { yield 1; }
const g = gen();
g.next(); // { value: 1, done: false }
g.next(); // { value: undefined, done: true }
g.next(); // { value: undefined, done: true }  ← vẫn return đúng, nhưng không có giá trị
```

### Bẫy 4: Nhầm Iterator vs Iterable
```js
// Iterator có next()
const it = [1,2,3][Symbol.iterator]();
console.log(typeof it.next); // 'function' ✅ là iterator

// Iterable có Symbol.iterator
console.log(typeof [1,2,3][Symbol.iterator]); // 'function' ✅ là iterable
```

### Bẫy 5: NodeList không phải Array — không có `map/filter`
```js
const nodes = document.querySelectorAll('div');
nodes.map(...); // ❌ TypeError: nodes.map is not a function
// Fix:
[...nodes].map(...); // ✅
Array.from(nodes).map(...); // ✅
```

### Bẫy 6: HTMLCollection (live) vs NodeList (static) — khác nhau khi DOM đổi
```js
const divs = document.getElementsByTagName('div'); // HTMLCollection — LIVE
const nodes = document.querySelectorAll('div');     // NodeList — STATIC snapshot
// Thêm div mới → divs.length tăng, nodes.length không đổi
```

## 💡 Khi nào dùng — Tình huống thực tế

1. **Class tùy chỉnh cần `for...of`** — linked list, tree, Range, Queue đều có thể iterable.
2. **Chuỗi giá trị theo quy tắc** — bộ đếm, bảng cửu chương, dãy số, sinh ngẫu nhiên có giới hạn.
3. **Chuyển đổi dữ liệu** — từ `NodeList`/`arguments`/`String` sang array để dùng `map`/`filter`.
4. **Điều khiển từng bước duyệt** — pause/resume, skip, tìm kiếm có điều kiện giữa chừng.
5. **Custom pagination** — iterator sinh trang dữ liệu theo yêu cầu từ API.
6. **State machine visualization** — iterator sinh từng bước trạng thái của automata.
7. **Large dataset sampling** — iterator tạo mẫu ngẫu nhiên từ tập dữ liệu khổng lồ.
8. **DOM traversal abstraction** — bọc DOM API thành iterable cho code downstream sạch hơn.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Object tự định nghĩa Iterator (file `app.js`)
```js
// Object thường + generator shorthand làm iterable
const obj = {
  *[Symbol.iterator]() {   // * = generator method
    yield 1;
    yield 2;
    yield 3;
  }
};

// Dùng với for...of
for (const x of obj) console.log(x); // 1, 2, 3

// Gọi tay next()
const it = obj[Symbol.iterator]();
console.log(it.next()); // { value: 1, done: false }
console.log(it.next()); // { value: 2, done: false }
console.log(it.next()); // { value: 3, done: false }
console.log(it.next()); // { value: undefined, done: true }
```

### Ví dụ 2: Range class — số từ start đến end
```js
class Range {
  constructor(start, end) {
    this.start = start;
    this.end = end;
  }
  *[Symbol.iterator]() {
    for (let i = this.start; i <= this.end; i++) {
      yield i;
    }
  }
}

console.log([...new Range(1, 5)]); // [1, 2, 3, 4, 5]
for (const n of new Range(10, 12)) console.log(n); // 10, 11, 12
```

### Ví dụ 3: Fibonacci iterable
```js
const fibonacci = {
  *[Symbol.iterator]() {
    let a = 0, b = 1;
    for (let i = 0; i < 10; i++) {
      yield a;
      [a, b] = [b, a + b];
    }
  }
};

console.log([...fibonacci]); // [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

### Ví dụ 4: Duyệt đối tượng (object entries iterable)
```js
const person = { name: 'Sơn', age: 25, city: 'Hà Nội' };

// Object.entries đã là iterable
for (const [key, value] of Object.entries(person)) {
  console.log(`${key}: ${value}`);
}
// name: Sơn
// age: 25
// city: Hà Nội
```

### Ví dụ 5: String iterable — duyệt ký tự
```js
const str = 'JavaScript';
for (const char of str) {
  console.log(char); // J, a, v, a, S, c, r, i, p, t
}

// Spread string thành array
const chars = [...str]; // ['J','a','v','a','S','c','r','i','p','t']
```

### Ví dụ 6: Linked List iterable
```js
class Node {
  constructor(value) { this.value = value; this.next = null; }
}

class LinkedList {
  constructor() { this.head = null; }
  add(value) {
    const node = new Node(value);
    if (!this.head) { this.head = node; return; }
    let current = this.head;
    while (current.next) current = current.next;
    current.next = node;
  }
  *[Symbol.iterator]() {
    let current = this.head;
    while (current) {
      yield current.value;
      current = current.next;
    }
  }
}

const list = new LinkedList();
list.add(1); list.add(2); list.add(3);
console.log([...list]); // [1, 2, 3]
```

### Ví dụ 7: Custom Map iterable (pairs)
```js
const myMap = new Map([['a', 1], ['b', 2], ['c', 3]]);

// Map đã iterable theo [key, value] pairs
for (const [k, v] of myMap) {
  console.log(k, v); // a 1, b 2, c 3
}

// Chuyển sang object
const obj = Object.fromEntries(myMap); // { a: 1, b: 2, c: 3 }
```

### Ví dụ 8: Skip-take utility (lấy N phần tử, bỏ M phần tử)
```js
function* skipTake(iterable, skip, take) {
  let i = 0;
  for (const item of iterable) {
    if (i < skip) { i++; continue; }     // bỏ skip phần tử đầu
    if (take <= 0) break;                 // đủ take rồi thì dừng
    yield item;
    take--;
    i++;
  }
}

console.log([...skipTake([1,2,3,4,5,6,7,8], 2, 3)]); // [3, 4, 5]
```

## 🔬 So sánh với alternatives

| Cách tiếp cận | Ưu điểm | Nhược điểm | Khi nào chọn |
|---|---|---|---|
| **Array传统产业** | Đơn giản, quen thuộc | Tốn RAM, phải biết trước kích thước | Dữ liệu nhỏ, fixed |
| **Iterator thủ công** | Kiểm soát 100%, không cần generator | Nhiều boilerplate, dễ lỗi `done` | Custom traversal phức tạp |
| **Generator `[Symbol.iterator]()`** | Code gọn, lazy, chuẩn | Một chiều, không seek | Hầu hết trường hợp tùy chỉnh |
| **Array methods (map/filter)** | Chức năng phong phú | Tạo array mới mỗi lần | Dữ liệu nhỏ, cần chaining |
| **RxJS Observable** | Operators phong phú, async | Thư viện nặng | Reactive app phức tạp |

## 📊 Performance & Best Practices

- **Iterator overhead**: mỗi `next()` call có chi phí function invocation ~microsecond, chấp nhận được.
- **Prefer generator shorthand** `*[Symbol.iterator]()` hơn viết tay object `next()` — code sạch hơn, ít lỗi hơn.
- **Cache iterator khi dùng nhiều lần** — đừng gọi `obj[Symbol.iterator]()` trong vòng lặp (mỗi lần tạo iterator mới).
- **Always handle `done: true`** — khi gọi `next()` thủ công, kiểm tra trước khi dùng `value`.
- **Memory**: iterator object bị GC khi hết reference — không cần dispose thủ công.
- **For large collections**: prefer streaming/iterator thay vì `Array.from()` toàn bộ nếu chỉ duyệt một lần.
- **Browser support**: IE không hỗ trợ `Symbol.iterator` — cần polyfill hoặc transpile.
- **TypeScript**: dùng `Iterable<T>` và `Iterator<T>` types để type-safe.

## 🔗 Liên kết chéo

- Xem thêm: `15_iterators-and-generators/01_generators/` — Generator và cơ chế `yield`.
- Xem thêm: `16_modules/03_modules/` — ESM module exports là iterable.
- Xem thêm: `18_dom-apis/01_dom-basics/01_f8-basic-dom/7_node-property/` — `childNodes` là NodeList (iterable).
- Xem thêm: `17_memory-management/` — iterator object và garbage collection behavior.
- Xem thêm: `18_dom-apis/03_events/` — event stream có thể biến thành iterable.
