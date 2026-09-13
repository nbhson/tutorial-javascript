# Classes — Khởi đầu (Basics) — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

`class` là **syntactic sugar** của cơ chế **prototype**: những gì class viết gọn, phiên bản cũ phải viết bằng function constructor + `prototype` — cùng một bản chất.

So sánh:

```js
// Cách cũ: function constructor + prototype
function Course(name, price) {
  this.name = name;
  this.price = price;
}
Course.prototype.getName = function() {
  return this.name;
};
Course.prototype.getPrice = function() {
  return this.price;
};

// Cách mới: class (tương đương)
class Course {
  constructor(name, price) {
    this.name = name;
    this.price = price;
  }
  getName() {
    return this.name;
  }
  getPrice() {
    return this.price;
  }
}
```

Những điểm cốt lõi:
- **`constructor`** chạy khi `new` — khởi tạo dữ liệu của instance.
- **Phương thức khai báo trong class** được đặt trên `prototype` — mọi instance dùng chung, không tạo lại mỗi lần `new`.
- Vẫn có thể "núp" thêm method vào `Course.prototype` từ bên ngoài — chứng tỏ class không cô lập với prototype.
- `new Class(...)` tạo object mới, gọi constructor với `this = instance`.

## 📐 Cấu trúc / Cú pháp

### Class anatomy

```js
class ClassName {
  // 1. Constructor — khởi tạo instance
  constructor(param1, param2) {
    this.param1 = param1; // instance property
    this.param2 = param2;
  }
  
  // 2. Instance methods — đặt trên prototype
  method1() { return this.param1; }
  method2() { return this.param2; }
  
  // 3. Getter — property accessor
  get fullName() {
    return `${this.param1} ${this.param2}`;
  }
  
  // 4. Setter — property mutator
  set fullName(value) {
    [this.param1, this.param2] = value.split(" ");
  }
}
```

### Tạo instance

```js
const instance = new ClassName(arg1, arg2);
// 1. Tạo object rỗng {}
// 2. Set [[Prototype]] → ClassName.prototype
// 3. Gọi constructor với this = object mới
// 4. Return object mới (trừ khi constructor return object khác)
```

### Bảng so sánh class vs constructor

| Đặc tính | Function Constructor | Class |
|----------|---------------------|-------|
| Syntax | `function Foo() { this.x = 1; }` | `class Foo { constructor() { this.x = 1; } }` |
| Hoisting | ✅ function declaration | ❌ must declare before use |
| Strict mode | Optional | Automatic |
| Prototype methods | `Foo.prototype.method = ...` | `method() { }` inside class |
| Readability | Verbose | Clean |

## ✅ Điểm mạnh — Tại sao nên dùng

1. **Code ngắn gọn**, tổ chức rõ ràng hơn function constructor.
2. **Các method nằm trên `prototype`** → tiết kiệm bộ nhớ, easy for fix chung.
3. **Quen thuộc** với lập trình viên biết OOP từ ngôn ngữ khác (Java, C#, Python).
4. **Tương thích** với mọi thư viện/framework dùng `new`.
5. **Dễ debug** — stack trace rõ ràng hơn constructor pattern.
6. **IDE support** — auto-complete, type checking (với TypeScript).
7. **Extension dễ** — `extends` cho inheritance rõ ràng.
8. **Standard** — ES6+, supported在所有现代浏览器.

## ⚠️ Bẫy thường gặp & Hạn chế

### Bẫy 1: Class không được hoisting

```js
const c = new Course("JS", 100); // ❌ ReferenceError: Cannot access 'Course' before initialization
class Course { constructor(name, price) { this.name = name; } }
// Fix: khai báo class trước khi dùng
```

### Bẫy 2: Thân class luôn strict mode

```js
class Foo {
  method() {
    x = 1; // ❌ TypeError: Cannot assign to read only property 'x' (strict mode)
  }
}
```

### Bẫy 3: Method không tự bind `this`

```js
class Button {
  constructor(label) { this.label = label; }
  click() { console.log(this.label); }
}
const btn = new Button("Submit");
const fn = btn.click;
fn(); // ❌ undefined — this lost
// Fix: btn.click.bind(btn) hoặc onclick={() => btn.click()}
```

### Bẫy 4: Thêm method vào prototype từ ngoài vẫn hoạt động

```js
class Course {
  constructor(name) { this.name = name; }
}
// Thêm method từ ngoài
Course.prototype.info = function() {
  return `Course: ${this.name}`;
};
const c = new Course("JS");
console.log(c.info()); // "Course: JS" — prototype accessible
```

### Bẫy 5: `new` bỏ qua nếu quên — this = window/undefined

```js
class Person {
  constructor(name) { this.name = name; }
}
const p = Person("Alice"); // ❌ quên new — this = globalThis
console.log(window.name); // "Alice" —污染 global scope
```

## 💡 Khi nào dùng — Tình huống thực tế

1. **Tạo nhiều instance cùng cấu trúc**: Course, User, Product...
2. **Gom dữ liệu + hành vi** vào một "khuôn" dễ tái sử dụng.
3. **Nền tảng** trước khi học `extends`, `static`, private fields.
4. **React class component** (legacy codebase).
5. **Node.js backend models** — User model, Product model.
6. **Game objects** — Player, Enemy, Item với methods riêng.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Basic class với constructor

```js
class Course {
  constructor(name, price) {
    this.name = name;
    this.price = price;
  }
  getName() {
    return this.name;
  }
  getPrice() {
    return this.price;
  }
}

const js = new Course("JavaScript", 100);
const py = new Course("Python", 80);

console.log(js.getName()); // "JavaScript"
console.log(py.getPrice()); // 80
console.log(js instanceof Course); // true
```

### Ví dụ 2: Thêm method vào prototype từ ngoài

```js
class Course {
  constructor(name, price) {
    this.name = name;
    this.price = price;
  }
}

// Thêm method từ bên ngoài class definition
Course.prototype.info = function () {
  return `${this.name} — ${this.price}$`;
};

const c = new Course("HTML", "Free");
console.log(c.info()); // "HTML — Free$"
console.log(c instanceof Course); // true
console.log(Course.prototype.isPrototypeOf(c)); // true
```

### Ví dụ 3: Getter và Setter

```js
class Rectangle {
  constructor(width, height) {
    this.width = width;
    this.height = height;
  }
  
  get area() {
    return this.width * this.height;
  }
  
  set scale(factor) {
    this.width *= factor;
    this.height *= factor;
  }
}

const rect = new Rectangle(10, 5);
console.log(rect.area); // 50
rect.scale = 2;
console.log(rect.area); // 200
```

### Ví dụ 4: Class với array storage (static)

```js
class Team {
  static members = [];
  
  constructor(name) {
    this.name = name;
    Team.members.push(this);
  }
  
  static getMembers() {
    return Team.members.map(m => m.name);
  }
}

new Team("Alice");
new Team("Bob");
new Team("Charlie");
console.log(Team.getMembers()); // ["Alice", "Bob", "Charlie"]
```

### Ví dụ 5: So sánh class vs constructor

```js
// Constructor pattern
function Person(name, age) {
  this.name = name;
  this.age = age;
}
Person.prototype.greet = function() {
  return `Hi, I'm ${this.name}, ${this.age} years old`;
};

