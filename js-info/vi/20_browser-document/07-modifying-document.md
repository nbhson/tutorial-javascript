# Sửa đổi tài liệu (Modifying the document)

> Nguồn: [https://javascript.info/modifying-document](https://javascript.info/modifying-document)

<!-- fetched: 2026-09-14 -->

DOM modification là key để tạo các pages "live".

Ở đây chúng ta sẽ thấy cách tạo new elements "on the fly" và modify existing page content.

## [Example: show a message]( #example-show-a-message)

Hãy demonstrate bằng một ví dụ. Chúng ta sẽ thêm một message trên page trông đẹp hơn `alert`.

Đây là nó sẽ trông như thế nào:

```
<style>
.alert {
  padding: 15px;
  border: 1px solid #d6e9c6;
  border-radius: 4px;
  color: #3c763d;
  background-color: #dff0d8;
}
</style>

<div class="alert">
  <strong>Hi there!</strong> You've read an important message.
</div>
```

Đó là ví dụ HTML. Bây giờ hãy tạo cùng `div` bằng JavaScript (giả sử styles đã có trong HTML/CSS).

## [Creating an element]( #creating-an-element)

Để tạo DOM nodes, có hai methods:

`document.createElement(tag)`
:   Tạo mới *element node* với tag đã cho:

    ```
    let div = document.createElement('div');
    ```

`document.createTextNode(text)`
:   Tạo mới *text node* với text đã cho:

    ```
    let textNode = document.createTextNode('Here I am');
    ```

Hầu hết thời gian chúng ta cần tạo element nodes, như `div` cho message.

### [Creating the message]( #creating-the-message)

Tạo message div tốn 3 steps:

```
 // 1. Create <div> element
let div = document.createElement('div');

 // 2. Set its class to "alert"
div.className = "alert";

 // 3. Fill it with the content
div.innerHTML = "<strong>Hi there!</strong> You've read an important message.";
```

Chúng ta đã tạo element. Nhưng hiện tại nó chỉ ở trong variable `div`, chưa có trong page. Vì vậy chúng ta không thể thấy nó.

## [Insertion methods]( #insertion-methods)

Để làm `div` hiển thị, chúng ta cần insert nó vào đâu đó trong `document`. Ví dụ, vào `<body>` element, được reference bởi `document.body`.

Có method đặc biệt `append` cho việc đó: `document.body.append(div)`.

Đây là full code:

```
<style>
.alert {
  padding: 15px;
  border: 1px solid #d6e9c6;
  border-radius: 4px;
  color: #3c763d;
  background-color: #dff0d8;
}
</style>

<script>
  let div = document.createElement('div');
  div.className = "alert";
  div.innerHTML = "<strong>Hi there!</strong> You've read an important message.";

  document.body.append(div);
</script>
```

Ở đây chúng ta gọi `append` trên `document.body`, nhưng chúng ta có thể gọi `append` method trên bất kỳ element nào khác, để put another element vào trong nó. Ví dụ, chúng ta có thể append something vào `<div>` bằng cách gọi `div.append(anotherElement)`.

Dưới đây là thêm insertion methods, chúng chỉ định các nơi khác nhau để insert:

- `node.append(...nodes or strings)` – append nodes or strings *at the end* của `node`,
- `node.prepend(...nodes or strings)` – insert nodes or strings *at the beginning* của `node`,
- `node.before(...nodes or strings)` –- insert nodes or strings *before* `node`,
- `node.after(...nodes or strings)` –- insert nodes or strings *after* `node`,
- `node.replaceWith(...nodes or strings)` –- replaces `node` với given nodes or strings.

Arguments của các methods này là một arbitrary list của DOM nodes để insert, hoặc text strings (trở thành text nodes tự động).

Hãy xem chúng trong action.

Đây là ví dụ dùng các methods này để add items vào list và text before/after nó:

```
<ol id="ol">
  <li>0</li>
  <li>1</li>
  <li>2</li>
</ol>

<script>
  ol.before('before'); // insert string "before" before <ol>
  ol.after('after'); // insert string "after" after <ol>

  let liFirst = document.createElement('li');
  liFirst.innerHTML = 'prepend';
  ol.prepend(liFirst); // insert liFirst at the beginning of <ol>

  let liLast = document.createElement('li');
  liLast.innerHTML = 'append';
  ol.append(liLast); // insert liLast at the end of <ol>
</script>
```

Đây là hình ảnh trực quan của những gì các methods làm:

![](/article/modifying-document/before-prepend-append-after.svg)

Vì vậy final list sẽ là:

```
before
<ol id="ol">
  <li>prepend</li>
  <li>0</li>
  <li>1</li>
  <li>2</li>
  <li>append</li>
</ol>
after
```

Như đã nói, các methods này có thể insert multiple nodes và text pieces trong một single call.

Ví dụ, ở đây một string và element được insert:

```
<div id="div"></div>
<script>
  div.before('<p>Hello</p>', document.createElement('hr'));
</script>
```

Xin lưu ý: text được insert "as text", không phải "as HTML", với proper escaping của các characters như `<`, `>`.

Vì vậy final HTML là:

```
<p>Hello</p>
<hr>
<div id="div"></div>
```

Nói cách khác, strings được insert theo cách safe, như `elem.textContent` làm.

Vì vậy, các methods này chỉ có thể dùng để insert DOM nodes hoặc text pieces.

Nhưng nếu chúng ta muốn insert HTML string "as html", với tất cả tags và stuff working, giống như `elem.innerHTML` làm?

## [insertAdjacentHTML/Text/Element]( #insertadjacenthtml-text-element)

Cho việc đó chúng ta có thể dùng method khác, pretty versatile: `elem.insertAdjacentHTML(where, html)`.

Tham số đầu tiên là code word, chỉ định nơi insert relative to `elem`. Phải là một trong sau:

- `"beforebegin"` – insert `html` ngay trước `elem`,
- `"afterbegin"` – insert `html` vào `elem`, at the beginning,
- `"beforeend"` – insert `html` vào `elem`, at the end,
- `"afterend"` – insert `html` ngay sau `elem`.

Tham số thứ hai là HTML string, được insert "as HTML".

Ví dụ:

```
<div id="div"></div>
<script>
  div.insertAdjacentHTML('beforebegin', '<p>Hello</p>');
  div.insertAdjacentHTML('afterend', '<p>Bye</p>');
</script>
```

…Sẽ dẫn đến:

```
<p>Hello</p>
<div id="div"></div>
<p>Bye</p>
```

Đó là cách chúng ta có thể append arbitrary HTML to the page.

Đây là hình ảnh của insertion variants:

![](/article/modifying-document/insert-adjacent.svg)

Chúng ta có thể dễ dàng nhận thấy similarities giữa này và hình trước. Insertion points thực sự là same, nhưng method này insert HTML.

Method có hai brothers:

- `elem.insertAdjacentText(where, text)` – same syntax, nhưng string `text` được insert "as text" thay vì HTML,
- `elem.insertAdjacentElement(where, elem)` – same syntax, nhưng insert element.

Chúng tồn tại mainly để make syntax "uniform". Trong thực tế, chỉ `insertAdjacentHTML` được dùng hầu hết thời gian. Vì cho elements và text, chúng ta có methods `append/prepend/before/after` – chúng ngắn hơn để viết và có thể insert nodes/text pieces.

Vì vậy đây là alternative variant của showing a message:

```
<style>
.alert {
  padding: 15px;
  border: 1px solid #d6e9c6;
  border-radius: 4px;
  color: #3c763d;
  background-color: #dff0d8;
}
</style>

<script>
  document.body.insertAdjacentHTML("afterbegin", `<div class="alert">
    <strong>Hi there!</strong> You've read an important message.
  </div>`);
</script>
```

## [Node removal]( #node-removal)

Để remove node, có method `node.remove()`.

Hãy làm message của chúng ta disappear sau một giây:

```
<style>
.alert {
  padding: 15px;
  border: 1px solid #d6e9c6;
  border-radius: 4px;
  color: #3c763d;
  background-color: #dff0d8;
}
</style>

<script>
  let div = document.createElement('div');
  div.className = "alert";
  div.innerHTML = "<strong>Hi there!</strong> You've read an important message.";

  document.body.append(div);
  setTimeout(() => div.remove(), 1000);
</script>
```

Xin lưu ý: nếu chúng ta muốn *move* element sang nơi khác – không cần remove nó từ nơi cũ.

**Tất cả insertion methods tự động remove node khỏi nơi cũ.**

Ví dụ, hãy swap elements:

```
<div id="first">First</div>
<div id="second">Second</div>
<script>
  // no need to call remove
  second.after(first); // take #second and after it insert #first
</script>
```

## [Cloning nodes: cloneNode]( #cloning-nodes-clonenode)

Làm thế nào để insert một message tương tự nữa?

Chúng ta có thể tạo function và put code ở đó. Nhưng alternative way là *clone* existing `div` và modify text bên trong nó (nếu cần).

Đôi khi khi chúng ta có big element, đó có thể faster và simpler.

- Call `elem.cloneNode(true)` tạo "deep" clone của element – với tất cả attributes và subelements. Nếu chúng ta gọi `elem.cloneNode(false)`, thì clone được tạo không có child elements.

Ví dụ về copy message:

```
<style>
.alert {
  padding: 15px;
  border: 1px solid #d6e9c6;
  border-radius: 4px;
  color: #3c763d;
  background-color: #dff0d8;
}
</style>

<div class="alert" id="div">
  <strong>Hi there!</strong> You've read an important message.
</div>

<script>
  let div2 = div.cloneNode(true); // clone the message
  div2.querySelector('strong').innerHTML = 'Bye there!'; // change the clone

  div.after(div2); // show the clone after the existing div
</script>
```

## [DocumentFragment]( #document-fragment)

`DocumentFragment` là một special DOM node đóng vai trò wrapper để pass around lists of nodes.

Chúng ta có thể append other nodes vào nó, nhưng khi chúng ta insert nó ở đâu đó, thì content của nó được insert thay thế.

Ví dụ, `getListContent` dưới đây tạo fragment với `<li>` items, sau đó insert vào `<ul>`:

```
<ul id="ul"></ul>

<script>
function getListContent() {
  let fragment = new DocumentFragment();

  for(let i=1; i<=3; i++) {
    let li = document.createElement('li');
    li.append(i);
    fragment.append(li);
  }

  return fragment;
}

ul.append(getListContent()); // (*)
</script>
```

Xin lưu ý, ở dòng cuối `(*)` chúng ta append `DocumentFragment`, nhưng nó "blends in", vì vậy resulting structure sẽ là:

```
<ul>
  <li>1</li>
  <li>2</li>
  <li>3</li>
</ul>
```

`DocumentFragment` hiếm khi được dùng explicitly. Tại sao append vào special kind of node, nếu chúng ta có thể return array of nodes instead? Rewritten example:

```
<ul id="ul"></ul>

<script>
function getListContent() {
  let result = [];

  for(let i=1; i<=3; i++) {
    let li = document.createElement('li');
    li.append(i);
    result.push(li);
  }

  return result;
}

ul.append(...getListContent()); // append + "..." operator = friends!
</script>
```

Chúng ta nhắc đến `DocumentFragment` chủ yếu vì có một số concepts trên nó, như [template](/template-element) element, mà chúng ta sẽ cover sau này.

## [Old-school insert/remove methods]( #old-school-insert-remove-methods)

Old school

Thông tin này giúp hiểu old scripts, nhưng không cần cho new development.

Có thêm "old school" DOM manipulation methods, tồn tại vì historical reasons.

Các methods này đến từ really ancient times. Ngày nay, không có lý do để dùng chúng, vì modern methods, như `append`, `prepend`, `before`, `after`, `remove`, `replaceWith`, linh hoạt hơn.

Lý do duy nhất chúng ta list các methods ở đây là bạn có thể tìm thấy chúng trong nhiều old scripts:

`parentElem.appendChild(node)`
:   Appends `node` as the last child của `parentElem`.

    Ví dụ sau adds new `<li>` to the end của `<ol>`:

    ```
    <ol id="list">
      <li>0</li>
      <li>1</li>
      <li>2</li>
    </ol>

    <script>
      let newLi = document.createElement('li');
      newLi.innerHTML = 'Hello, world!';

      list.appendChild(newLi);
    </script>
    ```

`parentElem.insertBefore(node, nextSibling)`
:   Inserts `node` before `nextSibling` vào `parentElem`.

    Code dưới đây inserts new list item before second `<li>`:

    ```
    <ol id="list">
      <li>0</li>
      <li>1</li>
      <li>2</li>
    </ol>
    <script>
      let newLi = document.createElement('li');
      newLi.innerHTML = 'Hello, world!';

      list.insertBefore(newLi, list.children[1]);
    </script>
    ```

    Để insert `newLi` as the first element, chúng ta có thể làm như này:

    ```
    list.insertBefore(newLi, list.firstChild);
    ```

`parentElem.replaceChild(node, oldChild)`
:   Replaces `oldChild` với `node` among children của `parentElem`.

`parentElem.removeChild(node)`
:   Removes `node` từ `parentElem` (giả sử `node` là its child).

    Ví dụ sau removes first `<li>` từ `<ol>`:

    ```
    <ol id="list">
      <li>0</li>
      <li>1</li>
      <li>2</li>
    </ol>

    <script>
      let li = list.firstElementChild;
      list.removeChild(li);
    </script>
    ```

Tất cả các methods này return inserted/removed node. Nói cách khác, `parentElem.appendChild(node)` trả về `node`. Nhưng thường returned value không được dùng, chúng ta chỉ run method.

## [A word about "document.write"]( #a-word-about-document-write)

Có thêm một, very ancient method để add something to web-page: `document.write`.

Cú pháp:

```
<p>Somewhere in the page...</p>
<script>
  document.write('<b>Hello from JS</b>');
</script>
<p>The end</p>
```

Call to `document.write(html)` viết `html` vào page "right here and now". `html` string có thể được dynamically generated, vì vậy nó kind of flexible. Chúng ta có thể dùng JavaScript để tạo full-fledged webpage và write nó.

Method này đến từ times khi không có DOM, không có standards… Really old times. Nó vẫn sống, vì có scripts dùng nó.

Trong modern scripts chúng ta hiếm khi thấy nó, vì limitation quan trọng sau:

**Call to `document.write` chỉ works while the page is loading.**

Nếu chúng ta call nó sau đó, existing document content bị erased.

Ví dụ:

```
<p>After one second the contents of this page will be replaced...</p>
<script>
  // document.write after 1 second
  // that's after the page loaded, so it erases the existing content
  setTimeout(() => document.write('<b>...By this.</b>'), 1000);
</script>
```

Vì vậy nó kind of unusable at "after loaded" stage, khác với các DOM methods chúng ta cover ở trên.

Đó là downside.

Có upside cũng. Về mặt kỹ thuật, khi `document.write` được called while browser đang đọc ("parsing") incoming HTML, và nó viết something, browser consume nó just as if it were initially there, in the HTML text.

Vì vậy nó works blazingly fast, vì không có *DOM modification* involved. Nó viết directly vào page text, while DOM chưa được built.

Vì vậy nếu chúng ta cần add a lot of text vào HTML dynamically, và chúng ta ở page loading phase, và speed matters, nó có thể help. Nhưng trong thực tế these requirements rarely come together. Và thường chúng ta thấy method này trong scripts chỉ vì chúng old.

## [Summary]( #summary)

- Methods để tạo new nodes:

  - `document.createElement(tag)` – tạo element với tag đã cho,
  - `document.createTextNode(value)` – tạo text node (rarely used),
  - `elem.cloneNode(deep)` – clone element, nếu `deep==true` thì với all descendants.
- Insertion and removal:

  - `node.append(...nodes or strings)` – insert vào `node`, at the end,
  - `node.prepend(...nodes or strings)` – insert vào `node`, at the beginning,
  - `node.before(...nodes or strings)` –- insert right before `node`,
  - `node.after(...nodes or strings)` –- insert right after `node`,
  - `node.replaceWith(...nodes or strings)` –- replace `node`.
  - `node.remove()` –- remove the `node`.

  Text strings được insert "as text".
- Có thêm "old school" methods:

  - `parent.appendChild(node)`
  - `parent.insertBefore(node, nextSibling)`
  - `parent.removeChild(node)`
  - `parent.replaceChild(newElem, node)`

  Tất cả methods này return `node`.
- Cho một HTML trong `html`, `elem.insertAdjacentHTML(where, html)` insert nó tùy vào value của `where`:

  - `"beforebegin"` – insert `html` right before `elem`,
  - `"afterbegin"` – insert `html` vào `elem`, at the beginning,
  - `"beforeend"` – insert `html` vào `elem`, at the end,
  - `"afterend"` – insert `html` right after `elem`.

  Cũng có similar methods, `elem.insertAdjacentText` và `elem.insertAdjacentElement`, insert text strings và elements, nhưng chúng rarely used.
- Để append HTML vào page trước khi nó finish loading:

  - `document.write(html)`

  Sau khi page loaded call như vậy erase document. Mostly seen in old scripts.

---

---

## Bài tập

## [Các bài tập](#tasks)

### [createTextNode vs innerHTML vs textContent]( #createtextnode-vs-innerhtml-vs-textcontent)

importance: 5

Chúng ta có empty DOM element `elem` và string `text`.

Which của 3 commands này sẽ làm exactly the same?

1. `elem.append(document.createTextNode(text))`
2. `elem.innerHTML = text`
3. `elem.textContent = text`

solution

Answer: **1 and 3**.

Cả hai commands dẫn đến adding `text` "as text" vào `elem`.

Đây là ví dụ:

```
<div id="elem1"></div>
<div id="elem2"></div>
<div id="elem3"></div>
<script>
  let text = '<b>text</b>';

  elem1.append(document.createTextNode(text));
  elem2.innerHTML = text;
  elem3.textContent = text;
</script>
```

### [Clear the element]( #clear-the-element)

importance: 5

Tạo function `clear(elem)` remove mọi thứ từ element.

```
<ol id="elem">
  <li>Hello</li>
  <li>World</li>
</ol>

<script>
  function clear(elem) { /* your code */ }

  clear(elem); // clears the list
</script>
```

solution

Trước tiên, hãy xem how *not* to do it:

```
function clear(elem) {
  for (let i=0; i < elem.childNodes.length; i++) {
      elem.childNodes[i].remove();
  }
}
```

Đó won't work, vì call to `remove()` shifts collection `elem.childNodes`, vì vậy elements bắt đầu từ index `0` every time. Nhưng `i` increases, và một vài elements sẽ bị skipped.

`for..of` loop cũng làm y như vậy.

Right variant có thể là:

```
function clear(elem) {
  while (elem.firstChild) {
    elem.firstChild.remove();
  }
}
```

Và cũng có simpler way để làm same:

```
function clear(elem) {
  elem.innerHTML = '';
}
```

### [Why does "aaa" remain?]( #why-does-aaa-remain)

importance: 1

Trong ví dụ dưới đây, call `table.remove()` removes table khỏi document.

Nhưng nếu bạn run nó, bạn có thể thấy text `"aaa"` vẫn visible.

Tại sao điều đó happen?

```
<table id="table">
  aaa
  <tr>
    <td>Test</td>
  </tr>
</table>

<script>
  alert(table); // the table, as it should be

  table.remove();
  // why there's still "aaa" in the document?
</script>
```

solution

HTML trong task là incorrect. Đó là reason của điều kỳ lạ.

Browser phải fix nó automatically. Nhưng có thể không có text bên trong `<table>`: theo spec chỉ table-specific tags được allowed. Vì vậy browser hiển thị `"aaa"` *trước* `<table>`.

Bây giờ rõ ràng khi chúng ta remove table, nó remains.

Câu hỏi có thể dễ dàng trả lời bằng cách explore DOM using browser tools. Bạn sẽ thấy `"aaa"` trước `<table>`.

HTML standard chỉ định chi tiết cách process bad HTML, và behavior của browser là correct.

### [Create a list]( #create-a-list)

importance: 4

Viết interface để create list từ user input.

Cho mỗi list item:

1. Hỏi user về content của nó dùng `prompt`.
2. Tạo `<li>` với nó và add vào `<ul>`.
3. Continue cho đến khi user cancel input (bằng cách press `Esc` hoặc empty entry).

Tất cả elements nên được tạo dynamically.

Nếu user type HTML-tags, chúng nên được treat như text.

[Demo in new window](https://en.js.cx/task/create-list/solution/)

solution

Xin lưu ý usage của `textContent` để assign `<li>` content.

[Mở lời giải trong sandbox.](https://plnkr.co/edit/bAZIwCiBujwcXu10?p=preview)

### [Create a tree from the object]( #create-a-tree-from-the-object)

importance: 5

Viết function `createTree` tạo nested `ul/li` list từ nested object.

Ví dụ:

```
let data = {
  "Fish": {
    "trout": {},
    "salmon": {}
  },

  "Tree": {
    "Huge": {
      "sequoia": {},
      "oak": {}
    },
    "Flowering": {
      "apple tree": {},
      "magnolia": {}
    }
  }
};
```

Cú pháp:

```
let container = document.getElementById('container');
createTree(container, data); // creates the tree in the container
```

Result (tree) nên trông như sau:

Chọn một trong hai ways of solving this task:

1. Tạo HTML cho tree và sau đó assign to `container.innerHTML`.
2. Tạo tree nodes và append với DOM methods.

Sẽ great nếu bạn làm được cả hai.

P.S. Tree không nên có "extra" elements như empty `<ul></ul>` cho the leaves.

[Mở sandbox cho bài tập.](https://plnkr.co/edit/5xY7BNtzpnesXE9G?p=preview)

solution

Cách dễ nhất để walk the object là dùng recursion.

1. [The solution with innerHTML](https://plnkr.co/edit/bmBB6yUI0hNUgo5Z?p=preview).
2. [The solution with DOM](https://plnkr.co/edit/x2nHmQx5Y7I2ZYfc?p=preview).

### [Show descendants in a tree]( #show-descendants-in-a-tree)

importance: 5

Có tree organized as nested `ul/li`.

Viết code add vào mỗi `<li>` số lượng descendants của nó. Skip leaves (nodes without children).

Result:

[Mở sandbox cho bài tập.](https://plnkr.co/edit/Bx4IuRtNjZsdSlL4?p=preview)

solution

Để append text vào mỗi `<li>` chúng ta có thể alter text node `data`.

[Mở lời giải trong sandbox.](https://plnkr.co/edit/Pg2rtiS97CJnJcSZ?p=preview)

### [Create a calendar]( #create-a-calendar)

importance: 4

Viết function `createCalendar(elem, year, month)`.

Call nên tạo calendar cho given year/month và put nó bên trong `elem`.

Calendar nên là table, where a week is `<tr>`, và a day là `<td>`. Table top nên là `<th>` với weekday names: first day nên là Monday, và cứ thế till Sunday.

Ví dụ, `createCalendar(cal, 2012, 9)` nên generate trong element `cal` calendar sau:

P.S. Cho task này chỉ cần generate calendar, chưa cần clickable.

[Mở sandbox cho bài tập.](https://plnkr.co/edit/BHBpmm3GWGXtQwzZ?p=preview)

solution

Chúng ta sẽ tạo table as a string: `"<table>...</table>"`, và sau đó assign nó to `innerHTML`.

Algorithm:

1. Tạo table header với `<th>` và weekday names.
2. Tạo date object `d = new Date(year, month-1)`. Đó là first day của `month` (taking into account rằng months trong JavaScript bắt đầu từ `0`, không phải `1`).
3. First few cells till first day of the month `d.getDay()` có thể empty. Hãy fill chúng với `<td></td>`.
4. Increase day in `d`: `d.setDate(d.getDate()+1)`. Nếu `d.getMonth()` not yet next month, thì add new cell `<td>` to calendar. Nếu đó là Sunday, thì add newline `“</tr><tr>”`.
5. Nếu month finished, nhưng table row not yet full, add empty `<td>` vào nó, để make it square.

[Mở lời giải trong sandbox.](https://plnkr.co/edit/pQhTkBrLvNivzIsr?p=preview)

### [Colored clock with setInterval]( #colored-clock-with-setinterval)

importance: 4

Tạo colored clock như ở đây:

Dùng HTML/CSS cho styling, JavaScript chỉ update time trong elements.

[Mở sandbox cho bài tập.](https://plnkr.co/edit/PyMPZ25dkjoDSxCc?p=preview)

solution

Trước hết, hãy làm HTML/CSS.

Mỗi component của time sẽ trông great trong own `<span>`:

```
<div id="clock">
  <span class="hour">hh</span>:<span class="min">mm</span>:<span class="sec">ss</span>
</div>
```

Cũng chúng ta sẽ cần CSS to color them.

Function `update` sẽ refresh clock, để được called bởi `setInterval` every second:

```
function update() {
  let clock = document.getElementById('clock');
  let date = new Date(); // (*)
  let hours = date.getHours();
  if (hours < 10) hours = '0' + hours;
  clock.children[0].innerHTML = hours;

  let minutes = date.getMinutes();
  if (minutes < 10) minutes = '0' + minutes;
  clock.children[1].innerHTML = minutes;

  let seconds = date.getSeconds();
  if (seconds < 10) seconds = '0' + seconds;
  clock.children[2].innerHTML = seconds;
}
```

Ở line `(*)` chúng ta every time check current date. Calls to `setInterval` không reliable: chúng có thể happen with delays.

Clock-managing functions:

```
let timerId;

function clockStart() { // run the clock
  if (!timerId) { // only set a new interval if the clock is not running
    timerId = setInterval(update, 1000);
  }
  update(); // (*)
}

function clockStop() {
  clearInterval(timerId);
  timerId = null; // (**)
}
```

Xin lưu ý rằng call to `update()` không chỉ scheduled trong `clockStart()`, mà immediately run ở line `(*)`. Nếu không visitor sẽ phải wait till first execution của `setInterval`. Và clock sẽ empty cho đến lúc đó.

Cũng quan trọng là set new interval trong `clockStart()` chỉ khi clock không running. Otherways clicking start button several times sẽ set multiple concurrent intervals. Even worse – chúng ta chỉ keep `timerID` của last interval, losing references to all others. Sau đó chúng ta won't be able to stop the clock ever again! Note that we need to clear `timerID` khi clock stopped ở line `(**)`, để nó có thể started again bằng cách run `clockStart()`.

[Mở lời giải trong sandbox.](https://plnkr.co/edit/aiyWmre5PQMMZY17?p=preview)

### [Insert the HTML in the list]( #insert-the-html-in-the-list)

importance: 5

Viết code để insert `<li>2</li><li>3</li>` giữa hai `<li>` ở đây:

```
<ul id="ul">
  <li id="one">1</li>
  <li id="two">4</li>
</ul>
```

solution

Khi chúng ta cần insert a piece of HTML ở đâu đó, `insertAdjacentHTML` là best fit.

The solution:

```
one.insertAdjacentHTML('afterend', '<li>2</li><li>3</li>');
```

### [Sort the table]( #sort-the-table)

importance: 5

Có table:

```
<table>
<thead>
  <tr>
    <th>Name</th><th>Surname</th><th>Age</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>John</td><td>Smith</td><td>10</td>
  </tr>
  <tr>
    <td>Pete</td><td>Brown</td><td>15</td>
  </tr>
  <tr>
    <td>Ann</td><td>Lee</td><td>5</td>
  </tr>
  <tr>
    <td>...</td><td>...</td><td>...</td>
  </tr>
</tbody>
</table>
```

Có thể có more rows.

Viết code để sort nó by "name" column.

[Mở sandbox cho bài tập.](https://plnkr.co/edit/qSFrxgowhbl63ydm?p=preview)

solution

The solution is short, yet may look a bit tricky, so here I provide it with extensive comments:

```
let sortedRows = Array.from(table.tBodies[0].rows) // 1
  .sort((rowA, rowB) => rowA.cells[0].innerHTML.localeCompare(rowB.cells[0].innerHTML));

table.tBodies[0].append(...sortedRows); // (3)
```

The step-by-step algorthm:

1. Get all `<tr>`, từ `<tbody>`.
2. Then sort them comparing by content of first `<td>` (the name field).
3. Now insert nodes in the right order by `.append(...sortedRows)`.

Chúng ta không phải remove row elements, just "re-insert", they leave the old place automatically.

P.S. In our case, there's an explicit `<tbody>` in the table, but even if HTML table doesn't have `<tbody>`, the DOM structure always has it.

[Mở lời giải trong sandbox.](https://plnkr.co/edit/Tjt2RzDKAANs96fF?p=preview)