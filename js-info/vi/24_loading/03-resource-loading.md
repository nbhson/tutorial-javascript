# Resource loading: onload và onerror

> Source: [https://javascript.info/onload-onerror](https://javascript.info/onload-onerror)

<!-- fetched: 2026-09-14 -->

Trình duyệt cho phép chúng ta theo dõi việc tải các tài nguyên external – scripts, iframes, ảnh, và các thứ tương tự.

Có hai sự kiện cho việc này:

- `onload` – tải thành công,
- `onerror` – có lỗi xảy ra.

## [Tải một script](#loading-a-script)

Giả sử chúng ta cần tải một script third-party và gọi một hàm nằm ở đó.

Chúng ta có thể tải nó động, như sau:

```
let script = document.createElement('script');
script.src = "my.js";

document.head.append(script);
```

…Nhưng làm thế nào để chạy hàm được khai báo bên trong script đó? Chúng ta cần chờ cho đến khi script tải xong, và chỉ sau đó mới có thể gọi nó.

Xin lưu ý:

Đối với scripts của chúng ta, chúng ta có thể dùng [JavaScript modules](/modules), nhưng chúng không được các thư viện third-party chấp nhận rộng rãi.

### [script.onload](#script-onload)

Helper chính là sự kiện `load`. Nó kích hoạt sau khi script được tải và thực thi.

Ví dụ:

```
let script = document.createElement('script');

// có thể tải bất kỳ script nào, từ bất kỳ domain nào
script.src = "https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.3.0/lodash.js"
document.head.append(script);

script.onload = function() {
  // script tạo một biến "_"
  alert( _.VERSION ); // hiển thị version của thư viện
};
```

Vậy trong `onload` chúng ta có thể dùng các biến của script, chạy các hàm, v.v.

…Và nếu việc tải thất bại thì sao? Ví dụ, không có script như vậy (lỗi 404) hoặc server bị lỗi (không khả dụng).

### [script.onerror](#script-onerror)

Các lỗi xảy ra trong quá trình tải script có thể được theo dõi trong sự kiện `error`.

Ví dụ, hãy request một script không tồn tại:

```
let script = document.createElement('script');
script.src = "https://example.com/404.js"; // không có script này
document.head.append(script);

script.onerror = function() {
  alert("Lỗi tải " + this.src); // Lỗi tải https://example.com/404.js
};
```

Xin lưu ý rằng chúng ta không thể nhận chi tiết HTTP error ở đây. Chúng ta không biết đó là lỗi 404 hay 500 hay thứ gì khác. Chỉ biết là việc tải thất bại.

Quan trọng:

Các sự kiện `onload`/`onerror` chỉ theo dõi việc tải itself.

Các lỗi có thể xảy ra trong quá trình xử lý và thực thi script nằm ngoài phạm vi của các sự kiện này. Tức là: nếu một script được tải thành công, thì `onload` kích hoạt, ngay cả khi nó có lỗi lập trình. Để theo dõi lỗi script, người ta có thể dùng handler global `window.onerror`.

## [Các tài nguyên khác](#other-resources)

Sự kiện `load` và `error` cũng hoạt động cho các tài nguyên khác, về cơ bản là bất kỳ tài nguyên nào có `src` external.

Ví dụ:

```
let img = document.createElement('img');
img.src = "https://js.cx/clipart/train.gif"; // (*)

img.onload = function() {
  alert(`Ảnh đã tải, kích thước ${img.width}x${img.height}`);
};

img.onerror = function() {
  alert("Có lỗi khi tải ảnh");
};
```

Tuy nhiên có vài điểm cần lưu ý:

- Hầu hết các tài nguyên bắt đầu tải khi chúng được thêm vào document. Nhưng `<img>` là một ngoại lệ. Nó bắt đầu tải khi nó có src `(*)`.
- Đối với `<iframe>`, sự kiện `iframe.onload` kích hoạt khi việc tải iframe kết thúc, cả cho tải thành công và trong trường hợp lỗi.

Điều đó là do lý do lịch sử.

## [Chính sách crossorigin](#crossorigin-policy)

Có một quy tắc: scripts từ một site không thể truy cập nội dung của site khác. Vậy, ví dụ, một script tại `https://facebook.com` không thể đọc mailbox của người dùng tại `https://gmail.com`.

Hay chính xác hơn, một origin (triplet domain/port/protocol) không thể truy cập nội dung từ origin khác. Vậy ngay cả khi chúng ta có một subdomain, hoặc chỉ là một port khác, những thứ đó là các origin khác nhau không có quyền truy cập vào nhau.

Quy tắc này cũng ảnh hưởng đến các tài nguyên từ các domain khác.

Nếu chúng ta đang dùng một script từ một domain khác, và có lỗi trong nó, chúng ta không thể nhận chi tiết lỗi.

Ví dụ, hãy lấy một script `error.js` gồm một hàm gọi (tệ) duy nhất:

```
// 📁 error.js
noSuchFunction();
```

Bây giờ tải nó từ cùng site nơi nó nằm:

```
<script>
window.onerror = function(message, url, line, col, errorObj) {
  alert(`${message}\n${url}, ${line}:${col}`);
};
</script>
<script src="/article/onload-onerror/crossorigin/error.js"></script>
```

Chúng ta có thể thấy một báo cáo lỗi tốt, như thế này:

```
Uncaught ReferenceError: noSuchFunction is not defined
https://javascript.info/article/onload-onerror/crossorigin/error.js, 1:1
```

Bây giờ hãy tải cùng script đó từ một domain khác:

```
<script>
window.onerror = function(message, url, line, col, errorObj) {
  alert(`${message}\n${url}, ${line}:${col}`);
};
</script>
<script src="https://cors.javascript.info/article/onload-onerror/crossorigin/error.js"></script>
```

Báo cáo khác, như thế này:

```
Script error.
, 0:0
```

Chi tiết có thể khác nhau tùy theo trình duyệt, nhưng ý tưởng là giống nhau: mọi thông tin về internals của một script, bao gồm error stack traces, bị ẩn. Chính xác là vì nó đến từ một domain khác.

Tại sao chúng ta cần chi tiết lỗi?

Có nhiều services (và chúng ta có thể tự xây dựng) nghe các lỗi global bằng `window.onerror`, lưu lỗi và cung cấp interface để truy cập và phân tích chúng. Thật tuyệt vời, vì chúng ta có thể thấy các lỗi thực tế, được kích hoạt bởi người dùng của chúng ta. Nhưng nếu một script đến từ một origin khác, thì không có nhiều thông tin về lỗi trong đó, như chúng ta vừa thấy.

Chính sách cross-origin tương tự (CORS) được enforce cho các loại tài nguyên khác nữa.

**Để cho phép truy cập cross-origin, thẻ `<script>` cần có thuộc tính `crossorigin`, cộng với server remote phải cung cấp các header đặc biệt.**

Có ba cấp độ truy cập cross-origin:

1. **Không có thuộc tính `crossorigin`** – truy cập bị cấm.
2. **`crossorigin="anonymous"`** – truy cập được cho phép nếu server phản hồi với header `Access-Control-Allow-Origin` với `*` hoặc origin của chúng ta. Trình duyệt không gửi thông tin authorization và cookies đến server remote.
3. **`crossorigin="use-credentials"`** – truy cập được cho phép nếu server gửi lại header `Access-Control-Allow-Origin` với origin của chúng ta và `Access-Control-Allow-Credentials: true`. Trình duyệt gửi thông tin authorization và cookies đến server remote.

Xin lưu ý:

Bạn có thể đọc thêm về truy cập cross-origin trong chương [Fetch: Cross-Origin Requests](/fetch-crossorigin). Nó mô tả phương thức `fetch` cho network requests, nhưng policy hoàn toàn giống nhau.

Chuyện như "cookies" nằm ngoài phạm vi hiện tại của chúng ta, nhưng bạn có thể đọc về chúng trong chương [Cookies, document.cookie](/cookie).

Trong trường hợp của chúng ta, chúng ta không có bất kỳ crossorigin attribute nào. Vậy truy cập cross-origin bị cấm. Hãy thêm nó vào.

Chúng ta có thể chọn giữa `"anonymous"` (không gửi cookies, cần một server-side header) và `"use-credentials"` (gửi cookies, cần hai server-side headers).

Nếu chúng ta không quan tâm đến cookies, thì `"anonymous"` là cách đi:

```
<script>
window.onerror = function(message, url, line, col, errorObj) {
  alert(`${message}\n${url}, ${line}:${col}`);
};
</script>
<script crossorigin="anonymous" src="https://cors.javascript.info/article/onload-onerror/crossorigin/error.js"></script>
```

Giờ đây, giả sử rằng server cung cấp header `Access-Control-Allow-Origin`, mọi thứ đều ổn. Chúng ta có báo cáo lỗi đầy đủ.

## [Tóm tắt](#summary)

Các ảnh `<img>`, external styles, scripts và các tài nguyên khác cung cấp các sự kiện `load` và `error` để theo dõi việc tải của chúng:

- `load` kích hoạt khi tải thành công,
- `error` kích hoạt khi tải thất bại.

Ngoại lệ duy nhất là `<iframe>`: do lý do lịch sử nó luôn kích hoạt `load`, cho bất kỳ việc tải nào hoàn tất, ngay cả khi trang không tìm thấy.

Sự kiện `readystatechange` cũng hoạt động cho các tài nguyên, nhưng hiếm khi được sử dụng, vì sự kiện `load/error` đơn giản hơn.

---

---

## Tasks

## [Tasks](#tasks)

### [Tải ảnh với callback](#load-images-with-a-callback)

importance: 4

Thông thường, ảnh được tải khi chúng được tạo. Vậy khi chúng ta thêm `<img>` vào trang, người dùng không thấy ảnh ngay lập tức. Trình duyệt cần tải nó trước.

Để hiển thị ảnh ngay lập tức, chúng ta có thể tạo nó "trước", như sau:

```
let img = document.createElement('img');
img.src = 'my.jpg';
```

Trình duyệt bắt đầu tải ảnh và nhớ nó trong cache. Sau đó, khi cùng ảnh xuất hiện trong document (bất kể thế nào), nó sẽ hiển thị ngay lập tức.

**Tạo hàm `preloadImages(sources, callback)` tải tất cả ảnh từ mảng `sources` và, khi sẵn sàng, chạy `callback`.**

Ví dụ, điều này sẽ hiển thị một `alert` sau khi ảnh được tải:

```
function loaded() {
  alert("Đã tải ảnh")
}

preloadImages(["1.jpg", "2.jpg", "3.jpg"], loaded);
```

Trong trường hợp có lỗi, hàm vẫn nên coi như ảnh đã "tải" xong.

Nói cách khác, `callback` được thực thi khi tất cả ảnh đều đã tải xong hoặc gặp lỗi.

Hàm hữu ích, ví dụ, khi chúng ta dự định hiển thị một gallery với nhiều ảnh có thể cuộn, và muốn đảm bảo rằng tất cả ảnh đều đã tải.

Trong source document bạn có thể tìm thấy links đến các test ảnh, và cũng là code để kiểm tra xem chúng có được tải hay chưa. Nó nên output `300`.

[Mở sandbox cho task.](https://plnkr.co/edit/e0RmWgFyyYt5k1ic?p=preview)

solution

Algorithm:

1. Tạo `img` cho mỗi source.
2. Thêm `onload/onerror` cho mỗi ảnh.
3. Tăng counter khi `onload` hoặc `onerror` kích hoạt.
4. Khi giá trị counter bằng với số sources – chúng ta đã xong: `callback()`.

[Mở solution trong sandbox.](https://plnkr.co/edit/wGSahhItuRACQKBU?p=preview)
