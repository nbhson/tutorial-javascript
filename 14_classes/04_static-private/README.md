# Classes — Static và Private — [Level: Intermediate]

## 🔑 Khái niệm cốt lõi

Class hỗ trợ hai hình thức thành viên đặc biệt:

### 1. `static` — thuộc tính/phương thức tĩnh

- Gắn với **chính class**, không phải instance.
- Truy cập qua `ClassName.staticMethod()` / `ClassName.staticField`.
- Bên trong static method, `this` trỏ tới **class** (không phải instance).
- Không thể truy cập instance properties (`this.prop`) — chỉ static properties khác.
- Không kế thừa qua instance — `(new Child()).staticMethod()` là **lỗi**.

### 2. `#private` — trường riêng tư (ES2022)

- Thuộc tính bắt đầu bằng `#` chỉ truy cập được **bên trong class**.
- Truy cập từ ngoài (`c.#value`) → **SyntaxError** (không phải TypeError — lỗi cú pháp, phát hiện lúc compile).
- Kết hợp getter/setter (`get value()` / `set value(v)`) để kiểm soát đọc/ghi.
- Private method `#methodName()` cũng chỉ accessible trong class.
- **Không kế thừa được** — subclass không thể truy cập parent private fields.

## 📐 Cấu trúc / Cú pháp

### Static syntax

```js
class Counter {
  static count = 0;           // static field (ES2022)
  
  static increment() {
    this.count++;             // this = Counter class
  }
  
  static reset() {
    this.count = 0;
  }
}

Counter.increment();
console.log(Counter.count); // 1
```

### Private syntax

```js
class SecureStore {
  #data = {};                  // private field
  #version = 1;                // private field
  
  #encrypt(value) {            // private method
    return `encrypted_${value}`;
  }
  
  set(key, value) {
    this.#data[key] = this.#encrypt(value);
  }
  
  get(key) {
    return this.#data[key];
  }
  
  get version() {
    return this.#version;
  }
}

const store = new SecureStore();
store.set("token", "abc123");
console.log(store.get("token")); // "encrypted_abc123"
// console.log(store.#data);      // ❌ SyntaxError
```

### Combined static + private

```js
class Database {
  static #instance = null;     // singleton private static
  
  static getInstance() {
    if (!Database.#instance) {
      Database.#instance = new Database();
    }
    return Database.#instance;
  }
  
  #connections = [];
  
  connect(url) {
    this.#connections.push(url);
  }
}
```

## ✅ Điểm mạnh — Tại sao nên dùng

1. **`static` dùng chung** dữ liệu/hàm tiện ích không cần instance (counter, config, helper).
2. **`#private` bảo vệ** dữ liệu nội bộ — không thể sửa trực tiếp từ ngoài.
3. **Getter/setter** cho phép kiểm soát (validate) khi đọc ghi.
4. **Đúng chuẩn OOP**: đóng gói (encapsulation) thật sự.
5. **Singleton pattern** dễ implement với static + private.
6. **Namespace organization** — static methods như utility functions trong class.
7. **Compile-time enforcement** — private fields gây SyntaxError nếu truy cập sai.

## ⚠️ Bẫy thường gặp & Hạn chế

### Bẫy 1: Static method không truy cập được instance properties

```js
class Foo {
  constructor() { this.x = 1; }
  static method() {
    console.log(this.x); // ❌ undefined — this là class, không phải instance
  }
}
Foo.method(); // undefined
```

### Bẫy 2: Private field truy cập từ ngoài → SyntaxError

```js
class Foo {
  #x = 1;
}
const f = new Foo();
console.log(f.#x); // ❌ SyntaxError: Private field '#x' must be declared
// Lỗi ở phase parse, không phải runtime
```

### Bẫy 3: Private fields không kế thừa được

```js
class Parent {
  #secret = "parent-secret";
}
class Child extends Parent {
  reveal() {
    return this.#secret; // ❌ ReferenceError — private field không visible in subclass
  }
}
```

