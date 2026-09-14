# Môi trường trình duyệt và đặc tả

> Nguồn: [https://javascript.info/browser-environment](https://javascript.info/browser-environment)

<!-- fetched: 2026-09-14 -->

Ngôn ngữ JavaScript ban đầu được tạo ra cho trình duyệt web. Kể từ đó, nó đã phát triển thành một ngôn ngữ với nhiều công dụng và nền tảng.

Một nền tảng có thể là trình duyệt, máy chủ web hoặc một *host* khác, hoặc thậm chí là một máy pha cà phê "thông minh" nếu nó có thể chạy JavaScript. Mỗi nền tảng cung cấp các tính năng đặc thù của riêng nó. Đặc tả JavaScript gọi đó là *môi trường host*.

Môi trường host cung cấp các đối tượng và hàm riêng của nó bên cạnh lõi ngôn ngữ. Trình duyệt web cho phép điều khiển các trang web. Node.js cung cấp các tính năng phía máy chủ, v.v.

Dưới đây là tổng quan về những gì chúng ta có khi JavaScript chạy trong trình duyệt web:

![](/article/browser-environment/windowObjects.svg)

Có một đối tượng "gốc" được gọi là `window`. Nó có hai vai trò:

1. Đầu tiên, nó là đối tượng toàn cục cho mã JavaScript, như đã mô tả trong chương [Đối tượng toàn cục](/global-object).
2. Thứ hai, nó đại diện cho "cửa sổ trình duyệt" và cung cấp các phương thức để điều khiển nó.

Ví dụ, chúng ta có thể sử dụng nó như một đối tượng toàn cục:

```
function sayHi() {
  alert("Hello");
}

// các hàm toàn cục là các phương thức của đối tượng toàn cục:
window.sayHi();
```

Và chúng ta có thể sử dụng nó như một cửa sổ trình duyệt, để hiển thị chiều cao cửa sổ:

```
alert(window.innerHeight); // chiều cao cửa sổ trong
```

Có nhiều phương thức và thuộc tính cụ thể của window hơn, chúng ta sẽ tìm hiểu sau.

## [DOM (Mô hình Đối tượng Tài liệu)](#dom-document-object-model)

Mô hình Đối tượng Tài liệu, gọi tắt là DOM, biểu diễn tất cả nội dung trang web dưới dạng các đối tượng có thể được sửa đổi.

Đối tượng `document` là điểm "vào" chính vào trang. Chúng ta có thể thay đổi hoặc tạo ra bất kỳ thứ gì trên trang bằng cách sử dụng nó.

Ví dụ:

```
// thay đổi màu nền thành đỏ
document.body.style.background = "red";

// thay đổi lại sau 1 giây
setTimeout(() => document.body.style.background = "", 1000);
```

Ở đây, chúng ta đã sử dụng `document.body.style`, nhưng còn rất nhiều thứ khác nữa. Các thuộc tính và phương thức được mô tả trong đặc tả: [DOM Living Standard](https://dom.spec.whatwg.org).

DOM không chỉ dành cho trình duyệt

Đặc tả DOM giải thích cấu trúc của một tài liệu và cung cấp các đối tượng để thao tác với nó. Có các công cụ không dùng trình duyệt cũng sử dụng DOM.

Ví dụ, các tập lệnh phía máy chủ tải xuống các trang HTML và xử lý chúng cũng có thể sử dụng DOM. Tuy nhiên, chúng có thể chỉ hỗ trợ một phần của đặc tả.

CSSOM để tạo kiểu

Cũng có một đặc tả riêng, [CSS Object Model (CSSOM)](https://www.w3.org/TR/cssom-1/) cho các quy tắc CSS và stylesheet, giải thích cách chúng được biểu diễn dưới dạng đối tượng và cách đọc/ghi chúng.

CSSOM được sử dụng cùng với DOM khi chúng ta sửa đổi các quy tắc style cho tài liệu. Tuy nhiên, trong thực tế, CSSOM hiếm khi được yêu cầu, vì chúng ta hiếm khi cần sửa đổi các quy tắc CSS từ JavaScript (thường thì chúng ta chỉ thêm/xóa các lớp CSS, không sửa đổi quy tắc CSS của chúng), nhưng cũng có thể làm được.

## [BOM (Mô hình Đối tượng Trình duyệt)](#bom-browser-object-model)

Mô hình Đối tượng Trình duyệt (BOM) đại diện cho các đối tượng bổ sung do trình duyệt (môi trường host) cung cấp để làm việc với mọi thứ ngoại trừ tài liệu.

Ví dụ:

- Đối tượng [navigator](https://developer.mozilla.org/en-US/docs/Web/API/Window/navigator) cung cấp thông tin nền về trình duyệt và hệ điều hành. Có nhiều thuộc tính, nhưng hai thuộc tính phổ biến nhất là: `navigator.userAgent` – về trình duyệt hiện tại, và `navigator.platform` – về nền tảng (có thể giúp phân biệt giữa Windows/Linux/Mac v.v.).
- Đối tượng [location](https://developer.mozilla.org/en-US/docs/Web/API/Window/location) cho phép chúng ta đọc URL hiện tại và có thể chuyển hướng trình duyệt đến một URL mới.

Dưới đây là cách chúng ta có thể sử dụng đối tượng `location`:

```
alert(location.href); // hiển thị URL hiện tại
if (confirm("Go to Wikipedia?")) {
  location.href = "https://wikipedia.org"; // chuyển hướng trình duyệt đến URL khác
}
```

Các hàm `alert/confirm/prompt` cũng là một phần của BOM: chúng không liên quan trực tiếp đến tài liệu, nhưng đại diện cho các phương thức thuần túy của trình duyệt để giao tiếp với người dùng.

Đặc tả

BOM là một phần của đặc tả chung [HTML](https://html.spec.whatwg.org).

Đúng vậy, bạn nghe rõ rồi đấy. Đặc tả HTML tại <https://html.spec.whatwg.org> không chỉ nói về "ngôn ngữ HTML" (thẻ, thuộc tính), mà còn bao gồm nhiều đối tượng, phương thức và các mở rộng DOM đặc thù cho trình duyệt. Đó là "HTML theo nghĩa rộng". Ngoài ra, một số phần có các đặc tả bổ sung được liệt kê tại <https://spec.whatwg.org>.

## [Tóm tắt](#summary)

Nói về các tiêu chuẩn, chúng ta có:

Đặc tả DOM
:   Mô tả cấu trúc tài liệu, các thao tác và sự kiện, xem <https://dom.spec.whatwg.org>.

Đặc tả CSSOM
:   Mô tả các stylesheet và quy tắc style, các thao tác với chúng và cách chúng liên kết với tài liệu, xem <https://www.w3.org/TR/cssom-1/>.

Đặc tả HTML
:   Mô tả ngôn ngữ HTML (ví dụ: các thẻ) và cũng bao gồm BOM (mô hình đối tượng trình duyệt) – các hàm trình duyệt khác nhau: `setTimeout`, `alert`, `location` và v.v., xem <https://html.spec.whatwg.org>. Nó kế thừa đặc tả DOM và mở rộng nó với nhiều thuộc tính và phương thức bổ sung.

Ngoài ra, một số lớp được mô tả riêng tại <https://spec.whatwg.org/>.

Xin lưu ý các liên kết này, vì có rất nhiều điều để học nên không thể bao quát hết mọi thứ và nhớ tất cả.

Khi bạn muốn đọc về một thuộc tính hoặc phương thức, cuốn hướng dẫn của Mozilla tại <https://developer.mozilla.org/en-US/> cũng là một nguồn tài liệu tốt, nhưng đặc tả tương ứng có thể tốt hơn: nó phức tạp hơn và dài hơn để đọc, nhưng sẽ giúp kiến thức nền tảng của bạn vững chắc và đầy đủ.

Để tìm kiếm thứ gì đó, thường tiện lợi khi sử dụng công cụ tìm kiếm internet "WHATWG [thuật ngữ]" hoặc "MDN [thuật ngữ]", ví dụ <https://google.com?q=whatwg+localstorage>, <https://google.com?q=mdn+localstorage>.

Bây giờ, chúng ta sẽ bắt đầu học về DOM, vì tài liệu đóng vai trò trung tâm trong UI.
