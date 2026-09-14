# Shadow DOM slots, composition (Kết hợp)

> Source: [https://javascript.info/slots-composition](https://javascript.info/slots-composition)

<!-- fetched: 2026-09-14 -->

Nhiều loại component, như tabs, menus, thư viện ảnh, và nhiều hơn nữa, cần nội dung để render.

Giống như `<select>` tích hợp sẵn của trình duyệt mong đợi các mục `<option>`, `<custom-tabs>` của chúng ta có thể mong đợi nội dung tab thực tế được truyền vào. Và `<custom-menu>` có thể mong đợi các mục menu.

Mã sử dụng `<custom-menu>` có thể trông như sau:

```
<custom-menu>
  <title>Candy menu</title>
  <item>Lollipop</item>
  <item>Fruit Toast</item>
  <item>Cup Cake</item>
</custom-menu>
```

…Sau đó component của chúng ta nên render nó đúng cách, như một menu đẹp với tiêu đề và các mục được cho, xử lý các event menu, v.v.

Làm cách nào để triển khai?

Chúng ta có thể thử phân tích nội dung phần tử và sao chép-xắp xếp lại các nút DOM động. Điều đó là có thể, nhưng nếu chúng ta di chuyển các phần tử vào shadow DOM, thì các style CSS từ document không được áp dụng ở đó, nên kiểu dáng trực quan có thể bị mất. Ngoài ra, điều đó cần một chút mã hóa.

May mắn là, chúng ta không cần phải làm vậy. Shadow DOM hỗ trợ các phần tử `<slot>`, được tự động điền bởi nội dung từ light DOM.

## [Named slots](#named-slots)

Hãy xem cách slots hoạt động bằng một ví dụ đơn giản.

Ở đây, shadow DOM của `<user-card>` cung cấp hai slots, được điền từ light DOM:

```
<script>
customElements.define('user-card', class extends HTMLElement {
  connectedCallback() {
    this.attachShadow({mode: 'open'});
    this.shadowRoot.innerHTML = `
      <div>Name:
        <slot name="username"></slot>
      </div>
      <div>Birthday:
        <slot name="birthday"></slot>
      </div>
    `;
  }
});
</script>

<user-card>
  <span slot="username">John Smith</span>
  <span slot="birthday">01.01.2001</span>
</user-card>
```

Trong shadow DOM, `<slot name="X">` định nghĩa một “điểm chèn”, nơi các phần tử có `slot="X"` được render.

Sau đó trình duyệt thực hiện “composition”: nó lấy các phần tử từ light DOM và render chúng trong các slot tương ứng của shadow DOM. Cuối cùng, chúng ta có chính xác những gì mong muốn – một component có thể được điền bằng dữ liệu.

Đây là cấu trúc DOM sau khi chạy script, không tính đến composition:

```
<user-card>
  #shadow-root
    <div>Name:
      <slot name="username"></slot>
    </div>
    <div>Birthday:
      <slot name="birthday"></slot>
    </div>
  <span slot="username">John Smith</span>
  <span slot="birthday">01.01.2001</span>
</user-card>
```

Chúng ta đã tạo shadow DOM, vì vậy ở đây nó nằm dưới `#shadow-root`. Giờ đây phần tử có cả light DOM và shadow DOM.

Mục đích render, đối với mỗi `<slot name="...">` trong shadow DOM, trình duyệt tìm kiếm `slot="..."` với cùng tên trong light DOM. Những phần tử này được render bên trong các slot:

![](/article/slots-composition/shadow-dom-user-card.svg)

Kết quả được gọi là DOM “flattened”:

```
<user-card>
  #shadow-root
    <div>Name:
      <slot name="username">
        <!-- slotted element is inserted into the slot -->
        <span slot="username">John Smith</span>
      </slot>
    </div>
    <div>Birthday:
      <slot name="birthday">
        <span slot="birthday">01.01.2001</span>
      </slot>
    </div>
</user-card>
```

…Nhưng DOM flattened chỉ tồn tại cho mục đích render và xử lý event. Nó mang tính “ảo”. Đó là cách các thứ được hiển thị. Nhưng các nút trong document thực sự không bị di chuyển!

Điều đó dễ dàng kiểm chứng được nếu chúng ta chạy `querySelectorAll`: các nút vẫn ở vị trí của chúng.

```
// light DOM <span> nodes are still at the same place, under `<user-card>`
alert( document.querySelectorAll('user-card span').length ); // 2
```

Vậy, DOM flattened được suy ra từ shadow DOM bằng cách chèn các slot. Trình duyệt render nó và sử dụng cho việc kế thừa style, lan truyền event (sẽ bàn sau). Nhưng JavaScript vẫn nhìn thấy document “như vậy”, trước khi flatten.

Chỉ các phần con cấp trên cùng mới có thể có attribute slot="…"

Attribute `slot="..."` chỉ hợp lệ với các phần con trực tiếp của shadow host (trong ví dụ của chúng ta, phần tử `<user-card>`). Đối với các phần tử lồng nhau, nó bị bỏ qua.

Ví dụ, `<span>` thứ hai ở đây bị bỏ qua (vì nó không phải là phần con trực tiếp của `<user-card>`):

```
<user-card>
  <span slot="username">John Smith</span>
  <div>
    <!-- invalid slot, must be direct child of user-card -->
    <span slot="birthday">01.01.2001</span>
  </div>
</user-card>
```

Nếu có nhiều phần tử trong light DOM cùng tên slot, chúng được thêm vào slot, lần lượt.

Ví dụ, cái này:

```
<user-card>
  <span slot="username">John</span>
  <span slot="username">Smith</span>
</user-card>
```

Cho ra DOM flattened với hai phần tử trong `<slot name="username">`:

```
<user-card>
  #shadow-root
    <div>Name:
      <slot name="username">
        <span slot="username">John</span>
        <span slot="username">Smith</span>
      </slot>
    </div>
    <div>Birthday:
      <slot name="birthday"></slot>
    </div>
</user-card>
```

## [Nội dung fallback của slot](#slot-fallback-content)

Nếu chúng ta đặt thứ gì đó vào trong `<slot>`, nó trở thành nội dung fallback, “mặc định”. Trình duyệt hiển thị nó nếu không có phần tử điền tương ứng trong light DOM.

Ví dụ, trong đoạn shadow DOM này, `Anonymous` được render nếu không có `slot="username"` trong light DOM.

```
<div>Name:
  <slot name="username">Anonymous</slot>
</div>
```

## [Slot mặc định: slot không tên đầu tiên](#default-slot-first-unnamed)

`<slot>` đầu tiên trong shadow DOM không có tên là slot “mặc định”. Nó nhận tất cả các nút từ light DOM không được đặt vào slot khác.

Ví dụ, hãy thêm slot mặc định vào `<user-card>` của chúng ta để hiển thị tất cả thông tin về người dùng không được gán slot:

```
<script>
customElements.define('user-card', class extends HTMLElement {
  connectedCallback() {
    this.attachShadow({mode: 'open'});
    this.shadowRoot.innerHTML = `
    <div>Name:
      <slot name="username"></slot>
    </div>
    <div>Birthday:
      <slot name="birthday"></slot>
    </div>
    <fieldset>
      <legend>Other information</legend>
      <slot></slot>
    </fieldset>
    `;
  }
});
</script>

<user-card>
  <div>I like to swim.</div>
  <span slot="username">John Smith</span>
  <span slot="birthday">01.01.2001</span>
  <div>...And play volleyball too!</div>
</user-card>
```

Tất cả nội dung light DOM không được gán slot sẽ vào fieldset “Other information”.

Các phần tử được thêm vào slot lần lượt, vì vậy cả hai mẩu thông tin không được gán slot đều nằm cùng nhau trong slot mặc định.

DOM flattened trông như thế này:

```
<user-card>
  #shadow-root
    <div>Name:
      <slot name="username">
        <span slot="username">John Smith</span>
      </slot>
    </div>
    <div>Birthday:
      <slot name="birthday">
        <span slot="birthday">01.01.2001</span>
      </slot>
    </div>
    <fieldset>
      <legend>Other information</legend>
      <slot>
        <div>I like to swim.</div>
        <div>...And play volleyball too!</div>
      </slot>
    </fieldset>
</user-card>
```

## [Ví dụ menu](#menu-example)

Giờ hãy quay lại `<custom-menu>`, được nhắc đến ở đầu chương.

Chúng ta có thể sử dụng slots để phân bổ các phần tử.

Đây là markup cho `<custom-menu>`:

```
<custom-menu>
  <span slot="title">Candy menu</span>
  <li slot="item">Lollipop</li>
  <li slot="item">Fruit Toast</li>
  <li slot="item">Cup Cake</li>
</custom-menu>
```

Shadow DOM template với các slots phù hợp:

```
<template id="tmpl">
  <style> /* menu styles */ </style>
  <div class="menu">
    <slot name="title"></slot>
    <ul><slot name="item"></slot></ul>
  </div>
</template>
```

1. `<span slot="title">` đi vào `<slot name="title">`.
2. Có nhiều `<li slot="item">` trong `<custom-menu>`, nhưng chỉ có một `<slot name="item">` trong template. Vì vậy tất cả các `<li slot="item">` như vậy được thêm vào `<slot name="item">` lần lượt, tạo thành danh sách.

DOM flattened trở thành:

```
<custom-menu>
  #shadow-root
    <style> /* menu styles */ </style>
    <div class="menu">
      <slot name="title">
        <span slot="title">Candy menu</span>
      </slot>
      <ul>
        <slot name="item">
          <li slot="item">Lollipop</li>
          <li slot="item">Fruit Toast</li>
          <li slot="item">Cup Cake</li>
        </slot>
      </ul>
    </div>
</custom-menu>
```

Có thể nhận thấy rằng, trong một DOM hợp lệ, `<li>` phải là phần con trực tiếp của `<ul>`. Nhưng đó là DOM flattened, nó mô tả cách component được render, điều như vậy xảy ra tự nhiên ở đây.

Chúng ta chỉ cần thêm một handler `click` để mở/đóng danh sách, và `<custom-menu>` sẵn sàng:

```
customElements.define('custom-menu', class extends HTMLElement {
  connectedCallback() {
    this.attachShadow({mode: 'open'});

    // tmpl is the shadow DOM template (above)
    this.shadowRoot.append( tmpl.content.cloneNode(true) );

    // we can't select light DOM nodes, so let's handle clicks on the slot
    this.shadowRoot.querySelector('slot[name="title"]').onclick = () => {
      // open/close the menu
      this.shadowRoot.querySelector('.menu').classList.toggle('closed');
    };
  }
});
```

Đây là demo đầy đủ:

Tất nhiên, chúng ta có thể thêm nhiều chức năng hơn: events, methods, và nhiều hơn nữa.

## [Cập nhật slots](#updating-slots)

Điều gì xảy ra nếu mã bên ngoài muốn thêm/xóa các mục menu động?

**Trình duyệt giám sát các slots và cập nhật render khi các phần tử slotted được thêm/xóa.**

Ngoài ra, vì các nút light DOM không bị sao chép, mà chỉ được render trong các slot, các thay đổi bên trong chúng ngay lập tức trở nên hiển thị.

Vì vậy chúng ta không cần làm gì để cập nhật render. Nhưng nếu mã component muốn biết về các thay đổi slot, thì event `slotchange` có sẵn.

Ví dụ, ở đây mục menu được chèn động sau 1 giây, và tiêu đề thay đổi sau 2 giây:

```
<custom-menu id="menu">
  <span slot="title">Candy menu</span>
</custom-menu>

<script>
customElements.define('custom-menu', class extends HTMLElement {
  connectedCallback() {
    this.attachShadow({mode: 'open'});
    this.shadowRoot.innerHTML = `<div class="menu">
      <slot name="title"></slot>
      <ul><slot name="item"></slot></ul>
    </div>`;

    // shadowRoot can't have event handlers, so using the first child
    this.shadowRoot.firstElementChild.addEventListener('slotchange',
      e => alert("slotchange: " + e.target.name)
    );
  }
});

setTimeout(() => {
  menu.insertAdjacentHTML('beforeEnd', '<li slot="item">Lollipop</li>')
}, 1000);

setTimeout(() => {
  menu.querySelector('[slot="title"]').innerHTML = "New menu";
}, 2000);
</script>
```

Render menu được cập nhật mỗi lần mà không cần chúng ta can thiệp.

Có hai event `slotchange` ở đây:

1. Khi khởi tạo:

   `slotchange: title` được kích hoạt ngay lập tức, vì `slot="title"` từ light DOM đi vào slot tương ứng.
2. Sau 1 giây:

   `slotchange: item` được kích hoạt, khi `<li slot="item">` mới được thêm.

Xin lưu ý: không có event `slotchange` sau 2 giây, khi nội dung của `slot="title"` bị sửa đổi. Đó là vì không có thay đổi slot. Chúng ta sửa đổi nội dung bên trong phần tử slotted, đó là chuyện khác.

Nếu chúng ta muốn theo dõi các thay đổi nội bộ của light DOM từ JavaScript, điều đó cũng có thể bằng cách sử dụng cơ chế tổng quát hơn: [MutationObserver](/mutation-observer).

## [Slot API](#slot-api)

Cuối cùng, hãy đề cập đến các phương thức JavaScript liên quan đến slot.

Như chúng ta đã thấy trước đó, JavaScript nhìn vào DOM “thực sự”, không flatten. Nhưng, nếu shadow tree có `{mode: 'open'}`, thì chúng ta có thể xác định những phần tử nào được gán cho một slot, và ngược lại, slot bởi phần tử bên trong nó:

- `node.assignedSlot` – trả về phần tử `<slot>` mà `node` được gán vào.
- `slot.assignedNodes({flatten: true/false})` – các nút DOM được gán cho slot. Tùy chọn `flatten` là `false` theo mặc định. Nếu đặt rõ là `true`, thì nó nhìn sâu hơn vào DOM flattened, trả về các slot lồng nhau trong trường hợp các component lồng nhau, và nội dung fallback nếu không có nút được gán.
- `slot.assignedElements({flatten: true/false})` – các phần tử DOM được gán cho slot (giống như trên, nhưng chỉ các phần tử node).

Các phương thức này hữu ích khi chúng ta cần không chỉ hiển thị nội dung slotted, mà còn theo dõi nó trong JavaScript.

Ví dụ, nếu component `<custom-menu>` muốn biết nó hiển thị gì, thì nó có thể theo dõi `slotchange` và lấy các mục từ `slot.assignedElements`:

```
<custom-menu id="menu">
  <span slot="title">Candy menu</span>
  <li slot="item">Lollipop</li>
  <li slot="item">Fruit Toast</li>
</custom-menu>

<script>
customElements.define('custom-menu', class extends HTMLElement {
  items = []

  connectedCallback() {
    this.attachShadow({mode: 'open'});
    this.shadowRoot.innerHTML = `<div class="menu">
      <slot name="title"></slot>
      <ul><slot name="item"></slot></ul>
    </div>`;

    // triggers when slot content changes
    this.shadowRoot.firstElementChild.addEventListener('slotchange', e => {
      let slot = e.target;
      if (slot.name == 'item') {
        this.items = slot.assignedElements().map(elem => elem.textContent);
        alert("Items: " + this.items);
      }
    });
  }
});

// items update after 1 second
setTimeout(() => {
  menu.insertAdjacentHTML('beforeEnd', '<li slot="item">Cup Cake</li>')
}, 1000);
</script>
```

## [Tóm tắt](#summary)

Thông thường, nếu một phần tử có shadow DOM, thì light DOM của nó không được hiển thị. Slots cho phép hiển thị các phần tử từ light DOM ở các vị trí được chỉ định trong shadow DOM.

Có hai loại slot:

- Named slots: `<slot name="X">...</slot>` – nhận các phần con light có `slot="X"`.
- Slot mặc định: `<slot>` đầu tiên không có tên (các slot không tên sau đó bị bỏ qua) – nhận các phần con light không được gán slot.
- Nếu có nhiều phần tử cho cùng một slot – chúng được thêm lần lượt.
- Nội dung của phần tử `<slot>` được sử dụng như fallback. Nó được hiển thị nếu không có phần con light nào cho slot.

Quy trình render các phần tử slotted bên trong các slot của chúng được gọi là “composition”. Kết quả được gọi là “flattened DOM”.

Composition không thực sự di chuyển các nút, từ góc nhìn của JavaScript DOM vẫn như cũ.

JavaScript có thể truy cập các slot bằng cách sử dụng các phương thức:

- `slot.assignedNodes/Elements()` – trả về các nút/phần tử bên trong `slot`.
- `node.assignedSlot` – thuộc tính ngược, trả về slot bằng một nút.

Nếu chúng ta muốn biết mình đang hiển thị gì, chúng ta có thể theo dõi nội dung slot bằng cách sử dụng:

- Event `slotchange` – được kích hoạt lần đầu tiên khi slot được điền, và ở bất kỳ thao tác thêm/xóa/thay thế nào của phần tử slotted, nhưng không phải các phần con của nó. Slot là `event.target`.
- [MutationObserver](/mutation-observer) để đi sâu hơn vào nội dung slot, theo dõi các thay đổi bên trong nó.

Giờ đây, khi chúng ta đã biết cách hiển thị các phần tử từ light DOM trong shadow DOM, hãy xem cách định style chúng đúng cách. Quy tắc cơ bản là các phần tử shadow được định style ở bên trong, và các phần tử light – ở bên ngoài, nhưng có một số ngoại lệ đáng chú ý.

Chúng ta sẽ xem chi tiết trong chương tiếp theo.
