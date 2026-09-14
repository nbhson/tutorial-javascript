# Animation CSS

> Source: [https://javascript.info/css-animations](https://javascript.info/css-animations)

<!-- fetched: 2026-09-14 -->

CSS animation cho phép thực hiện các animation đơn giản mà hoàn toàn không cần JavaScript.

JavaScript có thể được dùng để điều khiển CSS animation và làm chúng tốt hơn, với rất ít mã.

## [CSS transitions](#css-transition)

Ý tưởng của CSS transitions rất đơn giản. Chúng ta mô tả một thuộc tính và cách thay đổi của nó nên được animate. Khi thuộc tính thay đổi, trình duyệt vẽ animation.

Nghĩa là, tất cả những gì chúng ta cần là thay đổi thuộc tính, và sự chuyển tiếp mượt mà sẽ được trình duyệt thực hiện.

Ví dụ, CSS bên dưới animate thay đổi của `background-color` trong 3 giây:

```
.animated {
  transition-property: background-color;
  transition-duration: 3s;
}
```

Giờ nếu một element có class `.animated`, mọi thay đổi của `background-color` sẽ được animate trong 3 giây.

Nhấp vào nút bên dưới để animate nền:

```
<button id="color">Click me</button>

<style>
  #color {
    transition-property: background-color;
    transition-duration: 3s;
  }
</style>

<script>
  color.onclick = function() {
    this.style.backgroundColor = 'red';
  };
</script>
```

Có 4 thuộc tính để mô tả CSS transitions:

- `transition-property`
- `transition-duration`
- `transition-timing-function`
- `transition-delay`

Chúng ta sẽ xem xét chúng ngay sau đây, bây giờ hãy lưu ý rằng thuộc tính chung `transition` cho phép khai báo chúng cùng nhau theo thứ tự: `property duration timing-function delay`, cũng như animate nhiều thuộc tính cùng lúc.

Ví dụ, nút này animate cả `color` và `font-size`:

```
<button id="growing">Click me</button>

<style>
#growing {
  transition: font-size 3s, color 2s;
}
</style>

<script>
growing.onclick = function() {
  this.style.fontSize = '36px';
  this.style.color = 'red';
};
</script>
```

Bây giờ, hãy xem xét các thuộc tính animation một bằng một.

## [transition-property](#transition-property)

Trong `transition-property`, chúng ta viết danh sách các thuộc tính cần animate, ví dụ: `left`, `margin-left`, `height`, `color`. Hoặc chúng ta có thể viết `all`, nghĩa là "animate tất cả các thuộc tính".

Lưu ý rằng, có những thuộc tính không thể animate được. Tuy nhiên, [hầu hết các thuộc tính thường dùng đều có thể animate](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_animated_properties).

## [transition-duration](#transition-duration)

Trong `transition-duration` chúng ta có thể chỉ định animation nên kéo dài bao lâu. Thời gian phải ở [định dạng thời gian CSS](https://www.w3.org/TR/css3-values/#time): bằng giây `s` hoặc mili-giây `ms`.

## [transition-delay](#transition-delay)

Trong `transition-delay` chúng ta có thể chỉ định độ trễ *trước* animation. Ví dụ, nếu `transition-delay` là `1s` và `transition-duration` là `2s`, thì animation bắt đầu sau 1 giây kể từ khi thuộc tính thay đổi và tổng thời lượng sẽ là 2 giây.

Các giá trị âm cũng có thể. Khi đó animation hiển thị ngay lập tức, nhưng điểm khởi động của animation sẽ nằm sau giá trị cho trước (thời gian). Ví dụ, nếu `transition-delay` là `-1s` và `transition-duration` là `2s`, thì animation bắt đầu từ giữa quá trình và tổng thời lượng sẽ là 1 giây.

Ở đây animation dịch chuyển các chữ số từ `0` đến `9` bằng thuộc tính CSS `translate`:

Result

script.js

style.css

index.html

```
stripe.onclick = function() {
  stripe.classList.add('animate');
};
```

```
#digit {
  width: .5em;
  overflow: hidden;
  font: 32px monospace;
  cursor: pointer;
}

#stripe {
  display: inline-block
}

#stripe.animate {
  transform: translate(-90%);
  transition-property: transform;
  transition-duration: 9s;
  transition-timing-function: linear;
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

  Click below to animate:

  <div id="digit"><div id="stripe">0123456789</div></div>

  <script src="script.js"></script>
</body>

</html>
```

Thuộc tính `transform` được animate như sau:

```
#stripe.animate {
  transform: translate(-90%);
  transition-property: transform;
  transition-duration: 9s;
}
```

Trong ví dụ trên JavaScript thêm class `.animate` vào element – và animation bắt đầu:

```
stripe.classList.add('animate');
```

Chúng ta cũng có thể bắt đầu từ giữa transition, từ một số chính xác, ví dụ: tương ứng với giây hiện tại, bằng cách dùng `transition-delay` âm.

Ở đây nếu bạn nhấp vào chữ số – nó bắt đầu animation từ giây hiện tại:

Result

script.js

style.css

index.html

```
stripe.onclick = function() {
  let sec = new Date().getSeconds() % 10;
  stripe.style.transitionDelay = '-' + sec + 's';
  stripe.classList.add('animate');
};
```

```
#digit {
  width: .5em;
  overflow: hidden;
  font: 32px monospace;
  cursor: pointer;
}

#stripe {
  display: inline-block
}

#stripe.animate {
  transform: translate(-90%);
  transition-property: transform;
  transition-duration: 9s;
  transition-timing-function: linear;
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

  Click below to animate:
  <div id="digit"><div id="stripe">0123456789</div></div>

  <script src="script.js"></script>
</body>
</html>
```

JavaScript làm điều đó với thêm một dòng:

```
stripe.onclick = function() {
  let sec = new Date().getSeconds() % 10;
  // for instance, -3s here starts the animation from the 3rd second
  stripe.style.transitionDelay = '-' + sec + 's';
  stripe.classList.add('animate');
};
```

## [transition-timing-function](#transition-timing-function)

Timing function mô tả quá trình animation được phân bố dọc theo timeline của nó như thế nào. Nó sẽ bắt đầu chậm rồi đi nhanh, hay ngược lại.

Ban đầu, nó có vẻ là thuộc tính phức tạp nhất. Nhưng nó sẽ trở nên rất đơn giản nếu chúng ta dành một chút thời gian cho nó.

Thuộc tính đó nhận hai loại giá trị: một đường cong Bézier hoặc các bước (steps). Hãy bắt đầu với đường cong, vì nó được dùng thường hơn.

### [Bezier curve](#bezier-curve)

Timing function có thể được đặt là một [đường cong Bézier](/bezier-curve) với 4 control points thỏa mãn các điều kiện:

1. Control point đầu tiên: `(0,0)`.
2. Control point cuối: `(1,1)`.
3. Với các điểm trung gian, các giá trị của `x` phải nằm trong khoảng `0..1`, `y` có thể là bất kỳ.

Cú pháp cho một đường cong Bézier trong CSS: `cubic-bezier(x2, y2, x3, y3)`. Ở đây chúng ta chỉ cần chỉ định control point thứ 2 và thứ 3, vì điểm thứ nhất được cố định là `(0,0)` và điểm thứ tư là `(1,1)`.

Timing function mô tả quá trình animation diễn ra nhanh như thế nào.

- Trục `x` là thời gian: `0` – bắt đầu, `1` – kết thúc của `transition-duration`.
- Trục `y` chỉ định mức hoàn thành của quá trình: `0` – giá trị khởi đầu của thuộc tính, `1` – giá trị cuối cùng.

Biến thể đơn giản nhất là khi animation diễn ra đều đặn, với tốc độ tuyến tính như nhau. Điều đó có thể được chỉ định bằng đường cong `cubic-bezier(0, 0, 1, 1)`.

Dưới đây là cách đường cong đó trông như thế nào:

![](/article/css-animations/bezier-linear.svg)

…Như chúng ta có thể thấy, đó chỉ là một đường thẳng. Khi thời gian (`x`) trôi qua, mức hoàn thành (`y`) của animation đều đặn đi từ `0` đến `1`.

Tàu trong ví dụ bên dưới đi từ trái sang phải với tốc độ không đổi (nhấp vào nó):

Result

style.css

index.html

```
.train {
  position: relative;
  cursor: pointer;
  width: 177px;
  height: 160px;
  left: 0;
  transition: left 5s cubic-bezier(0, 0, 1, 1);
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

  <img class="train" src="https://js.cx/clipart/train.gif" onclick="this.style.left='450px'">

</body>

</html>
```

CSS `transition` dựa trên đường cong đó:

```
.train {
  left: 0;
  transition: left 5s cubic-bezier(0, 0, 1, 1);
  /* click on a train sets left to 450px, thus triggering the animation */
}
```

…Và chúng ta có thể cho tàu chạy chậm dần như thế nào?

Chúng ta có thể dùng một đường cong Bézier khác: `cubic-bezier(0.0, 0.5, 0.5 ,1.0)`.

Đồ thị:

![](/article/css-animations/train-curve.svg)

Như chúng ta có thể thấy, quá trình bắt đầu nhanh: đường cong vọt lên cao, rồi chậm dần dần.

Dưới đây là timing function trong thực tế (nhấp vào tàu):

Result

style.css

index.html

```
.train {
  position: relative;
  cursor: pointer;
  width: 177px;
  height: 160px;
  left: 0px;
  transition: left 5s cubic-bezier(0.0, 0.5, 0.5, 1.0);
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

  <img class="train" src="https://js.cx/clipart/train.gif" onclick="this.style.left='450px'">

</body>

</html>
```

CSS:

```
.train {
  left: 0;
  transition: left 5s cubic-bezier(0, .5, .5, 1);
  /* click on a train sets left to 450px, thus triggering the animation */
}
```

Có một vài đường cong có sẵn: `linear`, `ease`, `ease-in`, `ease-out` và `ease-in-out`.

`linear` là viết tắt của `cubic-bezier(0, 0, 1, 1)` – một đường thẳng, mà chúng ta đã mô tả ở trên.

Các tên khác là viết tắt của các `cubic-bezier` sau:

| `ease`\* | `ease-in` | `ease-out` | `ease-in-out` |
| --- | --- | --- | --- |
| `(0.25, 0.1, 0.25, 1.0)` | `(0.42, 0, 1.0, 1.0)` | `(0, 0, 0.58, 1.0)` | `(0.42, 0, 0.58, 1.0)` |
|  |  |  |  |

`*` – mặc định, nếu không có timing function, `ease` được sử dụng.

Vì vậy chúng ta có thể dùng `ease-out` cho tàu chạy chậm dần:

```
.train {
  left: 0;
  transition: left 5s ease-out;
  /* same as transition: left 5s cubic-bezier(0, .5, .5, 1); */
}
```

Nhưng nó trông hơi khác.

**Một đường cong Bézier có thể làm animation vượt quá phạm vi của nó.**

Các control points trên đường cong có thể có bất kỳ tọa độ `y` nào: thậm chí là âm hoặc rất lớn. Khi đó đường cong Bézier cũng sẽ vươn rất thấp hoặc cao, khiến animation đi vượt ra ngoài phạm vi bình thường của nó.

Trong ví dụ bên dưới mã animation là:

```
.train {
  left: 100px;
  transition: left 5s cubic-bezier(.5, -1, .5, 2);
  /* click on a train sets left to 450px */
}
```

Thuộc tính `left` nên animate từ `100px` đến `400px`.

Nhưng nếu bạn nhấp vào tàu, bạn sẽ thấy rằng:

- Trước tiên, tàu đi *lùi*: `left` trở nên nhỏ hơn `100px`.
- Sau đó nó tiến về trước, xa hơn một chút so với `400px`.
- Rồi lại lùi về – đến `400px`.

Result

style.css

index.html

```
.train {
  position: relative;
  cursor: pointer;
  width: 177px;
  height: 160px;
  left: 100px;
  transition: left 5s cubic-bezier(.5, -1, .5, 2);
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

  <img class="train" src="https://js.cx/clipart/train.gif" onclick="this.style.left='400px'">

</body>

</html>
```

Tại sao điều đó xảy ra thì khá rõ ràng nếu chúng ta nhìn vào đồ thị của đường cong Bézier cho trước:

![](/article/css-animations/bezier-train-over.svg)

Chúng ta đã di chuyển tọa độ `y` của điểm thứ 2 xuống dưới không, và với điểm thứ 3 chúng ta đặt nó vượt quá `1`, vì vậy đường cong đi ra ngoài "góc phần tư" thông thường. Giá trị `y` nằm ngoài "phạm vi chuẩn" `0..1`.

Như chúng ta biết, `y` đo "mức hoàn thành của quá trình animation". Giá trị `y = 0` tương ứng với giá trị khởi đầu của thuộc tính và `y = 1` – giá trị kết thúc. Vì vậy các giá trị `y<0` đẩy thuộc tính vượt quá giá trị `left` khởi đầu và `y>1` – vượt quá `left` cuối cùng.

Đó chắc chắn là một biến thể "mềm". Nếu chúng ta đặt các giá trị `y` như `-99` và `99` thì tàu sẽ nhảy ra ngoài phạm vi nhiều hơn.

Nhưng làm thế nào để tạo một đường cong Bézier cho một nhiệm vụ cụ thể? Có rất nhiều công cụ.

- Ví dụ, chúng ta có thể làm điều đó trên trang <https://cubic-bezier.com>.
- Công cụ phát triển của trình duyệt cũng có hỗ trợ đặc biệt cho các đường cong Bézier trong CSS:
  1. Mở công cụ phát triển với `F12` (Mac: `Cmd+Opt+I`).
  2. Chọn tab `Elements`, rồi chú ý vào panel con `Styles` ở phía bên phải.
  3. Các thuộc tính CSS có từ `cubic-bezier` sẽ có một icon trước từ đó.
  4. Nhấp vào icon này để chỉnh sửa đường cong.

### [Steps](#steps)

Timing function `steps(number of steps[, start/end])` cho phép chia một transition thành nhiều bước.

Hãy xem điều đó trong một ví dụ với các chữ số.

Đây là một danh sách các chữ số, không có animation, chỉ như một nguồn:

Result

style.css

index.html

```
#digit {
  border: 1px solid red;
  width: 1.2em;
}

#stripe {
  display: inline-block;
  font: 32px monospace;
}
```

```
<!DOCTYPE html>
<html>

<head>
  <meta charset="utf-8">
  <link rel="stylesheet" href="style.css">
</head>

<body>

  <div id="digit"><div id="stripe">0123456789</div></div>

</body>
</html>
```

Trong HTML, dải chữ số được bao trong một `<div id="digits">` có chiều dài cố định:

```
<div id="digit">
  <div id="stripe">0123456789</div>
</div>
```

Div `#digit` có bề rộng cố định và viền, vì vậy nó trông như một ô cửa sổ màu đỏ.

Chúng ta sẽ tạo một đồng hồ: các chữ số sẽ xuất hiện lần lượt, theo cách rời rạc.

Để đạt được điều đó, chúng ta sẽ ẩn `#stripe` ngoài `#digit` bằng cách sử dụng `overflow: hidden`, rồi dịch chuyển `#stripe` sang trái từng bước một.

Sẽ có 9 bước, một bước dịch chuyển cho mỗi chữ số:

```
#stripe.animate  {
  transform: translate(-90%);
  transition: transform 9s steps(9, start);
}
```

Tham số đầu tiên của `steps(9, start)` là số bước. Transform sẽ được chia thành 9 phần (mỗi phần 10%). Khoảng thời gian cũng tự động được chia thành 9 phần, vì vậy `transition: 9s` cho chúng ta 9 giây cho toàn bộ animation – 1 giây cho mỗi chữ số.

Tham số thứ hai là một trong hai từ: `start` hoặc `end`.

`start` nghĩa là ở đầu animation, chúng ta cần thực hiện bước đầu tiên ngay lập tức.

Trong thực tế:

Result

style.css

index.html

```
#digit {
  width: .5em;
  overflow: hidden;
  font: 32px monospace;
  cursor: pointer;
}

#stripe {
  display: inline-block
}

#stripe.animate {
  transform: translate(-90%);
  transition-property: transform;
  transition-duration: 9s;
  transition-timing-function: steps(9, start);
}
```

```
<!DOCTYPE html>
<html>

<head>
  <meta charset="utf-8">
  <link rel="stylesheet" href="style.css">
</head>

<body>

  Click below to animate:

  <div id="digit"><div id="stripe">0123456789</div></div>

  <script>
    digit.onclick = function() {
      stripe.classList.add('animate');
    }
  </script>

</body>

</html>
```

Một nhấp vào chữ số sẽ thay đổi nó thành `1` (bước đầu tiên) ngay lập tức, và sau đó thay đổi vào đầu giây tiếp theo.

Quá trình diễn ra như sau:

- `0s` – `-10%` (thay đổi đầu tiên vào đầu giây thứ 1, ngay lập tức)
- `1s` – `-20%`
- …
- `8s` – `-90%`
- (giây cuối cùng hiển thị giá trị cuối cùng).

Ở đây, thay đổi đầu tiên diễn ra ngay lập tức vì `start` trong `steps`.

Giá trị thay thế `end` sẽ nghĩa là thay đổi nên được áp dụng không phải ở đầu, mà ở cuối mỗi giây.

Vậy quá trình với `steps(9, end)` sẽ diễn ra như sau:

- `0s` – `0` (trong giây đầu tiên không có gì thay đổi)
- `1s` – `-10%` (thay đổi đầu tiên ở cuối giây thứ 1)
- `2s` – `-20%`
- …
- `9s` – `-90%`

Dưới đây là `steps(9, end)` trong thực tế (chú ý khoảng dừng trước khi chữ số đầu tiên thay đổi):

Result

style.css

index.html

```
#digit {
  width: .5em;
  overflow: hidden;
  font: 32px monospace;
  cursor: pointer;
}

#stripe {
  display: inline-block
}

#stripe.animate {
  transform: translate(-90%);
  transition-property: transform;
  transition-duration: 9s;
  transition-timing-function: steps(9, end);
}
```

```
<!DOCTYPE html>
<html>

<head>
  <meta charset="utf-8">
  <link rel="stylesheet" href="style.css">
</head>

<body>

  Click below to animate:

  <div id="digit"><div id="stripe">0123456789</div></div>

  <script>
    digit.onclick = function() {
      stripe.classList.add('animate');
    }
  </script>

</body>

</html>
```

Cũng có một vài viết tắt có sẵn cho `steps(...)`:

- `step-start` – giống hệt `steps(1, start)`. Nghĩa là, animation bắt đầu ngay lập tức và thực hiện 1 bước. Vì vậy nó bắt đầu và kết thúc ngay lập tức, như thể không có animation.
- `step-end` – giống `steps(1, end)`: thực hiện animation trong một bước duy nhất ở cuối `transition-duration`.

Các giá trị này ít được dùng, vì chúng không đại diện cho một animation thực sự, mà là một thay đổi một bước. Chúng ta đề cập ở đây cho đầy đủ.

## [Sự kiện: “transitionend”](#event-transitionend)

Khi CSS animation kết thúc, sự kiện `transitionend` kích hoạt.

Nó được dùng rộng rãi để thực hiện một hành động sau khi animation hoàn tất. Chúng ta cũng có thể nối các animation lại với nhau.

Ví dụ, con thuyền trong ví dụ bên dưới bắt đầu chạy đi và về khi được nhấp, mỗi lần xa hơn về phía bên phải:

Animation được khởi tạo bằng hàm `go` chạy lại mỗi khi transition hoàn tất, và đảo ngược hướng:

```
boat.onclick = function() {
  //...
  let times = 1;

  function go() {
    if (times % 2) {
      // sail to the right
      boat.classList.remove('back');
      boat.style.marginLeft = 100 * times + 200 + 'px';
    } else {
      // sail to the left
      boat.classList.add('back');
      boat.style.marginLeft = 100 * times - 200 + 'px';
    }

  }

  go();

  boat.addEventListener('transitionend', function() {
    times++;
    go();
  });
};
```

Đối tượng sự kiện cho `transitionend` có một vài thuộc tính cụ thể:

`event.propertyName`
:   Thuộc tính đã hoàn thành animation. Hữu ích nếu chúng ta animate nhiều thuộc tính cùng lúc.

`event.elapsedTime`
:   Thời gian (tính bằng giây) mà animation đã mất, không tính `transition-delay`.

## [Keyframes](#keyframes)

Chúng ta có thể kết hợp nhiều animation đơn giản lại bằng quy tắc CSS `@keyframes`.

Nó chỉ định "tên" của animation và các quy tắc – animate cái gì, khi nào và ở đâu. Sau đó dùng thuộc tính `animation`, chúng ta có thể gắn animation vào element và chỉ định các tham số bổ sung cho nó.

Đây là một ví dụ kèm giải thích:

```
<div class="progress"></div>

<style>
  @keyframes go-left-right {        /* give it a name: "go-left-right" */
    from { left: 0px; }             /* animate from left: 0px */
    to { left: calc(100% - 50px); } /* animate to left: 100%-50px */
  }

  .progress {
    animation: go-left-right 3s infinite alternate;
    /* apply the animation "go-left-right" to the element
       duration 3 seconds
       number of times: infinite
       alternate direction every time
     */

    position: relative;
    border: 2px solid green;
    width: 50px;
    height: 20px;
    background: lime;
  }
</style>
```

Có rất nhiều bài viết về `@keyframes` và một [đặc tả chi tiết](https://drafts.csswg.org/css-animations/).

Có thể bạn không cần `@keyframes` thường xuyên, trừ khi mọi thứ trên trang web của bạn đều chuyển động liên tục.

## [Hiệu năng](#performance)

Hầu hết các thuộc tính CSS có thể animate, vì hầu hết chúng là giá trị số. Ví dụ, `width`, `color`, `font-size` đều là số. Khi animate chúng, trình duyệt dần dần thay đổi những con số này theo từng khung hình, tạo ra hiệu ứng mượt mà.

Tuy nhiên, không phải animation nào cũng trông mượt như bạn muốn, vì các thuộc tính CSS khác nhau có chi phí thay đổi khác nhau.

Chi tiết kỹ thuật hơn, khi có thay đổi style, trình duyệt đi qua 3 bước để render ngoại hình mới:

1. **Layout**: tính lại hình học và vị trí của mỗi element, rồi
2. **Paint**: tính lại cách mọi thứ nên trông như thế nào tại các vị trí của chúng, bao gồm cả nền, màu sắc,
3. **Composite**: render kết quả cuối cùng thành pixel trên màn hình, áp dụng CSS transform nếu có.

Trong một CSS animation, quá trình này lặp lại mỗi khung hình. Tuy nhiên, các thuộc tính CSS không bao giờ ảnh hưởng đến hình học hoặc vị trí, chẳng hạn như `color`, có thể bỏ qua bước Layout. Nếu `color` thay đổi, trình duyệt không tính bất kỳ hình học mới nào, nó chuyển sang Paint → Composite. Và có một vài thuộc tính chuyển thẳng đến Composite. Bạn có thể tìm thấy danh sách dài hơn các thuộc tính CSS và các giai đoạn chúng kích hoạt tại <https://csstriggers.com>.

Các phép tính có thể mất thời gian, đặc biệt trên các trang có nhiều element và layout phức tạp. Và các độ trễ thực sự có thể thấy được trên hầu hết các thiết bị, dẫn đến các animation "lấp", kém mượt mà.

Animation của các thuộc tính bỏ qua bước Layout thì nhanh hơn. Tốt hơn nữa nếu bước Paint cũng được bỏ qua.

Thuộc tính `transform` là một lựa chọn tuyệt vời, vì:

- CSS transform ảnh hưởng đến toàn bộ box của element đích (xoay, lật, co giãn, dịch chuyển nó).
- CSS transform không bao giờ ảnh hưởng đến các element lân cận.

…Vì vậy trình duyệt áp dụng `transform` "trên" các tính toán Layout và Paint hiện có, ở giai đoạn Composite.

Nói cách khác, trình duyệt tính Layout (kích thước, vị trí), vẽ chúng với màu sắc, nền, v.v. ở giai đoạn Paint, rồi áp dụng `transform` lên các box element cần thiết.

Các thay đổi (animation) của thuộc tính `transform` không bao giờ kích hoạt các bước Layout và Paint. Hơn thế nữa, trình duyệt tận dụng bộ tăng tốc đồ họa (một chip đặc biệt trên CPU hoặc card đồ họa) cho CSS transform, giúp chúng rất hiệu quả.

May mắn thay, thuộc tính `transform` rất mạnh mẽ. Bằng cách dùng `transform` trên một element, bạn có thể xoay và lật nó, co giãn và thu nhỏ nó, di chuyển nó khắp nơi, và [nhiều hơn nữa](https://developer.mozilla.org/docs/Web/CSS/transform#syntax). Vì vậy thay vì các thuộc tính `left/margin-left` chúng ta có thể dùng `transform: translateX(…)`, dùng `transform: scale` để tăng kích thước element, v.v.

Thuộc tính `opacity` cũng không bao giờ kích hoạt Layout (cũng bỏ qua Paint trong Mozilla Gecko). Chúng ta có thể dùng nó cho hiệu ứng show/hide hoặc fade-in/fade-out.

Kết hợp `transform` với `opacity` thường có thể đáp ứng hầu hết nhu cầu của chúng ta, cung cấp các animation mượt mà, đẹp mắt.

Ví dụ, ở đây nhấp vào element `#boat` sẽ thêm class với `transform: translateX(300px)` và `opacity: 0`, khiến nó di chuyển `300px` về bên phải và biến mất:

```
<img src="https://js.cx/clipart/boat.png" id="boat">

<style>
#boat {
  cursor: pointer;
  transition: transform 2s ease-in-out, opacity 2s ease-in-out;
}

.move {
  transform: translateX(300px);
  opacity: 0;
}
</style>
<script>
  boat.onclick = () => boat.classList.add('move');
</script>
```

Dưới đây là một ví dụ phức tạp hơn, với `@keyframes`:

```
<h2 onclick="this.classList.toggle('animated')">click me to start / stop</h2>
<style>
  .animated {
    animation: hello-goodbye 1.8s infinite;
    width: fit-content;
  }
  @keyframes hello-goodbye {
    0% {
      transform: translateY(-60px) rotateX(0.7turn);
      opacity: 0;
    }
    50% {
      transform: none;
      opacity: 1;
    }
    100% {
      transform: translateX(230px) rotateZ(90deg) scale(0.5);
      opacity: 0;
    }
  }
</style>
```

## [Tóm tắt](#summary)

CSS animation cho phép thay đổi (trơn hoặc theo từng bước) một hoặc nhiều thuộc tính CSS một cách động.

Chúng rất tốt cho hầu hết các nhiệm vụ animation. Chúng ta cũng có thể dùng JavaScript cho animation, chương tiếp theo dành cho điều đó.

Hạn chế của CSS animation so với JavaScript animation:

Ưu điểm

- Những thứ đơn giản được thực hiện một cách đơn giản.
- Nhanh và nhẹ cho CPU.

Nhược điểm

- JavaScript animation linh hoạt hơn. Chúng có thể thực hiện bất kỳ logic animation nào, như hiệu ứng "nổ" của một element.
- Không chỉ thay đổi thuộc tính. Chúng ta có thể tạo các element mới trong JavaScript như một phần của animation.

Trong các ví dụ đầu chương này, chúng ta animate `font-size`, `left`, `width`, `height`, v.v. Trong các dự án thực tế, chúng ta nên dùng `transform: scale()` và `transform: translate()` để có hiệu năng tốt hơn.

Hầu hết các animation có thể được thực hiện bằng CSS như đã mô tả trong chương này. Và sự kiện `transitionend` cho phép JavaScript được chạy sau animation, vì vậy nó tích hợp tốt với mã.

Nhưng ở chương tiếp theo chúng ta sẽ thực hiện một số JavaScript animation để xử lý các trường hợp phức tạp hơn.

---

---

## Bài tập

## [Bài tập](#tasks)

### [Animate máy bay (CSS)](#animate-a-plane-css)

importance: 5

Hiển thị animation như trong hình bên dưới (nhấp vào máy bay):

- Hình ảnh phóng to khi nhấp từ `40x24px` đến `400x240px` (lớn gấp 10 lần).
- Animation mất 3 giây.
- Khi kết thúc in ra: "Done!".
- Trong quá trình animation, có thể có thêm các lần nhấp vào máy bay. Chúng không nên "làm hỏng" gì.

[Mở sandbox cho bài tập.](https://plnkr.co/edit/KHFIZQde023GpAh4?p=preview)

solution

CSS animate cả `width` và `height`:

```
/* original class */

#flyjet {
  transition: all 3s;
}

/* JS adds .growing */
#flyjet.growing {
  width: 400px;
  height: 240px;
}
```

Vui lòng lưu ý rằng `transitionend` kích hoạt hai lần – một lần cho mỗi thuộc tính. Vì vậy nếu chúng ta không thực hiện thêm kiểm tra, thông điệp sẽ hiển thị 2 lần.

[Mở lời giải trong sandbox.](https://plnkr.co/edit/dJPTPqcl2XV55DPu?p=preview)

### [Animate máy bay bay (CSS)](#animate-the-flying-plane-css)

importance: 5

Sửa đổi lời giải của bài tập trước [Animate máy bay (CSS)](/task/animate-logo-css) để máy bay phóng to vượt quá kích thước gốc 400x240px (nhảy ra ngoài), rồi quay về kích thước đó.

Nó nên trông như sau (nhấp vào máy bay):

Lấy lời giải của bài tập trước làm nguồn.

solution

Chúng ta cần chọn đúng đường cong Bézier cho animation đó. Nó nên có `y>1` ở đâu đó để máy bay "nhảy ra ngoài".

Ví dụ, chúng ta có thể đặt cả hai control points với `y>1`, như: `cubic-bezier(0.25, 1.5, 0.75, 1.5)`.

Đồ thị:

![](/task/animate-logo-bezier-css/bezier-up.svg)

[Mở lời giải trong sandbox.](https://plnkr.co/edit/Bg8o7SFJIh2bcZNs?p=preview)

### [Vòng tròn animate](#animated-circle)

importance: 5

Tạo một hàm `showCircle(cx, cy, radius)` hiển thị một vòng tròn lớn dần có animation.

- `cx,cy` là tọa độ của tâm vòng tròn so với cửa sổ,
- `radius` là bán kính của vòng tròn.

Nhấp vào nút bên dưới để xem nó nên trông như thế nào:

Tài liệu nguồn có một ví dụ vòng tròn với các style đúng, vì vậy nhiệm vụ chính xác là thực hiện animation đúng.

[Mở sandbox cho bài tập.](https://plnkr.co/edit/OzkTI5FREB9INJ34?p=preview)

solution

[Mở lời giải trong sandbox.](https://plnkr.co/edit/GdNDBSIAExU66SrG?p=preview)

### [Vòng tròn animate với callback](#animated-circle-with-callback)

Trong bài tập [Vòng tròn animate](/task/animate-circle) một vòng tròn lớn dần có animation được hiển thị.

Giờ giả sử chúng ta cần không chỉ một vòng tròn, mà còn hiển thị một thông điệp bên trong nó. Thông điệp nên xuất hiện *sau* khi animation hoàn tất (vòng tròn đã lớn hoàn toàn), nếu không nó sẽ trông xấu.

Trong lời giải của bài tập, hàm `showCircle(cx, cy, radius)` vẽ vòng tròn, nhưng không cho cách nào để theo dõi khi nó sẵn sàng.

Thêm đối số callback: `showCircle(cx, cy, radius, callback)` để được gọi khi animation hoàn tất. `callback` nên nhận vòng tròn `<div>` làm đối số.

Đây là ví dụ:

```
showCircle(150, 150, 100, div => {
  div.classList.add('message-ball');
  div.append("Hello, world!");
});
```

Demo:

Lấy lời giải của bài tập [Vòng tròn animate](/task/animate-circle) làm nền tảng.

solution

[Mở lời giải trong sandbox.](https://plnkr.co/edit/sJbTVivu38I4jIY2?p=preview)
