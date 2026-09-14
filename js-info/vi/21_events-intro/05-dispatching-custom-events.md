# Gửi sự kiện tùy chỉnh

> Source: [https://javascript.info/dispatch-events](https://javascript.info/dispatch-events)

<!-- fetched: 2026-09-14 -->

Chúng ta không chỉ có thể gán trình xử lý, mà còn có thể tạo sự kiện từ JavaScript.

Sự kiện tùy chỉnh có thể được dùng để tạo "thành phần đồ họa". Ví dụ, phần tử gốc của menu JS dựa trên của chúng ta có thể kích hoạt sự kiện báo cho biết những gì xảy ra với menu: `open` (menu mở), `select` (một mục được chọn) và cứ thế. Code khác có thể lắng nghe sự kiện và quan sát những gì xảy ra với menu.

Chúng ta có thể tạo không chỉ các sự kiện hoàn toàn mới mà chúng ta phát minh cho mục đích riêng, mà còn cả các sự kiện tích hợp, như `click`, `mousedown` v.v. Điều đó có thể hữu ích cho kiểm thử tự động.

## [Hàm tạo sự kiện](#event-constructor)

Các lớp sự kiện tích hợp tạo thành một hệ thống phân cấp, tương tự các lớp phần tử DOM. Gốc là lớp [Event](https://dom.spec.whatwg.org/#events) tích hợp.

Chúng ta có thể tạo đối tượng `Event` như sau:

```
let event = new Event(type[, options]);
```

Đối số:

- *type* – tên sự kiện, một chuỗi như `"click"` hoặc của riêng chúng ta như `"my-event"`.
- *options* – đối tượng với hai thuộc tính tùy chọn:

  - `bubbles: true/false` – nếu `true`, thì sự kiện tràn.
  - `cancelable: true/false` – nếu `true`, thì "hành động mặc định" có thể bị ngăn. Sau này chúng ta sẽ thấy điều đó có nghĩa gì đối với sự kiện tùy chỉnh.

  Mặc định cả hai là false: `{bubbles: false, cancelable: false}`.

## [dispatchEvent](#dispatchevent)

Sau khi đối tượng sự kiện được tạo, chúng ta cần "chạy" nó trên một phần tử bằng cách gọi `elem.dispatchEvent(event)`.

Sau đó trình xử lý phản ứng với nó giống như nếu đó là sự kiện trình duyệt thường. Nếu sự kiện được tạo với cờ `bubbles`, thì nó tràn.

Trong ví dụ dưới đây, sự kiện `click` được khởi tạo trong JavaScript. Trình xử lý hoạt động giống hệt như nếu nút được nhấp:

```
<button id="elem" onclick="alert('Click!');">Autoclick</button>

<script>
  let event = new Event("click");
  elem.dispatchEvent(event);
</script>
```

event.isTrusted

Có cách để phân biệt sự kiện "thực" của người dùng với sự kiện tạo bởi script.

Thuộc tính `event.isTrusted` là `true` cho các sự kiện đến từ hành động thực của người dùng và `false` cho sự kiện tạo bởi script.

## [Ví dụ tràn](#bubbling-example)

Chúng ta có thể tạo sự kiện tràn với tên `"hello"` và bắt nó trên `document`.

Tất cả những gì cần là đặt `bubbles` thành `true`:

```
<h1 id="elem">Hello from the script!</h1>

<script>
  // bắt trên document...
  document.addEventListener("hello", function(event) { // (1)
    alert("Hello from " + event.target.tagName); // Hello from H1
  });

  // ...dispatch trên elem!
  let event = new Event("hello", {bubbles: true}); // (2)
  elem.dispatchEvent(event);

  // trình xử lý trên document sẽ kích hoạt và hiển thị thông điệp.

</script>
```

Lưu ý:

1. Chúng ta nên dùng `addEventListener` cho sự kiện tùy chỉnh, vì `on<event>` chỉ tồn tại cho sự kiện tích hợp, `document.onhello` không hoạt động.
2. Phải đặt `bubbles:true`, nếu không sự kiện sẽ không tràn lên.

Cơ chế tràn giống nhau cho sự kiện tích hợp (`click`) và tùy chỉnh (`hello`). Cũng có các giai đoạn bắt giữ và tràn.

## [MouseEvent, KeyboardEvent và các loại khác](#mouseevent-keyboardevent-and-others)

Dưới đây là danh sách ngắn các lớp cho UI Events từ [UI Event specification](https://www.w3.org/TR/uievents):

- `UIEvent`
- `FocusEvent`
- `MouseEvent`
- `WheelEvent`
- `KeyboardEvent`
- …
```

Chúng ta nên dùng chúng thay vì `new Event` nếu muốn tạo các sự kiện như vậy. Ví dụ, `new MouseEvent("click")`.

Hàm tạo đúng cho phép chỉ định các thuộc tính tiêu chuẩn cho loại sự kiện đó.

Như `clientX/clientY` cho sự kiện chuột:

```
let event = new MouseEvent("click", {
  bubbles: true,
  cancelable: true,
  clientX: 100,
  clientY: 100
});

alert(event.clientX); // 100
```

Lưu ý: hàm tạo `Event` tổng quát không cho phép điều đó.

Hãy thử:

```
let event = new Event("click", {
  bubbles: true, // chỉ bubbles và cancelable
  cancelable: true, // hoạt động trong hàm tạo Event
  clientX: 100,
  clientY: 100
});

alert(event.clientX); // undefined, thuộc tính không biết bị bỏ qua!
```

Về mặt kỹ thuật, chúng ta có thể khắc phục bằng cách gán trực tiếp `event.clientX=100` sau khi tạo. Vì vậy đó là vấn đề tiện lợi và tuân thủ quy tắc. Sự kiện do trình duyệt tạo luôn có đúng loại.

Danh sách đầy đủ các thuộc tính cho các sự kiện UI khác nhau có trong đặc tả, ví dụ, [MouseEvent](https://www.w3.org/TR/uievents/#mouseevent).

## [Sự kiện tùy chỉnh](#custom-events)

Đối với các loại sự kiện hoàn toàn mới của riêng chúng ta như `"hello"`, chúng ta nên dùng `new CustomEvent`. Về mặt kỹ thuật [CustomEvent](https://dom.spec.whatwg.org/#customevent) giống hệt `Event`, với một ngoại lệ.

Trong đối số thứ hai (đối tượng), chúng ta có thể thêm thuộc tính bổ sung `detail` cho bất kỳ thông tin tùy chỉnh nào mà chúng ta muốn truyền cùng sự kiện.

Ví dụ:

```
<h1 id="elem">Hello for John!</h1>

<script>
  // chi tiết bổ sung đi cùng sự kiện đến trình xử lý
  elem.addEventListener("hello", function(event) {
    alert(event.detail.name);
  });

  elem.dispatchEvent(new CustomEvent("hello", {
    detail: { name: "John" }
  }));
</script>
```

Thuộc tính `detail` có thể có bất kỳ dữ liệu nào. Về mặt kỹ thuật chúng ta có thể sống không có nó, vì chúng ta có thể gán bất kỳ thuộc tính nào vào đối tượng `new Event` thường sau khi tạo. Nhưng `CustomEvent` cung cấp trường `detail` đặc biệt cho nó để tránh xung đột với các thuộc tính sự kiện khác.

Bên cạnh đó, lớp sự kiện mô tả "loại sự kiện gì" nó là, và nếu sự kiện là tùy chỉnh, thì chúng ta nên dùng `CustomEvent` để rõ ràng về những gì nó là.

## [event.preventDefault()](#event-preventdefault)

Nhiều sự kiện trình duyệt có "hành động mặc định", như điều hướng đến liên kết, bắt đầu chọn, và cứ thế.

Đối với sự kiện mới, tùy chỉnh, chắc chắn không có hành động trình duyệt mặc định, nhưng code gửi sự kiện như vậy có thể có kế hoạch riêng về những gì làm sau khi kích hoạt sự kiện.

Bằng cách gọi `event.preventDefault()`, trình xử lý sự kiện có thể gửi tín hiệu rằng các hành động đó nên bị hủy.

Trong trường hợp đó, lời gọi `elem.dispatchEvent(event)` trả về `false`. Và code đã gửi nó biết rằng nó không nên tiếp tục.

Hãy xem ví dụ thực tế – thỏ ẩn (có thể là menu đóng hoặc thứ gì khác).

Dưới đây bạn có thể thấy `#rabbit` và hàm `hide()` gửi sự kiện `"hide"` trên nó, để báo cho tất cả các bên quan tâm biết rằng thỏ sẽ ẩn.

Bất kỳ trình xử lý nào cũng có thể lắng nghe sự kiện đó bằng `rabbit.addEventListener('hide',...)` và, nếu cần, hủy hành động bằng `event.preventDefault()`. Sau đó thỏ sẽ không biến mất:

```
<pre id="rabbit">
  |\   /|
   \|_|/
   /. .\
  =\_Y_/=
   {>o<}
</pre>
<button onclick="hide()">Hide()</button>

<script>
  function hide() {
    let event = new CustomEvent("hide", {
      cancelable: true // không có cờ này preventDefault không hoạt động
    });
    if (!rabbit.dispatchEvent(event)) {
      alert('The action was prevented by a handler');
    } else {
      rabbit.hidden = true;
    }
  }

  rabbit.addEventListener('hide', function(event) {
    if (confirm("Call preventDefault?")) {
      event.preventDefault();
    }
  });
</script>
```

Lưu ý: sự kiện phải có cờ `cancelable: true`, nếu không lời gọi `event.preventDefault()` bị bỏ qua.

## [Sự kiện trong sự kiện là đồng bộ](#events-in-events-are-synchronous)

Thường sự kiện được xử lý trong hàng đợi. Nghĩa là: nếu trình duyệt đang xử lý `onclick` và một sự kiện mới xảy ra, ví dụ chuột di chuyển, thì việc xử lý nó được xếp hàng, trình xử lý `mousemove` tương ứng sẽ được gọi sau khi xử lý `onclick` hoàn tất.

Ngoại lệ đáng chú ý là khi một sự kiện được khởi tạo từ bên trong sự kiện khác, ví dụ dùng `dispatchEvent`. Các sự kiện như vậy được xử lý ngay lập tức: trình xử lý sự kiện mới được gọi, sau đó xử lý sự kiện hiện tại được tiếp tục.

Ví dụ, trong mã dưới đây, sự kiện `menu-open` được kích hoạt trong quá trình `onclick`.

Nó được xử lý ngay lập tức, không chờ trình xử lý `onclick` kết thúc:

```
<button id="menu">Menu (click me)</button>

<script>
  menu.onclick = function() {
    alert(1);

    menu.dispatchEvent(new CustomEvent("menu-open", {
      bubbles: true
    }));

    alert(2);
  };

  // kích hoạt giữa 1 và 2
  document.addEventListener('menu-open', () => alert('nested'));
</script>
```

Thứ tự đầu ra là: 1 → nested → 2.

Lưu ý rằng sự kiện lồng `menu-open` được bắt trên `document`. Việc truyền và xử lý sự kiện lồng kết thúc trước khi xử lý quay lại code ngoài (`onclick`).

Không chỉ về `dispatchEvent`, có các trường hợp khác. Nếu trình xử lý sự kiện gọi các phương thức kích hoạt sự kiện khác – chúng cũng được xử lý đồng bộ, theo kiểu lồng nhau.

Giả sử chúng ta không thích điều đó. Chúng ta muốn `onclick` được xử lý đầy đủ trước, độc lập với `menu-open` hoặc bất kỳ sự kiện lồng nào khác.

Sau đó chúng ta có thể đặt `dispatchEvent` (hoặc lời gọi kích hoạt sự kiện khác) ở cuối `onclick` hoặc, có thể tốt hơn, gói nó trong `setTimeout` trễ không:

```
<button id="menu">Menu (click me)</button>

<script>
  menu.onclick = function() {
    alert(1);

    setTimeout(() => menu.dispatchEvent(new CustomEvent("menu-open", {
      bubbles: true
    })));

    alert(2);
  };

  document.addEventListener('menu-open', () => alert('nested'));
</script>
```

Bây giờ `dispatchEvent` chạy không đồng bộ sau khi thực thi code hiện tại hoàn tất, bao gồm `menu.onclick`, vì vậy trình xử lý sự kiện hoàn toàn tách biệt.

Thứ tự đầu ra trở thành: 1 → 2 → nested.

## [Tóm tắt](#summary)

Để tạo sự kiện từ code, trước tiên chúng ta cần tạo đối tượng sự kiện.

Hàm tạo `Event(name, options)` chung chấp nhận tên sự kiện tùy ý và đối tượng `options` với hai thuộc tính:

- `bubbles: true` nếu sự kiện nên tràn.
- `cancelable: true` nếu `event.preventDefault()` nên hoạt động.

Các hàm tạo khác của sự kiện native như `MouseEvent`, `KeyboardEvent` và cứ thế chấp nhận các thuộc tính cụ thể cho loại sự kiện đó. Ví dụ, `clientX` cho sự kiện chuột.

Đối với sự kiện tùy chỉnh, chúng ta nên dùng hàm tạo `CustomEvent`. Nó có tùy chọn bổ sung gọi là `detail`, chúng ta nên gán dữ liệu cụ thể sự kiện cho nó. Sau đó tất cả trình xử lý có thể truy cập nó qua `event.detail`.

Mặc dù có khả năng kỹ thuật tạo sự kiện trình duyệt như `click` hoặc `keydown`, chúng ta nên dùng chúng với sự cẩn trọng cao.

Chúng ta không nên tạo sự kiện trình duyệt vì đó là cách hack để chạy trình xử lý. Đó là kiến trúc kém phần lớn thời gian.

Sự kiện native có thể được tạo:

- Như một hack bẩn để làm cho thư viện bên thứ ba hoạt động theo cách cần thiết, nếu chúng không cung cấp phương tiện tương tác khác.
- Cho kiểm thử tự động, để "nhấp vào nút" trong script và xem giao diện phản ứng đúng không.

Sự kiện tùy chỉnh với tên của riêng chúng ta thường được tạo cho mục đích kiến trúc, để báo hiệu những gì xảy ra trong menu, slider, carousel của chúng ta v.v.