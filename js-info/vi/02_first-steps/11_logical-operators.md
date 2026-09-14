# Các toán tử logic

> Nguồn: [https://javascript.info/logical-operators](https://javascript.info/logical-operators)

<!-- fetched: 2026-09-14 -->

Có bốn toán tử logic trong JavaScript: `||` (HOẶC), `&&` (VÀ), `!` (PHỦ ĐỊNH), `??` (Ghép không rỗng). Ở đây chúng ta sẽ đề cập đến ba toán tử đầu tiên, toán tử `??` sẽ được nói đến ở bài viết tiếp theo.

Mặc dù được gọi là "logic", chúng có thể được áp dụng cho các giá trị thuộc bất kỳ kiểu nào, không chỉ boolean. Kết quả của chúng cũng có thể thuộc bất kỳ kiểu nào.

Hãy cùng xem chi tiết.

## [|| (HOẶC)](#or)

Toán tử "HOẶC" được biểu diễn bằng hai ký tự đường dọc:

```
result = a || b;
```

Trong lập trình cổ điển, HOẶC logic có nghĩa là thao tác với các giá trị boolean. Nếu bất kỳ đối số nào là `true`, nó trả về `true`, ngược lại nó trả về `false`.

Trong JavaScript, toán tử phức tạp hơn một chút và mạnh mẽ hơn. Nhưng trước tiên, hãy xem những gì xảy ra với các giá trị boolean.

Có bốn tổ hợp logic có thể:

```
alert( true || true );   // true
alert( false || true );  // true
alert( true || false );  // true
alert( false || false ); // false
```

Như chúng ta có thể thấy, kết quả luôn là `true` ngoại trừ trường hợp cả hai toán hạng đều là `false`.

Nếu một toán hạng không phải là boolean, nó sẽ được chuyển đổi sang boolean để đánh giá.

Ví dụ, số `1` được xử lý là `true`, số `0` là `false`:

```
if (1 || 0) { // hoạt động giống như if( true || false )
  alert( 'truthy!' );
}
```

Hầu hết thời gian, HOẶC `||` được sử dụng trong câu lệnh `if` để kiểm tra xem *bất kỳ* điều kiện nào trong các điều kiện đã cho là `true`.

Ví dụ:

```
let hour = 9;

if (hour < 10 || hour > 18) {
  alert( 'Văn phòng đóng cửa.' );
}
```

Chúng ta có thể truyền nhiều điều kiện hơn:

```
let hour = 12;
let isWeekend = true;

if (hour < 10 || hour > 18 || isWeekend) {
  alert( 'Văn phòng đóng cửa.' ); // cuối tuần
}
```

## [HOẶC "||" tìm giá trị truthy đầu tiên](#or-finds-the-first-truthy-value)

Logic được mô tả ở trên là somewhat cổ điển. Bây giờ, hãy tìm hiểu các tính năng "bổ sung" của JavaScript.

Thuật toán mở rộng hoạt động như sau.

Cho nhiều giá trị HOẶC với nhau:

```
result = value1 || value2 || value3;
```

Toán tử HOẶC `||` làm những điều sau:

- Đánh giá các toán hạng từ trái sang phải.
- Với mỗi toán hạng, chuyển đổi nó sang boolean. Nếu kết quả là `true`, dừng và trả về giá trị gốc của toán hạng đó.
- Nếu tất cả các toán hạng đã được đánh giá (tức là tất cả đều là `false`), trả về toán hạng cuối cùng.

Một giá trị được trả về ở dạng gốc, không có chuyển đổi.

Nói cách khác, một chuỗi HOẶC `||` trả về giá trị truthy đầu tiên hoặc giá trị cuối cùng nếu không tìm thấy giá trị truthy nào.

Ví dụ:

```
alert( 1 || 0 ); // 1 (1 là truthy)

alert( null || 1 ); // 1 (1 là giá trị truthy đầu tiên)
alert( null || 0 || 1 ); // 1 (giá trị truthy đầu tiên)

alert( undefined || null || 0 ); // 0 (tất cả đều falsy, trả về giá trị cuối cùng)
```

Điều này dẫn đến một số cách sử dụng thú vị so với "HOẶC thuần túy, cổ điển, chỉ boolean".

1. **Lấy giá trị truthy đầu tiên từ một danh sách các biến hoặc biểu thức.**

   Ví dụ, chúng ta có các biến `firstName`, `lastName` và `nickName`, tất cả đều tùy chọn (tức là có thể là undefined hoặc có giá trị falsy).

   Hãy sử dụng HOẶC `||` để chọn cái có dữ liệu và hiển thị nó (hoặc `"Anonymous"` nếu không có gì được đặt):

   ```
   let firstName = "";
   let lastName = "";
   let nickName = "SuperCoder";

   alert( firstName || lastName || nickName || "Anonymous"); // SuperCoder
   ```

   Nếu tất cả các biến đều falsy, `"Anonymous"` sẽ được hiển thị.

2. **Đánh giá ngắn gọn (short-circuit evaluation).**

   Một tính năng khác của toán tử HOẶC `||` là gọi là "đánh giá ngắn gọn".

   Nó có nghĩa là `||` xử lý các đối số của nó cho đến khi đạt được giá trị truthy đầu tiên, sau đó giá trị được trả về ngay lập tức, mà không cần chạm vào đối số khác.

   Tầm quan trọng của tính năng này trở nên rõ ràng nếu một toán hạng không phải là một giá trị, mà là một biểu thức có tác dụng phụ, chẳng hạn như gán biến hoặc gọi hàm.

   Trong ví dụ dưới đây, chỉ có thông báo thứ hai được in ra:

   ```
   true || alert("không được in");
   false || alert("được in");
   ```

   Ở dòng đầu tiên, toán tử HOẶC `||` dừng đánh giá ngay lập tức khi thấy `true`, vì vậy `alert` không được chạy.

   Đôi khi, người ta sử dụng tính năng này để thực thi các lệnh chỉ khi điều kiện ở phần bên trái là falsy.

## [&& (VÀ)](#and)

Toán tử AND được biểu diễn bằng hai ký tự ampersand `&&`:

```
result = a && b;
```

Trong lập trình cổ điển, AND trả về `true` nếu cả hai toán hạng đều truthy và `false` ngược lại:

```
alert( true && true );   // true
alert( false && true );  // false
alert( true && false );  // false
alert( false && false ); // false
```

Một ví dụ với `if`:

```
let hour = 12;
let minute = 30;

if (hour == 12 && minute == 30) {
  alert( 'Giờ là 12:30' );
}
```

Giống như với HOẶC, bất kỳ giá trị nào cũng được phép làm toán hạng của AND:

```
if (1 && 0) { // được đánh giá là true && false
  alert( "không hoạt động, vì kết quả là falsy" );
}
```

## [AND "&&" tìm giá trị falsy đầu tiên](#and-finds-the-first-falsy-value)

Cho nhiều giá trị AND với nhau:

```
result = value1 && value2 && value3;
```

Toán tử AND `&&` làm những điều sau:

- Đánh giá các toán hạng từ trái sang phải.
- Với mỗi toán hạng, chuyển đổi nó sang boolean. Nếu kết quả là `false`, dừng và trả về giá trị gốc của toán hạng đó.
- Nếu tất cả các toán hạng đã được đánh giá (tức là tất cả đều truthy), trả về toán hạng cuối cùng.

Nói cách khác, AND trả về giá trị falsy đầu tiên hoặc giá trị cuối cùng nếu không tìm thấy giá trị falsy nào.

Các quy tắc ở trên tương tự như HOẶC. Sự khác biệt là AND trả về giá trị *falsy* đầu tiên trong khi HOẶC trả về giá trị *truthy* đầu tiên.

Ví dụ:

```
// nếu toán hạng đầu tiên là truthy,
// AND trả về toán hạng thứ hai:
alert( 1 && 0 ); // 0
alert( 1 && 5 ); // 5

// nếu toán hạng đầu tiên là falsy,
// AND trả về nó. Toán hạng thứ hai bị bỏ qua
alert( null && 5 ); // null
alert( 0 && "không quan trọng" ); // 0
```

Chúng ta cũng có thể truyền nhiều giá trị liên tiếp. Xem cách giá trị falsy đầu tiên được trả về:

```
alert( 1 && 2 && null && 3 ); // null
```

Khi tất cả các giá trị đều truthy, giá trị cuối cùng được trả về:

```
alert( 1 && 2 && 3 ); // 3, giá trị cuối cùng
```

Độ ưu tiên của AND `&&` cao hơn HOẶC `||`

Độ ưu tiên của toán tử AND `&&` cao hơn HOẶC `||`.

Vì vậy, mã `a && b || c && d` về cơ bản giống như nếu các biểu thức `&&` nằm trong dấu ngoặc đơn: `(a && b) || (c && d)`.

Không thay thế `if` bằng `||` hoặc `&&`

Đôi khi, người ta sử dụng toán tử AND `&&` như một "cách viết ngắn hơn của `if`".

Ví dụ:

```
let x = 1;

(x > 0) && alert( 'Lớn hơn không!' );
```

Hành động ở phần bên phải của `&&` sẽ thực thi chỉ khi việc đánh giá đạt đến nó. Tức là, chỉ khi `(x > 0)` là true.

Vì vậy, về cơ bản chúng ta có một phiên bản tương đương của:

```
let x = 1;

if (x > 0) alert( 'Lớn hơn không!' );
```

Mặc dù, phiên bản với `&&` xuất hiện ngắn gọn hơn, `if` rõ ràng hơn và có xu hướng dễ đọc hơn một chút. Vì vậy, chúng ta khuyến nghị sử dụng mỗi cấu trúc cho mục đích của nó: sử dụng `if` nếu chúng ta muốn `if` và sử dụng `&&` nếu chúng ta muốn VÀ.

## [! (PHỦ ĐỊNH)](#not)

Toán tử phủ định boolean được biểu diễn bằng ký tự dấu chấm than `!`.

Cú pháp khá đơn giản:

```
result = !value;
```

Toán tử nhận một đối số và làm những điều sau:

1. Chuyển đổi toán hạng sang kiểu boolean: `true/false`.
2. Trả về giá trị đảo ngược.

Ví dụ:

```
alert( !true ); // false
alert( !0 ); // true
```

Phủ định kép `!!` đôi khi được sử dụng để chuyển đổi một giá trị sang kiểu boolean:

```
alert( !!"chuỗi không rỗng" ); // true
alert( !!null ); // false
```

Tức là, phủ định đầu tiên chuyển đổi giá trị sang boolean và trả về giá trị đảo ngược, và phủ định thứ hai đảo ngược nó một lần nữa. Cuối cùng, chúng ta có một chuyển đổi giá trị sang boolean thuần túy.

Có một cách verbose hơn một chút để làm điều tương tự – hàm built-in `Boolean`:

```
alert( Boolean("chuỗi không rỗng") ); // true
alert( Boolean(null) ); // false
```

Độ ưu tiên của PHỦ ĐỊNH `!` là cao nhất trong số tất cả các toán tử logic, vì vậy nó luôn thực thi đầu tiên, trước `&&` hoặc `||`.

---

---

## Các bài tập

## [Các bài tập](#tasks)

### [Kết quả của HOẶC là gì?](#what-s-the-result-of-or)

mức độ quan trọng: 5

Mã dưới đây sẽ xuất ra gì?

```
alert( null || 2 || undefined );
```

lời giải

Câu trả lời là `2`, đó là giá trị truthy đầu tiên.

```
alert( null || 2 || undefined );
```

### [Kết quả của các alert HOẶC với nhau là gì?](#what-s-the-result-of-or-ed-alerts)

mức độ quan trọng: 3

Mã dưới đây sẽ xuất ra gì?

```
alert( alert(1) || 2 || alert(3) );
```

lời giải

Câu trả lời: đầu tiên là `1`, sau đó là `2`.

```
alert( alert(1) || 2 || alert(3) );
```

Lệnh gọi `alert` không trả về giá trị. Hay nói cách khác, nó trả về `undefined`.

1. HOẶC `||` đầu tiên đánh giá toán hạng bên trái `alert(1)`. Điều đó hiển thị thông báo đầu tiên với `1`.
2. `alert` trả về `undefined`, vì vậy HOẶC chuyển sang toán hạng thứ hai tìm kiếm một giá trị truthy.
3. Toán hạng thứ hai `2` là truthy, vì vậy việc thực thi bị dừng, `2` được trả về và sau đó được hiển thị bởi alert bên ngoài.

Sẽ không có `3`, vì việc đánh giá không đạt đến `alert(3)`.

### [Kết quả của AND là gì?](#what-is-the-result-of-and)

mức độ quan trọng: 5

Mã này sẽ hiển thị gì?

```
alert( 1 && null && 2 );
```

lời giải

Câu trả lời: `null`, vì đó là giá trị falsy đầu tiên trong danh sách.

```
alert(1 && null && 2);
```

### [Kết quả của các alert AND với nhau là gì?](#what-is-the-result-of-and-ed-alerts)

mức độ quan trọng: 3

Mã này sẽ hiển thị gì?

```
alert( alert(1) && alert(2) );
```

lời giải

Câu trả lời: `1`, và sau đó là `undefined`.

```
alert( alert(1) && alert(2) );
```

Lệnh gọi `alert` trả về `undefined` (nó chỉ hiển thị một thông báo, vì vậy không có return có ý nghĩa).

Bởi vì vậy, `&&` đánh giá toán hạng bên trái (xuất `1`), và ngay lập tức dừng, vì `undefined` là một giá trị falsy. Và `&&` tìm kiếm một giá trị falsy và trả về nó, vì vậy là xong.

### [Kết quả của HOẶC VÀ HOẶC](#the-result-of-or-and-or)

mức độ quan trọng: 5

Kết quả sẽ là gì?

```
alert( null || 2 && 3 || 4 );
```

lời giải

Câu trả lời: `3`.

```
alert( null || 2 && 3 || 4 );
```

Độ ưu tiên của AND `&&` cao hơn `||`, vì vậy nó thực thi trước.

Kết quả của `2 && 3 = 3`, vì vậy biểu thức trở thành:

```
null || 3 || 4
```

Bây giờ kết quả là giá trị truthy đầu tiên: `3`.

### [Kiểm tra khoảng между](#check-the-range-between)

mức độ quan trọng: 3

Viết điều kiện `if` để kiểm tra rằng `age` nằm trong khoảng từ `14` đến `90` bao gồm.

"Bao gồm" có nghĩa là `age` có thể đạt đến các cạnh `14` hoặc `90`.

lời giải

```
if (age >= 14 && age <= 90)
```

### [Kiểm tra khoảng ngoài](#check-the-range-outside)

mức độ quan trọng: 3

Viết điều kiện `if` để kiểm tra rằng `age` KHÔNG nằm trong khoảng từ `14` đến `90` bao gồm.

Tạo hai biến thể: cái đầu tiên sử dụng PHỦ ĐỊNH `!`, cái thứ hai – không sử dụng nó.

lời giải

Biến thể đầu tiên:

```
if (!(age >= 14 && age <= 90))
```

Biến thể thứ hai:

```
if (age < 14 || age > 90)
```

### [Một câu hỏi về "if"](#a-question-about-if)

mức độ quan trọng: 5

Trong số các `alert` sau đây, những cái nào sẽ thực thi?

Kết quả của các biểu thức bên trong `if(...)` sẽ là gì?

```
if (-1 || 0) alert( 'first' );
if (-1 && 0) alert( 'second' );
if (null || -1 && 1) alert( 'third' );
```

lời giải

Câu trả lời: cái đầu tiên và cái thứ ba sẽ thực thi.

Chi tiết:

```
// Chạy.
// Kết quả của -1 || 0 = -1, truthy
if (-1 || 0) alert( 'first' );

// Không chạy
// -1 && 0 = 0, falsy
if (-1 && 0) alert( 'second' );

// Thực thi
// Toán tử && có độ ưu tiên cao hơn ||
// vì vậy -1 && 1 thực thi trước, cho chúng ta chuỗi:
// null || -1 && 1  ->  null || 1  ->  1
if (null || -1 && 1) alert( 'third' );
```

### [Kiểm tra login](#check-the-login)

mức độ quan trọng: 3

Viết mã yêu cầu login với `prompt`.

Nếu người truy cập nhập `"Admin"`, thì `prompt` yêu cầu mật khẩu, nếu input là dòng trống hoặc `Esc` – hiển thị "Đã hủy", nếu là chuỗi khác – thì hiển thị "Tôi không biết bạn".

Mật khẩu được kiểm tra như sau:

- Nếu nó bằng "TheMaster", thì hiển thị "Chào mừng!",
- Chuỗi khác – hiển thị "Sai mật khẩu",
- Đối với chuỗi trống hoặc input bị hủy, hiển thị "Đã hủy"

Sơ đồ:

![](/task/check-login/ifelse_task.svg)

Vui lòng sử dụng các khối `if` lồng nhau. Chú ý đến khả năng đọc tổng thể của mã.

Gợi ý: truyền input trống vào prompt trả về chuỗi trống `''`. Nhấn `ESC` trong khi prompt trả về `null`.

[Chạy demo](#)

lời giải

```
let userName = prompt("Ai đó đấy?", '');

if (userName === 'Admin') {

  let pass = prompt('Mật khẩu?', '');

  if (pass === 'TheMaster') {
    alert( 'Chào mừng!' );
  } else if (pass === '' || pass === null) {
    alert( 'Đã hủy' );
  } else {
    alert( 'Sai mật khẩu' );
  }

} else if (userName === '' || userName === null) {
  alert( 'Đã hủy' );
} else {
  alert( "Tôi không biết bạn" );
}
```

Lưu ý các thụt lề dọc bên trong các khối `if`. Về mặt kỹ thuật chúng không bắt buộc, nhưng làm cho mã dễ đọc hơn.
