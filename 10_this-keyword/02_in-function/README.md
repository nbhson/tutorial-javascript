# `this` trong hàm thường (không phải method của object) — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

Khi một hàm được gọi **không qua object** — tức gọi trần `fn()` hoặc gọi qua biến tham chiếu đã tách từ object — JavaScript áp dụng quy tắc **default binding**. Giá trị của `this` trong trường hợp này phụ thuộc vào **strict mode**:

- **Non-strict mode:** `this` = `window` (browser) / `globalThis` (Node.js). Đây là object toàn cục.
- **Strict mode (`"use strict"`):** `this` = `undefined`. Engine không gán gì cả — an toàn hơn vì bắt lỗi sớm.

Trường hợp **"mất context"** kinh điển nhất: gán `const fn = obj.hi;` rồi gọi `fn()`. Về mặt kỹ thuật, hàm vẫn y nguyên nhưng **không còn ai đứng trước dấu chấm** khi gọi — nên `this` không còn là `obj` nữa mà rơi về default binding.

Đây là lỗi phổ biến hàng đầu khiến developer mới bối rối. Nhiều người nghĩ `this` được "ghép cứng" vào hàm khi khai báo, nhưng thực tế `this` được xác định **tại thời điểm gọi** (call-site).

## 📐 Cấu trúc / Cú pháp

### Bảng so sánh default binding

| Scenario | Code | `this` trong hàm |
|----------|------|------------------|
| Gọi hàm trần (non-strict) | `function fn() {} fn()` | `window` / `globalThis` |
| Gọi hàm trần (strict) | `"use strict"; function fn() {} fn()` | `undefined` |
| Gọi qua biến đã tách | `const fn = obj.method; fn()` | Như trên — default binding |
| Gọi qua biến global | `let x = 1; function fn() { return x; }` | `window` (read `x` qua closure) |
| Constructor gọi trần | `Car("Ford")` thay vì `new Car("Ford")` | `window` / `undefined` |

### Sự khác biệt giữa implicit và default

```js
const obj = { name: "A", hi() { console.log(this.name); } };

obj.hi();          // implicit → this = obj → "A"
const fn = obj.hi;
fn();              // default → this = window/undefined → undefined
```

## ✅ Điểm mạnh — Tại sao nên dùng

1. **Hiểu cốt lõi `this`** — nắm được default binding là nền tảng để hiểu mọi quy tắc khác.
2. **Phát hiện lỗi sớm** — strict mode khiến `this` = `undefined` thay vì `window`, dễ throw TypeError.
3. **Vẫn hữu ích** — khi hàm không cần `this` (pure function), default binding không gây hại.
4. **Access global object** — trong non-strict mode, `this` cho phép truy cập `window` mà không cần tên biến.
5. **Nhận diện "detached method"** — biết rõ nguyên nhân khi method không hoạt động như mong đợi.
6. **Debug hiệu quả** — hiểu tại sao `this.name` là `undefined` giúp sửa lỗi nhanh hơn.

## ⚠️ Bẫy thường gặp & Hạn chế

### Bẫy 1: Strict mode khiến `this` = `undefined`

```js
"use strict";
function whatIsThis() {
  return this;
}
whatIsThis(); // undefined — không phải window!
```

### Bẫy 2: Tách method khỏi object — silent failure

```js
const store = { items: [1, 2], count() { return this.items.length; } };
const getCount = store.count;
getCount(); // TypeError: Cannot read properties of undefined
```

### Bẫy 3: Callback nhận method — mất context

```js
function process(fn) { fn(); }
process(store.count); // undefined — this mất trong process()
```

### Bẫy 4: `new` không được gọi — constructor hoạt động như hàm thường

```js
function Book(title) { this.title = title; }
const b = Book("JS"); // ❌ gán vào window
console.log(window.title); // "JS" — bug nguy hiểm!
```

### Bẫy 5: Arrow function trong function thường vẫn kế thừa đúng

