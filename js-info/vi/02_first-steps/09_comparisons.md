# So sánh

> Nguồn: [https://javascript.info/comparison](https://javascript.info/comparison)

<!-- fetched: 2026-09-14 -->

Chúng ta biết nhiều toán tử so sánh từ toán học.

Trong JavaScript chúng được viết như sau:

- Lớn/hơn bé: `a > b`, `a < b`.
- Lớn hơn hoặc bằng/bé hơn hoặc bằng: `a >= b`, `a <= b`.
- Bằng: `a == b`, xin lưu ý dấu bằng kép `==` có nghĩa là kiểm tra bằng, trong khi dấu bằng đơn `a = b` có nghĩa là một phép gán.
- Không bằng: Trong toán học ký hiệu là `≠`, nhưng trong JavaScript nó được viết là `a != b`.

Trong bài viết này chúng ta sẽ tìm hiểu thêm về các loại so sánh khác nhau, cách JavaScript thực hiện chúng, bao gồm các điểm đặc biệt quan trọng.

Ở cuối bạn sẽ tìm được một công thức tốt để tránh các vấn đề liên quan đến “JavaScript quirks”.

## [Boolean là kết quả](#boolean-is-the-result)

Tất cả các toán tử so sánh trả về một giá trị boolean:

- `true` – có nghĩa là “có”, “đúng” hoặc “sự thật”.
- `false` – có nghĩa là “không”, “sai” hoặc “không phải sự thật”.

Ví dụ:

```
alert( 2 > 1 );  // true (đúng)
alert( 2 == 1 ); // false (sai)
alert( 2 != 1 ); // true (đúng)
```

Kết quả so sánh có thể được gán cho một biến, giống như bất kỳ giá trị nào:

```
let result = 5 > 4; // gán kết quả của phép so sánh
alert( result ); // true
```

## [So sánh chuỗi](#string-comparison)

Để xem một chuỗi lớn hơn chuỗi khác, JavaScript sử dụng thứ tự được gọi là “từ điển” hoặc “lexicographical”.

Nói cách khác, các chuỗi được so sánh từng ký tự.

Ví dụ:

```
alert( 'Z' > 'A' ); // true
alert( 'Glow' > 'Glee' ); // true
alert( 'Bee' > 'Be' ); // true
```

Thuật toán để so sánh hai chuỗi đơn giản:

1. So sánh ký tự đầu tiên của cả hai chuỗi.
2. Nếu ký tự đầu tiên từ chuỗi đầu tiên lớn hơn (hoặc nhỏ hơn) chuỗi kia, thì chuỗi đầu lớn hơn (hoặc nhỏ hơn) chuỗi thứ hai. Chúng ta kết thúc.
3. Ngược lại, nếu ký tự đầu tiên của cả hai chuỗi giống nhau, so sánh ký tự thứ hai theo cách tương tự.
4. Lặp lại cho đến khi kết thúc của chuỗi nào đó.
5. Nếu cả hai chuỗi kết thúc ở cùng độ dài, thì chúng bằng nhau. Ngược lại, chuỗi dài hơn là lớn hơn.

Trong ví dụ đầu tiên ở trên, so sánh `'Z' > 'A'` đạt kết quả ở bước đầu tiên.

So sánh thứ hai `'Glow'` và `'Glee'` cần nhiều bước hơn vì chuỗi được so sánh từng ký tự:

1. `G` giống như `G`.
2. `l` giống như `l`.
3. `o` lớn hơn `e`. Dừng ở đây. Chuỗi đầu lớn hơn.

Không phải là từ điển thực, nhưng là thứ tự Unicode

Thuật toán so sánh được đưa ra ở trênroughly tương đương với thuật toán được sử dụng trong từ điển hoặc sách điện thoại, nhưng nó không chính xác giống nhau.

Ví dụ, phân biệt chữ hoa/thường. Một chữ cái hoa `"A"` không bằng chữ thường `"a"`. Cái nào lớn hơn? Chữ thường `"a"`. Tại sao? Vì ký tự thường có chỉ số lớn hơn trong bảng mã hóa nội bộ mà JavaScript sử dụng (Unicode). Chúng ta sẽ quay lại chi tiết cụ thể và hậu quả của điều này trong chương [Strings](/string).

## [So sánh các kiểu khác nhau](#comparison-of-different-types)

Khi so sánh các giá trị của các kiểu khác nhau, JavaScript chuyển đổi các giá trị thành số.

Ví dụ:

```
alert( '2' > 1 ); // true, chuỗi '2' trở thành số 2
alert( '01' == 1 ); // true, chuỗi '01' trở thành số 1
```

Đối với các giá trị boolean, `true` trở thành `1` và `false` trở thành `0`.

Ví dụ:

```
alert( true == 1 ); // true
alert( false == 0 ); // true
```

Một hậu quả thú vị

Có thể xảy ra rằng cùng lúc:

- Hai giá trị bằng nhau.
- Một trong số chúng là `true` như một boolean và cái kia là `false` như một boolean.

Ví dụ:

```
let a = 0;
alert( Boolean(a) ); // false

let b = "0";
alert( Boolean(b) ); // true

alert(a == b); // true!
```

Từ quan điểm của JavaScript, kết quả này khá bình thường. Một phép kiểm tra bằng chuyển đổi giá trị bằng chuyển đổi số (do đó `"0"` trở thành `0`), trong khi chuyển đổi `Boolean` rõ ràng sử dụng một bộ quy tắc khác.

## [Bằngstrict](#strict-equality)

Một phép kiểm tra bằngregular `==` có một vấn đề. Nó không thể phân biệt `0` từ `false`:

```
alert( 0 == false ); // true
```

Cũng xảy ra với chuỗi rỗng:

```
alert( '' == false ); // true
```

Điều này xảy ra vì các operand của các kiểu khác nhau được chuyển đổi thành số bởi toán tử bằng `==`. Chuỗi rỗng, giống như `false`, trở thành không.

Làm thế nào nếu chúng ta muốn phân biệt `0` từ `false`?

**Một toán tử bằngstrict `===` kiểm tra bằng mà không có chuyển đổi kiểu.**

Nói cách khác, nếu `a` và `b` thuộc các kiểu khác nhau, thì `a === b` ngay lập tức trả về `false` mà không cần cố gắng chuyển đổi chúng.

Hãy thử nó:

```
alert( 0 === false ); // false, vì các kiểu khác nhau
```

Cũng có một toán tử “strict non-equality” `!==` tương tự như `!=`.

Toán tử bằngstrict dài hơn một chút để viết, nhưng làm rõ những gì đang xảy ra và để lại ít chỗ cho lỗi hơn.

## [So sánh với null và undefined](#comparison-with-null-and-undefined)

Có một hành vi khó hiểu khi `null` hoặc `undefined` được so sánh với các giá trị khác.

Đối với phép kiểm tra bằngstrict `===`
:   Các giá trị này khác nhau, vì mỗi cái là một kiểu khác nhau.

    ```
    alert( null === undefined ); // false
    ```

Đối với phép kiểm tra không strict `==`
:   Có một quy tắc đặc biệt. Hai cái này là một “cặp đôi ngọt ngào”: chúng bằng nhau (theo nghĩa của `==`), nhưng không bằng bất kỳ giá trị nào khác.

    ```
    alert( null == undefined ); // true
    ```

Đối với toán học và các so sánh khác `< > <= >=`
:   `null/undefined` được chuyển đổi thành số: `null` trở thành `0`, trong khi `undefined` trở thành `NaN`.

Bây giờ hãy xem một số điều thú vị xảy ra khi chúng ta áp dụng các quy tắc này. Và quan trọng hơn, làm thế nào để không rơi vào bẫy với chúng.

### [Kết quả kỳ lạ: null vs 0](#strange-result-null-vs-0)

Hãy so sánh `null` với không:

```
alert( null > 0 );  // (1) false
alert( null == 0 ); // (2) false
alert( null >= 0 ); // (3) true
```

Về mặt toán học, điều đó kỳ lạ. Kết quả cuối cùng nêu rằng “`null` lớn hơn hoặc bằng không”, vì vậy trong một trong các so sánh ở trên nó phải là `true`, nhưng cả hai đều sai.

Lý do là một phép kiểm tra bằng `==` và các so sánh `> < >= <=` làm việc khác nhau. Các phép so sánh chuyển đổi `null` thành số, coi nó là `0`. Đó là lý do tại sao (3) `null >= 0` là true và (1) `null > 0` là false.

Mặt khác, phép kiểm tra bằng `==` cho `undefined` và `null` được định nghĩa sao cho, mà không có bất kỳ chuyển đổi nào, chúng bằng nhau và không bằng bất kỳ giá trị nào khác. Đó là lý do tại sao (2) `null == 0` là false.

### [Một undefined không thể so sánh](#an-incomparable-undefined)

Giá trị `undefined` không nên được so sánh với các giá trị khác:

```
alert( undefined > 0 ); // false (1)
alert( undefined < 0 ); // false (2)
alert( undefined == 0 ); // false (3)
```

Tại sao nó ghét zero nhiều đến vậy? Luôn luôn false!

Chúng ta nhận được những kết quả này vì:

- Các so sánh `(1)` và `(2)` trả về `false` vì `undefined` được chuyển đổi thành `NaN` và `NaN` là một giá trị số đặc biệt trả về `false` cho tất cả các so sánh.
- Phép kiểm tra bằng `(3)` trả về `false` vì `undefined` chỉ bằng `null`, `undefined`, và không bằng giá trị nào khác.

### [Tránh vấn đề](#avoid-problems)

Tại sao chúng ta lại đi qua các ví dụ này? Chúng ta có nên nhớ các điểm đặc biệt này luôn không? Chà, không thực sự. Thực tế, những thứ tinh tế này sẽ dần trở nên quen thuộc theo thời gian, nhưng có một cách vững chắc để tránh vấn đề với chúng:

- Xử lý bất kỳ so sánh nào với `undefined/null` ngoại trừ strict equality `===` với sự cẩn thận đặc biệt.
- Không sử dụng các so sánh `>= > < <=` với một biến có thể là `null/undefined`, trừ khi bạn thực sự chắc chắn về những gì bạn đang làm. Nếu một biến có thể có các giá trị này, hãy kiểm tra chúng riêng.

## [Tổng kết](#summary)

- Các toán tử so sánh trả về một giá trị boolean.
- Các chuỗi được so sánh từng ký tự theo thứ tự “từ điển”.
- Khi các giá trị của các kiểu khác nhau được so sánh, chúng được chuyển đổi thành số (ngoại trừ phép kiểm tra bằngstrict).
- Các giá trị `null` và `undefined` bằng `==` với chính chúng và nhau, nhưng không bằng bất kỳ giá trị nào khác.
- Hãy cẩn thận khi sử dụng các so sánh như `>` hoặc `<` với các biến có thể thỉnh thoảng là `null/undefined`. Kiểm tra `null/undefined` riêng là một ý tưởng tốt.

---

---

## Các bài tập

## [Các bài tập](#tasks)

### [So sánh](#comparisons)

mức độ quan trọng: 5

Kết quả sẽ là gì cho các biểu thức này?

```
5 > 4
"apple" > "pineapple"
"2" > "12"
undefined == null
undefined === null
null == "\n0\n"
null === +"\n0\n"
```

lời giải

```
5 > 4 → true
"apple" > "pineapple" → false
"2" > "12" → true
undefined == null → true
undefined === null → false
null == "\n0\n" → false
null === +"\n0\n" → false
```

Một số lý do:

1. Hiển nhiên là true.
2. So sánh từ điển, do đó false. `"a"` nhỏ hơn `"p"`.
3. Một lần nữa, so sánh từ điển, ký tự đầu tiên `"2"` lớn hơn ký tự đầu tiên `"1"`.
4. Các giá trị `null` và `undefined` chỉ bằng nhau.
5. Bằngstrict thì nghiêm ngặt. Các kiểu khác nhau từ cả hai phía dẫn đến false.
6. Tương tự như `(4)`, `null` chỉ bằng `undefined`.
7. Bằngstrict của các kiểu khác nhau.
