# JavaScript là gì? — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

**JavaScript** (viết tắt **JS**) là một ngôn ngữ lập trình **thông dịch cấp cao** (high-level, compiled JIT), và là một trong ba công nghệ cốt lõi của **World Wide Web**, bên cạnh **HTML** (cấu trúc) và **CSS** (trình bày). Nếu ví trang web như một con người, thì HTML là bộ xương, CSS là quần áo, và JavaScript là **bộ não** — thứ giúp trang web "suy nghĩ", phản ứng, và tương tác với người dùng.

Bạn gặp JavaScript mọi nơi: thanh trượt tìm kiếm tự động hoàn thành, menu đổ xuống khi hover, xác thực form ngay khi gõ, bản đồ tương tác, game trên trình duyệt, ứng dụng máy chủ, app desktop, app di động… Tất cả đều có thể được xây dựng bằng JavaScript.

### Các tính chất quyết định của JavaScript

1. **First-class functions**: hàm được xử lý như bất kỳ giá trị nào — gán cho biến, truyền vào hàm khác, trả về từ hàm. Đây là nền tảng của callback, higher-order function, và closure. Xem thêm: `00_introduction/01_what-is-javascript/01_first-class-function`.

2. **Prototype-based OOP**: không có `class` nguyên thủy (trước ES6), đối tượng kế thừa từ đối tượng khác qua **chuỗi prototype**. ES6 `class` thực chất là syntactic sugar trên prototype. Xem thêm: `00_introduction/01_what-is-javascript/02_prototype-based-programming`.

3. **Garbage-collected**: JavaScript engine tự động quản lý bộ nhớ — bạn không cần `free()` hay `delete` thủ công như C/C++. Cơ chế thu gom rác (GC) được mô tả chi tiết ở `17_memory-management/`.

4. **Dynamic typing**: biến không khai báo kiểu; kiểu dữ liệu được xác định tại runtime dựa trên giá trị gán. Một biến có thể chứa số lúc đầu, sau đó là chuỗi. Học kỹ ở `01_variables/` và `02_data-types/`.

5. **Đa mô hình lập trình**: JS hỗ trợ imperative (mệnh lệnh), object-oriented (hướng đối tượng), và functional (hàm) — thậm chí kết hợp nhiều phong cách trong cùng một file.

### Tại sao JavaScript chạy được ở đâu cũng được?

JavaScript engine là trái tim của mọi môi trường chạy JS:

| Engine | Trình duyệt / Môi trường |
|--------|-------------------------|
| **V8** | Chrome, Edge, Node.js, Deno |
| **SpiderMonkey** | Firefox |
| **JavaScriptCore (Nitro)** | Safari, WebKit |
| **JSCore** | React Native (iOS) |

Tất cả các engine này đều thực thi cùng một **đặc tả ECMAScript** — chuẩn do TC39 soạn thảo — nên code JS chạy tương đối đồng nhất giữa các môi trường (dù có chênh lệch nhỏ về API thuộc môi trường).

## 📐 Cấu trúc / Cú pháp

JavaScript không yêu cầu khai báo kiểu, không cần main(), không cần biên dịch. File `.js` được nhúng vào HTML hoặc chạy trực tiếp bởi Node.js:

```html
<!-- Cách nhúng JS vào trang HTML -->
<!DOCTYPE html>
<html>
<head>
  <title>JS Demo</title>
</head>
<body>
  <h1 id="title">Xin chào</h1>
  <!-- defer: tải song song, chạy sau khi HTML parse xong -->
  <script src="app.js" defer></script>
</body>
</html>
```

```js
// app.js — syntax cơ bản nhất
const greeting = "Hello, JavaScript!";
console.log(greeting); // In ra console

// Arrow function (ES6)
const add = (a, b) => a + b;
console.log(add(2, 3)); // 5

// Object literal
const user = { name: "Sơn", age: 23 };
console.log(user.name); // "Sơn"
```

## ✅ Điểm mạnh — Tại sao nên dùng

