# Di chuyển chuột: mouseover/out, mouseenter/leave

> Source: [https://javascript.info/mousemove-mouseover-mouseout-mouseenter-mouseleave](https://javascript.info/mousemove-mouseover-mouseout-mouseenter-mouseleave)

<!-- fetched: 2026-09-14 -->

Hãy đi sâu hơn vào chi tiết về các sự kiện xảy ra khi chuột di chuyển giữa các phần tử.

## [Sự kiện mouseover/mouseout, relatedTarget](#events-mouseover-mouseout-relatedtarget)

Sự kiện `mouseover` xảy ra khi con trỏ chuột di chuyển vào một phần tử, và `mouseout` – khi nó rời khỏi.

![](/article/mousemove-mouseover-mouseout-mouseenter-mouseleave/mouseover-mouseout.svg)

Các sự kiện này đặc biệt vì chúng có thuộc tính `relatedTarget`. Thuộc tính này bổ sung cho `target`. Khi chuột rời khỏi một phần tử để sang phần tử khác, một trong hai trở thành `target`, và phần tử kia – `relatedTarget`.

Đối với `mouseover`:

- `event.target` – là phần tử mà chuột di chuyển vào.
- `event.relatedTarget` – là phần tử mà chuột rời khỏi (`relatedTarget` → `target`).

Đối với `mouseout` thì ngược lại:

- `event.target` – là phần tử mà chuột đã rời.
- `event.relatedTarget` – là phần tử mới bên dưới con trỏ, mà chuột đã rời khỏi (`target` → `relatedTarget`).

Trong ví dụ dưới đây, mỗi khuôn mặt và các đặc điểm của nó là các phần tử riêng biệt. Khi bạn di chuyển chuột, bạn có thể thấy các sự kiện mouse trong vùng văn bản.

Mỗi sự kiện có thông tin về cả `target` và `relatedTarget`:

Kết quả

script.js

style.css

index.html

```
container.onmouseover = container.onmouseout = handler;

function handler(event) {

  function str(el) {
    if (!el) return "null"
    return el.className || el.tagName;
  }

  log.value += event.type + ':  ' +
    'target=' + str(event.target) +
    ',  relatedTarget=' + str(event.relatedTarget) + "\n";
  log.scrollTop = log.scrollHeight;

  if (event.type == 'mouseover') {
    event.target.style.background = 'pink'
  }
  if (event.type == 'mouseout') {
    event.target.style.background = ''
  }
}
```

```
body,
html {
  margin: 0;
  padding: 0;
}

#container {
  border: 1px solid brown;
  padding: 10px;
  width: 330px;
  margin-bottom: 5px;
  box-sizing: border-box;
}

#log {
  height: 120px;
  width: 350px;
  display: block;
  box-sizing: border-box;
}

[class^="smiley-"] {
  display: inline-block;
  width: 70px;
  height: 70px;
  border-radius: 50%;
  margin-right: 20px;
}

.semicolon-green {
  background: #a9db7a;
  border: 5px solid #92c563;
  position: relative;
}

.semicolon-green .left-eye {
  width: 18%;
  height: 18%;
  background: #84b458;
  position: relative;
  top: 29%;
  left: 22%;
  border-radius: 50%;
  float: left;
}

.semicolon-green .right-eye {
  width: 18%;
  height: 18%;
  border-radius: 50%;
  position: relative;
  background: #84b458;
  top: 29%;
  right: 22%;
  float: right;
}

.semicolon-green .smile {
  position: absolute;
  top: 67%;
  left: 16.5%;
  width: 70%;
  height: 20%;
  overflow: hidden;
}

.semicolon-green .smile:after,
.semicolon-green .smile:before {
  content: "";
  position: absolute;
  top: -50%;
  left: 0%;
  border-radius: 50%;
  background: #84b458;
  height: 100%;
  width: 97%;
}

.semicolon-green .smile:after {
  background: #84b458;
  height: 80%;
  top: -40%;
  left: 0%;
}

.semicolon-yellow {
  background: #eed16a;
  border: 5px solid #dbae51;
  position: relative;
}

.semicolon-yellow .left-eye {
  width: 18%;
  height: 18%;
  background: #dba652;
  position: relative;
  top: 29%;
  left: 22%;
  border-radius: 50%;
  float: left;
}

.semicolon-yellow .right-eye {
  width: 18%;
  height: 18%;
  border-radius: 50%;
  position: relative;
  background: #dba652;
  top: 29%;
  right: 22%;
  float: right;
}

.semicolon-yellow .smile {
  position: absolute;
  top: 67%;
  left: 19%;
  width: 65%;
  height: 14%;
  background: #dba652;
  overflow: hidden;
  border-radius: 8px;
}

.semicolon-red {
  background: #ee9295;
  border: 5px solid #e27378;
  position: relative;
}

.semicolon-red .left-eye {
  width: 18%;
  height: 18%;
  background: #d96065;
  position: relative;
  top: 29%;
  left: 22%;
  border-radius: 50%;
  float: left;
}

.semicolon-red .right-eye {
  width: 18%;
  height: 18%;
  border-radius: 50%;
  position: relative;
  background: #d96065;
  top: 29%;
  right: 22%;
  float: right;
}

.semicolon-red .smile {
  position: absolute;
  top: 57%;
  left: 16.5%;
  width: 70%;
  height: 20%;
  overflow: hidden;
}

.semicolon-red .smile:after,
.semicolon-red .smile:before {
  content: "";
  position: absolute;
  top: 50%;
  left: 0%;
  border-radius: 50%;
  background: #d96065;
  height: 100%;
  width: 97%;
}

.semicolon-red .smile:after {
  background: #d96065;
  height: 80%;
  top: 60%;
  left: 0%;
}
```

```
<!DOCTYPE HTML>
<html>

<head>
  <meta charset="utf-8">
  <link rel="stylesheet" href="style.css">
</head>

<body>

  <div id="container">
    <div class="semicicolon-green">
      <div class="left-eye"></div>
      <div class="right-eye"></div>
      <div class="smile"></div>
    </div>

    <div class="semicicolon-yellow">
      <div class="left-eye"></div>
      <div class="right-eye"></div>
      <div class="smile"></div>
    </div>

    <div class="semicicolon-red">
      <div class="left-eye"></div>
      <div class="right-eye"></div>
      <div class="smile"></div>
    </div>
  </div>

  <textarea id="log">Events will show up here!
</textarea>

  <script src="script.js"></script>

</body>
</html>
```

`relatedTarget` có thể là `null`

Thuộc tính `relatedTarget` có thể là `null`.

Điều đó bình thường và chỉ có nghĩa là chuột không đến từ một phần tử khác, mà từ ngoài cửa sổ. Hoặc là nó đã rời khỏi cửa sổ.

Chúng ta nên nhớ khả năng này khi sử dụng `event.relatedTarget` trong mã của chúng ta. Nếu chúng ta truy cập `event.relatedTarget.tagName`, thì sẽ có lỗi.

## [Bỏ qua các phần tử](#skipping-elements)

Sự kiện `mousemove` kích hoạt khi chuột di chuyển. Nhưng điều đó không có nghĩa là mọi pixel đều dẫn đến một sự kiện.

Trình duyệt kiểm tra vị trí chuột theo thời gian. Và nếu nó nhận thấy thay đổi thì kích hoạt các sự kiện.

Điều đó có nghĩa là nếu người truy cập di chuyển chuột rất nhanh, thì một số phần tử DOM có thể bị bỏ qua:

![](/article/mousemove-mouseover-mouseout-mouseenter-mouseleave/mouseover-mouseout-over-elems.svg)

Nếu chuột di chuyển rất nhanh từ phần tử `#FROM` đến `#TO` như vẽ trên, thì các phần tử `<div>` trung gian (hoặc một số trong số chúng) có thể bị bỏ qua. Sự kiện `mouseout` có thể kích hoạt trên `#FROM` và sau đó ngay lập tức là `mouseover` trên `#TO`.

Điều đó tốt cho hiệu suất, vì có thể có nhiều phần tử trung gian. Chúng ta thực sự không muốn xử lý vào và ra của mỗi phần tử.

Mặt khác, chúng ta nên nhớ rằng con trỏ chuột không "ghé thăm" tất cả các phần tử dọc theo đường đi. Nó có thể "nhảy".

Đặc biệt, có trường hợp con trỏ nhảy thẳng vào giữa trang từ ngoài cửa sổ. Trong trường hợp đó `relatedTarget` là `null`, vì nó đến từ "khắp đâu":

![](/article/mousemove-mouseover-mouseout-mouseenter-mouseleave/mouseover-mouseout-from-outside.svg)

Bạn có thể kiểm tra điều này "trực tiếp" tại teststand bên dưới.

HTML của nó có hai phần tử lồng nhau: `<div id="child">` nằm trong `<div id="parent">`. Nếu bạn di chuyển chuột nhanh qua chúng, thì có thể chỉ có child div kích hoạt sự kiện, hoặc có thể là parent, hoặc có thể không có sự kiện nào.

Also move the pointer into the child `div`, and then move it out quickly down through the parent one. If the movement is fast enough, then the parent element is ignored. The mouse will cross the parent element without noticing it.

Result

script.js

style.css

index.html

```
let parent = document.getElementById('parent');
parent.onmouseover = parent.onmouseout = parent.onmousemove = handler;

function handler(event) {
  let type = event.type;
  while (type.length < 11) type += ' ';

  log(type + " target=" + event.target.id)
  return false;
}

function clearText() {
  text.value = "";
  lastMessage = "";
}

let lastMessageTime = 0;
let lastMessage = "";
let repeatCounter = 1;

function log(message) {
  if (lastMessageTime == 0) lastMessageTime = new Date();

  let time = new Date();

  if (time - lastMessageTime > 500) {
    message = '------------------------------\n' + message;
  }

  if (message === lastMessage) {
    repeatCounter++;
    if (repeatCounter == 2) {
      text.value = text.value.trim() + ' x 2\n';
    } else {
      text.value = text.value.slice(0, text.value.lastIndexOf('x') + 1) + repeatCounter + "\n";
    }

  } else {
    repeatCounter = 1;
    text.value += message + "\n";
  }

  text.scrollTop = text.scrollHeight;

  lastMessageTime = time;
  lastMessage = message;
}
```

```
#parent {
  background: #99C0C3;
  width: 160px;
  height: 120px;
  position: relative;
}

#child {
  background: #FFDE99;
  width: 50%;
  height: 50%;
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
}

textarea {
  height: 140px;
  width: 300px;
  display: block;
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

  <div id="parent">parent
    <div id="child">child</div>
  </div>
  <textarea id="text"></textarea>
  <input onclick="clearText()" value="Clear" type="button">

  <script src="script.js"></script>

</body>

</html>
```

Nếu `mouseover` kích hoạt, thì phải có `mouseout`

Trong trường hợp di chuyển chuột nhanh, các phần tử trung gian có thể bị bỏ qua, nhưng một điều chúng ta biết chắc chắn: nếu con trỏ "chính thức" đã vào một phần tử (sự kiện `mouseover` được tạo), thì khi rời khỏi nó, chúng ta luôn nhận được `mouseout`.

## [Mouseout khi di chuyển sang phần tử con](#mouseout-when-leaving-for-a-child)

Một tính năng quan trọng của `mouseout` – nó kích hoạt khi con trỏ di chuyển từ một phần tử sang phần tử con của nó, ví dụ từ `#parent` đến `#child` trong HTML sau:

```
<div id="parent">
  <div id="child">...</div>
</div>
```

Nếu chúng ta đang ở `#parent` và sau đó di chuyển con trỏ sâu hơn vào `#child`, chúng ta sẽ nhận được `mouseout` trên `#parent`!

![](/article/mousemove-mouseover-mouseout-mouseenter-mouseleave/mouseover-to-child.svg)

Điều đó có vẻ lạ, nhưng có thể giải thích dễ dàng.

**Theo logic của trình duyệt, con trỏ chuột chỉ có thể nằm trên *một* phần tử tại một thời điểm – phần tử lồng sâu nhất và xếp lớp cao nhất theo z-index.**

Vì vậy, nếu nó di chuyển sang một phần tử khác (ngay cả phần tử con), thì nó đã rời khỏi phần tử trước đó.

Xin lưu ý một chi tiết quan trọng khác về xử lý sự kiện.

Sự kiện `mouseover` trên phần tử con sẽ bubbling lên. Vì vậy, nếu `#parent` có handler `mouseover`, nó sẽ kích hoạt:

![](/article/mousemove-mouseover-mouseout-mouseenter-mouseleave/mouseover-bubble-nested.svg)

Bạn có thể thấy rất rõ trong ví dụ dưới đây: `<div id="child">` nằm trong `<div id="parent">`. Có các handler `mouseover/out` trên phần tử `#parent` để hiển thị chi tiết sự kiện.

Nếu bạn di chuyển chuột từ `#parent` đến `#child`, bạn sẽ thấy hai sự kiện trên `#parent`:

1. `mouseout [target: parent]` (rời khỏi parent), sau đó
2. `mouseover [target: child]` (đến child, bubbled).

Result

script.js

style.css

index.html

```
function mouselog(event) {
  let d = new Date();
  text.value += `${d.getHours()}:${d.getMinutes()}:${d.getSeconds()} | ${event.type} [target: ${event.target.id}]\n`.replace(/(:|^)(\d\D)/, '$10$2');
  text.scrollTop = text.scrollHeight;
}
```

```
#parent {
  background: #99C0C3;
  width: 160px;
  height: 120px;
  position: relative;
}

#child {
  background: #FFDE99;
  width: 50%;
  height: 50%;
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
}

textarea {
  height: 140px;
  width: 300px;
  display: block;
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

  <div id="parent" onmouseover="mouselog(event)" onmouseout="mouselog(event)">parent
    <div id="child">child</div>
  </div>

  <textarea id="text"></textarea>
  <input type="button" onclick="text.value=''" value="Clear">

  <script src="script.js"></script>

</body>

</html>
```

Như hiển thị, khi con trỏ di chuyển từ phần tử `#parent` đến `#child`, hai handler kích hoạt trên phần tử parent: `mouseout` và `mouseover`:

```
parent.onmouseout = function(event) {
  /* event.target: parent element */
};
parent.onmouseover = function(event) {
  /* event.target: child element (bubbled) */
};
```

**Nếu chúng ta không kiểm tra `event.target` bên trong các handler, thì có vẻ như con trỏ chuột đã rời khỏi phần tử `#parent`, và sau đó ngay lập tức quay lại.**

Nhưng không phải vậy! Con trỏ vẫn nằm trên parent, nó chỉ di chuyển sâu hơn vào phần tử child.

Nếu có một số hành động khi rời khỏi phần tử parent, ví dụ animation chạy trong `parent.onmouseout`, chúng ta thường không muốn nó khi con trỏ chỉ di chuyển sâu hơn vào `#parent`.

Để tránh điều đó, chúng ta có thể kiểm tra `relatedTarget` trong handler và, nếu chuột vẫn nằm trong phần tử, thì bỏ qua sự kiện đó.

Hoặc chúng ta có thể sử dụng các sự kiện khác: `mouseenter` và `mouseleave`, mà chúng ta sẽ đề cập đến ngay bây giờ, vì chúng không có các vấn đề như vậy.

## [Sự kiện mouseenter và mouseleave](#events-mouseenter-and-mouseleave)

Các sự kiện `mouseenter/mouseleave` giống như `mouseover/mouseout`. Chúng kích hoạt khi con trỏ chuột đi vào/ra khỏi phần tử.

Nhưng có hai sự khác biệt quan trọng:

1. Các chuyển đổi bên trong phần tử, đến/từ phần tử con, không được tính.
2. Các sự kiện `mouseenter/mouseleave` không bubbling.

Các sự kiện này cực kỳ đơn giản.

Khi con trỏ đi vào một phần tử – `mouseenter` kích hoạt. Vị trí chính xác của con trỏ bên trong phần tử hoặc các phần tử con của nó không quan trọng.

Khi con trỏ rời khỏi một phần tử – `mouseleave` kích hoạt.

Ví dụ này tương tự như ví dụ trên, nhưng bây giờ phần tử trên cùng có `mouseenter/mouseleave` thay vì `mouseover/mouseout`.

Như bạn có thể thấy, các sự kiện được tạo duy nhất là những sự kiện liên quan đến việc di chuyển con trỏ vào và ra khỏi phần tử trên cùng. Không có gì xảy ra khi con trỏ di chuyển vào child và quay lại. Các chuyển đổi giữa các phần tử con bị bỏ qua

Result

script.js

style.css

index.html

```
function mouselog(event) {
  let d = new Date();
  text.value += `${d.getHours()}:${d.getMinutes()}:${d.getSeconds()} | ${event.type} [target: ${event.target.id}]\n`.replace(/(:|^)(\d\D)/, '$10$2');
  text.scrollTop = text.scrollHeight;
}
```

```
#parent {
  background: #99C0C3;
  width: 160px;
  height: 120px;
  position: relative;
}

#child {
  background: #FFDE99;
  width: 50%;
  height: 50%;
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
}

textarea {
  height: 140px;
  width: 300px;
  display: block;
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

  <div id="parent" onmouseenter="mouselog(event)" onmouseleave="mouselog(event)">parent
    <div id="child">child</div>
  </div>

  <textarea id="text"></textarea>
  <input type="button" onclick="text.value=''" value="Clear">

  <script src="script.js"></script>

</body>

</html>
```

## [Event delegation](#event-delegation)

Các sự kiện `mouseenter/leave` rất đơn giản và dễ sử dụng. Nhưng chúng không bubbling. Vì vậy chúng ta không thể sử dụng event delegation với chúng.

Hãy tưởng tượng chúng ta muốn xử lý việc chuột di chuyển vào/ra khỏi các ô bảng. Và có hàng trăm ô.

Giải pháp tự nhiên sẽ là – đặt handler trên `<table>` và xử lý sự kiện ở đó. Nhưng `mouseenter/leave` không bubbling. Vì vậy, nếu sự kiện đó xảy ra trên `<td>`, thì chỉ có handler trên `<td>` đó mới có thể bắt được nó.

Các handler cho `mouseenter/leave` trên `<table>` chỉ kích hoạt khi con trỏ đi vào/ra khỏi toàn bộ table. Không thể lấy bất kỳ thông tin nào về các chuyển đổi bên trong nó.

Vì vậy, hãy sử dụng `mouseover/mouseout`.

Hãy bắt đầu với các handler đơn giản để làm nổi bật phần tử bên dưới chuột:

```
// let's highlight an element under the pointer
table.onmouseover = function(event) {
  let target = event.target;
  target.style.background = 'pink';
};

table.onmouseout = function(event) {
  let target = event.target;
  target.style.background = '';
};
```

Đây là chúng hoạt động. Khi chuột di chuyển qua các phần tử của bảng này, phần tử hiện tại được làm nổi bật:

Result

script.js

style.css

index.html

```
table.onmouseover = function(event) {
  let target = event.target;
  target.style.background = 'pink';

  text.value += `over -> ${target.tagName}\n`;
  text.scrollTop = text.scrollHeight;
};

table.onmouseout = function(event) {
  let target = event.target;
  target.style.background = '';

  text.value += `out <- ${target.tagName}\n`;
  text.scrollTop = text.scrollHeight;
};
```

```
#text {
  display: block;
  height: 100px;
  width: 456px;
}

#table th {
  text-align: center;
  font-weight: bold;
}

#table td {
  width: 150px;
  white-space: nowrap;
  text-align: center;
  vertical-align: bottom;
  padding-top: 5px;
  padding-bottom: 12px;
  cursor: pointer;
}

#table .nw {
  background: #999;
}

#table .n {
  background: #03f;
  color: #fff;
}

#table .ne {
  background: #ff6;
}

#table .w {
  background: #ff0;
}

#table .c {
  background: #60c;
  color: #fff;
}

#table .e {
  background: #09f;
  color: #fff;
}

#table .sw {
  background: #963;
  color: #fff;
}

#table .s {
  background: #f60;
  color: #fff;
}

#table .se {
  background: #0c3;
  color: #fff;
}

#table .highlight {
  background: red;
}
```

```
<!DOCTYPE HTML>
<html>

<head>
  <meta charset="utf-8">
  <link rel="stylesheet" href="style.css">
</head>

<body>

  <table id="table">
    <tr>
      <th colspan="3"><em>Bagua</em> Chart: Direction, Element, Color, Meaning</th>
    </tr>
    <tr>
      <td class="nw"><strong>Northwest</strong>
        <br>Metal
        <br>Silver
        <br>Elders
      </td>
      <td class="n"><strong>North</strong>
        <br>Water
        <br>Blue
        <br>Change
      </td>
      <td class="ne"><strong>Northeast</strong>
        <br>Earth
        <br>Yellow
        <br>Direction
      </td>
    </tr>
    <tr>
      <td class="w"><strong>West</strong>
        <br>Metal
        <br>Gold
        <br>Youth
      </td>
      <td class="c"><strong>Center</strong>
        <br>All
        <br>Purple
        <br>Harmony
      </td>
      <td class="e"><strong>East</strong>
        <br>Wood
        <br>Blue
        <br>Future
      </td>
    </tr>
    <tr>
      <td class="sw"><strong>Southwest</strong>
        <br>Earth
        <br>Brown
        <br>Tranquility
      </td>
      <td class="s"><strong>South</strong>
        <br>Fire
        <br>Orange
        <br>Fame
      </td>
      <td class="se"><strong>Southeast</strong>
        <br>Wood
        <br>Green
        <br>Romance
      </td>
    </tr>

  </table>

  <textarea id="text"></textarea>

  <input type="button" onclick="text.value=''" value="Clear">

  <script src="script.js"></script>

</body>
</html>
```

Trong trường hợp của chúng ta, chúng ta muốn xử lý các chuyển đổi giữa các ô bảng `<td>`: vào một ô và rời khỏi nó. Các chuyển đổi khác, chẳng hạn như bên trong ô hoặc bên ngoài bất kỳ ô nào, không hứng thú với chúng ta. Hãy lọc chúng ra.

Đây là những gì chúng ta có thể làm:

- Ghi nhớ `<td>` đang được làm nổi bật hiện tại trong một biến, gọi nó là `currentElem`.
- Trên `mouseover` – bỏ qua sự kiện nếu chúng ta vẫn đang ở trong `<td>` hiện tại.
- Trên `mouseout` – bỏ qua nếu chúng ta không rời khỏi `<td>` hiện tại.

Đây là ví dụ về mãaccount tất cả các tình huống có thể:

```
// <td> under the mouse right now (if any)
let currentElem = null;

table.onmouseover = function(event) {
  // before entering a new element, the mouse always leaves the previous one
  // if currentElem is set, we didn't leave the previous <td>,
  // that's a mouseover inside it, ignore the event
  if (currentElem) return;

  let target = event.target.closest('td');

  // we moved not into a <td> - ignore
  if (!target) return;

  // moved into <td>, but outside of our table (possible in case of nested tables)
  // ignore
  if (!table.contains(target)) return;

  // hooray! we entered a new <td>
  currentElem = target;
  onEnter(currentElem);
};

table.onmouseout = function(event) {
  // if we're outside of any <td> now, then ignore the event
  // that's probably a move inside the table, but out of <td>,
  // e.g. from <tr> to another <tr>
  if (!currentElem) return;

  // we're leaving the element – where to? Maybe to a descendant?
  let relatedTarget = event.relatedTarget;

  while (relatedTarget) {
    // go up the parent chain and check – if we're still inside currentElem
    // then that's an internal transition – ignore it
    if (relatedTarget == currentElem) return;

    relatedTarget = relatedTarget.parentNode;
  }

  // we left the <td>. really.
  onLeave(currentElem);
  currentElem = null;
};

// any functions to handle entering/leaving an element
function onEnter(elem) {
  elem.style.background = 'pink';

  // show that in textarea
  text.value += `over -> ${currentElem.tagName}.${currentElem.className}\n`;
  text.scrollTop = 1e6;
}

function onLeave(elem) {
  elem.style.background = '';

  // show that in textarea
  text.value += `out <- ${elem.tagName}.${elem.className}\n`;
  text.scrollTop = 1e6;
}
```

Một lần nữa, các tính năng quan trọng là:

1. Nó sử dụng event delegation để xử lý việc vào/ra của bất kỳ `<td>` nào trong bảng. Vì vậy, nó dựa vào `mouseover/out` thay vì `mouseenter/leave` không bubbling và do đó không cho phép delegation.
2. Các sự kiện thêm, chẳng hạn như di chuyển giữa các phần tử con của `<td>`, bị lọc ra, vì vậy `onEnter/Leave` chỉ chạy nếu con trỏ rời hoặc vào `<td>` như một tổng thể.

Đây là ví dụ đầy đủ với tất cả chi tiết:

Result

script.js

style.css

index.html

```
// <td> under the mouse right now (if any)
let currentElem = null;

table.onmouseover = function(event) {
  // before entering a new element, the mouse always leaves the previous one
  // if currentElem is set, we didn't leave the previous <td>,
  // that's a mouseover inside it, ignore the event
  if (currentElem) return;

  let target = event.target.closest('td');

  // we moved not into a <td> - ignore
  if (!target) return;

  // moved into <td>, but outside of our table (possible in case of nested tables)
  // ignore
  if (!table.contains(target)) return;

  // hooray! we entered a new <td>
  currentElem = target;
  onEnter(currentElem);
};

table.onmouseout = function(event) {
  // if we're outside of any <td> now, then ignore the event
  // that's probably a move inside the table, but out of <td>,
  // e.g. from <tr> to another <tr>
  if (!currentElem) return;

  // we're leaving the element – where to? Maybe to a descendant?
  let relatedTarget = event.relatedTarget;

  while (relatedTarget) {
    // go up the parent chain and check – if we're still inside currentElem
    // then that's an internal transition – ignore it
    if (relatedTarget == currentElem) return;

    relatedTarget = relatedTarget.parentNode;
  }

  // we left the <td>. really.
  onLeave(currentElem);
  currentElem = null;
};

// any functions to handle entering/leaving an element
function onEnter(elem) {
  elem.style.background = 'pink';

  // show that in textarea
  text.value += `over -> ${currentElem.tagName}.${currentElem.className}\n`;
  text.scrollTop = 1e6;
}

function onLeave(elem) {
  elem.style.background = '';

  // show that in textarea
  text.value += `out <- ${elem.tagName}.${elem.className}\n`;
  text.scrollTop = 1e6;
}
```

```
#text {
  display: block;
  height: 100px;
  width: 456px;
}

#table th {
  text-align: center;
  font-weight: bold;
}

#table td {
  width: 150px;
  white-space: nowrap;
  text-align: center;
  vertical-align: bottom;
  padding-top: 5px;
  padding-bottom: 12px;
  cursor: pointer;
}

#table .nw {
  background: #999;
}

#table .n {
  background: #03f;
  color: #fff;
}

#table .ne {
  background: #ff6;
}

#table .w {
  background: #ff0;
}

#table .c {
  background: #60c;
  color: #fff;
}

#table .e {
  background: #09f;
  color: #fff;
}

#table .sw {
  background: #963;
  color: #fff;
}

#table .s {
  background: #f60;
  color: #fff;
}

#table .se {
  background: #0c3;
  color: #fff;
}

#table .highlight {
  background: red;
}
```

```
<!DOCTYPE HTML>
<html>

<head>
  <meta charset="utf-8">
  <link rel="stylesheet" href="style.css">
</head>

<body>

  <table id="table">
    <tr>
      <th colspan="3"><em>Bagua</em> Chart: Direction, Element, Color, Meaning</th>
    </tr>
    <tr>
      <td class="nw"><strong>Northwest</strong>
        <br>Metal
        <br>Silver
        <br>Elders
      </td>
      <td class="n"><strong>North</strong>
        <br>Water
        <br>Blue
        <br>Change
      </td>
      <td class="ne"><strong>Northeast</strong>
        <br>Earth
        <br>Yellow
        <br>Direction
      </td>
    </tr>
    <tr>
      <td class="w"><strong>West</strong>
        <br>Metal
        <br>Gold
        <br>Youth
      </td>
      <td class="c"><strong>Center</strong>
        <br>All
        <br>Purple
        <br>Harmony
      </td>
      <td class="e"><strong>East</strong>
        <br>Wood
        <br>Blue
        <br>Future
      </td>
    </tr>
    <tr>
      <td class="sw"><strong>Southwest</strong>
        <br>Earth
        <br>Brown
        <br>Tranquility
      </td>
      <td class="s"><strong>South</strong>
        <br>Fire
        <br>Orange
        <br>Fame
      </td>
      <td class="se"><strong>Southeast</strong>
        <br>Wood
        <br>Green
        <br>Romance
      </td>
    </tr>

  </table>

  <textarea id="text"></textarea>

  <input type="button" onclick="text.value=''" value="Clear">

  <script src="script.js"></script>

</body>
</html>
```

Hãy thử di chuyển con trỏ vào và ra khỏi các ô bảng và bên trong chúng. Nhanh hay chậm – không quan trọng. Chỉ có `<td>` như một tổng thể được làm nổi bật, khác với ví dụ trước.

## [Tổng kết](#summary)

Chúng ta đã đề cập đến các sự kiện `mouseover`, `mouseout`, `mousemove`, `mouseenter` và `mouseleave`.

Những điều sau đây đáng chú ý:

- Di chuyển chuột nhanh có thể bỏ qua các phần tử trung gian.
- Các sự kiện `mouseover/out` và `mouseenter/leave` có một thuộc tính bổ sung: `relatedTarget`. Đó là phần tử mà chúng ta đang đến/đi từ, bổ sung cho `target`.

Các sự kiện `mouseover/out` kích hoạt ngay cả khi chúng ta di chuyển từ phần tử cha sang phần tử con. Trình duyệt giả định rằng chuột chỉ có thể nằm trên một phần tử tại một thời điểm – phần tử sâu nhất.

Các sự kiện `mouseenter/leave` khác ở khía cạnh này: chúng chỉ kích hoạt khi chuột đi vào và ra khỏi phần tử như một tổng thể. Ngoài ra chúng không bubbling.

---

---

## Bài tập

## [Bài tập](#tasks)

### [Hành vi tooltip được cải thiện](#improved-tooltip-behavior)

mức độ khó: 5

Viết JavaScript hiển thị tooltip над phần tử có thuộc tính `data-tooltip`. Giá trị của thuộc tính này sẽ trở thành văn bản tooltip.

Đó là giống như bài tập [Tooltip behavior](/task/behavior-tooltip), nhưng ở đây các phần tử được chú thích có thể lồng nhau. Tooltip sâu nhất được hiển thị.

Chỉ một tooltip có thể hiển thị cùng một lúc.

Ví dụ:

```
<div data-tooltip="Here – is the house interior" id="house">
  <div data-tooltip="Here – is the roof" id="roof"></div>
  ...
  <a href="https://en.wikipedia.org/wiki/The_Three_Little_Pigs" data-tooltip="Read on…">Hover over me</a>
</div>
```

Kết quả trong iframe:

[Mở sandbox cho bài tập.](https://plnkr.co/edit/rduudfMDvEHrY0BP?p=preview)

lời giải

[Mở lời giải trong sandbox.](https://plnkr.co/edit/A8t6hDOvb1EEpPHj?p=preview)

### [Tooltip "thông minh"](#smart-tooltip)

mức độ khó: 5

Viết một hàm hiển thị tooltip над phần tử chỉ nếu người truy cập di chuyển chuột *đến nó*, chứ không phải *qua nó*.

Nói cách khác, nếu người truy cập di chuyển chuột đến phần tử và dừng lại ở đó – hiển thị tooltip. Và nếu họ chỉ di chuyển chuột qua, thì không cần, ai muốn nhấp nháy extra?

Về mặt kỹ thuật, chúng ta có thể đo tốc độ chuột над phần tử, và nếu nó chậm thì chúng ta giả định rằng nó đến "above the element" và hiển thị tooltip, nếu nó nhanh – thì chúng ta bỏ qua.

Tạo một đối tượng `new HoverIntent(options)` universal cho nó.

Các `options` của nó:

- `elem` – phần tử để theo dõi.
- `over` – một hàm để gọi nếu chuột đến phần tử: tức là, nó di chuyển chậm hoặc dừng lại trên nó.
- `out` – một hàm để gọi khi chuột rời khỏi phần tử (nếu `over` đã được gọi).

Một ví dụ về việc sử dụng đối tượng như vậy cho tooltip:

```
// a sample tooltip
let tooltip = document.createElement('div');
tooltip.className = "tooltip";
tooltip.innerHTML = "Tooltip";

// the object will track mouse and call over/out
new HoverIntent({
  elem,
  over() {
    tooltip.style.left = elem.getBoundingClientRect().left + 'px';
    tooltip.style.top = elem.getBoundingClientRect().bottom + 5 + 'px';
    document.body.append(tooltip);
  },
  out() {
    tooltip.remove();
  }
});
```

Bản demo:

Nếu bạn di chuyển chuột над "đồng hồ" nhanh thì không có gì xảy ra, và nếu bạn làm chậm hoặc dừng lại, thì sẽ có tooltip.

Xin lưu ý: tooltip không "nhấp nháy" khi con trỏ di chuyển giữa các subelement của đồng hồ.

[Mở sandbox với tests.](https://plnkr.co/edit/iPiQ7lM0he7izHD1?p=preview)

lời giải

Thuật toán trông đơn giản:

1. Đặt các handler `onmouseover/out` над phần tử. Cũng có thể sử dụng `onmouseenter/leave` ở đây, nhưng chúng ít universal hơn, không hoạt động nếu chúng ta giới thiệu delegation.
2. Khi con trỏ chuột đã vào phần tử, bắt đầu đo tốc độ на `mousemove`.
3. Nếu tốc độ chậm, thì chạy `over`.
4. Khi chúng ta đang rời khỏi phần tử, và `over` đã được thực thi, chạy `out`.

Nhưng làm thế nào để đo tốc độ?

Ý tưởng đầu tiên có thể là: chạy một hàm mỗi `100ms` và đo khoảng cách giữa tọa độ trước đó và mới. Nếu nó nhỏ, thì tốc độ nhỏ.

Rất tiếc, không có cách nào để lấy "tọa độ chuột hiện tại" trong JavaScript. Không có hàm như `getCurrentMouseCoordinates()`.

Cách duy nhất để lấy tọa độ là nghe các sự kiện chuột, như `mousemove`, và lấy tọa độ từ đối tượng sự kiện.

Vì vậy, hãy đặt handler на `mousemove` để theo dõi tọa độ và ghi nhớ chúng. Sau đó so sánh chúng, một lần mỗi `100ms`.

P.S. Xin lưu ý: các solution tests sử dụng `dispatchEvent` để xem liệu tooltip có hoạt động đúng không.

[Mở solution với tests trong sandbox.](https://plnkr.co/edit/VSPiMWMWJTQvXXsN?p=preview)
