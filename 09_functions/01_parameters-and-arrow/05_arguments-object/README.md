# Đối tượng arguments (arguments object) — Thực hành chi tiết — [Level: Intermediate]

## 🔑 Khái niệm cốt lõi

Bên trong **hàm thường** (không phải arrow), JavaScript tự tạo sẵn một biến đặc biệt tên là **`arguments`** — chứa tất cả tham đối (arguments) bạn truyền vào khi gọi hàm, **dù khai báo bao nhiêu tham số**.

```js
function f() {
  console.log(arguments);          // Arguments(3) [1, 2, 3]
  console.log(Array.from(arguments)); // [1, 2, 3] — thành mảng thật
  console.log(arguments.length);   // 3
}
f(1, 2, 3);
```

**Đặc điểm quan trọng**:

- **Array-like**: có `length` và truy cập bằng index `arguments[0]`, nhưng **không phải mảng thật** — không có `map`, `filter`, `push`...
- Chỉ tồn tại trong **function thường**, **không có trong arrow function** — arrow kế thừa `arguments` của phạm vi bên ngoài nếu có.
- Muốn dùng như mảng → `Array.from(arguments)` hoặc `[...arguments]`.
- **Cách hiện đại hơn**: dùng rest parameter `(...args)` — nhận về **mảng thật** và hoạt động cả trong arrow.

File `app.js` demo cả hai cách: arguments object trong hàm thường và rest parameter trong arrow.

**Sự khác biệt then chốt**: `arguments` là object được JavaScript tự động tạo, còn `...args` (rest parameter) là syntax ECMAScript 6 cho phép gom các đối số thừa thành mảng thật. Cả hai đều cho phép hàm nhận **số lượng đối số không xác định**, nhưng rest parameter hiện đại hơn, sạch hơn, và hoạt động trong arrow.

## 📐 Cấu trúc / Cú pháp

### Arguments object
```js
function example() {
  console.log(arguments);          // Arguments(3) [1, 2, 3]
  console.log(arguments[0]);       // 1 — truy cập bằng index
  console.log(arguments.length);   // 3 — độ dài
  console.log(Array.from(arguments)); // [1, 2, 3] — convert sang mảng thật
  console.log([...arguments]);     // [1, 2, 3] — spread sang mảng thật
}
example(1, 2, 3);
```

### Rest parameter (ES6+)
```js
// Rest trong regular function
function sum(...nums) {
  return nums.reduce((a, b) => a + b, 0);
}
console.log(sum(1, 2, 3, 4)); // 10

// Rest trong arrow function
const multiply = (...nums) => nums.reduce((a, b) => a * b, 1);
console.log(multiply(2, 3, 4)); // 24

// Rest kết hợp named parameters
function greet(greeting, ...names) {
  return names.map(name => `${greeting}, ${name}!`);
}
console.log(greet("Hello", "Sơn", "An")); // ["Hello, Sơn!", "Hello, An!"]
```

### So sánh arguments vs rest
```js
// Arguments — array-like, only in regular functions
function withArgs() {
  console.log(typeof arguments);   // "object"
  console.log(arguments instanceof Array); // false
  console.log(Array.isArray(arguments));   // false
}

// Rest — real array, works everywhere
const withRest = (...args) => {
  console.log(typeof args);        // "object"
  console.log(args instanceof Array); // true
  console.log(Array.isArray(args));    // true
};
```

## ✅ Điểm mạnh

1. **Hàm thường nhận được vô hạn tham số** qua `arguments` mà không cần khai báo rest — legacy codebase quen thuộc.
2. **`arguments.length`** hữu ích để kiểm tra số lượng đối số thực tế truyền vào — validation pattern.
3. **Hỗ trợ tương thích với code cũ** (các thư viện viết trước ES6 dùng khá nhiều `arguments`) — cần biết để đọc legacy code.
4. **`arguments[0]` truy cập nhanh** như mảng — index access O(1).
5. **Minh họa rõ khái niệm "array-like"** — kiến thức gặp lại ở `NodeList`, `HTMLCollection`, `DOMTokenList`.
6. **Rest parameter thay thế hiện đại** — mảng thật, dùng được trong arrow, cú pháp rõ ràng hơn.
7. **Kết hợp với spread** — `[...arguments]` convert nhanh thành mảng thật.
8. **`Array.from(arguments)`** — convert có mapper function: `Array.from(arguments, x => x * 2)`.
9. **Default parameters work with arguments** — arguments.length vẫn đúng kể cả khi dùng default.
10. **Named parameters vẫn synchronized** với arguments (trong non-strict mode) — `arguments[0] === a`.

## ⚠️ Bẫy thường gặp & Hạn chế

1. **Không có các phương thức mảng**: gọi `arguments.map(...)` sẽ lỗi — phải chuyển bằng `Array.from`/`...spread` trước.
   ```js
   function example() {
     arguments.map(x => x * 2); // TypeError: arguments.map is not a function
     // ✅ Sửa
     Array.from(arguments).map(x => x * 2);
   }
   ```

