# Tham số hàm (Function Parameters)

## 🔑 Khái niệm

Đây là bài về **cách khai báo và truyền dữ liệu vào hàm** trong JavaScript, với ba khái niệm quan trọng:

### 1. Parameters vs Arguments
- **Parameter (tham số)**: biến khai báo trong dấu `()` của hàm — `function greet(name, age)`.
- **Argument (tham đối)**: giá trị thực sự truyền vào khi gọi — `greet("A", 20)`.
- Nếu gọi thiếu, tham số nhận `undefined` (không lỗi như một số ngôn ngữ khác).

### 2. Default parameters (ES6)
Tham số có **giá trị mặc định** khi không truyền hoặc truyền `undefined`:

```js
function greet(name, age = 18) {
  console.log(name, age);
}
greet("A");      // A 18 — age dùng mặc định
```

### 3. Rest parameters (`...rest`)
Gom **các đối số còn lại** thành một **mảng thật**:

```js
function greet(name, age = 18, ...rest) {
  console.log({ name, age, rest });
}
greet("A", 20, "x", "y"); // { name: "A", age: 20, rest: ["x", "y"] }
greet();                 // { name: undefined, age: 18, rest: [] }
```

File `app.js` demo tổng hợp cả ba + một hàm cộng ba số:

```js
function sum(a, b, c) {
  console.log(a + b + c); // sum(1,2,3) → 6
}
```

## ✅ Điểm mạnh

- **Default parameter** giúp bỏ đi hàng trăm dòng kiểu `age = age ?? 18` thủ công.
- **Rest `...args`** thay thế `arguments` gọn và là mảng thật (có `map`, `filter`...).
- Cú pháp rõ ràng, đọc là hiểu mục đích (`...rest` tự nói "phần còn lại").
- Gọi thiếu đối số không gây lỗi — JS linh hoạt cho đối số tùy chọn.
- Kết hợp được: default và rest dùng chung trong một hàm.
- Rest trả mảng rỗng nếu không có đối số thừa, không sợ `undefined`.

## ⚠️ Lưu ý / Hạn chế

- Rest **phải nằm cuối cùng** trong danh sách tham số — `(...rest, a)` là cú pháp sai.
- Tham số thiếu nhận `undefined` chứ không nhất thiết là lỗi — dễ sót điều kiện kiểm tra.
- Default parameter chỉ áp dụng cho `undefined`, **không áp dụng** cho `null` hay `0` (truyền `null` thì `age = null`, không phải 18).
- Đổi thứ tự tham số khi gọi sẽ đổi nghĩa (JS không có named parameters sẵn — dùng destructuring object để giả lập).
- Nhầm lẫn khai báo nhiều tham số nhưng gọi ít → biến `undefined`, tính toán ra `NaN`.

## 💡 Khi nào dùng

- Hàm có tham số tùy chọn (page size mặc định 10, role mặc định "user").
- Hàm nhận danh sách động đối số (log, gom giá trị, tính tổng).
- Truyền cờ/tùy biến qua object destructuring — `function open(options = {})`.
- Viết API thư viện thân thiện với người dùng.

## 🎯 Ví dụ minh họa

```js
// Nội dung app.js trong thư mục
function greet(name, age = 18, ...rest) {
  console.log({ name, age, rest });
}
greet("A", 20, "x", "y"); // { name: "A", age: 20, rest: ["x", "y"] }
greet();                  // { name: undefined, age: 18, rest: [] }

// Rest gom đối số: hàm tính tổng
function sumAll(...nums) {
  return nums.reduce((acc, n) => acc + n, 0);
}
console.log(sumAll(1, 2, 3, 4)); // 10
```

## 📚 Tham khảo / Bài tập

- Mở `index.html` (Console) hoặc chạy `node app.js` để thấy `{name:"A", age:20, rest:["x","y"]}` rồi đến `{name:undefined, age:18, rest:[]}` và `6`.
- Tự thử: gọi `greet("B", null)` xem `age = null` — nhớ mặc định chỉ áp cho `undefined`.
- Tự thử: viết `const info = ({ name = "Ẩn danh", age = 18 } = {}) => ...` và gọi `info({ name: "Sơn" })`.
- Tự thử: đảo rest lên trước `function bad(...a, b) {}` để xem lỗi cú pháp xảy ra.