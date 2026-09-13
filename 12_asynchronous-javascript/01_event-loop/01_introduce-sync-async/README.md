# Giới thiệu Synchronous và Asynchronous — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

**Lập trình đồng bộ (synchronous)**: code chạy từng dòng một theo thứ tự viết; mỗi dòng phải xử lý xong mới đến dòng tiếp theo. Nếu một hàm chạy lâu (ví dụ đọc file, gọi mạng), mọi thứ phía sau phải **đứng chờ** — chương trình bị chặn.

**Lập trình bất đồng bộ (asynchronous)**: chương trình có thể **bắt đầu** một tác vụ dài rồi **trả quyền điều khiển ngay lập tức**, tiếp tục đáp ứng các sự kiện khác. Khi tác vụ hoàn thành, kết quả được thông báo qua callback/promise.

JavaScript là ngôn ngữ **single-threaded** — chỉ có một call stack. Để xử lý bất đồng bộ mà không chặn luồng chính, JS dựa vào **Web APIs** (browser) hoặc **libuv** (Node.js) để offload các tác vụ dài, rồi đưa callback vào queue khi xong.

Cơ chế này hoạt động như sau:
1. Code đồng bộ chạy trên **Call Stack** (ngăn xếp LIFO).
2. Gặp tác vụ bất đồng bộ → đẩy sang **Web APIs** (timer, network, DOM).
3. Web APIs xử lý xong → đưa callback vào **Task Queue** hoặc **Microtask Queue**.
4. **Event Loop** liên tục kiểm tra: nếu Call Stack trống → lấy callback từ queue đưa vào stack.
5. Lặp lại vô tận.

**Hiểu đúng bản chất:** asynchronous KHÔNG có nghĩa là "chạy song song nhiều thread" — JS vẫn đơn luồng. Nó có nghĩa là **không chặn** — trong lúc chờ tác vụ dài, engine có thể làm việc khác.

## 📐 Cấu trúc / Cú pháp

### So sánh sync vs async

| Đặc tính | Synchronous | Asynchronous |
|----------|-------------|--------------|
| Thứ tự thực thi | Theo dòng code | Không theo dòng code |
| Chặn thread | Có | Không |
| UI response | Đứng hình khi chờ | Vẫn responsive |
| Complexity | Thấp | Cao (cần hiểu event loop) |
| Error handling | Try/catch | `.catch()` / `try/catch` async |
| Readability | Cao | Thấp hơn (callback hell) |
| Debugging | Dễ | Khó hơn (stack trace phức tạp) |
| Resource usage | Idle thời gian chờ | Tận dụng thời gian chờ |

### Timeline visual — so sánh rõ ràng

```
SYNC:   [──── A ────][──── B ────][──── C ────]
        thời gian →

ASYNC:  [── A start ──][── B start ──][── C start ──]
                              ↓              ↓
         [── A result ───────────────────────][── B result ──][── C result ──]
                              thời gian →
```

### Các dạng async phổ biến trong JS

| Dạng | Ví dụ | Cơ chế |
|------|-------|--------|
| **Timer** | `setTimeout`, `setInterval` | Macrotask queue |
| **Network** | `fetch`, `XMLHttpRequest` | Web API → callback |
| **DOM Event** | `addEventListener` | Event queue |
| **Promise** | `.then()`, `await` | Microtask queue |
| **I/O** | `fs.readFile` (Node) | libuv thread pool |
| **Animation** | `requestAnimationFrame` | Browser repaint cycle |

## ✅ Điểm mạnh — Tại sao nên dùng

1. **UI không bị "đứng hình"** khi chờ dữ liệu/timer — trải nghiệm người dùng tốt hơn.
2. **Nhiều tác vụ chờ** (network, I/O) có thể chạy đan xen, tận dụng tối đa thời gian rảnh của CPU.
3. **Nền tảng** để hiểu callback, promise, async/await — các khái niệm quan trọng nhất trong JS hiện đại.
4. **Event handler phản ứng tức thì** với người dùng — click, scroll không blocking main thread.
5. **Parallel operations** — nhiều request cùng lúc với `Promise.all`, tiết kiệm thời gian đáng kể.
6. **Better resource utilization** — CPU không idle chờ I/O, tăng throughput.
7. **Scalable** — cùng một server có thể phục vụ nhiều client đồng thời nhờ non-blocking I/O.
8. **Real-time capabilities** — WebSocket, Server-Sent Events cho ứng dụng realtime.

## ⚠️ Bẫy thường gặp & Hạn chế

### Bẫy 1: Kết quả in ra không theo thứ tự khai báo