| # | Điểm mạnh | Lý do |
|---|-----------|-------|
| 1 | **Phổ biến mọi nơi** | Browser, server, desktop, mobile, IoT — học một lần, dùng đa nền tảng |
| 2 | **Hệ sinh thái khổng lồ** | npm với hơn 2 triệu gói thư viện; React, Vue, Angular, Node.js, Electron |
| 3 | **Bắt đầu nhanh** | Không cần cài đặt phức tạp; mở DevTools (F12) là viết được JS ngay |
| 4 | **Đa mô hình** | Imperative, OOP (prototype/class), functional — chọn cách phù hợp bài toán |
| 5 | **Không cần type khi khởi tạo** | Rapid prototyping nhanh; TypeScript bổ sung khi dự án lớn |
| 6 | **Non-blocking I/O** | Event loop giúp xử lý nhiều request đồng thời (Node.js) — lý tưởng cho API |
| 7 | **Cross-platform UI** | Electron cho desktop, React Native cho di động — cùng một ngôn ngữ |
| 8 | **Cộng đồng đông đảo** | Hàng triệu developer, tài liệu dồi dào,Stack Overflow hoạt động mạnh |

## ⚠️ Bẫy thường gặp & Hạn chế

| # | Bẫy | Ví dụ code |
|---|-----|-----------|
| 1 | **Dynamic typing** gây lỗi runtime | `let x = 5; x = "hello";` — không báo lỗi, nhưng `x + 1` sẽ thành `"hello1"` |
| 2 | **Ép kiểu ngầm định** (`coercion`) | `1 + "1"` = `"11"`; `null + 1` = `1`; `"5" - 3` = `2` |
| 3 | **`typeof null === "object"`** | Bug lịch sử từ ES1; luôn dùng `=== null` thay vì `typeof` để kiểm tra null |
| 4 | **`this` binding thay đổi** | `(button.onclick = handler)()` → `this` trỏ `window` thay vì button |
| 5 | **Prototype chain hiểu sai** | Sửa `Array.prototype.push` ảnh hưởng đến TẤT CẢ mảng — gọi là monkey-patching |
| 6 | **`var` function-scoped, không block-scoped** | `for(var i=0;i<3;i++){}; console.log(i)` → `i` còn tồn tại sau vòng lặp |
| 7 | **ReferenceError trong TDZ** | `console.log(x); let x = 1;` → lỗi, không phải `undefined` như `var` |
| 8 | **`NaN !== NaN`** | NaN không bằng chính nó; dùng `Number.isNaN()` để kiểm tra đúng |
| 9 | **`[] + []` cho kết quả kỳ lạ** | `[] + []` → `""`, `{}` + `[]` → `0` — do automatic type coercion |
| 10 | **Arrow function không có `this` riêng** | `const obj = { fn: () => this }` → `this` trỏ scope ngoài, không phải `obj` |

## 💡 Khi nào dùng — Tình huống thực tế

1. **Xây dựng tương tác website** — xác thực form, cập nhật nội dung không reload, animation, drag-and-drop.
2. **Viết API / máy chủ** — Node.js + Express/NestJS cho REST API, real-time (Socket.io).
3. **Tạo app desktop** — Electron (VS Code, Slack, Discord đều dùng Electron).
4. **Tạo app di động** — React Native, Ionic, Capacitor — cùng codebase JavaScript.
5. **Xử lý dữ liệu client-side** — filter/sort/paginate bảng dữ liệu lớn mà không gọi server.
6. **Web scraping / automation** — Puppeteer, Playwright dùng JS điều khiển browser.
7. **IoT / robotics** — Johnny-Five, JavaScriptCore nhúng vào thiết bị phần cứng.
8. **Phân tích dữ liệu / ML** — TensorFlow.js chạy model AI trực tiếp trên trình duyệt.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: First-class function — hàm là giá trị

```js
// Gán hàm cho biến
const chao = (ten) => `Xin chào, ${ten}!`;
console.log(chao("Nam"));            // "Xin chào, Nam!"

// Truyền hàm làm đối số (callback)
function xuLy(x, fn) { return fn(x); }
console.log(xuLy(5, chao));          // "Xin chào, 5!"
```

### Ví dụ 2: Dynamic typing — đổi kiểu linh hoạt

