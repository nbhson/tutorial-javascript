# DevTools — Memory (Săn Memory Leak) — [Level: Intermediate]

## 🔑 Khái niệm cốt lõi

Tab **Memory** của Chrome DevTools dùng để phân tích cách ứng dụng **cấp phát và giữ bộ nhớ**. Ba công cụ chính:

### 1. Heap Snapshot
"Chụp ảnh" toàn bộ JS heap tại một thời điểm: danh sách object, kích thước (Shallow/Retained), và **Retainers** — đường tham chiếu từ root tới object, trả lời câu *"vì sao cái này chưa bị GC?"*. 

- **Shallow size**: bộ nhớ object tự nó chiếm (không tính children).
- **Retained size**: bộ nhớ object + tất cả object chỉ reachable qua nó (nếu remove object này, bao nhiêu memory sẽ được free).

Chụp **trước và sau một action**, so sánh 2 snapshot để tìm phần bộ nhớ không được trả lại → **memory leak**. Mục đặc biệt hữu ích: **Detached DOM** — node đã gỡ khỏi trang nhưng JS vẫn giữ tham chiếu.

### 2. Allocation Instrumentation on Timeline
Ghi lại **cấp phát theo thời gian**: thấy từng "đợt" memory tăng, từ hàm nào (call stack). Hợp để tìm code tạo rác liên tục. Màu xanh = đã thu hồi, màu đen = đang giữ.

### 3. Allocation Sampling
Lấy mẫu cấp phát nhẹ hơn khi muốn khảo sát nhanh — không record every allocation, chỉ sample.

### Quy trình chuẩn

1. Mở `01_devtools-memory/index.html`.
2. **Memory → Heap snapshot** bắt đầu (baseline).
3. Gọi `leak()` nhiều lần trên Console (hoặc chạy kịch bản thật).
4. Chụp snapshot lần 2 → chọn **Summary**, tìm `Array` với retained size cao; dùng cột **Retainers** để tìm ai giữ mảng — ở đây là biến global `arr`.

Nền tảng lý thuyết liên quan tại `17_memory-management`: GC Mark & Sweep, reachability, các pattern leak (global, listener, closure, timer).

## 📐 Cấu trúc / Cú pháp

### Heap Snapshot workflow
```
Bước 1: baseline
  Memory tab → Heap snapshot → Take snapshot
  Ghi lại usedJSHeapSize

Bước 2: thực hiện action
  Console: leak() 5 lần
  Hoặc: tương tác UI (click, scroll, mở modal...)

Bước 3: post-action snapshot
  Memory tab → Take snapshot lần 2

Bước 4: so sánh
  Chọn snapshot 2 → Dropdown: "Comparison"
  → "Objects allocated between snapshot 1 and 2"
  → Sắp xếp theo "Shallow size" hoặc "Retained size"

Bước 5: phân tích retainers
  Click vào object tăng → xem Retainers column
  → Tìm đường từ root (global, DOM, closure) đến object
  → Cắt reference đó để fix leak
```

### Allocation Timeline workflow
```
Bước 1: Memory tab → "Allocation instrumentation on timeline"
Bước 2: Click "Record"
Bước 3: Thực hiện action (gọi leak(), scroll, click...)
Bước 4: Click "Stop"
Bước 5: Nhìn timeline:
  - Cột xanh = objects đã GC
  - Cột đen = objects still retained
  - Click vào peak → xem call stack của allocation
```

### Đọc heap snapshot — các cột quan trọng

| Cột | Ý nghĩa |
|---|---|
| **Constructor** | Type của object (Array, Object, String, Function...) |
| **Shallow size** | Byte object tự chiếm (properties + structure) |
| **Retained size** | Byte object + tất cả objects chỉ reachable qua nó |
| **Retainers** | Ai đang giữ object này (global variable, closure, DOM node...) |
| **Detached** | DOM node đã remove khỏi DOM nhưng JS vẫn giữ ref |

