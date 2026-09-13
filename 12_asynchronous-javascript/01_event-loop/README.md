# Event Loop — Chi tiết — [Level: Advanced]

## 🔑 Khái niệm cốt lõi

**Event Loop** là cơ chế cho phép JS (đơn luồng) xử lý các tác vụ bất đồng bộ mà không bị chặn. Nó liên tục **quan sát Call Stack và các hàng đợi**, và chỉ khi **Call Stack trống** mới đưa callback từ hàng đợi vào stack để thực thi.

Tóm tắt chu trình:
```
1. Call Stack chạy code đồng bộ.
2. Gặp tác vụ bất đồng bộ (setTimeout, fetch...) → đẩy sang Web APIs.
3. Web APIs xử lý xong → bỏ callback vào hàng đợi (queue).
4. Event Loop: nếu Call Stack trống → lấy callback theo FIFO vào stack.
5. Lặp lại vô tận.
```

Có **hai hàng đợi** với thứ tự ưu tiên khác nhau:

- **Microtask Queue** (ưu tiên cao): `Promise.then()`, `queueMicrotask()`, `MutationObserver`.
- **Macrotask Queue** (ưu tiên thấp): `setTimeout`, `setInterval`, I/O, click events...

Thứ tự thực thi chuẩn trong **mỗi tick** của event loop:
```
sync code → (microtask queue hết) → 1 macrotask → (microtask queue hết) → 1 macrotask → ...
```

Sau mỗi macrotask, event loop **dọn hết microtask** trước khi lấy macrotask tiếp theo.

## 📐 Cấu trúc / Cú pháp

### Kiến trúc JavaScript Runtime

```
┌─────────────────────────────────────────────┐
│           JavaScript Runtime                │
│  ┌──────────────┐    ┌──────────────────┐   │
│  │  Call Stack  │    │      Heap        │   │
│  │  (LIFO)      │    │  (dynamic memory)│   │
│  └──────────────┘    └──────────────────┘   │
│  ┌──────────────────────────────────────┐   │
│  │           Event Loop                 │   │
│  └──────────────────────────────────────┘   │
│  ┌──────────────┐    ┌──────────────────┐   │
│  │  Macrotask   │    │    Web APIs      │   │
│  │    Queue     │    │ setTimeout/fetch │   │
│  │  (task)      │    └──────────────────┘   │
│  └──────────────┘    ┌──────────────────┐   │
│  ┌──────────────┐    │ Microtask Queue  │   │
│  │   Web APIs   │    │ Promise.then()   │   │
│  │  (timer,     │    │ queueMicrotask() │   │
│  │   DOM, etc)  │    │ MutationObserver │   │
│  └──────────────┘    └──────────────────┘   │
└─────────────────────────────────────────────┘
```

### Bảng queue priority

| Hàng đợi | Phương thức | Ưu tiên | Chạy khi |
|----------|-------------|---------|----------|
| **Microtask** | `Promise.then/catch/finally` | Cao nhất | Sau mỗi macrotask, trước macrotask tiếp |
| **Microtask** | `queueMicrotask(fn)` | Cao nhất | Ngay sau sync code |
| **Microtask** | `MutationObserver callbacks` | Cao nhất | Sau mỗi DOM mutation |
| **Macrotask** | `setTimeout(fn, 0)` | Thấp | Khi stack trống, sau microtasks |
| **Macrotask** | `setInterval(fn, ms)` | Thấp | Mỗi interval, sau microtasks |
| **Macrotask** | `click`, `scroll`, `load` | Thấp | Khi event xảy ra |

## ✅ Điểm mạnh — Tại sao nên dùng

1. **Giải thích được mọi output "bất ngờ"** của code bất đồng bộ.
2. **Khiến JS nhanh và responsive** bất chấp đơn luồng.
3. **Microtask ưu tiên cao** giúp Promise settle ngay khi stack trống.
4. **Dự đoán chính xác thứ tự log** giữa promise và setTimeout.
5. **Hiểu được race conditions** trong event-driven programming.
6. **Debug hiệu quả** — biết được tại sao code chạy không theo thứ tự mong đợi.
7. **Tối ưu performance** — tránh chặn main thread bằng cách đẩy work ra queue.
8. **Foundation cho mọi async pattern** — callback, promise, async/await đều dựa trên event loop.

## ⚠️ Bẫy thường gặp & Hạn chế

### Bẫy 1: `setTimeout(fn, 0)` không chạy ngay

```js
console.log("A");
setTimeout(() => console.log("B"), 0);
console.log("C");
// Output: A → C → B (B chạy sau cùng, dù timeout = 0)
```

### Bẫy 2: Microtask "bỏ đói" macrotask

```js
// Tạo infinite microtask loop
Promise.resolve().then(() => {
  queueMicrotask(() => { /* lại enqueue thêm */ });
});
//Macrotask tasks bị delay vô hạn
```

### Bẫy 3: Task nặng trong stack chặn mọi callback

```js
console.log("Start");
// Tính toán nặng 10 giây
for (let i = 0; i < 1e9; i++) {}
console.log("End"); // Chỉ khi loop xong callback mới chạy
```

### Bẫy 4: Thứ tự microtask không theo thứ tự khai báo

