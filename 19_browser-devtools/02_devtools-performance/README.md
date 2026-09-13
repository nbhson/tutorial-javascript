# DevTools — Performance (Đo FPS, Long Task, Jank)

## 🔑 Khái niệm

Tab **Performance** ghi lại hoạt động của **main thread** trong một khoảng thời gian để bạn thấy *"thời gian đi đâu"*. Các thông số nền tảng:

- **FPS (frames per second)** — số khung hình mỗi giây; tiêu chuẩn mượt là **60fps** (≈16.7ms mỗi khung). FPS tụt / đường đồ thị FPS không nằm trên vạch xanh → UI đang **jank (giật)**.
- **Long task** — tác vụ chạy **> 50ms** trên main thread; theo mô hình INP (Interaction to Next Paint) đây là thủ phạm chính khiến thao tác cảm giác chậm.
- **Tasks / Frames / Phases Layout–Paint** — main thread hoàn thành việc vẽ qua các pha: *JS execution → Style → Layout → Paint → Composite*. Bạn nhìn được chỗ nào đỏ to (đắt).
- **Layout thrashing** — vòng lặp xen kẽ *đọc → ghi → đọc → ghi* `offsetWidth/style` buộc trình duyệt **tính layout lại liên tục** — hiện rõ dưới dạng nhiều lần Recalculate Style/Layout cạnh nhau.

Quy trình thực hành trong nhóm này với file `app.js` (vòng lặp `1e7` trong `heavy()`):

1. Mở `02_devtools-performance/index.html` → **Performance tab → record (●)**.
2. Đợi script chạy (`setTimeout(heavy, 100)`), giữ record ~5 giây, bấm **Stop**.
3. Đọc kết quả: tại thời điểm `heavy()` chạy xuất hiện **long task > 50ms**, FPS tụt; bạn có thể **drill vào task** để xem stack gọi tới `heavy`.

## ✅ Điểm mạnh

- **Định lượng chính xác**: "task >50ms" có số liệu cụ thể — không đoán mò.
- **Xem được call stack của task**: biết đúng hàm nào tốn thời gian (ở demo là `heavy`).
- **Phân biệt pha đắt tiền**: phân bổ giữa Scripting/Layout/Paint để chọn cách tối ưu phù hợp.
- **So sánh nhiều lần record** khi tối ưu — đo lại sau khi sửa.
- **Lighthouse / UX metrics** bổ trợ: FCP, LCP, INP định dạng theo metric chuẩn web.

## ⚠️ Lưu ý / Hạn chế

- Kết quả **nhạy với máy hiện tại**: CPU bận/tab khác chạy cũng ảnh hưởng — thử lại vài lần.
- Record lâu/heo làm dữ liệu rối — nên record **kịch bản ngắn** (vài giây) đúng thao tác bạn muốn đo.
- Long task đầu tiên thường do **tải trang** (parse/bundle) — tách biệt với tác vụ runtime.
- Hiểu FPS chưa đủ: còn cần phân biệt **network** (Memory/Network tab) nếu chậm do tải dữ liệu.

## 💡 Khi nào dùng

- **UI giật khi cuộn / click / nhập liệu** — tìm long task và những pha Layout/Paint đắt.
- **Phê chuẩn tối ưu**: trước/sau khi tách worker, debounce, giảm reflow.
- Debug **layout thrashing** khi danh sách/phức tạp thêm/xóa phần tử liên tục.
- Kiểm tra độ mượt của **animation** (60fps, missing frames).
- Đo tác động của **script nặng** (ở demo: `heavy()` chặn thread 1e7 vòng lặp).

## 🎯 Ví dụ minh họa

```js
// app.js — hàm nặng chạy trên main thread, tạo long task
function heavy() {
  let s = 0;
  for (let i = 0; i < 1e7; i++) s += i;   // ~đủ để vượt 50ms
  return s;
}
console.log('click to record performance');
setTimeout(heavy, 100);
```

Cách áp dụng trong DevTools:

1. Mở `index.html`, bấm **● Record** trong **Performance**.
2. Chờ `heavy()` chạy (100ms sau khi load), giữ 3–5 giây rồi **Stop**.
3. Trên timeline: tìm **Task** màu vàng đỏ > 50ms; click để xem **self time / underlying call** = `heavy`.

## 📚 Tham khảo / Bài tập

- Chạy `index.html` theo 3 bước trên; thử đổi `1e7` → `1e8` và record lại, quan sát thời lượng task và mức FPS tụt.
- Tự làm: giả lập **layout thrashing** bằng vòng lặp đọc `box.offsetHeight` rồi ghi `box.style.height = ...` — record và đếm số lần Recalculate Layout.
- Tự làm: so sánh 2 version — `heavy()` chạy trên main thread vs chạy trong **Web Worker** (kết quả send về qua message) — xem FPS khác nhau thế nào.
- Tự làm: dùng **Lighthouse** (thẻ Audits/Lighthouse) trên cùng trang để lấy thêm chỉ số performance tổng thể.
- Xem thêm: [web.dev/measure](https://web.dev/measure) và tab *Performance monitor* (bật mỗi 10s để xem CPU/memory theo thời gian).