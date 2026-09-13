# Shadow DOM — Encapsulation cho Component UI — [Level: Intermediate]

## 🔑 Khái niệm cốt lõi

**Shadow DOM** là công nghệ Web Components cho phép **gắn một cây DOM con riêng biệt** vào một element (gọi là **Shadow Host**) và bao nó trong **Shadow Boundary** — ranh giới cách ly:

- **Shadow Host**: phần tử thường của trang mà bạn gắn Shadow DOM vào (`host.attachShadow({ mode: 'open'|'closed' })`).
- **Shadow Tree**: cây DOM ẩn bên trong host — bao gồm style và các element riêng.
- **Shadow Boundary**: "hộp kín" — **CSS và DOM bên trong không bị ảnh hưởng bởi trang**, và ngược lại, trang không nhìn thấy hay chỉnh được nội dung bên trong (khi mode `closed` càng chặt).

Mục tiêu: **encapsulation (đóng gói)** — build UI component **tái sử dụng độc lập** mà không lo xung đột style với phần còn lại của trang: không "CSS leak" ra ngoài, không bị CSS toàn cục xâm nhập, selector nội bộ không đụng nhau. Cùng với `customElements.define`, đây chính là bộ khung của tiêu chuẩn **Web Components** (như thẻ `<video>`, `<input>` nội bộ trình duyệt cũng dùng shadow tree).

### Shadow DOM mode

| Mode | Đặc điểm |
|---|---|
| `open` | `host.shadowRoot` truy cập được từ bên ngoài —便于 debug |
| `closed` | `host.shadowRoot` trả về `null` — encapsulation strict hơn |

**Lưu ý quan trọng**: `closed` mode không tuyệt đối — vẫn có thể leak qua `inspect()` trong DevTools. Đây là security qua obscurity, không phải encryption.

### Slot — content projection
`<slot>` cho phép content từ **light DOM** (bên ngoài) được đưa vào **shadow DOM** — gọi là **content projection**. Tương tự React's `props.children`.

```html
<!-- Light DOM (user của component) -->
<my-card>
  <img slot="media" src="photo.jpg">
  <h3>Card Title</h3>
</my-card>

<!-- Shadow DOM template -->
<div class="card">
  <slot name="media"></slot>
  <slot></slot> <!-- default slot -->
</div>
```

Thư mục này có 2 ví dụ:
- `example1/app.js` — tạo shadow DOM **mode `closed`** trên `#appContainer`, thêm một `<div>` chữ "Hello from Shadow DOM!" cùng class `red_color`.
- `example2/app.js` — định nghĩa **custom element** `<custom-widget>` với shadow root **mode `open`**, style qua `:host`, đăng ký bằng `customElements.define`.

## 📐 Cấu trúc / Cú pháp

### Basic shadow DOM
```js
const host = document.getElementById('appContainer');
const shadowRoot = host.attachShadow({ mode: 'closed' }); // hoặc 'open'
const el = document.createElement('div');
el.textContent = 'Hello from Shadow DOM!';
el.classList.add('red_color');
shadowRoot.appendChild(el);
// Với mode closed: host.shadowRoot === null (không truy cập được từ ngoài)
```

### Custom element với shadow DOM
```js
class CustomWidget extends HTMLElement {
  constructor() {
    super();
    const root = this.attachShadow({ mode: 'open' });
    root.innerHTML = `
      <style>
        :host { display:block; border:2px solid green; padding:10px; }
        p { color: blue; }
      </style>
      <p>I'm a custom widget!</p>
    `;
  }
}
customElements.define('custom-widget', CustomWidget);
// Dùng: <custom-widget></custom-widget>
```

