# Phương thức `apply()` — [Level: Intermediate]

## 🔑 Khái niệm cốt lõi

`fn.apply(thisArg, [arg1, arg2, ...])` **gọi ngay lập tức** hàm `fn` với `this` = `thisArg`, nhưng đối số được truyền **dưới dạng mảng** (array) thay vì danh sách.

Về bản chất `apply` giống hệt `call`, chỉ khác hình thức truyền đối số:
- `call`: `fn.call(ctx, a, b, c)` — từng đối số riêng lẻ
- `apply`: `fn.apply(ctx, [a, b, c])` — tất cả trong một mảng

`apply` rất hợp khi số lượng đối số không biết trước — ví dụ rải (`spread`) một mảng vào hàm nhận lẻ từng giá trị như `Math.max`, `Math.min`.

**Lưu ý quan trọng:** ES2015+ có spread operator `...` khiến `apply` ít cần hơn trong code hiện đại, nhưng `apply` vẫn quan trọng khi làm việc với `arguments` object (không phải array thật) hoặc legacy code.

## 📐 Cấu trúc / Cú pháp

### Signature

```js
result = fn.apply(thisArg, [arg1, arg2, arg3, ...])
```

### Bảng so sánh call vs apply

| Đặc tính | `call` | `apply` |
|----------|--------|---------|
| Cách truyền đối số | `fn.call(ctx, a, b, c)` | `fn.apply(ctx, [a, b, c])` |
| Gọi ngay | ✅ | ✅ |
| Applicable when | Đối số cố định, biết trước | Đối số động, trong mảng/arguments |

### `thisArg` special values

| `thisArg` | Non-strict | Strict |
|-----------|------------|--------|
| Object | Object đó | Object đó |
| `null` / `undefined` | `window` / `globalThis` | `null` / `undefined` |
| Primitive | Boxed object | Primitive |

### Apply vs Spread operator (ES2015+)

```js
const nums = [1, 2, 3];

// ES5: apply
Math.max.apply(null, nums); // 3

// ES2015+: spread (ngắn gọn hơn)
Math.max(...nums); // 3

// Nhưng apply vẫn cần khi làm việc với arguments
function sum() {
  return Array.prototype.reduce.call(arguments, (a, b) => a + b, 0);
}
// apply version:
function sumApply() {
  return Array.prototype.reduce.apply(arguments, [(a, b) => a + b, 0]);
}
```

## ✅ Điểm mạnh — Tại sao nên dùng

1. **Làm việc tự nhiên với mảng và object `arguments`** — đối số mềm của hàm.
2. **Dùng chung với `call`** cho mọi nhu cầu mượn hàm, bind this, kế thừa.
3. **Khi cần gọi hàm cha trong constructor**: `Parent.apply(this, arguments)` truyền thẳng toàn bộ đối số.
4. **Linh hoạt khi đối số đến từ mảng xây dựng động** — không cần biết trước số lượng.
5. **Math functions với array** — `Math.max.apply(null, arr)` tìm max dễ dàng.
6. **Copy array nhanh** — `Array.prototype.push.apply(arr1, arr2)` gộp array.
7. **Min/Max trên array lớn** — tránh loop thủ công.
8. **Legacy code compatibility** — code cũ thường dùng `apply`.
9. **Convert array-like to real array** — `Array.prototype.slice.apply(arguments)`.
10. **Function composition** — apply arguments from one function to another.

## ⚠️ Bẫy thường gặp & Hạn chế

### Bẫy 1: Truyền sai dạng đối số — call vs apply nhầm

```js
const nums = [1, 2, 3];
Math.max.call(null, nums);   // NaN — nums là 1 đối số duy nhất (array)
Math.max.apply(null, nums);  // 3 ✅ — array được spread thành 3 đối số
```

### Bẫy 2: `arguments` không phải array thật

```js
function example() {
  Math.max.apply(null, arguments); // ✅ arguments là array-like, apply chấp nhận
  Math.max.call(null, arguments);  // ❌ NaN — arguments là 1 đối số object
}
```

### Bẫy 3: Mảng quá lớn — stack overflow

