# Toán tử ghép không rỗng '??'

> Nguồn: [https://javascript.info/nullish-coalescing-operator](https://javascript.info/nullish-coalescing-operator)

<!-- fetched: 2026-09-14 -->

Một tính năng mới gần đây

Đây là một tính năng mới được thêm vào ngôn ngữ.
Các trình duyệt cũ có thể cần [polyfills](https://javascript.info/polyfills).

Toán tử ghép không rỗng được viết bằng hai dấu chấm hỏi `??`.

Vì nó xử lý `null` và `undefined` tương tự nhau, chúng ta sẽ sử dụng một thuật ngữ đặc biệt ở đây, trong bài viết này. Để ngắn gọn, chúng ta sẽ nói rằng một giá trị là "có giá trị" khi nó không phải là `null` nor `undefined`.

Kết quả của `a ?? b` là:

- nếu `a` có giá trị, thì `a`,
- nếu `a` không có giá trị, thì `b`.

Nói cách khác, `??` trả về đối số đầu tiên nếu nó không phải là `null/undefined`. Ngược lại, trả về đối số thứ hai.

Toán tử ghép không rỗng không phải là hoàn toàn mới. Nó chỉ là một cú pháp đẹp để lấy giá trị "có giá trị" đầu tiên trong hai giá trị.

Chúng ta có thể viết lại `result = a ?? b` bằng các toán tử mà chúng ta đã biết, như thế này:

```
result = (a !== null && a !== undefined) ? a : b;
```

Bây giờ phải tuyệt đối rõ ràng `??` làm gì. Hãy xem nó giúp đỡ ở đâu.

Trường hợp sử dụng phổ biến cho `??` là cung cấp giá trị mặc định.

Ví dụ, ở đây chúng ta hiển thị `user` nếu giá trị của nó không phải là `null/undefined`, nếu không thì hiển thị `Anonymous`:

```
let user;

alert(user ?? "Anonymous"); // Anonymous (user là undefined)
```

Đây là ví dụ với `user` được gán một tên:

```
let user = "John";

alert(user ?? "Anonymous"); // John (user không phải null/undefined)
```

Chúng ta cũng có thể sử dụng một chuỗi các `??` để chọn giá trị đầu tiên từ một danh sách mà không phải là `null/undefined`.

Giả sử chúng ta có dữ liệu người dùng trong các biến `firstName`, `lastName` hoặc `nickName`. Tất cả chúng đều có thể chưa được gán, nếu người dùng quyết định không điền các giá trị tương ứng.

Chúng ta muốn hiển thị tên người dùng bằng cách sử dụng một trong các biến này, hoặc hiển thị "Anonymous" nếu tất cả đều là `null/undefined`.

Hãy sử dụng toán tử `??` cho việc đó:

```
let firstName = null;
let lastName = null;
let nickName = "Supercoder";

// hiển thị giá trị có giá trị đầu tiên:
alert(firstName ?? lastName ?? nickName ?? "Anonymous"); // Supercoder
```

## [So sánh với \|\|](#comparison-with)

Toán tử HOẶC `||` có thể được sử dụng theo cùng cách như `??`, như đã mô tả trong [chương trước](/logical-operators#or-finds-the-first-truthy-value).

Vígiụ, trong mã ở trên chúng ta có thể thay thế `??` bằng `||` và vẫn nhận được kết quả giống hệt:

```
let firstName = null;
let lastName = null;
let nickName = "Supercoder";

// hiển thị giá trị truthy đầu tiên:
alert(firstName || lastName || nickName || "Anonymous"); // Supercoder
```

Về mặt lịch sử, toán tử HOẶC `||` có từ trước. Nó có từ đầu của JavaScript, vì vậy các nhà phát triển đã sử dụng nó cho các mục đích như vậy trong một thời gian dài.

Mặt khác, toán tử ghép không rỗng `??` chỉ được thêm vào JavaScript gần đây, và lý do cho việc đó là mọi người không hoàn toàn hài lòng với `||`.

Sự khác biệt quan trọng giữa chúng là:

- `||` trả về giá trị *truthy* đầu tiên.
- `??` trả về giá trị *có giá trị* đầu tiên.

Nói cách khác, `||` không phân biệt giữa `false`, `0`, chuỗi rỗng `""` và `null/undefined`. Tất cả đều giống nhau – các giá trị falsy. Nếu bất kỳ cái nào trong số này là đối số đầu tiên của `||`, thì chúng ta sẽ nhận được đối số thứ hai làm kết quả.

Trong thực tế, tuy nhiên, chúng ta có thể muốn sử dụng giá trị mặc định chỉ khi biến là `null/undefined`. Tức là, khi giá trị thực sự chưa được biết/chưa được đặt.

Ví dụ, hãy xem xét điều này:

```
let height = 0;

alert(height || 100); // 100
alert(height ?? 100); // 0
```

- `height || 100` kiểm tra `height` có phải là giá trị falsy không, và nó là `0`, đúng là falsy.
  - vì vậy kết quả của `||` là đối số thứ hai, `100`.
- `height ?? 100` kiểm tra `height` có phải là `null/undefined` không, và nó không phải,
  - vì vậy kết quả là `height` "nguyên vẹn", tức là `0`.

Trong thực tế, chiều cao bằng không thường là giá trị hợp lệ, không nên được thay thế bằng giá trị mặc định. Vì vậy `??` làm đúng những gì cần thiết.

## [Độ ưu tiên](#precedence)

Độ ưu tiên của toán tử `??` bằng với `||`. Cả hai đều bằng `3` trong [bảng MDN](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Operator_Precedence#Table).

Điều có nghĩa là, giống như `||`, toán tử ghép không rỗng `??` được đánh giá trước `=` và `?`, nhưng sau hầu hết các phép toán khác, như `+`, `*`.

Vì vậy, chúng ta có thể cần thêm dấu ngoặc đơn trong các biểu thức như thế này:

```
let height = null;
let width = null;

// quan trọng: sử dụng dấu ngoặc đơn
let area = (height ?? 100) * (width ?? 50);

alert(area); // 5000
```

Nếu không, nếu chúng ta bỏ qua dấu ngoặc đơn, thì vì `*` có độ ưu tiên cao hơn `??`, nó sẽ thực thi trước, dẫn đến kết quả sai.

```
// không có dấu ngoặc đơn
let area = height ?? 100 * width ?? 50;

// ...hoạt động theo cách này (không phải những gì chúng ta muốn):
let area = height ?? (100 * width) ?? 50;
```

### [Sử dụng ?? với && hoặc \|\|](#using-with-or)

Do lý do an toàn, JavaScript cấm sử dụng `??` cùng với các toán tử `&&` và `||`, trừ khi độ ưu tiên được chỉ định rõ ràng bằng dấu ngoặc đơn.

Mã dưới đây kích hoạt lỗi cú pháp:

```
let x = 1 && 2 ?? 3; // Lỗi cú pháp
```

Giới hạn này chắc chắn có thể tranh cãi, nó được thêm vào đặc tả ngôn ngữ với mục đích tránh lỗi lập trình, khi mọi người bắt đầu chuyển từ `||` sang `??`.

Sử dụng dấu ngoặc đơn rõ ràng để vượt qua nó:

```
let x = (1 && 2) ?? 3; // Hoạt động

alert(x); // 2
```

## [Tổng kết](#summary)

- Toán tử ghép không rỗng `??` cung cấp một cách ngắn gọn để chọn giá trị "có giá trị" đầu tiên từ một danh sách.

  Nó được sử dụng để gán giá trị mặc định cho các biến:

  ```
  // gán height=100, nếu height là null hoặc undefined
  height = height ?? 100;
  ```
- Toán tử `??` có độ ưu tiên rất thấp, chỉ cao hơn một chút so với `?` và `=`, vì vậy hãy cân nhắc thêm dấu ngoặc đơn khi sử dụng nó trong một biểu thức.
- Cấm sử dụng nó với `||` hoặc `&&` mà không có dấu ngoặc đơn rõ ràng.
