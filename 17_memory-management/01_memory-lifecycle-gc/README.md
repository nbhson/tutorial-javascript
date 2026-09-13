# Vòng đời bộ nhớ và Garbage Collection

## 🔑 Khái niệm

Mọi chương trình đều trải qua vòng đời bộ nhớ ba bước:

1. **Allocate (cấp phát)**: biến, object, hàm được cấp vùng nhớ khi khai báo / tạo.
2. **Use (sử dụng)**: đọc, ghi, truy cập dữ liệu.
3. **Release (giải phóng)**: trả vùng nhớ về hệ thống khi không dùng nữa.

Trong JavaScript, bước 3 do **Garbage Collector (GC)** của engine tự động làm. Bạn không gọi `free()` như C — nhưng để viết đúng, bạn phải hiểu *khi nào* một object "chết", và GC áp thuật toán nào:

- **Mark & Sweep (hiện đại)**: bắt đầu từ các **root** (biến toàn cục, call stack, document/DOM đang hiển thị, module exports...), duyệt và **đánh dấu** mọi object reachable. Sau đó **quét sạch** object không được đánh dấu. Điểm mạnh quyết định: **xử lý được circular reference** (vì không đếm tham chiếu, chỉ check xem có đường đi từ root hay không).
- **Reference Counting (cũ)**: đếm số tham chiếu tới mỗi object; về 0 là xóa. Thất bại với **circular reference** — obj1→obj2→obj1 không bao giờ về 0 → **leak vĩnh viễn**.

Thư mục này chia làm hai phần:

- `01_garbage-collection/` — demo đầy đủ: kịch bản tham chiếu, circular, các loại leak, WeakMap, object pooling, theo dõi `performance.memory`.
- `02_memory-leaks/` — các pattern rò rỉ bộ nhớ điển hình và cách sửa.

## ✅ Điểm mạnh

- **Tự động**: không cần quản lý bộ nhớ tay, giảm lỗi use-after-free / double-free.
- **Hiểu vòng đời** = biết khi nào cắt tham chiếu để GC dọn được — tránh leak mà không cần tool phức tạp.
- **Mark & Sweep mạnh mẽ**: vượt qua giới hạn circular reference của reference counting.
- **WeakMap / WeakRef** cho phép đánh dấu "tham chiếu yếu" — GC thoải mái thu hồi khi không còn key mạnh.
- **Quan sát được** bằng `performance.memory` (Chrome) hoặc `v8.getHeapStatistics()` (Node).

## ⚠️ Lưu ý / Hạn chế

- GC **không chạy ngay lập tức** khi bạn "không dùng nữa" — nó đợi lúc engine rảnh; `usedJSHeapSize` giảm chậm.
- **Không có lệnh ép GC** chuẩn; `gc()` chỉ có trong DevTools / Node `--expose-gc`.
- `performance.memory` là API không tiêu chuẩn, chỉ đáng tin trên Chrome.
- Reference counting là bài học lịch sử — engine hiện đại không dùng nó làm thuật toán chính, nhưng khái niệm vẫn hữu ích để hiểu "leak do 2-side tham chiếu".

## 💡 Khi nào dùng

- Kiểm tra một ứng dụng **chạy lâu bị tăng RAM dần** — áp dụng vòng đời nhớ để tìm nơi giữ tham chiếu.
- Dọn **cache bằng WeakMap** thay vì Map để không biến cache thành leak.
- Quyết định **null / removeEventListener / clear interval** khi component unmount.
- Viết hệ thống **stream / cấp phát tạm** với khối lượng lớn — biết rõ lúc nào memory được trả lại.
- **Profile** bằng DevTools Memory / Node `--expose-gc` trước khi tối ưu.

## 🎯 Ví dụ minh họa

```js
let user = { name: "John" };
let admin = user;     // same object, 2 tham chiếu
user = null;          // vẫn còn admin -> KHÔNG bị GC
admin = null;         // hết tham chiếu -> GC thu hồi

// Circular: dù không ai dùng ngoài, Mark & Sweep vẫn dọn được
let obj1 = {}, obj2 = {};
obj1.ref = obj2; obj2.ref = obj1;
obj1 = null; obj2 = null;
```

## 📚 Tham khảo / Bài tập

- Vào `01_garbage-collection/`, chạy `index.html` trong trình duyệt: bấm **Chạy Demo**, **Profile Memory (~50MB)**, rồi **GC Demo (không gán null)** để thấy used heap tăng rồi tự về gần mốc ban đầu.
- Chạy `node --expose-gc garbage-collection-examples.js` để ép GC và đọc output từng phần (basic ref, circular, leak, weak, pooling...).
- Đọc `HOW_TO_USE.md` để theo đúng quy trình demo + mẹo Force GC.
- Vào `02_memory-leaks/` để xem danh sách 4 pattern rò rỉ phổ biến (global, listener, closure, timer) và cách sửa.
- Tự làm: chụp Heap Snapshot trước/sau khi bấm **Profile Memory** — tìm "Allocate ~50MB", so sánh Constructor/Dominator để xác định nguồn cấp phát.