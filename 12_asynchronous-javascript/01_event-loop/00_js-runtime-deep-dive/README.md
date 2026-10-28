# JavaScript Runtime — Đi sâu vào bộ máy của JS — [Level: Advanced]

## 🔑 Khái niệm cốt lõi

**JavaScript Runtime** là môi trường thực thi JS, gồm các thành phần phối hợp với nhau để chạy code. Nó không chỉ là V8 engine — runtime bao gồm cả browser/Node APIs, memory management, và event loop.

```
┌────────────────────────────────────────────────────┐
│ JavaScript Runtime                                 │
│  ┌───────────────┐   ┌───────────────┐            │
│  │  Call Stack   │   │     Heap      │            │
│  │  (LIFO)       │   │  (bộ nhớ động)│            │
│  └───────────────┘   └───────────────┘            │
│  ┌──────────────────────────────────────────────┐  │
│  │            Event Loop                        │  │
│  └──────────────────────────────────────────────┘  │
│  ┌───────────────┐   ┌───────────────────┐        │
│  │ Callback Queue│   │    Web APIs       │        │
│  │ (macrotask)   │   │ setTimeout/fetch..│        │
│  │ Microtask Q.  │   └───────────────────┘        │
│  └───────────────┘                                │
└────────────────────────────────────────────────────┘
```

**Call Stack** (ngăn xếp): lưu các frames của hàm đang thực thi. Khi gọi hàm → push frame; khi return → pop frame. LIFO (Last In First Out). **Stack overflow** xảy ra khi đệ quy vô hạn.

**Heap** (vùng nhớ): lưu object, array, function — quản lý bởi Garbage Collector (GC). GC dùng **mark-and-sweep** algorithm để thu gom object không còn reference.

**Web APIs**: do browser/Node cung cấp, chạy ngoài JS thread chính — timer, DOM, fetch, file system...

**Event Loop**: đồng bộ Call Stack với các hàng đợi. Khi stack trống, lấy callback từ queue đưa vào stack.

**Task Queue (macrotask)** và **Microtask Queue**: nơi callback chờ lượt. Microtask ưu tiên cao hơn — dọn hết trước khi lấy macrotask tiếp.

## 📐 Cấu trúc / Cú pháp

### Các thành phần chi tiết

| Thành phần | Chức năng | Vị trí | Quản lý bởi |
|------------|-----------|--------|-------------|
| **Call Stack** | Thực thi hàm, tracking execution context | Engine | V8/SpiderMonkey |
| **Heap** | Cấp phát động cho object/array | Engine | Garbage Collector |
| **Web APIs** | Timer, DOM, Network, File | Browser/Node | OS + Browser |
| **Callback Queue** | Macrotask waiting area | Browser/Node | Event Loop |
| **Microtask Queue** | Promise/MutationObserver queue | Browser/Node | Event Loop |
| **Event Loop** | Orchestrator giữa stack và queues | Engine | V8/SpiderMonkey |

### Memory lifecycle

```
Allocation → Usage → Collection (GC)
    ↑                              ↓
  new obj                    unreachable
                             (no references)
```

### Stack frame structure

```
┌─────────────────────────┐
│ Execution Context       │
│  ├─ Variable Environment│  (biến, hàm khai báo)
│  ├─ This Binding        │  (this value)
│  └─ Outer Environment   │  (scope chain)
├─────────────────────────┤
│ Return Address          │  (vị trí quay lại)
├─────────────────────────┤
│ Arguments               │  (tham số truyền vào)
└─────────────────────────┘
```

## ✅ Điểm mạnh — Tại sao nên hiểu

1. **Nhìn thấy bức tranh toàn cảnh** từ lúc code chạy đến lúc trả kết quả.
2. **Giải thích chính xác lỗi `RangeError: Maximum call stack size exceeded`** (stack overflow).
3. **Hiểu hoisting, scope chain, closure, this binding** trong bối cảnh runtime thật.
4. **Phân biệt rõ thứ tự chạy** của sync, microtask, macrotask — nền tảng debug bất đồng bộ.
5. **Debug memory leak** — hiểu cách GC hoạt động, object nào bị giữ lại.
6. **Tối ưu performance** — tránh tạo object không cần, quản lý reference đúng cách.

## ⚠️ Bẫy thường gặp & Hạn chế

### Bẫy 1: Stack overflow — đệ quy vô hạn

```js
function infinite() { infinite(); }
infinite(); // RangeError: Maximum call stack size exceeded
// Stack giới hạn ~10k-15k frames tùy engine
```

### Bẫy 2: Memory leak — global variable rò rỉ

