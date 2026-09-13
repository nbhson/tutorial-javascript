# Tham số hàm (Function Parameters) — Thực hành chi tiết — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

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
greet("A", undefined); // A 18 — undefined trigger default
greet("A", null);      // A null — null KHÔNG trigger default!
greet("A", 0);         // A 0 — 0 KHÔNG trigger default!
```

### 3. Rest parameters (`...rest`)
Gom **các đối số còn lại** thành một **mảng thật**:

```js
function greet(name, age = 18, ...rest) {
  console.log({ name, age, rest });
}
greet("A", 20, "x", "y"); // { name: "A", age: 20, rest: ["x", "y"] }
greet();                  // { name: undefined, age: 18, rest: [] }
```

File `app.js` demo tổng hợp cả ba + một hàm cộng ba số.

**Điểm then chốt**: default parameter chỉ áp dụng khi argument là `undefined` — **không áp dụng** cho `null`, `0`, `""`, `false`. Đây là khác biệt quan trọng so với pattern cũ `arg = arg || defaultValue`.

## 📐 Cấu trúc / Cú pháp

### Default Parameters
```js
// Cú pháp
function fn(param1, param2 = defaultValue) {
  // param2 sẽ là defaultValue nếu không truyền hoặc truyền undefined
}

// Multiple defaults
function createUser(name, role = "user", active = true) {
  return { name, role, active };
}

// Default từ expression
function randomInRange(min = 0, max = Math.random() * 10) {
  return max;
}

// Default từ function call
function getCurrentDate(defaultDate = new Date()) {
  return defaultDate;
}
```

### Rest Parameters
```js
// Cú pháp — ... phải đứng cuối
function fn(first, second, ...rest) {
  // rest là mảng thật
}

// Không có named params — chỉ rest
function sum(...nums) {
  return nums.reduce((a, b) => a + b, 0);
}

// Kết hợp default + rest
function log(level = "info", ...messages) {
  console.log(`[${level}]`, ...messages);
}
```

### Parameters vs Arguments
```js
// Parameter: tên biến trong khai báo
function add(a, b) { // a, b là parameters
  return a + b;
}

