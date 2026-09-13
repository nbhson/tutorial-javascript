# Hàm (Functions) — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

**Hàm** (function) là **khối code có tên**, nhận tham số đầu vào, thực thi logic, và trả về kết quả — giúp **tái sử dụng** và **chia nhỏ chương trình** thành các phần độc lập, dễ hiểu, dễ test. Trong JavaScript, hàm là **first-class citizens**: có thể gán cho biến, truyền làm đối số, trả về từ hàm khác, và có properties/methods riêng.

JavaScript có **3 cách khai báo hàm** cơ bản, mỗi cách có hành vi khác nhau về **hoisting** (nâng lên đầu scope):

| Cách khai báo | Cú pháp | Hoisted? | `this` | `arguments` |
|---|---|---|---|---|
| Function Declaration | `function name() {}` | ✅ Có | Dynamic | Có |
| Function Expression | `const fn = function() {}` | ❌ Không | Dynamic | Có |
| Arrow Function | `const fn = () => {}` | ❌ Không | Lexical (from parent) | Không |

**Lộ trình học hàm** trong repo này chia làm hai nhóm lớn, đi theo đúng thứ tự roadmap.sh:

### 01_parameters-and-arrow — cách tạo và dùng hàm
| Thư mục | Nội dung | File chính |
|---|---|---|
| `01_callbacks/` | Callback — truyền hàm làm đối số; tự tái tạo `forEach`, `filter`, `some`, `every`, `map` | 6 file JS |
| `02_builtin-functions/` | Các hàm có sẵn của ngôn ngữ/môi trường | `app.js` |
| `03_arrow-functions/` | Cú pháp mũi tên `() => {}` và sự khác biệt với function thường (`this`, return ngầm) | `app.js` + `index.html` |
| `04_recursion/` | Đệ quy — hàm gọi chính nó: giai thừa, Fibonacci | `app.js` + `index.html` |
| `05_arguments-object/` | Object `arguments` ẩn giấu bên trong hàm thường, dùng rest `...args` thay thế | `app.js` + `index.html` |
| `06_function-parameters/` | Tham số: default value, rest parameter `...args` | `app.js` + `index.html` |

### 02_scope-closure-strict-mode — vòng đời và phạm vi của hàm
| Thư mục | Nội dung | File chính |
|---|---|---|
| `01_strict-mode/` | Chế độ nghiêm ngặt `"use strict"` — bật kiểm tra gắt gao | `app.js` + `index.html` |
| `02_iife/` | Hàm được gọi ngay lập tức (IIFE) và tính private | `app.js` + `index.html` |
| `03_closure/` | Hàm nhớ được biến của phạm vi bên ngoài | `app.js` + `index.html` |
| `04_non-blocking-io/` | Lý thuyết: cách JavaScript xử lý bất đồng bộ, không chặn luồng | README only |
| `05_function-stack/` | Call stack (ngăn xếp gọi hàm) và scope chain | `app.js` + `index.html` |

**Tại sao học theo thứ tự này?** Vì mỗi khái niệm xây dựng trên cái trước: callback → hiểu được event handler; arrow function → hiểu được `this`; recursion → hiểu được call stack; closure → hiểu được module pattern; strict mode → hiểu được rules chặt chẽ hơn.

## 📐 Cấu trúc / Cú pháp

### Function Declaration
```js
function greet(name) {
  return "Xin chào " + name;
}
// Hoisted — dùng được trước khi khai báo
console.log(greet("Sơn")); // "Xin chào Sơn"
```

### Function Expression
```js
const greet = function(name) {
  return "Xin chào " + name;
};
// KHÔNG hoisted — phải khai báo trước khi dùng
```

### Arrow Function
```js
const greet = (name) => {
  return "Xin chào " + name;
};
// Implicit return (1 expression body)
const greet = name => "Xin chào " + name;
```

### Default Parameters & Rest
```js
function greet(name, age = 18, ...rest) {
  console.log(name, age, rest);
}
greet("A", 20, "x", "y"); // "A" 20 ["x", "y"]
```

