# Giới thiệu về các sự kiện trình duyệt

> Source: [https://javascript.info/introduction-browser-events](https://javascript.info/introduction-browser-events)

<!-- fetched: 2026-09-14 -->

*Một sự kiện* là tín hiệu cho biết đã có cái gì đó xảy ra. Tất cả các nút DOM đều tạo ra các tín hiệu như vậy (nhưng sự kiện không giới hạn ở DOM).

Dưới đây là danh sách các sự kiện DOM hữu ích nhất, chỉ để xem thôi:

**Sự kiện chuột:**

- `click` – khi chuột nhấp vào một phần tử (thiết bị màn hình cảm ứng tạo ra nó khi nhấn chạm).
- `contextmenu` – khi chuột nhấp chuột phải vào một phần tử.
- `mouseover` / `mouseout` – khi con trỏ chuột đi vào / rời khỏi một phần tử.
- `mousedown` / `mouseup` – khi nút chuột được nhấn / thả ra trên một phần tử.
- `mousemove` – khi chuột được di chuyển.

**Sự kiện bàn phím:**

- `keydown` và `keyup` – khi một phím bàn phím được nhấn và thả ra.

**Sự kiện phần tử biểu mẫu:**

- `submit` – khi người truy cập gửi một `<form>`.
- `focus` – khi người truy cập tập trung vào một phần tử, ví dụ trên một `<input>`.

**Sự kiện tài liệu:**

- `DOMContentLoaded` – khi HTML được tải và xử lý, DOM được xây dựng hoàn toàn.

**Sự kiện CSS:**

- `transitionend` – khi một animation CSS kết thúc.

Còn nhiều sự kiện khác. Chúng ta sẽ đi sâu vào chi tiết các sự kiện cụ thể trong các chương tới.

## [Trình xử lý sự kiện](#event-handlers)

Để phản ứng lại sự kiện, chúng ta có thể gán một *trình xử lý* – một hàm chạy trong trường hợp sự kiện xảy ra.

Trình xử lý là cách để chạy mã JavaScript khi có hành động của người dùng.

Có một số cách để gán trình xử lý. Hãy xem chúng, bắt đầu từ cách đơn giản nhất.

### [Thuộc tính HTML](#html-attribute)

Một trình xử lý có thể được đặt trong HTML với một thuộc tính tên là `on<event>`.

Ví dụ, để gán trình xử lý `click` cho một `input`, chúng ta có thể sử dụng `onclick`, như sau:

```
<input value="Click me" onclick="alert('Click!')" type="button">
```

Khi nhấp chuột, mã bên trong `onclick` chạy.

Lưu ý rằng bên trong `onclick` chúng ta sử dụng dấu ngoặc đơn, vì chính thuộc tính đó nằm trong dấu ngoặc kép. Nếu quên rằng mã nằm bên trong thuộc tính và sử dụng dấu ngoặc kép bên trong, như sau: `onclick="alert("Click!")"`, thì nó sẽ không hoạt động đúng.

Thuộc tính HTML không phải là nơi thuận tiện để viết nhiều mã, vì vậy chúng ta nên tạo một hàm JavaScript và gọi nó ở đó.

Ở đây một lần nhấp chuột chạy hàm `countRabbits()`:

```
<script>
  function countRabbits() {
    for(let i=1; i<=3; i++) {
      alert("Rabbit number " + i);
    }
  }
</script>

<input type="button" onclick="countRabbits()" value="Count rabbits!">
```

Như chúng ta biết, tên thuộc tính HTML không phân biệt chữ hoa chữ thường, nên `ONCLICK` hoạt động giống như `onClick` và `onCLICK`... Nhưng thường thì các thuộc tính được viết thường: `onclick`.

### [Thuộc tính DOM](#dom-property)

Chúng ta có thể gán trình xử lý bằng cách sử dụng thuộc tính DOM `on<event>`.

Ví dụ, `elem.onclick`:

```
<input id="elem" type="button" value="Click me">
<script>
  elem.onclick = function() {
    alert('Thank you');
  };
</script>
```

Nếu trình xử lý được gán bằng thuộc tính HTML thì trình duyệt đọc nó, tạo một hàm mới từ nội dung thuộc tính và ghi nó vào thuộc tính DOM.

Vì vậy cách này thực tế giống với cách trước.

Hai đoạn mã này hoạt động giống nhau:

1. Chỉ HTML:

   ```
   <input type="button" onclick="alert('Click!')" value="Button">
   ```
2. HTML + JS:

   ```
   <input type="button" id="button" value="Button">
   <script>
     button.onclick = function() {
       alert('Click!');
     };
   </script>
   ```

Trong ví dụ đầu tiên, thuộc tính HTML được dùng để khởi tạo `button.onclick`, còn trong ví dụ thứ hai – là script, đó là toàn bộ sự khác biệt.

**Vì chỉ có một thuộc tính `onclick`, chúng ta không thể gán hơn một trình xử lý sự kiện.**

Trong ví dụ dưới đây, việc thêm trình xử lý bằng JavaScript ghi đè trình xử lý hiện có:

```
<input type="button" id="elem" onclick="alert('Before')" value="Click me">
<script>
  elem.onclick = function() { // ghi đè trình xử lý hiện có
    alert('After'); // chỉ cái này được hiển thị
  };
</script>
```

Để xóa trình xử lý – gán `elem.onclick = null`.

## [Truy cập phần tử: this](#accessing-the-element-this)

Giá trị của `this` bên trong trình xử lý là phần tử. Phần tử có trình xử lý trên nó.

Trong mã dưới đây `button` hiển thị nội dung của nó bằng `this.innerHTML`:

```
<button onclick="alert(this.innerHTML)">Click me</button>
```

## [Các lỗi có thể xảy ra](#possible-mistakes)

Nếu bạn mới bắt đầu làm việc với sự kiện – hãy lưu ý một số điểm tinh tế.

Chúng ta có thể đặt một hàm hiện có làm trình xử lý:

```
function sayThanks() {
  alert('Thanks!');
}

elem.onclick = sayThanks;
```

Nhưng hãy cẩn thận: hàm nên được gán như `sayThanks`, không phải `sayThanks()`.

```
// đúng
button.onclick = sayThanks;

// sai
button.onclick = sayThanks();
```

Nếu thêm dấu ngoặc đơn, thì `sayThanks()` trở thành lời gọi hàm. Vì vậy dòng cuối cùng thực tế lấy *kết quả* của việc thực thi hàm, đó là `undefined` (vì hàm không trả về gì), và gán nó cho `onclick`. Điều đó không hoạt động.

…Mặt khác, trong markup chúng ta *cần* dấu ngoặc đơn:

```
<input type="button" id="button" onclick="sayThanks()">
```

Sự khác biệt dễ hiểu. Khi trình duyệt đọc thuộc tính, nó tạo một hàm trình xử lý với nội dung từ thuộc tính.

Vì vậy markup tạo ra thuộc tính này:

```
button.onclick = function() {
  sayThanks(); // <-- nội dung thuộc tính ở đây
};
```

**Đừng dùng `setAttribute` cho trình xử lý.**

Lời gọi như vậy sẽ không hoạt động:

```
// nhấp vào <body> sẽ tạo ra lỗi,
// vì thuộc tính luôn là chuỗi, hàm trở thành chuỗi
document.body.setAttribute('onclick', function() { alert(1) });
```

**Chữ hoa chữ thường của thuộc tính DOM quan trọng.**

Gán trình xử lý cho `elem.onclick`, không phải `elem.ONCLICK`, vì thuộc tính DOM phân biệt chữ hoa chữ thường.

## [addEventListener](#addeventlistener)

Vấn đề cơ bản của các cách gán trình xử lý nêu trên là chúng ta *không thể gán nhiều trình xử lý cho một sự kiện*.

Giả sử, một phần code của chúng ta muốn làm nổi bật nút khi nhấp chuột, và phần khác muốn hiển thị thông báo trên cùng một lần nhấp.

Chúng ta muốn gán hai trình xử lý sự kiện cho việc đó. Nhưng một thuộc tính DOM mới sẽ ghi đè cái hiện có:

```
input.onclick = function() { alert(1); }
// ...
input.onclick = function() { alert(2); } // thay thế trình xử lý trước đó
```

Nhà phát triển chuẩn web đã hiểu điều đó từ lâu và đề xuất một cách thay thế để quản lý trình xử lý bằng các phương thức đặc biệt `addEventListener` và `removeEventListener` không bị giới hạn bởi ràng buộc đó.

Cú pháp để thêm trình xử lý:

```
element.addEventListener(event, handler, [options]);
```

`event`
:   Tên sự kiện, ví dụ `"click"`.

`handler`
:   Hàm trình xử lý.

`options`
:   Một đối tượng tùy chọn bổ sung với các thuộc tính:

    - `once`: nếu `true`, thì trình lắng nghe sẽ tự động bị xóa sau khi nó kích hoạt.
    - `capture`: giai đoạn để xử lý sự kiện, sẽ được trình bày sau trong chương [Bubbling and capturing](/bubbling-and-capturing). Với lý do lịch sử, `options` cũng có thể là `false/true`, tương đương với `{capture: false/true}`.
    - `passive`: nếu `true`, thì trình xử lý sẽ không gọi `preventDefault()`, chúng ta sẽ giải thích sau trong [Browser default actions](/default-browser-action).

Để xóa trình xử lý, sử dụng `removeEventListener`:

```
element.removeEventListener(event, handler, [options]);
```

Xóa yêu cầu cùng một hàm

Để xóa trình xử lý, chúng ta nên truyền chính xác hàm giống như đã gán.

Điều này không hoạt động:

```
elem.addEventListener( "click" , () => alert('Thanks!'));
// ....
elem.removeEventListener( "click", () => alert('Thanks!'));
```

Trình xử lý sẽ không bị xóa, vì `removeEventListener` nhận một hàm khác – với cùng mã, nhưng đó không quan trọng, vì nó là một đối tượng hàm khác.

Đây là cách đúng:

```
function handler() {
  alert( 'Thanks!' );
}

input.addEventListener("click", handler);
// ....
input.removeEventListener("click", handler);
```

Lưu ý – nếu chúng ta không lưu hàm trong một biến, thì không thể xóa nó. Không có cách nào để "đọc lại" các trình xử lý được gán bởi `addEventListener`.

Nhiều lần gọi `addEventListener` cho phép nó thêm nhiều trình xử lý, như sau:

```
<input id="elem" type="button" value="Click me"/>

<script>
  function handler1() {
    alert('Thanks!');
  };

  function handler2() {
    alert('Thanks again!');
  }

  elem.onclick = () => alert("Hello");
  elem.addEventListener("click", handler1); // Thanks!
  elem.addEventListener("click", handler2); // Thanks again!
</script>
```

Như chúng ta thấy trong ví dụ trên, chúng ta có thể đặt trình xử lý *cả* bằng thuộc tính DOM và `addEventListener`. Nhưng nói chung chúng ta chỉ dùng một trong hai cách này.

Đối với một số sự kiện, trình xử lý chỉ hoạt động với `addEventListener`

Tồn tại các sự kiện không thể gán qua thuộc tính DOM. Chỉ với `addEventListener`.

Ví dụ, sự kiện `DOMContentLoaded`, kích hoạt khi tài liệu được tải và DOM đã được xây dựng.

```
// sẽ không bao giờ chạy
document.onDOMContentLoaded = function() {
  alert("DOM built");
};
```

```
// cách này hoạt động
document.addEventListener("DOMContentLoaded", function() {
  alert("DOM built");
});
```

Vì vậy `addEventListener` phổ biến hơn. Mặc dù, những sự kiện như vậy là ngoại lệ chứ không phải quy tắc.

## [Đối tượng sự kiện](#event-object)

Để xử lý đúng một sự kiện, chúng ta muốn biết thêm về những gì đã xảy ra. Không chỉ "click" hay "keydown", mà tọa độ con trỏ là gì? Phím nào được nhấn? V.v.

Khi sự kiện xảy ra, trình duyệt tạo một *đối tượng sự kiện*, đặt chi tiết vào nó và truyền nó làm đối số cho trình xử lý.

Đây là ví dụ về lấy tọa độ con trỏ từ đối tượng sự kiện:

```
<input type="button" value="Click me" id="elem">

<script>
  elem.onclick = function(event) {
    // hiển thị loại sự kiện, phần tử và tọa độ của lần nhấp
    alert(event.type + " at " + event.currentTarget);
    alert("Coordinates: " + event.clientX + ":" + event.clientY);
  };
</script>
```

Một số thuộc tính của đối tượng `event`:

`event.type`
:   Loại sự kiện, ở đây là `"click"`.

`event.currentTarget`
:   Phần tử đã xử lý sự kiện. Đó chính xác là `this`, trừ khi trình xử lý là hàm mũi tên, hoặc `this` của nó bị gán cho cái khác, thì chúng ta có thể lấy phần tử từ `event.currentTarget`.

`event.clientX` / `event.clientY`
:   Tọa độ tương đối cửa sổ của con trỏ, cho sự kiện con trỏ.

Còn nhiều thuộc tính khác. Nhiều thuộc tính trong số đó phụ thuộc vào loại sự kiện: sự kiện bàn phím có một tập thuộc tính, sự kiện con trỏ – tập khác, chúng ta sẽ nghiên cứu chúng sau khi chuyển sang chi tiết các sự kiện khác nhau.

Đối tượng sự kiện cũng có sẵn trong trình xử lý HTML

Nếu chúng ta gán trình xử lý trong HTML, chúng ta cũng có thể dùng đối tượng `event`, như sau:

```
<input type="button" onclick="alert(event.type)" value="Event type">
```

Điều đó có thể vì khi trình duyệt đọc thuộc tính, nó tạo trình xử lý như sau: `function(event) { alert(event.type) }`. Nghĩa là: đối số đầu tiên của nó gọi là `"event"`, và nội dung được lấy từ thuộc tính.

## [Trình xử lý đối tượng: handleEvent](#object-handlers-handleevent)

Chúng ta không chỉ gán một hàm, mà còn có thể gán một đối tượng làm trình xử lý sự kiện bằng `addEventListener`. Khi sự kiện xảy ra, phương thức `handleEvent` của nó được gọi.

Ví dụ:

```
<button id="elem">Click me</button>

<script>
  let obj = {
    handleEvent(event) {
      alert(event.type + " at " + event.currentTarget);
    }
  };

  elem.addEventListener('click', obj);
</script>
```

Như chúng ta thấy, khi `addEventListener` nhận một đối tượng làm trình xử lý, nó gọi `obj.handleEvent(event)` khi có sự kiện.

Chúng ta cũng có thể dùng đối tượng của lớp tùy chỉnh, như sau:

```
<button id="elem">Click me</button>

<script>
  class Menu {
    handleEvent(event) {
      switch(event.type) {
        case 'mousedown':
          elem.innerHTML = "Mouse button pressed";
          break;
        case 'mouseup':
          elem.innerHTML += "...and released.";
          break;
      }
    }
  }

  let menu = new Menu();

  elem.addEventListener('mousedown', menu);
  elem.addEventListener('mouseup', menu);
</script>
```

Ở đây cùng một đối tượng xử lý cả hai sự kiện. Lưu ý rằng chúng ta cần thiết lập rõ ràng các sự kiện để lắng nghe bằng `addEventListener`. Đối tượng `menu` chỉ nhận `mousedown` và `mouseup` ở đây, không phải bất kỳ loại sự kiện nào khác.

Phương thức `handleEvent` không phải làm tất cả việc mình. Nó có thể gọi các phương thức cụ thể cho sự kiện thay vào đó, như sau:

```
<button id="elem">Click me</button>

<script>
  class Menu {
    handleEvent(event) {
      // mousedown -> onMousedown
      let method = 'on' + event.type[0].toUpperCase() + event.type.slice(1);
      this[method](event);
    }

    onMousedown() {
      elem.innerHTML = "Mouse button pressed";
    }

    onMouseup() {
      elem.innerHTML += "...and released.";
    }
  }

  let menu = new Menu();

  elem.addEventListener('mousedown', menu);
  elem.addEventListener('mouseup', menu);
</script>
```

Bây giờ trình xử lý sự kiện được tách biệt rõ ràng, có thể dễ dàng hỗ trợ hơn.

## [Tóm tắt](#summary)

Có 3 cách để gán trình xử lý sự kiện:

1. Thuộc tính HTML: `onclick="..."`.
2. Thuộc tính DOM: `elem.onclick = function`.
3. Phương thức: `elem.addEventListener(event, handler[, phase])` để thêm, `removeEventListener` để xóa.

Thuộc tính HTML được dùng ít, vì JavaScript ở giữa thẻ HTML trông hơi lạ. Cũng không thể viết nhiều mã ở đó.

Thuộc tính DOM ổn để dùng, nhưng chúng ta không thể gán hơn một trình xử lý cho một sự kiện cụ thể. Trong nhiều trường hợp hạn chế đó không quá khẩn thiết.

Cách cuối cùng linh hoạt nhất, nhưng cũng dài nhất để viết. Có một ít sự kiện chỉ hoạt động với nó, ví dụ `transitionend` và `DOMContentLoaded` (sẽ trình bày). Cũng `addEventListener` hỗ trợ đối tượng làm trình xử lý sự kiện. Trong trường hợp đó phương thức `handleEvent` được gọi khi có sự kiện.

Không quan trọng bạn gán trình xử lý như thế nào – nó nhận đối tượng sự kiện làm đối số đầu tiên. Đối tượng đó chứa chi tiết về những gì đã xảy ra.

Chúng ta sẽ tìm hiểu thêm về sự kiện nói chung và về các loại sự kiện khác nhau trong các chương tới.

---

---

## Các bài tập

## [Tasks](#tasks)

### [Ẩn khi nhấp](#hide-on-click)

importance: 5

Thêm JavaScript cho `button` để làm `<div id="text">` biến mất khi nhấp vào nó.

Demo:

[Open a sandbox for the task.](https://plnkr.co/edit/6IFBx7wDt0dZMqP1?p=preview)

solution

[Open the solution in a sandbox.](https://plnkr.co/edit/PAzsU3E4l4hhkTAl?p=preview)

### [Ẩn chính mình](#hide-self)

importance: 5

Tạo một nút ẩn chính mình khi nhấp.

Như sau:

solution

Có thể dùng `this` trong trình xử lý để tham chiếu "phần tử chính nó" ở đây:

```
<input type="button" onclick="this.hidden=true" value="Click to hide">
```

### [Trình xử lý nào chạy?](#which-handlers-run)

importance: 5

Có một nút trong biến. Không có trình xử lý nào trên nó.

Trình xử lý nào chạy khi nhấp sau mã sau? Alert nào hiện lên?

```
button.addEventListener("click", () => alert("1"));

button.removeEventListener("click", () => alert("1"));

button.onclick = () => alert(2);
```

solution

Đáp án: `1` và `2`.

Trình xử lý đầu tiên kích hoạt, vì nó không bị xóa bởi `removeEventListener`. Để xóa trình xử lý, chúng ta cần truyền chính xác hàm đã gán. Và trong mã một hàm mới được truyền, trông giống nhau, nhưng vẫn là một hàm khác.

Để xóa một đối tượng hàm, chúng ta cần lưu tham chiếu đến nó, như sau:

```
function handler() {
  alert(1);
}

button.addEventListener("click", handler);
button.removeEventListener("click", handler);
```

Trình xử lý `button.onclick` hoạt động độc lập và bổ sung cho `addEventListener`.

### [Di chuyển bóng qua sân](#move-the-ball-across-the-field)

importance: 5

Di chuyển bóng qua sân đến vị trí nhấp. Như sau:

Yêu cầu:

- Tâm bóng phải nằm chính xác dưới con trỏ khi nhấp (nếu có thể mà không vượt ra rìa sân).
- Chào đón CSS-animation.
- Bóng không được vượt ra ranh giới sân.
- Khi trang được cuộn, không gì nên bị phá vỡ.

Lưu ý:

- Mã cũng phải hoạt động với kích thước bóng và sân khác nhau, không gắn liền với bất kỳ giá trị cố định nào.
- Dùng thuộc tính `event.clientX/event.clientY` cho tọa độ nhấp.

[Open a sandbox for the task.](https://plnkr.co/edit/IGCSLHiEspDxro6B?p=preview)

solution

Trước tiên chúng ta cần chọn phương thức định vị bóng.

Chúng ta không thể dùng `position:fixed` cho nó, vì cuộn trang sẽ di chuyển bóng ra khỏi sân.

Vì vậy chúng ta nên dùng `position:absolute` và, để định vị thực sự vững chắc, làm cho `field` được định vị.

Sau đó bóng sẽ được định vị tương đối với sân:

```
#field {
  width: 200px;
  height: 150px;
  position: relative;
}

#ball {
  position: absolute;
  left: 0; /* tương đối với tổ tiên được định vị gần nhất (field) */
  top: 0;
  transition: 1s all; /* CSS animation cho left/top làm bóng bay */
}
```

Tiếp theo chúng ta cần gán đúng `ball.style.left/top`. Chúng chứa tọa độ tương đối sân bây giờ.

Đây là hình ảnh:

![](/task/move-ball-field/move-ball-coords.svg)

Chúng ta có `event.clientX/clientY` – tọa độ tương đối cửa sổ của lần nhấp.

Để lấy tọa độ `left` tương đối sân của lần nhấp, chúng ta có thể trừ cạnh trái sân và độ rộng viền:

```
let left = event.clientX - fieldCoords.left - field.clientLeft;
```

Bình thường, `ball.style.left` có nghĩa là "cạnh trái phần tử" (bóng). Vì vậy nếu gán `left` đó, thì cạnh bóng, không phải tâm, sẽ nằm dưới con trỏ chuột.

Chúng ta cần di chuyển bóng nửa chiều rộng sang trái và nửa chiều cao lên trên để làm cho nó nằm giữa.

Vì vậy `left` cuối cùng sẽ là:

```
let left = event.clientX - fieldCoords.left - field.clientLeft - ball.offsetWidth/2;
```

Tọa độ dọc được tính bằng logic tương tự.

Lưu ý rằng chiều rộng/cao bóng phải được biết tại thời điểm truy cập `ball.offsetWidth`. Nên được chỉ định trong HTML hoặc CSS.

[Open the solution in a sandbox.](https://plnkr.co/edit/wuQbNr1Sz9GuDim1?p=preview)

### [Tạo menu trượt](#create-a-sliding-menu)

importance: 5

Tạo menu mở/thu gọn khi nhấp:

P.S. HTML/CSS của tài liệu nguồn sẽ được sửa đổi.

[Open a sandbox for the task.](https://plnkr.co/edit/FaUkuVA0NqIkeOxr?p=preview)

solution

HTML/CSS

#### HTML/CSS

Trước hãy tạo HTML/CSS.

Menu là thành phần đồ họa độc lập trên trang, vì vậy tốt hơn là đặt nó vào một phần tử DOM đơn nhất.

Danh sách các mục menu có thể bố trí như danh sách `ul/li`.

Đây là cấu trúc ví dụ:

```
<div class="menu">
  <span class="title">Sweeties (click me)!</span>
  <ul>
    <li>Cake</li>
    <li>Donut</li>
    <li>Honey</li>
  </ul>
</div>
```

Chúng ta dùng `<span>` cho tiêu đề, vì `<div>` có `display:block` ngầm định, và nó sẽ chiếm 100% chiều ngang.

Như sau:

```
<div style="border: solid red 1px" onclick="alert(1)">Sweeties (click me)!</div>
```

Vì vậy nếu đặt `onclick` trên nó, thì nó sẽ bắt nhấp chuột bên phải văn bản.

Vì `<span>` có `display: inline` ngầm định, nó chiếm đúng đủ chỗ cho vừa văn bản:

```
<span style="border: solid red 1px" onclick="alert(1)">Sweeties (click me)!</span>
```

Bật/tắt menu

#### Bật/tắt menu

Bật/tắt menu nên thay đổi mũi tên và hiển thị/ẩn danh sách menu.

Tất cả thay đổi này được xử lý hoàn hảo bởi CSS. Trong JavaScript, chúng ta chỉ nên gán nhãn trạng thái hiện tại của menu bằng cách thêm/xóa class `.open`.

Nó sẽ bị đóng nếu không có class:

```
.menu ul {
  margin: 0;
  list-style: none;
  padding-left: 20px;
  display: none;
}

.menu .title::before {
  content: '▶ ';
  font-size: 80%;
  color: green;
}
```

…Và với `.open` mũi tên thay đổi và danh sách hiện lên:

```
.menu.open .title::before {
  content: '▼ ';
}

.menu.open ul {
  display: block;
}
```

[Open the solution in a sandbox.](https://plnkr.co/edit/PYMbEaFxTp7NBw8y?p=preview)

### [Thêm nút đóng](#add-a-closing-button)

importance: 5

Có một danh sách tin nhắn.

Dùng JavaScript để thêm nút đóng vào góc trên bên phải của từng tin nhắn.

Kết quả nên trông như sau:

[Open a sandbox for the task.](https://plnkr.co/edit/IHg4ZICFUtAhqi8n?p=preview)

solution

Để thêm nút, chúng ta có thể dùng `position:absolute` (và làm pane `position:relative`) hoặc `float:right`. `float:right` có lợi thế là nút không bao giờ chồng lên văn bản, nhưng `position:absolute` cho nhiều tự do hơn. Vì vậy lựa chọn thuộc về bạn.

Sau đó cho mỗi pane mã có thể như sau:

```
pane.insertAdjacentHTML("afterbegin", '<button class="remove-button">[x]</button>');
```

Sau đó `<button>` trở thành `pane.firstChild`, vì vậy chúng ta có thể thêm trình xử lý cho nó như sau:

```
pane.firstChild.onclick = () => pane.remove();
```

[Open the solution in a sandbox.](https://plnkr.co/edit/a1RbQkIgBi9pzbGe?p=preview)

### [Carousel](#carousel)

importance: 4

Tạo một "carousel" – dải hình ảnh có thể cuộn bằng cách nhấp vào mũi tên.

Sau này có thể thêm nhiều tính năng hơn: cuộn vô hạn, tải động v.v.

P.S. Với bài tập này cấu trúc HTML/CSS thực tế là 90% giải pháp.

[Open a sandbox for the task.](https://plnkr.co/edit/vw9EAQcWlH1Xw9Nj?p=preview)

solution

Dải hình ảnh có thể biểu diễn dưới dạng danh sách `ul/li` các hình ảnh `<img>`.

Bình thường, dải như vậy rộng, nhưng chúng ta đặt một `<div>` kích thước cố định xung quanh để "cắt" nó, để chỉ một phần của dải hiển thị:

![](/task/carousel/carousel1.svg)

Để danh sách hiển thị ngang, chúng ta cần áp dụng thuộc tính CSS đúng cho `<li>`, như `display: inline-block`.

Cho `<img>` chúng ta cũng nên điều chỉnh `display`, vì mặc định nó là `inline`. Có khoảng trống dự phòng dưới các phần tử `inline` cho "đuôi chữ", vì vậy chúng ta có thể dùng `display:block` để loại bỏ nó.

Để cuộn, chúng ta có thể dịch `<ul>`. Có nhiều cách, ví dụ thay đổi `margin-left` hoặc (hiệu suất tốt hơn) dùng `transform: translateX()`:

![](/task/carousel/carousel2.svg)

`<div>` bên ngoài có chiều rộng cố định, nên các hình ảnh "thừa" bị cắt.

Cả carousel là một "thành phần đồ họa" độc lập trên trang, vì vậy tốt hơn là gói nó vào một `<div class="carousel">` đơn và định kiểu các thứ bên trong nó.

[Open the solution in a sandbox.](https://plnkr.co/edit/2xa7Ra0Bkq3yUndf?p=preview)