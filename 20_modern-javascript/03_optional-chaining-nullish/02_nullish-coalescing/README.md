# Nullish Coalescing (`??`)

## Khái niệm
`a ?? b` trả `b` nếu `a` là `null` hoặc `undefined` (khác `||` vì `||` bỏ cả `""`, `0`, `false`).

## Điểm mạnh
- Default value chỉ khi null/undefined
- Giữ nguyên `0`, `""`, `false` hợp lệ

## Khi nào dùng
- Default config; fallback value cho form input.

## 📚 Tham khảo
- `app.js`, `index.html`
