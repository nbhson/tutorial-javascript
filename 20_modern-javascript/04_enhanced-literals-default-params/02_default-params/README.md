# Default Parameters

## Khái niệm
`function foo(a = 1, b = 2) {}`. Default áp dụng khi argument là `undefined`. Có expression `a = a || 1` hoặc `a = a ?? 1`.

## Điểm mạnh
- Giảm `if (x === undefined) x = default`
- Hỗ trợ lazy default `a = computeDefault()`

## Khi nào dùng
- API wrapper; component props; config merger.

## 📚 Tham khảo
- `app.js`, `index.html`
