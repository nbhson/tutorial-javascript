# Duyệt DOM

> Nguồn: [https://javascript.info/dom-navigation](https://javascript.info/dom-navigation)

<!-- fetched: 2026-09-14 -->

DOM cho phép chúng ta làm mọi thứ với các phần tử và nội dung của chúng, nhưng trước tiên chúng ta cần truy cập được đối tượng DOM tương ứng.

Tất cả các thao tác trên DOM bắt đầu với đối tượng `document`. Đó là "điểm vào" chính vào DOM. Từ đó, chúng ta có thể truy cập mọi nút.

Đây là hình ảnh về các liên kết cho phép di chuyển giữa các nút DOM:

![](/article/dom-navigation/dom-links.svg)

Hãy cùng thảo luận chi tiết hơn về chúng.

## [Trên cùng: documentElement và body](#on-top-documentelement-and-body)

Các nút cây cao nhất có sẵn trực tiếp như các thuộc tính của `document`:

`<html>` = `document.documentElement`
:   Nút tài liệu cao nhất là `document.documentElement`. Đó là nút DOM của thẻ `<html>`.

`<body>` = `document.body`
:   Một nút DOM được sử dụng rộng rãi khác là phần tử `<body>` – `document.body`.

`<head>` = `document.head`
:   Thẻ `<head>` có sẵn dưới dạng `document.head`.

Có một điểm cần lưu ý: `document.body` có thể là `null`

Một tập lệnh không thể truy cập một phần tử không tồn tại tại thời điểm chạy.

Cụ thể, nếu một tập lệnh nằm trong `<head>`, thì `document.body` không khả dụng, vì trình duyệt chưa đọc nó.

Vì vậy, trong ví dụ dưới đây, `alert` đầu tiên hiển thị `null`:

```
<html>

<head>
  <script>
    alert( "From HEAD: " + document.body ); // null, chưa có <body>
  </script>
</head>

<body>

  <script>
    alert( "From BODY: " + document.body ); // HTMLBodyElement, bây giờ nó đã tồn tại
  </script>

</body>
</html>
```

Trong thế giới DOM, `null` có nghĩa là "không tồn tại"

Trong DOM, giá trị `null` có nghĩa là "không tồn tại" hoặc "không có nút như vậy".

## [Con: childNodes, firstChild, lastChild](#children-childnodes-firstchild-lastchild)

Có hai thuật ngữ mà chúng ta sẽ sử dụng từ giờ trở đi:

- **Nút con (hoặc con)** – các phần tử là con trực tiếp. Nói cách khác, chúng được lồng chính xác trong phần tử đã cho. Ví dụ: `<head>` và `<body>` là con của phần tử `<html>`.
- **Hậu duệ** – tất cả các phần tử được lồng trong phần tử đã cho, bao gồm con, con của chúng và v.v.

Ví dụ, ở đây `<body>` có con là `<div>` và `<ul>` (và một vài nút văn bản trống):

```
<html>
<body>
  <div>Begin</div>

  <ul>
    <li>
      <b>Information</b>
    </li>
  </ul>
</body>
</html>
```

…Và hậu duệ của `<body>` không chỉ là con trực tiếp `<div>`, `<ul>` mà còn các phần tử lồng sâu hơn, chẳng hạn như `<li>` (con của `<ul>`) và `<b>` (con của `<li>`) – toàn bộ cây con.

**Bộ sưu tập `childNodes` liệt kê tất cả các nút con, bao gồm cả nút văn bản.**

Ví dụ dưới đây cho thấy các con của `document.body`:

```
<html>
<body>
  <div>Begin</div>

  <ul>
    <li>Information</li>
  </ul>

  <div>End</div>

  <script>
    for (let i = 0; i < document.body.childNodes.length; i++) {
      alert( document.body.childNodes[i] ); // Text, DIV, Text, UL, ..., SCRIPT
    }
  </script>
  ...thêm nội dung...
</body>
</html>
```

Xin lưu ý một chi tiết thú vị ở đây. Nếu chúng ta chạy ví dụ trên, phần tử cuối cùng được hiển thị là `<script>`. Thực tế, tài liệu có nhiều nội dung hơn bên dưới, nhưng tại thời điểm tập lệnh chạy, trình duyệt chưa đọc nó, nên tập lệnh không nhìn thấy được.

**Thuộc tính `firstChild` và `lastChild` cung cấp quyền truy cập nhanh vào con đầu tiên và cuối cùng.**

Chúng chỉ là các tên viết tắt. Nếu tồn tại các nút con, thì điều sau luôn đúng:

```
elem.childNodes[0] === elem.firstChild
elem.childNodes[elem.childNodes.length - 1] === elem.lastChild
```

Cũng có một hàm đặc biệt `elem.hasChildNodes()` để kiểm tra xem có tồn tại nút con nào không.

### [Bộ sưu tập DOM](#dom-collections)

Như chúng ta có thể thấy, `childNodes` trông giống như một mảng. Nhưng thực tế nó không phải là mảng, mà là *bộ sưu tập* – một đối tượng iterable đặc biệt giống mảng.

Có hai hệ quả quan trọng:

1. Chúng ta có thể sử dụng `for..of` để lặp qua nó:

```
for (let node of document.body.childNodes) {
  alert(node); // hiển thị tất cả các nút trong bộ sưu tập
}
```

Điều đó là vì nó iterable (cung cấp thuộc tính `Symbol.iterator`, như yêu cầu).

2. Các phương thức mảng sẽ không hoạt động, vì nó không phải là mảng:

```
alert(document.body.childNodes.filter); // undefined (không có phương thức filter!)
```

Điều đầu tiên thì tốt. Điều thứ hai có thể chấp nhận được, vì chúng ta có thể sử dụng `Array.from` để tạo một mảng "thực" từ bộ sưu tập, nếu chúng ta muốn các phương thức mảng:

```
alert( Array.from(document.body.childNodes).filter ); // function
```

Bộ sưu tập DOM chỉ đọc

Bộ sưu tập DOM, và thậm chí – *tất cả* các thuộc tính điều hướng được liệt kê trong chương này là chỉ đọc.

Chúng ta không thể thay thế một con bằng thứ gì khác bằng cách gán `childNodes[i] = ...`.

Thay đổi DOM cần các phương thức khác. Chúng ta sẽ thấy chúng trong chương tiếp theo.

Bộ sưu tập DOM sống

Hầu hết tất cả các bộ sưu tập DOM với một số ngoại lệ nhỏ là *sống*. Nói cách khác, chúng phản ánh trạng thái hiện tại của DOM.

Nếu chúng ta giữ một tham chiếu đến `elem.childNodes`, và thêm/xóa các nút vào DOM, thì chúng sẽ xuất hiện trong bộ sưu tập một cách tự động.

Không sử dụng `for..in` để lặp qua bộ sưu tập

Bộ sưu tập iterable bằng `for..of`. Đôi khi mọi người cố gắng sử dụng `for..in` cho việc đó.

Xin vui lòng không làm vậy. Vòng lặp `for..in` lặp qua tất cả các thuộc tính có thể liệt kê. Và bộ sưu tập có một số thuộc tính "thêm" hiếm khi được sử dụng mà chúng ta thường không muốn lấy:

```
<body>
<script>
  // hiển thị 0, 1, length, item, values và nhiều hơn nữa.
  for (let prop in document.body.childNodes) alert(prop);
</script>
</body>
```

## [Anh em và cha](#siblings-and-the-parent)

*Anh em* là các nút là con của cùng một cha.

Ví dụ, ở đây `<head>` và `<body>` là anh em:

```
<html>
  <head>...</head><body>...</body>
</html>
```

- `<body>` được gọi là "anh em sau" hoặc "anh em phải" của `<head>`,
- `<head>` được gọi là "anh em trước" hoặc "anh em trái" của `<body>`.

Anh em sau nằm trong thuộc tính `nextSibling`, và anh em trước – trong `previousSibling`.

Phần tử cha có sẵn dưới dạng `parentNode`.

Ví dụ:

```
// cha của <body> là <html>
alert( document.body.parentNode === document.documentElement ); // true

// sau <head> là <body>
alert( document.head.nextSibling ); // HTMLBodyElement

// trước <body> là <head>
alert( document.body.previousSibling ); // HTMLHeadElement
```

## [Điều hướng chỉ phần tử](#element-only-navigation)

Các thuộc tính điều hướng được liệt kê ở trên tham chiếu đến *tất cả* các nút. Ví dụ, trong `childNodes` chúng ta có thể thấy cả nút văn bản, nút phần tử, và thậm chí cả nút chú thích nếu chúng tồn tại.

Nhưng đối với nhiều tác vụ, chúng ta không muốn nút văn bản hoặc chú thích. Chúng ta muốn thao tác với các nút phần tử đại diện cho các thẻ và hình thành cấu trúc của trang.

Vì vậy, hãy xem các liên kết điều hướng hơn nữa chỉ tính đến *nút phần tử*:

![](/article/dom-navigation/dom-links-elements.svg)

Các liên kết tương tự như những gì đã nêu ở trên, chỉ có từ `Element` nằm trong đó:

- `children` – chỉ những con là nút phần tử.
- `firstElementChild`, `lastElementChild` – con phần tử đầu tiên và cuối cùng.
- `previousElementSibling`, `nextElementSibling` – phần tử lân cận.
- `parentElement` – phần tử cha.

Tại sao `parentElement`? Cha có thể *không phải* là phần tử không?

Thuộc tính `parentElement` trả về phần tử cha "phần tử", trong khi `parentNode` trả về phần tử cha "bất kỳ nút nào". Các thuộc tính này thường giống nhau: cả hai đều lấy phần tử cha.

Với một ngoại lệ duy nhất của `document.documentElement`:

```
alert( document.documentElement.parentNode ); // document
alert( document.documentElement.parentElement ); // null
```

Lý do là nút gốc `document.documentElement` (`<html>`) có `document` là cha của nó. Nhưng `document` không phải là nút phần tử, vì vậy `parentNode` trả về nó và `parentElement` thì không.

Chi tiết này có thể hữu ích khi chúng ta muốn di chuyển lên từ một phần tử tùy ý `elem` đến `<html>`, nhưng không phải đến `document`:

```
while(elem = elem.parentElement) { // di chuyển lên đến <html>
  alert( elem );
}
```

Hãy sửa đổi một trong các ví dụ trên: thay `childNodes` bằng `children`. Giờ đây nó chỉ hiển thị các phần tử:

```
<html>
<body>
  <div>Begin</div>

  <ul>
    <li>Information</li>
  </ul>

  <div>End</div>

  <script>
    for (let elem of document.body.children) {
      alert(elem); // DIV, UL, DIV, SCRIPT
    }
  </script>
  ...
</body>
</html>
```

## [Thêm liên kết: bảng](#dom-navigation-tables)

Cho đến nay chúng ta đã mô tả các thuộc tính điều hướng cơ bản.

Certain types of DOM elements may provide additional properties, specific to their type, for convenience.

Các loại phần tử DOM nhất định có thể cung cấp các thuộc tính bổ sung, đặc thù cho loại của chúng, để tiện lợi.

Bảng là một ví dụ tuyệt vời về điều đó, và đại diện cho một trường hợp đặc biệt quan trọng:

**Phần tử `<table>` hỗ trợ (ngoài những gì đã nêu ở trên) các thuộc tính sau:**

- `table.rows` – bộ sưu tập các phần tử `<tr>` của bảng.
- `table.caption/tHead/tFoot` – tham chiếu đến các phần tử `<caption>`, `<thead>`, `<tfoot>`.
- `table.tBodies` – bộ sưu tập các phần tử `<tbody>` (có thể có nhiều theo tiêu chuẩn, nhưng sẽ luôn có ít nhất một – ngay cả khi nó không có trong HTML nguồn, trình duyệt sẽ đưa nó vào DOM).

**`<thead>`, `<tfoot>`, `<tbody>`** cung cấp thuộc tính `rows`:

- `tbody.rows` – bộ sưu tập các `<tr>` bên trong.

**`<tr>`:**

- `tr.cells` – bộ sưu tập các ô `<td>` và `<th>` bên trong `<tr>` đã cho.
- `tr.sectionRowIndex` – vị trí (chỉ mục) của `<tr>` đã cho bên trong `<thead>/<tbody>/<tfoot>` bao quanh.
- `tr.rowIndex` – số của `<tr>` trong toàn bộ bảng (bao gồm tất cả các hàng bảng).

**`<td>` và `<th>`:**

- `td.cellIndex` – số của ô bên trong `<tr>` bao quanh.

Một ví dụ về cách sử dụng:

```
<table id="table">
  <tr>
    <td>one</td><td>two</td>
  </tr>
  <tr>
    <td>three</td><td>four</td>
  </tr>
</table>

<script>
  // lấy td có "two" (hàng đầu tiên, cột thứ hai)
  let td = table.rows[0].cells[1];
  td.style.backgroundColor = "red"; // đánh dấu nó
</script>
```

Đặc tả: [dữ liệu dạng bảng](https://html.spec.whatwg.org/multipage/tables.html).

Cũng có các thuộc tính điều hướng bổ sung cho các biểu mẫu HTML. Chúng ta sẽ xem chúng sau khi bắt đầu làm việc với biểu mẫu.

## [Tóm tắt](#summary)

Cho một nút DOM, chúng ta có thể di chuyển đến các phần tử lân cận ngay lập tức của nó bằng cách sử dụng các thuộc tính điều hướng.

Có hai bộ chính của chúng:

- Cho tất cả các nút: `parentNode`, `childNodes`, `firstChild`, `lastChild`, `previousSibling`, `nextSibling`.
- Chỉ cho các nút phần tử: `parentElement`, `children`, `firstElementChild`, `lastElementChild`, `previousElementSibling`, `nextElementSibling`.

Một số loại phần tử DOM, ví dụ bảng, cung cấp các thuộc tính và bộ sưu tập bổ sung để truy cập nội dung của chúng.

---

---

## Bài tập

## [Bài tập](#tasks)

### [Con DOM](#dom-children)

độ khó: 5

Xem trang này:

```
<html>
<body>
  <div>Users:</div>
  <ul>
    <li>John</li>
    <li>Pete</li>
  </ul>
</body>
</html>
```

Đối với mỗi thứ sau đây, đưa ra ít nhất một cách để truy cập chúng:

- Nút DOM `<div>`?
- Nút DOM `<ul>`?
- `<li>` thứ hai (với Pete)?

lời giải

Có nhiều cách, ví dụ:

Nút DOM `<div>`:

```
document.body.firstElementChild
// hoặc
document.body.children[0]
// hoặc (nút đầu tiên là khoảng trắng, nên chúng ta lấy thứ 2)
document.body.childNodes[1]
```

Nút DOM `<ul>`:

```
document.body.lastElementChild
// hoặc
document.body.children[1]
```

`<li>` thứ hai (với Pete):

```
// lấy <ul>, sau đó lấy con phần tử cuối cùng của nó
document.body.lastElementChild.lastElementChild
```

### [Câu hỏi về anh em](#the-sibling-question)

độ khó: 5

Nếu `elem` – là một nút phần tử DOM tùy ý…

- Có đúng không khi `elem.lastChild.nextSibling` luôn là `null`?
- Có đúng không khi `elem.children[0].previousSibling` luôn là `null`?

lời giải

1. Đúng. Phần tử `elem.lastChild` luôn là phần tử cuối cùng, nó không có `nextSibling`.
2. Không, sai, vì `elem.children[0]` là con đầu tiên *giữa các phần tử*. Nhưng có thể tồn tại các nút không phải phần tử trước nó. Vì vậy `previousSibling` có thể là một nút văn bản.

Xin lưu ý: đối với cả hai trường hợp nếu không có con, thì sẽ có lỗi.

Nếu không có con, `elem.lastChild` là `null`, vì vậy chúng ta không thể truy cập `elem.lastChild.nextSibling`. Và bộ sưu tập `elem.children` trống (giống như mảng trống `[]`).

### [Chọn tất cả các ô đường chéo](#select-all-diagonal-cells)

độ khó: 5

Viết mã để tô màu tất cả các ô đường chéo của bảng thành màu đỏ.

Bạn sẽ cần lấy tất cả `<td>` đường chéo từ `<table>` và tô màu chúng bằng mã:

```
// td nên là tham chiếu đến ô bảng
td.style.backgroundColor = 'red';
```

Kết quả sẽ là:

[Mở sandbox cho bài tập.](https://plnkr.co/edit/2AOS4aj5TiW1oD5J?p=preview)

lời giải

Chúng ta sẽ sử dụng các thuộc tính `rows` và `cells` để truy cập các ô bảng đường chéo.

[Mở lời giải trong sandbox.](https://plnkr.co/edit/z8AeflcSowLaF4WF?p=preview)
