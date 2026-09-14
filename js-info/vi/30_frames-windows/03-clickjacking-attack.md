# Tấn công clickjacking

> Source: [https://javascript.info/clickjacking](https://javascript.info/clickjacking)

<!-- fetched: 2026-09-14 -->

Tấn công "clickjacking" cho phép một trang độc hại nhấp vào một "trang nạn nhân" *thay cho người truy cập*.

Nhiều trang web đã bị hack theo cách này, bao gồm Twitter, Facebook, Paypal và các trang web khác. Tất cả đều đã được sửa chữa, tất nhiên.

## [Ý tưởng](#the-idea)

Ý tưởng rất đơn giản.

Đây là cách clickjacking đã được thực hiện với Facebook:

1. Một người truy cập bị lure đến trang độc hại. Nó không quan trọng như thế nào.
2. Trang có một liên kết trông vô hại (như "làm giàu ngay" hoặc "nhấp vào đây, rất vui").
3. Lên trên liên kết đó, trang độc hại định vị một `<iframe>` trong suốt với `src` từ facebook.com, theo cách mà nút "Like" nằm ngay phía trên liên kết đó. Thường thì điều đó được thực hiện với `z-index`.
4. Cố gắng nhấp vào liên kết, người truy cập thực sự đang nhấp vào nút.

## [Demo](#the-demo)

Đây là cách trang độc hại trông như thế nào. Để dễ hiểu, `<iframe>` bán trong suốt (trong các trang độc hại thực tế nó hoàn toàn trong suốt):

```
<style>
iframe { /* iframe từ trang nạn nhân */
  width: 400px;
  height: 100px;
  position: absolute;
  top:0; left:-20px;
  opacity: 0.5; /* trong thực tế opacity:0 */
  z-index: 1;
}
</style>

<div>Nhấp để làm giàu ngay:</div>

<!-- Url từ trang nạn nhân -->
<iframe src="/clickjacking/facebook.html"></iframe>

<button>Nhấp vào đây!</button>

<div>...Và bạn sẽ cool (thực ra tôi là hacker cool)!</div>
```

Demo đầy đủ của cuộc tấn công:

Kết quả

facebook.html

index.html

```
<!DOCTYPE HTML>
<html>

<body style="margin:10px;padding:10px">

  <input type="button" onclick="alert('Nhấp Like trên facebook.html!')" value="TÔI THÍCH NÓ !">

</body>

</html>
```

```
<!doctype html>
<html>

<head>
  <meta charset="UTF-8">
</head>

<body>

  <style>
    iframe {
      width: 400px;
      height: 100px;
      position: absolute;
      top: 5px;
      left: -14px;
      opacity: 0.5;
      z-index: 1;
    }
  </style>

  <div>Nhấp để làm giàu ngay:</div>

  <!-- Url từ trang nạn nhân -->
  <iframe src="facebook.html"></iframe>

  <button>Nhấp vào đây!</button>

  <div>...Và bạn sẽ cool (thực ra tôi là hacker cool)!</div>

</body>
</html>
```

Ở đây chúng ta có một `<iframe src="facebook.html">` bán trong suốt, và trong ví dụ chúng ta có thể thấy nó lơ lửng trên nút. Một cú nhấp chuột vào nút thực sự nhấp vào iframe, nhưng điều đó không hiển thị với người dùng, vì iframe là trong suốt.

Kết quả là, nếu người truy cập đã đăng nhập vào Facebook ("ghi nhớ tôi" thường được bật), thì nó sẽ thêm một "Like". Trên Twitter đó sẽ là nút "Follow".

Đây là ví dụ tương tự, nhưng gần với thực tế hơn, với `opacity:0` cho `<iframe>`:

Kết quả

facebook.html

index.html

```
<!DOCTYPE HTML>
<html>

<body style="margin:10px;padding:10px">

  <input type="button" onclick="alert('Nhấp Like trên facebook.html!')" value="TÔI THÍCH NÓ !">

</body>

</html>
```

```
<!doctype html>
<html>

<head>
  <meta charset="UTF-8">
</head>

<body>

  <style>
    iframe {
      width: 400px;
      height: 100px;
      position: absolute;
      top: 5px;
      left: -14px;
      opacity: 0;
      z-index: 1;
    }
  </style>

  <div>Nhấp để làm giàu ngay:</div>

  <!-- Url từ trang nạn nhân -->
  <iframe src="facebook.html"></iframe>

  <button>Nhấp vào đây!</button>

  <div>...Và bạn sẽ cool (thực ra tôi là hacker cool)!</div>

</body>
</html>
```

Tất cả những gì chúng ta cần để tấn công – là định vị `<iframe>` trên trang độc hại theo cách mà nút nằm ngay trên liên kết. Vậy là khi người dùng nhấp vào liên kết, họ thực sự đang nhấp vào nút. Điều đó thường có thể thực hiện được với CSS.

Clickjacking dành cho cú nhấp chuột, không phải bàn phím

Tấn công chỉ ảnh hưởng đến các hành động chuột (hoặc tương tự, như chạm trên di động).

Nhập liệu bàn phím khó chuyển hướng hơn nhiều. Về mặt kỹ thuật, nếu chúng ta có một trường văn bản để hack, thì chúng ta có thể định vị một iframe theo cách mà các trường văn bản chồng lên nhau. Vì vậy, khi người truy cập cố gắng focus vào ôinput họ thấy trên trang, họ thực sự đang focus vào ôinput bên trong iframe.

Nhưng sau đó có một vấn đề. Mọi thứ người truy cập gõ sẽ bị ẩn, vì iframe không hiển thị.

Mọi người thường sẽ dừng gõ khi họ không thể thấy các ký tự mới của mình in trên màn hình.

## [Phòng thủ thời xưa (yếu)](#old-school-defences-weak)

Phòng thủ cổ xưa nhất là một chút JavaScript ngăn cản việc mở trang trong frame (được gọi là "framebusting").

Nó trông như thế này:

```
if (top != window) {
  top.location = window.location;
}
```

Đó là: nếu cửa sổ phát hiện ra rằng nó không ở trên cùng, thì nó tự động khiến chính nó trở thành cửa sổ trên cùng.

Điều này không phải là phòng thủ đáng tin cậy, vì có nhiều cách để vượt qua nó. Hãy điểm qua một vài cách.

### [Chặn top-navigation](#blocking-top-navigation)

Chúng ta có thể chặn chuyển đổi gây ra bởi thay đổi `top.location` trong trình xử lý sự kiện [beforeunload](/onload-ondomcontentloaded#window.onbeforeunload).

Trang顶层 (trang bao bọc, thuộc về kẻ hack) đặt một trình xử lý ngăn cản, như thế này:

```
window.onbeforeunload = function() {
  return false;
};
```

Khi `iframe` cố gắng thay đổi `top.location`, người truy cập nhận được một thông báo hỏi họ có muốn rời đi hay không.

Trong hầu hết các trường hợp, người truy cập sẽ trả lời phủ định vì họ không biết về iframe – tất cả những gì họ thấy là trang顶层, không có lý do gì để rời đi. Vì vậy `top.location` sẽ không thay đổi!

Trong thực tế:

Kết quả

iframe.html

index.html

```
<!doctype html>
<html>

<head>
  <meta charset="UTF-8">
</head>

<body>

  <div>Thay đổi top.location thành javascript.info</div>

  <script>
    top.location = 'https://javascript.info';
  </script>

</body>

</html>
```

```
<!doctype html>
<html>

<head>
  <meta charset="UTF-8">

  <style>
    iframe {
      width: 400px;
      height: 100px;
      position: absolute;
      top: 0;
      left: -20px;
      opacity: 0;
      z-index: 1;
    }
  </style>

  <script>
    function attack() {

      window.onbeforeunload = function() {
        window.onbeforeunload = null;
        return "Muốn rời đi mà không học hết bí mật (he-he)?";
      };

      document.body.insertAdjacentHTML('beforeend', '<iframe src="iframe.html">');
    }
  </script>
</head>

<body>

  <p>Sau khi nhấp vào nút, người truy cập nhận được câu hỏi "lạ" về việc họ có muốn rời đi hay không.</p>

  <p>Bầu cử có lẽ sẽ trả lời "Không", và bảo vệ iframe bị hack.</p>

  <button onclick="attack()">Thêm iframe "được bảo vệ"</button>

</body>
</html>
```

### [Thuộc tính Sandbox](#sandbox-attribute)

Một trong những thứ bị hạn chế bởi thuộc tính `sandbox` là điều hướng. Một iframe sandboxed không thể thay đổi `top.location`.

Vì vậy, chúng ta có thể thêm iframe với `sandbox="allow-scripts allow-forms"`. Điều đó sẽ nới lỏng các hạn chế, cho phép script và biểu mẫu. Nhưng chúng ta bỏ qua `allow-top-navigation` vì vậy việc thay đổi `top.location` bị cấm.

Đây là mã:

```
<iframe sandbox="allow-scripts allow-forms" src="facebook.html"></iframe>
```

Cũng có những cách khác để vượt qua bảo vệ đơn giản đó.

## [X-Frame-Options](#x-frame-options)

Header phía máy chủ `X-Frame-Options` có thể cho phép hoặc cấm hiển thị trang bên trong khung.

Nó phải được gửi chính xác như HTTP-header: trình duyệt sẽ bỏ qua nó nếu tìm thấy trong thẻ HTML `<meta>`. Vì vậy, `<meta http-equiv="X-Frame-Options"...>` sẽ không có tác dụng.

Header có thể có 3 giá trị:

`DENY`
:   Không bao giờ hiển thị trang bên trong khung.

`SAMEORIGIN`
:   Cho phép bên trong khung nếu tài liệu cha đến từ cùng origin.

`ALLOW-FROM domain`
:   Cho phép bên trong khung nếu tài liệu cha đến từ miền đã cho.

Ví dụ, Twitter sử dụng `X-Frame-Options: SAMEORIGIN`.

Đây là kết quả:

```
<iframe src="https://twitter.com"></iframe>
```

Tùy thuộc vào trình duyệt của bạn, `iframe` ở trên要么 trống либо cảnh báo bạn rằng trình duyệt sẽ không cho phép trang đó điều hướng theo cách này.

## [Hiển thị với chức năng bị tắt](#showing-with-disabled-functionality)

Header `X-Frame-Options` có một tác dụng phụ. Các trang web khác sẽ không thể hiển thị trang của chúng ta trong khung, ngay cả khi chúng có lý do chính đáng để làm như vậy.

Vì vậy, có các giải pháp khác… Ví dụ, chúng ta có thể "phủ" trang bằng một `<div>` với styles `height: 100%; width: 100%;`, vì vậy nó sẽ chặn mọi cú nhấp chuột. `<div>` đó sẽ bị xóa nếu `window == top` hoặc nếu chúng ta quyết định rằng chúng ta không cần bảo vệ.

Thứ gì đó như thế này:

```
<style>
  #protector {
    height: 100%;
    width: 100%;
    position: absolute;
    left: 0;
    top: 0;
    z-index: 99999999;
  }
</style>

<div id="protector">
  <a href="/" target="_blank">Đi đến trang web</a>
</div>

<script>
  // sẽ có lỗi nếu cửa sổ top đến từ origin khác
  // nhưng ở đây thì ổn
  if (top.document.domain == document.domain) {
    protector.remove();
  }
</script>
```

Demo:

Kết quả

iframe.html

index.html

```
<!doctype html>
<html>

<head>
  <meta charset="UTF-8">

  <style>
    #protector {
      height: 100%;
      width: 100%;
      position: absolute;
      left: 0;
      top: 0;
      z-index: 99999999;
    }
  </style>

</head>

<body>

<div id="protector">
  <a href="/" target="_blank">Đi đến trang web</a>
</div>

<script>

  if (top.document.domain == document.domain) {
    protector.remove();
  }

</script>

  Văn bản này luôn hiển thị.

  Nhưng nếu trang được mở bên trong tài liệu từ miền khác, div ở trên nó sẽ ngăn mọi hành động.

  <button onclick="alert(1)">Nhấp sẽ không hoạt động trong trường hợp đó</button>

</body>
</html>
```

```
<!doctype html>
<html>

<head>
  <meta charset="UTF-8">
</head>
<body>

  <iframe src="iframe.html"></iframe>

</body>
</html>
```

## [Thuộc tính cookie samesite](#samesite-cookie-attribute)

Thuộc tính cookie `samesite` cũng có thể ngăn chặn các cuộc tấn công clickjacking.

Một cookie với thuộc tính như vậy chỉ được gửi đến trang web nếu nó được mở trực tiếp, không phải qua khung, hoặc các cách khác. Thông tin chi tiết hơn trong chương [Cookies, document.cookie](/cookie#samesite).

Nếu trang web, chẳng hạn như Facebook, có thuộc tính `samesite` trên cookie xác thực của nó, như thế này:

```
Set-Cookie: authorization=secret; samesite
```

…Thì cookie như vậy sẽ không được gửi khi Facebook được mở trong iframe từ trang web khác. Vì vậy, cuộc tấn công sẽ thất bại.

Thuộc tính cookie `samesite` sẽ không có hiệu quả khi cookie không được sử dụng. Điều đó có thể cho phép các trang web khác dễ dàng hiển thị các trang công khai, chưa xác thực của chúng ta trong iframe.

Tuy nhiên, điều này cũng có thể cho phép các cuộc tấn công clickjacking hoạt động trong một vài trường hợp hạn chế. Một trang web bình luận ẩn danh ngăn chặn bầu cử trùng lặp bằng cách kiểm tra địa chỉ IP, ví dụ, vẫn sẽ dễ bị clickjacking vì nó không xác thực người dùng bằng cookie.

## [Tóm tắt](#summary)

Clickjacking là một cách để "lừa" người dùng nhấp vào một trang nạn nhân mà thậm chí không biết những gì đang xảy ra. Điều đó nguy hiểm nếu có các hành động kích hoạt bằng cú nhấp chuột quan trọng.

Một hacker có thể đăng một liên kết đến trang độc hại của họ trong tin nhắn, hoặc lure người truy cập đến trang của họ bằng cách khác. Có nhiều biến thể.

Từ một góc nhìn – cuộc tấn công "không sâu": tất cả những gì một hacker đang làm là chặn một cú nhấp chuột duy nhất. Nhưng từ góc nhìn khác, nếu hacker biết rằng sau cú nhấp chuột một điều khiển khác sẽ xuất hiện, thì họ có thể sử dụng các tin nhắn tinh vi để thúc ép người dùng nhấp vào chúng.

Cuộc tấn công khá nguy hiểm, vì khi chúng ta thiết kế UI, chúng ta thường không dự đoán được rằng hacker có thể nhấp thay cho người truy cập. Vì vậy, lỗ hổng có thể được tìm thấy ở những nơi hoàn toàn không ngờ tới.

- Người ta khuyên nên sử dụng `X-Frame-Options: SAMEORIGIN` trên các trang (hoặc toàn bộ trang web) không được thiết kế để hiển thị bên trong khung.
- Sử dụng `<div>` phủ nếu chúng ta muốn cho phép các trang của chúng ta được hiển thị trong iframe, nhưng vẫn an toàn.
