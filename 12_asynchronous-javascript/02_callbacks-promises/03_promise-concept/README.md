# Promise — Khái niệm và 3 trạng thái — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

Promise sinh ra (từ ES6) để **giải quyết các vấn đề bất đồng bộ**. Trước promise, người ta dùng callback — và callback sinh ra **callback hell**, nên promise ra đời để thay thế.

Một promise được tạo bằng `new Promise(executor)` — **executor chạy ngay lập tức**, trước khi bạn nhận được biến promise, và nhận 2 hàm:

- `resolve(value)` → promise chuyển sang **fulfilled**; các `.then()` được gọi.
- `reject(error)` → promise chuyển sang **rejected**; `.catch()` được gọi.

Ba trạng thái:

1. **Pending** — không gọi `resolve`/`reject`.
2. **Fulfilled** — gọi `resolve()` → `.then()` chạy.
3. **Rejected** — gọi `reject()` → `.catch()` chạy.

Sau một trong hai, `.finally()` luôn chạy bất kể thành công hay thất bại. Lưu ý: nếu **không gọi** cả `resolve` và `reject`, promise rơi vào pending vĩnh viễn → **memory leak**.

Trong file demo: các tác vụ bất đồng bộ điển hình gồm `setTimeout`, `setInterval`, `fetch`, `XMLHttpRequest`, file reading, requestAnimationFrame.

## 📐 Cấu trúc / Cú pháp

### Promise executor

```js
const promise = new Promise((resolve, reject) => {
  // executor chạy đồng bộ ngay lập tức
  doAsyncWork((err, result) => {
    if (err) reject(err);
    else resolve(result);
  });
});
```

### State transition diagram

```
         ┌──────────────┐
         │   pending    │
         └──────┬───────┘
                │
        ┌───────┴───────┐
        ▼               ▼
 ┌─────────────┐   ┌─────────────┐
 │  fulfilled  │   │  rejected   │
 │  .then()    │   │  .catch()   │
 └──────┬──────┘   └──────┬──────┘
        └────────┬────────┘
                 ▼
          ┌─────────────┐
          │  .finally() │
          │  (always)   │
          └─────────────┘
```

## ✅ Điểm mạnh — Tại sao nên dùng

1. **Tách rõ 3 trạng thái** → dễ suy luận hành vi của code.
2. **`.then/.catch/.finally`** xử lý lỗi tập trung, tránh callback lồng nhau.
3. **Executor chạy ngay** giúp khởi tạo tác vụ đúng lúc.
4. **Nền tảng để ghép nối** (`Promise.all`) và viết `async/await`.
5. **Settled once** — state không thay đổi sau khi fulfill/reject, đảm bảo consistency.
6. **Chainable** — `.then()` trả về promise mới, nối tiếp vô hạn.

## ⚠️ Bẫy thường gặp & Hạn chế

### Bẫy 1: Không gọi resolve/reject → pending forever (memory leak)

```js
const broken = new Promise((resolve, reject) => {
  // quên gọi resolve hoặc reject
  console.log("doing work...");
  // không có resolve/reject ở đây!
});
broken.then(() => console.log("never runs"));
broken.catch(() => console.log("never runs either"));
```

### Bẫy 2: Gọi cả resolve lẫn reject — chỉ lần đầu có effect

```js
const p = new Promise((resolve, reject) => {
  resolve(1);
  reject(2); // bị bỏ qua
});
p.then(v => console.log(v)); // 1
```

### Bẫy 3: Executor chạy đồng bộ ngay

```js
console.log("Before");
new Promise((resolve) => {
  console.log("Executor runs immediately");
  resolve("value");
});
console.log("After");
// Output: Before → Executor runs immediately → After → (microtask) value
```

### Bẫy 4: `.then()` luôn trả về promise mới

```js
const p1 = Promise.resolve(1);
const p2 = p1.then(v => v + 1);
console.log(p1 === p2); // false
console.log(await p2);  // 2
```

## 💡 Khi nào dùng — Tình huống thực tế

