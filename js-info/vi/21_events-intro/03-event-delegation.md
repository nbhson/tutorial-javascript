# Ủy quyền sự kiện

> Source: [https://javascript.info/event-delegation](https://javascript.info/event-delegation)

<!-- fetched: 2026-09-14 -->

Bắt giữ và tràn cho phép chúng ta triển khai một trong những mẫu xử lý sự kiện mạnh mẽ nhất gọi là *event delegation*.

Ý tưởng là nếu chúng ta có nhiều phần tử được xử lý theo cách tương tự, thì thay vì gán trình xử lý cho từng cái – chúng ta đặt một trình xử lý duy nhất trên phần tử tổ tiên chung của chúng.

Trong trình xử lý, chúng ta lấy `event.target` để xem sự kiện thực sự xảy ra ở đâu và xử lý nó.

Hãy xem ví dụ – [Sơ đồ Ba-Gua](http://en.wikipedia.org/wiki/Ba_gua) phản ánh triết học Trung Hoa cổ đại.

Đây là nó:

HTML như sau:

```
<table>
  <tr>
    <th colspan="3"><em>Bagua</em> Chart: Direction, Element, Color, Meaning</th>
  </tr>
  <tr>
    <td class="nw"><strong>Northwest</strong><br>Metal<br>Silver<br>Elders</td>
    <td class="n">...</td>
    <td class="ne">...</td>
  </tr>
  <tr>...2 more lines of this kind...</tr>
  <tr>...2 more lines of this kind...</tr>
</table>
```

Bảng có 9 ô, nhưng có thể có 99 hoặc 9999, không quan trọng.

**Nhiệm vụ của chúng ta là làm nổi bật một ô `<td>` khi nhấp chuột.**

Thay vì gán trình xử lý `onclick` cho mỗi `<td>` (có thể nhiều) – chúng ta sẽ thiết lập trình xử lý "bắt khắp" trên phần tử `<table>`.

Nó sẽ dùng `event.target` để lấy phần tử đã nhấp và làm nổi bật nó.

Mã:

```
let selectedTd;

table.onclick = function(event) {
  let target = event.target; // ở đâu đã nhấp?

  if (target.tagName != 'TD') return; // không phải TD? Vậy chúng ta không quan tâm

  highlight(target); // làm nổi bật nó
};

function highlight(td) {
  if (selectedTd) { // xóa highlight hiện có nếu có
    selectedTd.classList.remove('highlight');
  }
  selectedTd = td;
  selectedTd.classList.add('highlight'); // làm nổi bật td mới
}
```

Mã như vậy không quan tâm có bao nhiêu ô trong bảng. Chúng ta có thể thêm/xóa `<td>` động bất cứ lúc nào và việc làm nổi bật vẫn hoạt động.

Vẫn còn đó một nhược điểm.

Nhấp chuột có thể xảy ra không phải trên `<td>`, nhưng bên trong nó.

Trong trường hợp của chúng ta, nếu nhìn vào HTML, chúng ta có thể thấy các thẻ lồng nhau bên trong `<td>`, như `<strong>`:

```
<td>
  <strong>Northwest</strong>
  ...
</td>
```

Tự nhiên, nếu nhấp chuột trên `<strong>` đó thì nó trở thành giá trị của `event.target`.

![](/article/event-delegation/bagua-bubble.svg)

Trong trình xử lý `table.onclick`, chúng ta nên lấy `event.target` đó và tìm ra xem lần nhấp có bên trong `<td>` hay không.

Đây là mã được cải tiến:

```
table.onclick = function(event) {
  let td = event.target.closest('td'); // (1)

  if (!td) return; // (2)

  if (!table.contains(td)) return; // (3)

  highlight(td); // (4)
};
```

Giải thích:

1. Phương thức `elem.closest(selector)` trả về phần tử tổ tiên gần nhất khớp với selector. Trong trường hợp của chúng ta, chúng ta tìm `<td>` trên đường đi lên từ phần tử nguồn.
2. Nếu `event.target` không nằm trong bất kỳ `<td>` nào, thì gọi trả về ngay lập tức, vì không có gì phải làm.
3. Trong trường hợp bảng lồng nhau, `event.target` có thể là một `<td>`, nhưng nằm ngoài bảng hiện tại. Vì vậy chúng ta kiểm tra xem đó có thực sự là `<td>` của *bảng chúng ta* không.
4. Và, nếu vậy, thì làm nổi bật nó.

Kết quả là chúng ta có mã làm nổi bật nhanh, hiệu quả, không quan tâm đến tổng số `<td>` trong bảng.

## [Ví dụ ủy quyền: hành động trong markup](#delegation-example-actions-in-markup)

Có các cách dùng khác cho event delegation.

Giả sử, chúng ta muốn tạo menu với các nút "Save", "Load", "Search" và cứ thế. Và có một đối tượng với các phương thức `save`, `load`, `search`… Làm sao để khớp chúng?

Ý nghĩ đầu tiên có thể là gán trình xử lý riêng cho mỗi nút. Nhưng có giải pháp thanh lịch hơn. Chúng ta có thể thêm trình xử lý cho toàn bộ menu và thuộc tính `data-action` cho các nút có phương thức để gọi:

```
<button data-action="save">Click to Save</button>
```

Trình xử lý đọc thuộc tính và thực thi phương thức. Hãy xem ví dụ hoạt động:

```
<div id="menu">
  <button data-action="save">Save</button>
  <button data-action="load">Load</button>
  <button data-action="search">Search</button>
</div>

<script>
  class Menu {
    constructor(elem) {
      this._elem = elem;
      elem.onclick = this.onClick.bind(this); // (*)
    }

    save() {
      alert('saving');
    }

    load() {
      alert('loading');
    }

    search() {
      alert('searching');
    }

    onClick(event) {
      let action = event.target.dataset.action;
      if (action) {
        this[action]();
      }
    };
  }

  new Menu(menu);
</script>
```

Lưu ý rằng `this.onClick` được bind với `this` trong `(*)`. Điều đó quan trọng, vì nếu không `this` bên trong nó sẽ tham chiếu đến phần tử DOM (`elem`), không phải đối tượng `Menu`, và `this[action]` sẽ không phải như chúng ta cần.

Vậy, những lợi ích nào mà ủy quyền mang lại ở đây?

- Chúng ta không cần viết mã để gán trình xử lý cho mỗi nút. Chỉ cần tạo phương thức và đặt nó trong markup.
- Cấu trúc HTML linh hoạt, chúng ta có thể thêm/xóa nút bất cứ lúc nào.

Chúng ta cũng có thể dùng các class `.action-save`, `.action-load`, nhưng thuộc tính `data-action` tốt hơn về mặt ngữ nghĩa. Và chúng ta có thể dùng nó trong các quy tắc CSS.

## [Mẫu "hành vi"](#the-behavior-pattern)

Chúng ta cũng có thể dùng event delegation để thêm "hành vi" vào các phần tử *khai báo*, với các thuộc tính và class đặc biệt.

Mẫu có hai phần:

1. Chúng ta thêm một thuộc tính tùy chỉnh cho một phần tử mô tả hành vi của nó.
2. Một trình xử lý toàn tài liệu theo dõi sự kiện, và nếu sự kiện xảy ra trên phần tử có thuộc tính – thực hiện hành động.

### [Hành vi: Bộ đếm](#behavior-counter)

Ví dụ, ở đây thuộc tính `data-counter` thêm hành vi: "tăng giá trị khi nhấp" cho các nút:

```
Counter: <input type="button" value="1" data-counter>
One more counter: <input type="button" value="2" data-counter>

<script>
  document.addEventListener('click', function(event) {

    if (event.target.dataset.counter != undefined) { // nếu thuộc tính tồn tại...
      event.target.value++;
    }

  });
</script>
```

Nếu chúng ta nhấp vào nút – giá trị của nó tăng lên. Không phải các nút, mà phương pháp tổng quát mới quan trọng ở đây.

Có thể có bao nhiêu thuộc tính với `data-counter` tùy thích. Chúng ta có thể thêm mới vào HTML bất cứ lúc nào. Dùng event delegation chúng ta đã "mở rộng" HTML, thêm một thuộc tính mô tả hành vi mới.

Đối với trình xử lý cấp tài liệu – luôn luôn `addEventListener`

Khi chúng ta gán trình xử lý sự kiện cho đối tượng `document`, chúng ta nên luôn dùng `addEventListener`, không phải `document.on<event>`, vì cái后者 sẽ gây xung đột: trình xử lý mới ghi đè trình xử lý cũ.

Đối với dự án thực tế, việc có nhiều trình xử lý trên `document` được đặt bởi các phần code khác nhau là bình thường.

### [Hành vi: Bộ chuyển đổi](#behavior-toggler)

Một ví dụ nữa về hành vi. Một lần nhấp vào phần tử có thuộc tính `data-toggle-id` sẽ hiện/ẩn phần tử có `id` đã cho:

```
<button data-toggle-id="subscribe-mail">
  Show the subscription form
</button>

<form id="subscribe-mail" hidden>
  Your mail: <input type="email">
</form>

<script>
  document.addEventListener('click', function(event) {
    let id = event.target.dataset.toggleId;
    if (!id) return;

    let elem = document.getElementById(id);

    elem.hidden = !elem.hidden;
  });
</script>
```

Hãy lưu lại một lần nữa những gì chúng ta đã làm. Bây giờ, để thêm chức năng chuyển đổi cho một phần tử – không cần biết JavaScript, chỉ cần dùng thuộc tính `data-toggle-id`.

Điều đó có thể rất tiện – không cần viết JavaScript cho mọi phần tử như vậy. Chỉ cần dùng hành vi. Trình xử lý cấp tài liệu làm nó hoạt động cho bất kỳ phần tử nào của trang.

Chúng ta cũng có thể kết hợp nhiều hành vi trên một phần tử.

Mẫu "hành vi" có thể là thay thế cho các đoạn mã JavaScript nhỏ.

## [Tóm tắt](#summary)

Event delegation thực sự tuyệt! Đó là một trong những mẫu hữu ích nhất cho sự kiện DOM.

Nó thường được dùng để thêm xử lý giống nhau cho nhiều phần tử tương tự, nhưng không chỉ vậy.

Thuật toán:

1. Đặt một trình xử lý duy nhất trên vùng chứa.
2. Trong trình xử lý – kiểm tra phần tử nguồn `event.target`.
3. Nếu sự kiện xảy ra bên trong phần tử chúng ta quan tâm, thì xử lý sự kiện.

Lợi ích:

- Đơn giản hóa khởi tạo và tiết kiệm bộ nhớ: không cần thêm nhiều trình xử lý.
- Ít mã hơn: khi thêm hoặc xóa phần tử, không cần thêm/xóa trình xử lý.
- Thay đổi DOM: chúng ta có thể thêm/xóa hàng loạt phần tử với `innerHTML` và tương tự.

Ủy quyền có các giới hạn của nó dĩ nhiên:

- Đầu tiên, sự kiện phải tràn. Một số sự kiện không tràn. Cũng nên tránh dùng `event.stopPropagation()` trong trình xử lý cấp thấp.
- Thứ hai, ủy quyền có thể thêm tải CPU, vì trình xử lý cấp vùng chứa phản ứng với sự kiện ở bất kỳ vị trí nào trong vùng chứa, bất kể chúng có quan tâm hay không. Nhưng thường tải không đáng kể, nên chúng ta không tính đến.

---

---

## Các bài tập

## [Tasks](#tasks)

### [Ẩn tin nhắn với ủy quyền](#hide-messages-with-delegation)

importance: 5

Có một danh sách tin nhắn với nút xóa `[x]`. Làm cho các nút hoạt động.

Như sau:

P.S. Nên chỉ có một trình lắng nghe sự kiện trên vùng chứa, dùng event delegation.

[Open a sandbox for the task.](https://plnkr.co/edit/DAtj1Sf3roead0td?p=preview)

solution

[Open the solution in a sandbox.](https://plnkr.co/edit/4lxsl5ZY8rW2kT0s?p=preview)

### [Menu cây](#tree-menu)

importance: 5

Tạo cây hiển thị/ẩn các phần tử con khi nhấp:

Yêu cầu:

- Chỉ một trình xử lý sự kiện (dùng ủy quyền)
- Nhấp chuột ngoài tiêu đề phần tử (trên khoảng trống) không nên làm gì.

[Open a sandbox for the task.](https://plnkr.co/edit/w3HHOacWRFRmWmfD?p=preview)

solution

Giải pháp có hai phần.

1. Đóng mọi tiêu đề nút cây vào `<span>`. Sau đó chúng ta có thể CSS-style chúng khi `:hover` và xử lý nhấp chuột chính xác trên văn bản, vì chiều rộng `<span>` chính xác là chiều rộng văn bản (khác với không có nó).
2. Đặt trình xử lý cho nút gốc `tree` và xử lý nhấp chuột trên các tiêu đề `<span>` đó.

[Open the solution in a sandbox.](https://plnkr.co/edit/YoJ5i6rY45o7oaXk?p=preview)

### [Bảng có thể sắp xếp](#sortable-table)

importance: 4

Làm cho bảng có thể sắp xếp: nhấp chuột vào các phần tử `<th>` nên sắp xếp theo cột tương ứng.

Mỗi `<th>` có loại trong thuộc tính, như sau:

```
<table id="grid">
  <thead>
    <tr>
      <th data-type="number">Age</th>
      <th data-type="string">Name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>5</td>
      <td>John</td>
    </tr>
    <tr>
      <td>10</td>
      <td>Ann</td>
    </tr>
    ...
  </tbody>
</table>
```

Trong ví dụ trên cột đầu có số, và cột thứ hai – chuỗi. Hàm sắp xếp nên xử lý sắp xếp theo loại.

Chỉ nên hỗ trợ các loại `"string"` và `"number"`.

Ví dụ hoạt động:

P.S. Bảng có thể lớn, với bất kỳ số dòng và cột nào.

[Open a sandbox for the task.](https://plnkr.co/edit/pfEuFs8BE2Sw3Iw9?p=preview)

solution

[Open the solution in a sandbox.](https://plnkr.co/edit/QRZyAxlQ8rEy1YMn?p=preview)

### [Hành vi Tooltip](#tooltip-behavior)

importance: 5

Tạo JS-code cho hành vi tooltip.

Khi chuột di vào phần tử có `data-tooltip`, tooltip nên hiện lên trên nó, và khi rời đi thì ẩn.

Ví dụ HTML chú thích:

```
<button data-tooltip="the tooltip is longer than the element">Short button</button>
<button data-tooltip="HTML<br>tooltip">One more button</button>
```

Nên hoạt động như sau:

Trong bài tập này chúng ta giả định rằng tất cả phần tử có `data-tooltip` chỉ có văn bản bên trong. Không có thẻ lồng nhau (chưa có).

Chi tiết:

- Khoảng cách giữa phần tử và tooltip nên là `5px`.
- Tooltip nên được căn giữa tương đối với phần tử, nếu có thể.
- Tooltip không được vượt ra cạnh cửa sổ. Bình thường nó nên ở trên phần tử, nhưng nếu phần tử ở đầu trang và không có chỗ cho tooltip, thì ở dưới nó.
- Nội dung tooltip được cho trong thuộc tính `data-tooltip`. Nó có thể là HTML tùy ý.

Bạn sẽ cần hai sự kiện ở đây:

- `mouseover` kích hoạt khi con trỏ di vào phần tử.
- `mouseout` kích hoạt khi con trỏ rời phần tử.

Hãy dùng event delegation: thiết lập hai trình xử lý trên `document` để theo dõi tất cả lần "vào" và "ra" từ các phần tử có `data-tooltip` và quản lý tooltip từ đó.

Sau khi hành vi được triển khai, thậm chí người không quen với JavaScript cũng có thể thêm các phần tử chú thích.

P.S. Chỉ một tooltip có thể hiện cùng lúc.

[Open a sandbox for the task.](https://plnkr.co/edit/h6G2YUWOGQHhcHVO?p=preview)

solution

[Open the solution in a sandbox.](https://plnkr.co/edit/s8bChzqdT2cphbpW?p=preview)