# Cấu trúc mã

> Nguồn: [https://javascript.info/structure](https://javascript.info/structure)

<!-- fetched: 2026-09-14 -->

Thứ chúng ta sẽ nghiên cứu đầu tiên là các khối xây dựng của mã.

## [Câu lệnh](#statements)

Các câu lệnh là các cấu trúc cú pháp và lệnh thực hiện các hành động.

Chúng ta đã thấy một câu lệnh, `alert('Hello, world!')`, hiển thị thông báo “Xin chào, thế giới!”.

Chúng ta có thể có bao nhiêu câu lệnh trong mã của mình tùy thích. Các câu lệnh có thể được phân tách bằng dấu chấm phẩy.

Ví dụ, ở đây chúng ta chia “Xin chào Thế giới” thành hai alerts:

```
alert('Hello'); alert('World');
```

Thông thường, các câu lệnh được viết trên các dòng riêng biệt để làm cho mã dễ đọc hơn:

```
alert('Hello');
alert('World');
```

## [Dấu chấm phẩy](#semicolon)

Dấu chấm phẩy có thể bị bỏ qua trong hầu hết các trường hợp khi có dấu ngắt dòng.

Điều này cũng hoạt động:

```
alert('Hello')
alert('World')
```

Ở đây, JavaScript diễn giải dấu ngắt dòng là một dấu chấm phẩy “ngầm”. Điều này được gọi là [chèn dấu chấm phẩy tự động](https://tc39.github.io/ecma262/#sec-automatic-semicolon-insertion).

**Trong hầu hết các trường hợp, ngắt dòng ngụ ý dấu chấm phẩy. Nhưng “trong hầu hết các trường hợp” không có nghĩa là “luôn luôn”!**

Có những trường hợp khi ngắt dòng không có nghĩa là dấu chấm phẩy. Ví dụ:

```
alert(3 +
1
+ 2);
```

Mã xuất ra `6` vì JavaScript không chèn dấu chấm phẩy ở đây. Nó là hiển nhiên rằng nếu dòng kết thúc với dấu cộng `"+"`, thì đó là một “biểu thức không hoàn chỉnh”, vì vậy dấu chấm phẩy ở đó sẽ sai. Và trong trường hợp này, nó hoạt động như dự định.

**Nhưng có những tình huống mà JavaScript “thất bại” trong việc giả định một dấu chấm phẩy nơi nó thực sự cần thiết.**

Các lỗi xảy ra trong những trường hợp như vậy khá khó tìm và sửa.

Một ví dụ về lỗi

Nếu bạn tò mò muốn xem một ví dụ cụ thể của lỗi như vậy, hãy kiểm tra mã này:

```
alert("Hello");

[1, 2].forEach(alert);
```

Không cần suy nghĩ về ý nghĩa của dấu ngoặc vuông `[]` và `forEach` nữa. Chúng ta sẽ nghiên cứu chúng sau. Hiện tại, chỉ cần nhớ kết quả của việc chạy mã: nó hiển thị `Hello`, sau đó `1`, sau đó `2`.

Bây giờ hãy xóa dấu chấm phẩy sau `alert`:

```
alert("Hello")

[1, 2].forEach(alert);
```

Sự khác biệt so với mã ở trên chỉ là một ký tự: dấu chấm phẩy ở cuối dòng đầu tiên đã biến mất.

Nếu chúng ta chạy mã này, chỉ có `Hello` đầu tiên hiển thị (và có lỗi, bạn có thể cần mở console để xem nó). Không còn số nào nữa.

Đó là vì JavaScript không giả định một dấu chấm phẩy trước dấu ngoặc vuông `[...]`. Vì vậy, mã trong ví dụ cuối cùng được xử lý như một câu lệnh đơn.

Đây là cách động cơ nhìn thấy nó:

```
alert("Hello")[1, 2].forEach(alert);
```

Có vẻ lạ, phải không? Sự hợp nhất như vậy trong trường hợp này là sai. Chúng ta cần đặt một dấu chấm phẩy sau `alert` để mã hoạt động chính xác.

Điều này có thể xảy ra trong các tình huống khác cũng.

Chúng ta khuyến nghị đặt dấu chấm phẩy giữa các câu lệnh ngay cả khi chúng được phân tách bằng newline. Quy tắc này được cộng đồng chấp nhận rộng rãi. Hãy ghi chú lần nữa – *có thể* bỏ qua dấu chấm phẩy trong hầu hết thời gian. Nhưng an toàn hơn – đặc biệt là đối với người mới bắt đầu – là sử dụng chúng.

## [Comment](#code-comments)

Khi thời gian trôi qua, các chương trình trở nên phức tạp hơn. Điều này trở nên cần thiết để thêm *comment* mô tả mã làm gì và tại sao.

Comment có thể được đặt vào bất kỳ nơi nào trong script. Chúng không ảnh hưởng đến việc thực thi vì động cơ đơn giản bỏ qua chúng.

**Comment một dòng bắt đầu bằng hai ký tự gạch chéo `//`.**

Phần còn lại của dòng là một comment. Nó có thể chiếm một dòng riêng của nó hoặc theo sau một câu lệnh.

Như ở đây:

```
// Comment này chiếm một dòng riêng của nó
alert('Hello');

alert('World'); // Comment này theo sau câu lệnh
```

**Comment nhiều dòng bắt đầu bằng một gạch chéo và một dấu hoa thị `/*` và kết thúc bằng một dấu hoa thị và một gạch chéo `*/`.**

Như thế này:

```
/* Một ví dụ với hai thông báo.
Đây là một comment nhiều dòng.
*/
alert('Hello');
alert('World');
```

Nội dung của comment bị bỏ qua, vì vậy nếu chúng ta đặt mã bên trong `/* … */`, nó sẽ không thực thi.

Đôi khi nó có thể hữu ích để tạm thời vô hiệu hóa một phần mã:

```
/* Comment mã
alert('Hello');
*/
alert('World');
```

Sử dụng phím nóng!

Trong hầu hết các editor, một dòng mã có thể được comment bằng cách nhấn phím nóng `Ctrl+/` cho comment một dòng và something like `Ctrl+Shift+/` – cho comment nhiều dòng (chọn một đoạn mã và nhấn phím nóng). Đối với Mac, hãy thử `Cmd` thay vì `Ctrl` và `Option` thay vì `Shift`.

Comment lồng nhau không được hỗ trợ!

Không thể có `/*...*/` bên trong một `/*...*/` khác.

Mã như vậy sẽ chết với lỗi:

```
/*
  /* comment lồng nhau ?!? */
*/
alert( 'World' );
```

Xin đừng ngại comment mã của bạn.

Comment làm tăng tổng kích thước mã, nhưng đó không phải là vấn đề gì. Có nhiều công cụ sẽ minify mã trước khi xuất bản lên máy chủ production. Chúng loại bỏ các comment, vì vậy chúng không xuất hiện trong các script đang hoạt động. Do đó, comment không có tác động tiêu cực nào đến production.

Sau này trong khóa học sẽ có một chương [Chất lượng mã](/code-quality) cũng giải thích cách viết comment tốt hơn.
