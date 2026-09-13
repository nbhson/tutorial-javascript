# Memory Leaks — 4 Pattern Rò Rỉ Bộ Nhớ Phổ Biến

## 🔑 Khái niệm

**Memory leak** xảy ra khi chương trình **giữ tham chiếu tới dữ liệu không còn dùng nữa**, khiến GC không thể thu hồi, bộ nhớ tăng dần theo thời gian và cuối cùng dẫn tới chậm, treo, hoặc **OOM (Out of Memory)**.

Vì GC chỉ dọn object "unreachable từ root", nên cách phòng chống leak đơn giản nhất là: **đừng tạo đường tham chiếu thừa**. Có bốn pattern rò rỉ kinh điển trong JavaScript (tài liệu tham khảo gốc: kipalog.com):

1. **Biến toàn cục** — quên `var/let/const`, tạo biến gắn lên `globalThis`, tồn tại mãi.
2. **Event listeners** — gắn callback vào một element nhưng không `removeEventListener` khi không cần; element bị hold → toàn bộ closure trong callback cũng bị giữ.
3. **Closure** — hàm inner giữ biến của scope cha; nếu hàm còn "sống" lâu hơn dự định, dữ liệu lớn trong scope bị giữ cùng.
4. **Timers / Intervals** — `setInterval/setTimeout` nhắc callback định kỳ; quên `clearInterval/clearTimeout` giữ callback và mọi thứ nó nắm. (Trong DOM còn có **detached DOM nodes** — node bị gỡ khỏi trang nhưng JS vẫn giữ tham chiếu.)

Các yếu tố làm leak trở nên nghiêm trọng: biến bị "nhô" lên global, closure bao quanh dữ liệu lớn, listener/callback không được dọn khi **unmount** (SPA chuyển trang).

## ✅ Điểm mạnh (của việc hiểu và tránh leak)

- **Ứng dụng ổn định**: RAM không "leo thang", không giật, không treo khi chạy lâu.
- **Tự tin trong SPA** lớn: biết khi nào phải dọn listener, interval, và tham chiếu DOM đã gỡ.
- **Kết nối tốt với GC**: hiểu reachability để quyết định đúng lúc cắt tham chiếu.
- **Tránh được lớp lỗi tinh vi** chỉ xuất hiện sau hours chạy thực tế.
- Dùng được **WeakMap/WeakRef** để biến một số cache nguy hiểm thành an toàn.

## ⚠️ Lưu ý / Hạn chế

- Leak khó thấy: không có lỗi gì ngay, chỉ RAM tăng chậm — cần **heap snapshot trước/sau** để đo.
- `clearInterval` không tự cho biết: bạn phải "nhớ" handle mình đã tạo.
- `removeEventListener` chỉ hiệu quả nếu truyền **đúng cùng hàm tham chiếu** đã add — dùng anonymous thì không gỡ được.
- Closure vô hại ở mức nhỏ, nguy hiểm khi bao quanh **dữ liệu lớn / DOM**. Đừng tin giá trị "chắc GC dọn" khi scope vẫn sống.
- Gán `= null` giúp cắt tham chiếu để GC dọn **sớm**, nhưng nếu object vẫn còn root tham chiếu thì vô dụng.

## 💡 Khi nào dùng (điểm áp dụng)

- **SPA chuyển trang / mở-đóng modal** liên tục — dọn listener, interval, ref DOM trong lifecycle teardown.
- **Danh sách vô hạn (infinite scroll)** — hủy observer (`IntersectionObserver.disconnect`) và ref node cũ.
- **Cache ứng dụng** — dùng `Map` hay `WeakMap`; xóa entry khi data hết hạn.
- **Cảnh báo** khi bạn viết closure bao quanh mảng lớn hoặc DOM để "dùng sau".

## 🎯 Ví dụ minh họa

```js
// 1. Global variable
function leak() { leaked = new Array(1e6).fill(0); }  // thiếu let/const => global
leak();

// 2. Event listener không dọn
const btn = document.getElementById('btn');
const handler = () => console.log('click');
btn.addEventListener('click', handler);
// khi không cần nữa:
btn.removeEventListener('click', handler);

// 3. Closure giữ data lớn
function create() {
  const big = new Array(1e6).fill('x');
  return function () { console.log('sum', big.length); };
}
const cb = create();  // big được giữ mãi theo cb

// 4. Timer quên dọn
const id = setInterval(() => tick(), 1000);
clearInterval(id);  // bắt buộc khi component unmount
```

## 📚 Tham khảo / Bài tập

- Đọc bài gốc: <https://kipalog.com/posts/Duc-khoet-Javascript--Phan-3---Quan-ly-bo-nho---4-truong-hop-ro-ri-pho-bien>
- Xem pattern demo có sẵn trong `01_garbage-collection/garbage-collection-examples.js` (mục **3. Memory Leak Examples** — global, event listener, closure) hoặc mở `index.html` để chạy trực quan.
- Tự làm trong DevTools: mở **Memory → Heap snapshot** ở trạng thái sạch, chạy một đoạn tạo `let arr = []` rồi push mảng lớn trong `setInterval`; chụp snapshot lần 2 — tìm node tăng bất thường để hiểu cách leak hiện hình.
- Tự làm: viết component nhỏ (vanilla JS) mô phỏng "unmount", trong đó quên `removeEventListener` — rồi dùng **Detached DOM / Retainers** trong snapshot để thấy node bị giữ.
- Tự làm: chuyển cache từ `Map` sang `WeakMap`, chụp snapshot và so sánh cấp phát khi key bị null.