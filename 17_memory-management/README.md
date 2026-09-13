# Quản lý bộ nhớ và hiệu năng

## 🔑 Khái niệm

JavaScript quản lý bộ nhớ **tự động**: khi bạn tạo biến, object, hàm, dữ liệu được đặt lên bộ nhớ, và khi không còn dùng nữa, engine sẽ dọn bằng **Garbage Collection (GC)**. Tài liệu này bao phủ các mảng kiến thức trọng tâm liên quan đến bộ nhớ và hiệu năng của JS:

- **Stack vs Heap**: Stack lưu giá trị nguyên thủy + tham chiếu (kích thước cố định, nhanh); Heap lưu object (lớn, cấp phát động, được GC dọn). Biến chứa object chỉ giữ "địa chỉ" trỏ vào Heap.
- **Vòng đời bộ nhớ**: *allocate → use → release*. JS lo phần "release" bằng GC, nhưng bạn vẫn có thể tạo **memory leak** nếu vô tình giữ tham chiếu không cần thiết.
- **GC — Mark & Sweep**: engine xuất phát từ các **root** (global, call stack, DOM hiển thị...) đánh dấu mọi object *reachable*; phần không reachable bị quét sạch. Khác với reference counting (đếm tham chiếu — **bó tay với circular reference**), mark & sweep loại bỏ cả vòng tròn tham chiếu.
- **V8 engine**: pipeline *Ignition (interpreter → bytecode) + TurboFan (JIT tối ưu → machine code)*, với **hidden class** và **inline caching** để truy cập property nhanh.
- **Metaprogramming**: `Proxy` và `Reflect` cho phép can thiệp hành vi object (validation, log, computed property, reactivity...) — một kỹ thuật nâng cao thường đi kèm các bài toán về hiệu năng/động.

Cấu trúc thư mục:

- `01_memory-lifecycle-gc/` — vòng đời bộ nhớ, GC, các loại memory leak.
- `03_v8-engine/` — cách V8 thực thi tối ưu JavaScript.
- `04_meta-programming/` — Proxy / Reflect.

## ✅ Điểm mạnh

- **Hiểu vòng đời bộ nhớ** giúp viết code không rò rỉ, ổn định khi chạy lâu.
- **Nắm GC (Mark & Sweep)** tự tin dùng closure, listener, cache — biết khi nào dữ liệu được giải phóng.
- **Hiểu V8 + hidden class/inline cache** giúp viết code "thân thiện JIT", tránh deopt hay tạo shape object rời rạc.
- **WeakMap/WeakSet** cho cache an toàn — mục GC thu hồi tự do.
- **Proxy/Reflect** mở ra reactivity, validation, logging mà không sửa code gốc.

## ⚠️ Lưu ý / Hạn chế

- Không có API JS thống nhất để "ép" GC — chỉ đoán được qua snapshot, `performance.memory` (Chrome), `--expose-gc` (Node).
- Chỉ dùng `performance.memory` được trên **Chrome/Chromium** — không tiêu chuẩn, không có trên Firefox/Safari.
- `used ≤ total ≤ limit` — `usedJSHeapSize` giảm chậm (GC trễ đến lúc idle), `totalJSHeapSize` thường giữ capacity.
- Proxy làm úp mở hành vi — gỡ lỗi khó; hidden class mất ổn định (deopt) khi thêm/xóa property không nhất quán.

## 💡 Khi nào dùng

- **Kiểm tra / sửa memory leak** trong SPA chạy lâu (danh sách không lọc, tab chuyển qua lại, toast accumulate...).
- **Tối ưu render/reflow** cho ứng dụng lớn — giảm tần suất can thiệp trực tiếp vào DOM.
- **Viết thư viện / framework** cần kiểm soát bộ nhớ, cache, hoặc phản ứng với dữ liệu.
- **Xử lý dữ liệu lớn** (stream, bảng dài) — tránh giữ toàn bộ trong bộ nhớ.
- **Metaprogramming**: proxy-validate input, biến object thành reactive, tạo "computed property".

## 🎯 Ví dụ minh họa

```js
// Leak qua global variable
function leak() { globalArr = new Array(1e6).fill(0); } // thiếu var/let/const
leak();

// GC dọn được circular reference nhờ Mark & Sweep
const a = {}, b = {};
a.ref = b; b.ref = a;
// ...khi không còn tham chiếu từ root, cả a và b đều bị thu hồi

// WeakMap: key yếu — khi key hết tham chiếu, entry bị GC
const cache = new WeakMap();
let key = { id: 1 };
cache.set(key, "value");
key = null; // entry này sẵn sàng bị thu hồi
```

## 📚 Tham khảo / Bài tập

- Vào `01_memory-lifecycle-gc/01_garbage-collection`, mở `index.html` chạy demo, hoặc `node --expose-gc garbage-collection-examples.js` để thử Force GC.
- Vào `04_meta-programming`, chạy `app.js` để xem Proxy log GET/SET mỗi lần truy cập property.
- Xem `03_v8-engine/README.md` + các ảnh `workflow.jpeg`, `code.png`, `wr2012-inline-cache.png` để hình dung pipeline V8.
- Tự làm: bật Chrome DevTools → Memory → Heap Snapshot trước/sau một action, so sánh `usedJSHeapSize`, tìm "Detached DOM" để phát hiện leak thật trong ứng dụng của bạn.