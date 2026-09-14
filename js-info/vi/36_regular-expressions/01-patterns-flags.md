# Pattern và flag

> Source: [https://javascript.info/regexp-introduction](https://javascript.info/regexp-introduction)

<!-- fetched: 2026-09-14 -->

Regular expression là các pattern cung cấp cách mạnh mẽ để tìm kiếm và thay thế trong văn bản.

Trong JavaScript, chúng có sẵn thông qua object [RegExp](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/RegExp), đồng thời được tích hợp trong các method của string.

## [Regular Expressions](#regular-expressions)

Một regular expression (còn gọi là “regexp”, hay chỉ đơn giản là “reg”) gồm một *pattern* và các *flag* tùy chọn.

Có hai cú pháp để tạo object regular expression.

Cú pháp “dài”:

```
regexp = new RegExp("pattern", "flags");
```

Và cú pháp “ngắn”, dùng dấu gạch chéo `"/"`:

```
regexp = /pattern/; // không có flag
regexp = /pattern/gmi; // có các flag g, m và i (sẽ tìm hiểu sau)
```

Dấu gạch chéo `/.../` báo cho JavaScript biết rằng chúng ta đang tạo một regular expression. Chúng đóng vai trò giống như dấu nháy kép đối với string.

Trong cả hai trường hợp, `regexp` đều là instance của class `RegExp` có sẵn.

Sự khác nhau chính giữa hai cú pháp này là pattern dùng dấu gạch chéo `/.../` không cho phép chèn các biểu thức (giống như string template literal với `${...}`). Chúng hoàn toàn tĩnh.

Dấu gạch chéo được dùng khi chúng ta đã biết regular expression tại thời điểm viết code – và đây là trường hợp phổ biến nhất. Trong khi đó, `new RegExp` thường được dùng khi cần tạo regexp “trực tiếp” từ một string sinh ra động. Ví dụ:

```
let tag = prompt("What tag do you want to find?", "h2");

let regexp = new RegExp(`<${tag}>`); // giống /<h2>/ nếu trả lời "h2" ở prompt trên
```

## [Flags](#flags)

Regular expression có thể có các flag ảnh hưởng đến việc tìm kiếm.

Trong JavaScript chỉ có 6 flag:

`i`
:   Có flag này thì việc tìm kiếm không phân biệt hoa thường: không có sự khác biệt giữa `A` và `a` (xem ví dụ bên dưới).

`g`
:   Có flag này thì việc tìm kiếm sẽ tìm tất cả các match, nếu không – chỉ trả về match đầu tiên.

`m`
:   Multiline mode (bài viết [Multiline mode của anchor ^ $, flag "m"](/regexp-multiline-mode)).

`s`
:   Bật chế độ “dotall”, cho phép dấu chấm `.` match ký tự xuống dòng `\n` (xem bài viết [Character classes](/regexp-character-classes)).

`u`
:   Bật hỗ trợ đầy đủ cho Unicode. Flag này cho phép xử lý đúng các surrogate pair. Xem thêm trong bài viết [Unicode: flag "u" và class \p{...}](/regexp-unicode).

`y`
:   Chế độ “sticky”: tìm kiếm tại đúng vị trí trong văn bản (xem bài viết [Sticky flag "y", tìm kiếm tại vị trí](/regexp-sticky))

Màu sắc

Từ đây trở đi, quy tắc màu như sau:

- regexp – `đỏ`
- string (nơi tìm kiếm) – `xanh dương`
- kết quả – `xanh lá`

## [Tìm kiếm: str.match](#searching-str-match)

Như đã đề cập ở trên, regular expression được tích hợp với các method của string.

Method `str.match(regexp)` tìm tất cả các match của `regexp` trong string `str`.

Nó có 3 chế độ hoạt động:

1. Nếu regular expression có flag `g`, nó trả về một mảng gồm tất cả các match:

    ```
    let str = "We will, we will rock you";

    alert( str.match(/we/gi) ); // We,we (mảng chứa 2 substring match)
    ```

    Lưu ý rằng cả `We` và `we` đều được tìm thấy, vì flag `i` làm regular expression không phân biệt hoa thường.
2. Nếu không có flag này, nó chỉ trả về match đầu tiên dưới dạng mảng, với match đầy đủ ở index `0` và một số chi tiết bổ sung trong các properties:

    ```
    let str = "We will, we will rock you";

    let result = str.match(/we/i); // không có flag g

    alert( result[0] );     // We (match thứ nhất)
    alert( result.length ); // 1

    // Chi tiết:
    alert( result.index );  // 0 (vị trí của match)
    alert( result.input );  // We will, we will rock you (string nguồn)
    ```

    Mảng có thể có các index khác ngoài `0` nếu một phần của regular expression được bọc trong dấu ngoặc. Chúng ta sẽ tìm hiểu trong bài viết [Capturing groups](/regexp-groups).
3. Cuối cùng, nếu không có match nào, `null` được trả về (dù có hay không có flag `g`).

    Đây là một điểm rất quan trọng. Nếu không có match nào, chúng ta không nhận được mảng rỗng mà nhận được `null`. Quên điều này có thể dẫn đến lỗi, ví dụ:

    ```
    let matches = "JavaScript".match(/HTML/); // = null

    if (!matches.length) { // Lỗi: Cannot read property 'length' of null
      alert("Lỗi ở dòng trên");
    }
    ```

    Nếu muốn kết quả luôn là mảng, chúng ta có thể viết như sau:

    ```
    let matches = "JavaScript".match(/HTML/) || [];

    if (!matches.length) {
      alert("Không có match"); // giờ hoạt động rồi
    }
    ```

## [Thay thế: str.replace](#replacing-str-replace)

Method `str.replace(regexp, replacement)` thay các match tìm thấy bằng `regexp` trong string `str` bằng `replacement` (thay tất cả nếu có flag `g`, nếu không thì chỉ thay match đầu tiên).

Ví dụ:

```
// không có flag g
alert( "We will, we will".replace(/we/i, "I") ); // I will, we will

// có flag g
alert( "We will, we will".replace(/we/ig, "I") ); // I will, I will
```

Thủ nguyên thứ hai là string `replacement`. Chúng ta có thể dùng các tổ hợp ký tự đặc biệt trong đó để chèn các phần của match:

| Kí hiệu | Hành động trong string thay thế |
| --- | --- |
| `$&` | chèn toàn bộ match |
| `` $` `` | chèn phần string trước match |
| `$'` | chèn phần string sau match |
| `$n` | nếu `n` là số có 1-2 chữ số, thì chèn nội dung cặp ngoặc thứ n, xem thêm trong bài viết [Capturing groups](/regexp-groups) |
| `$<name>` | chèn nội dung cặp ngoặc có `name` đã cho, xem thêm trong bài viết [Capturing groups](/regexp-groups) |
| `$$` | chèn ký tự `$` |

Ví dụ với `$&`:

```
alert( "I love HTML".replace(/HTML/, "$& and JavaScript") ); // I love HTML and JavaScript
```

## [Kiểm tra: regexp.test](#testing-regexp-test)

Method `regexp.test(str)` tìm ít nhất một match, nếu tìm thấy thì trả về `true`, nếu không thì `false`.

```
let str = "I love JavaScript";
let regexp = /LOVE/i;

alert( regexp.test(str) ); // true
```

Sau này trong chương này chúng ta sẽ học thêm về regular expression, đi qua thêm các ví dụ, và cũng sẽ gặp các method khác.

Thông tin đầy đủ về các method được nêu trong bài viết [Các method của RegExp và String](/regexp-methods).

## [Tóm tắt](#summary)

- Một regular expression gồm một pattern và các flag tùy chọn: `g`, `i`, `m`, `u`, `s`, `y`.
- Không có flag và các ký tự đặc biệt (sẽ học sau), việc tìm kiếm bằng regexp giống như tìm kiếm substring.
- Method `str.match(regexp)` tìm các match: tất cả nếu có flag `g`, nếu không thì chỉ match đầu tiên.
- Method `str.replace(regexp, replacement)` thay các match tìm thấy bằng `regexp` bằng `replacement`: tất cả nếu có flag `g`, nếu không thì chỉ match đầu tiên.
- Method `regexp.test(str)` trả về `true` nếu có ít nhất một match, nếu không thì trả về `false`.
