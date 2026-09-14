# Thuộc tính và thuộc tính (Attributes và Properties)

> Nguồn: [https://javascript.info/dom-attributes-and-properties](https://javascript.info/dom-attributes-and-properties)

<!-- fetched: 2026-09-14 -->

Khi browser load page, nó "đọc" (từ khác: "parses") HTML và tạo DOM objects từ nó. Cho element nodes, hầu hết standard HTML attributes tự động trở thành properties của DOM objects.

Ví dụ, nếu tag là `<body id="page">`, thì DOM object có `body.id="page"`.

Nhưng attribute-property mapping không phải one-to-one! Trong chương này chúng ta sẽ chú ý tách biệt hai khái niệm này, để xem cách làm việc với chúng, khi nào chúng giống nhau, và khi nào khác nhau.

## [DOM properties]( #dom-properties)

Chúng ta đã thấy built-in DOM properties. Có rất nhiều. Nhưng về mặt kỹ thuật không ai limit chúng ta, và nếu không đủ, chúng ta có thể thêm自己的.

DOM nodes là regular JavaScript objects. Chúng ta có thể alter chúng.

Ví dụ, hãy tạo property mới trong `document.body`:

```
document.body.myData = {
  name: 'Caesar',
  title: 'Imperator'
};

alert(document.body.myData.title); // Imperator
```

Chúng ta cũng có thể thêm method:

```
document.body.sayTagName = function() {
  alert(this.tagName);
};

document.body.sayTagName(); // BODY (giá trị của "this" trong method là document.body)
```

Chúng ta cũng có thể modify built-in prototypes như `Element.prototype` và thêm methods mới cho tất cả elements:

```
Element.prototype.sayHi = function() {
  alert(`Hello, I'm ${this.tagName}`);
};

document.documentElement.sayHi(); // Hello, I'm HTML
document.body.sayHi(); // Hello, I'm BODY
```

Vì vậy, DOM properties và methods hoạt động giống như của regular JavaScript objects:

- Chúng có thể có bất kỳ value nào.
- Chúng case-sensitive (viết `elem.nodeType`, không phải `elem.NoDeTyPe`).

## [HTML attributes]( #html-attributes)

Trong HTML, tags có thể có attributes. Khi browser parse HTML để tạo DOM objects cho tags, nó nhận diện *standard* attributes và tạo DOM properties từ chúng.

Vì vậy khi element có `id` hoặc *standard* attribute khác, corresponding property được tạo. Nhưng điều đó không xảy ra nếu attribute là non-standard.

Ví dụ:

```
<body id="test" something="non-standard">
  <script>
    alert(document.body.id); // test
    // non-standard attribute không tạo property
    alert(document.body.something); // undefined
  </script>
</body>
```

Xin lưu ý rằng standard attribute cho một element có thể unknown cho element khác. Ví dụ, `"type"` là standard cho `<input>` ([HTMLInputElement](https://html.spec.whatwg.org/#htmlinputelement)), nhưng không cho `<body>` ([HTMLBodyElement](https://html.spec.whatwg.org/#htmlbodyelement)). Standard attributes được mô tả trong specification cho corresponding element class.

Chúng ta có thể thấy nó ở đây:

```
<body id="body" type="...">
  <input id="input" type="text">
  <script>
    alert(input.type); // text
    alert(body.type); // undefined: DOM property không được tạo, vì nó non-standard
  </script>
</body>
```

Vì vậy, nếu attribute là non-standard, sẽ không có DOM-property cho nó. Có cách nào truy cập các attributes như vậy không?

Chắc chắn. Tất cả attributes đều accessible bằng các methods sau:

- `elem.hasAttribute(name)` – kiểm tra sự tồn tại.
- `elem.getAttribute(name)` – lấy value.
- `elem.setAttribute(name, value)` – set value.
- `elem.removeAttribute(name)` – remove attribute.

Các methods này operate chính xác với những gì được viết trong HTML.

Cũng có thể đọc tất cả attributes bằng `elem.attributes`: một collection của objects thuộc built-in [Attr](https://dom.spec.whatwg.org/#attr) class, với properties `name` và `value`.

Đây là demo của việc đọc non-standard property:

```
<body something="non-standard">
  <script>
    alert(document.body.getAttribute('something')); // non-standard
  </script>
