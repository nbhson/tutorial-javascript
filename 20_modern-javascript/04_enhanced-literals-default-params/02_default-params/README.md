# Default Parameters

## 🔑 Khái niệm

ES2015 (ES6) cho phép gán giá trị mặc định cho function parameters:
```js
function greet(name = "Guest", age = 0) {
  return `Hello ${name}, age ${age}`;
}
```

Nếu argument là `undefined` (hoặc không truyền) → dùng default. Nếu là `null` → dùng `null`.

## ✅ Điểm mạnh
- Giảm boilerplate `if (x === undefined) x = default`
- Hỗ trợ expression: `function foo(x = computeDefault())`
- Hỗ trợ destructuring default: `function bar({ role = "user" } = {})`

## ⚠️ Lưu ý
- `null` KHÔNG trigger default — chỉ `undefined` và missing argument
- Default param eval **mỗi lần** gọi function → side effect lặp nếu dùng function call
- Rest parameter không thể có default

## 💡 Khi nào dùng
- Function có nhiều optional params
- Config object pattern
- API wrapper với default options

## 🎯 Ví dụ minh họa

### Cơ bản
```js
function createuser(name = "Anonymous", role = "user") {
  return { name, role, createdAt: new Date() };
}
console.log(createuser());           // { name: "Anonymous", role: "user" }
console.log(createuser("A"));        // { name: "A", role: "user" }
console.log(createuser("A", "admin")); // { name: "A", role: "admin" }
```

### Expression default
```js
function randomId(length = Math.floor(Math.random() * 10) + 5) {
  return Math.random().toString(36).slice(2, length + 2);
}
```

### Destructuring default
```js
function configure({ timeout = 5000, retries = 3 } = {}) {
  console.log(timeout, retries);
}
configure();       // 5000 3
configure({});     // 5000 3
configure({ timeout: 1000 }); // 1000 3
```

## 📚 Tham khảo & Bài tập
- File: `app.js`, `index.html` trong folder `02_default-params/`
- Thực hành: viết function `mergeConfig(defaults, overrides)` với default params
- Câu hỏi: `null ?? defaultValue` vs `null = defaultValue` khác nhau ở đâu?
