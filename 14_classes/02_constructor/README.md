# Classes — Constructor — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

**`constructor`** là hàm khởi tạo của class — **mỗi class chỉ có một**. Khi bạn gọi `new User(...)`:

1. Tạo object mới (instance) — `{}`.
2. Set `[[Prototype]]` của object mới → `User.prototype`.
3. Gọi `constructor` với `this` = instance đó.
4. Instance được gán các thuộc tính (qua `this.name = ...`).
5. Trả về instance.

```js
class User {
  constructor(name, age) {
    this.name = name;
    this.age = age;
  }
}
const u = new User("An", 20);
console.log(u); // User { name: "An", age: 20 }
```

**Quy tắc với subclass:**
- Subclass **phải gọi `super(...)`** ở đầu constructor — **trước khi dùng `this`** — nếu không sẽ báo lỗi `ReferenceError`.
- `super(...)` chạy constructor của lớp cha, khởi tạo phần dữ liệu cha trước, sau đó subclass mới khởi tạo phần riêng.

**Default constructor:** Nếu không khai báo `constructor`, JS tự tạo empty constructor: `constructor() {}`.

## 📐 Cấu trúc / Cú pháp

### Constructor signature

```js
class ClassName {
  constructor(param1, param2, ...) {
    this.prop1 = param1;
    this.prop2 = param2;
    // ... init logic
  }
}
```

### Subclass với super()

```js
class Parent {
  constructor(x, y) {
    this.x = x;
    this.y = y;
  }
}

class Child extends Parent {
  constructor(x, y, z) {
    super(x, y);  // ✅ gọi constructor cha TRƯỚC
    this.z = z;   // ✅ sau đó mới dùng this
  }
}
```

### Bảng rules của constructor

| Quy tắc | Mô tả |
|---------|--------|
| Một class chỉ một constructor | Không overloading như Java/C# |
| `super()` bắt buộc trước `this` trong subclass | Nếu có constructor |
| Tự động gọi `super()` | Nếu subclass không khai báo constructor |
| Constructor có thể return object | Nhưng `new` luôn return instance (bỏ qua return value trừ khi return object khác) |
| Arrow function không thể là constructor | `new (() => {})()` → TypeError |

## ✅ Điểm mạnh — Tại sao nên dùng

1. **Khởi tạo dữ liệu instance** ngay, rõ ràng và nhất quán.
2. **Bắt buộc quy trình cha → con** qua `super()` tránh quên khởi tạo class cha.
3. **Cú pháp một lần `new`** gọn gàng so với function constructor.
4. **Dễ thêm logic mặc định** — ép kiểu, giá trị fallback, validation.
5. **Encapsulation** — data được set ngay khi create, khó state inconsistency.
6. **Factory pattern alternative** — `new` rõ ràng hơn factory function.

## ⚠️ Bẫy thường gặp & Hạn chế

### Bẫy 1: Quên `super()` trong subclass constructor

```js
class Animal {}
class Dog extends Animal {
  constructor() {
    this.legs = 4; // ❌ ReferenceError: Must call super constructor
  }
}
// Fix: thêm super() trước
class Dog extends Animal {
  constructor() {
    super(); // ✅
    this.legs = 4;
  }
}
```

### Bẫy 2: Gọi `super()` sau khi dùng `this`

```js
class Dog extends Animal {
  constructor() {
    this.legs = 4; // ❌ ReferenceError
    super();       // quá muộn
  }
}
```

### Bẫy 3: Constructor không overloading — chỉ có một

```js
class Point {
  constructor(x, y) {
    this.x = x;
    this.y = y;
  }
  // constructor(x) { ... } // ❌ SyntaxError — duplicate constructor
}
// Fix: dùng default parameters hoặc static factory method
class Point {
  constructor(x, y = 0) {
    this.x = x;
    this.y = y;
  }
}
```

### Bẫy 4: Constructor return object khác — `new` bỏ qua

```js
class Foo {
  constructor() {
    this.x = 1;
    return { y: 2 }; // return object khác
  }
}
const f = new Foo();
console.log(f.x); // undefined — f là {y: 2}, không phải Foo instance
console.log(f.y); // 2
```

### Bẫy 5: Gọi constructor không qua `new` — this = window/undefined

```js
class User {
  constructor(name) { this.name = name; }
}
const u = User("Alice"); // ❌ quên new
console.log(window.name); // "Alice" — làm bẩn global
```

## 💡 Khi nào dùng — Tình huống thực tế

1. **Tạo instance cần tham số đầu vào** — name, age, price...
2. **Chuẩn hóa dữ liệu đầu vào** khi khởi tạo — trim, number, default...
3. **Subclass cần khởi tạo lớp cha** rồi mới thêm thuộc tính riêng.
4. **Validation đầu vào** — throw error nếu params không hợp lệ.
5. **Side effects during creation** — log, register, subscribe.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Basic constructor

```js
class User {
  constructor(name, age) {
    this.name = name;
    this.age = age;
  }
}

const u = new User("An", 20);
console.log(u); // User { name: "An", age: 20 }
console.log(u.name); // "An"
console.log(u.age); // 20
```