```js
console.log("Start");
fetch("/api").then(data => console.log("Data:", data));
console.log("End");
// Output: Start → End → Data: ... (Data đến sau, không phải giữa)
// Nguyên nhân: fetch là async, callback vào microtask queue
```

### Bẫy 2: Code đồng bộ đơn giản nhưng nguy hiểm khi tác vụ lâu

```js
// Đồng bộ fetch (nếu có) sẽ đóng băng browser
const data = syncFetch("/api"); // ❌ blocking — browser đơ cho đến khi xong
console.log(data); // chỉ chạy sau khi fetch xong
// Trong browser thật: không có sync fetch, nhưng sync XHR thì có
```

### Bẫy 3: Callback hell — code lồng nhau thành kim tự tháp

```js
step1(function(result1) {
  step2(result1, function(result2) {
    step3(result2, function(result3) {
      step4(result3, function(result4) {
        // pyramid of doom — khó đọc, khó debug, khó test
      });
    });
  });
});
```

### Bẫy 4: `await` chỉ dùng được trong hàm `async`

```js
const data = await fetch("/api"); // ❌ SyntaxError outside async
// Fix: wrap trong async function
async function main() {
  const data = await fetch("/api");
}
```

### Bẫy 5: Async function luôn trả về Promise

```js
async function getData() {
  return "hello";
}
const result = getData();
console.log(result); // Promise { 'hello' } — không phải "hello"!
// Phải await hoặc .then() mới lấy được value
```

### Bẫy 6: Race condition — thứ tự không đảm bảo

```js
fetch("/api/a").then(data => console.log("A:", data));
fetch("/api/b").then(data => console.log("B:", data));
// Không biết A hay B in trước — phụ thuộc network latency
```

## 💡 Khi nào dùng — Tình huống thực tế

1. **Mọi tác vụ mạng, file, timer** — không nên đồng bộ hóa. Đây là use case phổ biến nhất.
2. **Lắng nghe hành vi người dùng** (click, input, scroll) — async theo bản chất, chờ event.
3. **Khi cần đáp ứng nhanh**: autocomplete (debounce), tải dữ liệu nền, chat realtime.
4. **Batch processing** — xử lý nhiều task song song với `Promise.all`.
5. **Real-time data** — WebSocket, Server-Sent Events cho live updates.
6. **File upload/download** — cần progress tracking, không chặn UI.
7. **Cron jobs / scheduled tasks** — `setInterval` cho polling định kỳ.
8. **Animation** — `requestAnimationFrame` thay vì `setInterval` cho smooth 60fps.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Synchronous — chạy tuần tự

```js
// Đồng bộ: mỗi dòng phải xong mới đến dòng sau
const name = "Miriam";
const greeting = `Hello, my name is ${name}!`;
console.log(greeting); // Hello, my name is Miriam!

const sum = 0;
for (let i = 0; i < 1000000; i++) {
  sum += i; // tính toán đồng bộ, có thể chậm
}
console.log("Sum:", sum); // chỉ chạy sau loop
// Tổng thứ tự: greeting → Sum (dễ dự đoán)
```

### Ví dụ 2: Asynchronous với Promise — kết quả đến sau

```js
// Bất đồng bộ: fetch không chặn, kết quả đến sau
console.log("Fetching...");
fetch("https://jsonplaceholder.typicode.com/posts/1")
  .then((res) => res.json())
  .then((post) => console.log("Title:", post.title))
  .catch((err) => console.error("Error:", err));
console.log("Request sent, continuing...");
// Output: Fetching... → Request sent, continuing... → Title: ...
// Promise là microtask → chạy sau sync code, trước macrotask
```

### Ví dụ 3: Asynchronous với setTimeout — macrotask

```js
console.log("Start");
setTimeout(() => {
  console.log("Timer fired after 2 seconds");
}, 2000);
console.log("End");
// Start → End → (2 giây sau) Timer fired...
// setTimeout là macrotask → chạy sau mọi microtask
```

### Ví dụ 4: Async/await — đọc như synchronous

```js
async function loadData() {
  console.log("Loading...");
  const res = await fetch("https://jsonplaceholder.typicode.com/posts/1");
  const data = await res.json();
  console.log("Title:", data.title);
  console.log("Done");
}
loadData();
// Loading... → (wait) → Title: ... → Done
// Code trông giống sync nhưng thực tế vẫn async
```

### Ví dụ 5: Parallel async operations — Promise.all

