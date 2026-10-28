# Lập trình Bất đồng bộ (Asynchronous JavaScript) — [Level: Intermediate]

## 🔑 Khái niệm cốt lõi

**JavaScript là ngôn ngữ đơn luồng (single-threaded)**: engine chỉ xử lý một câu lệnh tại một thời điểm trong một luồng duy nhất. Điều này có nghĩa nếu có một tác vụ chạy lâu (gọi API, đọc file, chờ timer...), toàn bộ chương trình sẽ **bị chặn (block)** — UI đơ, không phản hồi.

**Lập trình bất đồng bộ (asynchronous)** giải quyết vấn đề đó: chương trình có thể **bắt đầu** một tác vụ dài và **tiếp tục đáp ứng các sự kiện khác** ngay lập tức, thay vì đứng chờ. Khi tác vụ hoàn thành, kết quả được thông báo lại qua callback, promise, hoặc event.

JavaScript hiện thực điều này bằng kiến trúc **Event Loop + Call Stack + Web APIs + hàng đợi (queue)**. Cơ chế hoạt động:

1. Code đồng bộ chạy trên **Call Stack** (LIFO).
2. Gặp tác vụ bất đồng bộ → đẩy sang **Web APIs** (timer, network, DOM...).
3. Web APIs xử lý xong → đưa callback vào **Task Queue** (macrotask) hoặc **Microtask Queue**.
4. **Event Loop** liên tục kiểm tra: nếu Call Stack trống → lấy callback từ queue đưa vào stack.
5. Lặp lại vô tận.

Thứ tự ưu tiên trong mỗi tick của event loop: **sync code → microtasks (Promise) → macrotasks (setTimeout)**.

Các kỹ thuật bất đồng bộ chính trong JS:
1. **Callbacks** — truyền hàm xử lý sau khi tác vụ xong (nền tảng, nhưng dễ thành callback hell).
2. **Promises (ES6)** — đối tượng đại diện kết quả tương lai, giải quyết callback hell.
3. **async/await (ES2017)** — cú pháp viết code bất đồng bộ nhìn như đồng bộ.

## 📐 Cấu trúc / Cú pháp

### Timeline của một tác vụ bất đồng bộ

```
Time →
[Sync code runs on Call Stack]
         ↓
[setTimeout/fetch → Web API (đồng hồ/rõ mạng)]
         ↓ (khi xong)
[Callback vào Macrotask Queue hoặc Microtask Queue]
         ↓
[Event Loop: Call Stack trống? → đưa callback vào Stack]
         ↓
[Callback chạy → trả về kết quả]
```

### Bảng so sánh kỹ thuật

| Kỹ thuật | Syntax | Error handling | Composition | Readability |
|----------|--------|----------------|-------------|-------------|
| Callback | `fn(callback)` | Try/catch không work | Nested | ❌ Kém |
| Promise | `.then().catch()` | `.catch()` | `.then().then()` | ⚠️ Trung bình |
| Async/Await | `await promise` | `try/catch` | Dòng tuần tự | ✅ Tốt |

### Priority queue order

| Hàng đợi | Ưu tiên | Chứa |
|----------|---------|------|
| **Microtask Queue** | Cao nhất | `Promise.then()`, `queueMicrotask()`, `MutationObserver` |
| **Macrotask Queue** | Thấp hơn | `setTimeout`, `setInterval`, I/O, event handlers |

## ✅ Điểm mạnh — Tại sao nên dùng

1. **Không chặn luồng chính** — trang web luôn phản hồi trong lúc tải dữ liệu.
2. **Xử lý song song các tác vụ độc lập** — `Promise.all` chạy nhiều API cùng lúc.
3. **Cải thiện UX** — UI mượt, không bị "đứng hình" khi chờ dữ liệu.
4. **Promise + async/await giúp code dễ đọc** — dễ debug hơn callback nối chồng.
5. **Mọi tác vụ I/O mạng, timer, DOM event đều tận dụng được** — không giới hạn.
6. **Error handling tập trung** — `.catch()` hoặc `try/catch` bắt lỗi xuyên suốt chain.
7. **Composition linh hoạt** — `Promise.all`, `Promise.race`, `Promise.allSettled` kết hợp nhiều promise.
8. **Native browser support** — fetch, service worker, web transport đều async.

## ⚠️ Bẫy thường gặp & Hạn chế

### Bẫy 1: Thứ tự thực thi không theo thứ tự khai báo

