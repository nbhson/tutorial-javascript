# Classes — Khởi đầu (Basics)

## 🔑 Khái niệm

`class` là **syntactic sugar** của cơ chế **prototype**: những gì class viết gọn, phiên bản cũ phải viết bằng function constructor + `prototype` — cùng một bản chất.

So sánh:

```js
// Cách cũ: function constructor + prototype
function Course(name, price) {
  this.name = name;
  this.price = price;
}

// Cách mới: class
class Course {
  constructor(name, price) {
    this.name = name;
    this.price = price;
  }
  getName() {
    return this.name;
  }
}
```

Những điểm cốt lõi:

- **`constructor`** chạy khi `new` — khởi tạo dữ liệu của instance.
- **Phương thức khai báo trong class** được đặt trên `prototype` — mọi instance dùng chung, không tạo lại mỗi lần `new`.
- Vẫn có thể "núp" thêm method vào `Course.prototype` từ bên ngoài — chứng tỏ class không cô lập với prototype.
- `new Class(...)` tạo object mới, gọi constructor với `this = instance`.

## ✅ Điểm mạnh

- Code ngắn gọn, tổ chức rõ ràng hơn function constructor.
- Các method nằm trên `prototype` → tiết kiệm bộ nhớ, easy for fix chung.
- Quen thuộc với lập trình viên biết OOP từ ngôn ngữ khác.
- Tương thích với mọi thư viện/framework dùng `new`.

## ⚠️ Lưu ý / Hạn chế

- Class không được "hoisting" như function declaration — phải khai báo trước khi dùng.
- Thân class luôn chạy trong **strict mode**.
- Method của class không tự động bind `this` — mất context nếu gọi như `const f = instance.method; f()`.
- Vẫn cần hiểu prototype chain để khai fail (theo dõi `instanceof`, kế thừa).

## 💡 Khi nào dùng

- Tạo nhiều instance cùng cấu trúc: Course, User, Product...
- Gom dữ liệu + hành vi vào một "khuôn" dễ tái sử dụng.
- Nền tảng trước khi học `extends`, `static`, private fields.

## 🎯 Ví dụ minh họa

```js
class Course {
  constructor(name, price) {
    this.name = name;
    this.price = price;
  }
  getName() {
    return this.name;
  }
  getPrice() {
    return this.price;
  }
}

// Vẫn thao tác được với prototype — class chỉ là "đường cú pháp"
Course.prototype.info = function () {
  console.log(this.name + " " + this.price);
};

const c = new Course("HTML", "Free");
c.info(); // HTML Free
console.log(c.getName()); // HTML
```

## 📚 Tham khảo / Bài tập

- Chạy `01_basics/app.js` qua `index.html` hoặc `node app.js`: xem class `Course`, method trên prototype, và `Course.prototype.info` được thêm từ ngoài vẫn dùng được.
- Tự thử: bỏ comment phần function-constructor đầu file để so sánh cách viết cũ; sau đó thêm class `Video` với `duration` và method `getDuration()`.