# Functions as Objects (Hàm cũng là object) — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

Ở JavaScript, **hàm về bản chất cũng là một object đặc biệt** — bạn có thể "gọi" nó như hàm, nhưng nó vẫn mang đầy đủ đặc tính của object: có property, phương thức, có thể gán vào biến, truyền vào hàm khác. Vì vậy JS có **first-class functions** (xem `00_introduction/01_what-is-javascript/01_first-class-function`).

### Cơ chế hoạt động trong JavaScript engine

Khi tạo một function, engine tạo một **Function object** trên heap với:
1. **Internal slot `[[Call]]`** — đánh dấu object là callable (có thể gọi `()`).
2. **`prototype` property** — object chứa method sẽ chia sẻ cho instances qua `new`.
3. **`[[Environment]]`** — reference đến lexical scope nơi function được tạo (nền tảng của **closure**).
4. **`name` property** — tên hàm (từ function name hoặc variable name khi assign).
5. **`length` property** — số lượng formal parameters.

```js
function greet(name) { return `Hi, ${name}`; }
console.log(typeof greet);         // "function" (special typeof!)
console.log(greet instanceof Function); // true
console.log(greet.name);           // "greet"
console.log(greet.length);         // 1 — số parameters
console.log(typeof greet === "function" && typeof greet === "object");
// false — typeof function trả "function", không phải "object" (spec special case)
```

### 3 cách tạo hàm

```js
// 1. Function declaration — được hoisting (gọi trước vẫn chạy)
function func_1() {}

// 2. Function expression — gán hàm cho biến, KHÔNG hoisting
var func_2 = function () {};

// 3. Arrow function (anonymous) — thường làm callback
setTimeout(() => {}, 1000);
```

### Truyền tham số — Function có `arguments` object

Bên trong một function (không phải arrow), `arguments` là một **array-like object** chứa tất cả đối số đã truyền:

```js
function argumentFunc() {
  console.log(arguments);
  // { '0': 'LOG 1', '1': 'LOG 2', '2': 'LOG 3', length: 3 }
  for (const item of arguments) {
    console.log(item);  // LOG 1 / LOG 2 / LOG 3
  }
}
argumentFunc('LOG 1', 'LOG 2', 'LOG 3');
```

> **Lưu ý:** `arguments` **chỉ tồn tại trong regular function**. Arrow function **không có `arguments`** — dùng rest parameter `(...args)` thay thế.

### Return — mặc định là `undefined`

Nếu hàm không có `return`, kết quả trả về mặc định là **`undefined`**.

```js
function noReturn() {}
console.log(noReturn()); // undefined

function explicitUndefined() { return; }
console.log(explicitUndefined()); // undefined
```

### Các dạng hàm trong object

```js
var obj1 = {
  myFunc: function () {},   // property chứa function
};

var obj2 = {
  myFunc() {},              // ES6 shorthand method — cùng tác dụng
};

console.log(obj1.myFunc.name); // "myFunc" — both have name
console.log(obj2.myFunc.name); // "myFunc"
```

## 📐 Cấu trúc nhóm

```
02_data-types/02_objects-and-prototype/02_functions-as-objects/
├── README.md                 ← bài này
├── 1_app.js                  ← function cơ bản, arguments, return undefined
└── 2_Cac-loai-function.js    ← declaration, expression, anonymous, method
```

## ✅ Điểm mạnh — Tại sao hàm là object

| # | Điểm mạnh | Lý do |
|---|-----------|-------|
| 1 | **Hoisting cho function declaration** | Gọi trước khi định nghĩa — tổ chức code linh hoạt hơn |
| 2 | **Function có property/method** | `name`, `length`, `call()`, `apply()`, `bind()` — introspection hữu ích |
| 3 | **First-class citizen** | Gán, truyền, trả về — nền tảng functional programming |
| 4 | **Closure** | Function giữ reference đến lexical scope — state persistence |
| 5 | **Higher-order functions** | `map(fn)`, `filter(fn)`, `reduce(fn)` — nhận/return function |
| 6 | **Method shorthand (ES6)** | `{ greet() {} }` — clean syntax, cùng behavior |
| 7 | **Named function expressions** | `const fn = function name() {}` — tên function cho stack trace |

