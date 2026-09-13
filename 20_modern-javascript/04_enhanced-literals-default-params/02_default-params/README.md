# Default Parameters

## Khái niệm

ES2015 (ES6) cho phép gán giá trị mặc định cho function parameters:
```js
function greet(name = "Guest", age = 0) {
  return `Hello ${name}, age ${age}`;
}
```

Nếu argument là `undefined` (hoặc không truyền) --> dùng default. Nếu là `null` --> dùng `null`.

## Điểm mạnh

- Giảm boilerplate `if (x === undefined) x = default`
- Hỗ trợ expression: `function foo(x = computeDefault())`
- Hỗ trợ destructuring default: `function bar({ role = "user" } = {})`

## Bẫy thường gặp

### Bẫy 1: null KHÔNG trigger default
```js
function test(x = 10) { return x; }
test(null);  // null -- KHÔNG phải 10
test(undefined); // 10
test(); // 10
```

### Bẫy 2: Default eval mỗi lần
```js
function create(id = generateId()) {
  // generateId() gọi MỖI lần không truyền id
  // Có thể gây side effect lặp
}
```

### Bẫy 3: Rest parameter không có default
```js
function foo(...args = [1, 2]) {} // SyntaxError!
// Rest không thể có default value
```

## Khi nào dùng

- Function có nhiều optional params
- Config object pattern
- API wrapper với default options
- React component props

## Ví dụ

```js
function createUser(name = "Anonymous", role = "user") {
  return { name, role, createdAt: new Date() };
}
console.log(createUser());              // { name: "Anonymous", role: "user" }
console.log(createUser("A"));           // { name: "A", role: "user" }
console.log(createUser("A", "admin"));  // { name: "A", role: "admin" }

// Expression default
function randomId(length = Math.floor(Math.random() * 10) + 5) {
  return Math.random().toString(36).slice(2, length + 2);
}

// Destructuring default
function configure({ timeout = 5000, retries = 3 } = {}) {
  console.log(timeout, retries);
}
configure();       // 5000 3
configure({});     // 5000 3
configure({ timeout: 1000 }); // 1000 3

// Thực tế: API wrapper
async function fetchData(url, options = { method: "GET", headers: {} }) {
  const res = await fetch(url, options);
  return res.json();
}
```

## Liên kết chéo

- Xem: `20_modern-javascript/04_enhanced-literals-default-params/01_enhanced-object-literals`
- Xem: `09_functions/01_parameters-and-arrow/06_function-parameters`
