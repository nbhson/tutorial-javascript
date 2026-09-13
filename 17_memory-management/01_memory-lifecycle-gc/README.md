# Vòng đời bộ nhớ và Garbage Collection — [Level: Intermediate]

## 🔑 Khái niệm cốt lõi

Mọi chương trình máy tính đều trải qua vòng đời bộ nhớ ba bước cơ bản:

1. **Allocate (cấp phát)**: biến, object, hàm được cấp vùng nhớ khi khai báo hoặc tạo ra. Trong JavaScript, primitive values (number, string, boolean, null, undefined, symbol, bigint) được cấp trên **stack** — kích thước cố định, truy cập nhanh. Object, array, function được cấp trên **heap** — kích thước động, được quản lý bởi GC.

2. **Use (sử dụng)**: đọc, ghi, truy cập dữ liệu. Đây là giai đoạn code thực sự làm việc với dữ liệu.

3. **Release (giải phóng)**: trả vùng nhớ về hệ thống khi không còn dùng nữa. Trong JavaScript, bước này do **Garbage Collector (GC)** của engine tự động làm — bạn không gọi `free()` như trong C/C++.

Tuy GC tự động, developer vẫn có thể vô tình tạo **memory leak** bằng cách giữ tham chiếu không cần thiết — khiến GC không bao giờ thu hồi được bộ nhớ đó.

### Thuật toán GC: Mark & Sweep vs Reference Counting

**Mark & Sweep** (thuật toán hiện đại, dùng bởi V8, SpiderMonkey, JavaScriptCore):
1. **Mark phase**: bắt đầu từ các **root** (biến toàn cục, call stack, DOM đang hiển thị, module exports...), duyệt và **đánh dấu** mọi object reachable (có đường từ root tới).
2. **Sweep phase**: quét toàn bộ heap, **giải phóng** các object không được đánh dấu (unreachable).

Ưu điểm quyết định: **xử lý được circular reference**. ObjA trỏ ObjB, ObjB trỏ ObjA — cả hai đều unreachable từ root → GC thu hồi được cả hai.

**Reference Counting** (thuật toán cũ, không dùng làm chính trong engine hiện đại):
- Đếm số tham chiếu tới mỗi object; về 0 thì xóa.
- Thất bại với **circular reference**: obj1→obj2→obj1 không bao giờ về 0 → **leak vĩnh viễn**.

### Root là gì?
Root là các đối tượng mà GC luôn coi là "đang sống":
- Biến toàn cục (`window`, `global`)
- Gọi stack frames đang active
- DOM nodes đang hiển thị trên trang
- Module exports
- Worker global scope

Thư mục này chia làm hai phần:
- `01_garbage-collection/` — demo đầy đủ: kịch bản tham chiếu, circular, các loại leak, WeakMap, object pooling, theo dõi `performance.memory`.
- `02_memory-leaks/` — các pattern rò rỉ bộ nhớ điển hình và cách sửa.

## 📐 Cấu trúc / Cú pháp

### Theo dõi bộ nhớ qua API

```js
// Chrome-only API (không tiêu chuẩn)
if (performance.memory) {
  console.log('usedJSHeapSize:', (performance.memory.usedJSHeapSize / 1024 / 1024).toFixed(2), 'MB');
  console.log('totalJSHeapSize:', (performance.memory.totalJSHeapSize / 1024 / 1024).toFixed(2), 'MB');
  console.log('jsHeapSizeLimit:', (performance.memory.jsHeapSizeLimit / 1024 / 1024).toFixed(2), 'MB');
}
// used ≤ total ≤ limit
```

### Node.js heap statistics
```js
const v8 = require('v8');
console.log(v8.getHeapStatistics());
// { total_heap_size, used_heap_size, heap_size_limit, ... }
```

### Force GC (Node.js với flag)
```bash
node --expose-gc script.js
```
```js
// Trong script
gc(); // ép garbage collection
console.log(performance.memory?.usedJSHeapSize);
```

### DevTools Memory Tab
1. Mở DevTools → **Memory** tab.
2. Chọn **Heap snapshot** → **Take snapshot**.
3. Thực hiện action (click, scroll, thêm element...).
4. Chụp snapshot lần 2 → so sánh **Summary** hoặc **Comparison**.
5. Tìm **Detached DOM** nodes — node đã gỡ khỏi trang nhưng JS vẫn giữ ref.

