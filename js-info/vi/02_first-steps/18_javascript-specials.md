# Các điểm đặc biệt của JavaScript

> Nguồn: [https://javascript.info/javascript-specials](https://javascript.info/javascript-specials)

<!-- fetched: 2026-09-14 -->

Chương này tóm tắt nhanh các tính năng của JavaScript mà chúng ta đã học cho đến nay, đặc biệt chú ý đến các thời điểm tinh tế.

## [Cấu trúc mã](#code-structure)

Các câu lệnh được phân tách bằng dấu chấm phẩy:

```
alert('Xin chào'); alert('Thế giới');
```

Thông thường, một ngắt dòng cũng được coi là trình phân tách, vì vậy điều này cũng hoạt động:

```
alert('Xin chào')
alert('Thế giới')
```

Điều đó được gọi là "automatic semicolon insertion". Đôi khi nó không hoạt động, vígiụ:

```
alert("Sẽ có lỗi sau thông điệp này")

[1, 2].forEach(alert)
```

Hầu hết các hướng dẫn style mã đồng ý rằng chúng ta nên đặt dấu chấm phẩy sau mỗi câu lệnh.

Dấu chấm phẩy không bắt buộc sau các khối mã `{...}` và các cấu trúc cú pháp có chúng như vòng lặp:

```
function f() {
  // không cần dấu chấm phẩy sau khai báo hàm
}

for(;;) {
  // không cần dấu chấm phẩy sau vòng lặp
}
```

…Nhưng ngay cả khi chúng ta có thể đặt một dấu chấm phẩy "thêm" ở đâu đó, đó không phải là lỗi. Nó sẽ bị bỏ qua.

Thêm trong: [Cấu trúc mã](/structure).

## [Chế độ strict](#strict-mode)

Để kích hoạt đầy đủ tất cả các tính năng của JavaScript hiện đại, chúng ta nên bắt đầu scripts với `"use strict"`.

```
'use strict';

...
```

Chỉ thị phải ở đầu script hoặc ở đầu thân hàm.

Không có `"use strict"`, mọi thứ vẫn hoạt động, nhưng một số tính năng hoạt động theo cách cũ, "tương thích". Chúng ta thường thích hành vi hiện đại hơn.

Một số tính năng hiện đại của ngôn ngữ (như classes mà chúng ta sẽ học trong tương lai) kích hoạt chế độ strict một cách ngầm định.

Thêm trong: [Chế độ hiện đại, "use strict"](/strict-mode).

## [Biến](#variables)

Có thể được khai báo bằng:

- `let`
- `const` (constant, không thể thay đổi)
- `var` (cũ, sẽ xem sau)

Tên biến có thể bao gồm:

- Chữ cái và chữ số, nhưng ký tự đầu tiên không thể là chữ số.
- Các ký tự `$` và `_` là bình thường, ngang hàng với chữ cái.
- Bảng chữ cái không Latin và hieroglyphs cũng được phép, nhưng thường không được sử dụng.

Các biến được gõ động. Chúng có thể lưu trữ bất kỳ giá trị nào:

```
let x = 5;
x = "John";
```

Có 8 kiểu dữ liệu:

- `number` cho cả số floating-point và số nguyên,
- `bigint` cho các số nguyên có độ dài tùy ý,
- `string` cho chuỗi,
- `boolean` cho các giá trị logic: `true/false`,
- `null` – một kiểu với một giá trị duy nhất `null`, có nghĩa là "trống" hoặc "không tồn tại",
- `undefined` – một kiểu với một giá trị duy nhất `undefined`, có nghĩa là "chưa được gán",
- `object` và `symbol` – cho các cấu trúc dữ liệu phức tạp và các định danh duy nhất, chúng ta chưa học chúng.

Toán tử `typeof` trả về kiểu cho một giá trị, với hai ngoại lệ:

```
typeof null == "object" // lỗi trong ngôn ngữ
typeof function(){} == "function" // các hàm được xử lý đặc biệt
```

Thêm trong: [Biến](/variables) và [Kiểu dữ liệu](/types).

## [Tương tác](#interaction)

Chúng ta đang sử dụng trình duyệt như một môi trường làm việc, vì vậy các hàm UI cơ bản sẽ là:

[`prompt(question, [default])`](https://developer.mozilla.org/en-US/docs/Web/API/Window/prompt)
:   Hỏi một `question`, và trả về những gì người truy cập đã nhập hoặc `null` nếu họ đã nhấn "cancel".

[`confirm(question)`](https://developer.mozilla.org/en-US/docs/Web/API/Window/confirm)
:   Hỏi một `question` và đề xuất chọn giữa Ok và Cancel. Lựa chọn được trả về dưới dạng `true/false`.

[`alert(message)`](https://developer.mozilla.org/en-US/docs/Web/API/Window/alert)
:   Xuất một `message`.

Tất cả các hàm này là *modal*, chúng tạm dừng việc thực thi mã và ngăn người truy cập tương tác với trang cho đến khi họ trả lời.

Vígiụ:

```
let userName = prompt("Tên của bạn?", "Alice");
let isTeaWanted = confirm("Bạn có muốn uống trà không?");

alert( "Khách: " + userName ); // Alice
alert( "Trà muốn: " + isTeaWanted ); // true
```

Thêm trong: [Tương tác: alert, prompt, confirm](/alert-prompt-confirm).

## [Các toán tử](#operators)

JavaScript hỗ trợ các toán tử sau:

Arithmetical
:   Thông thường: `* + - /`, cũng có `%` cho phần dư và `**` cho lũy thừa của một số.

    Dấu cộng binary `+` nối chuỗi. Và nếu bất kỳ toán hạng nào là chuỗi, toán hạng còn lại được chuyển đổi sang chuỗi:

    ```
    alert( '1' + 2 ); // '12', chuỗi
    alert( 1 + '2' ); // '12', chuỗi
    ```

Assignments
:   Có phép gán đơn giản: `a = b` và các phép gán kết hợp như `a *= 2`.

Bitwise
:   Các toán tử bitwise làm việc với các số nguyên 32-bit ở mức thấp nhất, bit-level: xem [docs](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Expressions_and_Operators#bitwise_operators) khi cần.

Conditional
:   Toán tử duy nhất với ba tham số: `cond ? resultA : resultB`. Nếu `cond` là truthy, trả về `resultA`, nếu không thì `resultB`.

Logical operators
:   Logical AND `&&` và OR `||` thực hiện short-circuit evaluation và sau đó trả về giá trị nơi nó dừng lại (không cần thiết `true`/`false`). Logical NOT `!` chuyển đổi toán hạng sang kiểu boolean và trả về giá trị đảo ngược.

Nullish coalescing operator
:   Toán tử `??` cung cấp một cách để chọn một giá trị có giá trị từ một danh sách các biến. Kết quả của `a ?? b` là `a` trừ khi nó là `null/undefined`, sau đó là `b`.

Comparisons
:   Phép kiểm tra bằng `==` cho các giá trị của các kiểu khác nhau chuyển đổi chúng thành số (ngoại trừ `null` và `undefined` bằng nhau và không bằng bất kỳ giá trị nào khác), vì vậy những cái này bằng nhau:

    ```
    alert( 0 == false ); // true
    alert( 0 == '' ); // true
    ```

    Các phép so sánh khác cũng chuyển đổi sang số.

    Toán tử bằngstrict `===` không thực hiện chuyển đổi: các kiểu khác nhau luôn có nghĩa là các giá trị khác nhau đối với nó.

    Các giá trị `null` và `undefined` là đặc biệt: chúng bằng `==` nhau và không bằng bất kỳ giá trị nào khác.

    Các phép so sánh lớn hơn/nhỏ hơn so sánh chuỗi ký tự theo ký tự, các kiểu khác được chuyển đổi thành số.

Other operators
:   Có một vài cái khác, như toán tử dấu phẩy.

Thêm trong: [Các toán tử cơ bản, toán học](/operators), [So sánh](/comparison), [Các toán tử logic](/logical-operators), [Toán tử ghép không rỗng '??']( /nullish-coalescing-operator).

## [Các vòng lặp](#loops)

- Chúng ta đã bao quát 3 loại vòng lặp:

  ```
  // 1
  while (condition) {
    ...
  }

  // 2
  do {
    ...
  } while (condition);

  // 3
  for(let i = 0; i < 10; i++) {
    ...
  }
  ```
- Biến được khai báo trong vòng lặp `for(let...)` chỉ hiển thị bên trong vòng lặp. Nhưng chúng ta cũng có thể bỏ qua `let` và tái sử dụng một biến đã tồn tại.
- Các chỉ thị `break/continue` cho phép thoát khỏi toàn bộ vòng lặp/lần lặp hiện tại. Sử dụng labels để phá vỡ các vòng lặp lồng nhau.

Chi tiết trong: [Các vòng lặp: while và for](/while-for).

Sau đó chúng ta sẽ nghiên cứu thêm các loại vòng lặp để xử lý các object.

## [Cấu trúc "switch"](#the-switch-construct)

Cấu trúc "switch" có thể thay thế nhiều câu lệnh `if` kiểm tra. Nó sử dụng `===` (bằngstrict) cho các phép so sánh.

Vígiụ:

```
let age = prompt('Tuổi của bạn?', 18);

switch (age) {
  case 18:
    alert("Không hoạt động"); // kết quả của prompt là chuỗi, không phải số
    break;

  case "18":
    alert("Cái này hoạt động!");
    break;

  default:
    alert("Bất kỳ giá trị nào không bằng một trong các giá trị ở trên");
}
```

Chi tiết trong: [Câu lệnh "switch"]( /switch).

## [Hàm](#functions)

Chúng ta đã bao quát ba cách để tạo một hàm trong JavaScript:

1. Function Declaration: hàm trong luồng mã chính

   ```
   function sum(a, b) {
     let result = a + b;

     return result;
   }
   ```
2. Function Expression: hàm trong ngữ cảnh của một biểu thức

   ```
   let sum = function(a, b) {
     let result = a + b;

     return result;
   };
   ```
3. Arrow functions:

   ```
   // biểu thức ở phía bên phải
   let sum = (a, b) => a + b;

   // hoặc cú pháp nhiều dòng với { ... }, cần return ở đây:
   let sum = (a, b) => {
     // ...
     return a + b;
   }

   // không có đối số
   let sayHi = () => alert("Xin chào");

   // với một đối số duy nhất
   let double = n => n * 2;
   ```

- Các hàm có thể có các biến cục bộ: những biến được khai báo bên trong thân của nó hoặc danh sách tham số của nó. Các biến như vậy chỉ hiển thị bên trong hàm.
- Các tham số có thể có giá trị mặc định: `function sum(a = 1, b = 2) {...}`.
- Các hàm luôn trả về một cái gì đó. Nếu không có câu lệnh `return`, thì kết quả là `undefined`.

Chi tiết: xem [Hàm](/function-basics), [Arrow functions, các cơ bản](/arrow-functions-basics).

## [Nhiều hơn sắp tới](#more-to-come)

Đó là một danh sách ngắn gọn về các tính năng của JavaScript. Tính đến nay chúng ta đã chỉ học các cơ bản. Tiếp theo trong hướng dẫn, bạn sẽ tìm thấy nhiều điểm đặc biệt và tính năng nâng cao hơn của JavaScript.
