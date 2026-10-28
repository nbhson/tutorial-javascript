# ES2025 Features — Tính Năng Mới Trong ECMAScript 2025 — [Level: Intermediate]

> **ES2025 (ECMAScript 2025)** — edition thứ 16 của chuẩn ECMAScript, được Đại hội Ecma thứ 129 phê duyệt ngày **25/06/2025**. Bản cập nhật tập trung vào **developer ergonomics**: iterator helpers, Set methods, Promise utilities, và RegExp improvements.

## 🔑 Khái niệm cốt lõi

ES2025 final hóa các tính năng Stage 4 sau:

| Tính năng | Proposal | Mô tả |
|---|---|---|
| **Iterator Helpers** | [proposal-iterator-helpers](https://github.com/tc39/proposal-iterator-helpers) | `map/filter/take/drop...` trên `Iterator.prototype` |
| **Set Methods** | [proposal-set-methods](https://github.com/tc39/proposal-set-methods) | `union/intersection/difference...` trên `Set.prototype` |
| **`Promise.try()`** | [proposal-promise-try](https://github.com/tc39/proposal-promise-try) | Execute function như promise, bắt cả lỗi sync |
| **`Promise.withResolvers()`** | Stage 4 | Tạo promise với resolve/reject tách riêng |
| **`RegExp.escape()`** | [proposal-regex-escaping](https://github.com/tc39/proposal-regex-escaping) | Escape chuỗi an toàn cho regex pattern |
| **Import Attributes** | Stage 4 | `import ... with { type: "json" }` |
| **JSON Modules** | Stage 4 | Import file JSON như module |
| **RegExp Duplicate Named Groups** | Stage 4 | Trùng tên group trong các alternative |
| **`Float16Array`** | Stage 4 | TypedArray 16-bit floating point |

> **Phân biệt phiên bản:** Một số tính năng hay bị nhầm với ES2025 thực ra thuộc **ES2023/ES2024** — ví dụ `Object.groupBy`/`Map.groupBy`, `Array.prototype.toSorted/toReversed/toSpliced/with` (ES2023), `Promise.withResolvers`, RegExp `v` flag, ArrayBuffer transfer (ES2024). **Temporal API** hiện ở Stage 3 và dự kiến hoàn thiện cho **ES2027** (không phải ES2026). **JSON.parse source text access** đã ship sớm trong trình duyệt nhưng thuộc **ES2026**.

## 📐 Browser Support (tham khảo Baseline 2025)

| Tính năng | Chrome | Firefox | Safari | Node.js |
|---|---|---|---|---|
| Iterator Helpers | 122+ | 131+ | 18.4+ | 22+ |
| Set Methods | 122+ | 127+ | 17+ | 22+ |
| Promise.try / withResolvers | 122+ | 128+ | 17.5+ | 22+ |
| RegExp.escape | 123+ | 127+ | 17.4+ | 22+ |
| Import Attributes / JSON Modules | 123+ | 123+ | 17.2+ | 22+ |
| ArrayBuffer transfer | 114+ | 127+ | 17+ | 18+ |
| Float16Array | 135+ | 129+ | 18.2+ | 22+ |
| Object/Map.groupBy (ES2024) | 117+ | 119+ | 17.4+ | 21+ |
| toSorted/toReversed/toSpliced (ES2023) | 110+ | 115+ | 16.4+ | 20+ |

> Nguồn: [MDN Baseline](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Iterator), [web.dev Baseline blog](https://web.dev/blog/baseline-iterator-helpers). Luôn kiểm tra [caniuse.com](https://caniuse.com) trước khi dùng production.

## 1️⃣ Iterator Helpers — pipeline lazy trên iterator

**Vấn đề trước đây:** `map/filter/reduce` chỉ có trên Array. Với iterator/generator (đặc biệt là chuỗi vô hạn), phải dùng vòng lặp thủ công hoặc thư viện (itertools, lodash), hoặc spread ra mảng trung gian tốn bộ nhớ.

**Giải pháp ES2025:** các method functional trực tiếp trên `Iterator.prototype`, hoạt động **lazy** — một thao tác mỗi phần tử, không tạo mảng trung gian.

**Browser support:** Chrome 122+, Firefox 131+, Safari 18.4+, Node 22+ — [Baseline 2025](https://web.dev/blog/baseline-iterator-helpers).

### Danh sách method

| Method | Chức năng | Lazy? |
|---|---|---|
| `Iterator.prototype.map(fn)` | Transform từng giá trị | ✅ |
| `Iterator.prototype.filter(fn)` | Lọc giá trị truthy | ✅ |
| `Iterator.prototype.take(n)` | Lấy tối đa n giá trị rồi đóng iterator | ✅ |
| `Iterator.prototype.drop(n)` | Bỏ qua n giá trị đầu | ✅ |
| `Iterator.prototype.flatMap(fn)` | Transform + flatten một cấp | ✅ |
| `Iterator.prototype.reduce(fn, init)` | Gộp về một giá trị | ❌ (eager) |
| `Iterator.prototype.toArray()` | Thu thập thành mảng | ❌ (eager) |
| `Iterator.prototype.forEach(fn)` | Duyệt hết, không trả về | ❌ |
| `Iterator.prototype.some(fn)` | Có ít nhất 1 giá trị thỏa? | Dừng sớm |
| `Iterator.prototype.every(fn)` | Tất cả thỏa? | Dừng khi sai |
| `Iterator.prototype.find(fn)` | Tìm giá trị đầu tiên thỏa | Dừng khi thấy |
| `Iterator.from(iterable)` | Bọc iterable/iterator thành Iterator object | ✅ |

### Ví dụ 1: Pipeline lazy với chuỗi vô hạn

```js
// Generator chuỗi số tự nhiên VÔ HẠN
function* naturalNumbers() {
  let n = 0;
  while (true) yield n;
}

// Trước ES2025: spread ra mảng → treo máy!
// [...naturalNumbers()].filter(...).map(...)  ❌

// ES2025: lazy pipeline — an toàn với chuỗi vô hạn
const result = naturalNumbers()
  .filter(n => n % 2 === 0)     // số chẵn
  .map(n => n * n)              // bình phương
  .take(5)                      // chỉ lấy 5 giá trị
  .toArray();

console.log(result); // [0, 4, 16, 36, 64]
```

### Ví dụ 2: `drop`, `flatMap`, `reduce`

```js
function* words() {
  yield 'apple pie';
  yield 'banana split';
  yield 'cherry cake';
}

const totalWords = words()
  .flatMap(sentence => sentence.split(' '))
  .reduce((count, word) => count + 1, 0);

console.log(totalWords); // 6

const skipFirstTwo = [1, 2, 3, 4, 5]
  .values()
  .drop(2)
  .toArray();
console.log(skipFirstTwo); // [3, 4, 5]
```

### Ví dụ 3: `some` / `every` / `find` — dừng sớm, không tiêu thụ hết

```js
function* counter() { let i = 1; while (true) yield i; }

const hasBig = counter().some(n => n > 3);
console.log(hasBig); // true — dừng ngay khi gặp 4

const firstBig = counter().find(n => n > 3);
console.log(firstBig); // 4

const allPositive = [1, 2, 3].values().every(n => n > 0);
console.log(allPositive); // true
```

### Ví dụ 4: Xử lý file/log lớn từng dòng (lazy)

```js
// Giả sử lines là generator đọc file từng dòng
function* readLines(fileText) {
  for (const line of fileText.split('\n')) yield line;
}

const errors = readLines(serverLog)
  .filter(line => line.includes('ERROR'))
  .take(100)          // chỉ cần 100 lỗi đầu — không scan tiếp
  .toArray();
```

> 📖 MDN: [Iterator](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Iterator) · [Iterator.prototype.map](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Iterator/map) · [take()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Iterator/take)

### Bẫy thường gặp với Iterator Helpers

```js
// 1. Iterator helper là one-shot — dùng lại sẽ rỗng
const it = [1, 2, 3].values().map(x => x * 2);
console.log([...it]); // [2, 4, 6]
console.log([...it]); // [] — đã hết!

// 2. Array method KHÔNG lazy — vẫn tạo mảng trung gian
[1, 2, 3].map(x => x * 2).filter(x => x > 2); // 2 mảng trung gian
[1, 2, 3].values().map(x => x * 2).filter(x => x > 2); // 0 mảng trung gian

// 3. Chỉ gọi được trên Iterator object, không phải iterable thô
[1, 2, 3].map(x => x);            // Array#map (eager, trên Array)
[1, 2, 3].values().map(x => x);   // Iterator#map (lazy)
```

## 2️⃣ Set Methods — phép toán tập hợp chuẩn toán học

**Vấn đề trước đây:** muốn union/intersection phải viết tay bằng `[...set].filter(...)` hoặc dùng Lodash.

**Giải pháp:** 7 method mới trên `Set.prototype`.

**Browser support:** Chrome 122+, Firefox 127+, Safari 17+, Node 22+ — [Baseline 2024](https://web.dev/blog/set-methods).

| Method | Trả về | Tương đương toán học |
|---|---|---|
| `union(other)` | Set các phần tử thuộc A hoặc B | A ∪ B |
| `intersection(other)` | Set thuộc cả A và B | A ∩ B |
| `difference(other)` | Set thuộc A nhưng không thuộc B | A \ B |
| `symmetricDifference(other)` | Set thuộc A hoặc B nhưng không cả hai | A △ B |
| `isSubsetOf(other)` | boolean — A ⊆ B? | ⊆ |
| `isSupersetOf(other)` | boolean — A ⊇ B? | ⊇ |
| `isDisjointFrom(other)` | boolean — A ∩ B = ∅? | rời nhau |

```js
const frontend = new Set(['js', 'css', 'html', 'react']);
const backend  = new Set(['js', 'node', 'sql', 'react']);

console.log(frontend.union(backend));
// Set {'js', 'css', 'html', 'react', 'node', 'sql'}

console.log(frontend.intersection(backend)); // Set {'js', 'react'}
console.log(frontend.difference(backend));   // Set {'css', 'html'}
console.log(frontend.symmetricDifference(backend)); // Set {'css', 'html', 'node', 'sql'}

console.log(frontend.isSubsetOf(backend));      // false
console.log(new Set(['js']).isSupersetOf(new Set(['js', 'react']))); // false
console.log(new Set(['html']).isDisjointFrom(new Set(['node'])));    // true
```

> 📖 MDN: [Set](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set) · [union()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set/union) · [intersection()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set/intersection) · [difference()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set/difference)

## 3️⃣ Promise.try() và Promise.withResolvers()

### Promise.try() — chuẩn hóa function thành promise

**Vấn đề:** function có thể throw lỗi **sync** hoặc trả promise — code xử lý không thống nhất.

```js
// ❌ Trước: nếu parseData throw sync → .catch() KHÔNG bắt được
function parseData(text) {
  return JSON.parse(text); // có thể throw Sync!
}

try {
  Promise.resolve(parseData(input)).then(console.log);
} catch (err) {
  // .catch ở chain không chạy, phải wrap try/catch thủ công
}
```

```js
// ✅ ES2025: Promise.try — mọi lỗi (sync hoặc async) đều vào .catch()
function parseData(text) {
  return JSON.parse(text);
}

Promise.try(parseData, '{"ok":true}')       // truyền cả arguments
  .then(data => console.log(data))           // { ok: true }
  .catch(err => console.error('Failed:', err.message));

// Dạng arrow: dùng khi cần closure
Promise.try(() => getUser(userId))
  .then(user => processUser(user))
  .catch(err => handleError(err));
```

**Browser support:** Chrome 122+, Firefox 128+, Safari 17.5+, Node 22+.
> 📖 MDN: [Promise.try()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/try)

### Promise.withResolvers() — resolve/reject tách riêng

**Vấn đề:** `new Promise(executor)` phải resolve/reject **bên trong executor**, không lấy được ra ngoài (cho event listener, timeout pattern...).

```js
// ❌ Trước: phải khai báo biến bên ngoài executor
let resolveRef, rejectRef;
const promise = new Promise((resolve, reject) => {
  resolveRef = resolve;   // gán ra ngoài — rườm rà
  rejectRef = reject;
});
```

```js
// ✅ ES2025: một dòng, gọn gàng
const { promise, resolve, reject } = Promise.withResolvers();

document.getElementById('submit-btn')
  .addEventListener('click', () => resolve('submitted'));

setTimeout(() => reject(new Error('Timeout!')), 5000);

promise
  .then(value => console.log(value))
  .catch(err => console.error(err.message));
```

**Use case kinh điển — flaky retry với external trigger:**

```js
function createDeferredQueue() {
  const pending = [];
  return {
    add() {
      const { promise, resolve, reject } = Promise.withResolvers();
      pending.push({ resolve, reject });
      return promise;
    },
    flushAll(value) { pending.forEach(p => p.resolve(value)); }
  };
}

const queue = createDeferredQueue();
const p1 = queue.add(); // chưa resolve — chờ flushAll
const p2 = queue.add();
queue.flushAll('done');
// p1, p2 giờ đều resolve 'done'
```

**Browser support:** Chrome 119+, Firefox 121+, Safari 17.4+, Node 22+ (ES2024).
> 📖 MDN: [Promise.withResolvers()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/withResolvers)

## 4️⃣ Object.groupBy() và Map.groupBy()

**Vấn đề:** nhóm (group) mảng theo key — phải viết reduce dài dòng.

**Browser support:** Chrome 117+, Firefox 119+, Safari 17.4+, Node 21+ (ES2024 — hay nhầm là ES2025).

```js
// ❌ Trước: reduce thủ công
const groupedOld = inventory.reduce((acc, item) => {
  (acc[item.type] ??= []).push(item);
  return acc;
}, {});

// ✅ Mới: Object.groupBy — key là string (coerced)
const inventory = [
  { name: 'asparagus', type: 'veg', qty: 5 },
  { name: 'bananas',   type: 'fruit', qty: 0 },
  { name: 'goat',      type: 'meat', qty: 23 },
  { name: 'cherries',  type: 'fruit', qty: 5 },
];

const result = Object.groupBy(inventory, ({ type }) => type);
// {
//   veg:   [{ name: 'asparagus', type: 'veg', qty: 5 }],
//   fruit: [{ name: 'bananas', ... }, { name: 'cherries', ... }],
//   meat:  [{ name: 'goat', ... }]
// }
```

```js
// ✅ Map.groupBy — key là GIÁ TRỊ BẤT KỲ (object, NaN, -0...)
const people = [
  { name: 'Alice', age: 21 },
  { name: 'Max',   age: 20 },
  { name: 'Jane',  age: 20 },
];

const byAge = Map.groupBy(people, ({ age }) => age);
console.log(byAge.get(20)); // [{ name: 'Max', ... }, { name: 'Jane', ... }]

// Key là object — Object.groupBy KHÔNG làm được
const minAge = { adult: 18, senior: 65 };
const byCategory = Map.groupBy(people, p =>
  p.age >= minAge.senior ? minAge : p.age >= minAge.adult ? 'adult' : 'minor'
);
```

**Khi nào dùng cái nào:**

| Tiêu chí | Object.groupBy | Map.groupBy |
|---|---|---|
| Kiểu key | String/Symbol (coerced) | Bất kỳ giá trị nào |
| Key số nguyên `1` | Chuyển thành `"1"` | Giữ nguyên `1` |
| Key object | Không (String coercion) | ✅ So theo reference |
| Destructuring | ❌ (prototype pollution risk) | ✅ An toàn |

> 📖 MDN: [Object.groupBy()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/groupBy) · [Map.groupBy()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map/groupBy)

## 5️⃣ RegExp.escape()

**Vấn đề:** nhúng chuỗi user-input vào regex → ký tự đặc biệt (`. * + ? ^ $ { } ( ) | [ ] \`) phá vỡ pattern, hoặc tệ hơn là tạo ReDoS/ injection.

```js
// ❌ Trước: tự viết helper — dễ sót ký tự
const userInput = 'a+b (c)';
const re = new RegExp(userInput);        // "a+b (c)" → + là quantifier → sai!
console.log(re.test('aab c'));           // true — pattern không phải literal

// Helper thủ công (chưa đầy đủ):
function escapeRegExp(string) {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}
```

```js
// ✅ ES2025: RegExp.escape() — chuẩn hóa, xử lý toàn bộ syntax chars
const userInput = 'a+b (c)';
const escaped = RegExp.escape(userInput);
console.log(escaped);       // 'a\\+b\\ \\(c\\)'

const re = new RegExp(escaped);
console.log(re.test('a+b (c)'));  // true — match literal chính xác
console.log(re.test('aab c'));    // false
```

**Use case thực tế — tìm chính xác chuỗi người dùng nhập:**

```js
function highlight(text, query) {
  const re = new RegExp(RegExp.escape(query), 'gi');
  return text.replace(re, match => `<mark>${query}</mark>`);
}

console.log(highlight('C++ and C# are languages', 'C++'));
// 'C++ and C# are languages' — chỉ C++ được bọc <mark>
```

**Browser support:** Chrome 123+, Firefox 127+, Safari 17.4+ — [Baseline 2025](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/RegExp/escape).

> 📖 MDN: [RegExp.escape()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/RegExp/escape)

## 6️⃣ ArrayBuffer Transfer (Transferable ArrayBuffer) — ES2024

Chuyển quyền sở hữu buffer mà **không copy dữ liệu** — O(1) thay vì O(n).

```js
// ✅ transfer(): move ownership, buffer gốc bị detached
const original = new Uint8Array([1, 2, 3]).buffer;
console.log(original.byteLength); // 3

const transferred = original.transfer();  // chuyển sang buffer mới
console.log(original.byteLength);         // 0 — detached!
console.log(transferred.byteLength);      // 3

// ✅ transferToFixedLength(): transfer với kích thước cố định
const fixed = new ArrayBuffer(8);
const moved = fixed.transferToFixedLength(4); // giữ nguyên pool cũ
```

**Use case:** Web Worker — chuyển dữ liệu binary lớn giữa threads không tốn chi phí serialize:

```js
const worker = new Worker('worker.js');
const buffer = new ArrayBuffer(1024 * 1024); // 1MB
worker.postMessage(buffer, [buffer]); // transfer list — zero-copy
// Sau postMessage, buffer ở main thread bị detached (byteLength === 0)
```

**Browser support:** Chrome 114+, Firefox 127+, Safari 17+, Node 18+.
> 📖 MDN: [ArrayBuffer.prototype.transfer()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/ArrayBuffer/transfer)

## 7️⃣ Float16Array

TypedArray lưu số thực **16-bit** (half precision) — giảm 50% bộ nhớ so với Float32Array, phù hợp AI/ML, GPU, WebGL/WebGPU nơi độ chính xác thấp chấp nhận được.

```js
const f16 = new Float16Array([1.5, 2.5, 3.14159, -100.75]);
console.log(f16[0]);              // 1
console.log(f16[2]);              // 3.140625 — mất chính xác (16-bit)
console.log(f16.byteLength);      // 8 (2 bytes/phần tử)

// Chuyển đổi số thường ↔ float16
console.log(Math.f16round(3.14159)); // 3.140625

const buffer = new ArrayBuffer(4);
const view = new DataView(buffer);
view.setFloat16(0, 1.5, true); // little-endian
console.log(view.getFloat16(0, true)); // 1.5
```

**Browser support:** Chrome 135+, Firefox 129+, Safari 18.2+, Node 22+.
> 📖 MDN: [Float16Array](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Float16Array) · [Math.f16round()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/f16round)

## 8️⃣ JSON.parse source text access (ES2026 — ship sớm)

Cho phép giữ nguyên **văn bản gốc** của số khi parse JSON — fix lỗi mất precision khi làm việc với ID/ timestamp lớn (VD: `12345678901234567890` → mất chính xác khi thành Number). Tính năng này đã có mặt trong các trình duyệt từ trước nhưng chính thức thuộc **ES2026**, không phải ES2025.

```js
const raw = '{"id": 12345678901234567890, "price": 19.99}';

// ✅ reviver với `source` — tham số thứ 3 mới
const parsed = JSON.parse(raw, (key, value, context) => {
  if (key === 'id') {
    console.log(context.source); // "12345678901234567890" — chuỗi GỐC
    return BigInt(context.source); // giữ độ chính xác
  }
  return value;
});
console.log(parsed.id); // 12345678901234567890n — không mất chữ số!
```

**Browser support:** Chrome 114+, Firefox 128+, Safari 17.4+.
> 📖 MDN: [JSON.parse()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON/parse) (tham khảo reviver với source)

## 9️⃣ Import Attributes & JSON Modules

Import file JSON (hoặc loại khác) như module với **attribute bắt buộc** để rõ kiểu — tránh nhầm binary/ parser khác nhau.

```js
// Static import — bắt buộc khai báo type
import config from './config.json' with { type: 'json' };
console.log(config.apiKey);

// Dynamic import
const data = await import('./data.json', { with: { type: 'json' } });
console.log(data.default);
```

```html
<!-- Trong DOM: -->
<script type="module">
  import theme from './theme.json' with { type: 'json' };
  document.body.style.background = theme.color;
</script>
```

**Lưu ý:** cú pháp cũ `assert { type: "json" }` (Stage 3) **đã bị thay** bằng `with` — `assert` sẽ bị loại bỏ dần. Nếu code cũ dùng `assert`, migrate sang `with`.

**Browser support:** Chrome 123+, Firefox 123+, Safari 17.2+, Node 22+ (`with` keyword).
> 📖 MDN: [Import attributes](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/import/with) · [JSON modules](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules#importing_modules_with_import_attributes)

## 🔟 Relative indexing — toSorted / toReversed / toSpliced / with (ES2023)

Các method **copy-on-write** — trả mảng mới, không mutate mảng gốc. Đây là "immutable flavor" của sort/reverse/splice.

```js
const arr = [5, 2, 9, 1, 7];

// ✅ toSorted — sort bản copy
console.log(arr.toSorted());        // [1, 2, 5, 7, 9]
console.log(arr.toSorted((a, b) => b - a)); // [9, 7, 5, 2, 1] (desc)
console.log(arr);                   // [5, 2, 1, 7, 9] — GỐC KHÔNG ĐỔI

// ✅ toReversed — reverse bản copy
console.log(arr.toReversed());      // [7, 1, 9, 2, 5]
console.log(arr);                   // gốc vẫn nguyên

// ✅ toSpliced — splice bản copy (không đổi gốc)
console.log(arr.toSpliced(1, 2, 'x', 'y')); // [5, 'x', 'y', 1, 7]
console.log(arr);                   // gốc không đổi

// ✅ with — thay phần tử tại index, trả mảng mới
console.log(arr.with(0, 'first'));  // ['first', 2, 1, 7, 9]

// ✅ Index âm được hỗ trợ — đếm từ cuối
console.log(arr.with(-1, 'last'));  // [5, 2, 1, 7, 'last']
console.log(arr.at(-1));            // 9 (đã có từ ES2022)
```

**Browser support:** Chrome 110+, Firefox 115+, Safari 16.4+, Node 20+.
> 📖 MDN: [Array.prototype.toSorted](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/toSorted) · [toReversed](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/toReversed) · [toSpliced](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/toSpliced) · [with](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/with)

## ⚠️ Bẫy thường gặp với ES2025

### Bẫy 1: Tính năng nhầm phiên bản
- `Object.groupBy`/`Map.groupBy` → **ES2024**, không phải ES2025.
- `Promise.withResolvers` → **ES2024**.
- Iterator Helpers, Set Methods, `Promise.try`, `RegExp.escape` → **ES2025** thật.
- Temporal → **ES2027** (đang Stage 3).

### Bẫy 2: Quên kiểm tra feature detection
```js
// ✅ Feature-detect trước khi dùng
if (typeof Iterator !== 'undefined' && Iterator.prototype.map) {
  // dùng iterator helpers
} else {
  // fallback: array methods hoặc polyfill core-js
}
```

### Bẫy 3: Object.groupBy key coercion
```js
const data = [{ id: 1 }, { id: 2 }];
const byId = Object.groupBy(data, ({ id }) => id);
console.log(Object.keys(byId)); // ['1', '2'] — keys đều là STRING
byId[1]   // vẫn work (coerce) nhưng byId['1'] cũng vậy
Map.groupBy(data, ({ id }) => id).get(1) // ✅ giữ nguyên number key
```

### Bẫy 4: Iterator helper one-shot
```js
const pipeline = [1, 2, 3].values().map(x => x * 2);
pipeline.toArray(); // [2, 4, 6]
pipeline.toArray(); // [] — iterator đã hết, KHÔNG dùng lại được
```

## 📊 Polyfill / Compatibility

```js
// Dùng core-js v3.33+ cho target cũ:
// import 'core-js/actual/iterator';
// import 'core-js/actual/set';
// import 'core-js/actual/promise';

// Hoặc feature detect thủ công
if (!Promise.try) {
  Promise.try = function (fn, ...args) {
    return new Promise((resolve, reject) => {
      try { resolve(fn(...args)); } catch (e) { reject(e); }
    });
  };
}
```

## 🔗 Liên kết chéo

- Xem thêm: `15_iterators-and-generators/` — iterator/generator nền tảng cho Iterator Helpers
- Xem thêm: `03_data-structures/` — Array, Map, Set chi tiết
- Xem thêm: `12_asynchronous-javascript/` — Promise cơ bản
- Xem thêm: `02_data-types/04_builtin-objects/03_regexp/` — RegExp API tổng hợp
- Xem thêm: `20_modern-javascript/` — tổng hợp ES6+ features
- Xem thêm: `03_data-structures/04_json` — JSON module import attributes
- Tài liệu: [ES2025 spec](https://tc39.es/ecma262/2025/), [TC39 finished proposals](https://github.com/tc39/proposals/blob/main/finished-proposals.md), [caniuse.com](https://caniuse.com)
