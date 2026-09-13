# 00. Giới thiệu về JavaScript — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

Nhóm **00_introduction** là cánh cửa đầu tiên bạn bước vào hành trình học JavaScript. Mục tiêu của nó không phải dạy cú pháp — mà là trả lời **4 câu hỏi nền tảng** giúp bạn có tư duy đúng về ngôn ngữ này trước khi viết dòng code đầu tiên:

1. **JavaScript là gì?** — một ngôn ngữ lập trình thông dịch cấp cao, prototype-based, hỗ trợ first-class functions, chạy được cả trên trình duyệt lẫn máy chủ (Node.js), và là một trong ba công nghệ cốt lõi của World Wide Web (cùng HTML và CSS).
2. **Lịch sử ra đời** — được tạo ra vội vàng trong khoảng 10 ngày tại Netscape năm 1995 bởi Brendan Eich, sau đó chuẩn hóa thành ECMAScript. Hiểu lịch sử giúp bạn chấp nhận được nhiều đặc điểm "kỳ lạ" của JS (ví dụ `typeof null === "object"`).
3. **Các phiên bản (ES1 → ESNext)** — quy trình TC39 gồm 4 giai đoạn (stage 0–4) quyết định tính năng nào đã "chín muồi" để dùng trong production. Từ ES6/ES2015 trở đi, mỗi năm có một bản phát hành mới.
4. **Cách chạy JavaScript** — ba cách chèn script vào HTML (inline head, inline cuối body, file ngoài với `defer`/`async`), cùng khái niệm render-blocking và browser caching.

Khi nắm chắc nhóm này, bạn sẽ hiểu **tại sao** JavaScript lại có những hành vi đôi khi phản trực giác, và vì sao hệ sinh thái khổng lồ xung quanh nó lại phát triển mạnh mẽ như vậy.

## 📐 Cấu trúc nhóm

```
00_introduction/
├── README.md                     ← tổng quan nhóm
├── 01_what-is-javascript/
│   ├── README.md                 ← JavaScript là gì?
│   ├── 01_first-class-function/  ← hàm là giá trị hạng nhất
│   └── 02_prototype-based-programming/ ← kế thừa qua prototype
├── 02_history-of-javascript/     ← lịch sử từ 1995 đến nay
├── 03_versions/                  ← ES1 → ESNext, quy trình TC39
└── 04_how-to-run-javascript/
    ├── README.md                 ← cách chèn script vào HTML
    └── 01_browser-caching/       ← cache và hiệu suất
```

## ✅ Điểm mạnh — Tại sao nên học nhóm này

| # | Lợi ích | Khi nào quan trọng |
|---|---------|-------------------|
| 1 | Nắm bối cảnh lịch sử → hiểu vì sao JS có nhiều "bẫy" tồn tại | Đọc code cũ, debug lỗi kỳ lạ |
| 2 | Biết quy trình TC39 → cập nhật tính năng mới có hệ thống | Ra quyết định dùng tính năng ES mới |
| 3 | Hiểu render-blocking & browser caching → trang tải nhanh hơn | Tối ưu UX, SEO cho website |
| 4 | Có tư duy đúng: JS không phải "Java phiên bản nhỏ" | Tránh hiểu lầm từ tên gọi |
| 5 | Biết cách chạy thử JS ngay lập tức | Chuyển nhanh từ lý thuyết sang thực hành |
| 6 | Nhận diện được các thuật ngữ chuyên ngành (ES5, ES2015, TC39) | Đọc tài liệu kỹ thuật, phỏng vấn |
| 7 | Hiểu mối quan hệ ECMAScript ↔ JavaScript | Tránh nhầm lẫn giữa chuẩn và thực thi |

## ⚠️ Bẫy thường gặp & Hạn chế

