# Arrow Functions (Hàm mũi tên) — Thực hành chi tiết — [Level: Intermediate]

## 🔑 Khái niệm cốt lõi

**Arrow function** là cú pháp viết hàm **ngắn gọn** với ký hiệu `=>`, ra đời từ **ES6 (ECMAScript 2015)**. Có ba cách viết function cho cùng một việc (file `app.js`):

```js
// 1. Function declaration
function myFunc1(param) { console.log(param); }

// 2. Function expression
const myFunc2 = function (param) { console.log(param); };

// 3. Arrow function
const myFunc3 = (param) => { console.log(param); };
```

**Ba quy tắc viết ngắn của arrow** (file `app.js` demo đầy đủ):

| Trường hợp | Cú pháp | Ghi chú |
|---|---|---|
| Có thân `{}` | `(a, b) => { return a + b; }` | cần `return` như thường |
| Thân một biểu thức | `(a, b) => a + b` | **tự trả về** (implicit return) |
| Trả về object | `(a, b) => ({ a, b })` | phải bọc `()` vì `{}` bị hiểu là thân hàm |
| Một tham số | `log => console.log(log)` | có thể bỏ ngoặc `()` |
| Không tham số | `() => 42` | bắt buộc có `()` |

**Khu vực nguy hiểm** (được demo ở cuối `app.js`):

1. **Arrow không có `this` riêng** — `this` trong arrow chính là `this` ở nơi hàm được *định nghĩa* (lexical this). Nên với object method dùng arrow, `this` sẽ không phải object đó.
2. **Arrow không thể dùng làm constructor**: `new funcConstruct(1, 2)` với arrow → lỗi (`TypeError: funcConstruct is not a constructor`).
3. **Arrow không có `arguments`** riêng — kế thừa `arguments` của scope ngoài (xem `05_arguments-object`).

**Cơ chế `this` lexical**: arrow function không tự tạo `this` mới — nó **giữ nguyên `this` từ môi trường bao quanh** (where it's defined, not where it's called). Điều này khác biệt căn bản so với regular function có `this` dynamic (dựa vào cách gọi).

## 📐 Cấu trúc / Cú pháp

### Cú pháp cơ bản
```js
// Không tham số
const noop = () => {};

// Một tham số — () optional
const square = x => x * x;

// Nhiều tham số — bắt buộc ()
const add = (a, b) => a + b;

// Body nhiều dòng — cần {} và return
const greet = (name) => {
  const msg = `Xin chào, ${name}!`;
  return msg;
};

// Return object — cần () bọc
const createUser = (name) => ({ name, id: Date.now() });
```

### Arrow trong array methods
```js
const numbers = [1, 2, 3];
const doubled = numbers.map(n => n * 2);       // [2, 4, 6]
const evens = numbers.filter(n => n % 2 === 0); // [2]
const sum = numbers.reduce((a, b) => a + b, 0); // 6
```

### Arrow giữ this từ outer scope
```js
const obj = {
  name: "Sơn",
  // ✅ Function method — this dynamic
  getName() {
    return this.name;
  },
  // ✅ Arrow trong method — this lexical (giữ this của getName)
  get_name_arrow() {
    const inner = () => this.name;
    return inner();
  },
  // ❌ Arrow property — this là outer scope (window/Module)
  badName: () => this.name
};
```

### Arrow không có arguments
```js
// Regular function — có arguments object
function regular() {
  console.log(arguments); // Arguments(2) [1, 2]
}
regular(1, 2);

// Arrow function — không có arguments riêng
const arrow = (...args) => console.log(args); // [1, 2]
arrow(1, 2);

// Arrow kế thừa arguments từ outer regular function
function outer() {
  const inner = () => console.log(arguments);
  inner();
}
outer(1, 2); // Arguments(2) [1, 2]
```

## ✅ Điểm mạnh

