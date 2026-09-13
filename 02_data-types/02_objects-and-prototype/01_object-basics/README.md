# Object Basics (Cơ bản về Object) — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

**Object** là một "hộp" chứa các cặp **khóa (key) – giá trị (value)**, gọi chung là **property**; nếu giá trị là hàm thì gọi là **method**. Object là nền tảng của JavaScript — học object là học "đơn vị dữ liệu cơ bản" của ngôn ngữ.

Trong JavaScript engine (V8), object được lưu trên **heap memory** dưới dạng **hidden class (map)** kết hợp với **property storage**:
- **In-object properties** — stored directly on the object for fast access.
- **Dictionary mode** — V8 chuyển sang hash table khi object có cấu trúc thay đổi liên tục (thêm/xóa property động).
- **Prototype chain** — mỗi object có internal slot `[[Prototype]]` (truy cập qua `Object.getPrototypeOf()`).

### Tạo object literal và truy cập thuộc tính

```js
var myInfo = {
  name: "Sơn",
  age: 23,
  sex: 1,
  getFullName: function () {
    return `${this.name} Nguyễn`; // method — dùng this để trỏ chính object
  },
};

console.log(myInfo.name);      // "Sơn" — dot notation
console.log(myInfo["name"]);   // "Sơn" — bracket notation
```

**Bracket notation đặc biệt hữu ích** khi key được lưu trong biến hoặc là dynamic key:

```js
var myKey = "email";
console.log(myInfo[myKey]);    // giá trị của thuộc tính "email"
myInfo[myKey] = "nbhson43@gmail.com"; // set dynamic key
```

### Thêm / xóa thuộc tính bất cứ lúc nào (tính động của object)

```js
myInfo.email = "nbhson43@gmail.com";  // Thêm mới
delete myInfo.sex;                     // Xóa
console.log(myInfo);
// { name: 'Sơn', age: 23, getFullName: [Function], email: 'nbhson43@gmail.com' }
```

### Object constructor (hàm tạo)

Dùng từ khóa `new` để tạo nhiều instance cùng "khuôn". Constructor function tạo:
1. **Object mới** — `this` trỏ đến object vừa tạo.
2. **Prototype link** — `new.target.prototype` được set làm prototype của object mới.

```js
function User(firstName, lastName, avatar) {
  this.firstName = firstName;   // this trỏ đến object vừa tạo
  this.lastName = lastName;
  this.avatar = avatar;
  // Method trong constructor — MỖI instance có bản sao riêng
  this.getFullName = function () {
    return `${this.firstName} ${this.lastName}`;
  };
}

var teacher = new User("Sơn", "Đặng", "avatar_1");
var student = new User("Sơn", "Nguyễn", "avatar_1");

teacher.luong = "10.000.000đ";   // property của riêng teacher
student.title = "Học sinh giỏi"; // property của riêng student
console.log(teacher.getFullName()); // Sơn Đặng
console.log(student.getFullName()); // Sơn Nguyễn
```

### Prototype — dùng chung phương thức cho mọi instance

Thay vì mỗi instance có một bản sao riêng của method (tốn bộ nhớ), đặt method trên `prototype`:

```js
function Person(name) {
  this.name = name;
}

// ĐẶT METHOD LÊN PROTOTYPE — dùng chung cho mọi instance
Person.prototype.greet = function () {
  return `Hello, I'm ${this.name}`;
};

const p1 = new Person("Sơn");
const p2 = new Person("Nam");

console.log(p1.greet());         // "Hello, I'm Sơn"
console.log(p1.greet === p2.greet); // true — CÙNG một function object!
```

### Kế thừa qua prototype chain

```js
function Person(name) {
  this.name = name;
}
Person.prototype.greet = function () {
  return `Hello, I'm ${this.name}`;
};

function Superman(name, power) {
  Person.call(this, name);  // kế thừa constructor
  this.power = power;
}

// Prototype chain: Superman.prototype → Person.prototype → Object.prototype
Superman.prototype = Object.create(Person.prototype);
Superman.prototype.constructor = Superman;

Superman.prototype.fly = function () {
  return `${this.name} uses ${this.power} to fly!`;
};

