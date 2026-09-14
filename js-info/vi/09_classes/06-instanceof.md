# Kiểm tra class: "instanceof"

> Nguồn: [https://javascript.info/instanceof](https://javascript.info/instanceof)

<!-- fetched: 2026-09-14 -->

Toán tử `instanceof` cho phép kiểm tra xem một đối tượng thuộc về một class nhất định. Nó cũng tính đến inheritance.

Kiểm tra như vậy có thể cần thiết trong nhiều trường hợp. Ví dụ, nó có thể được sử dụng để xây dựng một hàm *polymorphic*, hàm xử lý các arguments khác nhau tùy thuộc vào type của chúng.

## [Toán tử instanceof](#ref-instanceof)

Cú pháp là:

```
obj instanceof Class
```

Nó trả về `true` nếu `obj` thuộc về `Class` hoặc một class kế thừa từ nó.

Ví dụ:

```
class Rabbit {}
let rabbit = new Rabbit();

// is it an object of Rabbit class?
alert( rabbit instanceof Rabbit ); // true
```

Nó cũng hoạt động với các constructor functions:

```
// instead of class
function Rabbit() {}

alert( new Rabbit() instanceof Rabbit ); // true
```

…Và với các built-in classes như `Array`:

```
let arr = [1, 2, 3];
alert( arr instanceof Array ); // true
alert( arr instanceof Object ); // true
```

Xin lưu ý rằng `arr` cũng thuộc về class `Object`. Đó là vì `Array` prototypically kế thừa từ `Object`.

Thông thường, `instanceof` kiểm tra prototype chain để kiểm tra. Chúng ta cũng có thể đặt logic tùy chỉnh trong static method `Symbol.hasInstance`.

Thuật toán của `obj instanceof Class` hoạt động đại khái như sau:

1. Nếu có static method `Symbol.hasInstance`, thì gọi nó: `Class[Symbol.hasInstance](obj)`. Nó nên trả về `true` hoặc `false`, và chúng ta xong. Đó là cách chúng ta có thể tùy chỉnh behavior của `instanceof`.

   Ví dụ:

   ```
   // set up instanceof check that assumes that
   // anything with canEat property is an animal
   class Animal {
     static [Symbol.hasInstance](obj) {
       if (obj.canEat) return true;
     }
   }

   let obj = { canEat: true };

   alert(obj instanceof Animal); // true: Animal[Symbol.hasInstance](obj) is called
   ```
2. Hầu hết các classes không có `Symbol.hasInstance`. Trong trường hợp đó, standard logic được sử dụng: `obj instanceof Class` kiểm tra xem `Class.prototype` có equal đến một trong các prototypes trong prototype chain của `obj` không.

   Nói cách khác, so sánh từng cái một:

   ```
   obj.__proto__ === Class.prototype?
   obj.__proto__.__proto__ === Class.prototype?
   obj.__proto__.__proto__.__proto__ === Class.prototype?
   ...
   // if any answer is true, return true
   // otherwise, if we reached the end of the chain, return false
   ```

   Trong ví dụ trên `rabbit.__proto__ === Rabbit.prototype`, vì vậy nó cho answer ngay lập tức.

   Trong trường hợp inheritance, match sẽ ở bước thứ hai:

   ```
   class Animal {}
   class Rabbit extends Animal {}

   let rabbit = new Rabbit();
   alert(rabbit instanceof Animal); // true

   // rabbit.__proto__ === Animal.prototype (no match)
   // rabbit.__proto__.__proto__ === Animal.prototype (match!)
   ```

Đây là minh họa về những gì `rabbit instanceof Animal` so sánh với `Animal.prototype`:

![](/article/instanceof/instanceof.svg)

Nhân tiện, cũng có method [objA.isPrototypeOf(objB)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/object/isPrototypeOf), trả về `true` nếu `objA` ở đâu đó trong chain prototypes cho `objB`. Vì vậy test của `obj instanceof Class` có thể được diễn đạt lại là `Class.prototype.isPrototypeOf(obj)`.

Thật vui là constructor `Class` chính nó không tham gia vào check! Chỉ có chain của prototypes và `Class.prototype` là matters.

Điều đó có thể dẫn đến các consequences thú vị khi một `prototype` property được thay đổi sau khi object được tạo.

Như ở đây:

```
function Rabbit() {}
let rabbit = new Rabbit();

// changed the prototype
Rabbit.prototype = {};

// ...not a rabbit any more!
alert( rabbit instanceof Rabbit ); // false
```

## [Bonus: Object.prototype.toString để kiểm tra type](#bonus-object-prototype-tostring-for-the-type)

Chúng ta đã biết rằng các plain object được convert thành string như `[object Object]`:

```
let obj = {};

alert(obj); // [object Object]
alert(obj.toString()); // the same
```

Đó là implementation của `toString`. Nhưng có một hidden feature làm cho `toString` thực sự mạnh mẽ hơn nhiều. Chúng ta có thể sử dụng nó như một `typeof` mở rộng và một phương án thay thế cho `instanceof`.

Nghe có vẻ kỳ lạ? Đúng vậy. Hãy demystify.

Theo [specification](https://tc39.github.io/ecma262/#sec-object.prototype.tostring), `toString` built-in có thể được extract từ object và thực thi trong context của bất kỳ value nào khác. Và kết quả của nó phụ thuộc vào value đó.

- Đối với một number, nó sẽ là `[object Number]`
- Đối với một boolean, nó sẽ là `[object Boolean]`
- Đối với `null`: `[object Null]`
- Đối với `undefined`: `[object Undefined]`
- Đối với arrays: `[object Array]`
- …v.v. (có thể tùy chỉnh).

Hãy demo:

```
// copy toString method into a variable for convenience
let objectToString = Object.prototype.toString;

// what type is this?
let arr = [];

alert( objectToString.call(arr) ); // [object Array]
```

Ở đây chúng ta đã sử dụng [call](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/function/call) như mô tả trong chương [Decorators and forwarding, call/apply](/call-apply-decorators) để thực thi function `objectToString` trong context `this=arr`.

Về mặt nội bộ, thuật toán `toString` xem xét `this` và trả về kết quả tương ứng. Các ví dụ khác:

```
let s = Object.prototype.toString;

alert( s.call(123) ); // [object Number]
alert( s.call(null) ); // [object Null]
alert( s.call(alert) ); // [object Function]
```

### [Symbol.toStringTag](#symbol-tostringtag)

Behavior của Object `toString` có thể được tùy chỉnh bằng cách sử dụng một object property đặc biệt `Symbol.toStringTag`.

Ví dụ:

```
let user = {
  [Symbol.toStringTag]: "User"
};

alert( {}.toString.call(user) ); // [object User]
```

Đối với hầu hết các objects đặc thù cho environment, có property như vậy. Dưới đây là một vài ví dụ đặc thù cho browser:

```
// toStringTag for the environment-specific object and class:
alert( window[Symbol.toStringTag]); // Window
alert( XMLHttpRequest.prototype[Symbol.toStringTag] ); // XMLHttpRequest

alert( {}.toString.call(window) ); // [object Window]
alert( {}.toString.call(new XMLHttpRequest()) ); // [object XMLHttpRequest]
```

Như bạn có thể thấy, kết quả chính xác là `Symbol.toStringTag` (nếu tồn tại), được wrap vào `[object ...]`.

Cuối cùng chúng ta có "typeof on steroids" không chỉ hoạt động cho primitive data types, mà còn cho các built-in objects và thậm chí có thể được tùy chỉnh.

Chúng ta có thể sử dụng `{}.toString.call` thay vì `instanceof` cho các built-in objects khi chúng ta muốn lấy type dưới dạng string chứ không chỉ để kiểm tra.

## [Tóm tắt](#summary)

Hãy tóm tắt các methods kiểm tra type mà chúng ta biết:

|  | works for | returns |
| --- | --- | --- |
| `typeof` | primitives | string |
| `{}.toString` | primitives, built-in objects, objects with `Symbol.toStringTag` | string |
| `instanceof` | objects | true/false |

Như chúng ta có thể thấy, `{}.toString` về mặt kỹ thuật là một `typeof` "advanced hơn".

Và toán tử `instanceof` thực sự tỏa sáng khi chúng ta đang làm việc với một thứ bậc class và muốn kiểm tra cho class tính đến inheritance.

---

---

## Bài tập

## [Các bài tập](#tasks)

### [instanceof kỳ lạ](#strange-instanceof)

importance: 5

Trong mã dưới đây, tại sao `instanceof` trả về `true`? Chúng ta có thể dễ dàng thấy rằng `a` không được tạo bởi `B()`.

```
function A() {}
function B() {}

A.prototype = B.prototype = {};

let a = new A();

alert( a instanceof B ); // true
```

[lời giải](#solution)

Đúng là trông kỳ lạ.

Nhưng `instanceof` không quan tâm đến function, mà là `prototype` của nó, mà nó match với prototype chain.

Và ở đây `a.__proto__ == B.prototype`, vì vậy `instanceof` trả về `true`.

Vì vậy, theo logic của `instanceof`, `prototype` thực sự định nghĩa type, không phải constructor function.
