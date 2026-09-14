# Điều kiện rẽ nhánh: if, '?'

> Nguồn: [https://javascript.info/ifelse](https://javascript.info/ifelse)

<!-- fetched: 2026-09-14 -->

Đôi khi, chúng ta cần thực hiện các hành động khác nhau dựa trên các điều kiện khác nhau.

Để làm điều đó, chúng ta có thể sử dụng câu lệnh `if` và toán tử có điều kiện `?`, còn được gọi là toán tử “dấu chấm hỏi”.

## [Câu lệnh “if”](#the-if-statement)

Câu lệnh `if(...)` đánh giá một điều kiện trong dấu ngoặc đơn và, nếu kết quả là `true`, thực thi một khối mã.

Ví dụ:

```
let year = prompt('Năm nào ECMAScript-2015 specification được publish?', '');

if (year == 2015) alert( 'Bạn đúng!' );
```

Trong ví dụ trên, điều kiện là một phép kiểm tra bằng đơn giản (`year == 2015`), nhưng nó có thể phức tạp hơn nhiều.

Nếu chúng ta muốn thực thi nhiều hơn một câu lệnh, chúng ta phải bao quanh khối mã của chúng ta trong dấu ngoặc nhọn:

```
if (year == 2015) {
  alert( "Đúng rồi!" );
  alert( "Bạn thông minh quá!" );
}
```

Chúng ta khuyến nghị bao quanh khối mã của bạn với dấu ngoặc nhọn `{}` mỗi khi bạn sử dụng một câu lệnh `if`, ngay cả khi chỉ có một câu lệnh để thực thi. Làm như vậy cải thiện khả năng đọc.

## [Chuyển đổi Boolean](#boolean-conversion)

Câu lệnh `if (…)` đánh giá biểu thức trong dấu ngoặc đơn của nó và chuyển đổi kết quả thành boolean.

Hãy nhớ lại các quy tắc chuyển đổi từ chương [Chuyển đổi kiểu](/type-conversions):

- Một số `0`, chuỗi rỗng `""`, `null`, `undefined`, và `NaN` đều trở thành `false`. Vì lý do đó chúng được gọi là các giá trị “falsy”.
- Các giá trị khác trở thành `true`, vì vậy chúng được gọi là “truthy”.

Vì vậy, mã bên dưới điều kiện này sẽ không bao giờ thực thi:

```
if (0) { // 0 là falsy
  ...
}
```

…và bên trong điều kiện này – nó luôn luôn:

```
if (1) { // 1 là truthy
  ...
}
```

Chúng ta cũng có thể chuyển một giá trị boolean đã được đánh giá trước đến `if`, như thế này:

```
let cond = (year == 2015); // equality evaluates to true or false

if (cond) {
  ...
}
```

## [Clause “else”](#the-else-clause)

Câu lệnh `if` có thể chứa một khối `else` tùy chọn. Nó thực thi khi điều kiện là falsy.

Ví dụ:

```
let year = prompt('Năm nào ECMAScript-2015 specification được publish?', '');

if (year == 2015) {
  alert( 'Bạn đoán đúng!' );
} else {
  alert( 'Làm sao bạn có thể sai được?' ); // bất kỳ giá trị nào trừ 2015
}
```

## [Nhiều điều kiện: “else if”](#several-conditions-else-if)

Đôi khi, chúng ta muốn kiểm tra nhiều biến thể của một điều kiện. Clause `else if` cho phép chúng ta làm điều đó.

Ví dụ:

```
let year = prompt('Năm nào ECMAScript-2015 specification được publish?', '');

if (year < 2015) {
  alert( 'Sớm quá...' );
} else if (year > 2015) {
  alert( 'Muộn quá' );
} else {
  alert( 'Chính xác!' );
}
```

Trong mã ở trên, JavaScript đầu tiên kiểm tra `year < 2015`. Nếu điều đó là falsy, nó chuyển sang điều kiện tiếp theo `year > 2015`. Nếu điều đó cũng là falsy, nó hiển thị `alert` cuối cùng.

Có thể có nhiều khối `else if`. `else` cuối cùng là tùy chọn.

## [Toán tử có điều kiện ‘?’](#conditional-operator)

Đôi khi, chúng ta cần gán một biến tùy thuộc vào một điều kiện.

Ví dụ:

```
let accessAllowed;
let age = prompt('Bạn bao nhiêu tuổi?', '');

if (age > 18) {
  accessAllowed = true;
} else {
  accessAllowed = false;
}

alert(accessAllowed);
```

Toán tử được gọi là “conditional” hoặc “question mark” cho phép chúng ta làm điều đó theo cách ngắn gọn và đơn giản hơn.

Toán tử được biểu diễn bằng dấu chấm hỏi `?`. Đôi khi nó được gọi là “ternary”, vì toán tử có ba operand. Nó thực sự là toán tử duy nhất trong JavaScript có nhiều như vậy.

Cú pháp là:

```
let result = condition ? value1 : value2;
```

`condition` được đánh giá: nếu nó truthy thì `value1` được trả về, nếu không – `value2`.

Ví dụ:

```
let accessAllowed = (age > 18) ? true : false;
```

Về mặt kỹ thuật, chúng ta có thể bỏ qua dấu ngoặc đơn xung quanh `age > 18`. Toán tử dấu chấm hỏi có độ ưu tiên thấp, vì vậy nó thực thi sau phép so sánh `>`.

Ví dụ này sẽ làm cùng một điều như cái trước:

```
// toán tử so sánh "age > 18" thực thi trước bất kể
// (không cần bao quanh nó trong dấu ngoặc đơn)
let accessAllowed = age > 18 ? true : false;
```

Nhưng dấu ngoặc đơn làm cho mã dễ đọc hơn, vì vậy chúng ta khuyến nghị sử dụng chúng.

Xin lưu ý:

Trong ví dụ ở trên, bạn có thể tránh sử dụng toán tử dấu chấm hỏi vì phép so sánh tự nó trả về `true/false`:

```
// giống nhau
let accessAllowed = age > 18;
```

## [Nhiều ‘?’](#multiple)

Một chuỗi các toán tử dấu chấm hỏi `?` có thể trả về một giá trị phụ thuộc vào nhiều hơn một điều kiện.

Ví dụ:

```
let age = prompt('tuổi?', 18);

let message = (age < 3) ? 'Chào bé!' :
  (age < 18) ? 'Xin chào!' :
  (age < 100) ? ' greetings!' :
  'Tuổi thật lạ!'

alert( message );
```

Có thể khó hiểu những gì đang xảy ra ban đầu. Nhưng sau khi nhìn kỹ hơn, chúng ta có thể thấy rằng đó chỉ là một chuỗi test thông thường:

1. Dấu chấm hỏi đầu tiên kiểm tra xem `age < 3`.
2. Nếu true – nó trả về `'Chào bé!'`. Ngược lại, nó tiếp tục đến biểu thức sau dấu hai chấm “:”, kiểm tra `age < 18`.
3. Nếu đó là true – nó trả về `'Xin chào!'`. Ngược lại, nó tiếp tục đến biểu thức sau dấu hai chấm tiếp theo “:”, kiểm tra `age < 100`.
4. Nếu đó là true – nó trả về `'Greetings!'`. Ngược lại, nó tiếp tục đến biểu thức sau dấu hai chấm cuối cùng “:”, trả về `'Tuổi thật lạ!'`.

Đây là cách nó trông bằng cách sử dụng `if..else`:

```
if (age < 3) {
  message = 'Chào bé!';
} else if (age < 18) {
  message = 'Xin chào!';
} else if (age < 100) {
  message = 'Greetings!';
} else {
  message = 'Tuổi thật lạ!';
}
```

## [Sử dụng không truyền thống của ‘?’](#non-traditional-use-of)

Đôi khi dấu chấm hỏi `?` được sử dụng như một sự thay thế cho `if`:

```
let company = prompt('Công ty nào tạo ra JavaScript?', '');

(company == 'Netscape') ?
   alert('Đúng!') : alert('Sai.');
```

Tùy thuộc vào điều kiện `company == 'Netscape'`, either biểu thức đầu tiên hoặc thứ hai sau `?` được thực thi và hiển thị alert.

Chúng ta không gán kết quả cho một biến ở đây. Thay vào đó, chúng ta thực thi các mã khác nhau tùy thuộc vào điều kiện.

**Không nên sử dụng toán tử dấu chấm hỏi theo cách này.**

Ký hiệu ngắn hơn câu lệnh `if` tương đương, điều này thu hút một số lập trình viên. Nhưng nó ít dễ đọc hơn.

Đây là cùng mã sử dụng `if` để so sánh:

```
let company = prompt('Công ty nào tạo ra JavaScript?', '');

if (company == 'Netscape') {
  alert('Đúng!');
} else {
  alert('Sai.');
}
```

Mắt chúng ta quét mã theo chiều dọc. Các khối mã trải dài qua nhiều dòng dễ hiểu hơn một tập lệnh hướng ngang dài.

Mục đích của toán tử dấu chấm hỏi `?` là trả về một giá trị hoặc giá trị khác tùy thuộc vào điều kiện của nó. Xin hãy sử dụng nó cho chính xác mục đích đó. Sử dụng `if` khi bạn cần thực thi các nhánh mã khác nhau.

---

---

## Các bài tập

## [Các bài tập](#tasks)

### [if (một chuỗi với không)](#if-a-string-with-zero)

mức độ quan trọng: 5

`alert` có được hiển thị không?

```
if ("0") {
  alert( 'Xin chào' );
}
```

lời giải

**Có, nó sẽ.**

Bất kỳ chuỗi nào ngoại trừ chuỗi rỗng (và `"0"` không trống) trở thành `true` trong ngữ cảnh logic.

Chúng ta có thể chạy và kiểm tra:

```
if ("0") {
  alert( 'Xin chào' );
}
```

### [Tên của JavaScript](#the-name-of-javascript)

mức độ quan trọng: 2

Sử dụng cấu trúc `if..else`, viết mã yêu cầu: ‘Tên “chính thức” của JavaScript là gì?’

Nếu người truy cập nhập “ECMAScript”, thì output “Đúng!”, ngược lại – output: “Bạn không biết? ECMAScript!”

![](/task/check-standard/ifelse_task2.svg)

[Demo trong cửa sổ mới](https://en.js.cx/task/check-standard/ifelse_task2/)

lời giải

```
<!DOCTYPE html>
<html>

<body>
  <script>
    'use strict';

    let value = prompt('Tên "chính thức" của JavaScript là gì?', '');

    if (value == 'ECMAScript') {
      alert('Đúng!');
    } else {
      alert("Bạn không biết? ECMAScript!");
    }
  </script>

</body>

</html>
```

### [Hiển thị dấu](#show-the-sign)

mức độ quan trọng: 2

Sử dụng `if..else`, viết mã nhận một số thông qua `prompt` và sau đó hiển thị trong `alert`:

- `1`, nếu giá trị lớn hơn không,
- `-1`, nếu nhỏ hơn không,
- `0`, nếu bằng không.

Trong task này chúng ta giả sử rằng input luôn là một số.

[Demo trong cửa sổ mới](https://en.js.cx/task/sign/if_sign/)

lời giải

```
let value = prompt('Nhập một số', 0);

if (value > 0) {
  alert( 1 );
} else if (value < 0) {
  alert( -1 );
} else {
  alert( 0 );
}
```

### [Viết lại 'if' thành '?'](#rewrite-if-into)

mức độ quan trọng: 5

Viết lại `if` này bằng toán tử có điều kiện `'?'`:

```
let result;

if (a + b < 4) {
  result = 'Dưới';
} else {
  result = 'Trên';
}
```

lời giải

```
let result = (a + b < 4) ? 'Dưới' : 'Trên';
```

### [Viết lại 'if..else' thành '?'](#rewrite-if-else-into)

mức độ quan trọng: 5

Viết lại `if..else` bằng cách sử dụng nhiều toán tử ternary `'?'`.

Để dễ đọc, nên chia mã thành nhiều dòng.

```
let message;

if (login == 'Employee') {
  message = 'Xin chào';
} else if (login == 'Director') {
  message = 'Greetings';
} else if (login == '') {
  message = 'Không có login';
} else {
  message = '';
}
```

lời giải

```
let message = (login == 'Employee') ? 'Xin chào' :
  (login == 'Director') ? 'Greetings' :
  (login == '') ? 'Không có login' :
  '';
```
