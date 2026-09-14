# Alternation (OR) |

> Source: [https://javascript.info/regexp-alternation](https://javascript.info/regexp-alternation)

<!-- fetched: 2026-09-14 -->

Alternation là thuật ngữ trong regular expression thực ra chỉ đơn giản là “OR”.

Trong regular expression nó được ký hiệu bằng ký tự đường thẳng đứng `|`.

Ví dụ, ta cần tìm các ngôn ngữ lập trình: HTML, PHP, Java hoặc JavaScript.

Regexp tương ứng: `html|php|java(script)?`.

Một ví dụ sử dụng:

```
let regexp = /html|php|css|java(script)?/gi;

let str = "First HTML appeared, then CSS, then JavaScript";

alert( str.match(regexp) ); // 'HTML', 'CSS', 'JavaScript'
```

Ta đã từng thấy một thứ tương tự – dấu ngoặc vuông. Chúng cho phép chọn giữa nhiều ký tự, ví dụ `gr[ae]y` khớp `gray` hoặc `grey`.

Dấu ngoặc vuông chỉ cho phép các ký tự hoặc lớp ký tự. Alternation cho phép bất kỳ biểu thức nào. Một regexp `A|B|C` có nghĩa là một trong các biểu thức `A`, `B` hoặc `C`.

Ví dụ:

- `gr(a|e)y` có nghĩa giống hệt `gr[ae]y`.
- `gra|ey` có nghĩa là `gra` hoặc `ey`.

Để áp dụng alternation cho một phần pattern chọn lọc, ta có thể bọc nó trong dấu ngoặc đơn:

- `I love HTML|CSS` khớp `I love HTML` hoặc `CSS`.
- `I love (HTML|CSS)` khớp `I love HTML` hoặc `I love CSS`.

## [Ví dụ: regexp cho thời gian](#example-regexp-for-time)

Trong các bài trước có một bài toán xây dựng regexp để tìm thời gian ở dạng `hh:mm`, ví dụ `12:00`. Nhưng một `\d\d:\d\d` đơn giản quá mơ hồ. Nó chấp nhận `25:99` như thời gian (vì 99 phút khớp pattern, nhưng thời điểm đó không hợp lệ).

Làm thế nào để tạo một pattern tốt hơn?

Ta có thể dùng khớp chính xác hơn. Trước hết, số giờ:

- Nếu chữ số đầu là `0` hoặc `1`, thì chữ số tiếp theo có thể là bất kỳ: `[01]\d`.
- Ngược lại, nếu chữ số đầu là `2`, thì chữ số tiếp theo phải là `[0-3]`.
- (không chấp nhận chữ số đầu nào khác)

Ta có thể viết cả hai biến thể trong một regexp dùng alternation: `[01]\d|2[0-3]`.

Tiếp theo, phút phải từ `00` đến `59`. Trong ngôn ngữ regular expression, điều đó có thể viết là `[0-5]\d`: chữ số đầu `0-5`, rồi bất kỳ chữ số nào.

Nếu ta ghép giờ và phút lại, ta được pattern: `[01]\d|2[0-3]:[0-5]\d`.

Ta gần xong, nhưng có một vấn đề. Alternation `|` bây giờ nằm giữa `[01]\d` và `2[0-3]:[0-5]\d`.

Nghĩa là: phút được thêm vào biến thể thứ hai của alternation, đây là hình ảnh rõ ràng:

```
[01]\d  |  2[0-3]:[0-5]\d
```

Pattern đó tìm `[01]\d` hoặc `2[0-3]:[0-5]\d`.

Nhưng điều đó sai, alternation nên chỉ được dùng trong phần “giờ” của regular expression, để cho phép `[01]\d` HOẶC `2[0-3]`. Hãy sửa bằng cách bọc “giờ” trong dấu ngoặc đơn: `([01]\d|2[0-3]):[0-5]\d`.

Giải pháp cuối cùng:

```
let regexp = /([01]\d|2[0-3]):[0-5]\d/g;

alert("00:00 10:10 23:59 25:99 1:2".match(regexp)); // 00:00,10:10,23:59
```

---

---

## Bài tập

## [Bài tập](#tasks)

### [Tìm ngôn ngữ lập trình](#find-programming-languages)

Có rất nhiều ngôn ngữ lập trình, ví dụ Java, JavaScript, PHP, C, C++.

Tạo một regexp tìm chúng trong chuỗi `Java JavaScript PHP C++ C`:

```
let regexp = /your regexp/g;

alert("Java JavaScript PHP C++ C".match(regexp)); // Java JavaScript PHP C++ C
```

solution

Ý tưởng đầu tiên có thể là liệt kê các ngôn ngữ với `|` ở giữa.

Nhưng điều đó không hoạt động đúng:

```
let regexp = /Java|JavaScript|PHP|C|C\+\+/g;

let str = "Java, JavaScript, PHP, C, C++";

alert( str.match(regexp) ); // Java,Java,PHP,C,C
```

Engine regular expression tìm kiếm các alternation lần lượt. Nghĩa là: trước hết nó kiểm tra có `Java` không, nếu không – thì tìm `JavaScript` và cứ thế.

Kết quả là, `JavaScript` không bao giờ được tìm thấy, chỉ vì `Java` được kiểm tra trước.

Tương tự với `C` và `C++`.

Có hai giải pháp cho vấn đề đó:

1. Đổi thứ tự để kiểm tra kết quả khớp dài hơn trước: `JavaScript|Java|C\+\+|C|PHP`.
2. Hợp nhất các biến thể cùng đầu: `Java(Script)?|C(\+\+)?|PHP`.

Trong thực tế:

```
let regexp = /Java(Script)?|C(\+\+)?|PHP/g;

let str = "Java, JavaScript, PHP, C, C++";

alert( str.match(regexp) ); // Java,JavaScript,PHP,C,C++
```

### [Tìm cặp bbtag](#find-bbtag-pairs)

Một “bb-tag” có dạng `[tag]...[/tag]`, trong đó `tag` là một trong: `b`, `url` hoặc `quote`.

Ví dụ:

```
[b]text[/b]
[url]http://google.com[/url]
```

Các BB-tag có thể lồng nhau. Nhưng một tag không thể lồng chính nó, ví dụ:

```
Normal:
[url] [b]http://google.com[/b] [/url]
[quote] [b]text[/b] [/quote]

Can't happen:
[b][b]text[/b][/b]
```

Tags có thể chứa ký tự xuống dòng, điều đó là bình thường:

```
[quote]
  [b]text[/b]
[/quote]
```

Tạo một regexp để tìm tất cả các BB-tag với nội dung của chúng.

Ví dụ:

```
let regexp = /your regexp/flags;

let str = "..[url]http://google.com[/url]..";
alert( str.match(regexp) ); // [url]http://google.com[/url]
```

Nếu các tag lồng nhau, thì ta cần tag ngoài (nếu muốn ta có thể tiếp tục tìm kiếm trong nội dung của nó):

```
let regexp = /your regexp/flags;

let str = "..[url][b]http://google.com[/b][/url]..";
alert( str.match(regexp) ); // [url][b]http://google.com[/b][/url]
```

solution

Tag mở là `\[(b|url|quote)]`.

Rồi để tìm mọi thứ cho đến tag đóng – hãy dùng pattern `.*?` với flag `s` để khớp bất kỳ ký tự nào kể cả ký tự xuống dòng, rồi thêm một backreference cho tag đóng.

Pattern đầy đủ: `\[(b|url|quote)\].*?\[/\1]`.

Trong thực tế:

```
let regexp = /\[(b|url|quote)].*?\[\/\1]/gs;

let str = `
  [b]hello![/b]
  [quote]
    [url]http://google.com[/url]
  [/quote]
`;

alert( str.match(regexp) ); // [b]hello![/b],[quote][url]http://google.com[/url][/quote]
```

Lưu ý rằng ngoài việc escape `[`, ta còn phải escape dấu gạch chéo cho tag đóng `[\/\1]`, vì bình thường dấu gạch chéo đóng pattern.

### [Tìm chuỗi có dấu nháy](#find-quoted-strings)

Tạo một regexp để tìm các chuỗi trong dấu nháy đôi `"..."`.

Các chuỗi phải hỗ trợ escape, giống hệt cách các chuỗi JavaScript làm. Ví dụ, dấu nháy có thể được chèn như `\"`, ký tự xuống dòng như `\n`, và chính backslash như `\\`.

```
let str = "Just like \"here\".";
```

Hãy lưu ý, đặc biệt là, rằng một dấu nháy được escape `\"` không kết thúc chuỗi.

Vậy ta nên tìm từ dấu nháy này đến dấu nháy kia, bỏ qua các dấu nháy được escape trên đường đi.

Đó là phần cốt lõi của bài toán, nếu không thì nó sẽ tầm thường.

Các ví dụ chuỗi cần khớp:

```
.. "test me" ..
.. "Say \"Hello\"!" ... (escaped quotes inside)
.. "\\" ..  (double backslash inside)
.. "\\ \"" ..  (double backslash and an escaped quote inside)
```

Trong JavaScript ta cần gấp đôi các backslash để truyền chúng đúng vào chuỗi, như thế này:

```
let str = ' .. "test me" .. "Say \\"Hello\\"!" .. "\\\\ \\"" .. ';

// the in-memory string
alert(str); //  .. "test me" .. "Say \"Hello\"!" .. "\\ \"" ..
```

solution

Giải pháp: `/"(\\.|[^"\\])*"/g`.

Từng bước:

- Đầu tiên ta tìm dấu nháy mở `"`
- Rồi nếu có backslash `\\` (ta phải gấp đôi nó trong pattern vì đó là ký tự đặc biệt), thì bất kỳ ký tự nào sau nó đều được (dấu chấm).
- Nếu không, ta lấy bất kỳ ký tự nào ngoại trừ dấu nháy (điều đó có nghĩa là kết thúc chuỗi) và backslash (để ngăn các backslash đơn lẻ, backslash chỉ được dùng cùng với một ký hiệu khác sau nó): `[^"\\]`
- …Và cứ thế cho đến dấu nháy đóng.

Trong thực tế:

```
let regexp = /"(\\.|[^"\\])*"/g;
let str = ' .. "test me" .. "Say \\"Hello\\"!" .. "\\\\ \\"" .. ';

alert( str.match(regexp) ); // "test me","Say \"Hello\"!","\\ \""
```

### [Tìm tag đầy đủ](#find-the-full-tag)

Viết một regexp tìm tag `<style...>`. Nó phải khớp tag đầy đủ: có thể không có thuộc tính `<style>` hoặc có nhiều thuộc tính `<style type="..." id="...">`.

…Nhưng regexp không được khớp `<styler>`!

Ví dụ:

```
let regexp = /your regexp/g;

alert( '<style> <styler> <style test="...">'.match(regexp) ); // <style>, <style test="...">
```

solution

Đầu pattern rõ ràng: `<style`.

…Nhưng sau đó ta không thể đơn giản viết `<style.*?>`, vì `<styler>` sẽ khớp nó.

Ta cần một khoảng trắng sau `<style` rồi một số thứ tùy chọn, hoặc dấu đóng `>`.

Trong ngôn ngữ regexp: `<style(>|\s.*?>)`.

Trong thực tế:

```
let regexp = /<style(>|\s.*?>)/g;

alert( '<style> <styler> <style test="...">'.match(regexp) ); // <style>, <style test="...">
```
