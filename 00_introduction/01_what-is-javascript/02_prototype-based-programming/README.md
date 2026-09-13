# Prototype-based Programming

## 🔑 Khái niệm

**Prototype-based programming** là một phong cách **lập trình hướng đối tượng** trong đó **không có khái niệm "class" được định nghĩa tường minh**. Thay vì định nghĩa blueprint (khuôn mẫu) rồi tạo đối tượng từ nó, JavaScript cho phép:

- Tạo đối tượng **trực tiếp** từ đối tượng rỗng hoặc literal `{}`.
- Một đối tượng mới **kế thừa** từ một đối tượng có sẵn (gọi là *prototype*) qua cơ chế **prototype chain**.
- Thêm/sửa thuộc tính và phương thức **bất cứ lúc nào** (dynamic).

Nói đơn giản: JS tiến hành kế thừa bằng cách **liên kết đối tượng với đối tượng**, không phải bằng cách khai báo lớp trước. Nhờ vậy khi thêm một thuộc tính vào prototype, **mọi đối tượng thừa kế từ nó đều lập tức thấy** thuộc tính mới.

**Cách hoạt động khi truy cập `obj.thuocTinh`:**

1. JS tìm trong chính `obj` — nếu có thì dừng.
2. Nếu không, đi theo `__proto__` / `Object.getPrototypeOf(obj)` lên prototype.
3. Lặp tiếp lên hết chuỗi prototype, gặp `null` thì trả về `undefined`.

Các cơ chế tạo đối tượng chính:

- `const obj = {}` — object literal.
- `Object.create(proto)` — tạo đối tượng kế thừa trực tiếp từ `proto`.
- Constructor function: `function Person() {}` + `new Person()` (phương thức gắn qua `Person.prototype.sayHello = ...`).
- (ES6 có cú pháp `class` nhưng bản chất bên trong vẫn là prototype — thuần syntactic sugar.)

## ✅ Điểm mạnh

- **Linh hoạt / dynamic**: thêm, sửa, xóa thuộc tính bất cứ lúc nào mà không cần biên dịch lại.
- **Tái sử dụng qua prototype chain**: một phương thức đặt trên prototype dùng chung cho hàng nghìn đối tượng, tiết kiệm bộ nhớ.
- **Không cần boilerplate**: không bắt buộc định nghĩa class trước khi tạo object.
- **Mở rộng dần**: trái ngược class cứng nhắc, ta có thể mở rộng đối tượng tại runtime.
- **Kế thừa thay đổi đồng bộ**: sửa ở prototype, tất cả con cháu thấy ngay.

## ⚠️ Lưu ý / Hạn chế

- `Object.create(null)` tạo đối tượng **không có** prototype — sẽ không có `toString`, `hasOwnProperty`, v.v.
- Ghi đè lên `Array.prototype`, `Object.prototype` của mọi đối tượng là **việc xấu** (monkey-patching global có thể phá code khác).
- Khó truy vết hơn class truyền thống; nhiều team chọn viết `class` ES6 để rõ ràng hơn (dù bản chất vẫn là prototype).
- Tính dynamic có thể khiến lỗi chỉ xuất hiện ở runtime, khó nắm được "kiểu" của đối tượng từ trước.

## 💡 Khi nào dùng

- Tạo họ đối tượng chia sẻ hành vi chung (ví dụ: động vật, phương tiện) mà không cần class.
- Define polyfill / thêm tiện ích vào thư viện (một cách cẩn thận).
- Kế thừa từ đối tượng model có sẵn (ORM, mô hình dữ liệu).
- Hiểu cách `class` ES6 hoạt động "bên trong" để debug lỗi prototype chain.

## 🎯 Ví dụ minh họa

```js
// 1. Tạo đối tượng từ đối tượng rỗng
const person = {};
person.name = "Nguyễn Văn A";
person.sayHello = function () {
  console.log(`Xin chào, tôi là ${this.name}`);
};
person.sayHello(); // Xin chào, tôi là Nguyễn Văn A

// 2. Tạo đối tượng từ đối tượng khác (Object.create)
const animal = { makeSound() { console.log("Some sound"); } };
const dog = Object.create(animal);
dog.makeSound = () => console.log("Woof! Woof!");
dog.makeSound(); // Woof! Woof!

// 3. Constructor function + prototype
function Person2(name, age) {
  this.name = name;
  this.age = age;
}
Person2.prototype.haveBirthday = function () {
  this.age++;
  console.log(`Giờ tôi ${this.age} tuổi`);
};
const p = new Person2("Trần Thị B", 30);
p.haveBirthday(); // Giờ tôi 31 tuổi
```

## 📚 Tham khảo / Bài tập

- Nhóm này **chưa có file `app.js`** — bạn có thể chạy trực tiếp các ví dụ trên trong DevTools (F12 → Console).
- Tự thử: tạo object `vehicle` với phương thức `start()`, dùng `Object.create` để tạo `car` và `motorcycle`; kiểm tra chuỗi prototype bằng `Object.getPrototypeOf(car)`, `car instanceof Object`.
- Liên hệ: `02_data-types/02_objects-and-prototype/` sẽ nghiên cứu kỹ hơn về object và prototype chain.