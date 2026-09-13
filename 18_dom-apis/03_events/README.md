# DOM Events — Sự Kiện Trong JavaScript — [Level: Intermediate]

## 🔑 Khái niệm cốt lõi

**DOM Event** là tín hiệu trình duyệt phát ra khi có điều gì đó xảy ra với trang (click, nhấn phím, hover, submit form, load...) và JS có thể **đăng ký lắng nghe** để phản hồi. Nền tảng nằm ở ba bài trong `01_f8-basic-dom`:

- **`10_dom-event`** — gán sự kiện qua *property* `element.onclick = fn`; object `MouseEvent` chứa mọi thông tin khi click.
- **`11_PreventDefault-StopPropagation`** — `preventDefault()` chặn hành vi mặc định của HTML (như click link điều hướng); `stopPropagation()` dừng sự lan truyền (bubbling) của sự kiện.
- **`12_EventListener`** — `addEventListener`/`removeEventListener`: đăng ký **nhiều listener** trên một element và **gỡ đúng listener** (bằng cùng tham chiếu hàm), hoặc tạm dừng bằng cách gán rỗng.

### Event Propagation — 3 pha

```
window
  ↓ capture phase
document
  ↓
html
  ↓
body
  ↓
div.parent
  ↓
button (target)  ← event xảy ra tại đây
  ↑ bubble phase
div.parent
  ↑
body
  ↑
html
  ↑
document
  ↑
window
```

1. **Capturing phase** (bắt): từ `window` đi xuống element đích.
2. **Target phase**: event đến element đích.
3. **Bubbling phase** (nổi bọt): từ element đích đi ngược lên `window`.

`addEventListener(type, handler, { capture: true })` đăng ký ở pha capturing. Mặc định là bubbling (`capture: false`).

### Event Delegation — kỹ thuật quan trọng

Thay vì gắn listener vào từng child element, ta gắn **một listener duy nhất vào parent** và dùng `e.target` để xác định child nào được tương tác:

```js
taskList.addEventListener('click', (e) => {
  if (e.target.tagName === 'LI') {
    e.target.remove();
  }
});
// 1 listener ở parent lo được hàng nghìn child — thêm/xóa child tùy ý
```

## 📐 Cấu trúc / Cú pháp

### Event listener basics
```js
// multiple handlers
function viec1() { console.log('Việc 1'); }
const btn = document.querySelector('button');
btn.addEventListener('click', viec1);
btn.addEventListener('click', () => console.log('Việc 2'));

// remove after 5 seconds
setTimeout(() => btn.removeEventListener('click', viec1), 5000);
```

### preventDefault + stopPropagation
```js
// preventDefault — chặn hành vi mặc định
div.onclick = () => console.log('div');
button.onclick = (e) => { e.stopPropagation(); console.log('button'); };

//阻止特定链接的默认导航
for (const a of document.links)
  a.onclick = (e) => { if (e.target.href !== 'http://facebook.com/') e.preventDefault(); };
```

### Event delegation pattern
```js
taskList.addEventListener('click', (e) => {
  if (e.target.tagName === 'LI') e.target.remove();
});
```

### Capture vs Bubble order
```js
document.addEventListener('click', () => console.log('document capture'), true);
div.addEventListener('click', () => console.log('div'));
button.addEventListener('click', () => console.log('button'));

// Click button → order:
// 1. "document capture" (capture phase)
// 2. "button" (target phase)
// 3. "div" (bubble phase)
// 4. document bubble (nếu có listener)
```

## ✅ Điểm mạnh

