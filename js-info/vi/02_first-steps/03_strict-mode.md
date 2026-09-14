# Chế độ hiện đại, "use strict"

> Nguồn: [https://javascript.info/strict-mode](https://javascript.info/strict-mode)

<!-- fetched: 2026-09-14 -->

Trong một thời gian dài, JavaScript phát triển mà không có vấn đề tương thích. Các tính năng mới được thêm vào ngôn ngữ trong khi chức năng cũ không thay đổi.

Điều đó có lợi ích là không bao giờ phá vỡ mã hiện có. Nhưng nhược điểm là mọi sai sót hoặc quyết định không hoàn hảo được tạo ra bởi các nhà sáng tạo JavaScript bị mắc kẹt trong ngôn ngữ mãi mãi.

Đây là trường hợp cho đến năm 2009 khi ECMAScript 5 (ES5) xuất hiện. Nó thêm các tính năng mới vào ngôn ngữ và sửa đổi một số tính năng hiện có. Để giữ cho mã cũ hoạt động, hầu hết các sửa đổi như vậy đều tắt mặc định. Bạn cần phải bật chúng bằng cách sử dụng chỉ thị đặc biệt: `"use strict"`.

## ["use strict"](#use-strict)

Chỉ thị trông giống như một chuỗi: `"use strict"` hoặc `'use strict'`. Khi nó được đặt ở đầu script, toàn bộ script hoạt động theo cách “hiện đại”.

Ví dụ:

```
"use strict";

// mã này hoạt động theo cách hiện đại
...
```

Sớm thôi, chúng ta sẽ học hàm (một cách nhóm các lệnh), vì vậy hãy ghi chú trước rằng `"use strict"` có thể được đặt ở đầu một hàm. Làm như vậy kích hoạt chế độ strict trong hàm đó. Nhưng thường mọi người sử dụng nó cho toàn bộ script.

Đảm bảo rằng “use strict” ở đầu

Xin hãy đảm bảo rằng `"use strict"` ở đầu script của bạn, nếu không chế độ strict có thể không được kích hoạt.

Chế độ strict không được kích hoạt ở đây:

```
alert("some code");
// "use strict" bên dưới bị bỏ qua--nó phải ở đầu

"use strict";

// chế độ strict không được kích hoạt
```

Chỉ có comment mới có thể xuất hiện trên `"use strict"`.

Không có cách nào để hủy `use strict`

Không có chỉ thị nào như `"no use strict"` hoàn tác động cơ về hành vi cũ.

Một khi chúng ta vào chế độ strict, không có cách quay lại.

## [Console trình duyệt](#browser-console)

Khi bạn sử dụng [developer console](/devtools) để chạy mã, xin lưu ý rằng nó không `use strict` mặc định.

Đôi khi, khi `use strict` tạo ra sự khác biệt, bạn sẽ nhận được kết quả sai.

Vì vậy, làm thế nào để thực sự `use strict` trong console?

Đầu tiên, bạn có thể thử nhấn `Shift+Enter` để nhập nhiều dòng, và đặt `use strict` ở đầu, như thế này:

```
'use strict'; <Shift+Enter để xuống dòng>
//  ...mã của bạn
<Nhấn Enter để chạy>
```

Nó hoạt động trong hầu hết các trình duyệt, cụ thể là Firefox và Chrome.

Nếu nó không hoạt động, ví dụ trong một trình duyệt cũ, có một cách thô sơ nhưng đáng tin cậy để đảm bảo `use strict`. Đặt nó bên trong wrapper kiểu này:

```
(function() {
  'use strict';

  // ...mã của bạn ở đây...
})()
```

## [Chúng ta có nên "use strict"?](#should-we-use-strict)

Câu hỏi có vẻ hiển nhiên, nhưng không phải vậy.

Một người có thể khuyên bắt đầu scripts với `"use strict"`… Nhưng bạn biết gì thú vị không?

JavaScript hiện đại hỗ trợ “classes” và “modules” – các cấu trúc ngôn ngữ nâng cao (chúng ta chắc chắn sẽ đến với chúng), những cái cho phép `use strict` tự động. Vì vậy, chúng ta không cần thêm chỉ thị `"use strict"`, nếu chúng ta sử dụng chúng.

**Vì vậy, hiện tại, `"use strict";` là một khách mời welcome ở đầu script của bạn. Sau này, khi mã của bạn đều trong classes và modules, bạn có thể bỏ qua nó.**

Cho đến nay, chúng ta đã biết về `use strict` nói chung.

Trong các chương tiếp theo, khi chúng ta học các tính năng ngôn ngữ, chúng ta sẽ thấy sự khác biệt giữa chế độ strict và chế độ cũ. May mắn thay, có rất ít và chúng thực sự làm cuộc sống của chúng ta tốt hơn.

Tất cả các ví dụ trong khóa học này giả định chế độ strict trừ khi (rất hiếm) được chỉ định ngược lại.