## ⚠️ Bẫy thường gặp & Hạn chế

| # | Bẫy | Ví dụ | Cách tránh |
|---|-----|-------|-----------|
| 1 | **Declaration hoisted, expression NOT** | `foo(); const foo = () => {};` → ReferenceError | Dùng `function` keyword cho hoisted functions |
| 2 | **Arrow function không có `arguments`** | `const f = () => arguments` → ReferenceError | Dùng rest params `(...args)` trong arrow |
| 3 | **Không có `return` → `undefined`** | `function f(){ "hello"; }` → `undefined` — thiếu `return` keyword | Luôn kiểm tra return statement |
| 4 | **`this` different between function types** | Arrow: lexical `this`; function: dynamic `this` | Hiểu `this` binding rules |
| 5 | **`typeof fn === "function"` special case** | `typeof` trả "function", không "object" | `instanceof Function` để kiểm tra callable |
| 6 | **Named function expression name leak** | `var f = function foo(){};` → `foo` accessible only inside function | Not a bug, but can confuse |
| 7 | **Function `length` excludes rest/default** | `function f(a, b=1, ...rest){}` → `f.length === 1` | Remember: only up to first non-simple param |

## 💡 Khi nào dùng — Tình huống thực tế

1. **Tổ chức code có mục** — function declaration hoisted, utility functions đặt dưới, logic chính ở trên.
2. **Callback pattern** — `setTimeout(fn, ms)`, `addEventListener(event, handler)`, `arr.map(transform)`.
3. **Function là object** — dùng `fn.name`, `fn.length` cho debugging, library introspection.
4. **Method shorthand** — `const api = { getUser() {}, setUser() {} }` — clean API objects.
5. **IIFE pattern** — `(function() { /* private scope */ })()` — encapsulation.
6. **Factory functions** — `function createValidator(rules) { return (value) => {...} }` — returns configured function.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Function declaration vs expression — hoisting difference

```js
// Function declaration — HOISTED, gọi trước được
console.log(sum(2, 3)); // 5 ✓
function sum(a, b) { return a + b; }

// Function expression — NOT hoisted, gọi trước sẽ lỗi
// console.log(sub(5, 2)); // ❌ TypeError: sub is not a function
var sub = function (a, b) { return a - b; };
console.log(sub(5, 2)); // 3 — gọi sau khi assign

// Arrow function — NOT hoisted (it's a const/let)
// console.log(div(6, 2)); // ❌ ReferenceError
const div = (a, b) => a / b;
console.log(div(6, 2)); // 3
```

### Ví dụ 2: Function properties — name, length

```js
function greet(name, age) {
  return `Hi ${name}, ${age} years old`;
}

// Function properties — like object properties
console.log(typeof greet);      // "function"
console.log(greet.name);        // "greet" — function name
console.log(greet.length);      // 2 — số formal parameters
console.log(greet.prototype);   // {} — prototype object for constructor

// Anonymous function — name comes from variable
const anonymous = function () {};
console.log(anonymous.name);    // "anonymous"

// Named function expression — name is function name, not variable
const named = function myRealName() {};
console.log(named.name);        // "myRealName"
// myRealName();               // ❌ ReferenceError — name only accessible inside
```

### Ví dụ 3: `arguments` object — access all passed args

```js
function logAll() {
  console.log(arguments);           // { '0': 'a', '1': 'b', '2': 'c', length: 3 }
  console.log(arguments.length);    // 3

  // Iterate with for...of
  for (const arg of arguments) {
    console.log(arg);               // a, b, c
  }

  // Convert to real array
  const argsArray = Array.from(arguments);
  console.log(argsArray.map(x => x.toUpperCase())); // ["A", "B", "C"]
}
logAll('a', 'b', 'c');

// Modern: rest parameter thay thế arguments
function logAllRest(...args) {
  console.log(args.map(x => x.toUpperCase())); // ["A", "B", "C"] — args is real Array!
}
logAllRest('a', 'b', 'c');
```

