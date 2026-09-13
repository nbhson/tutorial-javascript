# Built-in Objects

## 🔑 Khái niệm

JavaScript đi kèm với hàng tá **built-in objects** (đối tượng có sẵn) được engine tích hợp sẵn — bạn không cần viết lại. Chung rất nhiều nhóm:

**Các đối tượng chính:**

| Đối tượng | Ghi chú |
|---|---|
| `Object`, `Function`, `Array` | Nền tảng mọi đối tượng |
| `String`, `Number`, `Boolean` | Wrapper cho primitive (nhưng nên dùng hàm `String()` hơn `new`) |
| `Math` | Hỗ trợ số học (hàm, hằng số) — **không** phải object instance |
| `Date` | Quản lý thời gian |
| `RegExp` | Biểu thức chính quy |
| `Error`, `TypeError`, `ReferenceError`... | Hệ thống báo lỗi |
| `JSON` | Parse/unescape object ↔ chuỗi |
| `Map`, `Set`, `WeakMap`, `WeakSet` | Collection nâng cao (xem nhóm `03_data-structures`) |
| `Promise`, `Symbol`, `BigInt`, `Proxy`... | Các built-in mới hơn |

> **`Math` là duy nhất trong nhóm này:** nó không có constructor (`new Math()` sẽ lỗi), chỉ là "namespace" chứa hàm/hằng số. Tất cả các đối tượng còn lại đều có constructor function.

Nhóm `04_builtin-objects/` gồm 4 bài nhỏ (mỗi bài 1 file `app.js`) tập trung vào 4 đối tượng quan trọng nhất: Math, Date, RegExp, Error.

## ✅ Điểm mạnh

- Tái sử dụng code chuẩn: không tự viết `sin()`, `random()`, `parseISO()` — đúng nghĩa đã được tối ưu và kiểm thử.
- `Math` cho phép tính toán số học mạnh mẽ chỉ trong một dòng.
- `Date` xử lý múi giờ, formatting, difference đầy đủ các tính năng.
- `RegExp` và `Error` được tối ưu nguyên bản, chạy nhanh hơn so với thư viện bên ngoài.
- Hiểu built-in → đọc được bất kỳ đoạn code JS hiện đại nào.

## ⚠️ Lưu ý / Hạn chế

- `new String(1)` tạo object, không phải primitive → `typeof` trả `"object"` (luôn dùng `String(1)`).
- `Date` Constructor hơi lệch: `new Date(2023, 1, 1)` (tháng tính từ 0!) — dễ sai 1 tháng.
- `RegExp` có slashes `/pattern/flags` gây nhầm lẫn nếu chưa quen — viết sai cũng không lỗi ngay.
- `Math` trên diện rộng có thể phức tạp; đủ dùng chỉ cần nhớ `PI`, `random()`, `round()`, `min()`, `max()`, `floor()`, `ceil()`.

## 💡 Khi nào dùng

- Tính toán, làm tròn, giá trị tuyệt đối, random trong khoảng → `Math`.
- Hiển thị/lưu lại thời gian → `Date`.
- Validate email, tìm text mẫu, replace theo pattern → `RegExp`.
- Bắt và xử lý lỗi runtime → `try/catch` + `Error` (các loại `TypeError`, `ReferenceError`...).
- Chuyển object ↔ JSON → `JSON.parse()` / `JSON.stringify()`.

## 🎯 Ví dụ minh họa

```js
// Math
console.log(Math.PI, Math.floor(1.9), Math.random());
// 3.14159... 1 <số ngẫu nhiên 0-1>

// Date
const d = new Date();
console.log(d.toISOString(), d.getTime());
// "2025-08-30T..."  1725012345678

// RegExp
const re = /ab+c/g;
console.log(re.test("abbbc"), "abc".match(re));
// true null

// Error
try { throw new TypeError("bad"); }
catch (e) { console.log(e.name, e.message); }
// TypeError bad
```

## 📚 Tham khảo / Bài tập

- Học lần lượt 4 bài con: `01_math/`, `02_date/`, `03_regexp/`, `04_error/` — mỗi bài có `app.js` chạy được ngay (`node app.js` hoặc mở `index.html`).
- Tự thử: 1) dùng `Math.random()` + `Math.floor()` trong khoảng `[1, 100]`; 2) tạo `Date` từ chuỗi `new Date("2024-01-01")` và in ra `toLocaleDateString("vi-VN")`; 3) regex kiểm tra số điện thoại VN; 4) try/catch với `JSON.parse("tệ")` và đọc lỗi.
- Tài liệu: [MDN — Built-in objects](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects).