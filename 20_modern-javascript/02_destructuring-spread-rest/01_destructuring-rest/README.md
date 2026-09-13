# Destructuring & Rest

## 🔑 Khái niệm

### Destructuring (Giải cấu trúc)
Rút giá trị từ array/object thành biến riêng:
```js
// Array
const [a, b, ...rest] = [1, 2, 3, 4];

// Object
const { name, age, ...meta } = { name: "A", age: 25, city: "HN" };
```

### Rest (Thu thập phần còn lại)
`...rest` gom phần còn lại thành array:
```js
function sum(...numbers) { return numbers.reduce((a, b) => a + b, 0); }
sum(1, 2, 3); // 6
```

## ✅ Điểm mạnh

| Ưu điểm | Ví dụ |
|---|---|
| Gán nhiều biến 1 dòng | `const [x, y] = point;` |
| Swap biến | `[a, b] = [b, a];` |
| Nested extraction | `const { profile: { bio } } = data;` |
| Default values | `const { role = "user" } = data;` |
| Skip elements | `const [first, , third] = arr;` |

## ⚠️ Bẫy thường gặp

### Bẫy 1: Statement context cần parens
```js
const { a } = obj;        // OK
{ a } = obj;              // SyntaxError!
({ a } = obj);            // OK — wrap in parens
```

### Bấu 2: Rest phải cuối cùng
```js
const [first, ...rest, last] = arr;  // SyntaxError! rest phải cuối
const { a, ...rest, b } = obj;       // SyntaxError! rest phải cuối
```

### Bẫy 3: Undefined vs missing
```js
const { x = 10 } = {};     // x = 10 (missing → default)
const { x = 10 } = { x: undefined }; // x = 10 (undefined → default)
const { x = 10 } = { x: null };      // x = null (null ≠ undefined, KHÔNG dùng default)
```

## 💡 Khi nào dùng

- React props extraction: `const { title, body } = props`
- API response handling: `const { data, meta } = response`
- Function param grouping
- Swap, rotate array elements
- Extract nested config

## 🎯 Ví dụ

```js
// Array destructuring
const point = [10, 20];
const [x, y] = point;
console.log(x, y); // 10 20

// Skip elements
const [first, , third] = [1, 2, 3];
console.log(first, third); // 1 3

// Default values
const [a = 10, b = 20] = [null, null];
console.log(a, b); // 10 20 (null triggers default)

// Object destructuring
const user = { id: 1, name: "A", profile: { bio: "Dev" } };
const { name, profile: { bio } } = user;
console.log(name, bio); // A Dev

// Rename + default
const { name: userName, age: userAge = 0 } = user;

// Rest
const { role = "guest", ...rest } = user;
// role="guest", rest={id:1, name:"A", profile:{...}}

// Function parameters
function greet({ name, age = 0 } = {}) {
  return `Hello ${name}, age ${age}`;
}
greet({ name: "A" }); // "Hello A, age 0"

// Swap
[a, b] = [b, a];
```

## 🔗 Liên kết chéo
- Xem: `20_modern-javascript/02_destructuring-spread-rest/02_spread`
- Xem: `03_data-structures/01_arrays`
