# let và const — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

`let` và `const` là hai từ khóa khai báo biến hiện đại (có từ **ES6/2015**), được thiết kế để thay thế `var` đầy rắc rối của JavaScript cũ. Cả hai có **block scope** (`{}`, `if`, `for`, `while`...) và **không thể khai báo lại** trong cùng một scope. Điểm khác nhau duy nhất: `let` cho phép **gán lại giá trị**, còn `const` **không** — nó khóa **tham chiếu (reference)** của biến.

```js
{
  let course = "JS Basic";
  {
    let course = "JS enhancement"; // biến trùng tên trong block lồng nhau là hợp lệ
    console.log(course);           // "JS enhancement" — truy cập thằng gần nhất (shadowing)
  }
}
console.log(course); // ❌ ReferenceError — course không tồn tại ngoài block
```

### Vì sao phải phân biệt `let` và `const`?

Vì nó ghi lại **ý định của lập trình viên**:
- `const` nói: *"tham chiếu này là cố định, không được trỏ sang nơi khác"*
- `let` nói: *"biến này có thể thay đổi giá trị trong tương lai"*

Trình biên dịch sẽ chặn bạn nếu vô tình gán lại `const`:

```js
const b = { name: "JS" };
b.name = "PHP";  // ✅ OK — sửa thuộc tính bên trong object
b.age = 89;      // ✅ OK — thêm thuộc tính mới
// b = {};       // ❌ TypeError: Assignment to constant variable
```

Nguyên nhân: `const` chỉ khóa **tham chiếu (reference)** của biến trỏ đến object, **không "đóng băng" object đó**. Đây chính là sự khác biệt giữa **tham trị (primitive)** và **tham chiếu (object/reference)** — sẽ học kỹ ở `02_data-types/01_primitive-types/03_value-vs-reference`.

### Block scope — sức mạnh cốt lõi của let/const

```js
// var: function-scoped — thoát khỏi block
if (true) {
  var legacy = "ES5";
}
console.log(legacy);  // "ES5" — var thoát khỏi if!

// let: block-scoped — chỉ tồn tại trong {}
if (true) {
  const modern = "ES6+";
}
// console.log(modern);  // ❌ ReferenceError: modern is not defined
```

### Temporal Dead Zone (TDZ)

`let` và `const` đều có **TDZ** — vùng chết tạm thời từ đầu scope đến dòng khai báo. Truy cập biến trong TDZ gây `ReferenceError` (khác với `var` chỉ in `undefined`):

```js
console.log(x);  // ❌ ReferenceError: Cannot access 'x' before initialization
let x = 10;

console.log(y);  // undefined — var hoisted về undefined, KHÔNG lỗi
var y = 20;
```

> TDZ là tính năng **an toàn**: giúp phát hiện lỗi "dùng biến trước khi khai báo" ngay khi chạy, thay vì im lặng và gây bug logic.

## 📐 Cấu trúc nhóm

```
01_variables/01_declarations/
├── README.md             ← var vs let vs const so sánh rộng
└── 01_let-and-const/
    ├── README.md         ← bài này
    ├── app.js            ← demo scope, hoisting, assignment
    └── index.html
```

## ✅ Điểm mạnh — Tại sao nên dùng let/const thay var

| # | Điểm mạnh | Lý do & Khi nào |
|---|-----------|----------------|
| 1 | **Block scope** | Biến chỉ tồn tại trong khối `{}`, không "rò rỉ" ra ngoài như `var` — an toàn hơn hẳn |
| 2 | **Không khai báo trùng** | `let x = 1; let x = 2;` → SyntaxError — bắt lỗi sớm |
| 3 | **`const` truyền tải ý định rõ** | "đừng gán lại cho biến này" — người đọc hiểu ngay |
| 4 | **Code an toàn hơn, dễ đoán** | Không hoisting kiểu gây `undefined` bất ngờ như `var` |
| 5 | **Shadowing hợp lệ** | Block lồng nhau có thể tạo biến trùng tên dùng riêng |
| 6 | **JIT compiler tối ưu tốt hơn** | V8 compile `let`/`const` nhanh hơn `var` vì scope xác định rõ |
| 7 | **Phù hợp với strict mode** | Kết hợp `"use strict"` ngăn accidental globals |

