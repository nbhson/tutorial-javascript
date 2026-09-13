# `this` bên trong method của object — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

Khi một hàm được gọi **dưới dạng method** của một object — tức cú pháp `objectName.methodName()` — JavaScript áp dụng quy tắc **implicit binding**: `this` bên trong hàm chính là **object đang gọi method đó**. Đây là quy tắc cơ bản nhất và là nền tảng cho mọi khái niệm `this` sau này.

Cơ chế hoạt động: khi engine gặp `obj.method()`, nó đọc toán hạng trái của dấu chấm (`obj`) và gán nó làm `this` cho execution context của `method`. Điều này xảy ra **tại thời điểm gọi** (runtime), không phải tại thời điểm khai báo. Vì vậy cùng một method, gọi từ object khác nhau sẽ cho `this` khác nhau.

Một điểm quan trọng: với **nested object** (object lồng nhau), `this` luôn trỏ tới **object trực tiếp sở hữu method** — tức object đứng ngay trước dấu chấm cuối cùng trong chuỗi gọi, không phải object ngoài cùng.

```
obj.inner.method()  →  this = obj.inner  (không phải obj)
```

## 📐 Cấu trúc / Cú pháp

### Cú pháp gọi method

| Cú pháp | Cách gọi | `this` |
|---------|----------|--------|
| `obj.method()` | Gọi trực tiếp qua object | `obj` |
| `obj.nested.method()` | Gọi qua object lồng | `obj.nested` |
| `(obj.method)()` | Tách ra biến rồi gọi | ❌ default binding (không phải `obj`) |
| `obj["method"]()` | Gọi qua key string | `obj` |

### So sánh implicit vs explicit

```js
// Implicit: this = obj
const person = {
  name: "Lan",
  greet() { return `Hello, ${this.name}`; }
};
person.greet(); // "Hello, Lan"

// Nếu gán ra biến riêng — mất implicit binding
const fn = person.greet;
fn(); // "Hello, undefined" — this = window/undefined
```

## ✅ Điểm mạnh — Tại sao nên dùng

1. **Code hướng object tự nhiên** — method truy cập trực tiếp dữ liệu của object chứa nó.
2. **Cùng method, khác object** — method `getInfo()` hoạt động đúng với bất kỳ object nào gọi nó.
3. **Không cần biến toàn cục** — dữ liệu đóng gói trong object, an toàn và sạch.
4. **Dễ mở rộng** — thêm object mới, chỉ cần đảm bảo có cùng cấu trúc method.
5. **Tiền đề cho prototype/class** — hiểu implicit binding là bước đầu học OOP trong JS.
6. **Hiệu suất tốt** — method trên object literal hoặc prototype đều nhanh, không tốn overhead.
7. **Debug dễ** — `console.log(this)` trong method cho thấy đúng object đang gọi.
8. **Tương thích với nhiều pattern** — function constructor, object literal, class đều dùng chung cơ chế.

## ⚠️ Bẫy thường gặp & Hạn chế

### Bẫy 1: Tách method ra biến — mất `this`

```js
const phone = { brand: "iPhone", info() { return this.brand; } };
const getInfo = phone.info;
getInfo();  // undefined — this không còn là phone
```

### Bẫy 2: Nested object — `this` là object trực tiếp, không phải object ngoài

```js
const company = {
  name: "FPT",
  dept: {
    name: "JS Team",
    label() { return `${this.name} @ ${company.name}`; }
  }
};
company.dept.label();  // "JS Team @ FPT" — this = dept, NOT company
```

### Bẫy 3: Arrow function làm method — `this` sai

```js
const obj = {
  value: 42,
  getValue: () => this.value  // undefined — arrow kế thừa global this
};
obj.getValue();  // undefined, không phải 42
```

### Bẫy 4: Callback trong method mất context

```js
const scheduler = {
  name: " Scheduler",
  delay(fn) {
    setTimeout(fn, 10);  // fn chạy với default binding
  }
};
scheduler.delay(function() { console.log(this.name); }); // undefined
```

### Bẫy 5: Phương thức gọi qua prototype chain

```js
const parent = { who() { return "parent"; } };
const child = Object.create(parent);
child.who();  // "parent" — this = child, method tìm trên prototype
```

## 💡 Khi nào dùng — Tình huống thực tế