### Slot content projection
```js
class MyCard extends HTMLElement {
  connectedCallback() {
    this.attachShadow({ mode: 'open' }).innerHTML = `
      <style>
        :host { display: block; border: 1px solid #ccc; border-radius: 8px; }
        .card { padding: 16px; }
        ::slotted(img) { width: 100%; border-radius: 8px 8px 0 0; }
      </style>
      <div class="card">
        <slot name="media"></slot>
        <slot></slot>
      </div>
    `;
  }
}
customElements.define('my-card', MyCard);
```

### CSS scoping trong shadow DOM
```css
/* Trong shadow root — chỉ ảnh hưởng nội bộ */
:host { display: block; }           /* target chính host element */
::slotted(*) { color: red; }        /* target projected content */
::part(custom-element) { ... }      /* target Light DOM part */

/* CSS ngoài trang KHÔNG ảnh hưởng được vào shadow DOM */
/* CSS trong shadow DOM KHÔNG leak ra ngoài */
```

## ✅ Điểm mạnh

1. **Cô lập CSS triệt để** — style component không "tràn" ra trang, không bị trang làm hỏng.
2. **Che giấu cấu trúc nội bộ** — logic/DOM bên trong là chi tiết cài đặt — truy cập bên ngoài bị hạn chế.
3. **Tái sử dụng an toàn** — cùng một component dùng nhiều nơi, nhiều dự án mà không đụng nhau.
4. **Bảo mật kiểu** — ngăn thành phần bên ngoài (thư viện UI tích hợp) làm rối giao diện.
5. **Hiệu năng render tốt hơn** — trình duyệt biết rõ phạm vi, quản lý style scoped hiệu quả.
6. **Standard Web Components** — tích hợp sẵn trong browser, không cần polyfill (trừ IE).
7. **Cross-framework** — Web Components chạy được trong React, Vue, Angular cùng lúc.
8. **Slot-based API** — consumer customize content qua slot, component giữ structure.

## ⚠️ Bẫy thường gặp & Hạn chế

1. **Giao tiếp ngoài-trong khó hơn** — cần cẩn thận để truyền dữ liệu/sự kiện qua boundary (thường qua attributes, events, hoặc `composed: true`).
2. **Mode `closed` hạn chế debug** — DevTools và code ngoài không "mở khóa" được shadowRoot để xem bên trong.
3. **Style slider/các pseudo-class** trình duyệt bên trong shadow tree hoạt động giới hạn hơn.
4. **Đúng một mình Shadow DOM (không kèm `customElements`)** vẫn chỉ là cách cô lập — chưa phải "component đầy đủ".
5. **CSS variables inheritance** — CSS custom properties từ host vẫn inherited vào shadow, cần `:host` context.
6. **Event composed** — sự kiện không composed mặc định không vượt qua shadow boundary lên document.
7. **Third-party library integration** — một số thư viện (chart, map) không hoạt động tốt bên trong shadow DOM.

## 💡 Khi nào dùng — Tình huống thực tến

1. **Xây dựng thư viện/marketplace UI widget** cần bọc kín style và hành vi.
2. **Tổ chức multiple apps / plugin** trên cùng trang mà không được xung đột CSS.
3. **Build Web Components** để tái sử dụng xuyên framework (dùng trong React lẫn Vue).
4. **Nhúng third-party UI** mà không thể kiểm soát CSS toàn cục.
5. **Design system component** — cách ly style giữa các component trong design system.
6. **Iframe alternative** — Shadow DOM nhẹ hơn iframe, cùng encapsulation level.
7. **Learn scoped CSS concept** — rèn luyện trước khi gặp scoped CSS của Vue (`<style scoped>`) hay CSS Modules.

## 🎯 Ví dụ minh họa

### Ví dụ 1: Shadow DOM basic (example1 pattern)
```js
const host = document.getElementById('appContainer');
const shadowRoot = host.attachShadow({ mode: 'closed' });
const el = document.createElement('div');
el.textContent = 'Hello from Shadow DOM!';
el.classList.add('red_color');
shadowRoot.appendChild(el);
// Ngoài không truy cập được shadowRoot (mode closed)
// Console: appContainer.shadowRoot → null
```

### Ví dụ 2: Custom element (example2 pattern)
```js
class CustomWidget extends HTMLElement {
  constructor() {
    super();
    const root = this.attachShadow({ mode: 'open' });
    root.innerHTML = `
      <style>
        :host { display:block; border:2px solid green; padding:10px; }
        p { color: blue; font-weight: bold; }
      </style>
      <div>I'm a custom widget!</div>`;
  }
}
customElements.define('custom-widget', CustomWidget);
// HTML: <custom-widget></custom-widget>
```

### Ví dụ 3: Slot content projection
```js
class AlertBox extends HTMLElement {
  connectedCallback() {
    this.attachShadow({ mode: 'open' }).innerHTML = `
      <style>
        :host { display: block; padding: 12px; border-radius: 4px; }
        .info { background: #e3f2fd; }
        .error { background: #ffebee; }
        ::slotted(*) { margin: 0; }
      </style>
      <div class="alert">
        <slot></slot>
      </div>
    `;
    // Set theme based on attribute
    const theme = this.getAttribute('type') || 'info';
    this.shadowRoot.querySelector('.alert').className = `alert ${theme}`;
  }
}
customElements.define('alert-box', AlertBox);
```

### Ví dụ 4: Read attribute in custom element
```js
class Greeting extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' }).innerHTML = `
      <style>:host { display:block; padding:8px; }</style>
      <span class="greeting"></span>
    `;
  }
  connectedCallback() {
    const name = this.getAttribute('name') || 'World';
    this.shadowRoot.querySelector('.greeting').textContent = `Hello, ${name}!`;
  }
}
customElements.define('greeting-element', Greeting);
// <greeting-element name="Sơn"></greeting-element>
```