### Bẫy 4: Reflection có thể access private field qua String

```js
class Foo {
  #secret = 42;
}
const f = new Foo();
// ❌ Không được, nhưng technincally:
const key = ReflectownKeys(f); // không hiện private fields
// Private fields không present trong Object.keys, Reflect.ownKeys
// Nhưng có thể dùng WeakMap workaround từ bên ngoài
```

### Bẫy 5: Static fields không share giữa subclass và parent

```js
class Parent {
  static count = 0;
  static increment() { Parent.count++; }
}
class Child extends Parent {}

Parent.increment();
console.log(Parent.count); // 1
console.log(Child.count);  // 0 — separate static namespace!
```

### Bẫy 6: ES2022 support — browser/Node cũ không chạy được

```js
// Private fields # require:
// - Chrome 74+
// - Firefox 90+
// - Safari 14.1+
// - Node.js 12+
// Kiểm tra trước dùng:
if (!Array.prototype.at) { /* polyfill */ }
```

## 💡 Khi nào dùng — Tình huống thực tế

1. **`static`**: bộ đếm, hằng số cấu hình, method tiện ích không cần state instance.
2. **`#private`**: bảo vệ dữ liệu nhạy cảm (mật, tiền, token nội bộ), chống sửa bậy.
3. **Getter/setter**: kiểm tra giá trị trước khi gán (age >= 0, price > 0...).
4. **Singleton pattern**: `static getInstance()`.
5. **Utility classes**: class chỉ có static methods (Math, StringUtils).
6. **Configuration management**: static config readonly.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Static method cơ bản

```js
class MathHelper {
  static add(a, b) { return a + b; }
  static multiply(a, b) { return a * b; }
  static PI = 3.14159265359;
}

console.log(MathHelper.add(2, 3));      // 5
console.log(MathHelper.PI);             // 3.14159265359
// console.log((new MathHelper()).add(2,3)); // ❌ TypeError
```

### Ví dụ 2: Static counter

```js
class Counter {
  static count = 0;
  
  static inc() {
    this.count++;
  }
  
  constructor() {
    Counter.inc();
  }
}

new Counter();
new Counter();
new Counter();
console.log(Counter.count); // 3
```

### Ví dụ 3: Private field với getter/setter

```js
class Counter {
  #value = 42;               // private field
  
  get value() { return this.#value; }
  set value(v) { 
    if (typeof v !== "number") throw new TypeError("Must be number");
    this.#value = v; 
  }
  
  #privateMethod() {
    return this.#value * 2;
  }
  
  double() {
    return this.#privateMethod();
  }
}

const c = new Counter();
console.log(c.value);   // 42
c.value = 100;
console.log(c.value);   // 100
console.log(c.double()); // 200
// console.log(c.#value);    // ❌ SyntaxError
// console.log(c.#privateMethod()); // ❌ SyntaxError
```

### Ví dụ 4: Full example — Static + Private combined

```js
class BankAccount {
  static #nextId = 1000;
  static #rate = 0.05; // 5% interest
  
  #id;
  #owner;
  #balance;
  
  constructor(owner, initialBalance = 0) {
    this.#id = BankAccount.#nextId++;
    this.#owner = owner;
    this.#balance = initialBalance;
  }
  
  get id() { return this.#id; }
  get owner() { return this.#owner; }
  get balance() { return this.#balance; }
  
  deposit(amount) {
    if (amount <= 0) throw new Error("Must be positive");
    this.#balance += amount;
  }
  
  withdraw(amount) {
    if (amount > this.#balance) throw new Error("Insufficient funds");
    this.#balance -= amount;
  }
  
  static getRate() {
    return BankAccount.#rate;
  }
  
  static getNextId() {
    return BankAccount.#nextId;
  }
}

const acc1 = new BankAccount("Alice", 1000);
const acc2 = new BankAccount("Bob", 500);
console.log(acc1.id);       // 1000
console.log(acc2.id);       // 1001
console.log(BankAccount.getRate()); // 0.05
// console.log(acc1.#balance); // ❌ SyntaxError
```

