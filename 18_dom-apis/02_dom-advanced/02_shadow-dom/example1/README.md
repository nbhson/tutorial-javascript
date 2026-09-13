# Shadow DOM — Example 1

## Khái niệm
Shadow DOM đóng gói style + markup bên trong một element, tránh ảnh hưởng từ CSS global. Tạo qua `el.attachShadow({ mode: "open"|"closed" })`.

## Điểm mạnh
- Encapsulation hoàn toàn: class/style bên trong không bị trùng với global
- Tái sử dụng component dễ

## Khi nào dùng
- Web Components; widget nhúng bên thứ 3; design system.

## 📚 Tham khảo
- `app.js`, `index.html`, `style.css`
