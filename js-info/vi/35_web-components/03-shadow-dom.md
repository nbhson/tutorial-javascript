# Shadow DOM

> Source: [https://javascript.info/shadow-dom](https://javascript.info/shadow-dom)

<!-- fetched: 2026-09-14 -->

Shadow DOM phục vụ cho encapsulation. Nó cho phép một component có cây DOM “shadow” riêng của mình, không thể bị truy cập nhầm từ document chính, có thể có các quy tắc style cục bộ, và nhiều hơn nữa.

## [Shadow DOM tích hợp sẵn](#built-in-shadow-dom)

Bạn đã bao giờ nghĩ xem các control của trình duyệt phức tạp được tạo và định style như thế nào chưa?

Chẳng hạn như `<input type="range">`:

Trình duyệt sử dụng DOM/CSS bên trong để vẽ chúng. Cấu trúc DOM đó thường được ẩn khỏi chúng ta, nhưng chúng ta có thể nhìn thấy nó trong developer tools. Ví dụ trong Chrome, chúng ta cần bật tùy chọn “Show user agent shadow DOM” trong Dev Tools.

Khi đó `<input type="range"` trông như thế này:

![](/article/shadow-dom/shadow-dom-range.png)

Những gì bạn nhìn thấy dưới `#shadow-root` được gọi là “shadow DOM”.

Chúng ta không thể lấy các phần tử shadow DOM tích hợp sẵn bằng các cuộc gọi JavaScript thông thường hoặc selectors. Đây không phải là các phần con thông thường, mà là một kỹ thuật encapsulation mạnh mẽ.

Trong ví dụ trên, chúng ta có thể thấy một attribute hữu ích `pseudo`. Nó không chuẩn, tồn tại vì lý do lịch sử. Chúng ta có thể sử dụng nó để định style các phần tử con bằng CSS, như sau:

```
<style>
/* make the slider track red */
input::-webkit-slider-runnable-track {
  background: red;
}
</style>

<input type="range">
```

Một lần nữa, `pseudo` là attribute không chuẩn. Theo thời gian, các trình duyệt trước tiên bắt đầu thử nghiệm với các cấu trúc DOM nội bộ để triển khai các control, và sau đó, theo thời gian, shadow DOM được chuẩn hóa để cho phép chúng ta, những nhà phát triển, làm điều tương tự.

Tiếp theo, chúng ta sẽ sử dụng tiêu chuẩn shadow DOM hiện đại, được bao phủ bởi [DOM spec](https://dom.spec.whatwg.org/#shadow-trees) và các quy tắc liên quan khác.

## [Cây shadow](#shadow-tree)

Một phần tử DOM có thể có hai loại cây con DOM:

1. Light tree – cây con DOM thông thường, được tạo từ các phần con HTML. Tất cả các cây con mà chúng ta đã thấy trong các chương trước đều là “light”.
2. Shadow tree – cây con DOM ẩn, không được phản ánh trong HTML, được che giấu khỏi các ánh nhìn tò mò.

Nếu một phần tử có cả hai, thì trình duyệt chỉ render cây shadow. Nhưng chúng ta cũng có thể thiết lập một kiểu composition giữa cây shadow và light. Chúng ta sẽ xem chi tiết sau trong chương [Shadow DOM slots, composition](/slots-composition).

Shadow tree có thể được sử dụng trong Custom Elements để ẩn các chi tiết nội bộ của component và áp dụng các style cục bộ của component.

Ví dụ, phần tử `<show-hello>` này ẩn DOM nội bộ của nó trong shadow tree:

```
<script>
customElements.define('show-hello', class extends HTMLElement {
  connectedCallback() {
    const shadow = this.attachShadow({mode: 'open'});
    shadow.innerHTML = `<p>
      Hello, ${this.getAttribute('name')}
    </p>`;
  }
});
</script>

<show-hello name="John"></show-hello>
```

Đây là cách DOM kết quả trông trong dev tools của Chrome, toàn bộ nội dung nằm dưới “#shadow-root”:

![](/article/shadow-dom/shadow-dom-say-hello.png)

Trước tiên, cuộc gọi `elem.attachShadow({mode: …})` tạo ra một shadow tree.

Có hai hạn chế:

1. Chúng ta chỉ có thể tạo một shadow root mỗi phần tử.
2. `elem` phải là một custom element, hoặc một trong: “article”, “aside”, “blockquote”, “body”, “div”, “footer”, “h1…h6”, “header”, “main” “nav”, “p”, “section”, hoặc “span”. Các phần tử khác, như `<img>`, không thể chứa shadow tree.

Tùy chọn `mode` thiết lập mức độ encapsulation. Nó phải có một trong hai giá trị:

- `"open"` – shadow root có sẵn dưới dạng `elem.shadowRoot`.

  Bất kỳ mã nào cũng có thể truy cập shadow tree của `elem`.
- `"closed"` – `elem.shadowRoot` luôn là `null`.

  Chúng ta chỉ có thể truy cập shadow DOM bằng tham chiếu trả về từ `attachShadow` (và có lẽ được giấu bên trong một class). Các shadow tree gốc của trình duyệt, như `<input type="range">`, là closed. Không có cách nào để truy cập chúng.

[Shadow root](https://dom.spec.whatwg.org/#shadowroot), được trả về bởi `attachShadow`, giống như một phần tử: chúng ta có thể sử dụng `innerHTML` hoặc các phương thức DOM, như `append`, để điền nội dung.

Phần tử có shadow root được gọi là “shadow tree host”, và có sẵn dưới dạng thuộc tính `host` của shadow root:

```
// assuming {mode: "open"}, otherwise elem.shadowRoot is null
alert(elem.shadowRoot.host === elem); // true
```

## [Encapsulation](#encapsulation)

Shadow DOM được giới hạn chặt chẽ khỏi document chính:

1. Các phần tử shadow DOM không nhìn thấy được bởi `querySelector` từ light DOM. Cụ thể, các phần tử shadow DOM có thể có các id xung đột với những cái trong light DOM. Chúng chỉ phải duy nhất bên trong shadow tree.
2. Shadow DOM có các stylesheet riêng. Các quy tắc style từ DOM bên ngoài không được áp dụng.

Ví dụ:

```
<style>
  /* document style won't apply to the shadow tree inside #elem (1) */
  p { color: red; }
</style>

<div id="elem"></div>

<script>
  elem.attachShadow({mode: 'open'});
    // shadow tree has its own style (2)
  elem.shadowRoot.innerHTML = `
    <style> p { font-weight: bold; } </style>
    <p>Hello, John!</p>
  `;

  // <p> is only visible from queries inside the shadow tree (3)
  alert(document.querySelectorAll('p').length); // 0
  alert(elem.shadowRoot.querySelectorAll('p').length); // 1
</script>
```

1. Style từ document không ảnh hưởng đến shadow tree.
2. …Nhưng style từ bên trong thì hoạt động.
3. Để lấy các phần tử trong shadow tree, chúng ta phải query từ bên trong tree.

## [Tham chiếu](#references)

- DOM: <https://dom.spec.whatwg.org/#shadow-trees>
- Compatibility: <https://caniuse.com/#feat=shadowdomv1>
- Shadow DOM được đề cập trong nhiều quy tắc khác, ví dụ [DOM Parsing](https://w3c.github.io/DOM-Parsing/#the-innerhtml-mixin) chỉ định rằng shadow root có `innerHTML`.

## [Tóm tắt](#summary)

Shadow DOM là cách để tạo một DOM cục bộ cho component.

1. `shadowRoot = elem.attachShadow({mode: open|closed})` – tạo shadow DOM cho `elem`. Nếu `mode="open"`, thì nó có thể truy cập được như thuộc tính `elem.shadowRoot`.
2. Chúng ta có thể điền `shadowRoot` bằng `innerHTML` hoặc các phương thức DOM khác.

Các phần tử shadow DOM:

- Có không gian id riêng,
- Không nhìn thấy được bởi các selector JavaScript từ document chính, như `querySelector`,
- Chỉ sử dụng style từ shadow tree, không phải từ document chính.

Shadow DOM, nếu tồn tại, được trình duyệt render thay cho “light DOM” (các phần con thông thường). Trong chương [Shadow DOM slots, composition](/slots-composition) chúng ta sẽ xem cách ghép chúng lại.
