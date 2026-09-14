# Unicode: flag "u" và class \p{...}

> Source: [https://javascript.info/regexp-unicode](https://javascript.info/regexp-unicode)

<!-- fetched: 2026-09-14 -->

JavaScript sử dụng [mã hóa Unicode](https://en.wikipedia.org/wiki/Unicode) cho string. Hầu hết các ký tự được mã hóa bằng 2 byte, nhưng điều đó chỉ cho phép biểu diễn tối đa 65536 ký tự.

Khoảng này không đủ lớn để mã hóa tất cả các ký tự có thể, vì vậy một số ký tự hiếm được mã hóa bằng 4 byte, ví dụ như `𝒳` (X toán học) hay `😄` (mỉm cười), một số hieroglyph, v.v.

Dưới đây là giá trị Unicode của một số ký tự:

| Ký tự | Unicode | Số byte trong Unicode |
| --- | --- | --- |
| a | `0x0061` | 2 |
| ≈ | `0x2248` | 2 |
| 𝒳 | `0x1d4b3` | 4 |
| 𝒴 | `0x1d4b4` | 4 |
| 😄 | `0x1f604` | 4 |

Vậy các ký tự như `a` và `≈` chiếm 2 byte, trong khi mã của `𝒳`, `𝒴` và `😄` dài hơn, chúng có 4 byte.

Rất lâu trước đây, khi ngôn ngữ JavaScript ra đời, mã hóa Unicode đơn giản hơn: không có ký tự 4 byte. Vì vậy, một số tính năng của ngôn ngữ vẫn xử lý chúng chưa đúng.

Ví dụ, `length` cho rằng ở đây có hai ký tự:

```
alert('😄'.length); // 2
alert('𝒳'.length); // 2
```

…Nhưng chúng ta thấy chỉ có một, đúng không? Vấn đề là `length` xử lý 4 byte như hai ký tự 2 byte. Điều đó không đúng, vì chúng phải được xem xét cùng nhau (gọi là “surrogate pair”, bạn có thể đọc về chúng trong bài viết [String](/string)).

Mặc định, regular expression cũng xử lý các “ký tự dài” 4 byte như một cặp 2 byte. Và giống như string, điều này có thể dẫn đến kết quả kỳ lạ. Chúng ta sẽ thấy điều đó sau, trong bài viết [Sets and ranges [...]](/regexp-character-sets-and-ranges).

Khác với string, regular expression có flag `u` để sửa những vấn đề này. Với flag đó, regexp xử lý đúng các ký tự 4 byte. Và tìm kiếm theo tính chất Unicode cũng trở nên khả dụng, chúng ta sẽ tìm hiểu tiếp sau.

## [Tính chất Unicode \p{…}](#unicode-properties-p)

Mỗi ký tự trong Unicode có rất nhiều tính chất. Chúng mô tả “loại” mà ký tự thuộc về, chứa các thông tin khác về nó.

Ví dụ, nếu một ký tự có tính chất `Letter`, điều đó có nghĩa là ký tự thuộc một bảng chữ cái (của bất kỳ ngôn ngữ nào). Và tính chất `Number` có nghĩa là nó là một chữ số: có thể là chữ số Ả Rập hoặc Trung Quốc, v.v.

Chúng ta có thể tìm các ký tự có một tính chất, được viết là `\p{…}`. Để dùng `\p{…}`, regular expression phải có flag `u`.

Ví dụ, `\p{Letter}` chỉ một chữ cái trong bất kỳ ngôn ngữ nào. Chúng ta cũng có thể dùng `\p{L}`, vì `L` là alias của `Letter`. Gần như mọi tính chất đều có alias ngắn hơn.

Trong ví dụ bên dưới, ba loại chữ cái sẽ được tìm thấy: tiếng Anh, tiếng Georgia và tiếng Hàn.

```
let str = "A ბ ㄱ";

alert( str.match(/\p{L}/gu) ); // A,ბ,ㄱ
alert( str.match(/\p{L}/g) ); // null (không match, \p không hoạt động không có flag "u")
```

Dưới đây là các loại ký tự chính và các loại phụ của chúng:

- Letter (chữ cái) `L`:
  - chữ thường `Ll`
  - modifier `Lm`,
  - titlecase `Lt`,
  - hoa `Lu`,
  - khác `Lo`.
- Number (chữ số) `N`:
  - chữ số thập phân `Nd`,
  - chữ số dạng chữ cái `Nl`,
  - khác `No`.
- Punctuation (câu điểm) `P`:
  - connector `Pc`,
  - dash (dấu gạch) `Pd`,
  - mở đầu (initial quote) `Pi`,
  - kết thúc (final quote) `Pf`,
  - mở (open) `Ps`,
  - đóng (close) `Pe`,
  - khác `Po`.
- Mark (vết) `M` (dấu thanh, v.v.):
  - spacing combining `Mc`,
  - bao quanh (enclosing) `Me`,
  - không khoảng cách (non-spacing) `Mn`.
- Symbol (ký hiệu) `S`:
  - tiền tệ (currency) `Sc`,
  - modifier `Sk`,
  - toán học (math) `Sm`,
  - khác `So`.
- Separator (ngăn cách) `Z`:
  - dòng (line) `Zl`,
  - đoạn (paragraph) `Zp`,
  - khoảng trắng (space) `Zs`.
- Khác (Other) `C`:
  - điều khiển (control) `Cc`,
  - định dạng (format) `Cf`,
  - chưa gán (not assigned) `Cn`,
  - dùng riêng (private use) `Co`,
  - surrogate `Cs`.

Vậy ví dụ, nếu chúng ta cần chữ cái thường, chúng ta có thể viết `\p{Ll}`, ký hiệu câu điểm: `\p{P}`, v.v.

Còn có các loại dẫn xuất khác, như:

- `Alphabetic` (`Alpha`), bao gồm Letter `L`, cộng thêm chữ số dạng chữ cái `Nl` (ví dụ Ⅻ – ký tự của số La Mã 12), cộng thêm một số ký hiệu khác `Other_Alphabetic` (`OAlpha`).
- `Hex_Digit` bao gồm chữ số hex: `0-9`, `a-f`.
- …Và vân vân.

Unicode hỗ trợ rất nhiều tính chất khác nhau, danh sách đầy đủ sẽ cần nhiều không gian, vì vậy đây là các tham chiếu:

- Liệt kê mọi tính chất theo một ký tự: <https://unicode.org/cldr/utility/character.jsp>.
- Liệt kê mọi ký tự theo một tính chất: <https://unicode.org/cldr/utility/list-unicodeset.jsp>.
- Alias ngắn cho các tính chất: <https://www.unicode.org/Public/UCD/latest/ucd/PropertyValueAliases.txt>.
- CSDL đầy đủ các ký tự Unicode ở định dạng text, với mọi tính chất, tại đây: <https://www.unicode.org/Public/UCD/latest/ucd/>.

### [Ví dụ: số hex](#example-hexadecimal-numbers)

Ví dụ, hãy tìm các số hex, được viết dạng `xFF`, trong đó `F` là một chữ số hex (0…9 hoặc A…F).

Một chữ số hex có thể được biểu diễn là `\p{Hex_Digit}`:

```
let regexp = /x\p{Hex_Digit}\p{Hex_Digit}/u;

alert("number: xAF".match(regexp)); // xAF
```

### [Ví dụ: hieroglyph tiếng Trung](#example-chinese-hieroglyphs)

Hãy tìm các hieroglyph tiếng Trung.

Có một tính chất Unicode `Script` (hệ thống chữ viết), có thể có giá trị: `Cyrillic`, `Greek`, `Arabic`, `Han` (Trung Quốc) và vân vân, [đây là danh sách đầy đủ](https://en.wikipedia.org/wiki/Script_(Unicode)).

Để tìm các ký tự trong một hệ chữ viết đã cho, chúng ta nên dùng `Script=<giá trị>`, ví dụ với chữ cái Cyrillic: `\p{sc=Cyrillic}`, với hieroglyph tiếng Trung: `\p{sc=Han}`, v.v.:

```
let regexp = /\p{sc=Han}/gu; // trả về hieroglyph tiếng Trung

let str = `Hello Привет 你好 123_456`;

alert( str.match(regexp) ); // 你,好
```

### [Ví dụ: tiền tệ](#example-currency)

Các ký tự biểu diễn tiền tệ, như `$`, `€`, `¥`, có tính chất Unicode `\p{Currency_Symbol}`, alias ngắn: `\p{Sc}`.

Hãy dùng nó để tìm giá tiền theo định dạng “tiền tệ, theo sau là chữ số”:

```
let regexp = /\p{Sc}\d/gu;

let str = `Prices: $2, €1, ¥9`;

alert( str.match(regexp) ); // $2,€1,¥9
```

Sau này, trong bài viết [Quantifier +, \*, ? và {n}](/regexp-quantifiers) chúng ta sẽ thấy cách tìm các số có nhiều chữ số.

## [Tóm tắt](#summary)

Flag `u` bật hỗ trợ Unicode trong regular expression.

Điều đó có nghĩa là hai điều:

1. Các ký tự 4 byte được xử lý đúng: như một ký tự đơn lẻ, không phải hai ký tự 2 byte.
2. Có thể dùng tính chất Unicode trong tìm kiếm: `\p{…}`.

Với tính chất Unicode, chúng ta có thể tìm các từ trong các ngôn ngữ đã cho, các ký tự đặc biệt (dấu nháy, tiền tệ) và vân vân.
