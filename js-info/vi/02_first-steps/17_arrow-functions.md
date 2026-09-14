# Arrow functions, các cơ bản

> Nguồn: [https://javascript.info/arrow-functions-basics](https://javascript.info/arrow-functions-basics)

<!-- fetched: 2026-09-14 -->

Có một cú pháp rất đơn giản và gọn gàng khác để tạo hàm, thường tốt hơn Function Expressions.

Nó được gọi là "arrow functions", vì nó trông như thế này:

```
let func = (arg1, arg2, ..., argN) => expression;
```

Điều này tạo ra một hàm `func` chấp nhận các đối số `arg1..argN`, sau đó đánh giá biểu thức `expression` ở phía bên phải với việc sử dụng chúng và trả về kết quả của nó.

Nói cách khác, đó là phiên bản ngắn hơn của:

```
let func = function(arg1, arg2, ..., argN) {
  return expression;
};
```

Hãy xem một vígiụ cụ thể:

```
let sum = (a, b) => a + b;

/* Arrow function này là phiên bản ngắn hơn của:

let sum = function(a, b) {
  return a + b;
};
*/

alert( sum(1, 2) ); // 3
```

Như bạn có thể thấy, `(a, b) => a + b` có nghĩa là một hàm chấp nhận hai đối số có tên `a` và `b`. Khi thực thi, nó đánh giá biểu thức `a + b` và trả về kết quả.

- Nếu chúng ta có một đối số duy nhất, thì dấu ngoặc đơn xung quanh các tham số có thể bị bỏ qua, làm cho nó thậm chí ngắn hơn.

  Vígiụ:

  ```
  let double = n => n * 2;
  // xấp xỉ giống như: let double = function(n) { return n * 2 }

  alert( double(3) ); // 6
  ```
- Nếu không có đối số nào, dấu ngoặc đơn trống, nhưng chúng phải có mặt:

  ```
  let sayHi = () => alert("Xin chào!");

  sayHi();
  ```

Arrow functions có thể được sử dụng theo cùng cách như Function Expressions.

Vígiụ, để tạo động một hàm:

```
let age = prompt("Bạn bao nhiêu tuổi?", 18);

let welcome = (age < 18) ?
  () => alert('Xin chào!') :
  () => alert("Trân trọng!");

welcome();
```

Arrow functions có thể trông quen thuộc và không dễ đọc lúc đầu, nhưng điều đó nhanh chóng thay đổi khi mắt làm quen với cấu trúc.

Chúng rất tiện lợi cho các hành động một dòng đơn giản, khi chúng ta quá lười để viết nhiều từ.

## [Arrow functions nhiều dòng](#multiline-arrow-functions)

Các arrow functions mà chúng ta đã thấy cho đến nay rất đơn giản. Chúng nhận các đối số từ phía bên trái của `=>`, đánh giá và trả về biểu thức phía bên phải với chúng.

Đôi khi chúng ta cần một hàm phức tạp hơn, với nhiều biểu thức và câu lệnh. Trong trường hợp đó, chúng ta có thể bao bọc chúng trong dấu ngoặc nhọn. Sự khác biệt chính là dấu ngoặc nhọn yêu cầu một `return` bên trong chúng để trả về một giá trị (giống như một hàm thông thường).

Như thế này:

```
let sum = (a, b) => {  // dấu ngoặc nhọn mở một hàm nhiều dòng
  let result = a + b;
  return result; // nếu chúng ta sử dụng dấu ngoặc nhọn, thì cần một "return" rõ ràng
};

alert( sum(1, 2) ); // 3
```

Sắp tới có nhiều hơn

Ở đây chúng ta đã ca ngợi arrow functions vì sự ngắn gọn. Nhưng đó không phải là tất cả!

Arrow functions có các tính năng thú vị khác.

Để nghiên cứu chúng một cách chuyên sâu, chúng ta trước tiên cần làm quen với một số khía cạnh khác của JavaScript, vì vậy chúng ta sẽ quay lại arrow functions sau trong chương [Arrow functions revisited](/arrow-functions).

Hiện tại, chúng ta đã có thể sử dụng arrow functions cho các hành động một dòng và callbacks.

## [Tổng kết](#summary)

Arrow functions tiện lợi cho các hành động đơn giản, đặc biệt là các câu lệnh một dòng. Chúng có hai loại:

1. Không có dấu ngoặc nhọn: `(...args) => expression` – phía bên phải là một biểu thức: hàm đánh giá nó và trả về kết quả. Dấu ngoặc đơn có thể bị bỏ qua, nếu chỉ có một đối số duy nhất, vígiụ `n => n*2`.
2. Có dấu ngoặc nhọn: `(...args) => { body }` – dấu ngoặc cho phép chúng ta viết nhiều câu lệnh bên trong hàm, nhưng chúng ta cần một `return` rõ ràng để trả về cái gì đó.

---

---

## Các bài tập

## [Các bài tập](#tasks)

### [Viết lại với arrow functions](#rewrite-with-arrow-functions)

Thay thế Function Expressions bằng arrow functions trong mã dưới đây:

```
function ask(question, yes, no) {
  if (confirm(question)) yes();
  else no();
}

ask(
  "Bạn có đồng ý?",
  function() { alert("Bạn đã đồng ý."); },
  function() { alert("Bạn đã hủy việc thực thi."); }
);
```

lời giải

```
function ask(question, yes, no) {
  if (confirm(question)) yes();
  else no();
}

ask(
  "Bạn có đồng ý?",
  () => alert("Bạn đã đồng ý."),
  () => alert("Bạn đã hủy việc thực thi.")
);
```

Nhìn ngắn gọn và sạch sẽ, phải không?
