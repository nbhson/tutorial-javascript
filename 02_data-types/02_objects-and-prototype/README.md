# Objects và Prototype — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

Trong JavaScript, **object** là kiểu tham chiếu lưu dữ liệu dạng cặp **khóa – giá trị** (`property: value`), trong đó giá trị có thể là dữ liệu hoặc hàm (khi đó gọi là **method**). Gần như mọi thứ trong JS đều là object hoặc kế thừa từ object: array, function, Date, RegExp...

**Prototype** là nền tảng của object: mỗi object đều "mang theo" một prototype — một object khác để **học theo**. Khi truy cập một thuộc tính không có sẵn, JS lần qua **chuỗi prototype (prototype chain)** từ trong ra ngoài cho đến khi gặp `null`.

```
obj
 ├── own properties: name, age
 └── __proto__ → Person.prototype
      ├── own methods: greet(), introduce()
      └── __proto__ → Object.prototype
           ├── own methods: toString(), hasOwnProperty()
           └── __proto__ → null  ← DỪNG
```

### Đặc tính cốt lõi của object

1. **Động (dynamic)** — thêm, xóa, sửa property bất kỳ lúc nào mà không cần khai báo trước.
2. **Key là string hoặc Symbol** — mọi key đều được convert thành string (trừ Symbol).
3. **Prototype chain cho kế thừa** — method đặt trên prototype dùng chung cho mọi instance.
4. **Reference type** — `const obj1 = obj2` chỉ copy tham chiếu, không tạo bản sao.
5. **Hàm cũng là object** — function có property/method, `typeof fn === "function"`.

### 3 bài con trong nhóm

- `01_object-basics/` — tạo và thao tác object, constructor function, prototype.
- `02_functions-as-objects/` — vì sao "hàm cũng là object" và các loại hàm.
- `03_shallow-deep-clone/` — copy object đúng cách (shallow vs deep).

## 📐 Cấu trúc nhóm

```
02_data-types/02_objects-and-prototype/
├── README.md                  ← bài tổng quan này
├── 01_object-basics/
│   ├── README.md
│   ├── 1_object.js            ← object literal, thêm/xóa property
│   ├── 2_object_constructor.js ← constructor function, new
│   └── 3_object_prototype.js  ← prototype chain, inheritance
├── 02_functions-as-objects/
│   ├── README.md
│   ├── 1_app.js               ← function cơ bản, arguments
│   └── 2_Cac-loai-function.js ← declaration, expression, anonymous, method
└── 03_shallow-deep-clone/
    ├── README.md
    └── app.js                 ← {...obj}, Object.assign, structuredClone
```

## ✅ Điểm mạnh — Tại sao nên hiểu object & prototype

| # | Điểm mạnh | Lý do |
|---|-----------|-------|
| 1 | **Object là "đơn vị dữ liệu" linh hoạt** | Thêm/xóa/key thuộc tính bất cứ lúc nào — không cần schema cứng |
| 2 | **Prototype tái sử dụng phương thức** | Gắn method trên prototype dùng chung hàng nghìn instance, tiết kiệm bộ nhớ |
| 3 | **Constructor function nền tảng** | Hiểu để đọc code cũ và hiểu class ES6 thực chất là gì |
| 4 | **Clone đúng cách bảo vệ dữ liệu** | `structuredClone`, lodash — tránh bug "sửa copy làm đổi gốc" |
| 5 | **Hàm cũng là object** | Function có `name`, `length`, `arguments`, có thể thêm property |
| 6 | **Prototype chain cho inheritance** | Kế thừa không cần class — `Object.create(proto)` là đủ |
| 7 | **Nền tảng cho toàn bộ JS ecosystem** | Class, module, prototype — tất cả đều build trên object model |

## ⚠️ Bẫy thường gặp & Hạn chế

| # | Bẫy | Ví dụ | Cách tránh |
|---|-----|-------|-----------|
| 1 | **`person2 = person1` không phải clone** | Chỉ tăng tham chiếu — ai sửa ai cũng thấy | Dùng `{...obj}` hoặc `structuredClone()` |
| 2 | **Shallow copy không tách lớp lồng nhau** | `{...person1}` — `person1.networks` vẫn shared | Dùng `structuredClone()` cho deep copy |
| 3 | **`JSON.parse(JSON.stringify(obj))` mất giá trị** | `undefined`, `function`, `Date`, `NaN` bị biến đổi | Dùng `structuredClone()` thay thế |
| 4 | **Sửa `Object.prototype` ảnh hưởng mọi object** | `Object.prototype.evil = true` — mọi object đều có `evil` | NEVER modify built-in prototypes globally |
| 5 | **`typeof null === "object"`** | `typeof null` trả "object" — bug lịch sử | Dùng `value === null` kiểm tra |
| 6 | **`for...in` lặp qua prototype chain** | `for (const key in obj)` include prototype properties | Dùng `Object.keys()` hoặc `hasOwnProperty` check |
| 7 | **Constructor thiếu `new`** | `User("Sơn")` (không `new`) → `this` leak ra window | Luôn dùng `new` hoặc class ES6 |

## 💡 Khi nào dùng — Tình huống thực tế

