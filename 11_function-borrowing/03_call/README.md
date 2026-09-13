# Phương thức `call()` — [Level: Intermediate]

## 🔑 Khái niệm cốt lõi

`fn.call(thisArg, arg1, arg2, ...)` **gọi ngay lập tức** hàm `fn` với `this` được gán bằng `thisArg`, các đối số truyền theo kiểu **danh sách** (list). Nếu không truyền `thisArg`, `this` mặc định là object global (`window` trong browser, `globalThis` trong Node).

Khác biệt quan trọng nhất so với `bind`: `call` **không tạo hàm mới** — nó gọi luôn và trả về kết quả của hàm. `bind` chỉ khóa `this` để dùng sau; `call` làm xong luôn một lần.

Ba ứng dụng lớn của `call`:
1. **Bind `this` khi gọi** — `obj2.method.call(obj1)` mượn method của obj2 cho obj1.
2. **Kế thừa trong constructor** — `Parent.call(this, ...)` để child nhận property của parent.
3. **Mượn method built-in** — `Array.prototype.forEach.call(arguments, fn)` xử lý object giống mảng.

## 📐 Cấu trúc / Cú pháp

### Signature

```js
result = fn.call(thisArg, arg1, arg2, arg3, ...)
```

### Bảng so sánh call vs apply

| Đặc tính | `call` | `apply` |
|----------|--------|---------|
| Truyền đối số | Danh sách rời rạc: `fn.call(ctx, a, b)` | Mảng: `fn.apply(ctx, [a, b])` |
| Gọi ngay | ✅ | ✅ |
| Trả về | Kết quả của fn | Kết quả của fn |
| Phù hợp khi | Đối số cố định, biết trước | Đối số động, trong mảng/arguments |
| Đọc hiểu | Dễ hơn với ít đối số | Dễ hơn với mảng đã có sẵn |

### Bảng `thisArg` behavior

| `thisArg` truyền vào | Non-strict mode | Strict mode |
|---------------------|-----------------|-------------|
| Object cụ thể | Object đó | Object đó |
| `null` / `undefined` | `window` / `globalThis` | `null` / `undefined` |
| Primitive (string, number) | Boxed object | Primitive (nhưng method thường expect object) |

## ✅ Điểm mạnh — Tại sao nên dùng

1. **Gọi hàm và ép `this` trong một cú pháp duy nhất** — trả về ngay kết quả, không cần biến trung gian.
2. **Kế thừa property+method** từ constructor khác không cần prototype phức tạp.
3. **Mượn method của Array/Math** cho mọi object "giống mảng" (arguments, NodeList, string).
4. **Hoạt động tốt trong strict mode** khi `this` được truyền tường minh — không phụ thuộc environment.
5. **One-liner borrowing** — `[].push.call(arr1, ...arr2)` gộp array nhanh.
6. **Super pattern pre-ES6** — gọi constructor cha trước ES6 class.
7. **Test mocking** — ép `this` thành mock object để test method độc lập.
8. **Function composition** — gọi function với context khác nhau trong pipeline.

## ⚠️ Bẫy thường gặp & Hạn chế

### Bẫy 1: Quên `call` — method chạy với wrong `this`

```js
const dog = { speak() { return `${this.name} speaks`; } };
const cat = { name: "Cat" };
dog.speak();      // "undefined speaks" (this = dog, dog.name undefined)
dog.speak.call(cat); // "Cat speaks" ✅
```

### Bẫy 2: Không truyền `thisArg` trong strict mode

```js
"use strict";
function fn() { return this; }
fn.call(); // undefined — không tự động thành window
```

### Bẫy 3: `call` gọi ngay — không dùng được cho callback

```js
// ❌ sai — call gọi ngay, không trả về hàm
setTimeout(obj.method.call(obj), 1000);
// ✅ đúng — bind tạo hàm mới
setTimeout(obj.method.bind(obj), 1000);
```

### Bẫy 4: Kế thừa qua `call` chỉ copy property, không nối prototype

```js
function Parent() { this.x = 1; }
Parent.prototype.add = function() { return this.x + 1; };

function Child() { Parent.call(this); }
// Child.prototype không kế thừa Parent.prototype!
// Cần thêm: Child.prototype = Object.create(Parent.prototype);
```

### Bẫy 5: Mượn method cho object không có cấu trúc phù hợp

```js
const empty = {};
Array.prototype.push.call(empty, 1, 2, 3);
console.log(empty.length); // 3
console.log(empty[0]);     // 1 — hoạt động vì empty có property numeric
```

## 💡 Khi nào dùng — Tình huống thực tế

