# Memory Leaks — 4 Pattern Rò Rỉ Bộ Nhớ Phổ Biến — [Level: Intermediate]

## 🔑 Khái niệm cốt lõi

**Memory leak** xảy ra khi chương trình **giữ tham chiếu tới dữ liệu không còn dùng nữa**, khiến GC không thể thu hồi, bộ nhớ tăng dần theo thời gian và cuối cùng dẫn tới chậm, treo, hoặc **OOM (Out of Memory)**.

Vì GC chỉ dọn object "unreachable từ root", nên cách phòng chống leak đơn giản nhất là: **đừng tạo đường tham chiếu thừa**. Có bốn pattern rò rỉ kinh điển trong JavaScript:

### 1. Biến toàn cục (Global Variable Leak)
Quên `var`/`let`/`const` khi khai báo → biến tự động trở thành property của `globalThis` (browser: `window`, Node: `global`). Biến toàn cục sống suốt lifecycle app → không bao giờ bị GC.

```js
function init() {
  leaked = new Array(1e6).fill(0); // ❌ thiếu let → global leak
}
init();
// leaked tồn tại mãi trên window, GC không bao giờ dọn
```

### 2. Event Listener Leak
Gắn callback vào element nhưng không `removeEventListener` khi không cần. Callback là closure — giữ mọi biến trong scope mà nó capture. Element bị hold → toàn bộ closure scope bị giữ → leak.

```js
const btn = document.getElementById('btn');
const handler = () => console.log('click');
btn.addEventListener('click', handler);
// Khi component unmount:
btn.removeEventListener('click', handler); // ✅ phải gọi
// Nếu quên: handler + closure scope sống mãi
```

### 3. Closure Leak
Hàm inner giữ biến của scope cha. Nếu hàm còn "sống" lâu hơn dự định (trong array callbacks, global registry), dữ liệu lớn trong scope bị giữ cùng.

```js
function create() {
  const bigData = new Array(1e6).fill('x'); // 8MB+
  return function() {
    console.log('sum', bigData.length); // closure giữ bigData
  };
}
const cb = create(); // bigData được giữ mãi theo cb
// Fix: nếu cb không cần bigData sau khi init, null nó
```

### 4. Timer/Interval Leak
`setInterval`/`setTimeout` nhắc callback định kỳ. Quên `clearInterval`/`clearTimeout` → callback chạy mãi → callback closure giữ mọi thứ nó capture.

```js
const id = setInterval(() => {
  console.log('tick');
}, 1000);
// Quên clearInterval(id) → tick mãi, mọi closure trong handler sống mãi
clearInterval(id); // ✅ phải gọi khi không cần
```

### Bonus: Detached DOM Node
Node bị gỡ khỏi DOM (`.remove()`) nhưng JavaScript vẫn giữ tham chiếu qua biến. Node không hiển thị trên trang nhưng vẫn chiếm bộ nhớ.

```js
const div = document.createElement('div');
document.body.appendChild(div);
div.remove(); // gỡ khỏi DOM
// div variable still holds reference → detached DOM leak
div = null; // ✅ fix
```

Các yếu tố làm leak trở nên nghiêm trọng: biến bị "nhô" lên global, closure bao quanh dữ liệu lớn, listener/callback không được dọn khi **unmount** (SPA chuyển trang).

## 📐 Cấu trúc / Cú pháp

### Phát hiện leak qua DevTools

1. **Memory → Heap Snapshot**: chụp ở trạng thái sạch, thực hiện action, chụp lần 2, so sánh.
2. **Allocation instrumentation on timeline**: ghi lại mọi allocation theo thời gian, thấy call stack.
3. **Allocation sampling**: nhẹ hơn, lấy mẫu allocation thay vì record tất cả.

### Kiểm tra leak qua code

```js
// Pattern 1: Global leak detection
function testGlobalLeak() {
  const before = Object.keys(window).length;
  leakyFunction();
  const after = Object.keys(window).length;
  console.log('New globals:', after - before);
}

// Pattern 2: Timer leak detection
let timerId = null;
function startLeakyTimer() {
  timerId = setInterval(() => console.log('tick'), 1000);
}
function stopLeakyTimer() {
  clearInterval(timerId);
  timerId = null;
}

// Pattern 3: Listener leak detection
function attachLeakyListener() {
  const handler = () => {};
  window.addEventListener('resize', handler);
  // Quên: window.removeEventListener('resize', handler)
}
```

### Sửa leak — patterns phổ biến

```js
//fix 1: Always use let/const
function fixGlobal() {
  let safeVar = new Array(1e6).fill(0); // ✅ scoped
}

//fix 2: Remove listener in cleanup
function fixListener(component) {
  const handler = (e) => console.log(e);
  component.addEventListener('click', handler);
  return () => component.removeEventListener('click', handler); // cleanup function
}

//fix 3: Clear timer in cleanup
function fixTimer() {
  const id = setInterval(tick, 1000);
  return () => clearInterval(id);
}

//fix 4: Null detached references
function fixDetached() {
  const div = document.createElement('div');
  document.body.appendChild(div);
  div.remove();
  return () => { div.textContent = ''; }; // null references in cleanup
}
```

