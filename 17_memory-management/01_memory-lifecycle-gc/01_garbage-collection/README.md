# Garbage Collection (GC) — [Level: Intermediate]

## 🔑 Khái niệm cốt lõi

**Garbage Collection (GC)** là quá trình tự động tìm và **xóa các object không còn được dùng nữa** trong bộ nhớ của JavaScript. Khi bạn tạo biến, object, function, chúng được lưu vào heap; nếu không có cơ chế dọn dẹp, bộ nhớ sẽ đầy và dẫn tới lỗi **"Out of Memory" (OOM)**.

GC trong JavaScript hiện đại dựa trên thuật toán **Mark and Sweep**, gồm hai pha:

### Pha 1: Mark (Đánh dấu)
Engine bắt đầu từ các **root** — những đối tượng chắc chắn đang sống:
- Biến toàn cục (`window.*`, `global.*`)
- Các frame trên call stack (biến cục bộ đang active)
- DOM nodes đang hiển thị trên trang
- Module exports
- Worker global scope

Từ mỗi root, engine **duyệt đệ quy** theo mọi tham chiếu, đánh dấu mọi object **reachable** (có đường đi từ root tới).

### Pha 2: Sweep (Quét)
Sau khi mark phase hoàn tất, engine quét toàn bộ heap. Mọi object **không được đánh dấu** (unreachable) bị **giải phóng** — bộ nhớ được trả lại cho hệ thống, sẵn sàng cấp phát mới.

### Reachability — chìa khóa của GC
GC quyết định theo **reachability** (có đường từ root tới hay không), **không** phải theo bạn có gán `= null` hay không. Đối tượng trong một `{}` kết thúc, không return, không gắn global/DOM/closure → tự mất reachability → bị GC thu hồi mà không cần null.

```js
function example() {
  const obj = { data: new Array(1e6).fill(0) };
  return obj;
}
const result = example();
// Khi example() return, obj cục bộ bị pop khỏi stack
// Nhưng result vẫn giữ reference → obj vẫn reachable → KHÔNG bị GC
result = null;
// Bây giờ obj unreachable → GC sẽ thu hồi
```

### Tại sao không dùng Reference Counting?
Reference counting đếm số người trỏ đến object; về 0 thì xóa. Nhưng **circular reference** làm nó thất bại:
```js
let a = {}, b = {};
a.ref = b;
b.ref = a;
// Cả hai đều có ref count = 1 (do nhau)
// Dù không ai dùng ngoài, count không bao giờ về 0 → leak vĩnh viễn
```
Mark & Sweep khắc phục bằng cách check **đường đi từ root**, không đếm số ref.

Thư mục này là **demo hoàn chỉnh** gồm `index.html` (giao diện theo dõi memory trực quan), `garbage-collection-examples.js` (code ví dụ), và `HOW_TO_USE.md` (hướng dẫn chạy).

## 📐 Cấu trúc / Cú pháp

### Theo dõi GC qua `performance.memory` (Chrome)
```js
const mem = performance.memory;
console.log({
  used: (mem.usedJSHeapSize / 1024 / 1024).toFixed(2) + ' MB',
  total: (mem.totalJSHeapSize / 1024 / 1024).toFixed(2) + ' MB',
  limit: (mem.jsHeapSizeLimit / 1024 / 1024).toFixed(2) + ' MB'
});
// used ≤ total ≤ limit
// used: bộ nhớ thực tế đang dùng
// total: dung lượng heap đang được cấp (có thể lớn hơn used)
// limit: giới hạn tối đa (thường ~4GB trên 64-bit)
```

### Force GC trong Node.js
```bash
node --expose-gc script.js
```
```js
// script.js
gc(); // ép garbage collection
console.log('After GC:', performance.memory?.usedJSHeapSize);
```

### DevTools — Heap Snapshot
1. **Memory tab** → **Take heap snapshot**.
2. Chọn filter: **Summary** (theo constructor), **Constructor** (theo type), **Comparison** (so 2 snapshot).
3. **Retainers column** — xem object bị giữ bởi ai (đường từ root).
4. **Detached DOM** filter — tìm node đã gỡ khỏi DOM nhưng JS vẫn giữ ref.

