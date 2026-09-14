# Backreference trong pattern: \N và \k<name>

> Source: [https://javascript.info/regexp-backreferences](https://javascript.info/regexp-backreferences)

<!-- fetched: 2026-09-14 -->

Ta có thể sử dụng nội dung của capturing group `(...)` không chỉ trong kết quả hay trong chuỗi thay thế, mà ngay cả trong chính pattern.

## [Backreference theo số: \N](#backreference-by-number-n)

Một group có thể được tham chiếu trong pattern bằng `\N`, trong đó `N` là số của group.

Để làm rõ tại sao điều đó hữu ích, hãy xem xét một bài toán.

Ta cần tìm các chuỗi có dấu nháy: hoặc nháy đơn `'...'` hoặc nháy đôi `"..."` – cả hai biến thể đều phải khớp.

Làm thế nào để tìm chúng?

Ta có thể đặt cả hai loại dấu nháy trong dấu ngoặc vuông: `['"](.*?)['"]`, nhưng nó sẽ tìm ra các chuỗi có dấu nháy lẫn lộn, như `"...'` và `'..."`. Điều đó dẫn đến các kết quả khớp sai khi một dấu nháy xuất hiện bên trong dấu nháy khác, như trong chuỗi `"She's the one!"`:

```
let str = `He said: "She's the one!".`;

let regexp = /['"](.*?)['"]/g;

// The result is not what we'd like to have
alert( str.match(regexp) ); // "She'
```

Như ta thấy, pattern đã tìm thấy dấu nháy mở `"`, rồi văn bản được tiêu thụ cho đến dấu nháy khác `'`, dấu đó đóng kết quả khớp.

Để đảm bảo rằng pattern tìm dấu nháy đóng giống hệt với dấu nháy mở, ta có thể bọc nó trong một capturing group và backreference nó: `(['"])(.*?)\1`.

Đây là mã đúng:

```
let str = `He said: "She's the one!".`;

let regexp = /(['"])(.*?)\1/g;

alert( str.match(regexp) ); // "She's the one!"
```

Giờ nó hoạt động! Engine regular expression tìm thấy dấu nháy đầu tiên `(['"])` và ghi nhớ nội dung của nó. Đó là capturing group thứ nhất.

Xa hơn trong pattern, `\1` có nghĩa là “tìm cùng văn bản như trong group thứ nhất”, chính xác là cùng dấu nháy trong trường hợp của ta.

Tương tự, `\2` sẽ có nghĩa là nội dung của group thứ hai, `\3` – group thứ ba, và cứ thế.

Lưu ý:

Nếu ta dùng `?:` trong group, thì ta không thể tham chiếu nó. Các group bị loại khỏi capturing `(?:...)` không được engine ghi nhớ.

Đừng nhầm lẫn: trong pattern dùng `\1`, trong thay thế: `$1`

Trong chuỗi thay thế ta dùng ký tự dollar: `$1`, trong khi trong pattern – dùng backslash `\1`.

## [Backreference theo tên: `\k<name>`](#backreference-by-name-k)

Nếu regexp có nhiều dấu ngoặc, sẽ tiện khi đặt tên cho chúng.

Để tham chiếu một named group, ta có thể dùng `\k<name>`.

Trong ví dụ bên dưới, group chứa dấu nháy được đặt tên `?<quote>`, nên backreference là `\k<quote>`:

```
let str = `He said: "She's the one!".`;

let regexp = /(?<quote>['"])(.*?)\k<quote>/g;

alert( str.match(regexp) ); // "She's the one!"
```
