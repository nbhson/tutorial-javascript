# Tài liệu hướng dẫn và quy cách

> Nguồn: [https://javascript.info/manuals-specifications](https://javascript.info/manuals-specifications)

<!-- fetched: 2026-09-14 -->

Cuốn sách này là một *hướng dẫn*. Nó nhằm mục đích giúp bạn dần dần học ngôn ngữ. Nhưng một khi bạn đã quen thuộc với các khái niệm cơ bản, bạn sẽ cần các tài nguyên khác.

## [Quy cách](#specification)

[Quy cách ECMA-262](https://www.ecma-international.org/publications/standards/Ecma-262.htm) chứa thông tin chuyên sâu, chi tiết và chính thức nhất về JavaScript. Nó định nghĩa ngôn ngữ.

Nhưng vì tính chính thức cao như vậy, nó khó hiểu ở lần đầu tiên đọc. Vì vậy, nếu bạn cần nguồn thông tin đáng tin cậy nhất về các chi tiết của ngôn ngữ, quy cách là nơi đúng đắn. Nhưng nó không dành cho việc sử dụng hàng ngày.

Một phiên bản quy cách mới được phát hành mỗi năm. Giữa các lần phát hành, bản nháp quy cách mới nhất có tại <https://tc39.es/ecma262/>.

Để đọc về các tính năng mới nhất, bao gồm cả những tính năng "gần như đã chuẩn" (gọi là "stage 3"), hãy xem các đề xuất tại <https://github.com/tc39/proposals>.

Ngoài ra, nếu bạn đang phát triển cho trình duyệt, thì có các quy cách khác được đề cập trong [phần hai](/browser-environment) của hướng dẫn.

## [Tài liệu hướng dẫn](#manuals)

- **Tham khảo JavaScript của MDN (Mozilla)** là tài liệu hướng dẫn chính với các ví dụ và thông tin khác. Nó rất tốt để tìm hiểu thông tin chuyên sâu về các hàm, phương thức riêng lẻ của ngôn ngữ.

  Bạn có thể tìm thấy nó tại <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference>.

Tuy nhiên, thường thì tốt nhất là sử dụng công cụ tìm kiếm trên internet. Chỉ cần dùng "MDN [thuật ngữ]" trong truy vấn, ví dụ <https://google.com/search?q=MDN+parseInt> để tìm hàm `parseInt`.

## [Bảng tương thích](#compatibility-tables)

JavaScript là một ngôn ngữ đang phát triển, các tính năng mới được thêm vào thường xuyên.

Để xem mức độ hỗ trợ của chúng trong các trình thông dịch dựa trên trình duyệt và các trình thông dịch khác, hãy xem:

- <https://caniuse.com> – bảng hỗ trợ theo từng tính năng, ví dụ để xem trình thông dịch nào hỗ trợ các hàm mật mã hiện đại: <https://caniuse.com/#feat=cryptography>.
- <https://kangax.github.io/compat-table> – bảng các tính năng ngôn ngữ và các trình thông dịch hỗ trợ hoặc không hỗ trợ chúng.

Tất cả các tài nguyên này hữu ích trong phát triển thực tế, vì chúng chứa thông tin giá trị về các chi tiết ngôn ngữ, mức độ hỗ trợ, v.v.

Hãy nhớ chúng (hoặc trang này) cho các trường hợp khi bạn cần thông tin chuyên sâu về một tính năng cụ thể.
