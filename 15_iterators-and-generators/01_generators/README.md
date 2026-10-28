# Generator — [Level: Intermediate]

## 🔑 Khái niệm cốt lõi

**Generator** là một loại hàm đặc biệt trong JavaScript, khai báo bằng cú pháp `function*` (hoặc arrow function không được). Khác với hàm thông thường chạy từ đầu đến cuối rồi `return` một kết quả duy nhất, generator có khả năng **tạm dừng và tiếp tục** execution tại bất kỳ điểm nào bên trong thân hàm nhờ từ khóa `yield`.

Cơ chế hoạt động bên trong JavaScript engine (V8):

1. Khi bạn gọi `gen()`, engine **không thực thi thân hàm** — nó chỉ tạo và trả về một **generator iterator object** (là một object thỏa Iterator Protocol, có phương thức `next()`).
2. Lần gọi `next()` đầu tiên: engine bắt đầu chạy thân hàm từ đầu, thực hiện các câu lệnh cho đến khi gặp `yield <expr>` đầu tiên. Giá trị `<expr>` được nhả ra dưới dạng `{ value: <expr>, done: false }`, rồi engine **ghi lại toàn bộ stack frame** (biến cục bộ, vị trí dòng lệnh hiện tại) và tạm dừng.
3. Lần gọi `next()` tiếp theo: engine **khôi phục stack frame** đã lưu, tiếp tục chạy từ sau `yield` cho đến `yield` kế tiếp (hoặc `return` / hết hàm). Quá trình này lặp lại cho đến khi generator kết thúc (`done: true`).
4. Khi generator kết thúc, stack frame bị giải phóng và generator object có thể được garbage collected nếu không còn reference.

Nhờ cơ chế tạm dừng-này, generator có thể biểu diễn các **chuỗi vô hạn** (infinite sequences) mà không bao giờ làm đầy bộ nhớ — mỗi giá trị chỉ được tính khi consumer yêu cầu qua `next()`. Đây là kỹ thuật **lazy evaluation** kinh điển.

Trong repo này, `01_generators/app.js` minh họa hàm `idCreator()` — một generator tạo chuỗi số nguyên `0, 1, 2, 3, ...` vô hạn. Vòng lặp `while (true)` bên trong không bao giờ treo máy vì nó chỉ chạy từng bước khi `next()` được gọi.

## 📐 Cấu trúc / Cú pháp

### Các dạng khai báo generator

```js
// Dạng 1: function declaration
function* gen1() {
  yield 1;
  yield 2;
}

// Dạng 2: function expression
const gen2 = function*() {
  yield 'a';
};

// Dạng 3: method trong object
const obj = {
  *values() { yield 1; yield 2; }
};

// Dạng 4: arrow function KHÔNG được (syntax error)
// const gen3 = () => { yield 1; }; // ❌ SyntaxError

// Dạng 5: async generator (ES2018+)
async function* asyncGen() {
  const res = await fetch('/api/data');
  yield await res.json();
}
```

### Cú pháp `yield` chi tiết

| Cú pháp | Ý nghĩa | Trả về từ `next()` |
|---|---|---|
| `yield expr` | Nhả `expr`, tạm dừng | `{ value: expr, done: false }` |
| `yield` (không expr) | Nhả `undefined`, tạm dừng | `{ value: undefined, done: false }` |
| `yield* iterable` | Delegate sang iterable khác | Trả về từng value của iterable |
| `return expr` | Kết thúc generator | `{ value: expr, done: true }` |
| `throw err` | Ném lỗi vào generator | Lỗi nổi lên từ `next()` |

### Gọi generator — các pattern phổ biến

```js
function* counter(start) {
  for (let i = start; ; i++) yield i;
}

// Pattern 1: for...of (phổ biến nhất)
for (const n of counter(10)) {
  if (n > 15) break;
  console.log(n); // 10, 11, 12, 13, 14, 15
}

// Pattern 2: gọi tay next()
const c = counter(10);
console.log(c.next()); // { value: 10, done: false }
console.log(c.next()); // { value: 11, done: false }

// Pattern 3: spread / Array.from
console.log([...counter(1), ...counter(1)]); // [1, 2, 3] — lấy 3 số đầu

// Pattern 4: destructuring
const [a, b, c] = counter(100);
console.log(a, b, c); // 100, 101, 102
```

## ✅ Điểm mạnh — Tại sao nên dùng

1. **Lazy evaluation** — tính toán chỉ khi cần, lý tưởng cho chuỗi vô hạn và dữ liệu lớn.
2. **Giữ trạng thái tự động** — biến cục bộ và vị trí dòng lệnh được bảo tồn giữa các lần `next()`, không cần closure thủ công.
3. **Code tuần tự, dễ đọc** — logic viết giống vòng lặp thường, không phải callback/promise lồng nhau.
4. **Tương thích mọi cú pháp iterable** — `for...of`, spread, `Array.from`, destructuring đều dùng được.
5. **Nền tảng async streaming** — `async function*` + `for await...of` để đọc stream bất đồng bộ.
6. **Tạo state machine sạch** — mỗi `yield` là một state, input nhận qua `next(data)`.
7. **Duyệt cấu trúc phức tạp** — tree traversal, graph traversal viết gọn hơn nhiều so với iterative stack.
8. **Pipeline functional** — kết hợp với map/filter tạo dây chuyền xử lý không sinh mảng trung gian.
9. **Không cần thư viện** — built-in language feature, zero dependency.
10. **Resource-friendly** — generator object bị GC tự động khi hết reference, không cần dispose thủ công.

