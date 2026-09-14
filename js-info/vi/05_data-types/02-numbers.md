# Số (Numbers)

> Nguồn: [https://javascript.info/number](https://javascript.info/number)

<!-- fetched: 2026-09-14 -->

Trong modern JavaScript, có hai types của numbers:

1. Regular numbers trong JavaScript được stored trong 64-bit format [IEEE-754](https://en.wikipedia.org/wiki/IEEE_754), còn được gọi là "double precision floating point numbers". Đây là những numbers mà chúng ta đang sử dụng most of the time, và chúng ta sẽ talk về chúng trong chương này.
2. BigInt numbers đại diện cho các integers of arbitrary length. Chúng đôi khi cần thiết vì một regular integer number không thể safely exceed `(2^53-1)` hoặc be less than `-(2^53-1)`, như chúng ta đã đề cập earlier trong chương [Data types](/types). Vì bigints được sử dụng trong một few special areas, chúng ta devote them cho một special chapter [BigInt](/bigint).

Vì vậy ở đây chúng ta sẽ talk về regular numbers. Hãy expand knowledge của chúng ta về chúng.

## [Nhiều ways to write a number](#more-ways-to-write-a-number)

Hãy tưởng tượng chúng ta cần viết 1 tỷ. Way obvious là:

```
let billion = 1000000000;
```

Chúng ta cũng có thể sử dụng underscore `_` như là một separator:

```
let billion = 1_000_000_000;
```

Ở đây underscore `_` plays the role của "[syntactic sugar](https://en.wikipedia.org/wiki/Syntactic_sugar)", nó làm cho number dễ đọc hơn. JavaScript engine đơn giản ignore `_` giữa các digits, vì vậy nó exactly cùng một billion như ở trên.

Trong thực life though, chúng ta try để tránh writing long sequences của zeroes. Chúng ta quá lazy для điều đó. Chúng ta sẽ try để viết something like `"1 tỷ"` cho một tỷ hoặc `"7.3 tỷ"` cho 7 tỷ 300 triệu. Điều tương tự đúng cho most large numbers.

Trong JavaScript, chúng ta có thể shorten một number bằng cách appending letter `"e"` vào nó và specifying the zeroes count:

```
let billion = 1e9;  // 1 tỷ, literally: 1 và 9 zeroes

alert( 7.3e9 );  // 7.3 tỷ (giống như 7300000000 hoặc 7_300_000_000)
```

Nói cách khác, `e` multiplies the number by `1` với given zeroes count.

```
1e3 === 1 * 1000; // e3 means *1000
1.23e6 === 1.23 * 1000000; // e6 means *1000000
```

Giờ hãy viết một thứ gì đó very small. Ví例, 1 microsecond (một-millionth của a second):

```
let mсs = 0.000001;
```

Giống như trước đó, sử dụng `"e"` có thể help. Nếu chúng ta muốn avoid writing các zeroes explicitly, chúng ta có thể viết same as:

```
let mcs = 1e-6; // năm zeroes ở bên trái từ 1
```

Nếu chúng ta đếm các zeroes trong `0.000001`, có 6 cái. Vì vậy naturally nó là `1e-6`.

Nói cách khác, một negative number sau `"e"` means một division by 1 với given number của zeroes:

```
// -3 divides by 1 với 3 zeroes
1e-3 === 1 / 1000; // 0.001

// -6 divides by 1 với 6 zeroes
1.23e-6 === 1.23 / 1000000; // 0.00000123

// một ví例 với một bigger number
1234e-2 === 1234 / 100; // 12.34, decimal point moves 2 times
```

### [Hex, binary and octal numbers](#hex-binary-and-octal-numbers)

[Hexadecimal](https://en.wikipedia.org/wiki/Hexadecimal) numbers được widely used trong JavaScript để đại diện cho colors, encode characters, và for many other things. Vì vậy naturally, có một shorter way để viết them: `0x` và sau đó là number.

Ví例:

```
alert( 0xff ); // 255
alert( 0xFF ); // 255 (same, case không matters)
```

Binary và octal numeral systems là rarely used, nhưng also supported bằng cách sử dụng `0b` và `0o` prefixes:

```
let a = 0b11111111; // binary form của 255
let b = 0o377; // octal form của 255

alert( a == b ); // true, cùng một number 255 ở cả two sides
```

Có only 3 numeral systems với such support. Cho các numeral systems khác, chúng ta nên sử dụng function `parseInt` (mà chúng ta sẽ thấy sau trong chương này).

## [toString(base)](#tostring-base)

Method `num.toString(base)` trả về một string representation của `num` trong numeral system với given `base`.

Ví例:

```
let num = 255;

alert( num.toString(16) );  // ff
alert( num.toString(2) );   // 11111111
```

`base` có thể vary từ `2` đến `36`. Theo mặc định, nó là `10`.

Common use cases cho cái này là:

- **base=16** được sử dụng cho hex colors, character encodings v.v., digits có thể là `0..9` hoặc `A..F`.
- **base=2** là mostly cho debugging bitwise operations, digits có thể là `0` hoặc `1`.
- **base=36** là maximum, digits có thể là `0..9` hoặc `A..Z`. Toàn bộ Latin alphabet được sử dụng để đại diện cho một number. Một funny, nhưng useful case cho `36` là khi chúng ta cần turn a long numeric identifier into something shorter, ví例, để make a short url. Có thể simply represent it trong numeral system với base `36`:

  ```
  alert( 123456..toString(36) ); // 2n9c
  ```

Hai dots để call một method

Xin lưu ý rằng hai dots trong `123456..toString(36)` không phải là a typo. Nếu chúng ta muốn call một method trực tiếp trên một number, như `toString` trong ví例 ở trên, sau đó chúng ta cần đặt hai dots `..` sau nó.

Nếu chúng ta đặt một single dot: `123456.toString(36)`, sau đó sẽ có một error, vì JavaScript syntax implies một decimal part sau dot đầu tiên. Và nếu chúng ta đặt một dot nữa, sau đó JavaScript biết rằng decimal part là empty và giờ sử dụng method.

Cũng có thể viết `(123456).toString(36)`.

## [Rounding](#rounding)

Một trong những used operations khi làm việc với numbers là rounding.

Có một few built-in functions cho rounding:

`Math.floor`
:   Rounds down: `3.1` becomes `3`, và `-1.1` becomes `-2`.

`Math.ceil`
:   Rounds up: `3.1` becomes `4`, và `-1.1` becomes `-1`.

`Math.round`
:   Rounds to the nearest integer: `3.1` becomes `3`, `3.6` becomes `4`. Trong middle cases `3.5` rounds up to `4`, và `-3.5` rounds up to `-3`.

`Math.trunc` (không được support bởi Internet Explorer)
:   Removes anything sau decimal point mà không rounding: `3.1` becomes `3`, `-1.1` becomes `-1`.

Đây là một table để summarize những differences giữa chúng:

|  | `Math.floor` | `Math.ceil` | `Math.round` | `Math.trunc` |
| --- | --- | --- | --- | --- |
| `3.1` | `3` | `4` | `3` | `3` |
| `3.5` | `3` | `4` | `4` | `3` |
| `3.6` | `3` | `4` | `4` | `3` |
| `-1.1` | `-2` | `-1` | `-1` | `-1` |
| `-1.5` | `-2` | `-1` | `-1` | `-1` |
| `-1.6` | `-2` | `-1` | `-2` | `-1` |

Các functions này cover all của the possible ways để deal với decimal part của một number. Nhưng nếu chúng ta muốn round number đến `n-th` digit sau decimal?

Ví例, chúng ta có `1.2345` và muốn round nó đến 2 digits, getting only `1.23`.

Có hai ways để làm điều đó:

1. Multiply-and-divide.

   Ví例, để round number đến 2nd digit sau decimal, chúng ta có thể multiply number by `100`, gọi rounding function và sau đó divide it back.

   ```
   let num = 1.23456;

   alert( Math.round(num * 100) / 100 ); // 1.23456 -> 123.456 -> 123 -> 1.23
   ```
2. Method [toFixed(n)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/toFixed) rounds number to `n` digits sau point và returns một string representation của result.

   ```
   let num = 12.34;
   alert( num.toFixed(1) ); // "12.3"
   ```

   Điều này rounds up hoặc down đến nearest value, tương tự như `Math.round`:

   ```
   let num = 12.36;
   alert( num.toFixed(1) ); // "12.4"
   ```

   Xin lưu ý rằng result của `toFixed` là một string. Nếu decimal part là shorter than required, zeroes được appended đến end:

   ```
   let num = 12.34;
   alert( num.toFixed(5) ); // "12.34000", added zeroes để make exactly 5 digits
   ```

   Chúng ta có thể convert nó sang một number bằng cách sử dụng unary plus hoặc một `Number()` call, ví例 viết `+num.toFixed(5)`.

## [Imprecise calculations](#imprecise-calculations)

Internally, một number được represented trong 64-bit format [IEEE-754](https://en.wikipedia.org/wiki/IEEE_754), vì vậy có exactly 64 bits để store một number: 52 của chúng được sử dụng để store các digits, 11 của chúng store position của decimal point, và 1 bit là cho sign.

Nếu một number really huge, nó có thể overflow 64-bit storage và become một special numeric value `Infinity`:

```
alert( 1e500 ); // Infinity
```

What có thể là một little less obvious, nhưng happens quite often, là loss of precision.

Hãy xem xét cái (falsy!) equality test này:

```
alert( 0.1 + 0.2 == 0.3 ); // false
```

Đúng vậy, nếu chúng ta check whether sum của `0.1` và `0.2` là `0.3`, chúng ta get `false`.

Strange! Thế thì nó là gì nếu không phải `0.3`?

```
alert( 0.1 + 0.2 ); // 0.30000000000000004
```

Ouch! Hãy tưởng tượng bạn đang making một e-shopping site và visitor put `$0.10` và `$0.20` goods vào cart của họ. Order total sẽ là `$0.30000000000000004`. Điều đó sẽ surprise bất kỳ ai.

Nhưng tại sao điều này happens?

Một number được stored trong memory trong binary form của nó, một sequence của bits – ones và zeroes. Nhưng fractions như `0.1`, `0.2` mà look simple trong decimal numeral system là actually unending fractions trong binary form của chúng.

```
alert(0.1.toString(2)); // 0.0001100110011001100110011001100110011001100110011001101
alert(0.2.toString(2)); // 0.001100110011001100110011001100110011001100110011001101
alert((0.1 + 0.2).toString(2)); // 0.0100110011001100110011001100110011001100110011001101
```

`0.1` là gì? Đó là one divided by ten `1/10`, one-tenth. Trong decimal numeral system, such numbers được easily representable. So sánh nó với one-third: `1/3`. Nó trở thành một endless fraction `0.33333(3)`.

Vì vậy, division by powers `10` được guaranteed để work well trong decimal system, nhưng division by `3` thì không. Cho cùng lý do, trong binary numeral system, division by powers của `2` được guaranteed để work, nhưng `1/10` trở thành một endless binary fraction.

Không có way nào để store *exactly 0.1* hoặc *exactly 0.2* bằng cách sử dụng binary system, giống như không có way nào để store one-third như một decimal fraction.

Numeric format IEEE-754 solves this bằng cách rounding đến nearest possible number. Những rounding rules normally không allow us để see rằng "tiny precision loss", nhưng nó exists.

Chúng ta có thể see điều này in action:

```
alert( 0.1.toFixed(20) ); // 0.10000000000000000555
```

Và khi chúng ta sum hai numbers, "precision losses" của chúng add up.

Đó là lý do tại sao `0.1 + 0.2` không exactly `0.3`.

Không chỉ JavaScript

Same issue exists trong many other programming languages.

PHP, Java, C, Perl, và Ruby give exactly cùng result, vì chúng是基于 cùng numeric format.

Có thể work around problem không? Chắc chắn, reliable method nhất là round result với help của method [toFixed(n)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/toFixed):

```
let sum = 0.1 + 0.2;
alert( sum.toFixed(2) ); // "0.30"
```

Xin lưu ý rằng `toFixed` luôn luôn trả về một string. Nó ensures rằng nó có 2 digits sau decimal point. Điều đó actually convenient nếu chúng ta có một e-shopping và cần show `$0.30`. Cho các cases khác, chúng ta có thể sử dụng unary plus để coerce nó vào một number:

```
let sum = 0.1 + 0.2;
alert( +sum.toFixed(2) ); // 0.3
```

Chúng ta cũng có thể temporarily multiply các numbers by 100 (hoặc một bigger number) để turn chúng thành integers, do maths, và sau đó divide back. Sau đó, vì chúng ta đang doing maths với integers, error somewhat decreases, nhưng chúng ta vẫn get it trên division:

```
alert( (0.1 * 10 + 0.2 * 10) / 10 ); // 0.3
alert( (0.28 * 100 + 0.14 * 100) / 100); // 0.4200000000000001
```

Vì vậy, multiply/divide approach reduces error, nhưng không remove it totally.

Đôi khi chúng ta có thể try để evade fractions at all. Như nếu chúng ta đang dealing với một shop, sau đó chúng ta có thể store prices trong cents thay vì dollars. Nhưng nếu chúng ta apply một discount của 30%? Trong thực tế, totally evading fractions là rarely possible. Just round them để cut "tails" khi needed.

Funny thing

Hãy thử chạy cái này:

```
// Hello! Tôi là một self-increasing number!
alert( 9999999999999999 ); // shows 10000000000000000
```

Điều này suffers từ cùng issue: một loss of precision. Có 64 bits cho number, 52 của chúng có thể được sử dụng để store digits, nhưng điều đó không đủ. Vì vậy least significant digits disappear.

JavaScript không trigger một error trong such events. Nó does its best để fit number vào desired format, nhưng unfortunately, format đó không big enough.

Hai zeroes

Một consequence funny khác của internal representation của numbers là existence của hai zeroes: `0` và `-0`.

Đó là vì một sign được represented bởi một single bit, vì vậy nó có thể được set hoặc không set cho bất kỳ number nào bao gồm một zero.

Trong hầu hết các cases, distinction là unnoticeable, vì operators được suited để treat them như same.

## [Tests: isFinite và isNaN](#tests-isfinite-and-isnan)

Hãy nhớ hai special numeric values này?

- `Infinity` (và `-Infinity`) là một special numeric value mà lớn hơn (nhỏ hơn) bất kỳ thing nào.
- `NaN` đại diện cho một error.

Chúng thuộc về type `number`, nhưng không phải là "normal" numbers, vì vậy có special functions để check cho chúng:

- `isNaN(value)` converts argument của nó sang một number và sau đó tests it để being `NaN`:

  ```
  alert( isNaN(NaN) ); // true
  alert( isNaN("str") ); // true
  ```

  Nhưng chúng ta có cần function này không? Không thể just use comparison `=== NaN` sao? Unfortunately không. Value `NaN` là unique trong that nó không equal anything, including itself:

  ```
  alert( NaN === NaN ); // false
  ```
- `isFinite(value)` converts argument của nó sang một number và trả về `true` nếu nó là một regular number, không phải `NaN/Infinity/-Infinity`:

  ```
  alert( isFinite("15") ); // true
  alert( isFinite("str") ); // false, vì một special value: NaN
  alert( isFinite(Infinity) ); // false, vì một special value: Infinity
  ```

Đôi khi `isFinite` được sử dụng để validate whether một string value là một regular number:

```
let num = +prompt("Nhập một số", '');

// sẽ là true trừ khi bạn enter Infinity, -Infinity hoặc not a number
alert( isFinite(num) );
```

Xin lưu ý rằng một empty hoặc space-only string được treat như `0` trong all numeric functions including `isFinite`.

`Number.isNaN` và `Number.isFinite`

[Number.isNaN](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/isNaN) và [Number.isFinite](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/isFinite) methods là các "strict" hơn versions của `isNaN` và `isFinite` functions. Chúng không autoconvert argument của chúng vào một number, nhưng check nếu nó thuộc về `number` type thay vì.

- `Number.isNaN(value)` trả về `true` nếu argument thuộc về `number` type và nó là `NaN`. Trong bất kỳ case khác, nó trả về `false`.

  ```
  alert( Number.isNaN(NaN) ); // true
  alert( Number.isNaN("str" / 2) ); // true

  // Note sự difference:
  alert( Number.isNaN("str") ); // false, vì "str" thuộc về string type, không phải number type
  alert( isNaN("str") ); // true, vì isNaN converts string "str" vào một number và gets NaN như là result của conversion này
  ```
- `Number.isFinite(value)` trả về `true` nếu argument thuộc về `number` type và nó không phải là `NaN/Infinity/-Infinity`. Trong bất kỳ case khác, nó trả về `false`.

  ```
  alert( Number.isFinite(123) ); // true
  alert( Number.isFinite(Infinity) ); // false
  alert( Number.isFinite(2 / 0) ); // false

  // Note sự difference:
  alert( Number.isFinite("123") ); // false, vì "123" thuộc về string type, không phải number type
  alert( isFinite("123") ); // true, vì isFinite converts string "123" vào một number 123
  ```

Theo một way, `Number.isNaN` và `Number.isFinite` là simpler và more straightforward hơn `isNaN` và `isFinite` functions. Trong thực tế though, `isNaN` và `isFinite` được mostly used, vì chúng ngắn hơn để写.

Comparison với `Object.is`

Có một special built-in method `Object.is` mà compares values như `===`, nhưng là more reliable cho hai edge cases:

1. Nó work với `NaN`: `Object.is(NaN, NaN) === true`, đó là một good thing.
2. Values `0` và `-0` là different: `Object.is(0, -0) === false`, technically đó là correct vì internally number có một sign bit mà có thể different ngay cả nếu all other bits là zeroes.

Trong tất cả các cases khác, `Object.is(a, b)` là same như `a === b`.

Chúng ta mention `Object.is` ở đây, vì nó thường được used trong JavaScript specification. Khi một internal algorithm needs để compare hai values để being exactly same, nó uses `Object.is` (internally called [SameValue](https://tc39.github.io/ecma262/#sec-samevalue)).

## [parseInt và parseFloat](#parseint-and-parsefloat)

Numeric conversion sử dụng một plus `+` hoặc `Number()` là strict. Nếu một value không exactly là một number, nó fails:

```
alert( +"100px" ); // NaN
```

 Ngoại lệ duy nhất là spaces ở beginning hoặc ở end của string, vì chúng được ignored.

Nhưng trong thực life, chúng ta thường have values trong units, như `"100px"` hoặc `"12pt"` trong CSS. Cũng trong nhiều countries, currency symbol goes sau amount, vì vậy chúng ta có `"19€"` và would like để extract một numeric value out của that.

Đó là những gì `parseInt` và `parseFloat` là for.

Chúng "read" một number từ một string cho đến khi chúng không thể. Trong case của một error, gathered number được returned. Function `parseInt` trả về một integer, trong khi `parseFloat` sẽ trả về một floating-point number:

```
alert( parseInt('100px') ); // 100
alert( parseFloat('12.5em') ); // 12.5

alert( parseInt('12.3') ); // 12, only integer part được returned
alert( parseFloat('12.3.4') ); // 12.3, second point stops reading
```

Có situations khi `parseInt/parseFloat` sẽ trả về `NaN`. Nó happens khi no digits có thể được read:

```
alert( parseInt('a123') ); // NaN, first symbol stops process
```

Second argument của `parseInt(str, radix)`

Function `parseInt()` có một optional second parameter. Nó specifies base của numeral system, vì vậy `parseInt` cũng có thể parse strings của hex numbers, binary numbers và vân vân:

```
alert( parseInt('0xff', 16) ); // 255
alert( parseInt('ff', 16) ); // 255, without 0x cũng work

alert( parseInt('2n9c', 36) ); // 123456
```

## [Other math functions](#other-math-functions)

JavaScript có một built-in [Math](https://developer.mozilla.org/en/docs/Web/JavaScript/Reference/Global_Objects/Math) object chứa một small library của mathematical functions và constants.

Một vài ví例:

`Math.random()`
:   Trả về một random number từ 0 đến 1 (không包括 1).

    ```
    alert( Math.random() ); // 0.1234567894322
    alert( Math.random() ); // 0.5435252343232
    alert( Math.random() ); // ... (any random numbers)
    ```

`Math.max(a, b, c...)` và `Math.min(a, b, c...)`
:   Trả về greatest và smallest từ arbitrary number của arguments.

    ```
    alert( Math.max(3, 5, -10, 0, 1) ); // 5
    alert( Math.min(1, 2) ); // 1
    ```

`Math.pow(n, power)`
:   Trả về `n` raised to given power.

    ```
    alert( Math.pow(2, 10) ); // 2 trong power 10 = 1024
    ```

Có more functions và constants trong `Math` object, bao gồm trigonometry, mà bạn có thể find trong [docs cho Math object](https://developer.mozilla.org/en/docs/Web/JavaScript/Reference/Global_Objects/Math).

## [Tổng kết](#summary)

Để viết numbers với nhiều zeroes:

- Append `"e"` với zeroes count vào number. Như: `123e6` là same như `123` với 6 zeroes `123000000`.
- Một negative number sau `"e"` causes number để được divided by 1 với given zeroes. Ví例. `123e-6` means `0.000123` (`123` millionths).

Cho các numeral systems khác nhau:

- Có thể viết numbers directly trong hex (`0x`), octal (`0o`) và binary (`0b`) systems.
- `parseInt(str, base)` parses string `str` vào một integer trong numeral system với given `base`, `2 ≤ base ≤ 36`.
- `num.toString(base)` converts một number sang một string trong numeral system với given `base`.

Cho regular number tests:

- `isNaN(value)` converts argument của nó sang một number và sau đó tests it để being `NaN`
- `Number.isNaN(value)` checks whether argument thuộc về `number` type, và nếu vậy, tests it để being `NaN`
- `isFinite(value)` converts argument của nó sang một number và sau đó tests it để not being `NaN/Infinity/-Infinity`
- `Number.isFinite(value)` checks whether argument thuộc về `number` type, và nếu vậy, tests it để not being `NaN/Infinity/-Infinity`

Cho converting values như `12pt` và `100px` vào một number:

- Sử dụng `parseInt/parseFloat` cho "soft" conversion, mà read một number từ một string và sau đó trả về value mà chúng có thể read trước error.

Cho fractions:

- Round bằng cách sử dụng `Math.floor`, `Math.ceil`, `Math.trunc`, `Math.round` hoặc `num.toFixed(precision)`.
- Make sure để remember có một loss of precision khi làm việc với fractions.

More mathematical functions:

- Xem [Math](https://developer.mozilla.org/en/docs/Web/JavaScript/Reference/Global_Objects/Math) object khi bạn cần chúng. Library là very small nhưng có thể cover basic needs.

---

---

## Các bài tập

## [Các bài tập](#tasks)

### [Sum numbers từ visitor](#sum-numbers-from-the-visitor)

mức độ quan trọng: 5

Tạo một script mà prompts visitor để enter two numbers và sau đó shows their sum.

[Chạy demo](#)

P.S. Có một gotcha với types.

lời giải

```
let a = +prompt("Số đầu tiên?", "");
let b = +prompt("Số thứ hai?", "");

alert( a + b );
```

Note unary plus `+` trước `prompt`. Nó immediately converts value vào một number.

Nếu không, `a` và `b` sẽ là string và sum của chúng sẽ là concatenation của chúng, tức là: `"1" + "2" = "12"`.

### [Tại sao 6.35.toFixed(1) == 6.3?](#why-6-35-tofixed-1-6-3)

mức độ quan trọng: 4

Theo documentation `Math.round` và `toFixed` both round to the nearest number: `0..4` lead down trong khi `5..9` lead up.

Ví例:

```
alert( 1.35.toFixed(1) ); // 1.4
```

Trong ví例 tương tự dưới đây, tại sao `6.35` được rounded to `6.3`, không phải `6.4`?

```
alert( 6.35.toFixed(1) ); // 6.3
```

Làm thế nào để round `6.35` the right way?

lời giải

Internally decimal fraction `6.35` là một endless binary. Như always trong such cases, nó được stored với một precision loss.

Hãy xem:

```
alert( 6.35.toFixed(20) ); // 6.34999999999999964473
```

Precision loss có thể cause cả increase và decrease của một number. Trong particular case này number trở thành một tiny bit less, đó là lý do tại sao nó rounded down.

Và còn `1.35` thì sao?

```
alert( 1.35.toFixed(20) ); // 1.35000000000000008882
```

Ở đây precision loss làm cho number một little bit greater, vì vậy nó rounded up.

**Làm thế nào chúng ta có thể fix problem với `6.35` nếu chúng ta muốn nó được rounded the right way?**

Chúng ta nên bring it closer to an integer prior to rounding:

```
alert( (6.35 * 10).toFixed(20) ); // 63.50000000000000000000
```

Note rằng `63.5` không có precision loss at all. Đó là vì decimal part `0.5` là actually `1/2`. Fractions divided by powers của `2` được exactly represented trong binary system, giờ chúng ta có thể round nó:

```
alert( Math.round(6.35 * 10) / 10 ); // 6.35 -> 63.5 -> 64(rounded) -> 6.4
```

### [Repeat until input là một number](#repeat-until-the-input-is-a-number)

mức độ quan trọng: 5

Tạo một function `readNumber` mà prompts cho một number cho đến khi visitor enter một valid numeric value.

Resulting value phải được returned như là một number.

Visitor cũng có thể stop process bằng cách enter một empty line hoặc nhấn "CANCEL". Trong case đó, function nên trả về `null`.

[Chạy demo](#)

[Mở một sandbox với tests.](https://plnkr.co/edit/NokU6dmDQg618eEo?p=preview)

lời giải

```
function readNumber() {
  let num;

  do {
    num = prompt("Nhập một number please?", 0);
  } while ( !isFinite(num) );

  if (num === null || num === '') return null;

  return +num;
}

alert(`Read: ${readNumber()}`);
```

Solution là một little bit more intricate that nó có thể là vì chúng ta cần để handle `null`/empty lines.

Vì vậy chúng ta thực sự accept input cho đến khi nó là một "regular number". Cả `null` (cancel) và empty line cũng fit that condition, vì trong numeric form chúng là `0`.

Sau khi chúng ta stopped, chúng ta cần để treat `null` và empty line đặc biệt (return `null`), vì converting chúng vào một number sẽ trả về `0`.

[Mở solution với tests trong một sandbox.](https://plnkr.co/edit/pUfTpGVg7d4H0bvC?p=preview)

### [Một occasional infinite loop](#an-occasional-infinite-loop)

mức độ quan trọng: 4

Loop này là infinite. Nó không bao giờ结束. Tại sao?

```
let i = 0;
while (i != 10) {
  i += 0.2;
}
```

lời giải

Đó là vì `i` sẽ không bao giờ equal `10`.

Run nó để see *real* values của `i`:

```
let i = 0;
while (i < 11) {
  i += 0.2;
  if (i > 9.8 && i < 10.2) alert( i );
}
```

Không có một trong số chúng là exactly `10`.

Such things happens vì precision losses khi adding fractions như `0.2`.

Conclusion: evade equality checks khi làm việc với decimal fractions.

### [Một random number từ min đến max](#a-random-number-from-min-to-max)

mức độ quan trọng: 2

Built-in function `Math.random()` creates một random value từ `0` đến `1` (không包括 `1`).

Viết function `random(min, max)` để generate một random floating-point number từ `min` đến `max` (không包括 `max`).

Các ví例 về work của nó:

```
alert( random(1, 5) ); // 1.2345623452
alert( random(1, 5) ); // 3.7894332423
alert( random(1, 5) ); // 4.3435234525
```

lời giải

Chúng ta cần để "map" all values từ interval 0…1 vào values từ `min` đến `max`.

Điều đó có thể được done trong hai stages:

1. Nếu chúng ta multiply một random number từ 0…1 by `max-min`, sau đó interval của possible values increases `0..1` to `0..max-min`.
2. Giờ nếu chúng ta add `min`, possible interval trở thành từ `min` đến `max`.

Function:

```
function random(min, max) {
  return min + Math.random() * (max - min);
}

alert( random(1, 5) );
alert( random(1, 5) );
alert( random(1, 5) );
```

### [Một random integer từ min đến max](#a-random-integer-from-min-to-max)

mức độ quan trọng: 2

Tạo một function `randomInteger(min, max)` mà generates một random *integer* number từ `min` đến `max` including both `min` và `max` như là possible values.

Bất kỳ number nào từ interval `min..max` phải appear với same probability.

Các ví例 về work của nó:

```
alert( randomInteger(1, 5) ); // 1
alert( randomInteger(1, 5) ); // 3
alert( randomInteger(1, 5) ); // 5
```

Bạn có thể sử dụng solution của [previous task](/task/random-min-max) như là base.

lời giải

Simple nhưng wrong solution

#### Simple nhưng wrong solution

Simplest, nhưng wrong solution sẽ là để generate một value từ `min` đến `max` và round nó:

```
function randomInteger(min, max) {
  let rand = min + Math.random() * (max - min);
  return Math.round(rand);
}

alert( randomInteger(1, 3) );
```

Function hoạt động, nhưng nó là incorrect. Probability để get edge values `min` và `max` là hai times less hơn bất kỳ other.

Nếu bạn run ví例 ở trên many times, bạn would dễ dàng thấy rằng `2` appears the most often.

Điều đó happens vì `Math.round()` gets random numbers từ interval `1..3` và rounds them như sau:

```
values từ 1    ... đến 1.4999999999  become 1
values từ 1.5  ... đến 2.4999999999  become 2
values từ 2.5  ... đến 2.9999999999  become 3
```

Giờ chúng ta có thể clearly see rằng `1` gets twice less values hơn `2`. Và same với `3`.

Correct solution

#### Correct solution

Có nhiều correct solutions cho task. Một trong số chúng là để adjust interval borders. Để ensure same intervals, chúng ta có thể generate values từ `0.5 đến 3.5`, do đó adding required probabilities đến edges:

```
function randomInteger(min, max) {
  // giờ rand là từ (min-0.5) đến (max+0.5)
  let rand = min - 0.5 + Math.random() * (max - min + 1);
  return Math.round(rand);
}

alert( randomInteger(1, 3) );
```

Một alternative way có thể là để sử dụng `Math.floor` cho một random number từ `min` đến `max+1`:

```
function randomInteger(min, max) {
  // giờ rand là từ min đến (max+1)
  let rand = min + Math.random() * (max + 1 - min);
  return Math.floor(rand);
}

alert( randomInteger(1, 3) );
```

Giờ tất cả intervals được map theo cách này:

```
values từ 1  ... đến 1.9999999999  become 1
values từ 2  ... đến 2.9999999999  become 2
values từ 3  ... đến 3.9999999999  become 3
```

Tất cả intervals có same length, making final distribution uniform.