### Ví dụ 5: Open vs Closed mode comparison
```js
// Mode open
const openHost = document.getElementById('open-host');
const openRoot = openHost.attachShadow({ mode: 'open' });
openRoot.innerHTML = '<p>Open mode</p>';
console.log(openHost.shadowRoot); // ShadowRoot { ... } ✅ accessible

// Mode closed
const closedHost = document.getElementById('closed-host');
const closedRoot = closedHost.attachShadow({ mode: 'closed' });
closedRoot.innerHTML = '<p>Closed mode</p>';
console.log(closedHost.shadowRoot); // null ❌ not accessible from outside
```

### Ví dụ 6: Event passing through shadow boundary
```js
class ParentComponent extends HTMLElement {
  connectedCallback() {
    this.attachShadow({ mode: 'open' }).innerHTML = `
      <button id="btn">Click me</button>
    `;
    this.shadowRoot.getElementById('btn').addEventListener('click', () => {
      // Custom event với composed: true để vượt qua shadow boundary
      this.dispatchEvent(new CustomEvent('item-click', { 
        detail: { message: 'clicked!' },
        bubbles: true,
        composed: true 
      }));
    });
  }
}
customElements.define('parent-comp', ParentComponent);

// External listener
document.querySelector('parent-comp').addEventListener('item-click', (e) => {
  console.log(e.detail.message); // "clicked!"
});
```

## 🔬 So sánh với alternatives

| Approach | Encapsulation | Browser Support | Complexity | Bundle Size |
|---|---|---|---|---|
| **Shadow DOM** | ✅ Strong | ✅ Modern browsers | Trung bình | 0KB (native) |
| **CSS Modules** | ✅ Scoped | ✅ Cần build | Thấp | ~5KB tooling |
| **Scoped CSS (Vue)** | ✅ Scoped | ✅ Cần build | Thấp | ~3KB tooling |
| **Iframe** | ✅ Very strong | ✅ Tất cả | Cao | Overhead nặng |
| **BEM naming** | ⚠️ Convention only | ✅ Tất cả | Thấp | 0KB |
| **Inline styles** | ⚠️ Partial | ✅ Tất cả | Thấp | 0KB |

## 📊 Performance & Best Practices

- **Prefer `mode: 'open'`** trong development — dễ debug qua DevTools.
- **Use `:host` selector** để style host element từ trong shadow — cleanest approach.
- **Use `::slotted()`** để style projected content — precise targeting.
- **Custom events with `composed: true`** — cần thiết để event vượt qua shadow boundary.
- **Keep shadow DOM small** — nhiều shadow roots trong cùng trang có overhead.
- **Test cross-browser** — Shadow DOM support tốt trên modern browsers, nhưng IE không support.
- **Combine with Custom Elements** — Shadow DOM + Custom Elements + HTML Templates = đầy đủ Web Components.
- **Avoid deep nesting** — shadow DOM trong shadow DOM (nested shadow) rarely needed, phức tạp hóa debug.

## 🔗 Liên kết chéo

- Xem thêm: `18_dom-apis/02_dom-advanced/02_shadow-dom/example1/` — basic encapsulation demo.
- Xem thêm: `18_dom-apis/02_dom-advanced/02_shadow-dom/example2/` — slot content projection.
- Xem thêm: `18_dom-apis/02_dom-advanced/03_virtual-dom/` — Virtual DOM so với Shadow DOM.
- Xem thêm: `18_dom-apis/02_dom-advanced/04_dom-combination/` — kết hợp cả hai.
- Xem thêm: `17_memory-management/04_meta-programming/` — Proxy foundation cho reactivity.
- Ảnh: `rdxxidul7q_4.png`, `id968au9dy_1.png` — hidden class visualization.