### Ví dụ 2: Subclass với super()

```js
class User {
  constructor(name, age) {
    this.name = name;
    this.age = age;
  }
  greet() {
    return `Hi, I'm ${this.name}`;
  }
}

class Admin extends User {
  constructor(name, age, role) {
    super(name, age);   // khởi tạo User trước
    this.role = role;   // sau đó mới dùng this
  }
  administer() {
    return `${this.name} (admin: ${this.role}) is managing`;
  }
}

const u = new User("An", 20);
console.log(u);               // User { name: "An", age: 20 }
console.log(u.greet());       // "Hi, I'm An"

const a = new Admin("B", 25, "superadmin");
console.log(a);               // Admin { name: "B", age: 25, role: "superadmin" }
console.log(a.greet());       // "Hi, I'm B" (inherited)
console.log(a.administer());  // "B (admin: superadmin) is managing"
```

### Ví dụ 3: Constructor với default parameters

```js
class Product {
  constructor(name, price = 0, category = "general") {
    this.name = name;
    this.price = price;
    this.category = category;
  }
}

const p1 = new Product("Laptop");           // price=0, category="general"
const p2 = new Product("Phone", 500);       // category="general"
const p3 = new Product("Book", 10, "education");
```

### Ví dụ 4: Constructor validation

```js
class BankAccount {
  constructor(owner, initialBalance = 0) {
    if (typeof owner !== "string" || owner.trim() === "") {
      throw new Error("Owner name is required");
    }
    if (initialBalance < 0) {
      throw new Error("Initial balance cannot be negative");
    }
    this.owner = owner;
    this.balance = initialBalance;
  }
}

try {
  const acc = new BankAccount("", -100);
} catch (err) {
  console.error(err.message); // "Owner name is required"
}
```

### Ví dụ 5: Default constructor (implicit)

```js
// Không khai báo constructor — JS tự tạo empty constructor
class Empty {
  // constructor() {}  // auto-generated
}
const e = new Empty();
console.log(e); // Empty {}
```

### Ví dụ 6: Constructor với computed property names

```js
class Config {
  constructor(settings) {
    for (const key of Object.keys(settings)) {
      this[`_${key}`] = settings[key]; // private-like via convention
    }
  }
  get(key) {
    return this[`_${key}`];
  }
}

const cfg = new Config({ host: "localhost", port: 3000 });
console.log(cfg.get("host")); // "localhost"
```

### Ví dụ 7: Static factory method alternative

```js
class DateRange {
  constructor(start, end) {
    this.start = start;
    this.end = end;
  }
  
  // Static factory — tạo instance từ string
  static fromISO(isoString) {
    const [start, end] = isoString.split("-");
    return new DateRange(new Date(start), new Date(end));
  }
  
  // Static factory — tạo từ milliseconds
  static fromMs(msStart, msEnd) {
    return new DateRange(new Date(msStart), new Date(msEnd));
  }
}

const range1 = DateRange.fromISO("2024-01-01-2024-12-31");
const range2 = DateRange.fromMs(0, 86400000);
```

### Ví dụ 8: Super() không đối số — automatic arguments forwarding

```js
class Animal {
  constructor(name, weight) {
    this.name = name;
    this.weight = weight;
  }
}

class Cat extends Animal {
  constructor(name, weight, color) {
    super(name, weight); // explicit args
    this.color = color;
  }
}

// Hoặc tự động forward tất cả arguments
class Dog extends Animal {
  constructor(...args) {
    super(...args); // forward all args to parent
    this.legs = 4;
  }
}

const dog = new Dog("Rex", 30);
console.log(dog.name); // "Rex"
console.log(dog.weight); // 30
console.log(dog.legs); // 4
```

## 🔬 So sánh với alternatives

| Pattern | Constructor call | Init logic | Inheritance |
|---------|-----------------|------------|-------------|
| Class + constructor | `new Foo()` | Inside constructor | `super()` |
| Constructor function | `new Foo()` | Inside function | `Parent.call(this)` |
| Factory function | `createFoo()` | Inside function | Composition |
| Object.create | `Object.create(proto)` | Manual | Prototype chain |

## 📊 Performance & Best Practices

- **Constructor nên nhanh** — tránh heavy computation, side effects phức tạp.
- **Validation sớm** — throw error ngay trong constructor để fail fast.
- **Default parameters** thay vì check `if (arg === undefined)` trong constructor body.
- **Static factory methods** cho complex creation logic — giữ constructor simple.
- **Không return object khác** từ constructor — gây confusing behavior.
- **Super() trước this** — quy tắc bắt buộc trong subclass.

## 🔗 Liên kết chéo

- **Xem thêm:** `14_classes/01_basics` — class basics overview
- **Xem thêm:** `14_classes/03_inheritance` — extends và super chi tiết
- **Xem thêm:** `14_classes/04_static-private` — static methods và private fields
- **Xem thêm:** `11_function-borrowing/03_call` — Parent.call(this) pattern (pre-class)
- **Xem thêm:** `10_this-keyword/README` — this binding trong constructor
- **Xem thêm:** `02_data-types/02_objects-and-prototype/01_object-basics` — prototype foundation
