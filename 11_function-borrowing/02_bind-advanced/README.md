# Function Borrowing — `bind` nâng cao — [Level: Advanced]

## 🔑 Khái niệm cốt lõi

Khi đã nắm `bind` cơ bản, ta khai thác hai sức mạnh lớn:

1. **Bind cho phương thức của object khác** — phổ biến nhất là `document.querySelector.bind(document)`: gán `$` như một shortcut sạch, và giữ đúng `this` là `document`. Kỹ thuật này biến method thành function độc lập, an toàn khi truyền qua nhiều scope.

2. **Partial application / currying** — chốt trước vài đối số vào thời điểm `bind`, phần còn lại truyền khi gọi. Kết hợp chốt cả `this` lẫn đối số trong một lần — đây là nền tảng của functional programming trong JS.

Trong ứng dụng thực tế, `bind` còn dùng để tổ chức event delegation: một listener duy nhất trên container, `this` chính xác là object quản lý (app controller).

## 📐 Cấu trúc / Cú pháp

### Partial Application pattern

```js
// Hàm tổng quát
function calculate(operator, a, b) { ... }

// Tạo hàm chuyên biệt bằng bind
const add = calculate.bind(null, "add");
const multiply = calculate.bind(null, "multiply");

// Gọi với đối số còn thiếu
add(5, 3);   // calculate("add", 5, 3)
multiply(5, 3); // calculate("multiply", 5, 3)
```

### DOM shortcut pattern

```js
// Bind document method — this luôn = document
const $ = document.querySelector.bind(document);
const $$ = document.querySelectorAll.bind(document);

// Sử dụng ở bất kỳ scope nào
$(".app").style.display = "none";
$$("button").forEach(btn => btn.disabled = true);
```

### Event delegation + bind

```js
const app = {
  handleDelete(e) {
    // this = app (do bind), e.target = button thực sự
    const btn = e.target.closest(".delete");
    if (btn) this.delete(btn.dataset.index);
  },
  init() {
    document.getElementById("list").onclick = this.handleDelete.bind(this);
  }
};
```

## ✅ Điểm mạnh — Tại sao nên dùng

1. **Shortcut DOM an toàn** — `const $ = document.querySelector.bind(document)` ngắn gọn, không bị mất context.
2. **Currying tự nhiên** — hàm chuyên biệt từ hàm tổng quát (đóng sẵn greeting, suffix...).
3. **Event delegation clean** — một listener, `this` chính xác là object quản lý.
4. **Không cần biến phụ** `that`/`self` khi viết callback.
5. **Reusable utilities** — tạo hàm tiện ích từ hàm chung với đối số cố định.
6. **Mock testing** — bind mock object để test method không phụ thuộc real data.
7. **Plugin architecture** — bind plugin method vào host object.
8. **Middleware pattern** — bind context cho middleware chain.

## ⚠️ Bẫy thường gặp & Hạn chế

### Bẫy 1: Quên bind — this rơi về global

```js
const $ = document.querySelector; // ❌ quên bind
$(".app"); // this = globalThis → TypeError: Cannot read properties of undefined
```

### Bẫy 2: Delegate + bind nhầm context

```js
root.onclick = this.handleDelete; // ❌ this = root element (event binding), không phải app
root.onclick = this.handleDelete.bind(this); // ✅
```

### Bẫy 3: Currying quá nhiều đối số — khó đọc

```js
// quá nested
const fn = baseFn.bind(null, a).bind(null, b).bind(null, c);
// nên dùng arrow hoặc partial helper
```

### Bẫy 4: Bind lại không được — permanent binding

```js
const fn = greet.bind(user1);
fn.call(user2); // vẫn là user1
```

### Bẫy 5: Bind method không có `this` (static/utility)

```js
const bound = Math.max.bind(null); // vô nghĩa — Math.max không dùng this
bound([1, 2, 3]); // NaN
```

## 💡 Khi nào dùng — Tình huống thực tế

1. **Tạo alias cho DOM API** — `const $ = document.querySelector.bind(document)`, `const $$ = document.querySelectorAll.bind(document)`.
2. **Gắn method của object vào event** — `root.onclick = app.handleDelete.bind(app)`.
3. **Currying utility** — hàm `greet(greeting, name)` → `sayHello = greet.bind({ suffix: "!" }, "Hello ")`.
4. **Viết library/framework** — module IIFE cần giữ context nội bộ.
5. **Middleware binding** — bind app context cho middleware chain.
6. **Component lifecycle** — bind handler trong constructor để dùng trong lifecycle.
7. **State management** — bind store method cho action handlers.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: DOM shortcut — $ và $$

```js
const $ = document.querySelector.bind(document);
const $$ = document.querySelectorAll.bind(document);

// An toàn ở mọi nơi, even trong nested callback
function initApp() {
  const header = $(".header");
  const items = $$("li");
  items.forEach(item => header.appendChild(item));
}

// Thử bỏ bind:
const bad$ = document.querySelector; // ❌
bad$(".header"); // TypeError: this is undefined
```

