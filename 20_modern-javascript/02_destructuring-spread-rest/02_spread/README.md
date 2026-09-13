# Spread Syntax (...)

## Khái niệm
Spread `...` copy iterable: `[...arr]`, `{...obj}`. Copy shallow, không deep clone. Kết hợp object, merge array.

## Điểm mạnh
- Clone array/object nhanh
- Merge/overwrite props: `{...defaults, ...override}`
- Function call spread: `Math.max(...arr)`

## Khi nào dùng
- Immutable update Redux; pass array as args; merge options.

## 📚 Tham khảo
- `app.js`, `index.html`
