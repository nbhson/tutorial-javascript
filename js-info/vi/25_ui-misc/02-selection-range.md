# Selection và Range (Khu vực chọn và Phạm vi)

> Source: [https://javascript.info/selection-range](https://javascript.info/selection-range)

<!-- fetched: 2026-09-14 -->

Trong chương này chúng ta sẽcover selection trong document, cũng như selection trong các form fields, như `<input>`.

JavaScript có thể truy cập một selection hiện có, select/deselect các DOM nodes như một tổng thể hoặc từng phần, xóa nội dung được chọn khỏi document, wrap nó vào một tag, và nhiều hơn nữa.

Bạn có thể tìm thấy một số recipes cho các tasks phổ biến ở cuối chương, trong phần "Tóm tắt". Có thể nó cover các nhu cầu hiện tại của bạn, nhưng bạn sẽ nhận được nhiều hơn nếu đọc toàn bộ nội dung.

Các objects `Range` và `Selection` nền tảng rất dễ hiểu, và sau đó bạn sẽ không cần recipes để làm cho chúng làm những gì bạn muốn.

## [Range](#range)

Khái niệm cơ bản của selection là [Range](https://dom.spec.whatwg.org/#ranges), về cơ bản là một cặp "boundary points": range start và range end.

Một object `Range` được tạo không có parameters:

```
let range = new Range();
```

Sau đó chúng ta có thể đặt các boundary selection bằng `range.setStart(node, offset)` và `range.setEnd(node, offset)`.

Như bạn có thể đoán, tiếp theo chúng ta sẽ dùng các object `Range` cho selection, nhưng trước tiên hãy tạo vài objects như vậy.

### [Chọn text từng phần](#selecting-the-text-partially)

Điều thú vị là argument đầu tiên `node` trong cả hai methods có thể là một text node hoặc một element node, và ý nghĩa của argument thứ hai phụ thuộc vào điều đó.

**Nếu `node` là một text node, thì `offset` phải là vị trí trong text của nó.**

Ví dụ, với element `<p>Hello</p>`, chúng ta có thể tạo range chứa các chữ cái "ll" như sau:

```
<p id="p">Hello</p>
<script>
  let range = new Range();
  range.setStart(p.firstChild, 2);
  range.setEnd(p.firstChild, 4);

  // toString của một range trả về nội dung của nó dưới dạng text
  console.log(range); // ll
</script>
```

Ở đây chúng ta lấy first child của `<p>` (đó là text node) và chỉ định các vị trí text bên trong nó:

![](/article/selection-range/range-hello-1.svg)

### [Chọn các element nodes](#selecting-element-nodes)

**Ngoài ra, nếu `node` là một element node, thì `offset` phải là số child.**

Điều đó tiện lợi cho việc tạo các range chứa các nodes như một tổng thể, không dừng ở đâu đó bên trong text của chúng.

Ví dụ, chúng ta có một fragment document phức tạp hơn:

```
<p id="p">Ví dụ: <i>nghiêng</i> và <b>đậm</b></p>
```

Đây là cấu trúc DOM của nó với cả element và text nodes:

let selectPDomtree = {
"tên": "P",
"nodeType": 1,
"children": [{
"tên": "#text",
"nodeType": 3,
"content": "Ví dụ: "
}, {
"tên": "I",
"nodeType": 1,
"children": [{
"tên": "#text",
"nodeType": 3,
"content": "nghiêng"
}]
}, {
"tên": "#text",
"nodeType": 3,
"content": " và "
}, {
"tên": "B",
"nodeType": 1,
"children": [{
"tên": "#text",
"nodeType": 3,
"content": "đậm"
}]
}]
}
drawHtmlTree(selectPDomtree, 'div.select-p-domtree', 690, 320);

Hãy tạo một range cho `"Ví dụ: <i>nghiêng</i>"`.

Như chúng ta có thể thấy, cụm từ này gồm chính xác hai children của `<p>`, với indexes `0` và `1`:

![](/article/selection-range/range-example-p-0-1.svg)

- Điểm bắt đầu có `<p>` làm parent `node`, và `0` làm offset.

  Vậy chúng ta có thể đặt nó là `range.setStart(p, 0)`.
- Điểm kết thúc cũng có `<p>` làm parent `node`, nhưng `2` là offset (nó chỉ định range cho đến, nhưng không bao gồm `offset`).

  Vậy chúng ta có thể đặt nó là `range.setEnd(p, 2)`.

Đây là demo. Nếu bạn chạy nó, bạn có thể thấy text được chọn:

```
<p id="p">Ví dụ: <i>nghiêng</i> và <b>đậm</b></p>

<script>
  let range = new Range();

  range.setStart(p, 0);
  range.setEnd(p, 2);

  // toString của một range trả về nội dung của nó dưới dạng text, không có tags
  console.log(range); // Ví dụ: nghiêng

  // áp dụng range này cho document selection (giải thích bên dưới)
  document.getSelection().addRange(range);
</script>
```

Đây là một test stand linh hoạt hơn nơi bạn có thể đặt các số range start/end và khám phá các variant khác:

```
<p id="p">Ví dụ: <i>nghiêng</i> và <b>đậm</b></p>

Từ <input id="start" type="number" value=1> – Đến <input id="end" type="number" value=4>
<button id="button">Nhấn để chọn</button>
<script>
  button.onclick = () => {
    let range = new Range();

    range.setStart(p, start.value);
    range.setEnd(p, end.value);

    // áp dụng selection, giải thích bên dưới
    document.getSelection().removeAllRanges();
    document.getSelection().addRange(range);
  };
</script>
```

Ví dụ, chọn trong cùng `<p>` từ offset `1` đến `4` cho chúng ta range `<i>nghiêng</i> và <b>đậm</b>`:

![](/article/selection-range/range-example-p-1-3.svg)

Các nodes start và end có thể khác nhau

Chúng ta không phải dùng cùng một node trong `setStart` và `setEnd`. Một range có thể trải qua nhiều nodes không liên quan. Chỉ quan trọng là end ở sau start trong document.

### [Chọn một fragment lớn hơn](#selecting-a-bigger-fragment)

Hãy chọn lớn hơn trong ví dụ của chúng ta, như thế này:

![](/article/selection-range/range-example-p-2-b-3.svg)

Chúng ta đã biết cách làm điều đó. Chúng ta chỉ cần đặt start và end là offset tương đối trong các text nodes.

Chúng ta cần tạo một range, mà:

- bắt đầu từ vị trí 2 trong first child của `<p>` (lấy tất cả trừ hai chữ cái đầu tiên của "V**í d**ụ: ")
- kết thúc tại vị trí 3 trong first child của `<b>` (lấy ba chữ cái đầu tiên của "**đậ**m", nhưng không hơn):

```
<p id="p">Ví dụ: <i>nghiêng</i> và <b>đậm</b></p>

<script>
  let range = new Range();

  range.setStart(p.firstChild, 2);
  range.setEnd(p.querySelector('b').firstChild, 3);

  console.log(range); // í dụ: nghiêng và đậ

  // dùng range này cho selection (giải thích bên dưới)
  window.getSelection().addRange(range);
</script>
```

Như bạn có thể thấy, khá dễ dàng để tạo một range của bất cứ thứ gì chúng ta muốn.

Nếu chúng ta muốn lấy các nodes như một tổng thể, chúng ta có thể truyền các elements trong `setStart/setEnd`. Nếu không, chúng ta có thể làm việc ở mức text.

## [Range properties](#range-properties)

Object range mà chúng ta tạo trong ví dụ trên có các properties sau:

![](/article/selection-range/range-example-p-2-b-3-range.svg)

- `startContainer`, `startOffset` – node và offset của start,
  - trong ví dụ trên: first text node bên trong `<p>` và `2`.
- `endContainer`, `endOffset` – node và offset của end,
  - trong ví dụ trên: first text node bên trong `<b>` và `3`.
- `collapsed` – boolean, `true` nếu range bắt đầu và kết thúc tại cùng một điểm (vậy không có nội dung bên trong range),
  - trong ví dụ trên: `false`
- `commonAncestorContainer` – common ancestor gần nhất của tất cả các nodes trong range,
  - trong ví dụ trên: `<p>`

## [Range selection methods](#range-selection-methods)

Có nhiều methods thuận tiện để thao tác với ranges.

Chúng ta đã thấy `setStart` và `setEnd`, đây là các methods tương tự khác.

Đặt range start:

- `setStart(node, offset)` đặt start tại: vị trí `offset` trong `node`
- `setStartBefore(node)` đặt start tại: ngay trước `node`
- `setStartAfter(node)` đặt start tại: ngay sau `node`

Đặt range end (các methods tương tự):

- `setEnd(node, offset)` đặt end tại: vị trí `offset` trong `node`
- `setEndBefore(node)` đặt end tại: ngay trước `node`
- `setEndAfter(node)` đặt end tại: ngay sau `node`

Về mặt kỹ thuật, `setStart/setEnd` có thể làm mọi thứ, nhưng nhiều methods hơn cung cấp sự tiện lợi hơn.

Trong tất cả các methods này, `node` có thể là cả text hoặc element node: đối với text nodes `offset` bỏ qua bấy nhiêu ký tự, trong khi đối với element nodes là bấy nhiêu child nodes.

Còn nhiều methods hơn để tạo ranges:

- `selectNode(node)` đặt range để chọn toàn bộ `node`
- `selectNodeContents(node)` đặt range để chọn toàn bộ nội dung của `node`
- `collapse(toStart)` nếu `toStart=true` đặt end=start, nếu không đặt start=end, do đó collapse range
- `cloneRange()` tạo một range mới với start/end giống nhau

## [Range editing methods](#range-editing-methods)

Một khi range được tạo, chúng ta có thể thao tác nội dung của nó bằng các methods sau:

- `deleteContents()` – xóa nội dung range khỏi document
- `extractContents()` – xóa nội dung range khỏi document và trả về dưới dạng [DocumentFragment](/modifying-document#document-fragment)
- `cloneContents()` – clone nội dung range và trả về dưới dạng [DocumentFragment](/modifying-document#document-fragment)
- `insertNode(node)` – chèn `node` vào document tại đầu range
- `surroundContents(node)` – wrap `node` quanh nội dung range. Để điều này hoạt động, range phải chứa cả opening và closing tags cho tất cả elements bên trong nó: không có partial ranges như `<i>abc`.

Với các methods này chúng ta có thể làm về cơ bản bất cứ thứ gì với các nodes được chọn.

Đây là test stand để xem chúng hoạt động:

```
Nhấn các nút để chạy các methods trên selection, "resetExample" để reset nó.

<p id="p">Ví dụ: <i>nghiêng</i> và <b>đậm</b></p>

<p id="result"></p>
<script>
  let range = new Range();

  // Mỗi method được demo được biểu diễn ở đây:
  let methods = {
    deleteContents() {
      range.deleteContents()
    },
    extractContents() {
      let content = range.extractContents();
      result.innerHTML = "";
      result.append("đã extract: ", content);
    },
    cloneContents() {
      let content = range.cloneContents();
      result.innerHTML = "";
      result.append("đã clone: ", content);
    },
    insertNode() {
      let newNode = document.createElement('u');
      newNode.innerHTML = "NODE MỚI";
      range.insertNode(newNode);
    },
    surroundContents() {
      let newNode = document.createElement('u');
      try {
        range.surroundContents(newNode);
      } catch(e) { console.log(e) }
    },
    resetExample() {
      p.innerHTML = `Ví dụ: <i>nghiêng</i> và <b>đậm</b>`;
      result.innerHTML = "";

      range.setStart(p.firstChild, 2);
      range.setEnd(p.querySelector('b').firstChild, 3);

      window.getSelection().removeAllRanges();
      window.getSelection().addRange(range);
    }
  };

  for(let method in methods) {
    document.write(`<div><button onclick="methods.${method}()">${method}</button></div>`);
  }

  methods.resetExample();
</script>
```

Cũng tồn tại các methods để so sánh các range, nhưng những cái này hiếm khi được sử dụng. Khi bạn cần chúng, vui lòng tham khảo [spec](https://dom.spec.whatwg.org/#interface-range) hoặc [MDN manual](https://developer.mozilla.org/en-US/docs/Web/api/Range).

## [Selection](#selection)

`Range` là một object chung để quản lý các selection ranges. Mặc dù, tạo một `Range` không có nghĩa là chúng ta thấy một selection trên màn hình.

Chúng ta có thể tạo các object `Range`, truyền chúng đi – chúng không tự chọn bất cứ thứ gì trực quan.

Selection document được biểu diễn bởi object `Selection`, có thể lấy được bằng `window.getSelection()` hoặc `document.getSelection()`. Một selection có thể chứa zero hoặc nhiều ranges. Ít nhất, [Selection API specification](https://www.w3.org/TR/selection-api/) nói vậy. Thực tế tuy nhiên, chỉ Firefox cho phép chọn nhiều range trong document bằng cách dùng `Ctrl+click` (`Cmd+click` cho Mac).

Đây là một screenshot của một selection với 3 ranges, được tạo trong Firefox:

![](/article/selection-range/selection-firefox.svg)

Các trình duyệt khác hỗ trợ tối đa 1 range. Như chúng ta sẽ thấy, một số methods `Selection` ngụ ý rằng có thể có nhiều ranges, nhưng một lần nữa, trong tất cả các trình duyệt trừ Firefox, có tối đa 1.

Đây là một demo nhỏ hiển thị selection hiện tại (chọn thứ gì đó và click) dưới dạng text:

alert(document.getSelection())

## [Selection properties](#selection-properties)

Như đã nói, một selection về lý thuyết có thể chứa nhiều ranges. Chúng ta có thể lấy các range objects này bằng method:

- `getRangeAt(i)` – lấy range thứ i, bắt đầu từ `0`. Trong tất cả các trình duyệt trừ Firefox, chỉ `0` được dùng.

Ngoài ra, tồn tại các properties thường cung cấp sự tiện lợi tốt hơn.

Tương tự như range, một selection object có start, gọi là "anchor", và end, gọi là "focus".

Các selection properties chính là:

- `anchorNode` – node nơi selection bắt đầu,
- `anchorOffset` – offset trong `anchorNode` nơi selection bắt đầu,
- `focusNode` – node nơi selection kết thúc,
- `focusOffset` – offset trong `focusNode` nơi selection kết thúc,
- `isCollapsed` – `true` nếu selection không chọn gì (empty range), hoặc không tồn tại.
- `rangeCount` – số ranges trong selection, tối đa `1` trong tất cả các trình duyệt trừ Firefox.

Selection end/start vs Range

Có một sự khác biệt quan trọng giữa selection anchor/focus so với range start/end.

Như chúng ta biết, các object `Range` luôn có start trước end.

Đối với selections, điều đó không phải luôn đúng.

Việc chọn thứ gì đó bằng chuột có thể được thực hiện theo cả hai hướng:either "left-to-right" hoặc "right-to-left".

Nói cách khác, khi nút chuột được nhấn, và sau đó nó di chuyển tiến về phía trước trong document, thì end của nó (focus) sẽ ở sau start của nó (anchor).

Ví dụ, nếu người dùng bắt đầu chọn bằng chuột và đi từ "Ví dụ" đến "nghiêng":

![](/article/selection-range/selection-direction-forward.svg)

…Nhưng cùng selection có thể được thực hiện theo chiều ngược lại: bắt đầu từ "nghiêng" đến "Ví dụ" (hướng ngược lại), thì end của nó (focus) sẽ ở trước start (anchor):

![](/article/selection-range/selection-direction-backward.svg)

## [Selection events](#selection-events)

Có các events để theo dõi selection:

- `elem.onselectstart` – khi selection *bắt đầu* cụ thể trên element `elem` (hoặc bên trong nó). Ví dụ, khi người dùng nhấn nút chuột trên nó và bắt đầu di chuyển con trỏ.
  - Ngăn阻止 default action hủy bắt đầu selection. Vậy bắt đầu selection từ element này trở nên không thể, nhưng element vẫn có thể được select. Người truy cập chỉ cần bắt đầu selection từ nơi khác.
- `document.onselectionchange` – bất cứ khi nào selection thay đổi hoặc bắt đầu.
  - Xin lưu ý: handler này chỉ có thể được đặt trên `document`, nó track tất cả selections trong đó.

### [Demo tracking selection](#selection-tracking-demo)

Đây là một demo nhỏ. Nó track selection hiện tại trên `document` và hiển thị các boundary của nó:

```
<p id="p">Chọn tôi: <i>nghiêng</i> và <b>đậm</b></p>

Từ <input id="from" disabled> – Đến <input id="to" disabled>
<script>
  document.onselectionchange = function() {
    let selection = document.getSelection();

    let {anchorNode, anchorOffset, focusNode, focusOffset} = selection;

    // anchorNode và focusNode thường là các text nodes
    from.value = `${anchorNode?.data}, offset ${anchorOffset}`;
    to.value = `${focusNode?.data}, offset ${focusOffset}`;
  };
</script>
```

### [Demo copy selection](#selection-copying-demo)

Có hai approaches để copy nội dung được chọn:

1. Chúng ta có thể dùng `document.getSelection().toString()` để lấy nó dưới dạng text.
2. Nếu không, để copy full DOM, ví dụ nếu chúng ta cần giữ formatting, chúng ta có thể lấy các underlying ranges bằng `getRangeAt(...)`. Một `Range` object, mặt khác, có method `cloneContents()` clone nội dung của nó và trả về dưới dạng object `DocumentFragment`, mà chúng ta có thể chèn ở nơi khác.

Đây là demo của việc copy nội dung được chọn cả dưới dạng text và dưới dạng các nodes DOM:

```
<p id="p">Chọn tôi: <i>nghiêng</i> và <b>đậm</b></p>

Đã clone: <span id="cloned"></span>
<br>
Dưới dạng text: <span id="astext"></span>

<script>
  document.onselectionchange = function() {
    let selection = document.getSelection();

    cloned.innerHTML = astext.innerHTML = "";

    // Clone các DOM nodes từ các ranges (chúng ta hỗ trợ multiselect ở đây)
    for (let i = 0; i < selection.rangeCount; i++) {
      cloned.append(selection.getRangeAt(i).cloneContents());
    }

    // Lấy dưới dạng text
    astext.innerHTML += selection;
  };
</script>
```

## [Selection methods](#selection-methods)

Chúng ta có thể làm việc với selection bằng cách thêm/xóa các ranges:

- `getRangeAt(i)` – lấy range thứ i, bắt đầu từ `0`. Trong tất cả các trình duyệt trừ Firefox, chỉ `0` được dùng.
- `addRange(range)` – thêm `range` vào selection. Tất cả các trình duyệt trừ Firefox bỏ qua call, nếu selection đã có một range liên quan.
- `removeRange(range)` – xóa `range` khỏi selection.
- `removeAllRanges()` – xóa tất cả các ranges.
- `empty()` – alias của `removeAllRanges`.

Cũng có các methods tiện lợi để thao tác trực tiếp với selection range, không cần các calls `Range` trung gian:

- `collapse(node, offset)` – thay thế range được chọn bằng một range mới bắt đầu và kết thúc tại `node` đã cho, ở vị trí `offset`.
- `setPosition(node, offset)` – alias của `collapse`.
- `collapseToStart()` – collapse (thay thế bằng empty range) về start selection,
- `collapseToEnd()` – collapse về end selection,
- `extend(node, offset)` – di chuyển focus của selection đến `node` đã cho, vị trí `offset`,
- `setBaseAndExtent(anchorNode, anchorOffset, focusNode, focusOffset)` – thay thế selection range bằng start đã cho `anchorNode/anchorOffset` và end `focusNode/focusOffset`. Tất cả nội dung giữa chúng được chọn.
- `selectAllChildren(node)` – chọn tất cả children của `node`.
- `deleteFromDocument()` – xóa nội dung được chọn khỏi document.
- `containsNode(node, allowPartialContainment = false)` – kiểm tra xem selection có chứa `node` hay không (phần nếu argument thứ hai là `true`)

Đối với hầu hết các tasks, các methods này là đủ, không cần truy cập object `Range` underlying.

Ví dụ, chọn toàn bộ nội dung của paragraph `<p>`:

```
<p id="p">Chọn tôi: <i>nghiêng</i> và <b>đậm</b></p>

<script>
  // chọn từ child thứ 0 của <p> đến child cuối cùng
  document.getSelection().setBaseAndExtent(p, 0, p, p.childNodes.length);
</script>
```

Cùng điều đó bằng cách dùng ranges:

```
<p id="p">Chọn tôi: <i>nghiêng</i> và <b>đậm</b></p>

<script>
  let range = new Range();
  range.selectNodeContents(p); // hoặc selectNode(p) để chọn cả thẻ <p>

  document.getSelection().removeAllRanges(); // xóa selection hiện có nếu có
  document.getSelection().addRange(range);
</script>
```

Để chọn thứ gì đó, xóa selection hiện có trước

Nếu một document selection đã tồn tại, hãy xóa nó trước bằng `removeAllRanges()`. Và sau đó thêm các ranges. Nếu không, tất cả các trình duyệt trừ Firefox bỏ qua các ranges mới.

Ngoại lệ là một số methods selection, thay thế selection hiện có, như `setBaseAndExtent`.

## [Selection trong form controls](#selection-in-form-controls)

Các form elements, như `input` và `textarea` cung cấp [special API cho selection](https://html.spec.whatwg.org/#textFieldSelection), không có objects `Selection` hoặc `Range`. Vì giá trị input là pure text, không phải HTML, không cần các objects như vậy, mọi thứ đơn giản hơn nhiều.

Properties:

- `input.selectionStart` – vị trí bắt đầu selection (có thể ghi),
- `input.selectionEnd` – vị trí kết thúc selection (có thể ghi),
- `input.selectionDirection` – hướng selection, một trong: "forward", "backward" hoặc "none" (nếu ví dụ được chọn bằng double mouse click),

Events:

- `input.onselect` – kích hoạt khi có thứ gì đó được chọn.

Methods:

- `input.select()` – chọn tất cả trong text control (có thể là `textarea` thay vì `input`),
- `input.setSelectionRange(start, end, [direction])` – thay đổi selection để span từ vị trí `start` đến `end`, theo direction đã cho (optional).
- `input.setRangeText(replacement, [start], [end], [selectionMode])` – thay thế một range của text bằng text mới.

  Các optional arguments `start` và `end`, nếu được cung cấp, đặt range start và end, nếu không dùng user selection.

  Argument cuối cùng, `selectionMode`, xác định cách selection sẽ được đặt sau khi text đã được thay thế. Các giá trị có thể là:

  - `"select"` – text mới được chèn sẽ được chọn.
  - `"start"` – selection range collapse ngay trước text đã chèn (con trỏ sẽ ngay trước nó).
  - `"end"` – selection range collapse ngay sau text đã chèn (con trỏ sẽ ngay sau nó).
  - `"preserve"` – cố gắng giữ selection. Đây là mặc định.

Giờ hãy xem các methods này hoạt động.

### [Ví dụ: tracking selection](#example-tracking-selection)

Ví dụ, code này dùng sự kiện `onselect` để track selection:

```
<textarea id="area" style="width:80%;height:60px">
Chọn trong text này cập nhật các giá trị bên dưới.
</textarea>
<br>
Từ <input id="from" disabled> – Đến <input id="to" disabled>

<script>
  area.onselect = function() {
    from.value = area.selectionStart;
    to.value = area.selectionEnd;
  };
</script>
```

Xin lưu ý:

- `onselect` kích hoạt khi có thứ gì đó được chọn, nhưng không phải khi selection bị xóa.
- Sự kiện `document.onselectionchange` không nên kích hoạt cho các selections bên trong một form control, theo [spec](https://w3c.github.io/selection-api/#dfn-selectionchange), vì nó không liên quan đến selection và ranges của `document`. Một số trình duyệt sinh ra nó, nhưng chúng ta không nên dựa vào nó.

### [Ví dụ: di chuyển cursor](#example-moving-cursor)

Chúng ta có thể thay đổi `selectionStart` và `selectionEnd`, điều đó đặt selection.

Một edge case quan trọng là khi `selectionStart` và `selectionEnd` bằng nhau. Sau đó nó chính xác là vị trí cursor. Hay nói cách khác, khi không có gì được chọn, selection được collapse tại vị trí cursor.

Vậy, bằng cách đặt `selectionStart` và `selectionEnd` bằng nhau, chúng ta di chuyển cursor.

Ví dụ:

```
<textarea id="area" style="width:80%;height:60px">
Focus vào tôi, cursor sẽ ở vị trí 10.
</textarea>

<script>
  area.onfocus = () => {
    // zero delay setTimeout để chạy sau khi hành động "focus" của browser kết thúc
    setTimeout(() => {
      // chúng ta có thể đặt bất kỳ selection nào
      // nếu start=end, cursor chính xác ở vị trí đó
      area.selectionStart = area.selectionEnd = 10;
    });
  };
</script>
```

### [Ví dụ: sửa đổi selection](#example-modifying-selection)

Để sửa đổi nội dung của selection, chúng ta có thể dùng method `input.setRangeText()`. Tất nhiên, chúng ta có thể đọc `selectionStart/End` và, với kiến thức về selection, thay đổi substring tương ứng của `value`, nhưng `setRangeText` mạnh mẽ hơn và thường tiện hơn.

Đó là một method phức tạp. Ở dạng đơn giản nhất một argument, nó thay thế range được người dùng chọn và xóa selection.

Ví dụ, ở đây selection của người dùng sẽ được wrap bởi `*...*`:

```
<input id="input" style="width:200px" value="Chọn ở đây và nhấn nút">
<button id="button">Wrap selection trong dấu sao *...*</button>

<script>
button.onclick = () => {
  if (input.selectionStart == input.selectionEnd) {
    return; // không có gì được chọn
  }

  let selected = input.value.slice(input.selectionStart, input.selectionEnd);
  input.setRangeText(`*${selected}*`);
};
</script>
```

Với nhiều arguments hơn, chúng ta có thể đặt range `start` và `end`.

Trong ví dụ này chúng ta tìm `"THIS"` trong input text, thay thế nó và giữ selection:

```
<input id="input" style="width:200px" value="Thay thế THIS trong text">
<button id="button">Thay thế THIS</button>

<script>
button.onclick = () => {
  let pos = input.value.indexOf("THIS");
  if (pos >= 0) {
    input.setRangeText("*THIS*", pos, pos + 4, "select");
    input.focus(); // focus để làm selection hiển thị
  }
};
</script>
```

### [Ví dụ: chèn tại cursor](#example-insert-at-cursor)

Nếu không có gì được chọn, hoặc chúng ta dùng equal `start` và `end` trong `setRangeText`, thì text mới chỉ được chèn, không có gì bị xóa.

Chúng ta cũng có thể chèn thứ gì đó "tại cursor" bằng `setRangeText`.

Đây là một nút chèn `"HELLO"` tại vị trí cursor và đặt cursor ngay sau nó. Nếu selection không rỗng, thì nó được thay thế (chúng ta có thể phát hiện nó bằng cách so sánh `selectionStart!=selectionEnd` và làm gì đó khác thay thế):

```
<input id="input" style="width:200px" value="Text Text Text Text Text">
<button id="button">Chèn "HELLO" tại cursor</button>

<script>
  button.onclick = () => {
    input.setRangeText("HELLO", input.selectionStart, input.selectionEnd, "end");
    input.focus();
  };
</script>
```

## [Làm không thể chọn](#making-unselectable)

Để làm cho thứ gì đó không thể chọn, có ba cách:

1. Dùng CSS property `user-select: none`.

   ```
   <style>
   #elem {
     user-select: none;
   }
   </style>
   <div>Có thể chọn <div id="elem">Không thể chọn</div> Có thể chọn</div>
   ```

   Điều này không cho phép selection bắt đầu tại `elem`. Nhưng người dùng có thể bắt đầu selection từ nơi khác và bao gồm `elem` vào nó.

   Sau đó `elem` sẽ trở thành một phần của `document.getSelection()`, vậy selection thực sự xảy ra, nhưng nội dung của nó thường bị bỏ qua trong copy-paste.
2. Ngăn阻止 default action trong `onselectstart` hoặc `mousedown` events.

   ```
   <div>Có thể chọn <div id="elem">Không thể chọn</div> Có thể chọn</div>

   <script>
     elem.onselectstart = () => false;
   </script>
   ```

   Điều này ngăn阻止 bắt đầu selection trên `elem`, nhưng người truy cập có thể bắt đầu nó tại một element khác, sau đó extend đến `elem`.

   Điều đó tiện lợi khi có một handler sự kiện khác trên cùng hành động kích hoạt selection (ví dụ `mousedown`). Vậy chúng ta vô hiệu hóa selection để tránh conflict, vẫn cho phép nội dung `elem` được copy.
3. Chúng ta cũng có thể xóa selection post-factum sau khi nó xảy ra với `document.getSelection().empty()`. Điều đó hiếm khi được dùng, vì điều này gây blinking không mong muốn khi selection xuất hiện-biến mất.

## [References](#references)

- [DOM spec: Range](https://dom.spec.whatwg.org/#ranges)
- [Selection API](https://www.w3.org/TR/selection-api/#dom-globaleventhandlers-onselectstart)
- [HTML spec: APIs cho text control selections](https://html.spec.whatwg.org/multipage/form-control-infrastructure.html#textFieldSelection)

## [Tóm tắt](#summary)

Chúng ta đã cover hai APIs khác nhau cho selections:

1. Cho document: các object `Selection` và `Range`.
2. Cho `input`, `textarea`: các methods và properties bổ sung.

API thứ hai rất đơn giản, vì nó làm việc với text.

Các recipes được dùng nhiều nhất có lẽ là:

1. Lấy selection:

   ```
   let selection = document.getSelection();

   let cloned = /* element để clone các nodes được chọn */;

   // sau đó áp dụng Range methods lên selection.getRangeAt(0)
   // hoặc, như ở đây, lên tất cả ranges để hỗ trợ multi-select
   for (let i = 0; i < selection.rangeCount; i++) {
     cloned.append(selection.getRangeAt(i).cloneContents());
   }
   ```
2. Đặt selection:

   ```
   let selection = document.getSelection();

   // trực tiếp:
   selection.setBaseAndExtent(...từ...đến...);

   // hoặc chúng ta có thể tạo một range và:
   selection.removeAllRanges();
   selection.addRange(range);
   ```

Và cuối cùng, về cursor. Vị trí cursor trong các elements có thể edit, như `<textarea>` luôn ở start hoặc end của selection. Chúng ta có thể dùng nó để lấy vị trí cursor hoặc để di chuyển cursor bằng cách đặt `elem.selectionStart` và `elem.selectionEnd`.