## ✅ Điểm mạnh

1. **Chỉ điểm "hung thủ"**: Retainers cho biết đúng đường ai đang giữ object -> sửa đúng chỗ.
2. **Định lượng**: so sánh retained size trước/sau — biết leak bao nhiêu.
3. **Bắt detached DOM**: DevTools đánh dấu sẵn các node "đã tháo nhưng bị giữ" — lỗi kinh điển khi unmount SPA.
4. **Allocation timeline** nhìn được nguồn cấp phát theo call stack — tìm nơi tạo object thừa.
5. **Kết nối lý thuyết ↔ thực hành** trong repo (nối với GC/leak).
6. **Visual feedback** —เห็น rõ memory growth qua time, không phải đoán mò.
7. **Find "hidden" leaks** — leaks không gây crash ngay nhưng RAM tăng dần theo thời gian.

## ⚠️ Bẫy thường gặp & Hạn chế

1. **Take snapshot kích hoạt GC** làm con số nhảy — muốn so sánh công bằng hãy chụp **đúng 2 thời điểm** cùng kiểu thao tác.
2. **Số liệu khác nhau giữa lần chạy** — nên chạy lại vài lần lấy xu hướng, không tin 1 lần duy nhất.
3. **Chỉ phân tích JS heap** — không thấy hết native memory, GPU, cache ảnh (đó là nhiệm vụ của Performance/Memory dạng khác).
4. **Snapshot với heap rất lớn tốn dung lượng và chậm** — lọc theo constructor hay "All objects" để giảm.
5. **Retainers path dài** — đôi khi khó trace từ object về root, cần click nhiều lần để mở rộng tree.
6. **True leak vs expected growth** — một số memory growth là normal (cache, buffer pre-allocation).
7. **Chrome-specific** — Firefox/Safari có Memory tools nhưng UI và metric khác.

## 💡 Khi nào dùng

1. **Ứng dụng RAM tăng dần** theo thời gian (tab càng mở càng "phình").
2. **SPA chuyển trang / mở-đóng modal** nhiều lần nghi ngờ giữ ref node hay listener.
3. **Sau khi `remove()` một phần tử mà danh sách "Detached" vẫn tăng**.
4. **Cache/global array phình to** (đúng demo `arr` trong thư mục này).
5. **Kiểm chứng một bản sửa leak** — đo trước khi sửa vs sau khi sửa.
6. **Pre-deployment memory check** — đảm bảo không có leak trước khi deploy production.
7. **Load testing** — chạy action lặp nhiều lần, chụp snapshot sau mỗi loop để track memory trend.

## 🎯 Ví dụ minh họa

### Ví dụ 1: Demo leak pattern (file `app.js`)
```js
let arr = [];
function leak() { arr.push(new Array(100000).fill(0)); }
console.log('call leak() nhiều lần rồi chụp heap snapshot');
```

**Quy trình 4 bước:**
1. Mở `index.html` → mở **Memory tab**.
2. Chụp snapshot 1 (khởi điểm).
3. Trên Console gõ `leak()` 5 lần.
4. Chụp snapshot 2 → trong dòng `Array`, thấy **retained size tăng**; click để xem Retainers trỏ về `(global) arr`.

### Ví dụ 2: Detached DOM node leak
```js
function createDetached() {
  const div = document.createElement('div');
  div.textContent = 'I am detached';
  document.body.appendChild(div);
  div.remove(); // gỡ khỏi DOM
  return div; // nhưng vẫn giữ reference!
}
const leaked = createDetached();
// Heap snapshot → filter "Detached" → thấy 1 node
// Retainers: (global) leaked → div node
// Fix: leaked = null;
```