```js
let bien = "chuỗi";
console.log(typeof bien);            // "string"
bien = 42;                           // giờ là number
console.log(typeof bien);            // "number"
console.log(bien + 1);              // 43 (number + number)
bien = "42";
console.log(bien + 1);              // "421" (string concat)
```

### Ví dụ 3: Prototype inheritance — kế thừa qua prototype

```js
// Tạo object gốc (prototype)
const dongVat = { tiengKeu: "..." };

// Tạo object mới kế thừa từ dongVat
const conCho = Object.create(dongVat);
conCho.ten = "Buddy";

console.log(conCho.ten);             // "Buddy" — thuộc tính riêng
console.log(conCho.tiengKeu);        // "..." — kế thừa từ prototype
console.log(Object.getPrototypeOf(conCho) === dongVat); // true
```

### Ví dụ 4: Đa mô hình — imperative + functional

```js
// Imperative: dùng vòng lặp
let tong = 0;
const so = [1, 2, 3, 4, 5];
for (let i = 0; i < so.length; i++) {
  tong += so[i];
}
console.log(tong);                   // 15

// Functional: dùng reduce
const tongFunctional = so.reduce((t, n) => t + n, 0);
console.log(tongFunctional);         // 15 — cùng kết quả, code ngắn hơn
```

### Ví dụ 5: Kết hợp nhiều tính chất

```js
// First-class function + prototype + dynamic typing
const nguoi = {
  ten: "Sơn",
  chao: function () {
    return `Xin chào, tôi là ${this.ten}`;
  },
};

// Thêm method mới vào prototype (động)
Object.setPrototypeOf(nguoi, {
  toiTen() {
    return this.ten.toUpperCase();
  },
});

console.log(nguoi.chao());           // "Xin chào, tôi là Sơn"
console.log(nguoi.toiTen());         // "SƠN"
```

## 🔬 So sánh với alternatives

| Ngôn ngữ | Điểm mạnh hơn JS | Điểm yếu so với JS |
|----------|-----------------|-------------------|
| **TypeScript** | Static typing, tooling mạnh | Phải transpile, học curve cao hơn |
| **Python** | Cú pháp sạch, Data Science mạnh | Không chạy native trên browser |
| **Java/C#** | Type-safe, enterprise framework | Chạy trên JVM/.NET, không phải web-native |
| **C++** | Hiệu suất cực cao, control bộ nhớ | Lập trình phức tạp, dễ leak memory |
| **Rust** | Memory-safe, async mạnh | Learning curve rất dốc |

## 📊 Performance & Best Practices

- **Luôn dùng `const` mặc định**, chuyển sang `let` khi cần gán lại — giảm bug vô tình ghi đè.
- **Tránh `var`** trong code hiện đại — block scope của `let`/`const` an toàn hơn nhiều.
- **Kiểm tra kiểu tường minh** — dùng `typeof`, `Array.isArray()`, `instanceof` khi cần.
- **Tách JS ra file riêng** — tận dụng browser caching, code sạch sẽ hơn inline.
- **Dùng ESLint** — phát hiện lỗi tiềm ẩn (undefined variable, unused variable, strict mode).
- **Cân nhắc TypeScript** khi dự án lớn — static typing giúp phát hiện lỗi trước khi chạy.

## 🔗 Liên kết chéo

- Xem thêm: `00_introduction/02_history-of-javascript/` — lịch sử ra đời của JavaScript
- Xem thêm: `00_introduction/03_versions/` — ES5, ES6, ESNext là gì
- Xem thêm: `00_introduction/01_what-is-javascript/01_first-class-function/` — first-class function chi tiết
- Xem thêm: `00_introduction/01_what-is-javascript/02_prototype-based-programming/` — prototype chain hoạt động ra sao
- Xem thêm: `01_variables/` — biến let/const/var, hoisting, scope
- Xem thêm: `02_data-types/` — 8 kiểu dữ liệu, primitive vs reference
- Xem thêm: `02_data-types/03_type-casting-and-coercion/` — ép kiểu ngầm định và tường minh
- Xem thêm: `17_memory-management/` — garbage collection và memory leaks
- Tài liệu: [MDN — JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript), [javascript.info](https://javascript.info/intro)