const clark = new Superman("Clark", "strength");
console.log(clark.greet());  // "Hello, I'm Clark" — from Person.prototype
console.log(clark.fly());    // "Clark uses strength to fly!" — from Superman.prototype
```

## 📐 Cấu trúc nhóm

```
02_data-types/02_objects-and-prototype/01_object-basics/
├── README.md                ← bài này
├── 1_object.js              ← object literal, thêm/xóa property, method
├── 2_object_constructor.js  ← constructor function, new pattern
└── 3_object_prototype.js    ← prototype, prototype chain, inheritance
```

## ✅ Điểm mạnh — Tại sao nên dùng object

| # | Điểm mạnh | Lý do |
|---|-----------|-------|
| 1 | **Linh hoạt** | Thêm/sửa/xóa property bất cứ lúc nào — không cần schema |
| 2 | **Constructor function tái sử dụng "khuôn"** | Tạo nhiều object cùng shape, consistent initialization |
| 3 | **Prototype tiết kiệm bộ nhớ** | Method dùng chung cho mọi instance, không duplicate |
| 4 | **Dot và bracket notation** | Dot cho static key, bracket cho dynamic key |
| 5 | **`delete`, `Object.assign`, spread** | Thao tác object nhanh gọn — CRUD operations |
| 6 | **Computed property keys** | `[symbolKey]: value`, `[dynamicKey]: value` |
| 7 | **Property shorthand** | ES6: `{ name, age }` thay `{ name: name, age: age }` |

## ⚠️ Bẫy thường gặp & Hạn chế

| # | Bẫy | Ví dụ | Cách tránh |
|---|-----|-------|-----------|
| 1 | **`delete` không xóa prototype property** | `delete obj.greet` → false nếu `greet` nằm trên prototype | Kiểm tra `obj.hasOwnProperty('greet')` trước |
| 2 | **`this` mất binding khi truyền method** | `const fn = obj.greet; fn()` → `this` là global | Dùng `fn.bind(obj)` hoặc arrow function |
| 3 | **Constructor thiếu `new`** | `User("Sơn")` (không `new`) → `this` leak ra window/global | Luôn dùng `new` hoặc class ES6 |
| 4 | **Key không hợp lệ phải bracket** | `obj.1stName` → SyntaxError; phải dùng `obj['1stName']` | Dùng camelCase cho key, bracket cho special |
| 5 | **Prototype property lookup chậm hơn own** | Mỗi lần truy cập → walk prototype chain | Cache frequent accessed values locally |
| 6 | **`for...in` include prototype properties** | `for (key in obj)` — lặp cả inherited enumerable props | Dùng `Object.keys()` hoặc check `hasOwnProperty` |
| 7 | **Object key được coerce về string** | `{ [1]: "a", [true]: "b" }` → `{ "1": "a", "true": "b" }` | Nhớ key luôn là string (trừ Symbol) |

## 💡 Khi nào dùng — Tình huống thực tế

1. **Nhóm dữ liệu logic với nhau** — thông tin người dùng, sản phẩm, cấu hình → object literal.
2. **Tạo nhiều đối tượng cùng cấu trúc** → constructor function (hoặc class ES6 cho syntax sạch).
3. **Chia sẻ hành vi cho tất cả instance** → `Prototype.method`.
4. **Dynamic key access** — `obj[userInput]` để lookup configuration, lookup table.
5. **API response** — server trả JSON → parse thành object, truy cập `data.user.name`.
6. **State management** — object giữ state của app, spread copy cho immutable update.
7. **Configuration object** — `const config = { host, port, timeout }` — grouped settings.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Object literal cơ bản + dot/bracket notation

```js
var myInfo = {
  name: "Sơn",
  age: 23,
  getFullName: function () {
    return `${this.name} Nguyễn`;
  },
};

// Dot notation — truy cập trực tiếp
console.log(myInfo.name);           // "Sơn"

// Bracket notation — key là string literal hoặc variable
console.log(myInfo["name"]);        // "Sơn"
console.log(myInfo["getFullName"]()); // "Sơn Nguyễn"

// Dynamic key
var key = "age";
console.log(myInfo[key]);           // 23

// Add new property
myInfo.email = "nbhson43@gmail.com";
console.log(myInfo.email);          // "nbhson43@gmail.com"

// Delete property
delete myInfo.age;
console.log(myInfo);                // { name: 'Sơn', getFullName: [Function], email: '...' }
```

### Ví dụ 2: Constructor function + prototype method

```js
function Product(name, price, category) {
  this.name = name;
  this.price = price;
  this.category = category;
}

// Method trên prototype — dùng chung cho mọi instance
Product.prototype.getFormattedPrice = function () {
  return `${this.name}: ${this.price.toLocaleString("vi-VN")}đ`;
};

Product.prototype.applyDiscount = function (percent) {
  return this.price * (1 - percent / 100);
};

const laptop = new Product("MacBook Pro", 45000000, "Electronics");
const phone = new Product("iPhone 15", 25000000, "Electronics");

console.log(laptop.getFormattedPrice()); // "MacBook Pro: 45.000.000đ"
console.log(laptop.applyDiscount(10));    // 40500000
console.log(laptop.getFormattedPrice === phone.getFormattedPrice); // true — same function!
```

### Ví dụ 3: Object.create — prototype kế thừa trực tiếp

```js
// Animal prototype
const animalProto = {
  init(name, sound) {
    this.name = name;
    this.sound = sound;
    return this; // return cho chaining
  },
  speak() {
    return `${this.name} says ${this.sound}`;
  },
};

// Create objects với prototype = animalProto
const dog = Object.create(animalProto).init("Buddy", "Woof");
const cat = Object.create(animalProto).init("Whiskers", "Meow");

console.log(dog.speak());  // "Buddy says Woof"
console.log(cat.speak());  // "Whiskers says Meow"
console.log(dog.speak === cat.speak); // true — shared via prototype!
console.log(Object.getPrototypeOf(dog) === animalProto); // true
```

### Ví dụ 4: Property descriptors

```js
const user = {};

// Define property with descriptor
Object.defineProperty(user, 'id', {
  value: 'USER001',
  enumerable: false,     // not shown in Object.keys()
  writable: false,       // cannot be changed
  configurable: false,   // cannot be deleted or reconfigured
});

user.id = 'CHANGED';      // silently fails (or TypeError in strict mode)
console.log(user.id);     // "USER001" — not changed!
console.log(Object.keys(user)); // [] — id not enumerable

// Regular property (writable, enumerable, configurable = true by default)
user.name = "Sơn";
console.log(Object.keys(user)); // ["name"]

// Get descriptor
console.log(Object.getOwnPropertyDescriptor(user, 'id'));
// { value: 'USER001', writable: false, enumerable: false, configurable: false }
```

### Ví dụ 5: Object.keys/values/entries

```js
const car = {
  brand: "Toyota",
  model: "Camry",
  year: 2024,
  color: "White",
};

// Object.keys — mảng các key (own enumerable)
console.log(Object.keys(car));
// ["brand", "model", "year", "color"]

// Object.values — mảng các giá trị
console.log(Object.values(car));
// ["Toyota", "Camry", 2024, "White"]

// Object.entries — mảng các [key, value] pairs
console.log(Object.entries(car));
// [["brand","Toyota"], ["model","Camry"], ["year",2024], ["color","White"]]

// Ứng dụng: Object.fromEntries (ES2019) — reverse entries
const entries = Object.entries(car);
const carCopy = Object.fromEntries(entries);

// Transform values: capitalize string values
const transformed = Object.fromEntries(
  Object.entries(car).map(([k, v]) => [k, String(v).toUpperCase()])
);
console.log(transformed.brand); // "TOYOTA"
```

## 🔬 So sánh với alternatives

| Phương án | Ưu điểm | Nhược điểm | Phù hợp khi |
|-----------|---------|------------|-------------|
| **Object literal `{}`** | Nhanh, đơn giản, readable | Không có shared methods tự động | Data, config, API responses |
| **Constructor function** | Shared prototype methods, `instanceof` | `new` dễ quên, `this` confusing | Legacy OOP, class understanding |
| **ES6 `class`** | Clean syntax, `extends`, `super`, `static` | Syntactic sugar over prototype | Modern OOP, team familiarity |
| **`Object.create(proto)`** | Explicit prototype, no constructor needed | Less familiar to OOP devs | Factory functions, mixin pattern |
| **Map/Set** | Any key type, ordered, `size` | Not JSON serializable, different API | Key-value pairs with complex keys |

## 📊 Performance & Best Practices

- **Đặt method trên prototype** thay vì trong constructor — tiết kiệm bộ nhớ cho hàng nghìn instances.
- **Dùng `const`** cho object references — prevents reassignment but allows mutation.
- **`Object.freeze()`** cho constants — shallow immutable, prevent accidental mutation.
- **`for...in` + `hasOwnProperty`** filter prototype properties — hoặc dùng `Object.keys()`.
- **Dùng spread `{...obj}`** thay `Object.assign({}, obj)` — cleaner syntax, same behavior.
- **Tránh `delete`** trên hot-path objects — gây dictionary mode in V8, slower property access.
- **Dùng `Object.hasOwn(obj, key)`** (ES2022) thay `hasOwnProperty.call(obj, key)` — cleaner syntax.
- **Prototype chain có thể làm chậm lookup** — deep chain = more lookups; keep chain shallow.

## 🔗 Liên kết chéo

- Xem thêm: `02_data-types/02_objects-and-prototype/` — overview objects & prototype
- Xem thêm: `02_data-types/02_objects-and-prototype/02_functions-as-objects/` — hàm là object
- Xem thêm: `02_data-types/02_objects-and-prototype/03_shallow-deep-clone/` — clone strategies
- Xem thêm: `00_introduction/01_what-is-javascript/02_prototype-based-programming/` — prototype deep dive
- Xem thêm: `14_classes/` — ES6 class, constructor, extends
- Tài liệu: [MDN — Objects](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Working_with_Objects), [javascript.info/object](https://javascript.info/object)
