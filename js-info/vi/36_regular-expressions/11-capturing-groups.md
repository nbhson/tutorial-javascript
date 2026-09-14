# Capturing group

> Source: [https://javascript.info/regexp-groups](https://javascript.info/regexp-groups)

<!-- fetched: 2026-09-14 -->

Một phần của pattern có thể được bọc trong dấu ngoặc đơn `(...)`. Điều này được gọi là “capturing group”.

Điều đó có hai tác dụng:

1. Cho phép lấy một phần của kết quả khớp làm một mục riêng trong mảng kết quả.
2. Nếu ta đặt quantifier sau dấu ngoặc, quantifier đó sẽ áp dụng cho toàn bộ dấu ngoặc.

## [Ví dụ](#examples)

Hãy xem dấu ngoặc hoạt động như thế nào qua các ví dụ.

### [Ví dụ: gogogo](#example-gogogo)

Không có dấu ngoặc, pattern `go+` có nghĩa là ký tự `g`, sau đó là `o` lặp lại một hoặc nhiều lần. Ví dụ, `goooo` hoặc `gooooooooo`.

Dấu ngoặc nhóm các ký tự lại với nhau, nên `(go)+` có nghĩa là `go`, `gogo`, `gogogo` và cứ thế.

```
alert( 'Gogogo now!'.match(/(go)+/ig) ); // "Gogogo"
```

### [Ví dụ: domain](#example-domain)

Hãy tạo thứ phức tạp hơn – một regular expression để tìm tên miền website.

Ví dụ:

```
mail.com
users.mail.com
smith.users.mail.com
```

Như ta thấy, một domain gồm các từ lặp lại, sau mỗi từ có một dấu chấm, ngoại trừ từ cuối.

Trong regular expression, điều đó là `(\w+\.)+\w+`:

```
let regexp = /(\w+\.)+\w+/g;

alert( "site.com my.site.com".match(regexp) ); // site.com,my.site.com
```

Việc tìm kiếm hoạt động, nhưng pattern không thể khớp với domain chứa gạch nối, ví dụ `my-site.com`, vì gạch nối không thuộc lớp `\w`.

Ta có thể sửa bằng cách thay `\w` bằng `[\w-]` ở mọi từ ngoại trừ từ cuối: `([\w-]+\.)+\w+`.

### [Ví dụ: email](#example-email)

Có thể mở rộng từ ví dụ trước. Ta có thể tạo một regular expression cho email dựa trên nó.

Định dạng email là: `name@domain`. Bất kỳ từ nào cũng có thể là name, gạch nối và dấu chấm được phép. Trong regular expression, điều đó là `[-.\w]+`.

Pattern:

```
let regexp = /[-.\w]+@([\w-]+\.)+[\w-]+/g;

alert("my@mail.com @ his@site.com.uk".match(regexp)); // my@mail.com, his@site.com.uk
```

Regexp đó không hoàn hảo, nhưng về cơ bản hoạt động và giúp sửa các lỗi đánh máy. Cách kiểm tra email thực sự đáng tin cậy duy nhất là gửi một bức thư.

## [Nội dung dấu ngoặc trong kết quả khớp](#parentheses-contents-in-the-match)

Các dấu ngoặc được đánh số từ trái sang phải. Engine tìm kiếm ghi nhớ nội dung được khớp bởi mỗi dấu ngoặc và cho phép lấy nó trong kết quả.

Phương thức `str.match(regexp)`, nếu `regexp` không có flag `g`, sẽ tìm kết quả khớp đầu tiên và trả về nó dưới dạng mảng:

1. Tại index `0`: kết quả khớp đầy đủ.
2. Tại index `1`: nội dung của dấu ngoặc thứ nhất.
3. Tại index `2`: nội dung của dấu ngoặc thứ hai.
4. …và cứ thế tiếp…

Ví dụ, ta muốn tìm các tag HTML `<.*?>` và xử lý chúng. Sẽ tiện nếu có nội dung của tag (thứ nằm trong dấu nhóc góc) trong một biến riêng.

Hãy bọc nội dung bên trong vào dấu ngoặc, như thế này: `<(.*?)>`.

Bây giờ ta sẽ nhận được cả tag đầy đủ `<h1>` và nội dung của nó `h1` trong mảng kết quả:

```
let str = '<h1>Hello, world!</h1>';

let tag = str.match(/<(.*?)>/);

alert( tag[0] ); // <h1>
alert( tag[1] ); // h1
```

### [Group lồng nhau](#nested-groups)

Các dấu ngoặc có thể lồng nhau. Trong trường hợp này, việc đánh số cũng đi từ trái sang phải.

Ví dụ, khi tìm tag trong `<span class="my">` ta có thể quan tâm đến:

1. Nội dung tag đầy đủ: `span class="my"`.
2. Tên tag: `span`.
3. Thuộc tính của tag: `class="my"`.

Hãy thêm dấu ngoặc cho chúng: `<(([a-z]+)\s*([^>]*))>`.

Chúng được đánh số như sau (từ trái sang phải, theo dấu ngoặc mở):

![](/article/regexp-groups/regexp-nested-groups-pattern.svg)

Trong thực tế:

```
let str = '<span class="my">';

let regexp = /<(([a-z]+)\s*([^>]*))>/;

let result = str.match(regexp);
alert(result[0]); // <span class="my">
alert(result[1]); // span class="my"
alert(result[2]); // span
alert(result[3]); // class="my"
```

Chỉ số 0 của `result` luôn chứa kết quả khớp đầy đủ.

Sau đó là các group, được đánh số từ trái sang phải theo dấu ngoặc mở. Group thứ nhất được trả về như `result[1]`. Ở đây nó bao gồm toàn bộ nội dung tag.

Sau đó, trong `result[2]` là group từ dấu ngoặc mở thứ hai `([a-z]+)` – tên tag, rồi trong `result[3]` là: `([^>]*)`.

Nội dung của mọi group trong chuỗi:

![](/article/regexp-groups/regexp-nested-groups-matches.svg)

### [Group tùy chọn](#optional-groups)

Ngay cả khi một group là tùy chọn và không tồn tại trong kết quả khớp (ví dụ có quantifier `(...)?`), thì phần tử tương ứng trong mảng `result` vẫn có mặt và bằng `undefined`.

Ví dụ, hãy xem xét regexp `a(z)?(c)?`. Nó tìm `"a"` tùy chọn theo sau bởi `"z"` tùy chọn theo sau bởi `"c"`.

Nếu ta chạy nó trên chuỗi chỉ có một ký tự `a`, thì kết quả là:

```
let match = 'a'.match(/a(z)?(c)?/);

alert( match.length ); // 3
alert( match[0] ); // a (whole match)
alert( match[1] ); // undefined
alert( match[2] ); // undefined
```

Mảng có độ dài `3`, nhưng tất cả các group đều trống.

Và đây là một kết quả khớp phức tạp hơn với chuỗi `ac`:

```
let match = 'ac'.match(/a(z)?(c)?/)

alert( match.length ); // 3
alert( match[0] ); // ac (whole match)
alert( match[1] ); // undefined, because there's nothing for (z)?
alert( match[2] ); // c
```

Độ dài mảng là cố định: `3`. Nhưng không có gì cho group `(z)?`, nên kết quả là `["ac", undefined, "c"]`.

## [Tìm kiếm tất cả kết quả khớp có group: matchAll](#searching-for-all-matches-with-groups-matchall)

`matchAll` là một phương thức mới, có thể cần polyfill

Phương thức `matchAll` không được hỗ trợ trong các trình duyệt cũ.

Có thể cần một polyfill, chẳng hạn <https://github.com/ljharb/String.prototype.matchAll>.

Khi ta tìm kiếm tất cả kết quả khớp (flag `g`), phương thức `match` không trả về nội dung cho các group.

Ví dụ, hãy tìm tất cả các tag trong một chuỗi:

```
let str = '<h1> <h2>';

let tags = str.match(/<(.*?)>/g);

alert( tags ); // <h1>,<h2>
```

Kết quả là một mảng các kết quả khớp, nhưng không có chi tiết về từng kết quả. Nhưng trong thực tế ta thường cần nội dung của capturing group trong kết quả.

Để lấy chúng, ta nên tìm kiếm bằng phương thức `str.matchAll(regexp)`.

Nó được thêm vào ngôn ngữ JavaScript rất lâu sau `match`, như một “phiên bản mới và cải tiến hơn”.

Giống như `match`, nó tìm các kết quả khớp, nhưng có 3 điểm khác biệt:

1. Nó không trả về mảng, mà trả về một đối tượng iterable.
2. Khi có flag `g`, nó trả về mỗi kết quả khớp như một mảng kèm các group.
3. Nếu không có kết quả khớp, nó không trả về `null`, mà trả về một đối tượng iterable rỗng.

Ví dụ:

```
let results = '<h1> <h2>'.matchAll(/<(.*?)>/gi);

// results - is not an array, but an iterable object
alert(results); // [object RegExp String Iterator]

alert(results[0]); // undefined (*)

results = Array.from(results); // let's turn it into array

alert(results[0]); // <h1>,h1 (1st tag)
alert(results[1]); // <h2>,h2 (2nd tag)
```

Như ta thấy, điểm khác biệt thứ nhất rất quan trọng, như thể hiện ở dòng `(*)`. Ta không thể lấy kết quả khớp dưới dạng `results[0]`, vì đối tượng đó là một pseudoarray. Ta có thể biến nó thành `Array` thật bằng `Array.from`. Có thêm chi tiết về pseudoarray và iterable trong bài [Iterables](/iterable).

Không cần `Array.from` nếu ta lặp qua các kết quả:

```
let results = '<h1> <h2>'.matchAll(/<(.*?)>/gi);

for(let result of results) {
  alert(result);
  // first alert: <h1>,h1
  // second: <h2>,h2
}
```

…Hoặc dùng destructuring:

```
let [tag1, tag2] = '<h1> <h2>'.matchAll(/<(.*?)>/gi);
```

Mỗi kết quả khớp do `matchAll` trả về có cùng định dạng như `match` không có flag `g`: đó là một mảng với các thuộc tính bổ sung `index` (vị trí kết quả khớp trong chuỗi) và `input` (chuỗi nguồn):

```
let results = '<h1> <h2>'.matchAll(/<(.*?)>/gi);

let [tag1, tag2] = results;

alert( tag1[0] ); // <h1>
alert( tag1[1] ); // h1
alert( tag1.index ); // 0
alert( tag1.input ); // <h1> <h2>
```

Tại sao kết quả của `matchAll` là một đối tượng iterable chứ không phải mảng?

Tại sao phương thức được thiết kế như vậy? Lý do đơn giản – để tối ưu hóa.

Lời gọi `matchAll` không thực hiện việc tìm kiếm. Thay vào đó, nó trả về một đối tượng iterable, ban đầu không có kết quả. Việc tìm kiếm được thực hiện mỗi khi ta lặp qua nó, ví dụ trong vòng lặp.

Vậy, sẽ chỉ tìm được nhiều kết quả bằng bao nhiêu là cần, không hơn.

Ví dụ, trong văn bản có thể có 100 kết quả khớp, nhưng trong vòng lặp `for..of` ta tìm thấy 5 trong số đó, rồi quyết định đã đủ và thực hiện `break`. Khi đó engine sẽ không mất thời gian tìm 95 kết quả còn lại.

## [Named group](#named-groups)

Ghi nhớ các group theo số của chúng là rất khó. Với các pattern đơn giản thì vẫn làm được, nhưng với những pattern phức tạp hơn, đếm dấu ngoặc là bất tiện. Ta có một lựa chọn tốt hơn nhiều: đặt tên cho dấu ngoặc.

Điều này được thực hiện bằng cách đặt `?<name>` ngay sau dấu ngoặc mở.

Ví dụ, hãy tìm một ngày theo định dạng “year-month-day”:

```
let dateRegexp = /(?<year>[0-9]{4})-(?<month>[0-9]{2})-(?<day>[0-9]{2})/;
let str = "2019-04-30";

let groups = str.match(dateRegexp).groups;

alert(groups.year); // 2019
alert(groups.month); // 04
alert(groups.day); // 30
```

Như bạn thấy, các group nằm trong thuộc tính `.groups` của kết quả khớp.

Để tìm kiếm tất cả các ngày, ta có thể thêm flag `g`.

Ta cũng sẽ cần `matchAll` để lấy được các kết quả khớp đầy đủ, cùng với các group:

```
let dateRegexp = /(?<year>[0-9]{4})-(?<month>[0-9]{2})-(?<day>[0-9]{2})/g;

let str = "2019-10-30 2020-01-01";

let results = str.matchAll(dateRegexp);

for(let result of results) {
  let {year, month, day} = result.groups;

  alert(`${day}.${month}.${year}`);
  // first alert: 30.10.2019
  // second: 01.01.2020
}
```

## [Capturing group trong thay thế](#capturing-groups-in-replacement)

Phương thức `str.replace(regexp, replacement)` thay thế mọi kết quả khớp của `regexp` trong `str` cho phép sử dụng nội dung dấu ngoặc trong chuỗi `replacement`. Điều này được thực hiện bằng cách dùng `$n`, trong đó `n` là số group.

Ví dụ,

```
let str = "John Bull";
let regexp = /(\w+) (\w+)/;

alert( str.replace(regexp, '$2, $1') ); // Bull, John
```

Với named group, tham chiếu sẽ là `$<name>`.

Ví dụ, hãy định dạng lại ngày từ “year-month-day” thành “day.month.year”:

```
let regexp = /(?<year>[0-9]{4})-(?<month>[0-9]{2})-(?<day>[0-9]{2})/g;

let str = "2019-10-30, 2020-01-01";

alert( str.replace(regexp, '$<day>.$<month>.$<year>') );
// 30.10.2019, 01.01.2020
```

## [Non-capturing group với ?:](#non-capturing-groups-with)

Đôi khi ta cần dấu ngoặc để áp dụng quantifier đúng cách, nhưng không muốn nội dung của chúng có mặt trong kết quả.

Một group có thể bị loại bỏ bằng cách thêm `?:` ở đầu.

Ví dụ, nếu ta muốn tìm `(go)+` nhưng không muốn nội dung dấu ngoặc (`go`) làm một phần tử riêng trong mảng, ta có thể viết: `(?:go)+`.

Trong ví dụ bên dưới, ta chỉ nhận được tên `John` làm một thành viên riêng của kết quả khớp:

```
let str = "Gogogo John!";

// ?: excludes 'go' from capturing
let regexp = /(?:go)+ (\w+)/i;

let result = str.match(regexp);

alert( result[0] ); // Gogogo John (full match)
alert( result[1] ); // John
alert( result.length ); // 2 (no more items in the array)
```

## [Tóm tắt](#summary)

Dấu ngoặc nhóm một phần của regular expression với nhau, để quantifier áp dụng cho nó như một khối.

Các dấu ngoặc group được đánh số từ trái sang phải, và có thể được đặt tên tùy chọn bằng `(?<name>...)`.

Nội dung được khớp bởi một group có thể lấy được trong kết quả:

- Phương thức `str.match` chỉ trả về capturing group khi không có flag `g`.
- Phương thức `str.matchAll` luôn trả về capturing group.

Nếu dấu ngoặc không có tên, thì nội dung của chúng có sẵn trong mảng match theo số của chúng. Dấu ngoặc có tên cũng có sẵn trong thuộc tính `groups`.

Ta cũng có thể sử dụng nội dung dấu ngoặc trong chuỗi thay thế của `str.replace`: theo số `$n` hoặc theo tên `$<name>`.

Một group có thể bị loại khỏi đánh số bằng cách thêm `?:` ở đầu nó. Điều đó được dùng khi ta cần áp dụng quantifier cho toàn bộ group, nhưng không muốn nó làm một mục riêng trong mảng kết quả. Ta cũng không thể tham chiếu các dấu ngoặc như vậy trong chuỗi thay thế.

---

---

## Bài tập

## [Bài tập](#tasks)

### [Kiểm tra MAC-address](#check-mac-address)

[MAC-address](https://en.wikipedia.org/wiki/MAC_address) của một giao diện mạng gồm 6 số hex hai chữ số ngăn cách bằng dấu hai chấm.

Ví dụ: `'01:32:54:67:89:AB'`.

Viết một regexp kiểm tra xem một chuỗi có phải là MAC-address hay không.

Cách dùng:

```
let regexp = /your regexp/;

alert( regexp.test('01:32:54:67:89:AB') ); // true

alert( regexp.test('0132546789AB') ); // false (no colons)

alert( regexp.test('01:32:54:67:89') ); // false (5 numbers, must be 6)

alert( regexp.test('01:32:54:67:89:ZZ') ) // false (ZZ at the end)
```

solution

Một số hex hai chữ số là `[0-9a-f]{2}` (giả sử đã đặt flag `i`).

Ta cần số đó `NN`, rồi `:NN` lặp lại 5 lần (các số tiếp theo);

Regexp là: `[0-9a-f]{2}(:[0-9a-f]{2}){5}`

Bây giờ hãy thể hiện rằng kết quả khớp phải bắt trọn toàn bộ văn bản: bắt đầu từ đầu và kết thúc ở cuối. Điều đó được làm bằng cách bọc pattern trong `^...$`.

Cuối cùng:

```
let regexp = /^[0-9a-f]{2}(:[0-9a-f]{2}){5}$/i;

alert( regexp.test('01:32:54:67:89:AB') ); // true

alert( regexp.test('0132546789AB') ); // false (no colons)

alert( regexp.test('01:32:54:67:89') ); // false (5 numbers, need 6)

alert( regexp.test('01:32:54:67:89:ZZ') ) // false (ZZ in the end)
```

### [Tìm màu ở định dạng #abc hoặc #abcdef](#find-color-in-the-format-abc-or-abcdef)

Viết một RegExp khớp với màu ở định dạng `#abc` hoặc `#abcdef`. Nghĩa là: `#` theo sau bởi 3 hoặc 6 chữ số hex.

Ví dụ sử dụng:

```
let regexp = /your regexp/g;

let str = "color: #3f3; background-color: #AA00ef; and: #abcd";

alert( str.match(regexp) ); // #3f3 #AA00ef
```

P.S. Phải đúng 3 hoặc 6 chữ số hex. Các giá trị có 4 chữ số, như `#abcd`, không được khớp.

solution

Regexp để tìm màu 3 chữ số `#abc`: `/#[a-f0-9]{3}/i`.

Ta có thể thêm đúng 3 chữ số hex tùy chọn nữa. Không cần nhiều hơn hoặc ít hơn. Màu có 3 hoặc 6 chữ số.

Hãy dùng quantifier `{1,2}` cho việc đó: ta sẽ có `/#([a-f0-9]{3}){1,2}/i`.

Ở đây pattern `[a-f0-9]{3}` được bọc trong dấu ngoặc để áp dụng quantifier `{1,2}`.

Trong thực tế:

```
let regexp = /#([a-f0-9]{3}){1,2}/gi;

let str = "color: #3f3; background-color: #AA00ef; and: #abcd";

alert( str.match(regexp) ); // #3f3 #AA00ef #abc
```

Ở đây có một vấn đề nhỏ: pattern đã tìm thấy `#abc` trong `#abcd`. Để ngăn điều đó, ta có thể thêm `\b` vào cuối:

```
let regexp = /#([a-f0-9]{3}){1,2}\b/gi;

let str = "color: #3f3; background-color: #AA00ef; and: #abcd";

alert( str.match(regexp) ); // #3f3 #AA00ef
```

### [Tìm tất cả các số](#find-all-numbers)

Viết một regexp tìm tất cả các số thập phân, bao gồm số nguyên, số dấu chấm động và số âm.

Một ví dụ sử dụng:

```
let regexp = /your regexp/g;

let str = "-1.5 0 2 -123.4.";

alert( str.match(regexp) ); // -1.5, 0, 2, -123.4
```

solution

Một số dương có phần thập phân tùy chọn là: `\d+(\.\d+)?`.

Hãy thêm `-` tùy chọn ở đầu:

```
let regexp = /-?\d+(\.\d+)?/g;

let str = "-1.5 0 2 -123.4.";

alert( str.match(regexp) );   // -1.5, 0, 2, -123.4
```

### [Phân tích một biểu thức](#parse-an-expression)

Một biểu thức toán học gồm 2 số và một toán tử ở giữa, ví dụ:

- `1 + 2`
- `1.2 * 3.4`
- `-3 / -6`
- `-2 - 2`

Toán tử là một trong các: `"+"`, `"-"`, `"*"` hoặc `"/"`.

Có thể có khoảng trắng thừa ở đầu, ở cuối hoặc giữa các phần.

Tạo một hàm `parse(expr)` nhận một biểu thức và trả về một mảng gồm 3 phần tử:

1. Số thứ nhất.
2. Toán tử.
3. Số thứ hai.

Ví dụ:

```
let [a, op, b] = parse("1.2 * 3.4");

alert(a); // 1.2
alert(op); // *
alert(b); // 3.4
```

solution

Regexp cho một số là: `-?\d+(\.\d+)?`. Ta đã tạo nó trong bài tập trước.

Toán tử là `[-+*/]`. Gạch nối `-` được đặt đầu trong dấu ngoặc vuông, vì ở giữa nó sẽ có nghĩa là khoảng ký tự, trong khi ta chỉ muốn ký tự `-`.

Gạch chéo `/` cần được escape trong một JavaScript regexp `/.../`, ta sẽ làm điều đó sau.

Ta cần một số, một toán tử, rồi một số nữa. Và khoảng trắng tùy chọn ở giữa chúng.

Regular expression đầy đủ: `-?\d+(\.\d+)?\s*[-+*/]\s*-?\d+(\.\d+)?`.

Nó có 3 phần, với `\s*` ở giữa chúng:

1. `-?\d+(\.\d+)?` – số thứ nhất,
2. `[-+*/]` – toán tử,
3. `-?\d+(\.\d+)?` – số thứ hai.

Để mỗi phần này là một phần tử riêng trong mảng kết quả, hãy bọc chúng trong dấu ngoặc: `(-?\d+(\.\d+)?)\s*([-+*/])\s*(-?\d+(\.\d+)?)`.

Trong thực tế:

```
let regexp = /(-?\d+(\.\d+)?)\s*([-+*\/])\s*(-?\d+(\.\d+)?)/;

alert( "1.2 + 12".match(regexp) );
```

Kết quả bao gồm:

- `result[0] == "1.2 + 12"` (full match)
- `result[1] == "1.2"` (group thứ nhất `(-?\d+(\.\d+)?)` – số thứ nhất, bao gồm phần thập phân)
- `result[2] == ".2"` (group thứ hai `(\.\d+)?` – phần thập phân thứ nhất)
- `result[3] == "+"` (group thứ ba `([-+*\/])` – toán tử)
- `result[4] == "12"` (group thứ tư `(-?\d+(\.\d+)?)` – số thứ hai)
- `result[5] == undefined` (group thứ năm `(\.\d+)?` – phần thập phân cuối vắng mặt, nên nó là undefined)

Ta chỉ cần các số và toán tử, không cần kết quả khớp đầy đủ hay các phần thập phân, nên hãy “dọn dẹp” kết quả một chút.

Kết quả khớp đầy đủ (phần tử đầu tiên của mảng) có thể bị xóa bằng cách shift mảng `result.shift()`.

Các group chứa phần thập phân (số 2 và 4) `(.\d+)` có thể bị loại bằng cách thêm `?:` ở đầu: `(?:\.\d+)?`.

Giải pháp cuối cùng:

```
function parse(expr) {
  let regexp = /(-?\d+(?:\.\d+)?)\s*([-+*\/])\s*(-?\d+(?:\.\d+)?)/;

  let result = expr.match(regexp);

  if (!result) return [];
  result.shift();

  return result;
}

alert( parse("-1.23 * 3.45") );  // -1.23, *, 3.45
```

Một phương án thay thế cho việc dùng `?:` non-capturing là ta có thể đặt tên cho các group, như thế này:

```
function parse(expr) {
  let regexp = /(?<a>-?\d+(?:\.\d+)?)\s*(?<operator>[-+*\/])\s*(?<b>-?\d+(?:\.\d+)?)/;

  let result = expr.match(regexp);

  return [result.groups.a, result.groups.operator, result.groups.b];
}

alert( parse("-1.23 * 3.45") );  // -1.23, *, 3.45;
```