1. **Lưu dữ liệu có cấu trúc** (user, product, cart) → object literal `{ name, price, quantity }`.
2. **Chia sẻ phương thức dùng chung** → gắn vào `prototype` thay vì lặp trong từng instance.
3. **Tạo nhiều đối tượng cùng "khuôn"** → constructor function hoặc class ES6.
4. **Cần bản sao độc lập để sửa không phá dữ liệu gốc** → deep clone `structuredClone(obj)`.
5. **Function là object** — dùng `fn.name`, `fn.length` khi debug, write higher-order functions.
6. **Prototype chain cho OOP** — hiểu cách `instanceof` hoạt động, debug `super` call.
7. **Dynamic key access** — `obj[dynamicKey]`, `obj[symbolKey]` — computed property.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Object literal cơ bản

```js
const user = {
  name: "Sơn",
  age: 23,
  getFullName() {
    return `${this.name} Nguyễn`;
  },
};

console.log(user.name);           // "Sơn" — dot notation
console.log(user["age"]);         // 23 — bracket notation
console.log(user.getFullName());  // "Sơn Nguyễn" — method

// Dynamic key access
const key = "name";
console.log(user[key]);           // "Sơn" — dùng biến làm key
```

### Ví dụ 2: Prototype — chia sẻ phương thức

```js
function Person(firstName) {
  this.firstName = firstName;
}

// Method trên prototype — dùng chung cho mọi instance
Person.prototype.who = function () {
  return `Tôi là ${this.firstName}`;
};

const p1 = new Person("Nam");
const p2 = new Person("Hoa");

console.log(p1.who());                // "Tôi là Nam"
console.log(p1.who === p2.who);       // true — cùng function object!

// Kiểm tra prototype chain
console.log(Object.getPrototypeOf(p1) === Person.prototype); // true
console.log(p1 instanceof Person);                            // true
```

### Ví dụ 3: Kế thừa qua prototype chain

```js
function Animal(name) {
  this.name = name;
}
Animal.prototype.speak = function () {
  return `${this.name} makes a sound`;
};

function Dog(name, breed) {
  Animal.call(this, name);  // call parent constructor
  this.breed = breed;
}

// Kế thừa: Dog.prototype inherit từ Animal.prototype
Dog.prototype = Object.create(Animal.prototype);
Dog.prototype.constructor = Dog;

// Thêm method riêng cho Dog
Dog.prototype.bark = function () {
  return `${this.name} barks: Woof!`;
};

const dog = new Dog("Buddy", "Labrador");
console.log(dog.speak());    // "Buddy makes a sound" — from Animal.prototype
console.log(dog.bark());     // "Buddy barks: Woof!" — from Dog.prototype
console.log(dog instanceof Animal); // true — prototype chain: dog → Dog.prototype → Animal.prototype
```

### Ví dụ 4: Deep clone — structuredClone

```js
const original = {
  name: "Sơn",
  address: { city: "SG", district: "Q1" },
  scores: [90, 85, 92],
  birthday: new Date("2000-01-01"),
};

// Shallow copy — nested object vẫn shared
const shallow = { ...original };
shallow.address.city = "HN";
console.log(original.address.city);   // "HN" — GỐC BỊ ĐỔI! ❌

// Deep copy — hoàn toàn độc lập
const deep = structuredClone(original);
deep.address.city = "DN";
console.log(original.address.city);   // "SG" — gốc không đổi ✓
console.log(deep.birthday instanceof Date); // true — Date được giữ nguyên ✓
```

## 🔬 So sánh với alternatives

| Phương án | Ưu điểm | Nhược điểm | Phù hợp khi |
|-----------|---------|------------|-------------|
| **Object literal `{}`** | Nhanh, đơn giản, readable | Prototype = Object.prototype, không reuse pattern | Data grouping, config |
| **`Object.create(proto)`** | Explicit prototype, lightweight | Verbose hơn class | Prototype-based inheritance |
| **Constructor function** | Shared prototype methods, `new` pattern | `new` dễ quên, `this` confusing | Legacy code, understanding ES6 class |
| **ES6 `class`** | Clean syntax, `extends`, `super` | Still prototype-based underneath | Modern OOP, team familiarity |
| **Factory function** | No `new` needed, flexible return | No `instanceof`, prototype chain flat | Functional programming, avoiding `this` |

## 📊 Performance & Best Practices

- **Đặt method trên prototype** thay vì trong constructor — mỗi instance chỉ trỏ đến một function object, tiết kiệm bộ nhớ.
- **Dùng `structuredClone()`** thay `JSON.parse/stringify` cho deep copy — giữ Date, Map, Set, NaN.
- **Tránh sửa built-in prototype** — `Object.prototype`, `Array.prototype` là global, modify ảnh hưởng toàn app.
- **Dùng `Object.keys()`** thay `for...in` — chỉ trả về own enumerable properties, không include prototype chain.
- **`Object.hasOwn(obj, key)`** (ES2022) thay `hasOwnProperty.call()` — cleaner syntax.
- **Class ES6 vẫn là prototype** — hiểu prototype giúp debug `this` binding, `super`, `instanceof`.

## 🔗 Liên kết chéo

- Xem thêm: `02_data-types/02_objects-and-prototype/01_object-basics/` — object literal, constructor, prototype
- Xem thêm: `02_data-types/02_objects-and-prototype/02_functions-as-objects/` — hàm là object, arguments
- Xem thêm: `02_data-types/02_objects-and-prototype/03_shallow-deep-clone/` — clone strategies
- Xem thêm: `14_classes/` — ES6 class syntax, extends, super
- Xem thêm: `10_this-keyword/` — `this` binding trong method và prototype
- Tài liệu: [MDN — Working with objects](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Working_with_Objects), [javascript.info/prototype](https://javascript.info/prototype)
