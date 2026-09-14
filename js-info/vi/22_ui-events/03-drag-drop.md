# Kéo thả (Drag'n'Drop) với sự kiện chuột

> Source: [https://javascript.info/mouse-drag-and-drop](https://javascript.info/mouse-drag-and-drop)

<!-- fetched: 2026-09-14 -->

Drag'n'Drop là một giải pháp giao diện tuyệt vời. Lấy một thứ gì đó và kéo thả nó là một cách rõ ràng và đơn giản để làm nhiều việc, từ sao chép và di chuyển tài liệu (như trong file managers) đến sắp xếp (thả các mục vào giỏ hàng).

Trong tiêu chuẩn HTML hiện đại có [một phần về Drag and Drop](https://html.spec.whatwg.org/multipage/interaction.html#dnd) với các sự kiện đặc biệt như `dragstart`, `dragend`, và cứ thế.

Các sự kiện này cho phép chúng ta hỗ trợ các loại drag'n'drop đặc biệt, chẳng hạn như xử lý kéo một file từ OS file-manager và thả nó vào cửa sổ trình duyệt. Sau đó JavaScript có thể truy cập nội dung của các file như vậy.

Nhưng Native Drag Events cũng có những hạn chế. Ví dụ, chúng ta không thể ngăn dragging từ một khu vực nhất định. Ngoài ra chúng ta không thể làm cho dragging "ngang" hoặc "dọc" duy nhất. Và có nhiều tác vụ drag'n'drop khác không thể làm được bằng cách sử dụng chúng. Ngoài ra, hỗ trợ thiết bị di động cho các sự kiện như vậy rất yếu.

Vì vậy, ở đây chúng ta sẽ xem cách triển khai Drag'n'Drop bằng mouse events.

## [Thuật toán Drag'n'Drop](#drag-n-drop-algorithm)

Thuật toán Drag'n'Drop cơ bản trông như sau:

1. Trên `mousedown` – chuẩn bị phần tử để di chuyển, nếu cần (có thể tạo một bản sao của nó, thêm một class hoặc bất cứ điều gì).
2. Sau đó trên `mousemove` di chuyển nó bằng cách thay đổi `left/top` với `position:absolute`.
3. Trên `mouseup` – thực hiện tất cả các hành động liên quan đến việc hoàn thành drag'n'drop.

Đây là những cơ bản. Sau đó chúng ta sẽ xem cách thêm các tính năng khác, chẳng hạn như làm nổi bật các phần tử hiện tại đang nằm dưới chúng ta trong khi chúng ta drag nad chúng.

Đây là triển khai kéo một quả bóng:

```
ball.onmousedown = function(event) {
  // (1) prepare to moving: make absolute and on top by z-index
  ball.style.position = 'absolute';
  ball.style.zIndex = 1000;

  // move it out of any current parents directly into body
  // to make it positioned relative to the body
  document.body.append(ball);

  // centers the ball at (pageX, pageY) coordinates
  function moveAt(pageX, pageY) {
    ball.style.left = pageX - ball.offsetWidth / 2 + 'px';
    ball.style.top = pageY - ball.offsetHeight / 2 + 'px';
  }

  // move our absolutely positioned ball under the pointer
  moveAt(event.pageX, event.pageY);

  function onMouseMove(event) {
    moveAt(event.pageX, event.pageY);
  }

  // (2) move the ball on mousemove
  document.addEventListener('mousemove', onMouseMove);

  // (3) drop the ball, remove unneeded handlers
  ball.onmouseup = function() {
    document.removeEventListener('mousemove', onMouseMove);
    ball.onmouseup = null;
  };

};
```

Nếu chúng ta chạy mã, chúng ta có thể nhận thấy điều gì đó kỳ lạ. Vào đầu drag'n'drop, quả bóng "phân nhánh": chúng ta bắt đầu kéo "clone" của nó.

Đây là một ví dụ về hành động:

Thử drag'n'drop với chuột và bạn sẽ thấy hành vi như vậy.

Đó là vì trình duyệt có hỗ trợ drag'n'drop riêng cho images và một số phần tử khác. Nó chạy tự động và xung đột với mã của chúng ta.

Để vô hiệu hóa nó:

```
ball.ondragstart = function() {
  return false;
};
```

Bây giờ mọi thứ sẽ ổn.

Trong hành động:

Một khía cạnh quan trọng khác – chúng ta theo dõi `mousemove` trên `document`, không phải trên `ball`. Từ cái nhìn đầu tiên có vẻ như chuột luôn над quả bóng, và chúng ta có thể đặt `mousemove` trên nó.

Nhưng như chúng ta nhớ, `mousemove` kích hoạt thường xuyên, nhưng không phải cho mọi pixel. Vì vậy, sau khi di chuyển nhanh, con trỏ có thể nhảy từ quả bóng đến đâu đó ở giữa document (hoặc thậm chí ngoài cửa sổ).

Vì vậy, chúng ta nên lắng nghe trên `document` để bắt được nó.

## [Định vị chính xác](#correct-positioning)

Trong các ví dụ trên, quả bóng luôn được di chuyển sao cho tâm của nó nằm dưới con trỏ:

```
ball.style.left = pageX - ball.offsetWidth / 2 + 'px';
ball.style.top = pageY - ball.offsetHeight / 2 + 'px';
```

Không tệ, nhưng có một tác dụng phụ. Để khởi tạo drag'n'drop, chúng ta có thể `mousedown` ở bất kỳ đâu trên quả bóng. Nhưng nếu "nhặt" nó từ cạnh, thì quả bóng đột ngột "nhảy" để trở thành centered under the mouse pointer.

Tốt hơn nếu chúng ta giữ nguyên độ lệch ban đầu của phần tử so với con trỏ.

Ví dụ, nếu chúng ta bắt đầu kéo bằng cạnh của quả bóng, thì con trỏ nên tetap nằm trên cạnh trong khi kéo.

![](/article/mouse-drag-and-drop/ball_shift.svg)

Hãy cập nhật thuật toán của chúng ta:

1. Khi người dùng nhấn nút (`mousedown`) – ghi nhớ khoảng cách từ con trỏ đến góc trên bên trái của quả bóng trong các biến `shiftX/shiftY`. Chúng ta sẽ giữ khoảng cách đó trong khi kéo.

   Để lấy các shift này, chúng ta có thể trừ tọa độ:

   ```
   // onmousedown
   let shiftX = event.clientX - ball.getBoundingClientRect().left;
   let shiftY = event.clientY - ball.getBoundingClientRect().top;
   ```
2. Sau đó trong khi kéo, chúng ta định vị quả bóng với cùng shift so với con trỏ, như sau:

   ```
   // onmousemove
   // ball has position:absolute
   ball.style.left = event.pageX - shiftX + 'px';
   ball.style.top = event.pageY - shiftY + 'px';
   ```

Mã cuối cùng với định vị tốt hơn:

```
ball.onmousedown = function(event) {

  let shiftX = event.clientX - ball.getBoundingClientRect().left;
  let shiftY = event.clientY - ball.getBoundingClientRect().top;

  ball.style.position = 'absolute';
  ball.style.zIndex = 1000;
  document.body.append(ball);

  moveAt(event.pageX, event.pageY);

  // moves the ball at (pageX, pageY) coordinates
  // taking initial shifts into account
  function moveAt(pageX, pageY) {
    ball.style.left = pageX - shiftX + 'px';
    ball.style.top = pageY - shiftY + 'px';
  }

  function onMouseMove(event) {
    moveAt(event.pageX, event.pageY);
  }

  // move the ball on mousemove
  document.addEventListener('mousemove', onMouseMove);

  // drop the ball, remove unneeded handlers
  ball.onmouseup = function() {
    document.removeEventListener('mousemove', onMouseMove);
    ball.onmouseup = null;
  };

};

ball.ondragstart = function() {
  return false;
};
```

Trong hành động (trong `<iframe>`):

Sự khác biệt đặc biệt rõ ràng nếu chúng ta kéo quả bóng bằng góc phải-dưới của nó. Trong ví dụ trước, quả bóng "nhảy" dưới con trỏ. Bây giờ nó di chuyển mượt mà theo con trỏ từ vị trí hiện tại.

## [Các drop target tiềm năng (droppables)](#potential-drop-targets-droppables)

Trong các ví dụ trước, quả bóng có thể được thả "bất kỳ đâu" để ở lại. Trong cuộc sống thực, chúng ta thường lấy một phần tử và thả nó lên một phần tử khác. Ví dụ, một "file" vào một "folder" hoặc thứ gì đó khác.

Nói một cách trừu tượng, chúng ta lấy một phần tử "draggable" và thả nó lên phần tử "droppable".

Chúng ta cần biết:

- nơi phần tử được thả vào cuối Drag'n'Drop – để thực hiện hành động tương ứng,
- và, tốt hơn hết, biết droppable mà chúng ta đang drag qua, để làm nổi bật nó.

Giải pháp khá thú vị và hơi tinh tế một chút, vì vậy hãy đề cập đến nó ở đây.

Ý nghĩ đầu tiên có thể là gì? Có lẽ đặt các handler `mouseover/mouseup` trên các droppables tiềm năng?

Nhưng điều đó không hoạt động.

Vấn đề là, trong khi chúng ta đang kéo, phần tử draggable luôn nằm trên các phần tử khác. Và các sự kiện mouse chỉ xảy ra trên phần tử trên cùng, không phải trên các phần tử bên dưới nó.

Ví dụ, bên dưới là hai phần tử `<div>`, một màu đỏ nằm trên màu xanh (che phủ hoàn toàn). Không có cách nào để bắt sự kiện trên màu xanh, vì màu đỏ nằm trên cùng:

```
<style>
  div {
    width: 50px;
    height: 50px;
    position: absolute;
    top: 0;
  }
</style>
<div style="background:blue" onmouseover="alert('never works')"></div>
<div style="background:red" onmouseover="alert('over red!')"></div>
```

Cũng giống với phần tử draggable. Quả bóng luôn nằm trên cùng над các phần tử khác, vì vậy các sự kiện xảy ra trên nó. Bất kể handler nào chúng ta đặt trên các phần tử bên dưới, chúng sẽ không hoạt động.

Đó là lý do tại sao ý tưởng ban đầu đặt các handler trên các droppables tiềm năng không hoạt động trong thực tế. Chúng sẽ không chạy.

Vậy phải làm gì?

Có một phương pháp gọi là `document.elementFromPoint(clientX, clientY)`. Nó trả về phần tử lồng sâu nhất trên tọa độ tương đối cửa sổ đã cho (hoặc `null` nếu tọa độ đã cho nằm ngoài cửa sổ). Nếu có nhiều phần tử chồng lấn nhau trên cùng tọa độ, thì phần tử trên cùng được trả về.

Chúng ta có thể sử dụng nó trong bất kỳ handler sự kiện mouse nào để phát hiện droppable tiềm năng dưới con trỏ, như sau:

```
// in a mouse event handler
ball.hidden = true; // (*) hide the element that we drag

let elemBelow = document.elementFromPoint(event.clientX, event.clientY);
// elemBelow is the element below the ball, may be droppable

ball.hidden = false;
```

Xin lưu ý: chúng ta cần ẩn quả bóng trước khi gọi `(*)`. Nếu không, chúng ta thường sẽ có một quả bóng trên những tọa độ đó, vì nó là phần tử trên cùng dưới con trỏ: `elemBelow=ball`. Vì vậy, chúng ta ẩn nó và ngay lập tức hiển thị lại.

Chúng ta có thể sử dụng mã đó để kiểm tra phần tử nào chúng ta đang "bay qua" tại bất kỳ thời điểm nào. Và xử lý drop khi nó xảy ra.

Mã mở rộng của `onMouseMove` để tìm các phần tử "droppable":

```
// potential droppable that we're flying over right now
let currentDroppable = null;

function onMouseMove(event) {
  moveAt(event.pageX, event.pageY);

  ball.hidden = true;
  let elemBelow = document.elementFromPoint(event.clientX, event.clientY);
  ball.hidden = false;

  // mousemove events may trigger out of the window (when the ball is dragged off-screen)
  // if clientX/clientY are out of the window, then elementFromPoint returns null
  if (!elemBelow) return;

  // potential droppables are labeled with the class "droppable" (can be other logic)
  let droppableBelow = elemBelow.closest('.droppable');

  if (currentDroppable != droppableBelow) {
    // we're flying in or out...
    // note: both values can be null
    //   currentDroppable=null if we were not over a droppable before this event (e.g over an empty space)
    //   droppableBelow=null if we're not over a droppable now, during this event

    if (currentDroppable) {
      // the logic to process "flying out" of the droppable (remove highlight)
      leaveDroppable(currentDroppable);
    }
    currentDroppable = droppableBelow;
    if (currentDroppable) {
      // the logic to process "flying in" of the droppable
      enterDroppable(currentDroppable);
    }
  }
}
```

Trong ví dụ dưới đây, khi quả bóng được kéo над khung thành bóng đá, khung thành được làm nổi bật.

Result

style.css

index.html

```
#gate {
  cursor: pointer;
  margin-bottom: 100px;
  width: 83px;
  height: 46px;
}

#ball {
  cursor: pointer;
  width: 40px;
  height: 40px;
}
```

```
<!doctype html>
<html>

<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="style.css">
</head>

<body>

  <p>Drag the ball.</p>

  <img src="https://en.js.cx/clipart/soccer-gate.svg" id="gate" class="droppable">

  <img src="https://en.js.cx/clipart/ball.svg" id="ball">

  <script>
    let currentDroppable = null;

    ball.onmousedown = function(event) {

      let shiftX = event.clientX - ball.getBoundingClientRect().left;
      let shiftY = event.clientY - ball.getBoundingClientRect().top;

      ball.style.position = 'absolute';
      ball.style.zIndex = 1000;
      document.body.append(ball);

      moveAt(event.pageX, event.pageY);

      function moveAt(pageX, pageY) {
        ball.style.left = pageX - shiftX + 'px';
        ball.style.top = pageY - shiftY + 'px';
      }

      function onMouseMove(event) {
        moveAt(event.pageX, event.pageY);

        ball.hidden = true;
        let elemBelow = document.elementFromPoint(event.clientX, event.clientY);
        ball.hidden = false;

        if (!elemBelow) return;

        let droppableBelow = elemBelow.closest('.droppable');
        if (currentDroppable != droppableBelow) {
          if (currentDroppable) { // null when we were not over a droppable before this event
            leaveDroppable(currentDroppable);
          }
          currentDroppable = droppableBelow;
          if (currentDroppable) { // null if we're not coming over a droppable now
            // (maybe just left the droppable)
            enterDroppable(currentDroppable);
          }
        }
      }

      document.addEventListener('mousemove', onMouseMove);

      ball.onmouseup = function() {
        document.removeEventListener('mousemove', onMouseMove);
        ball.onmouseup = null;
      };

    };

    function enterDroppable(elem) {
      elem.style.background = 'pink';
    }

    function leaveDroppable(elem) {
      elem.style.background = '';
    }

    ball.ondragstart = function() {
      return false;
    };
  </script>

</body>
</html>
```

Bây giờ chúng ta có "drop target" hiện tại, mà chúng ta đang bay qua, trong biến `currentDroppable` trong suốt quá trình và có thể sử dụng nó để làm nổi bật hoặc bất cứ thứ gì khác.

## [Tổng kết](#summary)

Chúng ta đã xem xét thuật toán Drag'n'Drop cơ bản.

Các thành phần chính:

1. Dòng sự kiện: `ball.mousedown` → `document.mousemove` → `ball.mouseup` (đừng quên hủy native `ondragstart`).
2. Tại thời điểm bắt đầu kéo – ghi nhớ độ lệch ban đầu của con trỏ so với phần tử: `shiftX/shiftY` và giữ nó trong khi kéo.
3. Phát hiện các phần tử droppable dưới con trỏ bằng cách sử dụng `document.elementFromPoint`.

Chúng ta có thể xây dựng nhiều thứ trên nền tảng này.

- Trên `mouseup` chúng ta có thể hoàn thành việc drop một cách thông minh: thay đổi dữ liệu, di chuyển các phần tử xung quanh.
- Chúng ta có thể làm nổi bật các phần tử mà chúng ta đang bay qua.
- Chúng ta có thể giới hạn kéo trong một khu vực hoặc hướng nhất định.
- Chúng ta có thể sử dụng event delegation cho `mousedown/up`. Một handler diện rộng kiểm tra `event.target` có thể quản lý Drag'n'Drop cho hàng trăm phần tử.
- Và cứ thế.

Có các framework xây dựng kiến trúc над nó: `DragZone`, `Droppable`, `Draggable` và các class khác. Phần lớn chúng làm những thứ tương tự như những gì được mô tả ở trên, vì vậy nên dễ hiểu chúng bây giờ. Hoặc tự tạo của riêng bạn, vì bạn có thể thấy rằng nó đủ dễ để làm, đôi khi dễ hơn là thích nghi với một giải pháp bên thứ ba.

---

---

## Bài tập

## [Bài tập](#tasks)

### [Slider](#slider)

mức độ khó: 5

Tạo một slider:

Kéo thumb màu xanh dương bằng chuột và di chuyển nó.

Các chi tiết quan trọng:

- Khi nút chuột được nhấn, trong khi kéo, chuột có thể đi над hoặc dưới slider. Slider vẫn sẽ hoạt động (thuận tiện cho người dùng).
- Nếu chuột di chuyển rất nhanh sang trái hoặc sang phải, thumb sẽ dừng lại chính xác ở cạnh.

[Mở sandbox cho bài tập.](https://plnkr.co/edit/O5BS81UcgnF59wgT?p=preview)

lời giải

Như chúng ta có thể thấy từ HTML/CSS, slider là một `<div>` với nền màu, chứa một runner – một `<div>` khác với `position:relative`.

Để định vị runner, chúng ta sử dụng `position:relative`, để cung cấp tọa độ tương đối với parent của nó, ở đây nó thuận tiện hơn `position:absolute`.

Sau đó chúng ta triển khai horizontal-only Drag'n'Drop với giới hạn bởi chiều rộng.

[Mở solution trong sandbox.](https://plnkr.co/edit/pVpnPtdObbEODNyb?p=preview)

### [Kéo các superheroes xung quanh field](#drag-superheroes-around-the-field)

mức độ khó: 5

Bài tập này có thể giúp bạn kiểm tra hiểu biết về nhiều khía cạnh của Drag'n'Drop và DOM.

Làm cho tất cả các phần tử có class `draggable` – draggable. Giống như quả bóng trong chương.

Yêu cầu:

- Sử dụng event delegation để theo dõi bắt đầu kéo: một handler sự kiện duy nhất trên `document` cho `mousedown`.
- Nếu các phần tử được kéo đến các cạnh trên/dưới của cửa sổ – trang sẽ scroll lên/xuống để cho phép kéo tiếp.
- Không có horizontal scroll (điều này làm cho bài tập đơn giản hơn, thêm vào đó dễ dàng).
- Các phần tử draggable hoặc các phần của chúng không bao giờ rời khỏi cửa sổ, ngay cả sau các chuyển động chuột nhanh.

Bản demo quá lớn để chứa ở đây, vì vậy đây là liên kết.

[Demo trong cửa sổ mới](https://en.js.cx/task/drag-heroes/solution/)

[Mở sandbox cho bài tập.](https://plnkr.co/edit/EaKVQSvt99GYC509?p=preview)

lời giải

Để kéo phần tử, chúng ta có thể sử dụng `position:fixed`, nó làm cho tọa độ dễ quản lý hơn. Ở cuối chúng ta nên chuyển nó lại thành `position:absolute` để đặt phần element vào document.

Khi tọa độ nằm ở trên/dưới cửa sổ, chúng ta sử dụng `window.scrollTo` để scroll nó.

Chi tiết hơn trong mã, trong các comments.

[Mở solution trong sandbox.](https://plnkr.co/edit/reabnpVkO85VIx7T?p=preview)
