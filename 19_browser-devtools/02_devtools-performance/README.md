# DevTools — Performance (Đo FPS, Long Task, Jank) — [Level: Intermediate]

## 🔑 Khái niệm cốt lõi

Tab **Performance** ghi lại hoạt động của **main thread** trong một khoảng thời gian để bạn thấy *"thời gian đi đâu"*. Các thông số nền tảng:

### FPS (Frames Per Second)
- Tiêu chuẩn mượt là **60fps** (≈16.7ms mỗi khung hình).
- FPS tụt / đường đồ thị FPS không nằm trên vạch xanh → UI đang **jank (giật)**.
- Mỗi frame budget: 16.7ms cho JS + CSS + Layout + Paint + Composite.

### Long Task
- Tác vụ chạy **> 50ms** trên main thread.
- Theo mô hình INP (Interaction to Next Paint), long task là thủ phạm chính khiến thao tác cảm giác chậm.
- Trong Performance panel, long tasks hiện màu **đỏ**.

### Main Thread Phases
Mỗi frame, main thread hoàn thành các pha:
1. **JS Execution** — chạy JavaScript
2. **Style** — recalculate CSS styles
3. **Layout** — compute geometry (reflow)
4. **Paint** — draw pixels
5. **Composite** — combine layers

Bạn nhìn được chỗ nào đỏ to (đắt) trên flame chart.

### Layout Thrashing
Vòng lặp xen kẽ *đọc → ghi → đọc → ghi* `offsetWidth/style` buộc trình duyệt **tính layout lại liên tục** — hiện rõ dưới dạng nhiều lần Recalculate Style/Layout cạnh nhau trên timeline.

### Quy trình thực hành

1. Mở `02_devtools-performance/index.html` → **Performance tab → record (●)**.
2. Đợi script chạy (`setTimeout(heavy, 100)`), giữ record ~5 giây, bấm **Stop**.
3. Đọc kết quả: tại thời điểm `heavy()` chạy xuất hiện **long task > 50ms**, FPS tụt; bạn có thể **drill vào task** để xem stack gọi tới `heavy`.

## 📐 Cấu trúc / Cú pháp

### Performance Tab — các metric chính

| Metric | Mô tả | Target |
|---|---|---|
| **FPS** | Frames per second | ≥ 60fps |
| **Long tasks** | Tasks > 50ms trên main thread | 0 tasks |
| **Layout** | Thời gian recalculate layout | < 5ms/frame |
| **Paint** | Thời gian vẽ pixel | < 10ms/frame |
| **Script** | Thời gian chạy JS | < 50ms/task |
| **GC** | Garbage collection pauses | Cố gắng giảm thiểu |

### Flame Chart — cách đọc
```
┌─────────────────────────────────┐
│ Timeline (ms)                   │
│ 0    50   100  150  200  250   │
│ ████░░░░████████░░░░░░░░░░░░░  │
│ Script  Idle  Script(Long!)Idle│
└─────────────────────────────────┘
█ = JS execution (scripting)
░ = Idle (main thread trống)
Đỏ = Long task (>50ms)
```

### CPU Throttling
```
Performance tab → CPU throttling dropdown:
- No throttling (mặc định)
- 4x CPU slowdown (simulate mid-range phone)
- 6x CPU slowdown (simulate low-end phone)
```

### Keyboards shortcuts
| Key | Action |
|---|---|
| `Ctrl+E` / `Cmd+E` | Toggle Elements |
| `Ctrl+Shift+C` / `Cmd+Opt+C` | Inspect element |
| `Ctrl+\` / `Cmd+\` | Toggle Performance recorder |
| `Esc` | Toggle Console |

## ✅ Điểm mạnh

1. **Định lượng chính xác**: "task >50ms" có số liệu cụ thể — không đoán mò.
2. **Xem được call stack của task**: biết đúng hàm nào tốn thời gian (ở demo là `heavy`).
3. **Phân biệt pha đắt tiền**: phân bổ giữa Scripting/Layout/Paint để chọn cách tối ưu phù hợp.
4. **So sánh nhiều lần record** khi tối ưu — đo lại sau khi sửa.
5. **Lighthouse / UX metrics** bổ trợ: FCP, LCP, INP định dạng theo metric chuẩn web.
6. **Flame chart trực quan** — thấy ngay function nào "ăn" nhiều time nhất.
7. **Simulate slow devices** — CPU throttling giúp test trên condition thực tế.

## ⚠️ Bẫy thường gặp & Hạn chế

1. **Kết quả nhạy với máy hiện tại**: CPU bận/tab khác chạy cũng ảnh hưởng — thử lại vài lần.
2. **Record lâu/heo làm dữ liệu rối** — nên record **kịch bản ngắn** (vài giây) đúng thao tác bạn muốn đo.
3. **Long task đầu tiên thường do tải trang** (parse/bundle) — tách biệt với tác vụ runtime.
4. **Hiểu FPS chưa đủ**: còn cần phân biệt **network** (Memory/Network tab) nếu chậm do tải dữ liệu.
5. **Performance recording có overhead** — chính việc record làm trang chậm hơn chút.
6. **Main thread bottleneck không phải lúc nào cũng JS** — có thể là Layout hoặc Paint.
7. **Mobile simulation qua throttling không chính xác 100%** — test trên device thật vẫn cần thiết.

## 💡 Khi nào dùng

1. **UI giật khi cuộn / click / nhập liệu** — tìm long task và những pha Layout/Paint đắt.
2. **Phê chuẩn tối ưu**: trước/sau khi tách worker, debounce, giảm reflow.
3. **Debug layout thrashing** khi danh sách/phức tạp thêm/xóa phần tử liên tục.
4. **Kiểm tra độ mượt của animation** (60fps, missing frames).
5. **Đo tác động của script nặng** (ở demo: `heavy()` chặn thread 1e7 vòng lặp).
6. **Pre-launch performance audit** — Lighthouse scores trước khi deploy.
7. **A/B test performance** — so sánh 2 versions của cùng một feature.

## 🎯 Ví dụ minh họa

### Ví dụ 1: Heavy function demo (file `app.js`)
```js
function heavy() {
  let s = 0;
  for (let i = 0; i < 1e7; i++) s += i;   // ~đủ để vượt 50ms
  return s;
}
console.log('click to record performance');
setTimeout(heavy, 100);
```

**Cách áp dụng trong DevTools:**
1. Mở `index.html`, bấm **● Record** trong **Performance**.
2. Chờ `heavy()` chạy (100ms sau khi load), giữ 3–5 giây rồi **Stop**.
3. Trên timeline: tìm **Task** màu vàng đỏ > 50ms; click để xem **self time / underlying call** = `heavy`.

### Ví dụ 2: Layout thrashing demonstration
```js
const boxes = document.querySelectorAll('.box');

