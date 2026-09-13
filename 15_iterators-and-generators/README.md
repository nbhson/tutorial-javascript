# Iterator và Generator — [Level: Intermediate]

## 🔑 Khái niệm cốt lõi

Trong JavaScript, **Iterator** và **Generator** là hai cơ chế nền tảng cho phép duyệt dữ liệu một cách **lazy (lười biếng)** — tức là giá trị chỉ được tính toán khi thực sự cần, chứ không phải tính sẵn cả tập hợp. Đây là kỹ thuật giúp JavaScript xử lý được các chuỗi vô hạn mà không bao giờ làm đầy bộ nhớ.

**Iterator** (bậc thấp) là một object thỏa mãn **Iterator Protocol**: phải có phương thức `next()` trả về object `{ value, done }`. `value` là phần tử hiện tại, `done` là boolean cho biết đã hết phần tử hay chưa. Bất kỳ object nào có property `Symbol.iterator` (ký hiệu biểu tượng của ngôn ngữ) trả về một iterator thì được gọi là **Iterable** — và từ đó có thể dùng được trong `for...of`, spread `...`, `Array.from()`, destructuring, v.v.

**Generator** (bậc cao) là một hàm đặc biệt khai báo bằng `function*` hoặc `async function*`. Khi gọi generator, nó **không chạy ngay thân hàm** — mà trả về một iterator object đặc biệt. Mỗi lần gọi `next()` trên iterator đó, code bên trong chạy đến câu lệnh `yield` tiếp theo, nhả ra giá trị rồi **dừng lại và ghi nhớ vị trí**. Lần `next()` sau tiếp tục từ đúng điểm dừng. Cơ chế này cho phép tạo các chuỗi vô hạn, pipeline xử lý dữ liệu tuần tự, hay state machine đơn giản.

Mối quan hệ then chốt: generator **tự động cung cấp** iterator chuẩn, nên bạn几乎 không bao giờ cần tự viết object iterator thủ công nữa. Nhưng hiểu rõ iterator protocol vẫn quan trọng khi bạn muốn custom một class có khả năng `for...of`.

Trong repo này:
- `01_generators/app.js` — ví dụ generator `idCreator()` tạo chuỗi số nguyên vô hạn.
- `02_iterators/app.js` — ví dụ object tự định nghĩa `[Symbol.iterator]()` dùng generator shorthand.

## 📐 Cấu trúc / Cú pháp

### Iterator Protocol (thuật ngữ chuẩn ECMAScript)

```js
const iterator = {
  [Symbol.iterator]() {
    let step = 0;
    return {
      next() {
        step++;
        return step <= 3
          ? { value: step, done: false }
          : { value: undefined, done: true };
      }
    };
  }
};
```

| Thành phần | Mô tả |
|---|---|
| `Symbol.iterator` | Key đặc biệt để object trở thành iterable |
| `iterator.next()` | Trả về `{ value, done }` — gọi lặp lại cho mỗi phần tử |
| `done: false` | Vẫn còn phần tử, `value` có ý nghĩa |
| `done: true` | Đã hết phần tử; `value` thường là `undefined` |
| Return value của `[Symbol.iterator]` | Phải là một iterator object (có `next()`) |

### Generator Syntax

```js
// Khai báo generator
function* gen() {
  yield 1;       // Nhả giá trị 1, tạm dừng
  yield 2;       // Nhả giá trị 2, tạm dừng
  return 3;      // Nhả giá trị 3 và kết thúc (done: true)
}

const g = gen();   // ⚠️ chưa chạy! Chỉ tạo iterator
console.log(g.next()); // { value: 1, done: false }
console.log(g.next()); // { value: 2, done: false }
console.log(g.next()); // { value: 3, done: true  }
```

