# Classes trong JavaScript — [Level: Intermediate]

## 🔑 Khái niệm cốt lõi

**Class** là cú pháp (ES6, 2015) để tạo **khuôn mẫu (blueprint)** sinh ra các object giống nhau. Quan trọng: class trong JS chỉ là **syntactic sugar** trên nền **prototype** — bản chất vẫn là function constructor + prototype chain, chỉ được viết gọn và rõ ràng hơn.

```js
class Course {
  constructor(name, price) {
    this.name = name;
    this.price = price;
  }
  getName() {
    return this.name;
  }
}
const c = new Course("JS", 100);
```

Dưới bề mặt, class trên tương đương với:
```js
function Course(name, price) {
  this.name = name;
  this.price = price;
}
Course.prototype.getName = function() {
  return this.name;
};
```

Các thành phần của class:
- **`constructor()`** — hàm khởi tạo, tự chạy khi `new`.
- **Phương thức (methods)** — định nghĩa trên `prototype`, dùng chung cho mọi instance.
- **`extends`** — kế thừa lớp cha, đi cùng `super()`.
- **`static`** — thuộc tính/phương thức gắn với class, không phải instance.
- **`#field`** — thuộc tính **private** (ES2022), chỉ truy cập bên trong class.

## 📐 Cấu trúc / Cú pháp

### Class declaration

```js
class ClassName {
  // Constructor
  constructor(param1, param2) {
    this.param1 = param1;
    this.param2 = param2;
  }
  
  // Instance method
  method1() {
    return this.param1;
  }
  
  // Getter
  get computed() {
    return this.param1 + this.param2;
  }
  
  // Setter
  set computed(value) {
    this.param1 = value;
  }
  
  // Static method
  static staticMethod() {
    return "called on class";
  }
  
  // Private field (ES2022)
  #privateField = 42;
  
  #privateMethod() {
    return this.#privateField;
  }
}
```

### Class expression

```js
const ClassName = class {
  constructor() { ... }
};

// Named class expression (name available inside class)
const Foo = class Foo {
  static isFoo() { return this === Foo; }
};
```

### Bảng thành viên class

| Thành viên | Truy cập từ | Ví dụ |
|------------|-------------|-------|
| `constructor` | `new ClassName()` | `new User("An")` |
| Instance method | `instance.method()` | `user.getName()` |
| Static method | `ClassName.method()` | `User.count()` |
| Private field `#x` | Inside class only | `this.#x` |
| Getter `get x()` | `instance.x` | `user.name` |
| Setter `set x(v)` | `instance.x = v` | `user.name = "New"` |

## ✅ Điểm mạnh — Tại sao nên dùng

1. **Cú pháp sạch, dễ đọc** so với function constructor + prototype thủ công.
2. **Kế thừa bằng `extends` + `super()`** rõ ràng như các ngôn ngữ OOP khác.
3. **Đóng gói dữ liệu** với private field `#`.
4. **`instanceof`** kiểm tra quan hệ kế thừa dễ dàng.
5. **Nền tảng framework** — React class component, Angular, NestJS đều dựa trên class.
6. **Tooling support** — TypeScript, linters, IDE auto-complete tốt hơn.
7. **Code organization** — gom data + behavior vào một khuôn mẫu.
8. **Memory efficient** — methods trên prototype, không tạo lại mỗi instance.

## ⚠️ Bẫy thường gặp & Hạn chế

### Bẫy 1: Class không được hoisting — phải khai báo trước khi dùng

```js
const obj = new MyClass(); // ❌ ReferenceError
class MyClass {} // ✅ khai báo sau

// So với function declaration:
const obj2 = new MyFunc(); // ✅ works (hoisting)
function MyFunc() {}
```

### Bẫy 2: Thân class luôn chạy strict mode

```js
class Foo {
  method() {
    console.log(this); // undefined nếu gọi không đúng cách
  }
}
// Không thể tắt strict mode trong class
```

### Bẫy 3: Method không tự bind `this`

```js
class Button {
  constructor(label) { this.label = label; }
  click() { console.log(this.label); }
}
const btn = new Button("Submit");
const fn = btn.click;
fn(); // ❌ undefined — this mất context
// Fix: btn.click.bind(btn) hoặc arrow field
```

### Bẫy 4: `super()` bắt buộc trước `this` trong subclass constructor

```js
class Animal {}
class Dog extends Animal {
  constructor() {
    this.legs = 4; // ❌ ReferenceError
    super();       // ✅ phải trước this
  }
}
```

### Bẫy 5: Class methods không tự động bind trong React

```jsx
class MyComponent extends React.Component {
  handleClick() { console.log(this.state); }
  render() {
    return <button onClick={this.handleClick}>Click</button>;
    // ❌ this.handleClick là undefined khi gọi
    // Fix: constructor bind hoặc arrow method
  }
}
```

## 💡 Khi nào dùng — Tình huống thực tế

1. **Mô hình hóa đối tượng** có dữ liệu + hành vi: User, Product, Order...
2. **Cần kế thừa và tái sử dụng code** giữa các "loại" đối tượng.
3. **Viết code hướng đối tượng** trong frontend/backend Node.js.
4. **Framework components** — React class component, Angular controller.
5. **Library/API design** — public class interface cho developer khác dùng.
6. **Stateful objects** — object cần giữ state và có methods thao tác state.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Basic class

