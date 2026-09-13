# DOM Text (Bài 5)

## Khái niệm
Text nội dung element qua `innerText` (render text, ẩn hidden) và `textContent` (raw text, nhanh hơn). Tạo text node bằng `document.createTextNode("...")`.

## Điểm mạnh
- `textContent` không parse HTML, an toàn hơn khi chèn raw text
- `innerText` nhận CSS visibility → render đúng mắt nhìn

## Khi nào dùng
- Cập nhật nội dung text động; parse HTML an toàn.

## Ví dụ
```js
const h1 = document.querySelector("h1");
h1.innerText = "Xin chào!";
h1.textContent = "Nội dung thô";
```

## 📚 Tham khảo
- `app.js`, `index.html`
