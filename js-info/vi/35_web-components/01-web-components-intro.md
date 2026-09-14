# Giới thiệu Web Components

> Source: [https://javascript.info/webcomponents-intro](https://javascript.info/webcomponents-intro)

<!-- fetched: 2026-09-14 -->

Phần này mô tả một tập hợp các tiêu chuẩn hiện đại dành cho “web components”.

Cho đến thời điểm hiện tại, các tiêu chuẩn này vẫn đang được phát triển. Một số tính năng đã được hỗ trợ tốt và tích hợp vào tiêu chuẩn HTML/DOM hiện đại, trong khi số khác vẫn ở giai đoạn dự thảo. Bạn có thể thử các ví dụ trên bất kỳ trình duyệt nào, Google Chrome có lẽ là trình duyệt cập nhật nhất các tính năng này. Có lẽ là vì các đồng nghiệp của Google đứng sau nhiều quy tắc liên quan.

## [Cái gì chung giữa…](#what-s-common-between)

Toàn bộ ý tưởng về component không có gì mới. Nó được sử dụng trong nhiều framework và ở nhiều nơi khác.

Trước khi đi vào chi tiết triển khai, hãy xem thành tựu vĩ đại này của nhân loại:

![](/article/webcomponents-intro/satellite.jpg)

Đó là Trạm Không gian Quốc tế (ISS).

Và đây là cách nó được tạo ra bên trong (xấp xỉ):

![](/article/webcomponents-intro/satellite-expanded.jpg)

Trạm Không gian Quốc tế:

- Gồm nhiều component.
- Mỗi component, đến lượt mình, lại có nhiều chi tiết nhỏ hơn bên trong.
- Các component rất phức tạp, phức tạp hơn nhiều so với hầu hết các website.
- Các component được phát triển quốc tế, bởi các đội từ các quốc gia khác nhau, nói các ngôn ngữ khác nhau.

…Và thứ này bay được, giữ con người sống trong không gian!

Những thiết bị phức tạp như vậy được tạo ra như thế nào?

Những nguyên tắc nào chúng ta có thể mượn để làm cho sự phát triển của mình đáng tin cậy và mở rộng quy mô ở cùng cấp độ? Hoặc ít nhất là gần với nó?

## [Kiến trúc component](#component-architecture)

Quy tắc nổi tiếng khi phát triển phần mềm phức tạp là: đừng tạo phần mềm phức tạp.

Nếu thứ gì đó trở nên phức tạp – hãy chia nó thành các phần đơn giản hơn và kết nối theo cách rõ ràng nhất.

**Một kiến trúc sư giỏi là người có thể làm cho cái phức tạp trở nên đơn giản.**

Chúng ta có thể chia giao diện người dùng thành các component trực quan: mỗi component có vị trí riêng trên trang, có thể “thực hiện” một nhiệm vụ được mô tả rõ ràng, và tách biệt với các component khác.

Hãy xem một website, ví dụ như Twitter.

Nó tự nhiên được chia thành các component:

![](/article/webcomponents-intro/web-components-twitter.svg)

1. Điều hướng phía trên.
2. Thông tin người dùng.
3. Gợi ý theo dõi.
4. Biểu mẫu gửi.
5. (và cả 6, 7) – tin nhắn.

Các component có thể có subcomponent, ví dụ tin nhắn có thể là phần của một component “danh sách tin nhắn” ở cấp cao hơn. Ảnh người dùng có thể click được tự nó có thể là một component, và cứ thế.

Làm sao chúng ta quyết định, cái gì là một component? Điều đó đến từ trực giác, kinh nghiệm và sự thông thường. Thông thường đó là một thực thể trực quan riêng biệt mà chúng ta có thể mô tả bằng cách nó làm gì và tương tác với trang như thế nào. Trong trường hợp trên, trang có các khối, mỗi khối đóng vai trò riêng, hợp lý để biến chúng thành component.

Một component có:

- Class JavaScript riêng.
- Cấu trúc DOM, được quản lý duy nhất bởi class của nó, mã bên ngoài không truy cập (“nguyên tắc encapsulation”).
- Style CSS, được áp dụng cho component.
- API: events, phương thức class, v.v., để tương tác với các component khác.

Một lần nữa, toàn bộ chuyện “component” không có gì đặc biệt.

Có nhiều framework và phương pháp phát triển để xây dựng chúng, mỗi cái có những điểm nổi bật riêng. Thông thường, các class CSS và quy ước đặc biệt được sử dụng để cung cấp “cảm giác component” – CSS scoping và DOM encapsulation.

“Web components” cung cấp các khả năng tích hợp sẵn của trình duyệt cho điều đó, nên chúng ta không cần phải giả lập chúng nữa.

- [Custom elements](https://html.spec.whatwg.org/multipage/custom-elements.html#custom-elements) – để định nghĩa các phần tử HTML tùy chỉnh.
- [Shadow DOM](https://dom.spec.whatwg.org/#shadow-trees) – để tạo một DOM nội bộ cho component, ẩn khỏi các phần khác.
- [CSS Scoping](https://drafts.csswg.org/css-scoping/) – để khai báo các style chỉ áp dụng bên trong Shadow DOM của component.
- [Event retargeting](https://dom.spec.whatwg.org/#retarget) và một số thứ phụ nhỏ khác để khiến các component tùy chỉnh phù hợp hơn với sự phát triển.

Trong chương tiếp theo chúng ta sẽ đi sâu vào chi tiết của “Custom Elements” – tính năng nền tảng và được hỗ trợ tốt của web components, tốt ngay cả khi dùng một mình.
