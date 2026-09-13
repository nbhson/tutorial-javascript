# Non-blocking I/O — Xử lý không chặn (Thực hành chi tiết) — [Level: Advanced]

## 🔑 Khái niệm cốt lõi

**Non-blocking I/O** là cơ chế *không chặn* luồng xử lý khi chờ thao tác nhập/xuất (I/O). Nghĩa là: khi chương trình đang chờ dữ liệu (đọc file, gọi API, nhập liệu), nó **vẫn tiếp tục chạy các công việc khác** thay vì đứng yên chờ.

Hai khái niệm đối lập:

| | Blocking I/O | Non-blocking I/O |
|---|---|---|
| Hành vi | Đợi thao tác xong rồi mới chạy tiếp | Bắt đầu thao tác, quay lại khi có kết quả |
| Hệ quả | Lãng phí thời gian chờ | Tận dụng thời gian để làm việc khác |
| Nhiều việc cùng lúc | Không (đơn luồng, tuần tự) | "Đa nhiệm" trên cùng một luồng |

Tác giả liên hệ trực quan: hệ điều hành Windows xử lý "đa luồng" vì bạn có thể vừa copy, vừa xóa, vừa chạy nhiều chương trình dù thao tác trước chưa xong. Ngược lại, JavaScript là ngôn ngữ **đơn luồng** — một main thread xử lý mọi việc. Vì vậy JS dùng cơ chế **bất đồng bộ và sự kiện** (async + event loop) để không bị "đứng hình" khi gặp thao tác I/O chậm.

**Điểm mấu chốt cần hiểu**:
- JavaScript **một luồng** nhưng **không chặn** — nhờ `setTimeout`, `fetch`, sự kiện, event loop.
- Khi gặp I/O, gọi hàm **callback / promise** và rời đi làm việc khác; khi xong, tác vụ quay lại thực thi.
- Lập trình hướng sự kiện: chỉ khi có tác động (click, dữ liệu về...) mới xử lý thêm → **tiết kiệm tài nguyên hệ thống** so với chạy quá nhiều luồng thật.

**Sự thật quan trọng**: thư mục này **không có file code** — chỉ có README lý thuyết. Bạn cần tự chạy các ví dụ trong console để cảm nhận behavior.

## 📐 Cấu trúc / Cú pháp

### Event Loop cơ bản
```
┌─────────────────────────────────────────┐
│         Call Stack                      │
│  (sync code chạy ở đây)                 │
└─────────────────────────────────────────┘
              ↓ push/pop
┌─────────────────────────────────────────┐
│      Web APIs / Node APIs               │
│  (setTimeout, fetch, fs.readFile...)    │
└─────────────────────────────────────────┘
              ↓ callback enqueue
┌─────────────────────────────────────────┐
│      Callback Queue                     │
│  (đợi call stack rỗng mới chạy)         │
└─────────────────────────────────────────┘
              ↓ process
┌─────────────────────────────────────────┐
│      Event Loop (vòng lặp vô tận)       │
│  "Call stack rỗng chưa? Nếu có,        │
│   đẩy callback từ queue vào stack"      │
└─────────────────────────────────────────┘
```

### Async patterns
```js
// 1. Callback
setTimeout(() => console.log("callback done"), 1000);

// 2. Promise
fetch("/api/data")
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(err => console.error(err));

// 3. Async/Await
async function loadData() {
  try {
    const response = await fetch("/api/data");
    const data = await response.json();
    console.log(data);
  } catch (err) {
    console.error(err);
  }
}
```

### Microtask vs Macrotask
```js
console.log("1. sync");

setTimeout(() => console.log("2. macrotask (setTimeout)"), 0);

Promise.resolve().then(() => console.log("3. microtask (promise)"));

queueMicrotask(() => console.log("4. microtask (queueMicrotask)"));

console.log("5. sync");

// Thứ tự: 1 → 5 → 3 → 4 → 2
// Microtasks (Promise) chạy TRƯỚC macrotasks (setTimeout)
```

## ✅ Điểm mạnh

1. **Không lãng phí thời gian chờ**: một luồng vẫn phục vụ được rất nhiều tác vụ I/O — hiệu quả tài nguyên cao.
2. **Hiệu năng phục vụ đồng thời tốt** (đặc biệt Node.js cho Web server: nhiều request cùng lúc) — single-threaded nhưng high throughput.
3. **Tiết kiệm tài nguyên**: không cần tạo hàng trăm luồng như các ngôn ngữ khác (Java, C++) — giảm memory overhead.
4. **Mô hình dựa trên sự kiện tự nhiên**, dễ hiểu với UI: click → xử lý — event-driven architecture fit cho web.
5. **Hệ sinh thái async hiện đại**: Promise, `async/await` làm code bất đồng bộ gần như code đồng bộ — readable, maintainable.
6. **Non-blocking UI**: browser không "đơ" khi gọi API — main thread vẫn responsive cho user interactions.
7. **Backpressure handling**: stream API (Node.js) xử lý dữ liệu lớn mà không overflow memory.
8. **Fan-out/fan-in patterns**: `Promise.all`, `Promise.race` — parallel async operations với control.
9. **Coroutine-like behavior**: async/await gives sequential appearance to async code — easier to reason about.
10. **Event emitter pattern**: publish/subscribe decoupled architecture — loose coupling between components.

