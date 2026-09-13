# Hàm — Tham số và Arrow (Parameters & Arrow) — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

Nhóm này bao gồm **cách tạo hàm và truyền dữ liệu vào hàm** trong JavaScript. Six thư mục con lần lượt giải quyết các khía cạnh từ cơ bản đến nâng cao:

| Thư mục | Nội dung | File chính |
|---|---|---|
| `01_callbacks/` | Callback — truyền hàm làm đối số; tự tái tạo `forEach`, `filter`, `some`, `every`, `map` | 6 file JS |
| `02_builtin-functions/` | Các hàm built-in có sẵn: `alert`, `confirm`, `prompt`, `setTimeout`, `setInterval`... | `app.js` |
| `03_arrow-functions/` | Cú pháp arrow `() => {}` và sự khác biệt so với hàm thường (`this`, return ngầm) | `app.js` + `index.html` |
| `04_recursion/` | Đệ quy — hàm gọi chính nó: giai thừa, Fibonacci | `app.js` + `index.html` |
| `05_arguments-object/` | Đối tượng `arguments` array-like ẩn trong hàm thường, dùng rest `...args` thay thế | `app.js` + `index.html` |
| `06_function-parameters/` | Khái niệm tham số/tham đối, default value, rest parameter | `app.js` + `index.html` |

**Hai kiến thức đáng chú ý nhất**:

1. **Params vs Arguments**: *tham số* (parameter) là biến trong khai báo hàm; *tham đối* (argument) là giá trị thực sự truyền khi gọi.
   ```js
   function greet(name, age) { // name, age là parameters
     console.log(name, age);
   }
   greet("Sơn", 18); // "Sơn", 18 là arguments
   ```

2. **Function declaration vs expression vs arrow**: cách thứ nhất được hoisted (dùng được trước khai báo), hai cách còn lại không.
   ```js
   // Hoisted
   hello(); // ✅ chạy được
   function hello() {}

   // Not hoisted
   hi(); // ❌ ReferenceError
   const hi = function() {};
   ```

## 📐 Cấu trúc / Cú pháp

### Callback
```js
function forEach(arr, callback) {
  for (let i = 0; i < arr.length; i++) {
    callback(arr[i], i, arr); // gọi callback với 3 args
  }
}
forEach([1, 2, 3], (val, idx) => console.log(idx, val));
```

### Arrow Function
```js
// Full syntax
const add = (a, b) => { return a + b; };

// Implicit return (1 expression)
const add = (a, b) => a + b;

// Return object — cần ()
const createUser = (name) => ({ name });

// No params
const now = () => new Date();

// One param — () optional
const square = x => x * x;
```

### Recursion
```js
function factorial(n) {
  if (n <= 1) return 1; // base case
  return n * factorial(n - 1); // recursive case
}
```

### Arguments Object
```js
function sum() {
  let total = 0;
  for (let i = 0; i < arguments.length; i++) {
    total += arguments[i];
  }
  return total;
}
sum(1, 2, 3, 4); // 10
```

### Default + Rest Parameters
```js
function greet(name, age = 18, ...rest) {
  console.log(name, age, rest);
}
greet("A", 20, "x", "y"); // A 20 ["x", "y"]
greet();                  // undefined 18 []
```

## ✅ Điểm mạnh

1. **Sắp xếp logic từ dễ đến khó**: callback → built-in → arrow → đệ quy → arguments → params — học từng bước, không bị quá tải.
2. **Các file bài tập tự viết lại phương thức mảng** (`forEach2`, `filter2`...) giúp hiểu cơ chế sâu, không chỉ dùng "thuộc lòng".
3. **Có cả lý thuyết nhẹ** (arguments object) lẫn thực hành (6 file callback) — cân bằng giữa hiểu và làm.
4. **Đa số thư mục con có `app.js` + `index.html`** để chạy ngay trong browser hoặc Node.js.
5. **Bao gồm cả cách viết gọn của arrow** và cách thoát khỏi giới hạn của nó (rest, return object dùng `()`).
6. **Default parameter** loại bỏ hàng trăm dòng kiểu `age = age || 18` thủ công.
7. **Rest parameter `...args`** thay thế `arguments` object — là mảng thật, có `map`, `filter`.
8. **Callback pattern** là nền tảng của event handling, async code, và functional programming.
9. **Recursion giải quyết bài toán phân cấp** tự nhiên hơn loop — tree traversal, flatten, factorial.
10. **Built-in functions** (`setTimeout`, `setInterval`) mở rộng khả năng của JS ra khỏi synchronous execution.
11. **Arrow function implicit return** — code cực kỳ gọn cho transformations: `arr.map(x => x * 2)`.
12. **Mỗi file chạy độc lập** — `node <file>.js` kiểm tra kết quả ngay lập tức.

## ⚠️ Bẫy thường gặp & Hạn chế

1. **Arrow function không có `arguments`, không làm constructor**, và `this` trong arrow là `this` của nơi định nghĩa (không phải nơi gọi).
   ```js
   const obj = {
     name: "Sơn",
     sayName: () => console.log(this.name) // undefined (this là global/Module)
   };
   ```

