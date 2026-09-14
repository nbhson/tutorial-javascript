# Vòng lặp: while và for

> Nguồn: [https://javascript.info/while-for](https://javascript.info/while-for)

<!-- fetched: 2026-09-14 -->

Chúng ta thường cần lặp lại các hành động.

Ví dụ, xuất các mặt hàng từ một danh sách này sang mặt hàng khác hoặc chỉ chạy cùng mã cho mỗi số từ 1 đến 10.

*Vòng lặp* là một cách để lặp lại cùng mã nhiều lần.

Các vòng lặp for…of và for…in

Một thông báo nhỏ cho người đọc nâng cao.

Bài viết này chỉ bao gồm các vòng lặp cơ bản: `while`, `do..while` và `for(..;..;..)`.

Nếu bạn đang tìm kiếm các loại vòng lặp khác, hãy xem:

- Xem [for…in](/object#forin) để lặp qua các thuộc tính của object.
- Xem [for…of](/array#loops) và [iterables](/iterable) để lặp qua arrays và các object có thể lặp.

Nếu không, xin vui lòng đọc tiếp.

## [Vòng lặp "while"](#the-while-loop)

Vòng lặp `while` có cú pháp sau:

```
while (condition) {
  // code
  // gọi là "thân vòng lặp"
}
```

Trong khi `condition` là truthy, `code` từ thân vòng lặp được thực thi.

Vígiụ, vòng lặp dưới đây xuất `i` trong khi `i < 3`:

```
let i = 0;
while (i < 3) { // hiển thị 0, sau đó 1, sau đó 2
  alert( i );
  i++;
}
```

Một lần thực thi thân vòng lặp được gọi là *một lần lặp*. Vòng lặp trong ví dụ trên thực hiện ba lần lặp.

Nếu `i++` bị thiếu trong ví dụ trên, vòng lặp sẽ lặp lại (về lý thuyết) mãi mãi. Trên thực tế, trình duyệt cung cấp các cách để dừng các vòng lặp như vậy, và trong JavaScript phía server, chúng ta có thể kill tiến trình.

Bất kỳ biểu thức hoặc biến nào cũng có thể là điều kiện vòng lặp, không chỉ các phép so sánh: điều kiện được đánh giá và chuyển đổi sang boolean bởi `while`.

Vígiụ, một cách ngắn gọn hơn để viết `while (i != 0)` là `while (i)`:

```
let i = 3;
while (i) { // khi i trở thành 0, điều kiện trở thành falsy, và vòng lặp dừng
  alert( i );
  i--;
}
```

Dấu ngoặc nhọn không bắt buộc cho thân một dòng

Nếu thân vòng lặp có một câu lệnh, chúng ta có thể bỏ qua dấu ngoặc nhọn `{…}`:

```
let i = 3;
while (i) alert(i--);
```

## [Vòng lặp "do…while"](#the-do-while-loop)

Kiểm tra điều kiện có thể được chuyển *bên dưới* thân vòng lặp bằng cách sử dụng cú pháp `do..while`:

```
do {
  // thân vòng lặp
} while (condition);
```

Vòng lặp trước tiên sẽ thực thi thân, sau đó kiểm tra điều kiện, và, trong khi nó là truthy, thực thi lại và lại nữa.

Vígiụ:

```
let i = 0;
do {
  alert( i );
  i++;
} while (i < 3);
```

Dạng cú pháp này chỉ nên được sử dụng khi bạn muốn thân vòng lặp thực thi **ít nhất một lần** bất kể điều kiện có truthy hay không. Thông thường, dạng khác được ưu tiên hơn: `while(…) {…}`.

## [Vòng lặp "for"](#the-for-loop)

Vòng lặp `for` phức tạp hơn, nhưng nó cũng là vòng lặp được sử dụng phổ biến nhất.

Nó trông như thế này:

```
for (begin; condition; step) {
  // ... thân vòng lặp ...
}
```

Hãy tìm hiểu ý nghĩa của các phần này bằng ví dụ. Vòng lặp dưới đây chạy `alert(i)` cho `i` từ `0` lên đến (nhưng không bao gồm) `3`:

```
for (let i = 0; i < 3; i++) { // hiển thị 0, sau đó 1, sau đó 2
  alert(i);
}
```

Hãy xem xét câu lệnh `for` từng phần:

| phần |  |  |
| --- | --- | --- |
| begin | `let i = 0` | Thực thi một lần khi vào vòng lặp. |
| condition | `i < 3` | Được kiểm tra trước mỗi lần lặp vòng lặp. Nếu false, vòng lặp dừng. |
| body | `alert(i)` | Chạy liên tục trong khi điều kiện là truthy. |
| step | `i++` | Thực thi sau thân vòng lặp ở mỗi lần lặp. |

Thuật toán vòng lặp tổng quát hoạt động như sau:

```
Chạy begin
→ (nếu condition → chạy body và chạy step)
→ (nếu condition → chạy body và chạy step)
→ (nếu condition → chạy body và chạy step)
→ ...
```

Tức là, `begin` thực thi một lần, và sau đó nó lặp lại: sau mỗi lần kiểm tra `condition`, `body` và `step` được thực thi.

Nếu bạn mới làm quen với vòng lặp, nó có thể hữu ích nếu quay lại ví dụ và mô phỏng cách nó chạy từng bước trên một tờ giấy.

Đây chính xác là những gì xảy ra trong trường hợp của chúng ta:

```
// for (let i = 0; i < 3; i++) alert(i)

// chạy begin
let i = 0
// nếu condition → chạy body và chạy step
if (i < 3) { alert(i); i++ }
// nếu condition → chạy body và chạy step
if (i < 3) { alert(i); i++ }
// nếu condition → chạy body và chạy step
if (i < 3) { alert(i); i++ }
// ...dừng, vì bây giờ i == 3
```

Khai báo biến inline

Ở đây, biến "bộ đếm" `i` được khai báo ngay trong vòng lặp. Điều này được gọi là khai báo biến "inline". Các biến như vậy chỉ hiển thị trong vòng lặp.

```
for (let i = 0; i < 3; i++) {
  alert(i); // 0, 1, 2
}
alert(i); // lỗi, không có biến như vậy
```

Thay vì định nghĩa một biến, chúng ta có thể sử dụng một biến đã tồn tại:

```
let i = 0;

for (i = 0; i < 3; i++) { // sử dụng biến đã tồn tại
  alert(i); // 0, 1, 2
}

alert(i); // 3, hiển thị, vì được khai báo bên ngoài vòng lặp
```

### [Bỏ qua các phần](#skipping-parts)

Bất kỳ phần nào của `for` cũng có thể bị bỏ qua.

Vígiụ, chúng ta có thể bỏ qua `begin` nếu chúng ta không cần làm gì đó khi bắt đầu vòng lặp.

Như ở đây:

```
let i = 0; // chúng ta đã có i được khai báo và gán

for (; i < 3; i++) { // không cần "begin"
  alert( i ); // 0, 1, 2
}
```

Chúng ta cũng có thể xóa phần `step`:

```
let i = 0;

for (; i < 3;) {
  alert( i++ );
}
```

Điều này làm cho vòng lặp giống hệt `while (i < 3)`.

Thực tế, chúng ta có thể xóa tất cả, tạo ra một vòng lặp vô hạn:

```
for (;;) {
  // lặp lại không giới hạn
}
```

Xin lưu ý rằng hai dấu chấm phẩy `;` của `for` phải có mặt. Nếu không sẽ có lỗi cú pháp.

## [Dừng vòng lặp](#breaking-the-loop)

Thông thường, vòng lặp thoát khi điều kiện của nó trở thành falsy.

Nhưng chúng ta có thể buộc thoát bất cứ lúc nào bằng cách sử dụng chỉ thị đặc biệt `break`.

Vígiụ, vòng lặp dưới đây yêu cầu người dùng nhập một loạt các số, "dừng" khi không có số nào được nhập:

```
let sum = 0;

while (true) {

  let value = +prompt("Nhập một số", '');

  if (!value) break; // (*)

  sum += value;

}
alert( 'Tổng: ' + sum );
```

Chỉ thị `break` được kích hoạt ở dòng `(*)` nếu người dùng nhập dòng trống hoặc hủy input. Nó dừng vòng lặp ngay lập tức, chuyển quyền kiểm soát đến dòng đầu tiên sau vòng lặp. Cụ thể là `alert`.

Sự kết hợp "vòng lặp vô hạn + `break` khi cần" rất tuyệt vời cho các tình huống khi điều kiện của vòng lặp phải được kiểm tra không phải ở đầu hoặc cuối vòng lặp, mà ở giữa hoặc thậm chí ở nhiều nơi trong thân của nó.

## [Tiếp tục đến lần lặp tiếp theo](#continue)

Chỉ thị `continue` là "phiên bản nhẹ hơn" của `break`. Nó không dừng toàn bộ vòng lặp. Thay vào đó, nó dừng lần lặp hiện tại và buộc vòng lặp bắt đầu một lần lặp mới (nếu điều kiện cho phép).

Chúng ta có thể sử dụng nó nếu chúng ta đã làm xong với lần lặp hiện tại và muốn chuyển sang lần lặp tiếp theo.

Vòng lặp dưới đây sử dụng `continue` để chỉ xuất các giá trị lẻ:

```
for (let i = 0; i < 10; i++) {

  // nếu true, bỏ qua phần còn lại của thân
  if (i % 2 == 0) continue;

  alert(i); // 1, sau đó 3, 5, 7, 9
}
```

Đối với các giá trị chẵn của `i`, chỉ thị `continue` dừng việc thực thi thân và chuyển quyền kiểm soát sang lần lặp tiếp theo của `for` (với số tiếp theo). Vì vậy, `alert` chỉ được gọi cho các giá trị lẻ.

`continue` giúp giảm độ lồng nhau

Một vòng lặp hiển thị các giá trị lẻ có thể trông như thế này:

```
for (let i = 0; i < 10; i++) {

  if (i % 2) {
    alert( i );
  }

}
```

Về mặt kỹ thuật, điều này giống hệt với ví dụ trên. Chắc chắn, chúng ta có thể chỉ cần bọc mã trong khối `if` thay vì sử dụng `continue`.

Nhưng như một tác dụng phụ, điều này tạo ra một mức độ lồng nhau nữa (lệnh gọi `alert` bên trong dấu ngoặc nhọn). Nếu mã bên trong `if` dài hơn một vài dòng, điều đó có thể làm giảm khả năng đọc tổng thể.

Không `break/continue` ở phía bên phải của '?'

Xin lưu ý rằng các cấu trúc cú pháp không phải là biểu thức không thể được sử dụng với toán tử tam phân `?`. Cụ thể, các chỉ thị như `break/continue` không được phép ở đó.

Vígiụ, nếu chúng ta lấy mã này:

```
if (i > 5) {
  alert(i);
} else {
  continue;
}
```

…và viết lại nó bằng dấu chấm hỏi:

```
(i > 5) ? alert(i) : continue; // continue không được phép ở đây
```

…nó ngừng hoạt động: có lỗi cú pháp.

Đây chỉ là một lý do khác để không sử dụng toán tử dấu chấm hỏi `?` thay vì `if`.

## [Labels cho break/continue](#labels-for-break-continue)

Đôi khi chúng ta cần thoát từ nhiều vòng lặp lồng nhau cùng một lúc.

Vígiụ, trong mã dưới đây chúng ta lặp qua `i` và `j`, yêu cầu tọa độ `(i, j)` từ `(0,0)` đến `(2,2)`:

```
for (let i = 0; i < 3; i++) {

  for (let j = 0; j < 3; j++) {

    let input = prompt(`Giá trị tại coords (${i},${j})`, '');

    // nếu chúng ta muốn thoát từ đây đến Done (dưới đây)?
  }
}

alert('Xong!');
```

Chúng ta cần một cách để dừng quá trình nếu người dùng hủy input.

`break` thông thường sau `input` sẽ chỉ phá vỡ vòng lặp bên trong. Điều đó không đủ – labels, hãy đến cứu!

*Một label* là một identifier với dấu hai chấm trước một vòng lặp:

```
labelName: for (...) {
  ...
}
```

Câu lệnh `break <labelName>` trong vòng lặp dưới đây thoát ra label:

```
outer: for (let i = 0; i < 3; i++) {

  for (let j = 0; j < 3; j++) {

    let input = prompt(`Giá trị tại coords (${i},${j})`, '');

    // nếu chuỗi trống hoặc bị hủy, thì thoát khỏi cả hai vòng lặp
    if (!input) break outer; // (*)

    // làm gì đó với giá trị...
  }
}

alert('Xong!');
```

Trong mã ở trên, `break outer` tìm kiếm lên label có tên `outer` và thoát khỏi vòng lặp đó.

Vì vậy, quyền kiểm soát đi thẳng từ `(*)` đến `alert('Xong!')`.

Chúng ta cũng có thể chuyển label sang một dòng riêng:

```
outer:
for (let i = 0; i < 3; i++) { ... }
```

Chỉ thị `continue` cũng có thể được sử dụng với một label. Trong trường hợp này, việc thực thi mã nhảy sang lần lặp tiếp theo của vòng lặp được gắn nhãn.

Labels không cho phép "nhảy" khắp nơi

Labels không cho phép chúng ta nhảy đến một chỗ tùy ý trong mã.

Vígiụ, không thể làm điều này:

```
break label; // nhảy đến label bên dưới (không hoạt động)

label: for (...)
```

Chỉ thị `break` phải nằm trong một khối mã. Về mặt kỹ thuật, bất kỳ khối mã được gắn nhãn nào cũng được, ví dụ:

```
label: {
  // ...
  break label; // hoạt động
  // ...
}
```

…Mặc dù, 99.9% thời gian `break` được sử dụng bên trong các vòng lặp, như chúng ta đã thấy trong các ví dụ ở trên.

`continue` chỉ có thể từ bên trong một vòng lặp.

## [Tổng kết](#summary)

Chúng ta đã bao quát 3 loại vòng lặp:

- `while` – Điều kiện được kiểm tra trước mỗi lần lặp.
- `do..while` – Điều kiện được kiểm tra sau mỗi lần lặp.
- `for (;;)` – Điều kiện được kiểm tra trước mỗi lần lặp, các cài đặt bổ sung có sẵn.

Để tạo một vòng lặp "vô hạn", thường cấu trúc `while(true)` được sử dụng. Vòng lặp như vậy, giống như bất kỳ vòng lặp nào khác, có thể được dừng bằng chỉ thị `break`.

Nếu chúng ta không muốn làm gì đó trong lần lặp hiện tại và muốn chuyển sang lần lặp tiếp theo, chúng ta có thể sử dụng chỉ thị `continue`.

`break/continue` hỗ trợ labels trước vòng lặp. Label là cách duy nhất để `break/continue` thoát khỏi vòng lặp lồng nhau để đi ra vòng lặp ngoài.

---

---

## Các bài tập

## [Các bài tập](#tasks)

### [Giá trị vòng lặp cuối cùng](#last-loop-value)

mức độ quan trọng: 3

Giá trị cuối cùng được alert bởi mã này là gì? Tại sao?

```
let i = 3;

while (i) {
  alert( i-- );
}
```

lời giải

Câu trả lời: `1`.

```
let i = 3;

while (i) {
  alert( i-- );
}
```

Mỗi lần lặp vòng lặp giảm `i` đi `1`. Kiểm tra `while(i)` dừng vòng lặp khi `i = 0`.

Do đó, các bước của vòng lặp tạo thành dãy sau ("loop unrolled"):

```
let i = 3;

alert(i--); // hiển thị 3, giảm i xuống 2

alert(i--) // hiển thị 2, giảm i xuống 1

alert(i--) // hiển thị 1, giảm i xuống 0

// dừng, kiểm tra while(i) dừng vòng lặp
```

### [Vòng lặp while hiển thị những giá trị nào?](#which-values-does-the-while-loop-show)

mức độ quan trọng: 4

Với mỗi lần lặp vòng lặp, ghi lại giá trị mà nó xuất ra và sau đó so sánh nó với lời giải.

Cả hai vòng lặp `alert` các giá trị giống nhau, hay không?

1. Dạng prefix `++i`:

   ```
   let i = 0;
   while (++i < 5) alert( i );
   ```
2. Dạng postfix `i++`

   ```
   let i = 0;
   while (i++ < 5) alert( i );
   ```

lời giải

Bài tập này minh họa cách các dạng postfix/prefix có thể dẫn đến các kết quả khác nhau khi được sử dụng trong các phép so sánh.

1. **Từ 1 đến 4**

   ```
   let i = 0;
   while (++i < 5) alert( i );
   ```

   Giá trị đầu tiên là `i = 1`, vì `++i` trước tiên tăng `i` và sau đó trả về giá trị mới. Vì vậy, phép so sánh đầu tiên là `1 < 5` và `alert` hiển thị `1`.

   Sau đó là `2, 3, 4…` – các giá trị xuất hiện lần lượt. Phép so sánh luôn sử dụng giá trị đã được tăng, vì `++` đứng trước biến.

   Cuối cùng, `i = 4` được tăng lên `5`, phép so sánh `while(5 < 5)` thất bại, và vòng lặp dừng. Vậy `5` không được hiển thị.

2. **Từ 1 đến 5**

   ```
   let i = 0;
   while (i++ < 5) alert( i );
   ```

   Giá trị đầu tiên lại là `i = 1`. Dạng postfix của `i++` tăng `i` và sau đó trả về *giá trị cũ*, vì vậy phép so sánh `i++ < 5` sẽ sử dụng `i = 0` (khác với `++i < 5`).

   Nhưng lệnh gọi `alert` là riêng biệt. Đó là một câu lệnh khác thực thi sau khi tăng và so sánh. Vì vậy nó nhận được `i = 1` hiện tại.

   Sau đó là `2, 3, 4…`

   Hãy dừng lại ở `i = 4`. Dạng prefix `++i` sẽ tăng nó và sử dụng `5` trong phép so sánh. Nhưng ở đây chúng ta có dạng postfix `i++`. Vì vậy nó tăng `i` lên `5`, nhưng trả về giá trị cũ. Do đó phép so sánh thực tế là `while(4 < 5)` – true, và quyền kiểm soát chuyển sang `alert`.

   Giá trị `i = 5` là giá trị cuối cùng, vì ở bước tiếp theo `while(5 < 5)` là false.

### [Vòng lặp "for" hiển thị những giá trị nào?](#which-values-get-shown-by-the-for-loop)

mức độ quan trọng: 4

Với mỗi vòng lặp, ghi lại giá trị mà nó sẽ hiển thị. Sau đó so sánh với câu trả lời.

Cả hai vòng lặp `alert` các giá trị giống nhau hay không?

1. Dạng postfix:

   ```
   for (let i = 0; i < 5; i++) alert( i );
   ```
2. Dạng prefix:

   ```
   for (let i = 0; i < 5; ++i) alert( i );
   ```

lời giải

**Câu trả lời: từ `0` đến `4` trong cả hai trường hợp.**

```
for (let i = 0; i < 5; ++i) alert( i );

for (let i = 0; i < 5; i++) alert( i );
```

Điều đó có thể dễ dàng suy ra từ thuật toán của `for`:

1. Thực thi một lần `i = 0` trước mọi thứ (begin).
2. Kiểm tra điều kiện `i < 5`
3. Nếu `true` – thực thi thân vòng lặp `alert(i)`, và sau đó `i++`

Phép tăng `i++` được tách rời khỏi kiểm tra điều kiện (2). Đó chỉ là một câu lệnh khác.

Giá trị được trả về bởi phép tăng không được sử dụng ở đây, vì vậy không có sự khác biệt giữa `i++` và `++i`.

### [Xuất các số chẵn trong vòng lặp](#output-even-numbers-in-the-loop)

mức độ quan trọng: 5

Sử dụng vòng lặp `for` để xuất các số chẵn từ `2` đến `10`.

[Chạy demo](#)

lời giải

```
for (let i = 2; i <= 10; i++) {
  if (i % 2 == 0) {
    alert( i );
  }
}
```

Chúng ta sử dụng toán tử "modulo" `%` để lấy phần dư và kiểm tra tính chẵn ở đây.

### [Thay thế "for" bằng "while"](#replace-for-with-while)

mức độ quan trọng: 5

Viết lại mã thay đổi vòng lặp `for` thành `while` mà không làm thay đổi hành vi của nó (output phải giữ nguyên).

```
for (let i = 0; i < 3; i++) {
  alert( `số ${i}!` );
}
```

lời giải

```
let i = 0;
while (i < 3) {
  alert( `số ${i}!` );
  i++;
}
```

### [Lặp lại cho đến khi input đúng](#repeat-until-the-input-is-correct)

mức độ quan trọng: 5

Viết một vòng lặp yêu cầu nhập một số lớn hơn `100`. Nếu người truy cập nhập một số khác – yêu cầu họ nhập lại.

Vòng lặp phải yêu cầu nhập một số cho đến khi người truy cập nhập một số lớn hơn `100` hoặc hủy input/nhập dòng trống.

Ở đây chúng ta có thể giả sử rằng người truy cập chỉ nhập các số. Không cần triển khai xử lý đặc biệt cho input không phải số trong bài tập này.

[Chạy demo](#)

lời giải

```
let num;

do {
  num = prompt("Nhập một số lớn hơn 100?", 0);
} while (num <= 100 && num);
```

Vòng lặp `do..while` lặp lại trong khi cả hai kiểm tra đều truthy:

1. Kiểm tra cho `num <= 100` – tức là, giá trị nhập vào vẫn chưa lớn hơn `100`.
2. Kiểm tra `&& num` là false khi `num` là `null` hoặc chuỗi trống. Sau đó vòng lặp `while` cũng dừng.

P.S. Nếu `num` là `null` thì `num <= 100` là `true`, vì vậy không có kiểm tra thứ 2, vòng lặp sẽ không dừng nếu người dùng nhấn HỦY. Cả hai kiểm tra đều cần thiết.

### [Xuất các số nguyên tố](#output-prime-numbers)

mức độ quan trọng: 3

Một số nguyên lớn hơn `1` được gọi là [nguyên tố](https://en.wikipedia.org/wiki/Prime_number) nếu nó không thể chia hết cho bất kỳ thứ gì ngoại trừ `1` và chính nó.

Nói cách khác, `n > 1` là số nguyên tố nếu nó không thể chia đều cho bất kỳ thứ gì ngoại trừ `1` và `n`.

Vígiụ, `5` là một số nguyên tố, vì nó không thể chia hết cho `2`, `3` và `4`.

**Viết mã hiển thị các số nguyên tố trong khoảng từ `2` đến `n`.**

Đối với `n = 10`, kết quả sẽ là `2,3,5,7`.

P.S. Mã nên hoạt động cho bất kỳ `n` nào, không được hard-code cho bất kỳ giá trị cố định nào.

lời giải

Có nhiều thuật toán cho bài tập này.

Hãy sử dụng một vòng lặp lồng nhau:

```
Với mỗi i trong khoảng {
  kiểm tra xem i có ước từ 1..i không
  nếu có => giá trị không phải là số nguyên tố
  nếu không => giá trị là số nguyên tố, hiển thị nó
}
```

Mã sử dụng một label:

```
let n = 10;

nextPrime:
for (let i = 2; i <= n; i++) { // với mỗi i...

  for (let j = 2; j < i; j++) { // tìm ước..
    if (i % j == 0) continue nextPrime; // không phải số nguyên tố, qua i tiếp theo
  }

  alert( i ); // số nguyên tố
}
```

Có rất nhiều không gian để tối ưu hóa nó. Vígiụ, chúng ta có thể tìm các ước từ `2` đến căn bậc hai của `i`. Nhưng dù sao, nếu chúng ta muốn thực sự hiệu quả cho các khoảng lớn, chúng ta cần thay đổi cách tiếp cận và dựa vào toán học nâng cao và các thuật toán phức tạp như [Quadratic sieve](https://en.wikipedia.org/wiki/Quadratic_sieve), [General number field sieve](https://en.wikipedia.org/wiki/General_number_field_sieve) v.v.
