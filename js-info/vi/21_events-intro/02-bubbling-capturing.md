# Tràn và bắt giữ

> Source: [https://javascript.info/bubbling-and-capturing](https://javascript.info/bubbling-and-capturing)

<!-- fetched: 2026-09-14 -->

Hãy bắt đầu với một ví dụ.

Trình xử lý này được gán cho `<div>`, nhưng cũng chạy nếu bạn nhấp vào bất kỳ thẻ lồng nhau nào như `<em>` hoặc `<code>`:

```
<div onclick="alert('The handler!')">
  <em>If you click on <code>EM</code>, the handler on <code>DIV</code> runs.</em>
</div>
```

Điều đó không có gì lạ sao? Tại sao trình xử lý trên `<div>` lại chạy nếu lần nhấp thực sự là trên `<em>`?

## [Tràn (Bubbling)](#bubbling)

Nguyên lý tràn rất đơn giản.

**Khi một sự kiện xảy ra trên một phần tử, trước tiên các trình xử lý chạy trên nó, sau đó trên phần tử cha của nó, rồi tiếp tục lên tất cả các phần tử tổ tiên khác.**

Giả sử chúng ta có 3 phần tử lồng nhau `FORM > DIV > P` với một trình xử lý trên mỗi phần tử:

```
<style>
  body * {
    margin: 10px;
    border: 1px solid blue;
  }
</style>

<form onclick="alert('form')">FORM
  <div onclick="alert('div')">DIV
    <p onclick="alert('p')">P</p>
  </div>
</form>
```

Một lần nhấp vào `<p>` bên trong trước tiên chạy `onclick`:

1. Trên `<p>` đó.
2. Sau đó trên `<div>` ngoài.
3. Sau đó trên `<form>` ngoài.
4. Và cứ thế lên cho tới đối tượng `document`.

![](/article/bubbling-and-capturing/event-order-bubbling.svg)

Vì vậy nếu chúng ta nhấp vào `<p>`, thì sẽ thấy 3 cảnh báo: `p` → `div` → `form`.

Quá trình gọi là "tràn" (bubbling), vì sự kiện "bong bóng" từ phần tử bên trong lên qua các phần tử cha giống như bong bóng trong nước.

Gần như *tất cả* sự kiện đều tràn.

Từ khóa trong cụm từ này là "gần như".

Ví dụ, sự kiện `focus` không tràn. Cũng có những ví dụ khác, chúng ta sẽ gặp chúng. Nhưng vẫn đó là ngoại lệ chứ không phải quy tắc, hầu hết sự kiện đều tràn.

## [event.target](#event-target)

Trình xử lý trên phần tử cha luôn có thể lấy chi tiết về nơi sự kiện thực sự xảy ra.

**Phần tử lồng sâu nhất gây ra sự kiện được gọi là phần tử *target*, truy cập được qua `event.target`.**

Lưu ý sự khác biệt từ `this` (=`event.currentTarget`):

- `event.target` – là phần tử "target" khởi tạo sự kiện, nó không thay đổi qua quá trình tràn.
- `this` – là phần tử "current", phần tử có trình xử lý đang chạy trên nó.

Ví dụ, nếu chúng ta có một trình xử lý `form.onclick` đơn, thì nó có thể "bắt" tất cả các lần nhấp bên trong form. Bất kể lần nhấp xảy ra ở đâu, nó tràn lên `<form>` và chạy trình xử lý.

Trong trình xử lý `form.onclick`:

- `this` (=`event.currentTarget`) là phần tử `<form>`, vì trình xử lý chạy trên nó.
- `event.target` là phần tử thực sự bên trong form đã được nhấp.

Kiểm tra:

Kết quả

script.js

example.css

index.html

```
form.onclick = function(event) {
  event.target.style.backgroundColor = 'yellow';

  // chrome cần một ít thời gian để vẽ màu vàng
  setTimeout(() => {
    alert("target = " + event.target.tagName + ", this=" + this.tagName);
    event.target.style.backgroundColor = ''
  }, 0);
};
```

```
form {
  background-color: green;
  position: relative;
  width: 150px;
  height: 150px;
  text-align: center;
  cursor: pointer;
}

div {
  background-color: blue;
  position: absolute;
  top: 25px;
  left: 25px;
  width: 100px;
  height: 100px;
}

p {
  background-color: red;
  position: absolute;
  top: 25px;
  left: 25px;
  width: 50px;
  height: 50px;
  line-height: 50px;
  margin: 0;
}

body {
  line-height: 25px;
  font-size: 16px;
}
```

```
<!DOCTYPE HTML>
<html>

<head>
  <meta charset="utf-8">
  <link rel="stylesheet" href="example.css">
</head>

<body>
  Một lần nhấp hiện cả <code>event.target</code> và <code>this</code> để so sánh:

  <form id="form">FORM
    <div>DIV
      <p>P</p>
    </div>
  </form>

  <script src="script.js"></script>
</body>
</html>
```

Có thể `event.target` bằng `this` – điều đó xảy ra khi lần nhấp được thực hiện trực tiếp trên phần tử `<form>`.

## [Ngừng tràn](#stopping-bubbling)

Một sự kiện tràn đi từ phần tử target thẳng lên trên. Bình thường nó đi lên tới `<html>`, và sau đó tới đối tượng `document`, và một số sự kiện thậm chí đạt đến `window`, gọi tất cả trình xử lý trên đường đi.

Nhưng bất kỳ trình xử lý nào cũng có thể quyết định rằng sự kiện đã được xử lý đầy đủ và ngừng tràn.

Phương thức cho việc đó là `event.stopPropagation()`.

Ví dụ, ở đây `body.onclick` không hoạt động nếu bạn nhấp vào `<button>`:

```
<body onclick="alert(`the bubbling doesn't reach here`)">
  <button onclick="event.stopPropagation()">Click me</button>
</body>
```

event.stopImmediatePropagation()

Nếu một phần tử có nhiều trình xử lý sự kiện trên một sự kiện, thì ngay cả khi một trong số chúng ngừng tràn, các trình xử lý khác vẫn thực thi.

Nói cách khác, `event.stopPropagation()` ngừng di chuyển lên trên, nhưng trên phần tử hiện tại tất cả các trình xử lý khác sẽ chạy.

Để ngừng tràn và ngăn trình xử lý trên phần tử hiện tại chạy, có phương thức `event.stopImmediatePropagation()`. Sau đó không còn trình xử lý nào khác thực thi.

Đừng ngừng tràn khi không cần thiết!

Tràn rất tiện lợi. Đừng ngừng nó khi không có lý do thực sự: rõ ràng và được cân nhắc kỹ về mặt kiến trúc.

Đôi khi `event.stopPropagation()` tạo ra những cạm bẫy ẩn có thể trở thành vấn đề sau này.

Ví dụ:

1. Chúng ta tạo menu lồng nhau. Mỗi menu con xử lý các lần nhấp trên các phần tử của nó và gọi `stopPropagation` để menu ngoài không kích hoạt.
2. Sau đó chúng ta quyết định bắt các lần nhấp trên toàn cửa sổ, để theo dõi hành vi người dùng (nơi mọi người nhấp). Một số hệ thống phân tích làm như vậy. Thường mã dùng `document.addEventListener('click'…)` để bắt tất cả lần nhấp.
3. Phân tích của chúng ta sẽ không hoạt động trên khu vực mà các lần nhấp bị `stopPropagation` ngăn chặn. Thật đáng tiếc, chúng ta đã tạo ra một "vùng chết".

Thường không có lý do thực sự để ngăn tràn. Một nhiệm vụ tưởng chừng cần điều đó có thể giải bằng phương pháp khác. Một trong số đó là dùng sự kiện tùy chỉnh, chúng ta sẽ đề cập sau. Cũng có thể ghi dữ liệu vào đối tượng `event` trong một trình xử lý và đọc nó trong trình xử lý khác, vì vậy chúng ta có thể truyền cho trình xử lý ở phần tử cha thông tin về xử lý bên dưới.

## [Bắt giữ (Capturing)](#capturing)

Có một giai đoạn xử lý sự kiện khác gọi là "bắt giữ". Nó hiếm khi được dùng trong code thực tế, nhưng đôi khi có thể hữu ích.

Tiêu chuẩn [DOM Events](https://www.w3.org/TR/DOM-Level-3-Events/) mô tả 3 giai đoạn truyền sự kiện:

1. Giai đoạn bắt giữ – sự kiện đi xuống phần tử.
2. Giai đoạn target – sự kiện đạt đến phần tử target.
3. Giai đoạn tràn – sự kiện tràn lên từ phần tử.

Đây là hình ảnh, lấy từ đặc tả, của các giai đoạn bắt giữ `(1)`, target `(2)` và tràn `(3)` cho một sự kiện click trên `<td>` trong bảng:

![](/article/bubbling-and-capturing/eventflow.svg)

Nghĩa là: cho một lần nhấp vào `<td>`, sự kiện trước tiên đi qua chuỗi tổ tiên xuống phần tử (giai đoạn bắt giữ), sau đó nó đạt đến target và kích hoạt tại đó (giai đoạn target), và rồi nó đi lên (giai đoạn tràn), gọi trình xử lý trên đường đi.

Cho đến nay, chúng ta chỉ nói về tràn, vì giai đoạn bắt giữ hiếm khi được dùng.

Thực tế, giai đoạn bắt giữ vô hình đối với chúng ta, vì trình xử lý thêm bằng thuộc tính `on<event>` hoặc dùng thuộc tính HTML hoặc dùng `addEventListener(event, handler)` hai đối số không biết gì về bắt giữ, chúng chỉ chạy trên 2 và 3 giai đoạn.

Để bắt sự kiện ở giai đoạn bắt giữ, chúng ta cần đặt tùy chọn `capture` của trình xử lý thành `true`:

```
elem.addEventListener(..., {capture: true})

// hoặc, chỉ "true" là bí danh của {capture: true}
elem.addEventListener(..., true)
```

Có hai giá trị có thể của tùy chọn `capture`:

- Nếu nó là `false` (mặc định), thì trình xử lý được đặt ở giai đoạn tràn.
- Nếu nó là `true`, thì trình xử lý được đặt ở giai đoạn bắt giữ.

Lưu ý rằng trong khi hình thức có 3 giai đoạn, giai đoạn 2 ("giai đoạn target": sự kiện đạt đến phần tử) không được xử lý riêng: trình xử lý trên cả hai giai đoạn bắt giữ và tràn kích hoạt ở giai đoạn đó.

Hãy xem cả bắt giữ và tràn trong hành động:

```
<style>
  body * {
    margin: 10px;
    border: 1px solid blue;
  }
</style>

<form>FORM
  <div>DIV
    <p>P</p>
  </div>
</form>

<script>
  for(let elem of document.querySelectorAll('*')) {
    elem.addEventListener("click", e => alert(`Capturing: ${elem.tagName}`), true);
    elem.addEventListener("click", e => alert(`Bubbling: ${elem.tagName}`));
  }
</script>
```

Mã đặt trình xử lý click trên *mọi* phần tử trong tài liệu để xem cái nào đang hoạt động.

Nếu bạn nhấp vào `<p>`, thì trình tự là:

1. `HTML` → `BODY` → `FORM` → `DIV` → `P` (giai đoạn bắt giữ, trình lắng nghe đầu tiên):
2. `P` → `DIV` → `FORM` → `BODY` → `HTML` (giai đoạn tràn, trình lắng nghe thứ hai).

Lưu ý, `P` xuất hiện hai lần, vì chúng ta đã đặt hai trình lắng nghe: bắt giữ và tràn. Target kích hoạt ở cuối đầu tiên và ở đầu giai đoạn thứ hai.

Có thuộc tính `event.eventPhase` cho biết số giai đoạn mà sự kiện được bắt. Nhưng nó hiếm khi được dùng, vì thường chúng ta đã biết trong trình xử lý.

Để xóa trình xử lý, `removeEventListener` cần cùng giai đoạn

Nếu chúng ta `addEventListener(..., true)`, thì nên đề cập cùng giai đoạn trong `removeEventListener(..., true)` để xóa trình xử lý đúng.

Các trình lắng nghe trên cùng phần tử và cùng giai đoạn chạy theo thứ tự đặt

Nếu chúng ta có nhiều trình xử lý sự kiện trên cùng giai đoạn, gán cho cùng phần tử bằng `addEventListener`, chúng chạy theo cùng thứ tự như khi chúng được tạo:

```
elem.addEventListener("click", e => alert(1)); // đảm bảo kích hoạt đầu tiên
elem.addEventListener("click", e => alert(2));
```

`event.stopPropagation()` trong giai đoạn bắt giữ cũng ngăn tràn

Phương thức `event.stopPropagation()` và anh em của nó `event.stopImmediatePropagation()` cũng có thể được gọi trong giai đoạn bắt giữ. Khi đó không chỉ bắt giữ tiếp theo bị dừng, mà tràn cũng vậy.

Nói cách khác, bình thường sự kiện đi trước xuống ("bắt giữ") rồi sau đó lên ("tràn"). Nhưng nếu `event.stopPropagation()` được gọi trong giai đoạn bắt giữ, thì chuyến đi sự kiện dừng lại, không tràn xảy ra.

## [Tóm tắt](#summary)

Khi một sự kiện xảy ra – phần tử lồng sâu nhất nơi nó xảy ra được gắn nhãn là "phần tử target" (`event.target`).

- Sau đó sự kiện di chuyển xuống từ gốc tài liệu đến `event.target`, gọi trình xử lý gán bằng `addEventListener(..., true)` trên đường đi (`true` là bí danh của `{capture: true}`).
- Sau đó trình xử lý được gọi trên chính phần tử target.
- Sau đó sự kiện tràn lên từ `event.target` đến gốc, gọi trình xử lý gán bằng `on<event>`, thuộc tính HTML và `addEventListener` không có đối số thứ 3 hoặc với đối số thứ 3 là `false/{capture:false}`.

Mỗi trình xử lý có thể truy cập các thuộc tính đối tượng `event`:

- `event.target` – phần tử sâu nhất đã khởi tạo sự kiện.
- `event.currentTarget` (=`this`) – phần tử hiện tại đang xử lý sự kiện (phần tử có trình xử lý trên nó)
- `event.eventPhase` – giai đoạn hiện tại (bắt giữ=1, target=2, tràn=3).

Bất kỳ trình xử lý sự kiện nào cũng có thể dừng sự kiện bằng cách gọi `event.stopPropagation()`, nhưng điều đó không được khuyến nghị, vì chúng ta không thể chắc chắn sẽ không cần nó phía trên, có thể cho hoàn toàn mục đích khác.

Giai đoạn bắt giữ được dùng rất hiếm, thường chúng ta xử lý sự kiện ở giai đoạn tràn. Và có lời giải thích logic cho điều đó.

Trong thế giới thực, khi tai nạn xảy ra, cơ quan địa phương phản ứng trước. Họ hiểu rõ nhất khu vực nơi tai nạn xảy ra. Sau đó cấp cao hơn nếu cần.

Cũng giống như trình xử lý sự kiện. Code đặt trình xử lý trên một phần tử cụ thể biết tối đa chi tiết về phần tử và những gì nó làm. Trình xử lý trên một `<td>` cụ thể có thể phù hợp cho chính `<td>` đó, nó biết tất cả về nó, vì vậy nó nên nhận cơ hội trước. Sau đó phần tử cha liền kề cũng biết về ngữ cảnh, nhưng ít hơn một chút, và cứ thế cho đến phần tử đỉnh cao nhất xử lý các khái niệm chung và chạy cuối cùng.

Tràn và bắt giữ đặt nền móng cho "event delegation" – mẫu xử lý sự kiện cực kỳ mạnh mẽ mà chúng ta nghiên cứu trong chương tới.