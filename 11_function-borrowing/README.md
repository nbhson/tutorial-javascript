# Function Borrowing (Mượn hàm) trong JavaScript — [Level: Intermediate]

## 🔑 Khái niệm cốt lõi

**Function borrowing** là kỹ thuật **dùng chung một hàm** của object/class này cho object khác mà không cần copy hay kế thừa: bạn mượn function và ép cho nó chạy với `this` = object mong muốn.

Cơ chế nền tảng là **3 phương thức explicit binding** có sẵn trên mọi hàm (vì hàm là object trong JS, mọi hàm đều thừa kế `Function.prototype`):

| Phương thức | Gọi ngay? | Cách truyền đối số | Trả về |
|-------------|-----------|-------------------|--------|
| `fn.call(thisArg, arg1, arg2, ...)` | ✅ Có | Từng đối số, ngăn cách bằng dấu phẩy | Kết quả của `fn` |
| `fn.apply(thisArg, [arg1, arg2, ...])` | ✅ Có | Mảng đối số (một phần tử) | Kết quả của `fn` |
| `fn.bind(thisArg, arg1, arg2, ...)` | ❌ Không | Từng đối số (tùy chọn) | **Hàm mới** đã khóa `this` |

Bản chất: cả ba đều làm đúng một việc — **quyết định `this` là ai**, rồi gọi hàm (hoặc chuẩn bị gọi sau). Khác nhau ở việc gọi ngay hay không và cách nhận đối số.

Arrow function là ngoại lệ: `call`/`apply`/`bind` **bị bỏ qua** vì arrow không có `this` riêng.

## 📐 Cấu trúc / Cú pháp

### Signature chi tiết

```js
// call: thisArg + danh sách đối số rời rạc
result = fn.call(thisArg, arg1, arg2, arg3)

// apply: thisArg + mảng đối số
result = fn.apply(thisArg, [arg1, arg2, arg3])

// bind: thisArg + optional đối số cố định → trả về hàm mới
const newFn = fn.bind(thisArg, arg1, arg2)
result = newFn(arg3, arg4)  // arg1, arg2 đã được chốt
```

### Bảng so sánh chi tiết

| Đặc tính | `call` | `apply` | `bind` |
|----------|--------|---------|--------|
| Gọi ngay | ✅ | ✅ | ❌ |
| Truyền đối số | Danh sách | Mảng | Danh sách (optional) |
| Trả về | Kết quả hàm | Kết quả hàm | Hàm mới |
| Dùng cho callback | ❌ | ❌ | ✅ |
| Dùng cho inheritance | ✅ | ✅ | ⚠️ Không khuyến khích |
| Dùng cho borrowing | ✅ | ✅ | ✅ |

## ✅ Điểm mạnh — Tại sao nên dùng

1. **Tái sử dụng code tối đa** — một hàm dùng cho vô số object, không cần viết lại.
2. **Kế thừa constructor dễ dàng** — `Parent.call(this, ...)` trong child constructor.
3. **Mượn method built-in** — `Array.prototype.forEach.call(arguments, ...)`, `Math.max.apply(null, arr)`.
4. **`bind` tạo hàm mới tiện cho callback** — khóa `this` và đối số, dùng sau.
5. **Partial application** — chốt trước một phần đối số, gọi sau với phần còn lại.
6. **Áp dụng được cho class lẫn object literal** — không cần đổi code nguồn.
7. **Event delegation pattern** — `bind` giữ context object trong listener.
8. **Polyfill pattern** — tự viết polyfill dựa trên nguyên lý borrowing.
9. **Mixin pattern** — gán method từ nhiều object khác nhau vào một object.
10. **Utility functions** — `Array.prototype.slice.call(nodeList)` chuyển NodeList thành array.

## ⚠️ Bẫy thường gặp & Hạn chế

### Bẫy 1: `bind` không gọi hàm ngay — quên `()`

```js
const bound = greet.bind(user);
bound;  // ❌ chỉ là hàm mới, chưa gọi
bound(); // ✅ phải gọi thêm
```

### Bẫy 2: `call` vs `apply` nhầm cách truyền đối số

```js
Math.max.call(null, [1, 2, 3]);    // NaN — array là 1 đối số duy nhất
Math.max.apply(null, [1, 2, 3]);   // 3 — ✅ spread array thành đối số
```

### Bẫy 3: Arrow function + `call`/`apply`/`bind` = vô dụng

```js
const arrow = () => console.log(this);
arrow.call({ x: 1 }); // không đổi được this
```

### Bẫy 4: `thisArg` là `null`/`undefined` trong strict mode

```js
"use strict";
function fn() { return this; }
fn.call(null);  // null (không tự động chuyển thành window)
```

### Bẫy 5: `bind` chỉ ràng buộc `this` lần đầu — không gỡ được

```js
const fn = greet.bind(user1);
fn.call(user2);  // vẫn là user1 — bind permanent
```

### Bẫy 6: Mượn method cho object không có cấu trúc tương thích

```js
const cat = { name: "Miao" };
dog.bark.call(cat); // cat.bark is not a function — cat không có bark method
```

### Bẫy 7: `arguments` object không phải array thật

```js
function showArgs() {
  Array.prototype.slice.call(arguments); // ✅ chuyển thành array
  arguments.map(x => x);                 // ❌ TypeError — arguments không có map
}
```

## 💡 Khi nào dùng — Tình huống thực tế