### WeakReference — ES2021
```js
const obj = { data: 'large' };
const weakRef = new WeakRef(obj);
console.log(weakRef.deref()?.data); // 'large' (hoặc undefined nếu đã GC)
```

## ✅ Điểm mạnh

1. **Giảm hẳn lớp người-quản-lý-bộ-nhớ** so với C/C++ — ít lỗi use-after-free, double-free, segfault.
2. **Mark & Sweep xử lý được circular reference** — vốn là tử huyệt của reference counting.
3. **Có thể giám sát** qua `performance.memory` (Chrome) và `v8.getHeapStatistics()` (Node).
4. **Hỗ trợ WeakMap / WeakSet / WeakRef** — "tham chiếu yếu" để GC thoải mái thu hồi khi cần.
5. **Compacting/Generational GC** (Minor young / Major old generation) giúp dọn nhanh với object tuổi thọ ngắn.
6. **Predictable deallocation** — biết được object nào reachable/unreachable qua retainer path.
7. **Zero-config** — không cần gọi free(), delete — engine lo hết.

## ⚠️ Bẫy thường gặp & Hạn chế

1. GC **tự động, không thể điều khiển trực tiếp** — `gc()` chỉ chạy khi có cờ đặc biệt (`--expose-gc`). Không có standard API.
2. **Trễ và không tức thời** — memory giảm sau vài giây (thường khi rảnh), hoặc chờ "Take Heap Snapshot" mới thấy rõ. Đừng đoán timing.
3. `performance.memory` **không tiêu chuẩn** — Firefox/Safari không có API này. Code phụ thuộc sẽ break trên các browser khác.
4. Chính GC cũng **tốn CPU** — cấp phát rác nhiều (allocation spawn trong loops) làm giật màn hình (GC pause) → cần hạn chế tạo object thừa.
5. **Detached DOM leak** — node bị `remove()` khỏi DOM nhưng JS vẫn giữ reference → GC không dọn được.
6. **Closure capture** — hàm inner giữ biến scope cha → biến không bị GC dù function scope đã kết thúc.

## 💡 Khi nào dùng — Tình huống thực tế

1. **Debug tăng RAM từ từ** trong SPA — kiểm tra xem object "xong việc" còn reachable hay không.
2. **Quyết định dùng WeakMap** cho cache tạm (cache theo key object) thay vì Map — cho GC thoải mái thu hồi.
3. **Tối ưu vòng lặp lớn** — giảm cấp phát object lặp đi lặp lại, dùng typed array thay Array.
4. **Quan sát used ≤ total ≤ limit** để biết heap đang áp lực ra sao — nếu used gần limit, nguy cơ OOM.
5. **Trước khi "gán null" để cleanup** — xác định xem thực sự cần cắt tham chiếu hay scope đã tự mất.
6. **So sánh heap snapshot trước/sau action** — tìm object tăng bất thường → xác định leak source.
7. **Profile allocation rate** — dùng "Allocation instrumentation on timeline" để thấy hàm nào tạo nhiều object nhất.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Basic reference — hiểu reachability
```js
let user = { name: "John" };
let admin = user;   // 2 tham chiếu, chưa bị GC
user = null;        // vẫn reachable qua admin
admin = null;       // giờ unreachable -> GC sẽ thu hồi
```

### Ví dụ 2: Circular reference — Mark & Sweep xử lý được
```js
const a = {}, b = {};
a.ref = b;
b.ref = a;
a = null;
b = null; // không còn đường từ root -> thu hồi cả hai
// Reference counting sẽ KHÔNG dọn được — đây là điểm khác biệt then chốt
```

### Ví dụ 3: Scope tự cleanup (không cần null)
```js
function process() {
  const bigData = new Array(1e6).fill(0); // 8MB
  const result = bigData.map(x => x * 2);
  return result;
  // bigData tự unreachable khi process() return
  // GC sẽ thu hồi — không cần gán null thủ công
}
const result = process();
```

### Ví dụ 4: WeakMap — cache tự GC
```js
const elementCache = new WeakMap();

function cacheElementInfo(el, info) {
  elementCache.set(el, info);
}

function getInfo(el) {
  return elementCache.get(el);
}

// Khi el bị remove khỏi DOM và không còn ref nào khác
// → entry trong WeakMap tự GC — không leak
```