## ⚠️ Bẫy thường gặp & Hạn chế

1. **Đơn luồng + không chặn nghĩa là một tác vụ nặng** (tính toán lớn, vòng lặp dài) **sẽ "chiếm" luồng** và làm mọi thứ khác đứng hình — phải chia nhỏ hoặc dùng Worker.
   ```js
   // ❌ Chặn event loop — UI đơ trong lúc tính
   for (let i = 0; i < 1e9; i++) {} // CPU-bound, blocks everything

   // ✅ Chia nhỏ với setTimeout — yield control back to event loop
   function chunkedWork(chunk, total, callback, index = 0) {
     const end = Math.min(index + chunk, total);
     for (let i = index; i < end; i++) {
       // do work...
     }
     if (end < total) {
       setTimeout(() => chunkedWork(chunk, total, callback, end), 0);
     } else {
       callback();
     }
   }
   ```

2. **Tư duy bất đồng bộ khó hơn** — dễ viết gián đoạn logic, thiếu await, quên xử lý lỗi.
   ```js
   // ❌ Quên await — result là Promise, không phải value
   const data = fetch("/api/data");
   console.log(data.name); // undefined — data là Promise object

   // ✅ Đúng
   const response = await fetch("/api/data");
   const data = await response.json();
   console.log(data.name); // actual data
   ```

3. **Thứ tự thực thi không theo thứ tự viết code** — cần hiểu event loop để predict behavior.
   ```js
   console.log("A");
   setTimeout(() => console.log("B"), 0);
   console.log("C");
   // Kết quả: A → C → B (không phải A → B → C!)
   ```

4. **Không phải "đa luồng thật sự"** như C++/Java — song song CPU-bound không tốt, cần Web Worker hoặc child_process.
   ```js
   // JavaScript single-threaded — không parallel CPU work
   // ✅ Dùng Web Worker cho CPU-heavy task
   const worker = new Worker("heavy-task.js");
   worker.postMessage(data);
   worker.onmessage = (e) => console.log(e.data);
   ```

5. **Callback sâu gây callback hell** nếu không dùng Promise/async — code khó đọc, khó error handle.
   ```js
   // ❌ Callback hell
   step1(function(a) {
     step2(a, function(b) {
       step3(b, function(c) {
         step4(c, function(d) {
           // ... deep nesting
         });
       });
     });
   });

   // ✅ Async/await — flat structure
   async function flow() {
     const a = await step1();
     const b = await step2(a);
     const c = await step3(b);
     const d = await step4(c);
   }
   ```

6. **Unhandled promise rejection** — lỗi không bắt gây crash trong Node.js, warning trong browser.
   ```js
   // ❌ Unhandled rejection
   Promise.reject(new Error("oops"));

   // ✅ Handle mọi path
   Promise.reject(new Error("oops")).catch(err => console.error(err));
   // hoặc global handler
   process.on("unhandledRejection", err => console.error(err));
   ```

## 💡 Khi nào dùng

1. **Gọi API / `fetch`** — UI cần phản hồi ngay dù mạng chậm — não-blocking keep UI responsive.
2. **Đọc/ghi file trong Node.js** (không chặn server) — `fs.readFile`, `fs.writeFile` async versions.
3. **Timer, sự kiện người dùng, socket, realtime** — `setTimeout`, DOM events, WebSocket callbacks.
4. **Query cơ sở dữ liệu**, gọi service bên thứ ba — DB queries, third-party API calls.
5. **Batch xử lý nhiều request đồng thời** (ví dụ gửi nhiều request song song rồi `Promise.all`) — parallel I/O.
6. **File upload/download** — stream processing, progress tracking, cancelable operations.
7. **Server-side rendering** — Node.js serve nhiều requests simultaneously without blocking.
8. **Real-time applications** — chat, live updates, multiplayer games — event-driven architecture.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: setTimeout non-blocking demonstration
```js
console.log("1. bắt đầu");

setTimeout(() => console.log("3. timer xong (bất đồng bộ)"), 0);

console.log("2. chạy tiếp ngay — không bị chặn");

// Kết quả in ra: 1. bắt đầu → 2. chạy tiếp → 3. timer xong
// Dù timeout = 0, nó vẫn chạy SAU các câu lệnh đồng bộ
// Vì setTimeout callback đẩy vào macrotask queue, chỉ chạy khi call stack rỗng
```

