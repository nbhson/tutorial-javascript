# Element template (Yếu tố mẫu)

> Source: [https://javascript.info/template-element](https://javascript.info/template-element)

<!-- fetched: 2026-09-14 -->

Phần tử `<template>` tích hợp sẵn đóng vai trò là nơi lưu trữ các mẫu HTML markup. Trình duyệt bỏ qua nội dung của nó, chỉ kiểm tra tính hợp lệ của cú pháp, nhưng chúng ta có thể truy cập và sử dụng nó trong JavaScript để tạo các phần tử khác.

Về lý thuyết, chúng ta có thể tạo bất kỳ phần tử vô hình nào đó trong HTML để lưu trữ HTML markup. Điều gì làm cho `<template>` đặc biệt?

Trước tiên, nội dung của nó có thể là bất kỳ HTML hợp lệ nào, kể cả những thứ thông thường cần một thẻ bao bọc thích hợp.

Ví dụ, chúng ta có thể đặt vào đó một hàng bảng `<tr>`:

```
<template>
  <tr>
    <td>Contents</td>
  </tr>
</template>
```

Thông thường, nếu chúng ta cố đặt `<tr>` vào bên trong, chẳng hạn, một `<div>`, trình duyệt sẽ phát hiện cấu trúc DOM không hợp lệ và “sửa” nó, thêm `<table>` bao quanh. Đó không phải điều chúng ta muốn. Mặt khác, `<template>` giữ đúng những gì chúng ta đặt vào đó.

Chúng ta có thể đặt cả styles và scripts vào `<template>`:

```
<template>
  <style>
    p { font-weight: bold; }
  </style>
  <script>
    alert("Hello");
  </script>
</template>
```

Trình duyệt coi nội dung `<template>` “nằm ngoài document”: các style không được áp dụng, các scripts không được thực thi, `<video autoplay>` không chạy, v.v.

Nội dung trở nên hoạt động (các style được áp dụng, các scripts được thực thi, v.v.) khi chúng ta chèn nó vào document.

## [Chèn template](#inserting-template)

Nội dung template có sẵn trong thuộc tính `content` của nó dưới dạng [DocumentFragment](/modifying-document#document-fragment) – một loại nút DOM đặc biệt.

Chúng ta có thể đối xử với nó như bất kỳ nút DOM nào khác, ngoại trừ một đặc tính đặc biệt: khi chúng ta chèn nó vào một nơi nào đó, các phần con của nó được chèn thay thế.

Ví dụ:

```
<template id="tmpl">
  <script>
    alert("Hello");
  </script>
  <div class="message">Hello, world!</div>
</template>

<script>
  let elem = document.createElement('div');

  // Clone the template content to reuse it multiple times
  elem.append(tmpl.content.cloneNode(true));

  document.body.append(elem);
  // Now the script from <template> runs
</script>
```

Hãy viết lại ví dụ Shadow DOM từ chương trước sử dụng `<template>`:

```
<template id="tmpl">
  <style> p { font-weight: bold; } </style>
  <p id="message"></p>
</template>

<div id="elem">Click me</div>

<script>
  elem.onclick = function() {
    elem.attachShadow({mode: 'open'});

    elem.shadowRoot.append(tmpl.content.cloneNode(true)); // (*)

    elem.shadowRoot.getElementById('message').innerHTML = "Hello from the shadows!";
  };
</script>
```

Ở dòng `(*)`, khi chúng ta clone và chèn `tmpl.content`, với tư cách là `DocumentFragment` của nó, các phần con của nó (`<style>`, `<p>`) được chèn thay thế.

Chúng tạo thành shadow DOM:

```
<div id="elem">
  #shadow-root
    <style> p { font-weight: bold; } </style>
    <p id="message"></p>
</div>
```

## [Tóm tắt](#summary)

Tóm lại:

- Nội dung `<template>` có thể là bất kỳ HTML chính xác về mặt cú pháp nào.
- Nội dung `<template>` được coi là “nằm ngoài document”, vì vậy nó không ảnh hưởng gì cả.
- Chúng ta có thể truy cập `template.content` từ JavaScript, clone nó để tái sử dụng trong component mới.

Thẻ `<template>` khá độc đáo, vì:

- Trình duyệt kiểm tra cú pháp HTML bên trong nó (khác với việc dùng template string bên trong script).
- …Nhưng vẫn cho phép sử dụng bất kỳ thẻ HTML cấp cao nào, kể cả những thẻ không có nghĩa nếu không có wrapper thích hợp (ví dụ `<tr>`).
- Nội dung trở nên tương tác: các scripts được thực thi, `<video autoplay>` được phát, v.v., khi được chèn vào document.

Phần tử `<template>` không có các cơ chế lặp, data binding hay thay thế biến, nhưng chúng ta có thể triển khai chúng trên cơ sở đó.
