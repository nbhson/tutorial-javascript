# Callback Hell (Pyramid of Doom) — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

**Callback hell** xảy ra khi bạn lồng callback này vào callback khác nhiều tầng để xử lý các tác vụ bất đồng bộ tuần tự. Càng lồng sâu, thụt vào càng nhiều — hình dạng giống một **kim tự tháp** (pyramid of doom), khiến code **khó đọc và khó gỡ lỗi**.

```js
async1((a) =>
  async2(a, (b) =>
    async3(b, (c) =>
      async4(c, (d) =>
        console.log(d)))); // pyramid!
);
```

Thông thường các hàm `async1/async2/async3` là các tác vụ bất đồng bộ (timer, fetch, I/O) nhận callback, và mỗi bước cần dữ liệu của bước trước.

**Giải pháp:** dùng **Promises** (chuỗi `.then()`) hoặc **async/await** để "giải nén" kim tự tháp thành các dòng tuần tự, dễ đọc.

Callback hell không chỉ là vấn đề readability — nó còn gây khó khăn trong:
- **Error handling**: phải truyền error qua từng callback, dễ bỏ sót.
- **Debugging**: stack trace sâu, khó theo dõi flow.
- **Testing**: khó mock và test từng step độc lập.
- **Maintenance**: thêm/bớt bước phải sửa nhiều level indentation.

## 📐 Cấu trúc / Cú pháp

### Callback hell pattern

```js
// ❌ Pyramid of doom
step1(function(result1) {
  step2(result1, function(result2) {
    step3(result2, function(result3) {
      step4(result3, function(result4) {
        console.log(result4);
      });
    });
  });
});
```

### Promise chain solution

```js
// ✅ Flat structure
step1()
  .then(result1 => step2(result1))
  .then(result2 => step3(result2))
  .then(result3 => step4(result3))
  .then(result4 => console.log(result4))
  .catch(err => console.error(err));
```

### Async/await solution

```js
// ✅ Most readable
async function run() {
  try {
    const result1 = await step1();
    const result2 = await step2(result1);
    const result3 = await step3(result2);
    const result4 = await step4(result3);
    console.log(result4);
  } catch (err) {
    console.error(err);
  }
}
```

## ✅ Điểm mạnh — Tại sao hiểu rõ callback hell quan trọng

1. **Nhận diện ngay "mùi code"** khi viết callback lồng nhau.
2. **Biết lý do vì sao Promise/async/await tồn tại** — đánh giá đúng công cụ.
3. **Duy trì code cũ** viết bằng callback (nhiều thư viện Node.js vẫn dùng callback).
4. **Chuyển đổi callback → promise** bằng `new Promise`.
5. **Debug legacy code** hiệu quả hơn.

## ⚠️ Bẫy thường gặp & Hạn chế

### Bẫy 1: Mỗi cấp lồng làm tăng biến cục bộ khó quản lý

```js
step1(function(a) {
  step2(a, function(b) {
    step3(b, function(c) {
      // a, b, c đều accessible — nhưng chỉ trong scope này
      // muốn dùng ra ngoài? phải lift lên
    });
  });
});
```

### Bẫy 2: Lỗi phải truyền bằng tay qua từng callback — dễ bỏ sót

```js
function async1(callback) {
  // forgot error handling
  callback(null, result);
}
function async2(a, callback) {
  if (!a) return callback(new Error("a is required")); // phải remember ở every step
  callback(null, result);
}
```

### Bẫy 3: Luồng rẽ nhánh, lỗi, hay thoát sớm rất khó viết

```js
step1(function(err, a) {
  if (err) return handleErr(err);
  step2(a, function(err, b) {
    if (err) return handleErr(err); // repetitive!
    if (b < 0) return done(null, -1); // early exit
    step3(b, function(err, c) {
      // ...
    });
  });
});
```

### Bẫy 4: Debug stack trace bị mất thông tin

```js
// Error trong callback sâu khó trace back vì nhiều layers
```

## 💡 Khi nào dùng (khi nào gặp phải)

1. **Đọc/ghi file tuần tự** trong Node.js với callback API.
2. **Gọi API nối tiếp nhau**, bước sau cần dữ liệu bước trước, dùng callback style.
3. **Legacy codebase** sử dụng error-first callback pattern.
4. **Library cũ** chưa migrate sang promise (older jQuery AJAX, some DB drivers).

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Callback hell — đọc 3 file tuần tự

```js
// ❌ Callback hell
const fs = require("fs");

fs.readFile("a.txt", "utf8", function(err, a) {
  if (err) return console.error(err);
  fs.readFile(bFileName(a), "utf8", function(err, b) {
    if (err) return console.error(err);
    fs.readFile(cFileName(b), "utf8", function(err, c) {
      if (err) return console.error(err);
      console.log(c);
    });
  });
});
```

