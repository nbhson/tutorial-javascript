# Shadow DOM — Example 1: Basic Encapsulation — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

**Shadow DOM** là kỹ thuật đóng gói markup + style bên trong một "shadow tree" tách biệt khỏi main document DOM. Element chứa shadow tree gọi là **shadow host**.

```js
const host = document.querySelector("#host");
const shadow = host.attachShadow({ mode: "open" | "closed" });
shadow.innerHTML = `<style>.box{color:red}</style><div class="box">Tôi trong shadow</div>`;
```

### Mode: open vs closed

| Mode | Đặc điểm | Debugging | Use case |
|---|---|---|---|
| `open` | `host.shadowRoot` truy cập được từ bên ngoài | Dễ — DevTools hiển thị shadow tree | Development, debugging |
| `closed` | `host.shadowRoot` trả về `null` | Khó — phải qua DevTools Elements panel | Production, strict encapsulation |

**Lưu ý**: `closed` mode không tuyệt đối bảo mật — DevTools vẫn hiển thị shadow tree trong Elements panel. Đây là encapsulation qua API, không phải security.

### CSS scoping trong Shadow DOM

- CSS trong shadow root **chỉ ảnh hưởng** đến nội dung trong shadow tree.
- CSS từ main document **không ảnh hưởng** được vào shadow tree.
- `:host` selector — target chính host element từ trong shadow.
- `::slotted(selector)` — target element được project vào slot từ light DOM.

## 📐 Cấu trúc / Cú pháp

### Shadow DOM cơ bản
```js
const host = document.getElementById("widget");
const shadow = host.attachShadow({ mode: "open" });

shadow.innerHTML = `
  <style>
    :host { display: block; padding: 16px; }
    .title { color: blue; font-weight: bold; }
  </style>
  <h2 class="title">Shadow Component</h2>
  <p>Nội dung trong shadow DOM, CSS global không ảnh hưởng.</p>
`;
```

### So sánh CSS scope
```html
<!-- Main document CSS -->
<style>
  .box { color: green; } /* áp dụng cho host DOM */
</style>

<!-- Shadow DOM CSS -->
<style>
  .box { color: red !important; } /* áp dụng cho shadow DOM */
</style>
```
→ `.box` trong shadow luôn đỏ, `.box` bên ngoài luôn xanh — **không ảnh hưởng lẫn nhau**.

### Host selector
```css
:host {
  display: block;
  border: 1px solid #ccc;
  border-radius: 8px;
}

:host(:hover) {
  border-color: blue;
}

:host(.featured) {
  background: yellow;
}
```

## ✅ Điểm mạnh

1. **Style bên trong không rò rỉ ra ngoài** — CSS global không ảnh hưởng, component tự chứa đầy đủ style.
2. **HTML/CSS bên trong không bị CSS global ghi đè** (trừ `::part` / `::slotted`) — encapsulation là thật.
3. **Basis của Web Components** — component tự chứa đầy đủ markup + style + behavior.
4. **Reusable across projects** — copy component sang project khác, style không xung đột.
5. **Performance** — browser có thể optimize style resolution tốt hơn với scoped CSS.

## ⚠️ Bẫy thường gặp & Hạn chế

1. **`closed` không tuyệt đối** — vẫn có thể leak qua `inspect()` DevTools. Đừng dựa vào closed mode cho security.
2. **Shadow DOM không share CSS variables từ host** trừ khi define `:host` — CSS custom properties vẫn inherited.
3. **Debug khó hơn** một chút vì element bị "ẩn" trong shadow boundary — cần mở DevTools Elements panel.
4. **Không được iframe sandbox nếu không cho `allow-same-origin`** — shadow DOM trong iframe có restrictions.
5. **`computedStyle` từ ngoài không đọc được shadow internals** — `getComputedStyle(host)` không hiện shadow styles.
6. **JavaScript query từ ngoài không vào được shadow** — `host.querySelector('.box')` không tìm thấy element trong shadow.

## 💡 Khi nào dùng — Tình huống thực tến

1. **Web Components tái sử dụng** (custom element + shadow) — component tự chứa đầy đủ.
2. **Widget nhúng từ bên thứ ba** (iframe alternative) — nhẹ hơn iframe, cùng encapsulation.
3. **Design system component** cách ly style — button, card, modal reusableAcross projects.
4. **Third-party ads/widgets** — prevent CSS conflicts với main site.
5. **Library distribution** — ship component với scoped style, consumer không cần config.

## 🎯 Ví dụ minh họa

### Ví dụ 1: Shadow DOM basic
```js
const host = document.getElementById("widget");
const shadow = host.attachShadow({ mode: "open" });

shadow.innerHTML = `
  <style>
    :host { display: block; padding: 16px; }
    .title { color: blue; font-weight: bold; }
    .content { color: #333; }
  </style>
  <h2 class="title">Shadow Component</h2>
  <p class="content">Nội dung trong shadow DOM, CSS global không ảnh hưởng.</p>
`;
```

### Ví dụ 2: Encapsulated modal component
```js
class Modal extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' }).innerHTML = `
      <style>
        :host { display: none; position: fixed; inset: 0; z-index: 9999; }
        :host([open]) { display: flex; }
        .overlay { position: absolute; inset: 0; background: rgba(0,0,0,0.5); }
        .dialog { position: relative; background: white; padding: 24px; border-radius: 8px; max-width: 400px; margin: auto; }
        .close { position: absolute; top: 8px; right: 8px; cursor: pointer; background: none; border: none; font-size: 20px; }
      </style>
      <div class="overlay"></div>
      <div class="dialog">
        <button class="close">×</button>
        <slot></slot>
      </div>
    `;
    
    this.shadowRoot.querySelector('.close').addEventListener('click', () => {
      this.removeAttribute('open');
    });
    this.shadowRoot.querySelector('.overlay').addEventListener('click', () => {
      this.removeAttribute('open');
    });
  }
  
  open() { this.setAttribute('open', ''); }
  close() { this.removeAttribute('open'); }
}
customElements.define('app-modal', Modal);
```

### Ví dụ 3: Theme-aware shadow component
```js
class ThemedCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' }).innerHTML = `
      <style>
        :host { display: block; padding: 16px; border-radius: 8px; background: var(--card-bg, white); color: var(--card-color, black); }
        h3 { margin-top: 0; }
      </style>
      <h3><slot name="title">Default Title</slot></h3>
      <div><slot></slot></div>
    `;
  }
}
customElements.define('themed-card', ThemedCard);
// Usage: <themed-card style="--card-bg: #f0f0f0;"><!-- content --></themed-card>
```

## 🔗 Liên kết chéo

- Xem thêm: `18_dom-apis/02_dom-advanced/02_shadow-dom/` — Shadow DOM tổng quan.
- Xem thêm: `18_dom-apis/02_dom-advanced/02_shadow-dom/example2/` — slot content projection.
- File tham khảo: `app.js`, `index.html`, `style.css` trong folder `example1/`.