```js
Promise.resolve().then(() => console.log("P1"));
Promise.resolve().then(() => console.log("P2"));
// P1 và P2 chạy ngay lập tức sau sync, nhưng thứ tự phụ thuộc enqueue order
```

### Bẫy 5: Hiểu sai `setTimeout` timing

```js
setTimeout(() => console.log("timeout"), 500);
// Callback KHÔNG chắc chạy đúng 500ms — chỉ là minimum
// Nếu stack bận, callback chờ đến khi stack trống
```

## 💡 Khi nào dùng — Tình huống thực tế

1. **Debug thứ tự thực thi** của promise so với setTimeout.
2. **Tối ưu UI** — đẩy tác vụ nặng ra khỏi main thread.
3. **Hiểu vì sao async/await** "treo" hàm mà không chặn chương trình.
4. **Xử lý race condition** trong concurrent async operations.
5. **Implement debounce/throttle** dùng setTimeout.
6. **Batch DOM updates** — gather changes rồi render một lần.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Basic event loop order

```js
console.log("1. Start");

setTimeout(() => console.log("2. Timeout"), 0);      // macrotask
Promise.resolve().then(() => console.log("3. Promise")); // microtask
queueMicrotask(() => console.log("4. queueMicrotask"));  // microtask

console.log("5. End");

// 1. Start → 5. End → 3. Promise → 4. queueMicrotask → 2. Timeout
```

### Ví dụ 2: Nested promise + timeout

```js
console.log("A");

setTimeout(() => console.log("B"), 0);

Promise.resolve()
  .then(() => {
    console.log("C");
    return Promise.resolve();
  })
  .then(() => console.log("D"));

console.log("E");

// A → E → C → D → B
```

### Ví dụ 3: Multiple microtasks in chain

```js
console.log("Start");

Promise.resolve().then(() => console.log("P1"));
Promise.resolve().then(() => console.log("P2"));

setTimeout(() => console.log("T1"), 0);
setTimeout(() => console.log("T2"), 0);

console.log("End");

// Start → End → P1 → P2 → T1 → T2
```

### Ví dụ 4: Macro + microtask interleaving

```js
console.log("1");

setTimeout(() => {
  console.log("2");
  Promise.resolve().then(() => console.log("3"));
}, 0);

Promise.resolve().then(() => console.log("4"));

console.log("5");

// 1 → 5 → 4 → 2 → 3
// Giải thích: sync(1,5) → microtask(4) → macrotask(2) → microtask trong macrotask(3)
```

### Ví dụ 5: Real-world — polling pattern

```js
async function poll(url, intervalMs) {
  while (true) {
    try {
      const res = await fetch(url);
      const data = await res.json();
      console.log("Data:", data);
    } catch (err) {
      console.error("Poll error:", err);
    }
    // chờ interval trước khi poll lần nữa
    await new Promise(resolve => setTimeout(resolve, intervalMs));
  }
}
// poll("/api/status", 5000); // polling mỗi 5 giây
```

### Ví dụ 6: Debounce với setTimeout

```js
function debounce(fn, delay) {
  let timer;
  return function (...args) {
    clearTimeout(timer); // hủy timer cũ
    timer = setTimeout(() => {
      fn.apply(this, args); // gọi sau delay ms
    }, delay);
  };
}

const search = debounce((query) => {
  console.log("Searching:", query);
}, 300);

// Input "hello" → chỉ log "Searching: hello" sau 300ms kể từ keystroke cuối
```

## 🔬 So sánh với alternatives

| Khái niệm | Mô tả | Tương đương |
|-----------|-------|-------------|
| Call Stack | Ngăn xếp thực thi hàm | LIFO, một luồng |
| Web APIs | Browser/Node cung cấp | Không nằm trong JS engine |
| Microtask Queue | Promise callbacks | Chạy trước macrotask |
| Macrotask Queue | Timer/event callbacks | Chạy sau microtask |

## 📊 Performance & Best Practices

- **Ưu tiên microtask cho kết quả khẩn cấp** — Promise.then chạy trước setTimeout.
- **Tránh tạo infinite microtask loop** — có thể block toàn bộ UI.
- **Đặt tác vụ nặng vào Web Worker** — không chặn main thread.
- **Dùng `requestAnimationFrame`** cho animation — sync với browser repaint.
- **Batch DOM reads/writes** — đọc nhiều lần rồi viết một lần để tránh reflow.
- **Hiểu rằng `setTimeout(fn, 0)` ≈ "as soon as possible"** — không phải "ngay lập tức".

## 🔗 Liên kết chéo

- **Xem thêm:** `12_asynchronous-javascript/01_event-loop/00_js-runtime-deep-dive` — runtime architecture
- **Xem thêm:** `12_asynchronous-javascript/01_event-loop/01_introduce-sync-async` — sync vs async intro
- **Xem thêm:** `12_asynchronous-javascript/01_event-loop/03_settimeout-setinterval` — timer behavior
- **Xem thêm:** `12_asynchronous-javascript/02_callbacks-promises/01_promise-theory` — promise microtask
- **Xem thêm:** `17_memory-management/01_memory-lifecycle-gc/01_garbage-collection` — heap memory
