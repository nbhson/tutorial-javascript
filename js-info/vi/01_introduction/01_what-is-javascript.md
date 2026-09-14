# Giới thiệu về JavaScript

> Nguồn: [https://javascript.info/intro](https://javascript.info/intro)

<!-- fetched: 2026-09-14 -->

Hãy cùng tìm hiểu xem JavaScript có gì đặc biệt, chúng ta có thể đạt được những gì với nó, và những công nghệ nào tương thích tốt với nó.

## [JavaScript là gì?](#what-is-javascript)

*JavaScript* ban đầu được tạo ra để "làm cho các trang web sống động".

Các chương trình trong ngôn ngữ này được gọi là *kịch bản* (scripts). Chúng có thể được viết trực tiếp trong HTML của trang web và chạy tự động khi trang được tải.

Các kịch bản được cung cấp và thực thi dưới dạng văn bản thuần túy. Chúng không cần chuẩn bị đặc biệt hoặc biên dịch để chạy.

Về phương diện này, JavaScript rất khác biệt so với một ngôn ngữ khác được gọi là [Java](https://en.wikipedia.org/wiki/Java_(programming_language)).

Tại sao lại gọi là JavaScript?

Khi JavaScript được tạo ra, ban đầu nó có một tên khác: "LiveScript". Nhưng Java rất phổ biến vào thời điểm đó, nên người ta quyết định định vị ngôn ngữ mới này như một "em trai" của Java sẽ giúp ích cho việc quảng bá.

Nhưng khi phát triển, JavaScript đã trở thành một ngôn ngữ hoàn toàn độc lập với quy cách riêng gọi là [ECMAScript](http://en.wikipedia.org/wiki/ECMAScript), và hiện nay nó không còn liên quan gì đến Java.

Ngày nay, JavaScript có thể chạy không chỉ trong trình duyệt, mà còn trên máy chủ, hoặc thực tế là trên bất kỳ thiết bị nào có một chương trình đặc biệt gọi là [trình thông dịch JavaScript](https://en.wikipedia.org/wiki/JavaScript_engine).

Trình duyệt có một trình thông dịch tích hợp đôi khi được gọi là "máy ảo JavaScript".

Các trình thông dịch khác nhau có các "bí danh" khác nhau. Ví dụ:

- [V8](https://en.wikipedia.org/wiki/V8_(JavaScript_engine)) – trong Chrome, Opera và Edge.
- [SpiderMonkey](https://en.wikipedia.org/wiki/SpiderMonkey) – trong Firefox.
- …Có các bí danh khác như "Chakra" cho IE, "JavaScriptCore", "Nitro" và "SquirrelFish" cho Safari, v.v.

Các thuật ngữ trên đáng để ghi nhớ vì chúng được sử dụng trong các bài viết dành cho nhà phát triển trên internet. Chúng ta cũng sẽ sử dụng chúng. Ví dụ, nếu "tính năng X được V8 hỗ trợ", thì có lẽ nó hoạt động trong Chrome, Opera và Edge.

Các trình thông dịch hoạt động như thế nào?

Các trình thông dịch rất phức tạp. Nhưng cơ bản thì dễ hiểu.

1. Trình thông dịch (tích hợp nếu là trong trình duyệt) đọc ("phân tích cú pháp") kịch bản.
2. Sau đó nó chuyển đổi ("biên dịch") kịch bản sang mã máy.
3. Và sau đó mã máy chạy, khá nhanh.

Trình thông dịch áp dụng các phép tối ưu hóa ở mỗi bước của quá trình. Nó thậm chí theo dõi kịch bản đã được biên dịch khi nó chạy, phân tích dữ liệu chảy qua nó, và tối ưu hóa thêm mã máy dựa trên kiến thức đó.

## [JavaScript trong trình duyệt có thể làm được những gì?](#what-can-in-browser-javascript-do)

JavaScript hiện đại là một ngôn ngữ lập trình "an toàn". Nó không cung cấp quyền truy cập cấp thấp vào bộ nhớ hoặc CPU, vì ban đầu nó được tạo ra cho các trình duyệt không yêu cầu điều đó.

Khả năng của JavaScript phụ thuộc rất nhiều vào môi trường mà nó chạy trong. Ví dụ, [Node.js](https://wikipedia.org/wiki/Node.js) hỗ trợ các hàm cho phép JavaScript đọc/ghi các file tùy ý, thực hiện các yêu cầu mạng, v.v.

JavaScript trong trình duyệt có thể làm mọi thứ liên quan đến thao tác trang web, tương tác với người dùng, và máy chủ web.

Ví dụ, JavaScript trong trình duyệt có thể:

- Thêm HTML mới vào trang, thay đổi nội dung hiện có, sửa đổi kiểu dáng.
- Phản ứng với các hành động của người dùng, chạy khi nhấp chuột, di chuyển con trỏ, nhấn phím.
- Gửi yêu cầu qua mạng đến máy chủ từ xa, tải xuống và tải lên tệp (các công nghệ gọi là [AJAX](https://en.wikipedia.org/wiki/Ajax_(programming)) và [COMET](https://en.wikipedia.org/wiki/Comet_(programming))).
- Lấy và đặt cookie, đặt câu hỏi cho người truy cập, hiển thị thông báo.
- Ghi nhớ dữ liệu ở phía máy khách ("local storage").

## [JavaScript trong trình duyệt KHÔNG THỂ làm được những gì?](#what-can-t-in-browser-javascript-do)

Khả năng của JavaScript trong trình duyệt bị giới hạn để bảo vệ sự an toàn của người dùng. Mục tiêu là ngăn chặn một trang web độc hại truy cập thông tin cá nhân hoặc làm hỏng dữ liệu của người dùng.

Ví dụ về các hạn chế như vậy bao gồm:

- JavaScript trên trang web không thể đọc/ghi các tệp tùy ý trên đĩa cứng, sao chép chúng hoặc thực thi chương trình. Nó không có quyền truy cập trực tiếp vào các hàm của hệ điều hành.

  Các trình duyệt hiện đại cho phép nó hoạt động với các tệp, nhưng quyền truy cập bị giới hạn và chỉ được cung cấp nếu người dùng thực hiện một số hành động nhất định, như "thả" một tệp vào cửa sổ trình duyệt hoặc chọn nó qua thẻ `<input>`.

  Có những cách để tương tác với camera/microphone và các thiết bị khác, nhưng chúng yêu cầu sự cho phép rõ ràng của người dùng. Vì vậy, một trang có bật JavaScript không thể lén bật webcam, quan sát xung quanh và gửi thông tin đến [NSA](https://en.wikipedia.org/wiki/National_Security_Agency).

- Các tab/cửa sổ khác nhau về cơ bản không biết về nhau. Đôi khi chúng có, ví dụ khi một cửa sổ sử dụng JavaScript để mở cửa sổ kia. Nhưng ngay cả trong trường hợp này, JavaScript từ trang này không thể truy cập trang khác nếu chúng đến từ các trang web khác nhau (từ tên miền, giao thức hoặc cổng khác nhau).

  Điều này được gọi là "Chính sách cùng nguồn gốc" (Same Origin Policy). Để khắc phục điều đó, *cả hai trang* phải đồng ý cho việc trao đổi dữ liệu và phải chứa mã JavaScript đặc biệt xử lý nó. Chúng ta sẽ đề cập đến điều đó trong hướng dẫn.

  Hạn chế này, một lần nữa, là vì sự an toàn của người dùng. Một trang từ `http://anysite.com` mà người dùng đã mở không được phép truy cập một tab trình duyệt khác với URL `http://gmail.com`, ví dụ, và đánh cắp thông tin từ đó.

- JavaScript có thể dễ dàng giao tiếp qua mạng với máy chủ mà trang hiện tại đến từ đó. Nhưng khả năng nhận dữ liệu từ các trang web/địa chỉ miền khác bị hạn chế nghiêm trọng. Mặc dù có thể, nhưng nó yêu cầu sự đồng ý rõ ràng (được thể hiện trong các tiêu đề HTTP) từ phía máy chủ từ xa. Một lần nữa, đó là một hạn chế về an toàn.

![](/article/intro/limitations.svg)

Các hạn chế như vậy không tồn tại nếu JavaScript được sử dụng bên ngoài trình duyệt, ví dụ như trên máy chủ. Các trình duyệt hiện đại cũng cho phép các plugin/mở rộng có thể yêu cầu quyền mở rộng.

## [Điều gì khiến JavaScript trở nên độc đáo?](#what-makes-javascript-unique)

Có ít nhất *ba* điều tuyệt vời về JavaScript:

- Tích hợp đầy đủ với HTML/CSS.
- Những điều đơn giản được thực hiện một cách đơn giản.
- Được hỗ trợ bởi tất cả các trình duyệt chính và được bật mặc định.

JavaScript là công nghệ trình duyệt duy nhất kết hợp cả ba điều này.

Đó là điều khiến JavaScript trở nên độc đáo. Đó là lý do tại sao nó là công cụ phổ biến nhất để tạo giao diện trình duyệt.

Tuy nhiên, JavaScript có thể được sử dụng để tạo máy chủ, ứng dụng di động, v.v.

## [Các ngôn ngữ "phía trên" JavaScript](#languages-over-javascript)

Cú pháp của JavaScript không phù hợp với nhu cầu của mọi người. Những người khác nhau muốn có các tính năng khác nhau.

Điều đó là điều dễ hiểu, vì các dự án và yêu cầu là khác nhau đối với mỗi người.

Vì vậy, gần đây đã xuất hiện rất nhiều ngôn ngữ mới, được *biên dịch ngược* (transpiled - chuyển đổi) sang JavaScript trước khi chúng chạy trong trình duyệt.

Các công cụ hiện đại khiến việc biên dịch ngược trở nên rất nhanh chóng và minh bạch, thực sự cho phép các nhà phát triển mã hóa bằng một ngôn ngữ khác và tự động chuyển đổi nó "ở hậu trường".

Ví dụ về các ngôn ngữ như vậy:

- [CoffeeScript](https://coffeescript.org/) là "đường syrup cú pháp" cho JavaScript. Nó giới thiệu cú pháp ngắn hơn, cho phép chúng ta viết mã rõ ràng và chính xác hơn. Thông thường, các lập trình viên Ruby thích nó.
- [TypeScript](https://www.typescriptlang.org/) tập trung vào việc thêm "kiểu dữ liệu nghiêm ngặt" để đơn giản hóa việc phát triển và bảo trì các hệ thống phức tạp. Nó được phát triển bởi Microsoft.
- [Flow](https://flow.org/) cũng thêm kiểu dữ liệu, nhưng theo một cách khác. Được phát triển bởi Facebook.
- [Dart](https://www.dartlang.org/) là một ngôn ngữ độc lập có trình thông dịch riêng chạy trong các môi trường không phải trình duyệt (như ứng dụng di động), nhưng cũng có thể được chuyển đổi sang JavaScript. Được phát triển bởi Google.
- [Brython](https://brython.info/) là một trình chuyển đổi Python sang JavaScript cho phép viết ứng dụng bằng Python thuần túy mà không cần JavaScript.
- [Kotlin](https://kotlinlang.org/docs/reference/js-overview.html) là một ngôn ngữ lập trình hiện đại, súc tích và an toàn có thể nhắm đến trình duyệt hoặc Node.

Còn nhiều hơn thế. Tất nhiên, ngay cả khi chúng ta sử dụng một trong các ngôn ngữ được chuyển đổi này, chúng ta cũng nên biết JavaScript để thực sự hiểu những gì chúng ta đang làm.

## [Tóm tắt](#summary)

- JavaScript ban đầu được tạo ra như một ngôn ngữ chỉ dành cho trình duyệt, nhưng bây giờ nó được sử dụng trong nhiều môi trường khác nhau.
- Ngày nay, JavaScript có vị trí độc đáo là ngôn ngữ trình duyệt được sử dụng rộng rãi nhất, được tích hợp đầy đủ với HTML/CSS.
- Có nhiều ngôn ngữ được "chuyển đổi" sang JavaScript và cung cấp các tính năng nhất định. Nên xem xét chúng, ít nhất là sơ lược, sau khi thành thạo JavaScript.
