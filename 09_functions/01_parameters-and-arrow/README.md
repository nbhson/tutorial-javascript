# Hàm — Tham số và Arrow (Parameters & Arrow)

## 🔑 Khái niệm

Nhóm này bao gồm **cách tạo hàm và truyền dữ liệu vào hàm** trong JavaScript. Sáu thư mục con lần lượt giải quyết:

| Thư mục | Nội dung |
|---|---|
| `01_callbacks/` | callback — truyền hàm làm đối số; tự tái tạo `forEach`, `filter`, `some`, `every`, `map` |
| `02_builtin-functions/` | các hàm built-in có sẵn: `alert`, `confirm`, `prompt`, `setTimeout`, `setInterval`... |
| `03_arrow-functions/` | cú pháp arrow `() => {}` và sự khác biệt so với hàm thường (`this`, return ngầm) |
| `04_recursion/` | đệ quy — hàm gọi chính nó: giai thừa, Fibonacci |
| `05_arguments-object/` | đối tượng `arguments` array-like ẩn trong hàm thường, dùng rest `...args` thay thế |
| `06_function-parameters/` | khái niệm tham số/tham đối, default value, rest parameter |

Hai kiến thức đáng chú ý nhất:

1. **Params vs Arguments**: *tham số* (parameter) là biến trong khai báo hàm; *tham đối* (argument) là giá trị thực sự truyền khi gọi.
2. **Function declaration vs expression vs arrow**: cách thứ nhất được hoisted (dùng được trước khai báo), hai cách còn lại không.

## ✅ Điểm mạnh

- Sắp xếp logic từ dễ đến khó: callback → built-in → arrow → đệ quy → arguments → params.
- Các file bài tập *tự viết lại* phương thức mảng (`forEach2`, `filter2`...) giúp hiểu cơ chế sâu, không chỉ dùng "thuộc lòng".
- Có cả lý thuyết nhẹ (arguments object) lẫn thực hành (6 file callback).
- Đa số thư mục con có `app.js` + `index.html` để chạy ngay.
- Bao gồm cả cách viết gọn của arrow và cách thoát khỏi giới hạn của nó (rest, return object dùng `()`).

## ⚠️ Lưu ý / Hạn chế

- Arrow function **không có `arguments`, không làm constructor**, và `this` trong arrow là `this` của nơi định nghĩa (không phải nơi gọi).
- `arguments` chỉ là array-like: không có `map`, `filter`... muốn dùng phải `Array.from(arguments)` hoặc chuyển sang rest.
- Đệ quy phải có base case; nếu không sẽ `Maximum call stack size exceeded`.
- Các hàm built-in như `alert`, `confirm`, `prompt` chỉ dùng được trong trình duyệt — **không chạy được trong Node.js thuần**.
- `eval` được nhắc như hàm built-in nhưng hiện "tránh dùng" — độc hại và chậm.

## 💡 Khi nào dùng

- Truyền hành vi cho hàm khác (callback) — xử lý sự kiện, xử lý danh sách.
- Dùng hàm có sẵn của trình duyệt cho UI thông báo, hẹn giờ.
- Viết arrow cho callback ngắn gọn, tránh mất `this` ở ngoài.
- Đệ quy cho bài toán chia nhỏ lặp lại (thư mục, cây, giai thừa).
- Khai báo tham số mặc định và gom thừa số vào `...rest`.

## 🎯 Ví dụ minh họa

```js
// Arrow + map
const [a] = [1, 2, 3].map(n => n * 2);
console.log(a); // 2

// Default + rest
function greet(name, age = 18, ...rest) {
  console.log(name, age, rest);
}
greet("A", 20, "x", "y"); // A 20 ["x", "y"]
```

## 📚 Tham khảo / Bài tập

- Lần lượt đi từ `01_callbacks/` (6 file) → `06_function-parameters/`.
- Trong mỗi thư mục, chạy `node app.js` (hoặc file cụ thể như `node 03_arrow-functions/app.js`) hoặc mở `index.html` trên trình duyệt.
- Tự thử: dùng `Array.from(arguments)` trong `05_arguments-object/app.js`, và viết một arrow có thân là object `({a, b})` trong `03_arrow-functions`.