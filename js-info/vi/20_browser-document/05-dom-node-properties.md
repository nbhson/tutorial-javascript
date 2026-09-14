# Thuộc tính của Node: type, tag và nội dung

> Nguồn: [https://javascript.info/basic-dom-node-properties](https://javascript.info/basic-dom-node-properties)

<!-- fetched: 2026-09-14 -->

Hãy nhìn sâu hơn vào DOM nodes.

Trong chương này chúng ta sẽ xem kỹ hơn về những gì chúng là và học các thuộc tính được sử dụng nhiều nhất.

## [Các lớp DOM node]( #dom-node-classes)

Các DOM nodes khác nhau có thể có các thuộc tính khác nhau. Ví dụ, element node tương ứng với thẻ `<a>` có các thuộc tính liên quan đến link, và element tương ứng với `<input>` có các thuộc tính liên quan đến input, vân vân. Text nodes không giống như element nodes. Nhưng cũng có các thuộc tính và phương thức chung giữa tất cả chúng, vì tất cả các lớp của DOM nodes tạo thành một hierarchy duy nhất.

Mỗi DOM node thuộc về built-in class tương ứng.

Root của hierarchy là [EventTarget](https://dom.spec.whatwg.org/#eventtarget), được kế thừa bởi [Node](https://dom.spec.whatwg.org/#interface-node), và các DOM nodes khác inherit từ nó.

Đây là hình ảnh, giải thích theo sau:

![](/article/basic-dom-node-properties/dom-class-hierarchy.svg)

Các lớp là:

- [EventTarget](https://dom.spec.whatwg.org/#eventtarget) – là class "abstract" gốc cho mọi thứ.

  Objects của class đó không bao giờ được tạo. Nó đóng vai trò base, để tất cả DOM nodes hỗ trợ so-called "events", chúng ta sẽ học sau.
- [Node](https://dom.spec.whatwg.org/#interface-node) – cũng là "abstract" class, đóng vai trò base cho DOM nodes.

  Nó cung cấp core tree functionality: `parentNode`, `nextSibling`, `childNodes` vân vân (chúng là getters). Objects của class `Node` không bao giờ được tạo. Nhưng có các classes khác kế thừa từ nó (và do đó kế thừa `Node` functionality).
- [Document](https://dom.spec.whatwg.org/#interface-document), vì lý do lịch sử thường được kế thừa bởi `HTMLDocument` (dù spec mới không quy định) – là document như một tổng thể.

  Global object `document` thuộc chính xác class này. Nó đóng vai trò entry point vào DOM.
- [CharacterData](https://dom.spec.whatwg.org/#interface-characterdata) – "abstract" class, được kế thừa bởi:

  - [Text](https://dom.spec.whatwg.org/#interface-text) – class tương ứng với text bên trong elements, ví dụ `Hello` trong `<p>Hello</p>`.
  - [Comment](https://dom.spec.whatwg.org/#interface-comment) – class cho comments. Chúng không được hiển thị, nhưng mỗi comment trở thành member của DOM.
- [Element](https://dom.spec.whatwg.org/#interface-element) – là base class cho DOM elements.

  Nó cung cấp element-level navigation như `nextElementSibling`, `children` và searching methods như `getElementsByTagName`, `querySelector`.

  Browser không chỉ hỗ trợ HTML, mà còn XML và SVG. Vì vậy class `Element` đóng vai trò base cho các classes cụ thể hơn: `SVGElement`, `XMLElement` (chúng ta không cần ở đây) và `HTMLElement`.
- Cuối cùng, [HTMLElement](https://html.spec.whatwg.org/multipage/dom.html#htmlelement) là base class cho tất cả HTML elements. Chúng ta sẽ làm việc với nó hầu hết thời gian.

  Nó được kế thừa bởi các concrete HTML elements:

  - [HTMLInputElement](https://html.spec.whatwg.org/multipage/forms.html#htmlinputelement) – class cho `<input>` elements,
  - [HTMLBodyElement](https://html.spec.whatwg.org/multipage/semantics.html#htmlbodyelement) – class cho `<body>` elements,
  - [HTMLAnchorElement](https://html.spec.whatwg.org/multipage/semantics.html#htmlanchorelement) – class cho `<a>` elements,
  - …vân vân.

Có nhiều tags khác với classes của riêng chúng có thể có specific properties và methods, trong khi một số elements, như `<span>`, `<section>`, `<article>` không có specific properties nào, nên chúng là instances của class `HTMLElement`.

Vì vậy, full set của properties và methods của một node cho trước đến từ chain of inheritance.

Ví dụ, hãy xem DOM object cho `<input>` element. Nó thuộc class [HTMLInputElement](https://html.spec.whatwg.org/multipage/forms.html#htmlinputelement).

Nó nhận properties và methods như một sự kết hợp của (liệt kê theo thứ tự inheritance):

- `HTMLInputElement` – class này cung cấp input-specific properties,
- `HTMLElement` – nó cung cấp common HTML element methods (và getters/setters),
- `Element` – cung cấp generic element methods,
- `Node` – cung cấp common DOM node properties,
- `EventTarget` – cung cấp support cho events (sẽ được cover),
- …và cuối cùng nó kế thừa từ `Object`, vì vậy "plain object" methods như `hasOwnProperty` cũng có sẵn.

Để xem DOM node class name, chúng ta có thể nhớ rằng một object thường có property `constructor`. Nó reference đến class constructor, và `constructor.name` là tên của nó:

```
alert( document.body.constructor.name ); // HTMLBodyElement
```

…Hoặc chúng ta có thể chỉ `toString` nó:

```
alert( document.body ); // [object HTMLBodyElement]
```

Chúng ta cũng có thể dùng `instanceof` để kiểm tra inheritance:

```
alert( document.body instanceof HTMLBodyElement ); // true
alert( document.body instanceof HTMLElement ); // true
alert( document.body instanceof Element ); // true
alert( document.body instanceof Node ); // true
alert( document.body instanceof EventTarget ); // true
```

Như chúng ta có thể thấy, DOM nodes là regular JavaScript objects. Chúng sử dụng prototype-based classes cho inheritance.

Đó cũng dễ thấy bằng cách output element với `console.dir(elem)` trong browser. Ở đó trong console bạn có thể thấy `HTMLElement.prototype`, `Element.prototype` vân vân.

`console.dir(elem)` versus `console.log(elem)`

Hầu hết browsers hỗ trợ hai commands trong developer tools của họ: `console.log` và `console.dir`. Chúng output arguments của chúng ra console. Cho JavaScript objects các commands này thường làm giống nhau.

Nhưng cho DOM elements chúng khác nhau:

- `console.log(elem)` hiển thị element DOM tree.
- `console.dir(elem)` hiển thị element như một DOM object, tốt để explore các properties của nó.

Thử nó trên `document.body`.

IDL in the spec

Trong specification, DOM classes không được mô tả bằng JavaScript, mà bằng một [Interface description language](https://en.wikipedia.org/wiki/Interface_description_language) (IDL) đặc biệt, thường dễ hiểu.

Trong IDL tất cả properties được prepend với types của chúng. Ví dụ, `DOMString`, `boolean` vân vân.

Đây là một đoạn trích từ nó, với comments:

```
113: // Define HTMLInputElement
114: // The colon ":" means that HTMLInputElement inherits from HTMLElement
115: interface HTMLInputElement: HTMLElement {
116: 116:   // here go properties and methods of <input> elements
117: 117:
118: 118:   // "DOMString" means that the value of a property is a string
119: 119:   attribute DOMString accept;
120: 120:   attribute DOMString alt;
121: 121:   attribute DOMString autocomplete;
122: 122:   attribute DOMString value;
123: 123:
124: 124:   // boolean value property (true/false)
125: 125:   attribute boolean autofocus;
126: 126:   ...
127: 127:   // now the method: "void" means that the method returns no value
128: 128:   void select();
129: 129:   ...
130: 130: }
```

## [Thuộc tính "nodeType"]( #property-nodetype)

Thuộc tính `nodeType` cung cấp thêm một cách, "old-fashioned" để lấy "type" của DOM node.

Nó có giá trị numeric:

- `elem.nodeType == 1` cho element nodes,
- `elem.nodeType == 3` cho text nodes,
- `elem.nodeType == 9` cho document object,
- có một vài values khác trong [the specification](https://dom.spec.whatwg.org/#node).

Ví dụ:

```
<body>
  <script>
  let elem = document.body;

  // let's examine: what type of node is in elem?
  alert(elem.nodeType); // 1 => element

  // and its first child is...
  alert(elem.firstChild.nodeType); // 3 => text

  // for the document object, the type is 9
  alert( document.nodeType ); // 9
  </script>
</body>
```

Trong scripts hiện đại, chúng ta có thể dùng `instanceof` và các class-based tests khác để xem node type, nhưng đôi khi `nodeType` có thể đơn giản hơn. Chúng ta chỉ có thể đọc `nodeType`, không thể thay đổi nó.

## [Tag: nodeName and tagName]( #tag-nodename-and-tagname)

Cho một DOM node, chúng ta có thể đọc tag name của nó từ properties `nodeName` hoặc `tagName`:

Ví dụ:

```
alert( document.body.nodeName ); // BODY
alert( document.body.tagName ); // BODY
```

Có sự khác biệt nào giữa `tagName` và `nodeName`?

Chắc chắn, sự khác biệt được phản ánh trong tên của chúng, nhưng thực sự hơi tinh tế.

- Property `tagName` chỉ tồn tại cho `Element` nodes.
- `nodeName` được định nghĩa cho bất kỳ `Node` nào:
  - cho elements nó có nghĩa giống như `tagName`.
  - cho các node types khác (text, comment, vân vân) nó có string với node type.

Nói cách khác, `tagName` chỉ được hỗ trợ bởi element nodes (vì nó xuất phát từ class `Element`), trong khi `nodeName` có thể nói gì đó về các node types khác.

Ví dụ, hãy so sánh `tagName` và `nodeName` cho `document` và comment node:

```
<body><!-- comment -->

  <script>
    // for comment
    alert( document.body.firstChild.tagName ); // undefined (not an element)
    alert( document.body.firstChild.nodeName ); // #comment

    // for document
    alert( document.tagName ); // undefined (not an element)
    alert( document.nodeName ); // #document
  </script>
</body>
```

Nếu chúng ta chỉ deal với elements, thì chúng ta có thể dùng cả `tagName` và `nodeName` – không có sự khác biệt.

Tag name luôn uppercase trừ XML mode

Browser có hai modes xử lý documents: HTML và XML. Thông thường HTML-mode được dùng cho webpages. XML-mode được enable khi browser nhận XML-document với header: `Content-Type: application/xml+xhtml`.

Trong HTML mode `tagName/nodeName` luôn uppercased: nó là `BODY` cho cả `<body>` hoặc `<BoDy>`.

Trong XML mode case được giữ "as is". Ngày nay XML mode hiếm khi được dùng.

## [innerHTML: nội dung]( #innerhtml-the-contents)

Property [innerHTML](https://w3c.github.io/DOM-Parsing/#the-innerhtml-mixin) cho phép lấy HTML bên trong element dưới dạng string.

Chúng ta cũng có thể modify nó. Vì vậy đó là một trong những cách mạnh mẽ nhất để thay đổi page.

Ví dụ dưới đây hiển thị contents của `document.body` và sau đó replace nó hoàn toàn:

```
<body>
  <p>A paragraph</p>
  <div>A div</div>

  <script>
    alert( document.body.innerHTML ); // read the current contents
    document.body.innerHTML = 'The new BODY!'; // replace it
  </script>

</body>
```

Chúng ta có thể thử chèn invalid HTML, browser sẽ fix errors của chúng ta:

```
<body>

  <script>
    document.body.innerHTML = '<b>test'; // forgot to close the tag
    alert( document.body.innerHTML ); // <b>test</b> (fixed)
  </script>

</body>
```

Scripts don't execute

Nếu `innerHTML` chèn `<script>` tag vào document – nó trở thành một phần của HTML, nhưng không execute.

### [Cẩn thận: "innerHTML+=" làm full overwrite]( #can-than-innerhtml-lam-full-overwrite)

Chúng ta có thể append HTML vào element bằng cách dùng `elem.innerHTML+="more html"`.

Như thế này:

```
chatDiv.innerHTML += "<div>Hello<img src='smile.gif'/> !</div>";
chatDiv.innerHTML += "How goes?";
```

Nhưng chúng ta nên rất cẩn trọng khi làm như vậy, vì những gì đang xảy ra *không phải* là addition, mà là full overwrite.

Về mặt kỹ thuật, hai dòng này làm điều giống nhau:

```
elem.innerHTML += "...";
// là cách viết ngắn gọn cho:
elem.innerHTML = elem.innerHTML + "..."
```

Nói cách khác, `innerHTML+=` làm điều này:

1. Old contents bị removed.
2. New `innerHTML` được viết thay thế (một sự concatenation của old và new).

**Vì content bị "zeroed-out" và rewritten from the scratch, tất cả images và resources khác sẽ được reload lại**.

Trong ví dụ `chatDiv` ở trên dòng `chatDiv.innerHTML+="How goes?"` re-creates HTML content và reload `smile.gif` (hy vọng nó được cached). Nếu `chatDiv` có nhiều text và images khác, thì reload sẽ trở nên rõ ràng.

Có những side-effects khác nữa. Ví dụ, nếu existing text đã được selected với mouse, thì hầu hết browsers sẽ remove selection khi rewrite `innerHTML`. Và nếu có `<input>` với text được nhập bởi visitor, thì text sẽ bị removed. Vân vân.

May mắn thay, có các cách khác để thêm HTML bên cạnh `innerHTML`, và chúng ta sẽ học chúng sớm.

## [outerHTML: full HTML của element]( #outerhtml-full-html-of-the-element)

Property `outerHTML` chứa full HTML của element. Đó giống như `innerHTML` cộng với chính element đó.

Đây là ví dụ:

```
<div id="elem">Hello <b>World</b></div>

<script>
  alert(elem.outerHTML); // <div id="elem">Hello <b>World</b></div>
</script>
```

**Cẩn thận: khác với `innerHTML`, viết vào `outerHTML` không thay đổi element. Thay vào đó, nó replace nó trong DOM.**

Đúng, nghe lạ, và nó thực sự lạ, đó là lý do chúng ta note riêng về nó ở đây. Hãy xem.

Xét ví dụ:

```
<div>Hello, world!</div>

<script>
  let div = document.querySelector('div');

  // replace div.outerHTML with <p>...</p>
  div.outerHTML = '<p>A new element</p>'; // (*)

  // Wow! 'div' vẫn là same!
  alert(div.outerHTML); // <div>Hello, world!</div> (**)
</script>
```

Trông thật kỳ lạ, đúng không?

Ở dòng `(*)` chúng ta replace `div` với `<p>A new element</p>`. Trong outer document (DOM) chúng ta có thể thấy new content thay vì `<div>`. Nhưng, như chúng ta thấy ở dòng `(**)`, giá trị của `div` variable cũ không thay đổi!

Gán `outerHTML` không modify DOM element (object được reference bởi, trong trường hợp này, variable 'div'), mà remove nó khỏi DOM và chèn new HTML vào vị trí của nó.

Vì vậy những gì xảy ra trong `div.outerHTML=...` là:

- `div` bị removed khỏi document.
- Another piece of HTML `<p>A new element</p>` được chèn vào vị trí của nó.
- `div` vẫn giữ giá trị cũ. New HTML không được lưu vào bất kỳ variable nào.

Rất dễ mắc lỗi ở đây: modify `div.outerHTML` và sau đó tiếp tục làm việc với `div` như thể nó có new content. Nhưng nó không có. Cái đó đúng cho `innerHTML`, nhưng không cho `outerHTML`.

Chúng ta có thể viết vào `elem.outerHTML`, nhưng nên nhớ rằng nó không thay đổi element chúng ta đang viết ('elem'). Nó đặt new HTML vào vị trí của nó thay thế. Chúng ta có thể get references đến new elements bằng cách query DOM.

## [nodeValue/data: text node content]( #nodevalue-data-text-node-content)

Property `innerHTML` chỉ valid cho element nodes.

Các node types khác, như text nodes, có counterparts của chúng: properties `nodeValue` và `data`. Hai properties này gần như giống nhau cho practical use, chỉ có một vài khác biệt nhỏ về specification. Vì vậy chúng ta sẽ dùng `data`, vì nó ngắn hơn.

Một ví dụ về đọc content của text node và comment:

```
<body>
  Hello
  <!-- Comment -->
  <script>
    let text = document.body.firstChild;
    alert(text.data); // Hello

    let comment = text.nextSibling;
    alert(comment.data); // Comment
  </script>
</body>
```

Cho text nodes chúng ta có thể tưởng tượng lý do để đọc hoặc modify chúng, nhưng tại sao comments?

Đôi khi developers nhúng information hoặc template instructions vào HTML trong chúng, như thế này:

```
<!-- if isAdmin -->
  <div>Welcome, Admin!</div>
<!-- /if -->
```

…Sau đó JavaScript có thể đọc nó từ property `data` và xử lý embedded instructions.

## [textContent: pure text]( #textcontent-pure-text)

Property `textContent` cung cấp quyền truy cập vào *text* bên trong element: chỉ text, trừ đi tất cả `<tags>`.

Ví dụ:

```
<div id="news">
  <h1>Headline!</h1>
  <p>Martians attack people!</p>
</div>

<script>
  // Headline! Martians attack people!
  alert(news.textContent);
</script>
```

Như chúng ta có thể thấy, chỉ text được trả về, như thể tất cả `<tags>` bị cắt bỏ, nhưng text trong chúng vẫn còn.

Trong thực tế, việc đọc text như vậy hiếm khi cần.

**Viết vào `textContent` hữu ích hơn nhiều, vì nó cho phép viết text theo "cách an toàn".**

Giả sử chúng ta có một string tùy ý, ví dụ được nhập bởi user, và muốn hiển thị nó.

- Với `innerHTML` chúng ta sẽ chèn nó "as HTML", với tất cả HTML tags.
- Với `textContent` chúng ta sẽ chèn nó "as text", tất cả symbols được treat literally.

So sánh hai cái:

```
<div id="elem1"></div>
<div id="elem2"></div>

<script>
  let name = prompt("What's your name?", "<b>Winnie-the-Pooh!</b>");

  elem1.innerHTML = name;
  elem2.textContent = name;
</script>
```

1. `<div>` đầu tiên nhận name "as HTML": tất cả tags trở thành tags, vì vậy chúng ta thấy bold name.
2. `<div>` thứ hai nhận name "as text", vì vậy chúng ta literally thấy `<b>Winnie-the-Pooh!</b>`.

Trong hầu hết các cases, chúng ta expect text từ user, và muốn treat nó như text. Chúng ta không muốn unexpected HTML trong site của mình. Gán vào `textContent` làm chính xác điều đó.

## [Thuộc tính "hidden"]( #property-hidden)

Attribute "hidden" và DOM property chỉ định element có visible hay không.

Chúng ta có thể dùng nó trong HTML hoặc gán nó bằng JavaScript, như thế này:

```
<div>Both divs below are hidden</div>

<div hidden>With the attribute "hidden"</div>

<div id="elem">JavaScript assigned the property "hidden"</div>

<script>
  elem.hidden = true;
</script>
```

Về mặt kỹ thuật, `hidden` hoạt động giống như `style="display:none"`. Nhưng nó ngắn hơn để viết.

Đây là một element nhấp nháy:

```
<div id="elem">A blinking element</div>

<script>
  setInterval(() => elem.hidden = !elem.hidden, 1000);
</script>
```

## [More properties]( #more-properties)

DOM elements cũng có thêm properties, đặc biệt là những thứ phụ thuộc vào class:

- `value` – value cho `<input>`, `<select>` và `<textarea>` (`HTMLInputElement`, `HTMLSelectElement`…).
- `href` – "href" cho `<a href="...">` (`HTMLAnchorElement`).
- `id` – value của "id" attribute, cho tất cả elements (`HTMLElement`).
- …vân vân…

Ví dụ:

```
<input type="text" id="elem" value="value">

<script>
  alert(elem.type); // "text"
  alert(elem.id); // "elem"
  alert(elem.value); // value
</script>
```

Hầu hết standard HTML attributes có corresponding DOM property, và chúng ta có thể truy cập nó như vậy.

Nếu chúng ta muốn biết full list của supported properties cho một class cho trước, chúng ta có thể tìm chúng trong specification. Ví dụ, `HTMLInputElement` được documented tại <https://html.spec.whatwg.org/#htmlinputelement>.

Hoặc nếu chúng ta muốn lấy chúng nhanh hoặc quan tâm đến browser specification cụ thể – chúng ta luôn có thể output element bằng `console.dir(elem)` và đọc properties. Hoặc explore "DOM properties" trong Elements tab của browser developer tools.

## [Summary]( #summary)

Mỗi DOM node thuộc về một class nhất định. Các classes tạo thành hierarchy. Full set của properties và methods đến như kết quả của inheritance.

Main DOM node properties là:

`nodeType`
:   Chúng ta có thể dùng nó để xem node là text hay element node. Nó có giá trị numeric: `1` cho elements,`3` cho text nodes, và một vài values khác cho các node types khác. Read-only.

`nodeName/tagName`
:   Cho elements, tag name (uppercased trừ khi XML-mode). Cho non-element nodes `nodeName` mô tả nó là gì. Read-only.

`innerHTML`
:   HTML content của element. Có thể modify.

`outerHTML`
:   Full HTML của element. Write operation vào `elem.outerHTML` không touch `elem` chính nó. Thay vào đó nó bị replace với new HTML trong outer context.

`nodeValue/data`
:   Content của non-element node (text, comment). Hai cái này gần như giống nhau, thường chúng ta dùng `data`. Có thể modify.

`textContent`
:   Text bên trong element: HTML minus tất cả `<tags>`. Viết vào nó đặt text bên trong element, với tất cả special characters và tags được treat chính xác như text. Có thể safely insert user-generated text và bảo vệ khỏi unwanted HTML insertions.

`hidden`
:   Khi set thành `true`, làm giống như CSS `display:none`.

DOM nodes cũng có các properties khác tùy vào class của chúng. Ví dụ, `<input>` elements (`HTMLInputElement`) hỗ trợ `value`, `type`, trong khi `<a>` elements (`HTMLAnchorElement`) hỗ trợ `href` vân vân. Hầu hết standard HTML attributes có corresponding DOM property.

Tuy nhiên, HTML attributes và DOM properties không phải lúc nào cũng giống nhau, như chúng ta sẽ thấy ở chương tiếp theo.

---

---

## Bài tập

## [Các bài tập](#tasks)

### [Count descendants]( #count-descendants)

importance: 5

Có một tree structured dưới dạng nested `ul/li`.

Viết code mà cho mỗi `<li>` hiển thị:

1. Text bên trong nó là gì (không có subtree)
2. Số lượng nested `<li>` – tất cả descendants, bao gồm cả deeply nested ones.

[Demo in new window](https://en.js.cx/task/tree-info/solution/)

[Mở sandbox cho bài tập.](https://plnkr.co/edit/HILrCNC2WQL70wBY?p=preview)

solution

Hãy tạo loop qua `<li>`:

```
for (let li of document.querySelectorAll('li')) {
  ...
}
```

Trong loop chúng ta cần lấy text bên trong mỗi `li`.

Chúng ta có thể đọc text từ first child node của `li`, đó là text node:

```
for (let li of document.querySelectorAll('li')) {
  let title = li.firstChild.data;

  // title là text trong <li> trước bất kỳ nodes khác
}
```

Sau đó chúng ta có thể lấy số descendants như `li.getElementsByTagName('li').length`.

[Mở lời giải trong sandbox.](https://plnkr.co/edit/F1UQNdzRcv7xkTpk?p=preview)

### [What's in the nodeType?]( #what-s-in-the-nodetype)

importance: 5

Script dưới đây hiển thị gì?

```
<html>

<body>
  <script>
    alert(document.body.lastChild.nodeType);
  </script>
</body>

</html>
```

solution

Đây có một catch.

Khi `<script>` executes last DOM node chính xác là `<script>`, vì browser chưa process phần còn lại của page.

Vì vậy result là `1` (element node).

```
<html>

<body>
  <script>
    alert(document.body.lastChild.nodeType);
  </script>
</body>

</html>
```

### [Tag in comment]( #tag-in-comment)

importance: 3

Mã này hiển thị gì?

```
<script>
  let body = document.body;

  body.innerHTML = "<!--" + body.tagName + "-->";

  alert( body.firstChild.data ); // what's here?
</script>
```

solution

Câu trả lời: **`BODY`**.

```
<script>
  let body = document.body;

  body.innerHTML = "<!--" + body.tagName + "-->";

  alert( body.firstChild.data ); // BODY
</script>
```

Those gì đang xảy ra step by step:

1. Content của `<body>` bị replace với comment. Comment là `<!--BODY-->`, vì `body.tagName == "BODY"`. Như chúng ta nhớ, `tagName` luôn uppercase trong HTML.
2. Comment bây giờ là only child node, vì vậy chúng ta lấy nó trong `body.firstChild`.
3. Property `data` của comment là contents của nó (bên trong `<!--...-->`): `"BODY"`.

### [Where's the "document" in the hierarchy?]( #where-s-the-document-in-the-hierarchy)

importance: 4

Class nào mà `document` thuộc về?

Địa vị của nó trong DOM hierarchy là gì?

Nó inherit từ `Node` hay `Element`, hay có lẽ `HTMLElement`?

solution

Chúng ta có thể xem class nào nó thuộc bằng cách output nó, như:

```
alert(document); // [object HTMLDocument]
```

Hoặc:

```
alert(document.constructor.name); // HTMLDocument
```

Vì vậy, `document` là instance của class `HTMLDocument`.

Địa vị của nó trong hierarchy là gì?

Đúng, chúng ta có thể browse specification, nhưng sẽ nhanh hơn để tự tìm ra.

Hãy traverse prototype chain qua `__proto__`.

Như chúng ta biết, methods của một class nằm trong `prototype` của constructor. Ví dụ, `HTMLDocument.prototype` có methods cho documents.

Cũng có reference đến constructor function bên trong `prototype`:

```
alert(HTMLDocument.prototype.constructor === HTMLDocument); // true
```

Để lấy tên class dưới dạng string, chúng ta có thể dùng `constructor.name`. Hãy làm nó cho cả `document` prototype chain, tới class `Node`:

```
alert(HTMLDocument.prototype.constructor.name); // HTMLDocument
alert(HTMLDocument.prototype.__proto__.constructor.name); // Document
alert(HTMLDocument.prototype.__proto__.__proto__.constructor.name); // Node
```

Đó là hierarchy.

Chúng ta cũng có thể examine object bằng `console.dir(document)` và thấy các names này bằng cách mở `__proto__`. Console lấy chúng từ `constructor` internally.