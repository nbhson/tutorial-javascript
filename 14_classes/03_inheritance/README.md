# Classes — Kế thừa (Inheritance) với `extends` — [Level: Intermediate]

## 🔑 Khái niệm cốt lõi

**`extends`** cho phép một class **kế thừa toàn bộ prototype** của class cha: subclass có đầy đủ phương thức/dữ liệu của cha, đồng thời có thể **ghi đè (override)** hoặc bổ sung của riêng mình.

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
    super.speak();      // gọi phương thức cha, phải qua super
    console.log(this.name + " barks");
  }
}
```

Những điểm cốt lõi:
- **`super.speak()`** gọi phiên bản method của class cha — giữ lại hành vi cha rồi thêm hành vi con.
- **`super()`** trong constructor gọi constructor của cha (xem bài constructor).
- Prototype chain sau khi extends: `dog → Dog.prototype → Animal.prototype → Object.prototype`.
- **`instanceof`** kiểm tra theo **chuỗi prototype**: `dog instanceof Dog` và `dog instanceof Animal` đều `true`. Kiểm tra được cả cấp prototype của class: `Dog.prototype instanceof Animal` → `true`.

## 📐 Cấu trúc / Cú pháp

### Extends syntax

```js
class Parent {
  constructor(prop1) {
    this.prop1 = prop1;
  }
  method1() { return "parent"; }
}

class Child extends Parent {
  constructor(prop1, prop2) {
    super(prop1);         // gọi Parent constructor
    this.prop2 = prop2;   // init Child-specific props
  }
  
  method1() {
    return `${super.method1()} + child override`;
  }
  
  method2() {
    return "child only";
  }
}
```

### Prototype chain visualization

```
const child = new Child("a", "b");

child           → Child instance
  [[Prototype]] → Child.prototype
                   methods: method1(), method2()
                   [[Prototype]] → Animal.prototype (Parent)
                                   methods: constructor(), method1()
                                   [[Prototype]] → Object.prototype
                                                   methods: constructor(), toString(), ...
                                                   [[Prototype]] → null
```

### Bảng super usage

| Position | `super()` | `super.method()` |
|----------|-----------|------------------|
| Constructor | ✅ Bắt buộc (trước `this`) | ❌ Không dùng được |
| Instance method | ❌ Không dùng được | ✅ Gọi method của parent |
| Static method | ✅ (gọi parent static) | ✅ (gọi parent static method) |

## ✅ Điểm mạnh — Tại sao nên dùng

1. **Tái sử dụng code cha**, tránh lặp lại logic.
2. **Override linh hoạt** — gọi `super` rồi thêm hành vi riêng.
3. **Mối quan hệ "is-a"** (con là cha) kiểm tra được bằng `instanceof`.
4. **Phân cấp mô hình hóa** tự nhiên: Animal → Dog → Puppy...
5. **Polymorphism** — cùng method name, behavior khác nhau tùy instance type.
6. **Open/closed principle** — mở rộng behavior mà không sửa code cha.
7. **Interface contract** — subclass guaranteed có methods của parent.

## ⚠️ Bẫy thường gặp & Hạn chế

### Bẫy 1: Constructor subclass phải gọi `super()` trước `this`

```js
class Dog extends Animal {
  constructor(name) {
    this.legs = 4; // ❌ ReferenceError: must call super first
    super(name);
  }
}
// ✅ Đúng:
class Dog extends Animal {
  constructor(name) {
    super(name); // ✅ trước
    this.legs = 4;
  }
}
```

### Bẫy 2: Nếu subclass không có constructor — JS tự gọi `super(...arguments)`

```js
class Dog extends Animal {
  // không có constructor
  // JS tự thêm: constructor(...args) { super(...args); }
}
const dog = new Dog("Rex"); // ✅ works — auto super()
```

### Bẫy 3: Kế thừa nhiều tầng sâu gây khó đọc

```js
class A {}
class B extends A {}
class C extends B {}
class D extends C {} // quá sâu — khó maintain
// Fix: dùng composition thay inheritance
```

### Bẫy 4: `instanceof` có thể sai với跨 realm (iframe)

```js
// Trong iframe khác
iframeWindow.Array instanceof window.Array // false!
// Fix: dùng Array.isArray() hoặc Object.prototype.toString.call()
```

### Bẫy 5: Method không tự bind — khi tách ra callback vẫn mất this

```js
class App {
  constructor() { this.count = 0; }
  increment() { this.count++; }
}
const app = new App();
setTimeout(app.increment, 1000); // ❌ this không phải app
// Fix: app.increment.bind(app) hoặc arrow method
```

### Bẫy 6: Static methods không kế thừa qua instance

```js
class Parent {
  static staticMethod() { return "parent"; }
}
class Child extends Parent {}

