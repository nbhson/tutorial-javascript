# Sự kiện chuột

> Source: [https://javascript.info/mouse-events-basics](https://javascript.info/mouse-events-basics)

<!-- fetched: 2026-09-14 -->

Trong chương này, chúng ta sẽ tìm hiểu chi tiết hơn về các sự kiện chuột và thuộc tính của chúng.

Lưu ý: các sự kiện này không chỉ đến từ "thiết bị chuột", mà còn từ các thiết bị khác như điện thoại và máy tính bảng, nơi chúng được mô phỏng để tương thích.

## [Các loại sự kiện chuột](#mouse-event-types)

Chúng ta đã thấy một số sự kiện trong danh sách sau:

`mousedown/mouseup`
:   Nút chuột được nhấn/thả trên một phần tử.

`mouseover/mouseout`
:   Con trỏ chuột di chuyển vào/ra khỏi một phần tử.

`mousemove`
:   Mọi chuyển động chuột trên phần tử đều kích hoạt sự kiện đó.

`click`
:   Kích hoạt sau `mousedown` và sau đó là `mouseup` trên cùng một phần tử nếu nút trái chuột được sử dụng.

`dblclick`
:   Kích hoạt sau hai lần nhấp vào cùng một phần tử trong một khoảng thời gian ngắn. Hiếm khi được sử dụng ngày nay.

`contextmenu`
:   Kích hoạt khi nhấn nút phải chuột. Có những cách khác để mở menu ngữ cảnh, ví dụ sử dụng phím đặc biệt trên bàn phím, cũng kích hoạt trong trường hợp đó, nên đây không phải là sự kiện chuột chính xác.

…Có một số sự kiện khác nữa, chúng ta sẽ đề cập đến sau.

## [Thứ tự sự kiện](#events-order)

Như bạn có thể thấy từ danh sách trên, một hành động của người dùng có thể kích hoạt nhiều sự kiện.

Ví dụ, một cú click nút trái đầu tiên kích hoạt `mousedown`, khi nút được nhấn, sau đó là `mouseup` và `click` khi nó được thả.

Trong các trường hợp khi một hành động đơn khởi tạo nhiều sự kiện, thứ tự của chúng được cố định. Tức là, các handler được gọi theo thứ tự `mousedown` → `mouseup` → `click`.

Nhấp vào nút bên dưới và bạn sẽ thấy các sự kiện. Hãy thử click đúp.

Tại teststand bên dưới, tất cả các sự kiện mouse được ghi lại, và nếu có độ trễ hơn 1 giây giữa chúng, chúng được phân cách bằng đường ngang.

Ngoài ra, chúng ta có thể thấy thuộc tính `button` cho phép chúng ta phát hiện nút chuột; nó được giải thích bên dưới.

## [Nút chuột](#mouse-button)

Các sự kiện liên quan đến click luôn có thuộc tính `button`, cho phép lấy chính xác nút chuột.

Chúng ta thường không sử dụng nó cho các sự kiện `click` và `contextmenu`, vì sự kiện前者 chỉ xảy ra trên click trái, và sự kiện后者 – chỉ trên click phải.

Mặt khác, các handler `mousedown` và `mouseup` có thể cần `event.button`, vì các sự kiện này kích hoạt trên bất kỳ nút nào, nên `button` cho phép phân biệt giữa "right-mousedown" và "left-mousedown".

Các giá trị có thể có của `event.button` là:

| Trạng thái nút | `event.button` |
| --- | --- |
| Nút trái (primary) | 0 |
| Nút giữa (auxiliary) | 1 |
| Nút phải (secondary) | 2 |
| Nút X1 (back) | 3 |
| Nút X2 (forward) | 4 |

Hầu hết các thiết bị chuột chỉ có nút trái và nút phải, vì vậy các giá trị có thể là `0` hoặc `2`. Các thiết bị cảm ứng cũng tạo ra các sự kiện tương tự khi người dùng chạm vào chúng.

Ngoài ra còn có thuộc tính `event.buttons` có tất cả các nút đang được nhấn dưới dạng số nguyên, mỗi nút là một bit. Trong thực tế, thuộc tính này rất hiếm khi được sử dụng, bạn có thể tìm chi tiết tại [MDN](https://developer.mozilla.org/en-US/docs/Web/api/MouseEvent/buttons) nếu bạn cần.

`event.which` lỗi thời

Mã cũ có thể sử dụng thuộc tính `event.which` – một cách cũ không chuẩn để lấy nút, với các giá trị có thể:

- `event.which == 1` – nút trái,
- `event.which == 2` – nút giữa,
- `event.which == 3` – nút phải.

Hiện tại, `event.which` đã bị khai tử, chúng ta không nên sử dụng nó.

## [Các phím điều khiển: shift, alt, ctrl và meta](#modifiers-shift-alt-ctrl-and-meta)

Tất cả các sự kiện chuột bao gồm thông tin về các phím điều khiển đang được nhấn.

Các thuộc tính sự kiện:

- `shiftKey`: `Shift`
- `altKey`: `Alt` (hoặc `Opt` đối với Mac)
- `ctrlKey`: `Ctrl`
- `metaKey`: `Cmd` đối với Mac

Chúng là `true` nếu phím tương ứng được nhấn trong suốt sự kiện.

Ví dụ, nút bên dưới chỉ hoạt động trên `Alt+Shift`+click:

```
<button id="button">Alt+Shift+Click on me!</button>

<script>
  button.onclick = function(event) {
    if (event.altKey && event.shiftKey) {
      alert('Hooray!');
    }
  };
</script>
```

Chú ý: trên Mac thường là `Cmd` thay vì `Ctrl`

Trên Windows và Linux có các phím điều khiển `Alt`, `Shift` và `Ctrl`. Trên Mac có thêm một phím nữa: `Cmd`, tương ứng với thuộc tính `metaKey`.

Trong hầu hết các ứng dụng, khi Windows/Linux sử dụng `Ctrl`, trên Mac sử dụng `Cmd`.

Tức là: nơi người dùng Windows nhấn `Ctrl+Enter` hoặc `Ctrl+A`, người dùng Mac sẽ nhấn `Cmd+Enter` hoặc `Cmd+A`, và cứ thế.

Vì vậy, nếu chúng ta muốn hỗ trợ các tổ hợp như `Ctrl`+click, thì đối với Mac, việc sử dụng `Cmd`+click có ý nghĩa. Điều đó thuận tiện hơn cho người dùng Mac.

Ngay cả khi chúng ta muốn bắt buộc người dùng Mac phải dùng `Ctrl`+click – điều đó khá khó. Vấn đề là: click trái với `Ctrl` được hiểu là *click phải* trên MacOS, và nó tạo ra sự kiện `contextmenu`, không phải `click` như Windows/Linux.

Vì vậy, nếu chúng ta muốn người dùng của mọi hệ điều hành cảm thấy thoải mái, thì ngoài `ctrlKey` chúng ta nên kiểm tra `metaKey`.

Đối với mã JS, điều đó có nghĩa là chúng ta nên kiểm tra `if (event.ctrlKey || event.metaKey)`.

Cũng có các thiết bị di động

Các tổ hợp phím tốt như một phần bổ sung cho quy trình làm việc. Vì vậy, nếu người truy cập sử dụng bàn phím – chúng hoạt động.

Nhưng nếu thiết bị của họ không có nó – thì nên có cách để hoạt động mà không có các phím điều khiển.

## [Tọa độ: clientX/Y, pageX/Y](#coordinates-clientx-y-pagex-y)

Tất cả các sự kiện chuột cung cấp tọa độ theo hai kiểu:

1. Tương đối cửa sổ: `clientX` và `clientY`.
2. Tương đối tài liệu: `pageX` và `pageY`.

Chúng ta đã đề cập đến sự khác biệt giữa chúng trong chương [Coordinates](/coordinates).

Nói ngắn gọn, tọa độ tương đối tài liệu `pageX/Y` được tính từ góc trên bên trái của tài liệu và không thay đổi khi trang được cuộn, trong khi `clientX/Y` được tính từ góc trên bên trái của cửa sổ hiện tại. Khi trang được cuộn, chúng thay đổi.

Ví dụ, nếu chúng ta có cửa sổ kích thước 500x500, và chuột ở góc trên bên trái, thì `clientX` và `clientY` là `0`, bất kể trang được cuộn như thế nào.

Và nếu chuột ở giữa, thì `clientX` và `clientY` là `250`, bất kể vị trí nào trong tài liệu. Chúng tương tự như `position:fixed` về khía cạnh này.

Di chuyển chuột qua ô nhập liệu để xem `clientX/clientY` (ví dụ nằm trong `iframe`, nên tọa độ tương đối với `iframe` đó):

```
<input onmousemove="this.value=event.clientX+':'+event.clientY" value="Mouse over me">
```

## [Ngăn chặn chọn văn bản trên mousedown](#preventing-selection-on-mousedown)

Click đúp có một tác dụng phụ có thể gây khó chịu trong một số giao diện: nó chọn văn bản.

Ví dụ, click đúp vào văn bản bên dưới sẽ chọn nó ngoài handler của chúng ta:

```
<span ondblclick="alert('dblclick')">Double-click me</span>
```

Nếu người dùng nhấn nút trái chuột và, mà không nhả ra, di chuyển chuột, điều đó cũng tạo ra lựa chọn, thường là không mong muốn.

Có nhiều cách để ngăn chặn việc chọn, bạn có thể đọc trong chương [Selection and Range](/selection-range).

Trong trường hợp cụ thể này, cách hợp lý nhất là ngăn hành động của trình duyệt trên `mousedown`. Nó ngăn chặn cả hai kiểu chọn này:

```
Before...
<b ondblclick="alert('Click!')" onmousedown="return false">
  Double-click me
</b>
...After
```

Bây giờ phần tử in đậm không được chọn khi click đúp, và nhấn nút trái trên nó sẽ không bắt đầu việc chọn.

Xin lưu ý: văn bản bên trong vẫn có thể được chọn. Tuy nhiên, việc chọn nên bắt đầu không phải trên chính văn bản, mà trước hoặc sau nó. Thông thường điều đó ổn đối với người dùng.

Ngăn chặn sao chép

Nếu chúng ta muốn vô hiệu hóa việc chọn để bảo vệ nội dung trang của chúng ta khỏi sao chép-dán, thì chúng ta có thể sử dụng một sự kiện khác: `oncopy`.

```
<div oncopy="alert('Copying forbidden!');return false">
  Dear user,
  The copying is forbidden for you.
  If you know JS or HTML, then you can get everything from the page source though.
</div>
```

Nếu bạn thử sao chép một đoạn văn bản trong `<div>`, điều đó sẽ không hoạt động, vì hành động mặc định `oncopy` bị ngăn chặn.

Chắc chắn người dùng có quyền truy cập vào nguồn HTML của trang, và có thể lấy nội dung từ đó, nhưng không phải ai cũng biết cách làm điều đó.

## [Tổng kết](#summary)

Các sự kiện chuột có các thuộc tính sau:

- Nút: `button`.
- Các phím điều khiển (`true` nếu được nhấn): `altKey`, `ctrlKey`, `shiftKey` và `metaKey` (Mac).

  - Nếu bạn muốn xử lý `Ctrl`, thì đừng quên người dùng Mac, họ thường sử dụng `Cmd`, vì vậy tốt hơn là kiểm tra `if (e.metaKey || e.ctrlKey)`.
- Tọa độ tương đối cửa sổ: `clientX/clientY`.
- Tọa độ tương đối tài liệu: `pageX/pageY`.

Hành động mặc định của trình duyệt đối với `mousedown` là chọn văn bản, nếu điều đó không tốt cho giao diện, thì nên ngăn chặn.

Trong chương tiếp theo, chúng ta sẽ xem chi tiết hơn về các sự kiện theo sau chuyển động của con trỏ và cách theo dõi sự thay đổi của phần tử dưới nó.

---

---

## Bài tập

## [Bài tập](#tasks)

### [Danh sách có thể chọn](#selectable-list)

mức độ khó: 5

Tạo một danh sách mà các phần tử có thể được chọn, giống như trong các trình quản lý tệp.

- Một click lên một phần tử danh sách sẽ chọn duy nhất phần tử đó (thêm class `.selected`), bỏ chọn tất cả các phần tử khác.
- Nếu một click được thực hiện với `Ctrl` (`Cmd` đối với Mac), thì việc chọn sẽ được chuyển đổi trên phần tử, nhưng các phần tử khác không bị thay đổi.

Bản demo:

P.S. Đối với bài tập này, chúng ta có thể giả định rằng các mục danh sách chỉ là văn bản. Không có thẻ lồng nhau.

P.P.S. Ngăn chặn việc chọn văn bản mặc định của trình duyệt trên các lần click.

[Mở sandbox cho bài tập.](https://plnkr.co/edit/ui9gDeFAivtUxeQy?p=preview)

lời giải

[Mở lời giải trong sandbox.](https://plnkr.co/edit/uZH8Kfizo0xwn7Cb?p=preview)
