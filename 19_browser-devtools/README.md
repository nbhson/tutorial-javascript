# Browser DevTools — Công Cụ Gỡ Lỗi Trình Duyệt — [Level: Intermediate]

## 🔑 Khái niệm cốt lõi

**Browser DevTools** là bộ công cụ tích hợp sẵn trong trình duyệt (Chrome DevTools phổ biến nhất) giúp bạn **inspect, debug và tối ưu** trang web khi nó đang chạy thật. Đây là kỹ năng bắt buộc của mọi frontend developer — không có DevTools, bạn như "mù" khi debug.

Các mảng quan trọng nhất trong scope của nhóm này:

### Memory Tab
- **Heap Snapshot**: "chụp ảnh" toàn bộ JS heap tại một thời điểm — danh sách object, kích thước (Shallow/Retained), và **Retainers** — đường tham chiếu từ root tới object, trả lời câu *"vì sao cái này chưa bị GC?"*. Chụp **trước và sau một action**, so sánh 2 snapshot để tìm **memory leak** và **detached DOM nodes**.
- **Allocation instrumentation on timeline**: ghi lại **cấp phát theo thời gian** — thấy từng "đợt" memory tăng, từ hàm nào (call stack). Hợp để tìm code tạo rác liên tục.
- **Allocation sampling / performance monitors**: lấy mẫu cấp phát nhẹ hơn khi muốn khảo sát nhanh.

### Performance Tab
- **Record** một phiên tương tác rồi xem **FPS (frames per second)**, **long tasks** (>50ms chặn main thread), các pha **Layout/Paint**, **Layout thrashing**, và "jank" (giật) của UI.
- **Flame chart** — hiển thị call stack theo thời gian, thấy hàm nào tốn nhiều time nhất.
- **CPU throttling** — simulate slow device (4x CPU throttle) để test performance trên mobile.

Nguyên tắc chung khi dùng DevTools cho hiệu năng:
1. **Đo trước khi sửa** — luôn có baseline từ record/snapshot.
2. **Tái hiện một kịch bản nhỏ** — một action cụ thể, không phải toàn trang hỗn độn.
3. **So sánh trước/sau khi thay đổi code** — số liệu phải có đối chứng.

Thư mục con:
- `01_devtools-memory/` — file demo (`app.js`/`index.html`) giả lập **memory leak** để bạn thực hành chụp heap snapshot.
- `02_devtools-performance/` — file demo hàm nặng (`1e7` vòng lặp) để record Performance.

## 📐 Cấu trúc / Cú pháp

### Chrome DevTools — các tab chính

| Tab | Công dụng | Key features |
|---|---|---|
| **Elements** | Inspect DOM + CSS | Live edit DOM/CSS, see computed styles |
| **Console** | Log + execute JS | `$0` (current selected element), `dir()`, `table()` |
| **Source** | Debug JS | Breakpoints, step through, watch expressions |
| **Network** | Network requests | Request timing, waterfall, cache status |
| **Performance** | Performance profiling | FPS, long tasks, flame chart, memory |
| **Memory** | Memory analysis | Heap snapshot, allocation timeline, leak detection |
| **Application** | Storage + manifests | Cookies, localStorage, service workers, PWAs |
| **Lighthouse** | Audit + scores | Performance, accessibility, SEO, best practices |

### Memory Tab workflow
```
1. Mở DevTools → Memory tab
2. Chọn "Heap snapshot"
3. Click "Take snapshot" (baseline)
4. Thực hiện action (click buttons, scroll, add items...)
5. Click "Take snapshot" (post-action)
6. Chọn snapshot 2 → filter "Comparison" → "Between snapshot 1 and 2"
7. Tìm objects tăng — check Retainers để biết ai giữ reference
8. Đặc biệt: filter "Detached" để tìm DOM nodes bị leak
```