```js
const hugeArray = new Array(1000000).fill(1);
Math.max.apply(null, hugeArray); // RangeError: Maximum call stack size exceeded
// Fix: dùng loop hoặc reduce
console.log(hugeArray.reduce((a, b) => Math.max(a, b)));
```

### Bẫy 4: `null` thisArg trong strict mode

```js
"use strict";
function fn() { return this; }
fn.apply(null); // null (không tự động thành window)
```

### Bẫy 5: Quên `apply` gọi ngay — nhầm với `bind`

```js
const result = Math.max.apply(null, [1, 2, 3]); // 3 — apply gọi ngay
// Nếu muốn hàm mới: Math.max.bind(null, ...) — nhưng bind không nhận array
```

### Bẫy 6: Apply với thisArg là primitive

```js
function greet() {
  return `Hello, ${this.name}!`;
}
greet.apply("string"); // "Hello, string!" — primitive auto-boxed
greet.apply(null);     // "Hello, undefined!" (non-strict) hoặc throw (strict)
```

### Bẫy 7: Apply không hoạt động với arrow function

```js
const arrow = () => console.log(this);
arrow.apply({ x: 1 }); // vẫn in globalThis — arrow không có this riêng
```

## 💡 Khi nào dùng — Tình huống thực tế

1. **Gọi constructor cha**: `Animal.apply(this, arguments)` — truyền toàn bộ arguments.
2. **`Math.max.apply(null, numbers)`** tìm max của mảng không biết trước độ dài.
3. **Ghép/gộp mảng** vào hàm nhận danh sách đối số.
4. **Mượn hàm với đối số tập hợp sẵn trong mảng**.
5. **Convert array-like to array**: `Array.prototype.slice.apply(arguments)`.
6. **Copy array elements**: `Array.prototype.push.apply(arr1, arr2)`.
7. **Check if value in array** (pre-ES6 includes): `Array.prototype.indexOf.call(arr, val)`.
8. **Apply bindings for utility functions** — khi arguments đến từ một mảng đã build.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Cơ bản — apply với mảng đối số

```js
const teacher = {
  firstName: "Thu",
  lastName: "Minh",
};

function greet(greeting, message) {
  return `${greeting} ${this.firstName} ${this.lastName}, ${message}`;
}

// apply: đối số trong mảng
console.log(greet.apply(teacher, ["Em chào cô", "Cô dạy môn gì thế?"]));
// Em chào cô Thu Minh, Cô dạy môn gì thế?

// tương đương với call (danh sách)
console.log(greet.call(teacher, "Em chào cô", "Cô dạy môn gì thế?"));
```

### Ví dụ 2: Kế thừa qua arguments

```js
function Animal(name, weight) {
  this.name = name;
  this.weight = weight;
}

function Parrot() {
  Animal.apply(this, arguments); // rải toàn bộ arguments
  this.speak = function () { console.log("Nhà có khách"); };
}

new Parrot("Vẹt", 300).speak(); // Nhà có khách
const p = new Parrot("Vẹt", 300);
console.log(p.name); // "Vẹt"
console.log(p.weight); // 300
```

### Ví dụ 3: Math.max với array

```js
const scores = [85, 92, 78, 95, 88];
console.log(Math.max.apply(null, scores)); // 95

// So sánh với reduce (alternative)
console.log(scores.reduce((a, b) => Math.max(a, b))); // 95

// So sánh với spread (modern)
console.log(Math.max(...scores)); // 95
```

### Ví dụ 4: Gộp array với push.apply

```js
const arr1 = [1, 2, 3];
const arr2 = [4, 5, 6];

// Cách cổ điển (pre-ES6)
Array.prototype.push.apply(arr1, arr2);
console.log(arr1); // [1, 2, 3, 4, 5, 6]

// Cách hiện đại (spread)
const arr3 = [...arr1, ...arr2];
console.log(arr3); // [1, 2, 3, 4, 5, 6]
```

### Ví dụ 5: Convert arguments to array

```js
function convertArgs() {
  // arguments là array-like
  const argsArray = Array.prototype.slice.apply(arguments);
  return argsArray.map(x => x * 2);
}
console.log(convertArgs(1, 2, 3)); // [2, 4, 6]

// Cách hiện đại
function convertArgsModern(...args) {
  return args.map(x => x * 2);
}
```