// Class pattern (tương đương)
class PersonClass {
  constructor(name, age) {
    this.name = name;
    this.age = age;
  }
  greet() {
    return `Hi, I'm ${this.name}, ${this.age} years old`;
  }
}

const p1 = new Person("An", 20);
const p2 = new PersonClass("An", 20);
console.log(p1.greet()); // "Hi, I'm An, 20 years old"
console.log(p2.greet()); // "Hi, I'm An, 20 years old"
console.log(p1 instanceof Person); // true
console.log(p2 instanceof PersonClass); // true
```

### Ví dụ 6: Class với default parameters

```js
class User {
  constructor(name, role = "user", active = true) {
    this.name = name;
    this.role = role;
    this.active = active;
  }
  
  isAdmin() {
    return this.role === "admin";
  }
}

const admin = new User("SuperUser", "admin");
const normal = new User("RegularUser"); // role = "user", active = true
console.log(admin.isAdmin()); // true
console.log(normal.isAdmin()); // false
console.log(normal.active); // true
```

### Ví dụ 7: Validate in constructor

```js
class Product {
  constructor(name, price) {
    if (typeof name !== "string" || name.trim() === "") {
      throw new Error("Name must be a non-empty string");
    }
    if (typeof price !== "number" || price < 0) {
      throw new Error("Price must be a non-negative number");
    }
    this.name = name;
    this.price = price;
  }
}

try {
  const p = new Product("", -10);
} catch (err) {
  console.error(err.message); // "Name must be a non-empty string"
}
```

## 🔬 So sánh với alternatives

| Pattern | Syntax | this binding | Private fields | Best for |
|---------|--------|--------------|----------------|----------|
| Class | Clean | Implicit | `#` (ES2022) | OOP modern JS |
| Constructor | Verbose | Implicit | None (convention) | Legacy code |
| Factory function | Flexible | Explicit return | Closure | Functional style |
| Object.create | Minimal | Manual | Symbols | Minimalist |

## 📊 Performance & Best Practices

- **Methods trên prototype** — chỉ 1 bản cho tất cả instance, tiết kiệm memory.
- **Class fields (arrow methods)** — `method = () => {}` tạo method mới mỗi instance — dùng khi cần bind tự động.
- **Constructor validation** — validate inputs ngay trong constructor.
- **Avoid deep inheritance** — max 2-3 levels, prefer composition.
- **Use `instanceof`** cẩn thận — cross-realm (iframe) có thể sai.

## 🔗 Liên kết chéo

- **Xem thêm:** `14_classes/02_constructor` — constructor chi tiết
- **Xem thêm:** `14_classes/03_inheritance` — extends and super
- **Xem thêm:** `14_classes/04_static-private` — static và private
- **Xem thêm:** `10_this-keyword/README` — this binding trong class
- **Xem thêm:** `02_data-types/02_objects-and-prototype/01_object-basics` — prototype foundation
- **Xem thêm:** `11_function-borrowing/03_call` — call/apply trong inheritance
