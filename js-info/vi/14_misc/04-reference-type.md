# Kiểu tham chiếu (Reference Type)

> Source: [https://javascript.info/reference-type](https://javascript.info/reference-type)

<!-- fetched: 2026-09-14 -->

Tính năng ngôn ngữ chuyên sâu

Bài viết này đề cập đến một chủ đề nâng cao, để hiểu rõ hơn các trường hợp biên.

Nó không quan trọng. Nhiều nhà phát triển có kinh nghiệm sống tốt mà không cần biết nó. Đọc tiếp nếu bạn muốn biết cách mọi thứ hoạt động phía sau.

Một cuộc gọi phương thức được đánh giá động có thể mất `this`.

Ví dụ:

```
let user = {
  name: "John",
  hi() { alert(this.name); },
  bye() { alert("Bye"); }
};

user.hi(); // works

// bây giờ hãy gọi user.hi hoặc user.bye tùy thuộc vào tên
(user.name == "John" ? user.hi : user.bye)(); // Error!
```

Ở dòng cuối cùng có một toán tử điều kiện chọn `user.hi` hoặc `user.bye`. Trong trường hợp này kết quả là `user.hi`.

Sau đó phương thức được gọi ngay lập tức với dấu ngoặc `()`. Nhưng nó không hoạt động chính xác!

Như bạn có thể thấy, cuộc gọi kết quả với lỗi, vì giá trị của `"this"` bên trong cuộc gọi trở thành `undefined`.

Điều này hoạt động (phương thức dot object):

```
user.hi();
```

Điều này không (phương thức evaluated):

```
(user.name == "John" ? user.hi : user.bye)(); // Error!
```

Tại sao? Nếu chúng ta muốn hiểu tại sao điều đó xảy ra, hãy đi vào nguyên nhân hoạt động của cuộc gọi `obj.method()`.

## [Kiểu tham chiếu được giải thích](#reference-type-explained)

Nhìn kỹ, chúng ta có thể nhận thấy hai thao tác trong câu lệnh `obj.method()`:

1. Đầu tiên, dấu chấm `'.'` truy xuất thuộc tính `obj.method`.
2. Sau đó dấu ngoặc `()` thực thi nó.

Vì vậy, làm thế nào thông tin về `this` được truyền từ phần đầu tiên sang phần thứ hai?

Nếu chúng ta đặt các thao tác này trên các dòng riêng biệt, thì `this` sẽ bị mất chắc chắn:

```
let user = {
  name: "John",
  hi() { alert(this.name); }
};

// chia việc lấy và gọi phương thức thành hai dòng
let hi = user.hi;
hi(); // Error, vì this là undefined
```

Ở đây `hi = user.hi` đặt hàm vào biến, và sau đó ở dòng cuối cùng nó hoàn toàn độc lập, vì vậy không có `this`.

**Để làm cho các cuộc gọi `user.hi()` hoạt động, JavaScript sử dụng một mẹo – dấu chấm `'.'` trả về không phải một hàm, mà là một giá trị của [Kiểu tham chiếu](https://tc39.github.io/ecma262/#sec-reference-specification-type) đặc biệt.**

Kiểu tham chiếu là một "kiểu đặc tả". Chúng ta không thể sử dụng nó một cách rõ ràng, nhưng nó được sử dụng nội bộ bởi ngôn ngữ.

Giá trị của Kiểu tham chiếu là sự kết hợp ba giá trị `(base, name, strict)`, trong đó:

- `base` là đối tượng.
- `name` là tên thuộc tính.
- `strict` là true nếu `use strict` đang được áp dụng.

Kết quả của truy xuất thuộc tính `user.hi` không phải là một hàm, mà là giá trị của Kiểu tham chiếu. Đối với `user.hi` trong chế độ strict nó là:

```
// Giá trị Kiểu tham chiếu
(user, "hi", true)
```

Khi dấu ngoặc `()` được gọi trên Kiểu tham chiếu, chúng nhận thông tin đầy đủ về đối tượng và phương thức của nó, và có thể đặt `this` đúng (`user` trong trường hợp này).

Kiểu tham chiếu là một loại "trung gian" đặc biệt nội bộ, với mục đích truyền thông tin từ dấu chấm `.` sang dấu ngoặc gọi `()`.

Bất kỳ thao tác nào khác như gán `hi = user.hi` loại bỏ kiểu tham chiếu hoàn toàn, lấy giá trị của `user.hi` (một hàm) và chuyển tiếp nó. Vì vậy bất kỳ thao tác nào sau đó "mất" `this`.

Vì vậy, kết quả là, giá trị của `this` chỉ được truyền đúng cách nếu hàm được gọi trực tiếp bằng cách sử dụng dấu chấm `obj.method()` hoặc dấu ngoặc vuông `obj['method']()` syntax (chúng làm cùng một điều ở đây). Có nhiều cách để giải quyết vấn đề này chẳng hạn như [func.bind()](/bind#solution-2-bind).

## [Tóm tắt](#summary)

Kiểu tham chiếu là một loại nội bộ của ngôn ngữ.

Đọc một thuộc tính, chẳng hạn như với dấu chấm `.` trong `obj.method()` trả về không chính xác giá trị thuộc tính, mà là một giá trị "kiểu tham chiếu" đặc biệt lưu trữ cả giá trị thuộc tính và đối tượng mà nó được lấy từ.

Điều đó là để cuộc gọi phương thức tiếp theo `()` có thể nhận đối tượng và đặt `this` thành nó.

Đối với tất cả các thao tác khác, kiểu tham chiếu tự động trở thành giá trị thuộc tính (một hàm trong trường hợp của chúng ta).

Toàn bộ cơ chế bị ẩn khỏi mắt chúng ta. Nó chỉ quan trọng trong các trường hợp tinh tế, chẳng hạn như khi một phương thức được lấy động từ đối tượng, bằng cách sử dụng một biểu thức.

---

---

## Bài tập

## [Các bài tập](#tasks)

### [Kiểm tra cú pháp](#syntax-check)

quan trọng: 2

Kết quả của mã này là gì?

```
let user = {
  name: "John",
  go: function() { alert(this.name) }
}

(user.go)()
```

P.S. Có một cái bẫy :)

lời giải

**Lỗi**!

Hãy thử:

```
let user = {
  name: "John",
  go: function() { alert(this.name) }
}

(user.go)() // error!
```

Thông báo lỗi trong hầu hết các trình duyệt không cho chúng ta nhiều manh mối về những gì đã đi sai.

**Lỗi xuất hiện vì thiếu dấu chấm phẩy sau `user = {...}`.**

JavaScript không tự động chèn dấu chấm phẩy trước một dấu ngoặc `(user.go)()`, vì vậy nó đọc mã như:

```
let user = { go:... }(user.go)()
```

Sau đó chúng ta cũng có thể thấy rằng biểu thức tổng hợp đó về mặt cú pháp là một cuộc gọi của đối tượng `{ go: ... }` như một hàm với đối số `(user.go)`. Và điều đó cũng xảy ra trên cùng một dòng với `let user`, vì vậy đối tượng `user` thậm chí chưa được định nghĩa, do đó có lỗi.

Nếu chúng ta chèn dấu chấm phẩy, mọi thứ đều ổn:

```
let user = {
  name: "John",
  go: function() { alert(this.name) }
};

(user.go)() // John
```

Xin lưu ý rằng các dấu ngoặc xung quanh `(user.go)` không làm gì ở đây. Thông thường chúng thiết lập thứ tự các thao tác, nhưng ở đây dấu chấm `.` hoạt động đầu tiên, vì vậy không có hiệu ứng. Chỉ có chuyện dấu chấm phẩy là quan trọng.

### [Giải thích giá trị của "this"](#explain-the-value-of-this)

quan trọng: 3

Trong mã dưới đây chúng ta dự định gọi phương thức `obj.go()` 4 lần liên tiếp.

Nhưng các cuộc gọi `(1)` và `(2)` hoạt động khác với `(3)` và `(4)`. Tại sao?

```
let obj, method;

obj = {
  go: function() { alert(this); }
};

obj.go();               // (1) [object Object]

(obj.go)();             // (2) [object Object]

(method = obj.go)();    // (3) undefined

(obj.go || obj.stop)(); // (4) undefined
```

lời giải

Dưới đây là các giải thích.

1. Đó là một cuộc gọi phương thức object thông thường.
2. Giống nhau, dấu ngoặc không thay đổi thứ tự các thao tác ở đây, dấu chấm là đầu tiên不管怎样.
3. Ở đây chúng ta có một cuộc gọi phức tạp hơn `(expression)()`. Cuộc gọi hoạt động như thể nó được chia thành hai dòng:

   ```
   f = obj.go; // tính toán biểu thức
   f();        // gọi những gì chúng ta có
   ```

   Ở đây `f()` được thực thi như một hàm, không có `this`.
4. Tương tự như `(3)`, ở bên trái của dấu ngoặc `()` chúng ta có một biểu thức.

Để giải thích hành vi của `(3)` và `(4)` chúng ta cần nhớ rằng các trình truy cập thuộc tính (dấu chấm hoặc ngoặc vuông) trả về giá trị của Kiểu tham chiếu.

Mọi thao tác trên nó ngoại trừ cuộc gọi phương thức (như gán `=` hoặc `||`) biến nó thành một giá trị thông thường, không mang thông tin cho phép đặt `this`.
