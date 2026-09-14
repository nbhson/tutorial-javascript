# Biến

> Nguồn: [https://javascript.info/variables](https://javascript.info/variables)

<!-- fetched: 2026-09-14 -->

Hầu hết thời gian, một ứng dụng JavaScript cần làm việc với thông tin. Đây là hai ví dụ:

1. Một cửa hàng trực tuyến – thông tin có thể bao gồm hàng hóa đang được bán và một giỏ hàng.
2. Một ứng dụng chat – thông tin có thể bao gồm người dùng, tin nhắn, và nhiều hơn nữa.

Biến được sử dụng để lưu trữ thông tin này.

## [Một biến](#a-variable)

Một [biến](https://en.wikipedia.org/wiki/Variable_(computer_science)) là một “bộ nhớ được đặt tên” cho dữ liệu. Chúng ta có thể sử dụng biến để lưu trữ data, visitor và data khác.

Để tạo một biến trong JavaScript, sử dụng từ khóa `let`.

Câu lệnh dưới đây tạo ra (nói cách khác: *khai báo*) một biến với tên “message”:

```
let message;
```

Bây giờ, chúng ta có thể đặt một số data vào nó bằng cách sử dụng toán tử gán `=`:

```
let message;

message = 'Hello'; // lưu trữ chuỗi 'Hello' trong biến có tên message
```

Chuỗi giờ được lưu vào vùng nhớ liên kết với biến. Chúng ta có thể truy cập nó bằng cách sử dụng tên biến:

```
let message;
message = 'Hello!';

alert(message); // hiển thị nội dung biến
```

Để ngắn gọn, chúng ta có thể kết hợp khai báo biến và gán vào một dòng đơn:

```
let message = 'Hello!'; // định nghĩa biến và gán giá trị

alert(message); // Hello!
```

Chúng ta cũng có thể khai báo nhiều biến trong một dòng:

```
let user = 'John', age = 25, message = 'Hello';
```

Điều đó có vẻ ngắn hơn, nhưng chúng ta không khuyến nghị điều đó. Để có khả năng đọc tốt hơn, xin hãy sử dụng một dòng cho mỗi biến.

Biến nhiều dòng dài hơn một chút, nhưng dễ đọc hơn:

```
let user = 'John';
let age = 25;
let message = 'Hello';
```

Một số người cũng định nghĩa nhiều biến theo kiểu nhiều dòng này:

```
let user = 'John',
  age = 25,
  message = 'Hello';
```

…Hoặc thậm chí theo kiểu “comma-first”:

```
let user = 'John'
  , age = 25
  , message = 'Hello';
```

Về mặt kỹ thuật, tất cả các biến thể này làm cùng một điều. Vì vậy, đó là vấn đề của sở thích cá nhân và thẩm mỹ.

`var` thay vì `let`

Trong các script cũ, bạn cũng có thể tìm thấy một từ khóa khác: `var` thay vì `let`:

```
var message = 'Hello';
```

Từ khóa `var` *gần như* giống như `let`. Nó cũng khai báo một biến nhưng theo một cách hơi khác, “cổ điển”.

Có những sự khác biệt tinh tế giữa `let` và `var`, nhưng chúng không quan trọng đối với chúng ta lúc này. Chúng ta sẽ đề cập chi tiết trong chương [Cũ "var"](/var).

## [Một phép tương tự thực tế](#a-real-life-analogy)

Chúng ta có thể dễ dàng hiểu khái niệm về một “biến” nếu chúng ta tưởng tượng nó là một “hộp” cho dữ liệu, với một nhãn dán có tên duy nhất trên đó.

Ví dụ, biến `message` có thể được tưởng tượng như một hộp được gắn nhãn `"message"` với giá trị `"Hello!"` bên trong:

![](/article/variables/variable.svg)

Chúng ta có thể đặt bất kỳ giá trị nào vào hộp.

Chúng ta cũng có thể thay đổi nó bao nhiêu lần tùy thích:

```
let message;

message = 'Hello!';

message = 'World!'; // giá trị thay đổi

alert(message);
```

Khi giá trị thay đổi, dữ liệu cũ bị xóa khỏi biến:

![](/article/variables/variable-change.svg)

Chúng ta cũng có thể khai báo hai biến và sao chép dữ liệu từ biến này sang biến khác.

```
let hello = 'Hello world!';

let message;

// sao chép 'Hello world' từ hello vào message
message = hello;

// giờ hai biến giữ cùng data
alert(hello); // Hello world!
alert(message); // Hello world!
```

Khai báo hai lần gây lỗi

Một biến chỉ nên được khai báo một lần.

Việc khai báo lại cùng một biến là một lỗi:

```
let message = "This";

// 'let' lặp lại dẫn đến lỗi
let message = "That"; // SyntaxError: 'message' đã được khai báo
```

Vì vậy, chúng ta nên khai báo một biến một lần và sau đó tham chiếu nó mà không có `let`.

Ngôn ngữ hàm

Thú vị là có những ngôn ngữ được gọi là [thuần hàm](https://en.wikipedia.org/wiki/Purely_functional_programming) như [Haskell](https://en.wikipedia.org/wiki/Haskell), cấm thay đổi giá trị biến.

Trong các ngôn ngữ như vậy, một khi giá trị được lưu “trong hộp”, nó ở đó mãi mãi. Nếu chúng ta cần lưu trữ cái gì đó khác, ngôn ngữ bắt chúng ta tạo một hộp mới (khai báo một biến mới). Chúng ta không thể tái sử dụng cái cũ.

Mặc dù có vẻ hơi kỳ lạ ở cái nhìn đầu tiên, các ngôn ngữ này khá có khả năng phát triển nghiêm túc. Hơn nữa, có những lĩnh vực như tính toán song song nơi hạn chế này mang lại lợi ích nhất định.

## [Đặt tên biến](#variable-naming)

Có hai hạn chế về tên biến trong JavaScript:

1. Tên phải chứa chỉ chữ cái, chữ số, hoặc các ký hiệu `$` và `_`.
2. Ký tự đầu tiên không được là chữ số.

Ví dụ về tên hợp lệ:

```
let userName;
let test123;
```

Khi tên chứa nhiều từ, [camelCase](https://en.wikipedia.org/wiki/CamelCase) được sử dụng phổ biến. Đó là: các từ đi sau nhau, với mỗi từ trừ từ đầu bắt đầu bằng chữ hoa: `myVeryLongName`.

Điều thú vị – ký hiệu dollar `'$'` và underscore `'_'` cũng có thể được sử dụng trong tên. Chúng là các ký tự thông thường, giống như chữ cái, không có ý nghĩa đặc biệt.

Các tên này hợp lệ:

```
let $ = 1; // khai báo một biến với tên "$"
let _ = 2; // và giờ một biến với tên "_"

alert($ + _); // 3
```

Ví dụ về tên biến không đúng:

```
let 1a; // không thể bắt đầu bằng chữ số

let my-name; // dấu gạch ngang '-' không được phép trong tên
```

Phân biệt chữ hoa/thường

Các biến tên `apple` và `APPLE` là hai biến khác nhau.

Các ký tự không Latin được phép, nhưng không nên dùng

Có thể sử dụng bất kỳ ngôn ngữ nào, bao gồm chữ cái Cyrillic, chữ Hán và vân vân, như thế này:

```
let имя = '...';
let 我 = '...';
```

Về mặt kỹ thuật, không có lỗi ở đây. Các tên như vậy được phép, nhưng có một quy ước quốc tế là sử dụng tiếng Anh trong tên biến. Ngay cả khi chúng ta đang viết một script nhỏ, nó có thể có một cuộc sống dài trước mắt. Người từ các quốc gia khác có thể cần đọc nó vào một lúc nào đó.

Tên dành riêng

Có một [danh sách các từ dành riêng](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Lexical_grammar#Keywords), không thể được sử dụng làm tên biến vì chúng được sử dụng bởi chính ngôn ngữ.

Ví dụ: `let`, `class`, `return`, và `function` là reserved.

Mã dưới đây cho lỗi cú pháp:

```
let let = 5; // không thể đặt tên biến là "let", lỗi!
let return = 5; // cũng không thể đặt tên là "return", lỗi!
```

Một phép gán mà không có `use strict`

Thông thường, chúng ta cần định nghĩa một biến trước khi sử dụng nó. Nhưng trong thời kỳ cũ, về mặt kỹ thuật có thể tạo một biến bằng cách gán giá trị mà không cần dùng `let`. Điều này vẫn hoạt động ngày nay nếu chúng ta không đặt `use strict` trong scripts của mình để duy trì tương thích với scripts cũ.

```
// lưu ý: không có "use strict" trong ví dụ này

num = 5; // biến "num" được tạo nếu nó chưa tồn tại

alert(num); // 5
```

Đây là một practice xấu và sẽ gây lỗi trong chế độ strict:

```
"use strict";

num = 5; // lỗi: num không được định nghĩa
```

## [Hằng số](#constants)

Để khai báo một biến hằng số (không đổi), sử dụng `const` thay vì `let`:

```
const myBirthday = '18.04.1982';
```

Các biến được khai báo bằng `const` được gọi là “constants”. Chúng không thể được gán lại. Một nỗ lực làm như vậy sẽ gây lỗi:

```
const myBirthday = '18.04.1982';

myBirthday = '01.01.2001'; // lỗi, không thể gán lại constant!
```

Khi lập trình viên chắc chắn rằng một biến sẽ không bao giờ thay đổi, họ có thể khai báo nó bằng `const` để đảm bảo và truyền đạt điều đó với mọi người.

### [Constants viết hoa](#uppercase-constants)

Có một practice phổ biến để sử dụng constants làm alias cho các giá trị khó nhớ được biết trước khi thực thi.

Các constants như vậy được đặt tên bằng chữ cái viết hoa và underscore.

Ví dụ, hãy tạo constants cho màu sắc theo định dạng “web” (hex):

```
const COLOR_RED = "#F00";
const COLOR_GREEN = "#0F0";
const COLOR_BLUE = "#00F";
const COLOR_ORANGE = "#FF7F00";

// ...khi cần chọn màu
let color = COLOR_ORANGE;
alert(color); // #FF7F00
```

Lợi ích:

- `COLOR_ORANGE` dễ nhớ hơn nhiều so với `"#FF7F00"`.
- Rất dễ đánh nhầm `"#FF7F00"` hơn là `COLOR_ORANGE`.
- Khi đọc mã, `COLOR_ORANGE` có ý nghĩa hơn nhiều so với `#FF7F00`.

Khi nào nên sử dụng chữ hoa cho một constant và khi nào nên đặt tên bình thường? Hãy làm rõ điều đó.

Việc là một “constant” chỉ có nghĩa là giá trị của biến không bao giờ thay đổi. Nhưng một số constants được biết trước khi thực thi (như giá trị hex cho màu đỏ) và một số constants được *tính toán* trong thời gian chạy, trong quá trình thực thi, nhưng không thay đổi sau khi gán lần đầu.

Ví dụ:

```
const pageLoadTime = /* thời gian trang web tải */;
```

Giá trị của `pageLoadTime` không được biết trước khi trang tải, vì vậy nó được đặt tên bình thường. Nhưng nó vẫn là một constant vì nó không thay đổi sau khi gán.

Nói cách khác, constants tên viết hoa chỉ được sử dụng như các alias cho các giá trị “hard-coded”.

## [Đặt tên đúng](#name-things-right)

Nói về biến, có một thứ cực kỳ quan trọng nữa.

Tên biến nên có ý nghĩa rõ ràng, mô tả data mà nó lưu trữ.

Đặt tên biến là một trong những kỹ năng quan trọng và phức tạp nhất trong lập trình. Một cái nhìn thoáng qua vào tên biến có thể tiết lộ mã nào được viết bởi người mới so với nhà phát triển có kinh nghiệm.

Trong một dự án thực tế, hầu hết thời gian được dành để sửa đổi và mở rộng cơ sở mã hiện có hơn là viết cái gì đó hoàn toàn mới từ đầu. Khi chúng ta quay lại một số mã sau khi làm gì đó trong một lúc, sẽ dễ dàng hơn để tìm thông tin được gắn nhãn tốt. Hay nói cách khác, khi các biến có tên tốt.

Xin hãy dành thời gian nghĩ về tên đúng cho một biến trước khi khai báo nó. Làm như vậy sẽ trả lại cho bạn rất nhiều.

Một số quy tắc nên tuân theo là:

- Sử dụng tên dễ đọc như `userName` hoặc `shoppingCart`.
- Tránh viết tắt hoặc tên ngắn như `a`, `b`, và `c`, trừ khi bạn biết mình đang làm gì.
- Làm cho tên mô tả và súc tích nhất có thể. Ví dụ về tên xấu là `data` và `value`. Những tên này không nói gì. Chỉ ổn khi sử dụng chúng nếu ngữ cảnh của mã làm cho nó đặc biệt rõ ràng biến đang tham chiếu đến data hoặc giá trị nào.
- Đồng ý về các thuật ngữ trong đội của bạn và trong tâm trí bạn. Nếu một visitor của trang web được gọi là “user” thì chúng ta nên đặt tên các biến liên quan là `currentUser` hoặc `newUser` thay vì `currentVisitor` hoặc `newManInTown`.

Nghe có vẻ đơn giản? Đúng vậy, nhưng tạo tên biến mô tả và súc tích trong thực tế không đơn giản. Hãy thử sức.

Tái sử dụng hay tạo mới?

Và lưu ý cuối cùng. Có một số lập trình viên lười biếng, thay vì khai báo biến mới, có xu hướng tái sử dụng các biến hiện có.

Kết quả là, các biến của họ giống như những hộp mà mọi người némthứ thứ vào mà không thay đổi nhãn dán của chúng. Bên trong hộp giờ là gì? Ai biết? Chúng ta cần đến gần hơn và kiểm tra.

Những lập trình viên này tiết kiệm một chút về khai báo biến nhưng mất nhiều hơn gấp mười lần khi debug.

Một biến extra là tốt, không phải xấu.

Minifiers và trình duyệt hiện đại tối ưu hóa mã đủ tốt, vì vậy nó sẽ không tạo ra vấn đề hiệu suất. Sử dụng các biến khác nhau cho các giá trị khác nhau thậm chí có thể giúp động cơ tối ưu hóa mã của bạn.

## [Tổng kết](#summary)

Chúng ta có thể khai báo biến để lưu trữ data bằng cách sử dụng các từ khóa `var`, `let`, hoặc `const`.

- `let` – là khai báo biến hiện đại.
- `var` – là khai báo biến cổ điển. Thông thường chúng ta không sử dụng nó, nhưng chúng ta sẽ đề cập đến các điểm tinh tế khác với `let` trong chương [Cũ "var"](/var), phòng trường hợp bạn cần chúng.
- `const` – giống như `let`, nhưng giá trị của biến không thể thay đổi.

Biến nên được đặt tên theo cách cho phép chúng ta dễ dàng hiểu bên trong là gì.

---

---

## Các bài tập

## [Các bài tập](#tasks)

### [Làm việc với biến](#working-with-variables)

mức độ quan trọng: 2

1. Khai báo hai biến: `admin` và `name`.
2. Gán giá trị `"John"` cho `name`.
3. Sao chép giá trị từ `name` sang `admin`.
4. Hiển thị giá trị của `admin` bằng cách sử dụng `alert` (phải xuất ra “John”).

lời giải

Trong mã dưới đây, mỗi dòng tương ứng với mục trong danh sách bài tập.

```
let admin, name; // có thể khai báo hai biến cùng lúc

name = "John";

admin = name;

alert( admin ); // "John"
```

### [Đặt tên đúng](#giving-the-right-name)

mức độ quan trọng: 3

1. Tạo một biến với tên của hành tinh chúng ta. Bạn sẽ đặt tên biến như vậy thế nào?
2. Tạo một biến để lưu trữ tên của người truy cập hiện tại của một trang web. Bạn sẽ đặt tên biến đó thế nào?

lời giải

Biến cho hành tinh của chúng ta

#### Biến cho hành tinh của chúng ta

Rất đơn giản:

```
let ourPlanetName = "Earth";
```

Lưu ý, chúng ta có thể sử dụng tên ngắn hơn `planet`, nhưng nó có thể không rõ ràng hành tinh nào mà nó đề cập đến. Tốt hơn nên diễn đạt rõ ràng. Ít nhất là cho đến khi biến quá dài.

Tên của người truy cập hiện tại

#### Tên của người truy cập hiện tại

```
let currentUserName = "John";
```

Một lần nữa, chúng ta có thể rút ngắn thành `userName` nếu chúng ta biết chắc chắn rằng người dùng là hiện tại.

Trình soạn thảo hiện đại và autocomplete làm cho các tên biến dài dễ viết. Đừng tiết kiệm chúng. Một tên có 3 từ là ổn.

Và nếu trình soạn thảo của bạn không có autocompletion đúng cách, hãy lấy [một trình mới](/code-editors).

### [Const viết hoa?](#uppercase-const)

mức độ quan trọng: 4

Hãy xem xét mã sau:

```
const birthday = '18.04.1982';

const age = someCode(birthday);
```

Ở đây chúng ta có một constant `birthday` cho ngày sinh, và cũng constant `age`.

`age` được tính toán từ `birthday` bằng cách sử dụng `someCode()`, có nghĩa là một lệnh gọi hàm mà chúng ta chưa giải thích (sớm thôi!), nhưng chi tiết không quan trọng ở đây, điểm là `age` được tính toán theo cách nào đó dựa trên `birthday`.

Có nên sử dụng chữ hoa cho `birthday` không? Cho `age` không? Hay cho cả hai?

```
const BIRTHDAY = '18.04.1982'; // viết hoa birthday?

const AGE = someCode(BIRTHDAY); // viết hoa age?
```

lời giải

Chúng ta thường sử dụng chữ hoa cho các constants “hard-coded”. Hay nói cách khác, khi giá trị được biết trước khi thực thi và được viết trực tiếp vào mã.

Trong mã này, `birthday` chính xác là như vậy. Vì vậy, chúng ta có thể sử dụng chữ hoa cho nó.

Ngược lại, `age` được đánh giá trong thời gian chạy. Hôm nay chúng ta có một age, một năm sau chúng ta sẽ có một age khác. Nó là constant theo nghĩa là nó không thay đổi trong quá trình thực thi mã. Nhưng nó “ít là constant” hơn `birthday`: nó được tính toán, vì vậy chúng ta nên giữ chữ thường cho nó.
