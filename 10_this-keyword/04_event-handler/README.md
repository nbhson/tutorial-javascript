# `this` trong event handler — [Level: Intermediate]

## 🔑 Khái niệm cốt lõi

Khi bạn đăng ký một event listener bằng `addEventListener` hoặc gán vào property event (như `element.onclick`), trình duyệt sẽ gọi callback **như một method của element** — tức bên trong callback, `this` chính là **element đã kích hoạt sự kiện**.

Cơ chế nội bộ: browser gọi `callback.call(element, event)`. Nói cách khác, `this` được ép ngầm bởi engine — tương đương với explicit binding, nhưng bạn không cần viết thủ công.

Điều này rất hữu ích khi bạn muốn thao tác trực tiếp lên element kích hoạt sự kiện (`this.style.color = "red"`) mà không cần `event.target`. Tuy nhiên, có **một ngoại lệ quan trọng**: nếu callback là **arrow function**, thì `this` **không phải element** — arrow function kế thừa `this` từ scope lexical bên ngoài.

```js
button.addEventListener("click", function () {
  console.log(this === button); // true — function thường
});

button.addEventListener("click", () => {
  console.log(this === button); // false — arrow kế thừa outer this
});
```

## 📐 Cấu trúc / Cú pháp

### Bảng so sánh handler types

| Kiểu handler | Cú pháp | `this` bên trong | Ghi chú |
|--------------|---------|-------------------|---------|
| Function thường | `el.onclick = function(){}` | `el` (element) | Default behavior |
| Function expression | `el.addEventListener("click", fn)` | `el` | Cùng mechanism |
| Arrow function | `el.addEventListener("click", ()=>{})` | Outer scope's `this` | Không phải element |
| Method bind | `el.addEventListener("click", obj.fn.bind(obj))` | `obj` | Ép thành obj |

### Sự khác biệt `this` vs `event.target`

| Thuộc tính | Ý nghĩa | Khi nào khác |
|------------|---------|---------------|
| `this` | Element đăng ký listener | Khi event bubbling từ con lên cha |
| `event.target` | Element thực sự được click | Luôn trỏ element gốc |
| `event.currentTarget` | Bằng `this` | Luôn bằng element có listener |

## ✅ Điểm mạnh — Tại sao nên dùng

1. **Truy cập element trực tiếp** — `this.style`, `this.classList` gọn hơn `event.target`.
2. **Event delegation tự nhiên** — một listener trên container, `this` xác định phần tử click.
3. **Tái sử dụng handler** — cùng một function, `this` tự động trỏ đúng element.
4. **Code ngắn gọn** — không cần `const el = e.target` nếu chỉ cần element hiện tại.
5. **Dễ đọc** — `this.disabled = true` rõ nghĩa hơn `event.currentTarget.disabled = true`.
6. **Phù hợp với OOP** — handler method truy cập `this.data`, `this.render()`.

## ⚠️ Bẫy thường gặp & Hạn chế

### Bẫy 1: Arrow function trong event handler — `this` sai

```js
const obj = {
  name: "Btn",
  init() {
    document.getElementById("btn").onclick = () => {
      console.log(this.name); // "Btn" — this là obj, KHÔNG phải button!
    };
  }
};
obj.init();
```

### Bẫy 2: Method của object làm handler — mất context nếu không bind

```js
const app = {
  name: "App",
  handleClick(e) {
    console.log(this.name); // "App" nếu bind, nhưng...
  }
};
document.getElementById("btn").onclick = app.handleClick;
// ❌ this = btn element, NOT app — method bị detached
```

### Bẫy 3: `this` trong bubbling phase

```js
parent.addEventListener("click", function () {
  console.log(this === parent); // true — listener trên parent
});
child.click(); // vẫn true vì listener đăng ký trên parent
```

### Bẫy 4: Inline handler `onclick="..."` — `this` là global

```html
<button onclick="console.log(this)">Click</button>
```
```js
// Trong inline handler, this = window (non-strict) hoặc undefined (strict)
// KHÔNG phải button! Muốn đúng phải dùng addEventListener
```

### Bẫy 5: `removeEventListener` cần cùng function reference

```js
function handler() { console.log(this); }
el.addEventListener("click", handler);
el.removeEventListener("click", handler); // ✅ xóa đúng
el.removeEventListener("click", function() { console.log(this); }); // ❌ hàm mới, không xóa được
```

