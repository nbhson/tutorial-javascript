# Promise Static Methods — `resolve` / `reject` / `all` / `race` — [Level: Intermediate]

## 🔑 Khái niệm cốt lõi

Ngoài `new Promise(executor)`, Promise cung cấp các **phương thức tĩnh** (gọi trên chính `Promise`, không cần instance) để tạo và kết hợp promise:

| Phương thức | Công dụng |
|-------------|-----------|
| `Promise.resolve(value)` | Tạo promise đã **fulfilled** ngay với giá trị cho trước |
| `Promise.reject(reason)` | Tạo promise đã **rejected** ngay với lý do |
| `Promise.all([p1, p2, ...])` | Chờ **tất cả** settle; fail nếu có bất kỳ cái nào reject |
| `Promise.race([p1, p2, ...])` | Trả về kết quả của cái **settle đầu tiên** |
| `Promise.allSettled([p1, p2, ...])` | Chờ tất cả, báo từng trạng thái dù fail hay success |
| `Promise.any([p1, p2, ...])` | Trả về cái **fulfilled đầu tiên** (bỏ qua reject) |

Điểm quan trọng với `Promise.all`: các promise trong mảng chạy **song song** (không tuần tự), và chỉ khi tất cả xong thì `.then` mới chạy. Nếu một promise `reject` ngay từ đầu → `all` fail luôn.

## 📐 Cấu trúc / Cú pháp

### Signature đầy đủ

```js
// Tạo promise từ giá trị
Promise.resolve(42);        // fulfilled với 42
Promise.reject("error");    // rejected với "error"

// Tất cả phải thành công
Promise.all([p1, p2, p3])
  .then(([v1, v2, v3]) => ...)
  .catch(err => ...);       // fail nếu ANY reject

// Race — ai nhanh hơn thắng
Promise.race([p1, p2, p3])
  .then(first => ...)      // giá trị của promise settle đầu
  .catch(err => ...);      // reject nếu first là reject

// All settled — biết kết quả từng cái
Promise.allSettled([p1, p2])
  .then(results =>          // [{status:"fulfilled",value:...}, ...]
    results.forEach(r => ...)
  );

// Any — fulfilled đầu tiên
Promise.any([p1, p2, p3])
  .then(first => ...)       // value của fulfilled đầu
  .catch(err => ...);       // AggregateError nếu ALL reject
```

## ✅ Điểm mạnh — Tại sao nên dùng

1. **`Promise.all`** chạy song song nhiều tác vụ, chỉ cần một `.then` khi đủ kết quả.
2. **Tạo nhanh promise** thành công/thất bại để test hoặc wrap giá trị đồng bộ.
3. **`Promise.race`** lấy kết quả nhanh nhất — hữu ích cho timeout.
4. **Rõ ràng**: ai reject thì `all` reject, ai xong sớm thì `race` thắng.
5. **`allSettled`** cho biết kết quả từng promise riêng biệt — không fail-fast.
6. **`any`** useful khi có multiple sources và chỉ cần một success.

## ⚠️ Bẫy thường gặp & Hạn chế

### Bẫy 1: `Promise.all` từ chối toàn bộ nếu một promise reject

```js
const p1 = Promise.resolve(1);
const p2 = Promise.reject("error");
const p3 = Promise.resolve(3);

Promise.all([p1, p2, p3])
  .then(values => console.log(values))  // KHÔNG chạy
  .catch(err => console.log(err));      // "error"
// p1 và p3 vẫn chạy xong nhưng result bị discard
```

### Bẫy 2: `race` có thể thắng bằng reject

```js
const slowResolve = new Promise(res => setTimeout(() => res("slow"), 1000));
const fastReject = Promise.reject("fast error");

Promise.race([slowResolve, fastReject])
  .then(v => console.log(v))    // KHÔNG chạy
  .catch(err => console.log(err)); // "fast error"
```

### Bẫy 3: `Promise.reject` không có `.catch` → unhandled rejection

```js
Promise.reject("Oops"); // unhandled rejection warning
// Fix: Promise.reject("Oops").catch(() => {});
```

### Bẫy 4: Thứ tự kết quả `all` theo thứự mảng, không theo thứ tự hoàn thành

```js
const fast = Promise.resolve("fast");
const slow = new Promise(res => setTimeout(() => res("slow"), 1000));

Promise.all([slow, fast])
  .then(values => console.log(values)); 
// ["slow", "fast"] — thứ tự theo mảng, KHÔNG theo thời gian hoàn thành
```

### Bẫy 5: `Promise.any` throws AggregateError khi all reject

```js
Promise.any([
  Promise.reject("a"),
  Promise.reject("b")
])
  .catch(err => console.log(err)); 
// AggregateError: All promises were rejected
```

## 💡 Khi nào dùng — Tình huống thực tế