## ✅ Điểm mạnh (của việc hiểu và tránh leak)

1. **Ứng dụng ổn định** — RAM không "leo thang", không giật, không treo khi chạy lâu.
2. **Tự tin trong SPA lớn** — biết khi nào phải dọn listener, interval, và ref DOM đã gỡ.
3. **Kết nối tốt với GC** — hiểu reachability để quyết định đúng lúc cắt tham chiếu.
4. **Tránh được lớp lỗi tinh vi** — chỉ xuất hiện sau hours chạy thực tế, khó reproduce.
5. **Dùng được WeakMap/WeakRef** — biến một số cache nguy hiểm thành an toàn.
6. **Tiết kiệm battery** — RAM ít hơn → CPU ít work hơn → pin device kéo dài.
7. **Better user experience** — app mượt mà, không lag sau khi mở nhiều tab.
8. **Professional code** — cleanup trong lifecycle hook là dấu hiệu của senior developer.

## ⚠️ Bẫy thường gặp & Hạn chế

1. **Leak khó thấy**: không có lỗi gì ngay, chỉ RAM tăng chậm — cần **heap snapshot trước/sau** để đo.
2. **`clearInterval` không tự nhớ**: bạn phải "nhớ" handle mình đã tạo — tốt nhất lưu vào biến component-level.
3. **`removeEventListener` chỉ hiệu quả với đúng hàm reference** — dùng anonymous function thì không gỡ được:
   ```js
   btn.addEventListener('click', () => console.log('x')); // ❌ không remove được
   const handler = () => console.log('x');
   btn.addEventListener('click', handler);
   btn.removeEventListener('click', handler); // ✅
   ```
4. **Closure vô hại ở mức nhỏ**, nguy hiểm khi bao quanh **dữ liệu lớn / DOM**. Đừng tin giá trị "chắc GC dọn" khi scope vẫn sống.
5. **Gán `= null` giúp cắt tham chiếu** để GC dọn sớm, nhưng nếu object vẫn còn root tham chiếu thì vô dụng.
6. **SPA route change** — component unmount nhưng listener/timer không được cleanup → leak tích lũy qua nhiều lần navigate.
7. **Third-party library leak** — thư viện bên thứ 3 có thể không cleanup đúng — cần tự gọi dispose/cleanup method.

## 💡 Khi nào dùng (điểm áp dụng)

1. **SPA chuyển trang / mở-đóng modal** liên tục — dọn listener, interval, ref DOM trong lifecycle teardown.
2. **Danh sách vô hạn (infinite scroll)** — hủy observer (`IntersectionObserver.disconnect`) và ref node cũ.
3. **Cache ứng dụng** — dùng `Map` hay `WeakMap`; xóa entry khi data hết hạn.
4. **Cảnh báo khi viết closure** bao quanh mảng lớn hoặc DOM để "dùng sau".
5. **Component unmount** trong framework vanilla — gọi cleanup function để removeAllListeners, clearAllTimers.
6. **Before page unload** — gửi analytics ping, lưu state quan trọng qua `beforeunload`.
7. **Worker cleanup** — `worker.terminate()` khi không cần, close channel.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Global variable leak
```js
// ❌ LEAK — thiếu let/const
function leak() {
  leakedArray = new Array(1e6).fill(0); // automatic global
}
leak();
console.log(window.leakedArray); // tồn tại mãi

// ✅ FIX
function safe() {
  let safeArray = new Array(1e6).fill(0); // scoped, GC sẽ dọn
}
safe();
```

### Ví dụ 2: Event listener leak
```js
// ❌ LEAK — không remove
const btn = document.getElementById('btn');
btn.addEventListener('click', () => console.log('click'));
// Component unmount → listener vẫn sống

// ✅ FIX — lưu reference để remove
const btn = document.getElementById('btn');
const handler = (e) => console.log('click');
btn.addEventListener('click', handler);
// Khi unmount:
btn.removeEventListener('click', handler);
```

### Ví dụ 3: Closure giữ data lớn
```js
// ❌ LEAK
function create() {
  const big = new Array(1e6).fill('x');
  return function() { console.log('sum', big.length); };
}
const cb = create(); // big được giữ mãi theo cb

// ✅ FIX — tách data không cần ra khỏi closure
function createFixed() {
  const big = new Array(1e6).fill('x');
  const len = big.length; // chỉ giữ number (nhỏ)
  big = null; // cắt reference đến big
  return function() { console.log('len', len); };
}
```

### Ví dụ 4: Timer leak
```js
// ❌ LEAK — quên clear
const id = setInterval(() => tick(), 1000);
// Component unmount → interval chạy mãi

// ✅ FIX — lưu id và clear khi unmount
const id = setInterval(() => tick(), 1000);
function cleanup() {
  clearInterval(id);
}
// Gọi cleanup() khi component unmount
```

