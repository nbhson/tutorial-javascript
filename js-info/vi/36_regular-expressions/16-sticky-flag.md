# Sticky flag "y", tìm kiếm tại vị trí

> Source: [https://javascript.info/regexp-sticky](https://javascript.info/regexp-sticky)

<!-- fetched: 2026-09-14 -->

Flag `y` cho phép thực hiện tìm kiếm tại vị trí được chỉ định trong chuỗi nguồn.

Để nắm rõ trường hợp sử dụng của flag `y` và hiểu tốt hơn các cách thức của regexp, hãy khám phá một ví dụ thực tế.

Một trong những bài toán thông dụng cho regexp là “phân tích từ vựng”: ta nhận được một văn bản, ví dụ bằng một ngôn ngữ lập trình, và cần tìm các thành phần cấu trúc của nó. Ví dụ, HTML có các tag và thuộc tính, mã JavaScript có các hàm, biến, v.v.

Viết các bộ phân tích từ vựng là một lĩnh vực chuyên biệt, với các công cụ và thuật toán riêng, nên ta không đi sâu vào đó, nhưng có một bài toán chung: đọc thứ gì đó tại vị trí được chỉ định.

Ví dụ ta có một chuỗi mã `let varName = "value"`, và cần đọc tên biến từ đó, bắt đầu từ vị trí `4`.

Ta sẽ tìm tên biến bằng regexp `\w+`. Thực ra, tên biến JavaScript cần một regexp phức tạp hơn một chút để khớp chính xác, nhưng ở đây không quan trọng.

- Lời gọi `str.match(/\w+/)` chỉ tìm thấy từ đầu tiên trong dòng (`let`). Không phải thứ ta cần.
- Ta có thể thêm flag `g`. Nhưng khi đó lời gọi `str.match(/\w+/g)` sẽ tìm mọi từ trong văn bản, trong khi ta cần một từ tại vị trí `4`. Lại một lần nữa, không phải thứ ta cần.

**Vậy, làm thế nào để tìm kiếm một regexp chính xác tại vị trí được chỉ định?**

Hãy thử dùng phương thức `regexp.exec(str)`.

Với một `regexp` không có flag `g` và `y`, phương thức này chỉ tìm kết quả khớp đầu tiên, hoạt động y như `str.match(regexp)`.

…Nhưng nếu có flag `g`, thì nó thực hiện tìm kiếm trong `str`, bắt đầu từ vị trí được lưu trong thuộc tính `regexp.lastIndex`. Và nếu nó tìm thấy một kết quả khớp, thì đặt `regexp.lastIndex` bằng index ngay sau kết quả khớp đó.

Nói cách khác, `regexp.lastIndex` đóng vai trò là điểm khởi đầu cho việc tìm kiếm, và mỗi lời gọi `regexp.exec(str)` đặt lại nó về giá trị mới (“sau kết quả khớp cuối cùng”). Tất nhiên chỉ khi có flag `g`.

Vậy, các lời gọi `regexp.exec(str)` liên tiếp trả về các kết quả khớp lần lượt.

Đây là ví dụ về các lời gọi như vậy:

```
let str = 'let varName'; // Let's find all words in this string
let regexp = /\w+/g;

alert(regexp.lastIndex); // 0 (initially lastIndex=0)

let word1 = regexp.exec(str);
alert(word1[0]); // let (1st word)
alert(regexp.lastIndex); // 3 (position after the match)

let word2 = regexp.exec(str);
alert(word2[0]); // varName (2nd word)
alert(regexp.lastIndex); // 11 (position after the match)

let word3 = regexp.exec(str);
alert(word3); // null (no more matches)
alert(regexp.lastIndex); // 0 (resets at search end)
```

Ta có thể lấy mọi kết quả khớp trong vòng lặp:

```
let str = 'let varName';
let regexp = /\w+/g;

let result;

while (result = regexp.exec(str)) {
  alert( `Found ${result[0]} at position ${result.index}` );
  // Found let at position 0, then
  // Found varName at position 4
}
```

Cách sử dụng `regexp.exec` như vậy là một phương án thay thế cho phương thức `str.matchAll`, với mức kiểm soát cao hơn một chút trong quá trình.

Hãy quay lại bài toán của ta.

Ta có thể đặt thủ công `lastIndex` thành `4`, để bắt đầu tìm kiếm từ vị trí được chỉ định!

Như thế này:

```
let str = 'let varName = "value"';

let regexp = /\w+/g; // without flag "g", property lastIndex is ignored

regexp.lastIndex = 4;

let word = regexp.exec(str);
alert(word); // varName
```

Tuyệt vời! Vấn đề đã được giải quyết!

Ta đã thực hiện tìm kiếm `\w+`, bắt đầu từ vị trí `regexp.lastIndex = 4`.

Kết quả là đúng.

…Nhưng khoan đã.

Lưu ý: lời gọi `regexp.exec` bắt đầu tìm kiếm tại vị trí `lastIndex` rồi đi xa hơn. Nếu tại vị trí `lastIndex` không có từ, nhưng nó ở đâu đó phía sau, thì nó vẫn sẽ được tìm thấy:

```
let str = 'let varName = "value"';

let regexp = /\w+/g;

// start the search from position 3
regexp.lastIndex = 3;

let word = regexp.exec(str);
// found the match at position 4
alert(word[0]); // varName
alert(word.index); // 4
```

Với một số bài toán, bao gồm cả phân tích từ vựng, điều đó đơn giản là sai. Ta cần tìm một kết quả khớp chính xác tại vị trí được chỉ định trong văn bản, chứ không phải ở đâu đó phía sau. Và đó chính là mục đích của flag `y`.

**Flag `y` làm cho `regexp.exec` tìm kiếm chính xác tại vị trí `lastIndex`, chứ không phải “bắt đầu từ” nó.**

Đây là cùng một cuộc tìm kiếm với flag `y`:

```
let str = 'let varName = "value"';

let regexp = /\w+/y;

regexp.lastIndex = 3;
alert( regexp.exec(str) ); // null (there's a space at position 3, not a word)

regexp.lastIndex = 4;
alert( regexp.exec(str) ); // varName (word at position 4)
```

Như ta thấy, regexp `/\w+/y` không khớp tại vị trí `3` (khác với flag `g`), nhưng khớp tại vị trí `4`.

Không chỉ đó là thứ ta cần, mà còn có một lợi ích hiệu năng quan trọng khi dùng flag `y`.

Hãy tưởng tượng, ta có một văn bản dài, và hoàn toàn không có kết quả khớp nào trong đó. Khi đó, việc tìm kiếm với flag `g` sẽ đi đến hết văn bản và không tìm thấy gì, và điều này sẽ mất đáng kể nhiều thời gian hơn so với việc tìm kiếm bằng flag `y`, thứ chỉ kiểm tra đúng vị trí đó.

Trong các bài toán như phân tích từ vựng, thường có rất nhiều lần tìm kiếm tại một vị trí chính xác, để kiểm tra xem tại đó có gì. Sử dụng flag `y` là chìa khóa cho các cài đặt chính xác và hiệu năng tốt.