### Ví dụ 2: Promise chain — sequential async
```js
console.log("1. start");

fetch("/api/users")
  .then(response => {
    console.log("2. response received");
    return response.json();
  })
  .then(users => {
    console.log("3. users:", users.length);
    return fetch(`/api/posts?userId=${users[0].id}`);
  })
  .then(response => response.json())
  .then(posts => {
    console.log("4. posts:", posts.length);
  })
  .catch(err => console.error("Error:", err));

console.log("5. fire and forget — không chặn");
// Kết quả: 1 → 5 → 2 → 3 → 4 (hoặc 5 → 2 → 3 → 4 tùy timing)
```

### Ví dụ 3: Async/await — sequential, looks synchronous
```js
async function loadDashboard() {
  console.log("1. start loading");

  const [users, posts, settings] = await Promise.all([
    fetch("/api/users").then(r => r.json()),
    fetch("/api/posts").then(r => r.json()),
    fetch("/api/settings").then(r => r.json())
  ]);

  console.log("2. all data loaded");
  console.log("Users:", users.length);
  console.log("Posts:", posts.length);
  console.log("Settings:", settings);
}
// Promise.all — parallel fetch, waits for ALL to complete
// Looks synchronous but actually non-blocking
```

### Ví dụ 4: Event loop order — microtask vs macrotask
```js
console.log("1. sync start");

setTimeout(() => console.log("2. macrotask"), 0);

Promise.resolve().then(() => console.log("3. microtask 1"));
Promise.resolve().then(() => console.log("4. microtask 2"));

queueMicrotask(() => console.log("5. queueMicrotask"));

console.log("6. sync end");

// Kết quả: 1 → 6 → 3 → 4 → 5 → 2
// Microtasks (Promise, queueMicrotask) luôn chạy TRƯỚC macrotasks (setTimeout)
// Và microtasks chạy hết mới đến macrotasks
```

### Ví dụ 5: Error handling in async — try/catch với await
```js
async function safeFetch(url) {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error(`Fetch failed for ${url}:`, error.message);
    return null; // graceful fallback
  }
}

// Usage
const userData = await safeFetch("/api/users/1");
if (userData) {
  console.log("User:", userData.name);
} else {
  console.log("Using fallback data");
}
```

### Ví dụ 6: Parallel vs Sequential — performance comparison
```js
// ❌ Sequential — slow, each wait for previous
async function sequential() {
  const t0 = Date.now();
  await fetch("/api/a"); // 500ms
  await fetch("/api/b"); // 500ms
  await fetch("/api/c"); // 500ms
  console.log(`Sequential: ${Date.now() - t0}ms`); // ~1500ms
}

// ✅ Parallel — fast, all fetch simultaneously
async function parallel() {
  const t0 = Date.now();
  await Promise.all([
    fetch("/api/a"),
    fetch("/api/b"),
    fetch("/api/c")
  ]);
  console.log(`Parallel: ${Date.now() - t0}ms`); // ~500ms
}
```

### Ví dụ 7: Retry with exponential backoff
```js
async function fetchWithRetry(url, retries = 3, delay = 1000) {
  for (let i = 0; i < retries; i++) {
    try {
      const response = await fetch(url);
      if (response.ok) return await response.json();
      throw new Error(`HTTP ${response.status}`);
    } catch (error) {
      if (i === retries - 1) throw error; // last try — rethrow
      const waitTime = delay * Math.pow(2, i); // exponential: 1s, 2s, 4s
      console.log(`Retry ${i + 1}/${retries} in ${waitTime}ms...`);
      await new Promise(r => setTimeout(r, waitTime));
    }
  }
}
```

### Ví dụ 8: Async iterator — stream processing
```js
async function* generateNumbers(limit) {
  for (let i = 0; i < limit; i++) {
    await new Promise(r => setTimeout(r, 100)); // non-blocking delay
    yield i;
  }
}

// Consume async iterator
(async () => {
  for await (const num of generateNumbers(5)) {
    console.log(num); // 0, 1, 2, 3, 4 — mỗi số sau 100ms
  }
})();
// Non-blocking: event loop không bị chiếm bởi setTimeout
```

### Ví dụ 9: Debounce — non-blocking user input
```js
function debounce(fn, delay) {
  let timerId;
  return function(...args) {
    clearTimeout(timerId); // hủy timer cũ
    timerId = setTimeout(() => {
      fn.apply(this, args); // chạy sau delay ms
    }, delay);
  };
}

// Usage: search input — chỉ fetch sau khi ngưng gõ 300ms
const searchInput = document.getElementById("search");
const debouncedSearch = debounce(async (query) => {
  const response = await fetch(`/api/search?q=${query}`);
  const results = await response.json();
  renderResults(results);
}, 300);

searchInput.addEventListener("input", (e) => debouncedSearch(e.target.value));
```

