# Từ khóa `this` trong JavaScript — [Level: Intermediate]

## 🔑 Khái niệm cốt lõi

`this` là một trong những khái niệm **phức tạp và gây nhầm lẫn nhất** trong JavaScript. Khác với nhiều ngôn ngữ khác (Java, C#, Python), `this` trong JS **không phụ thuộc vào nơi hàm được khai báo**, mà phụ thuộc vào **cách hàm được gọi** (call-site). Điều này có nghĩa cùng một hàm, gọi theo 4 cách khác nhau sẽ cho 4 giá trị `this` khác nhau.

Cơ chế hoạt động bên trong JavaScript engine: mỗi khi hàm được gọi, engine tạo ra một **execution context** (bối cảnh thực thi). Trong bối cảnh đó, `this` được gán giá trị dựa trên 4 quy tắc binding theo thứ tự ưu tiên. Engine không "đọc" `this` từ scope chain (như biến thông thường) — nó là một cơ chế đặc biệt, được thiết kế để hỗ trợ lập trình hướng đối tượng kiểu duck-typing.

**Arrow function là ngoại lệ duy nhất**: arrow function **không tạo execution context mới** cho `this`, mà kế thừa `this` từ scope lexical (văn cảnh tĩnh) nơi nó được khai báo. Đây là lý do arrow function không bao giờ hoạt động đúng khi dùng làm method của object hay event handler.

## 📐 Cấu trúc / Cú pháp

### Bốn quy tắc `this` (từ ưu tiên thấp đến cao)

| # | Quy tắc | Điều kiện | `this` trỏ tới |
|---|---------|-----------|----------------|
| 1 | **Default binding** | Gọi hàm trần: `fn()`, `var x = fn; x()` | `window`/`globalThis` (non-strict) hoặc `undefined` (strict mode) |
| 2 | **Implicit binding** | Gọi qua object: `obj.method()` | Chính `obj` — object đứng trước dấu chấm cuối cùng |
| 3 | **Explicit binding** | Dùng `call`, `apply`, `bind` | Object bạn truyền vào làm `thisArg` |
| 4 | **`new` binding** | Gọi qua constructor: `new Fn()` | Object instance mới được tạo |

**Thứ tự ưu tiên:** `new` > `explicit` (`call`/`apply`/`bind`) > `implicit` > `default`.

### Bảng cú pháp chi tiết

| Cú pháp | Kiểu gọi | `this` là gì | Lưu ý |
|---------|----------|---------------|-------|
| `fn()` | Default | `window` hoặc `undefined` (strict) | Hàm trần, không gắn object |
| `obj.method()` | Implicit | `obj` | Chỉ object đứng ngay trước dấu chấm cuối cùng |
| `fn.call(obj, a, b)` | Explicit | `obj` | Gọi ngay, đối số truyền rời rạc |
| `fn.apply(obj, [a, b])` | Explicit | `obj` | Gọi ngay, đối số truyền mảng |
| `fn.bind(obj)` | Explicit | `obj` (hàm mới) | Trả về hàm mới, không gọi ngay |
| `new Fn()` | New | Object instance mới | Tự động gọi constructor |
| `() => {}` | Arrow | Kế thừa từ scope bao bọc | Không có `this` riêng, `call/apply/bind` vô dụng |

## ✅ Điểm mạnh — Tại sao nên dùng

1. **Tái sử dụng method cho nhiều object** — cùng một hàm có thể chạy với `this` khác nhau nhờ implicit/explicit binding.
2. **Viết code hướng object tự nhiên** — method truy cập dữ liệu của object chứa nó (`this.name`, `this.price`).
3. **Event handler trực quan** — `this` trong callback mặc định là element kích hoạt sự kiện, không cần `event.target`.
4. **Constructor pattern mạnh mẽ** — `new` + `this` tạo instance riêng biệt, mỗi instance có state riêng.
5. **Function borrowing linh hoạt** — mượn method của object này cho object khác bằng `call`/`apply`/`bind`.
6. **Arrow function ổn định context** — giữ `this` của scope ngoài trong callback bất đồng bộ, không bị mất context.
7. **Dễ hiểu prototype chaining** — `this` giúp truy cập methods trên prototype của instance.
8. **Tích hợp tốt với DOM** — event listener gán `this` = element, tiện cho thao tác DOM.
9. **Phân biệt rõ method vs function** — `obj.method()` khác `const f = obj.method; f()` về `this`.
10. **Foundation cho class** — class trong JS thực chất là syntactic sugar trên constructor + prototype, và `this` là cầu nối.

## ⚠️ Bẫy thường gặp & Hạn chế

### Bẫy 1: Mất context khi tách method khỏi object

```js
const obj = {
  name: "A",
  hi() { console.log(this.name); }
};
obj.hi();           // "A" — this = obj (implicit)
const detached = obj.hi;
detached();         // undefined — this = window/undefined (default binding)
```

### Bẫy 2: Arrow function không có `this` riêng

```js
const obj = {
  name: "B",
  hello: () => console.log(this.name)  // undefined — arrow kế thừa global this
};
obj.hello();
```

### Bẫy 3: `new` binding ép `this` thành instance mới

```js
function Car(color) { this.color = color; }
const c = Car("red");  // ❌ gán vào window/globalThis
const d = new Car("blue");  // ✅ d.color = "blue"
```

### Bẫy 4: Arrow function không bind được bằng `call`/`apply`/`bind`

```js
const arrow = () => console.log(this);
arrow.call({ x: 1 });  // vẫn in window/globalThis — không đổi được!
```

### Bẫy 5: Event handler là function thường, `this` = element; arrow thì sai

```js
btn.addEventListener("click", () => {
  console.log(this);  // global/undefined, KHÔNG phải btn
});
btn.addEventListener("click", function () {
  console.log(this);  // btn — đúng!
});
```

### Bẫy 6: Strict mode khiến default binding trả về `undefined`

```js
"use strict";
function whoAmI() { return this; }
whoAmI();  // undefined — không phải window nữa
```

### Bẫy 7: Nested object — `this` là object trực tiếp chứa method

```js
const outer = {
  name: "outer",
  inner: {
    name: "inner",
    getName() { return this.name; }
  }
};
outer.inner.getName();  // "inner" — không phải "outer"
```

### Bẫy 8: Callback truyền vào array method mất `this`

```js
const arr = [1, 2, 3];
const obj = { prefix: "[", logAll() { arr.forEach(function(n) { console.log(this.prefix + n); }); } };
obj.logAll();  // undefined1, undefined2... — forEach callback là default binding
```

## 💡 Khi nào dùng — Tình huống thực tế

1. **DOM event handler** — dùng function thường trong `addEventListener` để `this` trỏ element, tránh phải viết `event.target` mọi nơi.
2. **Object method truy cập dữ liệu riêng** — `this.name`, `this.items` trong method của object literal hoặc class instance.
3. **Constructor pattern** — `new Person(name)` dùng `this.name = name` để gán property cho instance mới.
4. **Function borrowing** — mượn `Array.prototype.push.call(arguments, ...)` để biến `arguments` (object-like array) thành array thật.
5. **Callback bất đồng bộ giữ context** — dùng arrow function trong `setTimeout`, `Promise.then`, `fetch().then()` để `this` không bị mất.
6. **Event delegation** — gán một listener trên container, dùng `this` (element) hoặc `e.target` (phần tử con) để xử lý.
7. **Partial application với `bind`** — tạo hàm chuyên biệt từ hàm tổng quát: `const greet = say.bind(person, "Hello")`.
8. **Polyfill built-in methods** — tự viết `myCall`/`myBind` để hiểu rõ cơ chế này.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Default binding (hàm trần)

```js
// Non-strict: this = window/globalThis
function showContext() {
  console.log("this === window:", this === window); // true trong browser
}
showContext(); // default binding

// Strict mode: this = undefined
"use strict";
function showStrict() {
  console.log(this); // undefined
}
showStrict();
```

### Ví dụ 2: Implicit binding (method call)

```js
const car = {
  brand: "Tesla",
  drive() {
    return `Driving a ${this.brand}`;  // this = car
  },
  nested: {
    brand: "BMW",
    drive() {
      return this.brand;  // this = nested, NOT car
    }
  }
};
car.drive();           // "Driving a Tesla"
car.nested.drive();    // "BMW" — this là object trước dấu chấm cuối
```

### Ví dụ 3: Explicit binding — call và apply

```js
const student = { name: "Minh" };
const teacher = { name: "Thảo" };

function introduce() {
  return `Tôi tên là ${this.name}`;
}

introduce.call(student); // "Tôi tên là Minh"   — call ép this = student
introduce.apply(teacher); // "Tôi tên là Thảo"   — apply ép this = teacher
```

### Ví dụ 4: Explicit binding — bind (tạo hàm mới)

```js
const user = { name: "Lan" };

function greet(greeting) {
  return `${greeting}, ${this.name}!`;
}

const boundGreet = greet.bind(user); // không gọi ngay, trả về hàm mới
boundGreet("Xin chào"); // "Xin chào, Lan!"
// bind không thể bị ép lại bằng call sau đó
boundGreet.call({ name: "Hoa" }, "Hi"); // vẫn là "Xin chào, Lan!" — đã bind rồi
```

### Ví dụ 5: New binding (constructor)

```js
function Book(title, pages) {
  this.title = title;      // this = object mới
  this.pages = pages;
}
const novel = new Book("Đắc Nhân Tâm", 300);
console.log(novel.title); // "Đắc Nhân Tâm"

// Tương đương với function expression + prototype
function Dog(name) {
  this.name = name;
}
Dog.prototype.bark = function () { return `${this.name} says: Gâu!`; };
const rex = new Dog("Rex");
console.log(rex.bark()); // "Rex says: Gâu!"
```

### Ví dụ 6: Arrow function kế thừa lexical this

```js
const counter = {
  count: 0,
  increment() {
    // arrow kế thừa this từ increment() — tức counter
    setTimeout(() => {
      this.count++;               // this vẫn là counter, không phải window
      console.log("count:", this.count);
    }, 100);
  }
};
counter.increment(); // sau 100ms in "count: 1"

// Hàm thường sẽ sai:
const counter2 = { count: 0, increment() { setTimeout(function() { this.count++; }, 100); } };
counter2.increment(); // lỗi — this.count là undefined
```

### Ví dụ 7: this trong event handler

```js
// Ví dụ mô phỏng (thực tế dùng addEventListener)
function simulateAddEventListener(element, handler) {
  handler.call(element);  // engine ép this = element
}

const button = { id: "btn1" };
function handleClick() {
  console.log("Clicked:", this.id);  // "Clicked: btn1"
}
simulateAddEventListener(button, handleClick);
```

### Ví dụ 8: Priority test — tất cả 4 quy tắc cùng lúc

```js
function who() { console.log(this); }

who();                          // 1. Default → window/undefined
who.call({ x: 1 });             // 2. Explicit → {x: 1}
({ y: 2, who }).who();          // 3. Implicit → {y: 2}
new who();                      // 4. New → {} (instance mới)
```

## 🔬 So sánh với alternatives

| Cách tiếp cận | Ưu điểm | Nhược điểm | Khi nào dùng |
|---------------|---------|------------|--------------|
| `this` (function method) | Tự động binding theo call-site | Dễ mất context nếu tách method | Object methods, event handlers |
| Arrow function lexical `this` | Dự đoán được, không bị mất context | Không thể dùng làm method | Callbacks, promises, setTimeout |
| `const that = this` / `self = this` | Hoạt động với mọi version JS | Code dài dòng, dễ quên gán | Legacy code, pre-ES6 |
| `.bind(this)` | Tạo hàm mới, ép `this` vĩnh viễn | Tạo thêm object function | Truyền method làm callback |
| `call`/`apply` trực tiếp | Ép `this` một lần, gọi ngay | Không tái sử dụng được | Polyfill, utility functions |
| Class (ES6 syntax sugar) | Gọn gàng, dễ đọc, `this` rõ ràng | Vẫn dùng underlying prototype | OOP modern JS |

## 📊 Performance & Best Practices

**Quy tắc coding:**

- Luôn dùng **strict mode** (`"use strict"`) để default binding trả về `undefined` thay vì `window` — dễ bắt lỗi hơn.
- Ưu tiên **arrow function** trong callback bất đồng bộ (`setTimeout`, `Promise.then`, `forEach`) để giữ context.
- Tránh **tách method khỏi object** rồi gọi riêng — nếu cần, dùng `bind` ngay khi gán: `const fn = obj.method.bind(obj)`.
- Event handler dùng **function thường** nếu muốn `this` = element; dùng arrow nếu muốn `this` = outer scope.
- Trong class, **bind constructor method** hoặc dùng arrow field: `method = () => { ... }`.

**Performance:**

- Method trên `prototype` (class) được dùng chung — chỉ tốn 1 bản sao, không tạo lại mỗi instance.
- `bind` tạo một closure function mới — overhead nhỏ nhưng nên tránh bind trong loop.
- Arrow function có overhead tối thiểu — engine tối ưu tốt.

## 🔗 Liên kết chéo

- **Xem thêm:** `11_function-borrowing/01_bind` — `bind()` chi tiết
- **Xem thêm:** `11_function-borrowing/03_call` — `call()` chi tiết
- **Xem thêm:** `11_function-borrowing/04_apply` — `apply()` chi tiết
- **Xem thêm:** `10_this-keyword/05_arrow-function` — arrow function không có `this` riêng
- **Xem thêm:** `10_this-keyword/06_arrow-lexical` — lexical binding sâu hơn
- **Xem thêm:** `14_classes/01_basics` — class là syntactic sugar trên prototype
- **Xem thêm:** `12_asynchronous-javascript/01_event-loop` — tại sao callback cần arrow `this`
