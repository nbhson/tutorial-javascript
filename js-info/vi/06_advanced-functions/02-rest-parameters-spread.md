# Tham số rest và cú pháp spread

> Source: [https://javascript.info/rest-parameters-spread](https://javascript.info/rest-parameters-spread)

<!-- fetched: 2026-09-14 -->

Nhiều built-in function của JavaScript hỗ trợ số lượng đối số tùy ý.

Ví dụ:

- `Math.max(arg1, arg2, ..., argN)` – trả về giá trị lớn nhất trong các đối số.
- `Object.assign(dest, src1, ..., srcN)` – sao chép các property từ `src1..N` vào `dest`.
-…vân vân.

Trong chương này chúng ta sẽ học cách làm điều tương tự. Và cũng, cách truyền mảng vào các function như tham số.

## [Tham số rest `...`](#rest-parameters)

Một function có thể được gọi với bất kỳ số lượng đối số nào, bất kể nó được định nghĩa như thế nào.

Như ở đây:

```
function sum(a, b) {
  return a + b;
}

alert( sum(1, 2, 3, 4, 5) );
```

Sẽ không có lỗi vì các đối số "thừa". Nhưng tất nhiên trong kết quả chỉ hai đối số đầu tiên được tính, vì vậy kết quả trong code trên là `3`.

Các tham số còn lại có thể được đưa vào định nghĩa function bằng cách sử dụng ba dấu chấm `...` theo sau là tên của mảng sẽ chứa chúng. Các dấu chấm có nghĩa là "thu thập các tham số còn lại vào một mảng".

Ví dụ, để thu thập tất cả đối số vào mảng `args`:

```
function sumAll(...args) { // args is the name for the array
  let sum = 0;

  for (let arg of args) sum += arg;

  return sum;
}

alert( sumAll(1) ); // 1
alert( sumAll(1, 2) ); // 3
alert( sumAll(1, 2, 3) ); // 6
```

Chúng ta có thể chọn lấy các tham số đầu tiên làm biến, và chỉ thu thập các tham số còn lại.

Ở đây hai đối số đầu tiên đi vào biến và phần còn lại đi vào mảng `titles`:

```
function showName(firstName, lastName, ...titles) {
  alert( firstName + ' ' + lastName ); // Julius Caesar

  // the rest go into titles array
  // i.e. titles = ["Consul", "Imperator"]
  alert( titles[0] ); // Consul
  alert( titles[1] ); // Imperator
  alert( titles.length ); // 2
}

showName("Julius", "Caesar", "Consul", "Imperator");
```

Các tham số rest phải ở cuối

Các tham số rest thu thập tất cả đối số còn lại, vì vậy điều sau không hợp lý và gây lỗi:

```
function f(arg1, ...rest, arg2) { // arg2 after ...rest ?!
  // error
}
```

`...rest` luôn phải ở cuối.

## [Biến "arguments"](#the-arguments-variable)

Cũng có một object giống mảng đặc biệt tên là `arguments` chứa tất cả đối số theo chỉ số của chúng.

Ví dụ:

```
function showName() {
  alert( arguments.length );
  alert( arguments[0] );
  alert( arguments[1] );

  // it's iterable
  // for(let arg of arguments) alert(arg);
}

// shows: 2, Julius, Caesar
showName("Julius", "Caesar");

// shows: 1, Ilya, undefined (no second argument)
showName("Ilya");
```

Ngày xưa, tham số rest không tồn tại trong ngôn ngữ, và sử dụng `arguments` là cách duy nhất để lấy tất cả đối số của function. Và nó vẫn hoạt động, chúng ta có thể tìm thấy nó trong code cũ.

Nhưng nhược điểm là mặc dù `arguments` vừa giống mảng vừa iterable, nó không phải là một mảng. Nó không hỗ trợ các phương thức mảng, vì vậy chúng ta không thể gọi `arguments.map(...)` ví dụ.

Ngoài ra, nó luôn chứa tất cả đối số. Chúng ta không thể thu thập một phần chúng, như chúng ta đã làm với tham số rest.

Vì vậy, khi chúng ta cần các tính năng này, tham số rest được ưu tiên.

Arrow function không có `"arguments"`

Nếu chúng ta truy cập object `arguments` từ một arrow function, nó lấy chúng từ function "bình thường" bên ngoài.

Đây là một ví dụ:

```
function f() {
  let showArg = () => alert(arguments[0]);
  showArg();
}

f(1); // 1
```

Như chúng ta nhớ, arrow function không có `this` riêng. Bây giờ chúng ta biết chúng cũng không có object `arguments` đặc biệt.

## [Cú pháp spread](#spread-syntax)

Chúng ta vừa thấy cách lấy một mảng từ danh sách các tham số.

Nhưng đôi khi chúng ta cần làm chính xác điều ngược lại.

Ví dụ, có một built-in function [Math.max](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/max) trả về số lớn nhất từ một danh sách:

```
alert( Math.max(3, 5, 1) ); // 5
```

Bây giờ hãy nói chúng ta có mảng `[3, 5, 1]`. Chúng ta gọi `Math.max` với nó như thế nào?

Truyền nó "nguyên trạng" sẽ không hoạt động, vì `Math.max` mong đợi một danh sách đối số số, không phải một mảng duy nhất:

```
let arr = [3, 5, 1];

alert( Math.max(arr) ); // NaN
```

Và chắc chắn chúng ta không thể liệt kê thủ công các mục trong code `Math.max(arr[0], arr[1], arr[2])`, vì chúng ta có thể không chắc có bao nhiêu. Khi script của chúng ta thực thi, có thể có rất nhiều, hoặc không có. Và điều đó sẽ trở nên xấu.

*Cú pháp spread* đến cứu! Nó trông giống tham số rest, cũng sử dụng `...`, nhưng làm điều ngược lại.

Khi `...arr` được sử dụng trong lời gọi function, nó "mở rộng" iterable object `arr` thành danh sách các đối số.

Cho `Math.max`:

```
let arr = [3, 5, 1];

alert( Math.max(...arr) ); // 5 (spread turns array into a list of arguments)
```

Chúng ta cũng có thể truyền nhiều iterable theo cách này:

```
let arr1 = [1, -2, 3, 4];
let arr2 = [8, 3, -8, 1];

alert( Math.max(...arr1, ...arr2) ); // 8
```

Chúng ta thậm chí có thể kết hợp cú pháp spread với các giá trị bình thường:

```
let arr1 = [1, -2, 3, 4];
let arr2 = [8, 3, -8, 1];

alert( Math.max(1, ...arr1, 2, ...arr2, 25) ); // 25
```

Ngoài ra, cú pháp spread có thể được sử dụng để merge các mảng:

```
let arr = [3, 5, 1];
let arr2 = [8, 9, 15];

let merged = [0, ...arr, 2, ...arr2];

alert(merged); // 0,3,5,1,2,8,9,15 (0, then arr, then 2, then arr2)
```

Trong các ví dụ ở trên chúng ta đã sử dụng mảng để minh họa cú pháp spread, nhưng bất kỳ iterable nào cũng được.

Ví dụ, ở đây chúng ta sử dụng cú pháp spread để biến một chuỗi thành mảng các ký tự:

```
let str = "Hello";

alert( [...str] ); // H,e,l,l,o
```

Cú pháp spread bên trong sử dụng iterator để thu thập các phần tử, giống như cách `for..of` làm.

Vì vậy, đối với một chuỗi, `for..of` trả về các ký tự và `...str` trở thành `"H","e","l","l","o"`. Danh sách các ký tự được truyền cho array initializer `[...str]`.

Đối với tác vụ cụ thể này chúng ta cũng có thể sử dụng `Array.from`, vì nó chuyển đổi một iterable (như chuỗi) thành một mảng:

```
let str = "Hello";

// Array.from converts an iterable into an array
alert( Array.from(str) ); // H,e,l,l,o
```

Kết quả giống như `[...str]`.

Nhưng có một khác biệt tinh tế giữa `Array.from(obj)` và `[...obj]`:

- `Array.from` hoạt động trên cả array-like và iterable.
- Cú pháp spread chỉ hoạt động với iterable.

Vì vậy, cho tác vụ biến một thứ gì đó thành mảng, `Array.from` có xu hướng phổ quát hơn.

## [Sao chép mảng/object](#copy-an-array-object)

Nhớ khi chúng ta nói về `Object.assign()` [trong quá khứ](/object-copy#cloning-and-merging-object-assign)?

Có thể làm điều tương tự với cú pháp spread.

```
let arr = [1, 2, 3];

let arrCopy = [...arr]; // spread the array into a list of parameters
                        // then put the result into a new array

// do the arrays have the same contents?
alert(JSON.stringify(arr) === JSON.stringify(arrCopy)); // true

// are the arrays equal?
alert(arr === arrCopy); // false (not same reference)

// modifying our initial array does not modify the copy:
arr.push(4);
alert(arr); // 1, 2, 3, 4
alert(arrCopy); // 1, 2, 3
```

Lưu ý rằng có thể làm điều tương tự để sao chép một object:

```
let obj = { a: 1, b: 2, c: 3 };

let objCopy = { ...obj }; // spread the object into a list of parameters
                          // then return the result in a new object

// do the objects have the same contents?
alert(JSON.stringify(obj) === JSON.stringify(objCopy)); // true

// are the objects equal?
alert(obj === objCopy); // false (not same reference)

// modifying our initial object does not modify the copy:
obj.d = 4;
alert(JSON.stringify(obj)); // {"a":1,"b":2,"c":3,"d":4}
alert(JSON.stringify(objCopy)); // {"a":1,"b":2,"c":3}
```

Cách sao chép object này ngắn hơn nhiều so với `let objCopy = Object.assign({}, obj)` hoặc cho mảng `let arrCopy = Object.assign([], arr)` vì vậy chúng ta thích sử dụng nó bất cứ khi nào có thể.

## [Tổng kết](#summary)

Khi chúng ta thấy `"..."` trong code, nó là tham số rest hoặc cú pháp spread.

Có một cách dễ để phân biệt giữa chúng:

- Khi `...` ở cuối tham số function, nó là "tham số rest" và thu thập phần còn lại của danh sách đối số vào một mảng.
- Khi `...` xuất hiện trong lời gọi function hoặc tương tự, nó được gọi là "cú pháp spread" và mở rộng một mảng thành danh sách.

Mẫu sử dụng:

- Tham số rest được sử dụng để tạo các function chấp nhận bất kỳ số lượng đối số nào.
- Cú pháp spread được sử dụng để truyền một mảng vào các function thường yêu cầu danh sách nhiều đối số.

Cùng nhau chúng giúp di chuyển dễ dàng giữa danh sách và mảng của các tham số.

Tất cả đối số của lời gọi function cũng có sẵn trong `arguments` kiểu cũ: array-like iterable object.