### Ví dụ 5: Leak qua closure — hiểu cơ chế
```js
function createHandler() {
  const largeBuffer = new ArrayBuffer(10 * 1024 * 1024); // 10MB
  return function() {
    return largeBuffer.byteLength; // closure giữ largeBuffer
  };
}
const handler = createHandler();
// largeBuffer sống mãi vì handler closure giữ — dù createHandler đã return
// Fix: nếu handler không cần largeBuffer sau init, clear trong closure
```

### Ví dụ 6: Object pooling — giảm GC pressure
```js
const pool = [];
function acquire() {
  return pool.length > 0 ? pool.pop() : { data: new Array(1000).fill(0) };
}
function release(obj) {
  if (pool.length < 50) pool.push(obj);
  // Ngoài 50 → obj tự GC
}
// Tái sử dụng object thay vì alloc/free liên tục
```

### Ví dụ 7: Monitor heap trong loop
```js
function benchmarkAllocation() {
  const before = performance.memory?.usedJSHeapSize || 0;
  for (let i = 0; i < 100000; i++) {
    const obj = { id: i, data: new Array(100).fill(i) };
    // obj tự GC mỗi iteration (không lưu reference)
  }
  const after = performance.memory?.usedJSHeapSize || 0;
  console.log('Heap change:', (after - before) / 1024 / 1024, 'MB');
  // Nếu heap tăng đáng kể → có thể có leak hoặc GC chưa chạy
}
```

### Ví dụ 8: Detached DOM detection
```js
function createDetached() {
  const div = document.createElement('div');
  div.textContent = 'I am detached';
  document.body.appendChild(div);
  div.remove(); // gỡ khỏi DOM
  return div; // giữ reference → detached DOM leak
}
const leaked = createDetached();
// Heap snapshot sẽ hiện: JS Heap → Detached DOM nodes → 1
// Fix: null leaked sau khi không cần
leaked = null;
```

## 🔬 So sánh với alternatives

| Thuật toán | Cơ chế | Circular ref | Engine hiện đại |
|---|---|---|---|
| **Mark & Sweep** | Root → mark reachable → sweep unreachable | ✅ Xử lý được | ✅ V8, JSC, SpiderMonkey |
| **Reference Counting** | Count refs → free when 0 | ❌ Thất bại | ❌ (chỉ dùng làm phần phụ) |
| **Mark & Compact** | Mark + sweep + copy về đầu heap | ✅ | ✅ V8 (generational) |
| **Tracing GC** | Duyệt graph từ root | ✅ | Tất cả engine hiện đại |

## 📊 Performance & Best Practices

- **Giảm allocation rate**: tạo ít object mới trong hot path → giảm GC frequency → smoother UI.
- **Typed arrays thay Array**: `new Float64Array(1000)` nhanh hơn và ít GC pressure hơn `new Array(1000)`.
- **Batch operations**: gộp nhiều DOM changes thành một lần (DocumentFragment, template literal) → ít reflow + ít allocation.
- **WeakMap cho metadata**: attach data lên DOM element mà không gây leak — GC tự dọn khi element gone.
- **Avoid global variables**: global sống suốt app lifecycle — dễ thành leak source.
- **Profile định kỳ**: dùng DevTools Memory tab trong dev để phát hiện leak sớm.
- **GC pause awareness**: heap > 100MB → sweep lâu → potential freeze. Limit heap size khi không cần.
- **Test on target browser**: `performance.memory` chỉ Chrome — test memory behavior trên target audience browsers.

## 🔗 Liên kết chéo

- Xem thêm: `17_memory-management/01_memory-lifecycle-gc/` — vòng đời bộ nhớ tổng quan.
- Xem thêm: `17_memory-management/01_memory-lifecycle-gc/02_memory-leaks/` — 4 pattern leak chi tiết.
- Xem thêm: `17_memory-management/03_v8-engine/` — V8 pipeline, hidden class, inline cache.
- Xem thêm: `17_memory-management/04_meta-programming/` — Proxy cho reactivity.
- Xem thêm: `19_browser-devtools/01_devtools-memory/` — thực hành heap snapshot tìm leak.
- Xem thêm: `garbage-collection-examples.js` — code demo đầy đủ chạy trong browser/Node.
- Xem thêm: `HOW_TO_USE.md` — hướng dẫn chạy demo.