### Ví dụ 2: Same logic với Promise chain

```js
// ✅ Flat structure
function readFile(path) {
  return new Promise((resolve, reject) => {
    fs.readFile(path, "utf8", (err, data) => err ? reject(err) : resolve(data));
  });
}

readFile("a.txt")
  .then(a => readFile(bFileName(a)))
  .then(b => readFile(cFileName(b)))
  .then(c => console.log(c))
  .catch(err => console.error(err));
```

### Ví dụ 3: Same logic với async/await

```js
// ✅ Most readable
async function readFiles() {
  try {
    const a = await readFile("a.txt");
    const b = await readFile(bFileName(a));
    const c = await readFile(cFileName(b));
    console.log(c);
  } catch (err) {
    console.error(err);
  }
}
readFiles();
```

### Ví dụ 4: API call cascade — callback vs promise

```js
// ❌ Callback
function getPostComments(postId, callback) {
  fetch(`/api/posts/${postId}`, (err, post) => {
    if (err) return callback(err);
    fetch(`/api/comments?post=${postId}`, (err, comments) => {
      if (err) return callback(err);
      callback(null, { post, comments });
    });
  });
}

// ✅ Promise
function getPostComments(postId) {
  return fetch(`/api/posts/${postId}`)
    .then(post => fetch(`/api/comments?post=${postId}`).then(comments => ({ post, comments })));
}
```

### Ví dụ 5: Real-world — authentication flow

```js
// ❌ Callback hell: login → getUser → getPreferences → render
function login(username, password, callback) {
  auth.authenticate(username, password, (err, token) => {
    if (err) return callback(err);
    user.get(token, (err, userData) => {
      if (err) return callback(err);
      prefs.get(userData.id, (err, preferences) => {
        if (err) return callback(err);
        callback(null, { user: userData, prefs: preferences });
      });
    });
  });
}

// ✅ Promise
function loginFlow(username, password) {
  return auth.authenticate(username, password)
    .then(token => user.get(token))
    .then(userData => prefs.get(userData.id))
    .then(preferences => ({ user: userData, prefs: preferences }));
}
```

### Ví dụ 6: Turning callback into promise (util function)

```js
// Utility: convert any callback-style function to promise
function promisify(fn) {
  return function (...args) {
    return new Promise((resolve, reject) => {
      fn(...args, (err, result) => err ? reject(err) : resolve(result));
    });
  };
}

// Usage
const readFileAsync = promisify(fs.readFile);
const unlinkAsync = promisify(fs.unlink);

// Bây giờ dùng async/await
async function processFiles() {
  const a = await readFileAsync("a.txt", "utf8");
  const b = await readFileAsync("b.txt", "utf8");
  console.log(a, b);
}
```

### Ví dụ 7: So sánh readability

```js
// Callback: 7 cấp indent, 21 dòng
async1((a) => async2(a, (b) => async3(b, (c) => console.log("hell result", c))));

// Promise: 5 dòng, flat
Promise.resolve(1)
  .then((x) => x + 1)
  .then((x) => x + 1)
  .then(console.log); // 3

// Async/await: 4 dòng, linear
(async () => {
  let x = await Promise.resolve(1);
  x = await Promise.resolve(x + 1);
  x = await Promise.resolve(x + 1);
  console.log(x);
})();
```

## 🔬 So sánh với alternatives

| Approach | Indentation level | Error handling | Readability |
|----------|-------------------|----------------|-------------|
| Callback nested | Deep (N cấp) | Manual per step | ❌ Poor |
| Promise chain | Flat (1 cấp) | `.catch()` centralized | ⚠️ Medium |
| Async/await | Flat (0 cấp extra) | `try/catch` | ✅ Excellent |

## 📊 Performance & Best Practices

- **Refactor ngay khi thấy 2-3 cấp callback lồng** — đừng để thành pyramid.
- **Mỗi callback step nên là function riêng** — lift out named functions.
- **Dùng `promisify` utility** để convert legacy callback APIs.
- **Promise/async-await** luôn preferred cho code mới.
- **Callback vẫn hữu ích** cho simple one-off operations.

## 🔗 Liên kết chéo

- **Xem thêm:** `12_asynchronous-javascript/02_callbacks-promises/01_promise-theory` — promise basics
- **Xem thêm:** `12_asynchronous-javascript/02_callbacks-promises/04_promise-chain` — chain solution
- **Xem thêm:** `12_asynchronous-javascript/02_callbacks-promises/02_async-await` — async/await solution
- **Xem thêm:** `12_asynchronous-javascript/02_callbacks-promises/README` — overview
- **Xem thêm:** `11_function-borrowing/05_polyfill` — polyfill pattern similar thinking