## ⚠️ Bẫy thường gặp & Hạn chế

| # | Bẫy | Ví dụ code | Cách tránh |
|---|-----|-----------|-----------|
| 1 | **`const` không làm object bất biến** | `const obj = {}; obj.x = 1;` — vẫn đổi được! | Dùng `Object.freeze(obj)` nếu cần immutable thật sự |
| 2 | **TDZ — dùng biến trước khai báo** | `console.log(x); let x = 1;` → ReferenceError | Luôn khai báo biến trước dòng dùng lần đầu |
| 3 | **Khai báo lại `let` trong cùng scope** | `let x = 1; let x = 2;` → SyntaxError | Gán lại `x = 2` thay vì `let x = 2` |
| 4 | **`const` buộc khởi tạo ngay** | `const x;` → SyntaxError | Luôn gán giá trị: `const x = 10;` |
| 5 | **Hiểu nhầm const = immutable** | `const arr = []; arr.push(1);` — mảng vẫn thay đổi! | `const` khóa tham chiếu, không khóa nội dung |
| 6 | **Shadowing gây nhầm lẫn** | `let x = 1; { let x = 2; } console.log(x)` → `1` | Tránh đặt tên trùng trong nested scope |

## 💡 Khi nào dùng — Tình huống thực tế

1. **Mặc định dùng `const`** cho MỌI biến — vì ràng buộc chặt chẽ nhất, ngăn gán lại vô tình.
2. **Chuyển sang `let`** chỉ khi chắc chắn biến cần gán lại: bộ đếm (`let i = 0`), biến lặp `for`, trạng thái thay đổi.
3. **`var` còn dùng** trong các đoạn script rất cũ, hoặc khi must support IE11 — nhưng ưu tiên transpile.
4. **Hằng số cấu hình** → `const API_URL = "https://...";` — `const` + UPPER_SNAKE_CASE.
5. **DOM elements cố định** → `const btn = document.querySelector('#btn');` — không gán lại element.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: const với DOM element — tham chiếu cố định, nội dung thay đổi

```js
// const dùng trỏ tới các phần tử DOM cố định
const button = document.getElementById("btn");
const container = document.querySelector(".container");

// Nội dung bên trong vẫn thay đổi được
button.textContent = "Click me";
button.classList.add("active");
container.innerHTML = "<p>New content</p>";

// Nhưng không thể gán lại biến
// button = document.getElementById("other"); // ❌ TypeError
```

### Ví dụ 2: let cho biến thay đổi — bộ đếm

```js
let count = 0;
button.addEventListener("click", () => {
  count += 1;              // gán lại — cần let
  button.textContent = `Clicked ${count} times`;
});
// const count = 0;        // ❌ không thể gán lại count += 1
```

### Ví dụ 3: const + object — sửa thuộc tính được, gán lại biến thì không

```js
const user = { name: "Sơn", age: 25 };

user.name = "Nam";         // ✅ sửa thuộc tính
user.email = "nam@example.com";  // ✅ thêm thuộc tính mới
console.log(user);         // { name: 'Nam', age: 25, email: 'nam@example.com' }

// user = {};               // ❌ TypeError: Assignment to constant variable
// user = { name: "Hoa" }; // ❌ TypeError
```

### Ví dụ 4: Block scope trong if/loop — so sánh var vs let

