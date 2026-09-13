# EventListener thông dụng (Bài 12)

## Khái niệm
Các listener phổ biến: `click`, `dblclick`, `mouseenter/mouseleave`, `keydown/keyup`, `submit`, `input`, `change`, `scroll`, `resize`. Có thể dùng `once`, `passive`, `capture` options.

## Điểm mạnh
- `once` tự gỡ sau 1 lần — tiện cho tooltip, modal open
- `passive=true` tăng scroll performance (mobile)
- `capture` bắt sự kiện từ root xuống leaf

## Khi nào dùng
- Scroll list infinite; keyboard shortcut; button submit; hover menu.

## Ví dụ
```js
window.addEventListener("scroll", () => {}, { passive: true });
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") closeModal();
}, { once: true });
```

## 📚 Tham khảo
- `app.js`, `index.html`
