# Arrow function không có `this` — [Level: Intermediate]

## 🔑 Khái niệm cốt lõi

Arrow function (`() => {}`) **không có `this` riêng của nó**. Đây là đặc điểm khác biệt quan trọng nhất so với function thường. Thay vì tạo `this` mới dựa trên cách gọi (call-site), arrow function **mượn lexical `this`** — tức `this` từ phạm vi bao bọc ngay bên ngoài nơi nó được khai báo.

Điều này có nghĩa:
- Gọi `arrow.call(obj)` / `arrow.apply(obj)` / `arrow.bind(obj)` đều **hoàn toàn không đổi** được `this` — các phương thức explicit binding bị bỏ qua.
- Gọi `arrow()` như method của object (`obj.arrow()`) thì `this` vẫn **không phải `obj`** — nó là `this` của scope bao quanh lúc khai báo.
- `this` bên trong arrow được "chốt" ngay lúc **khai báo**, dựa vào scope LEXICAL chứ không phải lúc gọi.

Chính vì vậy, arrow function **không bao giờ được dùng làm method của object** nếu bạn cần `this` trỏ object đó.

## 📐 Cấu trúc / Cú pháp

### Đặc điểm arrow function liên quan đến `this`

| Đặc điểm | Function thường | Arrow function |
|----------|-----------------|----------------|
| Có `this` riêng | ✅ | ❌ — kế thừa từ outer scope |
| `call`/`apply`/`bind` đổi được `this` | ✅ | ❌ — bị bỏ qua |
| Dùng làm method | ✅ | ❌ — `this` sai |
| Dùng làm constructor (`new`) | ✅ | ❌ — TypeError |
| Có `arguments` object | ✅ | ❌ — dùng rest params `...args` |
| Lexical `this` | ❌ — dynamic binding | ✅ — static binding |

### Cú pháp cơ bản

```js
// Function thường — this được xác định khi gọi
function regular() { console.log(this); }

// Arrow function — this kế thừa từ scope chứa nó
const arrow = () => console.log(this);
```

## ✅ Điểm mạnh — Tại sao nên dùng

1. **Giữ context ổn định trong callback** — `setTimeout(() => this.method(), 0)` không lo mất `this`.
2. **Không cần `const that = this` hay `.bind(this)`** — code sạch hơn nhiều.
3. **Dự đoán được** — nhìn vào nơi khai báo là biết `this` là gì.
4. **Ngắn gọn, súc tích** — cú pháp ít chữ, phù hợp callback one-liner.
5. **Không có `arguments`** — tránh nhầm lẫn với biến `arguments` của outer function.
6. **Không dùng được `new`** — ngăn ngừa việc gọi nhầm arrow làm constructor.
7. **Hiệu suất tốt** — engine tối ưu arrow function tốt hơn function thường trong nhiều case.
8. **Phù hợp array methods** — `arr.map(x => x * 2)` — `this` không liên quan, không lo conflict.

## ⚠️ Bẫy thường gặp & Hạn chế

### Bẫy 1: Arrow làm method — `this` là global/undefined

```js
const obj = {
  value: 42,
  getValue: () => this.value  // this = globalThis, không phải obj
};
obj.getValue(); // undefined (hoặc globalThis.value)
```

### Bẫy 2: Call/Apply/Bind vô dụng với arrow

```js
const arrow = () => console.log(this);
arrow.call({ x: 1 }); // vẫn in globalThis/undefined, KHÔNG in {x: 1}
```

### Bẫy 3: Arrow trong object method — kế thừa từ method, không từ object

```js
const counter = {
  count: 0,
  increment() {
    setTimeout(() => {
      this.count++; // ✅ this = counter (kế thừa từ increment)
    }, 100);
  }
};
```

### Bẫy 4: Không dùng được `new` với arrow

```js
const Person = () => {};
new Person(); // TypeError: Person is not a constructor
```

### Bẫy 5: Mất `arguments` object

```js
const fn = (...args) => args;  // ✅ dùng rest
const bad = () => arguments;   // ❌ ReferenceError — arrow không có arguments
```

### Bẫy 6: Arrow trong event handler — `this` không phải element

```js
btn.addEventListener("click", () => {
  console.log(this); // globalThis/undefined — KHÔNG phải btn
});
```

## 💡 Khi nào dùng — Tình huống thực tế

