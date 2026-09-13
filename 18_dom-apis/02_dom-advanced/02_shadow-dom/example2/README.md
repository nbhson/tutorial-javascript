# Shadow DOM — Example 2: Slot Content Projection — [Level: Intermediate]

## 🔑 Khái niệm cốt lõi

**`<slot>`** cho phép content từ **light DOM** (bên ngoài) được đưa vào **shadow DOM** — gọi là **content projection**. Tương tự React's `props.children`.

```js
const shadow = host.attachShadow({ mode: "open" });
shadow.innerHTML = `
  <div class="wrapper">
    <h3>Tiêu đề component</h3>
    <slot name="header">Fallback header</slot>
    <slot>Content mặc định</slot>
    <slot name="footer">Fallback footer</slot>
  </div>
`;
```
```html
<my-component>
  <span slot="header">Custom header</span>
  <p>Default content (không có slot name)</p>
  <footer slot="footer">Custom footer</footer>
</my-component>
```

### Loại slot

| Loại | Mô tả |
|---|---|
| **Default slot** | Không có `name` attribute — nhận content không đánh dấu `slot` |
| **Named slot** | Có `name` attribute — nhận content có `slot="name"` attribute |
| **Fallback content** | Content bên trong `<slot>` tag — hiện khi không có light DOM content project vào |

### `::slotted()` selector
Dùng để style element được project vào slot từ bên trong shadow CSS:
```css
::slotted(img) { width: 100%; border-radius: 8px; }
::slotted(.highlight) { color: red; }
```

## 📐 Cấu trúc / Cú pháp

### Card component với slot
```js
// custom-element.js
class MyCard extends HTMLElement {
  connectedCallback() {
    this.attachShadow({ mode: "open" }).innerHTML = `
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
customElements.define("my-card", MyCard);
```
```html
<my-card>
  <img slot="media" src="photo.jpg" alt="Photo">
  <h3>Card Title</h3>
  <p>Card body content goes here.</p>
