# Object Basics (Cơ bản về Object)

## 🔑 Khái niệm

**Object** là một "hộp" chứa các cặp **khóa (key) – giá trị (value)**, gọi chung là **property**; nếu giá trị là hàm thì gọi là **method**. Object là nền tảng của JavaScript — học object là học "đơn vị dữ liệu cơ bản" của ngôn ngữ.

**Tạo object literal và truy cập thuộc tính:**

```js
var myInfo = {
  name: "Sơn",
  age: 23,
  sex: 1,
  getFullName: function () {
    return `${this.name} Nguyễn`; // method — dùng this để trỏ chính object
  },
};

console.log(myInfo.name);      // "Sơn" — chấm
console.log(myInfo["name"]);   // "Sơn" — cú pháp ngoặc vuông
```

Cú pháp ngoặc vuông đặc biệt hữu ích khi khóa được lưu trong biến:

```js
var myKey = "email";
console.log(myInfo[myKey]);    // giá trị của thuộc tính "email"
```

**Thêm / xóa thuộc tính bất cứ lúc nào (tính động của object):**

```js
myInfo.email = "nbhson43@gmail.com";  // Thêm mới
delete myInfo.sex;                    // Xóa
console.log(myInfo);
```

**Object constructor (hàm tạo)** — dùng từ khóa `new` để tạo nhiều instance cùng "khuôn":

```js
function User(firstName, lastName, avatar) {
  this.firstName = firstName;   // this trỏ đến object vừa tạo
  this.lastName = lastName;
  this.avatar = avatar;
  this.getFullName = function () {
    return `${this.firstName} ${this.lastName}`;
  };
}

var teacher = new User("Sơn", "Đặng", "avatar_1");
var student = new User("Sơn", "Nguyễn", "avatar_1");

teacher.luong = "10.000.000đ";   // tv của riêng teacher
student.title = "Học sinh giỏi"; // của riêng student
console.log(teacher.getFullName()); // Sơn Đặng
console.log(student.getFullName()); // Sơn Nguyễn
```

**Prototype** — để **dùng chung** thuộc tính/phương thức thay vì lặp lại trong từng instance:

```js
User.prototype.className = "F8";
User.prototype.getFullName = function () {
  return `${this.firstName} ${this.lastName}`;
};

var student = new User("Sơn", "Nguyễn", "avatar_1");
console.log(student.className);       // "F8" (cả class chung)
console.log(student.getFullName());   // "Sơn Nguyễn"
```

> Nguyên tắc: mọi object (trừ `null`/`undefined`) đều có **prototype riêng** định nghĩa thuộc tính/phương thức mặc định của nó. Thuộc tính/phương thức nằm trong **chính object** thì đó thuộc "instance"; đặt trên `prototype` thì dùng chung cho tất cả instance — và **không thể `delete`** từ từng instance.

Phần cuối của `3_object_prototype.js` minh họa **kế thừa qua prototype**: gán `Superman.prototype = new Person()` để Superman "học" được các phương thức của Person; khi truy cập thuộc tính JS tìm trong instance trước, không có mới lần lên chuỗi prototype.

## ✅ Điểm mạnh

- Object linh hoạt: thêm/sửa/xóa property bất cứ lúc nào.
- **Constructor function** tái sử dụng "khuôn" tạo nhiều object cùng shape.
- **Prototype** dùng chung phương thức → tiết kiệm bộ nhớ và dễ mở rộng.
- Truy cập bằng cả dấu chấm lẫn ngoặc vuông (khóa động trong biến).
- `delete`, `Object.assign`, spread giúp thao tác object nhanh gọn.

## ⚠️ Lưu ý / Hạn chế

- `delete` không xóa được property nằm trong **prototype** (chỉ property riêng của instance).
- Nếu `this` không được ràng buộc, method có thể mất ngữ cảnh (gọi `getFullName()` đơn thuần → `this` là global/undefined).
- Constructor function gọi **thiếu `new`** sẽ gán vào global — luôn dùng `new` hoặc class ES6.
- Truy cập key xấu (`name` có khoảng trắng/hyphen) bắt buộc dùng `["..."]`.

## 💡 Khi nào dùng

- Nhóm dữ liệu logic với nhau (thông tin người dùng, sản phẩm, cấu hình...).
- Tạo nhiều đối tượng cùng cấu trúc → constructor function (hoặc class ES6).
- Chia sẻ một hành vi cho tất cả instance → `Prototype.method`.

## 🎯 Ví dụ minh họa

```js
var myInfo = {
  name: "Sơn",
  age: 23,
  getFullName: function () {
    return `${this.name} Nguyễn`;
  },
};
myInfo.email = "nbhson43@gmail.com";   // thêm
console.log(myInfo["name"], myInfo.email); // Sơn nbhson43@gmail.com

var key = "email";
console.log(myInfo[key]);              // nbhson43@gmail.com

delete myInfo.age;                     // xóa
console.log(myInfo.getFullName());     // Sơn Nguyễn
```

## 📚 Tham khảo / Bài tập

- Chạy lần lượt `1_object.js` → `2_object_constructor.js` → `3_object_prototype.js` bằng `node` (hoặc mở `index.html` và quan sát Console):
  - `1_object.js`: object literal, thêm/xóa property, truy cập bằng key biến, method `getFullName`.
  - `2_object_constructor.js`: `new User(...)`, mỗi instance có property riêng.
  - `3_object_prototype.js`: `User.prototype.className/getFullName`, kế thừa `Superman.prototype = new Person()`.
- Tự thử: 1) tạo object `car` với `brand`, `speed`, method `run()` in `"Xe chạy với tốc độ ...km/h"`; 2) thêm method `car.save()`, sau đó `delete` thử property được lưu trong prototype và giải thích kết quả.
- Tài liệu: [MDN — Objects](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Working_with_Objects), [javascript.info/object](https://javascript.info/object).