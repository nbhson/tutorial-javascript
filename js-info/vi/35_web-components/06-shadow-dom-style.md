# Shadow DOM styling (Kiểu dáng)

> Source: [https://javascript.info/shadow-dom-style](https://javascript.info/shadow-dom-style)

<!-- fetched: 2026-09-14 -->

Shadow DOM có thể bao gồm cả các thẻ `<style>` và `<link rel="stylesheet" href="…">`. Trong trường hợp sau, các stylesheet được HTTP-cache, nên chúng không được tải lại cho nhiều component sử dụng cùng một template.

Như một quy tắc chung, các style cục bộ chỉ hoạt động bên trong shadow tree, và style document hoạt động ở bên ngoài nó. Nhưng có một số ngoại lệ.

## [:host](#host)

Selector `:host` cho phép chọn shadow host (phần tử chứa shadow tree).

Ví dụ, chúng ta đang tạo phần tử `<custom-dialog>` nên được căn giữa. Để làm điều đó, chúng ta cần định style chính phần tử `<custom-dialog>`.

Đó chính xác là điều `:host` làm:

```
<template id="tmpl">
  <style>
    /* the style will be applied from inside to the custom-dialog element */
    :host {
      position: fixed;
      left: 50%;
      top: 50%;
      transform: translate(-50%, -50%);
      display: inline-block;
      border: 1px solid red;
      padding: 10px;
    }
  </style>
  <slot></slot>
</template>

<script>
customElements.define('custom-dialog', class extends HTMLElement {
  connectedCallback() {
    this.attachShadow({mode: 'open'}).append(tmpl.content.cloneNode(true));
  }
});
</script>

<custom-dialog>
  Hello!
</custom-dialog>
```

## [Cascading](#cascading)

Shadow host (chính `<custom-dialog>`), nằm trong light DOM, nên bị ảnh hưởng bởi các quy tắc CSS của document.

Nếu có một thuộc tính được định style cả trong `:host` cục bộ, và trong document, thì style document được ưu tiên.

Ví dụ, nếu trong document chúng ta có:

```
<style>
custom-dialog {
  padding: 0;
}
</style>
```

…Thì `<custom-dialog>` sẽ không có padding.

Điều đó rất tiện lợi, vì chúng ta có thể thiết lập các style “mặc định” của component trong quy tắc `:host` của nó, và sau đó dễ dàng ghi đè chúng trong document.

Ngoại lệ là khi một thuộc tính cục bộ được gắn nhãn `!important`, đối với các thuộc tính như vậy, style cục bộ được ưu tiên.

## [:host(selector)](#host-selector)

Giống như `:host`, nhưng chỉ được áp dụng nếu shadow host khớp với `selector`.

Ví dụ, chúng ta muốn căn giữa `<custom-dialog>` chỉ khi nó có attribute `centered`:

```
<template id="tmpl">
  <style>
    :host([centered]) {
      position: fixed;
      left: 50%;
      top: 50%;
      transform: translate(-50%, -50%);
      border-color: blue;
    }

    :host {
      display: inline-block;
      border: 1px solid red;
      padding: 10px;
    }
  </style>
  <slot></slot>
</template>

<script>
customElements.define('custom-dialog', class extends HTMLElement {
  connectedCallback() {
    this.attachShadow({mode: 'open'}).append(tmpl.content.cloneNode(true));
  }
});
</script>

<custom-dialog centered>
  Centered!
</custom-dialog>

<custom-dialog>
  Not centered.
</custom-dialog>
```

Giờ các style căn giữa bổ sung chỉ được áp dụng cho dialog đầu tiên: `<custom-dialog centered>`.

Tóm lại, chúng ta có thể sử dụng họ selector `:host` để định style phần tử chính của component. Các style này (trừ khi `!important`) có thể bị document ghi đè.

## [Định style nội dung slotted](#styling-slotted-content)

Giờ hãy xem xét tình huống với slots.

Các phần tử slotted đến từ light DOM, vì vậy chúng sử dụng style document. Các style cục bộ không ảnh hưởng đến nội dung slotted.

Trong ví dụ bên dưới, `<span>` slotted in đậm, theo style document, nhưng không nhận `background` từ style cục bộ:

```
<style>
  span { font-weight: bold }
</style>

<user-card>
  <div slot="username"><span>John Smith</span></div>
</user-card>

<script>
customElements.define('user-card', class extends HTMLElement {
  connectedCallback() {
    this.attachShadow({mode: 'open'});
    this.shadowRoot.innerHTML = `
      <style>
      span { background: red; }
      </style>
      Name: <slot name="username"></slot>
    `;
  }
});
</script>
```

Kết quả là in đậm, nhưng không đỏ.

Nếu chúng ta muốn định style các phần tử slotted trong component của mình, có hai lựa chọn.

Thứ nhất, chúng ta có thể định style chính `<slot>` và dựa vào CSS inheritance:

```
<user-card>
  <div slot="username"><span>John Smith</span></div>
</user-card>

<script>
customElements.define('user-card', class extends HTMLElement {
  connectedCallback() {
    this.attachShadow({mode: 'open'});
    this.shadowRoot.innerHTML = `
      <style>
      slot[name="username"] { font-weight: bold; }
      </style>
      Name: <slot name="username"></slot>
    `;
  }
});
</script>
```

Ở đây `<p>John Smith</p>` trở nên in đậm, vì CSS inheritance có hiệu lực giữa `<slot>` và nội dung của nó. Nhưng trong chính CSS không phải tất cả thuộc tính đều được kế thừa.

Một lựa chọn khác là sử dụng pseudo-class `::slotted(selector)`. Nó khớp với các phần tử dựa trên hai điều kiện:

1. Đó là một phần tử slotted, đến từ light DOM. Tên slot không quan trọng. Bất kỳ phần tử slotted nào, nhưng chỉ chính phần tử đó, không phải các phần con của nó.
2. Phần tử khớp với `selector`.

Trong ví dụ của chúng ta, `::slotted(div)` chọn đúng `<div slot="username">`, nhưng không chọn các phần con của nó:

```
<user-card>
  <div slot="username">
    <div>John Smith</div>
  </div>
</user-card>

<script>
customElements.define('user-card', class extends HTMLElement {
  connectedCallback() {
    this.attachShadow({mode: 'open'});
    this.shadowRoot.innerHTML = `
      <style>
      ::slotted(div) { border: 1px solid red; }
      </style>
      Name: <slot name="username"></slot>
    `;
  }
});
</script>
```

Xin lưu ý, selector `::slotted` không thể đi sâu hơn nữa vào slot. Các selector này không hợp lệ:

```
::slotted(div span) {
  /* our slotted <div> does not match this */
}

::slotted(div) p {
  /* can't go inside light DOM */
}
```

Ngoài ra, `::slotted` chỉ có thể được sử dụng trong CSS. Chúng ta không thể sử dụng nó trong `querySelector`.

## CSS hooks với custom properties

Làm thế nào chúng ta định style các phần tử nội bộ của một component từ document chính?

Các selector như `:host` áp dụng các quy tắc cho phần tử `<custom-dialog>` hoặc `<user-card>`, nhưng làm thế nào để định style các phần tử shadow DOM bên trong chúng?

Không có selector nào có thể trực tiếp ảnh hưởng đến style shadow DOM từ document. Nhưng cũng giống như chúng ta phơi bày các method để tương tác với component, chúng ta có thể phơi bày các biến CSS (custom CSS properties) để định style nó.

**Các custom CSS properties tồn tại ở mọi cấp, cả trong light DOM và shadow DOM.**

Ví dụ, trong shadow DOM chúng ta có thể sử dụng biến CSS `--user-card-field-color` để định style các trường, và document bên ngoài có thể đặt giá trị của nó:

```
<style>
  .field {
    color: var(--user-card-field-color, black);
    /* if --user-card-field-color is not defined, use black color */
  }
</style>
<div class="field">Name: <slot name="username"></slot></div>
<div class="field">Birthday: <slot name="birthday"></slot></div>
```

Sau đó, chúng ta có thể khai báo thuộc tính này trong document bên ngoài cho `<user-card>`:

```
user-card {
  --user-card-field-color: green;
}
```

Các custom CSS properties xuyên qua shadow DOM, chúng nhìn thấy được ở mọi nơi, nên quy tắc `.field` bên trong sẽ tận dụng nó.

Đây là ví dụ đầy đủ:

```
<style>
  user-card {
    --user-card-field-color: green;
  }
</style>

<template id="tmpl">
  <style>
    .field {
      color: var(--user-card-field-color, black);
    }
  </style>
  <div class="field">Name: <slot name="username"></slot></div>
  <div class="field">Birthday: <slot name="birthday"></slot></div>
</template>

<script>
customElements.define('user-card', class extends HTMLElement {
  connectedCallback() {
    this.attachShadow({mode: 'open'});
    this.shadowRoot.append(document.getElementById('tmpl').content.cloneNode(true));
  }
});
</script>

<user-card>
  <span slot="username">John Smith</span>
  <span slot="birthday">01.01.2001</span>
</user-card>
```

## [Tóm tắt](#summary)

Shadow DOM có thể bao gồm các style, như `<style>` hoặc `<link rel="stylesheet">`.

Các style cục bộ có thể ảnh hưởng đến:

- shadow tree,
- shadow host bằng các pseudoclass `:host` và `:host()`,
- các phần tử slotted (đến từ light DOM), `::slotted(selector)` cho phép chọn chính các phần tử slotted, nhưng không chọn các phần con của chúng.

Style document có thể ảnh hưởng đến:

- shadow host (vì nó nằm trong document bên ngoài)
- các phần tử slotted và nội dung của chúng (vì đó cũng ở trong document bên ngoài)

Khi các thuộc tính CSS xung đột, thông thường style document được ưu tiên, trừ khi thuộc tính được gắn nhãn `!important`. Khi đó style cục bộ được ưu tiên.

Các custom CSS properties xuyên qua shadow DOM. Chúng được sử dụng như các “hooks” để định style component:

1. Component sử dụng một custom CSS property để định style các phần tử chính, như `var(--component-name-title, <default value>)`.
2. Tác giả component công bố các thuộc tính này cho các nhà phát triển, chúng quan trọng ngang với các method công khai khác của component.
3. Khi một nhà phát triển muốn định style tiêu đề, họ gán thuộc tính CSS `--component-name-title` cho shadow host hoặc cao hơn.
4. Lợi nhuận!
