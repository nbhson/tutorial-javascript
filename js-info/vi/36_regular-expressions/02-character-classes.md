# Character class

> Source: [https://javascript.info/regexp-character-classes](https://javascript.info/regexp-character-classes)

<!-- fetched: 2026-09-14 -->

Hãy xem một bài toán thực tế – chúng ta có số điện thoại như `"+7(903)-123-45-67"`, và cần biến nó thành các chữ số thuần: `79031234567`.

Để làm điều đó, chúng ta có thể tìm và xóa tất cả những gì không phải số. Character class sẽ giúp ích được.

*Character class* là một cách ghi đặc biệt để match bất kỳ ký tự nào thuộc một tập hợp nhất định.

Ban đầu, hãy tìm hiểu class “chữ số”. Nó được viết là `\d` và có nghĩa là “bất kỳ một chữ số đơn lẻ”.

Ví dụ, hãy tìm chữ số đầu tiên trong số điện thoại:

```
let str = "+7(903)-123-45-67";

let regexp = /\d/;

alert( str.match(regexp) ); // 7
```

Không có flag `g`, regular expression chỉ tìm match đầu tiên, tức là chữ số `\d` đầu tiên.

Hãy thêm flag `g` để tìm tất cả các chữ số:

```
let str = "+7(903)-123-45-67";

let regexp = /\d/g;

alert( str.match(regexp) ); // mảng các match: 7,9,0,3,1,2,3,4,5,6,7

// tạo số điện thoại chỉ gồm chữ số từ chúng:
alert( str.match(regexp).join('') ); // 79031234567
```

Đó là character class cho chữ số. Còn có các character class khác nữa.

Các class được dùng nhiều nhất:

`\d` (“d” lấy từ “digit” – chữ số)
:   Một chữ số: ký tự từ `0` đến `9`.

`\s` (“s” lấy từ “space” – khoảng trắng)
:   Ký tự khoảng trắng: bao gồm dấu cách, tab `\t`, xuống dòng `\n` và một số ký tự hiếm khác như `\v`, `\f` và `\r`.

`\w` (“w” lấy từ “word” – từ)
:   Ký tự “thuộc từ”: hoặc là chữ cái trong bảng Latin, hoặc chữ số, hoặc dấu gạch dưới `_`. Các chữ cái không phải Latin (như tiếng Nga hay tiếng Hindi) không thuộc `\w`.

Ví dụ, `\d\s\w` nghĩa là một “chữ số” theo sau bởi một “ký tự khoảng trắng” rồi theo sau bởi một “ký tự thuộc từ”, chẳng hạn như `1 a`.

**Regex có thể chứa cả ký tự thường lẫn character class.**

Ví dụ, `CSS\d` match string `CSS` có theo sau một chữ số:

```
let str = "Is there CSS4?";
let regexp = /CSS\d/

alert( str.match(regexp) ); // CSS4
```

Ta cũng có thể dùng nhiều character class:

```
alert( "I love HTML5!".match(/\s\w\w\w\w\d/) ); // ' HTML5'
```

Match (mỗi character class trong regexp tương ứng với ký tự kết quả):

![](/article/regexp-character-classes/love-html5-classes.svg)

## [Class nghịch đảo](#inverse-classes)

Với mỗi character class, luôn tồn tại một “class nghịch đảo”, được ghi bằng cùng chữ cái nhưng viết hoa.

“Nghịch đảo” có nghĩa là nó match mọi ký tự còn lại, ví dụ:

`\D`
:   Không phải chữ số: bất kỳ ký tự nào trừ `\d`, ví dụ như một chữ cái.

`\S`
:   Không phải khoảng trắng: bất kỳ ký tự nào trừ `\s`, ví dụ như một chữ cái.

`\W`
:   Ký tự không “thuộc từ”: bất cứ thứ gì trừ `\w`, ví dụ như một chữ cái không phải Latin hay khoảng trắng.

Ở đầu chương, chúng ta đã thấy cách tạo số điện thoại chỉ gồm chữ số từ string như `+7(903)-123-45-67`: tìm tất cả các chữ số rồi nối chúng lại.

```
let str = "+7(903)-123-45-67";

alert( str.match(/\d/g).join('') ); // 79031234567
```

Một cách khác, ngắn gọn hơn là tìm các ký tự không phải chữ số `\D` và xóa chúng khỏi string:

```
let str = "+7(903)-123-45-67";

alert( str.replace(/\D/g, "") ); // 79031234567
```

## [Dấu chấm là “bất kỳ ký tự nào”](#a-dot-is-any-character)

Dấu chấm `.` là một character class đặc biệt match “bất kỳ ký tự nào trừ xuống dòng”.

Ví dụ:

```
alert( "Z".match(/./) ); // Z
```

Hoặc ở giữa regexp:

```
let regexp = /CS.4/;

alert( "CSS4".match(regexp) ); // CSS4
alert( "CS-4".match(regexp) ); // CS-4
alert( "CS 4".match(regexp) ); // CS 4 (khoảng trắng cũng là một ký tự)
```

Lưu ý rằng dấu chấm có nghĩa là “bất kỳ ký tự nào”, chứ không phải “không có ký tự”. Phải có một ký tự để match nó:

```
alert( "CS4".match(/CS.4/) ); // null, không match vì không có ký tự cho dấu chấm
```

### [Dấu chấm match bất kỳ ký tự với flag “s”](#dot-as-literally-any-character-with-s-flag)

Mặc định, dấu chấm không match ký tự xuống dòng `\n`.

Ví dụ, regexp `A.B` match `A`, rồi đến `B` với bất kỳ ký tự nào ở giữa, trừ xuống dòng `\n`:

```
alert( "A\nB".match(/A.B/) ); // null (không match)
```

Có nhiều trường hợp chúng ta muốn dấu chấm có nghĩa là đúng “bất kỳ ký tự nào”, kể cả xuống dòng.

Flag `s` làm đúng việc đó. Nếu regexp có flag này, thì dấu chấm `.` match bất kỳ ký tự nào:

```
alert( "A\nB".match(/A.B/s) ); // A\nB (match!)
```

Không hỗ trợ trong IE

Flag `s` không được hỗ trợ trong IE.

May mắn là có một cách thay thế hoạt động ở khắp nơi. Chúng ta có thể dùng regexp như `[\s\S]` để match “bất kỳ ký tự nào” (pattern này sẽ được giới thiệu trong bài viết [Sets and ranges [...]](/regexp-character-sets-and-ranges)).

```
alert( "A\nB".match(/A[\s\S]B/) ); // A\nB (match!)
```

Pattern `[\s\S]` có nghĩa đen là: “ký tự khoảng trắng HOẶC không phải khoảng trắng”. Nói cách khác, “bất cứ thứ gì”. Chúng ta có thể dùng cặp class bổ sung khác, chẳng hạn như `[\d\D]`, không quan trọng. Hoặc thậm chí là `[^]` – vì nó có nghĩa là match bất kỳ ký tự nào trừ không có gì.

Ta cũng có thể dùng mánh này khi muốn dùng cả hai loại “chấm” trong cùng một pattern: dấu chấm thực sự `.` hoạt động theo cách thường (“không bao gồm xuống dòng”), và một cách để match “bất kỳ ký tự nào” với `[\s\S]` hay tương tự.

Chú ý đến khoảng trắng

Thường thì chúng ta ít chú ý đến khoảng trắng. Đối với chúng ta, các string `1-5` và `1 - 5` gần như giống hệt nhau.

Nhưng nếu regexp không tính đến khoảng trắng, nó có thể không hoạt động.

Hãy thử tìm các chữ số ngăn cách bằng dấu gạch:

```
alert( "1 - 5".match(/\d-\d/) ); // null, không match!
```

Hãy sửa bằng cách thêm khoảng trắng vào regexp `\d - \d`:

```
alert( "1 - 5".match(/\d - \d/) ); // 1 - 5, giờ hoạt động rồi
// hoặc ta có thể dùng class \s:
alert( "1 - 5".match(/\d\s-\s\d/) ); // 1 - 5, cũng hoạt động
```

**Khoảng trắng là một ký tự. Quan trọng như mọi ký tự khác.**

Ta không thể thêm hoặc xóa khoảng trắng khỏi regular expression và mong nó hoạt động như trước.

Nói cách khác, trong regular expression mọi ký tự đều quan trọng, kể cả khoảng trắng.

## [Tóm tắt](#summary)

Có các character class sau:

- `\d` – chữ số.
- `\D` – không phải chữ số.
- `\s` – ký tự khoảng trắng, tab, xuống dòng.
- `\S` – mọi thứ trừ `\s`.
- `\w` – chữ cái Latin, chữ số, dấu gạch dưới `'_'`.
- `\W` – mọi thứ trừ `\w`.
- `.` – bất kỳ ký tự nào nếu regexp có flag `'s'`, nếu không thì bất kỳ ký tự nào trừ xuống dòng `\n`.

…Nhưng chưa hết!

Mã hóa Unicode, được JavaScript sử dụng cho string, cung cấp nhiều tính chất cho ký tự, như: ký tự thuộc ngôn ngữ nào (nếu nó là chữ cái), có phải ký hiệu câu điểm không, v.v.

Chúng ta cũng có thể tìm kiếm theo các tính chất này. Điều đó cần flag `u`, được đề cập trong bài viết tiếp theo.