1. **Tạo object model** — `const user = { name, role, whoAmI() {...} }` — mỗi user có hành vi riêng.
2. **Form validation** — method `validate()` đọc `this.inputs` để kiểm tra.
3. **State management** — object có `state`, `setState()`, `getState()` truy cập bằng `this`.
4. **API client wrapper** — object `const api = { baseUrl, get(url) {...} }` dùng `this.baseUrl`.
5. **Component pattern (trước React)** — object đại diện component, method render DOM.
6. **Utility module** — object chứa các helper function dùng chung `this.config`.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Method cơ bản

```js
const phone = {
  name: "iPhone 15",
  color: "pink",
  take() {
    // this === phone — object đang gọi method
    console.log("this là:", this);
    console.log("Tên máy:", this.name);  // "iPhone 15"
    console.log("Màu:", this.color);     // "pink"
  }
};
phone.take();
```

### Ví dụ 2: Nested object — `this` đúng object trực tiếp

```js
const iPhone7 = {
  name: "iPhone 7",
  color: "pink",
  take() {
    console.log(this.name);   // "iPhone 7"
  },
  objChild: {
    name: "child-object",
    methodChild() {
      console.log(this.name); // "child-object" — this = objChild
    }
  }
};
iPhone7.take();              // "iPhone 7"
iPhone7.objChild.methodChild(); // "child-object"
```

### Ví dụ 3: Same method, different objects

```js
function describe() {
  return `Tên: ${this.name}, Giá: ${this.price} VNĐ`;
}

const course1 = { name: "HTML", price: 0 };
const course2 = { name: "React", price: 500000 };

course1.describe = describe;
course2.describe = describe;

console.log(course1.describe()); // "Tên: HTML, Giá: 0 VNĐ"
console.log(course2.describe()); // "Tên: React, Giá: 500000 VNĐ"
```

### Ví dụ 4: Method trên prototype (hiểu sâu hơn)

```js
function Course(name, price) {
  this.name = name;
  this.price = price;
}
// Method đặt trên prototype — tất cả instance dùng chung
Course.prototype.getInfo = function () {
  return `${this.name} — ${this.price}$`;
};

const js = new Course("JavaScript", 100);
const py = new Course("Python", 80);
console.log(js.getInfo()); // "JavaScript — 100$"
console.log(py.getInfo()); // "Python — 80$"
```

### Ví dụ 5: Mất context — bài tập tự sửa

```js
const blog = {
  title: "JS Basics",
  printTitle() {
    console.log(this.title);
  }
};

blog.printTitle();           // ✅ "JS Basics"
const fn = blog.printTitle;
fn();                        // ❌ undefined — this bị mất
// Sửa bằng bind:
fn.bind(blog)();             // ✅ "JS Basics"
// Sửa bằng arrow wrapper:
const safeFn = () => blog.printTitle();
safeFn();                    // ✅ "JS Basics"
```

## 🔬 So sánh với alternatives

| Cách tiếp cận | Ưu điểm | Nhược điểm |
|---------------|---------|------------|
| `obj.method()` implicit binding | Tự động, gọn, chuẩn | Dễ mất context nếu tách biến |
| `Function.prototype.call(obj)` | Ép this tường minh | Dài dòng hơn, không tự động |
| Arrow function method | Không bao giờ mất context | Không thể dùng làm method đúng nghĩa |
| `.bind(obj)` | Giữ context khi truyền callback | Tạo hàm mới, overhead nhẹ |

## 📊 Performance & Best Practices

- **Method trong object literal** được tạo lại mỗi lần khởi tạo object — nếu object tạo nhiều lần, method được copy nhiều lần. prefers prototype.
- **Method trên prototype** — chỉ tồn tại 1 bản, tất cả instance chia sẻ → tiết kiệm bộ nhớ.
- Luôn dùng **strict mode** để phát hiện sớm lỗi `this` mất context (trả về `undefined` thay vì `window`).
- Không bao giờ dùng arrow function làm method của object nếu cần `this` trỏ object.

## 🔗 Liên kết chéo

- **Xem thêm:** `10_this-keyword/02_in-function` — default binding khi tách method
- **Xem thêm:** `10_this-keyword/03_alone` — global `this` ở scope ngoài
- **Xem thêm:** `11_function-borrowing/01_bind` — cách sửa bằng `bind`
- **Xem thêm:** `14_classes/01_basics` — class kế thừa cơ chế method prototype
- **Xem thêm:** `02_data-types/02_objects-and-prototype/01_object-basics` — nền tảng object