</my-card>
```

### Multiple named slots
```js
this.attachShadow({ mode: "open" }).innerHTML = `
  <header><slot name="header"></slot></header>
  <main><slot></slot></main>
  <footer><slot name="footer"></slot></footer>
`;
```

### Slot với fallback content
```js
shadow.innerHTML = `
  <div class="container">
    <slot>
      <p>No content provided — showing fallback</p>
    </slot>
  </div>
`;
// Nếu light DOM empty → fallback hiện ra
// Nếu light DOM có content → content project vào slot
```

## ✅ Điểm mạnh

1. **Component reusable** — consumer custom hóa phần content qua slot.
2. **Giữ scope CSS của shadow DOM** — style nội bộ không bị ảnh hưởng bởi light DOM.
3. **Tương tự JSX `children` prop** trong React — familiar pattern cho React developers.
4. **Multiple slots** — chia content thành header/body/footer areas.
5. **Fallback content** — component vẫn hoạt động đẹp khi không có slot content.
6. **`::slotted()` styling** — style projected content từ trong shadow CSS.

## ⚠️ Bẫy thường gặp & Hạn chế

1. **Slot không có `name` = default slot** — chứa content không đánh dấu `slot`.
2. **Nhiều default slot cùng tên sẽ được hợp nhất (merged)** thành 1 slot — tất cả unlabeled content vào cùng default slot.
3. **`::slotted(selector)`** chỉ áp dụng cho element trực tiếp trong slot, không recursive.
4. **Light DOM CSS vẫn ảnh hưởng** đến slotted content trước khi vào shadow — shadow CSS override sau.
5. **Slot chỉ project element, không project text trực tiếp** — text phải nằm trong element wrapper.
6. **Dynamic slot content** — thêm/bớt slotted element sau khi component render cần manual update.

## 💡 Khi nào dùng — Tình huống thực tến

1. **Card component** với header/body/footer linh hoạt.
2. **Modal/dialog** có custom content — title, body, actions slots.
3. **Layout wrapper** (sidebar + main + aside) — flexible content areas.
4. **Button với icon slot** — icon + label flexibly.
5. **Table component** — custom header cells, row templates.
6. **Accordion/Tabs** — each panel content từ consumer.

## 🎯 Ví dụ minh họa

### Ví dụ 1: Card component với slot
```js
class MyCard extends HTMLElement {
  connectedCallback() {
    this.attachShadow({ mode: "open" }).innerHTML = `
      <style>
        :host { display: block; border: 1px solid #ccc; border-radius: 8px; overflow: hidden; }
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
customElements.define("my-card", MyCard);
```
```html
<my-card>
  <img slot="media" src="photo.jpg" alt="Photo">
  <h3>Card Title</h3>
  <p>Card body content goes here.</p>
</my-card>
```

### Ví dụ 2: Modal với slots
```js
class Modal extends HTMLElement {
  connectedCallback() {
    this.attachShadow({ mode: "open" }).innerHTML = `
      <style>
        :host { display: block; }
        .overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; }
        .dialog { background: white; padding: 24px; border-radius: 8px; max-width: 500px; width: 90%; }
        .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
        .close { background: none; border: none; font-size: 24px; cursor: pointer; }
        .footer { margin-top: 16px; text-align: right; }
      </style>
      <div class="overlay">
        <div class="dialog">
          <div class="header">
            <slot name="title">Modal Title</slot>
            <button class="close">×</button>
          </div>
          <div class="body"><slot></slot></div>
          <div class="footer"><slot name="footer"></slot></div>
        </div>
      </div>
    `;
    
    this.shadowRoot.querySelector('.close').addEventListener('click', () => {
      this.close();
    });
  }
  
  close() { this.style.display = 'none'; }
}
customElements.define('app-modal', Modal);
```
```html
<app-modal>
  <h2 slot="title">Confirm Action</h2>
  <p>Are you sure you want to proceed?</p>
  <div slot="footer">
    <button>Cancel</button>
    <button>Confirm</button>
  </div>
</app-modal>
```

### Ví dụ 3: Button với icon slot
```js
class IconBtn extends HTMLElement {
  connectedCallback() {
    this.attachShadow({ mode: "open" }).innerHTML = `
      <style>
        :host { display: inline-block; }
        button { display: flex; align-items: center; gap: 8px; padding: 8px 16px; border: none; border-radius: 4px; background: #007bff; color: white; cursor: pointer; }
        ::slotted(svg) { width: 16px; height: 16px; fill: currentColor; }
      </style>
      <button><slot name="icon"></slot><slot></slot></button>
    `;
  }
}
customElements.define('icon-btn', IconBtn);
```
```html
<icon-btn>
  <svg slot="icon" viewBox="0 0 24 24"><path d="M12 2L2 7l10 5 10-5-10-5z"/></svg>
  Save
</icon-btn>
```

### Ví dụ 4: Fallback content trong slot
```js
class Panel extends HTMLElement {
  connectedCallback() {
    this.attachShadow({ mode: "open" }).innerHTML = `
      <style>
        :host { display: block; border: 1px solid #ddd; padding: 16px; }
        .empty { color: #999; font-style: italic; }
      </style>
      <div>
        <slot>
          <p class="empty">No content — showing empty state</p>
        </slot>
      </div>
    `;
  }
}
customElements.define('panel', Panel);
// <panel></panel> → show empty state
// <panel><p>Custom</p></panel> → show custom content
```

### Ví dụ 5: Multiple named slots — Dashboard layout
```js
class Dashboard extends HTMLElement {
  connectedCallback() {
    this.attachShadow({ mode: "open" }).innerHTML = `
      <style>
        :host { display: grid; grid-template-columns: 200px 1fr; grid-template-rows: 60px 1fr 40px; height: 100vh; }
        header { grid-column: 1 / -1; background: #333; color: white; padding: 0 16px; display: flex; align-items: center; }
        aside { background: #f5f5f5; padding: 16px; }
        main { padding: 16px; overflow: auto; }
        footer { grid-column: 1 / -1; background: #333; color: white; padding: 0 16px; display: flex; align-items: center; justify-content: flex-end; }
      </style>
      <header><slot name="header"></slot></header>
      <aside><slot name="sidebar"></slot></aside>
      <main><slot></slot></main>
      <footer><slot name="footer"></slot></footer>
    `;
  }
}
customElements.define('dashboard-layout', Dashboard);
```

## 🔗 Liên kết chéo

- Xem thêm: `18_dom-apis/02_dom-advanced/02_shadow-dom/` — Shadow DOM tổng quan.
- Xem thêm: `18_dom-apis/02_dom-advanced/02_shadow-dom/example1/` — basic Shadow DOM.
- File tham khảo: `app.js`, `index.html`, `style.css` trong folder `example2/`.
