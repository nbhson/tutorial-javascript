# Classes trong JavaScript

## 🔑 Khái niệm

**Class** là cú pháp (ES6) để tạo **khuôn mẫu (blueprint)** sinh ra các object giống nhau. Quan trọng: class trong JS chỉ là **syntactic sugar** trên nền **prototype** — bản chất vẫn là function constructor + prototype chain, chỉ được viết gọn và rõ ràng hơn.

```js
class Course {
  constructor(name, price) {
    this.name = name;
    this.price = price;
  }
  getName() {
    return this.name;
  }
}
const c = new Course("JS", 100);
```

Các thành phần của class:

- **`constructor()`** — hàm khởi tạo, tự chạy khi `new`.
- **Phương thức (methods)** — định nghĩa trên `prototype`, dùng chung cho mọi instance.
- **`extends`** — kế thừa lớp cha, đi cùng `super()`.
- **`static`** — thuộc tính/phương thức gắn với class, không phải instance.
- **`#field`** — thuộc tính **private** (ES2022), chỉ truy cập bên trong class.

## ✅ Điểm mạnh

- Cú pháp sạch, dễ đọc so với function constructor + prototype thủ công.
- Kế thừa bằng `extends` + `super()` rõ ràng như các ngôn ngữ khác.
- Đóng gói dữ liệu với private field `#`.
- `instanceof` kiểm tra quan hệ kế thừa dễ dàng.
- Nền tảng để làm việc với framework (React class component, Angular, OOP).

## ⚠️ Lưu ý / Hạn chế

- Không phải "class" như Java/C++ — vẫn là prototype + hàm ở nền.
- Trong subclass, **`super()` phải gọi trước** khi dùng `this` — ngược lại báo lỗi.
- Method của class không tự bind `this` — mất context khi tách ra làm callback.
- Máy các quy tắc `this` vẫn áp dụng đầy đủ (implicit/new binding...).

## 💡 Khi nào dùng

- Mô hình hóa đối tượng có dữ liệu + hành vi: User, Product, Order...
- Cần kế thừa và tái sử dụng code giữa các "loại" đối tượng.
- Viết code hướng đối tượng trong frontend/backend Node.js.

## 🎯 Ví dụ minh họa

```js
class Animal {
  constructor(name) {
    this.name = name;
  }
  speak() {
    console.log(this.name + " makes noise");
  }
}
class Dog extends Animal {
  speak() {
    super.speak();          // gọi phương thức cha
    console.log(this.name + " barks");
  }
}
new Dog("Rex").speak();
// Rex makes noise
// Rex barks
```

## 📚 Tham khảo / Bài tập

- Nhóm này gồm: `01_basics`, `02_constructor`, `03_inheritance`, `04_static-private` — đọc theo thứ tự.
- Mỗi folder có `app.js` + `index.html`; chạy và quan sát console.
- Tự thử: tạo class `Car` (name, color, price) với method `info()` và một subclass kế thừa nó.