### Ví dụ 4: Functions in objects — method patterns

```js
const calculator = {
  result: 0,

  // Regular method — `this` binds to calculator
  add(num) {
    this.result += num;
    return this; // chaining!
  },

  // ES6 shorthand method
  subtract(num) {
    this.result -= num;
    return this;
  },

  // Property holding function
  multiply: function (num) {
    this.result *= num;
    return this;
  },

  // Arrow method — DANGER: `this` from lexical scope, not object!
  // divide: (num) => { this.result /= num; return this; } // ❌ this ≠ calculator

  reset() {
    this.result = 0;
    return this;
  },
};

// Method chaining — each returns `this`
calculator.reset().add(10).subtract(3).multiply(2);
console.log(calculator.result); // 14
```

### Ví dụ 5: Higher-order function — function as parameter

```js
// Takes a function as parameter and returns a new function
function once(fn) {
  let called = false;
  let result;
  return function (...args) {
    if (!called) {
      called = true;
      result = fn.apply(this, args);
    }
    return result; // cached first call result
  };
}

let initialize = 0;
const initOnce = once(() => {
  initialize++;
  return `initialized ${initialize} times`;
});

console.log(initOnce()); // "initialized 1 times"
console.log(initOnce()); // "initialized 1 times" — only runs once!
console.log(initOnce()); // "initialized 1 times"
```

### Ví dụ 6: Function as object — adding properties dynamically

```js
function counter() {
  counter.count++;
  return counter.count;
}
counter.count = 0; // Add property to function object

console.log(counter()); // 1
console.log(counter()); // 2
console.log(counter()); // 3
console.log(counter.count); // 3

// Common pattern: add utility methods to functions
function formatDate(date) {
  return date.toLocaleDateString("vi-VN");
}
formatDate.ISO = (date) => date.toISOString(); // static-like method

console.log(formatDate(new Date()));     // local format
console.log(formatDate.ISO(new Date())); // ISO format
```

## 🔬 So sánh với alternatives

| Loại function | Hoisted? | Has `this`? | Has `arguments`? | Prototype? | Use when |
|--------------|----------|-------------|------------------|------------|----------|
| **Declaration** `function f() {}` | ✅ Yes | Dynamic | ✅ Yes | ✅ Yes | Utility functions, methods |
| **Expression** `var f = function() {}` | ❌ No | Dynamic | ✅ Yes | ✅ Yes | Assigned functions, conditional |
| **Arrow** `const f = () => {}` | ❌ No | Lexical | ❌ No | ❌ No | Callbacks, lexical `this`, concise |
| **Method shorthand** `{ f() {} }` | ❌ No | Dynamic | ✅ Yes | ❌ No | Object methods |
| **Constructor** `function F() {}` | ✅ Yes | New instance | ✅ Yes | ✅ Yes | Class pattern (with `new`) |

## 📊 Performance & Best Practices

- **Dùng function declaration** cho helper/utility functions — hoisting giúp tổ chức code tự nhiên.
- **Dùng arrow function** cho short callbacks và khi muốn lexical `this`.
- **Dùng rest parameter** `(...args)` thay `arguments` object — cleaner, real array.
- **Dùng ES6 method shorthand** cho object methods — concise syntax.
- **Tránh `arguments` trong arrow function** — không có `arguments`, sẽ ReferenceError.
- **Dùng `Array.from(arguments)`** nếu cần full Array methods trên arguments.
- **Method chaining** — return `this` từ mỗi method để tạo fluent API.

## 🔗 Liên kết chéo

- Xem thêm: `00_introduction/01_what-is-javascript/01_first-class-function/` — first-class function concept
- Xem thêm: `01_variables/02_hoisting/` — function hoisting chi tiết
- Xem thêm: `02_data-types/02_objects-and-prototype/01_object-basics/` — constructor function
- Xem thêm: `09_functions/01_parameters-and-arrow/03_arrow-functions/` — arrow function deep dive
- Xem thêm: `10_this-keyword/` — `this` binding trong regular function vs arrow
- Tài liệu: [MDN — Functions](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions), [javascript.info/function-basics](https://javascript.info/function-basics)