## 💡 Khi nào dùng — Tình huống thực tế

1. **Button toggle** — `this.classList.toggle("active")` đổi class element được click.
2. **Form input** — `this.value` lấy giá trị input mà không cần `event.target.value`.
3. **List item action** — một listener trên `<ul>`, `this` là `<li>` con trong delegation.
4. **Custom component** — method `handleClick()` dùng `this.setState(...)`.
5. **Dynamic form validation** — `this.checkValidity()` trên element focus.
6. **Drag & drop** — `this` là element đang drag, dễ truy cập attributes.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Basic event handler với `this`

```js
// Mô phỏng cách browser gọi handler
const btn = { id: "myBtn", tag: "BUTTON" };

function addListener(el, cb) {
  cb.call(el); // browser ép this = el
}

function handleClick() {
  console.log("Clicked:", this.id); // "Clicked: myBtn"
}
addListener(btn, handleClick);
```

### Ví dụ 2: Real DOM — function thường vs arrow

```js
const button = document.getElementById("action-btn");

// ✅ Function thường — this = button
button.addEventListener("click", function () {
  this.style.backgroundColor = "blue";
  console.log("Handler this === button:", this === button);
});

// ❌ Arrow function — this = outer scope (window/global)
button.addEventListener("click", () => {
  this.style.backgroundColor = "red"; // lỗi hoặc wrong element
  console.log("Arrow this === button:", this === button); // false
});
```

### Ví dụ 3: Event delegation — một listener xử lý nhiều phần tử

```js
const list = document.getElementById("item-list");

list.addEventListener("click", function (e) {
  // this = list (element có listener)
  // e.target = item thực sự được click
  if (e.target.matches("li.delete-btn")) {
    const item = e.target.closest("li");
    item.remove();
  }
});
```

### Ví dụ 4: Object method + bind cho event handler

```js
const controller = {
  name: "MyController",
  init() {
    const btn = document.getElementById("trigger");
    // ⚠️ KHÔNG làm thế này: btn.onclick = this.handleClick;
    // ✅ Phải bind:
    btn.onclick = this.handleClick.bind(this);
  },
  handleClick() {
    console.log("Clicked from:", this.name); // "Clicked from: MyController"
  }
};
controller.init();
```

### Ví dụ 5: Multiple listeners với khác `this`

```js
const box = document.getElementById("box");

box.addEventListener("click", function () {
  console.log("Listener 1 (function):", this === box); // true
});

box.addEventListener("click", () => {
  console.log("Listener 2 (arrow):", this === window); // true (hoặc outer scope)
});
```

### Ví dụ 6: Form handler — lấy `this.value`

```js
const input = document.querySelector('input[name="username"]');

input.addEventListener("input", function () {
  // this === input, lấy value trực tiếp
  console.log("Typed:", this.value);
  this.dataset.typed = this.value; // thêm data attribute
});
```

## 🔬 So sánh với alternatives

| Cách | `this` | Ưu điểm | Nhược điểm |
|------|--------|---------|------------|
| `function(){}` handler | Element | Tự động, trực quan | Arrow không được |
| Arrow `()=>{}` handler | Outer scope | Giữ context object | Không lấy được element |
| `event.target` | Element clicked | Chính xác nhất | Dài dòng hơn |
| `event.currentTarget` | Element có listener | Luôn = `this` | Ít dùng |
| `.bind(this)` | Ép thành object | Giữ context class | Cần nhớ bind |

## 📊 Performance & Best Practices

- **Dùng function thường** khi cần `this` = element; **arrow** khi cần `this` = outer scope.
- **Sự kiện delegation** (một listener trên container) hiệu quả hơn nhiều listener trên từng item.
- **Ghi nhớ function reference** khi dùng `removeEventListener` — arrow tạo function mới mỗi lần.
- **Never dùng inline `onclick="..."`** — `this` trong inline handler là global, không phải element.

## 🔗 Liên kết chéo

- **Xem thêm:** `10_this-keyword/01_in-method` — implicit binding (nền tảng)
- **Xem thêm:** `10_this-keyword/05_arrow-function` — tại sao arrow sai trong handler
- **Xem thêm:** `10_this-keyword/06_arrow-lexical` — lexical binding deep dive
- **Xem thêm:** `11_function-borrowing/01_bind` — fix handler bằng bind
- **Xem thêm:** `18_dom-apis/README` — DOM event handling patterns