1. **Gọi constructor cha** ngay trong constructor con: `Animal.call(this, name, weight)`.
2. **Mượn array method** cho `arguments`/`NodeList`: `[].forEach.call(...)`, `[].slice.call(...)`.
3. **Ép `this` tức thời** khi muốn chạy hàm với object khác ngay lập tức.
4. **Mix-in pattern** — gán method của class này vào instance class khác.
5. **Test unit** — mock `this` để test method không phụ thuộc state.
6. **Function pipeline** — gọi cùng function với different contexts.
7. **Data transformation** —借用 array method cho custom collections.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Basic call — mượn method

```js
const teacher = {
  firstName: "Thu",
  lastName: "Minh",
  introduce() {
    return `Tôi tên là ${this.firstName} ${this.lastName}`;
  }
};

const student = { firstName: "Nam", lastName: "Anh" };

console.log(teacher.introduce());           // "Tôi tên là Thu Minh"
console.log(teacher.introduce.call(student)); // "Tôi tên là Nam Anh"
```

### Ví dụ 2: Inheritance qua call

```js
function Animal(name, weight) {
  this.name = name;
  this.weight = weight;
}

function Chicken(name, weight, legs) {
  Animal.call(this, name, weight); // kế thừa name, weight
  this.legs = legs;
}

const son = new Chicken("Sơn", 53, 2);
console.log(son); // Chicken { name: "Sơn", weight: 53, legs: 2 }
```

### Ví dụ 3: Mượn Array method cho arguments

```js
function showAll() {
  // arguments là array-like, không có push
  const arr = [];
  Array.prototype.push.call(arr, ...arguments); // spread arguments vào push
  return arr;
}
console.log(showAll(1, 2, 3)); // [1, 2, 3]
```

### Ví dụ 4: Mượn Array method cho string

```js
const str = "hello";
// String có length và numeric index → array-like
const chars = Array.prototype.slice.call(str);
console.log(chars); // ["h", "e", "l", "l", "o"]

const reversed = Array.prototype.reverse.call(chars);
console.log(reversed.join("")); // "olleh"
```

### Ví dụ 5: Mượn Math method cho array

```js
const numbers = [3, 7, 1, 9, 4];
// Math.max không nhận array — phải spread hoặc dùng apply
console.log(Math.max.call(null, ...numbers)); // 9 ✅ (spread)
console.log(Math.max.apply(null, numbers));   // 9 ✅ (apply)
```

### Ví dụ 6: Mixin pattern

```js
const flyable = {
  fly() { return `${this.name} is flying!`; }
};

function Bird(name) {
  this.name = name;
}
// Mixin: gán method của flyable vào Bird.prototype
Object.assign(Bird.prototype, flyable);

const sparrow = new Bird("Sparrow");
console.log(sparrow.fly()); // "Sparrow is flying!"
```

### Ví dụ 7: Call với primitive thisArg

```js
function greet() {
  return `Hello, ${this.toUpperCase()}!`;
}
// Primitive được auto-box thành object
console.log(greet.call("world")); // "Hello, WORLD!"
console.log(greet.call(42));      // "Hello, 42!" (42 → Number {42})
```

## 🔬 So sánh với alternatives

| Cách | Gọi ngay? | Truyền đối số | Trả về | Khi nào dùng |
|------|-----------|---------------|--------|--------------|
| `call` | ✅ | Danh sách | Kết quả fn | Kế thừa, mượn hàm một lần |
| `apply` | ✅ | Mảng | Kết quả fn | Đối số trong mảng/arguments |
| `bind` | ❌ | Danh sách | Hàm mới | Callback, partial application |
| Direct call | ✅ | — | Kết quả fn | Không cần ép this |

## 📊 Performance & Best Practices

- **`call` vs `apply`**: performance tương đương — chọn theo readability và cách dữ liệu đến.
- **Spread `...args`** hiện đại thay `apply` khi engine hỗ trợ ES2015+.
- **Không gọi `call` trong loop** — tạo overhead nhỏ, pre-compute nếu có thể.
- **Luôn truyền `thisArg` tường minh** — đặc biệt trong strict mode.
- **Kết hợp `Object.assign`** với mixin pattern cho multiple method borrowing.

## 🔗 Liên kết chéo

- **Xem thêm:** `11_function-borrowing/04_apply` — apply khác call ở dạng đối số
- **Xem thêm:** `11_function-borrowing/01_bind` — bind tạo hàm mới
- **Xem thêm:** `11_function-borrowing/README` — overview call/apply/bind
- **Xem thêm:** `14_classes/02_constructor` — super() trong class kế thừa
- **Xem thêm:** `11_function-borrowing/05_polyfill` — tự viết myCall
