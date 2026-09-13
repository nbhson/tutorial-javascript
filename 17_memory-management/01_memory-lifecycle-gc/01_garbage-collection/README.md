# Garbage Collection (GC)

## 🔑 Khái niệm

**Garbage Collection** là quá trình tự động tìm và **xóa các object không còn được dùng nữa** trong bộ nhớ của JavaScript. Khi bạn tạo biến, object, function, chúng được lưu vào heap; nếu không có cơ chế dọn dẹp, bộ nhớ sẽ đầy và dẫn tới lỗi **"Out of Memory"**.

GC trong JavaScript hiện đại dựa trên thuật toán **Mark and Sweep**:

1. **Mark Phase**: đi từ các **gốc (root)** — biến toàn cục, call stack, DOM đang hiển thị, module exports... — đánh dấu mọi object *reachable* (truy cập được).
2. **Sweep Phase**: quét toàn bộ heap, **giải phóng** các object *không được đánh dấu* (unreachable).

Một cách tư duy quan trọng: GC quyết định theo **reachability** (có đường từ root tới hay không), **không** phải theo bạn có gán `= null` hay không. Đối tượng trong một `{}` kết thúc, không return, không gắn global/DOM/closure → tự mất reachability → bị GC thu hồi mà không cần null.

Thư mục này là **demo hoàn chỉnh** gồm `index.html` (giao diện theo dõi memory trực quan), `garbage-collection-examples.js` (code ví dụ), và `HOW_TO_USE.md` (hướng dẫn chạy).

## ✅ Điểm mạnh

- Giảm hẳn lớp người-quản-lý-bộ-nhớ so với C/C++ — ít lỗi use-after-free.
- **Mark & Sweep xử lý được circular reference** — vốn là tử huyệt của reference counting.
- Có thể **giám sát** qua `performance.memory` (Chrome) và `v8.getHeapStatistics()` (Node).
- Hỗ trợ **WeakMap / WeakSet / WeakRef** — "tham chiếu yếu" để GC thoải mái thu hồi khi cần.
- Compacting/Generational GC (Minor young / Major old generation) giúp dọn nhanh với object tuổi thọ ngắn.

## ⚠️ Lưu ý / Hạn chế

- GC **tự động, không thể điều khiển trực tiếp**; `gc()` chỉ chạy khi có cờ đặc biệt (`--expose-gc`).
- **Trễ và không tức thời**: memory giảm sau vài giây (thường khi rảnh), hoặc chờ "Take Heap Snapshot" mới thấy rõ.
- `performance.memory` không tiêu chuẩn — Firefox/Safari không có.
- Chính GC cũng tốn CPU: cấp phát rác nhiều (allocation tấn/loops) làm giật màn hình → cần hạn chế tạo object thừa.

## 💡 Khi nào dùng

- Debug **tăng RAM từ từ** trong SPA — kiểm tra xem object "xong việc" còn reachable hay không.
- Quyết định dùng **WeakMap** cho cache tạm (cache theo key object).
- Tối ưu vòng lặp lớn — giảm cấp phát object lặp đi lặp lại.
- Quan sát **used ≤ total ≤ limit** để biết heap đang áp lực ra sao.
- Trước khi "gán null" để cleanup — xác định xem thực sự cần cắt tham chiếu hay scope đã tự mất.

## 🎯 Ví dụ minh họa

```js
let user = { name: "John" };
let admin = user;   // 2 tham chiếu, chưa bị GC
user = null;        // vẫn reachable qua admin
admin = null;       // giờ unreachable -> GC sẽ thu hồi

// Circular reference: Mark & Sweep vẫn dọn được
const a = {}, b = {};
a.ref = b; b.ref = a;
a = null; b = null; // không còn đường từ root -> thu hồi cả hai
```

## 📚 Tham khảo / Bài tập

- Mở `index.html` trong Chrome: bấm **▶️ Chạy Demo**, **📈 Profile Memory (~50MB)**, **🧹 Free Allocation**, rồi **🧪 GC Demo (không gán null)** — quan sát các dòng `usedJSHeapSize` trước/sau (MB) để thấy GC thu hồi tự nhiên.
- Chạy script Node: `node --expose-gc garbage-collection-examples.js` — theo dõi 7 phần demo (basic ref, circular, leak, weak ref, object pool, monitor, best practices).
- Mở DevTools → Memory → chụp "Allocation instrumentation on timeline" để thấy cấp phát theo thời gian.
- Đọc `HOW_TO_USE.md` để nắm đủ nút bấm và mẹo Force GC.
- Tự làm: đổi `30 * 1024 * 1024` trong `demoEphemeralAllocation()` thành 80MB, chạy lại, xem tốc độ GC dọn — từ đó hiểu ảnh hưởng của kích thước cấp phát mãi tới khi engine cần dọn gấp.