### Ví dụ 10: CPU-bound work — chunking to avoid blocking
```js
// Problem: heavy computation blocks event loop
function heavyComputation() {
  let result = 0;
  for (let i = 0; i < 1e9; i++) {
    result += i;
  }
  return result;
}
// ⬇️ Chặn event loop ~100-500ms — UI đơ!

// Solution: chunk work với setTimeout
function chunkedComputation(total, chunkSize = 1000000, callback, index = 0) {
  const end = Math.min(index + chunkSize, total);
  let result = 0;
  for (let i = index; i < end; i++) {
    result += i;
  }
  if (end < total) {
    setTimeout(() => chunkedComputation(total, chunkSize, callback, end), 0);
  } else {
    callback(result);
  }
}
// ✅ UI vẫn responsive vì event loop không bị chiếm dài
chunkedComputation(1e9, 1e7, (result) => console.log("Done:", result));
```

## 🔬 So sánh với alternatives

| Pattern | Ưu điểm | Nhược điểm | Phù hợp khi |
|---|---|---|---|
| **Callback** | Simple, native | Callback hell, inversion of control | Simple one-off async |
| **Promise** | Chainable, error handling | Verbose without async/await | Complex async flows |
| **async/await** | Sequential-looking, clean | Same as Promise underneath | Modern async (recommended) |
| **Observable** | Streaming, operators | RxJS heavy, learning curve | Real-time data, complex streams |
| **Event Emitter** | Decoupled pub/sub | Manual management | Event-driven architecture |
| **Web Worker** | True parallel CPU | Complex communication | CPU-heavy background tasks |
| **Generator** | Custom iteration control | Lower-level, manual resume | Custom async control flow |

## 📊 Performance & Best Practices

**Event Loop Performance**:
- Macrotask queue (setTimeout, setInterval): processed one per event loop tick.
- Microtask queue (Promise.then, queueMicrotask): ALL processed before next macrotask.
- I/O operations (network, file): handled by OS/libuv, callback enqueued khi xong.
- **CPU-bound work blocks event loop** — dùng Web Worker hoặc chunking.

**Best practices**:
- **Luôn handle promise rejection** — `.catch()` hoặc `try/catch` với `await`.
- **Prefer `async/await`** over promise chains — readable, maintainable.
- **Use `Promise.all`** for parallel independent operations — faster than sequential.
- **Use `Promise.allSettled`** khi cần result of ALL promises regardless of failure.
- **Avoid nested async** — flatten với `await` instead of callback in callback.
- **Chunk CPU-bound work** — dùng `setTimeout` hoặc Web Worker tránh block main thread.
- **Set timeout on long operations** — `AbortController` để cancel stale requests.
- **Use `queueMicrotask`** khi cần chạy sau current sync code nhưng trước next macrotask.
- **Monitor event loop latency** — `performance.mark`/`measure` trong browser, `process.nextTick` in Node.
- **Backpressure awareness** — stream APIs (`ReadableStream`) for large data to avoid memory overflow.

**Quy tắc "3 nên — 3 không"**:
- ✅ Nên dùng `async/await` + `try/catch` cho clean error handling.
- ✅ Nên `Promise.all` cho parallel independent async operations.
- ✅ Nên chunk CPU-heavy work để không block event loop.
- ❌ Không nên quên `.catch()` trên promise — unhandled rejection crash.
- ❌ Không nên CPU-bound operation trên main thread — dùng Worker.
- ❌ Không nên nested async callbacks — flatten với async/await.

## 🔗 Liên kết chéo

- Tổng quan Functions: `09_functions/README.md` — callback, async context.
- Callbacks: `09_functions/01_parameters-and-arrow/01_callbacks/` — callback trong async.
- Arrow functions: `09_functions/01_parameters-and-arrow/03_arrow-functions/` — arrow trong async callbacks.
- Built-in functions: `09_functions/01_parameters-and-arrow/02_builtin-functions/` — setTimeout, setInterval.
- Recursion: `09_functions/01_parameters-and-arrow/04_recursion/` — recursive async (promise chain).
- Call stack: `09_functions/02_scope-closure-strict-mode/05_function-stack/` — call stack trong async context.
- Closure: `09_functions/02_scope-closure-strict-mode/03_closure/` — closure trong async callback.
- Exceptional handling: `07_exceptional-handling/02_try-catch-finally/` — try/catch với async/await.
- Strict mode: `09_functions/02_scope-closure-strict-mode/01_strict-mode/` — strict mode trong module/async.