```js
// var: function-scoped — thoát khỏi if
if (true) {
  var legacy = 10;
}
console.log(legacy);        // 10 — var thoát khỏi if!

// let: block-scoped — chỉ trong if
if (true) {
  let modern = 20;
}
// console.log(modern);     // ❌ ReferenceError: modern is not defined

// let trong for loop — mỗi iteration có binding riêng
for (let i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 10);
}
// In: 0, 1, 2 — đúng! (var would print 3, 3, 3 do closure over same var)
```

### Ví dụ 5: TDZ — thời điểm khai báo quan trọng

```js
// TDZ: từ đầu scope đến dòng let
console.log(a);  // ❌ ReferenceError: Cannot access 'a' before initialization
let a = 1;

console.log(b);  // undefined — var hoisted về undefined (không lỗi)
var b = 2;

// Function declaration: hoisted trọn vẹn — gọi trước định nghĩa OK
console.log(sum(2, 3));    // 5 — function declaration được hoist
function sum(x, y) {
  return x + y;
}
```

### Ví dụ 6: Object.freeze — khi nào thực sự cần immutable

```js
const config = { host: "localhost", port: 3000 };

// const chỉ khóa tham chiếu — nội dung vẫn mutate được
config.host = "production";  // ✅ vẫn đổi được

// Object.freeze — shallow freeze, khóa toàn bộ thuộc tính
const frozenConfig = Object.freeze({ host: "localhost", port: 3000 });
frozenConfig.host = "production";  // ❌ silently fails (hoặc TypeError in strict mode)
console.log(frozenConfig.host);    // "localhost" — không đổi

// Lưu ý: freeze chỉ shallow — nested object vẫn mutate được
const deep = Object.freeze({ user: { name: "Sơn" } });
deep.user.name = "Nam";            // ✅ vẫn mutate được nested object!
// Cần deep freeze hoặc immutable library (Immer, Immutable.js)
```

## 🔬 So sánh với alternatives

| Phương án | Ưu điểm | Nhược điểm | Phù hợp khi |
|-----------|---------|------------|-------------|
| **`const` mặc định** | An toàn, ngăn gán lại vô tình | Không gán lại được — cần đổi sang `let` nếu cần | Mọi biến không đổi tham chiếu |
| **`let` khi cần mutate** | Linh hoạt, gán lại được | Dễ vô tình gán sai | Bộ đếm, biến trạng thái, vòng lặp |
| **`var` (legacy)** | Support mọi browser cũ | Function scope, hoisting confusing | Bảo trì code IE11, legacy systems |
| **`Object.freeze` + `const`** | Shallow immutable | Không freeze nested, overhead nhỏ | Config objects, constants |
| **Deep freeze libraries** | Immutable thật sự | Performance cost, learning curve | State management (Redux, Immer) |

## 📊 Performance & Best Practices

- **Mặc định `const`, chuyển `let` khi cần gán lại** — pattern được khuyến nghị bởi Airbnb, Google JS style guide.
- **Dùng `for (let i = 0; ...)`** thay `for (var i = 0; ...)` — mỗi iteration có binding riêng, tránh closure bug.
- **Tránh `const` với object mutable dài** — nếu object sẽ thay đổi nhiều, dùng `let` để rõ ý định.
- **Dùng `Object.freeze()`** cho config object — shallow freeze đủ cho object phẳng.
- **Không dùng `var`** — ESLint rule `no-var` enforcement tự động.
- **Arrow function + `const`** là pattern phổ biến nhất trong codebase hiện đại.

## 🔗 Liên kết chéo

- Xem thêm: `01_variables/01_declarations/` — so sánh var/let/const tổng quan
- Xem thêm: `01_variables/02_hoisting/` — TDZ và hoisting mechanism
- Xem thêm: `01_variables/03_scopes/` — block scope chi tiết hơn
- Xem thêm: `02_data-types/01_primitive-types/03_value-vs-reference/` — giá trị vs tham chiếu
- Tài liệu: [MDN — let](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/let), [MDN — const](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/const), [javascript.info/let-const](https://javascript.info/let-const)
