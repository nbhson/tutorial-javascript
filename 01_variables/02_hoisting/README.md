# Hoisting — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

**Hoisting** (nâng lên) là hành vi của JavaScript engine: khi phân tích một phạm vi (scope), nó **"kéo" các khai báo** — biến `var`, `let`, `const` và **function declaration** — lên **đầu phạm vi** trước khi thực thi bất kỳ dòng code nào. Tuy nhiên, cách "kéo" của từng loại rất khác nhau, và đây là nguồn gốc của nhiều bug khó hiểu.

### Cơ chế hoạt động trong JavaScript engine

Khi engine gặp một scope (global script, function body, hoặc block `{}`), nó thực hiện **hai bước**:

1. **Creation phase**: quét toàn bộ scope, tạo các binding (biến/function) và khởi tạo chúng.
2. **Execution phase**: thực thi từng dòng code theo thứ tự.

Trong creation phase:
- `var` → binding được tạo, khởi tạo thành `undefined`.
- `let`/`const` → binding được tạo, nhưng **không khởi tạo** — nằm trong **TDZ (Temporal Dead Zone)** cho đến dòng khai báo.
- `function declaration` → binding được tạo và khởi tạo với **full function body** (hoisted trọn vẹn).
- `class declaration` → binding được tạo nhưng không khởi tạo (giống `let`/`const`, có TDZ).

### 4 loại hoisting khác nhau

#### 1. Hoisting với `var` — khai báo kéo lên, giá trị `undefined`

```js
console.log(age);      // undefined — khai báo `var age` đã được hoist lên trên
var age = 16;          // initialization (gán giá trị) xảy ra tại dòng này
// Quy trình thực tế:
// var age;             ← creation phase: age = undefined
// console.log(age);    ← execution phase: in undefined
// age = 16;            ← execution phase: gán 16
```

#### 2. Hoisting với `let`/`const` — có TDZ, truy cập trước gây ReferenceError

```js
console.log(fullName);
// ❌ ReferenceError: Cannot access 'fullName' before initialization
let fullName = "Sơn Nguyễn";
// Quy trình thực tế:
// let fullName;        ← creation phase: binding tồn tại nhưng trong TDZ
// console.log(fullName); ← execution phase: TDZ → ReferenceError
// fullName = "Sơn Nguyễn"; ← initialization (gán giá trị)
```

**TDZ (Temporal Dead Zone)**: "vùng chết tạm thời" — biến *đã tồn tại* trong phạm vi nhưng **chưa thể dùng** cho đến khi dòng khai báo được thực thi. Nhờ vậy, `let`/`const` giúp tránh lỗi logic khi vô tình dùng biến trước khi khai báo — thay vì in `undefined` im lặng, engine ném `ReferenceError` ngay.

#### 3. Hoisting với function declaration — kéo lên TRọn vẹn

```js
console.log(sum(6, 9));  // 15 — hàm được hoist trọn vẹn
function sum(a, b) {
  return a + b;
}
// Quy trình thực tế:
// function sum(a, b) { ... }  ← creation phase: hàm sẵn sàng dùng
// console.log(sum(6, 9));     ← execution phase: gọi được ngay
```

> ⚠️ **Arrow function và function expression KHÔNG được hoist** — chúng là biến, nên rơi vào TDZ như `let`/`const`:

```js
console.log(gapBa(4));  // ❌ ReferenceError: Cannot access 'gapBa' before initialization
const gapBa = (n) => n * 3;
```

#### 4. Hoisting trong closure — function declaration bên trong hàm khác vẫn được hoist

```js
function makeCounter() {
  let counter = 0;
  return increase;  // ✅ trả về tham chiếu dù increase định nghĩa phía dưới
  // increase được hoist trong phạm vi makeCounter
  function increase() {
    return ++counter;
  }
}
const c = makeCounter();
console.log(c());  // 1
console.log(c());  // 2
```

## 📐 Cấu trúc nhóm

```
01_variables/02_hoisting/
├── README.md         ← bài này
└── app.js            ← demo hoisting thực tế
    └── index.html
```

## ✅ Điểm mạnh — Tại sao nên hiểu hoisting

| # | Điểm mạnh | Lý do |
|---|-----------|-------|
| 1 | **Function declaration gọi trước định nghĩa** | Code có thể sắp xếp "ý nghĩa" trước, chi tiết sau — tổ chức file tự nhiên hơn |
| 2 | **TDZ bắt lỗi sớm** | `let`/`const` dùng trước khai báo → `ReferenceError` thay vì `undefined` im lặng |
| 3 | **Đọc được code cũ viết bằng `var`** | Biết `var` hoisted về undefined → không bị lừa bởi `console.log(x)` in `undefined` |
| 4 | **Closure hoạt động đúng cách** | Function declaration trong closure được hoist đúng scope — hiểu được behavior này |
| 5 | **Debug lỗi "undefined is not a function"** | Recognize pattern: function expression dùng trước khi khai báo |

## ⚠️ Bẫy thường gặp & Hạn chế

| # | Bẩy | Ví dụ code | Cách tránh |
|---|-----|-----------|-----------|
| 1 | **`var` hoisted về undefined — không báo lỗi** | `console.log(age); var age = 16;` → in `undefined` | Dùng `let`/`const` — TDZ sẽ báo lỗi ngay |
| 2 | **Arrow function không hoisted** | `const fn = () => {}; fn();` trước khai báo → ReferenceError | Viết function declaration hoặc đặt khai báo trước gọi |
| 3 | **Class declaration có TDZ** | `new Person(); class Person {}` → ReferenceError | Đặt class trước khi dùng hoặc dùng function declaration pattern |
| 4 | **Function expression vs declaration confusion** | `var fn = function(){};` (expression) không hoisted | Phân biệt `function fn(){} ` (declaration) vs `var fn = function(){}` (expression) |
| 5 | **IIFE lợi dụng hoisting** | `(function(){...})()` chạy ngay — hiểu scope để tránh leak | Dùng `let`/`const` trong IIFE, không `var` |

