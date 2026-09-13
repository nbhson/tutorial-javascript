# Browser DevTools — Công Cụ Gỡ Lỗi Trình Duyệt

## 🔑 Khái niệm

**Browser DevTools** là bộ công cụ tích hợp sẵn trong trình duyệt (Chrome DevTools phổ biến nhất) giúp bạn **inspect, debug và tối ưu** trang web khi nó đang chạy thật. Các mảng quan trọng nhất trong scope của nhóm này:

- **Memory tab** — đo lượng bộ nhớ, chụp **Heap Snapshot**, so sánh snapshot trước/sau một action để tìm **memory leak** và **detached DOM nodes**; **Allocation timeline** cho thấy cấp phát theo thời gian; **GC root / Retainers** cho biết vì sao một object không bị thu hồi.
- **Performance tab** — **record** một phiên tương tác rồi xem **FPS (frames per second)**, **long tasks** (>50ms chặn main thread), các pha **Layout/Paint**, **Layout thrashing**, và "jank" (giật) của UI.

Nguyên tắc chung khi dùng DevTools cho hiệu năng:

1. **Đo trước khi sửa** — luôn có baseline từ record/snapshot.
2. **Tái hiện một kịch bản nhỏ** — một action cụ thể, không phải toàn trang hỗn độn.
3. **So sánh trước/sau khi thay đổi code** — số liệu phải có đối chứng.

Thư mục con:

- `01_devtools-memory/` — file demo (`app.js`/`index.html`) giả lập **memory leak** để bạn thực hành chụp heap snapshot.
- `02_devtools-performance/` — file demo hàm nặng (`1e7` vòng lặp) để record Performance.

## ✅ Điểm mạnh

- **Nhìn "trong ruột" ứng dụng**: DOM, network, JS heap, main thread — không cần sửa code.
- **Chẩn đoán leak chính xác**: heap snapshot cho biết object nào bị giữ và giữ bởi ai (retainer path).
- **Đo FPS long task định lượng**: biết chính xác task nào >50ms gây chậm.
- **Miễn phí, có sẵn**: không cần cài thêm, hỗ trợ đầy đủ trên Chrome/Chromium.
- **Gắn liền học tập**: dùng kết hợp với `17_memory-management` để hiểu GC và leak trong thực tế.

## ⚠️ Lưu ý / Hạn chế

- **Đo trên Chrome là chính**: một số metric (như `performance.memory`) chỉ đáng tin ở Chrome/Chromium.
- Giá trị bộ nhớ **đổi lệch nhỏ** giữa các lần đo (GC trễ) — cần chạy lặp và so sánh tương đối, không tuyệt đối.
- Record Performance **bị ảnh hưởng bởi máy đang tải** — đóng bớt tab, phần cứng ổn định để số liệu sạch.
- "Take Heap Snapshot" thường kích hoạt **GC nên số liệu nhảy** — đừng ngạc nhiên khi usedJSHeapSize giảm sau khi chụp.

## 💡 Khi nào dùng

- **Ứng dụng chậm dần theo thời gian** → Memory tab, tìm leak/detached DOM.
- **UI giật khi cuộn/click** → Performance record, tìm long task & heavy layout.
- **Cần xác nhận bản sửa hiệu quả** → đo lại sau khi tối ưu.
- **Học memory management thực chiến** (nối với `17_memory-management`).
- **Phỏng vấn frontend** — thành thạo DevTools là kỹ năng được "soi" thường xuyên.

## 🎯 Ví dụ minh họa

```js
// memory demo (01_devtools-memory/app.js) — cố tình tạo leak
let arr = [];
function leak() { arr.push(new Array(100000).fill(0)); }
console.log('call leak() nhiều lần rồi chụp heap snapshot');

// performance demo (02_devtools-performance/app.js) — task nặng chặn thread
function heavy() { let s = 0; for (let i = 0; i < 1e7; i++) s += i; return s; }
setTimeout(heavy, 100);
```

## 📚 Tham khảo / Bài tập

- Vào `01_devtools-memory`: mở `index.html`, gọi `leak()` nhiều lần trên Console, rồi **Memory → Take heap snapshot** — tìm mảng tăng; thử "Allocation instrumentation on timeline" để thấy từng đợt cấp phát.
- Vào `02_devtools-performance`: mở `index.html`, bật **Performance → record** ~5 giây — tìm task >50ms (hàm `heavy`), xem FPS giảm ra sao.
- Tự làm: với mỗi thư mục, thay đổi tham số (`1e7` thành `1e8`, số lần `leak()`) rồi đo lại — tập đọc số liệu.
- Tự làm kết hợp: tạo một thành phần DOM rồi `remove()` nó nhưng vẫn giữ biến JS tham chiếu; chụp snapshot tìm mục **Detached** trong Memory tab.