### Performance Tab workflow
```
1. Mở DevTools → Performance tab
2. Click "Record" (●)
3. Thực hiện action cần measure (scroll, click, type...)
4. Click "Stop" (■)
5. Phân tích:
   - FPS graph: đường dưới vạch xanh = jank
   - Long tasks (>50ms): highlight đỏ
   - Flame chart: hàm nào tốn time nhất
   - Layout/Paint bars: tần suất reflow
```

## ✅ Điểm mạnh

1. **Nhìn "trong ruột" ứng dụng**: DOM, network, JS heap, main thread — không cần sửa code.
2. **Chẩn đoán leak chính xác**: heap snapshot cho biết object nào bị giữ và giữ bởi ai (retainer path).
3. **Đo FPS long task định lượng**: biết chính xác task nào >50ms gây chậm.
4. **Miễn phí, có sẵn**: không cần cài thêm, hỗ trợ đầy đủ trên Chrome/Chromium.
5. **Gắn liền học tập**: dùng kết hợp với `17_memory-management` để hiểu GC và leak trong thực tế.
6. **Live edit**: Elements tab cho phép sửa DOM/CSS realtime — test fix ngay trên trang.
7. **Network throttling**: simulate 3G/slow CPU để test performance trên device yếu.
8. **Breakpoints đa dạng**: conditional breakpoint, DOM change breakpoint, XHR breakpoint.

## ⚠️ Bẫy thường gặp & Hạn chế

1. **Đo trên Chrome là chính**: một số metric (như `performance.memory`) chỉ đáng tin ở Chrome/Chromium.
2. **Giá trị bộ nhớ đổi lệch nhỏ giữa các lần đo** (GC trễ) — cần chạy lặp và so sánh tương đối, không tuyệt đối.
3. **Record Performance bị ảnh hưởng bởi máy đang tải** — đóng bớt tab, phần cứng ổn định để số liệu sạch.
4. **"Take Heap Snapshot" thường kích hoạt GC** nên số liệu nhảy — đừng ngạc nhiên khi usedJSHeapSize giảm sau khi chụp.
5. **Performance recording có overhead** — chính việc record làm chậm trang, số liệu có thể không hoàn toàn chính xác.
6. **Memory tab chậm với heap lớn** — snapshot heap > 500MB có thể tốn nhiều giây, browser có thể freeze tạm.
7. **DevTools có thể bị crash** trên trang rất nặng — dùng Task Manager của browser (`Shift+Esc`) để kill tab.

## 💡 Khi nào dùng — Tình huống thực tến

1. **Ứng dụng chậm dần theo thời gian** → Memory tab, tìm leak/detached DOM.
2. **UI giật khi cuộn/click** → Performance record, tìm long task & heavy layout.
3. **Cần xác nhận bản sửa hiệu quả** → đo lại sau khi tối ưu, so sánh số liệu.
4. **Học memory management thực chiến** (nối với `17_memory-management`).
5. **Phỏng vấn frontend** — thành thạo DevTools là kỹ năng được "soi" thường xuyên.
6. **Debug CSS layout issue** → Elements tab + computed style inspector.
7. **Optimize bundle size** → Network tab + Coverage tab (unused JS/CSS).
8. **Debug async/code flow** → Source tab + breakpoints + call stack.

## 🎯 Ví dụ minh họa

### Ví dụ 1: Memory leak demo (01_devtools-memory/app.js)
```js
let arr = [];
function leak() { arr.push(new Array(100000).fill(0)); }
console.log('call leak() nhiều lần rồi chụp heap snapshot');
```
Workflow:
1. Mở `index.html` → Memory tab → Take snapshot (baseline).
2. Console: gọi `leak()` 5-10 lần.
3. Take snapshot lần 2 → Summary → tìm `Array` với retained size tăng.
4. Click vào Array → Retainers column → thấy `(global) arr` giữ mảng.

