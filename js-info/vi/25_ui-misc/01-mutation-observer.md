# Bộ quan sát thay đổi (Mutation observer)

> Source: [https://javascript.info/mutation-observer](https://javascript.info/mutation-observer)

<!-- fetched: 2026-09-14 -->

`MutationObserver` là một built-in object quan sát một DOM element và fire callback khi nó phát hiện thay đổi.

Chúng ta sẽ xem xét syntax trước, rồi khám phá một use case thực tế, để xem thứ như vậy hữu ích ở đâu.

## [Syntax](#syntax)

`MutationObserver` dễ sử dụng.

Đầu tiên, chúng ta tạo một observer với callback-function:

```
let observer = new MutationObserver(callback);
```

Và sau đó attach nó vào một DOM node:

```
observer.observe(node, config);
```

`config` là một object với các boolean options "các loại thay đổi nào để phản hồi":

- `childList` – thay đổi trong children trực tiếp của `node`,
- `subtree` – trong tất cả descendants của `node`,
- `attributes` – attributes của `node`,
- `attributeFilter` – một mảng các tên attribute, để chỉ quan sát những cái được chọn.
- `characterData` – liệu có quan sát `node.data` (nội dung text) hay không,

Một số options khác:

- `attributeOldValue` – nếu `true`, truyền cả giá trị cũ và mới của attribute vào callback (xem bên dưới), nếu không thì chỉ truyền giá trị mới (cần option `attributes`),
- `characterDataOldValue` – nếu `true`, truyền cả giá trị cũ và mới của `node.data` vào callback (xem bên dưới), nếu không thì chỉ truyền giá trị mới (cần option `characterData`).

Sau đó sau bất kỳ thay đổi nào, `callback` được thực thi: các thay đổi được truyền trong argument đầu tiên dưới dạng danh sách các object [MutationRecord](https://dom.spec.whatwg.org/#mutationrecord), và bản thân observer là argument thứ hai.

Các object [MutationRecord](https://dom.spec.whatwg.org/#mutationrecord) có các properties:

- `type` – kiểu mutation, một trong
  - `"attributes"`: attribute đã bị sửa đổi
  - `"characterData"`: data đã bị sửa đổi, dùng cho text nodes,
  - `"childList"`: các child elements được thêm/bỏ,
- `target` – nơi xảy ra thay đổi: một element cho `"attributes"`, hoặc text node cho `"characterData"`, hoặc một element cho mutation `"childList"`,
- `addedNodes/removedNodes` – các nodes đã được thêm/bỏ,
- `previousSibling/nextSibling` – anh em trước và sau của các nodes được thêm/bỏ,
- `attributeName/attributeNamespace` – tên/namespace (cho XML) của attribute bị thay đổi,
- `oldValue` – giá trị trước đó, chỉ cho attribute hoặc text changes, nếu option tương ứng được đặt `attributeOldValue`/`characterDataOldValue`.

Ví dụ, đây là một `<div>` với attribute `contentEditable`. Attribute đó cho phép chúng ta focus vào nó và chỉnh sửa.

```
<div contentEditable id="elem">Nhấn và <b>chỉnh sửa</b>, vui lòng</div>

<script>
let observer = new MutationObserver(mutationRecords => {
  console.log(mutationRecords); // console.log(các thay đổi)
});

// quan sát mọi thứ trừ attributes
observer.observe(elem, {
  childList: true, // quan sát direct children
  subtree: true, // và các descendants thấp hơn nữa
  characterDataOldValue: true // truyền data cũ vào callback
});
</script>
```

Nếu chúng ta chạy code này trong trình duyệt, sau đó focus vào `<div>` đã cho và thay đổi text bên trong `<b>chỉnh sửa</b>`, `console.log` sẽ hiển thị một mutation:

```
mutationRecords = [{
  type: "characterData",
  oldValue: "chỉnh sửa",
  target: <text node>,
  // các properties khác trống
}];
```

Nếu chúng ta thực hiện các hoạt động chỉnh sửa phức tạp hơn, ví dụ xóa `<b>chỉnh sửa</b>`, mutation event có thể chứa nhiều mutation records:

```
mutationRecords = [{
  type: "childList",
  target: <div#elem>,
  removedNodes: [<b>],
  nextSibling: <text node>,
  previousSibling: <text node>
  // các properties khác trống
}, {
  type: "characterData"
  target: <text node>
  // ...chi tiết mutation phụ thuộc vào cách trình duyệt xử lý việc xóa như vậy
  // nó có thể gộp hai text nodes liền kề "chỉnh sửa " và ", vui lòng" thành một node
  // hoặc nó có thể để chúng ở riêng
}];
```

Vậy, `MutationObserver` cho phép phản hồi với mọi thay đổi trong DOM subtree.

## [Dùng cho integration](#usage-for-integration)

Khi nào thứ như vậy hữu ích?

Hãy tưởng tượng tình huống khi bạn cần thêm một script third-party có chứa functionality hữu ích, nhưng cũng làm một thứ không mong muốn, ví dụ hiển thị ads `<div class="ads">Quảng cáo không mong muốn</div>`.

Tất nhiên, script third-party không cung cấp cơ chế để xóa nó.

Dùng `MutationObserver`, chúng ta có thể phát hiện khi phần tử không mong muốn xuất hiện trong DOM của chúng ta và xóa nó.

Có các tình huống khác khi một script third-party thêm thứ gì đó vào document của chúng ta, và chúng ta muốn phát hiện khi điều đó xảy ra, để thích nghi trang của chúng ta, thay đổi kích thước thứ gì đó động, v.v.

`MutationObserver` cho phép triển khai điều này.

## [Dùng cho kiến trúc](#usage-for-architecture)

Cũng có những tình huống khi `MutationObserver` tốt xét về mặt kiến trúc.

Giả sử chúng ta đang làm một website về lập trình. Tất nhiên, articles và các tài liệu khác có thể chứa các đoạn code.

Đoạn code như vậy trong HTML markup trông như sau:

```
...
<pre class="language-javascript"><code>
  // đây là code
  let hello = "world";
</code></pre>
...
```

Để đọc dễ hơn và cùng lúc đó, để làm đẹp nó, chúng ta sẽ dùng một thư viện syntax highlighting JavaScript trên site của mình, như [Prism.js](https://prismjs.com/). Để có syntax highlighting cho snippet trên trong Prism, `Prism.highlightElement(pre)` được gọi, nó xem xét nội dung của các `pre` elements như vậy và thêm các tags và styles đặc biệt cho syntax highlighting có màu sắc vào các elements đó, tương tự như những gì bạn thấy trong các ví dụ ở đây, trên trang này.

Chính xác khi nào chúng ta nên chạy phương thức highlighting đó? Chúng ta có thể làm nó trên sự kiện `DOMContentLoaded`, hoặc đặt script ở cuối trang. Ngay khi DOM của chúng ta sẵn sàng, chúng ta có thể tìm kiếm các elements `pre[class*="language"]` và gọi `Prism.highlightElement` trên chúng:

```
// highlight tất cả các đoạn code trên trang
document.querySelectorAll('pre[class*="language"]').forEach(elem => Prism.highlightElement(elem));
```

Mọi thứ vẫn còn đơn giản, phải không? Chúng ta tìm các đoạn code trong HTML và highlight chúng.

Giờ hãy tiếp tục. Giả sử chúng ta sẽ fetch materials động từ server. Chúng ta sẽ nghiên cứu các methods cho việc đó [sau trong tutorial](/fetch). Hiện tại chỉ cần biết rằng chúng ta fetch một HTML article từ webserver và hiển thị nó khi được yêu cầu:

```
let article = /* fetch new content from server */
articleElem.innerHTML = article;
```

HTML `article` mới có thể chứa các đoạn code. Chúng ta cần gọi `Prism.highlightElement` trên chúng, nếu không chúng sẽ không được highlight.

**Ở đâu và khi nào gọi `Prism.highlightElement` cho một article được load động?**

Chúng ta có thể append call đó vào code tải article, như sau:

```
let article = /* fetch new content from server */
articleElem.innerHTML = article;

let snippets = articleElem.querySelectorAll('pre[class*="language-"]');
snippets.forEach(elem => Prism.highlightElement(elem));
```

…Nhưng hãy tưởng tượng nếu chúng ta có nhiều chỗ trong code nơi chúng ta tải content của mình – articles, quizzes, forum posts, v.v. Chúng ta có cần đặt call highlighting ở mọi nơi, để highlight code trong content sau khi tải không? Điều đó không tiện lắm.

Và nếu content được tải bởi một third-party module thì sao? Ví dụ, chúng ta có một forum được viết bởi người khác, tải content động, và chúng ta muốn thêm syntax highlighting vào nó. Không ai thích vá third-party scripts.

May mắn thay, có một option khác.

Chúng ta có thể dùng `MutationObserver` để tự động phát hiện khi các đoạn code được chèn vào trang và highlight chúng.

Vậy chúng ta sẽ xử lý functionality highlighting ở một chỗ, giải phóng chúng ta khỏi nhu cầu tích hợp nó.

### [Demo highlight động](#dynamic-highlight-demo)

Đây là một example đang hoạt động.

Nếu bạn chạy code này, nó bắt đầu quan sát element bên dưới và highlight bất kỳ đoạn code nào xuất hiện ở đó:

```
let observer = new MutationObserver(mutations => {

  for(let mutation of mutations) {
    // xem xét các nodes mới, có gì cần highlight không?

    for(let node of mutation.addedNodes) {
      // chúng ta chỉ theo dõi elements, bỏ qua các nodes khác (ví dụ text nodes)
      if (!(node instanceof HTMLElement)) continue;

      // kiểm tra element được chèn có phải là đoạn code không
      if (node.matches('pre[class*="language-"]')) {
        Prism.highlightElement(node);
      }

      // hoặc có thể có một đoạn code ở đâu đó trong subtree của nó?
      for(let elem of node.querySelectorAll('pre[class*="language-"]')) {
        Prism.highlightElement(elem);
      }
    }
  }

});

let demoElem = document.getElementById('highlight-demo');

observer.observe(demoElem, {childList: true, subtree: true});
```

Ở đây, phía dưới, có một HTML-element và JavaScriptfills nó động bằng `innerHTML`.

Hãy chạy code trước đó (phía trên, quan sát element đó), và sau đó code bên dưới. Bạn sẽ thấy cách `MutationObserver` phát hiện và highlight snippet.

Một demo-element với `id="highlight-demo"`, chạy code phía trên để quan sát nó.

Code sau đây populate `innerHTML` của nó, điều đó khiến `MutationObserver` phản hồi và highlight nội dung của nó:

```
let demoElem = document.getElementById('highlight-demo');

// chèn động content với các đoạn code
demoElem.innerHTML = `Một đoạn code ở bên dưới:
  <pre class="language-javascript"><code> let hello = "world!"; </code></pre>
  <div>Một cái nữa:</div>
  <div>
    <pre class="language-css"><code>.class { margin: 5px; } </code></pre>
  </div>
`;
```

Giờ chúng ta có `MutationObserver` có thể track mọi highlighting trong các elements được quan sát hoặc toàn bộ `document`. Chúng ta có thể thêm/xóa các đoạn code trong HTML mà không cần nghĩ về nó.

## [Các methods bổ sung](#additional-methods)

Có một method để dừng quan sát node:

- `observer.disconnect()` – dừng việc quan sát.

Khi chúng ta dừng quan sát, có thể có một số thay đổi chưa được xử lý bởi observer. Trong các trường hợp như vậy, chúng ta dùng

- `observer.takeRecords()` – lấy danh sách các mutation records chưa xử lý – những cái đã xảy ra, nhưng callback chưa xử lý chúng.

Hai methods này có thể được dùng cùng nhau, như sau:

```
// lấy danh sách các mutations chưa xử lý
// nên được gọi trước khi disconnecting,
// nếu bạn quan tâm đến các mutations gần đây có thể chưa được xử lý
let mutationRecords = observer.takeRecords();

// dừng tracking thay đổi
observer.disconnect();
...
```

Các records trả về bởi `observer.takeRecords()` bị xóa khỏi processing queue

Callback sẽ không được gọi cho các records, trả về bởi `observer.takeRecords()`.

Tương tác garbage collection

Các observer dùng weak references đến các node ở mức internal. Tức là, nếu một node bị xóa khỏi DOM, và trở nên không thể truy cập được, thì nó có thể bị garbage collected.

Việc một DOM node được quan sát đơn thuần không ngăn garbage collection.

## [Tóm tắt](#summary)

`MutationObserver` có thể phản hồi với các thay đổi trong DOM – attributes, nội dung text và việc thêm/xóa elements.

Chúng ta có thể dùng nó để track các thay đổi được giới thiệu bởi các phần khác của code chúng ta, cũng như để tích hợp với các script third-party.

`MutationObserver` có thể track mọi thay đổi. Các options config "cần quan sát gì" được dùng cho việc tối ưu hóa, không phải để tiêu tốn resources cho các callback invocations không cần thiết.
