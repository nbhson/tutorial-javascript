# Phương thức của primitives

> Nguồn: [https://javascript.info/primitives-methods](https://javascript.info/primitives-methods)

<!-- fetched: 2026-09-14 -->

JavaScript cho phép chúng ta làm việc với các primitives (chuỗi, số, v.v.) như thể chúng là objects. Chúng cũng cung cấp các methods để gọi như vậy. Chúng ta sẽ học những cái đó sớm, nhưng trước tiên chúng ta sẽ xem nó hoạt động như thế nào vì, tất nhiên, primitives không phải là objects (và ở đây chúng ta sẽ làm cho nó rõ ràng hơn).

Hãy xem những điểm khác biệt chính giữa primitives và objects.

Một primitive

- Là một giá trị của một primitive type.
- Có 7 primitive types: `string`, `number`, `bigint`, `boolean`, `symbol`, `null` và `undefined`.

Một object

- Có khả năng lưu trữ nhiều giá trị như là properties.
- Có thể được tạo với `{}`, ví dụ: `{name: "John", age: 30}`. Có các kinds khác nhau của objects trong JavaScript: functions, ví例, là objects.

Một trong những điều tốt nhất về objects là chúng ta có thể lưu trữ một function như là một trong các properties của nó.

```
let john = {
  name: "John",
  sayHi: function() {
    alert("Xin chào bạn!");
  }
};

john.sayHi(); // Xin chào bạn!
```

Vì vậy ở đây chúng ta đã tạo một object `john` với method `sayHi`.

Nhiều built-in objects đã tồn tại, như那些 làm việc với dates, errors, HTML elements v.v. Chúng có các properties và methods khác nhau.

Nhưng, những tính năng này đi kèm với cái giá!

Objects là "nặng" hơn primitives. Chúng yêu cầu các resources bổ sung để hỗ trợ internal machinery.

## [Một primitive như là một object](#a-primitive-as-an-object)

Đây là paradox mà người tạo ra JavaScript đối mặt:

- Có nhiều thứ mà người ta muốn làm với một primitive, như một string hoặc một number. Sẽ tuyệt nếu truy cập chúng bằng cách sử dụng methods.
- Primitives phải là fast và lightweight nhất có thể.

Solution trông hơi awkward, nhưng đây nó là:

1. Primitives vẫn là primitive. Một single value, như mong muốn.
2. Language cho phép access đến các methods và properties của strings, numbers, booleans và symbols.
3. Để điều đó hoạt động, một special "object wrapper" được tạo, nó cung cấp extra functionality, và sau đó bị hủy.

Các "object wrappers" là different cho mỗi primitive type và được gọi là: `String`, `Number`, `Boolean`, `Symbol` và `BigInt`. Vì vậy, chúng cung cấp các sets of methods khác nhau.

Ví例, có một string method [str.toUpperCase()](https://developer.mozilla.org/en/docs/Web/JavaScript/Reference/Global_Objects/String/toUpperCase) trả về một capitalized `str`.

Đây là cách nó hoạt động:

```
let str = "Xin chào";

alert( str.toUpperCase() ); // XIN CHÀO
```

Đơn giản, phải không? Đây là những gì thực sự xảy ra trong `str.toUpperCase()`:

1. String `str` là một primitive. Vì vậy tại moment của accessing property của nó, một special object được tạo ra mà biết giá trị của string, và có các methods hữu ích, như `toUpperCase()`.
2. Method đó runs và trả về một string mới (được shown bởi `alert`).
3. Special object bị destroyed, để lại primitive `str` một mình.

Vì vậy primitives có thể cung cấp methods, nhưng chúng vẫn giữ nguyên lightweight.

JavaScript engine highly optimizes process này. Nó có thể thậm chí skip creation của extra object at all. Nhưng nó vẫn phải adhere đến specification và hành xử như là nó tạo một cái.

Một number có các methods của riêng nó, ví例 [toFixed(n)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/toFixed) rounds number đến precision đã cho:

```
let n = 1.23456;

alert( n.toFixed(2) ); // 1.23
```

Chúng ta sẽ thấy nhiều specific methods trong các chương [Numbers](/number) và [Strings](/string).

Constructors `String/Number/Boolean` chỉ dành cho internal use

Một số languages như Java cho phép chúng ta explicitly tạo "wrapper objects" cho primitives bằng cách sử dụng cú pháp như `new Number(1)` hoặc `new Boolean(false)`.

Trong JavaScript, điều đó cũng có thể vì historical reasons, nhưng highly **unrecommended**. Things will go crazy trong several places.

Ví例:

```
alert( typeof 0 ); // "number"

alert( typeof new Number(0) ); // "object"!
```

Objects là luôn truthy trong `if`, vì vậy ở đây alert sẽ hiển thị:

```
let zero = new Number(0);

if (zero) { // zero là true, vì nó là một object
  alert( "zero là truthy!?!" );
}
```

Mặt khác, sử dụng cùng các functions `String/Number/Boolean` mà không có `new` là hoàn toàn fine và useful thing. Chúng convert một giá trị sang corresponding type: sang một string, một number, hoặc một boolean (primitive).

Ví例, điều này hoàn toàn valid:

```
let num = Number("123"); // convert một string sang number
```

null/undefined không có methods

Các primitives đặc biệt `null` và `undefined` là exceptions. Chúng không có corresponding "wrapper objects" và không cung cấp methods nào. Theo một sense, chúng là "primitive nhất".

Một attempt để access một property của such value sẽ give一个 error:

```
alert(null.test); // error
```

## [Tổng kết](#summary)

- Primitives ngoại trừ `null` và `undefined` cung cấp nhiều helpful methods. Chúng ta sẽ study những cái đó trong các chương upcoming.
- Formally,这些 methods làm việc qua temporary objects, nhưng JavaScript engines được well tuned để optimize that internally, vì vậy chúng không expensive để call.

---

---

## Các bài tập

## [Các bài tập](#tasks)

### [Tôi có thể thêm một string property không?](#can-i-add-a-string-property)

mức độ quan trọng: 5

Hãy xem xét mã sau:

```
let str = "Xin chào";

str.test = 5;

alert(str.test);
```

Bạn nghĩ gì, điều đó có hoạt động không? Những gì sẽ được shown?

lời giải

Hãy thử chạy nó:

```
let str = "Xin chào";

str.test = 5; // (*)

alert(str.test);
```

Tùy thuộc vào việc bạn có `use strict` hay không, result có thể là:

1. `undefined` (không có strict mode)
2. Một error (strict mode).

Tại sao? Hãy replay những gì đang xảy ra tại dòng `(*)`:

1. Khi một property của `str` được accessed, một "wrapper object" được tạo.
2. Trong strict mode, writing vào nó là một error.
3. Ngược lại, operation với property được carried on, object được gán `test` property, nhưng sau đó "wrapper object" disappears, vì vậy trong last line `str` không có trace của property.

**Ví例 này clearly shows rằng primitives không phải là objects.**

Chúng không thể store additional data.