</body>
```

HTML attributes có các features sau:

- Tên của chúng case-insensitive (`id` giống `ID`).
- Values của chúng luôn strings.

Đây là extended demo của việc làm việc với attributes:

```
<body>
  <div id="elem" about="Elephant"></div>

  <script>
    alert( elem.getAttribute('About') ); // (1) 'Elephant', reading

    elem.setAttribute('Test', 123); // (2), writing

    alert( elem.outerHTML ); // (3), xem attribute có trong HTML không (có)

    for (let attr of elem.attributes) { // (4) list all
      alert( `${attr.name} = ${attr.value}` );
    }
  </script>
</body>
```

Xin lưu ý:

1. `getAttribute('About')` – first letter uppercase ở đây, và trong HTML nó all lowercase. Nhưng không quan trọng: attribute names case-insensitive.
2. Chúng ta có thể gán bất cứ thứ gì cho attribute, nhưng nó trở thành string. Vì vậy ở đây chúng ta có `"123"` làm value.
3. Tất cả attributes bao gồm những gì chúng ta set đều visible trong `outerHTML`.
4. Collection `attributes` là iterable và có tất cả attributes của element (standard và non-standard) như objects với properties `name` và `value`.

## [Property-attribute synchronization]( #property-attribute-synchronization)

Khi standard attribute thay đổi, corresponding property tự động update, và (với một vài exceptions) ngược lại cũng đúng.

Trong ví dụ dưới đây `id` được modify như attribute, và chúng ta thấy property cũng thay đổi. Và sau đó ngược lại:

```
<input>

<script>
  let input = document.querySelector('input');

  // attribute => property
  input.setAttribute('id', 'id');
  alert(input.id); // id (updated)

  // property => attribute
  input.id = 'newId';
  alert(input.getAttribute('id')); // newId (updated)
</script>
```

Nhưng có exclusions, ví dụ `input.value` chỉ synchronize từ attribute → property, không ngược lại:

```
<input>

<script>
  let input = document.querySelector('input');

  // attribute => property
  input.setAttribute('value', 'text');
  alert(input.value); // text

  // NOT property => attribute
  input.value = 'newValue';
  alert(input.getAttribute('value')); // text (not updated!)
</script>
```

Trong ví dụ trên:

- Thay đổi attribute `value` update property.
- Nhưng property change không ảnh hưởng attribute.

"Feature" đó thực sự có thể tiện lợi, vì user actions có thể dẫn đến `value` changes, và sau đó, nếu chúng ta muốn recover "original" value từ HTML, nó nằm trong attribute.

## [DOM properties are typed]( #dom-properties-are-typed)

DOM properties không phải lúc nào cũng là strings. Ví dụ, property `input.checked` (cho checkboxes) là boolean:

```
<input id="input" type="checkbox" checked> checkbox

<script>
  alert(input.getAttribute('checked')); // attribute value là: empty string
  alert(input.checked); // property value là: true
</script>
```

Có các ví dụ khác. Attribute `style` là string, nhưng property `style` là object:

```
<div id="div" style="color:red;font-size:120%">Hello</div>

<script>
  // string
  alert(div.getAttribute('style')); // color:red;font-size:120%

  // object
  alert(div.style); // [object CSSStyleDeclaration]
  alert(div.style.color); // red
</script>
```

Hầu hết properties là strings tuy nhiên.

Khá hiếm, ngay cả khi DOM property type là string, nó có thể khác với attribute. Ví dụ, DOM property `href` luôn là *full* URL, ngay cả khi attribute chứa relative URL hoặc chỉ `#hash`.

Đây là ví dụ:

```
<a id="a" href="#hello">link</a>
<script>
  // attribute
  alert(a.getAttribute('href')); // #hello

  // property
  alert(a.href ); // full URL in the form http://site.com/page#hello
</script>
```

Nếu chúng ta cần value của `href` hoặc attribute nào khác exactly as written trong HTML, chúng ta có thể dùng `getAttribute`.

## [Non-standard attributes, dataset]( #non-standard-attributes-dataset)

Khi viết HTML, chúng ta dùng nhiều standard attributes. Nhưng non-standard, custom ones thì sao? Trước hết, hãy xem chúng có hữu ích hay không? Cho gì?

Đôi khi non-standard attributes được dùng để pass custom data từ HTML đến JavaScript, hoặc để "mark" HTML-elements cho JavaScript.

Như thế này:

```
<!-- mark the div to show "name" here -->
<div show-info="name"></div>
<!-- and age here -->
<div show-info="age"></div>

<script>
  // code tìm element với mark và hiển thị what's requested
  let user = {
    name: "Pete",
    age: 25
  };

  for(let div of document.querySelectorAll('[show-info]')) {
    // insert corresponding info into the field
    let field = div.getAttribute('show-info');
    div.innerHTML = user[field]; // first Pete into "name", then 25 into "age"
  }
</script>
```

Chúng cũng có thể được dùng để style element.

Ví dụ, ở đây cho order state attribute `order-state` được dùng:

```
<style>
  /* styles rely on the custom attribute "order-state" */
  .order[order-state="new"] {
    color: green;
  }

  .order[order-state="pending"] {
    color: blue;
  }

  .order[order-state="canceled"] {
    color: red;
  }
</style>

<div class="order" order-state="new">
  A new order.
</div>

<div class="order" order-state="pending">
  A pending order.
</div>

<div class="order" order-state="canceled">
  A canceled order.
</div>
```

Tại sao dùng attribute lại ưu việt hơn so với các classes như `.order-state-new`, `.order-state-pending`, `.order-state-canceled`?

Vì attribute dễ manage hơn. State có thể thay đổi dễ dàng như:

```
// a bit simpler than removing old/adding a new class
div.setAttribute('order-state', 'canceled');
```

Nhưng có thể có vấn đề với custom attributes. Nếu chúng ta dùng non-standard attribute cho purposes của chúng ta và sau đó standard introduce nó và làm nó làm gì đó? HTML language luôn sống, nó lớn lên, và nhiều attributes hơn xuất hiện để suit needs của developers. Có thể có unexpected effects trong case như vậy.

