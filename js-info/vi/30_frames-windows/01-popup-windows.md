# Cửa sổ popup và các phương thức window

> Source: [https://javascript.info/popup-windows](https://javascript.info/popup-windows)

<!-- fetched: 2026-09-14 -->

Cửa sổ popup là một trong những phương pháp cổ xưa nhất để hiển thị tài liệu bổ sung cho người dùng.

Về cơ bản, bạn chỉ cần chạy:

```
window.open('https://javascript.info/')
```

…Và nó sẽ mở một cửa sổ mới với URL đã cho. Hầu hết các trình duyệt hiện đại được cấu hình để mở URL trong tab mới thay vì cửa sổ riêng biệt.

Popup tồn tại từ rất lâu rồi. Ý tưởng ban đầu là hiển thị nội dung khác mà không đóng cửa sổ chính. Hiện nay, có những cách khác để làm điều đó: chúng ta có thể tải nội dung động bằng [fetch](/fetch) và hiển thị nó trong `<div>` được tạo động. Vì vậy, popup không phải là thứ chúng ta sử dụng hàng ngày.

Ngoài ra, popup khá phức tạp trên thiết bị di động, những thiết bị không hiển thị nhiều cửa sổ cùng lúc.

Vẫn còn những tác vụ nơi popup vẫn được sử dụng, ví dụ như xác thực OAuth (đăng nhập bằng Google/Facebook/…), vì:

1. Popup là một cửa sổ riêng biệt có môi trường JavaScript độc lập. Vì vậy, mở popup từ trang web bên thứ ba, không đáng tin cậy là an toàn.
2. Rất dễ để mở một popup.
3. Popup có thể điều hướng (thay đổi URL) và gửi tin nhắn đến cửa sổ đã mở.

## [Chặn popup](#popup-blocking)

Trong quá khứ, các trang web độc hại đã lạm dụng popup rất nhiều. Một trang xấu có thể mở vô số cửa sổ popup với quảng cáo. Vì vậy, hiện nay hầu hết các trình duyệt cố gắng chặn popup và bảo vệ người dùng.

**Hầu hết các trình duyệt chặn popup nếu chúng được gọi outside của các trình xử lý sự kiện do người dùng kích hoạt như `onclick`.**

Ví dụ:

```
// popup bị chặn
window.open('https://javascript.info');

// popup được cho phép
button.onclick = () => {
  window.open('https://javascript.info');
};
```

Cách này người dùng được bảo vệ phần nào khỏi popup không mong muốn, nhưng chức năng không bị tắt hoàn toàn.

## [window.open](#window-open)

Cú pháp để mở popup là: `window.open(url, name, params)`:

url
:   URL để tải vào cửa sổ mới.

name
:   Tên của cửa sổ mới. Mỗi cửa sổ có một `window.name`, và ở đây chúng ta có thể chỉ định cửa sổ nào sẽ sử dụng cho popup. Nếu đã có cửa sổ với tên như vậy – URL đã cho sẽ mở trong đó, nếu không thì cửa sổ mới sẽ được mở.

params
:   Chuỗi cấu hình cho cửa sổ mới. Nó chứa các cài đặt, được phân cách bằng dấu phẩy. Không được có khoảng trắng trong params, ví dụ: `width=200,height=100`.

Các cài đặt cho `params`:

- Vị trí:
  - `left/top` (số) – tọa độ của góc trên bên trái cửa sổ trên màn hình. Có một giới hạn: cửa sổ mới không thể được định vị ngoài màn hình.
  - `width/height` (số) – chiều rộng và chiều cao của cửa sổ mới. Có giới hạn về chiều rộng/cao tối thiểu, vì vậy không thể tạo cửa sổ vô hình.
- Tính năng cửa sổ:
  - `menubar` (yes/no) – hiển thị hoặc ẩn thanh menu của trình duyệt trên cửa sổ mới.
  - `toolbar` (yes/no) – hiển thị hoặc ẩn thanh điều hướng của trình duyệt (quay lại, tiến tới, tải lại v.v.) trên cửa sổ mới.
  - `location` (yes/no) – hiển thị hoặc ẩn trường URL trong cửa sổ mới. FF và IE không cho phép ẩn nó theo mặc định.
  - `status` (yes/no) – hiển thị hoặc ẩn thanh trạng thái. Một lần nữa, hầu hết các trình duyệt bắt buộc hiển thị nó.
  - `resizable` (yes/no) – cho phép tắt khả năng thay đổi kích thước cho cửa sổ mới. Không khuyến nghị.
  - `scrollbars` (yes/no) – cho phép tắt thanh cuộn cho cửa sổ mới. Không khuyến nghị.

Cũng có một số tính năng cụ thể của trình duyệt ít được hỗ trợ hơn, thường không được sử dụng. Xem [window.open trong MDN](https://developer.mozilla.org/en/DOM/window.open) để biết ví dụ.

## [Ví dụ: cửa sổ tối giản](#example-a-minimalistic-window)

Hãy mở một cửa sổ với tập hợp tính năng tối thiểu, chỉ để xem trình duyệt cho phép tắt những tính năng nào:

```
let params = `scrollbars=no,resizable=no,status=no,location=no,toolbar=no,menubar=no,
width=0,height=0,left=-1000,top=-1000`;

open('/', 'test', params);
```

Ở đây hầu hết các "tính năng cửa sổ" bị tắt và cửa sổ được định vị ngoài màn hình. Chạy nó và xem những gì thực sự xảy ra. Hầu hết các trình duyệt "sửa chữa" những thứ kỳ lạ như `width/height` bằng không và `left/top` ngoài màn hình. Ví dụ, Chrome mở cửa sổ như vậy với chiều rộng/cao đầy đủ, chiếm toàn màn hình.

Hãy thêm các tùy chọn định vị bình thường và tọa độ `width`, `height`, `left`, `top` hợp lý:

```
let params = `scrollbars=no,resizable=no,status=no,location=no,toolbar=no,menubar=no,
width=600,height=300,left=100,top=100`;

open('/', 'test', params);
```

Hầu hết các trình duyệt hiển thị ví dụ trên như yêu cầu.

Quy tắc cho các cài đặt bị lược bỏ:

- Nếu không có đối số thứ 3 trong lệnh gọi `open`, hoặc nó trống, thì các tham số cửa sổ mặc định sẽ được sử dụng.
- Nếu có chuỗi params nhưng một số tính năng `yes/no` bị lược bỏ, thì các tính năng bị lược bỏ được giả định có giá trị `no`. Vì vậy, nếu bạn chỉ định params, hãy đảm bảo bạn thiết lập rõ ràng tất cả các tính năng cần thiết thành yes.
- Nếu không có `left/top` trong params, thì trình duyệt cố gắng mở cửa sổ mới gần cửa sổ đã mở cuối cùng.
- Nếu không có `width/height`, thì cửa sổ mới sẽ có cùng kích thước với cửa sổ đã mở cuối cùng.

## [Truy cập popup từ cửa sổ](#accessing-popup-from-window)

Lệnh `open` trả về một tham chiếu đến cửa sổ mới. Nó có thể được sử dụng để thao tác các thuộc tính của nó, thay đổi vị trí và thậm chí nhiều hơn nữa.

Trong ví dụ này, chúng ta tạo nội dung popup từ JavaScript:

```
let newWin = window.open("about:blank", "hello", "width=200,height=200");

newWin.document.write("Hello, world!");
```

Và ở đây chúng ta sửa đổi nội dung sau khi tải:

```
let newWindow = open('/', 'example', 'width=300,height=300')
newWindow.focus();

alert(newWindow.location.href); // (*) about:blank, việc tải chưa bắt đầu

newWindow.onload = function() {
  let html = `<div style="font-size:30px">Chào mừng!</div>`;
  newWindow.document.body.insertAdjacentHTML('afterbegin', html);
};
```

Xin lưu ý: ngay sau `window.open`, cửa sổ mới chưa được tải. Điều đó được minh họa bởi `alert` ở dòng `(*)`. Vì vậy, chúng ta đợi `onload` để sửa đổi nó. Chúng ta cũng có thể sử dụng trình xử lý `DOMContentLoaded` cho `newWin.document`.

Chính sách Same Origin

Các cửa sổ có thể tự do truy cập nội dung của nhau chỉ nếu chúng đến từ cùng một origin (cùng giao thức://miền: cổng).

Nếu không, ví dụ nếu cửa sổ chính đến từ `site.com`, và popup đến từ `gmail.com`, thì điều đó là không thể vì lý do an toàn người dùng. Để biết chi tiết, xem chương [Giao tiếp giữa các cửa sổ](/cross-window-communication).

## [Truy cập cửa sổ từ popup](#accessing-window-from-popup)

Popup có thể truy cập cửa sổ "opener" bằng cách sử dụng tham chiếu `window.opener`. Nó là `null` đối với tất cả các cửa sổ ngoại trừ popup.

Nếu bạn chạy mã dưới đây, nó sẽ thay đổi nội dung cửa sổ opener (hiện tại) thành "Test":

```
let newWin = window.open("about:blank", "hello", "width=200,height=200");

newWin.document.write(
  "<script>window.opener.document.body.innerHTML = 'Test'<\/script>"
);
```

Vì vậy, kết nối giữa các cửa sổ là hai chiều: cửa sổ chính và popup có tham chiếu đến nhau.

## [Đóng popup](#closing-a-popup)

Để đóng cửa sổ: `win.close()`.

Để kiểm tra xem cửa sổ đã đóng chưa: `win.closed`.

Về mặt kỹ thuật, phương thức `close()` có sẵn cho bất kỳ `window` nào, nhưng `window.close()` bị bỏ qua bởi hầu hết các trình duyệt nếu `window` không được tạo bằng `window.open()`. Vì vậy, nó sẽ chỉ hoạt động trên popup.

Thuộc tính `closed` là `true` nếu cửa sổ đã đóng. Điều đó hữu ích để kiểm tra xem popup (hoặc cửa sổ chính) có còn mở hay không. Người dùng có thể đóng nó bất cứ lúc nào, và mã của chúng ta nên tính đến khả năng đó.

Mã này tải và sau đó đóng cửa sổ:

```
let newWindow = open('/', 'example', 'width=300,height=300');

newWindow.onload = function() {
  newWindow.close();
  alert(newWindow.closed); // true
};
```

## [Di chuyển và thay đổi kích thước](#moving-and-resizing)

Có các phương thức để di chuyển/thay đổi kích thước cửa sổ:

`win.moveBy(x,y)`
:   Di chuyển cửa sổ so với vị trí hiện tại `x` pixel sang phải và `y` pixel xuống dưới. Các giá trị âm được cho phép (để di chuyển trái/lên).

`win.moveTo(x,y)`
:   Di chuyển cửa sổ đến tọa độ `(x,y)` trên màn hình.

`win.resizeBy(width,height)`
:   Thay đổi kích thước cửa sổ theo `width/height` đã cho so với kích thước hiện tại. Các giá trị âm được cho phép.

`win.resizeTo(width,height)`
:   Thay đổi kích thước cửa sổ đến kích thước đã cho.

Cũng có sự kiện `window.onresize`.

Chỉ dành cho popup

Để ngăn chặn lạm dụng, trình duyệt thường chặn các phương thức này. Chúng chỉ hoạt động đáng tin cậy trên các popup mà chúng ta đã mở, không có thêm tab.

Không có thu nhỏ/tối đa hóa

JavaScript không có cách nào để thu nhỏ hoặc tối đa hóa cửa sổ. Những chức năng cấp hệ điều hành này bị ẩn khỏi nhà phát triển Frontend.

Các phương thức di chuyển/thay đổi kích thước không hoạt động đối với cửa sổ đã được tối đa hóa/thu nhỏ.

## [Cuộn cửa sổ](#scrolling-a-window)
Chúng ta đã nói về cuộn cửa sổ trong chương [Kích thước cửa sổ và cuộn](/size-and-scroll-window).

`win.scrollBy(x,y)`
:   Cuộn cửa sổ `x` pixel sang phải và `y` xuống dưới so với cuộn hiện tại. Các giá trị âm được cho phép.

`win.scrollTo(x,y)`
:   Cuộn cửa sổ đến tọa độ đã cho `(x,y)`.

`elem.scrollIntoView(top = true)`
:   Cuộn cửa sổ để làm cho `elem` xuất hiện ở đầu (mặc định) hoặc ở cuối đối với `elem.scrollIntoView(false)`.

Cũng có sự kiện `window.onscroll`.

## [Focus/blur trên cửa sổ](#focus-blur-on-a-window)

Về lý thuyết, có các phương thức `window.focus()` và `window.blur()` để focus/unfocus trên một cửa sổ. Và cũng có các sự kiện `focus/blur` cho phép bắt khoảnh khắc khi người truy cập focus vào cửa sổ và chuyển sang nơi khác.

Tuy nhiên, trong thực tế chúng bị hạn chế nghiêm trọng, vì trong quá khứ các trang độc hại đã lạm dụng chúng.

Ví dụ, hãy xem mã này:

```
window.onblur = () => window.focus();
```

Khi người dùng cố gắng chuyển ra khỏi cửa sổ (`window.onblur`), nó đưa cửa sổ trở lại focus. Ý định là "khóa" người dùng trong `window`.

Vì vậy, các trình duyệt đã phải giới thiệu nhiều hạn chế để cấm mã như vậy và bảo vệ người dùng khỏi quảng cáo và các trang độc hại. Chúng phụ thuộc vào trình duyệt.

Ví dụ, trình duyệt di động thường bỏ qua `window.focus()` hoàn toàn. Ngoài ra, focus không hoạt động khi popup mở trong tab riêng biệt thay vì cửa sổ mới.

Vẫn còn, có một số trường hợp sử dụng khi các lệnh gọi như vậy hoạt động và có thể hữu ích.

Ví dụ:

- Khi chúng ta mở một popup, có thể là một ý tưởng tốt để chạy `newWindow.focus()` trên nó. Chỉ phòng khi, đối với một số tổ hợp OS/trình duyệt, nó đảm bảo rằng người dùng hiện đang ở cửa sổ mới.
- Nếu chúng ta muốn theo dõi khi nào người truy cập thực sự sử dụng ứng dụng web của chúng ta, chúng ta có thể theo dõi `window.onfocus/onblur`. Điều đó cho phép chúng ta tạm dừng/tiếp tục các hoạt động trong trang, hoạt hình v.v. Nhưng xin lưu ý rằng sự kiện `blur` có nghĩa là người truy cập đã chuyển ra khỏi cửa sổ, nhưng họ vẫn có thể quan sát nó. Cửa sổ ở chế độ nền, nhưng vẫn có thể nhìn thấy được.

## [Tóm tắt](#summary)

Cửa sổ popup được sử dụng hiếm khi, vì có các lựa chọn thay thế: tải và hiển thị thông tin trong trang, hoặc trong iframe.

Nếu chúng ta định mở một popup, thực hành tốt là thông báo cho người dùng về điều đó. Biểu tượng "mở cửa sổ" gần một liên kết hoặc nút sẽ cho phép người truy cập sống sót sau khi chuyển focus và giữ cả hai cửa sổ trong tâm trí.

- Một popup có thể được mở bằng lệnh gọi `open(url, name, params)`. Nó trả về tham chiếu đến cửa sổ vừa mở.
- Các trình duyệt chặn các lệnh gọi `open` từ mã bên ngoài hành động của người dùng. Thông thường một thông báo xuất hiện, vì vậy người dùng có thể cho phép chúng.
- Trình duyệt mở tab mới theo mặc định, nhưng nếu kích thước được cung cấp, thì đó sẽ là cửa sổ popup.
- Popup có thể truy cập cửa sổ opener bằng cách sử dụng thuộc tính `window.opener`.
- Cửa sổ chính và popup có thể tự do đọc và sửa đổi lẫn nhau nếu chúng có cùng origin. Nếu không, chúng có thể thay đổi vị trí của nhau và [trao đổi tin nhắn](/cross-window-communication).

Để đóng popup: sử dụng lệnh gọi `close()`. Người dùng cũng có thể đóng chúng (giống như bất kỳ cửa sổ nào khác). `window.closed` sẽ là `true` sau đó.

- Các phương thức `focus()` và `blur()` cho phép focus/unfocus một cửa sổ. Nhưng chúng không hoạt động luôn luôn.
- Các sự kiện `focus` và `blur` cho phép theo dõi chuyển vào và ra khỏi cửa sổ. Nhưng xin lưu ý rằng một cửa sổ vẫn có thể được nhìn thấy ngay cả ở trạng thái nền, sau khi `blur`.
