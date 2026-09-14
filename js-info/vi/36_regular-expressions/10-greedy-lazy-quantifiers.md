# Quantifier kiểu greedy và lazy

> Source: [https://javascript.info/regexp-greedy-and-lazy](https://javascript.info/regexp-greedy-and-lazy)

<!-- fetched: 2026-09-14 -->

Quantifier thoạt nhìn trông rất đơn giản, nhưng thực ra chúng có thể gây khó hiểu.

Nếu ta dự định tìm kiếm thứ gì phức tạp hơn `/\d+/`, thì phải hiểu rõ cách thức hoạt động của quá trình tìm kiếm.

Hãy lấy một bài toán dưới đây làm ví dụ.

Ta có một văn bản và cần thay thế tất cả các cặp dấu nháy `"..."` bằng dấu guillemet: `«...»`. Ở nhiều quốc gia, dấu này được ưa chuộng hơn trong typography.

Ví dụ: `"Hello, world"` nên trở thành `«Hello, world»`. Có những kiểu dấu nháy khác, chẳng hạn `„Witaj, świecie!”` (tiếng Ba Lan) hay `「你好，世界」` (tiếng Trung), nhưng trong bài toán này ta chọn `«...»`.

Điều đầu tiên cần làm là định vị các chuỗi có dấu nháy, rồi ta có thể thay thế chúng.

Một regular expression dạng `/".+"/g` (một dấu nháy, sau đó là nội dung gì đó, rồi đến dấu nháy còn lại) nghe có vẻ hợp lý, nhưng thực ra không phải vậy!

Hãy thử:

```
let regexp = /".+"/g;

let str = 'a "witch" and her "broom" is one';

alert( str.match(regexp) ); // "witch" and her "broom"
```

…Ta có thể thấy rằng nó không hoạt động như dự định!

Thay vì tìm thấy hai kết quả khớp là `"witch"` và `"broom"`, nó chỉ tìm thấy một: `"witch" and her "broom"`.

Có thể diễn đạt điều này rằng “sự tham lam là nguyên nhân của mọi tai họa”.

## [Tìm kiếm kiểu greedy](#greedy-search)

Để tìm một kết quả khớp, engine regular expression sử dụng thuật toán sau:

- Với mỗi vị trí trong chuỗi
  - Thử khớp mẫu pattern tại vị trí đó.
  - Nếu không khớp, chuyển sang vị trí tiếp theo.

Những cách diễn đạt chung chung này không cho thấy rõ tại sao regexp lại thất bại, vì vậy hãy làm rõ cách tìm kiếm hoạt động với pattern `".+"`.

1. Ký tự đầu tiên của pattern là dấu nháy `"`.

   Engine regular expression thử tìm nó tại vị trí 0 của chuỗi nguồn `a "witch" and her "broom" is one`, nhưng ở đó là `a`, nên ngay lập tức không khớp.

   Sau đó nó tiến lên: đi đến các vị trí tiếp theo trong chuỗi nguồn và thử tìm ký tự đầu tiên của pattern, lại thất bại, và cuối cùng tìm thấy dấu nháy tại vị trí thứ 3:

   ![](/article/regexp-greedy-and-lazy/witch_greedy1.svg)
2. Dấu nháy được tìm thấy, và sau đó engine thử khớp phần còn lại của pattern. Nó thử xem phần còn lại của chuỗi có khớp với `.+"` không.

   Trong trường hợp của ta, ký tự pattern tiếp theo là `.` (dấu chấm). Nó biểu thị “bất kỳ ký tự nào ngoại trừ xuống dòng”, nên ký tự tiếp theo trong chuỗi `'w'` khớp:

   ![](/article/regexp-greedy-and-lazy/witch_greedy2.svg)
3. Sau đó dấu chấm lặp lại vì quantifier `.+`. Engine regular expression thêm vào kết quả khớp từng ký tự một.

   …Đến bao giờ? Mọi ký tự đều khớp với dấu chấm, nên nó chỉ dừng lại khi chạm đến cuối chuỗi:

   ![](/article/regexp-greedy-and-lazy/witch_greedy3.svg)
4. Bây giờ engine đã hoàn tất việc lặp `.+` và thử tìm ký tự tiếp theo của pattern. Đó là dấu nháy `"`. Nhưng có vấn đề: chuỗi đã kết thúc, không còn ký tự nào nữa!

   Engine regular expression hiểu rằng nó đã lấy quá nhiều `.+` và bắt đầu *backtrack*.

   Nói cách khác, nó rút ngắn kết quả khớp của quantifier đi một ký tự:

   ![](/article/regexp-greedy-and-lazy/witch_greedy4.svg)

   Bây giờ nó giả định rằng `.+` kết thúc trước cuối chuỗi một ký tự và thử khớp phần còn lại của pattern từ vị trí đó.

   Nếu ở đó có dấu nháy thì quá trình tìm kiếm sẽ kết thúc, nhưng ký tự cuối là `'e'`, nên không khớp.
5. …Vì vậy engine giảm thêm một ký tự số lần lặp của `.+`:

   ![](/article/regexp-greedy-and-lazy/witch_greedy5.svg)

   Dấu nháy `'"'` không khớp với `'n'`.
6. Engine tiếp tục backtrack: nó giảm dần số lần lặp của `'.'` cho đến khi phần còn lại của pattern (trong trường hợp của ta là `'"'`) khớp:

   ![](/article/regexp-greedy-and-lazy/witch_greedy6.svg)
7. Kết quả khớp hoàn tất.
8. Vậy kết quả khớp đầu tiên là `"witch" and her "broom"`. Nếu regexp có flag `g`, thì việc tìm kiếm sẽ tiếp tục từ nơi kết quả khớp đầu tiên kết thúc. Phần còn lại của chuỗi `is one` không còn dấu nháy nào, nên không có kết quả nào khác.

Đó có lẽ không phải điều ta mong đợi, nhưng đó là cách nó hoạt động.

**Ở chế độ greedy (mặc định), ký tự có quantifier được lặp lại càng nhiều lần càng tốt.**

Engine regexp thêm vào kết quả khớp càng nhiều ký tự càng có thể với `.+`, rồi nếu phần còn lại của pattern không khớp, sẽ rút ngắn lại một một.

Với bài toán của ta, ta muốn thứ khác. Đó là nơi chế độ lazy có thể giúp ích.

## [Chế độ lazy](#lazy-mode)

Chế độ lazy của quantifier là ngược lại với chế độ greedy. Nó có nghĩa: “lặp lại với số lần tối thiểu”.

Ta có thể bật nó bằng cách đặt dấu hỏi `'?'` sau quantifier, để nó trở thành `*?` hoặc `+?` hoặc thậm chí `??` với `'?'`.

Để làm rõ: thông thường dấu hỏi `?` tự nó là một quantifier (không hoặc một lần), nhưng nếu được thêm *sau một quantifier khác (hoặc thậm chí sau chính nó)* thì nó mang ý nghĩa khác – nó chuyển chế độ khớp từ greedy sang lazy.

Regexp `/".+?"/g` hoạt động đúng như dự định: nó tìm thấy `"witch"` và `"broom"`:

```
let regexp = /".+?"/g;

let str = 'a "witch" and her "broom" is one';

alert( str.match(regexp) ); // "witch", "broom"
```

Để hiểu rõ sự thay đổi, hãy theo dõi quá trình tìm kiếm từng bước.

1. Bước đầu tiên giống hệt: nó tìm thấy đầu pattern `'"'` tại vị trí thứ 3:

   ![](/article/regexp-greedy-and-lazy/witch_greedy1.svg)
2. Bước tiếp theo cũng tương tự: engine tìm thấy kết quả khớp cho dấu chấm `'.'`:

   ![](/article/regexp-greedy-and-lazy/witch_greedy2.svg)
3. Và bây giờ quá trình tìm kiếm diễn ra khác đi. Vì ta có chế độ lazy cho `+?`, engine không thử khớp dấu chấm thêm một lần nữa, mà dừng lại và thử khớp ngay phần còn lại của pattern `'"'`:

   ![](/article/regexp-greedy-and-lazy/witch_lazy3.svg)

   Nếu ở đó có dấu nháy thì quá trình tìm kiếm sẽ kết thúc, nhưng ở đó là `'i'`, nên không khớp.
4. Sau đó engine regular expression tăng số lần lặp cho dấu chấm và thử một lần nữa:

   ![](/article/regexp-greedy-and-lazy/witch_lazy4.svg)

   Thất bại lần nữa. Sau đó số lần lặp được tăng lên lần nữa…
5. …Cho đến khi tìm thấy kết quả khớp cho phần còn lại của pattern:

   ![](/article/regexp-greedy-and-lazy/witch_lazy5.svg)
6. Lần tìm kiếm tiếp theo bắt đầu từ kết thúc của kết quả khớp hiện tại và cho ra thêm một kết quả:

   ![](/article/regexp-greedy-and-lazy/witch_lazy6.svg)

Trong ví dụ này ta đã thấy chế độ lazy hoạt động với `+?` như thế nào. Các quantifier `*?` và `??` hoạt động theo cách tương tự – engine regexp chỉ tăng số lần lặp nếu phần còn lại của pattern không thể khớp tại vị trí cho trước.

**Chế độ lazy chỉ được bật cho quantifier có `?` đi kèm.**

Các quantifier khác vẫn giữ nguyên chế độ greedy.

Ví dụ:

```
alert( "123 456".match(/\d+ \d+?/) ); // 123 4
```

1. Pattern `\d+` thử khớp càng nhiều chữ số càng tốt (chế độ greedy), nên nó tìm thấy `123` và dừng lại, vì ký tự tiếp theo là khoảng trắng `' '`.
2. Sau đó pattern có một khoảng trắng, nó khớp.
3. Tiếp theo là `\d+?`. Quantifier ở chế độ lazy, nên nó chỉ tìm thấy một chữ số `4` và thử kiểm tra xem phần còn lại của pattern có khớp từ đó không.

   …Nhưng sau `\d+?` không còn gì trong pattern cả.

   Chế độ lazy không lặp lại thứ gì nếu không cần. Pattern đã hoàn tất, nên ta xong việc. Ta có kết quả khớp `123 4`.

Tối ưu hóa

Các engine regular expression hiện đại có thể tối ưu các thuật toán nội bộ để chạy nhanh hơn. Vì vậy chúng có thể hoạt động hơi khác so với thuật toán được mô tả.

Nhưng để hiểu regular expression hoạt động như thế nào và để xây dựng regular expression, ta không cần biết điều đó. Chúng chỉ được dùng nội bộ để tối ưu.

Các regular expression phức tạp khó tối ưu, nên việc tìm kiếm có thể hoạt động y như cách đã mô tả.

## [Cách tiếp cận khác](#alternative-approach)

Với regexp, thường có nhiều hơn một cách để làm cùng một việc.

Trong trường hợp của ta, ta có thể tìm các chuỗi có dấu nháy mà không cần chế độ lazy bằng regexp `"[^"]+"`:

```
let regexp = /"[^"]+"/g;

let str = 'a "witch" and her "broom" is one';

alert( str.match(regexp) ); // "witch", "broom"
```

Regexp `"[^"]+"` cho kết quả đúng, vì nó tìm một dấu nháy `'"'` tiếp theo là một hoặc nhiều ký tự không phải dấu nháy `[^"]`, rồi đến dấu nháy đóng.

Khi engine regexp tìm `[^"]+`, nó dừng việc lặp khi gặp dấu nháy đóng, và ta xong việc.

Lưu ý rằng logic này không thay thế được quantifier lazy!

Nó chỉ đơn giản là khác nhau. Có những lúc ta cần cái này hay cái kia.

**Hãy xem một ví dụ mà quantifier lazy thất bại và biến thể này hoạt động đúng.**

Ví dụ, ta muốn tìm các liên kết dạng `<a href="..." class="doc">`, với bất kỳ `href` nào.

Nên dùng regular expression nào?

Ý tưởng đầu tiên có thể là: `/<a href=".*" class="doc">/g`.

Hãy kiểm tra:

```
let str = '...<a href="link" class="doc">...';
let regexp = /<a href=".*" class="doc">/g;

// Works!
alert( str.match(regexp) ); // <a href="link" class="doc">
```

Nó hoạt động. Nhưng hãy xem chuyện gì xảy ra nếu trong văn bản có nhiều liên kết?

```
let str = '...<a href="link1" class="doc">... <a href="link2" class="doc">...';
let regexp = /<a href=".*" class="doc">/g;

// Whoops! Two links in one match!
alert( str.match(regexp) ); // <a href="link1" class="doc">... <a href="link2" class="doc">
```

Bây giờ kết quả sai vì cùng lý do như ví dụ “witches” của ta. Quantifier `.*` đã lấy quá nhiều ký tự.

Kết quả khớp trông như thế này:

```
<a href="....................................." class="doc">
<a href="link1" class="doc">... <a href="link2" class="doc">
```

Hãy sửa pattern bằng cách làm cho quantifier `.*?` trở thành lazy:

```
let str = '...<a href="link1" class="doc">... <a href="link2" class="doc">...';
let regexp = /<a href=".*?" class="doc">/g;

// Works!
alert( str.match(regexp) ); // <a href="link1" class="doc">, <a href="link2" class="doc">
```

Giờ có vẻ hoạt động đúng, có hai kết quả khớp:

```
<a href="....." class="doc">    <a href="....." class="doc">
<a href="link1" class="doc">... <a href="link2" class="doc">
```

…Nhưng hãy thử với một đầu vào văn bản khác:

```
let str = '...<a href="link1" class="wrong">... <p style="" class="doc">...';
let regexp = /<a href=".*?" class="doc">/g;

// Wrong match!
alert( str.match(regexp) ); // <a href="link1" class="wrong">... <p style="" class="doc">
```

Bây giờ nó thất bại. Kết quả khớp bao gồm không chỉ liên kết, mà còn rất nhiều văn bản sau đó, bao gồm cả `<p...>`.

Tại sao?

Điều đang xảy ra là:

1. Đầu tiên regexp tìm thấy đầu liên kết `<a href="`.
2. Sau đó nó tìm `.*?`: lấy một ký tự (một cách lazy!), kiểm tra xem có khớp `" class="doc">` không (không có).
3. Rồi lấy thêm một ký tự vào `.*?`, và cứ thế… cho đến khi cuối cùng chạm đến `" class="doc">`.

Nhưng vấn đề là: lúc đó đã vượt quá liên kết `<a...>`, nằm trong tag khác `<p>`. Không phải thứ ta muốn.

Đây là hình ảnh của kết quả khớp đặt cạnh văn bản:

```
<a href="..................................." class="doc">
<a href="link1" class="wrong">... <p style="" class="doc">
```

Vậy, ta cần pattern tìm `<a href="...thứ gì đó..." class="doc">`, nhưng cả biến thể greedy lẫn lazy đều có vấn đề.

Biến thể đúng có thể là: `href="[^"]*"`. Nó sẽ lấy mọi ký tự bên trong thuộc tính `href` cho đến dấu nháy gần nhất, đúng thứ ta cần.

Một ví dụ hoạt động:

```
let str1 = '...<a href="link1" class="wrong">... <p style="" class="doc">...';
let str2 = '...<a href="link1" class="doc">... <a href="link2" class="doc">...';
let regexp = /<a href="[^"]*" class="doc">/g;

// Works!
alert( str1.match(regexp) ); // null, no matches, that's correct
alert( str2.match(regexp) ); // <a href="link1" class="doc">, <a href="link2" class="doc">
```

## [Tóm tắt](#summary)

Quantifier có hai chế độ hoạt động:

Greedy
:   Mặc định engine regular expression thử lặp ký tự có quantifier càng nhiều lần càng tốt. Ví dụ, `\d+` tiêu thụ mọi chữ số có thể. Khi không thể tiêu thụ thêm được nữa (không còn chữ số hoặc hết chuỗi), nó tiếp tục khớp phần còn lại của pattern. Nếu không khớp thì nó giảm số lần lặp (backtrack) và thử lại.

Lazy
:   Được bật bằng dấu hỏi `?` sau quantifier. Engine regexp thử khớp phần còn lại của pattern trước mỗi lần lặp của ký tự có quantifier.

Như ta đã thấy, chế độ lazy không phải là “thần dược” cho việc tìm kiếm kiểu greedy. Một phương án thay thế là tìm kiếm greedy được “tinh chỉnh” với các ngoại lệ, như trong pattern `"[^"]+"`.

---

---

## Bài tập

## [Bài tập](#tasks)

### [Một kết quả khớp của /d+? d+?/](#a-match-for-d-d)

Kết quả khớp ở đây là gì?

```
alert( "123 456".match(/\d+? \d+?/g) ); // ?
```

solution

Kết quả là: `123 4`.

Đầu tiên, `\d+?` kiểu lazy thử lấy ít chữ số nhất có thể, nhưng nó phải đạt đến khoảng trắng, nên nó lấy `123`.

Sau đó `\d+?` thứ hai chỉ lấy một chữ số, vì như vậy là đủ.

### [Tìm chú thích HTML](#find-html-comments)

Tìm tất cả các chú thích HTML trong văn bản:

```
let regexp = /your regexp/g;

let str = `... <!-- My -- comment
 test --> ..  <!----> ..
`;

alert( str.match(regexp) ); // '<!-- My -- comment \n test -->', '<!---->'
```

solution

Ta cần tìm phần đầu của chú thích `<!--`, rồi mọi thứ cho đến cuối `-->`.

Một biến thể chấp nhận được là `<!--.*?-->` – quantifier lazy làm cho dấu chấm dừng ngay trước `-->`. Ta cũng cần thêm flag `s` để dấu chấm bao gồm cả ký tự xuống dòng.

Nếu không, các chú thích nhiều dòng sẽ không được tìm thấy:

```
let regexp = /<!--.*?-->/gs;

let str = `... <!-- My -- comment
 test --> ..  <!----> ..
`;

alert( str.match(regexp) ); // '<!-- My -- comment \n test -->', '<!---->'
```

### [Tìm tag HTML](#find-html-tags)

Tạo một regular expression để tìm tất cả các tag HTML (cả mở và đóng) với thuộc tính của chúng.

Một ví dụ sử dụng:

```
let regexp = /your regexp/g;

let str = '<> <a href="/"> <input type="radio" checked> <b>';

alert( str.match(regexp) ); // '<a href="/">', '<input type="radio" checked>', '<b>'
```

Ở đây ta giả sử rằng thuộc tính tag không chứa `<` và `>` (kể cả bên trong dấu nháy), điều này giúp việc đơn giản hơn một chút.

solution

Giải pháp là `<[^<>]+>`.

```
let regexp = /<[^<>]+>/g;

let str = '<> <a href="/"> <input type="radio" checked> <b>';

alert( str.match(regexp) ); // '<a href="/">', '<input type="radio" checked>', '<b>'
```
