# Promise Chain — nối chuỗi `.then()` — [Level: Intermediate]

## 🔑 Khái niệm cốt lõi

`.then()` luôn trả về **một promise mới**, nên bạn có thể **nối tiếp** nhiều bước xử lý thành một chuỗi (chain). Giá trị đẩy xuống bước kế tiếp quyết định bởi những gì bước trước **return**:

- `return` một giá trị thường → bước sau nhận giá trị đó.
- `return` một **promise** → bước sau **chờ promise đó settle xong** rồi mới chạy (đây là cách nối 2 tác vụ bất đồng bộ phụ thuộc nhau).
- Không `return` gì → bước sau nhận `undefined`.

Khi bất kỳ mắt xích nào **throw/reject** → chuỗi dừng tại đó và rơi thẳng xuống `.catch()` gần nhất; các `.then()` phía sau bị bỏ qua. `.finally()` luôn chạy cuối cùng dù thành công hay thất bại.

**Key insight:** Promise chain là **linear pipeline** — mỗi `.then()` nhận output của `.then()` trước, tạo thành dây chuyền xử lý dữ liệu bất đồng bộ.

## 📐 Cấu trúc / Cú pháp

### Promise chain pattern

```js
promise
  .then(result1 => {
    // xử lý result1
    return nextPromise; // hoặc value
  })
  .then(result2 => {
    // result2 = resolved value of nextPromise
    return value;
  })
  .then(result3 => {
    // result3 = value from previous .then
  })
  .catch(error => {
    // bắt lỗi từ ANY previous step
  })
  .finally(() => {
    // cleanup, luôn chạy
  });
```

### Return behavior table

| Return value từ `.then()` | Bước tiếp nhận | Bước tiếp theo chờ? |
|---------------------------|----------------|---------------------|
| Plain value `42` | `42` | ❌ Không |
| `undefined` (no return) | `undefined` | ❌ Không |
| Promise `P` | Resolved value của P | ✅ Có — chờ P settle |
| Thrown error | — | ❌ Chuyển sang `.catch()` |

## ✅ Điểm mạnh — Tại sao nên dùng

1. **Biểu diễn quy trình nhiều bước** phụ thuộc nhau một cách tuyến tính, dễ đọc.
2. **Chờ promise trong promise** (`return` promise) giúp nối các tác vụ async.
3. **Lỗi dừng chuỗi ngay** và chỉ cần một `.catch()` cho cả chuỗi.
4. **Linh hoạt**: pha trộn giá trị thường và promise trong cùng chain.
5. **Short-circuit on error** — reject bỏ qua các `.then()` phía sau.
6. **Clean separation** — mỗi `.then()` xử lý một bước logic.

## ⚠️ Bẫy thường gặp & Hạn chế

### Bẫy 1: Quên `return` — bước sau nhận `undefined`

```js
fetch("/api")
  .then(res => res.json())     // ✅ return promise
  .then(data => console.log(data)) // ❌ không return → undefined xuống bước sau
  .then(result => result.items)  // result = undefined → TypeError
```

### Bẫy 2: `.then` không return promise sẽ không chờ bất đồng bộ

```js
fetch("/api")
  .then(res => {
    res.json(); // ❌ không return — .then tiếp nhận undefined ngay
  })
  .then(data => console.log(data)); // data = undefined
```

### Bẫy 3: Một mắt xích reject bỏ qua mọi `.then()` sau

```js
Promise.resolve(1)
  .then(v => { throw new Error("fail"); })
  .then(v => console.log(v))     // BỎ QUA
  .then(v => console.log(v))     // BỎ QUA
  .catch(err => console.log(err)); // "fail" ✅
```

### Bẫy 4: Chain quá dài khó đọc — cân nhắc async/await

```js
// ❌ Chain dài khó đọc
fetch("/a").then(a => fetch(`/b/${a.id}`))
  .then(b => fetch(`/c/${b.id}`))
  .then(c => render(c))
  .catch(err => handleError(err));

// ✅ async/await cleaner
async function load() {
  try {
    const a = await fetch("/a").then(r => r.json());
    const b = await fetch(`/b/${a.id}`).then(r => r.json());
    const c = await fetch(`/c/${b.id}`).then(r => r.json());
    render(c);
  } catch (err) {
    handleError(err);
  }
}
```

## 💡 Khi nào dùng — Tình huống thực tế