1. **Ngắn gọn** — đặc biệt với callback `value => value * 2` — code sạch, ít characters hơn nhiều so với `function(value) { return value * 2; }`.
2. **Implicit return** — viết tỉnh bất kỳ biểu thức nào là hàm trả về luôn — không cần `return` keyword.
3. **`this` tĩnh (lexical)** — rất tiện khi làm việc với event handler, timer, promise: không lo bị đổi `this` như function thường.
4. **Bọc `({...})` để trả object gọn và đẹp** — phù hợp kiểu "functional" với array methods.
5. **Không ghi từ khóa `function`** — code sạch hơn, giảm boilerplate.
6. **Là chuẩn viết hiện đại** trong phần lớn dự án JS/React/Vue — codebase hiện đại đều dùng arrow.
7. **Perfect cho one-liner callbacks** — `arr.map(x => x.id)` đọc như ngôn ngữ tự nhiên.
8. **Arrow property trong object literal** — ngắn gọn cho utility functions (nhưng lưu ý `this` limitation).
9. **Default parameters work** với arrow — `const add = (a = 0, b = 0) => a + b;`.
10. **Rest parameters work** — `const sum = (...nums) => nums.reduce((a, b) => a + b, 0);`.

## ⚠️ Bẫy thường gặp & Hạn chế

1. **Không có `this`, `arguments`, `new.target` riêng** — không phù hợp làm method của object, constructor, hoặc cần dynamic `this`.
   ```js
   const obj = {
     name: "Sơn",
     // ❌ Arrow mất this của obj
     getName: () => console.log(this.name), // undefined (trong module context)
     // ✅ Function method giữ this
     getName() { console.log(this.name); } // "Sơn"
   };
   ```

2. **Implicit return đôi khi gây nhầm**: muốn trả object mà quên `()` → lỗi `SyntaxError`.
   ```js
   // ❌ SyntaxError — { } bị hiểu là function body
   const getUser = (name) => { name: name };
   // ✅ Đúng — bọc object trong ()
   const getUser = (name) => ({ name });
   ```

3. **Không hoisted** như function declaration — phải khai báo trước khi dùng.
   ```js
   // ❌ ReferenceError
   hello();
   const hello = () => console.log("hi");
   // ✅ Đúng
   const hello = () => console.log("hi");
   hello();
   ```

4. **Không dùng được với `new`** — arrow không phải constructor.
   ```js
   const Person = (name) => { this.name = name; };
   new Person("Sơn"); // TypeError: Person is not a constructor
   ```

5. **Không dùng được làm method trong object literal** nếu cần `this` trỏ object.
   ```js
   const calculator = {
     value: 0,
     // ❌ Arrow method — this không trỏ calculator
     add: (n) => { this.value += n; },
     // ✅ Function method
     subtract(n) { this.value -= n; }
   };
   ```

6. **Arrow trong object property** — `this` trỏ outer scope, thường là `undefined` (strict mode) hoặc `window` (non-strict).
   ```js
   const course = {
     name: "JS Basic",
     // ❌ Arrow property — this === window/undefined
     getName: () => this.name,
     // ✅ Method shorthand — this === course
     getName() { return this.name; }
   };
   ```

7. **Khó debug stack trace** — arrow function không có tên trong stack (trừ khi gán cho variable có tên).
   ```js
   const fn = () => {};
   throw new Error(); // stack: Error at fn (...)
   // vs
   function namedFn() {} // stack: Error at namedFn (...)
   ```

8. **Không thể dùng `yield`** — arrow không thể là generator function.

## 💡 Khi nào dùng

1. **Callback ngắn**: `arr.map(x => x * 2)`, `arr.filter(c => c.price > 100)` — gọn, rõ ràng.
2. **Truyền hàm cho `setTimeout`**, event listener, promise chain — giữ `this` từ outer scope.
3. **Hàm tiện ích không cần thay đổi `this`** — pure function, utility helpers.
4. **Viết hàm một biểu thức** để tăng tính biểu cảm — functional style.
5. **React props handlers**: `onClick={(e) => handleClick(e)}` — giữ context.
6. **Array method callbacks** — `map`, `filter`, `reduce`, `sort` đều perfect với arrow.
7. **IIFE arrow** — ``(a, b) => a + b ``(1, 2)`` — immediate invoke ngắn gọn.
8. **Default/REST parameters** — arrow support đầy đủ như regular function.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Ba cách viết hàm (file `app.js`)
```js
// 1. Function declaration
function myFunc1(param) { console.log(param); }

// 2. Function expression
const myFunc2 = function (param) { console.log(param); };

// 3. Arrow function
const myFunc3 = (param) => { console.log(param); };

myFunc1("hello"); // hello
myFunc2("hello"); // hello
myFunc3("hello"); // hello
```