## 💡 Khi nào dùng — Tình huống thực tế

1. **Tổ chức file có mục** — hàm "tiện ích" đặt dưới, logic chính gọi ở trên (function declaration hoist giúp được).
2. **Debug lỗi `Cannot access 'fullName' before initialization`** — nhận ra dấu hiệu TDZ, nguyên nhân do dùng `let`/`const` trước khai báo.
3. **Nhận diện code cũ** — thấy `console.log(x)` in `undefined` mà không lỗi → xem có phải `var` không.
4. **Viết recursive function** — function declaration hoist cho phép gọi tên hàm bên trong thân hàm (cần `function` keyword).
5. **Setup test fixtures** — các helper function declaration được hoist, test code gọn hơn.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: var vs let hoisting difference

```js
// var: hoisted về undefined — KHÔNG lỗi
console.log(str);    // undefined
var str = "Hoisting";

// let: hoisted nhưng trong TDZ — ReferenceError
// console.log(x);   // ❌ ReferenceError
let x = 10;
```

### Ví dụ 2: Function declaration vs function expression hoisting

```js
// Function declaration: hoisted trọn vẹn — gọi trước được
console.log(gapDoi(4));   // 8
function gapDoi(n) {
  return n * 2;
}

// Function expression (arrow): KHÔNG hoisted — gọi trước lỗi
// console.log(gapBa(4)); // ❌ ReferenceError
const gapBa = (n) => n * 3;
console.log(gapBa(4));    // 12 — gọi sau khi khai báo
```

### Ví dụ 3: TDZ trong block scope

```js
{
  console.log(x);       // ❌ ReferenceError — TDZ
  let x = "xxx";        // khai báo trong block
}
// console.log(x);      // ❌ ReferenceError — x không tồn tại ngoài block

// So sánh var trong cùng block:
{
  console.log(y);       // undefined — var hoisted về undefined
  var y = 10;
}
console.log(y);          // 10 — var thoát khỏi block!
```

### Ví dụ 4: Closure + hoisting

```js
function createGreeter(greeting) {
  // greeting được capture trong closure
  return function (name) {
    return `${greeting}, ${name}!`;
  };
}

const sayHi = createGreeter("Xin chào");
console.log(sayHi("Nam"));  // "Xin chào, Nam!"
console.log(sayHi("Hoa"));  // "Xin chào, Hoa!"
// greeting vẫn tồn tại trong closure scope — không bị GC thu hồi
```

### Ví dụ 5: Class TDZ — class cũng có TDZ như let/const

```js
// new Student();        // ❌ ReferenceError — class có TDZ
// class Student {}      // sai thứ tự

class Student {
  constructor(name) {
    this.name = name;
  }
  introduce() {
    return `Tôi là ${this.name}`;
  }
}

const sv = new Student("Lan");
console.log(sv.introduce());  // "Tôi là Lan"
// Đặt class trước khi dùng — tránh TDZ
```

### Ví dụ 6: Thực nghiệm hoisting trong devtools

```js
// Chạy từng dòng trong Console và quan sát:
console.log(typeof foo);   // "function" — function declaration hoisted
function foo() { return 1; }

console.log(typeof bar);   // "undefined" — var hoisted về undefined
var bar = 2;

console.log(typeof baz);   // ❌ ReferenceError — const/let có TDZ
const baz = 3;
```

## 🔬 So sánh với alternatives

| Phương án | Ưu điểm | Nhược điểm |
|-----------|---------|------------|
| **Function declaration (hoisted)** | Gọi trước khi định nghĩa — code tổ chức tự nhiên | Chỉ hoạt động với `function` keyword, không với arrow |
| **Arrow function (không hoisted)** | Cú pháp gọn, `this` lexical | Phải khai báo trước khi dùng — TDZ |
| **Function expression (var)** | Gán động, flexible | Không hoisted — gọi trước sẽ lỗi |
| **ES module top-level** | Import hoisted tự động | Requires module system setup |

## 📊 Performance & Best Practices

- **Ưu tiên khai báo trước khi dùng** — dù `var` hoisted, viết code theo thứ tự tự nhiên giúp đọc dễ hơn.
- **Dùng function declaration cho helper functions** — tận dụng hoist, gọi trước khi định nghĩa.
- **Arrow function nên đặt trước khi gọi** — tránh TDZ confusion.
- **Class declaration nên đặt trước khi instantiate** — class có TDZ như `let`.
- **ESLint `no-use-before-define`** — enforce rule khai báo trước sử dụng, giảm hoisting bug.
- **Không dựa vào hoisting của `var`** — code rely hoisting khó đọc, dễ gây hiểu lầm.

## 🔗 Liên kết chéo

- Xem thêm: `01_variables/01_declarations/` — var vs let vs const so sánh
- Xem thêm: `01_variables/01_declarations/01_let-and-const/` — TDZ chi tiết
- Xem thêm: `01_variables/03_scopes/` — scope chain và hoisting context
- Xem thêm: `09_functions/02_scope-closure-strict-mode/03_closure/` — closure và hoisting trong function scope
- Tài liệu: [MDN — Hoisting](https://developer.mozilla.org/en-US/docs/Glossary/Hoisting), [javascript.info/var](https://javascript.info/var), [javascript.info/let-const](https://javascript.info/let-const)