// Argument: giá trị truyền vào khi gọi
add(2, 3); // 2, 3 là arguments
add();     // a = undefined, b = undefined
```

## ✅ Điểm mạnh

1. **Default parameter** giúp bỏ đi hàng trăm dòng kiểu `age = age ?? 18` thủ công — cú pháp cleaner hẳn.
2. **Rest `...args`** thay thế `arguments` object gọn và là mảng thật (có `map`, `filter`...) — modern approach.
3. **Cú pháp rõ ràng, đọc là hiểu mục đích** — `...rest` tự nói "phần còn lại" — self-documenting.
4. **Gọi thiếu đối số không gây lỗi** — JS linh hoạt cho đối số tùy chọn, rất thân thiện với API design.
5. **Kết hợp được**: default và rest dùng chung trong một hàm — `function f(a, b = 1, ...rest)`.
6. **Rest trả mảng rỗng** nếu không có đối số thừa, không sợ `undefined` — an toàn hơn arguments.
7. **Default parameter evaluation** — evaluated tại call time, không tại definition time (khác nhiều ngôn ngữ).
8. **Destructuring trong parameters** — `function fn({ name, age })` hay `function fn([first, second])`.
9. **Works with arrow functions** — `const fn = (a, b = 1, ...rest) => {}`.
10. **Cross-environment** — supported từ ES6 (2015) trên mọi browser và Node.js hiện đại.

## ⚠️ Bẫy thường gặp & Hạn chế

1. **Rest phải nằm cuối cùng** trong danh sách tham số — `(...rest, a)` là cú pháp sai (SyntaxError).
   ```js
   function bad(...a, b) {} // SyntaxError: Rest element must be last element
   function good(a, ...rest) {} // ✅
   ```

2. **Tham số thiếu nhận `undefined`** chứ không nhất thiết là lỗi — dễ sót điều kiện kiểm tra.
   ```js
   function divide(a, b) {
     // Nếu gọi divide(10) → b = undefined → 10 / undefined = NaN
     return a / b; // Không throw, chỉ return NaN!
   }
   // ✅ Guard clause
   function divideSafe(a, b) {
     if (b === undefined) throw new Error("b is required");
     return a / b;
   }
   ```

3. **Default parameter chỉ áp dụng cho `undefined`**, không áp dụng cho `null` hay `0` (truyền `null` thì `age = null`, không phải 18).
   ```js
   function greet(name = "Guest") { console.log(name); }
   greet(undefined); // "Guest" ✓
   greet(null);      // "null" ← default KHÔNG áp dụng!
   greet(0);         // "0" ← default KHÔNG áp dụng!
   greet("");        // "" ← default KHÔNG áp dụng!

   // ✅ Dùng nullish coalescing trong function body
   function greet2(name = "Guest") {
     console.log(name ?? "Guest");
   }
   ```

4. **Đổi thứ tự tham số khi gọi sẽ đổi nghĩa** (JS không có named parameters sẵn) — dùng destructuring object để giả lập.
   ```js
   // ❌ Dễ nhầm thứ tự
   createUser("admin", "Sơn"); // role="admin", name="Sơn" ← ngược!

   // ✅ Dùng object destructuring
   function createUser({ name = "Ẩn danh", role = "user" } = {}) {
     return { name, role };
   }
   createUser({ role: "admin", name: "Sơn" }); // { name: "Sơn", role: "admin" }
   ```

5. **Nhầm lẫn khai báo nhiều tham số nhưng gọi ít** → biến `undefined`, tính toán ra `NaN`.
   ```js
   function calc(a, b) { return a + b; }
   console.log(calc(5)); // NaN ← b = undefined, 5 + undefined = NaN
   ```

6. **Default parameter là expression** — nếu dùng mutable object/array, sẽ shared across calls.
   ```js
   // ❌ Danger — default array shared
   function bad(items = []) {
     items.push(1);
     return items;
   }
   bad(); // [1]
   bad(); // [1, 1] ← shared mutable default!

   // ✅ Safe — create new each time
   function good(items = undefined) {
     items = items || [];
     items.push(1);
     return items;
   }
   ```

7. **Default parameter evaluted tại call time** — có thể truy cập variable từ outer scope.
   ```js
   let defaultVal = 10;
   function test(a = defaultVal) { console.log(a); }
   defaultVal = 20;
   test(); // 20 ← evaluted tại call time, not definition time
   ```

## 💡 Khi nào dùng

1. **Hàm có tham số tùy chọn** (page size mặc định 10, role mặc định "user") — default parameters.
2. **Hàm nhận danh sách động đối số** (log, gom giá trị, tính tổng) — rest parameter `...args`.
3. **Truyền cờ/tùy biến qua object destructuring** — `function open({ title = "", mode = "default" } = {})`.
4. **Viết API thư viện thân thiện với người dùng** — optional params với sensible defaults.
5. **Variadic functions** (số đối số không xác định) — `...args` là cách hiện đại nhất.
6. **Object-oriented style với parameters** — destructuring nhận config object thay nhiều params.
7. **Guard clauses** — check `if (arg === undefined) throw` sau default parameter.
8. **Factory functions** — `function createPair(defaultA = 1, defaultB = 2) => [defaultA, defaultB]`.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Default parameters cơ bản (file `app.js`)
```js
// Nội dung app.js trong thư mục
function greet(name, age = 18, ...rest) {
  console.log({ name, age, rest });
}
greet("A", 20, "x", "y"); // { name: "A", age: 20, rest: ["x", "y"] }
greet();                  // { name: undefined, age: 18, rest: [] }
```

### Ví dụ 2: Rest parameter — hàm tính tổng
```js
// Nội dung app.js trong thư mục
function sumAll(...nums) {
  return nums.reduce((acc, n) => acc + n, 0);
}
console.log(sumAll(1, 2, 3, 4)); // 10

