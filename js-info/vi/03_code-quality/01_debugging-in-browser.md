# Gỡ lỗi trên trình duyệt

> Source: [https://javascript.info/debugging-chrome](https://javascript.info/debugging-chrome)

<!-- fetched: 2026-09-14 -->

Trước khi viết code phức tạp hơn, hãy nói về gỡ lỗi (debugging).

[Gỡ lỗi](https://en.wikipedia.org/wiki/Debugging) là quá trình tìm và sửa lỗi trong một script. Tất cả các trình duyệt hiện đại và hầu hết các môi trường khác đều hỗ trợ công cụ gỡ lỗi – một giao diện đặc biệt trong developer tools giúp việc gỡ lỗi dễ dàng hơn nhiều. Nó cũng cho phép chúng ta theo dõi từng bước thực thi của code để xem chính xác đang xảy ra điều gì.

Chúng ta sẽ sử dụng Chrome ở đây, vì nó có đủ tính năng, các trình duyệt khác cũng có quy trình tương tự.

## [Panel "Sources"](#the-sources-panel)

Phiên bản Chrome của bạn có thể hơi khác một chút, nhưng vẫn phải rõ ràng những gì có ở đó.

- Mở [trang ví dụ](/article/debugging-chrome/debugging/index.html) trong Chrome.
- Bật developer tools với `F12` (Mac: `Cmd+Opt+I`).
- Chọn panel `Sources`.

Đây là những gì bạn nên thấy nếu làm lần đầu tiên:

![](/article/debugging-chrome/chrome-open-sources.svg)

Nút toggle  mở tab với các file.

Hãy bấm vào nó và chọn `hello.js` trong cây thư mục. Đây là những gì sẽ hiện ra:

![](/article/debugging-chrome/chrome-tabs.svg)

Panel Sources có 3 phần:

1.-pane **File Navigator** liệt kê các file HTML, JavaScript, CSS và các file khác, bao gồm cả hình ảnh đính kèm vào trang. Các extension của Chrome cũng có thể xuất hiện ở đây.
2. pane **Code Editor** hiển thị source code.
3. pane **JavaScript Debugging** dùng để gỡ lỗi, chúng ta sẽ khám phá nó sớm.

Giờ bạn có thể bấm lại nút toggle  để ẩn danh sách tài nguyên và cho code thêm không gian.

## [Console](#console)

Nếu chúng ta nhấn `Esc`, thì một console sẽ mở ra bên dưới. Chúng ta có thể nhập lệnh ở đó và nhấn `Enter` để thực thi.

Sau khi một câu lệnh được thực thi, kết quả của nó sẽ được hiển thị bên dưới.

Ví dụ, ở đây `1+2` cho kết quả là `3`, còn hàm gọi `hello("debugger")` trả về không gì, nên kết quả là `undefined`:

![](/article/debugging-chrome/chrome-sources-console.svg)

## [Breakpoints](#breakpoints)

Hãy xem xét những gì đang xảy ra trong code của [trang ví dụ](/article/debugging-chrome/debugging/index.html). Trong `hello.js`, bấm vào số dòng `4`. Đúng vậy, bấm ngay vào chữ `4`, không phải vào code.

Chúc mừng! Bạn đã đặt một breakpoint. Vui lòng cũng bấm vào số dòng `8`.

Nó sẽ trông như thế này (màu xanh là nơi bạn nên bấm):

![](/article/debugging-chrome/chrome-sources-breakpoint.svg)

Một *breakpoint* là điểm trong code nơi debugger sẽ tự động tạm dừng việc thực thi JavaScript.

Trong khi code đang tạm dừng, chúng ta có thể kiểm tra các biến hiện tại, thực thi các lệnh trong console v.v. Nói cách khác, chúng ta có thể gỡ lỗi nó.

Chúng ta luôn có thể tìm thấy danh sách các breakpoint trong panel bên phải. Điều đó hữu ích khi chúng ta có nhiều breakpoint trong các file khác nhau. Nó cho phép chúng ta:

- Nhanh chóng nhảy đến breakpoint trong code (bằng cách bấm vào nó trong panel bên phải).
- Tạm thời vô hiệu hóa breakpoint bằng cách bỏ tích nó.
- Xóa breakpoint bằng cách bấm chuột phải và chọn Remove.
- …Và nhiều hơn nữa.

Conditional breakpoints

*Bấm chuột phải* vào số dòng cho phép tạo một *conditional* breakpoint. Nó chỉ kích hoạt khi biểu thức cho trước (mà bạn phải cung cấp khi tạo nó) là truthy.

Điều đó rất tiện khi chúng ta cần dừng lại chỉ cho một giá trị biến nhất định hoặc cho các đối số hàm nhất định.

## [Câu lệnh "debugger"](#the-command-debugger)

Chúng ta cũng có thể tạm dừng code bằng cách sử dụng câu lệnh `debugger` trong code, như thế này:

```
function hello(name) {
  let phrase = `Hello, ${name}!`;

  debugger;  // <-- debugger dừng tại đây

  say(phrase);
}
```

Câu lệnh như vậy chỉ hoạt động khi developer tools đang mở, nếu không trình duyệt sẽ bỏ qua nó.

## [Tạm dừng và quan sát](#pause-and-look-around)

Trong ví dụ của chúng ta, `hello()` được gọi trong quá trình tải trang, vì vậy cách dễ nhất để kích hoạt debugger (sau khi chúng ta đã đặt các breakpoint) là tải lại trang. Vì vậy, hãy nhấn `F5` (Windows, Linux) hoặc `Cmd+R` (Mac).

Khi breakpoint được đặt, việc thực thi sẽ tạm dừng ở dòng thứ 4:

![](/article/debugging-chrome/chrome-sources-debugger-pause.svg)

Vui lòng mở các dropdown thông tin bên phải (được đánh dấu bằng mũi tên). Chúng cho phép bạn kiểm tra trạng thái code hiện tại:

1. **`Watch` – hiển thị giá trị hiện tại cho bất kỳ biểu thức nào.**

   Bạn có thể bấm dấu cộng `+` và nhập một biểu thức. Debugger sẽ hiển thị giá trị của nó, tự động tính toán lại trong quá trình thực thi.
2. **`Call Stack` – hiển thị chuỗi các lời gọi lồng nhau.**

   Tại thời điểm hiện tại, debugger đang ở bên trong lời gọi `hello()`, được gọi bởi một script trong `index.html` (không có hàm ở đó, nên được gọi là "anonymous").

   Nếu bạn bấm vào một mục trong call stack (ví dụ: "anonymous"), debugger sẽ nhảy đến code tương ứng, và tất cả các biến của nó cũng có thể được kiểm tra.
3. **`Scope` – các biến hiện tại.**

   `Local` hiển thị các biến cục bộ của hàm. Bạn cũng có thể thấy giá trị của chúng được làm nổi bật ngay trên source code.

   `Global` có các biến toàn cục (ngoài mọi hàm).

   Cũng có từ khóa `this` ở đó mà chúng ta chưa học, nhưng chúng ta sẽ học sớm thôi.

## [Theo dõi quá trình thực thi](#tracing-the-execution)

Bây giờ là lúc *theo dõi* script.

Có các nút cho việc này ở đầu panel bên phải. Hãy sử dụng chúng.

– "Resume": tiếp tục thực thi, phím nóng `F8`.
:   Tiếp tục việc thực thi. Nếu không có breakpoint nào khác, thì việc thực thi sẽ tiếp tục và debugger mất kiểm soát.

    Đây là những gì chúng ta có thể thấy sau khi bấm vào nó:

    ![](/article/debugging-chrome/chrome-sources-debugger-trace-1.svg)

    Việc thực thi đã tiếp tục, đạt đến một breakpoint khác bên trong `say()` và tạm dừng ở đó. Hãy nhìn vào "Call Stack" ở bên phải. Nó đã tăng thêm một lời gọi nữa. Bây giờ chúng ta đang ở bên trong `say()`.

– "Step": chạy câu lệnh tiếp theo, phím nóng `F9`.
:   Chạy câu lệnh tiếp theo. Nếu chúng ta bấm nó bây giờ, `alert` sẽ được hiển thị.

    Bấm lại nhiều lần sẽ cho phép ta đi qua từng câu lệnh của script.

– "Step over": chạy câu lệnh tiếp theo, nhưng *không đi vào một hàm*, phím nóng `F10`.
:   Tương tự như lệnh "Step" trước đó, nhưng hành vi khác nếu câu lệnh tiếp theo là một lời gọi hàm (không phải hàm built-in, như `alert`, mà là hàm của chúng ta tự viết).

    Nếu so sánh chúng, lệnh "Step" đi vào một lời gọi hàm lồng nhau và tạm dừng việc thực thi ở dòng đầu tiên của nó, trong khi "Step over" thực thi lời gọi hàm lồng nhau một cách vô hình đối với chúng ta, bỏ qua chi tiết bên trong hàm.

    Việc thực thi sau đó sẽ tạm dừng ngay sau lời gọi hàm đó.

    Điều đó tốt nếu chúng ta không quan tâm đến việc xem những gì đang xảy ra bên trong lời gọi hàm.

– "Step into", phím nóng `F11`.
:   Tương tự như "Step", nhưng hành vi khác trong trường hợp các lời gọi hàm bất đồng bộ. Nếu bạn mới bắt đầu học JavaScript, thì bạn có thể bỏ qua sự khác biệt này, vì chúng ta chưa có lời gọi bất đồng bộ.

    Về sau, hãy ghi nhớ rằng lệnh "Step" bỏ qua các hành động bất đồng bộ, chẳng hạn như `setTimeout` (lời gọi hàm được lên lịch), thực thi sau đó. "Step into" sẽ đi vào code của chúng, chờ đợi nếu cần thiết. Xem [Tài liệu DevTools](https://developers.google.com/web/updates/2018/01/devtools#async) để biết thêm chi tiết.

– "Step out": tiếp tục thực thi đến cuối hàm hiện tại, phím nóng `Shift+F11`.
:   Tiếp tục việc thực thi và dừng nó ở dòng cuối cùng của hàm hiện tại. Điều đó rất tiện khi chúng ta vô tình đi vào một lời gọi lồng nhau bằng , nhưng nó không làm chúng ta quan tâm, và chúng ta muốn tiếp tục đến cuối của nó sớm nhất có thể.

– bật/tắt tất cả breakpoints.
:   Nút này không di chuyển việc thực thi. Chỉ là bật/tắt hàng loạt cho các breakpoint.

– bật/tắt tự động tạm dừng trong trường hợp có lỗi.
:   Khi được bật, nếu developer tools đang mở, lỗi trong quá trình thực thi script sẽ tự động tạm dừng nó. Sau đó chúng ta có thể phân tích các biến trong debugger để xem điều gì đã xảy ra sai. Vì vậy, nếu script của chúng ta bị lỗi, chúng ta có thể mở debugger, bật tùy chọn này và tải lại trang để xem nó bị lỗi ở đâu và bối cảnh lúc đó là gì.

Continue to here

Bấm chuột phải vào một dòng code mở menu ngữ cảnh với một tùy chọn tuyệt vời được gọi là "Continue to here".

Điều đó rất tiện khi chúng ta muốn di chuyển nhiều bước về phía trước đến dòng đó, nhưng chúng ta quá lười để đặt một breakpoint.

## [Logging](#logging)

Để xuất thứ gì đó ra console từ code của chúng ta, có hàm `console.log`.

Ví dụ, cái này xuất các giá trị từ `0` đến `4` ra console:

```
// mở console để xem
for (let i = 0; i < 5; i++) {
  console.log("value,", i);
}
```

Người dùng thông thường không thấy output đó, nó nằm trong console. Để xem nó, hãy mở panel Console của developer tools hoặc nhấn `Esc` khi đang ở panel khác: điều đó sẽ mở console ở phía dưới.

Nếu chúng ta có đủ logging trong code, thì chúng ta có thể thấy những gì đang xảy ra từ các bản ghi, mà không cần debugger.

## [Tổng kết](#summary)

Như chúng ta có thể thấy, có ba cách chính để tạm dừng một script:

1. Một breakpoint.
2. Các câu lệnh `debugger`.
3. Lỗi (nếu dev tools đang mở và nút  đang "bật").

Khi tạm dừng, chúng ta có thể gỡ lỗi: kiểm tra các biến và theo dõi code để xem nơi thực thi bị sai.

Có nhiều tùy chọn hơn trong developer tools so với những gì được đề cập ở đây. Tài liệu đầy đủ có tại <https://developers.google.com/web/tools/chrome-devtools>.

Thông tin từ chương này là đủ để bắt đầu gỡ lỗi, nhưng sau này, đặc biệt nếu bạn làm nhiều việc với trình duyệt, vui lòng vào đó và xem qua các khả năng nâng cao hơn của developer tools.

À, và bạn cũng có thể bấm vào các vị trí khác nhau trong dev tools và chỉ xem những gì hiển thị. Đó có lẽ là cách nhanh nhất để học dev tools. Đừng quên bấm chuột phải và các menu ngữ cảnh!
