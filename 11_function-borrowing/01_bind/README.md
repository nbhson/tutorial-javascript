# Phương thức `bind()` — [Level: Intermediate]

## 🔑 Khái niệm cốt lõi

`fn.bind(thisArg, arg1, arg2, ...)` trả về một **hàm mới** với `this` được khóa lại thành `thisArg` (và các đối số đầu có thể được truyền trước). Điểm then chốt: **`bind` không gọi hàm ngay** — bạn phải tự gọi hàm mới trả về bằng `()`.

Khi gọi `bind`, engine tạo một **closure wrapper** mới. Hàm mới này có vùng nhớ riêng, không bằng hàm gốc (`boundFn !== originalFn`). Mỗi lần gọi hàm mới, engine gọi lại hàm gốc với `this` đã được ép thành `thisArg`.

Các đối số truyền vào lúc `bind` được **ưu tiên hơn** khi gọi — chúng được chốt trước, phần còn lại truyền khi gọi hàm mới (partial application).

**Arrow function là ngoại lệ**: `call`/`apply`/`bind` đều bị bỏ qua, không ảnh hưởng gì.

## 📐 Cấu trúc / Cú pháp

### Signature đầy đủ

```js
const boundFn = fn.bind(thisArg, arg1, arg2, ...);
// sau đó gọi:
const result = boundFn(argN, argN+1, ...);
```

### Bảng tham số

| Tham số | Bắt buộc? | Ý nghĩa |
|---------|-----------|---------|
| `thisArg` | ✅ | Object sẽ成为 `this` bên trong hàm |
| `arg1, arg2, ...` | ❌ | Các đối số cố định, ghép trước khi gọi |

###.return value

| Trường hợp | Trả về |
|------------|--------|
| `fn.bind(obj)` | Hàm mới, `this` = `obj`, không có đối số cố định |
| `fn.bind(obj, a)` | Hàm mới, `this` = `obj`, đối số đầu = `a` |
| `fn.bind(obj, a, b)` | Hàm mới, `this` = `obj`, đối số đầu = `a`, second = `b` |

## ✅ Điểm mạnh — Tại sao nên dùng

1. **Tạo hàm "đóng gói sẵn"** — `this` đã khóa, dùng cho callback/event handler mà không sợ mất context.
2. **Partial application** — chốt trước một phần đối số, gọi sau với phần còn lại.
3. **Reusable bound function** — hàm mới có thể gọi nhiều lần với cùng `this`.
4. **Event handler pattern** — `el.onclick = obj.method.bind(obj)` giữ context object.
5. **Method borrowing** — mượn method object này cho object khác.
6. **Currying step** — từng bước chốt đối số, xây dựng hàm chuyên biệt.
7. **Safe callback passing** — truyền method làm callback mà không bị detached.
8. **Testing/mock pattern** — bind mock object để test method độc lập.

## ⚠️ Bẫy thường gặp & Hạn chế

### Bẫy 1: Quên gọi hàm mới — bug phổ biến nhất

```js
const bound = greet.bind(user);
// bound là hàm, chưa gọi!
// bound(); // ✅ phải gọi thêm
```

### Bẫy 2: Bind permanent — không thể override sau đó

```js
const fn = sayHi.bind(user1);
fn.call(user2); // vẫn là user1 — bind đã khóa permanent
```

### Bẫy 3: Bind arrow function = vô dụng

```js
const arrow = () => console.log(this);
arrow.bind({ x: 1 })(); // vẫn in globalThis
```

### Bẫy 4: Bind không hoạt động với method cần `this` động

```js
const obj = { val: 1, get() { return this.val; } };
const boundGet = obj.get.bind({ val: 2 });
boundGet(); // 2 — đã bind thì không đổi được
```

### Bẫy 5: Mượn method cho object không tương thích

```js
const dog = { bark() { return "Gâu!"; } };
const cat = { meow() { return "Meo!"; } };
dog.bark.call(cat); // "Gâu!" — cat nhận bark nhưng không có meow logic
```

### Bẫy 6: Bind trong loop — tạo nhiều function object

```js
items.forEach((item, i) => {
  btns[i].onclick = handler.bind(this, item); // tạo N hàm mới
});
// Fix: dùng arrow wrapper thay bind trong loop
```

## 💡 Khi nào dùng — Tình huống thực tế

