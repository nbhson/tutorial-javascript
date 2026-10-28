# Promise — Lý thuyết nền tảng — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

**Promise** là đối tượng được trả về bởi một hàm bất đồng bộ, **đại diện cho trạng thái hiện tại** của hoạt động đó. Promises chính là nền tảng của lập trình bất đồng bộ hiện đại trong JavaScript.

Một promise có 3 trạng thái:
- `pending` — promise đã được tạo, tác vụ chưa thành công hoặc thất bại.
- `fulfilled` — tác vụ **thành công**; khi đó handler `.then()` được gọi.
- `rejected` — tác vụ **thất bại**; khi đó handler `.catch()` được gọi.

**Đặc tính quan trọng:** Promise **chỉ settle một lần** — trạng thái không bao giờ quay lại `pending` sau khi đã fulfilled hoặc rejected. Một khi settled, giá trị/lý do bị đóng băng.

 executor function chạy **ngay lập tức** khi `new Promise()` được gọi — không đợi ai gọi `.then()`. Đây là điểm khác biệt then chốt so với lazy evaluation.

## 📐 Cấu trúc / Cú pháp

### Promise constructor

```js
const promise = new Promise((resolve, reject) => {
  // executor chạy ngay lập tức
  if (success) {
    resolve(value);    // chuyển sang fulfilled
  } else {
    reject(error);     // chuyển sang rejected
  }
});
```

### Promise methods chain

```js
promise
  .then(onFulfilled)      // chạy khi fulfilled
  .then(onFulfilled2)     // tiếp nối chain
  .catch(onRejected)      // bắt lỗi từ any previous step
  .finally(onSettled);    // luôn chạy, bất kể fulfilled/rejected
```

### Bảng trạng thái transitions

| State hiện tại | Gọi `resolve()` | Gọi `reject()` | Không gọi gì |
|----------------|-----------------|----------------|--------------|
| `pending` | → `fulfilled` | → `rejected` | Giữ `pending` (memory leak!) |
| `fulfilled` | No-op | No-op | Giữ `fulfilled` |
| `rejected` | No-op | No-op | Giữ `rejected` |

## ✅ Điểm mạnh — Tại sao nên dùng

1. **Ưu tiên cao (microtask)**: kết quả được xử lý ngay khi call stack trống — chạy trước setTimeout.
2. **Xử lý lỗi tập trung**, tránh lồng callback.
3. **Dễ kết hợp nhiều promise** bằng `Promise.all`, `Promise.race`, `Promise.allSettled`.
4. **Nền tảng cho `async/await`** — async/await là syntactic sugar trên promise.
5. **State là không thể đảo ngược** — promise settled một lần, không thể thay đổi, đảm bảo consistency.
6. **Chainable** — `.then()` trả về promise mới, nối tiếp vô hạn.
7. **Error propagation** — lỗi tự động propagate xuống `.catch()` gần nhất.

## ⚠️ Bẫy thường gặp & Hạn chế

### Bẫy 1: Quên `.catch()` — unhandled rejection

```js
const p = new Promise((_, reject) => reject("Error"));
p.then(value => console.log(value));
// UnhandledPromiseRejection: Error
// Fix: thêm .catch(err => console.error(err))
```

### Bẫy 2: Promise treo vĩnh viễn (memory leak)

```js
const broken = new Promise((resolve, reject) => {
  // không gọi resolve cũng không gọi reject
  // Promise sẽ pending mãi mãi
});
broken.then(() => console.log("never runs"));
```

### Bẫy 3: Promise chỉ settle một lần — call resolve nhiều lần chỉ lần đầu có effect

```js
const p = new Promise((resolve) => {
  resolve(1);
  resolve(2); // bị ignore
  setTimeout(() => resolve(3), 100); // cũng ignore
});
p.then(v => console.log(v)); // 1
```

### Bẫy 4: Fetch không throw khi HTTP error — phải tự check `response.ok`

```js
fetch("/api/missing")
  .then(res => {
    console.log(res.status); // 404 — nhưng promise vẫn resolved!
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
  })
  .catch(err => console.error(err));
```

### Bẫy 5: `.then()` luôn trả về promise mới — chain không tự động await

