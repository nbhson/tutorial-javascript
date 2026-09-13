# Làm việc với APIs (Working with APIs) — [Level: Intermediate]

## 🔑 Khái niệm cốt lõi

**API (Application Programming Interface)** là "cổng giao tiếp" giữa các phần mềm. Trong phát triển web, chúng ta thường dùng **REST API**: gửi HTTP request tới server để **tạo / đọc / sửa / xóa** dữ liệu theo các phương thức:

| Phương thức | Mục đích | Ví dụ |
|-------------|----------|-------|
| `GET` | Đọc dữ liệu (Read) | lấy danh sách khóa học |
| `POST` | Tạo mới (Create) | thêm khóa học |
| `PUT` / `PATCH` | Cập nhật (Update) | sửa toàn bộ / sửa một phần |
| `DELETE` | Xóa (Delete) | xóa khóa học |

Để gọi API từ JS có các công cụ chính:

- **`fetch()`** — hiện đại, dựa trên Promise, cú pháp gọn. Default không send cookie cross-origin.
- **`XMLHttpRequest` (XHR)** — tiền thân của fetch, dựa trên callback. Hỗ trợ progress tracking.
- **JSON Server** — giả lập REST server bằng file JSON để phát triển/prototype nhanh.
- **Postman / Thunder Client** — kiểm thử API bằng giao diện mà không cần viết code.
- **Service Worker** — cache requests, support offline, background sync.

**Quan trọng:** `fetch` chỉ trả lỗi khi **mạng hỏng** (network error). HTTP error (404, 500) vẫn resolve bình thường — bạn phải tự kiểm tra `res.ok` / `res.status`.

## 📐 Cấu trúc / Cú pháp

### Fetch API signature

```js
fetch(url, {
  method: "GET",           // GET, POST, PUT, PATCH, DELETE
  headers: {               // custom headers
    "Content-Type": "application/json",
    "Authorization": "Bearer token"
  },
  body: JSON.stringify(data), // POST/PUT body (string)
  credentials: "include",    // send cookies cross-origin
  mode: "cors",             // cors, no-cors, same-origin
  cache: "default"          // default, no-store, reload, force-cache
})
  .then(res => {
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();      // hoặc .text(), .blob(), .formData()
  })
  .then(data => ...)
  .catch(err => console.error(err));
```

### HTTP Method reference table

| Method | Safe? | Idempotent? | Body? | Typical use |
|--------|-------|-------------|-------|-------------|
| `GET` | ✅ | ✅ | ❌ | Read data |
| `POST` | ❌ | ❌ | ✅ | Create resource |
| `PUT` | ❌ | ✅ | ✅ | Update full resource |
| `PATCH` | ❌ | ❌ | ✅ | Update partial resource |
| `DELETE` | ❌ | ✅ | ❌ | Delete resource |

## ✅ Điểm mạnh — Tại sao nên dùng

1. **Tách frontend và backend** — chỉ trao đổi dữ liệu qua HTTP, không phụ thuộc implementation.
2. **`fetch` + Promise/async-await** giúp code gọi API ngắn gọn, dễ lỗi rất rõ ràng.
3. **JSON Server** cho phép làm CRUD đầy đủ mà không cần backend thật — prototype nhanh.
4. **Postman** kiểm thử nhanh trước khi viết code — tiết kiệm thời gian debug.
5. **Service Worker** giúp nâng cao trải nghiệm offline, background sync, push notification.
6. **CORS** chuẩn hóa cross-origin requests giữa các domain.
7. **JSON format** lightweight, human-readable, native JS support (`JSON.parse`/`stringify`).
8. **RESTful design** predictable URLs và methods — developer experience tốt.

## ⚠️ Bẫy thường gặp & Hạn chế

### Bẫy 1: Fetch không throw với HTTP error

```js
fetch("/api/missing")
  .then(res => {
    console.log(res.status); // 404 — nhưng promise vẫn resolved!
    // Phải tự check:
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
  });
```

### Bẫy 2: CORS blocking cross-origin requests

```js
// Nếu server không set Access-Control-Allow-Origin header
fetch("https://other-domain.com/api")
  .catch(err => console.error("CORS error:", err));
```

### Bẫy 3: XHR verbose và callback-based

```js
const xhr = new XMLHttpRequest();
xhr.open("GET", url);
xhr.onload = function() {
  if (xhr.status >= 200 && xhr.status < 300) {
    console.log(xhr.responseText);
  } else {
    console.error("Error", xhr.status);
  }
};
xhr.onerror = () => console.error("Network error");
xhr.send();
// Dài dòng so với fetch
```

### Bẫy 4: JSON Server chỉ là giả lập

```bash
# Chỉ chạy localhost, data lưu file — không production-ready
json-server --watch server.json
```

### Bẫy 5: Fetch mặc định không send cookie cross-origin

```js
fetch("https://api.example.com/data", {
  credentials: "include" // must specify for cross-origin cookies
});
```

