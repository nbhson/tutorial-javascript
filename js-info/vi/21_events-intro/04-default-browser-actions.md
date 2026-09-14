# Hành động mặc định của trình duyệt

> Source: [https://javascript.info/default-browser-action](https://javascript.info/default-browser-action)

<!-- fetched: 2026-09-14 -->

Nhiều sự kiện tự động dẫn đến các hành động nhất định được thực hiện bởi trình duyệt.

Ví dụ:

- Nhấp chuột vào một liên kết – khởi tạo điều hướng đến URL của nó.
- Nhấp chuột vào nút gửi biểu mẫu – khởi tạo gửi nó đến máy chủ.
- Nhấn nút chuột trên văn bản và di chuyển nó – chọn văn bản.

Nếu chúng ta xử lý sự kiện trong JavaScript, chúng ta có thể không muốn hành động trình duyệt tương ứng xảy ra, và muốn triển khai hành vi khác thay thế.

## [Ngăn hành động trình duyệt](#preventing-browser-actions)

Có hai cách để nói với trình duyệt rằng chúng ta không muốn nó hành động:

- Cách chính là dùng đối tượng `event`. Có phương thức `event.preventDefault()`.
- Nếu trình xử lý được gán bằng `on<event>` (không phải bằng `addEventListener`), thì trả về `false` cũng hoạt động tương tự.

Trong HTML này, một lần nhấp vào liên kết không dẫn đến điều hướng; trình duyệt không làm gì cả:

```
<a href="/" onclick="return false">Click here</a>
hoặc
<a href="/" onclick="event.preventDefault()">here</a>
```

Trong ví dụ tới, chúng ta sẽ dùng kỹ thuật này để tạo menu bằng JavaScript.

Trả về `false` từ trình xử lý là ngoại lệ

Giá trị trả về của trình xử lý sự kiện thường bị bỏ qua.

Ngoại lệ duy nhất là `return false` từ trình xử lý gán bằng `on<event>`.

Trong mọi trường hợp khác, giá trị `return` bị bỏ qua. Đặc biệt, không có lý do gì để trả về `true`.

### [Ví dụ: menu](#example-the-menu)

Xét menu trang web, như sau:

```
<ul id="menu" class="menu">
  <li><a href="/html">HTML</a></li>
  <li><a href="/javascript">JavaScript</a></li>
  <li><a href="/css">CSS</a></li>
</ul>
```

Đây là cách nó trông với một số CSS:

Các mục menu được triển khai dưới dạng liên kết HTML `<a>`, không phải nút `<button>`. Có vài lý do để làm vậy, ví dụ:

- Nhiều người thích dùng "nhấp chuột phải" – "mở trong cửa sổ mới". Nếu chúng ta dùng `<button>` hoặc `<span>`, điều đó không hoạt động.
- Công cụ tìm kiếm làm theo các liên kết `<a href="...">` khi lập chỉ mục.

Vì vậy chúng ta dùng `<a>` trong markup. Nhưng thông thường chúng ta dự định xử lý các lần nhấp trong JavaScript. Vì vậy chúng ta nên ngăn hành động mặc định của trình duyệt.

Như sau:

```
menu.onclick = function(event) {
  if (event.target.nodeName != 'A') return;

  let href = event.target.getAttribute('href');
  alert( href ); // ...có thể tải từ máy chủ, tạo UI v.v

  return false; // ngăn hành động trình duyệt (không điều hướng đến URL)
};
```

Nếu chúng ta bỏ qua `return false`, thì sau khi mã chúng ta thực thi, trình duyệt sẽ làm "hành động mặc định" – điều hướng đến URL trong `href`. Và chúng ta không cần điều đó ở đây, vì chúng ta đang xử lý nhấp chuột bằng chính mình.

Nhân tiện, dùng event delegation ở đây làm cho menu của chúng ta rất linh hoạt. Chúng ta có thể thêm danh sách lồng nhau và style chúng bằng CSS để "trượt xuống".

Sự kiện nối tiếp

Một số sự kiện chảy vào nhau. Nếu chúng ta ngăn sự kiện đầu tiên, sẽ không có sự kiện thứ hai.

Ví dụ, `mousedown` trên trường `<input>` dẫn đến focus trong đó, và sự kiện `focus`. Nếu chúng ta ngăn sự kiện `mousedown`, sẽ không có focus.

Thử nhấp vào `<input>` đầu tiên bên dưới – sự kiện `focus` xảy ra. Nhưng nếu bạn nhấp vào cái thứ hai, sẽ không có focus.

```
<input value="Focus works" onfocus="this.value=''">
<input onmousedown="return false" onfocus="this.value=''" value="Click me">
```

Điều đó là vì hành động trình duyệt bị hủy trên `mousedown`. Việc focus vẫn có thể xảy ra nếu chúng ta dùng cách khác để nhập vào input. Ví dụ, phím `Tab` để chuyển từ input 1 sang input 2. Nhưng không còn bằng nhấp chuột nữa.

## [Tùy chọn trình xử lý "passive"](#the-passive-handler-option)

Tùy chọn `passive: true` của `addEventListener` báo cho trình duyệt biết trình xử lý sẽ không gọi `preventDefault()`.

Tại sao điều đó có thể cần?

Có một số sự kiện như `touchmove` trên thiết bị di động (khi người dùng di chuyển ngón tay trên màn hình), gây cuộn mặc định, nhưng cuộn đó có thể bị ngăn bằng `preventDefault()` trong trình xử lý.

Vì vậy khi trình duyệt phát hiện sự kiện như vậy, nó phải xử lý tất cả trình xử lý trước, và sau đó nếu `preventDefault` không được gọi ở đâu, nó có thể tiếp tục với cuộn. Điều đó có thể gây trễ không cần thiết và "giật" trong UI.

Tùy chọn `passive: true` báo cho trình duyệt rằng trình xử lý sẽ không hủy cuộn. Sau đó trình duyệt cuộn ngay lập tức mang lại trải nghiệm mượt mà nhất, và sự kiện được xử lý đồng thời.

Đối với một số trình duyệt (Firefox, Chrome), `passive` mặc định là `true` cho các sự kiện `touchstart` và `touchmove`.

## [event.defaultPrevented](#event-defaultprevented)

Thuộc tính `event.defaultPrevented` là `true` nếu hành động mặc định bị ngăn, và `false` nếu ngược lại.

Có một trường hợp sử dụng thú vị cho nó.

Bạn nhớ trong chương [Bubbling and capturing](/bubbling-and-capturing) chúng ta đã nói về `event.stopPropagation()` và tại sao ngừng tràn là xấu không?

Đôi khi chúng ta có thể dùng `event.defaultPrevented` thay thế, để báo hiệu cho các trình xử lý sự kiện khác rằng sự kiện đã được xử lý.

Hãy xem ví dụ thực tế.

Mặc định, trình duyệt trên sự kiện `contextmenu` (nhấp chuột phải) hiển thị menu ngữ cảnh với các tùy chọn tiêu chuẩn. Chúng ta có thể ngăn nó và hiển thị menu của riêng, như sau:

```
<button>Right-click shows browser context menu</button>

<button oncontextmenu="alert('Draw our menu'); return false">
  Right-click shows our context menu
</button>
```

Bây giờ, ngoài menu ngữ cảnh đó, chúng ta muốn triển khai menu ngữ cảnh toàn tài liệu.

Khi nhấp chuột phải, menu ngữ cảnh gần nhất sẽ hiện lên.

```
<p>Right-click here for the document context menu</p>
<button id="elem">Right-click here for the button context menu</button>

<script>
  elem.oncontextmenu = function(event) {
    event.preventDefault();
    alert("Button context menu");
  };

  document.oncontextmenu = function(event) {
    event.preventDefault();
    alert("Document context menu");
  };
</script>
```

Vấn đề là khi chúng ta nhấp vào `elem`, chúng ta nhận được hai menu: menu cấp nút và (sự kiện tràn lên) menu cấp tài liệu.

Làm sao để sửa? Một trong các giải pháp là nghĩ như sau: "Khi chúng ta xử lý nhấp chuột phải trong trình xử lý nút, hãy ngừng tràn của nó" và dùng `event.stopPropagation()`:

```
<p>Right-click for the document menu</p>
<button id="elem">Right-click for the button menu (fixed with event.stopPropagation)</button>

<script>
  elem.oncontextmenu = function(event) {
    event.preventDefault();
    event.stopPropagation();
    alert("Button context menu");
  };

  document.oncontextmenu = function(event) {
    event.preventDefault();
    alert("Document context menu");
  };
</script>
```

Bây giờ menu cấp nút hoạt động như dự định. Nhưng giá phải trả cao. Chúng ta vĩnh viễn từ chối truy cập thông tin về nhấp chuột phải cho bất kỳ code ngoài nào, bao gồm các bộ đếm thu thập thống kê v.v. Điều đó khá phi lý trí.

Giải pháp thay thế là kiểm tra trong trình xử lý `document` xem hành động mặc định có bị ngăn không? Nếu có, thì sự kiện đã được xử lý, và chúng ta không cần phản ứng lại nó.

```
<p>Right-click for the document menu (added a check for event.defaultPrevented)</p>
<button id="elem">Right-click for the button menu</button>

<script>
  elem.oncontextmenu = function(event) {
    event.preventDefault();
    alert("Button context menu");
  };

  document.oncontextmenu = function(event) {
    if (event.defaultPrevented) return;

    event.preventDefault();
    alert("Document context menu");
  };
</script>
```

Bây giờ mọi thứ cũng hoạt động đúng. Nếu chúng ta có các phần tử lồng nhau, và mỗi cái có menu ngữ cảnh riêng, điều đó cũng hoạt động. Chỉ cần đảm bảo kiểm tra `event.defaultPrevented` trong mỗi trình xử lý `contextmenu`.

event.stopPropagation() và event.preventDefault()

Như chúng ta thấy rõ, `event.stopPropagation()` và `event.preventDefault()` (còn gọi là `return false`) là hai điều khác nhau. Chúng không liên quan đến nhau.

Kiến trúc menu ngữ cảnh lồng nhau

Cũng có các cách thay thế để triển khai menu ngữ cảnh lồng nhau. Một trong số đó là có một đối tượng toàn cục đơn với trình xử lý cho `document.oncontextmenu`, và cũng các phương thức cho phép chúng ta lưu trữ các trình xử lý khác trong nó.

Đối tượng sẽ bắt bất kỳ nhấp chuột phải, tìm qua các trình xử lý đã lưu và chạy cái phù hợp.

Nhưng sau đó mỗi đoạn code muốn có menu ngữ cảnh nên biết về đối tượng đó và dùng sự giúp đỡ của nó thay vì trình xử lý `contextmenu` riêng.

## [Tóm tắt](#summary)

Có nhiều hành động mặc định của trình duyệt:

- `mousedown` – bắt đầu chọn (di chuyển chuột để chọn).
- `click` trên `<input type="checkbox">` – đánh dấu/bỏ đánh dấu `input`.
- `submit` – nhấp vào `<input type="submit">` hoặc nhấn `Enter` trong trường biểu mẫu gây ra sự kiện này, và trình duyệt gửi biểu mẫu sau đó.
- `keydown` – nhấn phím có thể dẫn đến thêm ký tự vào trường, hoặc các hành động khác.
- `contextmenu` – sự kiện xảy ra khi nhấp chuột phải, hành động là hiển thị menu ngữ cảnh trình duyệt.
- …còn nhiều…

Tất cả hành động mặc định có thể bị ngăn nếu chúng ta muốn xử lý sự kiện exclusively bằng JavaScript.

Để ngăn hành động mặc định – dùng `event.preventDefault()` hoặc `return false`. Phương thức thứ hai chỉ hoạt động cho trình xử lý gán bằng `on<event>`.

Tùy chọn `passive: true` của `addEventListener` báo cho trình duyệt rằng hành động sẽ không bị ngăn. Điều đó hữu ích cho một số sự kiện di động, như `touchstart` và `touchmove`, để báo cho trình duyệt rằng nó không nên chờ tất cả trình xử lý hoàn thành trước khi cuộn.

Nếu hành động mặc định bị ngăn, giá trị của `event.defaultPrevented` trở thành `true`, ngược lại là `false`.

Giữ tính ngữ nghĩa, đừng lạm dụng

Về mặt kỹ thuật, bằng cách ngăn hành động mặc định và thêm JavaScript, chúng ta có thể tùy chỉnh hành vi của bất kỳ phần tử nào. Ví dụ, chúng ta có thể làm cho liên kết `<a>` hoạt động như nút, và nút `<button>` hoạt động như liên kết (điều hướng đến URL khác v.v).

Nhưng nói chung chúng ta nên giữ ý nghĩa ngữ nghĩa của các phần tử HTML. Ví dụ, `<a>` nên thực hiện điều hướng, không phải nút.

Bên cạnh là "chỉ là điều tốt", điều đó làm cho HTML của bạn tốt hơn về mặt khả năng truy cập.

Cũng nếu chúng ta xem xét ví dụ với `<a>`, thì xin lưu ý: trình duyệt cho phép chúng ta mở các liên kết như vậy trong cửa sổ mới (bằng cách nhấp chuột phải và các cách khác). Và mọi người thích điều đó. Nhưng nếu chúng ta làm cho nút hoạt động như liên kết bằng JavaScript và thậm chí trông như liên kết bằng CSS, thì các tính năng trình duyệt cụ thể cho `<a>` vẫn sẽ không hoạt động cho nó.

---

---

## Các bài tập

## [Tasks](#tasks)

### [Tại sao "return false" không hoạt động?](#why-return-false-doesn-t-work)

importance: 3

Tại sao trong mã dưới đây `return false` hoàn toàn không hoạt động?

```
<script>
  function handler() {
    alert( "..." );
    return false;
  }
</script>

<a href="https://w3.org" onclick="handler()">the browser will go to w3.org</a>
```

Trình duyệt làm theo URL khi nhấp, nhưng chúng ta không muốn vậy.

Làm sao để sửa?

solution

Khi trình duyệt đọc thuộc tính `on*` như `onclick`, nó tạo trình xử lý từ nội dung của nó.

Cho `onclick="handler()"` hàm sẽ là:

```
function(event) {
  handler() // nội dung của onclick
}
```

Bây giờ chúng ta có thể thấy giá trị trả về bởi `handler()` không được dùng và không ảnh hưởng đến kết quả.

Sửa đơn giản:

```
<script>
  function handler() {
    alert("...");
    return false;
  }
</script>

<a href="https://w3.org" onclick="return handler()">w3.org</a>
```

Cũng có thể dùng `event.preventDefault()`, như sau:

```
<script>
  function handler(event) {
    alert("...");
    event.preventDefault();
  }
</script>

<a href="https://w3.org" onclick="handler(event)">w3.org</a>
```

### [Bắt liên kết trong phần tử](#catch-links-in-the-element)

importance: 5

Làm cho tất cả liên kết bên trong phần tử có `id="contents"` hỏi người dùng liệu họ có thực sự muốn rời đi không. Và nếu không thì đừng điều hướng.

Như sau:

Chi tiết:

- HTML bên trong phần tử có thể được tải hoặc tạo lại động bất cứ lúc nào, vì vậy chúng ta không thể tìm tất cả liên kết và đặt trình xử lý trên chúng. Dùng event delegation.
- Nội dung có thể có thẻ lồng nhau. Bên trong liên kết cũng vậy, như `<a href=".."><i>...</i></a>`.

[Open a sandbox for the task.](https://plnkr.co/edit/wEVgoQjkbl47YQHS?p=preview)

solution

Đó là một cách dùng tuyệt vời của mẫu event delegation.

Trong đời thực thay vì hỏi, chúng ta có thể gửi yêu cầu "logging" đến máy chủ lưu thông tin về nơi người truy cập rời đi. Hoặc chúng ta có thể tải nội dung và hiển thị nó ngay trên trang (nếu cho phép).

Tất cả những gì cần là bắt `contents.onclick` và dùng `confirm` để hỏi người dùng. Ý tưởng tốt là dùng `link.getAttribute('href')` thay vì `link.href` cho URL. Xem giải pháp để biết chi tiết.

[Open the solution in a sandbox.](https://plnkr.co/edit/aleE38sfmV3CM7kB?p=preview)

### [Thư viện ảnh](#image-gallery)

importance: 5

Tạo thư viện ảnh nơi ảnh chính thay đổi bằng nhấp chuột vào ảnh thu nhỏ.

Như sau:

P.S. Dùng event delegation.

[Open a sandbox for the task.](https://plnkr.co/edit/f109tDcY1h2Ll0Qh?p=preview)

solution

Giải pháp là gán trình xử lý cho vùng chứa và theo dõi nhấp chuột. Nếu lần nhấp là trên liên kết `<a>`, thì thay đổi `src` của `#largeImg` thành `href` của ảnh thu nhỏ.

[Open the solution in a sandbox.](https://plnkr.co/edit/M87V9DEGPlAgeyOk?p=preview)