2. **Không tồn tại trong arrow function** — dùng `...args` thay thế.
   ```js
   // ❌ ReferenceError trong arrow
   const arrow = () => { console.log(arguments); };
   arrow(1, 2);

   // ✅ Dùng rest trong arrow
   const arrow = (...args) => { console.log(args); };
   arrow(1, 2); // [1, 2]
   ```

3. **`arguments` bị liên kết với tham số khi không dùng strict mode** — thay đổi tham số ảnh hưởng `arguments` và ngược lại — dễ gây bug.
   ```js
   // Non-strict mode — arguments và parameter shared reference
   function example(a) {
     a = 99;
     console.log(arguments[0]); // 99 ← thay đổi!
   }
   example(1);

   // ✅ Strict mode — decoupled
   "use strict";
   function exampleStrict(a) {
     a = 99;
     console.log(arguments[0]); // 1 ← không ảnh hưởng
   }
   exampleStrict(1);
   ```

4. **Khái niệm cũ, khó đọc hơn so với rest parameter hiện đại** — codebase mới nên dùng rest.
5. **Arguments object được tạo ngầm** — overhead nhỏ mỗi khi gọi hàm, negligible trong practice.
6. **Không thể dùng destructuring trực tiếp trên arguments** — phải convert sang array trước.
7. **Arrow function kế thừa arguments từ outer scope** — nếu outer là regular function, arrow sẽ thấy arguments của outer.
   ```js
   function outer() {
     const inner = () => console.log(arguments);
     inner(100); // Arguments(1) [1] — kế thừa arguments của outer, không phải inner!
   }
   outer(1);
   ```

## 💡 Khi nào dùng

1. **Khi viết hàm nhận số lượng đối số không xác định** (accumulator, function đếm tổng) — rest parameter hiện đại hơn.
2. **Trong code cũ / thư viện legacy đang phải bảo trì** — đọc và hiểu `arguments` object.
3. **Khi cần đếm hoặc truy xuất linh hoạt đối số theo index** — `arguments[i]` truy cập random.
4. **Học phân biệt "array-like" để xử lý các đối tượng DOM dạng list** — NodeList, HTMLCollection.
5. **Wrapper/decorator pattern** — chuyển tiếp arguments tới hàm khác: `fn.apply(this, arguments)`.
6. **Proxy/Reflect pattern** — intercept and forward arguments in proxied functions.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Cơ bản — arguments object (file `app.js`)
```js
// Nội dung app.js trong thư mục
function f() {
  console.log(arguments);            // Arguments(3) [1, 2, 3]
  console.log(Array.from(arguments)); // [1, 2, 3] — thành mảng thật
  console.log(arguments.length);     // 3
}
f(1, 2, 3); // Arguments(3) [1, 2, 3] / [1, 2, 3] / 3
```

### Ví dụ 2: Rest parameter trong arrow (file `app.js`)
```js
// Nội dung app.js trong thư mục
const arrow = (...args) => console.log(args);
arrow(1, 2); // [1, 2] — rest thay thế arguments trong arrow
```

### Ví dụ 3: Cộng mọi đối số không cần khai báo (file `app.js`)
```js
// Nội dung app.js trong thư mục
function sum() {
  let total = 0;
  for (let i = 0; i < arguments.length; i++) total += arguments[i];
  return total;
}
console.log(sum(1, 2, 3, 4)); // 10
```

### Ví dụ 4: Convert arguments sang mảng thật
```js
function example() {
  // ❌ Không dùng được map trực tiếp
  // arguments.map(x => x * 2); // TypeError

  // ✅ Convert sang mảng
  const args = Array.from(arguments);
  console.log(args.map(x => x * 2)); // [2, 4, 6]

  // ✅ Spread syntax
  const args2 = [...arguments];
  console.log(args2.sort((a, b) => b - a)); // [3, 2, 1]
}
example(1, 3, 2);
```

### Ví dụ 5: Arguments với named parameters — synchronization
```js
// Non-strict mode — arguments và parameter linked
function linked(a, b) {
  console.log(a, arguments[0]); // 10 10 — linked
  a = 99;
  console.log(a, arguments[0]); // 99 99 — thay đổi cả hai
}
linked(10, 20);

// ✅ Strict mode — decoupled
"use strict";
function decoupled(a, b) {
  console.log(a, arguments[0]); // 10 10
  a = 99;
  console.log(a, arguments[0]); // 99 10 — KHÔNG linked!
}
decoupled(10, 20);
```

### Ví dụ 6: Rest parameter — modern replacement
```js
// Regular function with rest
function sumAll(...nums) {
  return nums.reduce((acc, n) => acc + n, 0);
}
console.log(sumAll(1, 2, 3, 4)); // 10

// Arrow with rest
const product = (...nums) => nums.reduce((a, b) => a * b, 1);
console.log(product(2, 3, 4)); // 24

// Mixed: named params + rest
function describe(type, ...items) {
  return `Type: ${type}, Items: ${items.join(", ")}`;
}
console.log(describe("fruit", "apple", "banana"));
// "Type: fruit, Items: apple, banana"
```

