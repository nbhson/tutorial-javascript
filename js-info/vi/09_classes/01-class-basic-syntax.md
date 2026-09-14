# Cú pháp cơ bản của Class

> Nguồn: [https://javascript.info/class](https://javascript.info/class)

<!-- fetched: 2026-09-14 -->

> Trong lập trình hướng đối tượng, một *class* là một khuôn mẫu mã chương trình có thể mở rộng để tạo ra các đối tượng, cung cấp giá trị khởi tạo cho trạng thái (các thuộc tính thành viên) và triển khai hành vi (các hàm thành viên hoặc phương thức).
>
> Wikipedia

Trong thực tế, chúng ta thường cần tạo nhiều đối tượng cùng loại, như users, hoặc goods, hay bất cứ thứ gì.

Như chúng ta đã biết từ chương [Constructor, toán tử "new"](/constructor-new), `new function` có thể giúp được việc đó.

Nhưng trong JavaScript hiện đại, có một construct "class" tiên tiến hơn, giới thiệu nhiều tính năng mới hữu ích cho lập trình hướng đối tượng.

## [Cú pháp "class"]( #cú-pháp-class)

Cú pháp cơ bản là:

```
class MyClass {
  // các phương thức class
  constructor() { ... }
  method1() { ... }
  method2() { ... }
  method3() { ... }
  ...
}
```

Sau đó dùng `new MyClass()` để tạo một đối tượng mới với tất cả các phương thức đã liệt kê.

Phương thức `constructor()` được gọi tự động bởi `new`, vì vậy chúng ta có thể khởi tạo đối tượng ở đó.

Ví dụ:

```
class User {

  constructor(name) {
    this.name = name;
  }

  sayHi() {
    alert(this.name);
  }

}

// Usage:
let user = new User("John");
user.sayHi();
```

Khi `new User("John")` được gọi:

1. Một đối tượng mới được tạo.
2. `constructor` chạy với đối số đã cho và gán nó cho `this.name`.

...Sau đó chúng ta có thể gọi các phương thức đối tượng, như `user.sayHi()`.

Không có dấu phẩy giữa các phương thức class

Một lỗi phổ biến của người mới là đặt dấu phẩy giữa các phương thức class, điều đó sẽ gây ra lỗi cú pháp.

Ký hiệu ở đây không nên nhầm lẫn với object literals. Trong class, không cần dấu phẩy.

## [Class là gì?](#class-la-gi)

Vậy chính xác thì `class` là gì? Đó không phải là một thực thể hoàn toàn mới ở cấp ngôn ngữ, như nhiều người có thể nghĩ.

Hãy bóc tách mọi phép màu và xem class thực sự là gì. Điều đó sẽ giúp hiểu nhiều khía cạnh phức tạp.

Trong JavaScript, một class là một dạng hàm.

Hãy xem:

```
class User {
  constructor(name) { this.name = name; }
  sayHi() { alert(this.name); }
}

// proof: User is a function
alert(typeof User); // function
```

Construct `class User {...}` thực sự làm những gì:

1. Tạo một hàm có tên `User`, trở thành kết quả của khai báo class. Mã hàm được lấy từ phương thức `constructor` (giả sử trống nếu chúng ta không viết phương thức đó).
2. Lưu trữ các phương thức class, như `sayHi`, trong `User.prototype`.

Sau khi đối tượng `new User` được tạo, khi chúng ta gọi phương thức của nó, nó được lấy từ prototype, như đã mô tả trong chương [F.prototype](/function-prototype). Vì vậy đối tượng có quyền truy cập vào các phương thức class.

Chúng ta có thể minh họa kết quả của khai báo `class User` như sau:

![](/article/class/class-user.svg)

Đây là mã để introspect nó:

```
class User {
  constructor(name) { this.name = name; }
  sayHi() { alert(this.name); }
}

// class is a function
alert(typeof User); // function

// ...hoặc chính xác hơn, là phương thức constructor
alert(User === User.prototype.constructor); // true

// Các phương thức nằm trong User.prototype, ví dụ:
alert(User.prototype.sayHi); // mã của phương thức sayHi

// chỉ có chính xác hai phương thức trong prototype
alert(Object.getOwnPropertyNames(User.prototype)); // constructor, sayHi
```

## [Không chỉ là syntactic sugar](#khong-chi-la-syntactic-sugar)

Đôi khi người ta nói rằng `class` là một "syntactic sugar" (cú pháp được thiết kế để dễ đọc hơn, nhưng không giới thiệu gì mới), vì trên thực tế chúng ta có thể khai báo cùng thứ mà không cần dùng từ khóa `class` whatsoever:

```
// rewriting class User in pure functions

// 1. Create constructor function
function User(name) {
  this.name = name;
}
// a function prototype has "constructor" property by default,
// so we don't need to create it

// 2. Add the method to prototype
User.prototype.sayHi = function() {
  alert(this.name);
};

// Usage:
let user = new User("John");
user.sayHi();
```

Kết quả của định nghĩa này tương tự nhau. Vì vậy, có lý do chính đáng để coi `class` là syntactic sugar để định nghĩa một constructor cùng với các phương thức prototype của nó.

Tuy nhiên, vẫn có những khác biệt quan trọng.

1. Đầu tiên, một hàm được tạo bởi `class` được dán nhãn bằng thuộc tính nội bộ đặc biệt `[[IsClassConstructor]]: true`. Vì vậy nó không hoàn toàn giống như tạo thủ công.

   Ngôn ngữ kiểm tra thuộc tính đó ở nhiều nơi. Ví dụ, khác với hàm thông thường, nó phải được gọi với `new`:

   ```
   class User {
     constructor() {}
   }

   alert(typeof User); // function
   User(); // Error: Class constructor User cannot be invoked without 'new'
   ```

   Ngoài ra, biểu diễn chuỗi của constructor class trong hầu hết các engine JavaScript bắt đầu bằng "class..."

   ```
   class User {
     constructor() {}
   }

   alert(User); // class User { ... }
   ```

   Có những khác biệt khác nữa, chúng ta sẽ thấy chúng sớm.
2. Các phương thức class là non-enumerable.
   Một định nghĩa class đặt cờ `enumerable` thành `false` cho tất cả các phương thức trong `"prototype"`.

   Điều đó tốt, vì nếu chúng ta `for..in` trên một đối tượng, chúng ta thường không muốn các phương thức class của nó.
3. Classes luôn `use strict`.
   Tất cả mã bên trong construct class tự động ở chế độ strict.

Ngoài ra, cú pháp `class` mang lại nhiều tính năng khác mà chúng ta sẽ khám phá sau.

## [Biểu thức Class](#class-expression)

Giống như functions, classes có thể được định nghĩa bên trong một expression khác, được truyền qua, trả về, gán, v.v.

Đây là một ví dụ về biểu thức class:

```
let User = class {
  sayHi() {
    alert("Hello");
  }
};
```

Tương tự như Named Function Expressions, các biểu thức class có thể có tên.

Nếu một class expression có tên, nó chỉ hiển thị bên trong class:

```
// "Named Class Expression"
// (no such term in the spec, but that's similar to Named Function Expression)
let User = class MyClass {
  sayHi() {
    alert(MyClass); // MyClass name is visible only inside the class
  }
};

new User().sayHi(); // works, shows MyClass definition

alert(MyClass); // error, MyClass name isn't visible outside of the class
```

Chúng ta thậm chí có thể tạo các class động "theo yêu cầu", như sau:

```
function makeClass(phrase) {
  // declare a class and return it
  return class {
    sayHi() {
      alert(phrase);
    }
  };
}

// Create a new class
let User = makeClass("Hello");

new User().sayHi(); // Hello
```

## [Getter/Setter](#getters-setters)

Giống như literal objects, classes có thể bao gồm getter/setter, computed properties, v.v.

Đây là một ví dụ cho `user.name` được triển khai bằng `get/set`:

```
class User {

  constructor(name) {
    // invokes the setter
    this.name = name;
  }

  get name() {
    return this._name;
  }

  set name(value) {
    if (value.length < 4) {
      alert("Name is too short.");
      return;
    }
    this._name = value;
  }

}

let user = new User("John");
alert(user.name); // John

user = new User(""); // Name is too short.
```

Về mặt kỹ thuật, khai báo class như vậy hoạt động bằng cách tạo getters và setters trong `User.prototype`.

## [Tên tính toán […]](#computed-names)

Đây là một ví dụ với tên phương thức computed sử dụng brackets `[...]`:

```
class User {

  ['say' + 'Hi']() {
    alert("Hello");
  }

}

new User().sayHi();
```

Các tính năng như vậy dễ nhớ, vì chúng giống với của literal objects.

## [Các trường Class](#class-fields)

Các browser cũ có thể cần polyfill

Các trường class là một bổ sung gần đây cho ngôn ngữ.

Trước đây, các class của chúng ta chỉ có methods.

"Các trường class" là một cú pháp cho phép thêm bất kỳ properties nào.

Ví dụ, hãy thêm property `name` vào `class User`:

```
class User {
  name = "John";

  sayHi() {
    alert(`Hello, ${this.name}!`);
  }
}

new User().sayHi(); // Hello, John!
```

Vì vậy, chúng ta chỉ viết "= " trong declaration, và thế là xong.

Sự khác biệt quan trọng của class fields là chúng được đặt trên từng object, không phải `User.prototype`:

```
class User {
  name = "John";
}

let user = new User();
alert(user.name); // John
alert(User.prototype.name); // undefined
```

Chúng ta cũng có thể gán các giá trị bằng các expressions và function calls phức tạp hơn:

```
class User {
  name = prompt("Name, please?", "John");
}

let user = new User();
alert(user.name); // John
```

### [Tạo bound methods với class fields](#making-bound-methods-with-class-fields)

Như đã minh họa trong chương [Function binding](/bind), functions trong JavaScript có `this` động. Nó phụ thuộc vào ngữ cảnh của lời gọi.

Vì vậy, nếu một object method được truyền đi và được gọi trong một ngữ cảnh khác, `this` sẽ không còn là reference đến object của nó nữa.

Ví dụ, mã này sẽ hiển thị `undefined`:

```
class Button {
  constructor(value) {
    this.value = value;
  }

  click() {
    alert(this.value);
  }
}

let button = new Button("hello");

setTimeout(button.click, 1000); // undefined
```

Vấn đề được gọi là "losing `this`".

Có hai cách tiếp cận để khắc phục nó, như đã thảo luận trong chương [Function binding](/bind):

1. Truyền một wrapper-function, như `setTimeout(() => button.click(), 1000)`.
2. Bind method vào object, ví dụ trong constructor.

Class fields cung cấp một cú pháp khác, khá thanh lịch:

```
class Button {
  constructor(value) {
    this.value = value;
  }
  click = () => {
    alert(this.value);
  }
}

let button = new Button("hello");

setTimeout(button.click, 1000); // hello
```

Class field `click = () => {...}` được tạo trên cơ sở từng object, có một function riêng cho mỗi đối tượng `Button`, với `this` bên trong nó reference đến object đó. Chúng ta có thể truyền `button.click` đi khắp nơi, và giá trị của `this` sẽ luôn đúng.

Điều đó đặc biệt hữu ích trong môi trường browser, cho event listeners.

## [Tóm tắt](#summary)

Cú pháp class cơ bản trông như thế này:

```
class MyClass {
  prop = value; // property

  constructor(...) { // constructor
    // ...
  }

  method(...) {} // method

  get something(...) {} // getter method
  set something(...) {} // setter method

  [Symbol.iterator]() {} // method with computed name (symbol here)
  // ...
}
```

`MyClass` về mặt kỹ thuật là một function (hàm mà chúng ta cung cấp dưới dạng `constructor`), trong khi các methods, getters và setters được viết vào `MyClass.prototype`.

Trong các chương tiếp theo chúng ta sẽ học thêm về classes, bao gồm inheritance và các tính năng khác.

---

---

## Bài tập

## [Các bài tập](#tasks)

### [Viết lại thành class](#rewrite-to-class)

importance: 5

Class `Clock` (xem trong sandbox) được viết theo phong cách functional. Hãy viết lại nó theo cú pháp "class".

P.S. Đồng hồ tick trong console, mở nó ra để xem.

[Mở sandbox cho bài tập.](https://plnkr.co/edit/zFpaXjL5VCqQhCsJ?p=preview)

[lời giải](#solution)

```
class Clock {
  constructor({ template }) {
    this.template = template;
  }

  render() {
    let date = new Date();

    let hours = date.getHours();
    if (hours < 10) hours = '0' + hours;

    let mins = date.getMinutes();
    if (mins < 10) mins = '0' + mins;

    let secs = date.getSeconds();
    if (secs < 10) secs = '0' + secs;

    let output = this.template
      .replace('h', hours)
      .replace('m', mins)
      .replace('s', secs);

    console.log(output);
  }

  stop() {
    clearInterval(this.timer);
  }

  start() {
    this.render();
    this.timer = setInterval(() => this.render(), 1000);
  }
}

let clock = new Clock({template: 'h:m:s'});
clock.start();
```

[Mở lời giải trong sandbox.](https://plnkr.co/edit/p49wtIpkvjhJgM5i?p=preview)
