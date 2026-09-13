# Bài 10 — DOM Event: Gắn Sự Kiện

## 🔑 Khái niệm

**Event** là sự kiện xảy ra với DOM: click, scroll, keydown, submit, load... `addEventListener` gắn handler:

```js
element.addEventListener(type, handler, options)
```

| Option | Ý nghĩa |
|---|---|
| `{capture: true}` | Chạy ở phase capture (root → leaf) |
| `{once: true}` | Tự remove sau lần gọi đầu |
| `{passive: true}` | Handler không gọi `preventDefault()` → tăng scroll perf |

**Event object** truyền vào handler:
- `e.target` — element phát sinh event (leaf)
- `e.currentTarget` — element đang lắng nghe (cha)
- `e.type` — type event (click, input…)
- `e.timeStamp` — timestamp ms

## ✅ Điểm mạnh
- Nhiều handler trên cùng 1 element, 1 type — chạy tuần tự
- `once` tự dọn sau lần đầu, không cần `removeEventListener` thủ công
- `capture` giúp "đóng" modal khi click ngoài bằng cách bắt từ document

## ⚠️ Lưu ý
- `e.target` !== `e.currentTarget` khi event bubble từ con lên cha
- `removeEventListener` cần **chính xác cùng function reference** — anonymous function không remove được
- `passive: true` không tương thích với `e.preventDefault()` — nếu gọi sẽ bị console warn

## 💡 Khi nào dùng
- Button click, form submit, input change
- Scroll infinite load, resize responsive
- Keyboard shortcut (hotkeys)

## 🎯 Ví dụ minh họa

### Click handler
```js
const btn = document.querySelector("button");
btn.addEventListener("click", (e) => {
  console.log("Target:", e.target.tagName);
  console.log("CurrentTarget:", e.currentTarget.tagName);
  console.log("Mouse x/y:", e.clientX, e.clientY);
});
```

### once option
```js
document.addEventListener("DOMContentLoaded", () => {
  console.log("Chỉ chạy 1 lần");
}, { once: true });
```

### Passive scroll handler
```js
window.addEventListener("scroll", () => {
  // chỉ đọc, không preventDefault → passive an toàn
}, { passive: true });
```

### Capture để đóng modal click-outside
```js
document.addEventListener("click", (e) => {
  if (!modal.contains(e.target)) closeModal();
}, { capture: true }); // bắt từ document trước khi bubble xuống button close
```

## 📚 Tham khảo & Bài tập
- File: `app.js`, `index.html` trong folder `10_dom-event/`
- Thực hành: toggle modal click-outside đóng modal
- Câu hỏi: `target` vs `currentTarget` khác nhau khi nào?
