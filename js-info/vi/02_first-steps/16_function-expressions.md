# Function expressions

> Nguồn: [https://javascript.info/function-expressions](https://javascript.info/function-expressions)

<!-- fetched: 2026-09-14 -->

Trong JavaScript, một hàm không phải là "cấu trúc ngôn ngữ kỳ diệu", mà là một loại giá trị đặc biệt.

Cú pháp mà chúng ta đã sử dụng trước đó được gọi là *Function Declaration*:

```
function sayHi() {
  alert( "Xin chào" );
}
```

Có một cú pháp khác để tạo một hàm được gọi là *Function Expression*.

Nó cho phép chúng ta tạo một hàm mới ở giữa bất kỳ biểu thức nào.

Vígiụ:

```
let sayHi = function() {
  alert( "Xin chào" );
};
```

Ở đây chúng ta có thể thấy một biến `sayHi` nhận một giá trị, hàm mới, được tạo là `function() { alert("Xin chào"); }`.

Vì việc tạo hàm xảy ra trong ngữ cảnh của biểu thức gán (ở phía bên phải của `=`), đây là một *Function Expression*.

Xin lưu ý, không có tên sau từ khóa `function`. Bỏ qua tên là được phép cho Function Expressions.

Ở đây chúng ta ngay lập tức gán nó vào biến, vì vậy ý nghĩa của hai mẫu mã này là giống nhau: "tạo một hàm và đặt nó vào biến `sayHi`".

Trong các tình huống nâng cao hơn, những tình huống mà chúng ta sẽ gặp sau này, một hàm có thể được tạo và ngay lập tức được gọi hoặc lên lịch cho thực thi sau này, không được lưu trữ ở đâu, do đó vẫn không có tên.

## [Hàm là một giá trị](#function-is-a-value)

Hãy lặp lại: bất kể hàm được tạo như thế nào, một hàm là một giá trị. Cả hai ví dụ trên đều lưu trữ một hàm trong biến `sayHi`.

Chúng ta thậm chí có thể in ra giá trị đó bằng `alert`:

```
function sayHi() {
  alert( "Xin chào" );
}

alert( sayHi ); // hiển thị mã hàm
```

Xin lưu ý rằng dòng cuối cùng không chạy hàm, vì không có dấu ngoặc đơn sau `sayHi`. Có những ngôn ngữ lập trình mà bất kỳ đề cập nào đến tên hàm đều gây ra việc thực thi của nó, nhưng JavaScript không phải như vậy.

Trong JavaScript, một hàm là một giá trị, vì vậy chúng ta có thể đối xử với nó như một giá trị. Mã ở trên hiển thị biểu diễn chuỗi của nó, là mã nguồn.

Chắc chắn, một hàm là một giá trị đặc biệt, theo nghĩa là chúng ta có thể gọi nó như `sayHi()`.

Nhưng nó vẫn là một giá trị. Vì vậy, chúng ta có thể làm việc với nó như với các loại giá trị khác.

Chúng ta có thể sao chép một hàm vào một biến khác:

```
function sayHi() {   // (1) create
  alert( "Xin chào" );
}

let func = sayHi;    // (2) copy

func(); // Xin chào     // (3) chạy bản sao (nó hoạt động)!
sayHi(); // Xin chào    //     cái này vẫn hoạt động (tại sao không)
```

Đây là những gì xảy ra ở trên chi tiết:

1. Function Declaration `(1)` tạo hàm và đặt nó vào biến có tên `sayHi`.
2. Dòng `(2)` sao chép nó vào biến `func`. Xin lưu ý lần nữa: không có dấu ngoặc đơn sau `sayHi`. Nếu có, thì `func = sayHi()` sẽ viết *kết quả của lệnh gọi* `sayHi()` vào `func`, chứ không phải *hàm* `sayHi`bản thân.
3. Bây giờ hàm có thể được gọi là cả `sayHi()` và `func()`.

Chúng ta cũng có thể sử dụng một Function Expression để khai báo `sayHi`, ở dòng đầu tiên:

```
let sayHi = function() { // (1) create
  alert( "Xin chào" );
};

let func = sayHi;  //(2)
// ...
```

Mọi thứ sẽ hoạt động giống nhau.

Tại sao có dấu chấm phẩy ở cuối?

Bạn có thể tự hỏi, tại sao Function Expressions có dấu chấm phẩy `;` ở cuối, nhưng Function Declarations thì không:

```
function sayHi() {
  // ...
}

let sayHi = function() {
  // ...
};
```

Câu trả lời đơn giản: một Function Expression được tạo ở đây là `function(…) {…}` bên trong câu lệnh gán: `let sayHi = …;`. Dấu chấm phẩy `;` được khuyến nghị ở cuối câu lệnh, nó không phải là một phần của cú pháp hàm.

Dấu chấm phẩy sẽ có mặt cho một phép gán đơn giản hơn, chẳng hạn như `let sayHi = 5;`, và nó cũng có mặt cho một phép gán hàm.

## [Callback functions](#callback-functions)

Hãy xem thêm các ví dụ về truyền hàm như giá trị và sử dụng function expressions.

Chúng ta sẽ viết một hàm `ask(question, yes, no)` với ba tham số:

`question`
:   Văn bản của câu hỏi

`yes`
:   Hàm để chạy nếu câu trả lời là "Có"

`no`
:   Hàm để chạy nếu câu trả lời là "Không"

Hàm nên hỏi `question` và, tùy thuộc vào câu trả lời của người dùng, gọi `yes()` hoặc `no()`:

```
function ask(question, yes, no) {
  if (confirm(question)) yes()
  else no();
}

function showOk() {
  alert( "Bạn đã đồng ý." );
}

function showCancel() {
  alert( "Bạn đã hủy việc thực thi." );
}

// usage: functions showOk, showCancel được truyền như là arguments cho ask
ask("Bạn có đồng ý?", showOk, showCancel);
```

Trong thực tế, các hàm như vậy khá hữu ích. Sự khác biệt chính giữa `ask` thực tế và ví dụ trên là các hàm thực tế sử dụng các cách phức tạp hơn để tương tác với người dùng hơn là `confirm` đơn giản. Trong trình duyệt, các hàm như vậy thường vẽ một cửa sổ câu hỏi đẹp mắt. Nhưng đó là một câu chuyện khác.

**Các đối số `showOk` và `showCancel` của `ask` được gọi là *callback functions* hay còn gọi là *callbacks*.**

Ý tưởng là chúng ta truyền một hàm và mong đợi nó sẽ được "gọi lại" sau này nếu cần. Trong trường hợp của chúng ta, `showOk` trở thành callback cho câu trả lời "có", và `showCancel` cho câu trả lời "không".

Chúng ta có thể sử dụng Function Expressions để viết một hàm tương đương, ngắn gọn hơn:

```
function ask(question, yes, no) {
  if (confirm(question)) yes()
  else no();
}

ask(
  "Bạn có đồng ý?",
  function() { alert("Bạn đã đồng ý."); },
  function() { alert("Bạn đã hủy việc thực thi."); }
);
```

Ở đây, các hàm được khai báo ngay bên trong lệnh gọi `ask(...)`. Chúng không có tên, và vì vậy được gọi là *anonymous*. Các hàm này không thể truy cập được bên ngoài `ask` (vì chúng không được gán cho các biến), nhưng đó là những gì chúng ta muốn ở đây.

Mã như vậy xuất hiện rất tự nhiên trong scripts của chúng ta, nó phù hợp với tinh thần của JavaScript.

Một hàm là một giá trị đại diện cho một "hành động"

Các giá trị thông thường như chuỗi hoặc số đại diện cho *dữ liệu*.

Một hàm có thể được cảm nhận như một *hành động*.

Chúng ta có thể truyền nó giữa các biến và chạy khi chúng ta muốn.

## [Function Expression vs Function Declaration](#function-expression-vs-function-declaration)

Hãy hình thành sự khác biệt chính giữa Function Declarations và Expressions.

Trước tiên, cú pháp: cách phân biệt giữa chúng trong mã.

- *Function Declaration:* một hàm, được khai báo như một câu lệnh riêng biệt, trong luồng mã chính:

  ```
  // Function Declaration
  function sum(a, b) {
    return a + b;
  }
  ```
- *Function Expression:* một hàm, được tạo bên trong một biểu thức hoặc bên trong một cấu trúc cú pháp khác. Ở đây, hàm được tạo ở phía bên phải của "biểu thức gán" `=`:

  ```
  // Function Expression
  let sum = function(a, b) {
    return a + b;
  };
  ```

Sự khác biệt tinh tế hơn là *khi* một hàm được tạo bởi động cơ JavaScript.

**Một Function Expression được tạo khi việc thực thi đạt đến nó và chỉ có thể sử dụng được từ thời điểm đó.**

Một khi luồng thực thi chuyển sang phía bên phải của phép gán `let sum = function…` – ở đây chúng ta đi, hàm được tạo và có thể được sử dụng (gán, gọi, v.v. ) từ bây giờ.

Function Declarations thì khác.

**Một Function Declaration có thể được gọi trước khi nó được định nghĩa.**

Vígiụ, một Function Declaration toàn cục hiển thị trong toàn bộ script, bất kể nó ở đâu.

Điều đó là do các thuật toán nội bộ. Khi JavaScript chuẩn bị chạy script, nó trước tiên tìm kiếm các Function Declarations toàn cục trong đó và tạo các hàm. Chúng ta có thể nghĩ về nó như một "giai đoạn khởi tạo".

Và sau khi tất cả Function Declarations được xử lý, mã được thực thi. Vì vậy, nó có quyền truy cập vào các hàm này.

Vígiụ, điều này hoạt động:

```
sayHi("John"); // Xin chào, John

function sayHi(name) {
  alert( `Xin chào, ${name}` );
}
```

Function Declaration `sayHi` được tạo khi JavaScript đang chuẩn bị bắt đầu script và hiển thị ở mọi nơi trong đó.

…Nếu đó là một Function Expression, thì nó sẽ không hoạt động:

```
sayHi("John"); // lỗi!

let sayHi = function(name) {  // (*) không còn ma thuật nữa
  alert( `Xin chào, ${name}` );
};
```

Function Expressions được tạo khi việc thực thi đạt đến chúng. Điều đó sẽ chỉ xảy ra ở dòng `(*)`. Quá muộn.

Một tính năng đặc biệt khác của Function Declarations là block scope của chúng.

**Trong chế độ strict, khi một Function Declaration nằm trong một code block, nó hiển thị ở mọi nơi bên trong block đó. Nhưng không phải bên ngoài nó.**

Vígiụ, hãy tưởng tượng chúng ta cần khai báo một hàm `welcome()` tùy thuộc vào biến `age` mà chúng ta nhận được trong thời gian chạy. Và sau đó chúng ta dự định sử dụng nó một thời gian sau.

Nếu chúng ta sử dụng Function Declaration, nó sẽ không hoạt động như dự định:

```
let age = prompt("Bạn bao nhiêu tuổi?", 18);

// điều kiện khai báo một hàm
if (age < 18) {

  function welcome() {
    alert("Xin chào!");
  }

} else {

  function welcome() {
    alert("Trân trọng!");
  }

}

// ...sử dụng nó sau
welcome(); // Lỗi: welcome không được định nghĩa
```

Điều đó là vì một Function Declaration chỉ hiển thị bên trong code block mà nó cư trú.

Đây là một ví dụ khác:

```
let age = 16; // lấy 16 như một ví dụ

if (age < 18) {
  welcome();               // \   (chạy)
                           //  |
  function welcome() {     //  |
    alert("Xin chào!");       //  |  Function Declaration có sẵn
  }                        //  |  ở mọi nơi trong block nơi nó được khai báo
                           //  |
  welcome();               // /   (chạy)

} else {

  function welcome() {
    alert("Trân trọng!");
  }
}

// Ở đây chúng ta ra ngoài dấu ngoặc nhọn,
// vì vậy chúng ta không thể nhìn thấy Function Declarations được tạo bên trong chúng.

welcome(); // Lỗi: welcome không được định nghĩa
```

Chúng ta có thể làm gì để làm cho `welcome` hiển thị bên ngoài `if`?

Cách tiếp cận đúng sẽ là sử dụng một Function Expression và gán `welcome` cho biến được khai báo bên ngoài `if` và có visibility thích hợp.

Mã này hoạt động như dự định:

```
let age = prompt("Bạn bao nhiêu tuổi?", 18);

let welcome;

if (age < 18) {

  welcome = function() {
    alert("Xin chào!");
  };

} else {

  welcome = function() {
    alert("Trân trọng!");
  };

}

welcome(); // ok bây giờ
```

Hoặc chúng ta có thể đơn giản hóa nó hơn nữa bằng cách sử dụng toán tử dấu chấm hỏi `?`:

```
let age = prompt("Bạn bao nhiêu tuổi?", 18);

let welcome = (age < 18) ?
  function() { alert("Xin chào!"); } :
  function() { alert("Trân trọng!"); };

welcome(); // ok bây giờ
```

Khi nào chọn Function Declaration versus Function Expression?

Như một quy tắc chung, khi chúng ta cần khai báo một hàm, điều đầu tiên cần xem xét là cú pháp Function Declaration. Nó mang lại nhiều tự do hơn trong cách tổ chức mã của chúng ta, vì chúng ta có thể gọi các hàm như vậy trước khi chúng được khai báo.

Điều đó cũng tốt hơn cho khả năng đọc, vì dễ dàng tìm kiếm `function f(…) {…}` trong mã hơn là `let f = function(…) {…};`. Function Declarations "bắt mắt" hơn.

…Nhưng nếu một Function Declaration không phù hợp với chúng ta vì lý do nào đó, hoặc chúng ta cần một khai báo điều kiện (chúng ta vừa thấy một ví dụ), thì nên sử dụng Function Expression.

## [Tổng kết](#summary)

- Các hàm là các giá trị. Chúng có thể được gán, sao chép hoặc khai báo ở bất kỳ nơi nào trong mã.
- Nếu hàm được khai báo như một câu lệnh riêng biệt trong luồng mã chính, đó được gọi là "Function Declaration".
- Nếu hàm được tạo như một phần của một biểu thức, nó được gọi là "Function Expression".
- Function Declarations được xử lý trước khi code block được thực thi. Chúng hiển thị ở mọi nơi trong block.
- Function Expressions được tạo khi luồng thực thi đạt đến chúng.

Hầu hết các trường hợp khi chúng ta cần khai báo một hàm, một Function Declaration là ưu tiên hơn, vì nó hiển thị trước bản thân khai báo. Điều đó mang lại cho chúng ta nhiều linh hoạt hơn trong tổ chức mã, và thường dễ đọc hơn.

Vì vậy, chúng ta nên sử dụng một Function Expression chỉ khi một Function Declaration không phù hợp với nhiệm vụ. Chúng ta đã thấy một vài ví dụ về điều đó trong chương này, và sẽ thấy nhiều hơn trong tương lai.