console.log(Child.staticMethod()); // "parent" ✅
console.log((new Child()).staticMethod()); // ❌ TypeError
```

## 💡 Khi nào dùng — Tình huống thực tế

1. **Các loại đối tượng có chung gốc**: Animal (Dog/Cat), Shape (Circle/Square)...
2. **Muốn mở rộng class có sẵn**: thêm method, đổi hành vi speak.
3. **Tổ chức code nền tảng framework**, base class dùng chung.
4. **Component hierarchy** trong UI framework (React, Vue).
5. **Error class hierarchy**: `class CustomError extends Error`.
6. **Repository/DAO pattern**: base repository với CRUD methods, subclass override.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Basic inheritance với super.speak()

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
    super.speak();                       // Rex makes noise
    console.log(this.name + " barks");   // Rex barks
  }
}

const dog = new Dog("Rex");
dog.speak();
// Rex makes noise
// Rex barks
```

### Ví dụ 2: instanceof kiểm tra

```js
console.log(dog instanceof Dog);        // true
console.log(dog instanceof Animal);     // true (qua prototype chain)
console.log(Dog.prototype instanceof Animal); // true
console.log(dog instanceof Object);     // true (Object.prototype ở cuối chain)
```

### Ví dụ 3: Multiple levels inheritance

```js
class Creature {
  constructor(type) {
    this.type = type;
  }
  breathe() { return `${this.type} breathes`; }
}

class Animal extends Creature {
  constructor(name) {
    super("animal");
    this.name = name;
  }
  speak() { return `${this.name} makes sound`; }
}

class Dog extends Animal {
  constructor(name) {
    super(name);
  }
  speak() {
    return `${super.speak()} — Woof!`;
  }
  fetch() { return `${this.name} fetches the ball`; }
}

const rex = new Dog("Rex");
console.log(rex.breathe()); // "animal breathes"
console.log(rex.speak());   // "Rex makes sound — Woof!"
console.log(rex.fetch());   // "Rex fetches the ball"
console.log(rex instanceof Dog);      // true
console.log(rex instanceof Animal);   // true
console.log(rex instanceof Creature); // true
```

### Ví dụ 4: Override với super() trong constructor

```js
class Vehicle {
  constructor(brand) {
    this.brand = brand;
    this.wheels = 4;
  }
}

class Car extends Vehicle {
  constructor(brand, doors) {
    super(brand);           // kế thừa brand, wheels
    this.doors = doors;     // thêm property riêng
  }
  describe() {
    return `${this.brand} car with ${this.doors} doors`;
  }
}

const myCar = new Car("Tesla", 4);
console.log(myCar.describe()); // "Tesla car with 4 doors"
console.log(myCar.wheels);     // 4 (from Vehicle)
```

### Ví dụ 5: Error class hierarchy

