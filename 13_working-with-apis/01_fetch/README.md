# Fetch API — [Level: Intermediate]

## 🔑 Khái niệm cốt lõi

**Fetch API** là cách hiện đại để gọi HTTP từ JavaScript. `fetch(url, options)` nhận URL (+ tùy chọn `method`, `headers`, `body`...) và trả về một **Promise** — kết quả là object `Response`.

Luồng xử lý chuẩn:

```js
fetch(url)            // → Promise<Response>
  .then((res) => res.json()) // parse thân dữ liệu (cũng là promise)
  .then((data) => ...)       // dùng dữ liệu
  .catch((err) => ...);      // bắt lỗi mạng
```

`res.json()` đọc toàn bộ thân response và chuyển thành object từ JSON. Các bước nối tiếp nhau qua promise chain — cùng pattern như khi gọi `Promise.all`.

> ⚠️ **Quan trọng:** `fetch` chỉ trả lỗi khi **mạng hỏng** (network error). HTTP lỗi (404, 500, 503) vẫn **resolve bình thường** — `res.ok` sẽ là `false` nhưng promise không reject. Bạn phải tự kiểm tra `res.ok` / `res.status` rồi `throw` nếu muốn bắt lỗi.

## 📐 Cấu trúc / Cú pháp

### Fetch options

```js
fetch(url, {
  method: "GET",           // GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS
  headers: {
    "Content-Type": "application/json",
    "Authorization": "Bearer <token>",
    "Custom-Header": "value"
  },
  body: JSON.stringify({ key: "value" }), // POST/PUT/PATCH only
  credentials: "omit",     // "omit" | "same-origin" | "include"
  mode: "cors",           // "cors" | "same-origin" | "no-cors"
  cache: "default",       // "default" | "no-store" | "reload" | "force-cache" | "only-if-cached"
  redirect: "follow",     // "follow" | "error" | "manual"
  referrer: "client",     // string hoặc ""
  integrity: "",          // subresource integrity hash
  signal: abortController.signal, // hủy request
  keepalive: false,       // cho background send
  window: null            // chỉ browser,通常为 null
});
```

### Response object properties

| Property | Type | Mô tả |
|----------|------|-------|
| `res.ok` | `boolean` | `true` nếu status 200-299 |
| `res.status` | `number` | HTTP status code (200, 404, 500...) |
| `res.statusText` | `string` | Status message ("OK", "Not Found") |
| `res.headers` | `Headers` | Response headers |
| `res.url` | `string` | Final URL (sau redirect) |
| `res.type` | `string` | "basic", "cors", "opaque", "error" |
| `res.body` | `ReadableStream` | Raw body stream |

### Response parsing methods

| Method | Returns | Use case |
|--------|---------|----------|
| `res.json()` | Promise\<any\> | JSON response (most common) |
| `res.text()` | Promise\<string\> | Plain text / HTML |
| `res.blob()` | Promise\<Blob\> | Binary data, images |
| `res.formData()` | Promise\<FormData\> | Multipart form |
| `res.arrayBuffer()` | Promise\<ArrayBuffer\> | Binary buffer |

## ✅ Điểm mạnh — Tại sao nên dùng

1. **Promise-based** → kết hợp tốt với async/await, `Promise.all`.
2. **Cú pháp ngắn gọn**, dễ đọc so với XMLHttpRequest.
3. **Hỗ trợ mọi phương thức HTTP** (GET, POST, PUT, PATCH, DELETE) qua `options`.
4. **Được hỗ trợ rộng rãi** trên browser và Node.js hiện đại (Node 18+).
5. **Dễ lấy nhiều nguồn cùng lúc** bằng `Promise.all([...])`.
6. **AbortController** — hủy request đang chạy.
7. **Streaming body** — `res.body` là ReadableStream, xử lý data lớn không load hết vào memory.
8. **CORS support** — chuẩn cross-origin, configurable qua headers.

## ⚠️ Bẫy thường gặp & Hạn chế

### Bẫy 1: Fetch không throw với HTTP error

```js
fetch("/api/missing")
  .then(res => {
    console.log(res.status); // 404 — nhưng promise vẫn resolved!
    // Phải tự check:
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
  })
  .catch(err => console.error(err)); // chỉ bắt network error
```

### Bẫy 2: Phải chờ `res.json()` (chính nó là promise) trước khi dùng dữ liệu

```js
fetch("/api/data")
  .then(res => res.json())  // ✅ đúng — await promise
  .then(data => console.log(data));

// ❌ Sai:
fetch("/api/data")
  .then(res => {
    const data = res.json(); // data là Promise, chưa resolve!
    console.log(data); // Promise { <pending> }
  });
```

### Bẫy 3: Default không gửi cookie trên cross-origin

```js
// Same-origin: cookie gửi tự động
fetch("/api/data");

// Cross-origin: phải chỉ định
fetch("https://api.example.com/data", {
  credentials: "include" // send cookies
});
```

### Bẫy 4: POST body phải stringify

```js
// ❌ Sai — object không tự convert
fetch("/api/users", {
  method: "POST",
  body: { name: "John" } // → "[object Object]"
});

// ✅ Đúng
fetch("/api/users", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ name: "John" })
});
```

### Bẫy 5: Redirect automatic — `res.url` là final URL

```js
fetch("http://example.com/redirect")
  .then(res => console.log(res.url)); 
// "https://example.com/" — sau khi redirect
```

### Bẫy 6: Network error chỉ bắt được bằng `.catch()`, không phải by status

```js
fetch("https://offline.example.com")
  .catch(err => console.error("Network error:", err)); 
// Chỉ chạy khi truly network failure, KHÔNG chạy với 404
```

## 💡 Khi nào dùng — Tình huống thực tế