```js
// Biến global không khai báo var/let/const
leakedVar = "I will never be GC'd"; // tạo property trên globalThis
```

### Bẫy 3: Closure giữ reference — GC không thu gom được

```js
function setup() {
  const bigArray = new Array(1000000).fill("data");
  return function() { return bigArray[0]; }; // closure giữ reference
}
const fn = setup();
// bigArray KHÔNG bị GC dù setup() đã return!
```

### Bẫy 4: Dangling reference — object bị giữ bởi event listener

```js
const element = document.getElementById("btn");
element.addEventListener("click", handler);
// element không bị GC until removeEventListener
```

### Bẫy 5: setInterval không clear — chạy mãi

```js
setInterval(() => console.log("tick"), 1000);
// Phải clearInterval(id) khi không cần nữa
```

## 💡 Khi nào dùng — Tình huống thực tế

1. **Giải thích/output thứ tự console.log** trong code không đồng bộ.
2. **Chẩn đoán lỗi treo, memory leak, stack overflow**.
3. **Tối ưu performance** — tránh object "chết" trong bộ nhớ, debounce DOM access.
4. **Debug production issues** — hiểu tại sao app chậm, RAM tăng dần.
5. **Write efficient code** — biết khi nào tạo object, khi nào reuse.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Call Stack trace

```js
function a() { b(); }
function b() { c(); }
function c() { console.log("deep"); }

a();
// Stack: a → b → c → (return c) → (return b) → (return a)
```

### Ví dụ 2: Stack overflow demonstration

```js
function count(n) {
  if (n === 0) return;
  count(n - 1); // đệ quy
}
count(10000); // có thể stack overflow tùy engine limit
```

### Ví dụ 3: Heap allocation

```js
const obj = { name: "test" };  // object trên heap
const arr = [1, 2, 3];        // array trên heap
const str = "hello";           // string có thể trên stack hoặc heap

// Khi gán: chỉ copy reference, không copy object
const ref = obj;
ref.name = "modified";
console.log(obj.name); // "modified" — cùng object trên heap
```

### Ví dụ 4: Garbage Collection demo

```js
function createLeak() {
  const data = new Array(1000000);
  setTimeout(() => {
    console.log("Timer fires, data may still be referenced");
  }, 1000);
  // data vẫn tồn tại vì setTimeout closure giữ reference
}
createLeak();
```

### Ví dụ 5: Event Loop trong action

```js
console.log("A");
setTimeout(() => console.log("B"), 0);
Promise.resolve().then(() => console.log("C"));
console.log("D");
// A → D → C → B
// Stack: A, D → Microtask: C → Macrotask: B
```

### Ví dụ 6: Memory usage monitoring

```js
if (performance && performance.memory) {
  console.log("JS Heap Size:", performance.memory.usedJSHeapSize);
  console.log("JS Heap Limit:", performance.memory.jsHeapSizeLimit);
}
// Chỉ available trong Chrome DevTools / Node.js --expose-gc
```

## 🔬 So sánh với alternatives

| Runtime | Environment | Đặc điểm |
|---------|-------------|----------|
| **V8 (Chrome/Node)** | Browser + Node | Fast JIT, Chrome DevTools |
| **SpiderMonkey (Firefox)** | Firefox | Mozilla engine, similar architecture |
| **JavaScriptCore (Safari)** | Safari/Safari extensions | Apple engine, WebKit |
| **Rhino (Java)** | Java environment | Pure JS interpreter |

## 📊 Performance & Best Practices

- **Giảm stack depth** — dùng iterative thay recursive khi có thể.
- **Clear timers** — `clearTimeout`/`clearInterval` khi component unmount.
- **Remove event listeners** — tránh memory leak từ dangling references.
- **Use WeakMap/WeakSet** — cho cache không giữ reference mạnh.
- **Profile memory** — DevTools Memory tab, Heap snapshot.
- **Avoid global variables** — tăng GC pressure.
- **Reuse objects** — tránh thường xuyên allocation/deallocation.

## 🔗 Liên kết chéo

- **Xem thêm:** `12_asynchronous-javascript/01_event-loop/02_event-loop` — event loop chi tiết
- **Xem thêm:** `17_memory-management/01_memory-lifecycle-gc/01_garbage-collection` — GC algorithms
- **Xem thêm:** `17_memory-management/01_memory-lifecycle-gc/02_memory-leaks` — leak patterns
- **Xem thêm:** `10_this-keyword/README` — this binding trong execution context
- **Xem thêm:** `09_functions/02_scope-closure-strict-mode/03_closure` — closure memory behavior