2. **`arguments` chỉ là array-like**: không có `map`, `filter`... muốn dùng phải `Array.from(arguments)` hoặc chuyển sang rest.
   ```js
   function example() {
     arguments.map(x => x); // TypeError: arguments.map is not a function
     Array.from(arguments).map(x => x); // ✅
   }
   ```

3. **Đệ quy phải có base case** — nếu không sẽ `Maximum call stack size exceeded`.
   ```js
   function bad(n) { return bad(n - 1); } // Infinity recursion
   bad(10); // RangeError: Maximum call stack size exceeded
   ```

4. **Các hàm built-in như `alert`, `confirm`, `prompt` chỉ dùng được trong trình duyệt** — không chạy được trong Node.js thuần.
   ```js
   // Node.js
   alert("hi"); // ReferenceError: alert is not defined
   ```

5. **`eval` được nhắc như hàm built-in nhưng hiện "tránh dùng"** — độc hại (code injection) và chậm (không được JIT optimize).
   ```js
   // ❌ Tránh
   eval("return 2 + 2");
   // ✅ Thay thế
   new Function("return 2 + 2")(); // tương đương, nhưng vẫn không nên dùng
   ```

6. **Default parameter_EVALUATED mỗi lần gọi** — tránh dùng mutable default (object/array).
   ```js
   // ❌ Danger — default array shared across calls
   function bad(items = []) { items.push(1); return items; }
   bad(); // [1]
   bad(); // [1, 1] ← shared mutable default!

   // ✅ Safe
   function good(items = undefined) {
     items = items || [];
     items.push(1);
     return items;
   }
   ```

7. **Rest parameter phải đứng cuối** — `function f(a, ...rest, b)` là SyntaxError.
8. **Arrow function không thể dùng `new`** — `new (() => {})()` throw TypeError.

## 💡 Khi nào dùng

1. **Truyền hành vi cho hàm khác** (callback) — xử lý sự kiện, xử lý danh sách, async completion.
2. **Dùng hàm có sẵn của trình duyệt** cho UI thông báo, hẹn giờ — `alert`, `setTimeout`, `setInterval`.
3. **Viết arrow cho callback ngắn gọn** — tránh mất `this` ở ngoài: `arr.map(x => x * 2)`.
4. **Đệ quy** cho bài toán chia nhỏ lặp lại: thư mục, cây DOM, giai thừa, Fibonacci.
5. **Khai báo tham số mặc định** khi giá trị có thể không truyền vào — `function open(size = 10)`.
6. **Gom thừa số vào `...rest`** khi số lượng đối số không xác định — `function sum(...nums)`.
7. **Dùng `arguments`** trong code legacy hoặc khi cần truy xuất tất cả đối số theo index.
8. **Arrow implicit return** khi hàm chỉ có một biểu thức — code gọn, functional style.

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

### Ví dụ 2: Arrow function + map (file `app.js` trong `03_arrow-functions/`)
```js
const [a] = [1, 2, 3].map(n => n * 2);
console.log(a); // 2

const doubled = [1, 2, 3].map(n => n * 2);
console.log(doubled); // [2, 4, 6]

// Implicit return object — cần ()
const createUser = name => ({ name, id: Date.now() });
console.log(createUser("Sơn")); // { name: "Sơn", id: ... }
```

### Ví dụ 3: Default + Rest parameters (file `app.js` trong `06_function-parameters/`)
```js
function greet(name, age = 18, ...rest) {
  console.log(name, age, rest);
}
greet("A", 20, "x", "y"); // A 20 ["x", "y"]
greet();                  // undefined 18 []
greet("B", null);         // B null [] ← null KHÔNG trigger default!
```

### Ví dụ 4: Recursion — factorial (file `app.js` trong `04_recursion/`)
```js
function factorial(n) {
  return n <= 1 ? 1 : n * factorial(n - 1);
}
console.log(factorial(5)); // 120
console.log(factorial(6)); // 720
```

### Ví dụ 5: Arguments object (file `app.js` trong `05_arguments-object/`)
```js
function f() {
  console.log(arguments);          // Arguments(3) [1, 2, 3]
  console.log(Array.from(arguments)); // [1, 2, 3] — thành mảng thật
  console.log(arguments.length);   // 3
}
f(1, 2, 3);

// Rest parameter — mảng thật, dùng được trong arrow
const arrow = (...args) => console.log(args);
arrow(1, 2); // [1, 2]
```

### Ví dụ 6: Self-reproduce array methods — forEach2 (file `2_foreach.js`)
```js
var courses = ["HTML", "CSS", "JS"];
Array.prototype.forEach2 = function(callBack) {
  for (let key in this) {
    if (this.hasOwnProperty(key)) {
      callBack(this[key], key, this);
    }
  }
};
courses.forEach2((course, index, rootArray) => {
  console.log(course, index, rootArray);
});
// HTML 0 ["HTML","CSS","JS"]
// CSS 1 ["HTML","CSS","JS"]
// JS 2 ["HTML","CSS","JS"]
```