### Bẫy 6: Không abort fetch request — memory leak

```js
const controller = new AbortController();
const signal = controller.signal;

fetch("/api/slow", { signal })
  .then(res => res.json())
  .catch(err => {
    if (err.name === "AbortError") {
      console.log("Request cancelled");
    }
  });

// Hủy sau 5 giây
setTimeout(() => controller.abort(), 5000);
```

## 💡 Khi nào dùng — Tình huống thực tế

1. **Mọi ứng dụng cần dữ liệu động** từ server: blog, shop, admin panel, dashboard.
2. **Prototype nhanh giao diện** với JSON Server trước khi có backend.
3. **Kiểm tra server/API** của đồng nghiệp bằng Postman trước khi tích hợp.
4. **Build PWA** có offline experience bằng Service Worker.
5. **Real-time features** — WebSocket, Server-Sent Events.
6. **File upload/download** — FormData với fetch.
7. **Authentication flows** — login, token refresh, JWT storage.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: GET đơn giản với fetch

```js
fetch("https://jsonplaceholder.typicode.com/posts")
  .then((res) => {
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
  })
  .then((posts) => console.log(posts.length)) // 100
  .catch((err) => console.error(err));
```

### Ví dụ 2: GET với async/await

```js
async function getPosts() {
  const res = await fetch("https://jsonplaceholder.typicode.com/posts");
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const posts = await res.json();
  return posts;
}
getPosts().then(posts => console.log(posts[0].title));
```

### Ví dụ 3: POST tạo mới

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
```

### Ví dụ 4: DELETE resource

```js
async function deletePost(id) {
  const res = await fetch(`https://jsonplaceholder.typicode.com/posts/${id}`, {
    method: "DELETE"
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return true;
}
```

### Ví dụ 5: Multiple parallel requests

```js
async function loadDashboard() {
  const [postsRes, usersRes, commentsRes] = await Promise.all([
    fetch("https://jsonplaceholder.typicode.com/posts"),
    fetch("https://jsonplaceholder.typicode.com/users"),
    fetch("https://jsonplaceholder.typicode.com/comments")
  ]);
  
  const [posts, users, comments] = await Promise.all([
    postsRes.json(),
    usersRes.json(),
    commentsRes.json()
  ]);
  
  return { posts, users, comments };
}
```

### Ví dụ 6: Form submission với FormData

```js
async function uploadImage(file) {
  const formData = new FormData();
  formData.append("image", file);
  
  const res = await fetch("/api/upload", {
    method: "POST",
    body: formData // tự động set Content-Type với boundary
  });
  return res.json();
}
```

### Ví dụ 7: Request với timeout (AbortController)

```js
async function fetchWithTimeout(url, timeoutMs = 5000) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), timeoutMs);
  
  try {
    const res = await fetch(url, { signal: controller.signal });
    clearTimeout(timeout);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
  } catch (err) {
    clearTimeout(timeout);
    if (err.name === "AbortError") throw new Error("Timeout");
    throw err;
  }
}
```

## 🔬 So sánh với alternatives

| Công cụ |.Syntax | Promise? | Progress | Browser support |
|---------|--------|----------|----------|-----------------|
| `fetch` | Modern | ✅ | ❌ | Modern browsers |
| `XMLHttpRequest` | Legacy | ❌ | ✅ | All browsers |
| `axios` | Library | ✅ | ✅ | All + Node |
| `jQuery.ajax` | Library | ✅ | ⚠️ | All (với jQuery) |

## 📊 Performance & Best Practices

- **Always check `response.ok`** sau fetch — fetch không throw với HTTP error.
- **Use `Promise.all`** cho parallel independent requests.
- **Set proper headers** — `Content-Type: application/json` cho POST/PUT.
- **Handle errors at every level** — network error, HTTP error, parse error.
- **Use `AbortController`** cho timeout và cancel request.
- **Cache strategically** — `cache: "no-store"` cho fresh data, `"force-cache"` cho offline.
- **JSON Server** cho prototype — chuyển sang real API khi ready.
- **Postman/Thunder** cho API testing trước khi code.

## 🔗 Liên kết chéo

- **Xem thêm:** `13_working-with-apis/01_fetch` — fetch API chi tiết
- **Xem thêm:** `13_working-with-apis/02_xmlhttprequest` — XHR legacy approach
- **Xem thêm:** `13_working-with-apis/03_json-server` — fake REST server
- **Xem thêm:** `13_working-with-apis/04_postman` — API testing tool
- **Xem thêm:** `13_working-with-apis/05_crud` — full CRUD example
- **Xem thêm:** `13_working-with-apis/06_service-worker` — offline/cache
- **Xem thêm:** `12_asynchronous-javascript/02_callbacks-promises/01_promise-theory` — promise foundation
- **Xem thêm:** `12_asynchronous-javascript/02_callbacks-promises/02_async-await` — async/await with fetch
