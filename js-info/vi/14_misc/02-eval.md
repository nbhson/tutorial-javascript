# Eval: chạy mã dạng chuỗi

> Source: [https://javascript.info/eval](https://javascript.info/eval)

<!-- fetched: 2026-09-14 -->

Hàm tích hợp sẵn `eval` cho phép thực thi một chuỗi mã.

Cú pháp là:

```
let result = eval(code);
```

Ví dụ:

```
let code = 'alert("Hello")';
eval(code); // Hello
```

Một chuỗi mã có thể dài, chứa các ngắt dòng, khai báo hàm, biến và vân vân.

Kết quả của `eval` là kết quả của câu lệnh cuối cùng.

Ví dụ:

```
let value = eval('1+1');
alert(value); // 2
```

```
let value = eval('let i = 0; ++i');
alert(value); // 1
```

Mã được eval thực thi trong môi trườnglexical hiện tại, vì vậy nó có thể thấy các biến outer:

```
let a = 1;

function f() {
  let a = 2;

  eval('alert(a)'); // 2
}

f();
```

Nó cũng có thể thay đổi các biến outer:

```
let x = 5;
eval("x = 10");
alert(x); // 10, giá trị đã được sửa đổi
```

Trong chế độ strict, `eval` có môi trường lexical riêng. Vì vậy các hàm và biến, được khai báo bên trong eval, không khả dụng từ bên ngoài:

```
// reminder: 'use strict' is enabled in runnable examples by default

eval("let x = 5; function f() {}");

alert(typeof x); // undefined (không có variable như vậy)
// function f cũng không可见
```

Nếu không có `use strict`, `eval` không có môi trường lexical riêng, vì vậy chúng ta sẽ thấy `x` và `f` từ bên ngoài.

## [Sử dụng "eval"](#using-eval)

Trong lập trình hiện đại, `eval` được sử dụng rất hạn chế. Người ta thường nói rằng "eval là evil".

Lý do đơn giản: từ rất lâu, JavaScript là một ngôn ngữ yếu hơn nhiều, nhiều thứ chỉ có thể được thực hiện với `eval`. Nhưng thời gian đó đã qua một thập kỷ.

Hiện tại, gần như không có lý do gì để sử dụng `eval`. Nếu ai đó đang sử dụng nó, có khả năng cao họ có thể thay thế nó bằng một construct ngôn ngữ hiện đại hoặc [JavaScript Module](/modules).

Xin lưu ý rằng khả năng truy cập các biến outer của nó có các side-effects.

Các công cụ minify mã (được sử dụng trước khi JS được đưa vào production, để nén nó) đổi tên các biến local thành các tên ngắn hơn (như `a`, `b` v.v.) để làm cho mã nhỏ hơn. Điều đó thường an toàn, nhưng không nếu `eval` được sử dụng, vì các biến local có thể được truy cập từ chuỗi mã eval. Vì vậy các công cụ minify không thực hiện đổi tên đó cho tất cả các biến có thể可见 từ `eval`. Điều đó ảnh hưởng tiêu cực đến tỷ lệ nén mã.

Sử dụng các biến local outer bên trong `eval` cũng được coi là thực hành lập trình kém, vì nó làm cho việc bảo trì mã khó khăn hơn.

Có hai cách để hoàn toàn an toàn khỏi các vấn đề như vậy.

**Nếu mã eval không sử dụng các biến outer, xin vui lòng gọi `eval` dưới dạng `window.eval(...)`:**

Cách này mã được thực thi trong global scope:

```
let x = 1;
{
  let x = 5;
  window.eval('alert(x)'); // 1 (biến global)
}
```

**Nếu mã eval cần các biến local, thay đổi `eval` thành `new Function` và chuyển chúng làm đối số:**

```
let f = new Function('a', 'alert(a)');

f(5); // 5
```

Construct `new Function` được giải thích trong chương [Cú pháp "new Function"](../new-function). Nó tạo một hàm từ một chuỗi, cũng trong global scope. Vì vậy nó không thể thấy các biến local. Nhưng rõ ràng hơn nhiều khi chuyển chúng rõ ràng dưới dạng các đối số, như trong ví dụ ở trên.

## [Tóm tắt](#summary)

Một cuộc gọi đến `eval(code)` chạy chuỗi mã và trả về kết quả của câu lệnh cuối cùng.

- Hiếm khi được sử dụng trong JavaScript hiện đại, vì thường không có nhu cầu.
- Có thể truy cập các biến local outer. Điều đó được coi là thực hành không tốt.
- Thay vào đó, để eval mã trong global scope, sử dụng `window.eval(code)`.
- Hoặc, nếu mã của bạn cần một số dữ liệu từ outer scope, sử dụng `new Function` và chuyển nó dưới dạng các đối số.

---

---

## Bài tập

## [Các bài tập](#tasks)

### [Máy tính eval](#eval-calculator)

quan trọng: 4

Tạo một máy tính nhắc người dùng nhập một biểu thức toán học và trả về kết quả của nó.

Không cần kiểm tra tính đúng đắn của biểu thức trong bài tập này. Chỉ cần evaluate và trả về kết quả.

[Chạy bản demo](#)

lời giải

Hãy sử dụng `eval` để tính biểu thức toán học:

```
let expr = prompt("Type an arithmetic expression?", '2*3+2');

alert( eval(expr) );
```

Tuy nhiên, người dùng có thể nhập bất kỳ văn bản hoặc mã nào.

Để làm cho mọi thứ an toàn, và giới hạn nó chỉ với các phép tính số học, chúng ta có thể kiểm tra `expr` bằng cách sử dụng [regular expression](/regular-expressions), để nó chỉ có thể chứa chữ số và các toán tử.