### Ví dụ 7: Tự viết map2 (file `6_map.js`)
```js
var courses = ["HTML", "CSS", "JS", "PHP"];
Array.prototype.map2 = function(callBack) {
  var result = [];
  for (let i = 0; i < this.length; i++) {
    result.push(callBack(this[i], i, this));
  }
  return result;
};
console.log(courses.map2((c, i) => c + " (free)"));
// ["HTML (free)", "CSS (free)", "JS (free)", "PHP (free)"]
```

### Ví dụ 8: Builtin functions — setTimeout (file `app.js` trong `02_builtin-functions/`)
```js
// Chỉ chạy trong browser
setTimeout(() => console.log("setTimeout"), 1000);   // sau 1s in setTimeout
setInterval(() => console.log("setInterval"), 1000); // mỗi 1s in setInterval

// Parser helpers
console.log(parseInt("42px"));    // 42
console.log(parseFloat("3.14"));  // 3.14
console.log(isNaN("abc"));        // true (deprecated — prefer Number.isNaN)
console.log(Number.isNaN("abc")); // false — không ép kiểu
```

### Ví dụ 9: Arrow function trong object method — this behavior
```js
const course = {
  name: "JS Basic",
  // ✅ Function method — this === course
  getName() {
    setTimeout(() => console.log(this.name), 0); // "JS Basic"
  },
  // ❌ Arrow method — this === outer scope (window/Module)
  // getName: () => { setTimeout(() => console.log(this.name), 0); }
};
course.getName();
```

### Ví dụ 10: Arguments vs Rest — so sánh
```js
// Arguments object — array-like, only in regular functions
function sum1() {
  let total = 0;
  for (let i = 0; i < arguments.length; i++) {
    total += arguments[i];
  }
  return total;
}
console.log(sum1(1, 2, 3)); // 6

// Rest parameter — real array, works in arrow
const sum2 = (...nums) => nums.reduce((a, b) => a + b, 0);
console.log(sum2(1, 2, 3)); // 6

// Rest có thể kết hợp với named params
function foo(first, ...rest) {
  console.log(first, rest); // 1 [2, 3]
}
foo(1, 2, 3);
```

## 🔬 So sánh với alternatives

| Tính năng | Function Declaration | Arrow Function | Function Expression |
|---|---|---|---|
| Hoisting | ✅ | ❌ | ❌ |
| `this` dynamic | ✅ | ❌ (lexical) | ✅ |
| `arguments` object | ✅ | ❌ | ✅ |
| Constructor (`new`) | ✅ | ❌ | ✅ |
| Method shorthand | ✅ (`fn() {}`) | ❌ | ✅ |
| Implicit return | ❌ | ✅ | ❌ |
| Concise syntax | ⚠️ | ✅ | ⚠️ |

## 📊 Performance & Best Practices

**Performance**:
- Function declaration slightly faster (engine can hoist and optimize).
- Arrow function has minimal overhead — negligible in practice.
- Recursion without memoization: O(2^n) for naive Fibonacci — use iterative or memoized version.
- Rest parameter slightly faster than `arguments` object access (real array vs array-like).

**Best practices**:
- **Dùng arrow function** cho callback ngắn, array methods, event handlers.
- **Dùng function declaration** cho named functions, object methods, constructors.
- **Luôn có base case** trong recursive functions — test với input nhỏ trước.
- **Dùng rest parameter `...args`** thay `arguments` — modern, real array.
- **Default parameter với immutable values** — tránh object/array default.
- **Arrow implicit return** chỉ cho 1 expression — nhiều câu lệnh dùng `{}` + `return`.
- **Object return trong arrow** cần `()`: `() => ({ key: value })`.
- **Kiểm tra `typeof param === "function"`** trước khi gọi callback — prevent TypeError.
- **Built-in functions** (`alert`, `prompt`) chỉ dùng trong browser — không dùng trong Node.js.
- **Avoid `eval()`** — security risk, performance penalty.

## 🔗 Liên kết chéo

- Callbacks chi tiết: `09_functions/01_parameters-and-arrow/01_callbacks/` — tự viết forEach/filter/map.
- Arrow functions chi tiết: `09_functions/01_parameters-and-arrow/03_arrow-functions/` — this, implicit return.
- Recursion chi tiết: `09_functions/01_parameters-and-arrow/04_recursion/` — factorial, Fibonacci.
- Arguments object: `09_functions/01_parameters-and-arrow/05_arguments-object/` — arguments vs rest.
- Function parameters: `09_functions/01_parameters-and-arrow/06_function-parameters/` — default, rest deep dive.
- Scope & Closure: `09_functions/02_scope-closure-strict-mode/` — closure, IIFE, strict mode.
- Operators: `08_expressions-and-operators/01_operators/` — toán tử trong function expressions.
- Loops: `05_loops-and-iterations/01_loops/` — loop trong function body.
