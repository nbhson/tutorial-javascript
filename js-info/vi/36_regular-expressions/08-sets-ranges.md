# Character set và range [...]

> Source: [https://javascript.info/regexp-character-sets-and-ranges](https://javascript.info/regexp-character-sets-and-ranges)

<!-- fetched: 2026-09-14 -->

Một vài ký tự hoặc character class bên trong dấu ngoặc vuông `[…]` có nghĩa là “tìm bất kỳ ký tự nào trong số đã cho”.

## [Character set](#sets)

Ví dụ, `[eao]` có nghĩa là bất kỳ ký tự nào trong 3: `'a'`, `'e'` hay `'o'`.

Điều này được gọi là *character set*. Character set có thể được dùng trong regexp cùng với các ký tự thường:

```
// tìm [t hoặc m], rồi đến "op"
alert( "Mop top".match(/[tm]op/gi) ); // "Mop", "top"
```

Lưu ý rằng mặc dù character set có nhiều ký tự, chúng chỉ tương ứng với đúng một ký tự trong match.

Vậy nên ví dụ bên dưới không có match nào:

```
// tìm "V", rồi [o hoặc i], rồi "la"
alert( "Voila".match(/V[oi]la/) ); // null, không có match
```

Pattern tìm:

- `V`,
- rồi *một* chữ cái trong `[oi]`,
- rồi `la`.

Vậy nên sẽ có match với `Vola` hoặc `Vila`.

## [Range](#ranges)

Dấu ngoặc vuông cũng có thể chứa *range ký tự*.

Ví dụ, `[a-z]` là một ký tự trong khoảng từ `a` đến `z`, và `[0-5]` là chữ số từ `0` đến `5`.

Trong ví dụ bên dưới, chúng ta tìm `"x"` theo sau bởi hai chữ số hoặc chữ cái từ `A` đến `F`:

```
alert( "Exception 0xAF".match(/x[0-9A-F][0-9A-F]/g) ); // xAF
```

Ở đây `[0-9A-F]` có hai range: nó tìm một ký tự là chữ số từ `0` đến `9` hoặc chữ cái từ `A` đến `F`.

Nếu muốn tìm cả chữ cái thường, chúng ta có thể thêm range `a-f`: `[0-9A-Fa-f]`. Hoặc thêm flag `i`.

Chúng ta cũng có thể dùng character class bên trong `[…]`.

Ví dụ, nếu muốn tìm một ký tự thuộc word `\w` hoặc dấu gạch `-`, thì character set là `[\w-]`.

Kết hợp nhiều class cũng khả thi, ví dụ `[\s\d]` có nghĩa là “ký tự khoảng trắng hoặc chữ số”.

Character class là cách viết tắt cho các character set nhất định

Ví dụ:

- **\d** – giống với `[0-9]`,
- **\w** – giống với `[a-zA-Z0-9_]`,
- **\s** – giống với `[\t\n\v\f\r ]`, cộng thêm một vài ký tự khoảng trắng Unicode hiếm khác.

### [Ví dụ: \w đa ngôn ngữ](#example-multi-language-w)

Vì character class `\w` là cách viết tắt của `[a-zA-Z0-9_]`, nên nó không thể tìm được hieroglyph tiếng Trung, chữ cái Cyrillic, v.v.

Chúng ta có thể viết một pattern tổng quát hơn, tìm các ký tự thuộc word trong bất kỳ ngôn ngữ nào. Điều đó dễ dàng với tính chất Unicode: `[\p{Alpha}\p{M}\p{Nd}\p{Pc}\p{Join_C}]`.

Hãy giải mã nó. Tương tự `\w`, chúng ta tạo một character set riêng bao gồm các ký tự có các tính chất Unicode sau:

- `Alphabetic` (`Alpha`) – cho chữ cái,
- `Mark` (`M`) – cho dấu thanh,
- `Decimal_Number` (`Nd`) – cho chữ số,
- `Connector_Punctuation` (`Pc`) – cho dấu gạch dưới `'_'` và các ký tự tương tự,
- `Join_Control` (`Join_C`) – hai mã đặc biệt `200c` và `200d`, được dùng trong ligature, ví dụ trong tiếng Ả Rập.

Ví dụ sử dụng:

```
let regexp = /[\p{Alpha}\p{M}\p{Nd}\p{Pc}\p{Join_C}]/gu;

let str = `Hi 你好 12`;

// tìm tất cả chữ cái và chữ số:
alert( str.match(regexp) ); // H,i,你,好,1,2
```

Tất nhiên, chúng ta có thể chỉnh sửa pattern này: thêm hoặc bỏ các tính chất Unicode. Tính chất Unicode được mô tả chi tiết hơn trong bài viết [Unicode: flag "u" và class \p{...}](/regexp-unicode).

Tính chất Unicode không được hỗ trợ trong IE

Các tính chất Unicode `\p{…}` không được triển khai trong IE. Nếu thực sự cần chúng, chúng ta có thể dùng thư viện [XRegExp](https://xregexp.com/).

Hoặc đơn giản là dùng range ký tự của ngôn ngữ quan tâm, ví dụ `[а-я]` cho chữ cái Cyrillic.

## [Loại trừ range](#excluding-ranges)

Ngoài các range thường, còn có các range “loại trừ” trông như `[^…]`.

Chúng được ký hiệu bằng dấu `^` ở đầu và match bất kỳ ký tự nào *ngoài những ký tự đã cho*.

Ví dụ:

- `[^aeyo]` – bất kỳ ký tự nào trừ `'a'`, `'e'`, `'y'` hay `'o'`.
- `[^0-9]` – bất kỳ ký tự nào không phải chữ số, giống `\D`.
- `[^\s]` – bất kỳ ký tự nào không phải khoảng trắng, giống `\S`.

Ví dụ bên dưới tìm các ký tự không phải chữ cái, chữ số hay khoảng trắng:

```
alert( "alice15@gmail.com".match(/[^\d\sA-Z]/gi) ); // @ và .
```

## [Escaping bên trong [...]](#escaping-in-)

Thường thì khi muốn tìm đúng một ký tự đặc biệt, chúng ta cần escape nó như `\.`. Và nếu cần dấu `\`, thì dùng `\\`, và vân vân.

Bên trong dấu ngoặc vuông, chúng ta có thể dùng phần lớn các ký tự đặc biệt mà không cần escape:

- Các ký hiệu `. + ( )` không bao giờ cần escape.
- Dấu gạch `-` không cần escape ở đầu hoặc cuối (nơi nó không xác định range).
- Dấu `^` chỉ cần escape ở đầu (nơi nó có nghĩa là loại trừ).
- Dấu ngoặc vuông đóng `]` luôn cần escape (nếu muốn tìm ký hiệu đó).

Nói cách khác, mọi ký tự đặc biệt đều được phép không cần escape, ngoại trừ khi chúng có ý nghĩa riêng đối với dấu ngoặc vuông.

Dấu chấm `.` bên trong dấu ngoặc vuông chỉ có nghĩa là dấu chấm. Pattern `[.,]` sẽ tìm một trong hai ký tự: dấu chấm hoặc dấu phẩy.

Trong ví dụ bên dưới, regexp `[-().^+]` tìm một trong các ký tự `-().^+`:

```
// Không cần escape
let regexp = /[-().^+]/g;

alert( "1 + 2 - 3".match(regexp) ); // Match +, -
```

…Nhưng nếu bạn muốn escape chúng “để chắc chắn”, thì không có hại gì:

```
// Escape mọi thứ
let regexp = /[\-\(\)\.\^\+]/g;

alert( "1 + 2 - 3".match(regexp) ); // cũng hoạt động: +, -
```

## [Range và flag “u”](#ranges-and-flag-u)

Nếu có surrogate pair trong character set, cần flag `u` để chúng hoạt động đúng.

Ví dụ, hãy tìm `[𝒳𝒴]` trong string `𝒳`:

```
alert( '𝒳'.match(/[𝒳𝒴]/) ); // hiển thị ký tự lạ, như [?]
// (việc tìm kiếm diễn ra không đúng, trả về nửa ký tự)
```

Kết quả không đúng, vì mặc định regular expression “không biết” về surrogate pair.

Bộ máy regular expression cho rằng `[𝒳𝒴]` – không phải hai mà là bốn ký tự:

1. nửa trái của `𝒳` `(1)`,
2. nửa phải của `𝒳` `(2)`,
3. nửa trái của `𝒴` `(3)`,
4. nửa phải của `𝒴` `(4)`.

Chúng ta có thể xem mã của chúng như sau:

```
for(let i=0; i<'𝒳𝒴'.length; i++) {
  alert('𝒳𝒴'.charCodeAt(i)); // 55349, 56499, 55349, 56500
};
```

Vậy, ví dụ trên tìm thấy và hiển thị nửa trái của `𝒳`.

Nếu thêm flag `u`, hành vi sẽ đúng:

```
alert( '𝒳'.match(/[𝒳𝒴]/u) ); // 𝒳
```

Tình huống tương tự xảy ra khi tìm một range, như `[𝒳-𝒴]`.

Nếu quên thêm flag `u`, sẽ có lỗi:

```
'𝒳'.match(/[𝒳-𝒴]/); // Error: Invalid regular expression
```

Lý do là không có flag `u`, surrogate pair bị hiểu là hai ký tự, nên `[𝒳-𝒴]` được diễn giải là `[<55349><56499>-<55349><56500>]` (mỗi surrogate pair được thay bằng mã của nó). Giờ dễ thấy rằng range `56499-55349` không hợp lệ: mã đầu `56499` lớn hơn mã cuối `55349`. Đó là lý do chính thức của lỗi.

Với flag `u`, pattern hoạt động đúng:

```
// tìm ký tự từ 𝒳 đến 𝒵
alert( '𝒴'.match(/[𝒳-𝒵]/u) ); // 𝒴
```

---

---

## Bài tập

## [Bài tập](#tasks)

### [Java[^script]](#java-script)

Chúng ta có regexp `/Java[^script]/`.

Nó có match gì trong string `Java`? Trong string `JavaScript`?

đáp án

Đáp án: **không, có**.

- Trong string `Java` nó không match gì, vì `[^script]` có nghĩa là “bất kỳ ký tự nào ngoại trừ những ký tự đã cho”. Vậy regexp tìm `"Java"` theo sau bởi một ký tự như vậy, nhưng ở đây là cuối string, không có ký tự nào phía sau.

  ```
  alert( "Java".match(/Java[^script]/) ); // null
  ```
- Có, vì phần `[^script]` match ký tự `"S"`. Nó không nằm trong `script`. Vì regexp phân biệt hoa thường (không có flag `i`), nó coi `"S"` là khác với `"s"`.

  ```
  alert( "JavaScript".match(/Java[^script]/) ); // "JavaS"
  ```

### [Tìm thời gian dạng hh:mm hoặc hh-mm](#find-the-time-as-hh-mm-or-hh-mm)

Thời gian có thể ở định dạng `giờ:phút` hoặc `giờ-phút`. Cả giờ và phút đều có 2 chữ số: `09:00` hoặc `21-30`.

Viết một regexp để tìm thời gian:

```
let regexp = /regexp của bạn/g;
alert( "Breakfast at 09:00. Dinner at 21-30".match(regexp) ); // 09:00, 21-30
```

P.S. Trong bài tập này, chúng ta giả định rằng thời gian luôn đúng, không cần lọc các string xấu như “45:67”. Sau này chúng ta sẽ xử lý điều đó.

đáp án

Đáp án: `\d\d[-:]\d\d`.

```
let regexp = /\d\d[-:]\d\d/g;
alert( "Breakfast at 09:00. Dinner at 21-30".match(regexp) ); // 09:00, 21-30
```

Lưu ý rằng dấu gạch `'-'` có ý nghĩa đặc biệt trong dấu ngoặc vuông, nhưng chỉ giữa các ký tự khác, không phải khi ở đầu hoặc cuối, nên chúng ta không cần escape nó.