1. **Tải danh sách / chi tiết dữ liệu** từ REST API.
2. **Gửi dữ liệu lên server** (POST/PUT/PATCH/DELETE).
3. **Gọi nhiều endpoint song song** và gộp kết quả.
4. **Upload file** — FormData + fetch.
5. **Stream large data** — đọc từng chunk qua `res.body`.
6. **Abort long-running requests** — user navigates away.
7. **Authenticated requests** — Bearer token in headers.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Basic GET

```js
const postApi = "https://jsonplaceholder.typicode.com/posts";

fetch(postApi)
  .then((res) => {
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
  })
  .then((posts) => console.log("posts:", posts.length))   // 100
  .catch((err) => console.error(err));
```

### Ví dụ 2: Multi-fetch bằng Promise.all

```js
const postApi = "https://jsonplaceholder.typicode.com/posts";
const todoApi = "https://jsonplaceholder.typicode.com/todos";

Promise.all([
  fetch(postApi).then((res) => res.json()),
  fetch(todoApi).then((res) => res.json())
])
  .then(([posts, todos]) => {
    console.log("Posts:", posts.length);    // 100
    console.log("Todos:", todos.length);    // 200
    console.log("Total:", posts.concat(todos).length); // 300
  })
  .catch((err) => console.error(err));
```

### Ví dụ 3: GET with async/await

```js
async function getPosts() {
  const res = await fetch("https://jsonplaceholder.typicode.com/posts");
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const posts = await res.json();
  return posts;
}

getPosts().then(posts => console.log(posts[0].title));
```

### Ví dụ 4: POST create

```js
async function createPost(title, body) {
  const res = await fetch("https://jsonplaceholder.typicode.com/posts", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, body, userId: 1 })
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

createPost("New Post", "Body content")
  .then(post => console.log("Created:", post));
```

### Ví dụ 5: PUT/PATCH update

```js
// PUT — replace toàn bộ
async function updatePost(id, data) {
  const res = await fetch(`https://jsonplaceholder.typicode.com/posts/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });
  return res.json();
}

// PATCH — update một phần
async function patchPost(id, updates) {
  const res = await fetch(`https://jsonplaceholder.typicode.com/posts/${id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(updates)
  });
  return res.json();
}
```

### Ví dụ 6: DELETE

```js
async function deletePost(id) {
  const res = await fetch(`https://jsonplaceholder.typicode.com/posts/${id}`, {
    method: "DELETE"
  });
  // 200-299 = success, thường không có body
  return res.ok;
}
```

### Ví dụ 7: AbortController — timeout/cancel

```js
async function fetchWithAbort(url, timeoutMs = 5000) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);
  
  try {
    const res = await fetch(url, { signal: controller.signal });
    clearTimeout(timeoutId);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
  } catch (err) {
    clearTimeout(timeoutId);
    if (err.name === "AbortError") throw new Error("Request timed out");
    throw err;
  }
}
```

### Ví dụ 8: File upload với FormData

```js
async function uploadFile(file) {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("metadata", JSON.stringify({ uploadedBy: "user1" }));
  
  const res = await fetch("/api/upload", {
    method: "POST",
    body: formData // không cần set Content-Type — browser tự thêm boundary
  });
  return res.json();
}
```

### Ví dụ 9: Streaming response body

```js
async function streamResponse(url) {
  const res = await fetch(url);
  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    const chunk = decoder.decode(value);
    console.log("Chunk:", chunk);
  }
}
```

### Ví dụ 10: Generic fetch wrapper

```js
const api = {
  async get(url) {
    const res = await fetch(url);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
  },
  async post(url, data) {
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
  },
  async delete(url) {
    const res = await fetch(url, { method: "DELETE" });
    return res.ok;
  }
};

// Usage
api.get("/api/posts").then(posts => console.log(posts));
api.post("/api/posts", { title: "New" }).then(post => console.log(post));
api.delete("/api/posts/1").then(ok => console.log("Deleted:", ok));
```

## 🔬 So sánh với alternatives

| API | Promise? | Progress | Timeout | Browser support |
|-----|----------|----------|---------|-----------------|
| `fetch` | ✅ | ❌ | AbortController | Modern |
| `XMLHttpRequest` | ❌ | ✅ | `.timeout` | All |
| `axios` | ✅ | ✅ | `timeout` option | All + Node |
| `jQuery.ajax` | ✅ | ⚠️ | `timeout` | Requires jQuery |

## 📊 Performance & Best Practices

- **Always check `res.ok`** — fetch không throw với HTTP error.
- **Use `Promise.all`** cho parallel requests — nhanh hơn sequential.
- **Set proper headers** — `Content-Type: application/json` cho POST/PUT.
- **Use `AbortController`** cho timeout và cancel — tránh memory leak.
- **Cache strategically** — `cache: "no-store"` cho fresh data, `"force-cache"` offline.
- **Stream large responses** — dùng `res.body` reader thay vì `.json()` cho data lớn.
- **Create wrapper utility** — generic `api.get/post/delete` để reuse code.
- **Handle all error types** — network error, HTTP error, parse error.

## 🔗 Liên kết chéo

- **Xem thêm:** `13_working-with-apis/02_xmlhttprequest` — XHR legacy alternative
- **Xem thêm:** `13_working-with-apis/03_json-server` — mock server cho fetch
- **Xem thêm:** `13_working-with-apis/05_crud` — CRUD đầy đủ với fetch
- **Xem thêm:** `12_asynchronous-javascript/02_callbacks-promises/01_promise-theory` — promise foundation
- **Xem thêm:** `12_asynchronous-javascript/02_callbacks-promises/02_async-await` — async/await + fetch
- **Xem thêm:** `12_asynchronous-javascript/02_callbacks-promises/05_promise-static-methods` — Promise.all với fetch