```js
const p1 = Promise.resolve(1);
const p2 = p1.then(v => v + 1); // p2 là promise mới, fulfilled với 2
console.log(p1 === p2); // false — different objects
```

## 💡 Khi nào dùng — Tình huống thực tế

1. **Fetch dữ liệu**, gọi API, đọc file — bất kỳ tác vụ bất đồng bộ nào.
2. **Xử lý theo giai đoạn**: kiểm tra response → parse JSON → render.
3. **Chờ nhiều tác vụ cùng lúc** (`Promise.all`).
4. **Wrap legacy callback API** thành promise để dùng modern syntax.
5. **Timeout pattern** — `Promise.race([task, timeout])`.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Basic promise create and consume

```js
// Tạo promise từ setTimeout
const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

delay(1000).then(() => console.log("1 second passed"));
```

### Ví dụ 2: Promise with resolve/reject

```js
const checkAge = (age) => {
  return new Promise((resolve, reject) => {
    if (age >= 18) {
      resolve(`Allowed: ${age} years old`);
    } else {
      reject(`Denied: ${age} years old`);
    }
  });
};

checkAge(20)
  .then(msg => console.log(msg))   // "Allowed: 20 years old"
  .catch(err => console.log(err)); // không chạy

checkAge(15)
  .then(msg => console.log(msg))   // không chạy
  .catch(err => console.log(err)); // "Denied: 15 years old"
```

### Ví dụ 3: Promise chain với fetch

```js
fetch("https://jsonplaceholder.typicode.com/posts/1")
  .then((response) => {
    if (!response.ok) {
      throw new Error(`HTTP error: ${response.status}`);
    }
    return response.json();   // trả về promise → nối tiếp .then
  })
  .then((data) => console.log(data.title))
  .catch((error) => console.error(`Could not get post: ${error}`));
```

### Ví dụ 4: Promise.finally — cleanup luôn chạy

```js
isLoading = true;
fetch("/api/data")
  .then(res => res.json())
  .catch(err => console.error(err))
  .finally(() => {
    isLoading = false; // luôn chạy, dù success hay error
  });
```

### Ví dụ 5: Convert callback to promise (wrapping)

```js
function readFileAsync(path) {
  return new Promise((resolve, reject) => {
    fs.readFile(path, "utf8", (err, data) => {
      if (err) reject(err);
      else resolve(data);
    });
  });
}
```

### Ví dụ 6: Promise.all error behavior — fail fast

```js
const p1 = Promise.resolve(1);
const p2 = Promise.reject("error");
const p3 = Promise.resolve(3);

Promise.all([p1, p2, p3])
  .then(values => console.log(values))  // không chạy
  .catch(err => console.log(err));      // "error" — fail fast
```

## 🔬 So sánh với alternatives

| Cách | Promise | Callback | Async/Await |
|------|---------|----------|-------------|
| Create | `new Promise()` | `fn(callback)` | `async function` |
| Consume | `.then().catch()` | callback parameter | `await` |
| Compose | `.then()` chain | nested callbacks | sequential `await` |

## 📊 Performance & Best Practices

- **Promise là microtask** — chạy trước setTimeout, sau sync code.
- **Never create promise without settling** — luôn gọi resolve/reject.
- **Always handle errors** — `.catch()` hoặc `try/catch` với async.
- **Use `Promise.all`** cho parallel independent operations.
- **Don't create promise in loop unnecessarily** — memory pressure.

## 🔗 Liên kết chéo

- **Xem thêm:** `12_asynchronous-javascript/02_callbacks-promises/03_promise-concept` — 3 states chi tiết
- **Xem thêm:** `12_asynchronous-javascript/02_callbacks-promises/04_promise-chain` — chaining pattern
- **Xem thêm:** `12_asynchronous-javascript/02_callbacks-promises/05_promise-static-methods` — all/race/any
- **Xem thêm:** `12_asynchronous-javascript/02_callbacks-promises/02_async-await` — async/await syntax
- **Xem thêm:** `12_asynchronous-javascript/01_event-loop/02_event-loop` — microtask priority
- **Xem thêm:** `13_working-with-apis/01_fetch` — fetch returns promise
