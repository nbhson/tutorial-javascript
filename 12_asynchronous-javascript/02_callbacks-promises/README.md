# Callbacks & Promises — [Level: Intermediate]

## 🔑 Khái niệm cốt lõi

Đây là phần đi sâu vào hai công cụ xử lý bất đồng bộ phổ biến nhất:

- **Callback**: hàm được truyền vào hàm khác và gọi lại sau khi tác vụ hoàn thành. Là nền tảng, nhưng lồng nhau nhiều tầng sẽ thành **callback hell**.
- **Promise**: đối tượng đại diện cho kết quả của một tác vụ bất đồng bộ (đang chờ, thành công hoặc thất bại), với các bước `.then()/.catch()/.finally()`. Ra đời từ ES6 để giải quyết callback hell.
- **async/await**: cú pháp (ES2017) viết promise gọn như code đồng bộ, dễ đọc/dễ giữ lỗi.

Promise có 3 trạng thái:
- `pending` — tác vụ chưa xong.
- `fulfilled` — thành công, các `.then()` được gọi.
- `rejected` — thất bại, `.catch()` được gọi.

Promise là **microtask** — chạy trước `setTimeout` (macrotask) trong mỗi tick của event loop. Điều này có nghĩa Promise callback luôn chạy trước timer callback, dù timer được set trước promise.

## 📐 Cấu trúc / Cú pháp

### Promise lifecycle

```
new Promise(executor)
       │
       ▼
   pending ────────┬──────────────────┐
                   ▼                  ▼
             fulfilled            rejected
               │                    │
               ▼                    ▼
         .then(onFulfilled)   .catch(onRejected)
               │                    │
               └────────┬───────────┘
                        ▼
                   .finally(onSettled)
                        │
                        ▼
                   Promise settles (never changes back)
```

### Async/Await syntax

```js
async function fetchData() {
  try {
    const response = await fetch("/api/data");
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Failed:", error);
  }
}
```

### Bảng so sánh 3 approaches

| Đặc tính | Callback | Promise | Async/Await |
|----------|----------|---------|-------------|
| Readability | ❌ Kém (nested) | ⚠️ Trung bình | ✅ Tốt |
| Error handling | Manual pass | `.catch()` | `try/catch` |
| Composition | Hard | `.then().then()` | Sequential |
| Debugging | Stack trace sâu | Clean stack | Clean stack |
| Browser support | All | ES6+ | ES2017+ |

## ✅ Điểm mạnh — Tại sao nên dùng

1. **Promise xử lý lỗi tập trung** qua `.catch`, không phải truyền lỗi lồng nhau.
2. **Chain `.then()`** cho phép nối các bước bất đồng bộ rõ ràng.
3. **`Promise.all`/`Promise.race`** chạy song song, kết hợp nhiều tác vụ.
4. **async/await** làm code gần với suy nghĩ tuần tự, dễ debug.
5. **Giải quyết triệt để "callback hell"** — chuyển pyramid thành dòng thẳng.
6. **Composable** — promise có thể return từ `.then()` để chain tiếp.
7. **Standardized error handling** — lỗi tự động propagate xuống `.catch()`.
8. **Native browser support** — fetch, Web API đều return promise.

## ⚠️ Bẫy thường gặp & Hạn chế

### Bẫy 1: Quên `return` trong `.then()` — chain break

```js
fetch("/api")
  .then(res => res.json())     // ✅ return promise
  .then(data => data.items);   // ✅
  
// ❌ Không return:
fetch("/api")
  .then(res => res.json())
  .then(data => { console.log(data); }) // undefined — không return
```

### Bẫy 2: Promise chỉ settle một lần

```js
const p = new Promise((resolve) => {
  resolve(1);
  resolve(2); // bị bỏ qua — promise đã fulfilled
});
p.then(v => console.log(v)); // 1
```

### Bẫy 3: `await` ngoài async function → SyntaxError

```js
const data = await fetch("/api"); // ❌ SyntaxError
async function main() {
  const data = await fetch("/api"); // ✅
}
```

### Bẫy 4: Await tuần tự nhiều task độc lập — chậm không cần

```js
// Chậm: chờ từng cái
const a = await fetch("/a");
const b = await fetch("/b");

// Nhanh: song song
const [a, b] = await Promise.all([fetch("/a"), fetch("/b")]);
```

### Bẫy 5: Fetch không throw với HTTP error

```js
fetch("/nonexistent")
  .then(res => {
    console.log(res.status); // 404 — nhưng KHÔNG throw!
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
  });
```

### Bẫy 6: Unhandled rejection — quên `.catch()`

```js
Promise.reject("Oops").then(() => {}); 
// Unhandled rejection warning in console
// Fix: thêm .catch(() => {})
```

## 💡 Khi nào dùng — Tình huống thực tế