1. **Tương tác phong phú** — mọi hành vi động của trang đều xoay quanh sự kiện.
2. **Nhiều listener trên một element** (30 `addEventListener`) — linh hoạt hơn `onclick` chỉ giữ được một.
3. **Delegation giảm số listener**: 1 listener ở cha lo được hàng nghìn con — nhẹ và bảo trì dễ.
4. **Kiểm soát mịn**: `preventDefault` / `stopPropagation` cho đúng ngữ nghĩa.
5. **Chuẩn, tương thích mọi trình duyệt** hiện đại.
6. **Event object rich** — `target`, `currentTarget`, `type`, `timeStamp`, mouse position, key info.
7. **Lifecycle events** — `DOMContentLoaded`, `load`, `beforeunload`, `hashchange`, `resize`.
8. **Custom events** — `new CustomEvent()` tạo event riêng cho component communication.

## ⚠️ Bẫy thường gặp & Hạn chế

1. **`removeEventListener` chỉ gỡ được khi truyền đúng cùng hàm đã add** — dùng anonymous thì không gỡ:
   ```js
   btn.addEventListener('click', () => console.log('x'));
   btn.removeEventListener('click', () => console.log('x')); // ❌ KHÔNG work — khác function reference
   ```
2. **Quên gỡ listener (hoặc giữ ref node đã gỡ) → memory leak / detached DOM** (SPA chuyển trang).
3. **`stopPropagation` chăn cả đường lan truyền** — nếu code khác cùng nhánh phụ thuộc bubbling sẽ bị ảnh hưởng.
4. **`preventDefault` chỉ chặn hành vi mặc định, không dừng sự lan truyền** — đừng nhầm với `stopPropagation`.
5. **Nhiều listener nhiều nơi (không delegation) dễ chậm và khó gỡ lỗi** khi app phình to.
6. **Event bubbling qua shadow boundary** — cần `composed: true` để event vượt qua shadow DOM.
7. **Passive listener + preventDefault conflict** — `{ passive: true }` khiến preventDefault bị ignore.

## 💡 Khi nào dùng — Tình huống thực tến

1. **Mọi tương tác người dùng**: click, input, keydown, submit, scroll, resize.
2. **Sự kiện động**: sự kiện cần tự hủy đúng lúc (dựa `options.once`, hoặc removeEventListener).
3. **Delegation cho danh sách lớn / phần tử sinh ra sau** (to-do, bảng dữ liệu, menu dropdown).
4. **Form UX**: `preventDefault()` submit để validate rồi fetch thay vì reload.
5. **SPA routing** theo hash (`hashchange`) hoặc khởi động sau khi DOM sẵn sàng (`DOMContentLoaded`).
6. **Touch gestures** — touchstart, touchmove, touchend cho mobile interactions.
7. **Intersection Observer** — lazy load, infinite scroll thay vì scroll event.
8. **Performance monitoring** — benchmark interaction timing qua event timestamps.

## 🎯 Ví dụ minh họa

### Ví dụ 1: Multiple handlers + removal
```js
function viec1() { console.log('Việc 1'); }
const btn = document.querySelector('button');
btn.addEventListener('click', viec1);
btn.addEventListener('click', () => console.log('Việc 2'));
setTimeout(() => btn.removeEventListener('click', viec1), 5000);
// Sau 5s: chỉ còn "Việc 2"
```

### Ví dụ 2: preventDefault + stopPropagation
```js
div.onclick = () => console.log('div');
button.onclick = (e) => {
  e.stopPropagation(); // ngăn bubble lên div
  console.log('button');
};

for (const a of document.links)
  a.onclick = (e) => {
    if (e.target.href !== 'http://facebook.com/') e.preventDefault();
  };
```

### Ví dụ 3: Event delegation
```js
taskList.addEventListener('click', (e) => {
  if (e.target.tagName === 'LI') e.target.remove();
});
// 1 listener lo được mọi LI — thêm/xóa LI mới vẫn hoạt động
```

### Ví dụ 4: Capture vs Bubble
```js
document.addEventListener('click', () => console.log('document (capture)'), true);
document.addEventListener('click', () => console.log('document (bubble)'));

div.addEventListener('click', () => console.log('div'));
button.addEventListener('click', () => console.log('button'));

// Click button →:
// 1. "document (capture)"
// 2. "button"
// 3. "div"
// 4. "document (bubble)"
```

