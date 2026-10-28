# ES2026 Features — Tính Năng Mới Trong ECMAScript 2026 — [Level: Intermediate]

> **ES2026 (ECMAScript 2026)** — edition kế tiếp của chuẩn ECMAScript, dự kiến được Ecma General Assembly phê duyệt tháng **06/2026**. Bản cập nhật này là "bộ sưu tập chất lượng cuộc sống" (quality-of-life): các API nhỏ, gọn, giải quyết đúng một vấn đề mỗi tính năng — từ async iterable → array, upsert cho Map, cộng số chính xác, kiểm tra Error, mã hóa Base64/Hex chuẩn ngôn ngữ, và ghép iterator.

> **Nguồn chính thức:** [TC39 Finished Proposals](https://github.com/tc39/proposals/blob/main/finished-proposals.md). Tất cả tính năng trong tài liệu này đều đã đạt **Stage 4** (chính thức vào chuẩn).

## 🔑 Khái niệm cốt lõi

ES2026 final hóa các proposal Stage 4 sau:

| Tính năng | Proposal | Mô tả |
|---|---|---|
| **`Array.fromAsync()`** | [proposal-array-from-async](https://github.com/tc39/proposal-array-from-async) | Tạo array từ async iterable / array-like — bản async của `Array.from()` |
| **Upsert — `Map.prototype.getOrInsert` / `getOrInsertComputed`** | [proposal-upsert](https://github.com/tc39/proposal-upsert) | Lấy giá trị theo key, chèn giá trị mặc định nếu chưa có |
| **`Math.sumPrecise()`** | [proposal-math-sum](https://github.com/tc39/proposal-math-sum) | Cộng dồn mảng số **không mất chính xác** trung gian |
| **`Error.isError()`** | [proposal-is-error](https://github.com/tc39/proposal-is-error) | Kiểm tra "giá trị này có phải Error thật không" — không thể bị giả mạo |
| **`Uint8Array.fromBase64()` / `.toBase64()` / `.fromHex()` / `.toHex()` / `.setFromBase64()` / `.setFromHex()`** | [proposal-arraybuffer-base64](https://github.com/tc39/proposal-arraybuffer-base64) | Chuyển đổi Base64 / Hex ↔ binary ngay trong ngôn ngữ |
| **Iterator Sequencing — `Iterator.concat()`** | [proposal-iterator-sequencing](https://github.com/tc39/proposal-iterator-sequencing) | Ghép nhiều iterator thành một, lazy |
| **JSON.parse source text access** | [proposal-json-parse-source-text-access](https://github.com/tc39/proposal-json-parse-source-text-access) | Reviver nhận `source` — văn bản gốc của số khi parse JSON |

> ⚠️ **Temporal KHÔNG thuộc ES2026.** Temporal đang ở **Stage 3** và được dự kiến đạt Stage 4 cho **ES2027**. Đừng tin các bài viết ghi "Temporal ra mắt trong ES2026" — xem [proposal-temporal](https://github.com/tc39/proposal-temporal).

## 📐 Browser Support (tham khảo — kiểm tra caniuse trước khi dùng)

| Tính năng | Chrome | Firefox | Safari | Node.js |
|---|---|---|---|---|
| `Array.fromAsync` | 134+ | 137+ | 18.4+ | 24+ |
| `Map.getOrInsert` / `getOrInsertComputed` | 136+ | 139+ | 18.4+ | 24+ |
| `Math.sumPrecise` | 132+ | 135+ | 18.2+ | 24+ |
| `Error.isError` | 135+ | 137+ | 18.4+ | 24+ |
| Uint8Array Base64/Hex | 140+ | 133+ | 18.2+ | 24+ |
| `Iterator.concat` | 138+ | 139+ | 18.4+ | 24+ |
| JSON.parse source text | 114+ | 128+ | 17.4+ | 21+ |

> Bảng trên mang tính tham khảo tại thời điểm viết. Phiên bản chính xác có thể khác giữa các engine — luôn kiểm tra [caniuse.com](https://caniuse.com) hoặc [MDN](https://developer.mozilla.org/) trước khi dùng production, và dùng feature detection.

## 1️⃣ Array.fromAsync() — bản async của Array.from()

**Vấn đề trước đây:** muốn thu thập giá trị từ async iterator (hoặc array của Promise) thành mảng, bạn phải viết vòng lặp tay:

```js
// Truoc ES2026: phai viet vong lap thu cong
const result = [];
for await (const chunk of stream) {
  result.push(chunk);
}
```

```js
// ES2026: mot dong
const result = await Array.fromAsync(stream);

// Tu mang Promise -> mang gia tri (chay tuan tu, khac Promise.all song song)
const promises = [fetch(url1), fetch(url2)];
const responses = await Array.fromAsync(promises);

// Async generator vo han + mapAsync khong ton bo nho
async function* fetchPages(urls) {
  for (const url of urls) yield fetch(url);
}
const pages = await Array.fromAsync(fetchPages(apiUrls));
```

**Khác biệt với `Promise.all`:**

| Tiêu chí | `Array.fromAsync(iterableOfPromises)` | `Promise.all(iterableOfPromises)` |
|---|---|---|
| Async iterator (`for await`) | ✅ Hoạt động | ❌ Không (không await từng giá trị) |
| Async generator | ✅ | ❌ |
| Sync iterable chứa Promise | ✅ (await từng cái, tuần tự) | ✅ (song song) |
| Thứ tự thực thi | **Tuần tự** — await từng giá trị | **Song song** — tất cả cùng lúc |
| Kết quả | Array giá trị | Array giá trị |

> 📖 MDN: [Array.fromAsync()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/fromAsync)

### Ví dụ thực tế: đọc toàn bộ file lớn theo từng dòng

```js
// Doc file theo dong ma khong phai load ca file vao bo nho
async function* lines(file) {
  const reader = file.stream().getReader();
  const decoder = new TextDecoder();
  let buffer = '';
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    const parts = buffer.split('\n');
    buffer = parts.pop();
    for (const line of parts) yield line;
  }
  if (buffer) yield buffer;
}

// Dem so loi trong log 10GB — bo nho chi giu 1 dong tai mot thoi diem
const errorCount = (await Array.fromAsync(lines(logFile)))
  .filter(l => l.includes('ERROR')).length;
```

**Bẫy thường gặp:**

```js
// 1. Array.fromAsync la ASYNC — quen await se nhan ve Promise, khong phai array
const wrong = Array.fromAsync(gen);   // Promise<Array>
const right = await Array.fromAsync(gen); // Array

// 2. Array.fromAsync KHÔNG truyền mapFn như Array.from
// Array.from(arr, mapFn) ✅ | Array.fromAsync(arr, mapFn) ❌ — map bằng for-await bên ngoài

// 3. Với iterable chứa Promise, thực thi TUẦN TỰ — cần song song thì dùng Promise.all
await Array.fromAsync([slow(), slow()]);      // mỗi promise chờ cái trước xong mới chạy
await Promise.all([slow(), slow()]);          // cả hai chạy đồng thời
```

## 2️⃣ Upsert — Map.prototype.getOrInsert() / getOrInsertComputed()

**Vấn đề trước đây:** pattern "lấy từ Map, nếu chưa có thì tạo mới rồi set" xuất hiện khắp nơi trong code JS — nhưng phải viết 3 dòng lặp đi lặp lại (và đọc Map 2 lần):

```js
// Truoc ES2026: pattern "upsert" viet tay — lap lai khap noi
const groups = new Map();
if (groups.has(key)) {
  groups.get(key).push(item);
} else {
  groups.set(key, [item]);
}

// Hoặc phiên bản ngắn nhưng khó đọc:
const list = groups.get(key) ?? [];
list.push(item);
groups.set(key, list); // đọc + ghi 2 lần
```

```js
// ES2026: getOrInsert — neu chua co key, chen defaultValue va tra ve
const list = groups.getOrInsert(key, []);
list.push(item); // list chính là giá trị trong Map — không cần set lại

// getOrInsertComputed — giá trị mặc định được tính từ key (lazy)
const cache = new Map();
const conn = cache.getOrInsertComputed(dbUrl, url => createConnection(url));
// callback CHỈ chạy khi key chưa tồn tại
```

**So sánh các cách tiếp cận:**

| Cách | Đọc Map bao nhiêu lần | Tính default khi key đã có? | Gọn? |
|---|---|---|---|
| `has` + `get` + `set` | 2–3 lần | Có (dù không dùng) | ❌ |
| `get` + `??` + `set` | 2 lần | Có | ⚠️ |
| `getOrInsert(key, value)` | 1 lần | Có — value được tạo sẵn | ✅ |
| `getOrInsertComputed(key, fn)` | 1 lần | ❌ — chỉ tính khi cần | ✅✅ |

**Use case kinh điển — grouping (thay cho Object.groupBy khi cần Map):**

```js
const byDepartment = new Map();
for (const emp of employees) {
  byDepartment.getOrInsertComputed(emp.dept, () => []).push(emp);
}
```

### Polyfill cho môi trường cũ

```js
if (!Map.prototype.getOrInsert) {
  Map.prototype.getOrInsert = function (key, value) {
    if (!this.has(key)) this.set(key, value);
    return this.get(key);
  };
  Map.prototype.getOrInsertComputed = function (key, callbackfn) {
    if (!this.has(key)) this.set(key, callbackfn(key));
    return this.get(key);
  };
}
```

> 📖 MDN: [Map.prototype.getOrInsert()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map/getOrInsert) · [getOrInsertComputed()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map/getOrInsertComputed)

**Bẫy thường gặp:**

```js
// getOrInsert LUÔN tạo giá trị default trước khi kiểm tra — object/array tốn kém
map.getOrInsert(key, expensiveBuild());            // expensiveBuild() CHẠY DÙ key đã có
map.getOrInsertComputed(key, expensiveBuild);      // chỉ chạy khi cần ✅

// getOrInsertComputed trả về giá trị đã có trong map (không gọi callback) —
// nhưng callback vẫn nhận key làm tham số: callbackfn(key)
```

## 3️⃣ Math.sumPrecise() — cộng số không mất chính xác

**Vấn đề trước đây:** `reduce((a, b) => a + b, 0)` với mảng số thực có thể trả kết quả sai nổi tiếng:

```js
// Bai toan kinh dien cua floating point
[0.1, 0.2].reduce((a, b) => a + b, 0);
// 0.30000000000000004 ❌

// Cộng dồn nhiều số → sai số tích lũy
[0.1, 0.2, 0.3].reduce((a, b) => a + b, 0);
// 0.6000000000000001 ❌
```

```js
// ES2026: Math.sumPrecise — cong chinh xac nhat co hoc
Math.sumPrecise([0.1, 0.2]);
// 0.3 ✅

Math.sumPrecise([0.1, 0.2, 0.3]);
// 0.6 ✅

// Hoạt động với mọi số float, trả về đúng số học IEEE 754 "tốt nhất có thể"
Math.sumPrecise([1e308, 1, -1e308]);
// 0 — giải thuật Neumaier/Shewchuk tránh mất số nhỏ khi cộng với số lớn
```

**Cách hoạt động bên trong:** thay vì cộng tuần tự từng cặp (mỗi phép cộng làm tròn một lần), `Math.sumPrecise` dùng giải thuật compensated summation — giữ phần "số dư" bị làm tròn rồi cộng lại sau. Kết quả là tổng **chính xác đến số thực gần nhất** của tổng toán học.

**Use case thực tế:**

```js
// Tính tổng tiền (float money) — sai số 1e-15 cũng có thể thành bug
const total = Math.sumPrecise(cart.map(i => i.price));

// Thống kê: trung bình cộng chính xác
const avg = Math.sumPrecise(measurements) / measurements.length;
```

**Lưu ý:**

```js
// Nhận iterable, KHÔNG phải rest args
Math.sumPrecise(1, 2);        // NaN? — KHÔNG dùng kiểu này
Math.sumPrecise([1, 2]);      // 3 ✅

// Mảng rỗng trả về -0 (theo spec), không phải 0
Math.sumPrecise([]); // -0

// Chỉ dùng cho Number — BigInt cộng bằng reduce như cũ
```

> 📖 MDN: [Math.sumPrecise()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/sumPrecise)

## 4️⃣ Error.isError() — kiểm tra Error "thật"

**Vấn đề trước đây:** cách kiểm tra phổ biến `value instanceof Error` **sai trong 3 trường hợp**:

1. **Cross-realm:** Error tạo từ iframe khác / vm context → prototype khác → `instanceof Error` trả `false` dù là Error thật.
2. **Giả mạo:** object tự set `Symbol.hasInstance` hoặc kế thừa để qua mặt kiểm tra.
3. **Serialization:** Error đi qua `postMessage`/`structuredClone` có thể mất prototype.

```js
// Truoc ES2026: cach kiem tra de bi qua mat
function handleError(err) {
  if (err instanceof Error) { ... } // sai voi cross-realm, co the bi gia mao
  if (err && err.stack) { ... }     // moi object co .stack deu "la error"?
}
```

```js
// ES2026: Error.isError — kiem tra theo tag nội bộ của engine
Error.isError(new Error('x'));        // true
Error.isError(new TypeError('x'));    // true
Error.isError('Error');               // false
Error.isError({ name: 'Error', message: 'x', stack: '...' }); // false — giả mạo không qua được
Error.isError(iframeWindow.Error('x')); // true ✅ — cross-realm vẫn đúng
```

**Use case thực tế — xử lý rejection an toàn:**

```js
window.addEventListener('unhandledrejection', (event) => {
  const reason = event.reason;
  if (Error.isError(reason)) {
    reportToSentry(reason);           // có stack thật
  } else {
    reportToSentry(new Error(String(reason))); // bọc lại để có stack
  }
});
```

> 📖 MDN: [Error.isError()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error/isError)

**Bẫy thường gặp:**

```js
// Không thay thế được try/catch — vẫn chỉ dùng để phân loại giá trị
// Không nhận diện được error-like object (throw 'string' là hợp lệ!)
try {
  throw 'just a string'; // hợp lệ trong JS
} catch (e) {
  Error.isError(e); // false — vì nó THẬT SỰ không phải Error
}
```

## 5️⃣ Uint8Array Base64/Hex — mã hóa binary chuẩn ngôn ngữ

**Vấn đề trước đây:** để encode/decode Base64 với binary data, bạn phải đi vòng qua **string** và API của trình duyệt (`btoa`/`atob` chỉ tồn tại trên window, xử lý sai với byte > 127), hoặc cài thư viện ngoài. Node.js thì có `Buffer` — nhưng đó là API riêng của Node, không phải chuẩn JS.

```js
// Truoc ES2026: vòng vèo qua string, dễ sai với binary
const bin = new Uint8Array([72, 105]);

// Browser: btoa chỉ nhận "binary string"
const b64 = btoa(String.fromCharCode(...bin)); // 'SGk='

// Byte lớn > 127 sẽ SAI nếu không cẩn thận:
const bytes = new Uint8Array([200]);
btoa(String.fromCharCode(...bytes)); // ✔ nhưng String.fromCharCode với mảng lớn → stack overflow
// Node: Buffer.from(bytes).toString('base64') — không chuẩn ECMAScript
```

```js
// ES2026: mot bo API hoan chinh tren Uint8Array

// === Base64 ===
const bytes = Uint8Array.fromBase64('SGVsbG8=');       // decode: base64 -> Uint8Array
const out = bytes.toBase64();                           // encode: Uint8Array -> 'SGVsbG8='

// Options: alphabet (base64 / base64url), lastChunkHandling
const urlSafe = bytes.toBase64({ alphabet: 'base64url', omitPadding: true });
const back = Uint8Array.fromBase64(urlSafe, { alphabet: 'base64url' });

// Ghi trực tiếp vào buffer có sẵn (không cấp phát mảng mới):
const target = new Uint8Array(16);
const { read, written } = target.setFromBase64(b64String);
// read: số ký tự base64 đã tiêu thụ, written: số byte đã ghi

// === Hex ===
const hex = bytes.toHex();            // '48656c6c6f'
const fromHex = Uint8Array.fromHex('48656c6c6f');
const target2 = new Uint8Array(8);
target2.setFromHex('48656c6c6f');     // ghi vào buffer sẵn có
```

**Tổng hợp API:**

| Method | Chức năng | Static/Instance |
|---|---|---|
| `Uint8Array.fromBase64(string, opts?)` | Base64 → Uint8Array mới | static |
| `Uint8Array.prototype.setFromBase64(string, opts?)` | Base64 → ghi vào buffer hiện có | instance |
| `Uint8Array.prototype.toBase64(opts?)` | Uint8Array → chuỗi Base64 | instance |
| `Uint8Array.fromHex(string)` | Hex → Uint8Array mới | static |
| `Uint8Array.prototype.setFromHex(string)` | Hex → ghi vào buffer hiện có | instance |
| `Uint8Array.prototype.toHex()` | Uint8Array → chuỗi Hex | instance |

**Options cho Base64:**

| Option | Giá trị | Ý nghĩa |
|---|---|---|
| `alphabet` | `"base64"` (mặc định) \| `"base64url"` | Base64 chuẩn (có `+/`) hay URL-safe (`-_`) |
| `omitPadding` | boolean | Bỏ dấu `=` đệm cuối |

**Use case thực tế:**

```js
// Web Crypto: tai sao can API nay?
const key = await crypto.subtle.generateKey({ name: 'AES-GCM', length: 256 }, true, ['encrypt']);
const raw = await crypto.subtle.exportKey('raw', key);
const keyB64 = new Uint8Array(raw).toBase64(); // luu vao DB / in ra config

// Decode khi nhan tu server (JWT payload, data URI...)
const payload = Uint8Array.fromBase64(token.split('.')[1]);

// So sánh 2 hash an toàn (timing-safe hơn là so chuỗi hex trực tiếp)
const hash1 = new Uint8Array(await crypto.digest('SHA-256', data)).toHex();
```

> 📖 MDN: [Uint8Array.fromBase64()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Uint8Array/fromBase64) · [toBase64()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Uint8Array/toBase64) · [toHex()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Uint8Array/toHex)

**Bẫy thường gặp:**

```js
// 1. setFromBase64 / setFromHex CẦN buffer đủ lớn và độ dài chẵn (hex: 2 ký tự = 1 byte)
const buf = new Uint8Array(3);
buf.setFromHex('aabbccddeeff'); // ✅ ghi 3 bytes, trả { read, written }

// 2. Chuỗi base64 chứa khoảng trắng/ký tự sai → throw (không như atob bỏ qua im lặng)
Uint8Array.fromBase64('SGk=!'); // throws SyntaxError

// 3. Chỉ có trên Uint8Array — không có trên DataView/ArrayBuffer
```

## 6️⃣ Iterator Sequencing — Iterator.concat()

**Vấn đề trước đây:** muốn duyệt tuần tự nhiều iterator/iterable bằng một vòng lặp, phải spread (mất lazy + tốn bộ nhớ) hoặc dùng generator trung gian:

```js
// Truoc ES2026
const combined = [...setA, ...setB, ...moreValues]; // copy tất cả vào mảng — KHÔNG lazy
// hoặc:
function* concat(...iters) {
  for (const it of iters) yield* it;
}
```

```js
// ES2026: Iterator.concat — ghep lazy, mot dong, chuan
const combined = Iterator.concat(list1.values(), list2.values(), generator());
for (const item of combined) {
  console.log(item); // duyệt list1 hết → list2 → generator, KHÔNG tạo mảng trung gian
}

// Kết hợp với iterator helpers (ES2025) — toàn pipeline lazy
Iterator.concat(a, b)
  .filter(x => x.active)
  .map(x => x.name)
  .take(10)
  .toArray();
```

**Điểm mạnh:** giữ tính **lazy** — phần tử chỉ được tính khi duyệt tới. Hợp với chuỗi dữ liệu lớn/vô hạn, phân trang:

```js
// Doc ket qua tu nhieu trang API nhu mot stream duy nhat
function* paginate() {
  for (const page of pages) yield* fetchPage(page);
}
const firstTen = Iterator.concat(page1Items, page2Items, morePages())
  .filter(i => i.active)
  .take(10)
  .toArray(); // chỉ fetch/duyệt đủ 10 phần tử đầu
```

> 📖 MDN: [Iterator.concat()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Iterator/concat)

**Bẫy thường gặp:**

```js
// 1. Tham số là iterator/iterable — KHÔNG phải giá trị
Iterator.concat([1, 2], [3, 4]); // ❌ array là iterable nhưng concat bọc từng PHẦN TỬ?
// Đúng: phải truyền iterator:
Iterator.concat([1, 2].values(), [3, 4].values()).toArray(); // [1, 2, 3, 4]

// 2. Kết quả là iterator mới — dùng một lần (one-shot), như mọi iterator helpers
```

## 7️⃣ JSON.parse source text access (nhắc lại — thuộc ES2026)

Đã được trình duyệt hỗ trợ từ trước (Chrome 114+), nhưng chính thức thuộc **ES2026**, không phải ES2025 như nhiều tài liệu ghi. Reviver của `JSON.parse` nhận tham số thứ 3 là `context.source` — văn bản gốc của giá trị số:

```js
const raw = '{"id": 12345678901234567890, "price": 19.99}';

const parsed = JSON.parse(raw, (key, value, context) => {
  if (key === 'id') return BigInt(context.source); // giu nguyen chu so
  if (key === 'price') return Number(context.source);
  return value;
});

console.log(parsed.id); // 12345678901234567890n — khong mat do chinh xac
```

> Chi tiết đầy đủ đã trình bày trong [`22_es2025-features/README.md`](../22_es2025-features/README.md) (mục 8) — tính năng này **ship sớm hơn edition của nó**, một hiện tượng phổ biến (như `Array.prototype.at` ship từ ES2022 nhưng có mặt trên trình duyệt từ 2021).

## ⚠️ Sắp xếp phiên bản — ES2025 / ES2026 / ES2027

Đây là bảng "ai thuộc version nào" — hay bị nhầm lẫn trong các bài viết:

| Tính năng | Phiên bản | Ghi chú |
|---|---|---|
| Iterator Helpers, Set Methods, `Promise.try`, `RegExp.escape`, Import Attributes, `Float16Array` | **ES2025** | |
| `Array.fromAsync`, `Map.getOrInsert` (Upsert), `Math.sumPrecise`, `Error.isError`, Uint8Array Base64/Hex, `Iterator.concat`, JSON.parse source text | **ES2026** | |
| **Temporal** | **ES2027** (dự kiến) | Hiện Stage 3 |
| Iterator chunking (`chunk`/`windowed`), `Iterator.includes`/`join`, `Iterator.zip`, Explicit Resource Management (`using`), `Atomics.pause` | **ES2027** (dự kiến) | Đã Stage 4, chờ ES2027 |

> 💡 Lưu ý: nhiều tính năng **ship trên trình duyệt trước khi edition chứa nó phát hành** (được gọi là "shipping ahead of ratification"). Việc một tính năng chạy được trên Chrome KHÔNG có nghĩa là nó thuộc ES hiện hành — hãy tra [TC39 finished proposals](https://github.com/tc39/proposals/blob/main/finished-proposals.md) theo cột "Expected Publication Year".

## ✅ Tổng kết — khi nào dùng gì

| Nhu cầu | Dùng |
|---|---|
| Thu thập async iterator thành mảng | `await Array.fromAsync(gen)` |
| Song song + nhanh | `Promise.all([...])` |
| Lấy hoặc tạo giá trị trong Map | `map.getOrInsertComputed(key, () => ...)` |
| Cộng số float chính xác | `Math.sumPrecise([...])` |
| Kiểm tra giá trị có phải Error | `Error.isError(x)` |
| Encode/decode Base64 hoặc Hex của binary | `Uint8Array.fromBase64` / `.toBase64` / `.fromHex` / `.toHex` |
| Ghép nhiều iterator thành một (lazy) | `Iterator.concat(...)` |
| Giữ văn bản gốc số khi parse JSON | `JSON.parse(text, (k, v, ctx) => ctx.source)` |
| Ngày tháng / múi giờ phức tạp | Chưa có — chờ **Temporal (ES2027)**, tạm dùng [Temporal polyfill](https://github.com/js-temporal/temporal-polyfill) |

## 🎯 Bài tập tự luyện

1. Viết hàm `groupByToMap(items, keyFn)` dùng `getOrInsertComputed` — so sánh với `Map.groupBy` của ES2024, khi nào nên dùng cái nào?
2. Đọc một file log lớn bằng async generator + `Array.fromAsync`, đếm số dòng ERROR mà không load cả file vào RAM.
3. Cho mảng 1 triệu số thực ngẫu nhiên: so sánh kết quả `reduce((a,b)=>a+b)` và `Math.sumPrecise` — tìm trường hợp chênh lệch.
4. Viết hàm chuyển đổi `ArrayBuffer` ↔ Base64 URL-safe dùng API mới, không dùng `btoa`/`Buffer`.
5. Dùng `Iterator.concat` + `take` để lấy 10 phần tử đầu từ 3 nguồn dữ liệu mà không ghép mảng trung gian.
6. Kiểm tra: `Error.isError` trả gì với `new DOMException()`, object giả mạo có `stack`, và Error từ iframe?

## 🔗 Liên kết chéo

- Xem thêm: `22_es2025-features/README.md` — Iterator Helpers (nền tảng cho `Iterator.concat`), Set Methods, `Promise.try`
- Xem thêm: `03_data-structures/01_arrays/` — Array.from, spread
- Xem thêm: `03_data-structures/02_keyed-collections/` — Map chi tiết
- Xem thêm: `12_asynchronous-javascript/` — Promise, async/await
- Xem thêm: `03_data-structures/03_typed-arrays/` — Uint8Array, ArrayBuffer
- Tài liệu: [TC39 finished proposals](https://github.com/tc39/proposals/blob/main/finished-proposals.md) · [ES2026 draft spec](https://tc39.es/ecma262/) · [caniuse.com](https://caniuse.com)
