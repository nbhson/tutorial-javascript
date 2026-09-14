# Animation JavaScript

> Source: [https://javascript.info/js-animation](https://javascript.info/js-animation)

<!-- fetched: 2026-09-14 -->

JavaScript animation có thể xử lý những thứ mà CSS không làm tốt.

Ví dụ, di chuyển dọc theo một đường phức tạp, với timing function khác đường cong Bézier, hoặc animation trên canvas.

## [Sử dụng setInterval](#using-setinterval)

Animation có thể được triển khai như một chuỗi các khung hình – thường là những thay đổi nhỏ đối với các thuộc tính HTML/CSS.

Ví dụ, thay đổi `style.left` từ `0px` đến `100px` sẽ di chuyển element. Và nếu chúng ta tăng nó bằng `setInterval`, thay đổi `2px` với một độ trễ nhỏ, khoảng 50 lần mỗi giây, thì nó trông mượt mà. Đó cũng là nguyên lý trong điện ảnh: 24 khung hình mỗi giây là đủ để trông mượt mà.

Mã giả có thể trông như thế này:

```
let timer = setInterval(function() {
  if (animation complete) clearInterval(timer);
  else increase style.left by 2px
}, 20); // change by 2px every 20ms, about 50 frames per second
```

Ví dụ hoàn chỉnh hơn của animation:

```
let start = Date.now(); // remember start time

let timer = setInterval(function() {
  // how much time passed from the start?
  let timePassed = Date.now() - start;

  if (timePassed >= 2000) {
    clearInterval(timer); // finish the animation after 2 seconds
    return;
  }

  // draw the animation at the moment timePassed
  draw(timePassed);

}, 20);

// as timePassed goes from 0 to 2000
// left gets values from 0px to 400px
function draw(timePassed) {
  train.style.left = timePassed / 5 + 'px';
}
```

Nhấp để xem demo:

Result

index.html

```
<!DOCTYPE HTML>
<html>

<head>
  <style>
    #train {
      position: relative;
      cursor: pointer;
    }
  </style>
</head>

<body>

  <img id="train" src="https://js.cx/clipart/train.gif">

  <script>
    train.onclick = function() {
      let start = Date.now();

      let timer = setInterval(function() {
        let timePassed = Date.now() - start;

        train.style.left = timePassed / 5 + 'px';

        if (timePassed > 2000) clearInterval(timer);

      }, 20);
    }
  </script>

</body>

</html>
```

## [Sử dụng requestAnimationFrame](#using-requestanimationframe)

Hãy tưởng tượng chúng ta có nhiều animation chạy đồng thời.

Nếu chúng ta chạy chúng riêng lẻ, thì mặc dù mỗi cái có `setInterval(..., 20)`, trình duyệt sẽ phải vẽ lại thường xuyên hơn nhiều so với mỗi `20ms`.

Điều đó là vì chúng có thời điểm bắt đầu khác nhau, vì vậy "mỗi 20ms" khác nhau giữa các animation. Các khoảng thời gian không được căn chỉnh. Vì vậy sẽ có nhiều lần chạy độc lập trong `20ms`.

Nói cách khác, cái này:

```
setInterval(function() {
  animate1();
  animate2();
  animate3();
}, 20)
```

…Nhẹ hơn so với ba lời gọi độc lập:

```
setInterval(animate1, 20); // independent animations
setInterval(animate2, 20); // in different places of the script
setInterval(animate3, 20);
```

Nhiều lần vẽ lại độc lập này nên được nhóm lại, để việc vẽ lại dễ dàng hơn cho trình duyệt và do đó ít tốn CPU hơn và trông mượt hơn.

Có một điều nữa cần ghi nhớ. Đôi khi CPU quá tải, hoặc có những lý do khác để vẽ lại ít thường xuyên hơn (như khi tab trình duyệt bị ẩn), vì vậy chúng ta thực sự không nên chạy mỗi `20ms`.

Nhưng làm thế nào để biết điều đó trong JavaScript? Có một đặc tả [Animation timing](https://www.w3.org/TR/animation-timing/) cung cấp hàm `requestAnimationFrame`. Nó giải quyết tất cả những vấn đề này và cả hơn thế.

Cú pháp:

```
let requestId = requestAnimationFrame(callback)
```

Điều đó lên lịch chạy hàm `callback` vào thời điểm gần nhất mà trình duyệt muốn thực hiện animation.

Nếu chúng ta thực hiện các thay đổi element trong `callback`, chúng sẽ được nhóm lại với các `requestAnimationFrame` callbacks khác và với các CSS animation. Vì vậy sẽ chỉ có một lần tính toán hình học và vẽ lại thay vì nhiều lần.

Giá trị trả về `requestId` có thể dùng để hủy lời gọi:

```
// cancel the scheduled execution of callback
cancelAnimationFrame(requestId);
```

`callback` nhận một đối số – thời gian trôi qua kể từ đầu tải trang tính bằng mili-giây. Thời gian này cũng có thể lấy bằng cách gọi [performance.now()](https://developer.mozilla.org/en-US/docs/Web/API/Performance/now).

Thường thì `callback` được chạy rất nhanh, trừ khi CPU quá tải, hoặc pin laptop sắp hết, hoặc có lý do khác.

Mã bên dưới hiển thị thời gian giữa 10 lần chạy đầu tiên của `requestAnimationFrame`. Thường thì nó là 10-20ms:

```
<script>
  let prev = performance.now();
  let times = 0;

  requestAnimationFrame(function measure(time) {
    document.body.insertAdjacentHTML("beforeEnd", Math.floor(time - prev) + " ");
    prev = time;

    if (times++ < 10) requestAnimationFrame(measure);
  })
</script>
```

## [Animation có cấu trúc](#structured-animation)

Giờ chúng ta có thể tạo một hàm animation phổ quát hơn dựa trên `requestAnimationFrame`:

```
function animate({timing, draw, duration}) {

  let start = performance.now();

  requestAnimationFrame(function animate(time) {
    // timeFraction goes from 0 to 1
    let timeFraction = (time - start) / duration;
    if (timeFraction > 1) timeFraction = 1;

    // calculate the current animation state
    let progress = timing(timeFraction)

    draw(progress); // draw it

    if (timeFraction < 1) {
      requestAnimationFrame(animate);
    }

  });
}
```

Hàm `animate` nhận 3 tham số mô tả bản chất của animation:

`duration`
:   Tổng thời gian của animation. Ví dụ: `1000`.

`timing(timeFraction)`
:   Timing function, giống thuộc tính CSS `transition-timing-function` nhận phần thời gian đã trôi qua (`0` ở đầu, `1` ở cuối) và trả về mức hoàn thành của animation (giống `y` trên đường cong Bézier).

    Ví dụ, một hàm tuyến tính nghĩa là animation diễn ra đều với cùng tốc độ:

    ```
    function linear(timeFraction) {
      return timeFraction;
    }
    ```

    Đồ thị của nó:
    ![](/article/js-animation/linear.svg)

    Giống hệt `transition-timing-function: linear`. Có nhiều biến thể thú vị hơn được hiển thị bên dưới.

`draw(progress)`
:   Hàm nhận trạng thái hoàn thành của animation và vẽ nó. Giá trị `progress=0` chỉ trạng thái bắt đầu của animation, và `progress=1` – trạng thái kết thúc.

    Đây là hàm thực sự vẽ ra animation.

    Nó có thể di chuyển element:

    ```
    function draw(progress) {
      train.style.left = progress + 'px';
    }
    ```

    …Hoặc làm bất kỳ điều gì khác, chúng ta có thể animate bất kỳ thứ gì, theo bất kỳ cách nào.

Hãy animate thuộc tính `width` của element từ `0` đến `100%` bằng hàm của chúng ta.

Nhấp vào element để xem demo:

Result

animate.js

index.html

```
function animate({duration, draw, timing}) {

  let start = performance.now();

  requestAnimationFrame(function animate(time) {
    let timeFraction = (time - start) / duration;
    if (timeFraction > 1) timeFraction = 1;

    let progress = timing(timeFraction)

    draw(progress);

    if (timeFraction < 1) {
      requestAnimationFrame(animate);
    }

  });
}
```

```
<!DOCTYPE HTML>
<html>

<head>
  <meta charset="utf-8">
  <style>
    progress {
      width: 5%;
    }
  </style>
  <script src="animate.js"></script>
</head>

<body>

  <progress id="elem"></progress>

  <script>
    elem.onclick = function() {
      animate({
        duration: 1000,
        timing: function(timeFraction) {
          return timeFraction;
        },
        draw: function(progress) {
          elem.style.width = progress * 100 + '%';
        }
      });
    };
  </script>

</body>

</html>
```

Mã cho nó:

```
animate({
  duration: 1000,
  timing(timeFraction) {
    return timeFraction;
  },
  draw(progress) {
    elem.style.width = progress * 100 + '%';
  }
});
```

Khác với CSS animation, chúng ta có thể tạo bất kỳ timing function nào và bất kỳ hàm vẽ nào ở đây. Timing function không bị giới hạn bởi đường cong Bézier. Và `draw` có thể vượt ra ngoài các thuộc tính, tạo các element mới như animation pháo hoa hoặc thứ gì đó.

## [Timing functions](#timing-functions)

Chúng ta đã thấy timing function tuyến tính đơn giản nhất ở trên.

Hãy xem thêm một số. Chúng ta sẽ thử các animation di chuyển với các timing function khác nhau để xem chúng hoạt động như thế nào.

### [Lũy thừa n](#power-of-n)

Nếu chúng ta muốn tăng tốc animation, chúng ta có thể dùng `progress` với lũy thừa `n`.

Ví dụ, đường cong parabolic:

```
function quad(timeFraction) {
  return Math.pow(timeFraction, 2)
}
```

Đồ thị:

![](/article/js-animation/quad.svg)

Xem trong thực tế (nhấp để kích hoạt):

…Hoặc đường cong bậc ba hoặc `n` lớn hơn. Tăng lũy thừa khiến nó tăng tốc nhanh hơn.

Đây là đồ thị cho `progress` với lũy thừa `5`:

![](/article/js-animation/quint.svg)

Trong thực tế:

### [Cung tròn](#the-arc)

Hàm:

```
function circ(timeFraction) {
  return 1 - Math.sin(Math.acos(timeFraction));
}
```

Đồ thị:

![](/article/js-animation/circ.svg)

### [Back: bắn cung](#back-bow-shooting)

Hàm này thực hiện "bắn cung". Trước tiên chúng ta "kéo dây cung", rồi "bắn".

Khác với các hàm trước, nó phụ thuộc vào một tham số bổ sung `x`, "hệ số đàn hồi". Khoảng cách "kéo dây cung" được xác định bởi nó.

Mã:

```
function back(x, timeFraction) {
  return Math.pow(timeFraction, 2) * ((x + 1) * timeFraction - x)
}
```

**Đồ thị cho `x = 1.5`:**

![](/article/js-animation/back.svg)

Để animate chúng ta dùng nó với một giá trị cụ thể của `x`. Ví dụ với `x = 1.5`:

### [Bounce](#bounce)

Hãy tưởng tượng chúng ta đang thả một quả bóng. Nó rơi xuống, rồi nảy lại vài lần rồi dừng.

Hàm `bounce` làm tương tự, nhưng theo thứ tự ngược: "nảy" bắt đầu ngay lập tức. Nó dùng một vài hệ số đặc biệt cho điều đó:

```
function bounce(timeFraction) {
  for (let a = 0, b = 1; 1; a += b, b /= 2) {
    if (timeFraction >= (7 - 4 * a) / 11) {
      return -Math.pow((11 - 6 * a - 11 * timeFraction) / 4, 2) + Math.pow(b, 2)
    }
  }
}
```

Trong thực tế:

### [Animation đàn hồi](#elastic-animation)

Một hàm "đàn hồi" khác nhận thêm tham số `x` cho "phạm vi ban đầu".

```
function elastic(x, timeFraction) {
  return Math.pow(2, 10 * (timeFraction - 1)) * Math.cos(20 * Math.PI * x / 3 * timeFraction)
}
```

**Đồ thị cho `x=1.5`:**
![](/article/js-animation/elastic.svg)

Trong thực tế với `x=1.5`:

## [Đảo ngược: ease*](#reversal-ease)

Vậy chúng ta có một bộ timing functions. Việc áp dụng trực tiếp của chúng được gọi là "easeIn".

Đôi khi chúng ta cần hiển thị animation theo thứ tự ngược lại. Điều đó được thực hiện bằng biến đổi "easeOut".

### [easeOut](#easeout)

Trong chế độ "easeOut", hàm `timing` được đặt trong một wrapper `timingEaseOut`:

```
timingEaseOut(timeFraction) = 1 - timing(1 - timeFraction)
```

Nói cách khác, chúng ta có một hàm "biến đổi" `makeEaseOut` nhận một timing function "thông thường" và trả về wrapper của nó:

```
// accepts a timing function, returns the transformed variant
function makeEaseOut(timing) {
  return function(timeFraction) {
    return 1 - timing(1 - timeFraction);
  }
}
```

Ví dụ, chúng ta có thể lấy hàm `bounce` được mô tả ở trên và áp dụng nó:

```
let bounceEaseOut = makeEaseOut(bounce);
```

Rồi bounce sẽ không nằm ở đầu, mà ở cuối của animation. Trông còn tốt hơn:

Result

style.css

index.html

```
#brick {
  width: 40px;
  height: 20px;
  background: #EE6B47;
  position: relative;
  cursor: pointer;
}

#path {
  outline: 1px solid #E8C48E;
  width: 540px;
  height: 20px;
}
```

```
<!DOCTYPE HTML>
<html>

<head>
  <meta charset="utf-8">
  <link rel="stylesheet" href="style.css">
  <script src="https://js.cx/libs/animate.js"></script>
</head>

<body>

  <div id="path">
    <div id="brick"></div>
  </div>

  <script>
    function makeEaseOut(timing) {
      return function(timeFraction) {
        return 1 - timing(1 - timeFraction);
      }
    }

    function bounce(timeFraction) {
      for (let a = 0, b = 1; 1; a += b, b /= 2) {
        if (timeFraction >= (7 - 4 * a) / 11) {
          return -Math.pow((11 - 6 * a - 11 * timeFraction) / 4, 2) + Math.pow(b, 2)
        }
      }
    }

    let bounceEaseOut = makeEaseOut(bounce);

    brick.onclick = function() {
      animate({
        duration: 3000,
        timing: bounceEaseOut,
        draw: function(progress) {
          brick.style.left = progress * 500 + 'px';
        }
      });
    };
  </script>

</body>

</html>
```

Ở đây chúng ta có thể thấy cách biến đổi thay đổi hành vi của hàm:

![](/article/js-animation/bounce-inout.svg)

Nếu có hiệu ứng animation ở đầu, như bounce – nó sẽ được hiển thị ở cuối.

Trong đồ thị ở trên, bounce thường có màu đỏ, và bounce easeOut có màu xanh dương.

- Bounce thường – object nảy ở phía dưới, rồi ở cuối nhảy vọt lên phía trên.
- Sau `easeOut` – nó trước tiên nhảy lên phía trên, rồi nảy ở đó.

### [easeInOut](#easeinout)

Chúng ta cũng có thể hiển thị hiệu ứng cả ở đầu và cuối của animation. Biến đổi được gọi là "easeInOut".

Với timing function cho trước, chúng ta tính trạng thái animation như sau:

```
if (timeFraction <= 0.5) { // first half of the animation
  return timing(2 * timeFraction) / 2;
} else { // second half of the animation
  return (2 - timing(2 * (1 - timeFraction))) / 2;
}
```

Mã wrapper:

```
function makeEaseInOut(timing) {
  return function(timeFraction) {
    if (timeFraction < .5)
      return timing(2 * timeFraction) / 2;
    else
      return (2 - timing(2 * (1 - timeFraction))) / 2;
  }
}

bounceEaseInOut = makeEaseInOut(bounce);
```

Trong thực tế, `bounceEaseInOut`:

Result

style.css

index.html

```
#brick {
  width: 40px;
  height: 20px;
  background: #EE6B47;
  position: relative;
  cursor: pointer;
}

#path {
  outline: 1px solid #E8C48E;
  width: 540px;
  height: 20px;
}
```

```
<!DOCTYPE HTML>
<html>

<head>
  <meta charset="utf-8">
  <link rel="stylesheet" href="style.css">
  <script src="https://js.cx/libs/animate.js"></script>
</head>

<body>

  <div id="path">
    <div id="brick"></div>
  </div>

  <script>
    function makeEaseInOut(timing) {
      return function(timeFraction) {
        if (timeFraction < .5)
          return timing(2 * timeFraction) / 2;
        else
          return (2 - timing(2 * (1 - timeFraction))) / 2;
      }
    }

    function bounce(timeFraction) {
      for (let a = 0, b = 1; 1; a += b, b /= 2) {
        if (timeFraction >= (7 - 4 * a) / 11) {
          return -Math.pow((11 - 6 * a - 11 * timeFraction) / 4, 2) + Math.pow(b, 2)
        }
      }
    }

    let bounceEaseInOut = makeEaseInOut(bounce);

    brick.onclick = function() {
      animate({
        duration: 3000,
        timing: bounceEaseInOut,
        draw: function(progress) {
          brick.style.left = progress * 500 + 'px';
        }
      });
    };
  </script>

</body>

</html>
```

Biến đổi "easeInOut" nối hai đồ thị thành một: `easeIn` (thường) cho nửa đầu của animation và `easeOut` (đảo ngược) – cho phần thứ hai.

Hiệu ứng rõ ràng khi so sánh các đồ thị của `easeIn`, `easeOut` và `easeInOut` của timing function `circ`:

![](/article/js-animation/circ-ease.svg)

- Màu đỏ là biến thể thường của `circ` (`easeIn`).
- Xanh lá – `easeOut`.
- Xanh dương – `easeInOut`.

Như chúng ta có thể thấy, đồ thị của nửa đầu animation là `easeIn` thu nhỏ, và nửa sau là `easeOut` thu nhỏ. Kết quả là, animation bắt đầu và kết thúc với cùng một hiệu ứng.

## ["draw" thú vị hơn](#more-interesting-draw)

Thay vì di chuyển element, chúng ta có thể làm những thứ khác. Tất cả những gì chúng ta cần là viết `draw` phù hợp.

Đây là ví dụ gõ chữ "nảy" có animation:

Result

style.css

index.html

```
textarea {
  display: block;
  border: 1px solid #BBB;
  color: #444;
  font-size: 110%;
}

button {
  margin-top: 10px;
}
```

```
<!DOCTYPE HTML>
<html>

<head>
  <meta charset="utf-8">
  <link rel="stylesheet" href="style.css">
  <script src="https://js.cx/libs/animate.js"></script>
</head>

<body>

  <textarea id="textExample" rows="5" cols="60">He took his vorpal sword in hand:
Long time the manxome foe he sought—
So rested he by the Tumtum tree,
And stood awhile in thought.
  </textarea>

  <button onclick="animateText(textExample)">Run the animated typing!</button>

  <script>
    function animateText(textArea) {
      let text = textArea.value;
      let to = text.length,
        from = 0;

      animate({
        duration: 5000,
        timing: bounce,
        draw: function(progress) {
          let result = (to - from) * progress + from;
          textArea.value = text.slice(0, Math.ceil(result))
        }
      });
    }

    function bounce(timeFraction) {
      for (let a = 0, b = 1; 1; a += b, b /= 2) {
        if (timeFraction >= (7 - 4 * a) / 11) {
          return -Math.pow((11 - 6 * a - 11 * timeFraction) / 4, 2) + Math.pow(b, 2)
        }
      }
    }
  </script>

</body>

</html>
```

## [Tóm tắt](#summary)

Đối với các animation mà CSS không xử lý tốt, hoặc những thứ cần kiểm soát chặt chẽ, JavaScript có thể giúp. JavaScript animation nên được triển khai bằng `requestAnimationFrame`. Phương thức tích hợp đó cho phép đặt một callback function để chạy khi trình duyệt chuẩn bị vẽ lại. Thường thì đó là rất nhanh, nhưng thời gian chính xác phụ thuộc vào trình duyệt.

Khi trang đang ở nền, không có vẽ lại nào cả, vì vậy callback sẽ không chạy: animation sẽ bị tạm dừng và không tiêu tốn tài nguyên. Điều đó rất tốt.

Dưới đây là hàm hỗ trợ `animate` để thiết lập hầu hết các animation:

```
function animate({timing, draw, duration}) {

  let start = performance.now();

  requestAnimationFrame(function animate(time) {
    // timeFraction goes from 0 to 1
    let timeFraction = (time - start) / duration;
    if (timeFraction > 1) timeFraction = 1;

    // calculate the current animation state
    let progress = timing(timeFraction);

    draw(progress); // draw it

    if (timeFraction < 1) {
      requestAnimationFrame(animate);
    }

  });
}
```

Các tùy chọn:

- `duration` – tổng thời gian animation tính bằng ms.
- `timing` – hàm tính tiến độ của animation. Nhận phần thời gian từ 0 đến 1, trả về tiến độ của animation, thường từ 0 đến 1.
- `draw` – hàm vẽ animation.

Tất nhiên chúng ta có thể cải thiện nó, thêm nhiều tính năng hơn, nhưng JavaScript animation không được áp dụng hàng ngày. Chúng được dùng để làm những thứ thú vị và không chuẩn. Vì vậy bạn sẽ muốn thêm các tính năng cần thiết khi cần.

JavaScript animation có thể dùng bất kỳ timing function nào. Chúng ta đã xem qua nhiều ví dụ và các biến đổi để làm chúng linh hoạt hơn. Khác với CSS, chúng ta không bị giới hạn bởi đường cong Bézier ở đây.

Điều tương tự cũng đúng với `draw`: chúng ta có thể animate bất kỳ thứ gì, không chỉ các thuộc tính CSS.

---

---

## Bài tập

## [Bài tập](#tasks)

### [Animate quả bóng nảy](#animate-the-bouncing-ball)

importance: 5

Tạo một quả bóng nảy. Nhấp để xem nó nên trông như thế nào:

[Mở sandbox cho bài tập.](https://plnkr.co/edit/nw27ZhXcuriGDSno?p=preview)

solution

Để nảy, chúng ta có thể dùng thuộc tính CSS `top` và `position:absolute` cho quả bóng bên trong ô có `position:relative`.

Tọa độ dưới cùng của ô là `field.clientHeight`. Thuộc tính CSS `top` tham chiếu đến cạnh trên của quả bóng. Vì vậy nó nên đi từ `0` đến `field.clientHeight - ball.clientHeight`, đó là vị trí thấp nhất cuối cùng của cạnh trên quả bóng.

Để có hiệu ứng "nảy", chúng ta có thể dùng timing function `bounce` ở chế độ `easeOut`.

Dưới đây là mã cuối cùng cho animation:

```
let to = field.clientHeight - ball.clientHeight;

animate({
  duration: 2000,
  timing: makeEaseOut(bounce),
  draw(progress) {
    ball.style.top = to * progress + 'px'
  }
});
```

[Mở lời giải trong sandbox.](https://plnkr.co/edit/gB6N1nIPQ2kzEf9m?p=preview)

### [Animate quả bóng nảy sang phải](#animate-the-ball-bouncing-to-the-right)

importance: 5

Làm cho quả bóng nảy sang phải. Như thế này:

Viết mã animation. Khoảng cách sang trái là `100px`.

Lấy lời giải của bài tập trước [Animate quả bóng nảy](/task/animate-ball) làm nguồn.

solution

Trong bài tập [Animate quả bóng nảy](/task/animate-ball) chúng ta chỉ có một thuộc tính để animate. Giờ chúng ta cần thêm một: `elem.style.left`.

Tọa độ ngang thay đổi theo quy luật khác: nó không "nảy", mà tăng dần dịch chuyển quả bóng sang phải.

Chúng ta có thể viết thêm một `animate` cho nó.

Với hàm thời gian chúng ta có thể dùng `linear`, nhưng thứ gì đó như `makeEaseOut(quad)` trông tốt hơn nhiều.

Mã:

```
let height = field.clientHeight - ball.clientHeight;
let width = 100;

// animate top (bouncing)
animate({
  duration: 2000,
  timing: makeEaseOut(bounce),
  draw: function(progress) {
    ball.style.top = height * progress + 'px'
  }
});

// animate left (moving to the right)
animate({
  duration: 2000,
  timing: makeEaseOut(quad),
  draw: function(progress) {
    ball.style.left = width * progress + "px"
  }
});
```

[Mở lời giải trong sandbox.](https://plnkr.co/edit/VugcOOgDCJVnGr8p?p=preview)