```js
console.log("1");
setTimeout(() => console.log("2"), 0);
console.log("3");
// Output: 1 → 3 → 2 (không phải 1 → 2 → 3)
```

### Bẫy 2: Promise microtask chạy trước setTimeout macrotask

```js
setTimeout(() => console.log("timeout"), 0);
Promise.resolve().then(() => console.log("promise"));
// Output: promise → timeout (dù setTimeout khai báo trước)
```

### Bẫy 3: Callback hell — code lồng nhau khó đọc

```js
getData(function(a) {
  getMoreData(a, function(b) {
    getMoreData(b, function(c) {
      getMoreData(c, function(d) {
        // pyramid of doom
      });
    });
  });
});
```

### Bẫy 4: `await` chỉ hợp lệ trong hàm `async`

```js
const result = await fetch("/api"); // ❌ SyntaxError ở top-level
async function main() {
  const result = await fetch("/api"); // ✅
}
```

### Bẫy 5: Fetch không throw khi HTTP error — chỉ throw khi mạng hỏng

```js
fetch("/nonexistent")
  .then(res => {
    console.log(res.status); // 404 — nhưng không throw!
    return res.json();
  })
  .catch(err => console.error(err)); // KHÔNG chạy với 404
```

### Bẫy 6: Unhandled promise rejection

```js
const p = Promise.reject("Oops");
// Không có .catch() → unhandled rejection (lỗi ngầm)
```

### Bẫy 7: Await tuần tự nhiều tác vụ độc lập — chậm không cần thiết

```js
// Chậm: chờ từng cái
const a = await fetch("/a");
const b = await fetch("/b");

// Nhanh: chạy song song
const [a, b] = await Promise.all([fetch("/a"), fetch("/b")]);
```

## 💡 Khi nào dùng — Tình huống thực tế

1. **Gọi REST API**, tải dữ liệu từ server (fetch, XHR).
2. **Đặt lịch tác vụ**: `setTimeout`, `setInterval`.
3. **Lắng nghe sự kiện người dùng** (click, scroll...) mà không chặn.
4. **Xử lý file, stream, realtime** (WebSocket), animation.
5. **Mọi tác vụ cần "chờ" kết quả ngoài luồng** mà không muốn đứng im chờ.
6. **Parallel operations** — `Promise.all` cho nhiều request độc lập.
7. **Sequential dependent operations** — async/await cho workflow phụ thuộc.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Event loop basic order

```js
console.log("1. Start"); // sync

setTimeout(() => {
  console.log("2. Timeout");     // macrotask → chạy cuối
}, 0);

Promise.resolve()
  .then(() => console.log("3. Promise")); // microtask → chạy sau sync

console.log("4. End"); // sync

// Output: 1. Start → 4. End → 3. Promise → 2. Timeout
```

### Ví dụ 2: Promise chain

```js
fetch("https://jsonplaceholder.typicode.com/posts/1")
  .then(response => {
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return response.json();
  })
  .then(post => console.log(post.title))
  .catch(err => console.error("Failed:", err.message));
```

### Ví dụ 3: Async/await với try/catch

```js
async function getPost() {
  try {
    const res = await fetch("https://jsonplaceholder.typicode.com/posts/1");
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const post = await res.json();
    console.log(post.title);
  } catch (err) {
    console.error("Failed:", err.message);
  }
}
getPost();
```

### Ví dụ 4: Promise.all — parallel fetch

```js
async function loadAll() {
  const [postsRes, usersRes] = await Promise.all([
    fetch("https://jsonplaceholder.typicode.com/posts"),
    fetch("https://jsonplaceholder.typicode.com/users")
  ]);
  const [posts, users] = await Promise.all([
    postsRes.json(),
    usersRes.json()
  ]);
  console.log(`Posts: ${posts.length}, Users: ${users.length}`);
}
loadAll();
```

### Ví dụ 5: Promise.race — timeout pattern

```js
function fetchWithTimeout(url, timeoutMs) {
  const timeout = new Promise((_, reject) =>
    setTimeout(() => reject(new Error("Timeout")), timeoutMs)
  );
  return Promise.race([fetch(url), timeout]);
}
```

### Ví dụ 6: Sequential dependency với async/await

```js
async function getCommentsAndUsers() {
  const commentsRes = await fetch("/api/comments");
  const comments = await commentsRes.json();
  
  const userIds = [...new Set(comments.map(c => c.userId))];
  const usersRes = await fetch(`/api/users?id=${userIds.join(",")}`);
  const users = await usersRes.json();
  
  return { comments, users };
}
```

