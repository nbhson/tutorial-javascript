# Scope (Phạm vi biến) — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

**Scope** là "phạm vi sống" của một biến — nơi biến tồn tại và có thể được truy cập. JavaScript có **3 loại scope chính** được sắp xếp thành **scope chain** (chuỗi phạm vi):

1. **Global scope** — khai báo ngoài cùng (top-level), mọi nơi đều truy cập được.
2. **Block scope** — `{}`, `if`, `for`, `while`... — **`let`/`const`** chỉ tồn tại trong khối; **`var` thì không** (nhảy ra ngoài khối!).
3. **Function scope** — biến khai báo trong hàm (**`var`**, `function`, `let`/`const`) không truy cập được từ bên ngoài hàm.

### Cơ chế lookup trong JavaScript engine

Khi bạn viết `console.log(tênBiến)`, engine thực hiện **scope chain lookup** theo các bước:

1. Kiểm tra scope hiện tại — có biến `tênBiến` không? Nếu có → dùng, dừng.
2. Nếu không, leo lên **outer scope** (scope bao quanh) — lặp lại bước 1.
3. Tiếp tục leo lên cho đến **global scope**.
4. Nếu không tìm thấy ở bất kỳ scope nào → **ReferenceError**.

```
Global scope
  └── Function scope A
        └── Block scope B (if/for)
              └── Block scope C (nested if)
```

> **Quy tắc quan trọng:** Mỗi lần **GỌI hàm** là một **scope mới** được tạo. Cùng một hàm nhưng gọi 3 lần sẽ tạo 3 phạm vi độc lập — biến local không "dính" nhau giữa các lần gọi.

### 3 loại scope chi tiết

#### 1. Global scope

```js
var globalMsg = "Học về scope";  // global variable
console.log(globalMsg);           // "Học về scope" — truy cập từ mọi nơi

function logger() {
  console.log(globalMsg);        // ✅ truy cập được biến global
}
logger();
```

#### 2. Block scope — let/const vs var

```js
{
  let blockScoped = 18;          // block-scoped — chỉ trong {}
  const alsoBlocked = "ES6";     // block-scoped
  var functionScoped = 100;      // var: function-scoped, THOÁT khỏi block!
}
console.log(blockScoped);         // ❌ ReferenceError
console.log(alsoBlocked);         // ❌ ReferenceError
console.log(functionScoped);      // 100 — var thoát block!
```

#### 3. Function scope

```js
function logger() {
  var name = "Son";              // function-scoped
  let age = 20;                  // block-scoped (trong function body)
}
logger();
// console.log(name);             // ❌ ReferenceError
// console.log(age);              // ❌ ReferenceError
```

### Lexical scoping (static scoping) — quy tắc "trong ra ngoài"

Hàm (hay block) có thể truy cập biến của chính nó **và** của mọi scope bên ngoài nó — đó là vì sao `logger2` đọc được `myName` ở global:

```js
const myName = "Sơn Nguyễn";     // global scope
function logger2() {
  const age = 20;                // function scope
  console.log(myName);           // ✅ Sơn Nguyễn — đọc từ outer scope
  console.log(age);              // ✅ 20 — đọc từ own scope
}
logger2();
```

**Khi tìm một biến, JS đi từ trong ra ngoài** (nested scope chain): gặp biến trùng tên ở scope gần nhất thì dừng; tìm hết global, không có thì `ReferenceError`.

```js
const age = 18;                  // global
{
  const age = 16;                // block 1 — override global age
  {
    const age = 12;              // block 2 — override block 1 age
    {
      console.log(age);          // 12 — thằng gần nhất bên trong
      // nếu chưa khai báo `const age` ở đây, sẽ trả về age của scope ngoài
    }
  }
}
console.log(age);                // 18 — global scope
```

### Shadowing — khi nào biến "che" biến ngoài?

Biến cùng tên ở scope trong **che** biến scope ngoài (shadowing). Đây là tính năng hợp lệ nhưng dễ gây bug nếu không để ý:

```js
let color = "red";               // global
function paint() {
  let color = "blue";            // shadow global color
  console.log(color);            // "blue" — dùng biến trong scope gần nhất
}
paint();
console.log(color);              // "red" — global không bị ảnh hưởng
```

### Khi nào biến bị xóa khỏi bộ nhớ? (Garbage Collection)