### Ví dụ 5: Custom event communication
```js
// Component A dispatches
const btn = document.querySelector('#btn-a');
btn.addEventListener('click', () => {
  btn.dispatchEvent(new CustomEvent('custom-action', {
    detail: { message: 'Hello from A' },
    bubbles: true,
    composed: true
  }));
});

// Component B listens (even across shadow boundary)
document.addEventListener('custom-action', (e) => {
  console.log('Received:', e.detail.message);
});
```

### Ví dụ 6: Form validation với events
```js
const form = document.querySelector('#login-form');
const emailInput = form.querySelector('#email');

emailInput.addEventListener('input', (e) => {
  const valid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(e.target.value);
  e.target.classList.toggle('error', !valid);
});

form.addEventListener('submit', (e) => {
  e.preventDefault();
  if (!emailInput.classList.contains('error')) {
    fetch('/api/login', { method: 'POST', body: new FormData(form) })
      .then(res => res.json())
      .then(data => console.log('Logged in:', data));
  }
});
```

### Ví dụ 7: Infinite scroll với debounce
```js
let scrollTimer;
window.addEventListener('scroll', () => {
  clearTimeout(scrollTimer);
  scrollTimer = setTimeout(() => {
    const atBottom = window.innerHeight + window.scrollY >= document.body.offsetHeight - 100;
    if (atBottom) loadMore();
  }, 100);
}, { passive: true });
```

### Ví dụ 8: Keyboard shortcuts
```js
document.addEventListener('keydown', (e) => {
  // Ctrl+S — save
  if (e.ctrlKey && e.key === 's') {
    e.preventDefault();
    saveDocument();
  }
  // Escape — close modal
  if (e.key === 'Escape') closeModal();
  // Arrow keys — navigate
  if (e.key === 'ArrowRight') nextSlide();
  if (e.key === 'ArrowLeft') prevSlide();
});
```

## 🔬 So sánh với alternatives

| Approach | Multiple handlers? | Removable? | Delegatable? | Modern? |
|---|---|---|---|---|
| **addEventListener** | ✅ | ✅ | ✅ (via target) | ✅ Chuẩn |
| **onclick property** | ❌ Chỉ 1 | ✅ Có | ❌ Không | ❌ Legacy |
| **inline onclick=""** | ❌ Chỉ 1 | ❌ Khó | ❌ Không | ❌ Bad |

## 📊 Performance & Best Practices

- **Event delegation** khi có nhiều similar elements — 1 listener thay N listeners.
- **Store handler reference** — cần `removeEventListener` → lưu function vào biến, không dùng anonymous.
- **Use `{ passive: true }` cho scroll/touch** —告诉 browser handler không preventDefault → optimize.
- **Use `{ once: true }` cho one-time handlers** — tự cleanup, tránh leak.
- **Remove listeners on unmount** — component cleanup để tránh memory leak.
- **Scope listeners** — không attach listener lên document nếu không cần.
- **Avoid listener density** — mỗi listener có memory + CPU overhead.
- **Test with DevTools** — Event listener breakpoints để debug propagation chain.

## 🔗 Liên kết chéo

- Xem thêm: `18_dom-apis/01_dom-basics/01_f8-basic-dom/10_dom-event/` — event basics.
- Xem thêm: `18_dom-apis/01_dom-basics/01_f8-basic-dom/11_PreventDefault-StopPropagation/` — event control.
- Xem thêm: `18_dom-apis/01_dom-basics/01_f8-basic-dom/12_EventListener/` — event types.
- Xem thêm: `18_dom-apis/02_dom-advanced/01_manipulation/example-2/` — lifecycle events.
- Xem thêm: `17_memory-management/01_memory-lifecycle-gc/02_memory-leaks/` — listener leak pattern.
- Tài liệu thêm: MDN Web Docs — Event interface, EventListener.
