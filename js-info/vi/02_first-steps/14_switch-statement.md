# Câu lệnh "switch"

> Nguồn: [https://javascript.info/switch](https://javascript.info/switch)

<!-- fetched: 2026-09-14 -->

Câu lệnh `switch` có thể thay thế nhiều câu lệnh `if` kiểm tra.

Nó cung cấp một cách mô tả hơn để so sánh một giá trị với nhiều biến thể.

## [Cú pháp](#the-syntax)

`switch` có một hoặc nhiều khối `case` và một `default` tùy chọn.

Nó trông như thế này:

```
switch(x) {
  case 'value1':  // nếu (x === 'value1')
    ...
    [break]

  case 'value2':  // nếu (x === 'value2')
    ...
    [break]

  default:
    ...
    [break]
}
```

- Giá trị của `x` được kiểm tra bằng strict equality với giá trị từ `case` đầu tiên (tức là, `value1`) sau đó đến `case` thứ hai (`value2`) và cứ thế.
- NếuEquality được tìm thấy, `switch` bắt đầu thực thi mã bắt đầu từ `case` tương ứng, cho đến `break` gần nhất (hoặc cho đến hết `switch`).
- Nếu không có `case` nào được khớp thì mã `default` được thực thi (nếu có).

## [Một ví dụ](#an-example)

Một ví dụ về `switch` (mã được thực thi được làm nổi bật):

```
let a = 2 + 2;

switch (a) {
  case 3:
    alert( 'Quá nhỏ' );
    break;
  case 4:
    alert( 'Chính xác!' );
    break;
  case 5:
    alert( 'Quá lớn' );
    break;
  default:
    alert( "Tôi không biết giá trị như vậy" );
}
```

Ở đây `switch` bắt đầu so sánh `a` từ `case` đầu tiên là `3`. Sự khớp thất bại.

Sau đó là `4`. Đó là một khớp, vì vậy việc thực thi bắt đầu từ `case 4` cho đến `break` gần nhất.

**Nếu không có `break` thì việc thực thi tiếp tục với `case` tiếp theo mà không có bất kỳ kiểm tra nào.**

Một ví dụ không có `break`:

```
let a = 2 + 2;

switch (a) {
  case 3:
    alert( 'Quá nhỏ' );
  case 4:
    alert( 'Chính xác!' );
  case 5:
    alert( 'Quá lớn' );
  default:
    alert( "Tôi không biết giá trị như vậy" );
}
```

Trong ví dụ trên, chúng ta sẽ thấy việc thực thi tuần tự của ba `alert`s:

```
alert( 'Chính xác!' );
alert( 'Quá lớn' );
alert( "Tôi không biết giá trị như vậy" );
```

Bất kỳ biểu thức nào cũng có thể là đối số `switch/case`

Cả `switch` và `case` đều cho phép các biểu thức tùy ý.

Vígiụ:

```
let a = "1";
let b = 0;

switch (+a) {
  case b + 1:
    alert("điều này chạy, vì +a là 1, chính xác bằng b+1");
    break;

  default:
    alert("điều này không chạy");
}
```

Ở đây `+a` cho `1`, được so sánh với `b + 1` trong `case`, và mã tương ứng được thực thi.

## [Nhóm các "case"](#grouping-of-case)

Nhiều biến thể của `case` chia sẻ cùng mã có thể được nhóm lại.

Vígiụ, nếu chúng ta muốn cùng mã chạy cho `case 3` và `case 5`:

```
let a = 3;

switch (a) {
  case 4:
    alert('Đúng!');
    break;

  case 3: // (*) nhóm hai cases
  case 5:
    alert('Sai!');
    alert("Sao bạn không học toán?");
    break;

  default:
    alert('Kết quả thật lạ. Thật sự.');
}
```

Bây giờ cả `3` và `5` đều hiển thị cùng thông điệp.

Khả năng "nhóm" các cases là một tác dụng phụ của cách `switch/case` hoạt động mà không có `break`. Ở đây, việc thực thi của `case 3` bắt đầu từ dòng `(*)` và đi qua `case 5`, vì không có `break`.

## [Kiểu quan trọng](#type-matters)

Hãy nhấn mạnh rằng phép kiểm tra bằng luôn là strict. Các giá trị phải cùng kiểu để khớp.

Vígiụ, hãy xem xét mã:

```
let arg = prompt("Nhập một giá trị?");
switch (arg) {
  case '0':
  case '1':
    alert( 'Một hoặc không' );
    break;

  case '2':
    alert( 'Hai' );
    break;

  case 3:
    alert( 'Không bao giờ chạy!' );
    break;
  default:
    alert( 'Một giá trị không biết' );
}
```

1. Đối với `0`, `1`, `alert` đầu tiên chạy.
2. Đối với `2` thì `alert` thứ hai chạy.
3. Nhưng đối với `3`, kết quả của `prompt` là chuỗi `"3"`, không bằng strict `===` với số `3`. Vì vậy chúng ta có mã chết trong `case 3`! Biến thể `default` sẽ thực thi.

---

---

## Các bài tập

## [Các bài tập](#tasks)

### [Viết lại "switch" thành "if"](#rewrite-the-switch-into-an-if)

mức độ quan trọng: 5

Viết mã sử dụng `if..else` sẽ tương ứng với `switch` sau:

```
switch (browser) {
  case 'Edge':
    alert( "Bạn có Edge!" );
    break;

  case 'Chrome':
  case 'Firefox':
  case 'Safari':
  case 'Opera':
    alert( 'Okay, chúng tôi cũng hỗ trợ các trình duyệt này' );
    break;

  default:
    alert( 'Chúng tôi hy vọng trang này trông ok!' );
}
```

lời giải

Để khớp chính xác chức năng của `switch`, `if` phải sử dụng phép so sánh strict `'==='`.

Tuy nhiên, đối với các chuỗi đã cho, đơn giản `'=='` cũng hoạt động.

```
if(browser == 'Edge') {
  alert("Bạn có Edge!");
} else if (browser == 'Chrome'
 || browser == 'Firefox'
 || browser == 'Safari'
 || browser == 'Opera') {
  alert( 'Okay, chúng tôi cũng hỗ trợ các trình duyệt này' );
} else {
  alert( 'Chúng tôi hy vọng trang này trông ok!' );
}
```

Xin lưu ý: cấu trúc `browser == 'Chrome' || browser == 'Firefox' …` được chia thành nhiều dòng để dễ đọc hơn.

Nhưng cấu trúc `switch` vẫn sạch sẽ và mô tả hơn.

### [Viết lại "if" thành "switch"](#rewrite-if-into-switch)

mức độ quan trọng: 4

Viết lại mã dưới đây bằng cách sử dụng một câu lệnh `switch` duy nhất:

```
let a = +prompt('a?', '');

if (a == 0) {
  alert( 0 );
}
if (a == 1) {
  alert( 1 );
}

if (a == 2 || a == 3) {
  alert( '2,3' );
}
```

lời giải

Hai kiểm tra đầu tiên trở thành hai `case`. Kiểm tra thứ ba được chia thành hai cases:

```
let a = +prompt('a?', '');

switch (a) {
  case 0:
    alert( 0 );
    break;

  case 1:
    alert( 1 );
    break;

  case 2:
  case 3:
    alert( '2,3' );
    break;
}
```

Xin lưu ý: `break` ở cuối không bắt buộc. Nhưng chúng ta đặt nó để làm cho mã an toàn về sau.

Trong tương lai, có khả năng chúng ta sẽ muốn thêm một `case` nữa, ví dụ `case 4`. Và nếu chúng ta quên thêm break trước nó, ở cuối `case 3`, sẽ có lỗi. Đó là một dạng tự bảo vệ.