### Ví dụ 2: Currying với bind

```js
function greet(greeting, name, suffix) {
  return `${greeting} ${name}${suffix}`;
}

// Chốt suffix = "!", greeting = "Hello "
const sayHello = greet.bind(null, "Hello ", null, "!");
// Vẫn cần name khi gọi
// ❌ bind đã chốt 2 đối số đầu, còn lại 1
// Đúng hơn:
const partialHello = greet.bind(null, "Hello ");
console.log(partialHello("An", "!")); // "Hello An!"
```

### Ví dụ 3: Event delegation với bind

```js
const app = {
  cars: ["BMW", "Audi", "Tesla"],
  
  handleDelete(e) {
    const btn = e.target.closest(".delete");
    if (btn) {
      this.deleteCar(btn.dataset.index);
    }
    this.render();
  },
  
  deleteCar(index) {
    this.cars.splice(index, 1);
  },
  
  render() {
    const root = $("#root");
    root.innerHTML = this.cars.map((car, i) => 
      `<li>${car} <button class="delete" data-index="${i}">X</button></li>`
    ).join("");
  },
  
  init() {
    // bind giữ this = app dù onclick gọi bởi element
    $("#root").onclick = this.handleDelete.bind(this);
    this.render();
  }
};
app.init();
```

### Ví dụ 4: Partial application — calculator

```js
function calculator(op, a, b) {
  switch(op) {
    case "add": return a + b;
    case "sub": return a - b;
    case "mul": return a * b;
    case "div": return a / b;
  }
}

const add = calculator.bind(null, "add");
const mul = calculator.bind(null, "mul");

console.log(add(5, 3));   // 8
console.log(mul(5, 3));   // 15
console.log(add(10, 20)); // 30
```

### Ví dụ 5: Multi-level binding (deep currying)

```js
function createPost(author, title, content) {
  return { author, title, content, published: false };
}

// Currying từng bước
const makePostWithTitle = createPost.bind(null, "Admin");
const draftPost = makePostWithTitle.bind(null, "JS Tutorial");
const post = draftPost("Understanding this keyword");

console.log(post); 
// { author: "Admin", title: "JS Tutorial", content: "Understanding this keyword", published: false }
```

### Ví dụ 6: Array method borrowing với bind

```js
const arrayLike = { 0: "a", 1: "b", 2: "c", length: 3 };

// Mượn Array.prototype methods
const slice = Array.prototype.slice.bind(arrayLike);
const arr = slice(); // ["a", "b", "c"]

const map = Array.prototype.map.bind(arrayLike);
const upper = map(item => item.toUpperCase()); // ["A", "B", "C"]
```

### Ví dụ 7: Binding với NaN/undefined edge cases

```js
function identity(x) { return x; }

// Bind với null/undefined
const fn1 = identity.bind(null);
fn1(42); // 42 — thisArg không dùng trong identity()

const fn2 = identity.bind(undefined);
fn2(42); // 42

// Nhưng với method cần this
const obj = { val: 1, get() { return this.val; } };
const getter = obj.get.bind(null);
getter(); // undefined (non-strict) hoặc throw (strict)
```

## 🔬 So sánh với alternatives

| Cách | Partial application | Reusable |可读性 |
|------|--------------------|----------|--------|
| `bind()` | ✅ | ✅ | Trung bình |
| Arrow wrapper | ✅ | ⚠️ | Cao |
| Curry function | ✅✅ | ✅ | Cao |
| Default params | ⚠️ | ❌ | Cao |

```js
// Alternative: arrow wrapper
const add5 = (b) => calculator("add", 5, b);

// Alternative: curry helper
function curry(fn) {
  return function curried(...args) {
    return args.length >= fn.length ? fn(...args) : (...more) => curried(...args, ...more);
  };
}
```

## 📊 Performance & Best Practices

- **Pre-bind trong constructor/init** — bind một lần, dùng nhiều lần → hiệu quả hơn bind trong loop.
- **Arrow wrapper thay bind trong loop** — tránh tạo N closure objects.
- **Currying depth ≤ 3** — quá sâu khó đọc, dùng helper function thay thế.
- **Bind `null` khi hàm không dùng this** — ví dụ `Math.max.bind(null)` vô nghĩa, dùng trực tiếp.
- **Cache bound functions** — nếu cùng đối số bind nhiều lần, lưu lại để reuse.

## 🔗 Liên kết chéo

- **Xem thêm:** `11_function-borrowing/01_bind` — bind cơ bản
- **Xem thêm:** `11_function-borrowing/03_call` — call gọi ngay
- **Xem thêm:** `11_function-borrowing/05_polyfill` — polyfill bind
- **Xem thêm:** `10_this-keyword/06_arrow-lexical` — lexical this alternative
- **Xem thêm:** `09_functions/01_parameters-and-arrow/06_function-parameters` — rest parameters cho curry