1. **Quy trình dữ liệu**: `getComment()` → lấy `userId` → `getUsersByIds()` → render.
2. **Gọi API tuần tự**: lấy user, lấy bài viết của user, lấy bình luận...
3. **Xử lý dữ liệu qua nhiều bước phép biến đổi**.
4. **Validation pipeline**: fetch → validate schema → transform → save.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Basic chain

```js
Promise.resolve(1)
  .then((v) => v + 1)                      // 2 (giá trị thường)
  .then((v) => new Promise((res) =>
    setTimeout(() => res(v * 10), 0)))     // chờ promise → 20
  .then((v) => console.log(v))             // 20
  .catch((err) => console.log("Fail", err))
  .finally(() => console.log("Done"));     // luôn chạy
```

### Ví dụ 2: Fetch chain thực tế

```js
fetch("https://jsonplaceholder.typicode.com/posts/1")
  .then(response => {
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return response.json();
  })
  .then(post => {
    console.log("Title:", post.title);
    return fetch(`https://jsonplaceholder.typicode.com/users/${post.userId}`);
  })
  .then(response => response.json())
  .then(user => {
    console.log("Author:", user.name);
    console.log("Email:", user.email);
  })
  .catch(err => console.error("Chain failed:", err));
```

### Ví dụ 3: Chained with intermediate validation

```js
function validateAndProcess(data) {
  if (!data || data.length === 0) {
    throw new Error("Empty data");
  }
  return data.filter(item => item.active);
}

fetch("/api/items")
  .then(res => {
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
  })
  .then(validateAndProcess)
  .then(items => {
    console.log(`Found ${items.length} active items`);
    return items.map(item => item.id);
  })
  .then(ids => console.log("IDs:", ids))
  .catch(err => console.error("Error:", err.message));
```

### Ví dụ 4: Error recovery in chain

```js
fetch("/api/data")
  .then(res => {
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
  })
  .catch(err => {
    // recover with fallback data
    console.warn("Primary failed, using fallback:", err.message);
    return { fallback: true, items: [] };
  })
  .then(data => {
    // this runs whether primary or fallback succeeded
    console.log("Data loaded:", data);
  });
```

### Ví dụ 5: Map + Promise chain

```js
const urls = ["/api/a", "/api/b", "/api/c"];

Promise.all(urls.map(url => 
  fetch(url)
    .then(res => {
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return res.json();
    })
))
.then(results => console.log("All results:", results))
.catch(err => console.error("One or more failed:", err));
```

### Ví dụ 6: Sequential dependent chains

```js
// Bước 1: lấy list users
fetch("/api/users")
  .then(res => res.json())
  // Bước 2: với mỗi user, lấy posts
  .then(users => Promise.all(
    users.map(user => 
      fetch(`/api/users/${user.id}/posts`)
        .then(res => res.json())
        .then(posts => ({ user, posts }))
    )
  ))
  // Bước 3: render
  .then(userPosts => {
    userPosts.forEach(({ user, posts }) => {
      console.log(`${user.name}: ${posts.length} posts`);
    });
  })
  .catch(err => console.error("Failed:", err));
```

## 🔬 So sánh với alternatives

| Cách | Syntax | Error handling | Readability |
|------|--------|----------------|-------------|
| Promise chain | `.then().catch()` | `.catch()` at end | ⚠️ Medium |
| Async/await | `await` sequential | `try/catch` | ✅ High |
| Callback | nested | error-first param | ❌ Poor |

## 📊 Performance & Best Practices

- **Luôn `return` từ `.then()`** nếu bước sau cần kết quả.
- **`.catch()` ở cuối chain** để bắt lỗi mọi bước.
- **Giới hạn chain depth ~5 steps** — nếu dài hơn, refactor thành async/await.
- **Avoid `.then().then().then()` deep nesting** — dùng async/await thay.
- **`.finally()` cho cleanup** — loading spinner, close modal, release lock.

## 🔗 Liên kết chéo

- **Xem thêm:** `12_asynchronous-javascript/02_callbacks-promises/01_promise-theory` — promise basics
- **Xem thêm:** `12_asynchronous-javascript/02_callbacks-promises/02_async-await` — async/await alternative
- **Xem thêm:** `12_asynchronous-javascript/02_callbacks-promises/05_promise-static-methods` — Promise.all trong chain
- **Xem thêm:** `12_asynchronous-javascript/02_callbacks-promises/06_promise-example` — real chain example
- **Xem thêm:** `12_asynchronous-javascript/02_callbacks-promises/07_callback-hell` — chain vs callback