### Ví dụ 7: Argument forwarding — wrapper pattern
```js
// Wrapper function that forwards all arguments
function logger(fn) {
  return function(...args) {
    console.log(`Calling ${fn.name} with`, args);
    const result = fn.apply(this, args); // forward arguments
    console.log(`Result:`, result);
    return result;
  };
}

function add(a, b) { return a + b; }
const loggedAdd = logger(add);
loggedAdd(2, 3);
// "Calling add with" [2, 3]
// "Result:" 5
```

### Ví dụ 8: Arguments trong nested function
```js
function outer(a, b) {
  console.log("outer arguments:", arguments.length); // 2

  function inner(c, d) {
    console.log("inner arguments:", arguments.length); // 2
    // inner có arguments riêng, KHÔNG kế thừa outer
  }
  inner(10, 20);

  // Arrow inner kế thừa arguments của outer
  const arrowInner = () => {
    console.log("arrow arguments:", arguments.length); // 2 — from outer!
  };
  arrowInner();
}
outer(1, 2);
```

### Ví dụ 9: Validator với arguments length check
```js
function validateRequired(...args) {
  const missing = [];
  args.forEach((arg, i) => {
    if (arg === undefined || arg === null) {
      missing.push(`argument ${i + 1}`);
    }
  });
  if (missing.length > 0) {
    throw new Error(`Missing required: ${missing.join(", ")}`);
  }
  return true;
}

validateRequired(1, "hello", true);  // true
validateRequired(1, null);           // throws Error: Missing required: argument 2
```

### Ví dụ 10: Math.max với arguments vs spread
```js
// Cách cũ — dùng arguments
function maxOld() {
  let max = -Infinity;
  for (let i = 0; i < arguments.length; i++) {
    if (arguments[i] > max) max = arguments[i];
  }
  return max;
}

// Cách mới — spread + Math.max
function maxNew(...nums) {
  return Math.max(...nums);
}

console.log(maxOld(1, 5, 3, 9, 2)); // 9
console.log(maxNew(1, 5, 3, 9, 2)); // 9

// Math.max native với spread
console.log(Math.max(...[1, 5, 3, 9, 2])); // 9
// ⚠️ Giới hạn: spread có thể overflow với mảng >100k elements
```

## 🔬 So sánh với alternatives

| Đặc điểm | `arguments` | Rest parameter `...args` |
|---|---|---|
| Loại | Array-like object | Real array |
| Methods | Không có (map, filter...) | Có đầy đủ |
| Arrow function | ❌ Không có | ✅ Có |
| Syntax | Tự động tạo | Khai báo rõ ràng |
| Compatibility | Tất cả JS versions | ES6+ |
| Performance | Slightly slower | Slightly faster |
| Readability | Less clear | More clear |
| Recommended | Legacy code only | Modern code (preferred) |

## 📊 Performance & Best Practices

**Performance**:
- `arguments` object creation có overhead nhỏ — engine must create array-like object.
- Rest parameter `...args` generally faster — native array allocation.
- `Array.from(arguments)` thêm overhead ~2x so với direct rest access.
- Trong vòng lặp tight, prefer rest parameter over arguments + conversion.

**Best practices**:
- **Ưu tiên rest parameter `...args`** — modern, real array, works in arrow.
- **Chỉ dùng `arguments`** khi bảo trì legacy code hoặc cần access theo index.
- **Luôn convert arguments** sang mảng thật trước khi dùng array methods.
- **Dùng `"use strict"`** để decouple arguments khỏi named parameters.
- **Arrow function** — dùng rest parameter, không mong đợi arguments.
- **Documentation** — ghi rõ function accepts variable args: `@param {...number} nums`.
- **TypeScript** — rest parameter có type annotation: `...nums: number[]`.
- **Avoid `arguments.callee`** — bị cấm trong strict mode, deprecated, security risk.

**Quy tắc "3 nên — 3 không"**:
- ✅ Nên dùng rest parameter `...args` trong code mới.
- ✅ Nên convert `arguments` to array before using methods.
- ✅ Nên dùng `"use strict"` để avoid arguments-parameter coupling.
- ❌ Không nên dùng `arguments.callee` — deprecated, strict mode forbidden.
- ❌ Không nên mong đợi `arguments` trong arrow function.
- ❌ Không nên rely trên arguments synchronization — dùng strict mode hoặc rest.

## 🔗 Liên kết chéo

- Tổng quan Functions: `09_functions/README.md` — khái niệm hàm, arguments context.
- Arrow functions: `09_functions/01_parameters-and-arrow/03_arrow-functions/` — arrow không có arguments.
- Function parameters: `09_functions/01_parameters-and-arrow/06_function-parameters/` — default + rest deep dive.
- Callbacks: `09_functions/01_parameters-and-arrow/01_callbacks/` — callback với arguments forwarding.
- Strict mode: `09_functions/02_scope-closure-strict-mode/01_strict-mode/` — strict mode decouples arguments.
- Closure: `09_functions/02_scope-closure-strict-mode/03_closure/` — closure access to arguments.
- Operators: `08_expressions-and-operators/05_unary/app.js` — typeof với arguments object.
- Builtin functions: `09_functions/01_parameters-and-arrow/02_builtin-functions/` — built-in hàm nhận arguments.
