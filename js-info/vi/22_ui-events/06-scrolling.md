# Cuộn trang (Scrolling)

> Source: [https://javascript.info/onscroll](https://javascript.info/onscroll)

<!-- fetched: 2026-09-14 -->

Sự kiện `scroll` cho phép phản ứng с cuộn trang hoặc cuộn phần tử. Có khá nhiều điều tốt chúng ta có thể làm ở đây.

Ví dụ:

- Hiển thị/ẩn các điều khiển hoặc thông tin bổ sung tùy thuộc vào vị trí của người dùng в document.
- Tải thêm dữ liệu khi người dùng scroll xuống đến cuối trang.

Đây là một hàm nhỏ để hiển thị scroll hiện tại:

```
window.addEventListener('scroll', function() {
  document.getElementById('showScroll').innerHTML = window.pageYOffset + 'px';
});
```

Trong hành động:

Current scroll = **scroll the window**

Sự kiện `scroll` hoạt động cả trên `window` và на các phần tử scrollable.

## [Ngăn scrolling](#prevent-scrolling)

Làm thế nào để làm cho một thứ gì đó không scrollable?

Chúng ta không thể ngăn scrolling bằng cách sử dụng `event.preventDefault()` trong listener `onscroll`, vì nó kích hoạt *sau khi* scroll đã xảy ra.

Nhưng chúng ta có thể ngăn scrolling bằng `event.preventDefault()` на một sự kiện gây ra scroll, chẳng hạn như sự kiện `keydown` cho `pageUp` và `pageDown`.

Nếu chúng ta thêm một event handler đến các sự kiện này và `event.preventDefault()` в nó, thì scroll sẽ không bắt đầu.

Có nhiều cách để khởi tạo scroll, vì vậy nó đáng tin cậy hơn khi sử dụng CSS, thuộc tính `overflow`.

Đây là vài tasks mà bạn có thể giải quyết hoặc xem qua để thấy các ứng dụng của `onscroll`.

---

---

## Bài tập

## [Bài tập](#tasks)

### [Endless page](#endless-page)

mức độ khó: 5

Tạo một endless page. Khi người truy cập scroll nó đến cuối, nó tự động append current date-time vào text (để người truy cập có thể scroll thêm).

Như vậy:

Xin lưu ý hai tính năng quan trọng của scroll:

1. **Scroll là "elastic".** Chúng ta có thể scroll một chút beyond document start hoặc end в một số browser/devices (empty space bên dưới được hiển thị, và sau đó document sẽ tự động "bounces back" về normal).
2. **Scroll không chính xác.** Khi chúng ta scroll đến cuối trang, thì thực tế chúng ta có thể đang ở cách document bottom thật sự như 0-50px.

Vì vậy, "scrolling đến cuối" có nghĩa là người truy cập không cách xa document end quá 100px.

P.S. Trong cuộc sống thực, chúng ta có thể muốn hiển thị "more messages" hoặc "more goods".

[Mở sandbox cho bài tập.](https://plnkr.co/edit/YWQcVXPxWF9zG60Q?p=preview)

lời giải

Core của solution là một function thêm nhiều dates vào trang (hoặc tải nhiều stuff trong cuộc sống thực) trong khi chúng ta ở cuối trang.

Chúng ta có thể gọi nó ngay lập tức và thêm nó как một `window.onscroll` handler.

Câu hỏi quan trọng nhất là: "Làm thế nào chúng ta phát hiện rằng trang được scroll đến bottom?"

Hãy sử dụng window-relative coordinates.

Document được biểu diễn (và chứa) trong thẻ `<html>`, đó là `document.documentElement`.

Chúng ta có thể lấy window-relative coordinates của toàn bộ document như `document.documentElement.getBoundingClientRect()`, thuộc tính `bottom` sẽ là window-relative coordinate của document bottom.

Ví dụ, nếu chiều cao của toàn bộ HTML document là `2000px`, thì:

```
// khi chúng ta đang ở top của trang
// window-relative top = 0
document.documentElement.getBoundingClientRect().top = 0

// window-relative bottom = 2000
// document dài, vì vậy có lẽ xa beyond window bottom
document.documentElement.getBoundingClientRect().bottom = 2000
```

Nếu chúng ta scroll `500px` xuống dưới, thì:

```
// document top nằm above window 500px
document.documentElement.getBoundingClientRect().top = -500
// document bottom gần hơn 500px
document.documentElement.getBoundingClientRect().bottom = 1500
```

Khi chúng ta scroll đến cuối, giả sử rằng chiều cao window là `600px`:

```
// document top nằm above window 1400px
document.documentElement.getBoundingClientRect().top = -1400
// document bottom nằm below window 600px
document.documentElement.getBoundingClientRect().bottom = 600
```

Xin lưu ý rằng `bottom` không thể là `0`, vì nó không bao giờ đạt đến window top. Giới hạn thấp nhất của coordinate `bottom` là chiều cao window (chúng ta giả định nó là `600`), chúng ta không thể scroll nó lên hơn nữa.

Chúng ta có thể lấy chiều cao window как `document.documentElement.clientHeight`.

Đối với task của chúng ta, chúng ta cần biết khi document bottom không cách xa nó quá 100px (tức là: `600-700px`, nếu chiều cao là `600`).

Vì vậy, đây là function:

```
function populate() {
  while(true) {
    // document bottom
    let windowRelativeBottom = document.documentElement.getBoundingClientRect().bottom;

    // nếu người dùng chưa scroll đủ xa (>100px đến end)
    if (windowRelativeBottom > document.documentElement.clientHeight + 100) break;

    // hãy thêm nhiều data hơn
    document.body.insertAdjacentHTML("beforeend", `<p>Date: ${new Date()}</p>`);
  }
}
```

[Mở solution trong sandbox.](https://plnkr.co/edit/cclA6BokVrkqb5Ls?p=preview)

### [Nút up/down](#up-down-button)

mức độ khó: 5

Tạo một nút "up to top" để giúp với page scrolling.

Nó nên hoạt động như sau:

- Trong khi trang chưa được scroll xuống ít nhất bằng chiều cao window – nó không hiển thị.
- Khi trang được scroll xuống hơn chiều cao window – một arrow "hướng lên" xuất hiện ở góc trên bên trái. Nếu trang được scroll ngược lại, nó biến mất.
- Khi arrow được click, trang scroll về top.

Như vậy (góc trên bên trái, scroll to see):

[Mở sandbox cho bài tập.](https://plnkr.co/edit/kbmUE99oEnyd6ASc?p=preview)

lời giải

[Mở solution trong sandbox.](https://plnkr.co/edit/h5fkZMlKRJOB1dcI?p=preview)

### [Load visible images](#load-visible-images)

mức độ khó: 4

Giả sử chúng ta có một client tốc độ chậm và muốn tiết kiệm mobile traffic của họ.

Để mục đích đó, chúng ta quyết định không hiển thị images ngay lập tức, mà thay vào đó thay thế chúng bằng placeholders, như sau:

```
<img src="placeholder.svg" width="128" height="128" data-src="real.jpg">
```

Vì vậy, ban đầu tất cả images là `placeholder.svg`. Khi trang scroll đến vị trí mà người dùng có thể thấy image – chúng ta thay đổi `src` thành cái в `data-src`, và do đó image tải.

Đây là một ví dụ в `iframe`:

Scroll nó để thấy các images load "on-demand".

Requirements:

- Khi trang load,那些 images mà on-screen nên load ngay lập tức, trước bất kỳ scrolling nào.
- Một số images có thể là regular, không có `data-src`. Mã không nên chạm vào chúng.
- Một khi image được load, nó không nên reload bất kỳ lúc nào khi scrolled in/out.

P.S. Nếu bạn có thể, hãy tạo một solution advanced hơn sẽ "preload" các images mà một page bên dưới/trong vị trí hiện tại.

P.P.S. Chỉ vertical scroll được xử lý, không có horizontal scrolling.

[Mở sandbox cho bài tập.](https://plnkr.co/edit/bS3h5iJHSS2xAG6O?p=preview)

lời giải

Handler `onscroll` nên kiểm tra哪些 images là visible và hiển thị chúng.

Chúng ta cũng muốn chạy nó когда trang load, để phát hiện ngay lập tức visible images và load chúng.

Mã nên thực hiện когда document được load, để nó có quyền truy cập vào nội dung của nó.

Hoặc đặt nó ở đáy `<body>`:

```
// ...the page content is above...

function isVisible(elem) {

  let coords = elem.getBoundingClientRect();

  let windowHeight = document.documentElement.clientHeight;

  // top elem edge visible?
  let topVisible = coords.top > 0 && coords.top < windowHeight;

  // bottom elem edge visible?
  let bottomVisible = coords.bottom < windowHeight && coords.bottom > 0;

  return topVisible || bottomVisible;
}
```

Function `showVisible()` sử dụng visibility check, được triển khai bời `isVisible()`, để load visible images:

```
function showVisible() {
  for (let img of document.querySelectorAll('img')) {
    let realSrc = img.dataset.src;
    if (!realSrc) continue;

    if (isVisible(img)) {
      img.src = realSrc;
      img.dataset.src = '';
    }
  }
}

showVisible();
window.onscroll = showVisible;
```

P.S. Solution cũng có một variant của `isVisible` mà "preloads" các images nằm trong 1 page trên/dưới document scroll hiện tại.

[Mở solution trong sandbox.](https://plnkr.co/edit/ENtjdtkVRwkmKqZ4?p=preview)