// So sánh với arguments object
function sumOld() {
  let total = 0;
  for (let i = 0; i < arguments.length; i++) total += arguments[i];
  return total;
}
console.log(sumOld(1, 2, 3, 4)); // 10
```

### Ví dụ 3: Default từ expression
```js
// Default từ hàm khác
function getTimestamp() { return Date.now(); }
function log(message, timestamp = getTimestamp()) {
  console.log(`[${timestamp}] ${message}`);
}
log("hello"); // "[1719... ] hello"

// Default từ Math
function randomBetween(min = 0, max = 100) {
  return Math.random() * (max - min) + min;
}
console.log(randomBetween());    // random giữa 0 và 100
console.log(randomBetween(10, 20)); // random giữa 10 và 20
```

### Ví dụ 4: Object destructuring in parameters
```js
// Nhận config object thay vì nhiều params
function createUser({ name = "Ẩn danh", age = 0, role = "user" } = {}) {
  return { name, age, role };
}
console.log(createUser());                    // { name: "Ẩn danh", age: 0, role: "user" }
console.log(createUser({ name: "Sơn" }));     // { name: "Sơn", age: 0, role: "user" }
console.log(createUser({ role: "admin" }));   // { name: "Ẩn danh", age: 0, role: "admin" }

// Array destructuring
function swap([a, b] = [0, 0]) {
  return [b, a];
}
console.log(swap([1, 2])); // [2, 1]
```

### Ví dụ 5: Default + Rest kết hợp
```js
function pizza(order, ...toppings) {
  const defaultToppings = ["cheese", "tomato"];
  const allToppings = toppings.length > 0 ? toppings : defaultToppings;
  return `${order} pizza with ${allToppings.join(", ")}`;
}
console.log(pizza("large"));             // "large pizza with cheese, tomato"
console.log(pizza("medium", "mushroom")); // "medium pizza with mushroom"
console.log(pizza("small", "pepperoni", "olive")); // "small pizza with pepperoni, olive"
```

### Ví dụ 6: Arrow function với default + rest
```js
const add = (a = 0, b = 0) => a + b;
console.log(add());       // 0
console.log(add(5));      // 5
console.log(add(2, 3));   // 5

const join = (sep = "-", ...parts) => parts.join(sep);
console.log(join("a", "b", "c"));       // "a-b-c"
console.log(join("/", "home", "user")); // "home/user"
```

### Ví dụ 7: Guard clause với default parameter
```js
function divide(a, b = 1) {
  if (b === 0) throw new Error("Cannot divide by zero");
  return a / b;
}
console.log(divide(10));     // 10  — b default = 1
console.log(divide(10, 2));  // 5
console.log(divide(10, 0));  // throws Error

// ✅ Better: undefined check instead of default
function divideSafe(a, b) {
  if (b === undefined) throw new Error("b is required");
  if (b === 0) throw new Error("Cannot divide by zero");
  return a / b;
}
```

### Ví dụ 8: Default mutable object trap
```js
// ❌ Shared mutable default
function appendItem(item, list = []) {
  list.push(item);
  return list;
}
appendItem(1); // [1]
appendItem(2); // [1, 2] ← shared! bug

// ✅ Safe: create new each call
function appendItemSafe(item, list = undefined) {
  list = list || [];
  list.push(item);
  return list;
}
appendItemSafe(1); // [1]
appendItemSafe(2); // [2] ← fresh array

