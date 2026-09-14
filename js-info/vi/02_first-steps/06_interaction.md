# Tương tác: alert, prompt, confirm

> Nguồn: [https://javascript.info/alert-prompt-confirm](https://javascript.info/alert-prompt-confirm)

<!-- fetched: 2026-09-14 -->

Khi chúng ta sẽ sử dụng trình duyệt như môi trường demo của mình, hãy xem một vài hàm để tương tác với người dùng: `alert`, `prompt` và `confirm`.

## [alert](#alert)

Hàm này chúng ta đã thấy rồi. Nó hiển thị một thông báo và đợi người dùng nhấn “OK”.

Ví dụ:

```
alert("Hello");
```

Cửa sổ nhỏ với thông báo được gọi là *cửa sổ modal*. Từ “modal” có nghĩa là người truy cập không thể tương tác với phần còn lại của trang, nhấn các nút khác, v.v., cho đến khi họ xử lý cửa sổ. Trong trường hợp này – cho đến khi họ nhấn “OK”.

## [prompt](#prompt)

Hàm `prompt` nhận hai đối số:

```
result = prompt(title, [default]);
```

Nó hiển thị một cửa sổ modal với một thông báo văn bản, một trường nhập liệu cho người truy cập, và các nút OK/Cancel.

`title`
:   Văn bản hiển thị cho người truy cập.

`default`
:   Tham số thứ hai tùy chọn, giá trị ban đầu cho trường nhập liệu.

Dấu ngoặc vuông trong cú pháp `[...]`

Dấu ngoặc vuông xung quanh `default` trong cú pháp ở trên cho biết tham số là tùy chọn, không bắt buộc.

Người truy cập có thể gõ gì đó trong trường nhập prompt và nhấn OK. Sau đó chúng ta nhận được văn bản đó trong `result`. Hoặc họ có thể hủy nhập bằng cách nhấn Cancel hoặc nhấn phím `Esc`, sau đó chúng ta nhận được `null` như là `result`.

Lệnh gọi `prompt` trả về văn bản từ trường nhập hoặc `null` nếu nhập đã bị hủy.

Ví dụ:

```
let age = prompt('Bạn bao nhiêu tuổi?', 100);

alert(`Bạn ${age} tuổi!`); // Bạn 100 tuổi!
```

Trong IE: luôn cung cấp một `default`

Tham số thứ hai là tùy chọn, nhưng nếu chúng ta không cung cấp nó, Internet Explorer sẽ chèn văn bản `"undefined"` vào prompt.

Chạy mã này trong Internet Explorer để xem:

```
let test = prompt("Test");
```

Vì vậy, để prompt trông tốt trong IE, chúng ta khuyến nghị luôn cung cấp đối số thứ hai:

```
let test = prompt("Test", ''); // <-- cho IE
```

## [confirm](#confirm)

Cú pháp:

```
result = confirm(question);
```

Hàm `confirm` hiển thị một cửa sổ modal với một `question` và hai nút: OK và Cancel.

Kết quả là `true` nếu OK được nhấn và `false` ngược lại.

Ví dụ:

```
let isBoss = confirm("Bạn có phải là sếp không?");

alert( isBoss ); // true nếu OK được nhấn
```

## [Tổng kết](#summary)

Chúng ta đã bao quát 3 hàm cụ thể cho trình duyệt để tương tác với visitor:

`alert`
:   hiển thị một thông báo.

`prompt`
:   hiển thị một thông báo yêu cầu người dùng nhập văn bản. Nó trả về văn bản hoặc, nếu nhấn nút Cancel hoặc `Esc`, trả về `null`.

`confirm`
:   hiển thị một thông báo và đợi người dùng nhấn “OK” hoặc “Cancel”. Nó trả về `true` cho OK và `false` cho Cancel/`Esc`.

Tất cả các phương pháp này là modal: chúng tạm dừng thực thi script và không cho phép người truy cập tương tác với phần còn lại của trang cho đến khi cửa sổ bị đóng.

Có hai hạn chế được chia sẻ bởi tất cả các phương pháp ở trên:

1. Vị trí chính xác của cửa sổ modal được xác định bởi trình duyệt. Thông thường, nó ở trung tâm.
2. Ngoại hình chính xác của cửa sổ cũng phụ thuộc vào trình duyệt. Chúng ta không thể sửa đổi nó.

Đó là cái giá cho sự đơn giản. Có những cách khác để hiển thị các cửa sổ đẹp hơn và tương tác phong phú hơn với người truy cập, nhưng nếu “nút chuông và còi” không quá quan trọng, các phương pháp này hoạt động rất tốt.

---

---

## Các bài tập

## [Các bài tập](#tasks)

### [Một trang đơn giản](#a-simple-page)

mức độ quan trọng: 4

Tạo một trang web hỏi tên và hiển thị nó.

[Chạy demo](#)

lời giải

Mã JavaScript:

```
let name = prompt("Tên của bạn là gì?", "");
alert(name);
```

Trang đầy đủ:

```
<!DOCTYPE html>
<html>
<body>

  <script>
    'use strict';

    let name = prompt("Tên của bạn là gì?", "");
    alert(name);
  </script>

</body>
</html>
```
