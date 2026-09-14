# Các toán tử cơ bản, toán học

> Nguồn: [https://javascript.info/operators](https://javascript.info/operators)

<!-- fetched: 2026-09-14 -->

Chúng ta biết nhiều toán tử từ trường học. Chúng là các thứ như cộng `+`, nhân `*`, trừ `-`, và vân vân.

Trong chương này, chúng ta sẽ bắt đầu với các toán tử đơn giản, sau đó tập trung vào các khía cạnh đặc thù của JavaScript, không được bao quát bởi arithmetic school.

## [Thuật ngữ: “unary”, “binary”, “operand”](#terms-unary-binary-operand)

Trước khi chuyển sang, hãy nắm bắt một số thuật ngữ phổ biến.

- *Một operand* – là thứ mà các toán tử được áp dụng. Ví dụ, trong phép nhân của `5 * 2` có hai operand: operand trái là `5` và operand phải là `2`. Đôi khi, người ta gọi những cái này là “arguments” thay vì “operands”.
- Một toán tử là *unary* nếu nó có một operand duy nhất. Ví dụ, phép phủ định unary `-` đảo ngược dấu của một số:

  ```
  let x = 1;

  x = -x;
  alert( x ); // -1, phép phủ định unary đã được áp dụng
  ```
- Một toán tử là *binary* nếu nó có hai operand. Phép trừ cũng tồn tại ở dạng binary:

  ```
  let x = 1, y = 3;
  alert( y - x ); // 2, phép trừ binary trừ các giá trị
  ```

  Về mặt hình thức, trong các ví dụ ở trên, chúng ta có hai toán tử khác nhau chia sẻ cùng ký hiệu: toán tử phủ định, một toán tử unary đảo ngược dấu, và toán tử trừ, một toán tử binary trừ một số cho số khác.

## [Toán học](#maths)

Các thao tác toán học sau được hỗ trợ:

- Cộng `+`,
- Trừ `-`,
- Nhân `*`,
- Chia `/`,
- Phần dư `%`,
- Lũy thừa `**`.

Bốn cái đầu là trực quan, trong khi `%` và `**` cần một vài lời về chúng.

### [Phần dư %](#remainder)

Toán tử phần dư `%`, mặc dù vẻ ngoài của nó, không liên quan đến phần trăm.

Kết quả của `a % b` là [phần dư](https://en.wikipedia.org/wiki/Remainder) của phép chia nguyên của `a` cho `b`.

Ví dụ:

```
alert( 5 % 2 ); // 1, phần dư của 5 chia cho 2
alert( 8 % 3 ); // 2, phần dư của 8 chia cho 3
alert( 8 % 4 ); // 0, phần dư của 8 chia cho 4
```

### [Lũy thừa **](#exponentiation)

Toán tử lũy thừa `a ** b` nâng `a` lên lũy thừa của `b`.

Trong toán học trường học, chúng ta viết là ab.

Ví dụ:

```
alert( 2 ** 2 ); // 2² = 4
alert( 2 ** 3 ); // 2³ = 8
alert( 2 ** 4 ); // 2⁴ = 16
```

Giống như trong toán học, toán tử lũy thừa được định nghĩa cho các số không nguyên.

Ví dụ, căn bậc hai là lũy thừa bởi ½:

```
alert( 4 ** (1/2) ); // 2 (lũy thừa của 1/2 là tương đương căn bậc hai)
alert( 8 ** (1/3) ); // 2 (lũy thừa của 1/3 là tương đương căn bậc ba)
```

## [Nối chuỗi với binary +](#string-concatenation-with-binary)

Hãy gặp các tính năng của toán tử JavaScript vượt ra ngoài arithmetic school.

Thông thường, toán tử cộng `+` cộng các số.

Nhưng, nếu binary `+` được áp dụng cho chuỗi, nó hợp nhất (nối) chúng:

```
let s = "my" + "string";
alert(s); // mystring
```

Lưu ý rằng nếu bất kỳ operand nào là chuỗi, thì operand còn lại được chuyển đổi sang chuỗi.

Ví dụ:

```
alert( '1' + 2 ); // "12"
alert( 2 + '1' ); // "21"
```

Thấy không, nó không quan trọng operand đầu tiên là chuỗi hay operand thứ hai.

Đây là một ví dụ phức tạp hơn:

```
alert(2 + 2 + '1' ); // "41" và không phải "221"
```

Ở đây, các toán tử làm việc lần lượt. Đầu tiên `+` cộng hai số, vì vậy nó trả về `4`, sau đó `+` tiếp theo thêm chuỗi `1` vào nó, vì vậy nó giống như `4 + '1' = '41'`.

```
alert('1' + 2 + 2); // "122" và không phải "14"
```

Ở đây, operand đầu tiên là chuỗi, compiler xử lý hai operand còn lại là chuỗi. `2` được nối vào `'1'`, vì vậy nó giống như `'1' + 2 = "12"` và `"12" + 2 = "122"`.

Binary `+` là toán tử duy nhất hỗ trợ chuỗi theo cách như vậy. Các toán tử arithmetic khác chỉ làm việc với số và luôn chuyển đổi operand của chúng thành số.

Đây là demo cho phép trừ và chia:

```
alert( 6 - '2' ); // 4, chuyển đổi '2' sang số
alert( '6' / '2' ); // 3, chuyển đổi cả hai operand sang số
```

## [Chuyển đổi số, unary +](#numeric-conversion-unary)

Dấu cộng `+` tồn tại ở hai dạng: dạng binary mà chúng ta đã sử dụng ở trên và dạng unary.

Dấu cộng unary, hay nói cách khác, toán tử cộng `+` được áp dụng cho một giá trị đơn, không làm gì với số. Nhưng nếu operand không phải là số, unary plus chuyển đổi nó thành số.

Ví dụ:

```
// Không ảnh hưởng đến số
let x = 1;
alert( +x ); // 1

let y = -2;
alert( +y ); // -2

// Chuyển đổi các giá trị không phải số
alert( +true ); // 1
alert( +"" );   // 0
```

Nó thực sự làm cùng một điều như `Number(...)`, nhưng ngắn hơn.

Nhu cầu chuyển đổi chuỗi thành số xảy ra rất thường xuyên. Ví dụ, nếu chúng ta đang lấy giá trị từ các trường form HTML, chúng thường là chuỗi. Nếu chúng ta muốn cộng chúng thì sao?

Binary plus sẽ cộng chúng như chuỗi:

```
let apples = "2";
let oranges = "3";

alert( apples + oranges ); // "23", binary plus nối chuỗi
```

Nếu chúng ta muốn đối xử chúng như số, chúng ta cần chuyển đổi và sau đó cộng chúng:

```
let apples = "2";
let oranges = "3";

// cả hai giá trị được chuyển đổi sang số trước khi binary plus
alert( +apples + +oranges ); // 5

// biến thể dài hơn
// alert( Number(apples) + Number(oranges) ); // 5
```

Từ góc độ toán học, sự phong phú của dấu cộng có vẻ kỳ lạ. Nhưng từ góc độ lập trình viên, không có gì đặc biệt: unary plus được áp dụng trước, chúng chuyển đổi chuỗi thành số, và sau đó binary plus cộng chúng lại.

Tại sao unary plus được áp dụng cho các giá trị trước các binary? Như chúng ta sẽ thấy, đó là vì *độ ưu tiên cao hơn* của chúng.

## [Độ ưu tiên toán tử](#operator-precedence)

Nếu một biểu thức có nhiều hơn một toán tử, thứ tự thực thi được xác định bởi *độ ưu tiên* của chúng, hay nói cách khác, thứ tự ưu tiên mặc định của các toán tử.

Từ trường học, tất cả chúng ta đều biết rằng phép nhân trong biểu thức `1 + 2 * 2` nên được tính trước phép cộng. Đó chính xác là điều độ ưu tiên. Phép nhân được nói là có *độ ưu tiên cao hơn* so với phép cộng.

Dấu ngoặc đơn overrides bất kỳ độ ưu tiên nào, vì vậy nếu chúng ta không hài lòng với thứ tự mặc định, chúng ta có thể sử dụng chúng để thay đổi nó. Ví dụ, viết `(1 + 2) * 2`.

Có nhiều toán tử trong JavaScript. Mọi toán tử có một số độ ưu tiên tương ứng. Cái có số lớn hơn thực thi trước. Nếu độ ưu tiên giống nhau, thứ tự thực thi là từ trái sang phải.

Đây là một trích xuất từ [bảng độ ưu tiên](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Operator_Precedence) (bạn không cần nhớ điều này, nhưng lưu ý rằng các toán tử unary cao hơn các toán tử binary tương ứng):

| Độ ưu tiên | Tên | Ký hiệu |
| --- | --- | --- |
| … | … | … |
| 14 | unary plus | `+` |
| 14 | unary negation | `-` |
| 13 | exponentiation | `**` |
| 12 | multiplication | `*` |
| 12 | division | `/` |
| 11 | addition | `+` |
| 11 | subtraction | `-` |
| … | … | … |
| 2 | assignment | `=` |
| … | … | … |

Như chúng ta có thể thấy, “unary plus” có độ ưu tiên `14` cao hơn `11` của “addition” (binary plus). Vì vậy, trong biểu thức `"+apples + +oranges"`, unary plus hoạt động trước phép cộng.

## [Gán](#assignment)

Hãy ghi chú rằng một phép gán `=` cũng là một toán tử. Nó được liệt kê trong bảng độ ưu tiên với độ ưu tiên rất thấp là `2`.

Vì vậy, khi chúng ta gán một biến, như `x = 2 * 2 + 1`, các phép tính được thực hiện trước và sau đó `=` được đánh giá, lưu kết quả vào `x`.

```
let x = 2 * 2 + 1;

alert( x ); // 5
```

### [Phép gán = trả về giá trị](#assignment-returns-a-value)

Thực tế của `=` là một toán tử, không phải là một “cấu trúc ngôn ngữ kỳ diệu” có một ý nghĩa thú vị.

Tất cả các toán tử trong JavaScript trả về một giá trị. Đó là hiển nhiên cho `+` và `-`, nhưng cũng đúng cho `=`.

Lệnh gọi `x = value` ghi `value` vào `x` *và sau đó trả về nó*.

Đây là một demo sử dụng một phép gán như một phần của biểu thức phức tạp hơn:

```
let a = 1;
let b = 2;

let c = 3 - (a = b + 1);

alert( a ); // 3
alert( c ); // 0
```

Trong ví dụ trên, kết quả của biểu thức `(a = b + 1)` là giá trị được gán cho `a` (đó là `3`). Nó sau đó được sử dụng cho các đánh giá tiếp theo.

Mã vui nhộn, phải không? Chúng ta nên hiểu cách nó hoạt động, bởi vì đôi khi chúng ta thấy nó trong các thư viện JavaScript.

Mặc dù, xin đừng viết mã như thế đó. Những thủ thuật như vậy chắc chắn không làm cho mã rõ ràng hoặc dễ đọc hơn.

### [Gán nối](#chaining-assignments)

Một tính năng thú vị khác là khả năng gán nối:

```
let a, b, c;

a = b = c = 2 + 2;

alert( a ); // 4
alert( b ); // 4
alert( c ); // 4
```

Các phép gán nối được đánh giá từ phải sang trái. Đầu tiên, biểu thức bên phải nhất `2 + 2` được đánh giá và sau đó gán cho các biến bên trái: `c`, `b` và `a`. Vào cuối, tất cả các biến chia sẻ một giá trị đơn.

Một lần nữa, vì mục đích readability, tốt hơn nên chia mã như vậy thành vài dòng:

```
c = 2 + 2;
b = c;
a = c;
```

Dễ đọc hơn, đặc biệt khi mắt quét mã nhanh.

## [Sửa đổi tại chỗ](#modify-in-place)

Chúng ta thường cần áp dụng một toán tử cho một biến và lưu kết quả mới trong cùng biến đó.

Ví dụ:

```
let n = 2;
n = n + 5;
n = n * 2;
```

Ký hiệu này có thể được rút gọn bằng cách sử dụng các toán tử `+=` và `*=`:

```
let n = 2;
n += 5; // giờ n = 7 (giống như n = n + 5)
n *= 2; // giờ n = 14 (giống như n = n * 2)

alert( n ); // 14
```

Các toán tử “sửa đổi-và-gán” ngắn tồn tại cho tất cả các toán tử arithmetic và bitwise: `/=`, `-=`, v.v.

Các toán tử này có cùng độ ưu tiên như một phép gán thông thường, vì vậy chúng chạy sau hầu hết các tính toán khác:

```
let n = 2;

n *= 3 + 5; // phần bên phải được đánh giá trước, giống như n *= 8

alert( n ); // 16
```

## [Tăng/giảm](#increment-decrement)

Tăng hoặc giảm một số đi một là trong số các thao tác số học phổ biến nhất.

Vì vậy, có các toán tử đặc biệt cho nó:

- **Tăng** `++` tăng một biến đi 1:

  ```
  let counter = 2;
  counter++;        // hoạt động giống như counter = counter + 1, nhưng ngắn hơn
  alert( counter ); // 3
  ```
- **Giảm** `--` giảm một biến đi 1:

  ```
  let counter = 2;
  counter--;        // hoạt động giống như counter = counter - 1, nhưng ngắn hơn
  alert( counter ); // 1
  ```

Quan trọng:

Tăng/giảm chỉ có thể được áp dụng cho biến. Cố gắng sử dụng nó trên một giá trị như `5++` sẽ cho lỗi.

Các toán tử `++` và `--` có thể được đặteither trước hoặc sau một biến.

- Khi toán tử đi sau biến, nó ở dạng “postfix”: `counter++`.
- Dạng “prefix” là khi toán tử đi trước biến: `++counter`.

Cả hai câu lệnh này làm cùng một điều: tăng `counter` đi `1`.

Có sự khác biệt không? Có, nhưng chúng ta chỉ có thể thấy nó nếu chúng ta sử dụng giá trị được trả về của `++/--`.

Hãy làm rõ. Như chúng ta biết, tất cả các toán tử trả về một giá trị. Tăng/giảm không có ngoại lệ. Dạng prefix trả về giá trị mới trong khi dạng postfix trả về giá trị cũ (trước khi tăng/giảm).

Để thấy sự khác biệt, đây là một ví dụ:

```
let counter = 1;
let a = ++counter; // (*)

alert(a); // 2
```

Ở dòng `(*)`, dạng *prefix* `++counter` tăng `counter` và trả về giá trị mới, `2`. Vì vậy, `alert` hiển thị `2`.

Bây giờ, hãy sử dụng dạng postfix:

```
let counter = 1;
let a = counter++; // (*) thay đổi ++counter thành counter++

alert(a); // 1
```

Ở dòng `(*)`, dạng *postfix* `counter++` cũng tăng `counter` nhưng trả về giá trị *cũ* (trước khi tăng). Vì vậy, `alert` hiển thị `1`.

Tóm tắt:

- Nếu kết quả của tăng/giảm không được sử dụng, không có sự khác biệt trong dạng nào để sử dụng:

  ```
  let counter = 0;
  counter++;
  ++counter;
  alert( counter ); // 2, các dòng trên làm cùng một điều
  ```
- Nếu chúng ta muốn tăng một giá trị *và* ngay lập tức sử dụng kết quả của toán tử, chúng ta cần dạng prefix:

  ```
  let counter = 0;
  alert( ++counter ); // 1
  ```
- Nếu chúng ta muốn tăng một giá trị nhưng sử dụng giá trị trước đó của nó, chúng ta cần dạng postfix:

  ```
  let counter = 0;
  alert( counter++ ); // 0
  ```

Tăng/giảm giữa các toán tử khác

Các toán tử `++/--` có thể được sử dụng bên trong biểu thức. Độ ưu tiên của chúng cao hơn hầu hết các thao tác arithmetic khác.

Ví dụ:

```
let counter = 1;
alert( 2 * ++counter ); // 4
```

So sánh với:

```
let counter = 1;
alert( 2 * counter++ ); // 2, vì counter++ trả về giá trị "cũ"
```

Mặc dù về mặt kỹ thuật ổn, ký hiệu như vậy thường làm mã ít đọc hơn. Một dòng làm nhiều điều – không tốt.

Khi đọc mã, một cái quét mắt “dọc” nhanh có thể dễ dàng bỏ qua thứ gì đó như `counter++` và nó sẽ không rõ ràng rằng biến đã tăng.

Chúng ta khuyên một style “một dòng – một hành động”:

```
let counter = 1;
alert( 2 * counter );
counter++;
```

## [Toán tử bitwise](#bitwise-operators)

Các toán tử bitwise xử lý các đối số như số nguyên 32-bit và làm việc ở cấp độ biểu diễn nhị phân của chúng.

Các toán tử này không đặc thù cho JavaScript. Chúng được hỗ trợ trong hầu hết các ngôn ngữ lập trình.

Danh sách các toán tử:

- AND ( `&` )
- OR ( `|` )
- XOR ( `^` )
- NOT ( `~` )
- LEFT SHIFT ( `<<` )
- RIGHT SHIFT ( `>>` )
- ZERO-FILL RIGHT SHIFT ( `>>>` )

Các toán tử này được sử dụng rất hiếm, khi chúng ta cần sửa đổi số ở cấp thấp nhất (bitwise). Chúng ta sẽ không cần các toán tử này sớm, vì phát triển web ít sử dụng chúng, nhưng trong một số lĩnh vực đặc biệt, như mật mã, chúng hữu ích. Bạn có thể đọc chương [Bitwise Operators](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Expressions_and_Operators#bitwise_operators) trên MDN khi có nhu cầu.

## [Dấu phẩy](#comma)

Toán tử dấu phẩy `,` là một trong những toán tử hiếm nhất và khác thường nhất. Đôi khi, nó được sử dụng để viết mã ngắn hơn, vì vậy chúng ta cần biết nó để hiểu những gì đang xảy ra.

Toán tử dấu phẩy cho phép chúng ta đánh giá nhiều biểu thức, chia chúng bằng dấu phẩy `,`. Mỗi biểu thức được đánh giá nhưng chỉ kết quả của biểu thức cuối cùng được trả về.

Ví dụ:

```
let a = (1 + 2, 3 + 4);

alert( a ); // 7 (kết quả của 3 + 4)
```

Ở đây, biểu thức đầu tiên `1 + 2` được đánh giá và kết quả của nó bị ném đi. Sau đó, `3 + 4` được đánh giá và trả về như kết quả.

Dấu phẩy có độ ưu tiên rất thấp

Xin lưu ý rằng toán tử dấu phẩy có độ ưu tiên rất thấp, thấp hơn `=`, vì vậy dấu ngoặc đơn quan trọng trong ví dụ ở trên.

Không có chúng: `a = 1 + 2, 3 + 4` đánh giá `+` trước, cộng các số vào `a = 3, 7`, sau đó toán tử gán `=` gán `a = 3`, và phần còn lại bị bỏ qua. Nó giống như `(a = 1 + 2), 3 + 4`.

Tại sao chúng ta cần một toán tử ném bỏ mọi thứ ngoại trừ biểu thức cuối cùng?

Đôi khi, người ta sử dụng nó trong các cấu trúc phức tạp hơn để đặt nhiều hành động trong một dòng.

Ví dụ:

```
// ba hoạt động trong một dòng
for (a = 1, b = 3, c = a * b; a < 10; a++) {
 ...
}
```

Những thủ thuật như vậy được sử dụng trong nhiều framework JavaScript. Đó là lý do tại sao chúng ta đề cập đến chúng. Nhưng thường chúng không cải thiện readability của mã vì vậy chúng ta nên nghĩ kỹ trước khi sử dụng chúng.

---

---

## Các bài tập

## [Các bài tập](#tasks)

### [Dạng postfix và prefix](#the-postfix-and-prefix-forms)

mức độ quan trọng: 5

Các giá trị cuối cùng của tất cả các biến `a`, `b`, `c` và `d` sau khi mã dưới đây là gì?

```
let a = 1, b = 1;

let c = ++a; // ?
let d = b++; // ?
```

lời giải

Câu trả lời là:

- `a = 2`
- `b = 2`
- `c = 2`
- `d = 1`

```
let a = 1, b = 1;

alert( ++a ); // 2, dạng prefix trả về giá trị mới
alert( b++ ); // 1, dạng postfix trả về giá trị cũ

alert( a ); // 2, đã tăng một lần
alert( b ); // 2, đã tăng một lần
```

### [Kết quả gán](#assignment-result)

mức độ quan trọng: 3

Các giá trị của `a` và `x` sau mã dưới đây là gì?

```
let a = 2;

let x = 1 + (a *= 2);
```

lời giải

Câu trả lời là:

- `a = 4` (nhân với 2)
- `x = 5` (tính toán như 1 + 4)

### [Chuyển đổi kiểu](#type-conversions)

mức độ quan trọng: 5

Kết quả của các biểu thức này là gì?

```
"" + 1 + 0
"" - 1 + 0
true + false
6 / "3"
"2" * "3"
4 + 5 + "px"
"$" + 4 + 5
"4" - 2
"4px" - 2
"  -9  " + 5
"  -9  " - 5
null + 1
undefined + 1
" \t \n" - 2
```

Hãy suy nghĩ kỹ, viết ra và sau đó so sánh với câu trả lời.

lời giải

```
"" + 1 + 0 = "10" // (1)
"" - 1 + 0 = -1 // (2)
true + false = 1
6 / "3" = 2
"2" * "3" = 6
4 + 5 + "px" = "9px"
"$" + 4 + 5 = "$45"
"4" - 2 = 2
"4px" - 2 = NaN
"  -9  " + 5 = "  -9  5" // (3)
"  -9  " - 5 = -14 // (4)
null + 1 = 1 // (5)
undefined + 1 = NaN // (6)
" \t \n" - 2 = -2 // (7)
```

1. Phép cộng với chuỗi `"" + 1` chuyển đổi `1` thành chuỗi: `"" + 1 = "1"`, và sau đó chúng ta có `"1" + 0`, quy tắc tương tự được áp dụng.
2. Phép trừ `-` (giống như hầu hết các thao tác math) chỉ làm việc với số, nó chuyển đổi chuỗi rỗng `""` thành `0`.
3. Phép cộng với chuỗi nối số `5` vào chuỗi.
4. Phép trừ luôn chuyển đổi sang số, vì vậy nó làm `" -9 "` thành số `-9` (bỏ qua khoảng trắng xung quanh nó).
5. `null` trở thành `0` sau chuyển đổi số.
6. `undefined` trở thành `NaN` sau chuyển đổi số.
7. Các ký tự khoảng trắng bị loại bỏ khỏi đầu và cuối chuỗi khi một chuỗi được chuyển đổi thành số. Ở đây toàn bộ chuỗi gồm các ký tự khoảng trắng, chẳng hạn như `\t`, `\n` và một khoảng trống “thông thường” giữa chúng. Vì vậy, tương tự như chuỗi rỗng, nó trở thành `0`.

### [Sửa phép cộng](#fix-the-addition)

mức độ quan trọng: 5

Đây là mã hỏi người dùng hai số và hiển thị tổng của chúng.

Nó hoạt động sai. Output trong ví dụ dưới đây là `12` (cho các giá trị prompt mặc định).

Tại sao? Sửa nó. Kết quả nên là `3`.

```
let a = prompt("Số đầu tiên?", 1);
let b = prompt("Số thứ hai?", 2);

alert(a + b); // 12
```

lời giải

Nguyên nhân là prompt trả về input của người dùng dưới dạng chuỗi.

Vì vậy các biến có giá trị `"1"` và `"2"` tương ứng.

```
let a = "1"; // prompt("Số đầu tiên?", 1);
let b = "2"; // prompt("Số thứ hai?", 2);

alert(a + b); // 12
```

Điều chúng ta nên làm là chuyển đổi chuỗi thành số trước `+`. Ví dụ, sử dụng `Number()` hoặc thêm chúng với `+`.

Ví dụ, ngay trước `prompt`:

```
let a = +prompt("Số đầu tiên?", 1);
let b = +prompt("Số thứ hai?", 2);

alert(a + b); // 3
```

Hoặc trong `alert`:

```
let a = prompt("Số đầu tiên?", 1);
let b = prompt("Số thứ hai?", 2);

alert(+a + +b); // 3
```

Sử dụng cả unary và binary `+` trong mã mới nhất. trông vui nhộn, phải không?