1. **Gán method làm callback** — `submit.onclick = obj.handle.bind(obj)`.
2. **Chốt context cho list handlers** — `document.querySelector.bind(document)`.
3. **Partial application** — `const add5 = add.bind(null, 5)`.
4. **Event delegation giữ context** — `root.onclick = app.handler.bind(app)`.
5. **Factory function** — tạo instance với method đã bind sẵn.
6. **Mock testing** — bind mock object để test method.
7. **Memoization wrapper** — bind cache object cho function.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Cơ bản — bind this

```js
const student = { firstName: "Dang", lastName: "Son" };

function getFullName() {
  return `${this.firstName} ${this.lastName}`;
}

const getName = getFullName.bind(student);
console.log(getName()); // "Dang Son"
console.log(getName === getFullName); // false — hàm mới, vùng nhớ khác
```

### Ví dụ 2: Partial application — chốt đối số

```js
function getFullName(age, city) {
  return `${this.firstName} ${this.lastName}, ${age} tuổi, ${city}`;
}

// Chốt age = 18, city còn lại khi gọi
const getName = getFullName.bind(student, 18);
console.log(getName("HCMC")); // "Dang Son, 18 tuổi, HCMC"
```

### Ví dụ 3: Event handler với bind

```js
const app = {
  name: "MyApp",
  handleClick(e) {
    console.log(`${this.name} clicked on`, e.target.id);
  },
  init() {
    document.getElementById("btn").onclick = this.handleClick.bind(this);
  }
};
app.init();
// Click button → "MyApp clicked on btn"
```

### Ví dụ 4: Method borrowing với bind

```js
const person = {
  greet() { return `Hello, I'm ${this.name}`; }
};

const user1 = { name: "Alice" };
const user2 = { name: "Bob" };

const sayHello = person.greet.bind;
console.log(sayHello(user1)); // "Hello, I'm Alice"
console.log(sayHello(user2)); // "Hello, I'm Bob"
```

### Ví dụ 5: currying với bind

```js
function multiply(a, b, c) {
  return a * b * c;
}

// Currying: chốt từng đối số
const double = multiply.bind(null, 2);
const triple = double.bind(null, 3);
console.log(triple(5)); // 30 (2 * 3 * 5)
```

### Ví dụ 6: DOM shortcut với bind

```js
const $ = document.querySelector.bind(document);
const $$ = document.querySelectorAll.bind(document);

// Dùng an toàn ở bất kỳ đâu, this luôn = document
$(".header").style.color = "red";
$$("li").forEach(li => li.classList.add("item"));
```

### Ví dụ 7: Bind trong class method field (modern pattern)

```js
class Timer {
  constructor(label) {
    this.label = label;
    this.count = 0;
    // Arrow field method — tự động bind this
    this.tick = () => {
      this.count++;
      console.log(`${this.label}: ${this.count}`);
    };
  }
}
const t = new Timer("Clock");
setInterval(t.tick, 1000); // ✅ this vẫn là t
```

## 🔬 So sánh với alternatives

| Cách | `this` behavior | Gọi ngay? | Ưu điểm | Nhược điểm |
|------|-----------------|-----------|---------|------------|
| `bind()` | Ép thành object | ❌ | Tạo hàm reusable | Tạo thêm closure |
| `call()` | Ép thành object | ✅ | Gọi ngay, gọn | Không dùng cho callback |
| `apply()` | Ép thành object | ✅ | Nhận mảng đối số | Không tạo hàm mới |
| Arrow method | Lexical this | ✅ | Không cần bind | Không dùng làm constructor |
| `const that = this` | Closure reference | ✅ | Works legacy | Dài dòng |

## 📊 Performance & Best Practices

- **Bind tạo một closure function** — overhead nhỏ (~1-2% slower), chấp nhận được cho event handlers.
- **Tránh bind trong loop** — tạo N function objects; dùng arrow wrapper hoặc pre-bind outside loop.
- **Pre-bind trong constructor** — nếu method dùng nhiều lần, bind một lần khi init.
- **Bind với `null`/`undefined`** — trong non-strict mode chuyển thành global, strict mode giữ nguyên.
- **Class field arrow** thay `bind` trong constructor — cleaner syntax, tự động bind.

## 🔗 Liên kết chéo

- **Xem thêm:** `11_function-borrowing/02_bind-advanced` — partial application, event delegation nâng cao
- **Xem thêm:** `11_function-borrowing/03_call` — gọi ngay thay vì tạo hàm mới
- **Xem thêm:** `11_function-borrowing/04_apply` — apply khác bind ở gọi ngay
- **Xem thêm:** `10_this-keyword/05_arrow-function` — arrow không cần bind
- **Xem thêm:** `11_function-borrowing/README` — overview function borrowing
