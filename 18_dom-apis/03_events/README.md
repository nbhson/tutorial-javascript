# DOM Events — Sự Kiện Trong JavaScript

## 🔑 Khái niệm

**DOM Event** là tín hiệu trình duyệt phát ra khi có điều gì đó xảy ra với trang (click, nhấn phím, hover, submit form, load...) và JS có thể **đăng ký lắng nghe** để phản hồi. Nền tảng nằm ở ba bài trong `01_f8-basic-dom`:

- **`10_dom-event`** — gán sự kiện qua *property* `element.onclick = fn`; object `MouseEvent` chứa mọi thông tin khi click.
- **`11_PreventDefault-StopPropagation`** — `preventDefault()` chặn hành vi mặc định của HTML (như click link điều hướng); `stopPropagation()` dừng sự lan truyền (bubbling) của sự kiện.
- **`12_EventListener`** — `addEventListener`/`removeEventListener`: đăng ký **nhiều listener** trên một element và **gỡ đúng listener** (bằng cùng tham chiếu hàm), hoặc tạm dừng bằng cách gán rỗng.

Hai khái niệm cốt lõi về đường lan truyền:

- **Bubbling (nổi bọt)**: sự kiện đi từ phần tử đích lên đến `window` — cha, ông... đều nhận được. Nhờ đó có **Event Delegation**: gắn một listener ở cha để xử lý cho tất cả con (thêm/xóa con tùy ý mà vẫn hoạt động).
- **Capturing (bắt)**: pha ngược lại — từ `window` xuống đích, qua `addEventListener(type, fn, { capture: true })`.

Các mẫu sự kiện vòng đời trang (`DOMContentLoaded`, `load`, `beforeunload`, `hashchange`, `resize`...) được minh họa trong `02_dom-advanced/01_manipulation/example-2`.

## ✅ Điểm mạnh

- **Tương tác phong phú**: mọi hành vi động của trang đều xoay quanh sự kiện.
- **Nhiều listener trên một element** (30 `addEventListener`) — linh hoạt hơn `onclick` chỉ giữ được một.
- **Delegation giảm số listener**: 1 listener ở cha lo được hàng nghìn con — nhẹ và bảo trì dễ.
- **Kiểm soát mịn**: `preventDefault` / `stopPropagation` cho đúng ngữ nghĩa.
- **Chuẩn, tương thích mọi trình duyệt** hiện đại.

## ⚠️ Lưu ý / Hạn chế

- `removeEventListener` **chỉ gỡ được** khi truyền đúng **cùng hàm** đã add — dùng anonymous thì không gỡ.
- Quên gỡ listener (hoặc giữ ref node đã gỡ) → **memory leak / detached DOM** (SPA chuyển trang).
- `stopPropagation` chăn cả đường lan truyền — nếu code khác cùng nhánh phụ thuộc bubbling sẽ bị ảnh hưởng.
- `preventDefault` chỉ chặn hành vi mặc định, **không dừng** sự lan truyền — đừng nhầm với `stopPropagation`.
- Nhiều listener nhiều nơi (không delegation) dễ **chậm và khó gỡ lỗi** khi app phình to.

## 💡 Khi nào dùng

- Mọi tương tác người dùng: click, input, keydown, submit, scroll, resize.
- **Sự kiện động**: sự kiện cần tự hủy đúng lúc (dựa `options.once`, hoặc removeEventListener).
- **Delegation** cho danh sách lớn / phần tử sinh ra sau (to-do, bảng dữ liệu, menu dropdown).
- **Form UX**: `preventDefault()` submit để validate rồi fetch thay vì reload.
- **SPA routing** theo hash (`hashchange`) hoặc khởi động sau khi DOM sẵn sàng (`DOMContentLoaded`).

## 🎯 Ví dụ minh họa

```js
// 12_EventListener — nhiều handler + gỡ handler
function viec1() { console.log('Việc 1'); }
const btn = document.querySelector('button');
btn.addEventListener('click', viec1);
btn.addEventListener('click', () => console.log('Việc 2'));
setTimeout(() => btn.removeEventListener('click', viec1), 5000); // sau 5s chỉ còn "Việc 2"

// 11 — chặn điều hướng mặc định + dừng nổi bọt
div.onclick = () => console.log('div');
button.onclick = (e) => { e.stopPropagation(); console.log('button'); };
for (const a of document.links)
  a.onclick = (e) => { if (e.target.href !== 'http://facebook.com/') e.preventDefault(); };

// Delegation mẫu
taskList.addEventListener('click', (e) => {
  if (e.target.tagName === 'LI') e.target.remove();
});
```

## 📚 Tham khảo / Bài tập

- Chạy tuần tự ba bài trong `01_f8-basic-dom`: `10_dom-event`, `11_PreventDefault-StopPropagation`, `12_EventListener` (mở `index.html` mỗi bài + Console).
- Xem `02_dom-advanced/01_manipulation/example-2` cho phần sự kiện vòng đời trang (`DOMContentLoaded`, `load`, `beforeunload`, `hashchange`, `resize`).
- Tự làm **event delegation**: trong `example-2` thay listener remove từng `<li>` bằng một listener ở `taskList` dùng `e.target.tagName === 'LI'`.
- Tự làm `capture`: `document.addEventListener('click', () => console.log('capture'), true)` rồi log thêm ở element — quan sát thứ tự capture/bubble.
- Đọc thêm chi tiết sự kiện: <https://www.w3schools.com/jsref/dom_obj_event.asp> và MDN Event (bubbles, composed, defaultPrevented).