// ❌ BAD — read then write in same loop → layout thrashing
boxes.forEach(box => {
  const height = box.offsetHeight; // read → trigger layout recalc
  box.style.height = (height * 2) + 'px'; // write → trigger another layout
});

// ✅ GOOD — batch reads then batch writes
const heights = [...boxes].map(box => box.offsetHeight); // all reads first
boxes.forEach((box, i) => {
  box.style.height = (heights[i] * 2) + 'px'; // then all writes
});
```
Performance tab sẽ hiện nhiều "Recalculate Style" + "Layout" bars liên tiếp cho case ❌.

### Ví dụ 3: Measuring FPS
```js
let frameCount = 0;
let lastTime = performance.now();

function animate() {
  frameCount++;
  const now = performance.now();
  if (now - lastTime >= 1000) {
    console.log(`FPS: ${frameCount}`);
    frameCount = 0;
    lastTime = now;
  }
  requestAnimationFrame(animate);
}
animate();
// Mục tiêu: ≥ 60 FPS
```

### Ví dụ 4: Long task detection
```js
// Performance API — detect long tasks automatically
if ('PerformanceObserver' in window) {
  const observer = new PerformanceObserver((list) => {
    for (const entry of list.getEntries()) {
      if (entry.duration > 50) {
        console.warn(`Long task detected: ${entry.duration.toFixed(2)}ms`, entry.name);
      }
    }
  });
  observer.observe({ type: 'longtask', buffered: true });
}
```

### Ví dụ 5: Web Worker để tránh blocking main thread
```js
// app.js — main thread
const worker = new Worker('heavy-worker.js');
worker.postMessage({ n: 1e8 });
worker.onmessage = (e) => {
  console.log('Result:', e.data);
  // Main thread vẫn responsive trong khi worker tính toán
};

// heavy-worker.js
self.onmessage = (e) => {
  let s = 0;
  for (let i = 0; i < e.data.n; i++) s += i;
  self.postMessage(s);
};
```

### Ví dụ 6: Before/After optimization comparison
```
// Before optimization
Performance record → Long task: 120ms (heavy function)
FPS drop: 60 → 12

// After: move to Web Worker
Performance record → Main thread idle during computation
FPS: stable 60

// Kết luận: Worker fix được long task issue
```

### Ví dụ 7: Measure specific operation duration
```js
performance.mark('start-operation');
// ... code to measure ...
performance.mark('end-operation');
performance.measure('operation-duration', 'start-operation', 'end-operation');

const measures = performance.getEntriesByName('operation-duration');
console.log(`Operation took: ${measures[0].duration.toFixed(2)}ms`);
```

## 🔬 So sánh với alternatives

| Tool | Metric | Accuracy | Browser support | Best for |
|---|---|---|---|---|
| **Chrome Performance** | FPS, tasks, layout | ⭐⭐⭐ High | Chrome, Edge | Detailed profiling |
| **Firefox Performance** | Same metrics | ⭐⭐⭐ High | Firefox | Firefox-specific |
| **Lighthouse** | FCP, LCP, INP | ⭐⭐⭐ High | All browsers | Overall score |
| **Web Vitals JS** | CLS, FID, LCP | ⭐⭐⭐ High | All browsers | Production monitoring |
| **console.time()** | Operation duration | ⭐⭐ Medium | All browsers | Quick measurement |

## 📊 Performance & Best Practices

- **Record short bursts** — 3-5 giây là đủ, record quá dài gây data overload.
- **Close other tabs** — giảm noise từ tab khác khi record.
- **Use CPU throttling** — 4x slowdown simulate mobile, phát hiện issues không hiện trên desktop.
- **Look for red bars** — long tasks >50ms là priority #1 để optimize.
- **Drill into flame chart** — click vào task để xem call stack chi tiết.
- **Compare before/after** — luôn có baseline trước khi optimize.
- **Use Performance.memory** — `performance.memory.usedJSHeapSize` để track heap over time.
- **Set performance budget** — ví dụ: "không có task nào >50ms", "FPS phải ≥55".

## 🔗 Liên kết chéo

- Xem thêm: `19_browser-devtools/01_devtools-memory/` — Memory profiling.
- Xem thêm: `19_browser-devtools/` — DevTools tổng quan.
- Xem thêm: `17_memory-management/03_v8-engine/` — V8 JIT impact on performance.
- Xem thêm: `18_dom-apis/01_dom-basics/02_how-browser-reads-html/` — rendering pipeline.
- Tài liệu thêm: [web.dev/measure](https://web.dev/measure), [Chrome DevTools Performance guide](https://developer.chrome.com/docs/devtools/performance).
