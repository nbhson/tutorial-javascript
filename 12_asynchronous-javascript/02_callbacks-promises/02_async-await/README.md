# async / await — [Level: Intermediate]

## 🔑 Khái niệm cốt lõi

`async/await` là cú pháp (ES2017) giúp làm việc với promise **như code đồng bộ** — dễ đọc hơn nhiều so với chuỗi `.then()`.

- Thêm `async` trước một hàm → hàm trở thành **async function**, luôn trả về một Promise.
- Bên trong async function, dùng `await` trước một lời gọi trả về promise: code **chờ** tại điểm đó cho đến khi promise settle. If fulfilled → nhận được giá trị; if rejected → lỗi được **ném ra** như throw.

```js
async function fetchProducts() {
  try {
    const response = await fetch(".../products.json"); // chờ fetch()
    if (!response.ok) {
      throw new Error(`HTTP error: ${response.status}`);
    }
    const data = await response.json(); // chờ parse JSON
    console.log(data[0].name);
  } catch (error) {
    console.error(`Could not get products: ${error}`);
  }
}
```

**Điểm cốt lõi:** `await` chỉ hợp lệ **bên trong async function**. Có thể dùng `try/catch` quen thuộc để bắt lỗi thay vì `.catch`.

**Lưu ý quan trọng:** `await` **không chặn thread** — nó tạm dừng execution của async function, cho phép event loop xử lý task khác, rồi tiếp tục khi promise settle.

## 📐 Cấu trúc / Cú pháp

### Async function declaration

```js
// Function declaration
async function name(params) { ... }

// Function expression
const name = async function(params) { ... };

// Arrow function
const name = async (params) => { ... };

// Method
const obj = { async method() { ... } };

// Class method
class Foo { async method() { ... } }
```

### Await expression

```js
const result = await promise;
// equivalent to:
// promise.then(result => { ... })
```

### Top-level await (ES2022+)

```js
// Bây giờ có thể dùng await ở top-level module
const data = await fetch("/api/data").then(r => r.json());
```

## ✅ Điểm mạnh — Tại sao nên dùng

1. **Code nhìn tuần tự, dễ đọc**, dễ bảo trì cho chuỗi nhiều bước.
2. **Lỗi xử lý bằng `try/catch` truyền thống** — quen thuộc với đa số dev.
3. **Vẫn đầy đủ sức mạnh promise**: `Promise.all` kết hợp được với `await`.
4. **Giảm "callback hell" và chain `.then()` dài ngoằng**.
5. **Debug dễ hơn** — stack trace rõ ràng, không bị mất như callback.
6. **Conditional await** — có thể `await` trong if/else, loop, v.v.
7. **Value extraction straightforward** — không cần `.then(value => ...)`.

## ⚠️ Bẫy thường gặp & Hạn chế

### Bẫy 1: Quên `await` — nhận về Promise thay vì value

```js
async function getData() {
  const response = fetch("/api"); // ❌ quên await — response là Promise
  const data = await response.json(); // TypeError: response.json is not a function
}
```

### Bẫy 2: `await` ngoài async function → SyntaxError

```js
const data = await fetch("/api"); // ❌ SyntaxError (trừ top-level await)
```

### Bẫy 3: `await` tuần tự nhiều tác vụ độc lập → chậm

```js
// ❌ Chậm: chờ từng cái
const a = await fetch("/a");
const b = await fetch("/b");

// ✅ Nhanh: song song
const [a, b] = await Promise.all([fetch("/a"), fetch("/b")]);
```

### Bẫy 4: Unhandled rejection — lỗi bỏ rơi nếu không try/catch

```js
async function risky() {
  const data = await fetch("/api"); // nếu fetch throw → unhandled
}
risky(); // không catch → unhandled rejection
```

### Bẫy 5: Catch không bắt lỗi synchronous trong async function

```js
async function broken() {
  throw new Error("sync error"); // ✅ được catch bởi try/catch
  const data = await fetch("/api");
}
```

## 💡 Khi nào dùng — Tình huống thực tế

