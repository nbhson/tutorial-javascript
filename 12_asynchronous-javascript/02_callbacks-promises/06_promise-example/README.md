# Promise — Ví dụ thực tế (bình luận & người dùng) — [Level: Intermediate]

## 🔑 Khái niệm cốt lõi

Ví dụ tổng hợp ứng dụng promise trong một luồng xử lý dữ liệu thực tế có **3 bước phụ thuộc nhau**:

1. Lấy danh sách **comments**.
2. Từ comments lấy ra các `userId`.
3. Từ userIds lấy các **user** tương ứng → ghép lại → render UI.

Trong đó dữ liệu là mảng object `users` và `comments`; hai hàm `getComment()` và `getUsersByIds(userId)` đều trả về promise (qua `Promise.resolve`) để mô phỏng dữ liệu từ server. Các bước được nối bằng `Promise chain`, kết quả cuối cùng là object `{ users, comments }` được render vào `<ul id="comments-block">`.

Pattern này là **khuôn mẫu chuẩn** cho mọi ứng dụng "lấy dữ liệu → biến đổi → hiển thị" — từ todo app đến social media feed.

## 📐 Cấu trúc / Cú pháp

### Data flow diagram

```
getComments() ──┐
                │  .then(comments => {
                │    userIds = comments.map(c => c.userId)
                │    return getUsersByIds(userIds)
                │  })
                │    .then(users => ({ users, comments }))
                │      .then(data => render(data))
                ▼
getUsersByIds() ──→ Promise.resolve(users)
```

### Expected data shape

```js
// comments
[
  { id: 1, userId: 1, content: "Hay quá!" },
  { id: 2, userId: 2, content: "Tôi cũng vậy" },
  { id: 3, userId: 1, content: "Cảm ơn bạn" }
]

// users
[
  { id: 1, name: "Kien Nguyen" },
  { id: 2, name: "Mai Tran" }
]

// rendered output
<li><strong>Kien Nguyen</strong>: Hay quá!</li>
<li><strong>Mai Tran</strong>: Tôi cũng vậy</li>
<li><strong>Kien Nguyen</strong>: Cảm ơn bạn</li>
```

## ✅ Điểm mạnh — Tại sao nên dùng

1. **Khuôn mẫu chuẩn** cho mọi ứng dụng "lấy dữ liệu → biến đổi → hiển thị".
2. **Tách logic lấy dữ liệu** (promise) khỏi logic render (function).
3. **Ghép nhiều nguồn dữ liệu** (users + comments) trong một chain.
4. **Dễ chuyển sang `fetch` + `async/await`** thật khi có server.
5. **Handle missing data gracefully** — `comments.find()` trả về undefined nếu không match.
6. **Scalable** — thêm bước mới chỉ cần thêm `.then()`.

## ⚠️ Bẫy thường gặp & Hạn chế

### Bẫy 1: `.then` lồng trong `.then` — chain phức tạp

```js
// ❌ Nested then — khó đọc
.getUsersByIds(userIds).then((users) => ({ users, comments }))

// ✅ Flatten với Promise.all
Promise.all([getComments(), getUsersByIds(userIds)]).then(([comments, users]) => ...)
```

### Bẫy 2: userId không tồn tại trong users → `find()` returns undefined

```js
const c = comments.find((c) => c.userId === u.id);
// Nếu c = undefined → c.content → TypeError
// Fix: thêm null check
if (!c) return null;
```

### Bẫy 3: Dữ liệu mẫu cứng (hard-code) trong file

```js
// Cần thay bằng fetch thật khi có backend
return Promise.resolve(mockComments); // hard-coded
```

### Bẫy 4: Chưa xử lý khi dữ liệu trống

```js
// Nếu comments = [] → html = "" → render empty list
// Cần thêm "No comments" message
```

## 💡 Khi nào dùng — Tình huống thực tế

1. **Mọi màn hình cần lấy nhiều nguồn dữ liệu** rồi gộp để render.
2. **Quy trình comments → userIds → users** (dữ liệu quan hệ kiểu "khóa ngoại").
3. **Học cách tổ chức code bất đồng bộ** gọn gàng trước khi dùng framework.
4. **E-commerce**: getProduct → getReviews → getSeller → render page.
5. **Dashboard**: nhiều widgets với data từ các API khác nhau.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Base implementation

