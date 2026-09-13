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
- Gán nhiều biến 1 dòng, rõ ràng
- Swap biến `[a, b] = [b, a]`
- Extract nested deeply: `const { user: { name } } = data`
- Default values: `const { role = "user" } = data`

## ⚠️ Lưu ý
- **Destructuring không gán lại** — tạo biến mới (trừ khi dùng `obj.prop = val`)
- `...rest` chỉ được **cuối cùng** trong destructuring
- Object destructuring với key trùng tên variable: `const { name } = obj` ↔ `const { name: name } = obj`
- Array destructuring bỏ qua phần tử không match (dùng `,` placeholder)

## 💡 Khi nào dùng
- React props extraction: `const { title, body } = props`
- API response handling: `const { data, meta } = response`
- Function param grouping
- Swap, rotate array elements

## 🎯 Ví dụ minh họa

### Array destructuring
```js
const point = [10, 20];
const [x, y] = point;
console.log(x, y); // 10 20

// Skip elements
const [first, , third] = [1, 2, 3];
console.log(first, third); // 1 3

// Default values
const [a = 10, b = 20] = [null, null];
console.log(a, b); // 10 20
```

### Object destructuring
```js
const user = { id: 1, name: "A", profile: { bio: "Dev" } };
const { name, profile: { bio } } = user;
console.log(name, bio); // A Dev

// Rename
const { name: userName, age: userAge = 0 } = user;

// Default + rest
const { role = "guest", ...rest } = user;
```

### Function parameters
```js
function greet({ name, age = 0 } = {}) {
  return `Hello ${name}, age ${age}`;
}
greet({ name: "A" }); // "Hello A, age 0"
```

### Rest parameters
```js
function multiply(factor, ...numbers) {
  return numbers.map(n => n * factor);
}
multiply(2, 1, 2, 3); // [2, 4, 6]
```

## 📚 Tham khảo & Bài tập
- File: `app.js`, `index.html` trong folder `01_destructuring-rest/`
- Thực hành: destructuring nested API response
- Câu hỏi: `const { a, a } = obj` có được không? (trả về lỗi SyntaxError)
