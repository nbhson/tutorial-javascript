# Hàm

> Nguồn: [https://javascript.info/function-basics](https://javascript.info/function-basics)

<!-- fetched: 2026-09-14 -->

Rất thường xuyên, chúng ta cần thực hiện một hành động tương tự ở nhiều nơi trong script.

Vígiụ, chúng ta cần hiển thị thông điệp đẹp mắt khi người dùng đăng nhập, đăng xuất và có thể ở đâu đó khác.

Hàm là "khối xây dựng" chính của chương trình. Chúng cho phép mã được gọi nhiều lần mà không lặp lại.

Chúng ta đã thấy các ví dụ về hàm built-in, như `alert(message)`, `prompt(message, default)` và `confirm(question)`. Nhưng chúng ta cũng có thể tạo hàm của riêng mình.

## [Khai báo hàm](#function-declaration)

Để tạo một hàm, chúng ta có thể sử dụng *khai báo hàm*.

Nó trông như thế này:

```
function showMessage() {
  alert( 'Xin chào mọi người!' );
}
```

Từ khóa `function` đi trước, sau đó là *tên của hàm*, sau đó là danh sách *các tham số* giữa dấu ngoặc đơn (phân cách bằng dấu phẩy, trống trong ví dụ trên, chúng ta sẽ thấy các ví dụ sau) và cuối cùng là mã của hàm, cũng được gọi là "thân hàm", giữa dấu ngoặc nhọn.

```
function name(parameter1, parameter2, ... parameterN) {
  // body
}
```

Hàm mới của chúng ta có thể được gọi bằng tên của nó: `showMessage()`.

Vígiụ:

```
function showMessage() {
  alert( 'Xin chào mọi người!' );
}

showMessage();
showMessage();
```

Lệnh gọi `showMessage()` thực thi mã của hàm. Ở đây chúng ta sẽ thấy thông điệp hai lần.

Vígiụ này minh họa rõ ràng một trong những mục đích chính của hàm: tránh lặp lại mã.

Nếu chúng ta cần thay đổi thông điệp hoặc cách nó được hiển thị, chỉ cần sửa đổi mã trong một chỗ: hàm xuất nó.

## [Biến cục bộ](#local-variables)

Một biến được khai báo bên trong một hàm chỉ hiển thị trong hàm đó.

Vígiụ:

```
function showMessage() {
  let message = "Xin chào, tôi là JavaScript!"; // biến cục bộ

  alert( message );
}

showMessage(); // Xin chào, tôi là JavaScript!

alert( message ); // <-- Lỗi! Biến này là cục bộ của hàm
```

## [Biến ngoài](#outer-variables)

Một hàm có thể truy cập biến ngoài, ví dụ:

```
let userName = 'John';

function showMessage() {
  let message = 'Xin chào, ' + userName;
  alert(message);
}

showMessage(); // Xin chào, John
```

Hàm có quyền truy cập đầy đủ vào biến ngoài. Nó cũng có thể sửa đổi nó.

Vígiụ:

```
let userName = 'John';

function showMessage() {
  userName = "Bob"; // (1) thay đổi biến ngoài

  let message = 'Xin chào, ' + userName;
  alert(message);
}

alert( userName ); // John trước khi gọi hàm

showMessage();

alert( userName ); // Bob, giá trị đã được sửa đổi bởi hàm
```

Biến ngoài chỉ được sử dụng nếu không có biến cục bộ nào.

Nếu một biến cùng tên được khai báo bên trong hàm thì nó *che khuất* biến ngoài. Vígiụ, trong mã dưới đây, hàm sử dụng `userName` cục bộ. Biến ngoài bị bỏ qua:

```
let userName = 'John';

function showMessage() {
  let userName = "Bob"; // khai báo một biến cục bộ

  let message = 'Xin chào, ' + userName; // Bob
  alert(message);
}

// hàm sẽ tạo và sử dụng userName của riêng nó
showMessage();

alert( userName ); // John, không thay đổi, hàm không truy cập biến ngoài
```

Biến toàn cục

Các biến được khai báo bên ngoài bất kỳ hàm nào, như `userName` ngoài trong mã ở trên, được gọi là *toàn cục*.

Biến toàn cục hiển thị từ bất kỳ hàm nào (trừ khi bị che khuất bởi cục bộ).

Đây là practice tốt để giảm thiểu việc sử dụng biến toàn cục. Mã hiện đại có ít hoặc không có globals. Hầu hết các biến nằm trong các hàm của chúng. Đôi khi, chúng có thể hữu ích để lưu trữ dữ liệu cấp dự án.

## [Các tham số](#parameters)

Chúng ta có thể truyền dữ liệu tùy ý đến các hàm bằng cách sử dụng các tham số.

Trong ví dụ dưới đây, hàm có hai tham số: `from` và `text`.

```
function showMessage(from, text) { // parameters: from, text
  alert(from + ': ' + text);
}

showMessage('Ann', 'Xin chào!'); // Ann: Xin chào! (*)
showMessage('Ann', "Có chuyện gì?"); // Ann: Có chuyện gì? (**)
```

Khi hàm được gọi ở các dòng `(*)` và `(**)`, các giá trị được truyền vào được sao chép vào các biến cục bộ `from` và `text`. Sau đó, hàm sử dụng chúng.

Đây là một ví dụ khác: chúng ta có một biến `from` và truyền nó vào hàm. Xin lưu ý: hàm thay đổi `from`, nhưng sự thay đổi không được thấy bên ngoài, vì hàm luôn nhận một bản sao của giá trị:

```
function showMessage(from, text) {

  from = '*' + from + '*'; // làm cho "from" trông đẹp hơn

  alert( from + ': ' + text );
}

let from = "Ann";

showMessage(from, "Xin chào"); // *Ann*: Xin chào

// giá trị của "from" vẫn giống nhau, hàm đã sửa đổi bản sao cục bộ
alert( from ); // Ann
```

Khi một giá trị được truyền như một tham số hàm, nó cũng được gọi là *đối số*.

Nói cách khác, để làm rõ các thuật ngữ này:

- Một tham số là biến được liệt kê trong dấu ngoặc đơn trong khai báo hàm (nó là một thuật ngữ thời điểm khai báo).
- Một đối số là giá trị được truyền đến hàm khi nó được gọi (nó là một thuật ngữ thời điểm gọi).

Chúng ta khai báo hàm liệt kê các tham số của chúng, sau đó gọi chúng truyền các đối số.

Trong ví dụ trên, có thể nói: "hàm `showMessage` được khai báo với hai tham số, sau đó được gọi với hai đối số: `from` và `"Hello"`".

## [Giá trị mặc định](#default-values)

Nếu một hàm được gọi, nhưng một đối số không được cung cấp, thì giá trị tương ứng trở thành `undefined`.

Vígiụ, hàm `showMessage(from, text)` đã nói ở trên có thể được gọi với một đối số duy nhất:

```
showMessage("Ann");
```

Điều đó không phải lỗi. Lệnh gọi như vậy sẽ xuất ra `"*Ann*: undefined"`. Vì giá trị cho `text` không được truyền, nó trở thành `undefined`.

Chúng ta có thể chỉ định cái được gọi là "mặc định" (để sử dụng nếu bị bỏ qua) cho một tham số trong khai báo hàm, bằng cách sử dụng `=`:

```
function showMessage(from, text = "không có text") {
  alert( from + ": " + text );
}

showMessage("Ann"); // Ann: không có text
```

Bây giờ nếu tham số `text` không được truyền, nó sẽ nhận giá trị `"không có text"`.

Giá trị mặc định cũng nhảy vào nếu tham số tồn tại, nhưng strict bằng `undefined`, như thế này:

```
showMessage("Ann", undefined); // Ann: không có text
```

Ở đây `"không có text"` là một chuỗi, nhưng nó có thể là một biểu thức phức tạp hơn, chỉ được đánh giá và gán nếu tham số bị thiếu. Vì vậy, điều này cũng có thể:

```
function showMessage(from, text = anotherFunction()) {
  // anotherFunction() chỉ được thực thi nếu không có text
  // kết quả của nó trở thành giá trị của text
}
```

Đánh giá các tham số mặc định

Trong JavaScript, một tham số mặc định được đánh giá mỗi khi hàm được gọi mà không có tham số tương ứng.

Trong ví dụ trên, `anotherFunction()` không được gọi hoàn toàn, nếu tham số `text` được cung cấp.

Mặt khác, nó được gọi độc lập mỗi khi `text` bị thiếu.

Tham số mặc định trong mã JavaScript cũ

Vài năm trước, JavaScript không hỗ trợ cú pháp cho các tham số mặc định. Vì vậy, người ta đã sử dụng các cách khác để chỉ định chúng.

Ngày nay, chúng ta có thể gặp chúng trong các script cũ.

Vígiụ, kiểm tra rõ ràng cho `undefined`:

```
function showMessage(from, text) {
  if (text === undefined) {
    text = 'không có text';
  }

  alert( from + ": " + text );
}
```

…Hoặc sử dụng toán tử `||`:

```
function showMessage(from, text) {
  // Nếu giá trị của text là falsy, gán giá trị mặc định
  // điều này giả định rằng text == "" giống như không có text
  text = text || 'không có text';
  ...
}
```

### [Tham số mặc định thay thế](#alternative-default-parameters)

Đôi khi có ý nghĩa để gán giá trị mặc định cho các tham số ở giai đoạn sau sau khi khai báo hàm.

Chúng ta có thể kiểm tra xem tham số có được truyền trong quá trình thực thi hàm không, bằng cách so sánh nó với `undefined`:

```
function showMessage(text) {
  // ...

  if (text === undefined) { // nếu tham số bị thiếu
    text = 'thông điệp trống';
  }

  alert(text);
}

showMessage(); // thông điệp trống
```

…Hoặc chúng ta có thể sử dụng toán tử `||`:

```
function showMessage(text) {
  // nếu text là undefined hoặc nói chung là falsy, đặt nó thành 'empty'
  text = text || 'empty';
  ...
}
```

JavaScript hiện đại hỗ trợ [toán tử ghép không rỗng](/nullish-coalescing-operator) `??`, nó tốt hơn khi hầu hết các giá trị falsy, như `0`, nên được coi là "bình thường":

```
function showCount(count) {
  // nếu count là undefined hoặc null, hiển thị "unknown"
  alert(count ?? "unknown");
}

showCount(0); // 0
showCount(null); // unknown
showCount(); // unknown
```

## [Trả về giá trị](#returning-a-value)

Một hàm có thể trả về một giá trị vào mã gọi như là kết quả.

Vígiụ đơn giản nhất là một hàm cộng hai giá trị:

```
function sum(a, b) {
  return a + b;
}

let result = sum(1, 2);
alert( result ); // 3
```

Chỉ thị `return` có thể ở bất kỳ vị trí nào trong hàm. Khi việc thực thi đạt đến nó, hàm dừng và giá trị được trả về cho mã gọi (được gán cho `result` ở trên).

Có thể có nhiều lần xuất hiện của `return` trong một hàm. Vígiụ:

```
function checkAge(age) {
  if (age >= 18) {
    return true;
  } else {
    return confirm('Bạn có được phép của cha mẹ không?');
  }
}

let age = prompt('Bạn bao nhiêu tuổi?', 18);

if ( checkAge(age) ) {
  alert( 'Được truy cập' );
} else {
  alert( 'Bị từ chối' );
}
```

Có thể sử dụng `return` mà không có giá trị. Điều đó khiến hàm thoát ngay lập tức.

Vígiụ:

```
function showMovie(age) {
  if ( !checkAge(age) ) {
    return;
  }

  alert( "Hiển thị phim cho bạn" ); // (*)
  // ...
}
```

Trong mã ở trên, nếu `checkAge(age)` trả về `false`, thì `showMovie` sẽ không tiến tới `alert`.

Hàm với `return` trống hoặc không có nó trả về `undefined`

Nếu một hàm không trả về giá trị, nó giống như nếu nó trả về `undefined`:

```
function doNothing() { /* trống */ }

alert( doNothing() === undefined ); // true
```

`return` trống cũng giống như `return undefined`:

```
function doNothing() {
  return;
}

alert( doNothing() === undefined ); // true
```

Không thêm newline giữa `return` và giá trị

Đối với một biểu thức dài trong `return`, có thểtempting để đặt nó trên một dòng riêng, như thế này:

```
return
 (some + long + expression + or + whatever * f(a) + f(b))
```

Điều đó không hoạt động, vì JavaScript giả định một dấu chấm phẩy sau `return`. Nó sẽ hoạt động giống như:

```
return;
 (some + long + expression + or + whatever * f(a) + f(b))
```

Vì vậy, về cơ bản nó trở thành một return trống.

Nếu chúng ta muốn biểu thức được trả về wrap qua nhiều dòng, chúng ta nên bắt đầu nó ở cùng dòng với `return`. Hoặc ít nhất là đặt dấu ngoặc đơn mở ở đó như sau:

```
return (
  some + long + expression
  + or +
  whatever * f(a) + f(b)
  )
```

Và nó sẽ hoạt động giống như chúng ta mong đợi.

## [Đặt tên hàm](#function-naming)

Hàm là các hành động. Vì vậy, tên của chúng thường là động từ. Nó nên ngắn gọn, chính xác nhất có thể và mô tả hàm làm gì, vì vậy ai đó đọc mã sẽ có ý tưởng về những gì hàm làm.

Đây là practice phổ biến để bắt đầu hàm với một tiền tố động từ mơ hồ mô tả hành động. Phải có sự thỏa thuận trong đội về ý nghĩa của các tiền tố.

Vígiụ, các hàm bắt đầu với "show" thường hiển thị cái gì đó.

Hàm bắt đầu với…

- `"get…"` – trả về một giá trị,
- `"calc…"` – tính toán cái gì đó,
- `"create…"` – tạo ra cái gì đó,
- `"check…"` – kiểm tra cái gì đó và trả về boolean, v.v.

Vígiụ về các tên như vậy:

```
showMessage(..)     // hiển thị một thông điệp
getAge(..)          // trả về tuổi (lấy nó bằng cách nào đó)
calcSum(..)         // tính toán một tổng và trả về kết quả
createForm(..)      // tạo một form (và thường trả về nó)
checkPermission(..) // kiểm tra một quyền, trả về true/false
```

Với các tiền tố ở vị trí, một cái nhìn thoáng qua vào tên hàm cho hiểu loại công việc nó làm và loại giá trị nó trả về.

Một hàm – một hành động

Một hàm nên làm chính xác những gì được gợi ý bởi tên của nó, không nhiều hơn.

Hai hành động độc lập thường xứng đáng hai hàm, ngay cả khi chúng thường được gọi cùng nhau (trong trường hợp đó chúng ta có thể tạo hàm thứ 3 gọi hai hàm đó).

Một vài ví dụ về việc vi phạm quy tắc này:

- `getAge` – sẽ xấu nếu nó hiển thị `alert` với tuổi (chỉ nên lấy).
- `createForm` – sẽ xấu nếu nó sửa đổi document, thêm một form vào đó (chỉ nên tạo nó và trả về).
- `checkPermission` – sẽ xấu nếu nó hiển thị thông điệp `truy cập được cho phép/từ chối` (chỉ nên thực hiện kiểm tra và trả về kết quả).

Các ví dụ này giả định ý nghĩa phổ biến của các tiền tố. Bạn và đội của bạn có thể tự do thỏa thuận về các ý nghĩa khác, nhưng thường chúng không khác nhiều. Trong bất kỳ trường hợp nào, bạn nên có hiểu biết vững chắc về ý nghĩa của một tiền tố, những gì một hàm có tiền tố có thể và không thể làm. Tất cả các hàm cùng tiền tố nên tuân theo các quy tắc. Và đội nên chia sẻ kiến thức.

Tên hàm siêu ngắn

Các hàm được sử dụng *rất thường xuyên* đôi khi có tên siêu ngắn.

Vígiụ, framework [jQuery](https://jquery.com/) định nghĩa một hàm với `$`. Thư viện [Lodash](https://lodash.com/) có hàm cốt lõi của nó được đặt tên là `_`.

Đây là các ngoại lệ. Nói chung, tên hàm nên ngắn gọn và mô tả.

## [Hàm == Comment](#functions-comments)

Hàm nên ngắn và làm chính xác một thứ. Nếu thứ đó lớn, có lẽ nên tách hàm thành một vài hàm nhỏ hơn. Đôi khi làm theo quy tắc này có thể không dễ dàng, nhưng chắc chắn đó là điều tốt.

Một hàm riêng biệt không chỉ dễ kiểm tra và debug hơn – sự tồn tại của nó là một comment tuyệt vời!

Vígiụ, hãy so sánh hai hàm `showPrimes(n)` dưới đây. Mỗi cái hiển thị [các số nguyên tố](https://en.wikipedia.org/wiki/Prime_number) lên đến `n`.

Biến thể đầu tiên sử dụng một label:

```
function showPrimes(n) {
  nextPrime: for (let i = 2; i < n; i++) {

    for (let j = 2; j < i; j++) {
      if (i % j == 0) continue nextPrime;
    }

    alert( i ); // một số nguyên tố
  }
}
```

Biến thể thứ hai sử dụng một hàm bổ sung `isPrime(n)` để kiểm tra tính nguyên tố:

```
function showPrimes(n) {

  for (let i = 2; i < n; i++) {
    if (!isPrime(i)) continue;

    alert(i);  // một số nguyên tố
  }
}

function isPrime(n) {
  for (let i = 2; i < n; i++) {
    if ( n % i == 0) return false;
  }
  return true;
}
```

Biến thể thứ hai dễ hiểu hơn, phải không? Thay vì đoạn mã, chúng ta thấy tên của hành động (`isPrime`). Đôi khi người ta gọi mã như vậy là *tự mô tả*.

Vì vậy, hàm có thể được tạo ngay cả khi chúng ta không dự định tái sử dụng chúng. Chúng cấu trúc mã và làm cho nó dễ đọc.

## [Tổng kết](#summary)

Một khai báo hàm trông như thế này:

```
function name(parameters, delimited, by, comma) {
  /* code */
}
```

- Giá trị được truyền đến hàm như các tham số được sao chép vào các biến cục bộ của nó.
- Một hàm có thể truy cập các biến ngoài. Nhưng nó chỉ hoạt động từ trong ra ngoài. Mã bên ngoài hàm không nhìn thấy các biến cục bộ của nó.
- Một hàm có thể trả về một giá trị. Nếu nó không, thì kết quả của nó là `undefined`.

Để làm cho mã sạch sẽ và dễ hiểu, khuyến nghị chủ yếu sử dụng các biến cục bộ và tham số trong hàm, không phải biến ngoài.

Luôn luôn dễ hiểu hơn một hàm nhận các tham số, làm việc với chúng và trả về kết quả hơn một hàm không nhận tham số, nhưng sửa đổi các biến ngoài như một tác dụng phụ.

Đặt tên hàm:

- Tên nên mô tả rõ ràng hàm làm gì. Khi chúng ta thấy một lệnh gọi hàm trong mã, một tên tốt ngay lập tức cho chúng ta hiểu nó làm gì và trả về gì.
- Một hàm là một hành động, vì vậy tên hàm thường là động từ.
- Có nhiều tiền tố hàm nổi tiếng như `create…`, `show…`, `get…`, `check…` và vân vân. Sử dụng chúng để gợi ý hàm làm gì.

Hàm là các khối xây dựng chính của scripts. Bây giờ chúng ta đã bao quát các cơ bản, vì vậy thực tế chúng ta có thể bắt đầu tạo và sử dụng chúng. Nhưng đó chỉ là bắt đầu của con đường. Chúng ta sẽ quay lại chúng nhiều lần, đi sâu hơn vào các tính năng nâng cao của chúng.

---

---

## Các bài tập

## [Các bài tập](#tasks)

### [Có cần "else" không?](#is-else-required)

mức độ quan trọng: 4

Hàm sau đây trả về `true` nếu tham số `age` lớn hơn `18`.

Nếu không, nó yêu cầu xác nhận và trả về kết quả của nó:

```
function checkAge(age) {
  if (age > 18) {
    return true;
  } else {
    // ...
    return confirm('Bạn có được phép của cha mẹ không?');
  }
}
```

Hàm sẽ hoạt động khác nếu `else` bị xóa?

```
function checkAge(age) {
  if (age > 18) {
    return true;
  }
  // ...
  return confirm('Bạn có được phép của cha mẹ không?');
}
```

Có sự khác biệt nào trong hành vi của hai biến thể này không?

lời giải

Không có sự khác biệt!

Trong cả hai trường hợp, `return confirm('Bạn có được phép của cha mẹ không?')` thực thi chính xác khi điều kiện `if` là falsy.

### [Viết lại hàm bằng '?' hoặc '||'](#rewrite-the-function-using-or)

mức độ quan trọng: 4

Hàm sau đây trả về `true` nếu tham số `age` lớn hơn `18`.

Nếu không, nó yêu cầu xác nhận và trả về kết quả của nó.

```
function checkAge(age) {
  if (age > 18) {
    return true;
  } else {
    return confirm('Bạn có được phép của cha mẹ không?');
  }
}
```

Viết lại nó, để thực hiện cùng, nhưng không có `if`, trong một dòng.

Tạo hai biến thể của `checkAge`:

1. Sử dụng toán tử dấu chấm hỏi `?`
2. Sử dụng HOẶC `||`

lời giải

Sử dụng toán tử dấu chấm hỏi `'?'`:

```
function checkAge(age) {
  return (age > 18) ? true : confirm('Bạn có được phép của cha mẹ không?');
}
```

Sử dụng HOẶC `||` (biến thể ngắn nhất):

```
function checkAge(age) {
  return (age > 18) || confirm('Bạn có được phép của cha mẹ không?');
}
```

Lưu ý rằng dấu ngoặc đơn xung quanh `age > 18` không bắt buộc ở đây. Chúng tồn tại để dễ đọc hơn.

### [Hàm min(a, b)](#function-min-a-b)

mức độ quan trọng: 1

Viết một hàm `min(a,b)` trả về số nhỏ nhất trong hai số `a` và `b`.

Vígiụ:

```
min(2, 5) == 2
min(3, -1) == -1
min(1, 1) == 1
```

lời giải

Một lời giải sử dụng `if`:

```
function min(a, b) {
  if (a < b) {
    return a;
  } else {
    return b;
  }
}
```

Một lời giải với toán tử dấu chấm hỏi `'?'`:

```
function min(a, b) {
  return a < b ? a : b;
}
```

P.S. Trong trường hợp bằng nhau `a == b`, không quan trọng trả về cái gì.

### [Hàm pow(x,n)](#function-pow-x-n)

mức độ quan trọng: 4

Viết một hàm `pow(x,n)` trả về `x` mũ `n`. Hay nói cách khác, nhân `x` với chính nó `n` lần và trả về kết quả.

```
pow(3, 2) = 3 * 3 = 9
pow(3, 3) = 3 * 3 * 3 = 27
pow(1, 100) = 1 * 1 * ...* 1 = 1
```

Tạo một trang web yêu cầu nhập `x` và `n`, và sau đó hiển thị kết quả của `pow(x,n)`.

[Chạy demo](#)

P.S. Trong bài tập này, hàm chỉ hỗ trợ các giá trị tự nhiên của `n`: các số nguyên từ `1` trở lên.

lời giải

```
function pow(x, n) {
  let result = x;

  for (let i = 1; i < n; i++) {
    result *= x;
  }

  return result;
}

let x = +prompt("x?", '');
let n = +prompt("n?", '');

if (n < 1) {
  alert(`Lũy thừa ${n} không được hỗ trợ, sử dụng số nguyên dương`);
} else {
  alert( pow(x, n) );
}
```