## 🔬 So sánh với alternatives

| Cách | Ưu điểm | Nhược điểm | Khi nào dùng |
|------|---------|------------|--------------|
| Callback | Đơn giản, mọi browser | Callback hell, khó test | Legacy code, small scripts |
| Promise | Chainable, error handling | Syntax dài hơn async/await | API calls, complex flows |
| Async/Await | Đọc như sync, dễ debug | Chỉ trong async function | Most modern async code |
| Observable (RxJS) | Reactive, powerful | Steep learning curve | Real-time data, complex streams |

## 📊 Performance & Best Practices

- **Luôn dùng `Promise.all`** cho các request độc lập — chạy song song thay vì tuần tự.
- **Dùng `async/await`** cho các bước phụ thuộc nhau — readability tốt hơn chain.
- **Always handle errors** — `.catch()` hoặc `try/catch` để tránh unhandled rejection.
- **Kiểm tra `response.ok`** sau fetch — fetch không throw với HTTP error.
- **Avoid nested async/await** — refactor thành functions riêng.
- **Dùng `queueMicrotask()`** khi cần chạy trước macrotask mà không tạo promise.
- **Giải phóng timer** — `clearTimeout`/`clearInterval` khi component unmount.

## 🔗 Liên kết chéo

- **Xem thêm:** `12_asynchronous-javascript/01_event-loop/00_js-runtime-deep-dive` — runtime architecture
- **Xem thêm:** `12_asynchronous-javascript/01_event-loop/02_event-loop` — event loop mechanism
- **Xem thêm:** `12_asynchronous-javascript/01_event-loop/03_settimeout-setinterval` — timer APIs
- **Xem thêm:** `12_asynchronous-javascript/02_callbacks-promises/01_promise-theory` — promise fundamentals
- **Xem thêm:** `12_asynchronous-javascript/02_callbacks-promises/02_async-await` — async/await syntax
- **Xem thêm:** `12_asynchronous-javascript/02_callbacks-promises/04_promise-chain` — promise chaining
- **Xem thêm:** `12_asynchronous-javascript/02_callbacks-promises/07_callback-hell` — callback hell solutions

## 🆕 ES2025 — Promise.try() và Promise.withResolvers()

### `Promise.try()` — thực thi một function như promise

Chuẩn hóa function có thể throw lỗi **sync** hoặc trả promise — mọi lỗi đều đi vào `.catch()`. Đạt Stage 4 (10/2024), chính thức trong **ES2025**.

**Browser support:** Chrome 122+, Firefox 128+, Safari 17.5+, Node 22+.

```js
// ❌ Trước: nếu getUser throw lỗi SYNC → .catch() KHÔNG bắt được
function getUser(id) { return JSON.parse(rawUser); } // có thể throw sync
Promise.resolve(getUser(1)).then(handle).catch(handleErr);
// lỗi sync văng ra ngoài chain!

// ✅ ES2025: Promise.try — mọi lỗi sync/async đều vào .catch()
Promise.try(getUser, 1)              // truyền arguments trực tiếp
  .then(user => processUser(user))
  .catch(err => handleError(err));   // bắt được CẢ lỗi sync

// Dạng arrow khi cần closure
Promise.try(() => fetch("/api").then(r => r.json()))
  .then(console.log)
  .catch(console.error);
```

> 📖 MDN: [Promise.try()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/try)

### `Promise.withResolvers()` — tạo promise với resolve/reject tách riêng

Cách hiện đại thay cho pattern khai báo biến bên ngoài executor (ES2024, thường được nhắc cùng ES2025).

**Browser support:** Chrome 119+, Firefox 121+, Safari 17.4+, Node 22+.

```js
// ❌ Trước: rườm rà
let resolveFn, rejectFn;
const p1 = new Promise((resolve, reject) => {
  resolveFn = resolve;
  rejectFn = reject;
});

// ✅ Mới: một dòng, dùng được ở scope ngoài
const { promise, resolve, reject } = Promise.withResolvers();

// Use case kinh điển: resolve từ event listener
document.getElementById("submit-btn")
  .addEventListener("click", () => resolve("submitted"));
setTimeout(() => reject(new Error("Timeout!")), 5000);

promise
  .then(value => console.log(value))
  .catch(err => console.error(err.message));
```

> 📖 MDN: [Promise.withResolvers()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/withResolvers)
>
> Xem thêm tổng hợp: `22_es2025-features/README.md`