## ✅ Điểm mạnh

1. **Tự động**: không cần quản lý bộ nhớ tay, giảm lỗi use-after-free / double-free — lỗi phổ biến trong C/C++.
2. **Hiểu vòng đời** = biết khi nào cắt tham chiếu để GC dọn được — tránh leak mà không cần tool phức tạp.
3. **Mark & Sweep mạnh mẽ**: vượt qua giới hạn circular reference của reference counting — thu hồi được cả vòng tròn tham chiếu.
4. **WeakMap / WeakRef** cho phép đánh dấu "tham chiếu yếu" — GC thoải mái thu hồi khi không còn key mạnh.
5. **Quan sát được** bằng `performance.memory` (Chrome) hoặc `v8.getHeapStatistics()` (Node).
6. **DevTools Heap Snapshot** cho biết chính xác object nào bị giữ và bởi ai (retainer path).
7. **Allocation timeline** cho thấy object được tạo khi nào, bởi hàm nào — debug leak chính xác.

## ⚠️ Lưu ý / Hạn chế

1. GC **không chạy ngay lập tức** khi bạn "không dùng nữa" — nó đợi lúc engine rảnh (idle). `usedJSHeapSize` có thể giảm chậm.
2. **Không có lệnh ép GC chuẩn** trong JS — `gc()` chỉ có trong DevTools Console hoặc Node `--expose-gc`.
3. `performance.memory` là API không tiêu chuẩn, **chỉ đáng tin trên Chrome/Chromium** — Firefox/Safari không support.
4. Reference counting là bài học lịch sử — engine hiện đại không dùng nó làm thuật toán chính, nhưng khái niệm vẫn hữu ích để hiểu "leak do 2-side tham chiếu".
5. GC tự nó **tốn CPU** — cấp phát rác nhiều (allocation spawn trong loop) gây giật màn hình → cần hạn chế tạo object thừa.
6. Heap snapshot **kích hoạt GC** — `usedJSHeapSize` có thể giảm đột ngột sau khi chụp, đừng ngạc nhiên.

## 💡 Khi nào dùng — Tình huống thực tế

1. **Kiểm tra ứng dụng chạy lâu bị tăng RAM dần** — áp dụng vòng đời nhớ để tìm nơi giữ tham chiếu thừa.
2. **Dọn cache bằng WeakMap** thay vì Map để không biến cache thành leak — key tự động bị thu hồi.
3. **Quyết định null / removeEventListener / clear interval** khi component unmount trong SPA.
4. **Viết hệ thống stream / cấp phát tạm** với khối lượng lớn — biết rõ lúc nào memory được trả lại.
5. **Profile** bằng DevTools Memory / Node `--expose-gc` trước khi tối ưu — có baseline để so sánh.
6. **Detect detached DOM** — node bị `remove()` nhưng JS vẫn giữ ref → tìm qua "Detached" filter trong snapshot.
7. **Object pooling** cho game/simulator — tái sử dụng object thay vì alloc/free liên tục.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Basic reference — hiểu reachability
```js
let user = { name: "John" };
let admin = user;     // cùng object, 2 tham chiếu
user = null;          // vẫn còn admin -> KHÔNG bị GC
admin = null;         // hết tham chiếu -> GC thu hồi
```

### Ví dụ 2: Circular reference — Mark & Sweep xử lý được
```js
let obj1 = {}, obj2 = {};
obj1.ref = obj2;
obj2.ref = obj1;     // circular
obj1 = null;
obj2 = null;
// Cả hai đều unreachable từ root → GC dọn được cả hai
// (Reference counting sẽ KHÔNG dọn được — đây là điểm khác biệt)
```

### Ví dụ 3: WeakMap — cache an toàn với GC
```js
const elementData = new WeakMap();

function cacheData(element, data) {
  elementData.set(element, data);
}

function getData(element) {
  return elementData.get(element);
}

// Khi element bị remove khỏi DOM và không còn ref nào khác
// → entry trong WeakMap tự động bị GC thu hồi
```

