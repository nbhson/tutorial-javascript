# Focus: focus/blur

> Source: [https://javascript.info/focus-blur](https://javascript.info/focus-blur)

<!-- fetched: 2026-09-14 -->

Một phần tử nhận focus khi người dùng click vào nó hoặc dùng phím `Tab` trên bàn phím. Cũng có thuộc tính HTML `autofocus` đặt focus vào một phần tử mặc định khi trang tải và các cách khác để nhận focus.

Focus vào một phần tử thường có nghĩa là "chuẩn bị chấp nhận dữ liệu ở đây", đó là lúc ta có thể chạy code để khởi tạo chức năng cần thiết.

Lúc mất focus ("blur") thậm chí còn quan trọng hơn. Đó là khi người dùng click vào nơi khác hoặc nhấn `Tab` để chuyển sang trường form tiếp theo, hoặc có các cách khác.

Mất focus thường có nghĩa là "dữ liệu đã được nhập", nên ta có thể chạy code để kiểm tra hoặc thậm chí lưu nó lên server và v.v.

Có những điểm đặc biệt quan trọng khi làm việc với sự kiện focus. Chúng ta sẽ làm tốt nhất để giải thích chúng.

## [Sự kiện focus/blur](#events-focus-blur)

Sự kiện `focus` được gọi khi focus vào, và `blur` – khi phần tử mất focus.

Hãy dùng chúng để validate một trường input.

Trong ví dụ dưới đây:

- Handler `blur` kiểm tra xem trường có nhập email hay không, và nếu không – hiện lỗi.
- Handler `focus` ẩn thông báo lỗi (khi `blur` sẽ được kiểm tra lại):

```
<style>
  .invalid { border-color: red; }
  #error { color: red }
</style>

Your email please: <input type="email" id="input">

<div id="error"></div>

<script>
input.onblur = function() {
  if (!input.value.includes('@')) { // không phải email
    input.classList.add('invalid');
    error.innerHTML = 'Please enter a correct email.'
  }
};

input.onfocus = function() {
  if (this.classList.contains('invalid')) {
    // bỏ trạng thái "lỗi", vì người dùng muốn nhập lại
    this.classList.remove('invalid');
    error.innerHTML = "";
  }
};
</script>
```

HTML hiện đại cho phép ta thực hiện nhiều validation bằng các thuộc tính input: `required`, `pattern` và v.v. Và đôi khi chúng chính là thứ ta cần. JavaScript có thể dùng khi ta muốn linh hoạt hơn. Ngoài ra ta có thể tự động gửi giá trị đã thay đổi lên server nếu nó hợp lệ.

## [Phương thức focus/blur](#methods-focus-blur)

Phương thức `elem.focus()` và `elem.blur()` đặt/bỏ focus trên phần tử.

Ví dụ, hãy làm cho người dùng không thể rời khỏi input nếu giá trị không hợp lệ:

```
<style>
  .error {
    background: red;
  }
</style>

Your email please: <input type="email" id="input">
<input type="text" style="width:220px" placeholder="make email invalid and try to focus here">

<script>
  input.onblur = function() {
    if (!this.value.includes('@')) { // không phải email
      // hiện lỗi
      this.classList.add("error");
      // và đặt lại focus
      input.focus();
    } else {
      this.classList.remove("error");
    }
  };
</script>
```

Nó hoạt động trên mọi trình duyệt trừ Firefox ([bug](https://bugzilla.mozilla.org/show_bug.cgi?id=53579)).

Nếu ta nhập gì đó vào input rồi thử dùng `Tab` hoặc click ra khỏi `<input>`, thì `onblur` sẽ trả focus lại.

Lưu ý rằng ta không thể "ngăn mất focus" bằng cách gọi `event.preventDefault()` trong `onblur`, vì `onblur` chạy *sau* khi phần tử đã mất focus.

Trong thực tế, ta nên cân nhắc kỹ trước khi cài đặt thứ gì đó như vậy, vì ta thường *nên hiện lỗi* cho người dùng, nhưng *không nên ngăn tiến trình* của họ khi điền form. Họ có thể muốn điền các trường khác trước.

Mất focus do JavaScript

Mất focus có thể xảy ra vì nhiều lý do.

Một trong số đó là khi người dùng click vào nơi khác. Nhưng cũng có thể JavaScript tự gây ra nó, ví dụ:

- `alert` di chuyển focus vào chính nó, nên nó gây mất focus tại phần tử (`blur` event), và khi `alert` bị đóng, focus quay lại (`focus` event).
- Nếu một phần tử bị xóa khỏi DOM, thì nó cũng gây mất focus. Nếu nó được chèn lại sau, thì focus không quay lại.

Những đặc điểm này đôi khi khiến handler `focus/blur` hoạt động sai – kích hoạt khi không cần.

Cách tốt nhất là cẩn trọng khi dùng các sự kiện này. Nếu ta muốn theo dõi focus-loss do người dùng khởi tạo, thì nên tránh tự gây ra nó.

## [Cho phép focus vào mọi phần tử: tabindex](#allow-focusing-on-any-element-tabindex)

Theo mặc định, nhiều phần tử không hỗ trợ focus.

Danh sách thay đổi một chút giữa các trình duyệt, nhưng một điều luôn đúng: `focus/blur` hỗ trợ được đảm bảo cho các phần tử mà người dùng có thể tương tác: `<button>`, `<input>`, `<select>`, `<a>` và v.v.

Ngược lại, các phần tử tồn tại để định dạng thứ gì đó, chẳng hạn `<div>`, `<span>`, `<table>` – không thể focus theo mặc định. Phương thức `elem.focus()` không hoạt động trên chúng, và sự kiện `focus/blur` không bao giờ được kích hoạt.

Điều này có thể thay đổi bằng thuộc tính HTML `tabindex`.

Bất kỳ phần tử nào cũng trở thành focusable nếu có `tabindex`. Giá trị của thuộc tính là số thứ tự của phần tử khi `Tab` (hoặc thứ gì đó tương tự) được dùng để chuyển đổi giữa chúng.

Nghĩa là: nếu ta có hai phần tử, phần tử đầu có `tabindex="1"`, và phần tử thứ hai có `tabindex="2"`, thì nhấn `Tab` trong khi ở phần tử đầu – sẽ di chuyển focus sang phần tử thứ hai.

Thứ tự chuyển đổi: các phần tử có `tabindex` từ `1` trở lên đi trước (theo thứ tự `tabindex`), rồi đến các phần tử không có `tabindex` (ví dụ `<input>` thường).

Các phần tử không có `tabindex` tương ứng được chuyển đổi theo thứ tự nguồn trong document (thứ tự mặc định).

Có hai giá trị đặc biệt:

- `tabindex="0"` đặt phần tử vào cùng nhóm những phần tử không có `tabindex`. Nghĩa là, khi ta chuyển đổi phần tử, các phần tử có `tabindex=0` đi sau các phần tử có `tabindex ≥ 1`.

  Thường dùng để làm phần tử focusable, nhưng giữ thứ tự chuyển đổi mặc định. Để phần tử trở thành một phần của form ngang hàng với `<input>`.
- `tabindex="-1"` chỉ cho phép focus theo chương trình lên phần tử. Phím `Tab` bỏ qua các phần tử như vậy, nhưng phương thức `elem.focus()` hoạt động.

Ví dụ, đây là một danh sách. Click item đầu tiên và nhấn `Tab`:

```
Click the first item and press Tab. Keep track of the order. Please note that many subsequent Tabs can move the focus out of the iframe in the example.
<ul>
  <li tabindex="1">One</li>
  <li tabindex="0">Zero</li>
  <li tabindex="2">Two</li>
  <li tabindex="-1">Minus one</li>
</ul>

<style>
  li { cursor: pointer; }
  :focus { outline: 1px dashed green; }
</style>
```

Thứ tự như vậy: `1 - 2 - 0`. Thông thường, `<li>` không hỗ trợ focus, nhưng `tabindex` bật hoàn toàn nó, cùng với events và styling bằng `:focus`.

Thuộc tính `elem.tabIndex` cũng hoạt động

Ta có thể thêm `tabindex` từ JavaScript bằng cách dùng thuộc tính `elem.tabIndex`. Cái đó có cùng hiệu ứng.

## [Delegation: focusin/focusout](#delegation-focusin-focusout)

Sự kiện `focus` và `blur` không bubble.

Ví dụ, ta không thể đặt `onfocus` trên `<form>` để highlight nó, như sau:

```
<!-- khi focus vào form -- thêm class -->
<form onfocus="this.className='focused'">
  <input type="text" name="name" value="Name">
  <input type="text" name="surname" value="Surname">
</form>

<style> .focused { outline: 1px solid red; } </style>
```

Ví dụ trên không hoạt động, vì khi người dùng focus vào một `<input>`, sự kiện `focus` chỉ kích hoạt trên input đó. Nó không bubble lên. Vậy `form.onfocus` không bao giờ kích hoạt.

Có hai giải pháp.

Thứ nhất, có một tính năng lịch sử kỳ lạ: `focus/blur` không bubble lên, nhưng propagate down trong capturing phase.

Điều này sẽ hoạt động:

```
<form id="form">
  <input type="text" name="name" value="Name">
  <input type="text" name="surname" value="Surname">
</form>

<style> .focused { outline: 1px solid red; } </style>

<script>
  // đặt handler trên capturing phase (tham số cuối true)
  form.addEventListener("focus", () => form.classList.add('focused'), true);
  form.addEventListener("blur", () => form.classList.remove('focused'), true);
</script>
```

Thứ hai, có các sự kiện `focusin` và `focusout` – giống hệt `focus/blur`, nhưng chúng bubble.

Lưu ý rằng chúng phải được gán bằng `elem.addEventListener`, không phải `on<event>`.

Vậy đây là một biến thể hoạt động khác:

```
<form id="form">
  <input type="text" name="name" value="Name">
  <input type="text" name="surname" value="Surname">
</form>

<style> .focused { outline: 1px solid red; } </style>

<script>
  form.addEventListener("focusin", () => form.classList.add('focused'));
  form.addEventListener("focusout", () => form.classList.remove('focused'));
</script>
```

## [Tóm tắt](#summary)

Sự kiện `focus` và `blur` kích hoạt trên phần tử focus/mất focus.

Đặc điểm của chúng:

- Chúng không bubble. Có thể dùng capturing state hoặc `focusin/focusout` thay thế.
- Hầu hết các phần tử không hỗ trợ focus theo mặc định. Dùng `tabindex` để làm bất kỳ thứ gì focusable.

Phần tử đang được focus có sẵn trong `document.activeElement`.

---

---

## Bài tập

## [Tasks](#tasks)

### [Editable div](#editable-div)

importance: 5

Tạo một `<div>` chuyển thành `<textarea>` khi click.

Textarea cho phép chỉnh sửa HTML trong `<div>`.

Khi người dùng nhấn `Enter` hoặc mất focus, `<textarea>` chuyển lại thành `<div>`, và nội dung của nó trở thành HTML trong `<div>`.

[Demo trong cửa sổ mới](https://en.js.cx/task/editable-div/solution/)

[Mở sandbox cho bài tập.](https://plnkr.co/edit/NFAJGdDJHcuYvHvN?p=preview)

solution

[Mở giải pháp trong sandbox.](https://plnkr.co/edit/c9KqjiReHjcIkGvo?p=preview)

### [Edit TD on click](#edit-td-on-click)

importance: 5

Làm cho các ô table có thể edit khi click.

- Khi click – ô phải trở thành "editable" (textarea xuất hiện bên trong), ta có thể thay đổi HTML. Không có resize, tất cả geometry phải giữ nguyên.
- Các nút OK và CANCEL xuất hiện bên dưới ô để kết thúc/hủy chỉnh sửa.
- Chỉ một ô có thể editable tại một thời điểm. Trong khi một `<td>` ở "edit mode", các click vào ô khác bị bỏ qua.
- Bảng có thể có nhiều ô. Dùng event delegation.

Demo:

[Mở sandbox cho bài tập.](https://plnkr.co/edit/Vz4D06ovppkdjBED?p=preview)

solution

1. Khi click – thay thế `innerHTML` của ô bằng `<textarea>` với cùng kích thước và không có border. Có thể dùng JavaScript hoặc CSS để đặt kích thước đúng.
2. Đặt `textarea.value` bằng `td.innerHTML`.
3. Focus vào textarea.
4. Hiện các nút OK/CANCEL dưới ô, xử lý click trên chúng.

[Mở giải pháp trong sandbox.](https://plnkr.co/edit/Lnr1JsNqWZe8KpeL?p=preview)

### [Keyboard-driven mouse](#keyboard-driven-mouse)

importance: 4

Focus vào chuột. Sau đó dùng phím mũi tên để di chuyển nó:

[Demo trong cửa sổ mới](https://en.js.cx/task/keyboard-mouse/solution/)

P.S. Không đặt event handler ở đâu ngoài phần tử `#mouse`.

P.P.S. Không sửa HTML/CSS, phương pháp phải là tổng quát và hoạt động với bất kỳ phần tử nào.

[Mở sandbox cho bài tập.](https://plnkr.co/edit/KWeoX4it2LwOhRg3?p=preview)

solution

Ta có thể dùng `mouse.onclick` để xử lý click và làm chuột "di chuyển được" với `position:fixed`, rồi `mouse.onkeydown` để xử lý phím mũi tên.

Lưu ý là `keydown` chỉ kích hoạt trên các phần tử có focus. Vậy ta cần thêm `tabindex` vào phần tử. Vì bị cấm sửa HTML, ta có thể dùng thuộc tính `mouse.tabIndex` để làm điều đó.

P.S. Ta cũng có thể thay `mouse.onclick` bằng `mouse.onfocus`.

[Mở giải pháp trong sandbox.](https://plnkr.co/edit/FzIo4brtQ43K5fGI?p=preview)