# Global object

> Source: [https://javascript.info/global-object](https://javascript.info/global-object)

<!-- fetched: 2026-09-14 -->

Global object cung cấp các biến và hàm có thể truy cập ở bất kỳ đâu. Theo mặc định, những thứ được tích hợp sẵn trong ngôn ngữ hoặc môi trường.

Trong trình duyệt nó được gọi là `window`, trong Node.js là `global`, còn các môi trường khác có thể có tên khác.

Gần đây, `globalThis` đã được thêm vào ngôn ngữ như một tên chuẩn cho global object, và sẽ được hỗ trợ trên mọi môi trường. Nó được hỗ trợ trong tất cả các trình duyệt chính.

Chúng ta sẽ sử dụng `window` ở đây, giả sử môi trường của ta là trình duyệt. Nếu script của bạn có thể chạy trên các môi trường khác, tốt hơn là nên dùng `globalThis`.

Tất cả các property của global object có thể được truy cập trực tiếp:

```
alert("Hello");
// tương đương với
window.alert("Hello");
```

Trong trình duyệt, các hàm và biến toàn cục được khai báo bằng `var` (không phải `let/const`!) sẽ trở thành property của global object:

```
var gVar = 5;

alert(window.gVar); // 5 (trở thành property của global object)
```

Function declarations cũng có cùng hiệu ứng (các câu lệnh có từ khóa `function` trong luồng code chính, không phải function expressions).

Đừng phụ thuộc vào điều này! Hành vi này tồn tại vì lý do tương thích. Các script hiện đại sử dụng [JavaScript modules](/modules) nơi mà điều này không xảy ra.

Nếu ta dùng `let` thay thế, điều đó sẽ không xảy ra:

```
let gLet = 5;

alert(window.gLet); // undefined (không trở thành property của global object)
```

Nếu một giá trị quan trọng đến mức bạn muốn nó có sẵn ở toàn cục, hãy gán trực tiếp như một property:

```
// làm thông tin user hiện tại thành global, để tất cả scripts đều có thể truy cập
window.currentUser = {
  name: "John"
};

// ở đâu đó trong code
alert(currentUser.name);  // John

// hoặc, nếu ta có một biến local với tên "currentUser"
// lấy nó từ window một cách rõ ràng (an toàn!)
alert(window.currentUser.name); // John
```

Tuy nhiên, việc sử dụng global variables nói chung không được khuyến khích. Nên có càng ít global variables càng tốt. Thiết kế code mà một hàm nhận các biến "đầu vào" và tạo ra "đầu ra" nhất định rõ ràng hơn, ít bị lỗi hơn và dễ test hơn so với việc sử dụng các biến ngoài hoặc biến toàn cục.

## [Sử dụng cho polyfills](#using-for-polyfills)

Ta sử dụng global object để kiểm tra khả năng hỗ trợ các tính năng hiện đại của ngôn ngữ.

Ví dụ, kiểm tra xem object `Promise` tích hợp có tồn tại không (nó không tồn tại trong các trình duyệt rất cũ):

```
if (!window.Promise) {
  alert("Trình duyệt của bạn quá cũ!");
}
```

Nếu không có (giả sử ta đang dùng trình duyệt cũ), ta có thể tạo "polyfills": thêm các hàm mà môi trường không hỗ trợ nhưng có trong tiêu chuẩn hiện đại.

```
if (!window.Promise) {
  window.Promise = ... // cài đặt tùy chỉnh cho tính năng ngôn ngữ hiện đại
}
```

## [Tóm tắt](#summary)

- Global object lưu trữ các biến cần có sẵn ở mọi nơi.

  Bao gồm các tích hợp sẵn của JavaScript như `Array` và các giá trị đặc thù môi trường như `window.innerHeight` – chiều cao cửa sổ trong trình duyệt.
- Global object có tên phổ quát là `globalThis`.

  …Nhưng thường được gọi bằng các tên "cổ điển" đặc thù môi trường, như `window` (trình duyệt) và `global` (Node.js).
- Ta chỉ nên lưu trữ giá trị trong global object khi chúng thực sự toàn cục cho dự án của ta. Và giữ số lượng ở mức tối thiểu.
- Trong trình duyệt, trừ khi ta dùng [modules](/modules), các hàm và biến toàn cục được khai báo bằng `var` sẽ trở thành property của global object.
- Để code tương lai và dễ hiểu hơn, ta nên truy cập các property của global object một cách trực tiếp, như `window.x`.
