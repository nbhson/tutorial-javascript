# Constructor, toán tử "new"

> Nguồn: [https://javascript.info/constructor-new](https://javascript.info/constructor-new)

<!-- fetched: 2026-09-14 -->

Cú pháp regular `{...}` cho phép chúng ta tạo một object. Nhưng thường chúng ta cần tạo nhiều objects similar, như nhiều users hoặc menu items và vân vân.

Điều đó có thể được thực hiện bằng constructor functions và toán tử `"new"`.

## [Constructor function](#constructor-function)

Constructor functions về mặt kỹ thuật là regular functions. Có hai conventions though:

1. Chúng được named với chữ hoa first.
2. Chúng nên được executed chỉ với toán tử `"new"`.

Ví dụ:

```
function User(name) {
  this.name = name;
  this.isAdmin = false;
}

let user = new User("Jack");

alert(user.name); // Jack
alert(user.isAdmin); // false
```

Khi một function được executed với `new`, nó làm các steps sau:

1. Một new empty object được tạo và gán cho `this`.
2. Function body executes. Thường nó modifies `this`, thêm new properties vào nó.
3. Giá trị của `this` được returned.

Nói cách khác, `new User(...)` làm something like:

```
function User(name) {
  // this = {};  (implicitly)

  // add properties to this
  this.name = name;
  this.isAdmin = false;

  // return this;  (implicitly)
}
```

Vì vậy `let user = new User("Jack")` gives cùng result như:

```
let user = {
  name: "Jack",
  isAdmin: false
};
```

Giờ nếu chúng ta muốn tạo các users khác, chúng ta có thể gọi `new User("Ann")`, `new User("Alice")` và vân vân. Ngắn hơn nhiều so với sử dụng literals mỗi lần, và cũng dễ đọc.

Đó là main purpose của constructors – để implement reusable object creation code.

Hãy note một lần nữa – về mặt kỹ thuật, bất kỳ function nào (ngoại trừ arrow functions, vì chúng không có `this`) có thể được sử dụng như một constructor. Nó có thể được chạy với `new`, và nó sẽ thực thi algorithm ở trên. "Chữ hoa first" là một common agreement, để làm rõ rằng một function sẽ được chạy với `new`.

new function() { … }

Nếu chúng ta có nhiều dòng code tất cả về creation của một single complex object, chúng ta có thể wrap them trong một immediately called constructor function, như thế này:

```
// create a function and immediately call it with new
let user = new function() {
  this.name = "John";
  this.isAdmin = false;

  // ...other code for user creation
  // maybe complex logic and statements
  // local variables etc
};
```

Constructor này không thể được gọi lại, vì nó không được lưu ở đâu, just created and called. Vì vậy trick này aims to encapsulate code that constructs the single object, without future reuse.

## [Constructor mode test: new.target](#constructor-mode-test-new-target)

Advanced stuff

Cú pháp từ section này hiếm khi được sử dụng, skip it trừ khi bạn muốn biết everything.

Bên trong một function, chúng ta có thể check xem nó được gọi với `new` hay không, bằng cách sử dụng một special `new.target` property.

Nó là undefined cho regular calls và bằng function nếu được gọi với `new`:

```
function User() {
  alert(new.target);
}

// without "new":
User(); // undefined

// with "new":
new User(); // function User { ... }
```

Điều đó có thể được sử dụng bên trong function để biết xem nó được gọi với `new`, "in constructor mode", hay không, "in regular mode".

Chúng ta cũng có thể làm cho cả `new` và regular calls làm cùng một thứ, như thế này:

```
function User(name) {
  if (!new.target) { // if you run me without new
    return new User(name); // ...I will add new for you
  }

  this.name = name;
}

let john = User("John"); // redirects call to new User
alert(john.name); // John
```

Approach như vậy đôi khi được sử dụng trong các libraries để làm cho syntax linh hoạt hơn. Vì vậy mọi người có thể gọi function với hoặc không có `new`, và nó vẫn hoạt động.

Có lẽ không phải là một good thing để sử dụng ở mọi nơi though, vì omitting `new` làm cho nó hơi less obvious what's going on. Với `new` chúng ta bất kỳ biết rằng new object đang được tạo.

## [Return từ constructors](#return-from-constructors)

Thông thường, constructors không có một `return` statement. Task của họ là viết tất cả necessary stuff vào `this`, và nó automatically trở thành result.

Nhưng nếu có một `return` statement, sau đó rule là đơn giản:

- Nếu `return` được gọi với một object, thì object được return thay vì `this`.
- Nếu `return` được gọi với một primitive, nó bị ignore.

Nói cách khác, `return` với một object return object đó, trong mọi trường hợp khác `this` được return.

Ví dụ, ở đây `return` overrides `this` bằng cách return một object:

```
function BigUser() {

  this.name = "John";

  return { name: "Godzilla" };  // <-- returns this object
}

alert( new BigUser().name );  // Godzilla, got that object
```

Và đây là mộtví dụví dụ với một empty `return` (hoặc chúng ta có thể place một primitive sau nó, không quan trọng):

```
function SmallUser() {

  this.name = "John";

  return; // <-- returns this
}

alert( new SmallUser().name );  // John
```

Thông thường constructors không có một `return` statement. Ở đây chúng ta đề cập đến special behavior với returning objects chủ yếu để completeness.

Bỏ qua parentheses

Bằng cách nào đó, chúng ta có thể omit parentheses sau `new`:

```
let user = new User; // <-- no parentheses
// same as
let user = new User();
```

Bỏ qua parentheses ở đây không được xem như là một "good style", nhưng syntax được permitted bởi specification.

## [Methods trong constructor](#methods-in-constructor)

Sử dụng constructor functions để tạo objects cho một great deal của flexibility. Constructor function có thể có parameters định nghĩa làm thế nào để construct object, và những gì để put trong nó.

Tất nhiên, chúng ta có thể thêm vào `this` không chỉ properties, mà còn methods.

Ví dụ, `new User(name)` dưới đây tạo một object với `name` được cho và method `sayHi`:

```
function User(name) {
  this.name = name;

  this.sayHi = function() {
    alert( "Tên của tôi là: " + this.name );
  };
}

let john = new User("John");

john.sayHi(); // Tên của tôi là: John

/*
john = {
   name: "John",
   sayHi: function() { ... }
}
*/
```

Để tạo các complex objects, có một advanced syntax hơn, [classes](/classes), mà chúng ta sẽ cover sau.

## [Tổng kết](#summary)

- Constructor functions hoặc, nói tắt, constructors, là regular functions, nhưng có một common agreement để named them với chữ hoa first.
- Constructor functions nên chỉ được called bằng cách sử dụng `new`. Một call như vậy ngụ ý một creation of empty `this` tại start và returning the populated one tại end.

Chúng ta có thể sử dụng constructor functions để tạo nhiều objects similar.

JavaScript cung cấp constructor functions cho nhiều built-in language objects: như `Date` cho dates, `Set` cho sets và others mà chúng ta plan để study.

Objects, chúng ta sẽ quay lại!

Trong chương này chúng ta chỉ cover basics về objects và constructors. Chúng essential để học thêm về data types và functions trong các chương sau.

Sau khi chúng ta học được rằng, chúng ta quay lại objects và cover chúng in-depth trong các chương [Prototypes, inheritance](/prototypes) và [Classes](/classes).

---

---

## Các bài tập

## [Các bài tập](#tasks)

### [Hai functions – một object](#two-functions--one-object)

mức độ quan trọng: 2

Có thể tạo các functions `A` và `B` sao cho `new A() == new B()` không?

```
function A() { ... }
function B() { ... }

let a = new A();
let b = new B();

alert( a == b ); // true
```

Nếu có thể, thì provide mộtví dụví dụ về code của chúng.

lời giải

Có, nó có thể.

Nếu một function return một object thì `new` return nó thay vì `this`.

Vì vậy chúng có thể,ví dụví dụ, return cùng externally defined object `obj`:

```
let obj = {};

function A() { return obj; }
function B() { return obj; }

alert( new A() == new B() ); // true
```

### [Tạo Calculator mới](#create-new-calculator)

mức độ quan trọng: 5

Tạo một constructor function `Calculator` tạo ra các objects với 3 methods:

- `read()` yêu cầu nhập hai giá trị và save chúng như object properties với names `a` và `b` respectively.
- `sum()` trả về sum củacác properties.
- `mul()` trả về multiplication product củacác properties.

Ví dụ:

```
let calculator = new Calculator();
calculator.read();

alert( "Sum=" + calculator.sum() );
alert( "Mul=" + calculator.mul() );
```

[Chạy demo](#)

[Mở một sandbox với tests.](https://plnkr.co/edit/JFVXYYeK4cf3cbyC?p=preview)

lời giải

```
function Calculator() {

  this.read = function() {
    this.a = +prompt('a?', 0);
    this.b = +prompt('b?', 0);
  };

  this.sum = function() {
    return this.a + this.b;
  };

  this.mul = function() {
    return this.a * this.b;
  };
}

let calculator = new Calculator();
calculator.read();

alert( "Sum=" + calculator.sum() );
alert( "Mul=" + calculator.mul() );
```

[Mở solution với tests trong một sandbox.](https://plnkr.co/edit/7mXTSwXLzswVByuQ?p=preview)

### [Tạo Accumulator mới](#create-new-accumulator)

mức độ quan trọng: 5

Tạo một constructor function `Accumulator(startingValue)`.

Object mà nó tạo nên:

- Store "current value" trong property `value`. Starting value được set đến argument của constructor `startingValue`.
- Method `read()` nên sử dụng `prompt` để đọc một số mới và add nó vào `value`.

Nói cách khác, property `value` là sum của tất cả user-entered values với initial value `startingValue`.

Ở đây là demo của code:

```
let accumulator = new Accumulator(1); // initial value 1

accumulator.read(); // adds the user-entered value
accumulator.read(); // adds the user-entered value

alert(accumulator.value); // shows the sum of these values
```

[Chạy demo](#)

[Mở một sandbox với tests.](https://plnkr.co/edit/7Iu20TXrAepw7V5J?p=preview)

lời giải

```
function Accumulator(startingValue) {
  this.value = startingValue;

  this.read = function() {
    this.value += +prompt('How much to add?', 0);
  };

}

let accumulator = new Accumulator(1);
accumulator.read();
accumulator.read();
alert(accumulator.value);
```

[Mở solution với tests trong một sandbox.](https://plnkr.co/edit/QpnKj8aVbW4EOnpR?p=preview)
