# Quantifier +, *, ? và {n}

> Source: [https://javascript.info/regexp-quantifiers](https://javascript.info/regexp-quantifiers)

<!-- fetched: 2026-09-14 -->

Giả sử chúng ta có một string như `+7(903)-123-45-67` và muốn tìm tất cả các số trong đó. Nhưng khác với trước đây, chúng ta quan tâm không phải từng chữ số đơn lẻ, mà là số hoàn chỉnh: `7, 903, 123, 45, 67`.

Một số là chuỗi gồm 1 hoặc nhiều chữ số `\d`. Để chỉ định cần bao nhiêu, chúng ta có thể thêm một *quantifier*.

## [Số lượng {n}](#quantity-n)

Quantifier đơn giản nhất là một số trong dấu ngoặc nhọn: `{n}`.

Quantifier được thêm vào một ký tự (hoặc character class, hoặc `[...]` set, v.v.) và chỉ định chúng ta cần bao nhiêu.

Nó có một số dạng nâng cao, hãy xem các ví dụ:

Số chính xác: `{5}`
:   `\d{5}` chỉ đúng 5 chữ số, giống `\d\d\d\d\d`.

    Ví dụ bên dưới tìm một số có 5 chữ số:

    ```
    alert( "I'm 12345 years old".match(/\d{5}/) ); //  "12345"
    ```

    Chúng ta có thể thêm `\b` để loại trừ các số dài hơn: `\b\d{5}\b`.

Khoảng: `{3,5}`, match 3-5 lần
:   Để tìm các số có từ 3 đến 5 chữ số, chúng ta có thể đặt giới hạn trong dấu ngoặc nhọn: `\d{3,5}`

    ```
    alert( "I'm not 12, but 1234 years old".match(/\d{3,5}/) ); // "1234"
    ```

    Chúng ta có thể bỏ qua giới hạn trên.

    Khi đó regexp `\d{3,}` tìm các chuỗi chữ số có độ dài từ `3` trở lên:

    ```
    alert( "I'm not 12, but 345678 years old".match(/\d{3,}/) ); // "345678"
    ```

Hãy quay lại string `+7(903)-123-45-67`.

Một số là chuỗi gồm một hoặc nhiều chữ số liền nhau. Vậy regexp là `\d{1,}`:

```
let str = "+7(903)-123-45-67";

let numbers = str.match(/\d{1,}/g);

alert(numbers); // 7,903,123,45,67
```

## [Cách viết tắt](#shorthands)

Có các cách viết tắt cho các quantifier được dùng nhiều nhất:

`+`
:   Có nghĩa “một hoặc nhiều”, giống `{1,}`.

    Ví dụ, `\d+` tìm các số:

    ```
    let str = "+7(903)-123-45-67";

    alert( str.match(/\d+/g) ); // 7,903,123,45,67
    ```

`?`
:   Có nghĩa “zero hoặc một”, giống `{0,1}`. Nói cách khác, nó làm ký trở nên tùy chọn.

    Ví dụ, pattern `ou?r` tìm `o` theo sau bởi zero hoặc một `u`, rồi đến `r`.

    Vậy, `colou?r` tìm cả `color` và `colour`:

    ```
    let str = "Should I write color or colour?";

    alert( str.match(/colou?r/g) ); // color, colour
    ```

`*`
:   Có nghĩa “zero hoặc nhiều”, giống `{0,}`. Tức là, ký tự có thể lặp lại bất kỳ lần nào hoặc không có.

    Ví dụ, `\d0*` tìm một chữ số theo sau bởi bất kỳ số lượng số nào (có thể nhiều hoặc không có):

    ```
    alert( "100 10 1".match(/\d0*/g) ); // 100, 10, 1
    ```

    So sánh với `+` (một hoặc nhiều):

    ```
    alert( "100 10 1".match(/\d0+/g) ); // 100, 10
    // 1 không match, vì 0+ yêu cầu ít nhất một số
    ```

## [Thêm ví dụ](#more-examples)

Quantifier được dùng rất thường xuyên. Chúng đóng vai trò là “đòn bẩy” chính của các regular expression phức tạp, vậy nên hãy xem thêm các ví dụ.

**Regexp cho phân số thập phân (số có dấu phẩy động): `\d+\.\d+`**

Trong thực tế:

```
alert( "0 1 12.345 7890".match(/\d+\.\d+/g) ); // 12.345
```

**Regexp cho “thẻ HTML mở không có thuộc tính”, như `<span>` hay `<p>`.**

1. Đơn giản nhất: `/<[a-z]+>/i`

    ```
    alert( "<body> ... </body>".match(/<[a-z]+>/gi) ); // <body>
    ```

    Regexp tìm ký tự `'<'` theo sau bởi một hoặc nhiều chữ cái Latin, rồi đến `'>'`.
2. Cải tiến: `/<[a-z][a-z0-9]*>/i`

    Theo chuẩn, tên thẻ HTML có thể có chữ số ở bất kỳ vị trí nào ngoại trừ vị trí đầu tiên, như `<h1>`.

    ```
    alert( "<h1>Hi!</h1>".match(/<[a-z][a-z0-9]*>/gi) ); // <h1>
    ```

**Regexp “thẻ HTML mở hoặc đóng không có thuộc tính”: `/<\/?[a-z][a-z0-9]*>/i`**

Chúng ta đã thêm dấu gạch chéo tùy chọn `/?` gần đầu pattern. Phải escape nó bằng dấu `\`, nếu không JavaScript sẽ coi đó là kết thúc pattern.

```
alert( "<h1>Hi!</h1>".match(/<\/?[a-z][a-z0-9]*>/gi) ); // <h1>, </h1>
```

Để regexp chính xác hơn, thường chúng ta cần làm nó phức tạp hơn

Chúng ta có thể thấy một quy tắc chung trong các ví dụ này: regular expression càng chính xác – càng dài và phức tạp.

Ví dụ, với thẻ HTML chúng ta có thể dùng regexp đơn giản hơn: `<\w+>`. Nhưng vì HTML có các giới hạn chặt chẽ hơn cho tên thẻ, `<[a-z][a-z0-9]*>` đáng tin cậy hơn.

Chúng ta có thể dùng `<\w+>` hay cần `<[a-z][a-z0-9]*>`?

Trong thực tế cả hai cách đều chấp nhận được. Tùy thuộc vào việc chúng ta có thể bao dung đến mức nào với các match “thừa” và việc loại chúng khỏi kết quả bằng cách khác có khó hay không.

---

---

## Bài tập

## [Bài tập](#tasks)

### [Làm thế nào để tìm dấu "..." ?](#how-to-find-an-ellipsis)

importance: 5

Tạo một regexp để tìm dấu ba chấm: 3 (hay nhiều hơn?) dấu chấm liền nhau.

Kiểm tra:

```
let regexp = /regexp của bạn/g;
alert( "Hello!... How goes?.....".match(regexp) ); // ..., .....
```

đáp án

Giải pháp:

```
let regexp = /\.{3,}/g;
alert( "Hello!... How goes?.....".match(regexp) ); // ..., .....
```

Lưu ý rằng dấu chấm là ký tự đặc biệt, nên chúng ta phải escape nó và chèn dưới dạng `\.`.

### [Regexp cho màu HTML](#regexp-for-html-colors)

Tạo một regexp để tìm các màu HTML được viết dạng `#ABCDEF`: đầu tiên `#` rồi theo sau là 6 ký tự hex.

Ví dụ sử dụng:

```
let regexp = /...regexp của bạn.../

let str = "color:#121212; background-color:#AA00ef bad-colors:f#fddee #fd2 #12345678";

alert( str.match(regexp) )  // #121212,#AA00ef
```

P.S. Trong bài tập này chúng ta không cần các định dạng màu khác như `#123` hay `rgb(1,2,3)` v.v.

đáp án

Chúng ta cần tìm `#` theo sau bởi 6 ký tự hex.

Một ký tự hex có thể được mô tả là `[0-9a-fA-F]`. Hoặc nếu dùng flag `i`, thì chỉ cần `[0-9a-f]`.

Rồi chúng ta có thể tìm 6 ký tự như vậy bằng quantifier `{6}`.

Kết quả, chúng ta có regexp: `/#[a-f0-9]{6}/gi`.

```
let regexp = /#[a-f0-9]{6}/gi;

let str = "color:#121212; background-color:#AA00ef bad-colors:f#fddee #fd2"

alert( str.match(regexp) );  // #121212,#AA00ef
```

Vấn đề là nó tìm thấy màu trong các chuỗi dài hơn:

```
alert( "#12345678".match( /#[a-f0-9]{6}/gi ) ) // #123456
```

Để sửa, chúng ta có thể thêm `\b` vào cuối:

```
// màu
alert( "#123456".match( /#[a-f0-9]{6}\b/gi ) ); // #123456

// không phải màu
alert( "#12345678".match( /#[a-f0-9]{6}\b/gi ) ); // null
```
