# Đối tượng arguments (arguments object)

## 🔑 Khái niệm

Bên trong **hàm thường** (không phải arrow), JavaScript tự tạo sẵn một biến đặc biệt tên là **`arguments`** — chứa tất cả tham đối (arguments) bạn truyền vào khi gọi hàm, dù khai báo bao nhiêu tham số.

```js
function f() {
  console.log(arguments);          // Arguments(3) [1, 2, 3]
  console.log(Array.from(arguments)); // [1, 2, 3] — thành mảng thật
  console.log(arguments.length);   // 3
}
f(1, 2, 3);
```

Đặc điểm quan trọng:

- **Array-like**: có `length` và truy cập bằng index `arguments[0]`, nhưng **không phải mảng thật** — không có `map`, `filter`, `push`...
- Chỉ tồn tại trong **function thường**, **không có trong arrow function** (arrow kế thừa `arguments` của phạm vi bên ngoài nếu có).
- Muốn dùng như mảng → `Array.from(arguments)` hoặc `[...arguments]`.
- **Cách hiện đại hơn**: dùng rest parameter `(...args)` — nhận về **mảng thật** và hoạt động cả trong arrow.

File `app.js` demo cả hai cách:

```js
function f() {
  console.log(arguments, Array.from(arguments));
  console.log(arguments.length);
}
f(1, 2, 3); // Arguments [1,2,3] / [1,2,3] / 3

const arrow = (...args) => console.log(args);
arrow(1, 2); // [1, 2] — rest thay thế arguments trong arrow
```

## ✅ Điểm mạnh

- Hàm thường nhận được **vô hạn tham số** qua `arguments` mà không cần khai báo rest.
- `arguments.length` hữu ích để kiểm tra số lượng đối số thực tế.
- Hỗ trợ tương thích với code cũ (các thư viện viết trước ES6 dùng khá nhiều).
- `arguments[0]` truy cập nhanh như mảng.
- Minh họa rõ khái niệm "array-like" — kiến thức gặp lại ở `NodeList`, `HTMLCollection`.

## ⚠️ Lưu ý / Hạn chế

- Không có các phương thức mảng: gọi `arguments.map(...)` sẽ lỗi — phải chuyển bằng `Array.from`/`...spread` trước.
- **Không tồn tại trong arrow function** — dùng `...args` thay thế.
- `arguments` bị liên kết với tham số khi không dùng strict mode (thay đổi tham số ảnh hưởng `arguments` và ngược lại) — dễ gây bug.
- Khái niệm cũ, khó đọc hơn so với rest parameter hiện đại.

## 💡 Khi nào dùng

- Khi viết hàm nhận số lượng đối số không xác định (accumulator, function đếm tổng).
- Trong code cũ / thư viện legacy đang phải bảo trì.
- Khi cần đếm hoặc truy xuất linh hoạt đối số theo index.
- Học phân biệt "array-like" để xử lý các đối tượng DOM dạng list.

## 🎯 Ví dụ minh họa

```js
// Nội dung app.js trong thư mục
function f() {
  console.log(arguments, Array.from(arguments));
  console.log(arguments.length);
}
f(1, 2, 3);

// Rest parameter — mảng thật, dùng được trong arrow
const arrow = (...args) => console.log(args);
arrow(1, 2); // [1, 2]

// Cộng mọi đối số không cần khai báo
function sum() {
  let total = 0;
  for (let i = 0; i < arguments.length; i++) total += arguments[i];
  return total;
}
console.log(sum(1, 2, 3, 4)); // 10
```

## 📚 Tham khảo / Bài tập

- Mở `index.html` (Console) hoặc chạy `node app.js` để thấy `Arguments(3)` và `[1, 2]`.
- Tự thử: dùng `[...arguments]` để chuyển thành mảng rồi gọi `.map(x => x * 2)`.
- Tự thử: viết arrow `const a = () => arguments;` ở top-level và xem nó tham chiếu `arguments` ngoài (undefield hoặc lỗi trong strict/Node) — chứng minh arrow không có `arguments` riêng.
- Tự thử: viết một hàm `countArgs()` trả về `arguments.length` và gọi với 0, 2, 5 đối số.