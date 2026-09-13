# preventDefault / stopPropagation (Bài 11)

## Khái niệm
`event.preventDefault()` ngăn hành vi mặc định (ví dụ `<a>` navigate, `<form>` submit reload). `event.stopPropagation()` dừng bubble/capture lên trên.

## Điểm mạnh
- Ngăn reload form mà vẫn lấy data
- Tách event handling giữa parent/child

## Khi nào dùng
- Form xử lý bằng JS; modal click-outside-đóng; nested click handler.

## Ví dụ
```js
form.addEventListener("submit", (e) => {
  e.preventDefault();
  console.log(new FormData(form));
});
child.addEventListener("click", (e) => {
  e.stopPropagation(); // không bubble lên parent
});
```

## 📚 Tham khảo
- `app.js`, `index.html`