- **Biến global**: chỉ bị giải phóng khi chương trình kết thúc (đóng tab, F5, thoát trình duyệt).
- **Biến trong block/hàm**: bị giải phóng khi thoát khỏi block hoặc sau khi hàm chạy xong → **ưu tiên khai báo biến trong hàm/block để tiết kiệm bộ nhớ**.
- **Biến trong hàm được tham chiếu bởi hàm khác (closure)**: **không bị xóa ngay**, vì closure còn giữ reference — xem bài `02_hoisting/` (mục closure) và `09_functions/02_scope-closure-strict-mode/03_closure/`.

## 📐 Cấu trúc nhóm

```
01_variables/03_scopes/
├── README.md         ← bài này
└── app.js            ← demo global, block, function scope
    └── index.html
```

## ✅ Điểm mạnh — Tại sao nên hiểu scope kỹ

| # | Lợi ích | Lý do |
|---|---------|-------|
| 1 | **Khai báo càng hẹp càng an toàn** | Tránh "ô nhiễm" biến toàn cục giữa các module |
| 2 | **Scope chain cho phép closure** | Nền tảng của hàm ghi nhớ trạng thái, memoization, factory |
| 3 | **Giải phóng bộ nhớ tự động** | Biến ra khỏi scope → GC thu hồi — tiết kiệm RAM |
| 4 | **Block scope của let/const** | Biến lặp `for` không rò rỉ ra ngoài — tránh bug kinh điển |
| 5 | **Debug dễ hơn** | Biết scope nào đang xét → tìm nhanh nguyên nhân "undefined" |
| 6 | **Viết module encapsulation** | IIFE + scope cô lập — pattern quan trọng cho library development |

## ⚠️ Bẫy thường gặp & Hạn chế

| # | Bẫy | Ví dụ code | Cách tránh |
|---|-----|-----------|-----------|
| 1 | **`var` không có block scope** | `for(var i=0;i<3;i++){}; console.log(i)` → `3` (i leak ra ngoài!) | Luôn dùng `let` cho vòng lặp |
| 2 | **Biến global giữ bộ nhớ lâu** | `let data = fetchData();` ở top-level — GC không thu hồi được | Đưa vào function scope khi không dùng nữa |
| 3 | **Shadowing tinh vi** | `let x = 1; if(true){ let x = 2; } console.log(x)` → `1` — không lỗi nhưng dễ nhầm | Tránh đặt tên trùng trong nested scope |
| 4 | **Implicit global (không khai báo)** | `count = 0;` (thiếu `let`) → tạo global ngầm | `"use strict"` + ESLint `no-undef` |
| 5 | **Closure giữ reference lâu** | `function makeHandler() { let largeData = ...; return () => largeData; }` | Giải phóng reference khi không cần |
| 6 | **`this` binding phụ thuộc scope** | Arrow function kế thừa `this` từ outer scope — không phải object gọi | Hiểu `this` rules ở `10_this-keyword/` |

## 💡 Khi nào dùng — Tình huống thực tế

1. **Khai báo cấu hình/dữ liệu dùng chung toàn app** → global (nhưng hạn chế — prefer module exports).
2. **Biến tạm trong vòng lặp, điều kiện** → block scope (`let`).
3. **Encapsulation: gói logic trong IIFE hoặc hàm** → ngăn lộ biến ra ngoài global namespace.
4. **Closure: tạo "state riêng" cho mỗi lần gọi function factory** — mỗi instance có scope riêng.
5. **Module pattern** — export chỉ những gì cần, giữ private state trong module scope.
6. **Event handler với captured variables** — closure giữ biến từ outer scope.
7. **Memoization cache** — object cache trong function scope, truy cập qua closure.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Global vs Block scope

```js
var message = "Học về scope"; // GLOBAL — tồn tại suốt vòng đời page

{
  let age = 18;               // BLOCK — let: chỉ trong {}, var thì thoát ra ngoài
  console.log(age);           // 18 ✓
}
// console.log(age);          // ❌ ReferenceError: age is not defined (với let)

var escaped = "I escaped!";   // var thoát block
console.log(escaped);         // "I escaped!"
```

### Ví dụ 2: Function scope — biến không ra ngoài được

```js
function local() {
  var name = "Son";           // FUNCTION scope — không lộ ra ngoài được
  let inner = "also private"; // block scope — càng không ra ngoài
  return name;
}
console.log(local());         // "Son"
// console.log(name);         // ❌ ReferenceError
// console.log(inner);        // ❌ ReferenceError
```

