# Chuỗi (Strings)

> Nguồn: [https://javascript.info/string](https://javascript.info/string)

<!-- fetched: 2026-09-14 -->

Trong JavaScript, textual data được stored như các strings. Không có separate type cho một single character.

Internal format cho strings là luôn [UTF-16](https://en.wikipedia.org/wiki/UTF-16), nó không tied đến page encoding.

## [Quotes](#quotes)

Hãy recall kinds của quotes.

Strings có thể được enclosed within either single quotes, double quotes hoặc backticks:

```
let single = 'single-quoted';
let double = "double-quoted";

let backticks = `backticks`;
```

Single và double quotes về cơ bản là same. Backticks, however, cho phép chúng ta embed any expression vào trong string, bằng cách wrapping nó trong `${…}`:

```
function sum(a, b) {
  return a + b;
}

alert(`1 + 2 = ${sum(1, 2)}.`); // 1 + 2 = 3.
```

Một advantage khác của việc sử dụng backticks là rằng chúng cho phép một string span multiple lines:

```
let guestList = `Guests:
 * John
 * Pete
 * Mary
`;

alert(guestList); // a list của guests, multiple lines
```

Nhìn natural, phải không? Nhưng single hoặc double quotes không hoạt động theo cách này.

Nếu chúng ta sử dụng chúng và try để sử dụng multiple lines, sẽ có một error:

```
let guestList = "Guests: // Error: Unexpected token ILLEGAL
  * John";
```

Single và double quotes come từ ancient times của language creation, khi need cho multiline strings was not taken into account. Backticks appeared much later và thus là more versatile.

Backticks cũng cho phép chúng ta specify một "template function" trước first backtick. Syntax là: `` func`string` ``. Function `func` được gọi tự động, receives string và embedded expressions và có thể process them. Tính năng này được gọi là "tagged templates", nó rarely seen, nhưng bạn có thể read về nó trong MDN: [Template literals](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Template_literals#Tagged_templates).

## [Special characters](#special-characters)

Vẫn có thể create multiline strings với single và double quotes bằng cách sử dụng một so-called "newline character", được viết là `\n`, mà denotes một line break:

```
let guestList = "Guests:\n * John\n * Pete\n * Mary";

alert(guestList); // a multiline list của guests, same như ở trên
```

Như một simpler ví例, hai dòng này là equal, chỉ được viết differently:

```
let str1 = "Hello\nWorld"; // hai dòng sử dụng một "newline symbol"

// hai dòng sử dụng một normal newline và backticks
let str2 = `Hello
World`;

alert(str1 == str2); // true
```

Có các khác, less common special characters:

| Character | Description |
| --- | --- |
| `\n` | New line |
| `\r` | Trong Windows text files một combination của hai characters `\r\n` represents một new break, trong khi trên non-Windows OS nó's just `\n`. Đó là vì historical reasons, most Windows software cũng hiểu `\n`. |
| `\'`, `\"`, `` \` `` | Quotes |
| `\\` | Backslash |
| `\t` | Tab |
| `\b`, `\f`, `\v` | Backspace, Form Feed, Vertical Tab – được mentioned for completeness, coming from old times, không được sử dụng nowadays (bạn có thể forget them right now). |

Như bạn có thể see, tất cả special characters start với một backslash character `\`. Nó cũng được gọi là một "escape character".

Vì nó's so special, nếu chúng ta cần để show một actual backslash `\` bên trong string, chúng ta cần để double nó:

```
alert( `Backslash: \\` ); // Backslash: \
```

So-called "escaped" quotes `\'`, `\"`, `` \` `` được sử dụng để insert một quote vào trong same-quoted string.

Ví例:

```
alert( 'I\'m the Walrus!' ); // I'm the Walrus!
```

Như bạn có thể see, chúng ta phải prepend inner quote bởi backslash `\'`, vì nếu không nó sẽ indicate string end.

Tất nhiên, only the quotes mà là same như enclosing ones cần được escaped. Vì vậy, như một more elegant solution, chúng ta có thể switch đến double quotes hoặc backticks thay vì:

```
alert( "I'm the Walrus!" ); // I'm the Walrus!
```

Bên cạnh这些 special characters, cũng có một special notation cho Unicode codes `\u…`, nó rarely được sử dụng và được covered trong optional chapter về [Unicode](/unicode).

## [String length](#string-length)

`length` property có string length:

```
alert( `My\n`.length ); // 3
```

Note rằng `\n` là một single "special" character, vì vậy length là indeed `3`.

`length` là một property

People với một background trong一些 anderen languages đôi khi mistype bằng cách calling `str.length()` thay vì just `str.length`. Điều đó không work.

Xin lưu ý rằng `str.length` là một numeric property, không phải là một function. Không có need để thêm parenthesis sau nó. Không phải `.length()`, mà là `.length`.

## [Accessing characters](#accessing-characters)

Để get một character tại position `pos`, sử dụng square brackets `[pos]` hoặc call method [str.at(pos)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/at). Character đầu tiên start từ zero position:

```
let str = `Xin chào`;

// character đầu tiên
alert( str[0] ); // X
alert( str.at(0) ); // X

// character cuối cùng
alert( str[str.length - 1] ); // o
alert( str.at(-1) );
```

Như bạn có thể see, `.at(pos)` method có một benefit của việc allowing negative position. Nếu `pos` là negative, sau đó nó được counted từ end của string.

Vì vậy `.at(-1)` means character cuối cùng, và `.at(-2)` là một trước nó, v.v.

Square brackets luôn luôn return `undefined` cho negative indexes, ví例:

```
let str = `Xin chào`;

alert( str[-2] ); // undefined
alert( str.at(-2) ); // l
```

Chúng ta cũng có thể iterate qua các characters sử dụng `for..of`:

```
for (let char of "Xin chào") {
  alert(char); // X,i,n, ,c,hà,o (char becomes "X", then "i", then "n" etc)
}
```

## [Strings là immutable](#strings-are-immutable)

Strings không thể được changed trong JavaScript. Không thể thay đổi một character.

Hãy thử nó để show rằng nó không work:

```
let str = 'Xin chào';

str[0] = 'h'; // error
alert( str[0] ); // không work
```

Workaround usual là để create một whole new string và assign nó vào `str` thay vì old one.

Ví例:

```
let str = 'Xin chào';

str = 'h' + str[1]; // replace string

alert( str ); // xin chào
```

Trong các sections sau chúng ta sẽ see nhiều ví例 của điều này.

## [Changing case](#changing-the-case)

Methods [toLowerCase()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/toLowerCase) và [toUpperCase()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/toUpperCase) change case:

```
alert( 'Interface'.toUpperCase() ); // INTERFACE
alert( 'Interface'.toLowerCase() ); // interface
```

Hoặc, nếu chúng ta muốn một single character lowercased:

```
alert( 'Interface'[0].toLowerCase() ); // 'i'
```

## [Searching cho substring](#searching-for-a-substring)

Có nhiều ways để look cho một substring bên trong một string.

### [str.indexOf](#str-indexof)

Method đầu tiên là [str.indexOf(substr, pos)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/indexOf).

Nó look cho `substr` trong `str`, bắt đầu từ given position `pos`, và trả về position nơi match được found hoặc `-1` nếu không có gì có thể được found.

Ví例:

```
let str = 'Widget với id';

alert( str.indexOf('Widget') ); // 0, vì 'Widget' được found ở beginning
alert( str.indexOf('widget') ); // -1, không found, search là case-sensitive

alert( str.indexOf("id") ); // 1, "id" được found tại position 1 (..idget với id)
```

Optional second parameter cho phép chúng ta bắt đầu search từ một given position.

Ví例, occurrence đầu tiên của `"id"` là tại position `1`. Để look cho next occurrence, hãy bắt đầu search từ position `2`:

```
let str = 'Widget với id';

alert( str.indexOf('id', 2) ) // 12
```

Nếu chúng ta interested trong tất cả occurrences, chúng ta có thể run `indexOf` trong một loop. Mỗi lần call được made với position sau previous match:

```
let str = 'As sly như một fox, as strong như một ox';

let target = 'as'; // hãy look cho nó

let pos = 0;
while (true) {
  let foundPos = str.indexOf(target, pos);
  if (foundPos == -1) break;

  alert( `Found at ${foundPos}` );
  pos = foundPos + 1; // continue search từ next position
}
```

Cùng algorithm có thể được layed out shorter:

```
let str = "As sly như một fox, as strong như một ox";
let target = "as";

let pos = -1;
while ((pos = str.indexOf(target, pos + 1)) != -1) {
  alert( pos );
}
```

`str.lastIndexOf(substr, position)`

Cũng có một similar method [str.lastIndexOf(substr, position)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/lastIndexOf) mà searches từ end của một string đến beginning của nó.

Nó sẽ liệt kê các occurrences theo reverse order.

Có một slight inconvenience với `indexOf` trong `if` test. Chúng ta không thể put nó trong `if` như thế này:

```
let str = "Widget với id";

if (str.indexOf("Widget")) {
    alert("We found it"); // không work!
}
```

`alert` trong ví例 ở trên không show vì `str.indexOf("Widget")` trả về `0` (meaning rằng nó found match tại starting position). Đúng vậy, nhưng `if` considers `0` để là `false`.

Vì vậy, chúng ta thực sự nên check cho `-1`, như thế này:

```
let str = "Widget với id";

if (str.indexOf("Widget") != -1) {
    alert("We found it"); // work giờ!
}
```

### [includes, startsWith, endsWith](#includes-startswith-endswith)

Modern method [str.includes(substr, pos)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/includes) trả về `true/false` tùy thuộc vào whether `str` contains `substr` within.

Nó là right choice nếu chúng ta cần để test cho match, nhưng không cần position của nó:

```
alert( "Widget với id".includes("Widget") ); // true

alert( "Hello".includes("Bye") ); // false
```

Optional second argument của `str.includes` là position để bắt đầu search từ:

```
alert( "Widget".includes("id") ); // true
alert( "Widget".includes("id", 3) ); // false, từ position 3 không có "id"
```

Các methods [str.startsWith](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/startsWith) và [str.endsWith](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/endsWith) do exactly những gì chúng nói:

```
alert( "Widget".startsWith("Wid") ); // true, "Widget" starts với "Wid"
alert( "Widget".endsWith("get") ); // true, "Widget" ends với "get"
```

## [Getting substring](#getting-a-substring)

Có 3 methods trong JavaScript để get một substring: `substring`, `substr` và `slice`.

`str.slice(start [, end])`
:   Returns part của string từ `start` đến (nhưng không including) `end`.

   Ví例:

   ```
   let str = "stringify";
   alert( str.slice(0, 5) ); // 'strin', substring từ 0 đến 5 (không including 5)
   alert( str.slice(0, 1) ); // 's', từ 0 đến 1, nhưng không including 1, vì vậy chỉ character tại 0
   ```

   Nếu không có second argument, sau đó `slice` goes till end của string:

   ```
   let str = "stringify";
   alert( str.slice(2) ); // 'ringify', từ 2nd position till end
   ```

   Negative values cho `start/end` cũng có thể. Chúng mean position được counted từ string end:

   ```
   let str = "stringify";

   // start tại 4th position từ bên phải, end tại 1st từ bên phải
   alert( str.slice(-4, -1) ); // 'gif'
   ```

`str.substring(start [, end])`
:   Returns part của string *between* `start` và `end` (không including `end`).

   Điều đó almost same như `slice`, nhưng nó allows `start` để be greater than `end` (trong case này nó simply swaps `start` và `end` values).

   Ví例:

   ```
   let str = "stringify";

   // these are same cho substring
   alert( str.substring(2, 6) ); // "ring"
   alert( str.substring(6, 2) ); // "ring"

   // ...but not cho slice:
   alert( str.slice(2, 6) ); // "ring" (same)
   alert( str.slice(6, 2) ); // "" (một empty string)
   ```

   Negative arguments là (không giống slice) không supported, chúng được treat như `0`.

`str.substr(start [, length])`
:   Returns part CỦA string từ `start`, với given `length`.

   Contrast với các methods trước, cái này allows chúng ta để specify `length` thay vì ending position:

   ```
   let str = "stringify";
   alert( str.substr(2, 4) ); // 'ring', từ 2nd position get 4 characters
   ```

   First argument có thể là negative, để counted từ end:

   ```
   let str = "stringify";
   alert( str.substr(-4, 2) ); // 'gi', từ 4th position get 2 characters
   ```

   Method này resides trong [Annex B](https://tc39.es/ecma262/#sec-string.prototype.substr) của language specification. Nó mean rằng chỉ browser-hosted Javascript engines nên support nó, và nó's không recommended để sử dụng nó. Trong thực tế, nó được supported everywhere.

Hãy recap这些 methods để avoid any confusion:

| method | selects… | negatives |
| --- | --- | --- |
| `slice(start, end)` | from `start` đến `end` (không including `end`) | allows negatives |
| `substring(start, end)` | between `start` và `end` (không including `end`) | negative values mean `0` |
| `substr(start, length)` | from `start` get `length` characters | allows negative `start` |

Nên choose哪一个?

Tất cả chúng có thể làm job. Formally, `substr` có một minor drawback: nó được described không phải trong core JavaScript specification, nhưng trong Annex B, mà covers browser-only features tồn tại chủ yếu vì historical reasons. Vì vậy, non-browser environments có thể fail để support nó. Nhưng trong thực tế nó work everywhere.

Trong số các other two variants, `slice` là a little bit more flexible, nó allows negative arguments và shorter để viết.

Vì vậy, cho practical use nó đủ để remember only `slice`.

## [Comparing strings](#comparing-strings)

Như chúng ta biết từ chương [Comparisons](/comparison), strings được compared character-by-character theo alphabetical order.

Mặc dù, có一些 oddities.

1. Một lowercase letter là luôn greater hơn uppercase:

   ```
   alert( 'a' > 'Z' ); // true
   ```
2. Các letters với diacritical marks là "out of order":

   ```
   alert( 'Österreich' > 'Zealand' ); // true
   ```

   Điều đó có thể lead đến strange results nếu chúng ta sort these country names. Thông thường people would expect `Zealand` để come sau `Österreich` trong list.

Để understand những gì happening, chúng ta nên aware rằng strings trong Javascript được encoded bằng cách sử dụng [UTF-16](https://en.wikipedia.org/wiki/UTF-16). Đó là: mỗi character có một corresponding numeric code.

Có các special methods cho phép để get character cho code và ngược lại:

`str.codePointAt(pos)`
:   Trả về một decimal number representing code cho character tại position `pos`:

   ```
   // different case letters có different codes
   alert( "Z".codePointAt(0) ); // 90
   alert( "z".codePointAt(0) ); // 122
   alert( "z".codePointAt(0).toString(16) ); // 7a (nếu chúng ta cần một hexadecimal value)
   ```

`String.fromCodePoint(code)`
:   Creates một character bởi numeric `code` của nó

   ```
   alert( String.fromCodePoint(90) ); // Z
   alert( String.fromCodePoint(0x5a) ); // Z (chúng ta cũng có thể sử dụng một hex value như là một argument)
   ```

Giờ hãy xem các characters với codes `65..220` (latin alphabet và một little bit extra) bằng cách making một string của chúng:

```
let str = '';

for (let i = 65; i <= 220; i++) {
  str += String.fromCodePoint(i);
}
alert( str );
// Output:
// ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~
// ¡¢£¤¥¦§¨©ª«¬­®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜ
```

See? Capital characters go first, sau đó một vài special ones, sau đó lowercase characters, và `Ö` gần end của output.

Giờ nó become obvious tại sao `a > Z`.

Các characters được compared bởi numeric code của chúng. Greater code means character là greater. Code cho `a` (97) là greater hơn code cho `Z` (90).

- Tất cả lowercase letters go sau uppercase letters vì codes của chúng là greater.
- Một số letters như `Ö` stand apart khỏi main alphabet. Ở đây, code của nó là greater hơn bất kỳ thing nào từ `a` đến `z`.

### [Correct comparisons](#correct-comparisons)

"Right" algorithm để làm string comparisons là more complex hơn nó có thể seem, vì alphabets là different cho các languages khác nhau.

Vì vậy, browser cần để know language để compare.

Good luck, modern browsers support internationalization standard [ECMA-402](https://www.ecma-international.org/publications-and-standards/standards/ecma-402/).

Nó provides một special method để compare strings trong các languages khác nhau, following their rules.

Call [str.localeCompare(str2)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/localeCompare) trả về một integer indicating whether `str` là less, equal hoặc greater than `str2` theo language rules:

- Trả về một negative number nếu `str` là less hơn `str2`.
- Trả về một positive number nếu `str` là greater hơn `str2`.
- Trả về `0` nếu chúng equivalent.

Ví例:

```
alert( 'Österreich'.localeCompare('Zealand') ); // -1
```

Method này thực sự có hai additional arguments được specified trong [documentation](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/localeCompare), mà allows nó để specify language (theo mặc định được take từ environment, letter order depends trên language) và setup additional rules như case sensitivity hoặc nên `"a"` và `"á"` được treat như same v.v.

## [Tổng kết](#summary)

- Có 3 types của quotes. Backticks cho phép một string span multiple lines và embed expressions `${…}`.
- Chúng ta có thể sử dụng special characters, như một line break `\n`.
- Để get một character, sử dụng: `[]` hoặc `at` method.
- Để get một substring, sử dụng: `slice` hoặc `substring`.
- Để lowercase/uppercase một string, sử dụng: `toLowerCase/toUpperCase`.
- Để look cho một substring, sử dụng: `indexOf`, hoặc `includes/startsWith/endsWith` cho simple checks.
- Để compare strings theo language, sử dụng: `localeCompare`, nếu không chúng được compared bởi character codes.

Có một vài other helpful methods trong strings:

- `str.trim()` – removes ("trims") spaces từ beginning và end của string.
- `str.repeat(n)` – repeats string `n` times.
- …và更多 để được tìm thấy trong [manual](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String).

Strings cũng có các methods cho doing search/replace với regular expressions. Nhưng đó là big topic, vì vậy nó được explained trong một separate tutorial section [Regular expressions](/regular-expressions).

Cũng, như hiện tại quan trọng để biết rằng strings là based trên Unicode encoding, và vì vậy có're issues với comparisons. Có更多 về Unicode trong chương [Unicode, String internals](/unicode).

---

---

## Các bài tập

## [Các bài tập](#tasks)

### [Uppercase first character](#uppercase-the-first-character)

mức độ quan trọng: 5

Viết một function `ucFirst(str)` mà trả về string `str` với uppercased first character, ví例:

```
ucFirst("john") == "John";
```

[Mở một sandbox với tests.](https://plnkr.co/edit/O8isa6qN6mtA8Ah1?p=preview)

lời giải

Chúng ta không thể "replace" first character, vì strings trong JavaScript là immutable.

Nhưng chúng ta có thể make một new string dựa trên existing one, với uppercased first character:

```
let newStr = str[0].toUpperCase() + str.slice(1);
```

Có một small problem though. Nếu `str` là empty, sau đó `str[0]` là `undefined`, và vì `undefined` không có `toUpperCase()` method, chúng ta sẽ get một error.

Easy way out là để add một test cho empty string, như thế này:

```
function ucFirst(str) {
  if (!str) return str;

  return str[0].toUpperCase() + str.slice(1);
}

alert( ucFirst("john") ); // John
```

[Mở solution với tests trong một sandbox.](https://plnkr.co/edit/FxVLnrCBpNYl7pzy?p=preview)

### [Check cho spam](#check-for-spam)

mức độ quan trọng: 5

Viết một function `checkSpam(str)` mà trả về `true` nếu `str` contains 'viagra' hoặc 'XXX', ngược lại `false`.

Function phải là case-insensitive:

```
checkSpam('buy ViAgRA now') == true
checkSpam('free xxxxx') == true
checkSpam("innocent rabbit") == false
```

[Mở một sandbox với tests.](https://plnkr.co/edit/AVyO0colH2sbXF9o?p=preview)

lời giải

Để make search case-insensitive, hãy bring string đến lower case và sau đó search:

```
function checkSpam(str) {
  let lowerStr = str.toLowerCase();

  return lowerStr.includes('viagra') || lowerStr.includes('xxx');
}

alert( checkSpam('buy ViAgRA now') );
alert( checkSpam('free xxxxx') );
alert( checkSpam("innocent rabbit") );
```

[Mở solution với tests trong một sandbox.](https://plnkr.co/edit/WnJrxb6EyqVP8v3e?p=preview)

### [Truncate text](#truncate-the-text)

mức độ quan trọng: 5

Tạo một function `truncate(str, maxlength)` mà checks length của `str` và, nếu nó exceeds `maxlength` – replaces end của `str` với ellipsis character `"…"`, để make length của nó equal đến `maxlength`.

Result của function nên là truncated (nếu needed) string.

Ví例:

```
truncate("Những gì tôi muốn nói trên chủ đề này là:", 20) == "Những gì tôi muốn nói trê…"

truncate("Hi everyone!", 20) == "Hi everyone!"
```

[Mở một sandbox với tests.](https://plnkr.co/edit/44bL5nMqGyAqKb5u?p=preview)

lời giải

Maximal length phải là `maxlength`, vì vậy chúng ta cần để cut nó một little shorter, để give space cho ellipsis.

Note rằng thực sự có một single Unicode character cho ellipsis. Đó là không phải ba dots.

```
function truncate(str, maxlength) {
  return (str.length > maxlength) ?
    str.slice(0, maxlength - 1) + '…' : str;
}
```

[Mở solution với tests trong một sandbox.](https://plnkr.co/edit/gGuuxcl1laKFOyTI?p=preview)

### [Extract money](#extract-the-money)

mức độ quan trọng: 4

Chúng ta có một cost trong hình thức `"$120"`. Tức là: dollar sign goes first, sau đó là number.

Tạo một function `extractCurrencyValue(str)` mà sẽ extract numeric value từ such string và trả về nó.

Ví例:

```
alert( extractCurrencyValue('$120') === 120 ); // true
```

[Mở một sandbox với tests.](https://plnkr.co/edit/LCTiYS8qoKZaiQbF?p=preview)

lời giải

```
function extractCurrencyValue(str) {
  return +str.slice(1);
}
```

[Mở solution với tests trong một sandbox.](https://plnkr.co/edit/AtmDbb9HlGcErvbk?p=preview)
