# Phương thức của RegExp và String

> Source: [https://javascript.info/regexp-methods](https://javascript.info/regexp-methods)

<!-- fetched: 2026-09-14 -->

Trong bài này ta sẽ đi sâu vào các phương thức khác nhau làm việc với regexp.

## [str.match(regexp)](#str-match-regexp)

Phương thức `str.match(regexp)` tìm các kết quả khớp của `regexp` trong chuỗi `str`.

Nó có 3 chế độ:

1. Nếu `regexp` không có flag `g`, thì nó trả về kết quả khớp đầu tiên dưới dạng mảng với các capturing group và các thuộc tính `index` (vị trí của kết quả khớp), `input` (chuỗi nhập, bằng `str`):

   ```
   let str = "I love JavaScript";

   let result = str.match(/Java(Script)/);

   alert( result[0] );     // JavaScript (full match)
   alert( result[1] );     // Script (first capturing group)
   alert( result.length ); // 2

   // Additional information:
   alert( result.index );  // 7 (match position)
   alert( result.input );  // I love JavaScript (source string)
   ```
2. Nếu `regexp` có flag `g`, thì nó trả về một mảng tất cả các kết quả khớp dưới dạng chuỗi, không có capturing group và các chi tiết khác.

   ```
   let str = "I love JavaScript";

   let result = str.match(/Java(Script)/g);

   alert( result[0] ); // JavaScript
   alert( result.length ); // 1
   ```
3. Nếu không có kết quả khớp, bất kể có flag `g` hay không, trả về `null`.

   Đó là một chi tiết quan trọng. Nếu không có kết quả khớp, ta không nhận được mảng rỗng, mà là `null`. Rất dễ mắc lỗi khi quên điều này, ví dụ:

   ```
   let str = "I love JavaScript";

   let result = str.match(/HTML/);

   alert(result); // null
   alert(result.length); // Error: Cannot read property 'length' of null
   ```

   Nếu ta muốn kết quả là một mảng, ta có thể viết như thế này:

   ```
   let result = str.match(regexp) || [];
   ```

## [str.matchAll(regexp)](#str-matchall-regexp)

Được thêm vào gần đây

Đây là tính năng mới được thêm vào ngôn ngữ.
Các trình duyệt cũ có thể cần [polyfills](https://javascript.info/polyfills).

Phương thức `str.matchAll(regexp)` là biến thể “mới hơn, cải tiến hơn” của `str.match`.

Nó chủ yếu được dùng để tìm tất cả kết quả khớp cùng với mọi group.

Có 3 điểm khác biệt so với `match`:

1. Nó trả về một đối tượng iterable chứa các kết quả khớp thay vì mảng. Ta có thể tạo một mảng thường từ nó bằng `Array.from`.
2. Mỗi kết quả khớp được trả về như một mảng với các capturing group (cùng định dạng như `str.match` không có flag `g`).
3. Nếu không có kết quả, nó trả về một đối tượng iterable rỗng thay vì `null`.

Ví dụ sử dụng:

```
let str = '<h1>Hello, world!</h1>';
let regexp = /<(.*?)>/g;

let matchAll = str.matchAll(regexp);

alert(matchAll); // [object RegExp String Iterator], not array, but an iterable

matchAll = Array.from(matchAll); // array now

let firstMatch = matchAll[0];
alert( firstMatch[0] );  // <h1>
alert( firstMatch[1] );  // h1
alert( firstMatch.index );  // 0
alert( firstMatch.input );  // <h1>Hello, world!</h1>
```

Nếu ta dùng `for..of` để lặp qua các kết quả khớp của `matchAll`, thì không cần `Array.from` nữa.

## [str.split(regexp|substr, limit)](#str-split-regexp-substr-limit)

Tách chuỗi bằng regexp (hoặc một con chuỗi) làm ký tự phân tách.

Ta có thể dùng `split` với chuỗi, như thế này:

```
alert('12-34-56'.split('-')) // array of ['12', '34', '56']
```

Nhưng ta cũng có thể tách bằng một regular expression, theo cách tương tự:

```
alert('12, 34, 56'.split(/,\s*/)) // array of ['12', '34', '56']
```

## [str.search(regexp)](#str-search-regexp)

Phương thức `str.search(regexp)` trả về vị trí của kết quả khớp đầu tiên hoặc `-1` nếu không tìm thấy:

```
let str = "A drop of ink may make a million think";

alert( str.search( /ink/i ) ); // 10 (first match position)
```

**Hạn chế quan trọng: `search` chỉ tìm kết quả khớp đầu tiên.**

Nếu ta cần vị trí của các kết quả khớp tiếp theo, ta nên dùng các phương tiện khác, như tìm tất cả chúng bằng `str.matchAll(regexp)`.

## [str.replace(str|regexp, str|func)](#str-replace-str-regexp-str-func)

Đây là một phương thức tổng quát cho việc tìm kiếm và thay thế, một trong những phương thức hữu ích nhất. Con dao Thụy Sĩ cho việc tìm kiếm và thay thế.

Ta có thể dùng nó không cần regexp, để tìm kiếm và thay thế một con chuỗi:

```
// replace a dash by a colon
alert('12-34-56'.replace("-", ":")) // 12:34-56
```

Tuy nhiên, có một bẫy.

**Khi đối số thứ nhất của `replace` là chuỗi, nó chỉ thay kết quả khớp đầu tiên.**

Bạn có thể thấy điều đó trong ví dụ trên: chỉ dấu `"-"` đầu tiên được thay bằng `":"`.

Để tìm tất cả các gạch ngang, ta cần dùng không phải chuỗi `"-"`, mà regexp `/-/g`, với flag `g` bắt buộc:

```
// replace all dashes by a colon
alert( '12-34-56'.replace( /-/g, ":" ) )  // 12:34:56
```

Đối số thứ hai là chuỗi thay thế. Ta có thể dùng các ký tự đặc biệt trong nó:

| Symbols | Action in the replacement string |
| --- | --- |
| `$&` | inserts the whole match |
| `` $` `` | inserts a part of the string before the match |
| `$'` | inserts a part of the string after the match |
| `$n` | if `n` is a 1-2 digit number, inserts the contents of n-th capturing group, for details see [Capturing groups](/regexp-groups) |
| `$<name>` | inserts the contents of the parentheses with the given `name`, for details see [Capturing groups](/regexp-groups) |
| `$$` | inserts character `$` |

Ví dụ:

```
let str = "John Smith";

// swap first and last name
alert(str.replace(/(john) (smith)/i, '$2, $1')) // Smith, John
```

**Với các tình huống đòi hỏi thay thế “thông minh”, đối số thứ hai có thể là một hàm.**

Hàm đó sẽ được gọi cho mỗi kết quả khớp, và giá trị trả về sẽ được chèn vào làm thay thế.

Hàm được gọi với các đối số `func(match, p1, p2, ..., pn, offset, input, groups)`:

1. `match` – kết quả khớp,
2. `p1, p2, ..., pn` – nội dung của các capturing group (nếu có),
3. `offset` – vị trí của kết quả khớp,
4. `input` – chuỗi nguồn,
5. `groups` – một object chứa các named group.

Nếu regexp không có dấu ngoặc đơn, thì chỉ có 3 đối số: `func(str, offset, input)`.

Ví dụ, hãy viết hoa mọi kết quả khớp:

```
let str = "html and css";

let result = str.replace(/html|css/gi, str => str.toUpperCase());

alert(result); // HTML and CSS
```

Thay mỗi kết quả khớp bằng vị trí của nó trong chuỗi:

```
alert("Ho-Ho-ho".replace(/ho/gi, (match, offset) => offset)); // 0-3-6
```

Trong ví dụ bên dưới có hai dấu ngoặc đơn, nên hàm thay thế được gọi với 5 đối số: đầu tiên là kết quả khớp đầy đủ, rồi 2 dấu ngoặc đơn, và sau đó (không được dùng trong ví dụ) vị trí kết quả khớp và chuỗi nguồn:

```
let str = "John Smith";

let result = str.replace(/(\w+) (\w+)/, (match, name, surname) => `${surname}, ${name}`);

alert(result); // Smith, John
```

Nếu có nhiều group, sẽ tiện khi dùng rest parameters để truy cập chúng:

```
let str = "John Smith";

let result = str.replace(/(\w+) (\w+)/, (...match) => `${match[2]}, ${match[1]}`);

alert(result); // Smith, John
```

Hoặc, nếu ta đang dùng named group, thì object `groups` chứa chúng luôn ở vị trí cuối, nên ta có thể lấy nó như thế này:

```
let str = "John Smith";

let result = str.replace(/(?<name>\w+) (?<surname>\w+)/, (...match) => {
  let groups = match.pop();

  return `${groups.surname}, ${groups.name}`;
});

alert(result); // Smith, John
```

Dùng một hàm mang lại cho ta quyền năng thay thế tối thượng, vì nó nhận được mọi thông tin về kết quả khớp, truy cập được các biến bên ngoài và có thể làm mọi thứ.

## [str.replaceAll(str|regexp, str|func)](#str-replaceall-str-regexp-str-func)

Phương thức này về cơ bản giống `str.replace`, với hai điểm khác biệt chính:

1. Nếu đối số thứ nhất là một chuỗi, nó thay *mọi lần xuất hiện* của chuỗi, trong khi `replace` chỉ thay *lần xuất hiện đầu tiên*.
2. Nếu đối số thứ nhất là một regular expression không có flag `g`, sẽ có lỗi. Với flag `g`, nó hoạt động giống `replace`.

Trường hợp sử dụng chính của `replaceAll` là thay mọi lần xuất hiện của một chuỗi.

Như thế này:

```
// replace all dashes by a colon
alert('12-34-56'.replaceAll("-", ":")) // 12:34:56
```

## [regexp.exec(str)](#regexp-exec-str)

Phương thức `regexp.exec(str)` trả về một kết quả khớp của `regexp` trong chuỗi `str`. Khác với các phương thức trước, nó được gọi trên một regexp, chứ không phải trên một chuỗi.

Nó hoạt động khác nhau tùy thuộc vào regexp có flag `g` hay không.

Nếu không có `g`, thì `regexp.exec(str)` trả về kết quả khớp đầu tiên y như `str.match(regexp)`. Hành vi này không mang lại gì mới.

Nhưng nếu có flag `g`, thì:

- Một lời gọi `regexp.exec(str)` trả về kết quả khớp đầu tiên và lưu vị trí ngay sau nó trong thuộc tính `regexp.lastIndex`.
- Lời gọi tiếp theo bắt đầu tìm kiếm từ vị trí `regexp.lastIndex`, trả về kết quả khớp tiếp theo và lưu vị trí sau nó trong `regexp.lastIndex`.
- …Và cứ thế tiếp.
- Nếu không có kết quả khớp, `regexp.exec` trả về `null` và đặt lại `regexp.lastIndex` về `0`.

Vậy, các lời gọi lặp lại trả về tất cả kết quả khớp lần lượt, sử dụng thuộc tính `regexp.lastIndex` để theo dõi vị trí tìm kiếm hiện tại.

Trước đây, trước khi phương thức `str.matchAll` được thêm vào JavaScript, các lời gọi `regexp.exec` được dùng trong vòng lặp để lấy tất cả kết quả khớp với groups:

```
let str = 'More about JavaScript at https://javascript.info';
let regexp = /javascript/ig;

let result;

while (result = regexp.exec(str)) {
  alert( `Found ${result[0]} at position ${result.index}` );
  // Found JavaScript at position 11, then
  // Found javascript at position 33
}
```

Cách này vẫn hoạt động bây giờ, mặc dù với các trình duyệt mới, `str.matchAll` thường tiện lợi hơn.

**Ta có thể dùng `regexp.exec` để tìm kiếm từ một vị trí được chỉ định bằng cách đặt thủ công `lastIndex`.**

Ví dụ:

```
let str = 'Hello, world!';

let regexp = /\w+/g; // without flag "g", lastIndex property is ignored
regexp.lastIndex = 5; // search from 5th position (from the comma)

alert( regexp.exec(str) ); // world
```

Nếu regexp có flag `y`, thì việc tìm kiếm sẽ được thực hiện chính xác tại vị trí `regexp.lastIndex`, chứ không đi xa hơn.

Hãy thay flag `g` bằng `y` trong ví dụ trên. Sẽ không có kết quả khớp, vì tại vị trí `5` không có từ:

```
let str = 'Hello, world!';

let regexp = /\w+/y;
regexp.lastIndex = 5; // search exactly at position 5

alert( regexp.exec(str) ); // null
```

Điều đó tiện lợi cho những tình huống ta cần “đọc” thứ gì đó từ chuỗi bằng regexp tại đúng vị trí, chứ không phải ở đâu đó xa hơn.

## [regexp.test(str)](#regexp-test-str)

Phương thức `regexp.test(str)` tìm một kết quả khớp và trả về `true/false` tùy thuộc vào việc nó có tồn tại hay không.

Ví dụ:

```
let str = "I love JavaScript";

// these two tests do the same
alert( /love/i.test(str) ); // true
alert( str.search(/love/i) != -1 ); // true
```

Một ví dụ với câu trả lời phủ định:

```
let str = "Bla-bla-bla";

alert( /love/i.test(str) ); // false
alert( str.search(/love/i) != -1 ); // false
```

Nếu regexp có flag `g`, thì `regexp.test` tìm từ thuộc tính `regexp.lastIndex` và cập nhật thuộc tính này, giống hệt như `regexp.exec`.

Vậy ta có thể dùng nó để tìm kiếm từ một vị trí được chỉ định:

```
let regexp = /love/gi;

let str = "I love JavaScript";

// start the search from position 10:
regexp.lastIndex = 10;
alert( regexp.test(str) ); // false (no match)
```

Cùng một regexp global được thử lặp lại trên các nguồn khác nhau có thể thất bại

Nếu ta áp dụng cùng một regexp global lên các đầu vào khác nhau, có thể dẫn đến kết quả sai, vì lời gọi `regexp.test` làm cho thuộc tính `regexp.lastIndex` tiến lên, nên việc tìm kiếm trong chuỗi khác có thể bắt đầu từ vị trí khác 0.

Ví dụ, ở đây ta gọi `regexp.test` hai lần trên cùng một văn bản, và lần thứ hai thất bại:

```
let regexp = /javascript/g;  // (regexp just created: regexp.lastIndex=0)

alert( regexp.test("javascript") ); // true (regexp.lastIndex=10 now)
alert( regexp.test("javascript") ); // false
```

Chính xác là vì `regexp.lastIndex` khác 0 trong phép thử thứ hai.

Để khắc phục, ta có thể đặt `regexp.lastIndex = 0` trước mỗi lần tìm kiếm. Hoặc thay vì gọi phương thức trên regexp, dùng các phương thức chuỗi `str.match/search/...`, chúng không dùng `lastIndex`.
