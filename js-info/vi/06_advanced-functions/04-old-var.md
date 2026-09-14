# "var" cũ

> Nguồn: [https://javascript.info/var](https://javascript.info/var)

<!-- fetched: 2026-09-14 -->

Bài viết này giúp hiểu các script cũ

Thông tin trong bài viết này hữu ích để hiểu các script cũ.

Đó không phải là cách chúng ta viết code mới.

Trong chương đầu tiên về [biến](/variables), chúng ta đã đề cập đến ba cách khai báo biến:

1. `let`
2. `const`
3. `var`

Cú pháp khai báo `var` tương tự như `let`. Phần lớn thời gian, chúng ta có thể thay `let` bằng `var` hoặc ngược lại và mong đợi mọi thứ hoạt động:

```
var message = "Hi";
alert(message); // Hi
```

Nhưng bên trong, `var` là một kiểu hoàn toàn khác, bắt nguồn từ những ngày rất cũ. Nó thường không được sử dụng trong script hiện đại, nhưng vẫn ẩn náu trong các script cũ.

Nếu bạn không có kế hoạch gặp các script như vậy, bạn thậm chí có thể bỏ qua chương này hoặc tạm hoãn nó.

Mặt khác, điều quan trọng là phải hiểu sự khác biệt khi di chuyển script cũ từ `var` sang `let`, để tránh các lỗi kỳ lạ.

## ["var" không có phạm vi khối](#var-has-no-block-scope)

Các biến được khai báo với `var` có phạm vi theo hàm hoặc toàn cục. Chúng xuất hiện qua các khối.

Ví dụ:

```
if (true) {
  var test = true; // dùng "var" thay vì "let"
}

alert(test); // true, biến vẫn tồn tại sau if
```

Vì `var` bỏ qua các khối mã, chúng ta có được một biến toàn cục `test`.

Nếu chúng ta dùng `let test` thay vì `var test`, thì biến chỉ hiển thị bên trong `if`:

```
if (true) {
  let test = true; // dùng "let"
}

alert(test); // ReferenceError: test is not defined
```

Cũng tương tự với các vòng lặp: `var` không thể là biến cục bộ theo khối hoặc vòng lặp:

```
for (var i = 0; i < 10; i++) {
  var one = 1;
  // ...
}

alert(i);   // 10, "i" hiển thị sau vòng lặp, nó là biến toàn cục
alert(one); // 1, "one" hiển thị sau vòng lặp, nó là biến toàn cục
```

Nếu một khối mã nằm trong một hàm, thì `var` trở thành biến cấp hàm:

```
function sayHi() {
  if (true) {
    var phrase = "Hello";
  }

  alert(phrase); // hoạt động
}

sayHi();
alert(phrase); // ReferenceError: phrase is not defined
```

Như chúng ta có thể thấy, `var` xuyên qua `if`, `for` hoặc các khối mã khác. Đó là vì từ rất lâu trong JavaScript, các khối không có Lexical Environments, và `var` là di tích của thời đó.

## ["var" dung nạp việc khai báo lại](#var-tolerates-redeclarations)

Nếu chúng ta khai báo cùng một biến với `let` hai lần trong cùng một phạm vi, đó là lỗi:

```
let user;
let user; // SyntaxError: 'user' has already been declared
```

Với `var`, chúng ta có thể khai báo lại biến bao nhiêu lần cũng được. Nếu chúng ta dùng `var` với biến đã được khai báo, nó sẽ bị bỏ qua:

```
var user = "Pete";

var user = "John"; // "var" này không làm gì (đã được khai báo)
// ...không gây lỗi

alert(user); // John
```

## [Biến "var" có thể được khai báo sau khi sử dụng](#var-variables-can-be-declared-below-their-use)

Các khai báo `var` được xử lý khi hàm bắt đầu (hoặc script bắt đầu đối với biến toàn cục).

Nói cách khác, các biến `var` được định nghĩa từ đầu hàm, bất kể vị trí của định nghĩa (giả sử định nghĩa không nằm trong hàm lồng nhau).

Vì vậy, mã này:

```
function sayHi() {
  phrase = "Hello";

  alert(phrase);

  var phrase;
}
sayHi();
```

…Về mặt kỹ thuật giống hệt (di chuyển `var phrase` lên trên):

```
function sayHi() {
  var phrase;

  phrase = "Hello";

  alert(phrase);
}
sayHi();
```

…Hoặc thậm chí như thế này (nhớ rằng, các khối mã bị bỏ qua):

```
function sayHi() {
  phrase = "Hello"; // (*)

  if (false) {
    var phrase;
  }

  alert(phrase);
}
sayHi();
```

Mọi người cũng gọi hành vi như vậy là "hoisting" (nâng lên), vì tất cả `var` đều được "hoist" (nâng) lên đầu hàm.

Vì vậy, trong ví dụ trên, nhánh `if (false)` không bao giờ thực thi, nhưng điều đó không quan trọng. `var` bên trong nó được xử lý ở đầu hàm, nên tại thời điểm `(*)` biến đã tồn tại.

**Các khai báo được hoist, nhưng các phép gán thì không.**

Điều này được chứng minh rõ nhất qua ví dụ:

```
function sayHi() {
  alert(phrase);

  var phrase = "Hello";
}

sayHi();
```

Dòng `var phrase = "Hello"` có hai hành động:

1. Khai báo biến `var`
2. Gán biến `=`.

Khai báo được xử lý ở đầu hàm ("hoisted"), nhưng phép gán luôn hoạt động tại vị trí nó xuất hiện. Vì vậy, mã hoạt động về cơ bản như sau:

```
function sayHi() {
  var phrase; // khai báo hoạt động từ đầu...

  alert(phrase); // undefined

  phrase = "Hello"; // ...phép gán - khi thực thi đến đó.
}

sayHi();
```

Vì tất cả các khai báo `var` được xử lý ở đầu hàm, chúng ta có thể tham chiếu chúng ở bất kỳ vị trí nào. Nhưng các biến sẽ là `undefined` cho đến khi có phép gán.

Trong cả hai ví dụ trên, `alert` chạy mà không có lỗi, vì biến `phrase` tồn tại. Nhưng giá trị của nó chưa được gán, nên nó hiển thị `undefined`.

## [IIFE](#iife)

Trong quá khứ, vì chỉ có `var` và nó không có phạm vi cấp khối, lập trình viên đã tìm ra một cách để mô phỏng nó. Những gì họ làm được gọi là "immediately-invoked function expressions" (viết tắt là IIFE).

Đây không phải là thứ chúng ta nên dùng nowadays, nhưng bạn có thể tìm thấy chúng trong các script cũ.

Một IIFE trông như thế này:

```
(function() {

  var message = "Hello";

  alert(message); // Hello

})();
```

Ở đây, một Function Expression được tạo ra và gọi ngay lập tức. Vì vậy, mã thực thi ngay lập tức và có các biến riêng tư của nó.

Function Expression được bao bọc trong dấu ngoặc đơn `(function {...})`, vì khi engine JavaScript gặp `"function"` trong mã chính, nó hiểu đó là bắt đầu của một Function Declaration. Nhưng một Function Declaration phải có tên, vì vậy loại mã này sẽ gây lỗi:

```
// Cố gắng khai báo và gọi ngay một hàm
function() { // <-- SyntaxError: Function statements require a function name

  var message = "Hello";

  alert(message); // Hello

}();
```

Ngay cả khi chúng ta nói: "được rồi, hãy thêm tên", điều đó cũng không hoạt động, vì JavaScript không cho phép gọi Function Declaration ngay lập tức:

```
// lỗi cú pháp vì dấu ngoặc đơn phía dưới
function go() {

}(); // <-- không thể gọi Function Declaration ngay lập tức
```

Vì vậy, dấu ngoặc đơn xung quanh hàm là một mẹo để cho JavaScript biết rằng hàm được tạo trong ngữ cảnh của một biểu thức khác, và do đó đó là một Function Expression: nó không cần tên và có thể được gọi ngay lập tức.

Có các cách khác ngoài dấu ngoặc đơn để cho JavaScript biết rằng chúng ta đang nói đến một Function Expression:

```
// Các cách tạo IIFE

(function() {
  alert("Dấu ngoặc đơn xung quanh hàm");
})();

(function() {
  alert("Dấu ngoặc đơn xung quanh toàn bộ");
}());

!function() {
  alert("Toán tử NOT bit bắt đầu biểu thức");
}();

+function() {
  alert("Toán tử unary plus bắt đầu biểu thức");
}();
```

Trong tất cả các trường hợp trên, chúng ta khai báo một Function Expression và chạy nó ngay lập tức. Một lần nữa lưu ý: nowadays không có lý do gì để viết mã như vậy.

## [Tóm tắt](#summary)

Có hai khác biệt chính của `var` so với `let/const`:

1. Biến `var` không có phạm vi khối, tầm nhìn của chúng được giới hạn trong hàm hiện tại, hoặc toàn cục nếu được khai báo bên ngoài hàm.
2. Các khai báo `var` được xử lý ở đầu hàm (đầu script đối với biến toàn cục).

Có một khác biệt rất nhỏ nữa liên quan đến đối tượng toàn cục, mà chúng ta sẽ.cover ở chương tới.

Những khác biệt này khiến `var` kém hơn `let` phần lớn thời gian. Biến cấp khối là một điều tuyệt vời. Đó là lý do `let` đã được đưa vào tiêu chuẩn từ lâu, và hiện là cách chính (cùng với `const`) để khai báo một biến.