1. **Gọi đồng thời nhiều endpoint** rồi gộp kết quả (`Promise.all`).
2. **Wrap object** thành promise cho đồng bộ API (`Promise.resolve`).
3. **Timeout cho tác vụ chậm** (`Promise.race([task, timeout])`).
4. **Graceful degradation** — `Promise.allSettled` để xử lý partial failure.
5. **Multiple source fallback** — `Promise.any` lấy response đầu tiên hợp lệ.
6. **Parallel independent operations** — upload nhiều files cùng lúc.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Promise.resolve và reject

```js
// Resolve — fulfilled ngay
Promise.resolve("Success!")
  .then((v) => console.log(v)); // Success!

// Reject — rejected ngay
Promise.reject("Fail!")
  .catch((v) => console.log(v)); // Fail!

// Wrap sync value into promise
const syncValue = 42;
Promise.resolve(syncValue)
  .then(v => v * 2); // 84
```

### Ví dụ 2: Promise.all — parallel fetch

```js
const p1 = new Promise((res) => setTimeout(() => { console.log("5s"); res([1]); }, 5000));
const p2 = new Promise((res) => setTimeout(() => { console.log("2.5s"); res([2, 3]); }, 2500));

Promise.all([p1, p2])
  .then(function (result) {
    const [arr1, arr2] = result;
    console.log(arr1.concat(arr2)); // [1, 2, 3] — chờ cả hai xong
  })
  .catch((err) => console.log(err));
```

### Ví dụ 3: Promise.race — timeout pattern

```js
function fetchWithTimeout(url, timeoutMs = 3000) {
  const timeout = new Promise((_, reject) =>
    setTimeout(() => reject(new Error("Timeout")), timeoutMs)
  );
  return Promise.race([fetch(url), timeout]);
}

fetchWithTimeout("/api/slow-endpoint", 2000)
  .then(res => res.json())
  .catch(err => console.error(err.message));
```

### Ví dụ 4: Promise.allSettled — partial failure handling

```js
const endpoints = ["/api/users", "/api/posts", "/api/comments"];

Promise.allSettled(endpoints.map(url => fetch(url).then(r => r.json())))
  .then(results => {
    results.forEach((result, i) => {
      if (result.status === "fulfilled") {
        console.log(`✅ ${endpoints[i]}: ${result.value.length} items`);
      } else {
        console.log(`❌ ${endpoints[i]}: ${result.reason.message}`);
      }
    });
  });
```

### Ví dụ 5: Promise.any — first successful response

```js
const primary = fetch("/api/data").then(r => r.json());
const backup = fetch("/api/backup").then(r => r.json());

Promise.any([primary, backup])
  .then(data => console.log("Using:", data.source))
  .catch(err => console.error("All sources failed"));
```

### Ví dụ 6: Parallel upload with progress

```js
async function uploadFiles(files) {
  const uploads = files.map(file => {
    return fetch("/api/upload", {
      method: "POST",
      body: file
    }).then(res => res.json());
  });
  
  const results = await Promise.all(uploads);
  return results; // array of upload results, same order as files
}
```

### Ví dụ 7: Combining all methods

```js
async function loadDashboard() {
  const endpoints = {
    users: "/api/users",
    posts: "/api/posts",
    stats: "/api/stats"
  };
  
  // Parallel load
  const results = await Promise.all(
    Object.entries(endpoints).map(async ([key, url]) => {
      const res = await fetch(url);
      return { key, data: await res.json() };
    })
  );
  
  // Transform to object
  const dashboard = results.reduce((acc, { key, data }) => {
    acc[key] = data;
    return acc;
  }, {});
  
  return dashboard;
}
```

## 🔬 So sánh với alternatives

| Method | Behavior | Fail strategy | Result shape |
|--------|----------|---------------|--------------|
| `all` | Wait all | Fail fast (any reject) | `[v1, v2, ...]` |
| `race` | First settle | First settle wins | single value |
| `allSettled` | Wait all | Wait all | `[{status, value/reason}, ...]` |
| `any` | First fulfilled | First fulfilled wins | single value |

## 📊 Performance & Best Practices

- **`Promise.all`** là fastest cho parallel independent tasks — tất cả chạy cùng lúc.
- **`Promise.allSettled`** chậm hơn một chút (chờ tất cả) nhưng an toàn cho partial failure.
- **`Promise.race`** with timeout — đảm bảo không treo mãi.
- **Tránh `Promise.reject` không `.catch()`** — unhandled rejection là lỗi nghiêm trọng.
- **Thứ tự kết quả `all`** luôn theo thứ tự mảng input — không phụ thuộc thời gian hoàn thành.

## 🔗 Liên kết chéo

- **Xem thêm:** `12_asynchronous-javascript/02_callbacks-promises/01_promise-theory` — promise basics
- **Xem thêm:** `12_asynchronous-javascript/02_callbacks-promises/04_promise-chain` — chain pattern
- **Xem thêm:** `12_asynchronous-javascript/02_callbacks-promises/02_async-await` — async/await + Promise.all
- **Xem thêm:** `12_asynchronous-javascript/02_callbacks-promises/06_promise-example` — real-world example
- **Xem thêm:** `13_working-with-apis/01_fetch` — fetch returns promise