// ✅ Best: use rest parameter (always fresh array)
function appendItemBest(item, ...list) {
  return [...list, item];
}
```

### Ví dụ 9: Simulating named parameters
```js
// JS không có named parameters — giả lập qua object
function connect({ host = "localhost", port = 3000, protocol = "http" } = {}) {
  return `${protocol}://${host}:${port}`;
}
console.log(connect());                        // "http://localhost:3000"
console.log(connect({ port: 8080 }));          // "http://localhost:8080"
console.log(connect({ host: "api.example.com", port: 443, protocol: "https" }));
// "https://api.example.com:443"
```

### Ví dụ 10: validate parameters helper
```js
function validate(...required) {
  return function(fn) {
    return function(...args) {
      for (let i = 0; i < required.length; i++) {
        if (args[i] === undefined) {
          throw new Error(`Missing required argument: ${required[i]}`);
        }
      }
      return fn.apply(this, args);
    };
  };
}

// Usage
const safeAdd = validate("a", "b")((a, b) => a + b);
console.log(safeAdd(2, 3)); // 5
console.log(safeAdd(2));    // throws Error: Missing required argument: b
```

## 🔬 So sánh với alternatives

| Tính năng | Default Parameter | Manual check | Nullish coalescing | Logical OR `||` |
|---|---|---|---|---|
| Cú pháp | `fn(a = 1)` | `if (a === undefined) a = 1` | `a ?? 1` | `a \|\| 1` |
| Xử lý `0` | ✅ Giữ 0 | ✅ Giữ 0 | ✅ Giữ 0 | ❌ Dùng default |
| Xử lý `""` | ✅ Giữ "" | ✅ Giữ "" | ✅ Giữ "" | ❌ Dùng default |
| Xử lý `false` | ✅ Giữ false | ✅ Giữ false | ✅ Giữ false | ❌ Dùng default |
| Readability | Cao nhất | Thấp | Cao | Cao |

## 📊 Performance & Best Practices

**Performance**:
- Default parameters có overhead nhỏ (~5-10%) so với không có default — negligible trong practice.
- Rest parameter tạo array mới mỗi call — overhead nhỏ, acceptably fast.
- Object destructuring trong parameters có overhead nhỏ hơn spread `...args`.

**Best practices**:
- **Ưu tiên default parameters** thay manual `if (a === undefined)` checks.
- **Dùng nullish coalescing `??`** trong function body khi cần phân biệt `null` và `undefined`.
- **Tránh mutable default** (object/array) — dùng rest parameter hoặc factory function.
- **Rest parameter đứng cuối** — không thể đặt ở giữa hoặc đầu.
- **Dùng object destructuring** cho hàm có >3 params — readable hơn, named args simulation.
- **Default từ pure expression** — tránh side-effect trong default value.
- **Document default values** — JSDoc `@param {number} [size=10]` cho biết default.
- **Validate after defaults** — check `if (a === undefined)` sau khi default đã apply.
- **Arrow + default + rest** — pattern phổ biến trong modern React/Vue codebases.

**Quy tắc "3 nên — 3 không"**:
- ✅ Nên dùng default parameters cho optional args.
- ✅ Nên dùng rest parameter thay arguments object.
- ✅ Nên dùng object destructuring cho nhiều params.
- ❌ Không nên dùng mutable object/array làm default.
- ❌ Không nên đặt rest parameter không ở cuối.
- ❌ Không nên nhầm `null` với `undefined` khi dùng default.

## 🔗 Liên kết chéo

- Arguments object: `09_functions/01_parameters-and-arrow/05_arguments-object/` — arguments vs rest comparison.
- Arrow functions: `09_functions/01_parameters-and-arrow/03_arrow-functions/` — arrow với default + rest.
- Callbacks: `09_functions/01_parameters-and-arrow/01_callbacks/` — callback parameters.
- Recursion: `09_functions/01_parameters-and-arrow/04_recursion/` — recursive function parameters.
- Scope & Closure: `09_functions/02_scope-closure-strict-mode/` — parameters trong closure context.
- Strict mode: `09_functions/02_scope-closure-strict-mode/01_strict-mode/` — strict mode + duplicate params.
- Operators: `08_expressions-and-operators/01_operators/` — toán tử trong default expressions.
- Expressions: `08_expressions-and-operators/06_string-operators/` — template literal trong default.