```js
function outer() {
  const arrow = () => console.log(this); // kế thừa this của outer
  arrow();
}
outer.call({ x: 1 }); // {x: 1} — arrow lấy this từ outer, không từ call
```

## 💡 Khi nào dùng — Tình huống thực tế

1. **Pure utility functions** — hàm không cần `this`, ví dụ `Math.max()`, `parseNumber()`.
2. **Debugging `this` bugs** — hiểu default binding giúp tìm ra nguyên nhân `undefined`.
3. **Nền tảng học `bind`** — hiểu vì sao cần `bind` khi method bị mất context.
4. **Global helper** — trong non-strict mode, đôi khi dùng `this` để truy cập object toàn cục.
5. **Transition cũ → mới** — code legacy có thể dựa vào `window`, cần hiểu hành vi này.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Default binding — non-strict

```js
function showGlobal() {
  console.log("this === window:", this === window); // true
  console.log("this === globalThis:", this === globalThis); // true
}
showGlobal();
```

### Ví dụ 2: Default binding — strict mode

```js
"use strict";
function showUndefined() {
  console.log(this); // undefined
  // this.name → TypeError: Cannot read properties of undefined
}
showUndefined();
```

### Ví dụ 3: Detached method — so sánh rõ ràng

```js
const obj = {
  name: "Detached Demo",
  hi() {
    console.log("Current this.name:", this.name);
  }
};

console.log("--- Gọi qua obj ---");
obj.hi(); // "Current this.name: Detached Demo"

console.log("--- Gọi qua biến detached ---");
const fn = obj.hi;
fn(); // "Current this.name: undefined" — THIS LÀ LỖI PHỔ BIẾN
```

### Ví dụ 4: Constructor gọi không có `new` — hậu quả

```js
function Person(name) {
  this.name = name; // gán vào globalThis nếu không có new
}

const p = Person("Alice"); // ❌ quên new
console.log(window.name);  // "Alice" — ôi trời, đã làm bẩn global scope!
```

### Ví dụ 5: Strict mode + constructor — lỗi sớm hơn

```js
"use strict";
function SafePerson(name) {
  if (new.target === undefined) {
    throw new Error("Must use 'new' keyword");
  }
  this.name = name;
}
SafePerson("Bob"); // Throws: Must use 'new' keyword
new SafePerson("Bob"); // ✅ Works fine
```

### Ví dụ 6: Nested function — từng scope có `this` riêng

```js
const obj = {
  name: "Outer Obj",
  nested() {
    console.log("nested this.name:", this.name); // "Outer Obj"
    
    function inner() {
      // inner() là hàm thường → default binding
      console.log("inner this:", this); // window / undefined
    }
    inner();
  }
};
obj.nested();
```

## 🔬 So sánh với alternatives

| Cách | Ưu điểm | Nhược điểm |
|------|---------|------------|
| Default binding (function thường) | Đơn giản, mặc định | Dễ mất context |
| `call`/`apply`/`bind` | Ép `this` tường minh | Cần chủ động gọi |
| Arrow function | Kế thừa `this` từ outer scope | Không dùng làm method được |
| `const that = this` | Works everywhere | Dài dòng, dễ quên |

## 📊 Performance & Best Practices

- **Luôn bật strict mode** — giúp default binding trả về `undefined` thay vì `window`, dễ debug.
- **Kiểm tra `new.target`** trong constructor để bắt lỗi gọi trần.
- **Không dựa vào `this` trong hàm toàn cục** — code portable cần không phụ thuộc environment.
- Khi truyền method làm callback, **luôn bind** hoặc dùng **arrow wrapper**.

## 🔗 Liên kết chéo

- **Xem thêm:** `10_this-keyword/01_in-method` — implicit binding (đối lập với default)
- **Xem thêm:** `10_this-keyword/03_alone` — global `this` chi tiết
- **Xem thêm:** `11_function-borrowing/01_bind` — cách sửa detached method
- **Xem thêm:** `10_this-keyword/05_arrow-function` — arrow function không bị default binding
- **Xem thêm:** `11_function-borrowing/03_call` — explicit binding qua call