### Ví dụ 2: Implicit return (file `app.js`)
```js
// Có thân {} — cần return
const func1 = (a, b) => { return a + b; };

// Thân 1 biểu thức — implicit return
const func2 = (a, b) => a + b;        // tự return
const func3 = (a, b) => ({ a, b });   // return object cần ()

console.log(func2(2, 3));    // 5
console.log(func3(2, 3));    // { a: 2, b: 3 }

// Single param — () optional
const log = msg => console.log(msg);
log("arrow with one param");

// No param — () required
const now = () => new Date();
console.log(now()); // Date {...}
```

### Ví dụ 3: Arrow trong array methods
```js
const numbers = [1, 2, 3, 4, 5];

// map
const doubled = numbers.map(n => n * 2);
console.log(doubled); // [2, 4, 6, 8, 10]

// filter
const evens = numbers.filter(n => n % 2 === 0);
console.log(evens); // [2, 4]

// reduce
const sum = numbers.reduce((acc, n) => acc + n, 0);
console.log(sum); // 15

// sort
const sorted = [3, 1, 4, 1, 5].sort((a, b) => a - b);
console.log(sorted); // [1, 1, 3, 4, 5]
```

### Ví dụ 4: this trong arrow — lexical binding (file `app.js`)
```js
// Arrow giữ this của nơi định nghĩa
const course = {
  name: "JS Basic",
  getName() {
    // setTimeout với arrow — this giữ của getName (=== course)
    setTimeout(() => console.log(this.name), 0); // "JS Basic"
  },
  // ❌ Arrow property — this === outer scope (window/Module)
  // badName: () => console.log(this.name) // undefined
};
course.getName();

// So sánh với regular function mất this
const course2 = {
  name: "JS Basic",
  getNameRegular() {
    setTimeout(function() {
      console.log(this.name); // undefined — this === window
    }, 0);
  }
};
course2.getNameRegular();
```

### Ví dụ 5: Arrow không dùng được làm constructor
```js
// ❌ Arrow không phải constructor
const Person = (name, age) => {
  this.name = name;
  this.age = age;
};
new Person("Sơn", 18); // TypeError: Person is not a constructor

// ✅ Dùng function declaration làm constructor
function Person(name, age) {
  this.name = name;
  this.age = age;
}
const son = new Person("Sơn", 18);
console.log(son.name); // "Sơn"
```

### Ví dụ 6: Object return với () — trick quan trọng
```js
// ❌ SyntaxError — { } bị hiểu là function body
const badUser = name => { name: name, id: 1 };

// ✅ Đúng — () bọc object
const goodUser = name => ({ name, id: 1 });
console.log(goodUser("Sơn")); // { name: "Sơn", id: 1 }

// Ứng dụng: factory function
const createStudent = (name, grade) => ({
  name,
  grade,
  toString() { return `${name} - lớp ${grade}`; }
});
console.log(createStudent("Sơn", 12).toString()); // "Sơn - lớp 12"
```

### Ví dụ 7: this trong object method — so sánh
```js
const user = {
  firstName: "Nguyễn",
  lastName: "Sơn",
  // ✅ Method shorthand — this === user
  getFullName() {
    return `${this.firstName} ${this.lastName}`;
  },
  // ❌ Arrow property — this !== user
  // getFullNameArrow: () => `${this.firstName} ${this.lastName}`,
  // ✅ Arrow trong method — this === user (lexical từ getFullName)
  getFullNameWithArrow() {
    const getFirst = () => this.firstName;
    const getLast = () => this.lastName;
    return `${getFirst()} ${getLast()}`;
  }
};
console.log(user.getFullName());           // "Nguyễn Sơn"
console.log(user.getFullNameWithArrow());  // "Nguyễn Sơn"
// console.log(user.getFullNameArrow());   // "undefined undefined"
```

### Ví dụ 8: Arrow với default + rest parameters
```js
// Default parameters
const greet = (name = "Guest", greeting = "Xin chào") =>
  `${greeting}, ${name}!`;
console.log(greet());              // "Xin chào, Guest!"
console.log(greet("Sơn"));         // "Xin chào, Sơn!"
console.log(greet("Sơn", "Hello")); // "Hello, Sơn!"

// Rest parameters
const sum = (...nums) => nums.reduce((a, b) => a + b, 0);
console.log(sum(1, 2, 3, 4)); // 10

// Kết hợp default + rest
const partition = (prefix, ...items) =>
  items.map(item => `${prefix}_${item}`);
console.log(partition("user", "admin", "guest")); // ["user_admin", "user_guest"]
```