### Ví dụ 3: Event listener leak
```js
function attachListener() {
  const btn = document.createElement('button');
  btn.textContent = 'Click me';
  const handler = () => console.log('clicked');
  document.body.appendChild(btn);
  btn.addEventListener('click', handler);
  return { btn, handler }; // return để simulate component lifecycle
}

const component = attachListener();
component.btn.remove(); // DOM removed
// Nhưng component.btn và component.handler vẫn giữ reference!
// Listener vẫn sống → closure giữ mọi thứ
// Fix: component.btn.removeEventListener('click', component.handler);
```

### Ví dụ 4: Closure leak
```js
function createClosureLeak() {
  const bigData = new Array(1e6).fill('x'); // 8MB
  return function() {
    return bigData.length; // closure giữ bigData
  };
}
const fn = createClosureLeak();
// bigData sống mãi vì fn closure giữ — dù createClosureLeak đã return
// Heap snapshot → Tìm Function objects với large retained size
// Retainers → tìm closure scope
```

### Ví dụ 5: Allocation timeline — find allocation source
```
Memory → Allocation instrumentation on timeline → Record
// Trong lúc record, gọi leak() nhiều lần
// Timeline hiện các peak — click vào peak
// Bottom panel hiện call stack:
//   leak() at app.js:2
//   <anonymous> at console:1
// → Biết leak() là nguồn cấp phát
```

### Ví dụ 6: So sánh snapshot — diff view
```
1. Snapshot A (before)
2. Action: click button 10 lần
3. Snapshot B (after)
4. Chọn Snapshot B → Dropdown: "Comparison"
5. Chọn "Objects allocated between snapshot A and B"
6. Sort by "Retained size" DESC
7. Objects top list = potential leaks
```

### Ví dụ 7: Finding the GC root
```
Heap snapshot → Chọn object nghi ngờ → Click "Retainers"
→ Xem tree:
  Global
    └── arr (global variable)
          └── Array [100000]  ← object của chúng ta
→ Root là global variable `arr`
→ Fix: arr = null; hoặc dùng WeakMap thay Map
```

## 🔬 So sánh với alternatives

| Method | Precision | Setup | Browser support | Best for |
|---|---|---|---|---|
| **Heap Snapshot** | ⭐⭐⭐ High | Manual | Chrome, Edge | Precise leak location |
| **Allocation Timeline** | ⭐⭐⭐ High | Manual record | Chrome, Edge | Find allocation source |
| **Allocation Sampling** | ⭐⭐ Medium | Lightweight | Chrome, Edge | Quick investigation |
| **performance.memory** | ⭐⭐ Medium | Code only | Chrome only | Quick check in code |
| **Node --expose-gc** | ⭐⭐⭐ High | CLI flag | Node.js | Server-side GC testing |

## 📊 Performance & Best Practices

- **Take snapshots at stable points** — đừng chụp lúc GC đang chạy (wait 1-2 seconds sau action).
- **Use "Comparison" view** — so sánh 2 snapshot thay vì guess từ 1 snapshot.
- **Filter by Constructor** — "Array", "String", "Function" để nhanh tìm leak type.
- **Sort by Retained size** — objects với retained size lớn nhất thường là leak sources.
- **Check Detached filter** —chuyên dụng detached DOM nodes filter trong Memory tab.
- **Repeat 2-3 times** — GC behavior varies, repeat để xác nhận trend thật.
- **Combine with Performance tab** — memory leak thường đi kèm performance degradation.
- **Set memory limit awareness** — biết giới hạn heap của browser (~4GB 64-bit, ~1GB mobile).

## 🔗 Liên kết chéo

- Xem thêm: `19_browser-devtools/` — DevTools tổng quan.
- Xem thêm: `19_browser-devtools/02_devtools-performance/` — Performance profiling.
- Xem thêm: `17_memory-management/01_memory-lifecycle-gc/` — GC theory.
- Xem thêm: `17_memory-management/01_memory-lifecycle-gc/02_memory-leaks/` — 4 leak patterns.
- File tham khảo: `app.js`, `index.html` trong folder `01_devtools-memory/`.