### Ví dụ 5: Singleton pattern

```js
class Singleton {
  static #instance = null;
  
  #secret = "classified";
  
  static getInstance() {
    if (!Singleton.#instance) {
      Singleton.#instance = new Singleton();
    }
    return Singleton.#instance;
  }
  
  getSecret() {
    return this.#secret;
  }
}

const s1 = Singleton.getInstance();
const s2 = Singleton.getInstance();
console.log(s1 === s2);     // true — cùng instance
console.log(s1.getSecret()); // "classified"
```

### Ví dụ 6: Private method pattern

```js
class EncryptionService {
  #key = "my-secret-key";
  
  #encrypt(text) {
    return text.split("").map(c => 
      String.fromCharCode(c.charCodeAt(0) + 1)
    ).join("");
  }
  
  #decrypt(text) {
    return text.split("").map(c => 
      String.fromCharCode(c.charCodeAt(0) - 1)
    ).join("");
  }
  
  encode(message) {
    return this.#encrypt(message);
  }
  
  decode(encoded) {
    return this.#decrypt(encoded);
  }
}

const svc = new EncryptionService();
const encoded = svc.encode("Hello");
const decoded = svc.decode(encoded);
console.log(decoded); // "Hello"
// svc.#encrypt("test"); // ❌ SyntaxError
```

### Ví dụ 7: Static vs Instance behavior

```js
class Robot {
  static totalBuilt = 0;
  
  constructor(model) {
    this.model = model;
    Robot.totalBuilt++;
  }
  
  static info() {
    return `Robots built: ${Robot.totalBuilt}`;
  }
  
  describe() {
    return `I am a ${this.model} robot`;
  }
}

const r1 = new Robot("Atlas");
const r2 = new Robot("Optimus");
console.log(Robot.info());       // "Robots built: 2"
console.log(r1.describe());      // "I am a Atlas robot"
console.log(r2.describe());      // "I am a Optimus robot"
// console.log(r1.info());       // ❌ TypeError: r1.info is not a function
```

## 🔬 So sánh với alternatives

| Feature | Static | Private (#) | Module closure | WeakMap |
|---------|--------|-------------|----------------|---------|
| Access from outside | Class name | ❌ SyntaxError | ❌ Không | ⚠️ Technically yes |
| Inheritance | Shared namespace | Not inherited | N/A | Not inherited |
| Browser support | All (static methods), ES2022 (fields) | ES2022+ | All | All |
| Enforced by engine | Yes | Yes | Yes (closure) | No (runtime only) |

## 📊 Performance & Best Practices

- **Static methods** — không có `this` binding overhead, gọi trực tiếp qua class name nhanh hơn instance method.
- **Private fields `#`** — engine tối ưu tốt, nhưng access slightly slower public fields (negligible).
- **Private methods** — tương đương private fields về performance.
- **Singleton với static + private** — pattern an toàn, tránh multiple instances.
- **Module pattern alternative** — nếu không cần OOP, dùng module closure cho encapsulation.
- **Check browser support** — private fields cần ES2022 (Chrome 74+, Node 12+).

## 🔗 Liên kết chéo

- **Xem thêm:** `14_classes/01_basics` — class basics
- **Xem thêm:** `14_classes/02_constructor` — constructor patterns
- **Xem thêm:** `14_classes/03_inheritance` — inheritance with static/private
- **Xem thêm:** `10_this-keyword/README` — this binding trong static vs instance
- **Xem thêm:** `09_functions/02_scope-closure-strict-mode/03_closure` — closure alternative to private
- **Xem thêm:** `11_function-borrowing/05_polyfill` — polyfill cho private fields (pre-ES2022)