## ⚠️ Bẫy thường gặp & Hạn chế

### Bẫy 1: Gọi `gen()` không chạy code
```js
function* gen() { console.log('chạy!'); yield 1; }
const g = gen();  // ⚠️ log 'chạy!' CHƯA in — cần g.next() mới chạy
g.next();         // bây giờ mới in 'chạy!' và nhả 1
```

### Bẫy 2: Generator chỉ duyệt một chiều, một lần
```js
function* gen() { yield 1; yield 2; }
const g = gen();
console.log([...g]);  // [1, 2]
console.log([...g]);  // []  ← đã done, phải tạo generator mới
```

### Bẫy 3: Không thể "quay ngược" (no seek/back)
```js
function* gen() { yield 1; yield 2; yield 3; }
const g = gen();
g.next(); g.next();
// Không có cách nào để lấy lại giá trị 1 — chỉ có thể tiến tới
```

### Bẫy 4: `yield` ngoài `function*` là SyntaxError
```js
const fn = () => yield 1; // ❌ SyntaxError
// Arrow function không thể là generator
```

### Bẫy 5: `yield*` cần iterable, không phải value vô hướng
```js
function* gen() {
  yield* 42;  // ❌ TypeError: 42 is not iterable
  yield* [1, 2]; // ✅
}
```

### Bẫy 6: Quên `return` khi generator xong việc
```js
function* gen() {
  yield 1;
  // thiếu return → lần next() cuối trả { value: undefined, done: true }
  // Nên explicit return để giá trị cuối rõ ràng
}
```

### Bẫy 7: Gửi dữ liệu vào generator qua `next()`
```js
function* gen() {
  const x = yield 'hello'; // lần next() thứ 2 truyền value vào x
  yield x * 2;
}
const g = gen();
g.next();           // { value: 'hello', done: false }
g.next(5);          // { value: 10, done: false }  ← x = 5
```

### Bẫy 8: Infinite loop nếu không break
```js
function* infinite() { while (true) yield Math.random(); }
// for (const v of infinite()) console.log(v); // ❌ infinite loop!
// Phải:
let count = 0;
for (const v of infinite()) { if (++count >= 10) break; }
```

## 💡 Khi nào dùng — Tình huống thực tế

1. **ID tự tăng vô hạn** — `function* uid() { let i = 0; while (true) yield ++i; }` thay vì pre-generate mảng.
2. **Stream file lớn** — đọc từng chunk, xử lý rồi discard, không load cả file vào RAM.
3. **API phân trang** — `async function* pages() { while (next) { yield await fetch(next); next = resp.next; } }`
4. **Finite State Machine** — game AI, workflow approval, mỗi bước yield state rồi nhận trigger.
5. **Tree traversal** — duyệt DOM/AST/cấu trúc cây theo pre-order/in-order/post-order.
6. **Data pipeline** — `pipe(map, filter, take)(source)` mà không tạo mảng trung gian.
7. **Virtual scroller** — chỉ render N items được yêu cầu, không tải hết danh sách.
8. **Event stream** — lắng nghe DOM events và stream chúng qua generator.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Generator cơ bản — chuỗi ID vô hạn (file `app.js`)
```js
// idCreator: generator tạo dãy số 0, 1, 2, 3, ... vô hạn
function* idCreator() {
  let i = 0;                        // biến cục bộ được ghi nhớ giữa các lần next()
  while (true) {                    // vòng lặp vô hạn — an toàn vì lazy
    yield i++;                      // nhả i hiện tại, sau đó tăng
  }
}

const ids = idCreator();            // ⚠️ chưa chạy code — chỉ tạo iterator
console.log(ids.next().value);      // 0
console.log(ids.next().value);      // 1
console.log(ids.next().value);      // 2
// Có thể gọi vô hạn lần mà không tốn bộ nhớ thêm
```

### Ví dụ 2: Fibonacci vô hạn
```js
function* fibonacci() {
  let a = 0, b = 1;
  while (true) {
    yield a;                        // nhả số Fibonacci hiện tại
    [a, b] = [b, a + b];           // tính số tiếp theo
  }
}

const fib = fibonacci();
for (let i = 0; i < 10; i++) {
  console.log(fib.next().value);    // 0, 1, 1, 2, 3, 5, 8, 13, 21, 34
}
```

### Ví dụ 3: Filter generator (pipeline lazy)
```js
function* filter(source, predicate) {
  for (const item of source) {
    if (predicate(item)) yield item; // chỉ nhả những item thỏa điều kiện
  }
}

function* range(start, end) {
  for (let i = start; i <= end; i++) yield i;
}

// Lấy các số chẵn từ 1 đến 20
const evens = [...filter(range(1, 20), n => n % 2 === 0)];
console.log(evens); // [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
```

