# BigInt

> Source: [https://javascript.info/bigint](https://javascript.info/bigint)

<!-- fetched: 2026-09-14 -->

Một bổ sung gần đây

Đây là một bổ sung gần đây cho ngôn ngữ.
Bạn có thể tìm trạng thái hỗ trợ hiện tại tại <https://caniuse.com/#feat=bigint>.

`BigInt` là một loại số đặc biệt cung cấp hỗ trợ cho các số nguyên có độ dài tùy ý.

Một bigint được tạo bằng cách gắn `n` vào cuối một literal số nguyên hoặc bằng cách gọi hàm `BigInt` tạo các bigint từ strings, numbers v.v.

```
const bigint = 1234567890123456789012345678901234567890n;

const sameBigint = BigInt("1234567890123456789012345678901234567890");

const bigintFromNumber = BigInt(10); // same as 10n
```

## [Các toán tử toán học](#math-operators)

`BigInt` chủ yếu có thể được sử dụng giống như một số thông thường, ví dụ:

```
alert(1n + 2n); // 3

alert(5n / 2n); // 2
```

Xin lưu ý: phép chia `5/2` trả về kết quả làm tròn về phía zero, không có phần thập phân. Tất cả các thao tác trên các bigint trả về các bigint.

Chúng ta không thể trộn bigint và số thông thường:

```
alert(1n + 2); // Error: Cannot mix BigInt and other types
```

Chúng ta nên chuyển đổi chúng một cách rõ ràng nếu cần: sử dụng `BigInt()` hoặc `Number()`, như thế này:

```
let bigint = 1n;
let number = 2;

// number to bigint
alert(bigint + BigInt(number)); // 3

// bigint to number
alert(Number(bigint) + number); // 3
```

Các thao tác chuyển đổi luôn im lặng, không bao giờ cho lỗi, nhưng nếu bigint quá lớn và không vừa với kiểu số, thì các bit thừa sẽ bị cắt, vì vậy chúng ta nên cẩn thận khi thực hiện chuyển đổi như vậy.

Unary plus không được hỗ trợ trên các bigint

Toán tử unary `+value` là một cách đã biết để chuyển đổi `value` thành một số.

Để tránh nhầm lẫn, nó không được hỗ trợ trên các bigint:

```
let bigint = 1n;

alert( +bigint ); // error
```

Vì vậy chúng ta nên sử dụng `Number()` để chuyển đổi một bigint thành một số.

## [So sánh](#comparisons)

Các phép so sánh, chẳng hạn như `<`, `>` hoạt động tốt với các bigint và số:

```
alert( 2n > 1n ); // true

alert( 2n > 1 ); // true
```

Tuy nhiên xin lưu ý, vì số và bigint thuộc về các kiểu khác nhau, chúng có thể bằng nhau `==`, nhưng không nghiêm ngặt bằng nhau `===`:

```
alert( 1 == 1n ); // true

alert( 1 === 1n ); // false
```

## [Các thao tác boolean](#boolean-operations)

Khi ở bên trong `if` hoặc các thao tác boolean khác, các bigint hoạt động giống như các số.

Ví dụ, trong `if`, bigint `0n` là falsy, các giá trị khác là truthy:

```
if (0n) {
  // never executes
}
```

Các toán tử boolean, chẳng hạn như `||`, `&&` và các toán tử khác cũng hoạt động với các bigint tương tự như các số:

```
alert( 1n || 2 ); // 1 (1n được coi là truthy)

alert( 0n || 2 ); // 2 (0n được coi là falsy)
```

## [Polyfills](#polyfills)

Polyfilling các bigint là khó khăn. Lý do là nhiều toán tử JavaScript, chẳng hạn như `+`, `-` và vân vân hoạt động khác nhau với các bigint so với các số thông thường.

Ví dụ, phép chia của các bigint luôn trả về một bigint (làm tròn nếu cần).

Để mô phỏng hành vi như vậy, một polyfill sẽ cần phân tích mã và thay thế tất cả các toán tử đó bằng các hàm của nó. Nhưng làm như vậy là cồng kềnh và sẽ tốn nhiều hiệu suất.

Vì vậy, không có polyfill tốt nào được biết đến.

Tuy nhiên, cách ngược lại được đề xuất bởi các nhà phát triển của thư viện [JSBI](https://github.com/GoogleChromeLabs/jsbi).

Thư viện này implement các số lớn bằng các phương thức riêng của nó. Chúng ta có thể sử dụng chúng thay vì các bigint native:

| Thao tác | `BigInt` native | JSBI |
| --- | --- | --- |
| Creation from Number | `a = BigInt(789)` | `a = JSBI.BigInt(789)` |
| Addition | `c = a + b` | `c = JSBI.add(a, b)` |
| Subtraction | `c = a - b` | `c = JSBI.subtract(a, b)` |
| … | … | … |

…Và sau đó sử dụng polyfill (Babel plugin) để chuyển đổi các lời gọi JSBI thành các bigint native cho那些 trình duyệt hỗ trợ chúng.

Nói cách khác, cách tiếp cận này gợi ý rằng chúng ta viết mã trong JSBI thay vì các bigint native. Nhưng JSBI làm việc với các số như với các bigint nội bộ, mô phỏng chúng theo cách chặt chẽ theo đặc tả, vì vậy mã sẽ "sẵn sàng bigint".

Chúng ta có thể sử dụng mã JSBI như vậy "nguyên bản" cho những engine không hỗ trợ bigint và cho những engine hỗ trợ – polyfill sẽ chuyển đổi các lời gọi thành các bigint native.

## [Tham khảo](#references)

- [Tài liệu MDN về BigInt](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/BigInt).
- [Đặc tả](https://tc39.es/ecma262/#sec-bigint-objects).
