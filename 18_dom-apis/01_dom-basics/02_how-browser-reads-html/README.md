# Trình duyệt đọc HTML như thế nào (Rendering Pipeline)

## 🔑 Khái niệm

Khi bạn nhập URL, trình duyệt trải qua chuỗi bước để vẽ trang:

1. **Request**: trình duyệt tạo HTTP request tới server (GET, header...).
2. **Server xử lý**: tìm tài nguyên, xác thực, trả **Response** kèm HTML/CSS/JS.
3. **Download**: trình duyệt tải về các tài nguyên (tuần tự/song song).
4. **HTML Parsing**: đọc từng ký tự HTML → chuyển thành **nodes** (mỗi thẻ là một node với attribute).
5. **DOM Tree Construction**: sắp xếp nodes thành **cây DOM** theo hệ phân cấp cha/con. Cây này đại diện trang web và được **phơi bày cho JS** qua API — "Cái nhận về từ mạng là chuỗi text; trình duyệt parse nó thành mô hình dữ liệu mà máy hiểu".
6. **CSSOM Construction**: các file CSS được tạo thành **CSS Object Model**.
7. **Render Tree**: gộp DOM + CSSOM — chỉ giữ phần tử cần hiển thị.
8. **Layout + Paint**: đặt vị trí từng phần tử rồi vẽ lên màn hình (xem `Painting-Phase*.png`).
9. **JavaScript Execution**: nếu gặp `<script>`, JS chạy và có thể **thay đổi DOM/CSSOM** giữa chừng → render lại.
10. **Load complete**: mọi tài nguyên xong → sự kiện `load`.

Hình vẽ trong thư mục: `DOM.png` (cây DOM), `HTML-Parsing.png` (chuỗi parse → render), `Painting-Phase-1.png` / `Painting-Phase.png` (layout/paint), `node-structure-in-dom.png` (cấu trúc node).

## ✅ Điểm mạnh (khi hiểu pipeline)

- **Biết vì sao sửa DOM lại "đắt"**: mỗi lần JS đổi DOM/CSSOM có thể kích hoạt layout + paint lại.
- **Tối ưu đúng chỗ**: batch thay đổi, hạn chế reflow, dùng `content-visibility`... trở nên có căn cứ.
- **Hiểu thứ tự load**: `<script>` (chặn parsing) vs `defer`/`async` — quyết định đúng khi tối ưu FCP.
- **Nối logic với sự kiện**: vì sao phải đợi `DOMContentLoaded`/`load`.
- **Đọc được CDP/Lighthouse reports**: "render-blocking resources", "layout shift" giờ có ý nghĩa cụ thể.

## ⚠️ Lưu ý / Hạn chế

- **Render Tree ≠ DOM Tree**: Render Tree chỉ chứa phần tử hiển thị; phần `display:none` có trong DOM nhưng không vào render.
- **JS đang parse bị chặn**: `<script>` ở giữa trang làm **dừng HTML parser** — tài nguyên nặng làm chậm trang.
- Cây DOM đầy đủ node text (xuống dòng) — dễ làm bạn đếm sai `childNodes`.
- Canvas/SVG/quy trình "server-side rendering" không đi theo toàn bộ chuỗi này theo cách giống hệt.

## 💡 Khi nào dùng

- **Tối ưu tốc độ tải trang**: sắp xếp nơi đặt `<script>`, nén ảnh, giảm CSS render-blocking.
- **Giải thích hiện tượng "trang nhấp nháy"**: FOUC — do CSSOM tới sau DOM.
- **Debug layout/paint**: dùng Performance panel xem các "Layout/Paint" tasks trong một thao tác.
- **Trước khi bàn đến CSR vs SSR**: nắm pipeline là tiền đề hiểu vì sao SSR thân thiện với SEO.
- Trong phỏng vấn frontend — câu "browser renders HTML như thế nào" cực kỳ kinh điển.

## 🎯 Ví dụ minh họa

```html
<!-- <script> chặn parser: DOM tiếp tục phân tích chỉ khi script đã thực thi -->
<script src="heavy.js"></script>

<!-- defer: tải song song, chạy SAU khi parse xong -> không chặn -->
<script defer src="app.js"></script>

<!-- Sự kiện giúp biết khi nào dùng JS gọn -->
<script>
  document.addEventListener('DOMContentLoaded', () => console.log('DOM sẵn sàng'));
  window.addEventListener('load', () => console.log('Mọi tài nguyên xong'));
</script>
```

## 📚 Tham khảo / Bài tập

- Xem lần lượt các ảnh: `DOM.png`, `HTML-Parsing.png`, `node-structure-in-dom.png`, `Painting-Phase-1.png` → `Painting-Phase.png` để hình dung từ parse tới vẽ.
- Đọc thêm: Critical Rendering Path — <https://web.dev/articles/critical-rendering-path/render-tree-construction> và bài tổng quan dev.to; kiểm tra API thông qua <https://caniuse.com/>.
- Tự làm: mở DevTools → **Performance**, record khi tải một trang, tìm các task "Parse HTML", "Layout", "Paint" — ước lượng thời gian từng pha.
- Tự làm: thử đổi ảnh thành một ảnh rất lớn rồi quan sát "Paint large areas" để hiểu chi phí paint.
- Tự làm: đưa một `<script>` nặng vào giữa `<body>` và cuối `<body>`; so sánh thời điểm `DOMContentLoaded` bắn ra.