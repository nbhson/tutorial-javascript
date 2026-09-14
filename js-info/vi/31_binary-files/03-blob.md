# Blob

> Source: [https://javascript.info/blob](https://javascript.info/blob)

<!-- fetched: 2026-09-14 -->

`ArrayBuffer` và các view là một phần của tiêu chuẩn ECMA, một phần của JavaScript.

Trong trình duyệt, có các đối tượng cấp cao hơn bổ sung, được mô tả trong [File API](https://www.w3.org/TR/FileAPI/), đặc biệt là `Blob`.

`Blob` bao gồm một chuỗi `type` tùy chọn (thường là MIME-type), cộng với `blobParts` – một dãy các đối tượng `Blob` khác, chuỗi và `BufferSource`.

![](/article/blob/blob.svg)

Cú pháp constructor là:

```
new Blob(blobParts, options);
```

- **`blobParts`** là mảng các giá trị `Blob`/`BufferSource`/`String`.
- **`options`** đối tượng tùy chọn:
  - **`type`** – kiểu `Blob`, thường là MIME-type, ví dụ `image/png`,
  - **`endings`** – xem có chuyển đổi dấu xuống dòng để làm cho `Blob` phù hợp với newline hiện tại của OS (`\r\n` hoặc `\n`) hay không. Mặc định là `"transparent"` (không làm gì), nhưng cũng có thể là `"native"` (chuyển đổi).

Ví dụ:

```
// tạo Blob từ một chuỗi
let blob = new Blob(["<html>…</html>"], {type: 'text/html'});
// xin lưu ý: đối số đầu tiên phải là mảng [...]
```

```
// tạo Blob từ mảng kiểu và chuỗi
let hello = new Uint8Array([72, 101, 108, 108, 111]); // "Hello" ở dạng nhị phân

let blob = new Blob([hello, ' ', 'world'], {type: 'text/plain'});
```

Chúng ta có thể trích xuất các slice của `Blob` với:

```
blob.slice([byteStart], [byteEnd], [contentType]);
```

- **`byteStart`** – byte bắt đầu, mặc định là 0.
- **`byteEnd`** – byte cuối (không bao gồm, mặc định tới cuối).
- **`contentType`** – `type` của blob mới, mặc định cùng với nguồn.

Các đối số tương tự như `array.slice`, số âm cũng được chấp nhận.

Đối tượng `Blob` không thể thay đổi

Chúng ta không thể thay đổi dữ liệu trực tiếp trong một `Blob`, nhưng chúng ta có thể cắt các phần của `Blob`, tạo các đối tượng `Blob` mới từ chúng, trộn chúng vào một `Blob` mới và cứ thế.

Hành vi này tương tự như chuỗi JavaScript: chúng ta không thể thay đổi một ký tự trong chuỗi, nhưng chúng ta có thể tạo chuỗi mới đã sửa chữa.

## [Blob dưới dạng URL](#blob-as-url)

Một Blob có thể dễ dàng được sử dụng như một URL cho `<a>`, `<img>` hoặc các thẻ khác, để hiển thị nội dung của nó.

Nhờ `type`, chúng ta cũng có thể tải lên/tải xuống các đối tượng `Blob`, và `type` tự nhiên trở thành `Content-Type` trong các yêu cầu mạng.

Hãy bắt đầu với một ví dụ đơn giản. Bằng cách nhấp vào liên kết, bạn sẽ tải xuống một `Blob` được tạo động với nội dung `hello world` dưới dạng tệp:

```
<!-- thuộc tính download buộc trình duyệt tải xuống thay vì điều hướng -->
<a download="hello.txt" href='#' id="link">Tải xuống</a>

<script>
let blob = new Blob(["Hello, world!"], {type: 'text/plain'});

link.href = URL.createObjectURL(blob);
</script>
```

Chúng ta cũng có thể tạo liên kết động trong JavaScript và mô phỏng nhấp chuột bằng `link.click()`, sau đó việc tải xuống bắt đầu tự động.

Đây là mã tương tự gây ra việc người dùng tải xuống `Blob` được tạo động, mà không có bất kỳ HTML nào:

```
let link = document.createElement('a');
link.download = 'hello.txt';

let blob = new Blob(['Hello, world!'], {type: 'text/plain'});

link.href = URL.createObjectURL(blob);

link.click();

URL.revokeObjectURL(link.href);
```

`URL.createObjectURL` lấy một `Blob` và tạo một URL duy nhất cho nó, dưới dạng `blob:<origin>/<uuid>`.

Đó là những gì giá trị của `link.href` trông như thế này:

```
blob:https://javascript.info/1e67e00e-860d-40a5-89ae-6ab0cbee6273
```

Đối với mỗi URL được tạo bởi `URL.createObjectURL`, trình duyệt lưu trữ một ánh xạ URL → `Blob` nội bộ. Vì vậy, các URL này ngắn, nhưng cho phép truy cập vào `Blob`.

Một URL được tạo (và do đó liên kết với nó) chỉ hợp lệ trong tài liệu hiện tại, trong khi nó mở. Và nó cho phép tham chiếu đến `Blob` trong `<img>`, `<a>`, về cơ bản là bất kỳ đối tượng nào khác mong đợi một URL.

Tuy nhiên, có một tác dụng phụ. Trong khi có ánh xạ cho một `Blob`, bản thân `Blob` tồn tại trong bộ nhớ. Trình duyệt không thể giải phóng nó.

Ánh xạ được xóa tự động khi document unload, vì vậy các đối tượng `Blob` được giải phóng. Nhưng nếu ứng dụng tồn tại lâu dài, thì điều đó không xảy ra sớm.

**Vì vậy, nếu chúng ta tạo một URL, `Blob` đó sẽ treo trong bộ nhớ, ngay cả khi không còn cần thiết nữa.**

`URL.revokeObjectURL(url)` xóa tham chiếu từ ánh xạ nội bộ, do đó cho phép `Blob` bị xóa (nếu không có tham chiếu khác), và bộ nhớ được giải phóng.

Trong ví dụ cuối cùng, chúng ta dự định sử dụng `Blob` chỉ một lần, để tải xuống tức thì, vì vậy chúng ta gọi `URL.revokeObjectURL(link.href)` ngay lập tức.

Trong ví dụ trước đó với liên kết HTML có thể nhấp, chúng ta không gọi `URL.revokeObjectURL(link.href)`, vì điều đó sẽ làm cho URL `Blob` không hợp lệ. Sau khi revoke, khi ánh xạ bị xóa, URL không hoạt động nữa.

## [Blob sang base64](#blob-to-base64)

Một cách thay thế cho `URL.createObjectURL` là chuyển đổi một `Blob` thành chuỗi được mã hóa base64.

Mã hóa đó biểu diễn dữ liệu nhị phân như một chuỗi các ký tự "đọc được" an toàn với mã ASCII từ 0 đến 64. Và quan trọng hơn – chúng ta có thể sử dụng mã hóa này trong "data-urls".

Một [data url](https://developer.mozilla.org/en-US/docs/Web/http/Data_URIs) có dạng `data:[<mediatype>][;base64],<data>`. Chúng ta có thể sử dụng các url như vậy ở mọi nơi, ngang hàng với các url "thông thường".

Ví dụ, đây là một hình smiley:

```
<img src="data:image/png;base64,R0lGODlhDAAMAKIFAF5LAP/zxAAAANyuAP/gaP///wAAAAAAACH5BAEAAAUALAAAAAAMAAwAAAMlWLPcGjDKFYi9lxKBOaGcF35DhWHamZUW0K4mAbiwWtuf0uxFAgA7">
```

Trình duyệt sẽ giải mã chuỗi và hiển thị hình ảnh: ![](data:image/png;base64,R0lGODlhDAAMAKIFAF5LAP/zxAAAANyuAP/gaP///wAAAAAAACH5BAEAAAUALAAAAAAMAAwAAAMlWLPcGjDKFYi9lxKBOaGcF35DhWHamZUW0K4mAbiwWtuf0uxFAgA7)

Để biến đổi một `Blob` thành base64, chúng ta sẽ sử dụng đối tượng tích hợp `FileReader`. Nó có thể đọc dữ liệu từ Blob ở nhiều định dạng. Trong [chương tiếp theo](/file) chúng ta sẽ tìm hiểu kỹ hơn về nó.

Đây là bản demo tải xuống blob, bây giờ qua base-64:

```
let link = document.createElement('a');
link.download = 'hello.txt';

let blob = new Blob(['Hello, world!'], {type: 'text/plain'});

let reader = new FileReader();
reader.readAsDataURL(blob); // chuyển đổi blob thành base64 và gọi onload

reader.onload = function() {
  link.href = reader.result; // data url
  link.click();
};
```

Cả hai cách tạo URL của một `Blob` đều có thể sử dụng được. Nhưng thường thì `URL.createObjectURL(blob)` đơn giản và nhanh hơn.

URL.createObjectURL(blob)

- Chúng ta cần revoke chúng nếu quan tâm đến bộ nhớ.
- Truy cập trực tiếp vào blob, không có "encoding/decoding"

Blob sang data url

- Không cần revoke bất cứ thứ gì.
- Hiệu suất và tổn thất bộ nhớ trên các đối tượng `Blob` lớn cho việc encoding.

## [Hình ảnh sang blob](#image-to-blob)

Chúng ta có thể tạo một `Blob` của hình ảnh, một phần hình ảnh, hoặc thậm chí tạo ảnh chụp màn hình trang. Điều đó hữu ích để tải nó lên đâu đó.

Các thao tác hình ảnh được thực hiện thông qua phần tử `<canvas>`:

1. Vẽ hình ảnh (hoặc phần của nó) trên canvas bằng [canvas.drawImage](https://developer.mozilla.org/en-US/docs/Web/api/CanvasRenderingContext2D/drawImage).
2. Gọi phương thức canvas [.toBlob(callback, format, quality)](https://developer.mozilla.org/en-US/docs/Web/api/HTMLCanvasElement/toBlob) tạo một `Blob` và chạy `callback` với nó khi hoàn tất.

Trong ví dụ dưới đây, hình ảnh chỉ được sao chép, nhưng chúng ta có thể cắt từ nó, hoặc biến đổi nó trên canvas trước khi tạo blob:

```
// lấy bất kỳ hình ảnh nào
let img = document.querySelector('img');

// tạo <canvas> cùng kích thước
let canvas = document.createElement('canvas');
canvas.width = img.clientWidth;
canvas.height = img.clientHeight;

let context = canvas.getContext('2d');

// sao chép hình ảnh vào nó (phương pháp này cho phép cắt hình ảnh)
context.drawImage(img, 0, 0);
// chúng ta có thể context.rotate(), và làm nhiều thứ khác trên canvas

// toBlob là thao tác bất đồng bộ, callback được gọi khi hoàn tất
canvas.toBlob(function(blob) {
  // blob sẵn sàng, tải xuống nó
  let link = document.createElement('a');
  link.download = 'example.png';

  link.href = URL.createObjectURL(blob);
  link.click();

  // xóa tham chiếu blob nội bộ, để trình duyệt giải phóng bộ nhớ từ nó
  URL.revokeObjectURL(link.href);
}, 'image/png');
```

Nếu chúng ta thích `async/await` thay vì callbacks:

```
let blob = await new Promise(resolve => canvasElem.toBlob(resolve, 'image/png'));
```

Đối với ảnh chụp màn hình trang, chúng ta có thể sử dụng thư viện như <https://github.com/niklasvh/html2canvas>. Những gì nó làm là duyệt trang và vẽ nó trên `<canvas>`. Sau đó chúng ta có thể lấy một `Blob` của nó theo cùng cách như trên.

## [Từ Blob sang ArrayBuffer](#from-blob-to-arraybuffer)

Constructor `Blob` cho phép tạo blob từ hầu hết mọi thứ, bao gồm bất kỳ `BufferSource` nào.

Nhưng nếu chúng ta cần thực hiện xử lý cấp thấp, chúng ta có thể lấy `ArrayBuffer` cấp thấp nhất từ `blob.arrayBuffer()`:

```
// lấy arrayBuffer từ blob
const bufferPromise = await blob.arrayBuffer();

// hoặc
blob.arrayBuffer().then(buffer => /* xử lý ArrayBuffer */);
```

## [Từ Blob sang stream](#from-blob-to-stream)

Khi chúng ta đọc và ghi vào một blob lớn hơn `2 GB`, việc sử dụng `arrayBuffer` trở nên tốn bộ nhớ hơn cho chúng ta. Tại thời điểm này, chúng ta có thể trực tiếp chuyển đổi blob thành stream.

Stream là một đối tượng đặc biệt cho phép đọc từ nó (hoặc ghi vào nó) từng phần một. Nó nằm ngoài phạm vi của chúng ta ở đây, nhưng đây là một ví dụ, và bạn có thể đọc thêm tại <https://developer.mozilla.org/en-US/docs/Web/API/Streams_API>. Streams tiện lợi cho dữ liệu phù hợp để xử lý từng mảnh.

Phương thức `stream()` của interface `Blob` trả về một `ReadableStream` mà khi đọc sẽ trả về dữ liệu chứa trong `Blob`.

Sau đó chúng ta có thể đọc từ nó, như thế này:

```
// lấy readableStream từ blob
const readableStream = blob.stream();
const stream = readableStream.getReader();

while (true) {
  // cho mỗi vòng lặp: value là fragment blob tiếp theo
  let { done, value } = await stream.read();
  if (done) {
    // không còn dữ liệu nào trong stream
    console.log('đã xử lý tất cả blob.');
    break;
  }

   // làm gì đó với phần dữ liệu chúng ta vừa đọc từ blob
  console.log(value);
}
```

## [Tóm tắt](#summary)

Trong khi `ArrayBuffer`, `Uint8Array` và các `BufferSource` khác là "dữ liệu nhị phân", [Blob](https://www.w3.org/TR/FileAPI/#dfn-Blob) đại diện cho "dữ liệu nhị phân có loại".

Điều đó làm cho Blobs thuận tiện cho các thao tác tải lên/tải xuống, vốn rất phổ biến trong trình duyệt.

Các phương thức thực hiện yêu cầu web, như [XMLHttpRequest](/xmlhttprequest), [fetch](/fetch) và cứ thế, có thể làm việc với `Blob` native, cũng như với các kiểu nhị phân khác.

Chúng ta có thể dễ dàng chuyển đổi giữa `Blob` và các kiểu dữ liệu nhị phân cấp thấp:

- Chúng ta có thể tạo một `Blob` từ một mảng kiểu bằng constructor `new Blob(...)`.
- Chúng ta có thể lấy lại `ArrayBuffer` từ một Blob bằng `blob.arrayBuffer()`, và sau đó tạo một view trên nó để xử lý nhị phân cấp thấp.

Các stream chuyển đổi rất hữu ích khi chúng ta cần xử lý blob lớn. Bạn có thể dễ dàng tạo một `ReadableStream` từ một blob. Phương thức `stream()` của interface `Blob` trả về một `ReadableStream` mà khi đọc sẽ trả về dữ liệu chứa trong blob.