```js
// Mock data
const users = [
  { id: 1, name: "Kien Nguyen" },
  { id: 2, name: "Mai Tran" }
];

const comments = [
  { id: 1, userId: 1, content: "Anh Son chua ra video" },
  { id: 2, userId: 2, content: "Hoan toan dong y" },
  { id: 3, userId: 1, content: "Video hay lam" }
];

function getComments() {
  return Promise.resolve(comments);
}

function getUsersByIds(userIds) {
  const filtered = users.filter(u => userIds.includes(u.id));
  return Promise.resolve(filtered);
}

// Chain
getComments()
  .then((comments) => {
    const userIds = comments.map((c) => c.userId);
    return getUsersByIds(userIds).then((users) => ({ users, comments }));
  })
  .then(({ users, comments }) => {
    const html = users
      .map((u) => {
        const c = comments.find((c) => c.userId === u.id);
        return `<li><strong>${u.name}</strong>: ${c ? c.content : "No comment"}</li>`;
      })
      .join("");
    document.querySelector("#comments-block").innerHTML = html;
  })
  .catch((err) => console.error("Failed:", err));
```

### Ví dụ 2: Refactored with Promise.all

```js
getComments()
  .then((comments) => {
    const userIds = [...new Set(comments.map((c) => c.userId))];
    return Promise.all([
      Promise.resolve(comments),
      getUsersByIds(userIds)
    ]);
  })
  .then(([comments, users]) => {
    const html = comments
      .map((c) => {
        const u = users.find((u) => u.id === c.userId);
        return `<li><strong>${u ? u.name : "Unknown"}</strong>: ${c.content}</li>`;
      })
      .join("");
    document.querySelector("#comments-block").innerHTML = html;
  });
```

### Ví dụ 3: Async/await version

```js
async function renderComments() {
  try {
    const comments = await getComments();
    const userIds = [...new Set(comments.map((c) => c.userId))];
    const users = await getUsersByIds(userIds);
    
    const html = comments
      .map((c) => {
        const u = users.find((u) => u.id === c.userId);
        return `<li><strong>${u ? u.name : "Unknown"}</strong>: ${c.content}</li>`;
      })
      .join("");
    
    document.querySelector("#comments-block").innerHTML = html || "<li>No comments</li>";
  } catch (err) {
    console.error("Failed to render comments:", err);
  }
}
renderComments();
```

### Ví dụ 4: With real fetch API

```js
async function renderCommentsLive() {
  try {
    const [commentsRes, usersRes] = await Promise.all([
      fetch("https://jsonplaceholder.typicode.com/comments"),
      fetch("https://jsonplaceholder.typicode.com/users")
    ]);
    
    const comments = await commentsRes.json();
    const users = await usersRes.json();
    
    const html = comments.slice(0, 10) // show first 10
      .map((c) => {
        const u = users.find((u) => u.id === c.userId);
        return `<li><strong>${u ? u.name : "Unknown"}</strong>: ${c.body}</li>`;
      })
      .join("");
    
    document.querySelector("#comments-block").innerHTML = html;
  } catch (err) {
    console.error("Failed:", err);
  }
}
renderCommentsLive();
```

### Ví dụ 5: Loading state management

```js
async function renderCommentsWithLoading() {
  const block = document.querySelector("#comments-block");
  block.innerHTML = "<li>Loading...</li>";
  
  try {
    const [commentsRes, usersRes] = await Promise.all([
      fetch("https://jsonplaceholder.typicode.com/comments"),
      fetch("https://jsonplaceholder.typicode.com/users")
    ]);
    
    const comments = await commentsRes.json();
    const users = await usersRes.json();
    
    const html = comments
      .map((c) => {
        const u = users.find((u) => u.id === c.userId);
        return `<li><strong>${u ? u.name : "?"}</strong>: ${c.body}</li>`;
      })
      .join("");
    
    block.innerHTML = html || "<li>No comments found</li>";
  } catch (err) {
    block.innerHTML = `<li class="error">Failed to load: ${err.message}</li>`;
  }
}
```

## 🔬 So sánh với alternatives

| Pattern | Code shape | Error handling | Best for |
|---------|------------|----------------|----------|
| Promise chain | Nested `.then()` | `.catch()` at end | Simple flows |
| Promise.all + chain | Parallel load | `.catch()` | Multiple sources |
| Async/await | Linear | `try/catch` | Complex flows |

## 📊 Performance & Best Practices

- **Dùng `Promise.all`** khi các requests độc lập — parallel thay vì sequential.
- **Add loading state** — UX tốt hơn khi chờ data.
- **Handle empty results** — show "No data" message instead of blank.
- **Limit results** — `slice(0, N)` để tránh render quá nhiều DOM nodes.
- **Migrate to fetch** — thay mock data bằng real API calls khi ready.

## 🔗 Liên kết chéo

- **Xem thêm:** `12_asynchronous-javascript/02_callbacks-promises/04_promise-chain` — chain pattern
- **Xem thêm:** `12_asynchronous-javascript/02_callbacks-promises/05_promise-static-methods` — Promise.all
- **Xem thêm:** `12_asynchronous-javascript/02_callbacks-promises/02_async-await` — async/await version
- **Xem thêm:** `13_working-with-apis/01_fetch` — real fetch implementation
- **Xem thêm:** `13_working-with-apis/05_crud` — CRUD pattern extension