Để avoid conflicts, tồn tại [data-*](https://html.spec.whatwg.org/#embedding-custom-non-visible-data-with-the-data-*-attributes) attributes.

**Tất cả attributes bắt đầu bằng "data-" được reserved cho programmers' use. Chúng available trong property `dataset`.**

Ví dụ, nếu `elem` có attribute tên `"data-about"`, nó available như `elem.dataset.about`.

Như thế này:

```
<body data-about="Elephants">
<script>
  alert(document.body.dataset.about); // Elephants
</script>
```

Multiword attributes như `data-order-state` trở thành camel-cased: `dataset.orderState`.

Đây là rewritten "order state" example:

```
<style>
  .order[data-order-state="new"] {
    color: green;
  }

  .order[data-order-state="pending"] {
    color: blue;
  }

  .order[data-order-state="canceled"] {
    color: red;
  }
</style>

<div id="order" class="order" data-order-state="new">
  A new order.
</div>

<script>
  // read
  alert(order.dataset.orderState); // new

  // modify
  order.dataset.orderState = "pending"; // (*)
</script>
```

Sử dụng `data-*` attributes là cách valid, safe để pass custom data.

Xin lưu ý rằng chúng ta không chỉ read, mà còn modify data-attributes. Sau đó CSS update view accordingly: trong ví dụ trên dòng cuối cùng `(*)` thay đổi color thành blue.

## [Summary]( #summary)

- Attributes – là những gì được viết trong HTML.
- Properties – là những gì trong DOM objects.

Một so sánh nhỏ:

|  | Properties | Attributes |
| --- | --- | --- |
| Type | Any value, standard properties có types described in the spec | A string |
| Name | Name là case-sensitive | Name không case-sensitive |

Methods để làm việc với attributes là:

- `elem.hasAttribute(name)` – để check existence.
- `elem.getAttribute(name)` – để get value.
- `elem.setAttribute(name, value)` – để set value.
- `elem.removeAttribute(name)` – để remove attribute.
- `elem.attributes` là collection của tất cả attributes.

Đối với hầu hết situations dùng DOM properties là ưu tiên. Chúng ta nên refer đến attributes chỉ khi DOM properties không suit chúng ta, khi chúng ta cần exactly attributes, ví dụ:

- Chúng ta cần non-standard attribute. Nhưng nếu nó bắt đầu bằng `data-`, thì chúng ta nên dùng `dataset`.
- Chúng ta muốn đọc value "as written" trong HTML. Giá trị của DOM property có thể khác, ví dụ property `href` luôn là full URL, và chúng ta có thể muốn lấy "original" value.

---

---

## Bài tập

## [Các bài tập](#tasks)

### [Get the attribute]( #get-the-attribute)

importance: 5

Viết code để select element với attribute `data-widget-name` từ document và đọc value của nó.

```
<!DOCTYPE html>
<html>
<body>

  <div data-widget-name="menu">Choose the genre</div>

  <script>
    /* your code */
  </script>
</body>
</html>
```

solution

```
<!DOCTYPE html>
<html>
<body>

  <div data-widget-name="menu">Choose the genre</div>

  <script>
    // getting it
    let elem = document.querySelector('[data-widget-name]');

    // reading the value
    alert(elem.dataset.widgetName);
    // or
    alert(elem.getAttribute('data-widget-name'));
  </script>
</body>
</html>
```

### [Make external links orange]( #make-external-links-orange)

importance: 3

Làm cho tất cả external links orange bằng cách alter `style` property của chúng.

Link là external nếu:

- `href` của nó có `://`
- Nhưng không bắt đầu bằng `http://internal.com`.

Example:

```
<a name="list">the list</a>
<ul>
  <li><a href="http://google.com">http://google.com</a></li>
  <li><a href="/tutorial">/tutorial.html</a></li>
  <li><a href="local/path">local/path</a></li>
  <li><a href="ftp://ftp.com/my.zip">ftp://ftp.com/my.zip</a></li>
  <li><a href="http://nodejs.org">http://nodejs.org</a></li>
  <li><a href="http://internal.com/test">http://internal.com/test</a></li>
</ul>

<script>
  // setting style for a single link
  let link = document.querySelector('a');
  link.style.color = 'orange';
</script>
```

Kết quả nên là:

[Mở sandbox cho bài tập.](https://plnkr.co/edit/GFHTmQn3BqqRzk20?p=preview)

solution

Đầu tiên, chúng ta cần tìm tất cả external references.

Có hai cách.

Cách đầu tiên là tìm tất cả links bằng `document.querySelectorAll('a')` sau đó filter ra những gì chúng ta cần:

```
let links = document.querySelectorAll('a');

for (let link of links) {
  let href = link.getAttribute('href');
  if (!href) continue; // no attribute

  if (!href.includes('://')) continue; // no protocol

  if (href.startsWith('http://internal.com')) continue; // internal

  link.style.color = 'orange';
}
```

Xin lưu ý: chúng ta dùng `link.getAttribute('href')`. Không phải `link.href`, vì chúng ta cần value từ HTML.

…Cách khác, đơn giản hơn là add checks vào CSS selector:

```
// look for all links that have :// in href
// but href doesn't start with http://internal.com
let selector = 'a[href*="://"]:not([href^="http://internal.com"])';
let links = document.querySelectorAll(selector);

links.forEach(link => link.style.color = 'orange');
```

[Mở lời giải trong sandbox.](https://plnkr.co/edit/rWNJkuV9eAtLnyBL?p=preview)