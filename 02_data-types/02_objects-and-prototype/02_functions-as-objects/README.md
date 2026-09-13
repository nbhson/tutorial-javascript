# Functions as Objects (Hàm cũng là object)

## 🔑 Khái niệm

Ở JavaScript, **hàm về bản chất cũng là một object đặc biệt** — bạn có thể "gọi" nó như hàm, nhưng nó vẫn mang đầy đủ đặc tính của object: có property, phương thức, có thể gán vào biến, truyền vào hàm khác. Vì vậy JS có **first-class functions** (xem `00_introduction/01_first-class-function`).

**Cách tạo hàm:**

```js
// 1. Function declaration — được hoisting (gọi trước vẫn chạy)
function func_1() {}

// 2. Function expression — gán hàm cho biến, KHÔNG hoisting
var func_2 = function () {};

// 3. Anonymous function — thường làm callback
setTimeout(() => {}, 1000);
```

**Truyền tham số:**

```js
function writeLog(mess, action) {
  console.log(mess, action);
}
writeLog('Do you want delete this item ?', 'Delete');
```

**Arguments object** — bên trong một hàm (không phải arrow), `arguments` là một array-like chứa **tất cả** đối số đã truyền, dù hàm không khai báo tham số:

```js
function argumentFunc() {
  console.log(arguments);            // { '0': 'LOG 1', '1': 'LOG 2', '2': 'LOG 3' }
  for (const item of arguments) {
    console.log(item);               // LOG 1 / LOG 2 / LOG 3
  }
}
argumentFunc('LOG 1', 'LOG 2', 'LOG 3');
```

**Return:** nếu hàm không có `return`, kết quả trả về mặc định là **`undefined`**.

**Vì sao hàm là object?**

- Hàm có thuộc tính riêng như `name`, `length` (số tham số khai báo).
- Hàm có phương thức như `call()`, `apply()`, `bind()`.
- Truy cập `f.name`, `f.length` như một object bình thường.
- Có thể lưu trong biến, đưa vào object/mảng, truyền và trả về (first-class).

**Các dạng hàm trong object:**

```js
var obj1 = {
  myFunc: function () {},   // property chứa hàm
};
var obj2 = {
  myFunc() {},              // shorthand method (ES6) — cùng tác dụng
};
```

## ✅ Điểm mạnh

- Function declaration tự hoisting → có thể gọi trước khi định nghĩa, dễ tổ chức file.
- Hàm là object → `name`, `length`, `arguments` hữu ích khi viết library/debug.
- Anonymous + callback (`setTimeout(() => {})`) tạo code bất đồng bộ gọn gàng.
- Expression function không hoisting → bắt buộc khai báo theo thứ tự, dễ kiểm soát.

## ⚠️ Lưu ý / Hạn chế

- **Function declaration** thì hoisted; **function expression** thì không — nhầm thứ tự sẽ lỗi `ReferenceError`.
- `arguments` chỉ tồn tại trong hàm "thường"; **arrow function không có `arguments`**.
- Nếu không khai báo `return`, hàm trả về `undefined` — dễ quên khi viết hàm cần kết quả.
- `alert`/`console` chỉ hoạt động ở môi trường phù hợp (trình duyệt cho `alert`, `console` cả Node).

## 💡 Khi nào dùng

- Hàm tái sử dụng, tổ chức logic rõ ràng → declaration.
- Gắn hành vi tạm, callback (sự kiện, timer) → anonymous/expression.
- Viết hàm đếm biến tham số linh hoạt → `arguments` (hoặc dùng rest parameter).
- Tạo method cho object → shorthand `myFunc() {}`.

## 🎯 Ví dụ minh họa

```js
// Declaration (hoisting được)
console.log(sum(2, 3)); // 5
function sum(a, b) { return a + b; }

// Expression (không hoisting)
const sub = function (a, b) { return a - b; }; // gọi sau khi định nghĩa
console.log(sub(5, 2)); // 3

// arguments
function logAll() {
  console.log(arguments.length); // 3
}
logAll('a', 'b', 'c');

// function là object
function demo() {}
console.log(typeof demo, demo.name, demo.length); // function demo 0
```

## 📚 Tham khảo / Bài tập

- Chạy `1_app.js` (tạo hàm, truyền tham số, `arguments`, return undefined) và `2_Cac-loai-function.js` (declaration, expression, anonymous callback, method shorthand) bằng `node` hoặc mở `index.html`.
- Tự thử: 1) gọi hàm `showDialog` (declaration) *trước* khi định nghĩa và xem nó chạy được; 2) đổi nó thành `const showDialog = () => {...}` và gọi trước để đọc lỗi hoisting; 3) viết hàm dùng rest `(...danhSach)` thay thế `arguments` và so sánh.
- Tài liệu: [MDN — Functions](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Functions).