| # | Bẫy | Ví dụ | Cách tránh |
|---|-----|-------|-----------|
| 1 | **JavaScript ≠ Java** — chỉ trùng tên vì marketing | `typeof null === "object"` là bug lịch sử | Hiểu rõ lịch sử, tránh so sánh sai |
| 2 | **Tính năng stage 0–2 chưa ổn định** | Dùng `Array.groupBy` (Stage 3) có thể đổi cú pháp | Kiểm tra caniuse trước khi dùng |
| 3 | **"ESNext" không phải bản release cụ thể** | Chỉ là tên gọi động | Tránh nói "tôi dùng ESNext" — gọi chính xác version |
| 4 | **Script inline trong head chặn render** | Đặt `<script src="app.js">` ở head làm trang trắng | Dùng `defer` hoặc đặt script cuối body |
| 5 | **Inline script không được cache** | Mỗi lần reload phải tải lại nội dung | Tách ra file `.js` riêng |
| 6 | **`typeof null === "object"`** — bug lịch sử | Đã tồn tại từ ES1 | Dùng `=== null` kiểm tra null |
| 7 | **`async` khác `defer` — async không giữ thứ tự** | Hai script async chạy xen kẽ | Dùng `defer` khi cần giữ thứ tự |

## 💡 Khi nào dùng — Tình huống thực tế

1. **Bắt đầu học JS** và muốn hiểu bản chất trước khi học cú pháp — giúp tránh hoang mang khi gặp hành vi kỳ lạ.
2. **Đọc tài liệu / đặc tả ECMAScript** và cần phân biệt thuật ngữ (ES5, ES2015, ESNext, TC39).
3. **Tối ưu tốc độ tải trang** — biết cách đặt thẻ `<script>` đúng chỗ, dùng `defer` thay vì `async` khi cần giữ thứ tự.
4. **Quyết định dùng tính năng mới** — kiểm tra stage của TC39 và mức hỗ trợ trên caniuse.com/kangax trước khi đưa vào production.
5. **Giải thích cho đồng nghiệp** vì sao một bug kỳ lạ lại xảy ra (ví dụ: `typeof null`).
6. **Chuẩn bị phỏng vấn** — câu hỏi "Nêu lịch sử và các phiên bản JavaScript" xuất hiện khá thường xuyên.
7. **Hiệu chỉnh tư duy** — khi bạn từng học Java rồi chuyển sang JS, nhóm này giúp bạn xoá bỏ định kiến sai lệch.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Chạy JavaScript đầu tiên (Hello World)

```js
// app.js — file JS đơn giản nhất
console.log("Hello, JavaScript!");   // In ra console của trình duyệt/Node
console.log(typeof null);            // "object" — bug lịch sử, null là primitive!
console.log(1 + "1");               // "11" — ép kiểu ngầm định (coercion), học ở 02_data-types
```

### Ví dụ 2: Ba cách chèn JS vào HTML

```html
<!-- Cách 1: Inline trong <head> — render-blocking -->
<head>
  <script>
    console.log("Script này chạy trước khi DOM sẵn sàng");
    // document.getElementById('main') → null vì DOM chưa parse!
  </script>
</head>

<!-- Cách 2: Inline cuối <body> — vẫn chặn render tại điểm chèn -->
<body>
  <p>Nội dung trang web</p>
  <script>
    console.log("DOM đã sẵn sàng, nhưng script lớn vẫn gây gián đoạn");
  </script>
</body>

<!-- Cách 3: File ngoài + defer — KHÔNG chặn render, chạy sau khi parse xong -->
<head>
  <script src="app.js" defer></script>
</head>
<!-- Trình duyệt tải app.js song song, chỉ chạy sau khi HTML parse xong -->
```

### Ví dụ 3: Phân biệt var / let / const (preview từ nhóm 01)

```js
// var: function-scoped, hoisted về undefined
var old = "ES5 style";
console.log(typeof old); // "string"

// let / const: block-scoped, có TDZ
let modern = "ES6+";
const CONSTANT = 42;
// CONSTANT = 10; // TypeError: Assignment to constant variable
```

### Ví dụ 4: Prototype chain đơn giản

