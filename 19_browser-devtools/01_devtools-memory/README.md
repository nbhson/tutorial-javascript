# DevTools — Memory (Săn Memory Leak)

## 🔑 Khái niệm

Tab **Memory** của Chrome DevTools dùng để phân tích cách ứng dụng **cấp phát và giữ bộ nhớ**. Ba công cụ chính:

1. **Heap Snapshot** — "chụp ảnh" toàn bộ JS heap tại một thời điểm: danh sách object, kích thước (Shallow/Retained), và **Retainers** — đường tham chiếu từ root tới object, trả lời câu *"vì sao cái này chưa bị GC?"*. Chụp **trước và sau một action**, so sánh 2 snapshot để tìm phần bộ nhớ không được trả lại → **memory leak**. Mục đặc biệt hữu ích: **Detached DOM** — node đã gỡ khỏi trang nhưng JS vẫn giữ tham chiếu.
2. **Allocation instrumentation on timeline** — ghi lại **cấp phát theo thời gian**: thấy từng "đợt" memory tăng, từ hàm nào (call stack). Hợp để tìm code tạo rác liên tục.
3. **Allocation sampling / performance monitors** — lấy mẫu cấp phát nhẹ hơn khi muốn khảo sát nhanh.

Quy trình chuẩn thực hành trong nhóm này với file `app.js` (chỉ tạo `arr.push(new Array(100000).fill(0))` qua `leak()`):

1. Mở `01_devtools-memory/index.html`.
2. **Memory → Heap snapshot** bắt đầu (baseline).
3. Gọi `leak()` nhiều lần trên Console (hoặc chạy kịch bản thật).
4. Chụp snapshot lần 2 → chọn **Summary**, tìm `Array` với retained size cao; dùng cột **Retainers** để tìm ai giữ mảng — ở đây là biến global `arr`.

Nền tảng lý thuyết liên quan tại `17_memory-management`: GC Mark & Sweep, reachability, các pattern leak (global, listener, closure, timer).

## ✅ Điểm mạnh

- **Chỉ điểm "hung thủ"**: Retainers cho biết đúng đường ai đang giữ object -> sửa đúng chỗ.
- **Định lượng**: so sánh retained size trước/sau — biết leak bao nhiêu.
- **Bắt detached DOM**: DevTools đánh dấu sẵn các node "đã tháo nhưng bị giữ" — lỗi kinh điển khi unmount SPA.
- **Allocation timeline** nhìn được nguồn cấp phát theo call stack — tìm nơi tạo object thừa.
- **Kết nối lý thuyết ↔ thực hành** trong repo (nối với GC/leak).

## ⚠️ Lưu ý / Hạn chế

- **Take snapshot kích hoạt GC** làm con số nhảy; muốn so sánh công bằng hãy chụp **đúng 2 thời điểm** cùng kiểu thao tác.
- Số liệu **khác nhau giữa lần chạy** — nên chạy lại vài lần lấy xu hướng.
- Chỉ phân tích **JS heap** — không thấy hết native memory, GPU, cache ảnh (đó là nhiệm vụ của Performance/Memory dạng khác).
- Snapshot với heap rất lớn **tốn dung lượng và chậm** — lọc theo constructor hay "All objects" để giảm.

## 💡 Khi nào dùng

- Ứng dụng **RAM tăng dần** theo thời gian (tab càng mở càng "phình").
- **SPA chuyển trang / mở-đóng modal** nhiều lần nghi ngờ giữ ref node hay listener.
- Sau khi `remove()` một phần tử mà **danh sách "Detached"** vẫn tăng.
- Cache/global array phình to (đúng demo `arr` trong thư mục này).
- Kiểm chứng một bản sửa leak — đo trước khi sửa vs sau khi sửa.

## 🎯 Ví dụ minh họa

```js
// app.js — mô phỏng leak do giữ mảng trong biến global
let arr = [];
function leak() { arr.push(new Array(100000).fill(0)); }
console.log('call leak() nhiều lần rồi chụp heap snapshot');
```

Quy trình 4 bước áp dụng trong DevTools:

1. Mở `index.html` → mở **Memory tab**.
2. Chụp snapshot 1 (khởi điểm).
3. Trên Console gõ `leak()` 5 lần.
4. Chụp snapshot 2 → trong dòng `Array`, thấy **retained size tăng**; click để xem Retainers trỏ về `(global) arr`.

## 📚 Tham khảo / Bài tập

- Chạy `index.html` và thực hiện đúng 4 bước ở trên; thử thêm mẹo: dùng **Summary → "Objects allocated between snapshots"** để chỉ lọc phần mới.
- Tự làm: đổi `new Array(100000)` → `new Array(1e6)` — đo lại, quan sát retained size tăng 10 lần.
- Tự làm: thêm một danh sách DOM (tạo `<li>`, `querySelector`, `appendChild`, rồi `ul.remove()` nhưng vẫn giữ biến `li`); chụp snapshot và tìm mục **"Detached"**.
- Tự làm: bấm **Allocation instrumentation on timeline**, record 5 giây có gọi `leak()` — nhìn các cột màu xanh (đã thu hồi) và đen (bị giữ) phân bố.
- Nối lý thuyết: đọc lại `17_memory-management/01_memory-lifecycle-gc` để hiểu vì sao mảng `arr` là "reachable từ root" và GC không thể dọn.