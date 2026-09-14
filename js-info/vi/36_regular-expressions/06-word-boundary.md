# Word boundary (ranh giới từ): \b

> Source: [https://javascript.info/regexp-boundary](https://javascript.info/regexp-boundary)

<!-- fetched: 2026-09-14 -->

Word boundary `\b` là một phép thử, giống như `^` và `$`.

Khi bộ máy regexp (module chương trình thực hiện tìm kiếm cho regexp) gặp `\b`, nó kiểm tra xem vị trí trong string có phải là word boundary không.

Có ba vị trí khác nhau được xem là word boundary:

- Ở đầu string, nếu ký tự đầu tiên của string là ký tự thuộc word `\w`.
- Giữa hai ký tự trong string, trong đó một bên là ký tự thuộc word `\w` và bên kia không phải.
- Ở cuối string, nếu ký tự cuối cùng của string là ký tự thuộc word `\w`.

Ví dụ, regexp `\bJava\b` sẽ được tìm thấy trong `Hello, Java!`, nơi `Java` là một từ độc lập, nhưng không có trong `Hello, JavaScript!`.

```
alert( "Hello, Java!".match(/\bJava\b/) ); // Java
alert( "Hello, JavaScript!".match(/\bJava\b/) ); // null
```

Trong string `Hello, Java!`, các vị trí sau tương ứng với `\b`:

![](/article/regexp-boundary/hello-java-boundaries.svg)

Vậy, nó match pattern `\bHello\b`, vì:

1. Ở đầu string match với phép thử đầu tiên `\b`.
2. Rồi match với từ `Hello`.
3. Rồi phép thử `\b` match lần nữa, vì chúng ta đang ở giữa `o` và dấu phẩy.

Vậy nên pattern `\bHello\b` sẽ match, nhưng không phải `\bHell\b` (vì không có word boundary sau `l`) và cũng không phải `Java!\b` (vì dấu than không phải ký tự thuộc word `\w`, nên không có word boundary sau nó).

```
alert( "Hello, Java!".match(/\bHello\b/) ); // Hello
alert( "Hello, Java!".match(/\bJava\b/) );  // Java
alert( "Hello, Java!".match(/\bHell\b/) );  // null (không match)
alert( "Hello, Java!".match(/\bJava!\b/) ); // null (không match)
```

Chúng ta có thể dùng `\b` không chỉ với từ mà còn với chữ số.

Ví dụ, pattern `\b\d\d\b` tìm các số có 2 chữ số độc lập. Nói cách khác, nó tìm các số 2 chữ số được bao quanh bởi các ký tự khác với `\w`, chẳng hạn như khoảng trắng hay dấu câu (hoặc đầu/cuối văn bản).

```
alert( "1 23 456 78".match(/\b\d\d\b/g) ); // 23,78
alert( "12,34,56".match(/\b\d\d\b/g) ); // 12,34,56
```

Word boundary `\b` không hoạt động với bảng chữ cái không phải Latin

Phép thử word boundary `\b` kiểm tra rằng một bên của vị trí phải có `\w` và “không phải `\w`” – ở bên kia.

Nhưng `\w` có nghĩa là chữ cái Latin `a-z` (hoặc chữ số hoặc dấu gạch dưới), nên phép thử không hoạt động với các ký tự khác, ví dụ như chữ cái Cyrillic hay hieroglyph.

---

---

## Bài tập

## [Bài tập](#tasks)

### [Tìm thời gian](#find-the-time)

Thời gian có định dạng: `giờ:phút`. Cả giờ và phút đều có hai chữ số, như `09:00`.

Tạo một regexp để tìm thời gian trong string: `Breakfast at 09:00 in the room 123:456.`

P.S. Trong bài tập này chưa cần kiểm tra tính đúng đắn của thời gian, nên `25:99` cũng có thể là kết quả hợp lệ.

P.P.S. Regexp không được match `123:456`.

đáp án

Đáp án: `\b\d\d:\d\d\b`.

```
alert( "Breakfast at 09:00 in the room 123:456.".match( /\b\d\d:\d\d\b/ ) ); // 09:00
```