1. **Wrapping callback API** thành promise để dùng modern syntax.
2. **Điều khiển luồng**: thành công thì `.then`, thất bại thì `.catch`, luôn kết thúc bằng `.finally`.
3. **Khởi tạo tác vụ bất đồng bộ** ngay lúc tạo promise.
4. **Timer-based operations** — wrap setTimeout trong promise.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Basic promise với setTimeout

```js
const delay = (ms) => {
  return new Promise((resolve) => {
    setTimeout(resolve, ms);
  });
};

delay(1000).then(() => console.log("1 second later"));
```

### Ví dụ 2: Resolve vs Reject

```js
var promise = new Promise((resolve, reject) => {
  // pending nếu không gọi gì
  reject("404"); // → rejected, .catch chạy
});

promise
  .then(function (result) {
    console.log("Success", result);   // chỉ chạy nếu resolve()
  })
  .catch(function (error) {
    console.log("Fail", error);       // → Fail 404
  })
  .finally(function () {
    console.log("Done");              // luôn chạy
  });
```

### Ví dụ 3: Promise wrapping XMLHttpRequest

```js
function xhrGet(url) {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    xhr.open("GET", url);
    xhr.onload = () => {
      if (xhr.status >= 200 && xhr.status < 300) {
        resolve(xhr.responseText);
      } else {
        reject(new Error(`HTTP ${xhr.status}`));
      }
    };
    xhr.onerror = () => reject(new Error("Network error"));
    xhr.send();
  });
}
```

### Ví dụ 4: Promise wrapping setInterval (custom)

```js
function periodicTask(fn, intervalMs, maxCalls = Infinity) {
  return new Promise((resolve, reject) => {
    let calls = 0;
    const id = setInterval(() => {
      calls++;
      try {
        const result = fn(calls);
        if (calls >= maxCalls) {
          clearInterval(id);
          resolve(result);
        }
      } catch (err) {
        clearInterval(id);
        reject(err);
      }
    }, intervalMs);
  });
}
```

### Ví dụ 5: Promise với fetch

```js
function fetchJSON(url) {
  return new Promise((resolve, reject) => {
    fetch(url)
      .then(response => {
        if (!response.ok) reject(new Error(`HTTP ${response.status}`));
        return response.json();
      })
      .then(resolve)
      .catch(reject);
  });
}
```

### Ví dụ 6: Promise animation frame

```js
function animate(duration) {
  return new Promise((resolve) => {
    const start = performance.now();
    function step() {
      const elapsed = performance.now() - start;
      if (elapsed < duration) {
        requestAnimationFrame(step);
      } else {
        resolve();
      }
    }
    requestAnimationFrame(step);
  });
}
animate(1000).then(() => console.log("Animation done"));
```

## 🔬 So sánh với alternatives

| Cách | State management | Error handling | Readability |
|------|-----------------|----------------|-------------|
| Callback | Manual flags | Error-first param | ❌ Poor |
| Promise | 3 states explicit | `.catch()` | ⚠️ Medium |
| Async/await | Hidden promise | `try/catch` | ✅ Good |

## 📊 Performance & Best Practices

- **Executor chạy đồng bộ** — đặt side-effect vào executor cẩn thận.
- **Luôn gọi resolve/reject** — tránh pending forever memory leak.
- **Dùng `.finally()`** cho cleanup code (loading spinner, close modal).
- **Don't create promise just to wrap another promise** — return existing promise directly.

## 🔗 Liên kết chéo

- **Xem thêm:** `12_asynchronous-javascript/02_callbacks-promises/01_promise-theory` — promise theory overview
- **Xem thêm:** `12_asynchronous-javascript/02_callbacks-promises/04_promise-chain` — chaining pattern
- **Xem thêm:** `12_asynchronous-javascript/02_callbacks-promises/05_promise-static-methods` — Promise.all/race
- **Xem thêm:** `12_asynchronous-javascript/02_callbacks-promises/06_promise-example` — real-world example
- **Xem thêm:** `12_asynchronous-javascript/01_event-loop/02_event-loop` — microtask priority
