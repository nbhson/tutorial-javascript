# Cây DOM

> Nguồn: [https://javascript.info/dom-nodes](https://javascript.info/dom-nodes)

<!-- fetched: 2026-09-14 -->

Xương sống của một tài liệu HTML là các thẻ.

Theo Mô hình Đối tượng Tài liệu (DOM), mọi thẻ HTML là một đối tượng. Các thẻ lồng nhau là "con" của thẻ bao quanh. Văn bản bên trong một thẻ cũng là một đối tượng.

Tất cả các đối tượng này có thể truy cập được bằng JavaScript, và chúng ta có thể sử dụng chúng để sửa đổi trang.

Ví dụ, `document.body` là đối tượng đại diện cho thẻ `<body>`.

Chạy đoạn mã sau sẽ làm cho `<body>` có màu đỏ trong 3 giây:

```
document.body.style.background = 'red'; // làm cho nền màu đỏ

setTimeout(() => document.body.style.background = '', 3000); // hoàn tác
```

Ở đây chúng ta đã sử dụng `style.background` để thay đổi màu nền của `document.body`, nhưng có nhiều thuộc tính khác, chẳng hạn như:

- `innerHTML` – nội dung HTML của nút.
- `offsetWidth` – chiều rộng của nút (theo pixel)
- …và nhiều thứ khác nữa.

Sớm thôi chúng ta sẽ học thêm nhiều cách thao tác với DOM, nhưng trước tiên chúng ta cần biết về cấu trúc của nó.

## [Một ví dụ về DOM](#an-example-of-the-dom)

Hãy bắt đầu với tài liệu đơn giản sau:

```
<!DOCTYPE HTML>
<html>
<head>
  <title>About elk</title>
</head>
<body>
  The truth about elk.
</body>
</html>
```

DOM biểu diễn HTML dưới dạng cấu trúc cây của các thẻ. Đây là cách nó trông:

let node1 = {"name":"HTML","nodeType":1,"children":[{"name":"HEAD","nodeType":1,"children":[{"name":"#text","nodeType":3,"content":"\n "},{"name":"TITLE","nodeType":1,"children":[{"name":"#text","nodeType":3,"content":"About elk"}]},{"name":"#text","nodeType":3,"content":"\n"}]},{"name":"#text","nodeType":3,"content":"\n"},{"name":"BODY","nodeType":1,"children":[{"name":"#text","nodeType":3,"content":"\n The truth about elk.\n"}]}]}
drawHtmlTree(node1, 'div.domtree', 690, 320);

Trong hình trên, bạn có thể nhấp vào các nút phần tử và con của chúng sẽ mở/rút gọn.

Mỗi nút trên cây là một đối tượng.

Các thẻ là *nút phần tử* (hoặc đơn giản là phần tử) và hình thành cấu trúc cây: `<html>` ở gốc, sau đó `<head>` và `<body>` là con của nó, v.v.

Văn bản bên trong các phần tử hình thành *nút văn bản*, được gắn nhãn là `#text`. Một nút văn bản chứa duy nhất một chuỗi. Nó không thể có con và luôn là lá của cây.

Ví dụ, thẻ `<title>` có văn bản `"About elk"`.

Xin lưu ý các ký tự đặc biệt trong nút văn bản:

- một ký tự xuống dòng: `↵` (trong JavaScript được gọi là `\n`)
- một khoảng trắng: `␣`

Khoảng trắng và ký tự xuống dòng là các ký tự hoàn toàn hợp lệ, giống như chữ cái và chữ số. Chúng hình thành các nút văn bản và trở thành một phần của DOM. Vì vậy, ví dụ, trong ví dụ trên, thẻ `<head>` chứa một số khoảng trắng trước `<title>`, và văn bản đó trở thành một nút `#text` (chỉ chứa ký tự xuống dòng và một số khoảng trắng).

Chỉ có hai ngoại lệ ở cấp cao nhất:

1. Khoảng trắng và ký tự xuống dòng trước `<head>` bị bỏ qua vì lý do lịch sử.
2. Nếu chúng ta đặt thứ gì đó sau `</body>`, thì thứ đó sẽ tự động được di chuyển vào bên trong `body`, ở cuối, vì đặc tả HTML yêu cầu tất cả nội dung phải nằm trong `<body>`. Vì vậy, không thể có khoảng trắng nào sau `</body>`.

Trong các trường hợp khác thì mọi thứ đều rõ ràng – nếu có khoảng trắng (giống như bất kỳ ký tự nào khác) trong tài liệu, thì chúng sẽ trở thành các nút văn bản trong DOM, và nếu chúng ta xóa chúng, thì sẽ không có gì.

Sau đây không có nút văn bản chỉ chứa khoảng trắng:

```
<!DOCTYPE HTML>
<html><head><title>About elk</title></head><body>The truth about elk.</body></html>
```

let node2 = {"name":"HTML","nodeType":1,"children":[{"name":"HEAD","nodeType":1,"children":[{"name":"TITLE","nodeType":1,"children":[{"name":"#text","nodeType":3,"content":"About elk"}]}]},{"name":"BODY","nodeType":1,"children":[{"name":"#text","nodeType":3,"content":"The truth about elk."}]}]}
drawHtmlTree(node2, 'div.domtree', 690, 210);

Các nút văn bản chỉ chứa khoảng trắng ở đầu/cuối chuỗi thường bị ẩn trong các công cụ

Các công cụ của trình duyệt (sẽ được đề cập sớm) làm việc với DOM thường không hiển thị khoảng trắng ở đầu/cuối của văn bản và các nút văn bản trống (ngắt dòng) giữa các thẻ.

Công cụ phát triển tiết kiệm không gian màn hình theo cách này.

Trong các hình DOM tiếp theo, chúng ta đôi khi sẽ bỏ qua chúng khi chúng không liên quan. Những khoảng trắng như vậy thường không ảnh hưởng đến cách tài liệu được hiển thị.

## [Tự động sửa chữa](#autocorrection)

Nếu trình duyệt gặp phải HTML không hợp lệ, nó sẽ tự động sửa chữa khi tạo DOM.

Ví dụ, thẻ ở cấp cao nhất luôn là `<html>`. Ngay cả khi nó không tồn tại trong tài liệu, nó sẽ tồn tại trong DOM, vì trình duyệt sẽ tạo ra nó. Điều tương tự cũng xảy ra với `<body>`.

Lấy ví dụ, nếu tệp HTML là một từ đơn "Hello", trình duyệt sẽ gói nó vào trong `<html>` và `<body>`, và thêm `<head>` cần thiết, và DOM sẽ là:

let node3 = {"name":"HTML","nodeType":1,"children":[{"name":"HEAD","nodeType":1,"children":[]},{"name":"BODY","nodeType":1,"children":[{"name":"#text","nodeType":3,"content":"Hello"}]}]}
drawHtmlTree(node3, 'div.domtree', 690, 150);

Trong quá trình tạo DOM, trình duyệt tự động xử lý các lỗi trong tài liệu, đóng các thẻ và v.v.

Một tài liệu với các thẻ chưa đóng:

```
<p>Hello
<li>Mom
<li>and
<li>Dad
```

…sẽ trở thành một DOM bình thường khi trình duyệt đọc các thẻ và khôi phục các phần bị thiếu:

let node4 = {"name":"HTML","nodeType":1,"children":[{"name":"HEAD","nodeType":1,"children":[]},{"name":"BODY","nodeType":1,"children":[{"name":"P","nodeType":1,"children":[{"name":"#text","nodeType":3,"content":"Hello"}]},{"name":"LI","nodeType":1,"children":[{"name":"#text","nodeType":3,"content":"Mom"}]},{"name":"LI","nodeType":1,"children":[{"name":"#text","nodeType":3,"content":"and"}]},{"name":"LI","nodeType":1,"children":[{"name":"#text","nodeType":3,"content":"Dad"}]}]}]}
drawHtmlTree(node4, 'div.domtree', 690, 360);

Bảng luôn có `<tbody>`

Một "trường hợp đặc biệt" thú vị là bảng. Theo đặc tả DOM, chúng phải có thẻ `<tbody>`, nhưng văn bản HTML có thể bỏ qua nó. Sau đó, trình duyệt sẽ tự tạo `<tbody>` trong DOM.

Đối với HTML:

```
<table id="table"><tr><td>1</td></tr></table>
```

Cấu trúc DOM sẽ là:

let node5 = {"name":"TABLE","nodeType":1,"children":[{"name":"TBODY","nodeType":1,"children":[{"name":"TR","nodeType":1,"children":[{"name":"TD","nodeType":1,"children":[{"name":"#text","nodeType":3,"content":"1"}]}]}]}]};
drawHtmlTree(node5, 'div.domtree', 600, 200);

Bạn thấy không? `<tbody>` xuất hiện từ đâu không rõ. Chúng ta nên ghi nhớ điều này khi làm việc với bảng để tránh những bất ngờ.

## [Các loại nút khác](#other-node-types)

Có một số loại nút khác ngoài nút phần tử và nút văn bản.

Ví dụ, chú thích:

```
<!DOCTYPE HTML>
<html>
<body>
  The truth about elk.
  <ol>
    <li>An elk is a smart</li>
    <!-- comment -->
    <li>...and cunning animal!</li>
  </ol>
</body>
</html>
```

let node6 = {"name":"HTML","nodeType":1,"children":[{"name":"HEAD","nodeType":1,"children":[]},{"name":"BODY","nodeType":1,"children":[{"name":"#text","nodeType":3,"content":"\n The truth about elk.\n "},{"name":"OL","nodeType":1,"children":[{"name":"#text","nodeType":3,"content":"\n "},{"name":"LI","nodeType":1,"children":[{"name":"#text","nodeType":3,"content":"An elk is a smart"}]},{"name":"#text","nodeType":3,"content":"\n "},{"name":"#comment","nodeType":8,"content":"comment"},{"name":"#text","nodeType":3,"content":"\n "},{"name":"LI","nodeType":1,"children":[{"name":"#text","nodeType":3,"content":"...and cunning animal!"}]},{"name":"#text","nodeType":3,"content":"\n "}]},{"name":"#text","nodeType":3,"content":"\n\n\n"}]}]};
drawHtmlTree(node6, 'div.domtree', 690, 500);

Chúng ta có thể thấy ở đây một loại nút cây mới – *nút chú thích*, được gắn nhãn là `#comment`, giữa hai nút văn bản.

Chúng ta có thể nghĩ – tại sao chú thích lại được thêm vào DOM? Nó không ảnh hưởng đến biểu diễn trực quan theo bất kỳ cách nào. Nhưng có một quy tắc – nếu thứ gì đó có trong HTML, thì nó cũng phải có trong cây DOM.

**Mọi thứ trong HTML, ngay cả chú thích, đều trở thành một phần của DOM.**

Ngay cả hướng dẫn `<!DOCTYPE...>` ở đầu HTML cũng là một nút DOM. Nó nằm trong cây DOM ngay trước `<html>`. Rất ít người biết điều đó. Chúng ta không chạm vào nút đó, thậm chí chúng ta không vẽ nó trên sơ đồ, nhưng nó có tồn tại.

Đối tượng `document` đại diện cho toàn bộ tài liệu, về mặt kỹ thuật cũng là một nút DOM.

Có [12 loại nút](https://dom.spec.whatwg.org/#node). Trong thực tế, chúng ta thường làm việc với 4 trong số chúng:

1. `document` – "điểm vào" vào DOM.
2. nút phần tử – các thẻ HTML, các khối xây dựng cây.
3. nút văn bản – chứa văn bản.
4. chú thích – đôi khi chúng ta có thể đặt thông tin vào đó, nó sẽ không được hiển thị, nhưng JS có thể đọc nó từ DOM.

## [Tự xem](#see-it-for-yourself)

Để xem cấu trúc DOM theo thời gian thực, hãy thử [Live DOM Viewer](https://software.hixie.ch/utilities/js/live-dom-viewer/). Chỉ cần nhập tài liệu, và nó sẽ hiển thị ngay lập tức dưới dạng DOM.

Một cách khác để khám phá DOM là sử dụng công cụ phát triển trình duyệt. Thực tế, đó là những gì chúng ta sử dụng khi phát triển.

Để làm điều đó, hãy mở trang web [elk.html](/article/dom-nodes/elk.html), bật công cụ phát triển trình duyệt và chuyển sang tab Elements.

Nó sẽ trông như thế này:

![](/article/dom-nodes/elk.svg)

Bạn có thể xem DOM, nhấp vào các phần tử, xem chi tiết của chúng và v.v.

Xin lưu ý rằng cấu trúc DOM trong công cụ phát triển được đơn giản hóa. Các nút văn bản được hiển thị chỉ dưới dạng văn bản. Và không có nút văn bản "trống" (chỉ chứa khoảng trắng) ở tất cả. Điều đó ổn, vì phần lớn thời gian chúng ta quan tâm đến các nút phần tử.

Nhấp vào  ở góc trên bên trái cho phép chúng ta chọn một nút từ trang web bằng chuột (hoặc các thiết bị trỏ khác) và "xem" nó (cuộn đến nó trong tab Elements). Điều này hoạt động rất tốt khi chúng ta có một trang HTML khổng lồ (và DOM khổng lồ tương ứng) và muốn xem vị trí của một phần tử cụ thể trong đó.

Một cách khác để làm điều đó là nhấp chuột phải vào trang web và chọn "Inspect" trong menu ngữ cảnh.

![](/article/dom-nodes/inspect.svg)

Ở phần bên phải của công cụ có các tab con sau:

- **Styles** – chúng ta có thể xem CSS được áp dụng cho phần tử hiện tại từng quy tắc một, bao gồm các quy tắc tích hợp (màu xám). Hầu hết mọi thứ có thể được chỉnh sửa tại chỗ, bao gồm kích thước/viền/padding của hộp bên dưới.
- **Computed** – để xem CSS được áp dụng cho phần tử theo thuộc tính: đối với mỗi thuộc tính, chúng ta có thể xem quy tắc tạo ra nó (bao gồm cả kế thừa CSS và tương tự).
- **Event Listeners** – để xem các trình lắng nghe sự kiện được gắn vào các phần tử DOM (chúng ta sẽ đề cập đến chúng trong phần tiếp theo của hướng dẫn).
- …và nhiều thứ khác.

Cách tốt nhất để tìm hiểu chúng là nhấp xung quanh. Hầu hết các giá trị có thể được chỉnh sửa tại chỗ.

## [Tương tác với bảng điều khiển](#interaction-with-console)

Khi làm việc với DOM, chúng ta cũng có thể muốn áp dụng JavaScript vào nó. Như: lấy một nút và chạy một số mã để sửa đổi nó, để xem kết quả. Dưới đây là một số mẹo để di chuyển giữa tab Elements và bảng điều khiển.

Để bắt đầu:

1. Chọn `<li>` đầu tiên trong tab Elements.
2. Nhấn `Esc` – nó sẽ mở bảng điều khiển ngay bên dưới tab Elements.

Giờ đây, phần tử được chọn cuối cùng có sẵn dưới dạng `$0`, phần tử được chọn trước đó là `$1`, v.v.

Chúng ta có thể chạy các lệnh trên chúng. Ví dụ, `$0.style.background = 'red'` làm cho mục danh sách được chọn có màu đỏ, như sau:

![](/article/dom-nodes/domconsole0.svg)

Đó là cách lấy một nút từ Elements trong Console.

Cũng có một đường đi ngược lại. Nếu có một biến tham chiếu đến một nút DOM, thì chúng ta có thể sử dụng lệnh `inspect(node)` trong Console để xem nó trong ngăn Elements.

Hoặc chúng ta có thể xuất nút DOM ra bảng điều khiển và khám phá "tại chỗ", như `document.body` bên dưới:

![](/article/dom-nodes/domconsole1.svg)

Điều đó là để gỡ lỗi. Từ chương tiếp theo trở đi, chúng ta sẽ truy cập và sửa đổi DOM bằng JavaScript.

Công cụ phát triển trình duyệt là một trợ giúp rất lớn trong phát triển: chúng ta có thể khám phá DOM, thử nghiệm và xem những gì đang sai.

## [Tóm tắt](#summary)

Một tài liệu HTML/XML được biểu diễn trong trình duyệt dưới dạng cây DOM.

- Thẻ trở thành các nút phần tử và hình thành cấu trúc.
- Văn bản trở thành các nút văn bản.
- …v.v., mọi thứ trong HTML đều có vị trí của nó trong DOM, ngay cả chú thích.

Chúng ta có thể sử dụng công cụ phát triển để kiểm tra DOM và sửa đổi nó thủ công.

Ở đây chúng ta đã đề cập đến những kiến thức cơ bản, các hành động được sử dụng và quan trọng nhất để bắt đầu. Có tài liệu hướng dẫn rộng rãi về Chrome Developer Tools tại <https://developers.google.com/web/tools/chrome-devtools>. Cách tốt nhất để làm quen với các công cụ là nhấp vào đây và đó, đọc menu: hầu hết các tùy chọn đều rõ ràng. Sau đó, khi bạn biết chúng nói chung, hãy đọc tài liệu và tìm hiểu phần còn lại.

Nút DOM có các thuộc tính và phương thức cho phép chúng ta di chuyển giữa chúng, sửa đổi chúng, di chuyển xung quanh trang và nhiều hơn nữa. Chúng ta sẽ đi sâu vào chúng trong các chương tiếp theo.