### Callback Pattern
```js
function forEach(arr, callback) {
  for (let i = 0; i < arr.length; i++) {
    callback(arr[i], i, arr);
  }
}
forEach([1, 2, 3], (val) => console.log(val));
```

### Closure
```js
function createCounter() {
  let count = 0;
  return () => ++count;
}
const counter = createCounter();
console.log(counter()); // 1
console.log(counter()); // 2
```

### IIFE
```js
const module = (function() {
  const privateVar = 42;
  return {
    get: () => privateVar
  };
})();
```

## ✅ Điểm mạnh

1. **Tái sử dụng code**: viết một lần, gọi nhiều nơi — giảm trùng lặp khủng khiếp.
2. **Chia nhỏ logic**: hàm nhỏ giúp test, sửa, đọc hiểu dễ hơn — mỗi hàm một trách nhiệm (SRP).
3. **Bóc tách rõ ràng giữa khai báo, biểu thức gán, và arrow** — so sánh trực tiếp từng cách trong cùng repo.
4. **Kèm ví dụ chạy ngay được** trong từng thư mục con — phần lớn có `app.js` + `index.html`.
5. **Đi theo đúng lộ trình roadmap.sh**: từ callback → built-in → arrow → recursion → arguments → params → strict → IIFE → closure → async.
6. **Hệ thống luôn bổ sung kiến thức nền** (strict mode, call stack, closure) — giúp hiểu "tại sao" chứ không chỉ "làm gì".
7. **Callback pattern là nền tảng** của event-driven programming, async code, và functional programming.
8. **Arrow function gọn gàng** — implicit return, lexical `this`, perfect cho callback ngắn.
9. **Closure cho phép private state** — module pattern, counter, cache mà không cần class.
10. **Recursion giải quyết bài toán phân cấp** — duyệt cây, thư mục, JSON lồng nhau tự nhiên hơn loop.
11. **Strict mode phát hiện lỗi sớm** — prevent silent bugs từ khâu viết code.
12. **Call stack + scope chain** — hiểu tại sao code chạy theo thứ tự nào, biến tìm thấy ở đâu.

## ⚠️ Bẫy thường gặp & Hạn chế

1. **Function declaration được hoisted** (dùng được trước khi khai báo), còn function expression và arrow thì **không**.
   ```js
   // ✅ Hoạt động
   hello();
   function hello() { console.log("hi"); }

   // ❌ ReferenceError
   hi();
   const hi = function() { console.log("hi"); };
   ```

2. **Arrow function không có `this`, `arguments` riêng**, không dùng làm constructor — đọc kỹ `03_arrow-functions` trước khi áp dụng.
   ```js
   const obj = {
     name: "Sơn",
     // ❌ Arrow mất this của obj
     getName: () => console.log(this.name), // undefined trong browser
     // ✅ Function method giữ this
     getName() { console.log(this.name); } // "Sơn"
   };
   ```

3. **Callback dễ dẫn tới "callback hell"** (lồng nhau quá sâu) nếu không tổ chức tốt — gợi ý dùng Promise/async sau này.
   ```js
   // ❌ Callback hell
   step1(function(a) {
     step2(a, function(b) {
       step3(b, function(c) {
         step4(c, function(d) {
           // ...
         });
       });
     });
   });
   ```

4. **Đệ quy cần base case rõ ràng** — nếu không sẽ tràn bộ nhớ (stack overflow).
   ```js
   // ❌ Vô hạn — không có base case
   function boom() { boom(); }
   boom(); // Maximum call stack size exceeded

   // ✅ Có base case
   function factorial(n) {
     if (n <= 1) return 1; // base case
     return n * factorial(n - 1);
   }
   ```

5. **`arguments` chỉ có trong hàm thường**, không có trong arrow function — arrow kế thừa `arguments` của scope ngoài.
   ```js
   function regular() { console.log(arguments); }
   regular(1, 2, 3); // Arguments(3) [1, 2, 3]

   const arrow = () => { console.log(arguments); };
   arrow(1, 2); // ReferenceError: arguments is not defined
   ```

