# Các thuộc tính và phương thức của form

> Source: [https://javascript.info/form-elements](https://javascript.info/form-elements)

<!-- fetched: 2026-09-14 -->

Form và các phần tử điều khiển, chẳng hạn như `<input>` có nhiều thuộc tính và sự kiện đặc biệt.

Làm việc với form sẽ thuận tiện hơn nhiều khi chúng ta nắm được chúng.

## [Điều hướng: form và các phần tử](#navigation-form-and-elements)

Các form trong document là thành viên của bộ sưu tập đặc biệt `document.forms`.

Đây là một "named collection" (bộ sưu tập được đặt tên): nó vừa được đặt tên vừa có thứ tự. Chúng ta có thể dùng cả tên hoặc số thứ tự trong document để lấy form.

```
document.forms.my; // form có name="my"
document.forms[0]; // form đầu tiên trong document
```

Khi đã có form, thì bất kỳ phần tử nào cũng có sẵn trong bộ sưu tập đặt tên `form.elements`.

Ví dụ:

```
<form name="my">
  <input name="one" value="1">
  <input name="two" value="2">
</form>

<script>
  // lấy form
  let form = document.forms.my; // phần tử <form name="my">

  // lấy phần tử
  let elem = form.elements.one; // phần tử <input name="one">

  alert(elem.value); // 1
</script>
```

Có thể có nhiều phần tử cùng tên. Điều này thường gặp với radio button và checkbox.

Trong trường hợp đó, `form.elements[name]` là một *collection* (bộ sưu tập). Ví dụ:

```
<form>
  <input type="radio" name="age" value="10">
  <input type="radio" name="age" value="20">
</form>

<script>
let form = document.forms[0];

let ageElems = form.elements.age;

alert(ageElems[0]); // [object HTMLInputElement]
</script>
```

Các thuộc tính điều hướng này không phụ thuộc vào cấu trúc thẻ. Tất cả các phần tử điều khiển, bất kể chúng sâu đến đâu trong form, đều có sẵn trong `form.elements`.

Fieldsets như "subforms" (form con)

Một form có thể chứa một hoặc nhiều phần tử `<fieldset>` bên trong. Chúng cũng có thuộc tính `elements` liệt kê các điều khiển form bên trong.

Ví dụ:

```
<body>
  <form id="form">
    <fieldset name="userFields">
      <legend>info</legend>
      <input name="login" type="text">
    </fieldset>
  </form>

  <script>
    alert(form.elements.login); // <input name="login">

    let fieldset = form.elements.userFields;
    alert(fieldset); // HTMLFieldSetElement

    // có thể lấy input theo tên từ cả form và fieldset
    alert(fieldset.elements.login == form.elements.login); // true
  </script>
</body>
```

Ký pháp ngắn gọn: `form.name`

Có một ký pháp ngắn gọn hơn: ta có thể truy cập phần tử như `form[index/name]`.

Nói cách khác, thay vì `form.elements.login` ta có thể viết `form.login`.

Cách đó cũng hoạt động, nhưng có một vấn đề nhỏ: nếu truy cập một phần tử, rồi thay đổi `name` của nó, thì nó vẫn có sẵn dưới tên cũ (cũng như tên mới).

Dễ thấy trong ví dụ:

```
<form id="form">
  <input name="login">
</form>

<script>
  alert(form.elements.login == form.login); // true, cùng một <input>

  form.login.name = "username"; // thay đổi name của input

  // form.elements cập nhật tên:
  alert(form.elements.login); // undefined
  alert(form.elements.username); // input

  // form cho phép cả hai tên: tên mới và tên cũ
  alert(form.username == form.login); // true
</script>
```

Điều đó thường không gây vấn đề, vì chúng ta hiếm khi thay đổi tên của các phần tử form.

## [Tham chiếu ngược: element.form](#backreference-element-form)

Đối với bất kỳ phần tử nào, form có sẵn trong `element.form`. Vậy form tham chiếu đến tất cả các phần tử, và các phần tử tham chiếu ngược về form.

Hình minh họa:

![](/article/form-elements/form-navigation.svg)

Ví dụ:

```
<form id="form">
  <input type="text" name="login">
</form>

<script>
  // form -> element
  let login = form.login;

  // element -> form
  alert(login.form); // HTMLFormElement
</script>
```

## [Các phần tử form](#form-elements)

Hãy nói về các điều khiển form.

### [input và textarea](#input-and-textarea)

Ta có thể truy cập giá trị của chúng bằng `input.value` (chuỗi) hoặc `input.checked` (boolean) cho checkbox và radio button.

Như sau:

```
input.value = "Giá trị mới";
textarea.value = "Văn bản mới";

input.checked = true; // cho checkbox hoặc radio button
```

Dùng `textarea.value`, không dùng `textarea.innerHTML`

Lưu ý rằng dù `<textarea>...</textarea>` giữ giá trị dưới dạng HTML lồng nhau, ta không bao giờ nên dùng `textarea.innerHTML` để truy cập nó.

Nó chỉ lưu HTML ban đầu trên trang, không phải giá trị hiện tại.

### [select và option](#select-and-option)

Phần tử `<select>` có 3 thuộc tính quan trọng:

1. `select.options` – tập hợp các phần tử con `<option>`,
2. `select.value` – *giá trị* của `<option>` đang được chọn,
3. `select.selectedIndex` – *số thứ tự* của `<option>` đang được chọn.

Chúng cung cấp ba cách khác nhau để đặt giá trị cho `<select>`:

1. Tìm phần tử `<option>` tương ứng (ví dụ trong `select.options`) và đặt `option.selected` thành `true`.
2. Nếu biết giá trị mới: đặt `select.value` thành giá trị mới.
3. Nếu biết số thứ tự option mới: đặt `select.selectedIndex` thành số đó.

Ví dụ về cả ba phương pháp:

```
<select id="select">
  <option value="apple">Apple</option>
  <option value="pear">Pear</option>
  <option value="banana">Banana</option>
</select>

<script>
  // cả ba dòng làm giống nhau
  select.options[2].selected = true;
  select.selectedIndex = 2;
  select.value = 'banana';
  // lưu ý: options bắt đầu từ 0, nên index 2 nghĩa là option thứ 3.
</script>
```

Khác với hầu hết các điều khiển khác, `<select>` cho phép chọn nhiều option cùng lúc nếu có thuộc tính `multiple`. Thuộc tính này ít khi dùng.

Đối với nhiều giá trị được chọn, dùng cách đầu tiên để đặt giá trị: thêm/xóa thuộc tính `selected` từ các phần tử con `<option>`.

Ví dụ cách lấy các giá trị được chọn từ multi-select:

```
<select id="select" multiple>
  <option value="blues" selected>Blues</option>
  <option value="rock" selected>Rock</option>
  <option value="classic">Classic</option>
</select>

<script>
  // lấy tất cả giá trị được chọn từ multi-select
  let selected = Array.from(select.options)
    .filter(option => option.selected)
    .map(option => option.value);

  alert(selected); // blues,rock
</script>
```

Đặc tả đầy đủ của phần tử `<select>` có tại <https://html.spec.whatwg.org/multipage/forms.html#the-select-element>.

### [new Option](#new-option)

Trong [đặc tả](https://html.spec.whatwg.org/multipage/forms.html#the-option-element) có cú pháp ngắn gọn hay để tạo phần tử `<option>`:

```
option = new Option(text, value, defaultSelected, selected);
```

Cú pháp này là tùy chọn. Ta có thể dùng `document.createElement('option')` và đặt thuộc tính thủ công. Tuy nhiên, nó có thể ngắn gọn hơn, nên đây là các tham số:

- `text` – văn bản bên trong option,
- `value` – giá trị option,
- `defaultSelected` – nếu `true`, thì thuộc tính HTML `selected` được tạo,
- `selected` – nếu `true`, thì option được chọn.

Khác biệt giữa `defaultSelected` và `selected` là `defaultSelected` đặt thuộc tính HTML (có thể lấy bằng `option.getAttribute('selected')`), còn `selected` đặt option có được chọn hay không.

Trong thực tế, thường nên đặt *cả hai* giá trị thành `true` hoặc `false`. (Hoặc đơn giản là bỏ qua chúng; cả hai mặc định đều là `false`.)

Ví dụ, một option "chưa chọn" mới:

```
let option = new Option("Text", "value");
// tạo <option value="value">Text</option>
```

Cùng option đó, nhưng đã chọn:

```
let option = new Option("Text", "value", true, true);
```

Các phần tử Option có các thuộc tính:

`option.selected`
:   Option có được chọn hay không.

`option.index`
:   Số thứ tự của option giữa các option khác trong `<select>` của nó.

`option.text`
:   Nội dung text của option (người dùng thấy).

## [Tham khảo](#references)

- Đặc tả: <https://html.spec.whatwg.org/multipage/forms.html>.

## [Tóm tắt](#summary)

Điều hướng form:

`document.forms`
:   Form có sẵn trong `document.forms[name/index]`.

`form.elements`
:   Các phần tử form có sẵn trong `form.elements[name/index]`, hoặc chỉ dùng `form[name/index]`. Thuộc tính `elements` cũng hoạt động cho `<fieldset>`.

`element.form`
:   Các phần tử tham chiếu form của chúng trong thuộc tính `form`.

Giá trị có sẵn trong `input.value`, `textarea.value`, `select.value`, v.v. (Đối với checkbox và radio button, dùng `input.checked` để xác định xem giá trị có được chọn hay không.)

Đối với `<select>`, cũng có thể lấy giá trị bằng chỉ số `select.selectedIndex` hoặc qua tập hợp options `select.options`.

Đây là những kiến thức cơ bản để bắt đầu làm việc với form. Chúng ta sẽ gặp nhiều ví dụ hơn trong các chương sau.

Trong chương tiếp theo chúng ta sẽ nói về sự kiện `focus` và `blur` có thể xảy ra trên bất kỳ phần tử nào, nhưng chủ yếu được xử lý trên form.

---

---

## Các bài tập

## [Tasks](#tasks)

### [Thêm option vào select](#add-an-option-to-select)

importance: 5

Có một `<select>`:

```
<select id="genres">
  <option value="rock">Rock</option>
  <option value="blues" selected>Blues</option>
</select>
```

Dùng JavaScript để:

1. Hiển thị giá trị và text của option đang chọn.
2. Thêm option: `<option value="classic">Classic</option>`.
3. Làm cho nó được chọn.

Lưu ý, nếu làm đúng hết, alert sẽ hiển thị `blues`.

solution

Giải pháp, từng bước:

```
<select id="genres">
  <option value="rock">Rock</option>
  <option value="blues" selected>Blues</option>
</select>

<script>
  // 1)
  let selectedOption = genres.options[genres.selectedIndex];
  alert( selectedOption.value );

  // 2)
  let newOption = new Option("Classic", "classic");
  genres.append(newOption);

  // 3)
  newOption.selected = true;
</script>
```