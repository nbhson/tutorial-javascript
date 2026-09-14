# Tìm kiếm: getElement*, querySelector*

> Nguồn: [https://javascript.info/searching-elements-dom](https://javascript.info/searching-elements-dom)

<!-- fetched: 2026-09-14 -->

Các thuộc tính điều hướng DOM rất tuyệt khi các phần tử ở gần nhau. Nhưng nếu chúng không gần thì sao? Làm thế nào để lấy một phần tử tùy ý của trang?

Có các phương thức tìm kiếm bổ sung cho mục đích đó.

## [document.getElementById hoặc chỉ id](#document-getelementbyid-or-just-id)

Nếu một phần tử có thuộc tính `id`, chúng ta có thể lấy phần tử bằng phương thức `document.getElementById(id)`, bất kể nó ở đâu.

Ví dụ:

```
<div id="elem">
  <div id="elem-content">Element</div>
</div>

<script>
  // lấy phần tử
  let elem = document.getElementById('elem');

  // làm cho nền của nó có màu đỏ
  elem.style.background = 'red';
</script>
```

Ngoài ra, có một biến toàn cục được đặt tên theo `id` tham chiếu đến phần tử:

```
<div id="elem">
  <div id="elem-content">Element</div>
</div>

<script>
  // elem là tham chiếu đến DOM-element với id="elem"
  elem.style.background = 'red';

  // id="elem-content" có dấu gạch ngang bên trong, nên không thể là tên biến
  // ...nhưng chúng ta có thể truy cập nó bằng dấu ngoặc vuông: window['elem-content']
</script>
```

…Trừ khi chúng ta khai báo một biến JavaScript có cùng tên, thì nó sẽ ưu tiên hơn:

```
<div id="elem"></div>

<script>
  let elem = 5; // bây giờ elem là 5, không phải tham chiếu đến <div id="elem">
  alert(elem); // 5
</script>
```

Xin đừng sử dụng biến toàn cục đặt tên theo id để truy cập phần tử

Hành vi này được mô tả [trong đặc tả](https://html.spec.whatwg.org/multipage/window-object.html#named-access-on-the-window-object), nhưng nó chủ yếu được hỗ trợ để tương thích.

Trình duyệt cố gắng giúp chúng ta bằng cách trộn không gian tên của JS và DOM. Điều đó ổn đối với các tập lệnh đơn giản, được nhúng vào HTML, nhưng nhìn chung không phải là điều tốt. Có thể có xung đột tên. Ngoài ra, khi ai đó đọc mã JS và không có HTML trong tầm nhìn, thì không rõ biến đến từ đâu.

Trong hướng dẫn này, chúng ta sử dụng `id` để tham chiếu trực tiếp đến một phần tử cho ngắn gọn, khi rõ ràng phần tử đến từ đâu.

Trong thực tế, `document.getElementById` là phương thức được ưu tiên.

`id` phải duy nhất

`id` phải duy nhất. Chỉ có thể có một phần tử trong tài liệu với `id` đã cho.

Nếu có nhiều phần tử có cùng `id`, thì hành vi của các phương thức sử dụng nó sẽ không dự đoán được, ví dụ `document.getElementById` có thể trả về bất kỳ phần tử nào trong số đó một cách ngẫu nhiên. Vì vậy, xin vui lòng tuân thủ quy tắc và giữ `id` duy nhất.

Chỉ `document.getElementById`, không phải `anyElem.getElementById`

Phương thức `getElementById` chỉ có thể được gọi trên đối tượng `document`. Nó tìm `id` đã cho trong toàn bộ tài liệu.

## [querySelectorAll](#querySelectorAll)

Cho đến nay, phương thức đa dụng nhất, `elem.querySelectorAll(css)` trả về tất cả các phần tử bên trong `elem` khớp với bộ chọn CSS đã cho.

Ở đây chúng ta tìm tất cả các phần tử `<li>` là con cuối cùng:

```
<ul>
  <li>The</li>
  <li>test</li>
</ul>
<ul>
  <li>has</li>
  <li>passed</li>
</ul>
<script>
  let elements = document.querySelectorAll('ul > li:last-child');

  for (let elem of elements) {
    alert(elem.innerHTML); // "test", "passed"
  }
</script>
```

Phương thức này thực sự mạnh mẽ, vì bất kỳ bộ chọn CSS nào cũng có thể được sử dụng.

Có thể sử dụng pseudo-classes

Các pseudo-class trong bộ chọn CSS như `:hover` và `:active` cũng được hỗ trợ. Ví dụ, `document.querySelectorAll(':hover')` sẽ trả về bộ sưu tập với các phần tử mà con trỏ đang nằm trên đó (theo thứ tự lồng nhau: từ `<html>` ngoài cùng đến phần tử lồng sâu nhất).

## [querySelector](#querySelector)

Lời gọi `elem.querySelector(css)` trả về phần tử đầu tiên khớp với bộ chọn CSS đã cho.

Nói cách khác, kết quả giống như `elem.querySelectorAll(css)[0]`, nhưng cái sau tìm kiếm *tất cả* các phần tử và chọn một, trong khi `elem.querySelector` chỉ tìm một. Vì vậy, nó nhanh hơn và cũng ngắn hơn để viết.

## [matches](#matches)

Các phương thức trước đó đang tìm kiếm DOM.

[elem.matches(css)](https://dom.spec.whatwg.org/#dom-element-matches) không tìm kiếm gì, nó chỉ kiểm tra xem `elem` có khớp với bộ chọn CSS đã cho hay không. Nó trả về `true` hoặc `false`.

Phương thức rất hữu ích khi chúng ta đang lặp qua các phần tử (như trong một mảng hoặc thứ gì đó) và cố gắng lọc ra những phần tử quan tâm đến chúng ta.

Ví dụ:

```
<a href="http://example.com/file.zip">...</a>
<a href="http://ya.ru">...</a>

<script>
  // có thể là bất kỳ bộ sưu tập nào thay thế cho document.body.children
  for (let elem of document.body.children) {
    if (elem.matches('a[href$="zip"]')) {
      alert("The archive reference: " + elem.href );
    }
  }
</script>
```

## [closest](#closest)

*Các tổ tiên* của một phần tử là: cha, cha của cha, tổ phụ của cha và v.v. Các tổ tiên cùng nhau hình thành chuỗi cha từ phần tử lên trên cùng.

Phương thức `elem.closest(css)` tìm tổ tiên gần nhất khớp với bộ chọn CSS. Bản thân `elem` cũng được bao gồm trong tìm kiếm.

Nói cách khác, phương thức `closest` di chuyển lên từ phần tử và kiểm tra từng phần tử cha. Nếu nó khớp với bộ chọn, thì tìm kiếm dừng lại, và tổ tiên được trả về.

Ví dụ:

```
<h1>Contents</h1>

<div class="contents">
  <ul class="book">
    <li class="chapter">Chapter 1</li>
    <li class="chapter">Chapter 2</li>
  </ul>
</div>

<script>
  let chapter = document.querySelector('.chapter'); // LI

  alert(chapter.closest('.book')); // UL
  alert(chapter.closest('.contents')); // DIV

  alert(chapter.closest('h1')); // null (vì h1 không phải là tổ tiên)
</script>
```

## [getElementsBy\*](#getelementsby)

Cũng có các phương thức khác để tìm các nút theo thẻ, lớp, v.v.

Ngày nay, chúng chủ yếu là lịch sử, vì `querySelector` mạnh mẽ hơn và ngắn hơn để viết.

Vì vậy, ở đây chúng ta chỉ đề cập đến chúng để đầy đủ, trong khi bạn vẫn có thể tìm thấy chúng trong các tập lệnh cũ.

- `elem.getElementsByTagName(tag)` tìm kiếm các phần tử có thẻ đã cho và trả về bộ sưu tập của chúng. Tham số `tag` cũng có thể là dấu sao `"*"` cho "bất kỳ thẻ nào".
- `elem.getElementsByClassName(className)` trả về các phần tử có lớp CSS đã cho.
- `document.getElementsByName(name)` trả về các phần tử có thuộc tính `name` đã cho, trong toàn bộ tài liệu. Rất hiếm khi sử dụng.

Ví dụ:

```
// lấy tất cả div trong tài liệu
let divs = document.getElementsByTagName('div');
```

Hãy tìm tất cả thẻ `input` bên trong bảng:

```
<table id="table">
  <tr>
    <td>Your age:</td>

    <td>
      <label>
        <input type="radio" name="age" value="young" checked> less than 18
      </label>
      <label>
        <input type="radio" name="age" value="mature"> from 18 to 50
      </label>
      <label>
        <input type="radio" name="age" value="senior"> more than 60
      </label>
    </td>
  </tr>
</table>

<script>
  let inputs = table.getElementsByTagName('input');

  for (let input of inputs) {
    alert( input.value + ': ' + input.checked );
  }
</script>
```

Đừng quên chữ `"s"`!

Nhà phát triển nghiệp dư đôi khi quên chữ cái `"s"`. Đó là, họ cố gọi `getElementByTagName` thay vì `getElementsByTagName`.

Chữ cái `"s"` không có trong `getElementById`, vì nó trả về một phần tử duy nhất. Nhưng `getElementsByTagName` trả về một bộ sưu tập các phần tử, vì vậy có `"s"` ở bên trong.

Nó trả về một bộ sưu tập, không phải một phần tử!

Một lỗi phổ biến khác của nhà phát triển nghiệp dư là viết:

```
// không hoạt động
document.getElementsByTagName('input').value = 5;
```

Điều đó sẽ không hoạt động, vì nó lấy một *bộ sưu tập* các input và gán giá trị cho bộ sưu tập thay vì các phần tử bên trong nó.

Chúng ta nên lặp qua bộ sưu tập hoặc lấy một phần tử theo chỉ mục của nó, sau đó gán, như thế này:

```
// nên hoạt động (nếu có input)
document.getElementsByTagName('input')[0].value = 5;
```

Tìm kiếm các phần tử `.article`:

```
<form name="my-form">
  <div class="article">Article</div>
  <div class="long article">Long article</div>
</form>

<script>
  // tìm theo thuộc tính name
  let form = document.getElementsByName('my-form')[0];

  // tìm theo lớp bên trong form
  let articles = form.getElementsByClassName('article');
  alert(articles.length); // 2, tìm thấy hai phần tử với class "article"
</script>
```

## [Bộ sưu tập sống](#live-collections)

Tất cả các phương thức `"getElementsBy*"` trả về một *bộ sưu tập sống*. Những bộ sưu tập này luôn phản ánh trạng thái hiện tại của tài liệu và "tự động cập nhật" khi nó thay đổi.

Trong ví dụ dưới đây, có hai tập lệnh.

1. Tập lệnh đầu tiên tạo một tham chiếu đến bộ sưu tập `<div>`. Tính đến nay, độ dài của nó là `1`.
2. Tập lệnh thứ hai chạy sau khi trình duyệt gặp thêm một `<div>` nữa, vì vậy độ dài của nó là `2`.

```
<div>First div</div>

<script>
  let divs = document.getElementsByTagName('div');
  alert(divs.length); // 1
</script>

<div>Second div</div>

<script>
  alert(divs.length); // 2
</script>
```

Ngược lại, `querySelectorAll` trả về một *bộ sưu tập tĩnh*. Nó giống như một mảng cố định các phần tử.

Nếu chúng ta sử dụng nó thay thế, thì cả hai tập lệnh đều xuất `1`:

```
<div>First div</div>

<script>
  let divs = document.querySelectorAll('div');
  alert(divs.length); // 1
</script>

<div>Second div</div>

<script>
  alert(divs.length); // 1
</script>
```

Bây giờ chúng ta có thể dễ dàng thấy sự khác biệt. Bộ sưu tập tĩnh không tăng sau khi xuất hiện một `div` mới trong tài liệu.

## [Tóm tắt](#summary)

Có 6 phương thức chính để tìm kiếm nút trong DOM:

| Phương thức | Tìm kiếm theo... | Có thể gọi trên phần tử? | Sống? |
| --- | --- | --- | --- |
| `querySelector` | CSS-selector | ✔ | - |
| `querySelectorAll` | CSS-selector | ✔ | - |
| `getElementById` | `id` | - | - |
| `getElementsByName` | `name` | - | ✔ |
| `getElementsByTagName` | thẻ hoặc `'*'` | ✔ | ✔ |
| `getElementsByClassName` | class | ✔ | ✔ |

Cho đến nay, `querySelector` và `querySelectorAll` được sử dụng nhiều nhất, nhưng `getElement(s)By*` có thể hữu ích tình cờ hoặc tìm thấy trong các tập lệnh cũ.

Ngoài ra:

- Có `elem.matches(css)` để kiểm tra xem `elem` có khớp với bộ chọn CSS đã cho không.
- Có `elem.closest(css)` để tìm tổ tiên gần nhất khớp với bộ chọn CSS đã cho. Bản thân `elem` cũng được kiểm tra.

Và hãy đề cập đến một phương thức nữa để kiểm tra mối quan hệ cha-con, vì nó đôi khi hữu ích:

- `elemA.contains(elemB)` trả về true nếu `elemB` nằm bên trong `elemA` (hậu duệ của `elemA`) hoặc khi `elemA==elemB`.

---

---

## Bài tập

## [Bài tập](#tasks)

### [Tìm kiếm phần tử](#search-for-elements)

độ khó: 4

Đây là tài liệu với bảng và biểu mẫu.

Làm thế nào để tìm?...

1. Bảng với `id="age-table"`.
2. Tất cả các phần tử `label` bên trong bảng đó (phải có 3 cái).
3. `td` đầu tiên trong bảng đó (với chữ "Age").
4. `form` với `name="search"`.
5. `input` đầu tiên trong form đó.
6. `input` cuối cùng trong form đó.

Mở trang [table.html](/task/find-elements/table.html) trong một cửa sổ riêng và sử dụng công cụ trình duyệt để làm điều đó.

lời giải

Có nhiều cách để làm điều đó.

Dưới đây là một số cách:

```
// 1. Bảng với `id="age-table"`.
let table = document.getElementById('age-table')

// 2. Tất cả các phần tử label bên trong bảng đó
table.getElementsByTagName('label')
// hoặc
document.querySelectorAll('#age-table label')

// 3. td đầu tiên trong bảng đó (với chữ "Age")
table.rows[0].cells[0]
// hoặc
table.getElementsByTagName('td')[0]
// hoặc
table.querySelector('td')

// 4. Form với tên "search"
// giả sử chỉ có một phần tử với name="search" trong tài liệu
let form = document.getElementsByName('search')[0]
// hoặc, form cụ thể
document.querySelector('form[name="search"]')

// 5. Input đầu tiên trong form đó.
form.getElementsByTagName('input')[0]
// hoặc
form.querySelector('input')

// 6. Input cuối cùng trong form đó
let inputs = form.querySelectorAll('input') // tìm tất cả input
inputs[inputs.length-1] // lấy cái cuối cùng
```
