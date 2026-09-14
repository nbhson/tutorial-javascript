# Cú pháp "new Function"

> Nguồn: [https://javascript.info/new-function](https://javascript.info/new-function)

<!-- fetched: 2026-09-14 -->

Còn một cách nữa để tạo hàm. Cách này ít được sử dụng, nhưng đôi khi không có lựa chọn nào khác.

## [Cú pháp](#syntax)

Cú pháp tạo hàm:

```
let func = new Function ([arg1, arg2, ...argN], functionBody);
```

Hàm được tạo với các đối số `arg1...argN` và thân hàm được chỉ định `functionBody`.

Dễ hiểu hơn khi nhìn vào một ví dụ. Đây là một hàm với hai đối số:

```
let sum = new Function('a', 'b', 'return a + b');

alert( sum(1, 2) ); // 3
```

Và đây là hàm không có đối số, chỉ có thân hàm:

```
let sayHi = new Function('alert("Hello")');

sayHi(); // Hello
```

Sự khác biệt lớn nhất so với các cách khác là hàm được tạo ra từ một chuỗi ký tự, được chuyển vào thời gian chạy.

Tất cả các khai báo trước đó yêu cầu chúng ta, lập trình viên, phải viết mã hàm trong tập lệnh.

Nhưng `new Function` cho phép biến bất kỳ chuỗi nào thành hàm. Ví dụ, chúng ta có thể nhận một hàm mới từ máy chủ và sau đó thực thi nó:

```
let str = ... nhận mã từ máy chủ một cách động ...

let func = new Function(str);
func();
```

Nó được sử dụng trong rất nhiều trường hợp cụ thể, như khi chúng ta nhận mã từ máy chủ, hoặc để biên dịch động một hàm từ mẫu, trong các ứng dụng web phức tạp.

## [Closure](#closure)

Thông thường, một hàm ghi nhớ nơi nó được sinh ra trong thuộc tính đặc biệt `[[Environment]]`. Nó tham chiếu đến Lexical Environment từ nơi nó được tạo (chúng ta đã đề cập đến điều đó trong chương [Phạm vi biến, closure](/closure)).

Nhưng khi một hàm được tạo bằng `new Function`, `[[Environment]]` của nó được đặt để tham chiếu không phải Lexical Environment hiện tại, mà là toàn cục.

Vì vậy, hàm như vậy không thể truy cập các biến bên ngoài, chỉ có thể truy cập các biến toàn cục.

```
function getFunc() {
  let value = "test";

  let func = new Function('alert(value)');

  return func;
}

getFunc()(); // lỗi: value is not defined
```

So sánh với hành vi thông thường:

```
function getFunc() {
  let value = "test";

  let func = function() { alert(value); };

  return func;
}

getFunc()(); // "test", từ Lexical Environment của getFunc
```

Đặc điểm đặc biệt của `new Function` này trông có vẻ lạ, nhưng rất hữu ích trong thực tế.

Hãy tưởng tượng rằng chúng ta phải tạo một hàm từ một chuỗi. Mã của hàm đó không biết được khi viết tập lệnh (đó là lý do chúng ta không sử dụng hàm thông thường), nhưng sẽ được biết trong quá trình thực thi. Chúng ta có thể nhận được nó từ máy chủ hoặc từ nguồn khác.

Hàm mới của chúng ta cần tương tác với tập lệnh chính.

Nhưng nếu nó có thể truy cập các biến bên ngoài?

Vấn đề là trước khi JavaScript được xuất bản để sản xuất, nó được nén bằng một *minifier* – một chương trình đặc biệt giúp thu nhỏ mã bằng cách loại bỏ các chú thích thừa, khoảng trắng và – điều quan trọng, đổi tên các biến địa phương thành các tên ngắn hơn.

Ví dụ, nếu một hàm có `let userName`, minifier sẽ thay thế nó bằng `let a` (hoặc một chữ cái khác nếu chữ cái này đã được sử dụng), và làm điều đó ở mọi nơi. Điều đó thường an toàn, vì biến là địa phương, không gì bên ngoài hàm có thể truy cập được nó. Và bên trong hàm, minifier thay thế mọi lần đề cập đến nó. Các minifier rất thông minh, chúng phân tích cấu trúc mã, vì vậy chúng không phá vỡ bất cứ thứ gì. Chúng không chỉ là tìm và thay thế ngu ngốc.

Vì vậy, nếu `new Function` có quyền truy cập vào các biến bên ngoài, nó sẽ không thể tìm thấy `userName` đã bị đổi tên.

**Nếu `new Function` có quyền truy cập vào các biến bên ngoài, nó sẽ gặp vấn đề với các minifier.**

Ngoài ra, mã như vậy sẽ có kiến trúc kém và dễ gặp lỗi.

Để chuyển thứ gì đó vào một hàm được tạo là `new Function`, chúng ta nên sử dụng các đối số của nó.

## [Tóm tắt](#summary)

Cú pháp:

```
let func = new Function ([arg1, arg2, ...argN], functionBody);
```

Theo lý do lịch sử, các đối số cũng có thể được cung cấp dưới dạng danh sách được phân tách bằng dấu phẩy.

Ba khai báo này có nghĩa như nhau:

```
new Function('a', 'b', 'return a + b'); // cú pháp cơ bản
new Function('a,b', 'return a + b'); // phân tách bằng dấu phẩy
new Function('a , b', 'return a + b'); // phân tách bằng dấu phẩy có khoảng trắng
```

Các hàm được tạo bằng `new Function` có `[[Environment]]` tham chiếu đến Lexical Environment toàn cục, không phải môi trường bên ngoài. Do đó, chúng không thể sử dụng các biến bên ngoài. Nhưng đó thực sự là điều tốt, vì nó bảo vệ chúng ta khỏi các lỗi. Truyền các tham số một cách rõ ràng là một phương pháp tốt hơn nhiều về mặt kiến trúc và không gây ra vấn đề với các minifier.