1. **Bất kỳ tác vụ bất đồng bộ nào**: fetch, đọc file, database, timer.
2. **Xử lý theo chuỗi**: lấy comment → lấy user từ comment → render.
3. **Chạy song song nhiều request**: `Promise.all`.
4. **Giữ code dễ đọc** trong quy trình nhiều bước phụ thuộc nhau — dùng async/await.
5. **Timeout pattern**: `Promise.race([fetch, timeout])`.
6. **Retry logic**: wrap fetch trong loop với delay.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Promise cơ bản

```js
const p = new Promise((resolve, reject) => {
  setTimeout(() => resolve("Success"), 1000);
});
p.then((msg) => console.log(msg))   // Success
 .catch((err) => console.log(err))
 .finally(() => console.log("Done"));
```

### Ví dụ 2: Promise chain — sequential dependency

```js
fetch("/api/posts")
  .then(res => {
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
  })
  .then(posts => {
    return Promise.all(posts.map(post => 
      fetch(`/api/users/${post.userId}`).then(r => r.json())
    ));
  })
  .then(users => {
    console.log("Users:", users.length);
  })
  .catch(err => console.error("Failed:", err));
```

### Ví dụ 3: Promise.all — parallel operations

```js
async function loadDashboard() {
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
  
  renderDashboard({ posts, users, stats });
}
```

### Ví dụ 4: Promise.race — timeout pattern

```js
async function fetchWithTimeout(url, timeoutMs = 5000) {
  const timeout = new Promise((_, reject) =>
    setTimeout(() => reject(new Error("Timeout")), timeoutMs)
  );
  const result = await Promise.race([fetch(url), timeout]);
  return result.json();
}
```

### Ví dụ 5: Async/await cơ bản

```js
async function getUser(id) {
  const res = await fetch(`https://jsonplaceholder.typicode.com/users/${id}`);
  if (!res.ok) throw new Error("Bad request");
  return res.json();
}

async function main() {
  try {
    const user = await getUser(1);
    console.log(user.name); // Leanne Graham
  } catch (err) {
    console.error(err.message);
  }
}
main();
```

### Ví dụ 6: Multiple await — đúng vs sai

```js
// ❌ Sai: tuần tự, chậm
async function bad() {
  const a = await fetch("/a");
  const b = await fetch("/b");
  const c = await fetch("/c");
}

// ✅ Đúng: song song, nhanh
async function good() {
  const [a, b, c] = await Promise.all([
    fetch("/a"), fetch("/b"), fetch("/c")
  ]);
}
```

### Ví dụ 7: Retry pattern với async/await

```js
async function retryFetch(url, retries = 3, delay = 1000) {
  for (let i = 0; i < retries; i++) {
    try {
      const res = await fetch(url);
      if (res.ok) return res.json();
    } catch (err) {
      if (i === retries - 1) throw err;
    }
    await new Promise(r => setTimeout(r, delay * Math.pow(2, i)));
  }
}
```

## 🔬 So sánh với alternatives

| Approach | Readability | Error Handling | Parallel Support |
|----------|-------------|----------------|------------------|
| Callback | ❌ Poor | Manual, error-first | None |
| Promise | ⚠️ Medium | `.catch()` | `Promise.all` |
| Async/Await | ✅ Good | `try/catch` | `Promise.all` + `await` |
| Observable | ⚠️ Steep | `.error()` | `forkJoin` |

## 📊 Performance & Best Practices

- **Dùng `Promise.all`** cho requests độc lập — parallel thay vì sequential.
- **Always add `.catch()`** hoặc `try/catch` — tránh unhandled rejection.
- **Kiểm tra `response.ok`** sau fetch — fetch không throw với HTTP error.
- **Avoid nested promises** — dùng async/await thay chain dài.
- **Use async IIFE** nếu cần top-level await: `(async () => { await ... })();`.
- **Reuse promises** — không create mới nếu data không đổi.

## 🔗 Liên kết chéo

- **Xem thêm:** `12_asynchronous-javascript/02_callbacks-promises/01_promise-theory` — promise theory
- **Xem thêm:** `12_asynchronous-javascript/02_callbacks-promises/02_async-await` — async/await syntax
- **Xem thêm:** `12_asynchronous-javascript/02_callbacks-promises/03_promise-concept` — 3 states
- **Xem thêm:** `12_asynchronous-javascript/02_callbacks-promises/04_promise-chain` — chaining
- **Xem thêm:** `12_asynchronous-javascript/02_callbacks-promises/05_promise-static-methods` — all/race/any
- **Xem thêm:** `12_asynchronous-javascript/02_callbacks-promises/07_callback-hell` — callback hell vs promise
- **Xem thêm:** `12_asynchronous-javascript/01_event-loop/02_event-loop` — microtask priority
