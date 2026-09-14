# Form: event và method submit

> Source: [https://javascript.info/forms-submit](https://javascript.info/forms-submit)

<!-- fetched: 2026-09-14 -->

Sự kiện `submit` kích hoạt khi form được gửi, thường được dùng để validate form trước khi gửi lên server hoặc để hủy submission và xử lý nó trong JavaScript.

Phương thức `form.submit()` cho phép khởi tạo việc gửi form từ JavaScript. Ta có thể dùng nó để tạo động và gửi form của mình lên server.

Hãy xem chi tiết hơn về chúng.

## [Event: submit](#event-submit)

Có hai cách chính để submit một form:

1. Cách đầu – click `<input type="submit">` hoặc `<input type="image">`.
2. Cách thứ hai – nhấn `Enter` trên một input field.

Cả hai hành động đều dẫn đến sự kiện `submit` trên form. Handler có thể kiểm tra dữ liệu, và nếu có lỗi, hiện lỗi và gọi `event.preventDefault()`, thì form sẽ không được gửi lên server.

Trong form dưới đây:

1. Nhập vào trường text và nhấn `Enter`.
2. Click `<input type="submit">`.

Cả hai hành động hiện `alert` và form không được gửi đi đâu cả do `return false`:

```
<form onsubmit="alert('submit!');return false">
  First: Enter in the input field <input type="text" value="text"><br>
  Second: Click "submit": <input type="submit" value="Submit">
</form>
```

Mối quan hệ giữa `submit` và `click`

Khi form được gửi bằng `Enter` trên một input field, sự kiện `click` kích hoạt trên `<input type="submit">`.

Điều đó khá vui vì không có click thực sự nào.

Demo:

```
<form onsubmit="return false">
 <input type="text" size="30" value="Focus here and press enter">
 <input type="submit" value="Submit" onclick="alert('click')">
</form>
```

## [Method: submit](#method-submit)

Để submit form lên server một cách thủ công, ta có thể gọi `form.submit()`.

Sau đó sự kiện `submit` không được tạo ra. Giả định là nếu programmer gọi `form.submit()`, thì script đã xử lý tất cả các việc liên quan rồi.

Đôi khi cái đó được dùng để tạo thủ công và gửi một form, như sau:

```
let form = document.createElement('form');
form.action = 'https://google.com/search';
form.method = 'GET';

form.innerHTML = '<input name="q" value="test">';

// form phải có trong document để submit nó
document.body.append(form);

form.submit();
```

---

---

## Bài tập

## [Tasks](#tasks)

### [Modal form](#modal-form)

importance: 5

Tạo một hàm `showPrompt(html, callback)` hiện một form với message `html`, một input field và các nút `OK/CANCEL`.

- Người dùng phải nhập gì đó vào trường text và nhấn `Enter` hoặc nút OK, sau đó `callback(value)` được gọi với giá trị họ đã nhập.
- Ngược lại, nếu người dùng nhấn `Esc` hoặc CANCEL, thì `callback(null)` được gọi.

Trong cả hai trường hợp, điều đó kết thúc quá trình nhập và xóa form.

Yêu cầu:

- Form phải ở giữa cửa sổ.
- Form là *modal*. Nói cách khác, không tương tác với phần còn lại của trang được cho đến khi người dùng đóng nó.
- Khi form được hiện, focus phải nằm trong `<input>` để người dùng sẵn sàng.
- Các phím `Tab`/`Shift+Tab` phải chuyển focus giữa các trường form, không cho phép nó thoát sang các phần tử trang khác.

Ví dụ usage:

```
showPrompt("Enter something<br>...smart :)", function(value) {
  alert(value);
});
```

Demo trong iframe:

P.S. Document source có HTML/CSS cho form với fixed positioning, nhưng tùy bạn làm cho nó modal.

[Mở sandbox cho bài tập.](https://plnkr.co/edit/B4sj7P5kInEWro90?p=preview)

solution

Modal window có thể được triển khai bằng một `<div id="cover-div">` nửa trong suốt che toàn bộ cửa sổ, như sau:

```
#cover-div {
  position: fixed;
  top: 0;
  left: 0;
  z-index: 9000;
  width: 100%;
  height: 100%;
  background-color: gray;
  opacity: 0.3;
}
```

Bởi vì `<div>` che mọi thứ, nó nhận tất cả click, không phải trang bên dưới nó.

Ngoài ra ta có thể ngăn page scroll bằng cách đặt `body.style.overflowY='hidden'`.

Form không nên ở trong `<div>`, mà cạnh đó, vì ta không muốn nó có `opacity`.

[Mở giải pháp trong sandbox.](https://plnkr.co/edit/O6VaMA3iVnSVwFqm?p=preview)