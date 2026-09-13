# innerHTML / outerHTML (Bài 6)

## Khái niệm
`innerHTML` lấy/thay đổi nội dung HTML bên trong element. `outerHTML` bao gồm cả element đó. `insertAdjacentHTML(position, html)` chèn mà không mất event listener cũ.

## Điểm mạnh
- Gọn, ghi HTML nhanh
- `insertAdjacentHTML` giữ content cũ, không re-render toàn bộ

## Khi nào dùng
- Render danh sách HTML nhanh. **Tránh** với user input chưa sanitize (XSS).

## Ví dụ
```js
const div = document.querySelector(".content");
div.innerHTML = "<p>Mới</p>";
div.insertAdjacentHTML("beforeend", "<span>thêm</span>");
```

## 📚 Tham khảo
- `app.js`, `index.html`
