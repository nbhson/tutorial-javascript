# Bài 10 — DOM Event: Gắn Sự Kiện — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

**Event** là tín hiệu trình duyệt phát ra khi có điều gì đó xảy ra với trang: click, scroll, keydown, submit, load... JavaScript có thể **đăng ký lắng nghe** để phản hồi qua `addEventListener`.

### addEventListener syntax
```js
element.addEventListener(type, handler, options)
```

| Option | Kiểu mặc định | Ý nghĩa |
|---|---|---|
| `{capture: false}` | false | Chạy ở phase bubbling (mặc định) |
| `{capture: true}` | false | Chạy ở phase capturing (root → leaf) |
| `{once: false}` | false | Tự remove sau lần gọi đầu tiên |
| `{passive: false}` | false | Handler có thể gọi preventDefault(); `{passive: true}` thông báo handler không gọi preventDefault → browser optimize scroll |

### Event object — thông tin truyền vào handler
```js
element.addEventListener('click', (e) => {
  e.target         // element phát sinh event (leaf/deepest)
  e.currentTarget  // element đang lắng nghe (có thể là parent)
  e.type           // type event: "click", "keydown"...
  e.timeStamp      // timestamp ms khi event xảy ra
  e.clientX/Y      // vị trí chuột trong viewport
  e.pageX/Y        // vị trí chuột trong document
  e.key            // phím nhấn (keydown/keyup)
  e.preventDefault() // chặn hành vi mặc định
  e.stopPropagation() // chặn bubbling/capturing
});
```

### Phân biệt target vs currentTarget — bẫy phổ biến
```html
<ul id="list">
  <li><button>Click</button></li>
</ul>
```
```js
document.getElementById('list').addEventListener('click', (e) => {
  console.log(e.target.tagName);     // "BUTTON" — element click thật
  console.log(e.currentTarget.tagName); // "UL" — element đang listen
});
```

## 📐 Cấu trúc / Cú pháp

### Click handler cơ bản
```js
const btn = document.querySelector("button");
btn.addEventListener("click", (e) => {
  console.log("Target:", e.target.tagName);
  console.log("CurrentTarget:", e.currentTarget.tagName);
  console.log("Mouse x/y:", e.clientX, e.clientY);
});
```

### Once option — tự remove sau lần đầu
```js
document.addEventListener("DOMContentLoaded", () => {
  console.log("Chỉ chạy 1 lần");
}, { once: true });
```

### Passive scroll handler
```js
window.addEventListener("scroll", () => {
  // chỉ đọc, không preventDefault → passive an toàn
  // browser có thể optimize scroll performance
}, { passive: true });
```

### Capture để đóng modal click-outside
```js
document.addEventListener("click", (e) => {
  if (!modal.contains(e.target)) closeModal();
}, { capture: true }); // bắt từ document trước khi bubble xuống button close
```

### Multiple handlers trên cùng element
```js
btn.addEventListener('click', () => console.log('handler 1'));
btn.addEventListener('click', () => console.log('handler 2'));
// Click → in "handler 1" rồi "handler 2" (theo thứ tự đăng ký)
```

## ✅ Điểm mạnh

1. **Nhiều handler trên cùng 1 element, 1 type** — chạy tuần tự theo thứ tự đăng ký, không ghi đè.
2. **`once` tự dọn sau lần đầu** — không cần `removeEventListener` thủ công, tránh leak.
3. **`capture` giúp "đóng modal khi click ngoài"** — bắt sự kiện từ document xuống, trước khi đến button close.
4. **`passive: true` tăng scroll performance** — browser biết handler không gọi preventDefault → optimize touch/scroll.
5. **Access full MouseEvent** — position, key, modifier keys (shift, ctrl, alt) đều có trong event object.
6. **Separation of concerns** — HTML không cần `onclick="..."`, JS quản lý hoàn toàn.
7. **Removable** — lưu reference handler → `removeEventListener` khi không cần.

## ⚠️ Bẫy thường gặp & Hạn chế

1. **`e.target` !== `e.currentTarget` khi event bubble từ con lên cha** — target là element click thật, currentTarget là element đang listen.
2. **`removeEventListener` cần chính xác cùng function reference** — anonymous function không remove được:
   ```js
   btn.addEventListener('click', () => console.log('x'));
   btn.removeEventListener('click', () => console.log('x')); // ❌ KHÔNG work — khác function reference
   ```
3. **`passive: true` không tương thích với `e.preventDefault()`** — nếu handler gọi preventDefault khi passive, browser sẽ ignore và log warning.
4. **Event listener trên detached element** — element bị remove khỏi DOM nhưng listener vẫn tồn tại → memory leak.
5. **Bubble vs Capture order** — capture chạy trước (root→leaf), bubble chạy sau (leaf→root). Hiểu sai thứ tự gây bug.

## 💡 Khi nào dùng — Tình huống thực tến

