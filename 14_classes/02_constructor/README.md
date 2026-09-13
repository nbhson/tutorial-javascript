# Classes — Constructor

## 🔑 Khái niệm

**`constructor`** là hàm khởi tạo của class — **mỗi class chỉ có một**. Khi bạn gọi `new User(...)`:

1. Tạo object mới (instance).
2. Gọi `constructor` với `this` = instance đó.
3. Instance được gán các thuộc tính (qua `this.name = ...`).
4. Trả về instance.

```js
class User {
  constructor(name, age) {
    this.name = name;
    this.age = age;
  }
}
const u = new User("An", 20);
console.log(u); // User { name: "An", age: 20 }
```

Quy tắc với **subclass**:

- Subclass **phải gọi `super(...)`** ở đầu constructor — **trước khi dùng `this`** — nếu không sẽ báo lỗi.
- `super(...)` chạy constructor của lớp cha, khởi tạo phần dữ liệu cha trước, sau đó subclass mới khởi tạo phần riêng.

## ✅ Điểm mạnh

- Khởi tạo dữ liệu instance ngay, rõ ràng và nhất quán.
- Bắt buộc quy trình cha → con qua `super()` tránh quên khởi tạo class cha.
- Cú pháp một lần `new` gọn gàng so với function constructor.
- Dễ thêm logic mặc định (ép kiểu, giá trị fallback) ngay khi tạo.

## ⚠️ Lưu ý / Hạn chế

- Chỉ **một** constructor — không overload như các ngôn ngữ khác.
- Quên `super()` trong subclass → `ReferenceError` khi dùng `this`.
- Gọi `super()` sau khi dùng `this` cũng bị lỗi cú pháp.
- Constructor không trả về object tùy biến thường xuyên — chỉ set state và thôi.

## 💡 Khi nào dùng

- Tạo instance cần tham số đầu vào (name, age, price...).
- Chuẩn hóa dữ liệu đầu vào khi khởi tạo (trim, number, default...).
- Subclass cần khởi tạo lớp cha rồi mới thêm thuộc tính riêng.

## 🎯 Ví dụ minh họa

```js
class User {
  constructor(name, age) {
    this.name = name;
    this.age = age;
  }
}

// Subclass phải gọi super() trước khi dùng this
class Admin extends User {
  constructor(name, age, role) {
    super(name, age);   // khởi tạo User trước
    this.role = role;   // sau đó mới dùng this
  }
}

const u = new User("An", 20);
console.log(u);                     // User { name: "An", age: 20 }
console.log(new Admin("B", 25, "admin")); // Admin { name: "B", age: 25, role: "admin" }
```

## 📚 Tham khảo / Bài tập

- Chạy `02_constructor/app.js` qua `index.html` hoặc `node app.js`: xem `constructor` chạy khi `new` (log "constructor An") và `super()` trong `Admin`.
- Tự thử: trong `Admin`, đặt `this.role = role;` **trước** `super(name, age)` — chạy lại và đọc lỗi để hiểu vì sao phải gọi `super` trước.