### Ví dụ 4: Monitor heap over time
```js
function profileMemory() {
  if (performance.memory) {
    const mb = (size) => (size / 1024 / 1024).toFixed(2);
    console.log({
      used: mb(performance.memory.usedJSHeapSize),
      total: mb(performance.memory.totalJSHeapSize),
      limit: mb(performance.memory.jsHeapSizeLimit)
    });
  }
}

profileMemory(); // before
// ... perform actions that allocate memory ...
profileMemory(); // after — so sánh để thấy allocation
```

### Ví dụ 5: Object pooling pattern
```js
class Pool {
  constructor(createFn, maxSize = 10) {
    this.pool = [];
    this.createFn = createFn;
    this.maxSize = maxSize;
  }
  acquire() {
    return this.pool.length > 0 ? this.pool.pop() : this.createFn();
  }
  release(obj) {
    if (this.pool.length < this.maxSize) {
      this.pool.push(obj);
    }
    // Ngoài maxSize → obj tự bị GC
  }
}

const objPool = new Pool(() => ({ data: new Array(1000).fill(0) }));
const obj = objPool.acquire();
// ... use obj ...
objPool.release(obj); // trả về pool, không alloc mới
```

### Ví dụ 6: Leak qua closure — hiểu scope chain
```js
function createLeak() {
  const bigBuffer = new ArrayBuffer(10 * 1024 * 1024); // 10MB
  return function() {
    return bigBuffer.byteLength; // closure giữ bigBuffer
  };
}
const fn = createLeak();
// bigBuffer vẫn sống mãi vì fn giữ reference — dù createLeak đã return
// Fix: nếu fn không cần bigBuffer sau khi init, null nó
```

### Ví dụ 7: Detached DOM node leak
```js
function createLeak() {
  const div = document.createElement('div');
  div.textContent = 'Leaked element';
  document.body.appendChild(div);
  div.remove(); // gỡ khỏi DOM
  return div; // nhưng vẫn giữ reference!
}
const leaked = createLeak();
// detached DOM node — không hiển thị trên trang nhưng JS vẫn giữ → GC không dọn
// Fix: null leaked sau khi không cần
```

## 🔬 So sánh với alternatives

| Phương pháp | Ưu điểm | Nhược điểm | Phù hợp khi |
|---|---|---|---|
| **Mark & Sweep (mặc định)** | Xử lý circular ref, tự động | Không control được timing | Hầu hết case |
| **Reference Counting (cũ)** | Đơn giản, immediate free | Circular ref leak | Không nên dùng |
| **WeakMap cache** | Auto-free khi key gone | Chỉ object key | Cache theo DOM node |
| **Manual null** | Kiểm soát được | Dễ quên, khó maintain | Resource lớn, lifecycle rõ |
| **Object pooling** | Giảm GC pressure | Phức tạp, phải quản lý | Game, high-frequency alloc |

## 📊 Performance & Best Practices

- **Đo baseline trước**: chụp heap snapshot ở trạng thái clean, so sánh sau action.
- **Avoid large allocations in loops**: tạo `new Array()` trong loop → GC pressure → jank.
- **Null khi không cần**: `element = null`, `timerId = null` sau khi dùng xong.
- **Use `const` thay `let`**: `const` không thể reassign → engineer nhớ rõ hơn khi nào cắt ref.
- **Monitor trong dev**: Chrome DevTools → Memory → Allocation instrumentation on timeline.
- **Node production**: `--expose-gc` chỉ dùng trong test, không production.
- **`performance.memory` chỉ Chrome**: không dùng cho cross-browser monitoring.
- **GC pause**: heap lớn → sweep lâu → UI freeze. Tránh heap quá 100MB không cần thiết.

## 🔗 Liên kết chéo

- Xem thêm: `17_memory-management/01_memory-lifecycle-gc/01_garbage-collection/` — demo GC đầy đủ.
- Xem thêm: `17_memory-management/01_memory-lifecycle-gc/02_memory-leaks/` — 4 pattern leak kinh điển.
- Xem thêm: `17_memory-management/03_v8-engine/` — hidden class, inline cache, V8 pipeline.
- Xem thêm: `17_memory-management/04_meta-programming/` — Proxy/Reflect cho reactivity.
- Xem thêm: `19_browser-devtools/01_devtools-memory/` — thực hành heap snapshot tìm leak.
- Xem thêm: `18_dom-apis/02_dom-advanced/01_manipulation/` — DOM manipulation và memory implications.