```js
class AppError extends Error {
  constructor(message, code) {
    super(message);
    this.code = code;
    this.name = this.constructor.name;
  }
}

class NotFoundError extends AppError {
  constructor(resource) {
    super(`${resource} not found`, 404);
  }
}

class ValidationError extends AppError {
  constructor(field, message) {
    super(`Validation failed for ${field}: ${message}`, 400);
    this.field = field;
  }
}

try {
  throw new NotFoundError("User");
} catch (err) {
  console.log(err.name);    // "NotFoundError"
  console.log(err.code);    // 404
  console.log(err.message); // "User not found"
}
```

### Ví dụ 6: Polymorphism — same interface, different behavior

```js
class Shape {
  area() { throw new Error("Must implement area()"); }
  perimeter() { throw new Error("Must implement perimeter()"); }
}

class Circle extends Shape {
  constructor(radius) {
    super();
    this.radius = radius;
  }
  area() { return Math.PI * this.radius ** 2; }
  perimeter() { return 2 * Math.PI * this.radius; }
}

class Rectangle extends Shape {
  constructor(width, height) {
    super();
    this.width = width;
    this.height = height;
  }
  area() { return this.width * this.height; }
  perimeter() { return 2 * (this.width + this.height); }
}

const shapes = [new Circle(5), new Rectangle(4, 6)];
shapes.forEach(s => {
  console.log(`Area: ${s.area().toFixed(2)}, Perimeter: ${s.perimeter().toFixed(2)}`);
});
// Area: 78.54, Perimeter: 31.42 (Circle)
// Area: 24.00, Perimeter: 20.00 (Rectangle)
```

### Ví dụ 7: Mixin + extends kết hợp

```js
// Mixin: thêm behavior vào class
const Serializable = {
  toJSON() {
    return Object.entries(this)
      .filter(([k]) => !k.startsWith("_"))
      .reduce((obj, [k, v]) => { obj[k] = v; return obj; }, {});
  }
};

class Entity {
  constructor(id) { this.id = id; }
}

// Apply mixin
Object.assign(Entity.prototype, Serializable);

const entity = new Entity(123);
console.log(entity.toJSON()); // { id: 123 }
```

### Ví dụ 8: Private field inheritance limitation

```js
class Parent {
  #secret = "parent-secret";
  getSecret() { return this.#secret; }
}

class Child extends Parent {
  // ❌ Không thể truy cập parent.#secret
  // Chỉ có thể qua parent's public method getSecret()
  reveal() {
    return this.getSecret(); // ✅ qua public method
  }
}

const c = new Child();
console.log(c.getSecret()); // "parent-secret"
// console.log(c.#secret); // ❌ SyntaxError — private field không kế thừa truy cập trực tiếp
```

## 🔬 So sánh với alternatives

| Pattern | Syntax | Code reuse | Flexibility | Complexity |
|---------|--------|------------|-------------|------------|
| `extends` + `super` | Clean | High | Medium | Medium |
| Mixin / Composition | Flexible | Medium | High | High |
| Prototype delegation | Low-level | Low | Very High | High |
| Copy properties | Simple | Low | Low | Low |

## 📊 Performance & Best Practices

- **Giới hạn inheritance depth ≤ 3** — sâu hơn khó debug, khó maintain.
- **Prefer composition over inheritance** — tránh tight coupling giữa parent/child.
- **Override có gọi `super()`** — giữ hành vi cha, mở rộng thêm.
- **Dùng `instanceof`** cẩn thận — cross-frame không đáng tin.
- **Private fields `#` không accessible** từ subclass — design cho encapsulation.
- **Static methods** không override được qua instance — gọi qua class name.

## 🔗 Liên kết chéo

- **Xem thêm:** `14_classes/01_basics` — class fundamentals
- **Xem thêm:** `14_classes/02_constructor` — constructor và super() requirement
- **Xem thêm:** `14_classes/04_static-private` — static và private fields trong inheritance
- **Xem thêm:** `10_this-keyword/README` — this binding trong inherited methods
- **Xem thêm:** `02_data-types/02_objects-and-prototype/01_object-basics` — prototype chain foundation
- **Xem thêm:** `11_function-borrowing/03_call` — Parent.call(this) pre-class inheritance
