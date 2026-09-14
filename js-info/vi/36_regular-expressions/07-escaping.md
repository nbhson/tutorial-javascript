# Escaping, ký tự đặc biệt

> Source: [https://javascript.info/regexp-escaping](https://javascript.info/regexp-escaping)

<!-- fetched: 2026-09-14 -->

Như chúng ta đã thấy, dấu `\` được dùng để ký hiệu character class, ví dụ `\d`. Vậy nên nó là ký tự đặc biệt trong regexp (cũng như trong string thường).

Còn có các ký tự đặc biệt khác, có ý nghĩa đặc biệt trong regexp, như `[ ] { } ( ) \ ^ $ . | ? * +`. Chúng được dùng để thực hiện các thao tác tìm kiếm mạnh mẽ hơn.

Đừng cố ghi nhớ danh sách – sớm thôi chúng ta sẽ xử lý từng ký tự, và bạn sẽ thuộc chúng theo cách tự nhiên.

## [Escaping](#escaping)

Giả sử chúng ta muốn tìm đúng một dấu chấm. Không phải “bất kỳ ký tự nào”, mà đúng dấu chấm.

Để dùng một ký tự đặc biệt như ký tự thường, thêm dấu `\` phía trước: `\.`.

Điều này còn gọi là “escape một ký tự”.

Ví dụ:

```
alert( "Chapter 5.1".match(/\d\.\d/) ); // 5.1 (match!)
alert( "Chapter 511".match(/\d\.\d/) ); // null (tìm đúng dấu chấm \.)
```

Dấu ngoặc cũng là ký tự đặc biệt, vậy nên nếu muốn dùng chúng, ta phải dùng `\(`. Ví dụ bên dưới tìm string `"g()"`:

```
alert( "function g()".match(/g\(\)/) ); // "g()"
```

Nếu chúng ta tìm dấu `\`, nó là ký tự đặc biệt trong cả string thường lẫn regexp, nên ta phải kép đôi nó.

```
alert( "1\\2".match(/\\/) ); // '\'
```

## [Dấu gạch chéo](#a-slash)

Ký hiệu `'/'` không phải là ký tự đặc biệt, nhưng trong JavaScript nó được dùng để mở và đóng regexp: `/...pattern.../`, nên chúng ta cũng phải escape nó.

Dưới đây là cách tìm dấu `'/'`:

```
alert( "/".match(/\//) ); // '/'
```

Mặt khác, nếu chúng ta không dùng `/.../` mà tạo regexp bằng `new RegExp`, thì không cần escape:

```
alert( "/".match(new RegExp("/")) ); // tìm thấy /
```

## [new RegExp](#new-regexp)

Nếu chúng ta tạo regular expression bằng `new RegExp`, thì không cần escape `/`, nhưng phải thực hiện một số escape khác.

Ví dụ, hãy xem xét:

```
let regexp = new RegExp("\d\.\d");

alert( "Chapter 5.1".match(regexp) ); // null
```

Việc tìm kiếm tương tự ở một trong các ví dụ trước hoạt động với `/\d\.\d/`, nhưng `new RegExp("\d\.\d")` không hoạt động, tại sao?

Lý do là các dấu `\` bị string “tiêu thụ”. Như chúng ta có thể nhớ lại, string thường có các ký tự đặc biệt riêng, như `\n`, và dấu `\` được dùng để escape.

Dưới đây là cách “\d.\d” được hiểu:

```
alert("\d\.\d"); // d.d
```

Dấu nháy của string “tiêu thụ” các dấu `\` và diễn giải chúng theo cách riêng, ví dụ:

- `\n` – trở thành ký tự xuống dòng,
- `\u1234` – trở thành ký tự Unicode có mã đó,
- …Và khi không có ý nghĩa đặc biệt: như `\d` hay `\z`, thì dấu `\` đơn giản bị bỏ đi.

Vậy `new RegExp` nhận được một string không có dấu `\`. Đó là lý do việc tìm kiếm không hoạt động!

Để sửa, chúng ta cần kép đôi các dấu `\`, vì dấu nháy của string biến `\\` thành `\`:

```
let regStr = "\\d\\.\\d";
alert(regStr); // \d\.\d (đúng rồi)

let regexp = new RegExp(regStr);

alert( "Chapter 5.1".match(regexp) ); // 5.1
```

## [Tóm tắt](#summary)

- Để tìm các ký tự đặc biệt `[ \ ^ $ . | ? * + (` một cách chính xác, chúng ta cần thêm dấu `\` phía trước (“escape” chúng).
- Chúng ta cũng cần escape `/` nếu ở bên trong `/.../` (nhưng không cần trong `new RegExp`).
- Khi truyền string cho `new RegExp`, chúng ta cần kép đôi các dấu `\\`, vì dấu nháy của string tiêu thụ một trong số chúng.
