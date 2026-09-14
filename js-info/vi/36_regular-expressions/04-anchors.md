# Anchor: đầu string ^ và cuối $

> Source: [https://javascript.info/regexp-anchors](https://javascript.info/regexp-anchors)

<!-- fetched: 2026-09-14 -->

Ký tự dấu `^` và `$` có ý nghĩa đặc biệt trong regexp. Chúng được gọi là “anchor”.

Dấu `^` match ở đầu văn bản, và `$` – ở cuối.

Ví dụ, hãy kiểm tra xem văn bản có bắt đầu bằng `Mary` không:

```
let str1 = "Mary had a little lamb";
alert( /^Mary/.test(str1) ); // true
```

Pattern `^Mary` có nghĩa là: “đầu string rồi đến Mary”.

Tương tự, chúng ta có thể kiểm tra xem string có kết thúc bằng `snow` bằng cách dùng `snow$`:

```
let str1 = "its fleece was white as snow";
alert( /snow$/.test(str1) ); // true
```

Trong những trường hợp cụ thể này, chúng ta có thể dùng các method `startsWith/endsWith` của string thay thế. Regular expression nên được dùng cho các kiểm tra phức tạp hơn.

## [Kiểm tra match toàn bộ](#testing-for-a-full-match)

Cả hai anchor kết hợp `^...$` thường được dùng để kiểm tra xem string có match hoàn toàn với pattern hay không. Ví dụ, để kiểm tra xem đầu vào của người dùng có đúng định dạng không.

Hãy kiểm tra xem một string có phải là thời gian ở định dạng `12:34` không. Tức là: hai chữ số, rồi một dấu hai chấm, rồi hai chữ số nữa.

Trong ngôn ngữ regular expression, đó là `\d\d:\d\d`:

```
let goodInput = "12:34";
let badInput = "12:345";

let regexp = /^\d\d:\d\d$/;
alert( regexp.test(goodInput) ); // true
alert( regexp.test(badInput) ); // false
```

Ở đây, match của `\d\d:\d\d` phải bắt đầu đúng ngay sau đầu văn bản `^`, và cuối `$` phải đến ngay sau đó.

Toàn bộ string phải đúng định dạng này. Nếu có sai lệch hay thừa thêm ký tự nào, kết quả là `false`.

Anchor hoạt động khác khi có flag `m`. Chúng ta sẽ thấy điều đó trong bài viết tiếp theo.

Anchor có “chiều rộng bằng zero”

Các anchor `^` và `$` là những phép thử. Chúng có chiều rộng bằng zero.

Nói cách khác, chúng không match ký tự, mà bắt bộ máy regexp kiểm tra điều kiện (đầu/cuối văn bản).

---

---

## Bài tập

## [Bài tập](#tasks)

### [Regexp ^$](#regexp)

String nào match pattern `^$`?

đáp án

String rỗng là match duy nhất: nó bắt đầu và kết thúc ngay lập tức.

Bài tập này một lần nữa cho thấy anchor không phải là ký tự, mà là các phép thử.

String là rỗng `""`. Bộ máy trước tiên match `^` (đầu input), có, rồi ngay lập tức đến cuối `$`, cũng có. Vậy nên có match.