### Ví dụ 3: Scope chain — đọc biến từ scope ngoài

```js
const globalX = 100;

function demo() {
  const x = 10;              // function scope
  function inner() {
    const x = 1;             // inner function scope — shadow outer x
    console.log(x);          // 1 — dùng thằng gần nhất
  }
  inner();
  console.log(x);            // 10 — function scope của demo
}
demo();
console.log(globalX);         // 100 — global scope
```

### Ví dụ 4: Closure — scope được "nhớ" sau khi hàm return

```js
function makeCounter() {
  let counter = 0;           // biến trong scope của makeCounter
  return function () {
    counter++;               // closure "nhớ" counter từ outer scope
    return counter;
  };
}
const count1 = makeCounter();
const count2 = makeCounter();
console.log(count1());       // 1 — count1 có scope riêng
console.log(count2());       // 1 — count2 có scope riêng (không dính count1)
console.log(count1());       // 2
```

### Ví dụ 5: IIFE — Encapsulation pattern

```js
// Immediately Invoked Function Expression — tạo private scope
const module = (function () {
  let privateVar = "secret"; // không thể truy cập từ bên ngoài

  function privateMethod() {
    return privateVar;
  }

  return {
    // Chỉ expose những gì cần
    getPrivate: privateMethod,
    publicVar: "public",
  };
})();

console.log(module.publicVar);   // "public"
console.log(module.getPrivate()); // "secret"
// console.log(module.privateVar); // ❌ undefined — private scope
// console.log(module.privateMethod()); // ❌ undefined
```

### Ví dụ 6: Loop + closure — var vs let khác biệt

```js
// var trong loop — tất cả closure share cùng ONE variable
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log("var i =", i), 10);
}
// Kết quả: 3, 3, 3 — vì i = 3 khi setTimeout chạy

// let trong loop — mỗi iteration có binding RIÊNG
for (let j = 0; j < 3; j++) {
  setTimeout(() => console.log("let j =", j), 10);
}
// Kết quả: 0, 1, 2 — mỗi closure capture binding của iteration đó
```

## 🔬 So sánh với alternatives

| Phương án | Ưu điểm | Nhược điểm |
|-----------|---------|------------|
| **Block scope (let/const)** | An toàn, biến không rò rỉ | Không tương thích IE11 |
| **Function scope (var)** | Hỗ trợ mọi browser | Biến rò rỉ ra ngoài block, dễ gây bug |
| **IIFE module pattern** | Encapsulation, private state | Cú pháp verbose, cần hiểu scope chain |
| **ES Module (import/export)** | Encapsulation tự nhiên, tree-shakeable | Cần build tool hoặc module support |
| **Global namespace** | Truy cập mọi nơi | Ô nhiễm, khó debug, memory leak |

## 📊 Performance & Best Practices

- **Khai báo biến càng hẹp càng tốt** — trong function scope thay vì global để giảm bộ nhớ tồn tại.
- **Dùng `let`/`const` thay `var`** — block scope an toàn hơn, engine tối ưu tốt hơn.
- **Tránh shadowing** — đặt tên khác nhau trong nested scope để code dễ đọc.
- **Sử dụng IIFE/Module pattern** cho library code — encapsulate private state.
- **Config ESLint** — `no-shadow`, `no-unused-vars`, `no-undef` enforce scope rules tự động.
- **Tận dụng closure cho memoization** — cache trong function scope, tránh global pollution.
- **Giải phóng reference khi không dùng** — `largeObj = null` để GC thu hồi, đặc biệt trong SPA.

## 🔗 Liên kết chéo

- Xem thêm: `01_variables/01_declarations/01_let-and-const/` — block scope chi tiết
- Xem thêm: `01_variables/02_hoisting/` — hoisting và TDZ trong scope
- Xem thêm: `09_functions/02_scope-closure-strict-mode/03_closure/` — closure deep dive
- Xem thêm: `09_functions/02_scope-closure-strict-mode/02_iife/` — IIFE encapsulation pattern
- Xem thêm: `10_this-keyword/` — `this` binding phụ thuộc scope
- Tài liệu: [MDN — Scope](https://developer.mozilla.org/en-US/docs/Glossary/Scope), [javascript.info/closure](https://javascript.info/closure), [javascript.info/var](https://javascript.info/var)