### Ví dụ 2: Performance heavy task demo (02_devtools-performance/app.js)
```js
function heavy() {
  let s = 0;
  for (let i = 0; i < 1e7; i++) s += i;
  return s;
}
console.log('click to record performance');
setTimeout(heavy, 100);
```
Workflow:
1. Mở `index.html` → Performance tab → Record.
2. Chờ `heavy()` chạy (~100ms sau load).
3. Stop record → tìm task >50ms (đỏ) → click để xem call stack = `heavy`.

### Ví dụ 3: Debug DOM leak — detached nodes
```js
function createDetached() {
  const div = document.createElement('div');
  div.textContent = 'Leaked';
  document.body.appendChild(div);
  div.remove(); // gỡ khỏi DOM
  return div; // giữ reference → detached DOM leak
}
const leaked = createDetached();
// Memory → Heap snapshot → filter "Detached" → thấy 1 node
```

### Ví dụ 4: Layout thrashing detection
```js
const boxes = document.querySelectorAll('.box');
// ❌ BAD — read then write in loop → layout thrashing
boxes.forEach(box => {
  const h = box.offsetHeight; // read → trigger layout
  box.style.height = (h * 2) + 'px'; // write → trigger layout
});
// Performance tab: nhiều "Recalculate Style" + "Layout" bars liên tiếp
```

### Ví dụ 5: Network瀑布图分析
```
Network tab → 看 waterfall:
- DNS Lookup: 域名解析时间
- Initial Connection: TCP连接时间
- SSL: 加密握手时间
- Wait (TTFB): 服务器响应时间
- Content Download: 下载时间
- Total: 总时间

 otimizar: 减少TTFB (server optimization), 压缩内容 (gzip/brotli)
```

### Ví dụ 6: Coverage tab — find unused code
```
DevTools → More tools → Coverage
1. Click "Start collecting coverage"
2. Interact with page
3. Stop → see % unused JS/CSS
4. Reduce bundle size by removing unused code
```

## 🔬 So sánh với alternatives

| Tool | Strengths | Weaknesses | Best for |
|---|---|---|---|
| **Chrome DevTools** | Full-featured, free | Chrome-only advanced features | General debugging |
| **Firefox DevTools** | Good CSS/Grid inspector | Less performant than Chrome | Firefox-specific issues |
| **Safari Web Inspector** | iOS debugging | Limited features | Apple ecosystem |
| **React DevTools** | Component tree, props | React-only | React apps |
| **Vue DevTools** | Component tree, state | Vue-only | Vue apps |
| **Lighthouse** | Automated audit | Offline only | Performance scoring |

## 📊 Performance & Best Practices

- **Always take baseline**: chụp snapshot/record ở trạng thái clean trước khi action.
- **Repeat measurements**: chạy 2-3 lần, lấy trung bình — GC và cache ảnh hưởng số liệu.
- **Use CPU throttling**: 4x slowdown simulate mobile device thực tế.
- **Focus on long tasks**: task >50ms là nguyên nhân chính của jank — ưu tiên optimize những task này.
- **Check Retainers path**: khi tìm leak, đừng只看 object size — xem retainer để biết ai giữ reference.
- **Use "Select DOM element" trong Allocation timeline**: click vào object trong timeline để see DOM node liên quan.
- **Close other tabs**: khi record performance, đóng tab khác để giảm noise.
- **Use Workbench/ snippets**: lưu code snippet trong Sources tab để tái hiện bug nhanh.

## 🔗 Liên kết chéo

- Xem thêm: `19_browser-devtools/01_devtools-memory/` — Memory tab chi tiết.
- Xem thêm: `19_browser-devtools/02_devtools-performance/` — Performance profiling.
- Xem thêm: `17_memory-management/` — GC theory, memory leak patterns.
- Xem thêm: `17_memory-management/01_memory-lifecycle-gc/01_garbage-collection/` — demo GC đầy đủ.
- Xem thêm: `18_dom-apis/` — DOM APIs được debug qua DevTools.
- Tài liệu thêm: [Chrome DevTools docs](https://developer.chrome.com/docs/devtools/), [web.dev measure](https://web.dev/measure).
