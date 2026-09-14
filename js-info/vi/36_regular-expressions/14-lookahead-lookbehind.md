# Lookahead và lookbehind

> Source: [https://javascript.info/regexp-lookahead-lookbehind](https://javascript.info/regexp-lookahead-lookbehind)

<!-- fetched: 2026-09-14 -->

Đôi khi ta cần tìm chỉ những kết quả khớp của một pattern có đi sau hoặc đi trước bởi một pattern khác.

Có một cú pháp đặc biệt cho điều đó, được gọi là “lookahead” và “lookbehind”, chung thường được gọi là “lookaround”.

Để bắt đầu, hãy tìm giá trị tiền tệ từ một chuỗi như `1 turkey costs 30€`. Nghĩa là: một số, đi trước bởi dấu `€`.

## [Lookahead](#lookahead)

Cú pháp là: `X(?=Y)`, nó có nghĩa “tìm `X`, nhưng chỉ khớp nếu đi sau bởi `Y`”. `X` và `Y` có thể là bất kỳ pattern nào.

Với một số nguyên đi trước bởi `€`, regexp sẽ là `\d+(?=€)`:

```
let str = "1 turkey costs 30€";

alert( str.match(/\d+(?=€)/) ); // 30, the number 1 is ignored, as it's not followed by €
```

Lưu ý: lookahead chỉ đơn thuần là một phép thử, nội dung trong dấu ngoặc `(?=...)` không được đưa vào kết quả `30`.

Khi ta tìm `X(?=Y)`, engine regular expression tìm `X` rồi kiểm tra xem ngay sau nó có `Y` không. Nếu không, thì kết quả khớp tiềm năng bị bỏ qua, và việc tìm kiếm tiếp tục.

Các phép thử phức tạp hơn là có thể, ví dụ `X(?=Y)(?=Z)` có nghĩa:

1. Tìm `X`.
2. Kiểm tra xem ngay sau `X` có `Y` không (bỏ qua nếu không).
3. Kiểm tra xem ngay sau `X` cũng có `Z` không (bỏ qua nếu không).
4. Nếu cả hai phép thử đều thành công, thì `X` là một kết quả khớp, nếu không thì tiếp tục tìm kiếm.

Nói cách khác, pattern như vậy có nghĩa là ta đang tìm `X` đi sau bởi cả `Y` lẫn `Z` cùng lúc.

Điều đó chỉ có thể nếu các pattern `Y` và `Z` không loại trừ nhau.

Ví dụ, `\d+(?=\s)(?=.*30)` tìm `\d+` đi sau bởi khoảng trắng `(?=\s)`, và có `30` ở đâu đó sau nó `(?=.*30)`:

```
let str = "1 turkey costs 30€";

alert( str.match(/\d+(?=\s)(?=.*30)/) ); // 1
```

Trong chuỗi của ta, điều đó khớp đúng với số `1`.

## [Negative lookahead](#negative-lookahead)

Giả sử ta muốn lấy số lượng thay vì giá trị tiền tệ từ cùng một chuỗi. Đó là một số `\d+`, KHÔNG đi trước bởi `€`.

Để làm điều đó, có thể áp dụng negative lookahead.

Cú pháp là: `X(?!Y)`, nó có nghĩa “tìm `X`, nhưng chỉ khi không đi trước bởi `Y`”.

```
let str = "2 turkeys cost 60€";

alert( str.match(/\d+\b(?!€)/g) ); // 2 (the price is not matched)
```

## [Lookbehind](#lookbehind)

Tương thích trình duyệt của Lookbehind

Lưu ý: Lookbehind không được hỗ trợ trong các trình duyệt không phải V8, như Safari, Internet Explorer.

Lookahead cho phép thêm một điều kiện cho “thứ đi sau”.

Lookbehind tương tự, nhưng nó nhìn về phía sau. Nghĩa là, nó cho phép khớp một pattern chỉ nếu có gì đó đi trước nó.

Cú pháp là:

- Positive lookbehind: `(?<=Y)X`, khớp `X`, nhưng chỉ nếu có `Y` đi trước.
- Negative lookbehind: `(?<!Y)X`, khớp `X`, nhưng chỉ nếu không có `Y` đi trước.

Ví dụ, hãy đổi tiền tệ sang đô la Mỹ. Ký hiệu đô la thường đi trước số, nên để tìm `$30` ta sẽ dùng `(?<=\$)\d+` – một số tiền đi trước bởi `$`:

```
let str = "1 turkey costs $30";

// the dollar sign is escaped \$
alert( str.match(/(?<=\$)\d+/) ); // 30 (skipped the sole number)
```

Và nếu ta cần số lượng – một số không đi trước bởi `$`, thì ta có thể dùng negative lookbehind `(?<!\$)\d+`:

```
let str = "2 turkeys cost $60";

alert( str.match(/(?<!\$)\b\d+/g) ); // 2 (the price is not matched)
```

## [Capturing group](#capturing-groups)

Nhìn chung, nội dung bên trong dấu ngoặc lookaround không trở thành một phần của kết quả.

Ví dụ, trong pattern `\d+(?=€)`, dấu `€` không được capture làm một phần của kết quả khớp. Điều đó là tự nhiên: ta tìm một số `\d+`, trong khi `(?=€)` chỉ là một phép thử rằng nó phải đi trước bởi `€`.

Nhưng trong một số tình huống ta có thể muốn capture cả biểu thức lookaround, hoặc một phần của nó. Điều đó là có thể. Chỉ cần bọc phần đó vào thêm dấu ngoặc đơn.

Trong ví dụ bên dưới, ký hiệu tiền tệ `(€|kr)` được capture, cùng với số tiền:

```
let str = "1 turkey costs 30€";
let regexp = /\d+(?=(€|kr))/; // extra parentheses around €|kr

alert( str.match(regexp) ); // 30, €
```

Và đây là tương tự cho lookbehind:

```
let str = "1 turkey costs $30";
let regexp = /(?<=(\$|£))\d+/;

alert( str.match(regexp) ); // 30, $
```

## [Tóm tắt](#summary)

Lookahead và lookbehind (thường gọi chung là “lookaround”) hữu ích khi ta muốn khớp thứ gì đó tùy thuộc vào ngữ cảnh trước/sau nó.

Với các regexp đơn giản, ta có thể làm tương tự một cách thủ công. Nghĩa là: khớp mọi thứ, trong mọi ngữ cảnh, rồi lọc theo ngữ cảnh trong vòng lặp.

Hãy nhớ, `str.match` (không có flag `g`) và `str.matchAll` (luôn luôn) trả về các kết quả khớp dưới dạng mảng có thuộc tính `index`, nên ta biết chính xác vị trí trong văn bản, và có thể kiểm tra ngữ cảnh.

Nhưng nhìn chung lookaround tiện lợi hơn.

Các loại lookaround:

| Pattern | type | matches |
| --- | --- | --- |
| `X(?=Y)` | Positive lookahead | `X` if followed by `Y` |
| `X(?!Y)` | Negative lookahead | `X` if not followed by `Y` |
| `(?<=Y)X` | Positive lookbehind | `X` if after `Y` |
| `(?<!Y)X` | Negative lookbehind | `X` if not after `Y` |

---

---

## Bài tập

## [Bài tập](#tasks)

### [Tìm số nguyên không âm](#find-non-negative-integers)

Có một chuỗi các số nguyên.

Tạo một regexp chỉ tìm các số không âm (cho phép không).

Một ví dụ sử dụng:

```
let regexp = /your regexp/g;

let str = "0 12 -5 123 -18";

alert( str.match(regexp) ); // 0, 12, 123
```

solution

Regexp cho một số nguyên là `\d+`.

Ta có thể loại trừ các số âm bằng cách thêm negative lookbehind vào trước: `(?<!-)\d+`.

Tuy nhiên, nếu thử ngay bây giờ, ta có thể nhận ra thêm một kết quả “thừa”:

```
let regexp = /(?<!-)\d+/g;

let str = "0 12 -5 123 -18";

console.log( str.match(regexp) ); // 0, 12, 123, 8
```

Như bạn thấy, nó khớp `8`, từ `-18`. Để loại trừ nó, ta cần đảm bảo rằng regexp bắt đầu khớp một số không phải từ giữa một số khác (không khớp).

Ta có thể làm điều đó bằng cách chỉ định thêm một negative lookbehind: `(?<!-)(?<!\d)\d+`. Bây giờ `(?<!\d)` đảm bảo rằng kết quả khớp không bắt đầu sau một chữ số khác, đúng thứ ta cần.

Ta cũng có thể ghép chúng thành một lookbehind duy nhất ở đây:

```
let regexp = /(?<![-\d])\d+/g;

let str = "0 12 -5 123 -18";

alert( str.match(regexp) ); // 0, 12, 123
```

### [Chèn sau Head](#insert-after-head)

Ta có một chuỗi chứa một tài liệu HTML.

Viết một regular expression chèn `<h1>Hello</h1>` ngay sau tag `<body>`. Tag có thể có thuộc tính.

Ví dụ:

```
let regexp = /your regular expression/;

let str = `
<html>
  <body style="height: 200px">
  ...
  </body>
</html>
`;

str = str.replace(regexp, `<h1>Hello</h1>`);
```

Sau đó giá trị của `str` phải là:

```
<html>
  <body style="height: 200px"><h1>Hello</h1>
  ...
  </body>
</html>
```

solution

Để chèn sau tag `<body>`, trước hết ta phải tìm nó. Ta có thể dùng pattern regular expression `<body.*?>` cho việc đó.

Trong bài toán này, ta không cần sửa đổi tag `<body>`. Ta chỉ cần thêm văn bản sau nó.

Đây là cách ta có thể làm:

```
let str = '...<body style="...">...';
str = str.replace(/<body.*?>/, '$&<h1>Hello</h1>');

alert(str); // ...<body style="..."><h1>Hello</h1>...
```

Trong chuỗi thay thế, `$&` có nghĩa là chính kết quả khớp, tức là phần văn bản nguồn tương ứng với `<body.*?>`. Nó được thay thế bằng chính nó cộng thêm `<h1>Hello</h1>`.

Một phương án thay thế là dùng lookbehind:

```
let str = '...<body style="...">...';
str = str.replace(/(?<=<body.*?>)/, `<h1>Hello</h1>`);

alert(str); // ...<body style="..."><h1>Hello</h1>...
```

Như bạn thấy, trong regexp này chỉ có phần lookbehind.

Nó hoạt động như thế này:

- Tại mỗi vị trí trong văn bản.
- Kiểm tra xem nó có đi trước bởi `<body.*?>` không.
- Nếu đúng, thì ta có kết quả khớp.

Tag `<body.*?>` sẽ không được trả về. Kết quả của regexp này về mặt kỹ thuật là một chuỗi rỗng, nhưng nó chỉ khớp tại các vị trí đi trước bởi `<body.*?>`.

Vậy nó thay thế “dòng rỗng” đi trước bởi `<body.*?>` bằng `<h1>Hello</h1>`. Đó chính là việc chèn sau `<body>`.

P.S. Các flag regexp, như `s` và `i` cũng có thể hữu ích: `/<body.*?>/si`. Flag `s` làm cho dấu chấm `.` khớp ký tự xuống dòng, và flag `i` làm cho `<body>` cũng khớp `<BODY>` không phân biệt hoa thường.