### Ví dụ 5: Detached DOM node leak
```js
// ❌ LEAK
function createLeak() {
  const div = document.createElement('div');
  document.body.appendChild(div);
  div.remove(); // DOM removed
  return div; // JS still holds reference
}
const leaked = createLeak(); // detached node, GC cannot collect

// ✅ FIX
function createSafe() {
  const div = document.createElement('div');
  document.body.appendChild(div);
  div.remove();
  return null; // no reference held
}
```

### Ví dụ 6: SPA route change leak pattern
```js
class Router {
  constructor() {
    this.currentCleanup = null;
  }
  navigate(path) {
    // Cleanup trang cũ
    if (this.currentCleanup) this.currentCleanup();
    
    // Setup trang mới
    this.currentCleanup = this.setupPage(path);
  }
  setupPage(path) {
    const btn = document.getElementById('action-btn');
    const handler = () => console.log('action');
    btn.addEventListener('click', handler);
    
    const timer = setInterval(() => console.log('tick'), 1000);
    
    // Return cleanup function
    return () => {
      btn.removeEventListener('click', handler);
      clearInterval(timer);
    };
  }
}
```

### Ví dụ 7: IntersectionObserver leak
```js
// ❌ LEAK — observer không disconnect
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) entry.target.classList.add('visible');
  });
});
observer.observe(document.querySelector('.item'));
// Component unmount → observer vẫn live, giữ reference đến .item

// ✅ FIX
const observer = new IntersectionObserver(...);
// Khi unmount:
observer.disconnect(); // ✅ clear all observations
```

### Ví dụ 8: WeakMap cache (không leak)
```js
// ✅ AN TOÀN — WeakMap tự GC
const elementMeta = new WeakMap();

function addMeta(element, meta) {
  elementMeta.set(element, meta);
}

function getMeta(element) {
  return elementMeta.get(element);
}

// Khi element bị remove khỏi DOM và không còn ref khác
// → entry trong WeakMap tự GC — không leak
```

## 🔬 So sánh với alternatives

| Pattern | Mức độ nguy hiểm | Dễ phát hiện | Cách sửa |
|---|---|---|---|
| **Global variable** | Cao | Dễ (console.log window.keys) | Thêm let/const |
| **Event listener** | Trung bình | Heap snapshot (retainers) | removeEventListener |
| **Closure** | Thấp-Trung bình | Heap snapshot (big retained size) | Null large refs trong closure |
| **Timer/Interval** | Cao | setInterval ID leak | clearInterval |
| **Detached DOM** | Trung bình | DevTools "Detached DOM" filter | Null JS reference |
| **Observer không disconnect** | Cao | Heap snapshot (observer retainers) | observer.disconnect() |

## 📊 Performance & Best Practices

- **Cleanup trong lifecycle**: mọi component nên có `mount()` và `unmount()` — cleanup tất cả listener, timer, observer trong unmount.
- **Single responsibility cleanup**: mỗi effect (listener, timer, observer) có một cleanup function tương ứng.
- **Test với heap snapshot**: thêm unit test so sánh heap before/after action — phát hiện leak tự động.
- **Use ESLint rules**: `no-invalid-this`, `prefer-const` giúp tránh global leak.
- **Framework hooks**: React `useEffect` cleanup, Vue `onUnmounted` — tận dụng lifecycle built-in.
- **Memory budget**: đặt giới hạn heap usage (ví dụ < 100MB) và alert khi vượt.
- **CI/CD memory test**: chạy load test trong CI, so sánh heap growth — fail build nếu leak.

## 📚 Tham khảo / Bài tập

- Đọc bài gốc: <https://kipalog.com/posts/Duc-khoet-Javascript--Phan-3---Quan-ly-bo-nho---4-truong-hop-ro-ri-pho-bien>
- Xem pattern demo có sẵn trong `01_garbage-collection/garbage-collection-examples.js` (mục **3. Memory Leak Examples** — global, event listener, closure) hoặc mở `index.html` để chạy trực quan.
- Tự làm trong DevTools: mở **Memory → Heap snapshot** ở trạng thái sạch, chạy một đoạn tạo `let arr = []` rồi push mảng lớn trong `setInterval`; chụp snapshot lần 2 — tìm node tăng bất thường để hiểu cách leak hiện hình.
- Tự làm: viết component nhỏ (vanilla JS) mô phỏng "unmount", trong đó quên `removeEventListener` — rồi dùng **Detached DOM / Retainers** trong snapshot để thấy node bị giữ.
- Tự làm: chuyển cache từ `Map` sang `WeakMap`, chụp snapshot và so sánh cấp phát khi key bị null.
- Xem thêm: `17_memory-management/01_memory-lifecycle-gc/` — lý thuyết GC nền tảng.
- Xem thêm: `19_browser-devtools/01_devtools-memory/` — thực hành heap snapshot.
