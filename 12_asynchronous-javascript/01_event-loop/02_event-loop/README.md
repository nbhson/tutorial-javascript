# Event Loop — cơ chế lõi của async JavaScript — [Level: Intermediate]

## 🔑 Khái niệm cốt lõi

JS là ngôn ngữ **đơn luồng**: chỉ một nhiệm vụ thực thi tại một thời điểm. Để không bị chặn bởi các tác vụ lâu (timer, request mạng), trình duyệt cung cấp **Web APIs** — các API bất đồng bộ, non-blocking (DOM API, HTTP request, `setTimeout`...).

Hành trình của một callback qua event loop:

1. Hàm được gọi → đẩy vào **Call Stack** (LIFO). Hàm xong thì lấy ra.
2. Gặp `setTimeout`/`fetch` → callback được đưa sang **Web APIs**, nơi có đồng hồ riêng chờ cho tới khi đủ thời gian.
3. Hết thời gian → callback **không vào thẳng Call Stack** mà nằm ở **Callback Queue** (FIFO) chờ lượt.
4. **Event Loop** chỉ có một việc: khi **Call Stack trống** thì lấy callback từ Queue đưa vào Stack để chạy.

Vì vậy `setTimeout(fn, 0)` **không** chạy ngay sau khi hết 0ms — nó phải chờ stack trống. Càng xếp nhiều setTimeout/setInterval thì càng chờ lâu.

**Microtask (Promise) có priority cao hơn macrotask (setTimeout)** — sau mỗi macrotask, event loop dọn hết microtask trước khi lấy macrotask tiếp.

## 📐 Cấu trúc / Cú pháp

### Chu trình event loop chi tiết

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Call Stack  │ ←── │ Event Loop  │ ──→ │  Queues     │
│  (executing) │     │  (checking) │     │  (waiting)  │
└─────────────┘     └─────────────┘     └─────────────┘
       ↑                                       │
       │              ┌──────────────┐         │
       └──────────────│ Microtask    │         │
                      │  Queue       │         │
                      │  (Promise)   │─────────┘
                      └──────────────┘
                               ↑
                      ┌──────────────┐
                      │ Macrotask    │
                      │  Queue       │
                      │  (setTimeout)│
                      └──────────────┘
```

### Queue priority trong mỗi tick

```
1. Chạy hết sync code trên Call Stack
2. Dọn hết Microtask Queue (Promise.then, queueMicrotask)
3. Chạy 1 Macrotask (setTimeout callback)
4. Dọn hết Microtask Queue
5. Chạy 1 Macrotask tiếp theo
6. Lặp lại...
```

## ✅ Điểm mạnh — Tại sao nên dùng

1. **Giải thích chính xác mọi thứ tự log bất ngờ** (stack, web API, queue).
2. **Hiểu vì sao setTimeout 0 vẫn chạy sau code đồng bộ**.
3. **Nền tảng để dùng đúng promise** (microtask) và timer (macrotask).
4. **Dự đoán được behavior** của code async phức tạp.
5. **Debug hiệu quả** — biết được tại sao callback chạy lúc này mà không phải lúc khác.
6. **Tối ưu code** — biết khi nào đẩy work ra queue thay vì chặn stack.

## ⚠️ Bẫy thường gặp & Hạn chế

### Bẫy 1: `setTimeout(fn, 0)` không tức thì

```js
console.log("A");
setTimeout(() => console.log("B"), 0);
console.log("C");
// Output: A → C → B (B chạy sau sync code, dù timeout = 0)
```

### Bẫy 2: Promise chạy trước setTimeout

```js
setTimeout(() => console.log("timeout"), 0);
Promise.resolve().then(() => console.log("promise"));
// Output: promise → timeout
```

### Bẫy 3: Task nặng trong stack chặn mọi callback

```js
console.log("Start");
while (true) {} // infinite loop — block stack
console.log("End"); // KHÔNG bao giờ chạy
// setTimeout callback cũng không chạy được
```

### Bẫy 4: Microtask starvation

```js
// Tạo loop microtask liên tục
function starve() {
  queueMicrotask(starve);
}
starve();
// Macrotask callbacks bị delay vô hạn
```

## 💡 Khi nào dùng — Tình huống thực tế

1. **Chạy trễ một đoạn code sau khi sự kiện hiện tại xử lý xong** (`setTimeout(0)`).
2. **Gộp nhiều thao tác DOM tốn kém** lại chờ lượt render.
3. **Đồng bộ hóa giữa các tác vụ bất đồng bộ độc lập** — `Promise.all`.
4. **Debouncing user input** — `setTimeout` + `clearTimeout`.
5. **Throttling scroll events** — chỉ chạy handler mỗi N ms.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Basic event loop tracing

```js
const foo = () => console.log("First");
const bar = () => setTimeout(() => console.log("Second"), 0);
const baz = () => console.log("Third");

