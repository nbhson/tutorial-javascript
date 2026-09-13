# Enhanced Object Literals

## 🔑 Khái niệm

ES2015 (ES6) thêm 3 tính năng object literal:

1. **Shorthand properties**: `{ x }` thay vì `{ x: x }`
2. **Shorthand methods**: `{ foo() {} }` thay vì `{ foo: function() {} }`
3. **Computed property names**: `{ [expr]: value }`

## ✅ Điểm mạnh
- Code ngắn gọn, dễ đọc
- Method shorthand có `prototype` đúng, `super` accessible
- Computed key tạo dynamic property name

## ⚠️ Lưu ý
- Shorthand method không có `function` keyword → không hoist
- Super trong shorthand method hoạt động, super trong regular method không
- Computed key eval mỗi lần → nếu dùng biến tĩnh nên gán ra ngoài

## 💡 Khi nào dùng
- Object literal nhanh (API response mapper)
- Class-like factory function
- Dynamic config object

## 🎯 Ví dụ minh họa

### Shorthand property
```js
const name = "Nguyễn";
const age = 25;
// Trước: { name: name, age: age }
const user = { name, age };
console.log(user); // { name: "Nguyễn", age: 25 }
```

### Shorthand method
```js
const calculator = {
  add(a, b) { return a + b; },
  multiply(a, b) { return a * b; },
  // method có access this
  summary() { return `${this.a} + ${this.b} = ${this.add(this.a, this.b)}`; }
};
```

### Computed property name
```js
const suffix = "Id";
const obj = {
  [`user${suffix}`]: 42,
  [`is${suffix}Active`]: true
};
// { userId: 42, isIdActive: true }

// Trong loop
const dynamic = {};
["a", "b", "c"].forEach(k => { dynamic[k] = k.toUpperCase(); });
```

## 📚 Tham khảo & Bài tập
- File: `app.js`, `index.html` trong folder `01_enhanced-object-literals/`
- Thực hành: tạo object literal từ API response với computed key
- Câu hỏi: computed key trong object literal khác gì `Object.defineProperty`?
