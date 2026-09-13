# Class Property (Bài 9)

## Khái niệm
`element.classList` cung cấp API quản lý class: `add`, `remove`, `toggle`, `contains`, `replace`. Nhanh hơn `className += ...` và không ghi đè class cũ.

## Điểm mạnh
- `toggle` có mode force (`classList.toggle("a", true)`)
- `contains` kiểm tra class có tồn tại O(1)
- Không làm rách chuỗi class

## Khi nào dùng
- UI state: active, open, disabled, theme toggle.

## Ví dụ
```js
const btn = document.querySelector("button");
btn.classList.add("active");
btn.classList.toggle("open");
console.log(btn.classList.contains("active"));
```

## 📚 Tham khảo
- `app.js`, `index.html`
