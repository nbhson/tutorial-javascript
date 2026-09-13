# Scope (Phạm vi biến)

## 🔑 Khái niệm

**Scope** là "phạm vi sống" của một biến — nơi biến tồn tại và có thể được truy cập. JavaScript có **3 loại scope**:

1. **Global scope** — khai báo ngoài cùng (top-level), mọi nơi đều truy cập được.

```js
var message = "Học về scope"; // biến toàn cục
function logger() {
  console.log(message); // truy cập biến global ✓
}
logger();
```

2. **Block scope** (`if`, `for`, `{}`, `while`...) — **`let`/`const`** chỉ tồn tại trong khối; **`var` thì không** (nhảy ra ngoài khối!):

```js
{
  let age = 18;
  console.log(age); // 18 ✓
}
console.log(age); // ReferenceError: age is not defined (nếu là var → 18)
```

3. **Function scope (local scope)** — biến khai báo trong hàm (**`var`**, `function`, `let`/`const`) không truy cập được từ bên ngoài hàm:

```js
function logger() {
  var name = "Son";
}
logger();
console.log(name); // ReferenceError: name is not defined
```

**Các quy luật quan trọng:**

- **Mỗi lần GỌI hàm là một scope mới.** Cùng một hàm nhưng gọi 3 lần sẽ tạo 3 phạm vi độc lập — biến local không "dính" nhau giữa các lần gọi:

```js
function logger(name) {
  console.log(name);
}
logger("name1"); // name1
logger("name2"); // name2
```

- **Scope hướng trong.** Hàm (hay block) có thể truy cập biến của chính nó **và** của mọi scope bên ngoài nó — đó là vì sao `logger2` đọc được `myName` ở global:

```js
const myName = "Sơn Nguyễn";
function logger2() {
  const age = 20;
  console.log(myName); // Sơn Nguyễn (ở ngoài)
  console.log(age);    // 20 (ở trong)
}
logger2();
```

- **Khi tìm một biến, JS đi từ trong ra ngoài** (nested scope chain): gặp biến trùng tên ở scope gần nhất thì dừng; tìm hết global, không có thì `ReferenceError`.

```js
const age = 18;
{
  const age = 16;
  {
    const age = 12;
    {
      console.log(age); // 12 — thằng gần nhất bên trong
      // nếu chưa khai báo `const age` ở đây, sẽ trả về age của scope ngoài
    }
  }
}
```

**Khi nào biến bị xóa khỏi bộ nhớ?**

- Biến **global**: chỉ bị giải phóng khi chương trình kết thúc (đóng tab, F5, thoát trình duyệt).
- Biến trong **block / hàm**: bị giải phóng khi thoát khỏi block hoặc sau khi hàm chạy xong → **ưu tiên khai báo biến trong hàm/block để tiết kiệm bộ nhớ**.
- Biến trong hàm **được tham chiếu bởi hàm khác (closure)**: không bị xóa ngay, vì closure còn giữ — xem bài `01_variables/02_hoisting` (mục closure) và closure trong `01_declarations/01_let-and-const`.

## ✅ Điểm mạnh

- Khai báo càng hẹp càng an toàn: tránh "ô nhiễm" biến toàn cục giữa các module.
- Scope chuỗi (chain) cho phép closure linh hoạt — nền tảng của hàm ghi nhớ trạng thái.
- Giải phóng bộ nhớ tự động sau khi ra khỏi scope → tiết kiệm RAM.
- Block scope của `let`/`const` giúp biến lặp `for` không bị rò rỉ.

## ⚠️ Lưu ý / Hạn chế

- `var` **không có block scope** — đây là nguồn bug kinh điển ở vòng lặp và `if`.
- Biến global giữ bộ nhớ lâu; lạm dụng gây rò rỉ và xung đột tên.
- Cùng tên ở scope trong "che" scope ngoài (shadowing) — nếu không để ý, lỗi tinh vi.
- Nếu không khai báo từ khóa (`count = 0`) trong non-strict mode, JS ngầm tạo biến **global** — cực kỳ khó kiểm soát.

## 💡 Khi nào dùng

- Khai báo cấu hình/dữ liệu dùng chung toàn app → global.
- Biến tạm trong vòng lặp, điều kiện → block scope (`let`).
- Encapsulation: gói logic trong IIFE hoặc hàm, ngăn lộ biến ra ngoài.
- Closure: tạo "state riêng" cho mỗi lần gọi function factory.

## 🎯 Ví dụ minh họa

```js
var message = "Học về scope"; // GLOBAL

{
  let age = 18;               // BLOCK — let: chỉ trong {}, var thì thoát ra ngoài
  console.log(age);           // 18
}
// console.log(age);          // ReferenceError (với let)

function local() {
  var name = "Son";           // FUNCTION scope — không lộ ra ngoài được
  return name;
}
console.log(local());         // Son
// console.log(name);         // ReferenceError

function demo() {
  const x = 10;
  function inner() {
    console.log(x);           // 10 — inner thấy biến của scope ngoài
  }
  inner();
}
demo();
```

## 📚 Tham khảo / Bài tập

- Chạy `app.js` trong thư mục (mở `index.html` → Console hoặc `node app.js`): nó demo Global (`var message`), Block scope (`let age` — dòng `console.log(age)` sau block sẽ lỗi), Function scope (`var name` không ra ngoài), và các nhận xét về scope mới mỗi lần gọi hàm.
- Tự thử: 1) sửa `let age` thành `var age` trong `app.js` và chạy lại — bây giờ `console.log(age)` bên ngoài block in được `18`, chứng minh `var` thoát block; 2) viết hàm đếm dùng closure (`makeCounter()`) và gọi 3 lần, để ý biến `counter` không bị xóa.
- Tài liệu: [MDN — Scope](https://developer.mozilla.org/en-US/docs/Glossary/Scope), [javascript.info/closure](https://javascript.info/closure).