6. **Default parameter chỉ áp dụng cho `undefined`**, không áp dụng cho `null` hay `0`.
   ```js
   function greet(name = "Guest") { console.log(name); }
   greet(undefined); // "Guest" ✓
   greet(null);      // "null" ← không dùng default!
   greet(0);         // "0" ← không dùng default!
   ```

7. **Rest parameter phải nằm cuối cùng** — `function f(...args, last)` là SyntaxError.
   ```js
   function sum(...nums) { return nums.reduce((a, b) => a + b, 0); }
   sum(1, 2, 3); // 6 ✓
   // function bad(...a, b) {} // SyntaxError
   ```

8. **Top-level `03_this-and-binding` trong roadmap.sh chưa có thư mục** trong repo này — kiến thức `this` được đề cập sơ bộ trong `03_arrow-functions` và `01_strict-mode`.

## 💡 Khi nào dùng

1. **Đóng gói các thao tác lặp lại**: format dữ liệu, tính toán, gọi API — viết một lần, dùng nhiều nơi.
2. **Xử lý danh sách bằng callback/map/filter** thay vì viết vòng lặp tay — code functional, dễ đọc.
3. **Tổ chức ứng dụng theo hướng hàm nhỏ ghép lại** (functional programming style) — mỗi hàm pure, testable.
4. **Hiểu đệ quy** cho các bài toán chia nhỏ: duyệt cây, thư mục, JSON lồng nhau, backtracking.
5. **Làm quen với closure** cho các pattern như counter, module, memoization, React hooks.
6. **Dùng arrow function** cho callback ngắn, event handler, promise chain — giữ `this` từ outer scope.
7. **Dùng IIFE** khi cần private scope trong script cũ (trước ES6 modules).
8. **Bật strict mode** cho mọi file mới — prevent silent bugs, enforce better coding practices.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Callback cơ bản (file `1_call-back.js`)
```js
function myFunction(param) {
  if (typeof param === "function") {
    param("Sơn Nguyễn"); // gọi callback
  }
}
function myCallback(value) {
  console.log("Value:", value);
}
myFunction(myCallback); // "Value: Sơn Nguyễn"
```

### Ví dụ 2: Arrow function (file `app.js` trong `03_arrow-functions/`)
```js
// Function declaration
function myFunc1(param) { console.log(param); }

// Function expression
const myFunc2 = function(param) { console.log(param); };

// Arrow function
const myFunc3 = (param) => { console.log(param); };

// Implicit return
const double = n => n * 2;
console.log(double(5)); // 10
```

### Ví dụ 3: Recursion — giai thừa (file `app.js` trong `04_recursion/`)
```js
function factorial(n) {
  return n <= 1 ? 1 : n * factorial(n - 1);
}
console.log(factorial(5)); // 120
console.log(factorial(6)); // 720
```

### Ví dụ 4: Arguments object (file `app.js` trong `05_arguments-object/`)
```js
function f() {
  console.log(arguments);          // Arguments(3) [1, 2, 3]
  console.log(Array.from(arguments)); // [1, 2, 3]
  console.log(arguments.length);   // 3
}
f(1, 2, 3);
```

### Ví dụ 5: Default + Rest parameters (file `app.js` trong `06_function-parameters/`)
```js
function greet(name, age = 18, ...rest) {
  console.log({ name, age, rest });
}
greet("A", 20, "x", "y"); // { name: "A", age: 20, rest: ["x", "y"] }
greet();                  // { name: undefined, age: 18, rest: [] }
```

### Ví dụ 6: Closure — biến đếm (file `app.js` trong `03_closure/`)
```js
function createCounter() {
  let count = 0;
  return () => ++count;
}
const c = createCounter();
console.log(c(), c(), c()); // 1 2 3
```

### Ví dụ 7: IIFE — module private (file `app.js` trong `02_iife/`)
```js
const app = (function() {
  const cars = []; // private
  return {
    add: car => cars.push(car),
    all: () => [cars]
  };
})();
app.add("Winner 2022");
console.log(app.all()); // [["Winner 2022"]]
```

### Ví dụ 8: Strict mode (file `app.js` trong `01_strict-mode/`)
```js
"use strict";
function test() {
  console.log(this); // undefined (không phải window/global)
}
test();
```