1. **Button click, form submit, input change** — tương tác cơ bản nhất.
2. **Scroll infinite load, resize responsive** — listen window scroll/resize.
3. **Keyboard shortcut (hotkeys)** — listen keydown trên document.
4. **Modal click-outside to close** — capture phase trên document check `!modal.contains(e.target)`.
5. **Event delegation** — 1 listener ở parent lo cho hàng nghìn child (see bài 12).
6. **Form validation real-time** — input event listener.
7. **Touch gestures** — touchstart, touchmove, touchend cho mobile.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Click handler cơ bản
```js
const btn = document.querySelector("button");
btn.addEventListener("click", (e) => {
  console.log("Target:", e.target.tagName);       // "BUTTON"
  console.log("CurrentTarget:", e.currentTarget.tagName); // "BUTTON"
  console.log("Mouse x/y:", e.clientX, e.clientY);
  console.log("Time:", e.timeStamp);              // ms since page load
});
```

### Ví dụ 2: Once option
```js
document.addEventListener("DOMContentLoaded", () => {
  console.log("Chỉ chạy 1 lần khi DOM ready");
  // Tự động remove sau lần gọi đầu
}, { once: true });
```

### Ví dụ 3: Passive scroll handler
```js
window.addEventListener("scroll", () => {
  // Chỉ đọc scroll position, không preventDefault
  // { passive: true } giúp browser optimize
  const scrolled = window.pageYOffset;
  console.log('Scrolled:', scrolled);
}, { passive: true });
```

### Ví dụ 4: Capture để đóng modal click-outside
```js
const modal = document.querySelector('.modal');

// Capture phase: document → modal
document.addEventListener("click", (e) => {
  if (!modal.contains(e.target)) {
    modal.classList.add('hidden');
  }
}, { capture: true });

// Button close vẫn hoạt động (bubble phase sau capture)
modal.querySelector('.close-btn').addEventListener("click", (e) => {
  e.stopPropagation(); // ngăn bubble lên document
  modal.classList.add('hidden');
});
```

### Ví dụ 5: Keyboard events
```js
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    closeModal();
  }
  if (e.ctrlKey && e.key === 's') {
    e.preventDefault(); // chặn browser save dialog
    saveDocument();
  }
});
```

### Ví dụ 6: Multiple handlers trên cùng element
```js
const btn = document.querySelector('#action-btn');

btn.addEventListener('click', () => console.log('Handler 1: log'));
btn.addEventListener('click', () => console.log('Handler 2: analytics'));
btn.addEventListener('click', () => console.log('Handler 3: update UI'));

// Click → in 3 dòng theo thứ tự
```

### Ví dụ 7: Touch events cho mobile
```js
const slider = document.querySelector('.slider');
let startX = 0;

slider.addEventListener('touchstart', (e) => {
  startX = e.touches[0].clientX;
}, { passive: true });

slider.addEventListener('touchmove', (e) => {
  const diff = e.touches[0].clientX - startX;
  slider.style.transform = `translateX(${diff}px)`;
}, { passive: true });

slider.addEventListener('touchend', () => {
  if (Math.abs(startX - /* end pos */) > 50) {
    console.log('Swipe detected');
  }
});
```

### Ví dụ 8: Event delegation pattern
```js
const list = document.querySelector('#task-list');
list.addEventListener('click', (e) => {
  const li = e.target.closest('li');
  if (li && e.target.classList.contains('delete')) {
    li.remove();
  }
});
// 1 listener ở ul lo được mọi button.delete bên trong — thêm/xóa li tùy ý
```

## 🔬 So sánh với alternatives

| Cách | Multiple handlers? | Removable? | Inline HTML? | Modern? |
|---|---|---|---|---|
| **addEventListener** | ✅ Nhiều | ✅ Có | ❌ Không | ✅ Chuẩn |
| **onclick property** | ❌ Chỉ 1 | ✅ Có | ⚠️ `<button onclick="...">` | ❌ Legacy |
| **inline onclick="..."** | ❌ Chỉ 1 | ❌ Khó | ✅ Có | ❌ Bad practice |

## 📊 Performance & Best Practices

- **Prefer `addEventListener` over `onclick`** — multiple handlers, removable, cleaner.
- **Use `{ passive: true }` cho scroll/touch** — báo cho browser biết handler không preventDefault → optimize.
- **Use `{ once: true }` cho one-time handlers** — tự cleanup, tránh leak.
- **Event delegation khi có nhiều similar elements** — 1 listener thay N listeners.
- **Store handler reference** — cần `removeEventListener` → lưu function vào biến, không dùng anonymous.
- **Avoid listener trên document nếu không cần** — mỗi listener có overhead, giới hạn scope.
- **Remove listeners on unmount** — component cleanup để tránh memory leak.

## 🔗 Liên kết chéo

- Xem thêm: `18_dom-apis/01_dom-basics/01_f8-basic-dom/11_PreventDefault-StopPropagation/` — preventDefault và stopPropagation.
- Xem thêm: `18_dom-apis/01_dom-basics/01_f8-basic-dom/12_EventListener/` — event types chi tiết.
- Xem thêm: `18_dom-apis/03_events/` — event bubbling/capturing deep dive.
- File tham khảo: `app.js`, `index.html` trong folder `10_dom-event/`.
