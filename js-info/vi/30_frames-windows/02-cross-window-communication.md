# Giao tiếp giữa các cửa sổ

> Source: [https://javascript.info/cross-window-communication](https://javascript.info/cross-window-communication)

<!-- fetched: 2026-09-14 -->

Chính sách "Same Origin" (cùng trang/web) hạn chế quyền truy cập của các cửa sổ và khung vào nhau.

Ý tưởng là nếu một người dùng có hai trang mở: một từ `john-smith.com`, và trang kia là `gmail.com`, thì họ không muốn một script từ `john-smith.com` đọc thư của họ từ `gmail.com`. Vì vậy, mục đích của chính sách "Same Origin" là bảo vệ người dùng khỏi đánh cắp thông tin.

## [Cùng origin (Same Origin)](#same-origin)

Hai URL được gọi là có "cùng origin" nếu chúng có cùng giao thức, miền và cổng.

Các URL sau đây đều có cùng origin:

- `http://site.com`
- `http://site.com/`
- `http://site.com/my/page.html`

Các URL sau đây thì không:

- `http://www.site.com` (miền khác: `www.` quan trọng)
- `http://site.org` (miền khác: `.org` quan trọng)
- `https://site.com` (giao thức khác: `https`)
- `http://site.com:8080` (cổng khác: `8080`)

Chính sách "Same Origin" quy định rằng:

- nếu chúng ta có tham chiếu đến một cửa sổ khác, ví dụ popup được tạo bởi `window.open` hoặc một cửa sổ bên trong `<iframe>`, và cửa sổ đó đến từ cùng origin, thì chúng ta có quyền truy cập đầy đủ vào cửa sổ đó.
- ngược lại, nếu nó đến từ origin khác, thì chúng ta không thể truy cập nội dung của cửa sổ đó: biến, tài liệu, bất cứ thứ gì. Ngoại lệ duy nhất là `location`: chúng ta có thể thay đổi nó (do đó chuyển hướng người dùng). Nhưng chúng ta không thể *đọc* location (vì vậy không thể biết người dùng đang ở đâu, không có rò rỉ thông tin).

### [Trong thực tế: iframe](#in-action-iframe)

Thẻ `<iframe>` chứa một cửa sổ nhúng riêng biệt, với các đối tượng `document` và `window` riêng biệt.

Chúng ta có thể truy cập chúng bằng các thuộc tính:

- `iframe.contentWindow` để lấy cửa sổ bên trong `<iframe>`.
- `iframe.contentDocument` để lấy tài liệu bên trong `<iframe>`, viết tắt của `iframe.contentWindow.document`.

Khi chúng ta truy cập thứ gì đó bên trong cửa sổ nhúng, trình duyệt kiểm tra xem iframe có cùng origin không. Nếu không thì quyền truy cập bị từ chối (ghi vào `location` là ngoại lệ, vẫn được phép).

Ví dụ, hãy thử đọc và ghi vào `<iframe>` từ origin khác:

```
<iframe src="https://example.com" id="iframe"></iframe>

<script>
  iframe.onload = function() {
    // chúng ta có thể lấy tham chiếu đến cửa sổ con
    let iframeWindow = iframe.contentWindow; // OK
    try {
      // ...nhưng không thể truy cập vào tài liệu bên trong nó
      let doc = iframe.contentDocument; // LỖI
    } catch(e) {
      alert(e); // Lỗi Bảo mật (origin khác)
    }

    // chúng ta cũng không thể ĐỌC URL của trang trong iframe
    try {
      // Không thể đọc URL từ đối tượng Location
      let href = iframe.contentWindow.location.href; // LỖI
    } catch(e) {
      alert(e); // Lỗi Bảo mật
    }

    // ...chúng ta có thể GHI vào location (và do đó tải thứ gì đó khác vào iframe)!
    iframe.contentWindow.location = '/'; // OK

    iframe.onload = null; // xóa trình xử lý, không chạy nó sau khi thay đổi location
  };
</script>
```

Mã ở trên hiển thị lỗi cho mọi thao tác ngoại trừ:

- Lấy tham chiếu đến cửa sổ con `iframe.contentWindow` – điều đó được phép.
- Ghi vào `location`.

Ngược lại, nếu `<iframe>` có cùng origin, chúng ta có thể làm mọi thứ với nó:

```
<!-- iframe từ cùng trang web -->
<iframe src="/" id="iframe"></iframe>

<script>
  iframe.onload = function() {
    // chỉ cần làm bất cứ điều gì
    iframe.contentDocument.body.prepend("Xin chào, thế giới!");
  };
</script>
```

`iframe.onload` vs `iframe.contentWindow.onload`

Sự kiện `iframe.onload` (trên thẻ `<iframe>`) về cơ bản giống với `iframe.contentWindow.onload` (trên đối tượng cửa sổ nhúng). Nó kích hoạt khi cửa sổ nhúng tải hoàn toàn với tất cả tài nguyên.

…Nhưng chúng ta không thể truy cập `iframe.contentWindow.onload` cho iframe từ origin khác, vì vậy sử dụng `iframe.onload`.

## [Cửa sổ trên các subdomain: document.domain](#windows-on-subdomains-document-domain)

Theo định nghĩa, hai URL với miền khác nhau có origin khác nhau.

Nhưng nếu các cửa sổ chia sẻ cùng miền cấp hai, ví dụ `john.site.com`, `peter.site.com` và `site.com` (vì vậy miền cấp hai chung của chúng là `site.com`), chúng ta có thể khiến trình duyệt bỏ qua sự khác biệt đó, vì vậy chúng có thể được coi là đến từ "cùng origin" cho mục đích giao tiếp giữa các cửa sổ.

Để làm được điều đó, mỗi cửa sổ như vậy nên chạy mã:

```
document.domain = 'site.com';
```

Vậy là đủ. Bây giờ chúng có thể tương tác mà không có hạn chế. Một lần nữa, điều đó chỉ có thể xảy ra đối với các trang có cùng miền cấp hai.

Đã lỗi thời, nhưng vẫn hoạt động

Thuộc tính `document.domain` đang trong quá trình bị loại bỏ khỏi [specification](https://html.spec.whatwg.org/multipage/origin.html#relaxing-the-same-origin-restriction). Giao tiếp giữa các cửa sổ (được giải thích sớm hơn bên dưới) là giải pháp thay thế được đề xuất.

Tuy nhiên, hiện tại tất cả các trình duyệt đều hỗ trợ nó. Và việc hỗ trợ sẽ được duy trì trong tương lai, để không phá vỡ mã cũ dựa vào `document.domain`.

## [Iframe: cạm bẫy document sai](#iframe-wrong-document-pitfall)

Khi một iframe đến từ cùng origin, và chúng ta có thể truy cập `document` của nó, có một cạm bẫy. Nó không liên quan đến các vấn đề cross-origin, nhưng quan trọng cần biết.

Ngay khi được tạo, iframe ngay lập tức có một tài liệu. Nhưng tài liệu đó khác với tài liệu đang tải vào nó!

Vì vậy, nếu chúng ta làm điều gì đó với tài liệu ngay lập tức, nó có thể bị mất.

Hãy xem:

```
<iframe src="/" id="iframe"></iframe>

<script>
  let oldDoc = iframe.contentDocument;
  iframe.onload = function() {
    let newDoc = iframe.contentDocument;
    // tài liệu đã tải không giống như ban đầu!
    alert(oldDoc == newDoc); // false
  };
</script>
```

Chúng ta không nên làm việc với tài liệu của iframe chưa tải, vì đó là *tài liệu sai*. Nếu chúng ta đặt bất kỳ trình xử lý sự kiện nào lên nó, chúng sẽ bị bỏ qua.

Làm thế nào để phát hiện khoảnh khắc khi tài liệu có đó?

Tài liệu đúng chắc chắn có đó khi `iframe.onload` kích hoạt. Nhưng nó chỉ kích hoạt khi toàn bộ iframe với tất cả tài nguyên được tải.

Chúng ta có thể cố gắng bắt khoảnh khắc sớm hơn bằng cách sử dụng các kiểm tra trong `setInterval`:

```
<iframe src="/" id="iframe"></iframe>

<script>
  let oldDoc = iframe.contentDocument;

  // mỗi 100ms kiểm tra xem tài liệu có phải là mới không
  let timer = setInterval(() => {
    let newDoc = iframe.contentDocument;
    if (newDoc == oldDoc) return;

    alert("Tài liệu mới đã có!");

    clearInterval(timer); // hủy setInterval, không cần nó nữa
  }, 100);
</script>
```

## [Danh sách: window.frames](#collection-window-frames)

Một cách khác để lấy đối tượng cửa sổ cho `<iframe>` – là lấy nó từ danh sách có tên `window.frames`:

- Theo số: `window.frames[0]` – đối tượng cửa sổ cho khung đầu tiên trong tài liệu.
- Theo tên: `window.frames.iframeName` – đối tượng cửa sổ cho khung có `name="iframeName"`.

Ví dụ:

```
<iframe src="/" style="height:80px" name="win" id="iframe"></iframe>

<script>
  alert(iframe.contentWindow == frames[0]); // true
  alert(iframe.contentWindow == frames.win); // true
</script>
```

Một iframe có thể có các iframe khác bên trong. Các đối tượng `window` tương ứng tạo thành một hệ thống phân cấp.

Các liên kết điều hướng là:

- `window.frames` – danh sách các cửa sổ "con" (đối với các khung lồng nhau).
- `window.parent` – tham chiếu đến cửa sổ "cha" (bên ngoài).
- `window.top` – tham chiếu đến cửa sổ cha lớn nhất.

Ví dụ:

```
window.frames[0].parent === window; // true
```

Chúng ta có thể sử dụng thuộc tính `top` để kiểm tra xem tài liệu hiện tại có đang mở trong khung hay không:

```
if (window == top) { // cửa sổ hiện tại == window.top?
  alert('Script đang chạy ở cửa sổ trên cùng, không phải trong khung');
} else {
  alert('Script đang chạy trong khung!');
}
```

## [Thuộc tính iframe "sandbox"](#the-sandbox-iframe-attribute)

Thuộc tính `sandbox` cho phép loại bỏ một số hành vi nhất định bên trong một `<iframe>` để ngăn nó thực thi mã không đáng tin cậy. Nó "sandbox" iframe bằng cách coi nó đến từ origin khác và/hoặc áp dụng các hạn chế khác.

Có một "tập hợp mặc định" các hạn chế được áp dụng cho `<iframe sandbox src="...">`. Nhưng nó có thể được nới lỏng nếu chúng ta cung cấp một danh sách các hạn chế được phân cách bằng khoảng trắng không nên áp dụng làm giá trị của thuộc tính, như thế này: `<iframe sandbox="allow-forms allow-popups">`.

Nói cách khác, một thuộc tính `"sandbox"` trống đặt các hạn chế nghiêm ngặt nhất có thể, nhưng chúng ta có thể đặt một danh sách được phân cách bằng dấu cách của những cái chúng ta muốn bỏ.

Đây là danh sách các hạn chế:

`allow-same-origin`
:   Theo mặc định, `"sandbox"` bắt buộc chính sách "origin khác" cho iframe. Nói cách khác, nó khiến trình duyệt coi `iframe` đến từ origin khác, ngay cả khi `src` của nó trỏ đến cùng trang web. Với tất cả các hạn chế ám chỉ cho script. Tùy chọn này loại bỏ tính năng đó.

`allow-top-navigation`
:   Cho phép `iframe` thay đổi `parent.location`.

`allow-forms`
:   Cho phép gửi biểu mẫu từ `iframe`.

`allow-scripts`
:   Cho phép chạy script từ `iframe`.

`allow-popups`
:   Cho phép `window.open` popup từ `iframe`

Xem [tài liệu](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/iframe) để biết thêm.

Ví dụ dưới đây minh họa một iframe sandboxed với tập hợp hạn chế mặc định: `<iframe sandbox src="...">`. Nó có một số JavaScript và biểu mẫu.

Xin lưu ý rằng không có gì hoạt động. Vì vậy, tập hợp mặc định thực sự nghiêm ngặt:

Kết quả

index.html

sandboxed.html

```
<!doctype html>
<html>

<head>
  <meta charset="UTF-8">
</head>

<body>

  <div>iframe bên dưới có thuộc tính <code>sandbox</code>.</div>

  <iframe sandbox src="sandboxed.html" style="height:60px;width:90%"></iframe>

</body>
</html>
```

```
<!doctype html>
<html>

<head>
  <meta charset="UTF-8">
</head>

<body>

  <button onclick="alert(123)">Nhấp để chạy script (không hoạt động)</button>

  <form action="http://google.com">
    <input type="text">
    <input type="submit" value="Gửi (không hoạt động)">
  </form>

</body>
</html>
```

Xin lưu ý:

Mục đích của thuộc tính `"sandbox"` chỉ là *thêm nhiều hạn chế hơn*. Nó không thể xóa chúng. Cụ thể, nó không thể nới lỏng các hạn chế same-origin nếu iframe đến từ origin khác.

## [Giao tiếp giữa các cửa sổ](#cross-window-messaging)

Giao diện `postMessage` cho phép các cửa sổ trò chuyện với nhau bất kể chúng đến từ origin nào.

Vì vậy, đó là cách vượt qua chính sách "Same Origin". Nó cho phép một cửa sổ từ `john-smith.com` trò chuyện với `gmail.com` và trao đổi thông tin, nhưng chỉ khi cả hai đều đồng ý và gọi các hàm JavaScript tương ứng. Điều đó làm cho nó an toàn cho người dùng.

Giao diện có hai phần.

### [postMessage](#postmessage)

Cửa sổ muốn gửi tin nhắn gọi phương thức [postMessage](https://developer.mozilla.org/en-US/docs/Web/API/Window.postMessage) của cửa sổ nhận. Nói cách khác, nếu chúng ta muốn gửi tin nhắn đến `win`, chúng ta nên gọi `win.postMessage(data, targetOrigin)`.

Các đối số:

`data`
:   Dữ liệu để gửi. Có thể là bất kỳ đối tượng nào, dữ liệu được sao chép bằng "thuật toán serialization có cấu trúc". IE chỉ hỗ trợ chuỗi, vì vậy chúng ta nên `JSON.stringify` các đối tượng phức tạp để hỗ trợ trình duyệt đó.

`targetOrigin`
:   Chỉ định origin cho cửa sổ mục tiêu, vì vậy chỉ một cửa sổ từ origin đã cho mới nhận được tin nhắn.

`targetOrigin` là biện pháp an toàn. Hãy nhớ lại, nếu cửa sổ mục tiêu đến từ origin khác, chúng ta không thể đọc `location` của nó trong cửa sổ người gửi. Vì vậy, chúng ta không thể chắc chắn trang web nào đang mở trong cửa sổ dự định: người dùng có thể đã điều hướng đi chỗ khác, và cửa sổ người gửi không biết về điều đó.

Việc chỉ định `targetOrigin` đảm bảo rằng cửa sổ chỉ nhận dữ liệu nếu nó vẫn đang ở trang web đúng. Quan trọng khi dữ liệu nhạy cảm.

Ví dụ, ở đây `win` sẽ chỉ nhận tin nhắn nếu nó có tài liệu từ origin `http://example.com`:

```
<iframe src="http://example.com" name="example">

<script>
  let win = window.frames.example;

  win.postMessage("message", "http://example.com");
</script>
```

Nếu chúng ta không muốn kiểm tra đó, chúng ta có thể đặt `targetOrigin` thành `*`.

```
<iframe src="http://example.com" name="example">

<script>
  let win = window.frames.example;

  win.postMessage("message", "*");
</script>
```

### [onmessage](#onmessage)

Để nhận tin nhắn, cửa sổ mục tiêu cần có trình xử lý trên sự kiện `message`. Nó kích hoạt khi `postMessage` được gọi (và kiểm tra `targetOrigin` thành công).

Đối tượng sự kiện có các thuộc tính đặc biệt:

`data`
:   Dữ liệu từ `postMessage`.

`origin`
:   Origin của người gửi, ví dụ `http://javascript.info`.

`source`
:   Tham chiếu đến cửa sổ người gửi. Chúng ta có thể ngay lập tức `source.postMessage(...)` lại nếu muốn.

Để gán trình xử lý đó, chúng ta nên sử dụng `addEventListener`, cú pháp ngắn `window.onmessage` không hoạt động.

Đây là một ví dụ:

```
window.addEventListener("message", function(event) {
  if (event.origin != 'http://javascript.info') {
    // thứ gì đó từ miền không xác định, hãy bỏ qua nó
    return;
  }

  alert( "Đã nhận: " + event.data );

  // có thể gửi tin nhắn lại bằng event.source.postMessage(...)
});
```

Ví dụ đầy đủ:

Kết quả

iframe.html

index.html

```
<!doctype html>
<html>

<head>
  <meta charset="UTF-8">
</head>

<body>

  Nhận iframe.
  <script>
    window.addEventListener('message', function(event) {
      alert(`Đã nhận ${event.data} từ ${event.origin}`);
    });
  </script>

</body>
</html>
```

```
<!doctype html>
<html>

<head>
  <meta charset="UTF-8">
</head>

<body>

  <form id="form">
    <input type="text" placeholder="Nhập tin nhắn" name="message">
    <input type="submit" value="Nhấp để gửi">
  </form>

  <iframe src="iframe.html" id="iframe" style="display:block;height:60px"></iframe>

  <script>
    form.onsubmit = function() {
      iframe.contentWindow.postMessage(this.message.value, '*');
      return false;
    };
  </script>

</body>
</html>
```

## [Tóm tắt](#summary)

Để gọi các phương thức và truy cập nội dung của cửa sổ khác, chúng ta cần trước tiên có tham chiếu đến nó.

Đối với popup, chúng ta có các tham chiếu sau:

- Từ cửa sổ opener: `window.open` – mở cửa sổ mới và trả về tham chiếu đến nó,
- Từ popup: `window.opener` – là tham chiếu đến cửa sổ opener từ một popup.

Đối với iframe, chúng ta có thể truy cập cửa sổ cha/con bằng cách sử dụng:

- `window.frames` – danh sách các đối tượng cửa sổ lồng nhau,
- `window.parent`, `window.top` là các tham chiếu đến cửa sổ cha và cửa sổ trên cùng,
- `iframe.contentWindow` là cửa sổ bên trong thẻ `<iframe>`.

Nếu các cửa sổ chia sẻ cùng origin (host, cổng, giao thức), thì các cửa sổ có thể làm bất cứ điều gì chúng muốn với nhau.

Nếu không, chỉ các hành động sau là có thể:

- Thay đổi `location` của cửa sổ khác (truy cập chỉ ghi).
- Gửi tin nhắn đến nó.

Các ngoại lệ là:

- Các cửa sổ chia sẻ cùng miền cấp hai: `a.site.com` và `b.site.com`. Sau đó, đặt `document.domain='site.com'` trong cả hai đặt chúng vào trạng thái "cùng origin".
- Nếu một iframe có thuộc tính `sandbox`, nó bị buộc vào trạng thái "origin khác", trừ khi `allow-same-origin` được chỉ định trong giá trị thuộc tính. Điều đó có thể được sử dụng để chạy mã không đáng tin cậy trong iframe từ cùng trang web.

Giao diện `postMessage` cho phép hai cửa sổ với mọi origin trò chuyện với nhau:

1. Người gửi gọi `targetWin.postMessage(data, targetOrigin)`.
2. Nếu `targetOrigin` không phải là `'*'`, thì trình duyệt kiểm tra xem cửa sổ `targetWin` có origin là `targetOrigin` không.
3. Nếu đúng như vậy, thì `targetWin` kích hoạt sự kiện `message` với các thuộc tính đặc biệt:

   - `origin` – origin của cửa sổ người gửi (như `http://my.site.com`)
   - `source` – tham chiếu đến cửa sổ người gửi.
   - `data` – dữ liệu, bất kỳ đối tượng nào ở mọi nơi ngoại trừ IE chỉ hỗ trợ chuỗi.

   Chúng ta nên sử dụng `addEventListener` để đặt trình xử lý cho sự kiện này bên trong cửa sổ mục tiêu.