1. **Đọc/ghi dữ liệu tuần tự phụ thuộc nhau** (tạo -> sửa -> hiển thị).
2. **Mọi tác vụ fetch/API** — đặc biệt khi cần xử lý nhiều bước.
3. **Làm sạch callback chain** khi migrate code cũ sang promise.
4. **Parallel operations** — `Promise.all` với `await`.
5. **Sequential with condition** — `if (cond) await step1(); else await step2();`

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Basic async/await

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

### Ví dụ 2: Sequential vs Parallel

```js
// ❌ Sequential — chờ từng request
async function slow() {
  const users = await fetch("/api/users").then(r => r.json());
  const posts = await fetch("/api/posts").then(r => r.json());
  const comments = await fetch("/api/comments").then(r => r.json());
  render(users, posts, comments);
}

// ✅ Parallel — tất cả cùng lúc
async function fast() {
  const [usersRes, postsRes, commentsRes] = await Promise.all([
    fetch("/api/users"),
    fetch("/api/posts"),
    fetch("/api/comments")
  ]);
  const [users, posts, comments] = await Promise.all([
    usersRes.json(),
    postsRes.json(),
    commentsRes.json()
  ]);
  render(users, posts, comments);
}
```

### Ví dụ 3: Conditional await

```js
async function processUser(userId) {
  const userRes = await fetch(`/api/users/${userId}`);
  if (!userRes.ok) throw new Error("User not found");
  
  const user = await userRes.json();
  
  // conditional: chỉ fetch posts nếu user có posts
  if (user.hasPosts) {
    const postsRes = await fetch(`/api/users/${userId}/posts`);
    user.posts = await postsRes.json();
  }
  
  return user;
}
```

### Ví dụ 4: Loop với await

```js
async function processAll(items) {
  const results = [];
  for (const item of items) {
    const res = await fetch(`/api/items/${item.id}`);
    const data = await res.json();
    results.push(data);
  }
  return results;
}

// Better: parallel trong loop
async function processAllParallel(items) {
  const promises = items.map(item => 
    fetch(`/api/items/${item.id}`).then(r => r.json())
  );
  return Promise.all(promises);
}
```

### Ví dụ 5: Retry với async/await

```js
async function fetchWithRetry(url, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      const res = await fetch(url);
      if (res.ok) return res.json();
    } catch (err) {
      if (i === maxRetries - 1) throw err;
    }
    await new Promise(r => setTimeout(r, 1000 * Math.pow(2, i)));
  }
}
```

### Ví dụ 6: Async IIFE (self-executing)

```js
(async function() {
  const data = await fetch("/api/data").then(r => r.json());
  console.log(data);
})();
```

### Ví dụ 7: Error handling pattern

```js
async function safeFetch(url) {
  try {
    const res = await fetch(url);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } catch (error) {
    console.error(`Failed to fetch ${url}:`, error.message);
    return null;
  }
}
```

## 🔬 So sánh với alternatives

| Cách | Syntax | Error handling | Readability |
|------|--------|----------------|-------------|
| Promise chain | `.then().catch()` | `.catch()` | ⚠️ Medium |
| Async/await | `await promise` | `try/catch` | ✅ High |
| Callback | `fn(callback)` | error-first | ❌ Poor |

## 📊 Performance & Best Practices

- **Luôn dùng `Promise.all`** cho independent awaits — chạy song song.
- **Always wrap in try/catch** — tránh unhandled rejection.
- **Kiểm tra `response.ok`** sau await fetch.
- **Avoid await in tight loops** — dùng `Promise.all` thay.
- **Top-level await** available in ES2022 modules — dùng trực tiếp không cần IIFE.
- **Async function always returns Promise** — even if you return a plain value.

## 🔗 Liên kết chéo

- **Xem thêm:** `12_asynchronous-javascript/02_callbacks-promises/01_promise-theory` — promise foundation
- **Xem thêm:** `12_asynchronous-javascript/02_callbacks-promises/03_promise-concept` — promise states
- **Xem thêm:** `12_asynchronous-javascript/02_callbacks-promises/04_promise-chain` — chain alternative
- **Xem thêm:** `12_asynchronous-javascript/02_callbacks-promises/05_promise-static-methods` — Promise.all với await
- **Xem thêm:** `12_asynchronous-javascript/01_event-loop/02_event-loop` — await = microtask
- **Xem thêm:** `13_working-with-apis/01_fetch` — fetch + async/await pattern
