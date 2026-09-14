# Object methods, "this"

> Nguồn: [https://javascript.info/object-methods](https://javascript.info/object-methods)

<!-- fetched: 2026-09-14 -->

Objects thường được tạo để đại diện cho các entities của thế giới thực, như users, orders và vân vân:

```
let user = {
  name: "John",
  age: 30
};
```

Và, trong thế giới thực, một user có thể *act*: select something from the shopping cart, login, logout v.v.

Hành động được đại diện trong JavaScript bằng functions trong properties.

## [Method examples](#method-examples)

Để bắt đầu, hãy dạy `user` nói xin chào:

```
let user = {
  name: "John",
  age: 30
};

user.sayHi = function() {
  alert("Xin chào!");
};

user.sayHi(); // Xin chào!
```

Ở đây chúng ta vừa mới sử dụng một Function Expression để tạo một function và gán nó vào property `user.sayHi` của object.

Sau đó chúng ta có thể gọi nó như `user.sayHi()`. User giờ có thể nói chuyện!

Một function mà là một property của một object được gọi là *method* của nó.

Vì vậy, ở đây chúng ta có một method `sayHi` của object `user`.

Tất nhiên, chúng ta có thể sử dụng một pre-declared function như là một method, như thế này:

```
let user = {
  // ...
};

// first, declare
function sayHi() {
  alert("Xin chào!");
}

// then add as a method
user.sayHi = sayHi;

user.sayHi(); // Xin chào!
```

Object-oriented programming

Khi chúng ta viết code của chúng ta bằng cách sử dụng objects để đại diện cho các entities, điều đó được gọi là [object-oriented programming](https://en.wikipedia.org/wiki/Object-oriented_programming), nói tắt: "OOP".

OOP là một big thing, một science thú vị của chính nó. Làm thế nào để chọn đúng entities? Làm thế nào để tổ chức interaction giữa chúng? Đó là architecture, và có những books hay về chủ đề đó, như "Design Patterns: Elements of Reusable Object-Oriented Software" của E. Gamma, R. Helm, R. Johnson, J. Vissides hoặc "Object-Oriented Analysis and Design with Applications" của G. Booch, và nhiều hơn nữa.

### [Method shorthand](#method-shorthand)

Có một cú pháp ngắn gọn hơn cho methods trong một object literal:

```
// these objects do the same

user = {
  sayHi: function() {
    alert("Hello");
  }
};

// method shorthand looks better, right?
user = {
  sayHi() { // giống như "sayHi: function(){...}"
    alert("Hello");
  }
};
```

Như demonstrated, chúng ta có thể omit `"function"` và chỉ viết `sayHi()`.

Nói thật, các notations không hoàn toàn identical. Có những subtle differences liên quan đến object inheritance (sẽ được cover sau), nhưng cho đến nay chúng không quan trọng. Trong hầu hết các cases, shorter syntax được prefer.

## ["this" trong methods](#this-in-methods)

Rất phổ biến rằng một object method cần access thông tin được lưu trữ trong object để làm job của nó.

Ví dụ, code bên trong `user.sayHi()` có thể cần name của `user`.

**Để access object, một method có thể sử dụng keyword `this`.**

Giá trị của `this` là object "trước dấu chấm", cái được sử dụng để gọi method.

Ví dụ:

```
let user = {
  name: "John",
  age: 30,

  sayHi() {
    // "this" là "current object"
    alert(this.name);
  }

};

user.sayHi(); // John
```

Ở đây trong quá trình execution của `user.sayHi()`, giá trị của `this` sẽ là `user`.

Về mặt kỹ thuật, cũng có thể access object mà không có `this`, bằng cách referencing nó thông qua outer variable:

```
let user = {
  name: "John",
  age: 30,

  sayHi() {
    alert(user.name); // "user" thay vì "this"
  }

};
```

…Nhưng mã như vậy không đáng tin cậy. Nếu chúng ta quyết định copy `user` sang một variable khác,ví dụví dụ `admin = user` và ghi đè `user` bằng cái gì đó khác, sau đó nó sẽ access sai object.

Điều đó được demonstrated bên dưới:

```
let user = {
  name: "John",
  age: 30,

  sayHi() {
    alert( user.name ); // leads to an error
  }

};

let admin = user;
user = null; // overwrite to make things obvious

admin.sayHi(); // TypeError: Cannot read property 'name' of null
```

Nếu chúng ta sử dụng `this.name` thay vì `user.name` bên trong `alert`, thì code sẽ hoạt động.

## ["this" không được bound](#this-is-not-bound)

Trong JavaScript, keyword `this` hành xử khác với hầu hết các programming languages khác. Nó có thể được sử dụng trong bất kỳ function nào, ngay cả khi nó không phải là method của một object.

Không có syntax error trongví dụví dụ sau:

```
function sayHi() {
  alert( this.name );
}
```

Giá trị của `this` được evaluated trong quá trình run-time, tùy thuộc vào context.

Ví dụ, ở đây function giống nhau được gán cho hai objects khác nhau và có "this" khác nhau trong các calls:

```
let user = { name: "John" };
let admin = { name: "Admin" };

function sayHi() {
  alert( this.name );
}

// use the same function in two objects
user.f = sayHi;
admin.f = sayHi;

// these calls have different this
// "this" bên trong function là object "trước dấu chấm"
user.f(); // John  (this == user)
admin.f(); // Admin  (this == admin)

admin['f'](); // Admin (dot hoặc square brackets access the method – không quan trọng)
```

Rule là đơn giản: nếu `obj.f()` được gọi, thì `this` là `obj` trong quá trình call của `f`. Vì vậy nó là `user` hoặc `admin` trongví dụví dụ ở trên.

Calling mà không có object: `this == undefined`

Chúng ta thậm chí có thể gọi function mà không có object ở tất cả:

```
function sayHi() {
  alert(this);
}

sayHi(); // undefined
```

Trong trường hợp này `this` là `undefined` trong strict mode. Nếu chúng ta cố gắng access `this.name`, sẽ có error.

Trong non-strict mode giá trị của `this` trong trường hợp như vậy sẽ là *global object* (`window` trong một browser, chúng ta sẽ đến nó sau trong chương [Global object](/global-object)). Đó là behavior lịch sử mà `"use strict"` sửa.

Thông thường call như vậy là một programming error. Nếu có `this` bên trong một function, nó mong đợi được gọi trong một object context.

The consequences of unbound `this`

Nếu bạn đến từ một programming language khác, thì bạn có lẽ đã quen với ý tưởng về một "bound `this`", nơi các methods được định nghĩa trong một object luôn có `this` referencing object đó.

Trong JavaScript `this` là "free", giá trị của nó được evaluated tại call-time và không phụ thuộc vào nơi method được khai báo, mà thay vào đó phụ thuộc vào object nào là "trước dấu chấm".

Concept của run-time evaluated `this` có cả pluses và minuses. Ở một mặt, một function có thể được reuse cho các objects khác nhau. Ở mặt khác, greater flexibility tạo nhiều possibilities hơn cho mistakes.

Ở đây position của chúng ta là không judge xem design decision language này là tốt hay xấu. Chúng ta sẽ hiểu làm thế nào để làm việc với nó, làm thế nào để get benefits và avoid problems.

## [Arrow functions không có "this"](#arrow-functions-have-no-this)

Arrow functions là đặc biệt: chúng không có "own" `this`. Nếu chúng ta referencing `this` từ function như vậy, nó được lấy từ outer "normal" function.

Ví dụ, ở đây `arrow()` sử dụng `this` từ outer `user.sayHi()` method:

```
let user = {
  firstName: "Ilya",
  sayHi() {
    let arrow = () => alert(this.firstName);
    arrow();
  }
};

user.sayHi(); // Ilya
```

Đó là một tính năng đặc biệt của arrow functions, nó hữu ích khi chúng ta thực sự không muốn có một `this` riêng biệt, mà thay vào đó lấy nó từ outer context. Sau đó trong chương [Arrow functions revisited](/arrow-functions) chúng ta sẽ đi sâu hơn vào arrow functions.

## [Tổng kết](#summary)

- Functions được lưu trong object properties được gọi là "methods".
- Methods cho phép objects "act" như `object.doSomething()`.
- Methods có thể referencing object như `this`.

Giá trị của `this` được define tại run-time.

- Khi một function được declare, nó có thể sử dụng `this`, nhưng `this` đó không có value cho đến khi function được gọi.
- Một function có thể được copy giữa các objects.
- Khi một function được gọi trong "method" syntax: `object.method()`, giá trị của `this` trong quá trình gọi là `object`.

Xin lưu ý rằng arrow functions là đặc biệt: chúng không có `this`. Khi `this` được access bên trong một arrow function, nó được lấy từ bên ngoài.

---

---

## Các bài tập

## [Các bài tập](#tasks)

### [Sử dụng "this" trong object literal](#using-this-in-object-literal)

mức độ quan trọng: 5

Ở đây function `makeUser` trả về một object.

Kết quả của accessing `ref` của nó là gì? Tại sao?

```
function makeUser() {
  return {
    name: "John",
    ref: this
  };
}

let user = makeUser();

alert( user.ref.name ); // Kết quả là gì?
```

lời giải

**Answer: an error.**

Hãy thử:

```
function makeUser() {
  return {
    name: "John",
    ref: this
  };
}

let user = makeUser();

alert( user.ref.name ); // Error: Cannot read property 'name' of undefined
```

Điều đó là vì rules که set `this` không nhìn vào object definition. Chỉ moment của call là quan trọng.

Ở đây giá trị của `this` bên trong `makeUser()` là `undefined`, vì nó được gọi như là một function, không phải như là một method với "dot" syntax.

Giá trị của `this` là một cho toàn bộ function, code blocks và object literals không ảnh hưởng đến nó.

Vì vậy `ref: this` thực sự lấy current `this` của function.

Chúng ta có thể rewrite function và return cùng `this` với giá trị `undefined`:

```
function makeUser(){
  return this; // lần này không có object literal
}

alert( makeUser().name ); // Error: Cannot read property 'name' of undefined
```

Như bạn có thể thấy result của `alert( makeUser().name )` là giống hệt result của `alert( user.ref.name )` từví dụví dụ trước.

Ở đây là opposite case:

```
function makeUser() {
  return {
    name: "John",
    ref() {
      return this;
    }
  };
}

let user = makeUser();

alert( user.ref().name ); // John
```

Bây giờ nó hoạt động, vì `user.ref()` là một method. Và giá trị của `this` được set đến object trước dấu chấm `.`.

### [Tạo một calculator](#create-a-calculator)

mức độ quan trọng: 5

Tạo một object `calculator` với ba methods:

- `read()` yêu cầu nhập hai giá trị và save chúng như object properties với names `a` và `b` respectively.
- `sum()` trả về sum của saved values.
- `mul()` multiplies saved values và trả về result.

```
let calculator = {
  // ... your code ...
};

calculator.read();
alert( calculator.sum() );
alert( calculator.mul() );
```

[Chạy demo](#)

[Mở một sandbox với tests.](https://plnkr.co/edit/xpOf39ov5xQ8UDnd?p=preview)

lời giải

```
let calculator = {
  sum() {
    return this.a + this.b;
  },

  mul() {
    return this.a * this.b;
  },

  read() {
    this.a = +prompt('a?', 0);
    this.b = +prompt('b?', 0);
  }
};

calculator.read();
alert( calculator.sum() );
alert( calculator.mul() );
```

[Mở solution với tests trong một sandbox.](https://plnkr.co/edit/NreUKdNQDiFaCmdw?p=preview)

### [Chaining](#chaining)

mức độ quan trọng: 2

Có một object `ladder` cho phép bạn đi lên và xuống:

```
let ladder = {
  step: 0,
  up() {
    this.step++;
  },
  down() {
    this.step--;
  },
  showStep: function() { // shows the current step
    alert( this.step );
  }
};
```

Giờ, nếu chúng ta cần thực hiện nhiều calls trong sequence, chúng ta có thể làm như thế này:

```
ladder.up();
ladder.up();
ladder.down();
ladder.showStep(); // 1
ladder.down();
ladder.showStep(); // 0
```

Sửa code của `up`, `down`, và `showStep` để làm cho các calls chainable, như thế này:

```
ladder.up().up().down().showStep().down().showStep(); // shows 1 then 0
```

Approach như vậy được sử dụng rộng rãi trên khắp các JavaScript libraries.

[Mở một sandbox với tests.](https://plnkr.co/edit/jK8ILGHeKgaxX3WE?p=preview)

lời giải

Solution là trả về objectbản thân từ mỗi call.

```
let ladder = {
  step: 0,
  up() {
    this.step++;
    return this;
  },
  down() {
    this.step--;
    return this;
  },
  showStep() {
    alert( this.step );
    return this;
  }
};

ladder.up().up().down().showStep().down().showStep(); // shows 1 then 0
```

Chúng ta cũng có thể viết một single call per line. Đối với long chains nó dễ đọc hơn:

```
ladder
  .up()
  .up()
  .down()
  .showStep() // 1
  .down()
  .showStep(); // 0
```

[Mở solution với tests trong một sandbox.](https://plnkr.co/edit/6U7x0RicuTtP24M7?p=preview)
