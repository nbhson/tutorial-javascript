# Optional Chaining (`?.`)

## Khái niệm
`obj?.prop`, `arr?.[i]`, `fn?.()`. Nếu `obj` null/undefined → trả `undefined` thay vì `TypeError: Cannot read property`.

## Điểm mạnh
- Ngăn lỗi runtime khi data thiếu
- Gọn hơn `obj && obj.prop`

## Khi nào dùng
- API response có thể thiếu field; optional config; deep property access.

## 📚 Tham khảo
- `app.js`, `index.html`
