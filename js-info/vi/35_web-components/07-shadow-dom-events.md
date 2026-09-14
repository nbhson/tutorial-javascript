# Shadow DOM và events

> Source: [https://javascript.info/shadow-dom-events](https://javascript.info/shadow-dom-events)

<!-- fetched: 2026-09-14 -->

Ý tưởng đằng sau shadow tree là encapsulation các chi tiết triển khai nội bộ của một component.

Giả sử, một event click xảy ra bên trong shadow DOM của component `<user-card>`. Nhưng các scripts trong document chính không hề biết gì về bên trong của shadow DOM, đặc biệt là khi component đến từ thư viện bên thứ ba.

Vì vậy, để giữ các chi tiết được encapsulate, trình duyệt *retargets* (chuyển hướng lại) event.

**Các event xảy ra trong shadow DOM có phần tử host làm target, khi được bắt ở bên ngoài component.**

Dưới đây là một ví dụ đơn giản:

```
<user-card></user-card>

<script>
customElements.define('user-card', class extends HTMLElement {
  connectedCallback() {
    this.attachShadow({mode: 'open'});
    this.shadowRoot.innerHTML = `<p>
      <button>Click me</button>
    </p>`;
    this.shadowRoot.firstElementChild.onclick =
      e => alert("Inner target: " + e.target.tagName);
  }
});

document.onclick =
  e => alert("Outer target: " + e.target.tagName);
</script>
```

Nếu bạn click vào nút, các thông điệp là:

1. Inner target: `BUTTON` – event handler nội bộ nhận được target đúng, phần tử bên trong shadow DOM.
2. Outer target: `USER-CARD` – event handler của document nhận được shadow host làm target.

Event retargeting là một điều rất tốt, vì document bên ngoài không cần phải biết về bên trong của component. Từ góc nhìn của nó, event xảy ra trên `<user-card>`.

**Retargeting không xảy ra nếu event xảy ra trên một phần tử slotted, mà vật lý nằm trong light DOM.**

Ví dụ, nếu người dùng click vào `<span slot="username">` trong ví dụ bên dưới, target của event chính là phần tử `span` này, đối với cả shadow và light handlers:

```
<user-card id="userCard">
  <span slot="username">John Smith</span>
</user-card>

<script>
customElements.define('user-card', class extends HTMLElement {
  connectedCallback() {
    this.attachShadow({mode: 'open'});
    this.shadowRoot.innerHTML = `<div>
      <b>Name:</b> <slot name="username"></slot>
    </div>`;

    this.shadowRoot.firstElementChild.onclick =
      e => alert("Inner target: " + e.target.tagName);
  }
});

userCard.onclick = e => alert(`Outer target: ${e.target.tagName}`);
</script>
```

Nếu click xảy ra trên `"John Smith"`, đối với cả inner và outer handlers, target là `<span slot="username">`. Đó là một phần tử từ light DOM, vì vậy không có retargeting.

Mặt khác, nếu click xảy ra trên một phần tử có nguồn gốc từ shadow DOM, ví dụ trên `<b>Name</b>`, thì khi nó lan (bubble) ra khỏi shadow DOM, `event.target` của nó được đặt lại thành `<user-card>`.

## [Bubbling, event.composedPath()](#bubbling-event-composedpath)

Để mục đích bubbling event, DOM flattened được sử dụng.

Vì vậy, nếu chúng ta có một phần tử slotted, và một event xảy ra ở đâu đó bên trong nó, thì nó lan lên đến `<slot>` và lên trên.

Đường dẫn đầy đủ đến target gốc của event, với tất cả các phần tử shadow, có thể được lấy bằng `event.composedPath()`. Như chúng ta có thể thấy từ tên của phương thức, đường dẫn đó được lấy sau khi composition.

Trong ví dụ trên, DOM flattened là:

```
<user-card id="userCard">
  #shadow-root
    <div>
      <b>Name:</b>
      <slot name="username">
        <span slot="username">John Smith</span>
      </slot>
    </div>
</user-card>
```

Vì vậy, đối với click trên `<span slot="username">`, một cuộc gọi `event.composedPath()` trả về một mảng: [`span`, `slot`, `div`, `shadow-root`, `user-card`, `body`, `html`, `document`, `window`]. Đó chính xác là chuỗi cha từ phần tử target trong DOM flattened, sau composition.

Chi tiết shadow tree chỉ được cung cấp cho các cây `{mode:'open'}`

Nếu shadow tree được tạo với `{mode: 'closed'}`, thì composed path bắt đầu từ host: `user-card` và lên trên.

Đó là nguyên tắc tương tự như đối với các phương thức khác hoạt động với shadow DOM. Bên trong của các cây closed bị che giấu hoàn toàn.

## [event.composed](#event-composed)

Hầu hết các event lan truyền (bubble) qua biên shadow DOM thành công. Có một số event không làm được điều đó.

Điều này được điều khiển bởi thuộc tính đối tượng event `composed`. Nếu nó là `true`, thì event vượt qua biên. Ngược lại, nó chỉ có thể được bắt từ bên trong shadow DOM.

Nếu bạn nhìn vào [quy tắc UI Events](https://www.w3.org/TR/uievents), hầu hết các event có `composed: true`:

- `blur`, `focus`, `focusin`, `focusout`,
- `click`, `dblclick`,
- `mousedown`, `mouseup` `mousemove`, `mouseout`, `mouseover`,
- `wheel`,
- `beforeinput`, `input`, `keydown`, `keyup`.

Tất cả các event touch và pointer cũng có `composed: true`.

Có một số event có `composed: false`:

- `mouseenter`, `mouseleave` (chúng không bubbling chút nào),
- `load`, `unload`, `abort`, `error`,
- `select`,
- `slotchange`.

Những event này chỉ có thể được bắt trên các phần tử trong cùng một DOM, nơi target của event cư trú.

## [Custom events](#custom-events)

Khi chúng ta dispatch các event tùy chỉnh, chúng ta cần đặt cả hai thuộc tính `bubbles` và `composed` thành `true` để event lan truyền lên và ra khỏi component.

Ví dụ, ở đây chúng ta tạo `div#inner` trong shadow DOM của `div#outer` và kích hoạt hai event trên nó. Chỉ event có `composed: true` mới ra ngoài đến document:

```
<div id="outer"></div>

<script>
outer.attachShadow({mode: 'open'});

let inner = document.createElement('div');
outer.shadowRoot.append(inner);

/*
div(id=outer)
  #shadow-dom
    div(id=inner)
*/

document.addEventListener('test', event => alert(event.detail));

inner.dispatchEvent(new CustomEvent('test', {
  bubbles: true,
  composed: true,
  detail: "composed"
}));

inner.dispatchEvent(new CustomEvent('test', {
  bubbles: true,
  composed: false,
  detail: "not composed"
}));
</script>
```

## [Tóm tắt](#summary)

Events chỉ vượt qua biên shadow DOM nếu cờ `composed` của chúng được đặt thành `true`.

Các event tích hợp sẵn hầu hết có `composed: true`, như được mô tả trong các quy tắc liên quan:

- UI Events <https://www.w3.org/TR/uievents>.
- Touch Events <https://w3c.github.io/touch-events>.
- Pointer Events <https://www.w3.org/TR/pointerevents>.
- …Và nhiều hơn nữa.

Một số event tích hợp sẵn có `composed: false`:

- `mouseenter`, `mouseleave` (cũng không bubbling),
- `load`, `unload`, `abort`, `error`,
- `select`,
- `slotchange`.

Những event này chỉ có thể được bắt trên các phần tử trong cùng một DOM.

Nếu chúng ta dispatch một `CustomEvent`, thì chúng ta nên đặt rõ `composed: true`.

Xin lưu ý rằng trong trường hợp các component lồng nhau, một shadow DOM có thể được lồng vào một shadow DOM khác. Trong trường hợp đó, các event composed lan truyền qua tất cả các biên shadow DOM. Vì vậy, nếu một event chỉ dành cho component bao chứa trực tiếp, chúng ta cũng có thể dispatch nó trên shadow host và đặt `composed: false`. Khi đó nó nằm ngoài shadow DOM của component, nhưng sẽ không lan lên DOM cấp cao hơn.