```js
async function loadDashboard() {
  console.log("Loading dashboard...");
  const [postsRes, usersRes, statsRes] = await Promise.all([
    fetch("/api/posts"),
    fetch("/api/users"),
    fetch("/api/stats")
  ]);
  const [posts, users, stats] = await Promise.all([
    postsRes.json(),
    usersRes.json(),
    statsRes.json()
  ]);
  renderDashboard(posts, users, stats);
  // 3 requests chạy song song, chờ tất cả xong rồi render
}
```

### Ví dụ 6: So sánh sequential vs parallel

```js
// Sequential — chậm: 3s + 2s + 1s = 6s
async function slow() {
  const a = await fetch("/api/a"); // 3s
  const b = await fetch("/api/b"); // 2s
  const c = await fetch("/api/c"); // 1s
}

// Parallel — nhanh: max(3,2,1) = 3s
async function fast() {
  const [a, b, c] = await Promise.all([
    fetch("/api/a"),
    fetch("/api/b"),
    fetch("/api/c")
  ]);
}
```

### Ví dụ 7: Event handler — async tự nhiên

```js
document.getElementById("btn").addEventListener("click", async () => {
  console.log("Button clicked!"); // chạy ngay
  const data = await fetch("/api/data"); // không chặn button khác
  console.log("Data loaded:", await data.json());
});
// User vẫn có thể click button khác trong lúc chờ fetch
```

### Ví dụ 8: Debounce pattern — async utility

```js
function debounce(fn, delay) {
  let timer;
  return function (...args) {
    clearTimeout(timer); // hủy timer cũ
    timer = setTimeout(() => {
      fn.apply(this, args); // gọi sau delay ms
    }, delay);
  };
}

const search = debounce((query) => {
  console.log("Searching:", query);
}, 300);

// Input "hello" → chỉ log "Searching: hello" sau 300ms kể từ keystroke cuối
search("h");
search("he");
search("hel");
search("hell");
search("hello");
```

## 🔬 So sánh với alternatives

| Cách tiếp cận | Sync hay Async | Ưu điểm | Nhược điểm | Phù hợp khi |
|---------------|----------------|---------|------------|-------------|
| Direct code | Sync | Đơn giản, dễ đọc | Chặn thread | Tính toán nhanh, không I/O |
| Callback | Async | Simple, mọi browser | Callback hell, khó test | Legacy code, simple cases |
| Promise | Async | Chainable, error handling | Syntax dài hơn async/await | API calls, complex flows |
| Async/Await | Async | Đọc như sync, dễ debug | Chỉ trong async function | Most modern async code |
| Web Worker | Async | Không chặn main thread | Không access DOM | Heavy computation |
| Observable (RxJS) | Async | Reactive, powerful | Steep learning curve | Real-time data, complex streams |

## 📊 Performance & Best Practices

- **Giữ main thread lightweight** — đẩy tính toán nặng (>50ms) ra Web Worker.
- **Dùng `Promise.all`** cho requests độc lập — parallel thay vì sequential, tiết kiệm thời gian đáng kể.
- **Avoid nested callbacks** — refactor thành promise/async-await ngay khi thấy 2-3 cấp lồng.
- **Always handle errors** — `.catch()` hoặc `try/catch` với async/await để tránh unhandled rejection.
- **Measure real impact** — DevTools Performance tab cho thấy blocked time, main thread load.
- **Dùng `requestAnimationFrame`** cho animation thay vì `setInterval` — sync với browser repaint (~60fps).
- **Debouncing và throttling** — giảm frequency của expensive operations (search, scroll).
- **Async IIFE** — `(async () => { await ... })();` nếu cần top-level await behavior.

## 🔗 Liên kết chéo

- **Xem thêm:** `12_asynchronous-javascript/01_event-loop/00_js-runtime-deep-dive` — runtime architecture
- **Xem thêm:** `12_asynchronous-javascript/01_event-loop/02_event-loop` — event loop cơ chế
- **Xem thêm:** `12_asynchronous-javascript/01_event-loop/03_settimeout-setinterval` — timer behavior
- **Xem thêm:** `12_asynchronous-javascript/02_callbacks-promises/01_promise-theory` — promise fundamentals
- **Xem thêm:** `12_asynchronous-javascript/02_callbacks-promises/02_async-await` — async/await syntax
- **Xem thêm:** `12_asynchronous-javascript/02_callbacks-promises/07_callback-hell` — callback hell solutions
- **Xem thêm:** `13_working-with-apis/01_fetch` — fetch API thực tế
- **Xem thêm:** `17_memory-management/01_memory-lifecycle-gc/01_garbage-collection` — memory implications
