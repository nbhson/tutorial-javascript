# F.prototype

> Source: [https://javascript.info/function-prototype](https://javascript.info/function-prototype)

<!-- fetched: 2026-09-14 -->

Hãy xem xét vấn đề này.

Chúng ta có một hàm `sayHi` muốn sử dụng để thêm vào nhiều đối tượng.

Làm thế nào để viết hàm một lần và sử dụng cho nhiều đối tượng?

```
let user = {
  name: "John",
  surname: "Smith",
  sayHi: function() {
    alert(`Hello, ${this.name}!`);
  }
};

let admin = {
  name: "Admin"
};

// "Copy" the method into admin (making a shorter reference to it)
admin.sayHi = user.sayHi;

user.sayHi(); // Hello, John!    (same method references this.user)
admin.sayHi(); // Hello, Admin!  (same method references this.admin)
```

Hàm `sayHi` hoạt động khác nhau trong các đối tượng khác nhau vì nó sử dụng `this`.

Nhưng trong thực tế, chúng ta có thể có nhiều đối tượng hơn, và muốn có một phương thức `sayHi` chung. Vấn đề là làm thế nào để tránh "copy/paste" `sayHi` vào mỗi đối tượng? Đó là một cách mã hóa kém.

Nếu một phương thức thay đổi, chúng ta cần cập nhật bản sao của nó trong nhiều nơi.

Đó là nơi `F.prototype` đến giúp đỡ.

Hãy xem cú pháp để nó hoạt động:

```
function User(name) {
  this.name = name;
}

let user = new User("John");
```

Bạn có chắc rằng bạn hiểu dòng `let user = new User("John")` ở trên đang làm gì không? Để làm rõ hơn, chúng ta hãy chia nó thành các bước.

1. Khi một hàm được gọi với `new`, nó thực hiện bước khởi tạo. Nó chạy mã trong `constructor`, đặt `this.name = "John"` và trả về `this` như một đối tượng mới.
2. Nhưng trước khi điều đó xảy ra, JavaScript lấy `User.prototype` và đặt nó làm `[[Prototype]]` của `this`.

Vậy `new` thực hiện hai thứ:
- Gọi constructor, khởi tạo đối tượng.
- Thiết lập nguyên mẫu cho đối tượng.

Đó là ý tưởng!

Hãy hình dung cấu trúc:

![](/article/function-prototype/user-new-user.svg)

Như chúng ta có thể thấy, có hai quy tắc:
1. Khi `new User()` được gọi, JavaScript đặt `User.prototype` làm `[[Prototype]]` của đối tượng mới được tạo.
2. `User.prototype` lưu trữ một tham chiếu đến hàm `User` chính nó. Đó là một thuộc tính đặc biệt gọi là `constructor`.

Vì vậy, thông qua `[[Prototype]]`, các đối tượng mới có quyền truy cập vào các phương thức của constructor function và có thể sử dụng chúng.

## [Thuộc tính User.prototype.constructor](#user-prototype-constructor)

Hãy nhìn vào `User.prototype` nhiều hơn một chút.

Thuộc tính đó được tạo tự động bởi hàm constructor.

Nó trông như thế này:

```
function User(name) {
  this.name = name;
}
// prototype có "constructor" property bởi default
alert(User.prototype.constructor == User); // true
```

Sau đó, nếu chúng ta lấy `User.prototype`, JavaScript tự động sử dụng nó để khôi phục `constructor` property.

Thuộc tính `constructor` không thực sự hữu ích, nhưng khá ổn để có nó.

…Nhưng nếu chúng ta thay thế toàn bộ `User.prototype` theo cách thủ công, thì `constructor` property sẽ biến mất.

Ví dụ, toàn bộ sơ đồ trên sẽ bị phá hủy trong ví dụ sau:

```
function User(name) {
  this.name = name;
}
User.prototype = {}; // (*)

let user = new User("John");
alert(user.constructor); // undefined (không có trong {}, sau khi thay thế prototype)
```

Có thể khôi phục nó bằng cách sử dụng `Object.defineProperty`:

```
function User(name) {
  this.name = name;
}
User.prototype = {};

// khôi phục
Object.defineProperty(User.prototype, "constructor", {
  value: User,
  writable: false,
  configurable: true,
  enumerable: true
});
```

Nhưng thực sự thì, chúng ta không nên thay thế toàn bộ prototype theo cách thủ công. Chúng ta nên thêm các phương thức vào nó.

Và JavaScript cung cấp cách đó.

## [Thêm phương thức vào prototype](#adding-methods-to-prototype)

Cách an toàn nhất để thêm các phương thức vào prototype là thêm chúng vào `prototype` property.

Ví dụ, hãy thêm `sayHi` vào `User`:

```
function User(name) {
  this.name = name;
}

// thêm phương thức vào prototype
User.prototype.sayHi = function() {
  alert(`Hello, ${this.name}!`);
};

let user = new User("John");
user.sayHi(); // Hello, John!
```

Bây giờ `user.sayHi()` tìm thấy phương thức từ prototype.

![](/article/function-prototype/user-sayhi.svg)

Phương thức được gọi với `this=user`, vì vậy nó chạy mã với đối tượng hiện tại.

Có một sự nhầm lẫn phổ biến giữa các nhà phát triển mới bắt đầu. Họ đặt `sayHi` vào `User` thay vì `User.prototype`, vì vậy `User.sayHi()` hoạt động, nhưng `user.sayHi()` thì không.

Đừng quên: để thêm một phương thức vào tất cả các đối tượng được tạo bởi một constructor, chúng ta phải thêm nó vào prototype.

```
function User(name) {
  this.name = name;
  // ...đặt phương thức vào this, không phải User.prototype
  this.sayHi = function() {
    alert(`Hello, ${this.name}!`);
  };
}


let user = new User("John");
user.sayHi(); // Hello, John!
```

Ở đây `user.sayHi()` hoạt động, nhưng `User.sayHi()` không, bởi vì nó không có phương thức đó. Ngoài ra, mỗi đối tượng `user` sẽ có bản sao riêng của `sayHi`, tiêu tốn bộ nhớ.

## [Nguyên mẫu mặc định](#default-prototype)

Một hàm constructor, được định nghĩa bằng cú pháp hàm hoặc lớp, có thuộc tính `prototype` theo mặc định.

Nhưng nếu một hàm không có `prototype` property, thì `new` sẽ ném lỗi.

```
function User() {};

alert(User.prototype); // undefined, prototype property mặc định là undefined

new User(); // Error
```

…Nhưng trong thực tế, hầu hết các hàm đều có `prototype`.

Giá trị `prototype` mặc định là một đối tượng trống với `constructor` property trỏ ngược lại hàm constructor.

JavaScript thêm `constructor` property vào prototype với các thuộc tính sau:
- `value`: cùng giá trị với hàm (tự tham chiếu)
- `writable`: `false`
- `configurable`: `false`
- `enumerable`: `false`

Điều này đảm bảo rằng khi chúng ta lặp qua một đối tượng bằng `for..in`, các property không cần thiết không xuất hiện.

```
function User() {}

alert(User.prototype); // [object Object], không có property nào để liệt kê
alert(User.prototype.constructor.name); // User
```

Chúng ta cũng có thể thêm các phương thức vào prototype mặc định. Ví dụ, dưới đây `User.prototype` được mở rộng với `sayHi`:

```
function User(name) {
  this.name = name;
}

// tất cả các hàm đều có cùng một prototype mặc định, thêm vào nó
User.prototype.sayHi = function() {
  alert(`Hello, ${this.name}!`);
};

let user = new User("John");
user.sayHi(); // Hello, John!
```

Điều gì xảy ra nếu chúng ta đặt một thuộc tính `prototype`?

```
function User() {};

User.prototype = {
  sayHi() { alert(`Hello, ${this.name}!`); }
};

let user = new User("John");
user.sayHi(); // Hello, John!
```

Đó là cú pháp thay thế, tương đương với ví dụ trước đó.

Nhưng một cái khác biệt ở đây: thuộc tính `constructor` bị mất.

```
function User() {};

User.prototype = {
  sayHi() { alert(`Hello, ${this.name}!`); }
};

alert(new User().constructor); // Object (đó là giá trị mặc định cho objects trong {} theo prototype)
```

Nếu chúng ta đang thêm các phương thức vào prototype mặc định thì không sao, bởi vì `constructor` property vẫn tồn tại và có thể truy cập được. Nhưng nếu chúng ta thay thế toàn bộ prototype, thì chúng ta nên khôi phục `constructor` property, nếu không nó sẽ bị mất.

Nói một cách chính xác, nó sẽ vẫn tồn tại trong prototype của prototype:

```
function User() {};

User.prototype = {
  sayHi() { alert(`Hello, ${this.name}!`); }
};

alert(Object.getPrototypeOf(new User()) === User.prototype); // true
alert(User.prototype.constructor === Object.prototype); // true (constructor property bị mất)
```

Nhưng giá trị của nó là `Object`, không phải `User`. Vì vậy, tốt hơn là giữ nó, bằng cách sử dụng cú pháp object shorthand hoặc `Object.defineProperty`.

Cú pháp object shorthand, `{sayHi() {…}}`, tạo property `constructor` với các flag thích hợp, như được mô tả trong chương [Thuộc tính đối tượng](/object-methods), vì vậy chúng ta không cần phải làm gì thêm:

```
function User() {};

// cú pháp shorthand hoạt động tốt
User.prototype = {
  sayHi() { alert(`Hello, ${this.name}!`); }
};

alert(Object.getPrototypeOf(new User()) === User.prototype); // true
alert(new User().constructor === User); // true
```

## [Object.prototype mặc định](#default-object-prototype)

Hãy xem xét điều gì xảy ra nếu một hàm constructor không có `prototype` property:

```
function User() {};

// prototype mặc định là undefined
alert(User.prototype); // undefined, như được quy định trong spec

let user = new User("John");
alert(user.__proto__); // ?
```

Theo đặc tả, nếu một hàm constructor không có `prototype`, thì một đối tượng mặc định được sử dụng làm prototype cho đối tượng được tạo bằng `new`.

Đối tượng mặc định đó chỉ có một `constructor` property trỏ ngược lại hàm `Function`, vì vậy tất cả các đối tượng đều kế thừa từ nó.

```
function User() {};

let user = new User("John");
alert(user.__proto__ == Function.prototype); // true, như được quy định trong spec
alert(user.constructor === Function.prototype.constructor); // true
```

Đó là một cơ chế đặc biệt để đảm bảo rằng mọi người dùng đều có quyền truy cập vào các phương thức đối tượng mặc định.

Tương tự như vậy, nếu prototype là một giá trị nguyên thủy, nó bị bỏ qua:

```
function User() {};
User.prototype = 1; // prototype là giá trị nguyên thủy

let user = new User("John");
alert(user.__proto__ == Function.prototype); // true (giá trị mặc định)
```

## [Getter/Setter trong prototype](#gettersetters-in-prototype)

Prototype có thể chứa không chỉ các phương thức, mà còn cả các thuộc tính getter/setter.

Mã sử dụng chúng sẽ hoạt động tốt:

```
// User.prototype có getter/setter
let user = {
  name: "John",
  surname: "Smith",

  get fullName() {
    return `${this.name} ${this.surname}`;
  }
};

alert(user.fullName); // John Smith
```

Đôi khi các thuộc tính getter/setter như vậy có thể hữu ích để triển khai các thuộc tính đối tượng bổ sung.

Ví dụ, để cung cấp thuộc tính `fullName` cho `user`:

```
function User(name) {
  this.name = name;
}

// định nghĩa getter
User.prototype.fullName = {

  get() {
    return `${this.name} ${this.surname}`;
  }
};

let user = new User("John");
alert(user.fullName); // John Smith
```

## [Summary](#summary)

- Tất cả các hàm constructor built-in, như `Object`, `Array`, `RegExp`, `String`, v.v., có `prototype` property.
- `prototype` property chỉ được sử dụng khi `new Func()` được gọi. Đối tượng được tạo với `new Func()` có `[[Prototype]]` là `Func.prototype`.
- Nếu `Func.prototype` là một giá trị nguyên thủy, thì giá trị mặc định là một đối tượng với `constructor` property trỏ ngược lại `Func` sẽ được sử dụng làm prototype.
- Các phương thức prototype được chia sẻ bởi tất cả các đối tượng được tạo bởi constructor.
- Khi chúng ta thêm một phương thức vào prototype, nó trở nên sẵn có cho tất cả các đối tượng hiện có.
