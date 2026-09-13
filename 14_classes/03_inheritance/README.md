# Classes — Kế thừa (Inheritance) với `extends`

## 🔑 Khái niệm

**`extends`** cho phép một class **kế thừa toàn bộ prototype** của class cha: subclass có đầy đủ phương thức/dữ liệu của cha, đồng thời có thể **ghi đè (override)** hoặc bổ sung của riêng mình.

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
    super.speak();      // gọi phương thức cha, phải qua super
    console.log(this.name + " barks");
  }
}
```

Những điểm cốt lõi:

- **`super.speak()`** gọi phiên bản method của class cha — giữ lại hành vi cha rồi thêm hành vi con.
- **`super()`** trong constructor gọi constructor của cha (xem bài constructor).
- Prototype chain sau khi extends: `dog → Dog.prototype → Animal.prototype → Object.prototype`.
- **`instanceof`** kiểm tra theo **chuỗi prototype**: `dog instanceof Dog` và `dog instanceof Animal` đều `true`. Kiểm tra được cả cấp prototype của class: `Dog.prototype instanceof Animal` → `true`.

## ✅ Điểm mạnh

- Tái sử dụng code cha, tránh lặp lại logic.
- Override linh hoạt: gọi `super` rồi thêm hành vi riêng.
- Mối quan hệ "is-a" (con là cha) kiểm tra được bằng `instanceof`.
- Phân cấp mô hình hóa tự nhiên: Animal → Dog → Puppy...

## ⚠️ Lưu ý / Hạn chế

- Constructor subclass **phải gọi `super()` trước `this`** — nếu không có constructor, JS tự ngầm gọi `super(...)` với toàn bộ đối số.
- Kế thừa nhiều tầng sâu gây khó đọc, khó bảo trì (ưu tiên composition).
- `instanceof` có thể trả `true` cho class "xa" hơn dự định — cần hiểu prototype chain.
- Method của class không tự bind — khi tách method ra callback vẫn mất `this`.

## 💡 Khi nào dùng

- Các loại đối tượng có chung gốc: Animal (Dog/Cat), Shape (Circle/Square)...
- Muốn mở rộng class có sẵn: thêm method, đổi hành vi speak.
- Tổ chức code nền tảng framework, base class dùng chung.

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
    super.speak();                       // Rex makes noise
    console.log(this.name + " barks");   // Rex barks
  }
}

const dog = new Dog("Rex");
dog.speak();
console.log(dog instanceof Dog);        // true
console.log(dog instanceof Animal);     // true (qua prototype chain)
console.log(Dog.prototype instanceof Animal); // true
```

## 📚 Tham khảo / Bài tập

- Chạy `03_inheritance/app.js` qua `index.html` hoặc `node app.js`: xem `super.speak()` gọi cha rồi con thêm "barks", và các dòng `instanceof`.
- Tự thử: viết `class Cat extends Animal` ghi đè `speak` thành "meows" có gọi `super`; sau đó viết `class Puppy extends Dog` và kiểm tra `puppy instanceof Animal`.