```js
class Animal {
  constructor(name) {
    this.name = name;
  }
  speak() {
    console.log(this.name + " makes noise");
  }
}
class Dog extends Animal {
  speak() {
    super.speak();          // gọi phương thức cha
    console.log(this.name + " barks");
  }
}
new Dog("Rex").speak();
// Rex makes noise
// Rex barks
```

### Ví dụ 2: Class với getter/setter

```js
class BankAccount {
  constructor(owner, balance = 0) {
    this.#owner = owner;
    this.#balance = balance;
  }
  
  get balance() { return this.#balance; }
  get owner() { return this.#owner; }
  
  deposit(amount) {
    if (amount <= 0) throw new Error("Must be positive");
    this.#balance += amount;
  }
  
  withdraw(amount) {
    if (amount > this.#balance) throw new Error("Insufficient funds");
    this.#balance -= amount;
  }
}

const account = new BankAccount("Alice", 1000);
account.deposit(500);
console.log(account.balance); // 1500
```

### Ví dụ 3: Static methods và fields

```js
class Counter {
  static count = 0;           // static field (ES2022)
  
  static increment() {
    Counter.count++;
  }
  
  static reset() {
    Counter.count = 0;
  }
}

Counter.increment();
Counter.increment();
console.log(Counter.count); // 2
```

### Ví dụ 4: Private fields encapsulation

```js
class SecureStorage {
  #data = {};
  #encryptionKey;
  
  constructor(key) {
    this.#encryptionKey = key;
  }
  
  set(key, value) {
    this.#data[key] = this.#encrypt(value, this.#encryptionKey);
  }
  
  get(key) {
    return this.#decrypt(this.#data[key], this.#encryptionKey);
  }
  
  #encrypt(value, key) { /* ... */ return value; }
  #decrypt(value, key) { /* ... */ return value; }
}
```

### Ví dụ 5: Class với array of instances

```js
class Course {
  static all = [];
  static count() { return Course.all.length; }
  
  constructor(name, price) {
    this.name = name;
    this.price = price;
    Course.all.push(this);
  }
}

new Course("HTML", 0);
new Course("CSS", 0);
new Course("JS", 100);
console.log(Course.count()); // 3
console.log(Course.all[0].name); // "HTML"
```

### Ví dụ 6: Mixin pattern với class

```js
const Flyable = {
  fly() { return `${this.name} is flying!`; }
};

const Swimmable = {
  swim() { return `${this.name} is swimming!` };
};

class Duck {
  constructor(name) { this.name = name; }
}
Object.assign(Duck.prototype, Flyable, Swimmable);

const donald = new Duck("Donald");
console.log(donald.fly()); // "Donald is flying!"
console.log(donald.swim()); // "Donald is swimming!"
```

### Ví dụ 7: Abstract-like class pattern

```js
class Shape {
  constructor(color) {
    if (new.target === Shape) {
      throw new Error("Cannot instantiate Abstract class");
    }
    this.color = color;
  }
  area() {
    throw new Error("Method 'area()' must be implemented");
  }
}

class Circle extends Shape {
  constructor(color, radius) {
    super(color);
    this.radius = radius;
  }
  area() {
    return Math.PI * this.radius ** 2;
  }
}
```

## 🔬 So sánh với alternatives

| Approach | Syntax | Inheritance | Private fields | Browser support |
|----------|--------|-------------|----------------|-----------------|
| Class (ES6) | Clean | `extends`/`super` | `#` (ES2022) | All modern |
| Constructor + prototype | Verbose | Manual | None (convention) | All |
| Object.create | Functional | Prototype chain | Symbols | All modern |
| Factory function | Flexible | Composition | Closures | All |

## 📊 Performance & Best Practices

- **Methods trên prototype** — chỉ tồn tại 1 bản, tiết kiệm bộ nhớ so với định nghĩa trong constructor.
- **Arrow field methods** (`method = () => {}`) tự bind this — tiện trong React nhưng tạo method mới mỗi instance.
- **Tránh class quá sâu** — kế thừa > 3 level khó bảo trì, dùng composition thay.
- **Static methods** cho utility không cần instance state.
- **Private fields `#`** — enforce encapsulation, nhưng không compile-time enforced (reflect có thể access).
- **Use `instanceof`** cẩn thận —跨 iframe/window khác nhau có thể sai.

## 🔗 Liên kết chéo

- **Xem thêm:** `14_classes/01_basics` — class fundamentals
- **Xem thêm:** `14_classes/02_constructor` — constructor chi tiết
- **Xem thêm:** `14_classes/03_inheritance` — extends và super
- **Xem thêm:** `14_classes/04_static-private` — static và private fields
- **Xem thêm:** `10_this-keyword/README` — this binding trong class
- **Xem thêm:** `02_data-types/02_objects-and-prototype/01_object-basics` — prototype foundation
- **Xem thêm:** `11_function-borrowing/03_call` — call trong inheritance pattern