### Ví dụ 4: Duyệt cây DOM đệ quy
```js
function* treeWalker(node) {
  yield node;                                    // pre-order: xử lý node hiện tại
  for (const child of node.childNodes) {
    if (child.nodeType === Node.ELEMENT_NODE) {
      yield* treeWalker(child);                  // delegate đệ quy
    }
  }
  // post-order: sau khi con xong
}

const allDivs = [...treeWalker(document.body)]
  .filter(n => n.tagName === 'DIV');
```

### Ví dụ 5: Generator nhận dữ liệu từ caller
```js
function* questionaire() {
  const name = yield 'Tên bạn là gì?';
  console.log('Xin chào,', name);
  const city = yield 'Bạn ở thành phố nào?';
  console.log('Thành phố:', city);
  yield 'Hẹn gặp lại,'+ name + '!';
}

const q = questionaire();
console.log(q.next().value);        // 'Tên bạn là gì?'
console.log(q.next('Sơn Nguyên').value); // 'Xin chào, Sơn Nguyên' → 'Bạn ở thành phố nào?'
console.log(q.next('Hà Nội').value);    // 'Thành phố: Hà Nội' → 'Hẹn gặp lại,Sơn Nguyên!'
q.next();                           // done: true
```

### Ví dụ 6: Chunk array thành khối
```js
function* chunk(arr, size) {
  for (let i = 0; i < arr.length; i += size) {
    yield arr.slice(i, i + size);  // mỗi khối là một mảng con
  }
}

const data = [1,2,3,4,5,6,7,8,9,10];
for (const c of chunk(data, 3)) {
  console.log(c); // [1,2,3] [4,5,6] [7,8,9] [10]
}
```

### Ví dụ 7: Async generator đọc API phân trang
```js
async function* fetchPages(baseUrl) {
  let url = baseUrl;
  while (url) {
    const res = await fetch(url);
    const json = await res.json();
    yield json.items;              // nhả data trang hiện tại
    url = json.nextUrl || null;    // chuẩn bị trang kế
  }
}

// Dùng:
for await (const page of fetchPages('https://api.example.com/items')) {
  console.log('Trang có', page.length, 'items');
}
```

### Ví dụ 8: Repeat generator (lặp lại N lần)
```js
function* repeat(value, times) {
  for (let i = 0; i < times; i++) {
    yield value;
  }
}

console.log([...repeat('hello', 3)]); // ['hello', 'hello', 'hello']
```

## 🔬 So sánh với alternatives

| Cách tiếp cận | Ưu điểm | Nhược điểm | Phù hợp khi |
|---|---|---|---|
| **Array push rồi duyệt** | Đơn giản, quen thuộc | Tốn RAM, phải biết trước độ lớn | Dữ liệu nhỏ, cố định |
| **Generator** | Lazy, memory-efficient, code gọn | Một chiều, không random-access | Chuỗi dài/vô hạn, streaming |
| **Async generator** | Streaming bất đồng bộ | Cần `for await...of` | API phân trang, file read |
| **RxJS Observable** | Operators phong phú | Thư viện nặng, learning curve | Reactive pipeline phức tạp |
| **Callback/Promise chain** | Familiar pattern | Callback hell khi nhiều bước | Async đơn giản, 1-2 bước |

## 📊 Performance & Best Practices

- **Overhead nhỏ**: mỗi `yield` có chi phí context switch ~nanosecond, chấp nhận được cho hầu hết use case.
- **Hot path**: tránh generator trong vòng lặp siêu dày (game loop, WebGL) — dùng pre-allocated array hoặc typed array thay thế.
- **Always check `done`**: khi gọi `next()` thủ công, kiểm tra `done === true` để tránh `undefined.value`.
- **Prefer `for...of`** thay vì `while(true) + next()` — ngắn gọn, ít lỗi hơn.
- **GC friendly**: generator object tự động bị thu hồi khi không còn reference — không cần close thủ công.
- **Deep recursion caveat**: generator đệ quy sâu có thể gây stack overflow trong một số engine — cân nhắc iterative approach.
- **Browser compatibility**: IE không support generator — cần Babel transpile nếu target legacy browsers.
- **Memory tip**: generator giữ reference đến scope closure — đừng tạo generator bao quanh dữ liệu lớn nếu không cần.

## 🔗 Liên kết chéo

- Xem thêm: `15_iterators-and-generators/02_iterators/` — Iterator Protocol và `Symbol.iterator`.
- Xem thêm: `16_modules/` — ESM modules, `import`/`export` tĩnh, có liên quan đến module loading.
- Xem thêm: `17_memory-management/01_memory-lifecycle-gc/` — generator object bị GC khi không còn reference.
- Xem thêm: `18_dom-apis/01_dom-basics/01_f8-basic-dom/7_node-property/` — duyệt DOM tree có thể áp dụng generator.
- Xem thêm: `18_dom-apis/03_events/` — event stream có thể pipe qua async generator.