| Thành phần | Mô tả |
|---|---|
| `function*` | Khai báo generator function |
| `yield <expr>` | Nhả `<expr>`, dừng tại đó |
| `yield* <iterable>` | Delegate sang iterable khác (flattening) |
| `return <expr>` | Kết thúc generator với giá trị cuối |
| `gen.next(value)` | Tiếp tục chạy, gửi `value` vào trong generator |
| `async function*` | Generator bất đồng bộ, kết hợp `await` + `yield` |

## ✅ Điểm mạnh — Tại sao nên dùng

1. **Tiết kiệm bộ nhớ cực lớn** — dữ liệu sinh ra theo demand, không lưu cả tập hợp vào RAM. Phù hợp với chuỗi vô hạn (Fibonacci vô tận, stream file lớn).
2. **Code tuần tự, dễ đọc** — `function*` + `yield` diễn tả logic tuần tự giống như viết vòng lặp thường, thay vì callback lồng nhau hay promise chaining rối rắm.
3. **Tương thích ngôn ngữ** — iterable chạy được ngay với `for...of`, spread `[...it]`, `Array.from()`, destructuring `const [a,b] = it`.
4. **Giữ trạng thái ngầm** — generator "nhớ" vị trí dừng và mọi biến cục bộ giữa các lần `next()`, không cần dùng closure thủ công.
5. **Hỗ trợ async streaming** — `async function*` kết hợp `for await...of` để đọc stream dữ liệu (HTTP, file, WebSocket) từng khối.
6. **Viết pipeline functional** — map/filter/reduce trên dữ liệu lazy vô hạn mà không sinh mảng trung gian.
7. **Tạo state machine đơn giản** — mỗi `yield` là một trạng thái; nhận input qua `next(data)` để chuyển trạng thái.
8. **Tree traversal dễ dàng** — duyệt cây (DOM, AST, file system) theo thứ tự trước/sau/vượt qua bằng generator đệ quy.
9. **Tách biệt producer-consumer** — một bên `yield`, một bên `next()` — mô hình publish/subscribe đơn giản.
10. **Không cần thư viện bên ngoài** — built-in của ngôn ngữ, không phụ thuộc jQuery/Lodash.

## ⚠️ Bẫy thường gặp & Hạn chế

### Bẫy 1: Quên gọi `next()` đầu tiên
```js
function* gen() { yield 1; }
const g = gen();
// g chưa chạy — phải gọi g.next() lần đầu mới bắt đầu
console.log(g.next().value); // 1
```

### Bẫy 2: Iterator dùng một lần — không duyệt lại được
```js
const arr = [1, 2, 3];
const it = arr[Symbol.iterator]();
console.log([...it]); // [1, 2, 3]
console.log([...it]); // []  ← đã hết, phải lấy iterator mới
```

### Bẫy 3: Generator không thể quay ngược (backward)
```js
function* gen() { yield 1; yield 2; yield 3; }
const g = gen();
g.next(); g.next();
// Không có cách nào để "quay lại" yield 1 — chỉ tiếp diễn về phía trước
```

### Bẫy 4: `yield` chỉ hợp lệ trong `function*`
```js
const fn = () => { yield 1; }; // ❌ SyntaxError
const gen = function*() { yield 1; }; // ✅
```

### Bẫy 5: `yield*` cần iterable, không phải iterator thô
```js
function* outer() {
  yield* [1, 2, 3]; // ✅ delegate sang array
  yield* "abc";     // ✅ delegate sang string (iterable)
  // yield* 42;     // ❌ TypeError: 42 is not iterable
}
```

### Bẫy 6: Gửi giá trị vào generator qua `next(data)`
```js
function* gen() {
  const x = yield 1;  // lần next() thứ 2 gửi giá trị vào x
  console.log('received:', x);
  yield 2;
}
const g = gen();
g.next();           // { value: 1, done: false }
g.next('hello');    // received: hello → { value: 2, done: false }
```

### Bẫy 7: Infinite loop nếu không check `done`
```js
function* infinite() { while (true) yield Math.random(); }
const it = infinite();
// for...of sẽ loop vô hạn — phải break chủ động
for (const v of it) { if (v > 0.9) break; }
```

