# Virtual DOM (React style)

## Khái niệm
Virtual DOM là bản sao DOM trong JS memory. Khi state thay đổi → tạo new VDOM → so sánh diff (reconciliation) → patch thay đổi nhỏ lên real DOM.

## Điểm mạnh
- Batch updates → giảm reflow/repaint
- Cross-browser abstraction
- Cách nhanh nhất update UI phức tạp

## Khi nào dùng
- React, Vue, Inferno — mọi SPA hiện đại đều dùng VDOM hoặc signal-based reactive.

## 📚 Tham khảo
- `app.js`, `helper.js`, `index.html`, `style.css`
