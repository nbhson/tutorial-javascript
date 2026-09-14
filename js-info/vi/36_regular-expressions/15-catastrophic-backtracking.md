# Catastrophic backtracking

> Source: [https://javascript.info/regexp-catastrophic-backtracking](https://javascript.info/regexp-catastrophic-backtracking)

<!-- fetched: 2026-09-14 -->

Một số regular expression trông có vẻ đơn giản, nhưng lại có thể thực thi trong một thời gian veeeeeery dài, thậm chí “đóng băng” JavaScript engine.

Sớm hay muộn, hầu hết các lập trình viên đôi khi đều gặp phải hành vi như vậy. Triệu chứng điển hình – một regular expression hoạt động tốt lúc này lúc khác, nhưng với một số chuỗi nhất định thì nó “đóng băng”, tiêu thụ 100% CPU.

Trong trường hợp đó, trình duyệt web đề xuất tắt script và tải lại trang. Tất nhiên đó là điều không hay.

Với JavaScript phía server, một regexp như vậy có thể làm đóng băng tiến trình server, còn tồi tệ hơn. Vì vậy chắc chắn ta nên tìm hiểu về nó.

## [Ví dụ](#example)

Giả sử ta có một chuỗi, và ta muốn kiểm tra xem nó có bao gồm các từ `\w+` với một khoảng trắng tùy chọn `\s?` sau mỗi từ hay không.

Cách rõ ràng nhất để xây dựng regexp là lấy một từ theo sau bởi một khoảng trắng tùy chọn `\w+\s?` rồi lặp lại nó bằng `*`.

Điều đó dẫn ta đến regexp `^(\w+\s?)*$`, nó chỉ định 0 hoặc nhiều từ như vậy, bắt đầu ở đầu `^` và kết thúc ở cuối `$` của dòng.

Trong thực tế:

```
let regexp = /^(\w+\s?)*$/;

alert( regexp.test("A good string") ); // true
alert( regexp.test("Bad characters: $@#") ); // false
```

Regexp dường như hoạt động. Kết quả đúng. Tuy nhiên, với một số chuỗi nhất định nó mất rất nhiều thời gian. Lâu đến mức JavaScript engine “đóng băng” với mức tiêu thụ CPU 100%.

Nếu bạn chạy ví dụ bên dưới, có lẽ bạn sẽ không thấy gì, vì JavaScript sẽ chỉ “đóng băng”. Trình duyệt web sẽ ngừng phản hồi các sự kiện, giao diện sẽ ngừng hoạt động (hầu hết các trình duyệt chỉ cho phép cuộn trang). Sau một thời gian nó sẽ đề xuất tải lại trang. Vì vậy hãy cẩn thận với điều này:

```
let regexp = /^(\w+\s?)*$/;
let str = "An input string that takes a long time or even makes this regexp hang!";

// will take a very long time
alert( regexp.test(str) );
```

Để công bằng, hãy lưu ý rằng một số engine regular expression có thể xử lý việc tìm kiếm như vậy hiệu quả, ví dụ engine V8 phiên bản từ 8.8 trở lên làm được điều đó (nên Google Chrome 88 không bị đóng băng ở đây), trong khi trình duyệt Firefox bị đóng băng.

## [Ví dụ rút gọn](#simplified-example)

Chuyện gì đang xảy ra? Tại sao regular expression bị đóng băng?

Để hiểu điều đó, hãy rút gọn ví dụ: bỏ các khoảng trắng `\s?`. Khi đó nó trở thành `^(\w+)*$`.

Và để việc rõ ràng hơn, hãy thay `\w` bằng `\d`. Regular expression kết quả vẫn bị đóng băng, ví dụ:

```
let regexp = /^(\d+)*$/;

let str = "012345678901234567890123456789z";

// will take a very long time (careful!)
alert( regexp.test(str) );
```

Vậy regexp nào có vấn đề?

Trước hết, một người có thể nhận ra rằng regexp `(\d+)*` hơi kỳ lạ. Quantifier `*` trông thừa thãi. Nếu ta muốn một số, ta có thể dùng `\d+`.

Quả thật, regexp này là nhân tạo; ta có được nó bằng cách rút gọn ví dụ trước. Nhưng lý do khiến nó chậm là như nhau. Vì vậy hãy hiểu điều đó, rồi ví dụ trước sẽ trở nên rõ ràng.

Điều gì xảy ra trong quá trình tìm kiếm `^(\d+)*$` trong dòng `123456789z` (được rút ngắn một chút cho rõ ràng, lưu ý ký tự không phải chữ số `z` ở cuối, điều đó quan trọng), tại sao nó lại mất nhiều thời gian như vậy?

Đây là những gì engine regexp làm:

1. Trước hết, engine regexp thử tìm nội dung của dấu ngoặc đơn: số `\d+`. Dấu cộng `+` mặc định là greedy, nên nó tiêu thụ mọi chữ số:

   ```
   \d+.......
   (123456789)z
   ```

   Sau khi mọi chữ số được tiêu thụ, `\d+` được coi là đã tìm thấy (như `123456789`).

   Rồi quantifier sao `(\d+)*` được áp dụng. Nhưng trong văn bản không còn chữ số nào, nên dấu sao không cho thêm gì.

   Ký tự tiếp theo trong pattern là cuối chuỗi `$`. Nhưng trong văn bản ta có `z` thay vì cuối, nên không khớp:

   ```
                  X
   \d+........$
   (123456789)z
   ```
2. Vì không có kết quả khớp, quantifier greedy `+` giảm số lần lặp, backtrack lùi một ký tự.

   Bây giờ `\d+` lấy mọi chữ số ngoại trừ chữ số cuối (`12345678`):

   ```
   \d+.......
   (12345678)9z
   ```
3. Sau đó engine thử tiếp tục tìm kiếm từ vị trí tiếp theo (ngay sau `12345678`).

   Dấu sao `(\d+)*` có thể được áp dụng – nó cho thêm một kết quả khớp của `\d+`, số `9`:

   ```
   \d+.......\d+
   (12345678)(9)z
   ```

   Engine thử khớp `$` lần nữa, nhưng thất bại, vì nó gặp `z` thay vì đó:

   ```
                    X
   \d+.......\d+
   (12345678)(9)z
   ```
4. Không có kết quả khớp, nên engine sẽ tiếp tục backtrack, giảm số lần lặp. Backtrack nhìn chung hoạt động như thế này: quantifier greedy gần nhất giảm số lần lặp cho đến khi đạt mức tối thiểu. Rồi quantifier greedy trước đó giảm, và cứ thế.

   Mọi tổ hợp có thể đều được thử. Dưới đây là các ví dụ về chúng.

   Số thứ nhất `\d+` có 7 chữ số, rồi một số có 2 chữ số:

   ```
                    X
   \d+......\d+
   (1234567)(89)z
   ```

   Số thứ nhất có 7 chữ số, rồi hai số mỗi số 1 chữ số:

   ```
                      X
   \d+......\d+\d+
   (1234567)(8)(9)z
   ```

   Số thứ nhất có 6 chữ số, rồi một số có 3 chữ số:

   ```
                    X
   \d+.......\d+
   (123456)(789)z
   ```

   Số thứ nhất có 6 chữ số, rồi 2 số:

   ```
                      X
   \d+.....\d+ \d+
   (123456)(78)(9)z
   ```

   …Và cứ thế tiếp.

Có rất nhiều cách để chia một dãy chữ số `123456789` thành các số. Chính xác hơn, có `2n-1` tổ hợp, trong đó `n` là độ dài của dãy.

- Với `123456789` ta có `n=9`, cho 511 tổ hợp.
- Với một dãy dài hơn có `n=20` có khoảng một triệu (1048575) tổ hợp.
- Với `n=30` – nhiều hơn một nghìn lần (1073741823 tổ hợp).

Thử từng tổ hợp chính là lý do khiến việc tìm kiếm mất nhiều thời gian như vậy.

## [Quay lại các từ và chuỗi](#back-to-words-and-strings)

Điều tương tự xảy ra trong ví dụ đầu tiên của ta, khi ta tìm các từ bằng pattern `^(\w+\s?)*$` trong chuỗi `An input that hangs!`.

Lý do là một từ có thể được biểu diễn bằng một `\w+` hoặc nhiều `\w+`:

```
(input)
(inpu)(t)
(inp)(u)(t)
(in)(p)(ut)
...
```

Đối với con người, rõ ràng rằng có thể không có kết quả khớp, vì chuỗi kết thúc bằng dấu cảm than `!`, nhưng regular expression kỳ vọng một ký tự kiểu từ `\w` hoặc khoảng trắng `\s` ở cuối. Nhưng engine không biết điều đó.

Nó thử mọi tổ hợp về cách regexp `(\w+\s?)*` có thể “tiêu thụ” chuỗi, bao gồm cả các biến thể có khoảng trắng `(\w+\s)*` và không có `(\w+)*` (vì khoảng trắng `\s?` là tùy chọn). Vì có nhiều tổ hợp như vậy (ta đã thấy với các chữ số), việc tìm kiếm mất nhiều thời gian.

Nên làm gì?

Có nên chuyển sang chế độ lazy không?

Rất tiếc, điều đó không giúp được: nếu ta thay `\w+` bằng `\w+?`, regexp vẫn bị đóng băng. Thứ tự của các tổ hợp sẽ thay đổi, nhưng tổng số của chúng thì không.

Một số engine regular expression có các phép thử tinh vi và máy hữu hạn (finite automata) cho phép tránh phải đi qua mọi tổ hợp hoặc làm điều đó nhanh hơn nhiều, nhưng hầu hết các engine không có, và điều đó không phải lúc nào cũng giúp được.

## [Làm sao để sửa?](#how-to-fix)

Có hai cách tiếp cận chính để sửa vấn đề.

Cách thứ nhất là giảm số tổ hợp có thể.

Hãy làm cho khoảng trắng không còn tùy chọn bằng cách viết lại regular expression thành `^(\w+\s)*\w*$` – ta sẽ tìm một số từ bất kỳ có khoảng trắng theo sau `(\w+\s)*`, rồi (tùy chọn) một từ cuối `\w*`.

Regexp này tương đương với regexp trước đó (khớp cùng các chuỗi) và hoạt động tốt:

```
let regexp = /^(\w+\s)*\w*$/;
let str = "An input string that takes a long time or even makes this regex hang!";

alert( regexp.test(str) ); // false
```

Tại sao vấn đề biến mất?

Đó là vì bây giờ khoảng trắng là bắt buộc.

Regexp trước đó, nếu bỏ khoảng trắng, trở thành `(\w+)*`, dẫn đến nhiều tổ hợp của `\w+` trong một từ đơn

Vậy `input` có thể được khớp như hai lần lặp của `\w+`, như thế này:

```
\w+  \w+
(inp)(ut)
```

Pattern mới khác: `(\w+\s)*` chỉ định các lần lặp của từ có khoảng trắng theo sau! Chuỗi `input` không thể được khớp như hai lần lặp của `\w+\s`, vì khoảng trắng là bắt buộc.

Thời gian cần thiết để thử rất nhiều (thực ra là hầu hết) các tổ hợp giờ đã được tiết kiệm.

## [Ngăn ngừa backtracking](#preventing-backtracking)

Tuy nhiên, không phải lúc nào cũng tiện khi viết lại regexp. Trong ví dụ trên, điều đó dễ làm, nhưng không phải lúc nào cũng rõ ràng phải làm thế nào.

Hơn nữa, regexp được viết lại thường phức tạp hơn, và điều đó không tốt. Regexps đã đủ phức tạp mà không cần thêm nổ lực.

May mắn là có một cách tiếp cận thay thế. Ta có thể cấm backtracking cho quantifier.

Cội nguồn của vấn đề là engine regexp thử rất nhiều tổ hợp mà rõ ràng là sai đối với con người.

Ví dụ, trong regexp `(\d+)*$` rõ ràng với con người rằng `+` không nên backtrack. Nếu ta thay một `\d+` bằng hai `\d+\d+` riêng biệt, không gì thay đổi:

```
\d+........
(123456789)!

\d+...\d+....
(1234)(56789)!
```

Và trong ví dụ gốc `^(\w+\s?)*$` ta có thể muốn cấm backtracking trong `\w+`. Nghĩa là: `\w+` phải khớp toàn bộ một từ, với độ dài tối đa có thể. Không cần giảm số lần lặp trong `\w+` hay tách nó thành hai từ `\w+\w+` và cứ thế.

Các engine regular expression hiện đại hỗ trợ possessive quantifiers cho điều đó. Các quantifier thường trở thành possessive khi ta thêm `+` sau chúng. Nghĩa là, ta dùng `\d++` thay vì `\d+` để ngăn `+` khỏi backtrack.

Các possessive quantifier thực ra đơn giản hơn các quantifier “thường”. Chúng chỉ khớp bao nhiêu được, không có backtrack nào. Quá trình tìm kiếm không backtrack đơn giản hơn.

Còn có cả “atomic capturing group” – một cách để tắt backtracking bên trong dấu ngoặc đơn.

…Nhưng tin xấu là, đáng tiếc, trong JavaScript chúng không được hỗ trợ.

Tuy nhiên ta có thể mô phỏng chúng bằng “lookahead transform”.

### [Lookahead đến cứu trợ!](#lookahead-to-the-rescue)

Vậy ta đã đi đến các chủ đề nâng cao thực sự. Ta muốn một quantifier, như `+`, không backtrack, vì đôi khi backtrack không có ý nghĩa.

Pattern để lấy càng nhiều lần lặp của `\w` càng có thể mà không backtrack là: `(?=(\w+))\1`. Tất nhiên, ta có thể lấy một pattern khác thay vì `\w`.

Điều đó có thể trông lạ, nhưng thực ra là một transform rất đơn giản.

Hãy giải mã nó:

- Lookahead `?=` nhìn về phía trước tìm từ dài nhất `\w+` bắt đầu từ vị trí hiện tại.
- Nội dung dấu ngoặc đơn với `?=...` không được engine ghi nhớ, nên bọc `\w+` trong dấu ngoặc đơn. Khi đó engine sẽ ghi nhớ nội dung của chúng
- …Và cho phép ta tham chiếu nó trong pattern dưới dạng `\1`.

Nghĩa là: ta nhìn về phía trước – và nếu có một từ `\w+`, thì khớp nó như `\1`.

Tại sao? Đó là vì lookahead tìm từ `\w+` như một khối và ta capture nó vào pattern bằng `\1`. Về cơ bản ta đã thực hiện một possessive quantifier `+`. Nó chỉ capture toàn bộ từ `\w+`, không phải một phần của nó.

Ví dụ, trong từ `JavaScript` nó không chỉ có thể khớp `Java` mà còn có thể để `Script` khớp phần còn lại của pattern.

Đây là sự so sánh giữa hai pattern:

```
alert( "JavaScript".match(/\w+Script/)); // JavaScript
alert( "JavaScript".match(/(?=(\w+))\1Script/)); // null
```

1. Trong biến thể đầu tiên, `\w+` đầu tiên capture toàn bộ từ `JavaScript` nhưng rồi `+` backtrack từng ký tự, để thử khớp phần còn lại của pattern, cho đến khi cuối cùng thành công (khi `\w+` khớp `Java`).
2. Trong biến thể thứ hai, `(?=(\w+))` nhìn về phía trước và tìm từ `JavaScript`, từ đó được đưa vào pattern như một khối bằng `\1`, nên không còn cách nào để tìm `Script` sau đó.

Ta có thể đặt một regular expression phức tạp hơn vào `(?=(\w+))\1` thay vì `\w`, khi ta cần cấm backtracking cho `+` sau nó.

Lưu ý:

Có thêm thông tin về mối quan hệ giữa possessive quantifiers và lookahead trong các bài [Regex: Emulate Atomic Grouping (and Possessive Quantifiers) with LookAhead](https://instanceof.me/post/52245507631/regex-emulate-atomic-grouping-with-lookahead) và [Mimicking Atomic Groups](https://blog.stevenlevithan.com/archives/mimic-atomic-groups).

Hãy viết lại ví dụ đầu tiên dùng lookahead để ngăn backtracking:

```
let regexp = /^((?=(\w+))\2\s?)*$/;

alert( regexp.test("A good string") ); // true

let str = "An input string that takes a long time or even makes this regex hang!";

alert( regexp.test(str) ); // false, works and fast!
```

Ở đây `\2` được dùng thay vì `\1`, vì có thêm dấu ngoặc đơn bên ngoài. Để tránh nhầm lẫn với các số, ta có thể đặt tên cho dấu ngoặc đơn, ví dụ `(?<word>\w+)`.

```
// parentheses are named ?<word>, referenced as \k<word>
let regexp = /^((?=(?<word>\w+))\k<word>\s?)*$/;

let str = "An input string that takes a long time or even makes this regex hang!";

alert( regexp.test(str) ); // false

alert( regexp.test("A correct string") ); // true
```

Vấn đề được mô tả trong bài này được gọi là “catastrophic backtracking”.

Ta đã xem xét hai cách để giải quyết nó:

- Viết lại regexp để giảm số tổ hợp có thể.
- Ngăn ngừa backtracking.