### Ví dụ 9: Curry với arrow function
```js
// Curry — transform multi-arg function into sequence of unary functions
const add = a => b => a + b;
const add5 = add(5);
console.log(add5(3)); // 8
console.log(add(2)(3)); // 5

// Ứng dụng thực tế: API builder
const createFetcher = baseUrl => endpoint => `/api/${baseUrl}/${endpoint}`;
const usersApi = createFetcher("users");
console.log(usersApi("list"));    // "/api/users/list"
console.log(usersApi("details")); // "/api/users/details"
```

### Ví dụ 10: IIFE với arrow
```js
// Regular IIFE
(const function() { return 42; })();

// Arrow IIFE
((a, b) => a + b)(1, 2); // 3
(() => "hello")();        // "hello"

// Arrow IIFE với params
const result = ((x) => x * x)(5); // 25
console.log(result);
```

## 🔬 So sánh với alternatives

| Tính năng | Arrow Function | Regular Function |
|---|---|---|
| `this` binding | Lexical (from definition) | Dynamic (from call) |
| `arguments` object | ❌ Không có | ✅ Có |
| Can be constructor | ❌ Không | ✅ Có |
| Hoisting | ❌ Không | ✅ Có (declaration only) |
| Syntax | Ngắn gọn | Dài dòng hơn |
| Implicit return | ✅ Có | ❌ Không |
| Generator support | ❌ Không | ✅ Có |
| Use in object method | ⚠️ Limitations | ✅ Full support |

## 📊 Performance & Best Practices

**Performance**:
- Arrow function có overhead nhỏ do lexical `this` binding — thường <5% so với regular function.
- Không đáng kể trong hầu hết applications — ưu tiên readability.
- V8 JIT optimize cả hai loại similarly sau warm-up.

**Best practices**:
- **Dùng arrow cho callback** — `map`, `filter`, `forEach`, event handlers.
- **Dùng regular function** cho object methods cần `this`, constructors, prototype methods.
- **Luôn bọc object trong `()`** khi implicit return object: `() => ({ key: value })`.
- **Dùng `()` even cho single param** khi có type annotation (TypeScript) hoặc clarity.
- **Tránh arrow trong object property** nếu cần `this` trỏ object — dùng method shorthand.
- **Arrow trong class field** (React component) — giữ `this` của instance: ` handleClick = () => {}`.
- **Named arrow function** cho debug-friendly stack traces: `const fn = function name() {}` hoặc named export.
- **Không dùng arrow làm Promise executor** nếu cần `this` — regular function hoặc bind.
- **Arrow trong reduce accumulator** — `(acc, val) => acc + val` — chuẩn functional pattern.
- **Test arrow vs regular** — nếu `this` behavior sai, switch sang regular function.

**Quy tắc "3 nên — 3 không"**:
- ✅ Nên dùng arrow cho array methods và callbacks.
- ✅ Nên bọc object trong `()` khi implicit return.
- ✅ Nên dùng arrow trong class fields để giữ `this`.
- ❌ Không nên dùng arrow làm object method nếu cần `this`.
- ❌ Không nên dùng arrow làm constructor (`new`).
- ❌ Không nên dùng arrow khi cần `arguments` object.

## 🔗 Liên kết chéo

- Callbacks: `09_functions/01_parameters-and-arrow/01_callbacks/` — arrow trong callback pattern.
- Arguments object: `09_functions/01_parameters-and-arrow/05_arguments-object/` — arrow không có arguments.
- Function parameters: `09_functions/01_parameters-and-arrow/06_function-parameters/` — default + rest trong arrow.
- Recursion: `09_functions/01_parameters-and-arrow/04_recursion/` — recursive arrow (cần named function).
- IIFE: `09_functions/02_scope-closure-strict-mode/02_iife/` — arrow IIFE pattern.
- Closure: `09_functions/02_scope-closure-strict-mode/03_closure/` — arrow trong closure.
- Strict mode: `09_functions/02_scope-closure-strict-mode/01_strict-mode/` — strict mode + arrow.
- Builtin functions: `09_functions/01_parameters-and-arrow/02_builtin-functions/` — arrow trong setTimeout.
- Operators: `08_expressions-and-operators/01_operators/5_toan-tu-logical.js` — arrow với logical operators.