## 💡 Khi nào dùng — Tình huống thực tế

1. **Tạo ID tự tăng vô hạn** — thay vì pre-generate mảng, dùng generator `function* uid() { let i = 0; while (true) yield ++i; }`.
2. **Xử lý stream dữ liệu lớn** — đọc từng dòng file, từng trang API, không tải toàn bộ vào RAM.
3. **Duyệt cấu trúc tùy chỉnh** — linked list, tree, graph — thêm `Symbol.iterator` để dùng `for...of`.
4. **Finite-state machine** — game logic, workflow approval,每一步 yield một state rồi nhận trigger.
5. **Data pipeline lazy** — `pipe(map, filter, take)(sourceGenerator)` — không tạo mảng trung gian.
6. **Paginated API consumer** — `async function* pages(url) { let next = url; while (next) { const r = await fetch(next); yield r.data; next = r.nextPage; } }`
7. **Tạo observable đơn giản** — kết hợp `yield*` với event listener để stream sự kiện DOM.
8. **Virtual scrolling / infinite scroll** — chỉ render N items tại thời điểm yêu cầu.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Generator tạo chuỗi Fibonacci vô hạn
```js
function* fibonacci() {
  let a = 0, b = 1;
  while (true) {
    yield a;           // nhả giá trị hiện tại
    [a, b] = [b, a + b]; // cập nhật cho bước tiếp
  }
}

// Dùng: lấy 10 số đầu
const fib = fibonacci();
for (let i = 0; i < 10; i++) {
  console.log(fib.next().value); // 0, 1, 1, 2, 3, 5, 8, 13, 21, 34
}
```

### Ví dụ 2: Object tự định nghĩa Iterator (không dùng generator)
```js
const range = {
  start: 1,
  end: 5,
  *[Symbol.iterator]() {
    for (let i = this.start; i <= this.end; i++) {
      yield i;
    }
  }
};

console.log([...range]); // [1, 2, 3, 4, 5]
for (const n of range) console.log(n);
```

### Ví dụ 3: Generator với `yield*` delegate
```js
function* letters() {
  yield* 'abc';   // delegate string → 'a', 'b', 'c'
  yield 'x';
  yield* [1, 2];  // delegate array → 1, 2
}
console.log([...letters()]); // ['a', 'b', 'c', 'x', 1, 2]
```

### Ví dụ 4: Gửi dữ liệu vào generator (hai chiều)
```js
function* conversation() {
  const name = yield 'Xin chào, bạn tên gì?';
  console.log('Tên bạn là:', name);
  const age = yield 'Bạn bao nhiêu tuổi?';
  console.log('Tuổi:', age);
  yield 'Hẹn gặp lại!';
}

const chat = conversation();
console.log(chat.next().value);         // 'Xin chào, bạn tên gì?'
console.log(chat.next('Sơn Nguyên').value); // 'Bạn tên là: Sơn Nguyên' → 'Bạn bao nhiêu tuổi?'
console.log(chat.next('25').value);     // 'Tuổi: 25' → 'Hẹn gặp lại!'
chat.next();                            // done: true
```

### Ví dụ 5: Async generator — đọc dữ liệu phân trang
```js
async function* fetchPages(baseUrl) {
  let url = baseUrl;
  while (url) {
    const res = await fetch(url);
    const json = await res.json();
    yield json.items;        // nhả dữ liệu trang hiện tại
    url = json.nextUrl || null;
  }
}

// Sử dụng
for await (const page of fetchPages('https://api.example.com/items')) {
  console.log('Nhận được', page.length, 'items');
}
```

### Ví dụ 6: Duyệt cây DOM bằng generator đệ quy
```js
function* traverseTree(node) {
  yield node;                          // Xử lý node hiện tại (pre-order)
  for (const child of node.childNodes) {
    if (child.nodeType === Node.ELEMENT_NODE) {
      yield* traverseTree(child);      // Delegate đệ quy cho từng con
    }
  }
  // Post-order: xử lý sau khi con xong
}

// Dùng: thu thập tất cả <a> tags
const links = [...traverseTree(document.body)]
  .filter(n => n.tagName === 'A');
```

