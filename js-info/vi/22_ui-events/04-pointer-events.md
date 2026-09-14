# Sự kiện con trỏ (Pointer events)

> Source: [https://javascript.info/pointer-events](https://javascript.info/pointer-events)

<!-- fetched: 2026-09-14 -->

Pointer events là một cách hiện đại để xử lý input từ nhiều loại pointing devices, như mouse, pen/stylus, touchscreen, và cứ thế.

## [Lịch sử tóm tắt](#the-brief-history)

Hãy xem xét tổng quan nhỏ, để bạn hiểu bức tranh tổng thể và vị trí của Pointer Events среди các loại sự kiện khác.

- Từ lâu, trong quá khứ, chỉ có mouse events.

  Sau đó, các thiết bị cảm ứng trở nên phổ biến, đặc biệt là điện thoại và máy tính bảng. Để các scripts hiện có hoạt động, chúng tạo ra (và vẫn tạo ra) các sự kiện mouse. Ví dụ, chạm vào touchscreen tạo ra `mousedown`. Vì vậy, các thiết bị cảm ứng hoạt động tốt với các trang web.

  Nhưng các thiết bị cảm ứng có nhiều khả năng hơn mouse. Ví dụ, có thể chạm vào nhiều điểm cùng một lúc ("multi-touch"). Tuy nhiên, các mouse events không có các thuộc tính cần thiết để xử lý các multi-touches như vậy.
- Vì vậy, các touch events được giới thiệu, chẳng hạn như `touchstart`, `touchend`, `touchmove`, có các thuộc tính đặc thù cho touch (chúng ta không đề cập chi tiết ở đây, vì pointer events thậm chí còn tốt hơn).

  Vẫn chưa đủ, vì có nhiều thiết bị khác, chẳng hạn như pens, có các tính năng riêng. Ngoài ra, viết code lắng nghe cả touch và mouse events là cồng kềnh.
- Để giải quyết các vấn đề này, tiêu chuẩn mới Pointer Events được giới thiệu. Nó cung cấp một bộ sự kiện duy nhất cho tất cả các loại pointing devices.

Tính đến nay, [Pointer Events Level 2](https://www.w3.org/TR/pointerevents2/) specification được hỗ trợ trong tất cả các browser chính, trong khi [Pointer Events Level 3](https://w3c.github.io/pointerevents/) mới hơn đang được phát triển và chủ yếu tương thích với Pointer Events level 2.

Trừ khi bạn phát triển cho các browser cũ, chẳng hạn như Internet Explorer 10, hoặc Safari 12 trở xuống, không có lý do gì để继续使用 mouse hoặc touch events nữa – chúng ta có thể chuyển sang pointer events.

Sau đó mã của bạn sẽ hoạt động tốt với cả touch và mouse devices.

Tuy nhiên, có một số điểm đặc biệt quan trọng mà một người nên biết để sử dụng Pointer Events đúng cách và tránh bất ngờ. Chúng ta sẽ ghi chú chúng trong bài viết này.

## [Các loại pointer events](#pointer-event-types)

Pointer events được đặt tên tương tự như mouse events:

| Pointer event | Similar mouse event |
| --- | --- |
| `pointerdown` | `mousedown` |
| `pointerup` | `mouseup` |
| `pointermove` | `mousemove` |
| `pointerover` | `mouseover` |
| `pointerout` | `mouseout` |
| `pointerenter` | `mouseenter` |
| `pointerleave` | `mouseleave` |
| `pointercancel` | - |
| `gotpointercapture` | - |
| `lostpointercapture` | - |

Như chúng ta có thể thấy, đối với mọi `mouse<event>`, có một `pointer<event>` đóng vai trò tương tự. Ngoài ra còn có 3 pointer events bổ sung không có counterpart `mouse...` tương ứng, chúng ta sẽ giải thích chúng sớm.

Thay thế `mouse<event>` bằng `pointer<event>` trong mã của chúng ta

Chúng ta có thể thay thế các sự kiện `mouse<event>` bằng `pointer<event>` trong mã của chúng ta và mong đợi mọi thứ tiếp tục hoạt động tốt với mouse.

Hỗ trợ cho các thiết bị cảm ứng cũng sẽ "tự động" cải thiện. Tuy nhiên, chúng ta có thể cần thêm `touch-action: none` ở một số chỗ trong CSS. Chúng ta sẽ đề cập đến nó bên dưới trong phần về `pointercancel`.

## [Các thuộc tính pointer event](#pointer-event-properties)

Pointer events có cùng các thuộc tính như mouse events, chẳng hạn như `clientX/Y`, `target`, v.v., cộng thêm một số khác:

- `pointerId` – identifier duy nhất của pointer gây ra sự kiện.

  Browser-generated. Cho phép chúng ta xử lý nhiều pointers, chẳng hạn như touchscreen với stylus và multi-touch (các ví dụ sẽ theo sau).
- `pointerType` – loại pointing device. Phải là một string, một trong số: "mouse", "pen" hoặc "touch".

  Chúng ta có thể sử dụng thuộc tính này để phản ứng khác nhau trên các loại pointer khác nhau.
- `isPrimary` – là `true` cho primary pointer (ngón tay đầu tiên trong multi-touch).

Một số thiết bị pointer đo diện tích tiếp xúc và áp suất, ví dụ cho một ngón tay на touchscreen, có các thuộc tính bổ sung cho điều đó:

- `width` – chiều rộng của khu vực nơi pointer (ví dụ ngón tay) chạm vào device. Nơi không được hỗ trợ, chẳng hạn như mouse, nó luôn là `1`.
- `height` – chiều cao của khu vực nơi pointer chạm vào device. Nơi không được hỗ trợ, nó luôn là `1`.
- `pressure` – áp suất của đầu pointer, trong khoảng từ 0 đến 1. Đối với các thiết bị không hỗ trợ pressure phải là `0.5` (pressed) hoặc `0`.
- `tangentialPressure` – áp suất tangential được normalize.
- `tiltX`, `tiltY`, `twist` – các thuộc tính đặc thù cho pen mô tả cách pen được định vị so với bề mặt.

Các thuộc tính này không được hỗ trợ bởi hầu hết các thiết bị, vì vậy chúng hiếm khi được sử dụng. Bạn có thể tìm chi tiết về chúng trong [specification](https://w3c.github.io/pointerevents/#pointerevent-interface) nếu cần.

## [Multi-touch](#multi-touch)

Một trong những thứ mà mouse events hoàn toàn không hỗ trợ là multi-touch: người dùng có thể chạm vào nhiều nơi cùng một lúc trên điện thoại hoặc máy tính bảng của họ, hoặc thực hiện các cử chỉ đặc biệt.

Pointer Events cho phép xử lý multi-touch với sự giúp đỡ của `pointerId` và `isPrimary` properties.

Đây là những gì xảy ra khi người dùng chạm vào touchscreen tại một điểm, sau đó đặt một ngón tay khác ở đâu đó trên đó:

1. Tại lần chạm ngón tay đầu tiên:
   - `pointerdown` với `isPrimary=true` và một `pointerId` nào đó.
2. Đối với ngón tay thứ hai và các ngón tay khác (giả sử ngón tay đầu tiên vẫn đang chạm):
   - `pointerdown` với `isPrimary=false` và một `pointerId` khác nhau cho mỗi ngón tay.

Xin lưu ý: `pointerId` được gán không phải cho toàn bộ device, mà cho mỗi ngón tay chạm. Nếu chúng ta sử dụng 5 ngón tay để đồng thời chạm vào màn hình, chúng ta có 5 sự kiện `pointerdown`, mỗi sự kiện có tọa độ riêng và một `pointerId` khác nhau.

Các sự kiện liên quan đến ngón tay đầu tiên luôn có `isPrimary=true`.

Chúng ta có thể theo dõi nhiều ngón tay chạm bằng cách sử dụng `pointerId` của chúng. Khi người dùng di chuyển và sau đó bỏ một ngón tay, chúng ta nhận được các sự kiện `pointermove` và `pointerup` với cùng `pointerId` như chúng ta có в `pointerdown`.

Đây là demo ghi lại các sự kiện `pointerdown` và `pointerup`:

Xin lưu ý: bạn phải đang sử dụng một thiết bị touchscreen, chẳng hạn như điện thoại hoặc máy tính bảng, để thực sự thấy sự khác biệt в `pointerId/isPrimary`. Đối với các thiết bị single-touch, chẳng hạn như mouse, sẽ luôn có cùng `pointerId` với `isPrimary=true`, для tất cả các pointer events.

## [Sự kiện: pointercancel](#event-pointercancel)

Sự kiện `pointercancel` kích hoạt khi có một tương tác pointer đang diễn ra, và sau đó có một số thứ xảy ra khiến nó bị hủy bỏ, vì vậy không còn tạo ra các sự kiện pointer nữa.

Các nguyên nhân đó là:

- Thiết bị pointer hardware bị vô hiệu hóa về mặt vật lý.
- Hướng device thay đổi (tablet rotated).
- Browser quyết định xử lý tương tác theo cách của riêng nó, coi nó là một mouse gesture hoặc zoom-and-pan action hoặc thứ gì đó khác.

Chúng ta sẽ minh họa `pointercancel` на một ví dụ thực tế để xem nó ảnh hưởng đến chúng ta như thế nào.

Giả sử chúng ta đang triển khai drag'n'drop cho một quả bóng, giống như ở đầu bài viết [Drag'n'Drop with mouse events](/mouse-drag-and-drop).

Đây là dòng các hành động của người dùng và các sự kiện tương ứng:

1. Người dùng nhấn vào một image, để bắt đầu kéo
   - sự kiện `pointerdown` kích hoạt
2. Sau đó họ bắt đầu di chuyển pointer (do đó kéo image)
   - `pointermove` kích hoạt, có thể nhiều lần
3. Và sau đó bất ngờ xảy ra! Browser có hỗ trợ drag'n'drop native cho images, kích hoạt và nắm lấy quy trình drag'n'drop, do đó tạo ra sự kiện `pointercancel`.
   - Browser bây giờ xử lý drag'n'drop của image theo cách của riêng nó. Người dùng thậm chí có thể kéo image bóng ra khỏi browser, vào chương trình Mail hoặc File Manager của họ.
   - Không còn các sự kiện `pointermove` nào для chúng ta nữa.

Vì vậy, vấn đề là browser "hijack" tương tác: `pointercancel` kích hoạt ở đầu quy trình "drag-and-drop", và không còn các sự kiện `pointermove` nào được tạo ra.

Đây là demo drag'n'drop với logging của các pointer events (chỉ `up/down`, `move` và `cancel`) trong `textarea`:

Chúng ta muốn triển khai drag'n'drop theo cách của riêng mình, vì vậy hãy nói với browser đừng nắm lấy nó.

**Ngăn chặn hành động mặc định của browser để tránh `pointercancel`.**

Chúng ta cần làm hai điều:

1. Ngăn chặn native drag'n'drop xảy ra:
   - Chúng ta có thể làm điều này bằng cách đặt `ball.ondragstart = () => false`, giống như được mô tả в bài viết [Drag'n'Drop with mouse events](/mouse-drag-and-drop).
   - Điều đó hoạt động tốt cho mouse events.
2. Đối với các thiết bị cảm ứng, có các hành động browser liên quan đến touch khác (ngoài drag'n'drop). Để tránh các vấn đề với chúng:
   - Ngăn chặn chúng bằng cách đặt `#ball { touch-action: none }` в CSS.
   - Sau đó mã của chúng ta sẽ bắt đầu hoạt động trên các thiết bị cảm ứng.

Sau khi chúng ta làm điều đó, các sự kiện sẽ hoạt động như dự định, browser sẽ không hijack quy trình và không phát ra `pointercancel`.

Demo này thêm các dòng sau:

Như bạn có thể thấy, không còn `pointercancel` nào nữa.

Bây giờ chúng ta có thể thêm mã để thực sự di chuyển quả bóng, và drag'n'drop của chúng ta sẽ hoạt động для mouse devices và touch devices.

## [Pointer capturing](#pointer-capturing)

Pointer capturing là một tính năng đặc biệt của pointer events.

Ý tưởng rất đơn giản, nhưng có vẻ khá kỳ lạ lúc đầu, vì không có gì như vậy tồn tại đối với bất kỳ loại sự kiện nào khác.

Phương pháp chính là:

- `elem.setPointerCapture(pointerId)` – binds các sự kiện với `pointerId` đã cho đến `elem`. Sau khi gọi, tất cả các sự kiện pointer với cùng `pointerId` sẽ có `elem` làm target (như thể xảy ra на `elem`), bất kể chúng thực sự xảy ra ở đâu trong document.

Nói cách khác, `elem.setPointerCapture(pointerId)` retargets tất cả các sự kiện tiếp theo với `pointerId` đã cho đến `elem`.

Binding được loại bỏ:

- tự động khi các sự kiện `pointerup` hoặc `pointercancel` xảy ra,
- tự động khi `elem` bị xóa khỏi document,
- khi `elem.releasePointerCapture(pointerId)` được gọi.

Bây giờ nó hữu ích cho cái gì? Đã đến lúc xem một ví dụ thực tế.

**Pointer capturing có thể được sử dụng để đơn giản hóa các tương tác loại drag'n'drop.**

Hãy nhớ lại cách một slider tùy chỉnh được triển khai, được mô tả в [Drag'n'Drop with mouse events](/mouse-drag-and-drop).

Chúng ta có thể tạo một phần tử `slider` để biểu diễn strip và "runner" (`thumb`) bên trong nó:

```
<div class="slider">
  <div class="thumb"></div>
</div>
```

Với styles, nó trông như vậy:

Và đây là logic hoạt động, như đã được mô tả, sau khi thay thế mouse events bằng các pointer events tương tự:

1. Người dùng nhấn vào slider `thumb` – `pointerdown` kích hoạt.
2. Sau đó họ di chuyển pointer – `pointermove` kích hoạt, và mã của chúng ta di chuyển phần tử `thumb` dọc theo.
   - …Khi pointer di chuyển, nó có thể rời khỏi phần tử slider `thumb`, đi над hoặc dưới nó. `thumb` nên di chuyển strictly horizontal, vẫn giữ căn chỉnh với pointer.

Trong giải pháp dựa на mouse events, để theo dõi tất cả các chuyển động của pointer, kể cả khi nó đi над/dưới `thumb`, chúng ta đã phải gán handler sự kiện `mousemove` trên toàn bộ `document`.

Đó không phải là giải pháp sạch sẽ nhất. Một trong những vấn đề là khi người dùng di chuyển pointer xung quanh document, nó có thể kích hoạt các handler sự kiện (chẳng hạn như `mouseover`) trên một số phần tử khác,.invoke các functionality UI hoàn toàn không liên quan, và chúng ta không muốn điều đó.

Đây là nơi `setPointerCapture` phát huy tác dụng.

- Chúng ta có thể gọi `thumb.setPointerCapture(event.pointerId)` в handler `pointerdown`,
- Sau đó các sự kiện pointer tiếp theo cho đến `pointerup/cancel` sẽ được retarget đến `thumb`.
- Khi `pointerup` xảy ra (kéo hoàn tất), binding được loại bỏ tự động, chúng ta không cần phải lo lắng về nó.

Vì vậy, ngay cả khi người dùng di chuyển pointer xung quanh toàn bộ document, các handler sự kiện sẽ được gọi на `thumb`. Tuy nhiên, các thuộc tính tọa độ của các đối tượng sự kiện, chẳng hạn như `clientX/clientY`, vẫn sẽ chính xác – capturing chỉ ảnh hưởng đến `target/currentTarget`.

Đây là mã thiết yếu:

```
thumb.onpointerdown = function(event) {
  // retarget all pointer events (until pointerup) to thumb
  thumb.setPointerCapture(event.pointerId);

  // start tracking pointer moves
  thumb.onpointermove = function(event) {
    // moving the slider: listen on the thumb, as all pointer events are retargeted to it
    let newLeft = event.clientX - slider.getBoundingClientRect().left;
    thumb.style.left = newLeft + 'px';
  };

  // on pointer up finish tracking pointer moves
  thumb.onpointerup = function(event) {
    thumb.onpointermove = null;
    thumb.onpointerup = null;
    // ...also process the "drag end" if needed
  };
};

// note: no need to call thumb.releasePointerCapture,
// it happens on pointerup automatically
```

Demo đầy đủ:

Trong demo, cũng có một phần tử bổ sung với handler `onmouseover` hiển thị ngày hiện tại.

Xin lưu ý: trong khi bạn đang kéo thumb, bạn có thể hover над phần tử này, và handler của nó *không* kích hoạt.

Vì vậy, việc kéo bây giờ không có side effects, dankи `setPointerCapture`.

Ở cuối, pointer capturing mang lại cho chúng ta hai lợi ích:

1. Mã trở nên sạch hơn vì chúng ta không cần phải thêm/xóa các handler trên toàn bộ `document` nữa. Binding được giải phóng tự động.
2. Nếu có các handler sự kiện pointer khác trong document, chúng sẽ không được trigger ngẫu nhiên bởi pointer trong khi người dùng đang kéo slider.

### [Pointer capturing events](#pointer-capturing-events)

Có một điều nữa cần đề cập ở đây, để completeness.

Có hai sự kiện liên quan đến pointer capturing:

- `gotpointercapture` kích hoạt khi một phần tử sử dụng `setPointerCapture` để enable capturing.
- `lostpointercapture` kích hoạt khi capture được release:要么是explicit với `releasePointerCapture` call, hoặc tự động на `pointerup`/`pointercancel`.

## [Tổng kết](#summary)

Pointer events cho phép xử lý mouse, touch và pen events đồng thời, với một đoạn mã duy nhất.

Pointer events mở rộng mouse events. Chúng ta có thể thay thế `mouse` bằng `pointer` trong tên sự kiện và mong đợi mã của chúng ta tiếp tục hoạt động cho mouse, với hỗ trợ tốt hơn cho các loại device khác.

Đối với drag'n'drops và các tương tác touch phức tạp mà browser có thể quyết định hijack và xử lý theo cách của riêng nó – hãy nhớ hủy action mặc định на các sự kiện và đặt `touch-action: none` в CSS cho các phần tử mà chúng ta tham gia.

Các khả năng bổ sung của pointer events là:

- Hỗ trợ multi-touch bằng cách sử dụng `pointerId` và `isPrimary`.
- Các thuộc tính đặc thù device, chẳng hạn như `pressure`, `width/height`, và các thuộc tính khác.
- Pointer capturing: chúng ta có thể retarget tất cả các sự kiện pointer đến một phần tử cụ thể cho đến `pointerup`/`pointercancel`.

Tính đến nay, pointer events được hỗ trợ trong tất cả các browser chính, vì vậy chúng ta có thể chuyển sang chúng một cách an toàn, đặc biệt nếu không cần IE10- và Safari 12-. Và ngay cả với các browser đó, có các polyfills cho phép hỗ trợ pointer events.
