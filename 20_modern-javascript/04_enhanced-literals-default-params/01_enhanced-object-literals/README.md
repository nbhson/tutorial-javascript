# Enhanced Object Literals

## Khái niệm

ES2015 (ES6) thêm 3 tính năng object literal:

1. **Shorthand properties**: `{ x }` thay vì `{ x: x }`
2. **Shorthand methods**: `{ foo() {} }` thay vì `{ foo: function() {} }`
3. **Computed property names**: `{ [expr]: value }`

## Điểm mạnh

- Code ngắn gọn, dễ đọc
- Method shorthand có `prototype` đúng, `super` accessible
- Computed key tạo dynamic property name
- Super trong method shorthand hoạt động đúng

## Bẫy thường gặp

### Bẫy 1: Shorthand method không hoist
```js
const obj = {
  foo() { this.bar(); }, // method shorthand
  bar() { console.log("bar"); }
};
obj.foo(); // "bar" ✓

// Nhưng nếu gọi trước khi định nghĩa:
// const obj = { foo() { this.bar(); } };
// obj.foo(); // TypeError: this.bar is not a function
```

### Bẫy 2: Super trong regular function property
```js
class Parent { greet() { return "Parent"; } }
class Child extends Parent {
  // Shorthand method -- super hoạt động
  greet() { return super.greet() + " Child"; }
}
```

### Bẫy 3: Computed key eval mỗi lần
```js
const key = "dynamic";
const obj = { [key]: 1, [key + "2"]: 2 }; // computed mỗi lần tạo object
```

## Khi nào dùng

- Object literal nhanh (API response mapper)
- Class-like factory function
- Dynamic config object
- Redux action creators

## Ví dụ

```js
// Shorthand property
const name = "Nguyễn";
const age = 25;
const user = { name, age }; // thay vì { name: name, age: age }

// Shorthand method
const calculator = {
  add(a, b) { return a + b; },
  multiply(a, b) { return a * b; },
  summary() { return `${this.a} + ${this.b} = ${this.add(this.a, this.b)}`; }
};

// Computed property name
const suffix = "Id";
const obj = {
  [`user${suffix}`]: 42,
  [`isActive`]: true
};
// { userId: 42, isActive: true }

// Dynamic keys trong loop
const dynamic = {};
["a", "b", "c"].forEach(k => { dynamic[k] = k.toUpperCase(); });
// { a: "A", b: "B", c: "C" }
```

## Liên kết chéo

- Xem: `20_modern-javascript/04_enhanced-literals-default-params/02_default-params`
- Xem: `02_data-types/02_objects-and-prototype`
