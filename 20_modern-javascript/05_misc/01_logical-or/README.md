# Logical OR / AND / Nullish

## Khái niệm
`||` trả truthy đầu tiên; `&&` trả falsy đầu tiên; `??` trả non-nullish đầu tiên. Short-circuit evaluation.

## Điểm mạnh
- Gọn default params: `name ?? "Anonymous"`
- Conditional render: `isAdmin && <Admin/>`

## Khi nào dùng
- Default value; conditional rendering; early return.

## 📚 Tham khảo
- `app.js`, `index.html`
