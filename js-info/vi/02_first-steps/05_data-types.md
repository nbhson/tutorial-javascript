# Kiểu dữ liệu

> Nguồn: [https://javascript.info/types](https://javascript.info/types)

<!-- fetched: 2026-09-14 -->

Một giá trị trong JavaScript luôn thuộc về một kiểu nhất định. Ví dụ, một chuỗi hoặc một số.

Có tám kiểu dữ liệu cơ bản trong JavaScript. Ở đây, chúng ta sẽ đề cập đến chúng nói chung và trong các chương tiếp theo chúng ta sẽ nói về từng cái chi tiết.

Chúng ta có thể đặt bất kỳ kiểu nào trong một biến. Ví dụ, một biến có thể lúc là chuỗi và sau đó lưu trữ một số:

```
// không lỗi
let message = "hello";
message = 123456;
```

Các ngôn ngữ lập trình cho phép những điều như vậy, như JavaScript, được gọi là “kiểu động”, có nghĩa là tồn tại các kiểu dữ liệu, nhưng biến không bị ràng buộc với bất kỳ kiểu nào trong số đó.

## [Số](#number)

```
let n = 123;
n = 12.345;
```

Kiểu *number* đại diện cho cả số nguyên và số floating point.

Có nhiều thao tác cho số, ví dụ: nhân `*`, chia `/`, cộng `+`, trừ `-`, và vân vân.

Ngoài các số thông thường, có những gì được gọi là “các giá trị số đặc biệt” cũng thuộc về kiểu dữ liệu này: `Infinity`, `-Infinity` và `NaN`.

- `Infinity` đại diện cho [Infinity](https://en.wikipedia.org/wiki/Infinity) toán học ∞. Nó là một giá trị đặc biệt lớn hơn bất kỳ số nào.

  Chúng ta có thể nhận được nó như là kết quả của phép chia cho không:

  ```
  alert( 1 / 0 ); // Infinity
  ```

  Hoặc đơn giản là tham chiếu trực tiếp:

  ```
  alert( Infinity ); // Infinity
  ```
- `NaN` đại diện cho lỗi tính toán. Nó là kết quả của một thao tác toán học không đúng hoặc không xác định, ví dụ:

  ```
  alert( "không phải số" / 2 ); // NaN, phép chia như vậy là sai
  ```

  `NaN` dính. Mọi thao tác toán học tiếp theo trên `NaN` trả về `NaN`:

  ```
  alert( NaN + 1 ); // NaN
  alert( 3 * NaN ); // NaN
  alert( "không phải số" / 2 - 1 ); // NaN
  ```

  Vì vậy, nếu có một `NaN` ở đâu đó trong một biểu thức toán học, nó lan truyền đến toàn bộ kết quả (có một ngoại lệ: `NaN ** 0` là `1`).

Các thao tác toán học an toàn

Làm toán là “an toàn” trong JavaScript. Chúng ta có thể làm bất cứ điều gì: chia cho không, xử lý các chuỗi không phải số như số, vân vân.

Script sẽ không bao giờ dừng với lỗi nghiêm trọng (“chết”). Tệ nhất, chúng ta sẽ nhận được `NaN` như là kết quả.

Các giá trị số đặc biệt formally thuộc về kiểu “number”. Tất nhiên chúng không phải là số theo nghĩa thông thường của từ.

Chúng ta sẽ thấy nhiều hơn về làm việc với số trong chương [Numbers](/number).

## [BigInt](#bigint-type)

Trong JavaScript, kiểu “number” không thể biểu diễn an toàn các giá trị nguyên lớn hơn `(2^53-1)` (đó là `9007199254740991`), hoặc nhỏ hơn `-(2^53-1)` cho các số âm.

Để thực sự chính xác, kiểu “number” có thể lưu trữ các số nguyên lớn hơn (lên đến `1.7976931348623157 * 10^308`), nhưng bên ngoài phạm vi số nguyên an toàn `±(2^53-1)` sẽ có lỗi độ chính xác, vì không phải tất cả các chữ số đều vừa với bộ lưu trữ cố định 64-bit. Vì vậy một giá trị “xấp xỉ” có thể được lưu trữ.

Ví dụ, hai số này (ngay phía trên phạm vi an toàn) là giống nhau:

```
console.log(9007199254740991 + 1); // 9007199254740992
console.log(9007199254740991 + 2); // 9007199254740992
```

Nói cách khác, tất cả các số nguyên lẻ lớn hơn `(2^53-1)` không thể lưu trữ được trong kiểu “number”.

Đối với hầu hết các mục đích, phạm vi `±(2^53-1)` là đủ, nhưng đôi khi chúng ta cần toàn bộ phạm vi của số nguyên thực sự lớn, ví dụ cho mật mã hoặc dấu thời gian microsecond.

Kiểu `BigInt` gần đây đã được thêm vào ngôn ngữ để biểu diễn số nguyên có độ dài tùy ý.

Một giá trị `BigInt` được tạo bằng cách nối `n` vào cuối một số nguyên:

```
// "n" ở cuối có nghĩa là BigInt
const bigInt = 1234567890123456789012345678901234567890n;
```

Vì `BigInt` hiếm khi cần, chúng ta không đề cập đến chúng ở đây, nhưng đã dành cho chúng một chương riêng [BigInt](/bigint). Đọc nó khi bạn cần những số lớn như vậy.

## [Chuỗi](#string)

Một chuỗi trong JavaScript phải được bao quanh bởi dấu ngoặc kép.

```
let str = "Hello";
let str2 = 'Single quotes are ok too';
let phrase = `can embed another ${str}`;
```

Trong JavaScript, có 3 loại dấu ngoặc kép.

1. Dấu ngoặc kép đôi: `"Hello"`.
2. Dấu ngoặc đơn: `'Hello'`.
3. Dấu backtick: `` `Hello` ``.

Dấu ngoặc kép đôi và đơn là “dấu ngoặc kép đơn giản”. Không có sự khác biệt thực tế giữa chúng trong JavaScript.

Dấu backtick là “dấu ngoặc kép chức năng mở rộng”. Chúng cho phép chúng ta nhúng biến và biểu thức vào chuỗi bằng cách bao quanh chúng trong `${…}`, ví dụ:

```
let name = "John";

// nhúng một biến
alert( `Hello, ${name}!` ); // Hello, John!

// nhúng một biểu thức
alert( `kết quả là ${1 + 2}` ); // kết quả là 3
```

Biểu thức bên trong `${…}` được đánh giá và kết quả trở thành một phần của chuỗi. Chúng ta có thể đặt bất cứ thứ gì vào đó: một biến như `name` hoặc một biểu thức số học như `1 + 2` hoặc cái gì đó phức tạp hơn.

Xin lưu ý rằng điều này chỉ có thể được thực hiện trong backticks. Các dấu ngoặc kép khác không có chức năng nhúng này!

```
alert( `kết quả là ${1 + 2}` ); // kết quả là ${1 + 2} (dấu ngoặc kép đôi không làm gì)
```

Chúng ta sẽ đề cập đến chuỗi kỹ hơn trong chương [Strings](/string).

Không có *kiểu ký tự*.

Trong một số ngôn ngữ, có một kiểu đặc biệt “ký tự” cho một ký tự đơn. Ví dụ, trong ngôn ngữ C và Java nó được gọi là “char”.

Trong JavaScript, không có kiểu như vậy. Chỉ có một kiểu: `string`. Một chuỗi có thể gồm không ký tự (trống), một ký tự hoặc nhiều ký tự.

## [Boolean (kiểu logic)](#boolean-logical-type)

Kiểu boolean có chỉ hai giá trị: `true` và `false`.

Kiểu này thường được sử dụng để lưu trữ các giá trị có/không: `true` có nghĩa là “có, đúng”, và `false` có nghĩa là “không, sai”.

Ví dụ:

```
let nameFieldChecked = true; // có, trường tên được kiểm tra
let ageFieldChecked = false; // không, trường tuổi không được kiểm tra
```

Giá trị boolean cũng xuất hiện như là kết quả của so sánh:

```
let isGreater = 4 > 1;

alert( isGreater ); // true (kết quả so sánh là “có”)
```

Chúng ta sẽ đề cập đến booleans sâu hơn trong chương [Các toán tử logic](/logical-operators).

## [Giá trị “null”](#the-null-value)

Giá trị đặc biệt `null` không thuộc về bất kỳ kiểu nào được mô tả ở trên.

Nó tạo thành một kiểu riêng biệt của nó chứa chỉ giá trị `null`:

```
let age = null;
```

Trong JavaScript, `null` không phải là “tham chiếu đến một đối tượng không tồn tại” hay “con trỏ null” như trong một số ngôn ngữ khác.

Nó chỉ là một giá trị đặc biệt đại diện cho “không có gì”, “trống” hoặc “giá trị không biết”.

Mã ở trên cho thấy `age` là không biết.

## [Giá trị “undefined”](#the-undefined-value)

Giá trị đặc biệt `undefined` cũng đứng riêng. Nó tạo thành một kiểu của riêng nó, giống như `null`.

Ý nghĩa của `undefined` là “giá trị chưa được gán”.

Nếu một biến được khai báo nhưng chưa được gán, thì giá trị của nó là `undefined`:

```
let age;

alert(age); // hiển thị "undefined"
```

Về mặt kỹ thuật, có thể gán rõ ràng `undefined` cho một biến:

```
let age = 100;

// thay đổi giá trị thành undefined
age = undefined;

alert(age); // "undefined"
```

…Nhưng chúng ta không khuyến nghị làm như vậy. Thông thường, một người sử dụng `null` để gán một giá trị “trống” hoặc “không biết” cho một biến, trong khi `undefined` được dành riêng như là giá trị khởi tạo mặc định cho những thứ chưa được gán.

## [Objects và Symbols](#objects-and-symbols)

Kiểu `object` là đặc biệt.

Tất cả các kiểu khác được gọi là “primitive” vì giá trị của chúng chỉ có thể chứa một thứ (là một chuỗi hoặc một số hoặc bất kỳ thứ gì). Ngược lại, objects được sử dụng để lưu trữ các bộ sưu tập data và các thực thể phức tạp hơn.

Quan trọng như vậy, objects deserving một sự xử lý đặc biệt. Chúng ta sẽ xử lý chúng sau trong chương [Objects](/object), sau khi chúng ta học thêm về primitives.

Kiểu `symbol` được sử dụng để tạo các định danh duy nhất cho objects. Chúng ta phải đề cập đến nó ở đây để hoàn thiện, nhưng cũng hoãn chi tiết đến khi chúng ta biết objects.

## [Toán tử typeof](#type-typeof)

Toán tử `typeof` trả về kiểu của toán hạng. Nó hữu ích khi chúng ta muốn xử lý các giá trị của các kiểu khác nhau theo cách khác nhau hoặc đơn giản muốn làm một kiểm tra nhanh.

Một lệnh gọi `typeof x` trả về một chuỗi với tên kiểu:

```
typeof undefined // "undefined"

typeof 0 // "number"

typeof 10n // "bigint"

typeof true // "boolean"

typeof "foo" // "string"

typeof Symbol("id") // "symbol"

typeof Math // "object"  (1)

typeof null // "object"  (2)

typeof alert // "function"  (3)
```

Ba dòng cuối có thể cần giải thích thêm:

1. `Math` là một built-in object cung cấp các thao tác toán học. Chúng ta sẽ học nó trong chương [Numbers](/number). Ở đây, nó phục vụ chỉ như một ví dụ về một object.
2. Kết quả của `typeof null` là `"object"`. Đó là một lỗi được công nhận chính thức trong `typeof`, bắt nguồn từ những ngày đầu rất sớm của JavaScript và được giữ lại để tương thích. Chắc chắn, `null` không phải là một object. Đó là một giá trị đặc biệt với một kiểu riêng biệt của nó. Hành vi của `typeof` là sai ở đây.
3. Kết quả của `typeof alert` là `"function"`, vì `alert` là một hàm. Chúng ta sẽ nghiên cứu các hàm trong các chương tiếp theo nơi chúng ta cũng sẽ thấy rằng không có “function” đặc biệt trong JavaScript. Các hàm thuộc về kiểu object. Nhưng `typeof` xử lý chúng khác biệt, trả về `"function"`. Điều đó cũng bắt nguồn từ những ngày đầu của JavaScript. Về mặt kỹ thuật, hành vi như vậy không đúng, nhưng có thể thuận tiện trong thực tế.

Cú pháp `typeof(x)`

Bạn cũng có thể gặp cú pháp khác: `typeof(x)`. Nó giống như `typeof x`.

Để làm rõ: `typeof` là một toán tử, không phải là một hàm. Dấu ngoặc đơn ở đây không phải là một phần của `typeof`. Đó là loại dấu ngoặc đơn được sử dụng cho nhóm toán học.

Thông thường, các dấu ngoặc đơn như vậy chứa một biểu thức toán học, chẳng hạn như `(2 + 2)`, nhưng ở đây chúng chỉ chứa một đối số `(x)`. Về mặt cú pháp, chúng cho phép tránh khoảng trắng giữa toán tử `typeof` và đối số của nó, và một số người thích điều đó.

Một số người thích `typeof(x)`, mặc dù cú pháp `typeof x` phổ biến hơn nhiều.

## [Tổng kết](#summary)

Có 8 kiểu dữ liệu cơ bản trong JavaScript.

- Bảy kiểu dữ liệu nguyên thủy:
  - `number` cho số của bất kỳ loại nào: số nguyên hoặc floating-point, số nguyên bị giới hạn bởi `±(2^53-1)`.
  - `bigint` cho số nguyên có độ dài tùy ý.
  - `string` cho chuỗi. Một chuỗi có thể có không hoặc nhiều ký tự, không có kiểu ký tự đơn riêng.
  - `boolean` cho `true`/`false`.
  - `null` cho các giá trị không biết – một kiểu độc lập có một giá trị duy nhất `null`.
  - `undefined` cho các giá trị chưa gán – một kiểu độc lập có một giá trị duy nhất `undefined`.
  - `symbol` cho các định danh duy nhất.
- Và một kiểu dữ liệu không nguyên thủy:
  - `object` cho các cấu trúc data phức tạp hơn.

Toán tử `typeof` cho phép chúng ta thấy kiểu nào đang được lưu trong một biến.

- Thông thường được sử dụng như `typeof x`, nhưng `typeof(x)` cũng có thể.
- Trả về một chuỗi với tên của kiểu, như `"string"`.
- Cho `null` trả về `"object"` – đây là một lỗi trong ngôn ngữ, nó không thực sự là một object.

Trong các chương tiếp theo, chúng ta sẽ tập trung vào các giá trị nguyên thủy và một khi chúng ta quen thuộc với chúng, chúng ta sẽ chuyển sang objects.

---

---

## Các bài tập

## [Các bài tập](#tasks)

### [Dấu ngoặc kép chuỗi](#string-quotes)

mức độ quan trọng: 5

Output của script là gì?

```
let name = "Ilya";

alert( `hello ${1}` ); // ?

alert( `hello ${"name"}` ); // ?

alert( `hello ${name}` ); // ?
```

lời giải

Backticks nhúng biểu thức bên trong `${...}` vào chuỗi.

```
let name = "Ilya";

// biểu thức là số 1
alert( `hello ${1}` ); // hello 1

// biểu thức là chuỗi "name"
alert( `hello ${"name"}` ); // hello name

// biểu thức là một biến, nhúng nó
alert( `hello ${name}` ); // hello Ilya
```