### Ví dụ 7: Finite State Machine với generator
```js
function* trafficLight() {
  while (true) {
    yield { color: 'đỏ',    msg: 'Dừng' };
    yield { color: 'vàng',  msg: 'Cẩn thận' };
    yield { color: 'xanh',  msg: 'Đi' };
  }
}

const light = trafficLight();
console.log(light.next().value); // { color: 'đỏ', msg: 'Dừng' }
console.log(light.next().value); // { color: 'vàng', msg: 'Cẩn thận' }
console.log(light.next().value); // { color: 'xanh', msg: 'Đi' }
console.log(light.next().value); // { color: 'đỏ', msg: 'Dừng' } — cycle
```

### Ví dụ 8: Chunk dữ liệu (chia mảng thành khối)
```js
function* chunk(arr, size) {
  for (let i = 0; i < arr.length; i += size) {
    yield arr.slice(i, i + size);
  }
}

const data = Array.from({ length: 10 }, (_, i) => i + 1);
for (const c of chunk(data, 3)) {
  console.log(c); // [1,2,3] [4,5,6] [7,8,9] [10]
}
```

## 🔬 So sánh với alternatives

| Cách tiếp cận | Ưu điểm | Nhược điểm | Khi nào chọn |
|---|---|---|---|
| **Array + push** | Đơn giản, quen thuộc | Tốn RAM, phải tính trước kích thước | Dữ liệu nhỏ, đã biết giới hạn |
| **Iterator thủ công** | Kiểm soát từng bước, linh hoạt | Viết nhiều boilerplate, dễ lỗi `done` | Cần custom traversal (tree, graph) |
| **Generator (`function*`)** | Code gọn, lazy, giữ state tự động | Một chiều, không random-access | Hầu hết trường hợp lazy evaluation |
| **Async generator** | Streaming bất đồng bộ | Cần `for await...of`, khó debug | API phân trang, file stream |
| **RxJS Observable** | Powerful operators (map/switchMap) | Thư viện nặng, learning curve | App phức tạp cần reactive pipeline |
| **Promise chain** | Async rõ ràng | Callback hell khi nhiều bước | Chỉ 1-2 bước async đơn giản |

## 📊 Performance & Best Practices

- **Generator overhead nhỏ**: mỗi `yield` có chi phí context switch, nhưng thường nhỏ hơn nhiều so với lợi ích lazy evaluation.
- **Không dùng generator cho hot path siêu tốc**: nếu cần performance cực cao (game loop, WebGL), prefer array pre-allocation hoặc typed arrays.
- **Always handle `done`**: khi gọi `next()` thủ công, luôn check `done === true` trước khi truy cập `.value`.
- **Dùng `for...of` thay vì `while` + `next()`** — ngắn gọn hơn, ít lỗi hơn.
- **Memory**: generator object tự gc khi hết reference — không cần `close()` thủ công trong JS thuần.
- **Avoid deep nesting**: generator đệ quy sâu có thể gây stack overflow; cân nhắc dùng iterative approach cho cây rất sâu.
- **Browser support**: IE không hỗ trợ generator — cần transpile (Babel) nếu target legacy.

## 🔗 Liên kết chéo

- Xem thêm: `15_iterators-and-generators/01_generators/` — ví dụ `idCreator()` cơ bản.
- Xem thêm: `15_iterators-and-generators/02_iterators/` — tự định nghĩa `Symbol.iterator`.
- Xem thêm: `16_modules/` — ESM module system, có `import`/`export` tĩnh liên quan đến module loading.
- Xem thêm: `18_dom-apis/01_dom-basics/01_f8-basic-dom/7_node-property/` — duyệt DOM tree có thể áp dụng generator.
- Xem thêm: `17_memory-management/` — generator object bị GC như thế nào khi không còn reference.