### Ví dụ 6: Min/Max trên dynamic data

```js
function findExtremes() {
  const values = Array.prototype.slice.apply(arguments);
  return {
    min: Math.min.apply(null, values),
    max: Math.max.apply(null, values),
  };
}
console.log(findExtremes(3, 7, 1, 9, 4)); // { min: 1, max: 9 }
```

### Ví dụ 7: Check if value in array (pre-ES6 includes)

```js
function contains(arr, value) {
  return Array.prototype.indexOf.call(arr, value) !== -1;
}
console.log(contains([1, 2, 3], 2)); // true
console.log(contains("hello", "l")); // true (string là array-like)
```

### Ví dụ 8: Apply với function nhận nhiều đối số

```js
function describe(color, size, brand) {
  return `A ${color} ${size} ${brand} shirt`;
}

const attrs = ["red", "M", "Nike"];
console.log(describe.apply(null, attrs)); // "A red M Nike shirt"

// So với call — phải liệt kê từng đối số
console.log(describe.call(null, "red", "M", "Nike")); // cùng result
```

### Ví dụ 9: Matrix operations với apply

```js
function addMatrices(a, b) {
  return a.map((row, i) => row.map((val, j) => val + b[i][j]));
}

function transformMatrix(matrix, fn) {
  return matrix.map(row => fn.apply(null, row));
}

const matrix = [[1, 2], [3, 4]];
console.log(transformMatrix(matrix, (a, b) => a + b)); // [[3], [7]]
```

### Ví dụ 10: Binding methods with pre-filled args

```js
function createLogger(prefix) {
  return function(level, message) {
    const timestamp = new Date().toISOString();
    console.log(`[${timestamp}] [${prefix}] [${level}] ${message}`);
  };
}

const info = createLogger("APP");
info.apply(null, ["INFO", "Server started"]);
// [2024-01-01T00:00:00.000Z] [APP] [INFO] Server started
```

## 🔬 So sánh với alternatives

| Cách | Spread vs Apply | Performance | Readability | Use case |
|------|-----------------|-------------|-------------|----------|
| `apply(null, arr)` | Legacy, array input | Nhanh | Trung bình | arguments object, dynamic args |
| `fn(...arr)` | ES2015+ spread | Nhanh tương đương | Cao | Modern code, known array |
| `reduce` | Loop-based | Chậm hơn | Cao | Functional style |
| `for` loop | Manual | Nhanh nhất | Thấp | Performance-critical |

```js
const nums = [1, 2, 3, 4, 5];

// Apply (legacy)
Math.max.apply(null, nums);

// Spread (modern)
Math.max(...nums);

// Reduce (functional)
nums.reduce((a, b) => Math.max(a, b));
```

## 📊 Performance & Best Practices

- **Spread `...` hiện đại hơn** — `Math.max(...nums)` đọc dễ hơn `Math.max.apply(null, nums)`.
- **Apply vẫn cần cho `arguments`** — arguments không hỗ trợ spread trong function signature cũ.
- **Tránh apply với mảng > 100k phần tử** — có thể gây stack overflow.
- **Prefer `call` khi đối số cố định**, `apply` khi đối số trong mảng/arguments.
- **Arrow function không dùng apply** — arrow không có `this` riêng, apply không ảnh hưởng.
- **Khi có thể, dùng native methods** — `.reduce()`, `.find()` thay vì borrow apply.

## 🔗 Liên kết chéo

- **Xem thêm:** `11_function-borrowing/03_call` — call tương tự, khác ở dạng đối số
- **Xem thêm:** `11_function-borrowing/01_bind` — bind tạo hàm mới
- **Xem thêm:** `11_function-borrowing/README` — overview call/apply/bind
- **Xem thêm:** `14_classes/02_constructor` — super() thay thế apply trong class
- **Xem thêm:** `11_function-borrowing/05_polyfill` — tự viết myApply
- **Xem thêm:** `20_modern-javascript/02_destructuring-spread-rest/02_spread` — spread operator alternative
