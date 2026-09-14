# Unicode, Nội bộ String

> Source: [https://javascript.info/unicode](https://javascript.info/unicode)

<!-- fetched: 2026-09-14 -->

Kiến thức chuyên sâu

Phần này đi sâu vào nội bộ string. Kiến thức này sẽ hữu ích cho bạn nếu bạn dự định xử lý emoji, các ký tự toán học hiếm hoặc hieroglyph, hoặc các ký tự hiếm khác.

Như chúng ta đã biết, các string JavaScript dựa trên [Unicode](https://en.wikipedia.org/wiki/Unicode): mỗi ký tự được biểu diễn bằng một chuỗi byte 1-4 byte.

JavaScript cho phép chúng ta chèn một ký tự vào string bằng cách chỉ định mã Unicode hexadecimal của nó với một trong ba ký hiệu sau:

- `\xXX`

  `XX` phải là hai chữ số hexadecimal với giá trị giữa `00` và `FF`, sau đó `\xXX` là ký tự có mã Unicode là `XX`.

  Vì ký hiệu `\xXX` chỉ hỗ trợ hai chữ số hexadecimal, nó chỉ có thể được sử dụng cho 256 ký tự Unicode đầu tiên.

  256 ký tự đầu tiên này bao gồm bảng chữ cái Latin, hầu hết các ký tự cú pháp cơ bản, và một số ký tự khác. Ví dụ, `"\x7A"` giống như `"z"` (Unicode `U+007A`).

  ```
  alert( "\x7A" ); // z
  alert( "\xA9" ); // ©, ký hiệu bản quyền
  ```
- `\uXXXX`
  `XXXX` phải chính xác là 4 chữ số hex với giá trị giữa `0000` và `FFFF`, sau đó `\uXXXX` là ký tự có mã Unicode là `XXXX`.

  Các ký tự có giá trị Unicode lớn hơn `U+FFFF` cũng có thể được biểu diễn bằng ký hiệu này, nhưng trong trường hợp đó, chúng ta sẽ cần sử dụng cặp surrogate (chúng ta sẽ nói về các cặp surrogate sau trong chương này).

  ```
  alert( "\u00A9" ); // ©, giống như \xA9, sử dụng ký hiệu 4 chữ số hex
  alert( "\u044F" ); // я, chữ cái bảng chữ cái Cyrillic
  alert( "\u2191" ); // ↑, ký hiệu mũi tên lên
  ```
- `\u{X…XXXXXX}`

  `X…XXXXXX` phải là một giá trị hexadecimal từ 1 đến 6 chữ số giữa `0` và `10FFFF` (mã điểm cao nhất được định nghĩa bởi Unicode). Ký hiệu này cho phép chúng ta dễ dàng biểu diễn tất cả các ký tự Unicode hiện có.

  ```
  alert( "\u{20331}" ); // 佫, một ký tự Trung Quốc hiếm (Unicode dài)
  alert( "\u{1F60D}" ); // 😍, ký hiệu mặt cười (Unicode dài khác)
  ```

## [Các cặp surrogate](#surrogate-pairs)

Tất cả các ký tự thường dùng có mã 2 byte (4 chữ số hex). Các chữ cái trong hầu hết các ngôn ngữ châu Âu, số, và các bộ ký tự CJK thống kê cơ bản (CJK – từ tiếng Trung, Nhật và Hàn), có biểu diễn 2 byte.

 ban đầu, JavaScript dựa trên encoding UTF-16 chỉ cho phép 2 byte mỗi ký tự. Nhưng 2 byte chỉ cho phép 65536 tổ hợp và điều đó không đủ cho mọi ký tự có thể có của Unicode.

Vì vậy các ký tự hiếm yêu cầu nhiều hơn 2 byte được mã hóa với một cặp 2 byte ký tự được gọi là "một cặp surrogate".

Như một side effect, độ dài của các ký tự như vậy là `2`:

```
alert( '𝒳'.length ); // 2, MATHEMATICAL SCRIPT CAPITAL X
alert( '😂'.length ); // 2, FACE WITH TEARS OF JOY
alert( '𩷶'.length ); // 2, một ký tự Trung Quốc hiếm
```

Điều đó là vì các cặp surrogate không tồn tại vào thời điểm JavaScript được tạo, và do đó không được xử lý đúng cách bởi ngôn ngữ!

Thực tế chúng ta có một ký tự duy nhất trong mỗi string ở trên, nhưng thuộc tính `length` hiển thị độ dài là `2`.

Nhận ký tự cũng có thể gây khó khăn, vì hầu hết các tính năng ngôn ngữ xử lý các cặp surrogate như hai ký tự.

Ví dụ, ở đây chúng ta có thể thấy hai ký tự kỳ lạ trong output:

```
alert( '𝒳'[0] ); // hiển thị các ký tự kỳ lạ...
alert( '𝒳'[1] ); // ...pieces của cặp surrogate
```

Các pieces của một cặp surrogate không có ý nghĩa khi không có nhau. Vì vậy các alert trong ví dụ ở trên thực sự hiển thị rác.

Về mặt kỹ thuật, các cặp surrogate cũng có thể được phát hiện bằng mã của chúng: nếu một ký tự có mã trong khoảng `0xd800..0xdbff`, thì đó là phần đầu tiên của cặp surrogate. Ký tự tiếp theo (phần thứ hai) phải có mã trong khoảng `0xdc00..0xdfff`. Các khoảng này được dành riêng exclusively cho các cặp surrogate theo tiêu chuẩn.

Vì vậy các phương thức [String.fromCodePoint](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/fromCodePoint) và [str.codePointAt](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/codePointAt) đã được thêm vào JavaScript để xử lý các cặp surrogate.

Chúng về cơ bản giống như [String.fromCharCode](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/fromCharCode) và [str.charCodeAt](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/charCodeAt), nhưng chúng xử lý các cặp surrogate một cách chính xác.

Một người có thể thấy sự khác biệt ở đây:

```
// charCodeAt không nhận biết surrogate-pair, vì vậy nó cho mã của phần 1 của 𝒳:

alert( '𝒳'.charCodeAt(0).toString(16) ); // d835

// codePointAt nhận biết surrogate-pair
alert( '𝒳'.codePointAt(0).toString(16) ); // 1d4b3, đọc cả hai phần của cặp surrogate
```

Tuy nhiên, nếu chúng ta lấy từ vị trí 1 (và điều đó khá sai ở đây), thì cả hai đều trả về chỉ phần thứ hai của cặp:

```
alert( '𝒳'.charCodeAt(1).toString(16) ); // dcb3
alert( '𝒳'.codePointAt(1).toString(16) ); // dcb3
// half thứ hai vô nghĩa của cặp
```

Bạn sẽ tìm thấy nhiều cách hơn để xử lý các cặp surrogate sau trong chương [Iterables](/iterable). Có lẽ có các thư viện đặc biệt cho điều đó, nhưng không có gì nổi tiếng enough để đề xuất ở đây.

Bài học: chia string tại một điểm tùy ý là nguy hiểm

Chúng ta không thể chỉ chia một string tại một vị trí tùy ý, ví dụ lấy `str.slice(0, 4)` và mong đợi nó là một string hợp lệ, ví dụ:

```
alert( 'hi 😂'.slice(0, 4) ); //  hi [?]
```

Ở đây chúng ta có thể thấy một ký tự rác (phần đầu tiên của surrogate pair smile) trong output.

Chỉ cần nhận thức về điều đó nếu bạn dự định làm việc đáng tin cậy với các cặp surrogate. Có thể không phải là vấn đề lớn, nhưng ít nhất bạn nên hiểu những gì đang xảy ra.

## [Các dấu phụ và chuẩn hóa](#diacritical-marks-and-normalization)

Trong nhiều ngôn ngữ, có các ký tự được cấu thành từ ký tự cơ bản với một dấu ở trên/dưới nó.

Ví dụ, chữ cái `a` có thể là ký tự cơ bản cho các ký tự: `àáâäãåā`.

Hầu hết các ký tự "composite" phổ biến có mã riêng trong bảng Unicode. Nhưng không phải tất cả, vì có quá nhiều tổ hợp có thể.

Để hỗ trợ các tổ hợp tùy ý, tiêu chuẩn Unicode cho phép chúng ta sử dụng nhiều ký tự Unicode: ký tự cơ bản theo sau bởi một hoặc nhiều ký tự "dấu" trang trí nó.

Ví dụ, nếu chúng ta có `S` theo sau là ký tự đặc biệt "dot above" (mã `\u0307`), nó được hiển thị là Ṡ.

```
alert( 'S\u0307' ); // Ṡ
```

Nếu chúng ta cần một dấu bổ sung trên chữ cái (hoặc dưới nó) – không có vấn đề, chỉ cần thêm ký tự dấu cần thiết.

Ví dụ, nếu chúng ta append một ký tự "dot below" (mã `\u0323`), thì chúng ta sẽ có "S với dots trên và dưới": `Ṩ`.

Ví dụ:

```
alert( 'S\u0307\u0323' ); // Ṩ
```

Điều này cung cấp flexibility lớn, nhưng cũng một vấn đề thú vị: hai ký tự có thể trông giống nhau về mặt trực quan, nhưng được biểu diễn với các composition Unicode khác nhau.

Ví dụ:

```
let s1 = 'S\u0307\u0323'; // Ṩ, S + dot above + dot below
let s2 = 'S\u0323\u0307'; // Ṩ, S + dot below + dot above

alert( `s1: ${s1}, s2: ${s2}` );

alert( s1 == s2 ); // false though the characters look identical (?!)
```

Để giải quyết điều này, tồn tại một thuật toán "chuẩn hóa Unicode" đưa mỗi string về một dạng "bình thường" duy nhất.

Nó được implement bởi [str.normalize()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/normalize).

```
alert( "S\u0307\u0323".normalize() == "S\u0323\u0307".normalize() ); // true
```

Thú vị là trong tình huống của chúng ta `normalize()` thực sự đưa một sequence của 3 ký tự thành một: `\u1e68` (S với hai dots).

```
alert( "S\u0307\u0323".normalize().length ); // 1

alert( "S\u0307\u0323".normalize() == "\u1e68" ); // true
```

Trong thực tế, điều đó không phải lúc nào cũng vậy. Lý do là ký tự `Ṩ` là "đủ phổ biến", vì vậy các nhà sáng tạo Unicode đã bao gồm nó trong bảng chính và cho nó mã.

Nếu bạn muốn tìm hiểu thêm về các quy tắc chuẩn hóa và các biến thể – chúng được mô tả trong phụ lục của tiêu chuẩn Unicode: [Unicode Normalization Forms](https://www.unicode.org/reports/tr15/), nhưng đối với hầu hết các mục đích thực tế thông tin từ phần này là đủ.