1. **Mượn `Array.prototype` method** cho `arguments`, `NodeList`, object giống mảng.
2. **Gọi hàm cha (super)** trong function-constructor khi chưa có `class`: `Animal.call(this, name)`.
3. **Khóa `this` cho callback/event handler** bằng `bind`.
4. **Tính toán với mảng động** — `Math.max.apply(null, numbers)`.
5. **Viết polyfill** — tự implement `forEach`, `includes`...
6. **Mixin pattern** — gộp method từ nhiều source vào một object.
7. **Factory function** — tạo object có sẵn method borrowed từ prototype.
8. **Event delegation** — một handler duy nhất, `bind` giữ context controller.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Cơ bản — call, apply, bind so sánh

```js
const teacher = {
  firstName: "Minh",
  lastName: "Thao",
  getFullName() {
    return `${this.firstName} ${this.lastName}`;
  },
};

const student = { firstName: "Dang", lastName: "Son" };

console.log(teacher.getFullName());                 // Minh Thao (own)
console.log(teacher.getFullName.call(student));     // Dang Son (mượn + call)
console.log(teacher.getFullName.apply(student));    // Dang Son (mượn + apply)
const bound = teacher.getFullName.bind(student);
console.log(bound());                               // Dang Son (hàm mới)
```

### Ví dụ 2: Inheritance qua call

```js
function Animal(name, weight) {
  this.name = name;
  this.weight = weight;
}

function Chicken(name, weight, legs) {
  Animal.call(this, name, weight); // kế thừa name, weight từ Animal
  this.legs = legs;
}

const son = new Chicken("Sơn", 53, 2);
console.log(son); // Chicken { name: "Sơn", weight: 53, legs: 2 }
```

### Ví dụ 3: Mượn array method cho arguments

```js
function sumAll() {
  const args = Array.prototype.slice.call(arguments); // arguments → array
  return args.reduce((a, b) => a + b, 0);
}
console.log(sumAll(1, 2, 3, 4)); // 10
```

### Ví dụ 4: Math.max với apply

```js
const numbers = [3, 7, 1, 9, 4];
console.log(Math.max.apply(null, numbers)); // 9
// Tương đương: numbers.reduce((a, b) => Math.max(a, b))
```

### Ví dụ 5: Partial application với bind

```js
function greet(greeting, name, suffix) {
  return `${greeting}, ${name}${suffix}`;
}

const hello Vietnamese = greet.bind(null, "Xin chào", "Minh");
console.log(helloVietnamese("!")); // "Xin chào, Minh!"
console.log(helloVietnamese("?")); // "Xin chào, Minh?"
```

### Ví dụ 6: Event handler với bind

```js
const app = {
  cars: ["BMW", "Audi"],
  handleDelete(e) {
    const index = e.target.dataset.index;
    this.cars.splice(index, 1);
    this.render();
  },
  render() {
    console.log("Cars:", this.cars.join(", "));
  },
  init() {
    // bind giữ this = app dù handler gọi bởi element
    document.getElementById("list").onclick = this.handleDelete.bind(this);
  }
};
app.init();
```

### Ví dụ 7: Polyfill pattern — self-implemented call

```js
Function.prototype.myCall = function (ctx, ...args) {
  ctx = ctx || globalThis;
  const key = Symbol("fn");
  ctx[key] = this;
  const result = ctx[key](...args);
  delete ctx[key];
  return result;
};

const obj = { name: "Polyfill" };
function say() { console.log(this.name); }
say.myCall(obj); // "Polyfill"
```

## 🔬 So sánh với alternatives

| Cách | Ưu điểm | Nhược điểm | Khi dùng |
|------|---------|------------|----------|
| `call` | Gọi ngay, rõ ràng | Chỉ nhận danh sách đối số | Kế thừa constructor, mượn hàm một lần |
| `apply` | Nhận mảng đối số | Dài hơn call với ít đối số | `Math.max.apply(null, arr)`, `arguments` |
| `bind` | Tạo hàm mới, dùng lại | Không gọi ngay | Callback, event handler, partial application |
| Arrow lexical this | Không cần bind | Không đổi được this | Callback giữ context |
| Object.assign methods | Copy method | Duplicate code | Mixin đơn giản |

## 📊 Performance & Best Practices

- **`call` vs `apply`**: performance gần như tương đương — chọn theo thói quen và số đối số.
- **`bind` tạo closure mới** — tránh bind trong loop (tạo nhiều function object).
- **Mượn built-in method** là pattern hiệu quả — `Array.prototype.slice.call` nhanh hơn loop.
- **Luôn dùng `globalThis`** thay vì `window` trong polyfill cho cross-platform.
- **Không bind arrow function** — vô nghĩa và gây hiểu nhầm.

## 🔗 Liên kết chéo

- **Xem thêm:** `11_function-borrowing/01_bind` — `bind()` chi tiết
- **Xem thêm:** `11_function-borrowing/02_bind-advanced` — partial application, event delegation
- **Xem thêm:** `11_function-borrowing/03_call` — `call()` chi tiết
- **Xem thêm:** `11_function-borrowing/04_apply` — `apply()` chi tiết
- **Xem thêm:** `11_function-borrowing/05_polyfill` — tự viết polyfill
- **Xem thêm:** `10_this-keyword/README` — 4 quy tắc this
- **Xem thêm:** `14_classes/02_constructor` — super() trong class kế thừa
