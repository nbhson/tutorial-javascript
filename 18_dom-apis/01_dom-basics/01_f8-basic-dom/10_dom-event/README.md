# DOM Event (Bài 10)

## Khái niệm
Sự kiện: click, input, submit, keydown, scroll... Đăng ký qua `addEventListener(type, handler, options)`. `event.target` là element phát sinh, `event.currentTarget` là element gắn listener.

## Điểm mạnh
- Nhiều listener cùng loại trên 1 element
- `removeEventListener` hủy listener
- `options.once` tự hủy sau lần đầu

## Khi nào dùng
- Tương tác user; form submit; button click; input real-time.

## Ví dụ
```js
const btn = document.querySelector("button");
btn.addEventListener("click", (e) => {
  console.log(e.target, e.currentTarget);
});
```

## 📚 Tham khảo
- `app.js`, `index.html`
