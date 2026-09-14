# Sự kiện: change, input, cut, copy, paste

> Source: [https://javascript.info/events-change-input](https://javascript.info/events-change-input)

<!-- fetched: 2026-09-14 -->

Hãy tìm hiểu các sự kiện khác nhau đi kèm việc cập nhật dữ liệu.

## [Sự kiện: change](#event-change)

Sự kiện `change` kích hoạt khi phần tử đã hoàn tất thay đổi.

Đối với text input, điều đó có nghĩa là sự kiện xảy ra khi nó mất focus.

Ví dụ, trong khi ta đang gõ trong trường text bên dưới – không có sự kiện. Nhưng khi ta di chuyển focus đi nơi khác, ví dụ click vào một button – sẽ có sự kiện `change`:

```
<input type="text" onchange="alert(this.value)">
<input type="button" value="Button">
```

Đối với các phần tử khác: `select`, `input type=checkbox/radio` nó kích hoạt ngay sau khi selection thay đổi:

```
<select onchange="alert(this.value)">
  <option value="">Select something</option>
  <option value="1">Option 1</option>
  <option value="2">Option 2</option>
  <option value="3">Option 3</option>
</select>
```

## [Sự kiện: input](#event-input)

Sự kiện `input` kích hoạt mỗi lần sau khi giá trị bị sửa đổi bởi người dùng.

Khác với keyboard events, nó kích hoạt sau mọi thay đổi giá trị, kể cả những thay đổi không liên quan đến hành động bàn phím: paste bằng chuột hoặc dùng speech recognition để nói văn bản.

Ví dụ:

```
<input type="text" id="input"> oninput: <span id="result"></span>
<script>
  input.oninput = function() {
    result.innerHTML = input.value;
  };
</script>
```

Nếu ta muốn xử lý mọi thay đổi của `<input>`, thì đây là lựa chọn tốt nhất.

Ngược lại, sự kiện `input` không kích hoạt khi gõ bàn phím và các hành động khác không liên quan đến thay đổi giá trị, ví dụ nhấn các phím mũi tên `⇦` `⇨` trong khi đang trong input.

Không thể ngăn chặn gì trong `oninput`

Sự kiện `input` xảy ra sau khi giá trị đã bị sửa đổi.

Vậy ta không thể dùng `event.preventDefault()` ở đó – quá muộn, sẽ không có hiệu ứng.

## [Sự kiện: cut, copy, paste](#events-cut-copy-paste)

Các sự kiện này xảy ra khi cắt/sao/chép/dán giá trị.

Chúng thuộc lớp [ClipboardEvent](https://www.w3.org/TR/clipboard-apis/#clipboard-event-interfaces) và cung cấp quyền truy cập vào dữ liệu bị cắt/sao/chép/dán.

Ta cũng có thể dùng `event.preventDefault()` để hủy hành động, sau đó sẽ không có gì được sao chép/dán.

Ví dụ, đoạn code dưới đây ngăn chặn mọi sự kiện `cut/copy/paste` và hiện text ta đang cố gắng cut/copy/paste:

```
<input type="text" id="input">
<script>
  input.onpaste = function(event) {
    alert("paste: " + event.clipboardData.getData('text/plain'));
    event.preventDefault();
  };

  input.oncut = input.oncopy = function(event) {
    alert(event.type + '-' + document.getSelection());
    event.preventDefault();
  };
</script>
```

Lưu ý: bên trong handler sự kiện `cut` và `copy`, việc gọi `event.clipboardData.getData(...)` trả về chuỗi rỗng. Đó là vì về mặt kỹ thuật, dữ liệu chưa có trong clipboard. Nếu ta dùng `event.preventDefault()` nó sẽ không được sao chép.

Vậy ví dụ trên dùng `document.getSelection()` để lấy text được chọn. Bạn có thể tìm thêm chi tiết về document selection trong bài viết [Selection and Range](/selection-range).

Có thể cut/paste không chỉ text, mà mọi thứ. Ví dụ, ta có thể copy một file trong OS file manager, và paste nó.

Đó là vì `clipboardData` triển khai interface `DataTransfer`, thường được dùng cho drag'n'drop và copy/paste. Hơi ngoài phạm vi của chúng ta bây giờ, nhưng bạn có thể tìm các phương thức của nó trong [DataTransfer specification](https://html.spec.whatwg.org/multipage/dnd.html#the-datatransfer-interface).

Ngoài ra, có một async API bổ sung để truy cập clipboard: `navigator.clipboard`. Thêm thông tin trong đặc tả [Clipboard API and events](https://www.w3.org/TR/clipboard-apis/), [không được Firefox hỗ trợ](https://caniuse.com/async-clipboard).

### [Safety restrictions](#safety-restrictions)

Clipboard là thứ "toàn cục" ở mức OS. Một người dùng có thể chuyển đổi giữa các ứng dụng khác nhau, copy/paste các thứ khác nhau, và một trang browser không nên thấy tất cả những điều đó.

Vậy hầu hết các trình duyệt chỉ cho phép đọc/ghi seamless access vào clipboard trong phạm vi của một số hành động cụ thể của người dùng, chẳng hạn copy/paste v.v.

Bị cấm tạo các sự kiện clipboard "custom" bằng `dispatchEvent` trong mọi trình duyệt trừ Firefox. Và ngay cả khi ta dispatch được event như vậy, đặc tả nói rõ rằng các event "synthetic" như vậy không được cung cấp quyền truy cập vào clipboard.

Ngay cả nếu ai đó quyết định lưu `event.clipboardData` trong một event handler, rồi truy cập nó sau – điều đó cũng không hoạt động.

Nhắc lại, [event.clipboardData](https://www.w3.org/TR/clipboard-apis/#clipboardevent-clipboarddata) chỉ hoạt động trong ngữ cảnh của user-initiated event handlers.

Mặt khác, [navigator.clipboard](https://www.w3.org/TR/clipboard-apis/#h-navigator-clipboard) là API gần đây hơn, dùng cho bất kỳ ngữ cảnh nào. Nó yêu cầu permission của người dùng nếu cần.

## [Tóm tắt](#summary)

Các sự kiện thay đổi dữ liệu:

| Event | Description | Specials |
| --- | --- | --- |
| `change` | Giá trị đã thay đổi. | Đối với text inputs, kích hoạt khi mất focus. |
| `input` | Đối với text inputs trên mọi thay đổi. | Kích hoạt ngay lập tức khác với `change`. |
| `cut/copy/paste` | Hành động cut/copy/paste. | Hành động có thể bị ngăn. Thuộc tính `event.clipboardData` cho quyền truy cập vào clipboard. Mọi trình duyệt trừ Firefox cũng hỗ trợ `navigator.clipboard`. |

---

---

## Bài tập

## [Tasks](#tasks)

### [Deposit calculator](#deposit-calculator)

importance: 5

Tạo một giao diện cho phép nhập số tiền gửi ngân hàng và lãi suất, sau đó tính toán sẽ có bao nhiêu sau các khoảng thời gian cho trước.

Đây là demo:

Mọi thay đổi input phải được xử lý ngay lập tức.

Công thức là:

```
// initial: số tiền ban đầu
// interest: ví dụ 0.05 nghĩa là 5% mỗi năm
// years: bao nhiêu năm để chờ
let result = Math.round(initial * (1 + interest) ** years);
```

[Mở sandbox cho bài tập.](https://plnkr.co/edit/UtN5jTOKRwNl9ke2?p=preview)

solution

[Mở giải pháp trong sandbox.](https://plnkr.co/edit/y6KtVv6LsK2xfVsB?p=preview)