# Các phương thức prototype

> Source: [https://javascript.info/prototype-methods](https://javascript.info/prototype-methods)

<!-- fetched: 2026-09-14 -->

Thuộc tính prototype của một hàm là một đối tượng được JavaScript sử dụng nội bộ để làm prototype cho các instances của hàm đó. Nó cũng có thể được sử dụng để thêm các phương thức chung cho tất cả các instances.

Tuy nhiên, cần phân biệt giữa việc sử dụng prototype để làm prototype và việc thêm các phương thức chung.

## [Sử dụng prototype để làm prototype](#using-prototype-as-prototype)

Khi một hàm được gọi với `new`, JavaScript tự động đặt prototype của hàm làm prototype của đối tượng được tạo ra.

```
function User(name) {
  this.name = name;
}

let user = new User("John");
alert(user.__proto__ === User.prototype); // true
```

Đây là cách chính để thiết lập mối quan hệ prototype giữa các đối tượng.

## [Thêm phương thức vào prototype](#adding-methods-to-prototype)

Chúng ta có thể thêm các phương thức vào `User.prototype`, và tất cả các instances của `User` sẽ có quyền truy cập vào chúng:

```
function User(name) {
  this.name = name;
}

User.prototype.sayHi = function() {
  alert(`Hello, ${this.name}!`);
};

let user = new User("John");
user.sayHi(); // Hello, John!
```

Điều này hoạt động vì `user.sayHi()` tìm thấy `sayHi` trong prototype của `user`, tức là `User.prototype`.

![](/article/prototype-methods/user-sayhi.svg)

Phương thức được gọi với `this=user`, vì vậy nó chạy mã với đối tượng hiện tại.

## [Prototype mặc định](#default-prototype)

Mỗi function đều có một thuộc tính `prototype` mặc định, ngay cả khi chúng ta không định nghĩa nó.

Đối với các function định nghĩa bằng cú pháp function declaration hoặc class, `prototype` là một đối tượng trống với `constructor` property trỏ ngược lại function đó.

```
function User() {}

alert(User.prototype); // [object Object], không có property nào để liệt kê
alert(User.prototype.constructor === User); // true
```

Đối với các arrow functions, `prototype` property không tồn tại:

```
let sayHi = () => alert("Hello");

alert(sayHi.prototype); // undefined
```

## [Thuộc tính constructor](#constructor-property)

Thuộc tính `constructor` trong `prototype` mặc định trỏ ngược lại function:

```
function User() {}

alert(User.prototype.constructor === User); // true
```

Chúng ta có thể sử dụng nó để khôi phục instance ban đầu:

```
let user = new User();
alert(user.constructor === user); // false (không phải là constructor)
alert(user.constructor === User); // true (đúng constructor)
```

## [Thay thế prototype](#replacing-prototype)

Nếu chúng ta thay thế toàn bộ `prototype`, thuộc tính `constructor` sẽ bị mất:

```
function User() {}

User.prototype = {}; // thay thế prototype

let user = new User("John");
alert(user.constructor); // undefined (không có trong {} theo prototype)
```

Chúng ta có thể khôi phục nó bằng cách sử dụng `Object.defineProperty`:

```
function User() {}

User.prototype = {};

// khôi phục
Object.defineProperty(User.prototype, "constructor", {
  value: User,
  writable: false,
  configurable: true,
  enumerable: true
});
```

## [Getter và Setter trong prototype](#getters-and-setters-in-prototype)

Prototype có thể chứa các getter và setter, không chỉ các phương thức thông thường:

```
function User(name) {
  this.name = name;
}

Object.defineProperty(User.prototype, "fullName", {
  get() {
    return `${this.name} ${this.surname}`;
  },
  set(value) {
    [this.name, this.surname] = value.split(" ");
  }
});

let user = new User("John");
user.surname = "Smith";
alert(user.fullName); // John Smith
```

## [Prototype của các built-in objects](#prototype-of-built-in-objects)

Tất cả các built-in objects trong JavaScript có prototype:

- `Object.prototype` – prototype cho tất cả các đối tượng.
- `Array.prototype` – prototype cho tất cả các mảng.
- `String.prototype` – prototype cho tất cả các chuỗi.
- `Number.prototype` – prototype cho tất cả các số.
- `Date.prototype` – prototype cho tất cả các ngày.
- `RegExp.prototype` – prototype cho tất cả các biểu thức regular.
- `Function.prototype` – prototype cho tất cả các hàm.

Chúng ta có thể thêm các phương thức vào các prototype này để thêm functionality chung:

```
// Thêm phương thức chung cho tất cả các chuỗi
String.prototype.reverse = function() {
  return this.split("").reverse().join("");
};

alert("abc".reverse()); // cba
```

Tuy nhiên, nên cẩn thận khi sửa đổi prototype của các built-in objects vì điều này có thể gây xung đột với các thư viện khác hoặc các phiên bản JavaScript mới.

## [Summary](#summary)

- `prototype` property của một function được sử dụng làm prototype cho các instances được tạo bởi `new`.
- Tất cả các function đều có `prototype` mặc định, trừ arrow functions.
- `prototype` mặc định có `constructor` property trỏ ngược lại function.
- Chúng ta có thể thêm các phương thức, getter và setter vào prototype.
- Chúng ta có thể thêm các phương thức vào các built-in prototype, nhưng nên cẩn thận.
