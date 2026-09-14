# Xin chào, thế giới!

> Nguồn: [https://javascript.info/hello-world](https://javascript.info/hello-world)

<!-- fetched: 2026-09-14 -->

Phần này của khóa học nói về JavaScript cốt lõi, ngôn ngữbản thân.

Nhưng chúng ta cần một môi trường làm việc để chạy các tập lệnh (script) của mình, và vì đây là sách trực tuyến, trình duyệt là một lựa chọn tốt. Chúng ta sẽ giữ lượng lệnh đặc thù cho trình duyệt (như `alert`) ở mức tối thiểu để bạn không mất thời gian cho chúng nếu dự định tập trung vào một môi trường khác (như Node.js). Chúng ta sẽ tập trung vào JavaScript trong trình duyệt ở [phần tiếp theo](/ui) của khóa học.

Vậy trước hết, hãy xem cách nhúng một script vào trang web. Đối với môi trường phía server (như Node.js), bạn có thể thực thi tập lệnh bằng lệnh như `"node my.js"`.

## [Thẻ "script"](#the-script-tag)

Chương trình JavaScript có thể được chèn vào hầu hết mọi nơi trong tài liệu HTML bằng thẻ `<script>`.

Ví dụ:

```
<!DOCTYPE HTML>
<html>

<body>

  <p>Trước script...</p>

  <script>
    alert( 'Xin chào, thế giới!' );
  </script>

  <p>...Sau script.</p>

</body>

</html>
```

Bạn có thể chạy ví dụ bằng cách nhấp vào nút "Chạy" ở góc trên bên phải của hộp bên trên.

Thẻ `<script>` chứa mã JavaScript sẽ tự động được thực thi khi trình duyệt xử lý thẻ.

## [Đánh dấu hiện đại](#modern-markup)

Thẻ `<script>` có một số thuộc tính hiếm khi được sử dụng ngày nay nhưng vẫn có thể tìm thấy trong mã cũ:

Thuộc tính `type`: `<script type=…>`
:   Tiêu chuẩn HTML cũ, HTML4, yêu cầu một script phải có một `type`. Thông thường đó là `type="text/javascript"`. Nó không còn bắt buộc nữa. Cũng, tiêu chuẩn HTML hiện đại đã thay đổi hoàn toàn ý nghĩa của thuộc tính này. Bây giờ, nó có thể được sử dụng cho các mô-đun JavaScript. Nhưng đó là một chủ đề nâng cao, chúng ta sẽ nói về các mô-đun trong một phần khác của khóa học.

Thuộc tính `language`: `<script language=…>`
:   Thuộc tính này có ý định hiển thị ngôn ngữ của script. Thuộc tính này không còn ý nghĩa vì JavaScript là ngôn ngữ mặc định. Không cần sử dụng nó.

Các comment trước và sau scripts.
:   Trong các sách và hướng dẫn rất cũ, bạn có thể tìm thấy các comment bên trong thẻ `<script>`, như thế này:

    ```
    <script type="text/javascript"><!--
        ...
    //--></script>
    ```

    Mẹo này không được sử dụng trong JavaScript hiện đại. Những comment này ẩn mã JavaScript khỏi các trình duyệt cũ không biết cách xử lý thẻ `<script>`. Vì các trình duyệt phát hành trong 15 năm gần đây không có vấn đề này, loại comment này có thể giúp bạn nhận ra mã rất cũ.

## [Scripts bên ngoài](#external-scripts)

Nếu chúng ta có nhiều mã JavaScript, chúng ta có thể đặt nó vào một tệp riêng biệt.

Các tệp script được đính kèm với HTML bằng thuộc tính `src`:

```
<script src="/path/to/script.js"></script>
```

Ở đây, `/path/to/script.js` là đường dẫn tuyệt đối đến script từ gốc trang web. Cũng có thể cung cấp đường dẫn tương đối từ trang hiện tại. Ví dụ, `src="script.js"`, giống như `src="./script.js"`, sẽ có nghĩa là một tệp `"script.js"` trong thư mục hiện tại.

Chúng ta cũng có thể đưa ra một URL đầy đủ. Ví dụ:

```
<script src="https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.17.11/lodash.js"></script>
```

Để đính kèm nhiều scripts, sử dụng nhiều thẻ:

```
<script src="/js/script1.js"></script>
<script src="/js/script2.js"></script>
…
```

Xin lưu ý:

Theo quy tắc, chỉ có các script đơn giản nhất được đặt vào HTML. Các script phức tạp hơn cư trú trong các tệp riêng biệt.

Lợi ích của một tệp riêng biệt là trình duyệt sẽ tải nó xuống và lưu trữ nó trong [bộ nhớ cache](https://en.wikipedia.org/wiki/Web_cache) của nó.

Các trang khác tham chiếu cùng một script sẽ lấy nó từ bộ nhớ cache thay vì tải xuống, vì vậy tệp thực sự chỉ được tải xuống một lần.

Điều đó giảm lưu lượng truy cập và làm cho các trang nhanh hơn.

Nếu `src` được đặt, nội dung script sẽ bị bỏ qua.

Một thẻ `<script>` đơn không thể có cả thuộc tính `src` và mã bên trong.

Điều này sẽ không hoạt động:

```
<script src="file.js">
  alert(1); // nội dung bị bỏ qua, vì src đã được đặt
</script>
```

Chúng ta phải chọn một trong hai: một `<script src="…">` bên ngoài hoặc một `<script>` thông thường với mã.

Ví dụ trên có thể được chia thành hai scripts để hoạt động:

```
<script src="file.js"></script>
<script>
  alert(1);
</script>
```

## [Tổng kết](#summary)

- Chúng ta có thể sử dụng thẻ `<script>` để thêm mã JavaScript vào trang.
- Các thuộc tính `type` và `language` không cần thiết.
- Một script trong một tệp bên ngoài có thể được chèn với `<script src="path/to/script.js"></script>`.

Còn rất nhiều điều cần học về các script trình duyệt và cách tương tác của chúng với trang web. Nhưng hãy nhớ rằng phần này của khóa học dành cho ngôn ngữ JavaScript, vì vậy chúng ta không nên làm phân tâm với các cài đặt cụ thể cho trình duyệt. Chúng ta sẽ sử dụng trình duyệt như một cách để chạy JavaScript, rất thuận tiện cho việc đọc trực tuyến, nhưng chỉ là một trong nhiều cách.

---

---

## Các bài tập

## [Các bài tập](#tasks)

### [Hiển thị một alert](#show-an-alert)

mức độ quan trọng: 5

Tạo một trang hiển thị thông báo “Tôi là JavaScript!”.

Làm nó trong một sandbox, hay trên ổ cứng của bạn, không quan trọng, chỉ đảm bảo rằng nó hoạt động.

[Demo trong cửa sổ mới](https://en.js.cx/task/hello-alert/solution/)

lời giải

```
<!DOCTYPE html>
<html>

<body>

  <script>
    alert( "Tôi là JavaScript!" );
  </script>

</body>

</html>
```

[Mở lời giải trong một sandbox.](https://plnkr.co/edit/97S8WJJeMzrV4sva?p=preview)

### [Hiển thị một alert với một script bên ngoài](#show-an-alert-with-an-external-script)

mức độ quan trọng: 5

Sử dụng lời giải của bài tập trước [Hiển thị một alert](/task/hello-alert). Sửa đổi nó bằng cách trích xuất nội dung script vào một tệp bên ngoài `alert.js`, nằm trong cùng thư mục.

Mở trang, đảm bảo rằng alert hoạt động.

lời giải

Mã HTML:

```
<!DOCTYPE html>
<html>

<body>

  <script src="alert.js"></script>

</body>

</html>
```

Cho tệp `alert.js` trong cùng thư mục:

```
alert("Tôi là JavaScript!");
```
