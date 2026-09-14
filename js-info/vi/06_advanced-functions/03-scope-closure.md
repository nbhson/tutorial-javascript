# Phạm vi biến, closure

> Nguồn: [https://javascript.info/closure](https://javascript.info/closure)

<!-- fetched: 2026-09-14 -->

JavaScript là một ngôn ngữ hướng hàm rất mạnh. Nó mang lại cho chúng ta nhiều sự tự do. Một hàm có thể được tạo ra bất cứ lúc nào, được truyền như một đối số đến hàm khác, và sau đó được gọi từ một vị trí hoàn toàn khác trong mã.

Chúng ta đã biết rằng một hàm có thể truy cập các biến bên ngoài nó ("biến ngoài").

Nhưng điều gì sẽ xảy ra nếu các biến ngoài thay đổi kể từ khi hàm được tạo? Hàm sẽ lấy giá trị mới hay giá trị cũ?

Và nếu một hàm được truyền như một đối số và được gọi từ một vị trí khác trong mã, liệu nó có thể truy cập các biến ngoài tại vị trí mới hay không?

Hãy mở rộng kiến thức của chúng ta để hiểu những kịch bản này và những trường hợp phức tạp hơn.

Chúng ta sẽ nói về các biến `let/const` ở đây

Trong JavaScript, có 3 cách để khai báo biến: `let`, `const` (các cách hiện đại), và `var` (di sản của quá khứ).

- Trong bài viết này, chúng ta sẽ sử dụng biến `let` trong các ví dụ.
- Các biến được khai báo với `const` hoạt động giống hệt, vì vậy bài viết này cũng áp dụng cho `const`.
- `var` cũ có một số khác biệt đáng chú ý, chúng sẽ được trình bày trong bài viết [Var cũ](/var).

## [Khối mã](#code-blocks)

Nếu một biến được khai báo bên trong một khối mã `{...}`, nó chỉ hiển thị trong khối đó.

Ví dụ:

```
{
  // thực hiện một số công việc với các biến cục bộ không nên hiển thị ra ngoài

  let message = "Hello"; // chỉ hiển thị trong khối này

  alert(message); // Hello
}

alert(message); // Error: message is not defined
```

Chúng ta có thể sử dụng điều này để cô lập một đoạn mã thực hiện nhiệm vụ riêng, với các biến chỉ thuộc về nó:

```
{
  // hiển thị thông điệp
  let message = "Hello";
  alert(message);
}

{
  // hiển thị một thông điệp khác
  let message = "Goodbye";
  alert(message);
}
```
Sẽ có lỗi nếu không có các khối

Xin lưu ý, không có các khối riêng biệt sẽ gây ra lỗi, nếu chúng ta sử dụng `let` với tên biến đã tồn tại:

```
// hiển thị thông điệp
let message = "Hello";
alert(message);

// hiển thị một thông điệp khác
let message = "Goodbye"; // Lỗi: biến đã được khai báo
alert(message);
```

Đối với `if`, `for`, `while` và tương tự, các biến được khai báo trong `{...}` cũng chỉ hiển thị bên trong:

```
if (true) {
  let phrase = "Hello!";

  alert(phrase); // Hello!
}

alert(phrase); // Lỗi, không có biến đó!
```

Ở đây, sau khi `if` kết thúc, `alert` bên dưới sẽ không thể nhìn thấy `phrase`, do đó gây ra lỗi.

Điều này rất tuyệt vì nó cho phép chúng ta tạo các biến cục bộ trong khối, cụ thể cho một nhánh `if`.

Điều tương tự cũng đúng với các vòng lặp `for` và `while`:

```
for (let i = 0; i < 3; i++) {
  // biến i chỉ hiển thị bên trong vòng for này
  alert(i); // 0, sau đó 1, sau đó 2
}

alert(i); // Lỗi, không có biến đó
```

Theo trực quan, `let i` nằm ngoài `{...}`. Nhưng cấu trúc `for` ở đây đặc biệt: biến được khai báo bên trong nó được coi là một phần của khối.

## [Hàm lồng nhau](#nested-functions)

Một hàm được gọi là "hàm lồng nhau" khi nó được tạo bên trong một hàm khác.

Điều này dễ dàng thực hiện được với JavaScript.

Chúng ta có thể sử dụng nó để tổ chức mã của mình, như thế này:

```
function sayHiBye(firstName, lastName) {

  // hàm helper lồng nhau để sử dụng bên dưới
  function getFullName() {
    return firstName + " " + lastName;
  }

  alert( "Hello, " + getFullName() );
  alert( "Bye, " + getFullName() );

}
```

Hàm *lồng nhau* `getFullName()` được tạo ra để thuận tiện. Nó có thể truy cập các biến ngoài và do đó có thể trả về tên đầy đủ. Hàm lồng nhau khá phổ biến trong JavaScript.

Điều thú vị hơn cả là một hàm lồng nhau có thể được trả về: như một thuộc tính của một đối tượng mới hoặc là kết quả trực tiếp. Nó sau đó có thể được sử dụng ở nơi khác. Bất kể ở đâu, nó vẫn có quyền truy cập vào các biến ngoài cùng.

Bên dưới, `makeCounter` tạo ra hàm "đếm" trả về số tiếp theo sau mỗi lần gọi:

```
function makeCounter() {
  let count = 0;

  return function() {
    return count++;
  };
}

let counter = makeCounter();

alert( counter() ); // 0
alert( counter() ); // 1
alert( counter() ); // 2
```

Mặc dù đơn giản, các biến thể hơi được sửa đổi của mã đó có ứng dụng thực tế, chẳng hạn như một [máy tạo số ngẫu nhiên](https://en.wikipedia.org/wiki/Pseudorandom_number_generator) để tạo các giá trị ngẫu nhiên cho các bài kiểm tra tự động.

Cách hoạt động của nó là gì? Nếu chúng ta tạo nhiều bộ đếm, chúng có độc lập không? Điều gì đang xảy ra với các biến ở đây?

Hiểu những điều như vậy rất tốt cho kiến thức tổng thể về JavaScript và hữu ích cho các kịch bản phức tạp hơn. Vì vậy, hãy đi sâu một chút.

## [Môi trường từ vựng](#lexical-environment)

Đây là phần chuyên sâu!

Giải thích kỹ thuật chi tiết đang chờ đón bạn.

Dù tôi muốn tránh các chi tiết ngôn ngữ cấp thấp, bất kỳ sự hiểu biết nào thiếu chúng đều không đầy đủ, vì vậy hãy chuẩn bị tinh thần.

Để rõ ràng, phần giải thích được chia thành nhiều bước.

### [Bước 1. Biến](#step-1-variables)

Trong JavaScript, mọi hàm đang chạy, khối mã `{...}`, và toàn bộ kịch bản đều có một đối tượng nội bộ (ẩn) được gọi là *Môi trường từ vựng* (Lexical Environment).

Đối tượng Môi trường từ vựng bao gồm hai phần:

1. *Environment Record* – đối tượng lưu trữ tất cả các biến cục bộ như các thuộc tính của nó (và một số thông tin khác như giá trị của `this`).
2. Một tham chiếu đến *môi trường từ vựng ngoài*, là môi trường được liên kết với mã bên ngoài.

**"Biến" chỉ là một thuộc tính của đối tượng nội bộ đặc biệt `Environment Record`. "Lấy hoặc thay đổi biến" có nghĩa là "lấy hoặc thay đổi thuộc tính của đối tượng đó".**

Trong mã đơn giản không có hàm, chỉ có một Môi trường từ vựng:

![](/article/closure/lexical-environment-global.svg)

Đây là Môi trường từ vựng *toàn cục*, được liên kết với toàn bộ kịch bản.

Trong hình trên, hình chữ nhật có nghĩa là Environment Record (bộ lưu trữ biến) và mũi tên có nghĩa là tham chiếu ra ngoài. Môi trường từ vựng toàn cục không có tham chiếu ra ngoài, đó là lý do tại sao mũi tên trỏ đến `null`.

Khi mã bắt đầu thực thi và tiếp tục, Môi trường từ vựng thay đổi.

Đây là một mã dài hơn một chút:

![](/article/closure/closure-variable-phrase.svg)

Các hình chữ nhật ở bên phải minh họa cách Môi trường từ vựng toàn cục thay đổi trong quá trình thực thi:

1. Khi kịch bản bắt đầu, Môi trường từ vựng được điền sẵn với tất cả các biến đã khai báo.
   - Ban đầu, chúng ở trạng thái "Chưa khởi tạo" (Uninitialized). Đó là một trạng thái nội bộ đặc biệt, có nghĩa là engine biết về biến nhưng không thể tham chiếu đến nó cho đến khi nó được khai báo với `let`. Nó gần như giống hệt như biến không tồn tại.
2. Sau đó định nghĩa `let phrase` xuất hiện. Chưa có phép gán, vì vậy giá trị của nó là `undefined`. Chúng ta có thể sử dụng biến từ thời điểm này trở đi.
3. `phrase` được gán một giá trị.
4. `phrase` thay đổi giá trị.

Tất cả trông rất đơn giản cho đến giờ, phải không?

- Biến là một thuộc tính của một đối tượng nội bộ đặc biệt, được liên kết với khối/hàm/kịch bản đang thực thi.
- Làm việc với biến thực chất là làm việc với các thuộc tính của đối tượng đó.

Môi trường từ vựng là một đối tượng đặc tả

"Môi trường từ vựng" là một đối tượng đặc tả: nó chỉ tồn tại "một cách lý thuyết" trong [đặc tả ngôn ngữ](https://tc39.es/ecma262/#sec-lexical-environments) để mô tả cách mọi thứ hoạt động. Chúng ta không thể lấy đối tượng này trong mã của mình và thao tác trực tiếp.

Các engine JavaScript cũng có thể tối ưu hóa nó, loại bỏ các biến không được sử dụng để tiết kiệm bộ nhớ và thực hiện các thủ thuật nội bộ khác, miễn là hành vi hiển thị vẫn được mô tả như trên.

### [Bước 2. Khai báo hàm](#step-2-function-declarations)

Hàm cũng là một giá trị, giống như biến.

**Sự khác biệt là Function Declaration được khởi tạo đầy đủ ngay lập tức.**

Khi một Môi trường từ vựng được tạo, một Function Declaration ngay lập tức trở thành một hàm sẵn sàng sử dụng (không giống như `let`, không thể sử dụng cho đến khi khai báo).

Đó là lý do tại sao chúng ta có thể sử dụng một hàm được khai báo là Function Declaration ngay cả trước khi khai báo chính nó.

Ví dụ, đây là trạng thái ban đầu của Môi trường từ vựng toàn cục khi chúng ta thêm một hàm:

![](/article/closure/closure-function-declaration.svg)

Tất nhiên, hành vi này chỉ áp dụng cho Function Declarations, không phải Function Expressions nơi chúng ta gán hàm cho một biến, chẳng hạn như `let say = function(name)...`.

### [Bước 3. Môi trường từ vựng trong và ngoài](#step-3-inner-and-outer-lexical-environment)

Khi một hàm chạy, ở đầu lời gọi, một Môi trường từ vựng mới được tạo tự động để lưu trữ các biến cục bộ và tham số của lời gọi.

Ví dụ, đối với `say("John")`, nó trông như thế này (việc thực thi đang ở dòng được gắn nhãn bằng mũi tên):

![](/article/closure/lexical-environment-simple.svg)

Trong quá trình gọi hàm, chúng ta có hai Môi trường từ vựng: môi trường trong (cho lời gọi hàm) và môi trường ngoài (toàn cục):

- Môi trường từ vựng trong tương ứng với việc thực thi hiện tại của `say`. Nó có một thuộc tính: `name`, đối số của hàm. Chúng ta đã gọi `say("John")`, vì vậy giá trị của `name` là `"John"`.
- Môi trường từ vựng ngoài là Môi trường từ vựng toàn cục. Nó có biến `phrase` và chính hàm đó.

Môi trường từ vựng trong có một tham chiếu đến môi trường `ngoài`.

**Khi mã muốn truy cập một biến – Môi trường từ vựng trong được tìm kiếm trước, sau đó đến môi trường ngoài, rồi đến môi trường ngoài hơn nữa và cứ thế cho đến khi đạt đến toàn cục.**

Nếu không tìm thấy biến ở bất kỳ đâu, đó là lỗi trong chế độ strict (không có `use strict`, việc gán cho biến không tồn tại sẽ tạo ra một biến toàn cục mới, để tương thích với mã cũ).

Trong ví dụ này, việc tìm kiếm diễn ra như sau:

- Đối với biến `name`, `alert` bên trong `say` tìm thấy nó ngay lập tức trong Môi trường từ vựng trong.
- Khi nó muốn truy cập `phrase`, thì không có `phrase` cục bộ, vì vậy nó đi theo tham chiếu đến Môi trường từ vựng ngoài và tìm thấy nó ở đó.

![](/article/closure/lexical-environment-simple-lookup.svg)

### [Bước 4. Trả về một hàm](#step-4-returning-a-function)

Hãy quay lại ví dụ `makeCounter`.

```
function makeCounter() {
  let count = 0;

  return function() {
    return count++;
  };
}

let counter = makeCounter();
```

Ở đầu mỗi lần gọi `makeCounter()`, một đối tượng Môi trường từ vựng mới được tạo, để lưu trữ các biến cho lần chạy `makeCounter` này.

Vì vậy, chúng ta có hai Môi trường từ vựng lồng nhau, giống như trong ví dụ trên:

![](/article/closure/closure-makecounter.svg)

Điều khác biệt là, trong quá trình thực thi `makeCounter()`, một hàm nhỏ lồng nhau chỉ có một dòng được tạo: `return count++`. Chúng ta chưa chạy nó, chỉ tạo ra.

Tất cả các hàm ghi nhớ Môi trường từ vựng mà chúng được tạo. Về mặt kỹ thuật, không có phép màu nào ở đây: tất cả các hàm có thuộc tính ẩn được đặt tên là `[[Environment]]`, lưu trữ tham chiếu đến Môi trường từ vựng nơi hàm được tạo:

![](/article/closure/closure-makecounter-environment.svg)

Vì vậy, `counter.[[Environment]]` có tham chiếu đến Môi trường từ vựng `{count: 0}`. Đó là cách hàm ghi nhớ nơi nó được tạo, bất kể nó được gọi ở đâu. Tham chiếu `[[Environment]]` được đặt một lần và mãi mãi tại thời điểm tạo hàm.

Sau đó, khi `counter()` được gọi, một Môi trường từ vựng mới được tạo cho lời gọi, và tham chiếu Môi trường từ vựng ngoài của nó được lấy từ `counter.[[Environment]]`:

![](/article/closure/closure-makecounter-nested-call.svg)

Bây giờ khi mã bên trong `counter()` tìm biến `count`, nó trước tiên tìm trong Môi trường từ vựng của chính nó (trống, vì không có biến cục bộ nào ở đó), sau đó tìm trong Môi trường từ vựng của lời gọi `makeCounter()` ngoài, nơi nó tìm thấy và thay đổi nó.

**Biến được cập nhật trong Môi trường từ vựng nơi nó sống.**

Đây là trạng thái sau khi thực thi:

![](/article/closure/closure-makecounter-nested-call-2.svg)

Nếu chúng ta gọi `counter()` nhiều lần, biến `count` sẽ được tăng lên `2`, `3` và cứ thế, tại cùng một vị trí.

Closure

Có một thuật ngữ lập trình tổng quát "closure", mà các nhà phát triển nói chung nên biết.

[Một closure](https://en.wikipedia.org/wiki/Closure_(computer_programming)) là một hàm ghi nhớ các biến ngoài của nó và có thể truy cập chúng. Trong một số ngôn ngữ, điều đó không khả thi, hoặc hàm phải được viết theo một cách đặc biệt để thực hiện được điều đó. Nhưng như đã giải thích ở trên, trong JavaScript, tất cả các hàm đều là closures (có một ngoại lệ duy nhất, sẽ được đề cập trong [Cú pháp "new Function"](/new-function)).

Điều đó có nghĩa là: chúng tự động ghi nhớ nơi chúng được tạo bằng thuộc tính `[[Environment]]` ẩn, và sau đó mã của chúng có thể truy cập các biến ngoài.

Khi phỏng vấn, một nhà phát triển frontend được hỏi về "closure là gì?", câu trả lời hợp lệ sẽ là định nghĩa của closure và giải thích rằng tất cả các hàm trong JavaScript đều là closures, và có lẽ vài lời更多关于 chi tiết kỹ thuật: thuộc tính `[[Environment]]` và cách Môi trường từ vựng hoạt động.

## [Thu gom rác](#garbage-collection)

Thông thường, Môi trường từ vựng bị xoá khỏi bộ nhớ cùng với tất cả các biến sau khi lời gọi hàm kết thúc. Đó là vì không có tham chiếu nào đến nó. Giống như bất kỳ đối tượng JavaScript nào, nó chỉ được giữ trong bộ nhớ khi còn có thể truy cập được.

Tuy nhiên, nếu có một hàm lồng nhau vẫn có thể truy cập được sau khi hàm kết thúc, thì nó có thuộc tính `[[Environment]]` trỏ đến môi trường từ vựng.

Trong trường hợp đó, Môi trường từ vựng vẫn có thể truy cập được ngay cả sau khi hàm hoàn tất, vì vậy nó vẫn sống.

Ví dụ:

```
function f() {
  let value = 123;

  return function() {
    alert(value);
  }
}

let g = f(); // g.[[Environment]] lưu trữ một tham chiếu đến Môi trường từ vựng
// của lời gọi f() tương ứng
```

Xin lưu ý rằng nếu `f()` được gọi nhiều lần, và các hàm kết quả được lưu, thì tất cả các đối tượng Môi trường từ vựng tương ứng cũng sẽ được giữ lại trong bộ nhớ. Trong mã dưới đây, cả 3 cái:

```
function f() {
  let value = Math.random();

  return function() { alert(value); };
}

// 3 hàm trong mảng, mỗi hàm đều trỏ đến Môi trường từ vựng
// từ lần chạy f() tương ứng
let arr = [f(), f(), f()];
```

Một đối tượng Môi trường từ vựng chết khi nó không thể truy cập được (giống như bất kỳ đối tượng nào khác). Nói cách khác, nó chỉ tồn tại khi có ít nhất một hàm lồng nhau trỏ đến nó.

Trong mã dưới đây, sau khi hàm lồng nhau bị xoá, Môi trường từ vựng bao quanh nó (và do đó là `value`) được dọn dẹp khỏi bộ nhớ:

```
function f() {
  let value = 123;

  return function() {
    alert(value);
  }
}

let g = f(); // trong khi hàm g tồn tại, giá trị vẫn tồn tại trong bộ nhớ

g = null; // ...và bây giờ bộ nhớ được dọn dẹp
```

### [Tối ưu hoá trong thực tế](#real-life-optimizations)

Như chúng ta đã thấy, về lý thuyết trong khi một hàm còn sống, tất cả các biến ngoài cũng được giữ lại.

Nhưng trong thực tế, các engine JavaScript cố gắng tối ưu hóa điều đó. Chúng phân tích việc sử dụng biến và nếu rõ ràng từ mã rằng một biến ngoài không được sử dụng – nó sẽ bị xoá.

**Một hiệu ứng phụ quan trọng trong V8 (Chrome, Edge, Opera) là biến đó sẽ trở nên không khả dụng trong quá trình gỡ lỗi.**

Hãy thử chạy ví dụ dưới đây trong Chrome với Developer Tools đang mở.

Khi nó tạm dừng, trong console gõ `alert(value)`.

```
function f() {
  let value = Math.random();

  function g() {
    debugger; // trong console: gõ alert(value); Không có biến đó!
  }

  return g;
}

let g = f();
g();
```

Như bạn có thể thấy – không có biến đó! Về lý thuyết, nó nên có thể truy cập được, nhưng engine đã tối ưu hóa nó ra.

Điều đó có thể dẫn đến các vấn đề gỡ lỗi kỳ lạ (nếu không phải là tốn thời gian). Một trong số chúng – chúng ta có thể thấy một biến ngoài cùng tên thay vì biến mong đợi:

```
let value = "Surprise!";

function f() {
  let value = "the closest value";

  function g() {
    debugger; // trong console: gõ alert(value); Surprise!
  }

  return g;
}

let g = f();
g();
```

Tính năng này của V8 là điều đáng biết. Nếu bạn đang gỡ lỗi với Chrome/Edge/Opera, sớm hay muộn bạn sẽ gặp phải nó.

Đó không phải là lỗi trong trình gỡ lỗi, mà là một tính năng đặc biệt của V8. Có lẽ nó sẽ được thay đổi vào một lúc nào đó. Bạn luôn có thể kiểm tra bằng cách chạy các ví dụ trên trang này.

---

---

## Bài tập

## [Bài tập](#tasks)

### [Hàm có lấy thay đổi mới nhất không?](#does-a-function-pickup-latest-changes)

độ quan trọng: 5

Hàm sayHi sử dụng biến ngoài name. Khi hàm chạy, nó sẽ sử dụng giá trị nào?

```
let name = "John";

function sayHi() {
  alert("Hi, " + name);
}

name = "Pete";

sayHi(); // nó sẽ hiển thị: "John" hay "Pete"?
```

Những tình huống như vậy phổ biến cả trong phát triển trình duyệt và server-side. Một hàm có thể được lên lịch thực thi sau khi nó được tạo, chẳng hạn như sau khi người dùng thực hiện hành động hoặc yêu cầu mạng.

Vì vậy, câu hỏi là: nó có lấy những thay đổi mới nhất không?

solution

Câu trả lời là: **Pete**.

Hàm nhận các biến ngoài như chúng đang tồn tại hiện tại, nó sử dụng các giá trị mới nhất.

Các giá trị biến cũ không được lưu ở bất kỳ đâu. Khi một hàm muốn một biến, nó lấy giá trị hiện tại từ Môi trường từ vựng của chính nó hoặc môi trường ngoài.

### [Các biến nào có sẵn?](#which-variables-are-available)

độ quan trọng: 5

Hàm `makeWorker` bên dưới tạo ra một hàm khác và trả về nó. Hàm mới đó có thể được gọi từ nơi khác.

Liệu nó có quyền truy cập vào các biến ngoài từ nơi nó được tạo, hay từ nơi nó được gọi, hay cả hai?

```
function makeWorker() {
  let name = "Pete";

  return function() {
    alert(name);
  };
}

let name = "John";

// tạo một hàm
let work = makeWorker();

// gọi nó
work(); // nó sẽ hiển thị gì?
```

Nó sẽ hiển thị giá trị nào? "Pete" hay "John"?

solution

Câu trả lời là: **Pete**.

Hàm `work()` trong mã dưới đây lấy `name` từ nơi khởi nguồn của nó thông qua tham chiếu môi trường từ vựng ngoài:

![](/task/closure-variable-access/lexenv-nested-work.svg)

Vì vậy, kết quả là `"Pete"` ở đây.

Nhưng nếu không có `let name` trong `makeWorker()`, thì việc tìm kiếm sẽ đi ra ngoài và lấy biến toàn cục như chúng ta có thể thấy từ chuỗi trên. Trong trường hợp đó kết quả sẽ là `"John"`.

### [Các bộ đếm có độc lập không?](#are-counters-independent)

độ quan trọng: 5

Ở đây chúng ta tạo hai bộ đếm: `counter` và `counter2` sử dụng cùng hàm `makeCounter`.

Chúng có độc lập không? Bộ đếm thứ hai sẽ hiển thị gì? `0,1` hay `2,3` hay cái gì khác?

```
function makeCounter() {
  let count = 0;

  return function() {
    return count++;
  };
}

let counter = makeCounter();
let counter2 = makeCounter();

alert( counter() ); // 0
alert( counter() ); // 1

alert( counter2() ); // ?
alert( counter2() ); // ?
```

solution

Câu trả lời: **0,1.**

Hàm `counter` và `counter2` được tạo bởi các lời gọi khác nhau của `makeCounter`.

Vì vậy, chúng có Môi trường từ vựng ngoài độc lập, mỗi cái có `count` riêng.

### [Đối tượng bộ đếm](#counter-object)

độ quan trọng: 5

Ở đây một đối tượng bộ đếm được tạo ra với sự trợ giúp của hàm khởi tạo.

Nó có hoạt động không? Nó sẽ hiển thị gì?

```
function Counter() {
  let count = 0;

  this.up = function() {
    return ++count;
  };
  this.down = function() {
    return --count;
  };
}

let counter = new Counter();

alert( counter.up() ); // ?
alert( counter.up() ); // ?
alert( counter.down() ); // ?
```

solution

Chắc chắn nó sẽ hoạt động tốt.

Cả hai hàm lồng nhau được tạo trong cùng Môi trường từ vựng ngoài, vì vậy chúng chia sẻ quyền truy cập vào cùng biến `count`:

```
function Counter() {
  let count = 0;

  this.up = function() {
    return ++count;
  };

  this.down = function() {
    return --count;
  };
}

let counter = new Counter();

alert( counter.up() ); // 1
alert( counter.up() ); // 2
alert( counter.down() ); // 1
```

### [Hàm trong if](#function-in-if)

độ quan trọng: 5

Hãy xem mã. Kết quả của lời gọi ở dòng cuối cùng là gì?

```
let phrase = "Hello";

if (true) {
  let user = "John";

  function sayHi() {
    alert(`${phrase}, ${user}`);
  }
}

sayHi();
```

solution

Kết quả là **lỗi**.

Hàm `sayHi` được khai báo bên trong `if`, vì vậy nó chỉ sống trong đó. Không có `sayHi` ở bên ngoài.

### [Phép cộng với closures](#sum-with-closures)

độ quan trọng: 4

Viết hàm `sum` hoạt động như thế này: `sum(a)(b) = a+b`.

Đúng vậy, chính xác theo cách này, sử dụng dấu ngoặc kép (không phải lỗi đánh máy).

Ví dụ:

```
sum(1)(2) = 3
sum(5)(-1) = 4
```

solution

Để dấu ngoặc kép thứ hai hoạt động, dấu ngoặc đơn thứ nhất phải trả về một hàm.

Như thế này:

```
function sum(a) {

  return function(b) {
    return a + b; // lấy "a" từ môi trường từ vựng ngoài
  };

}

alert( sum(1)(2) ); // 3
alert( sum(5)(-1) ); // 4
```

### [Biến có hiển thị không?](#is-variable-visible)

độ quan trọng: 4

Kết quả của mã này là gì?

```
let x = 1;

function func() {
  console.log(x); // ?

  let x = 2;
}

func();
```

P.S. Có một cạm bẫy trong nhiệm vụ này. Lời giải không rõ ràng.

solution

Kết quả là: **lỗi**.

Hãy thử chạy nó:

```
let x = 1;

function func() {
  console.log(x); // ReferenceError: Cannot access 'x' before initialization
  let x = 2;
}

func();
```

Trong ví dụ này chúng ta có thể quan sát sự khác biệt kỳ lạ giữa biến "không tồn tại" và biến "chưa khởi tạo".

Như bạn có thể đã đọc trong bài viết [Phạm vi biến, closure](/closure), một biến bắt đầu ở trạng thái "chưa khởi tạo" kể từ khi việc thực thi nhập vào một khối mã (hoặc một hàm). Và nó vẫn chưa khởi tạo cho đến khi câu lệnh `let` tương ứng.

Nói cách khác, về mặt kỹ thuật biến tồn tại, nhưng không thể sử dụng trước `let`.

Mã ở trên minh chứng cho điều đó.

```
function func() {
  // biến cục bộ x được engine biết từ đầu hàm,
  // nhưng "chưa khởi tạo" (không thể sử dụng) cho đến let (vùng chết)
  // do đó gây ra lỗi

  console.log(x); // ReferenceError: Cannot access 'x' before initialization

  let x = 2;
}
```

Vùng không khả dụng tạm thời này của biến (từ đầu khối mã đến `let`) đôi khi được gọi là "vùng chết" (dead zone).

### [Lọc qua hàm](#filter-through-function)

độ quan trọng: 5

Chúng ta có phương thức có sẵn `arr.filter(f)` cho mảng. Nó lọc tất cả các phần tử qua hàm `f`. Nếu nó trả về `true`, thì phần tử đó được trả về trong mảng kết quả.

Tạo một bộ "sẵn sàng sử dụng" cho các bộ lọc:

- `inBetween(a, b)` – giữa `a` và `b` hoặc bằng chúng (bao gồm cả hai đầu).
- `inArray([...])` – trong mảng đã cho.

Cách sử dụng phải như thế này:

- `arr.filter(inBetween(3,6))` – chỉ chọn các giá trị giữa 3 và 6.
- `arr.filter(inArray([1,2,3]))` – chỉ chọn các phần tử khớp với một trong các thành viên của `[1,2,3]`.

Ví dụ:

```
/* .. mã của bạn cho inBetween và inArray */
let arr = [1, 2, 3, 4, 5, 6, 7];

alert( arr.filter(inBetween(3, 6)) ); // 3,4,5,6

alert( arr.filter(inArray([1, 2, 10])) ); // 1,2
```

[Mở sandbox với các bài kiểm tra.](https://plnkr.co/edit/VjHggNnmZjJqoUyY?p=preview)

solution

Lọc inBetween

#### Lọc inBetween

```
function inBetween(a, b) {
  return function(x) {
    return x >= a && x <= b;
  };
}

let arr = [1, 2, 3, 4, 5, 6, 7];
alert( arr.filter(inBetween(3, 6)) ); // 3,4,5,6
```

Lọc inArray

#### Lọc inArray

```
function inArray(arr) {
  return function(x) {
    return arr.includes(x);
  };
}

let arr = [1, 2, 3, 4, 5, 6, 7];
alert( arr.filter(inArray([1, 2, 10])) ); // 1,2
```

[Mở lời giải với các bài kiểm tra trong sandbox.](https://plnkr.co/edit/t3Y0JoreWEhO5nED?p=preview)

### [Sắp xếp theo trường](#sort-by-field)

độ quan trọng: 5

Chúng ta có một mảng các đối tượng để sắp xếp:

```
let users = [
  { name: "John", age: 20, surname: "Johnson" },
  { name: "Pete", age: 18, surname: "Peterson" },
  { name: "Ann", age: 19, surname: "Hathaway" }
];
```

Cách thông thường để làm điều đó là:

```
// theo tên (Ann, John, Pete)
users.sort((a, b) => a.name > b.name ? 1 : -1);

// theo tuổi (Pete, Ann, John)
users.sort((a, b) => a.age > b.age ? 1 : -1);
```

Có thể làm cho nó gọn gàng hơn không, như thế này?

```
users.sort(byField('name'));
users.sort(byField('age'));
```

Vì vậy, thay vì viết một hàm, chỉ cần đặt `byField(fieldName)`.

Viết hàm `byField` có thể được sử dụng cho mục đích đó.

[Mở sandbox với các bài kiểm tra.](https://plnkr.co/edit/NVcpKrKxSrM51sLP?p=preview)

solution

```
function byField(fieldName){
  return (a, b) => a[fieldName] > b[fieldName] ? 1 : -1;
}
```

[Mở lời giải với các bài kiểm tra trong sandbox.](https://plnkr.co/edit/fM9R72meB79VtlBx?p=preview)

### [Đội quân các hàm](#army-of-functions)

độ quan trọng: 5

Mã sau tạo ra một mảng `shooters`.

Mỗi hàm được thiết kế để xuất ra số của nó. Nhưng có gì đó sai...

```
function makeArmy() {
  let shooters = [];

  let i = 0;
  while (i < 10) {
    let shooter = function() { // tạo một hàm shooter,
      alert( i ); // sẽ hiển thị số của nó
    };
    shooters.push(shooter); // và thêm nó vào mảng
    i++;
  }

  // ...và trả về mảng các shooter
  return shooters;
}

let army = makeArmy();

// tất cả shooters đều hiển thị 10 thay vì số của chúng 0, 1, 2, 3...
army[0](); // 10 từ shooter số 0
army[1](); // 10 từ shooter số 1
army[2](); // 10 ...và cứ thế.
```

Tại sao tất cả shooters đều hiển thị cùng một giá trị?

Sửa mã sao cho chúng hoạt động như dự định.

[Mở sandbox với các bài kiểm tra.](https://plnkr.co/edit/HpB8vhw3UAlD3wEI?p=preview)

solution

Hãy xem xét những gì xảy ra bên trong `makeArmy`, và lời giải sẽ trở nên rõ ràng.

1. Nó tạo một mảng rỗng `shooters`:

   ```
   let shooters = [];
   ```
2. Điền nó bằng các hàm qua `shooters.push(function)` trong vòng lặp.

   Mỗi phần tử là một hàm, vì vậy mảng kết quả trông như thế này:

   ```
   shooters = [
     function () { alert(i); },
     function () { alert(i); },
     function () { alert(i); },
     function () { alert(i); },
     function () { alert(i); },
     function () { alert(i); },
     function () { alert(i); },
     function () { alert(i); },
     function () { alert(i); },
     function () { alert(i); }
   ];
   ```
3. Mảng được trả về từ hàm.

   Sau đó, sau đó, lời gọi bất kỳ thành viên nào, ví dụ `army[5]()` sẽ lấy phần tử `army[5]` từ mảng (là một hàm) và gọi nó.

   Bây giờ tại sao tất cả các hàm như vậy lại hiển thị cùng một giá trị, `10`?

   Đó là vì không có biến cục bộ `i` bên trong các hàm `shooter`. Khi một hàm như vậy được gọi, nó lấy `i` từ môi trường từ vựng ngoài của nó.

   Sau đó, giá trị của `i` sẽ là gì?

   Nếu chúng ta nhìn vào nguồn:

   ```
   function makeArmy() {
     ...
     let i = 0;
     while (i < 10) {
       let shooter = function() { // hàm shooter
         alert( i ); // sẽ hiển thị số của nó
       };
       shooters.push(shooter); // thêm hàm vào mảng
       i++;
     }
     ...
   }
   ```

   Chúng ta có thể thấy rằng tất cả các hàm `shooter` được tạo trong môi trường từ vựng của hàm `makeArmy()`. Nhưng khi `army[5]()` được gọi, `makeArmy` đã hoàn thành công việc của nó, và giá trị cuối cùng của `i` là `10` (`while` dừng lại ở `i=10`).

   Kết quả là, tất cả các hàm `shooter` nhận cùng một giá trị từ môi trường từ vựng ngoài và đó là, giá trị cuối cùng, `i=10`.

   ![](/task/make-army/lexenv-makearmy-empty.svg)

   Như bạn có thể thấy ở trên, trên mỗi lần lặp của khối `while {...}`, một môi trường từ vựng mới được tạo. Vì vậy, để sửa lỗi này, chúng ta có thể sao chép giá trị của `i` vào một biến trong khối `while {...}`, như thế này:

   ```
   function makeArmy() {
     let shooters = [];

     let i = 0;
     while (i < 10) {
         let j = i;
         let shooter = function() { // hàm shooter
           alert( j ); // sẽ hiển thị số của nó
         };
       shooters.push(shooter);
       i++;
     }

     return shooters;
   }

   let army = makeArmy();

   // Bây giờ mã hoạt động đúng
   army[0](); // 0
   army[5](); // 5
   ```

   Ở đây `let j = i` khai báo biến `j` "theo lần lặp" và sao chép `i` vào nó. Các kiểu nguyên thủy được sao chép "bằng giá trị", vì vậy chúng ta thực sự nhận được một bản sao độc lập của `i`, thuộc về lần lặp vòng lặp hiện tại.

   Các shooter hoạt động đúng, vì giá trị của `i` bây giờ sống gần hơn một chút. Không trong Môi trường từ vựng `makeArmy()`, mà trong Môi trường từ vựng tương ứng với lần lặp vòng lặp hiện tại:

   ![](/task/make-army/lexenv-makearmy-while-fixed.svg)

   Vấn đề tương tự cũng có thể được tránh nếu chúng ta sử dụng `for` ngay từ đầu, như thế này:

   ```
   function makeArmy() {

     let shooters = [];

     for(let i = 0; i < 10; i++) {
       let shooter = function() { // hàm shooter
         alert( i ); // sẽ hiển thị số của nó
       };
       shooters.push(shooter);
     }

     return shooters;
   }

   let army = makeArmy();

   army[0](); // 0
   army[5](); // 5
   ```

   Về cơ bản điều đó giống nhau, vì `for` trên mỗi lần lặp tạo ra một môi trường từ vựng mới, với biến `i` riêng. Vì vậy `shooter` được tạo trong mỗi lần lặp tham chiếu đến `i` riêng của nó, từ chính lần lặp đó.

   ![](/task/make-army/lexenv-makearmy-for-fixed.svg)

Bây giờ, vì bạn đã bỏ nhiều nỗ lực đọc điều này, và công thức cuối cùng đơn giản chỉ – chỉ cần sử dụng `for`, bạn có thể tự hỏi – liệu có đáng không?

Chà, nếu bạn có thể dễ dàng trả lời câu hỏi, bạn đã không đọc lời giải. Vì vậy, hy vọng nhiệm vụ này đã giúp bạn hiểu rõ hơn một chút.

Bên cạnh đó, có những trường hợp người ta thích `while` hơn `for`, và các kịch bản khác, nơi những vấn đề như vậy là có thật.

[Mở lời giải với các bài kiểm tra trong sandbox.](https://plnkr.co/edit/71PUiPA2uT028lWJ?p=preview)