```js
// Mỗi object đều kế thừa từ Object.prototype
const obj = {};
console.log(obj.toString);        // function toString() { [native code] }
console.log(obj.hasOwnProperty);  // function hasOwnProperty() { ... }
// Những method này không định nghĩa trên obj — ta lấy từ prototype chain
```

### Ví dụ 5: Browser caching — quan sát trong DevTools

```html
<!-- index.html — mở DevTools → Network tab, reload để quan sát cache behavior -->
<!DOCTYPE html>
<html>
<head><title>Browser Caching Demo</title></head>
<body>
  <h1>Hệ thống cache</h1>
  <script src="app.js" defer></script>
</body>
</html>
```

```js
// app.js — file JS riêng biệt
console.log("APP");
console.log("APP 2");
console.log("APP 3");
// Lần đầu: Network tab hiện app.js với size ~100B, từ "localhost"
// Lần sau: Network tab hiện app.js với size "(memory cache)" hoặc "(disk cache)"
```

### Ví dụ 6: TC39 stages — ví dụ về optional chaining

```js
// Optional chaining (?.) — đạt Stage 4 (ES2020)
// Trước đây phải viết dài dòng:
const city = user && user.address && user.address.city;

// Ngày nay:
const cityModern = user?.address?.city;
// Tương đương với việc kiểm tra từng level, tránh ReferenceError nếu null/undefined
```

## 🔬 So sánh với alternatives

| Phương án | Ưu điểm | Nhược điểm |
|-----------|---------|------------|
| **Học qua nhóm 00 (tutorial này)** | Có lộ trình rõ ràng, đi từ khái niệm → thực hành | Cần đọc nhiều bài con |
| **Đọc trực tiếp MDN docs** | Thông tin chính xác, luôn cập nhật | Thiếu ngữ cảnh, dễ choáng ngợp |
| **Học qua lộ trình roadmap.sh** | Có mục tiêu dài hạn, kết nối các topic | Chưa có giải thích chi tiết bằng tiếng Việt |
| **Xem video YouTube** | Trực quan, dễ theo dõi | Thiếu tham chiếu, dễ bỏ lỡ chi tiết quan trọng |
| **Dự án thực tế ngay** | Học nhanh qua làm | Dễ bỏ sót kiến thức nền tảng, code thiếu cấu trúc |

## 📊 Performance & Best Practices

- **Đặt `<script>` ở cuối `<body>`** hoặc dùng `defer` — tránh render-blocking, cải thiện Time to Interactive (TTI).
- **Tách JS ra file riêng** — tận dụng được browser caching, giảm HTML bundle size.
- **Dùng `async` cho script độc lập** (analytics, quảng cáo) — không phụ thuộc thứ tự thực thi.
- **Dùng `defer` cho script phụ thuộc DOM** — chạy sau khi HTML parse xong, giữ nguyên thứ tự.
- **Kiểm tra compatibility** — dùng [caniuse.com](https://caniuse.com) hoặc [kangax.github.io/compat-table](https://kangax.github.io/compat-table/) trước khi dùng tính năng ES mới.
- **Không dùng `var` trong code mới** — block scope của `let`/`const` an toàn hơn hẳn.

## 🔗 Liên kết chéo

- Xem thêm: `01_what-is-javascript/` — JavaScript là gì?
- Xem thêm: `01_what-is-javascript/01_first-class-function/` — vì sao hàm là giá trị hạng nhất
- Xem thêm: `01_what-is-javascript/02_prototype-based-programming/` — cơ chế prototype chain
- Xem thêm: `02_history-of-javascript/` — lịch sử từ 1995 đến nay
- Xem thêm: `03_versions/` — ES1 đến ESNext, quy trình TC39
- Xem thêm: `04_how-to-run-javascript/` — cách chèn script vào HTML
- Xem thêm: `04_how-to-run-javascript/01_browser-caching/` — browser cache hoạt động ra sao
- Xem thêm: `01_variables/01_declarations/` — var vs let vs const (preview)
- Xem thêm: `02_data-types/01_primitive-types/` — typeof null === "object" (giải thích)