1. **Callback bất đồng bộ giữ context** — `setTimeout`, `Promise.then`, `fetch().then()`.
2. **Array methods** — `map`, `filter`, `reduce` với callback ngắn, không cần `this`.
3. **React/Vue component callbacks** — `onClick={() => this.handleSubmit()}`.
4. **Higher-order functions** — `compose`, `curry` không cần `this`.
5. **One-liner expressions** — `arr.sort((a, b) => a - b)`.
6. **IIFE modern替代** — `(params => { ... })(values)` không cần function keyword.
7. **Data transformation pipelines** — chuỗi `.map().filter().reduce()` sạch sẽ.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Arrow không đổi bằng call/apply/bind

```js
const globalThis = { name: "global" };
const customThis = { name: "custom" };

const arrow = () => console.log(this.name);

arrow.call(customThis);   // "global" — call bị bỏ qua
arrow.apply(customThis);  // "global" — apply bị bỏ qua
arrow.bind(customThis)(); // "global" — bind bị bỏ qua
```

### Ví dụ 2: Arrow làm method — sai kết quả

```js
const user = {
  name: "Alice",
  // ❌ WRONG: arrow method
  getName: () => this.name,
};
user.getName(); // undefined — this không phải user
```

### Ví dụ 3: Arrow giữ context trong setTimeout

```js
const person = {
  name: "Bob",
  greet() {
    // Arrow kế thừa this từ greet() — tức person
    setTimeout(() => {
      console.log(`Hello, I'm ${this.name}`); // "Hello, I'm Bob"
    }, 1000);
  }
};
person.greet();
```

### Ví dụ 4: So sánh function thường vs arrow trong setTimeout

```js
const app = {
  count: 0,

  // ❌ Function thường — this = window trong setTimeout
  incrementBad() {
    setInterval(function () {
      this.count++; // TypeError: Cannot read properties of undefined
    }, 1000);
  },

  // ✅ Arrow — this = app
  incrementGood() {
    setInterval(() => {
      this.count++; // ✅ this vẫn là app
      console.log("count:", this.count);
    }, 1000);
  }
};
```

### Ví dụ 5: Arrow trong Array methods

```js
const numbers = [1, 2, 3, 4, 5];

// ✅ Arrow không cần this — perfect cho array methods
const doubled = numbers.map(n => n * 2);          // [2, 4, 6, 8, 10]
const evens = numbers.filter(n => n % 2 === 0);   // [2, 4]
const sum = numbers.reduce((acc, n) => acc + n);   // 15
```

### Ví dụ 6: Arrow trong object method — trường hợp hợp lệ

```js
const calculator = {
  base: 10,
  operations: [
    { name: "square", fn: x => x * x },
    { name: "double", fn: x => x * 2 }
  ],
  run(opIndex, value) {
    return this.operations[opIndex].fn(value);
  }
};
console.log(calculator.run(0, 5)); // 25 (square)
console.log(calculator.run(1, 5)); // 10 (double)
```

## 🔬 So sánh với alternatives

| Cách | `this` behavior | Ưu điểm | Nhược điểm |
|------|-----------------|---------|------------|
| Arrow `()=>{}` | Kế thừa từ outer scope | Dự đoán được, không bind | Không dùng làm method |
| Function thường | Dynamic (call-site) | Linh hoạt, dùng được mọi chỗ | Dễ mất context |
| `.bind(this)` | Ép thành object | Giữ được function thường | Tạo thêm closure |
| `const that = this` | Tham chiếu outer `this` | Works everywhere | Dài dòng |

## 📊 Performance & Best Practices

- **Arrow function nhẹ hơn** function thường — engine tối ưu tốt hơn cho callback pattern.
- **Tránh arrow trong class fields** nếu không cần — có thể gây memory leak nếu subclass override.
- **Luôn dùng arrow trong Promise chains** — `promise.then(() => ...)` giữ context đúng.
- **Không bao giờ dùng arrow làm constructor hoặc object method** —违背设计意图.
- **Dùng arrow trong React props** — `onClick={() => handler()}` hoặc arrow method field.

## 🔗 Liên kết chéo

- **Xem thêm:** `10_this-keyword/06_arrow-lexical` — lexical binding sâu hơn
- **Xem thêm:** `10_this-keyword/05_arrow-function` — bài này đang đọc
- **Xem thêm:** `10_this-keyword/04_event-handler` — tại sao arrow sai trong event handler
- **Xem thêm:** `11_function-borrowing/01_bind` — alternative khi cần bind
- **Xem thêm:** `09_functions/01_parameters-and-arrow/03_arrow-functions` — arrow functions chi tiết