### Ví dụ 9: Non-blocking I/O concept (file `04_non-blocking-io/` README)
```js
console.log("1. bắt đầu");
setTimeout(() => console.log("3. timer xong (bất đồng bộ)"), 0);
console.log("2. chạy tiếp ngay — không bị chặn");
// Kết quả: 1. bắt đầu → 2. chạy tiếp → 3. timer xong
```

### Ví dụ 10: Call stack trace (file `app.js` trong `05_function-stack/`)
```js
function a() { b(); }
function b() { c(); }
function c() {
  console.log("stack:");
  console.trace(); // in ra a → b → c
}
a();
```

## 🔬 So sánh với alternatives

| Tình huống | Function Declaration | Arrow Function | Function Expression |
|---|---|---|---|
| Cần hoisting | ✅ Dùng | ❌ Không | ❌ Không |
| Cần `this` dynamic | ✅ Dùng | ❌ Không (lexical) | ✅ Dùng |
| Cần `arguments` object | ✅ Dùng | ❌ Không | ✅ Dùng |
| Callback ngắn gọn | ⚠️ Dài dòng | ✅ Perfect | ⚠️ Dài dòng |
| Constructor / prototype | ✅ Dùng | ❌ Không | ✅ Dùng |
| Method của object | ⚠️ Được | ❌ Mất `this` | ✅ Dùng |

## 📊 Performance & Best Practices

**Performance**:
- Function declaration slightly faster than expression (engine can optimize).
- Arrow function có overhead nhỏ do lexical binding nhưng negligible trong practice.
- Recursive function không có tail-call optimization trong JavaScript engines hiện tại (trừ Safari).
- Avoid deep recursion (>10k frames) — stack overflow risk.

**Best practices**:
- **Dùng arrow function** cho callback ngắn, event handler, array methods.
- **Dùng function declaration** cho named functions cần hoisting, object methods.
- **Dùng function expression** khi cần `this` dynamic và không muốn hoisting.
- **Always add base case** trong recursive functions.
- **Dùng rest parameter `...args`** thay `arguments` object — modern, array thực sự.
- **Dùng default parameters** thay `arg = arg || default` — xử lý đúng `0`, `""`, `false`.
- **Bật `"use strict"`** ở đầu mọi file mới.
- **Giữ hàm nhỏ** (<30 lines), một trách nhiệm — dễ test, dễ đọc.
- **Avoid callback hell** — dùng Promise/async-await thay thế.
- **Hiểu call stack** để debug stack overflow và tối ưu recursion.

## 🔗 Liên kết chéo

- Callbacks chi tiết: `09_functions/01_parameters-and-arrow/01_callbacks/` — tự viết lại forEach/filter/map.
- Built-in functions: `09_functions/01_parameters-and-arrow/02_builtin-functions/` — alert, setTimeout, setInterval.
- Arrow functions: `09_functions/01_parameters-and-arrow/03_arrow-functions/` — cú pháp, `this`, implicit return.
- Recursion: `09_functions/01_parameters-and-arrow/04_recursion/` — factorial, Fibonacci, flatten.
- Arguments object: `09_functions/01_parameters-and-arrow/05_arguments-object/` — array-like arguments, rest parameter.
- Function parameters: `09_functions/01_parameters-and-arrow/06_function-parameters/` — default, rest params.
- Strict mode: `09_functions/02_scope-closure-strict-mode/01_strict-mode/` — "use strict" rules.
- IIFE: `09_functions/02_scope-closure-strict-mode/02_iife/` — immediate invocation, private scope.
- Closure: `09_functions/02_scope-closure-strict-mode/03_closure/` — closure pattern, memory leak.
- Non-blocking I/O: `09_functions/02_scope-closure-strict-mode/04_non-blocking-io/` — async concept theory.
- Call stack: `09_functions/02_scope-closure-strict-mode/05_function-stack/` — execution context, scope chain.
- Điều kiện: `06_control-flow/01_conditionals/5_condition/` — if/switch/ternary trong function body.
- Loop: `05_loops-and-iterations/01_loops/` — vòng lặp trong function.
- Operators: `08_expressions-and-operators/01_operators/` — toán tử trong function expression.