bar(); // callback → Web API (timer 0ms) → queue
foo(); // First
baz(); // Third
// stack trống → Event Loop lấy callback từ queue
// Second   ← in cuối cùng
// Output: First → Third → Second
```

### Ví dụ 2: Promise microtask priority

```js
console.log("1. Sync");

setTimeout(() => console.log("2. Macro"), 0);

Promise.resolve().then(() => console.log("3. Micro1"));
Promise.resolve().then(() => console.log("4. Micro2"));

console.log("5. Sync end");

// 1. Sync → 5. Sync end → 3. Micro1 → 4. Micro2 → 2. Macro
```

### Ví dụ 3: Nested async operations

```js
console.log("A");

setTimeout(() => {
  console.log("B (setTimeout)");
  Promise.resolve().then(() => console.log("C (micro inside macro)"));
}, 0);

Promise.resolve().then(() => console.log("D (microtask)"));

console.log("E");

// A → E → D → B → C
```

### Ví dụ 4: Multiple timers competing

```js
console.log("Start");

setTimeout(() => console.log("T1"), 100);
setTimeout(() => console.log("T2"), 50);
setTimeout(() => console.log("T3"), 0);

console.log("End");
// Start → End → T3 → T2 → T1
// (Thứ tự chạy phụ thuộc thời gian thực, không phải khai báo)
```

### Ví dụ 5: Async function = promise behind the scene

```js
async function example() {
  console.log("Async start");
  await Promise.resolve(); // tạo microtask
  console.log("After await");
}

example();
console.log("Sync after call");
// Async start → Sync after call → After await
// (await tạo microtask, chạy sau sync code)
```

### Ví dụ 6: Real-world — render after DOM update

```js
// Force reflow sau DOM mutation
element.innerHTML = "<p>New content</p>";
// DOM đã update nhưng browser chưa repaint
setTimeout(() => {
  const height = element.scrollHeight; // đọc sau repaint
  console.log("Height:", height);
}, 0);
```

## 🔬 So sánh với alternatives

| Khái niệm | Vai trò | Queue type |
|-----------|---------|------------|
| Call Stack | Thực thi code | — |
| Web APIs | Chứa tác vụ async | — |
| Microtask Queue | Promise callbacks | Ưu tiên cao |
| Macrotask Queue | Timer/event callbacks | Ưu tiên thấp |
| Event Loop | Chuyển callback từ queue sang stack | Orchestrator |

## 📊 Performance & Best Practices

- **Giữ sync code ngắn** — stack phải trống nhanh để callback chạy.
- **Dùng `requestAnimationFrame`** cho animation thay vì `setTimeout`.
- **Avoid heavy computation** trong event handler — đẩy ra worker nếu cần.
- **Clear unused timers** — `clearTimeout`/`clearInterval` khi không còn cần.
- **Batch DOM writes** — nhiều thay đổi rồi render một lần.

## 🔗 Liên kết chéo

- **Xem thêm:** `12_asynchronous-javascript/01_event-loop/00_js-runtime-deep-dive` — runtime deep dive
- **Xem thêm:** `12_asynchronous-javascript/01_event-loop/03_settimeout-setinterval` — timer behavior
- **Xem thêm:** `12_asynchronous-javascript/02_callbacks-promises/01_promise-theory` — promise microtask
- **Xem thêm:** `12_asynchronous-javascript/02_callbacks-promises/02_async-await` — async/await vs event loop
- **Xem thêm:** `17_memory-management/01_memory-lifecycle-gc/01_garbage-collection` — heap + GC
