# Bảng điều khiển nhà phát triển

> Nguồn: [https://javascript.info/devtools](https://javascript.info/devtools)

<!-- fetched: 2026-09-14 -->

Mã nguồn dễ mắc lỗi. Bạn sẽ khá thường xuyên mắc lỗi… Ôi, tôi đang nói gì nhỉ? Bạn chắc chắn sẽ mắc lỗi, ít nhất là nếu bạn là con người, không phải [robot](https://en.wikipedia.org/wiki/Bender_(Futurama)).

Nhưng trong trình duyệt, người dùng không thấy lỗi theo mặc định. Vì vậy, nếu có gì đó sai hỏng trong kịch bản, chúng ta sẽ không thấy vấn đề gì và không thể sửa nó.

Để xem lỗi và nhận nhiều thông tin hữu ích khác về các kịch bản, "công cụ dành cho nhà phát triển" đã được tích hợp vào các trình duyệt.

Hầu hết các nhà phát triển chọn Chrome hoặc Firefox để phát triển vì những trình duyệt này có công cụ dành cho nhà phát triển tốt nhất. Các trình duyệt khác cũng cung cấp công cụ dành cho nhà phát triển, đôi khi với các tính năng đặc biệt, nhưng thường đang "đuổi theo" Chrome hoặc Firefox. Vì vậy, hầu hết các nhà phát triển có một trình duyệt "yêu thích" và chuyển sang trình duyệt khác nếu vấn đề mang tính đặc thù của trình duyệt.

Công cụ dành cho nhà phát triển rất mạnh; chúng có nhiều tính năng. Để bắt đầu, chúng ta sẽ học cách mở chúng, xem lỗi, và chạy các lệnh JavaScript.

## [Google Chrome](#google-chrome)
Mở trang [bug.html](/article/devtools/bug.html).

Có một lỗi trong mã JavaScript trên đó. Nó được ẩn khỏi mắt của một khách truy cập thông thường, vì vậy hãy mở công cụ dành cho nhà phát triển để xem nó.

Nhấn `F12` hoặc, nếu bạn đang dùng Mac, thì `Cmd+Opt+J`.

Công cụ dành cho nhà phát triển sẽ mở trên tab Console theo mặc định.

Nó trông giống như thế này:

![](/article/devtools/chrome.webp)

Hình dáng chính xác của công cụ dành cho nhà phát triển phụ thuộc vào phiên bản Chrome của bạn. Nó thay đổi theo thời gian nhưng sẽ tương tự.

- Ở đây chúng ta có thể thấy thông báo lỗi màu đỏ. Trong trường hợp này, kịch bản chứa lệnh "lalala" không xác định.
- Ở bên phải, có một liên kết có thể nhấp vào nguồn `bug.html:12` với số dòng nơi lỗi xảy ra.

Dưới thông báo lỗi, có ký hiệu `>` màu xanh. Nó đánh dấu một "dòng lệnh" nơi chúng ta có thể nhập các lệnh JavaScript. Nhấn `Enter` để chạy chúng.

Giờ chúng ta có thể xem lỗi, và đó đủ dùng để bắt đầu. Chúng ta sẽ quay lại với công cụ dành cho nhà phát triển sau và tìm hiểu sâu hơn về gỡ lỗi trong chương [Gỡ lỗi trong trình duyệt](/debugging-chrome).

Nhập nhiều dòng

Thông thường, khi chúng ta đặt một dòng mã vào bảng điều khiển, và sau đó nhấn `Enter`, nó sẽ thực thi.

Để chèn nhiều dòng, nhấn `Shift+Enter`. Bằng cách này, người ta có thể nhập các đoạn mã JavaScript dài.

## [Firefox, Edge, và các trình duyệt khác](#firefox-edge-and-others)

Hầu hết các trình duyệt khác sử dụng `F12` để mở công cụ dành cho nhà phát triển.

Cách hoạt động của chúng khá tương tự. Một khi bạn biết cách sử dụng một trong các công cụ này (bạn có thể bắt đầu với Chrome), bạn có thể dễ dàng chuyển sang cái khác.

## [Safari](#safari)
Safari (trình duyệt Mac, không hỗ trợ Windows/Linux) hơi đặc biệt ở đây. Chúng ta cần bật "Menu Develop" trước.

Mở Cài đặt và đi đến ngăn "Nâng cao". Có một hộp kiểm ở cuối:

![](/article/devtools/safari.png)

Giờ `Cmd+Opt+C` có thể chuyển đổi bảng điều khiển. Ngoài ra, lưu ý rằng mục menu mới có tên "Develop" đã xuất hiện. Nó có nhiều lệnh và tùy chọn.

## [Tóm tắt](#summary)

- Công cụ dành cho nhà phát triển cho phép chúng ta xem lỗi, chạy lệnh, kiểm tra các biến, và nhiều hơn nữa.
- Chúng có thể được mở bằng `F12` cho hầu hết các trình duyệt trên Windows. Chrome cho Mac cần `Cmd+Opt+J`, Safari: `Cmd+Opt+C` (cần bật trước).

Bây giờ chúng ta đã sẵn sàng môi trường. Trong phần tiếp theo, chúng ta sẽ đi vào JavaScript.
