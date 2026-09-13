# 00. Giới thiệu về JavaScript

## 🔑 Khái niệm

Đây là **nhóm bài đầu tiên** trong lộ trình học JavaScript (theo [roadmap.sh/javascript](https://roadmap.sh/javascript)). Mục tiêu nhóm này không phải dạy cú pháp, mà giúp bạn trả lời 4 câu hỏi nền tảng trước khi viết dòng code đầu tiên:

1. **JavaScript là gì** — một ngôn ngữ lập trình thông dịch, prototype-based, có first-class function, chạy được trên trình duyệt lẫn máy chủ (Node.js).
2. **Lịch sử ra đời** — sinh tại Netscape năm 1995 bởi Brendan Eich, chuẩn hóa bởi ECMA International thành ECMAScript.
3. **Các phiên bản** — từ ES1 đến ESNext, quyết định bởi quy trình TC39 gồm bốn giai đoạn (stages).
4. **Cách chạy** — chèn JavaScript vào HTML, dùng DevTools, hiểu render-blocking và browser caching.

Nắm chắc kiến thức nhóm này giúp bạn hiểu **tại sao** JavaScript lại có nhiều đặc điểm kỳ lạ (ep `typeof null === "object"`), và vì sao nhiều công cụ lại được xây dựng bằng nó.

## ✅ Điểm mạnh

- Nắm được bối cảnh lịch sử -> hiểu vì sao nhiều tính năng "xấu" của JS tồn tại.
- Hiểu quy trình TC39 -> cập nhật tính năng mới một cách có hệ thống.
- Hiểu render-blocking & browser caching -> viết trang web tải nhanh hơn.
- Có tư duy đúng: JS không phải "Java phiên bản nhỏ", mà là một hệ sinh thái riêng.
- Biết cách chạy thử JS ngay lập tức -> chuyển nhanh từ lý thuyết sang thực hành.

## ⚠️ Lưu ý / Hạn chế

- Quy trình TC39 có **4 giai đoạn**; một tính năng ở stage nhỏ (0–2) chưa nên dùng trong production.
- Không phải tính năng mới nào cũng được mọi trình duyệt hỗ trợ ngay; hãy kiểm tra cẩn thận bằng [caniuse.com](https://caniuse.com) / [kangax compat-table](https://kangax.github.io/compat-table/).
- "ESNext" chỉ là cái tên động cho phiên bản đang phát triển, không phải một bản phát hành cụ thể.
- Các ví dụ về browser caching cần có DevTools thật (cột *Size* trong Network) mới nhìn thấy kết quả rõ ràng nhất.

## 💡 Khi nào dùng

- Bắt đầu học JS và muốn hiểu bản chất trước khi học cú pháp.
- Đọc tài liệu/đặc tả ECMAScript và cần biết thuật ngữ (ES5, ES2015, ESNext, TC39).
- Tối ưu tốc độ tải trang và muốn biết cách đặt thẻ `<script>` đúng chỗ.
- Quyết định dùng tính năng mới cho dự án thực tế và cần đánh giá mức độ hỗ trợ.

## 🎯 Ví dụ minh họa

```html
<!-- index.html — chạy JS ngoài file, không chặn render -->
<body>
  <script src="app.js" defer></script>
</body>
```

```js
// app.js
console.log("Hello, JavaScript!");
console.log(typeof null);          // "object" — lỗi lịch sử, null là primitive!
console.log(1 + "1");              // "11" — ép kiểu ngầm định (coercion)
```

## 📚 Tham khảo / Bài tập

- Nhóm này gồm 4 bài con: `01_what-is-javascript/`, `02_history-of-javascript/`, `03_versions/`, `04_how-to-run-javascript/`.
- Chạy thử `04_how-to-run-javascript/01_browser-caching/app.js` bằng cách mở `index.html` trong cùng thư mục lên trình duyệt, mở Console (F12) để xem `console.log` in ra.
- Tự thử: viết một file `index.html` + `app.js` riêng, thêm thuộc tính `defer` và mở DevTools → Network để quan sát file JS được load từ cache.