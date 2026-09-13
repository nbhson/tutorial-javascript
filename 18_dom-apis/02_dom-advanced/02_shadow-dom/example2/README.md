# Shadow DOM — Example 2: Slot Content Projection

## 🔑 Khái niệm

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

## ✅ Điểm mạnh
- Component reusable — consumer custom hóa phần content
- Giữ scope CSS của shadow DOM
- Tương tự JSX `children` prop trong React

## ⚠️ Lưu ý
- `slot` không có `name` = **default slot** (chứa content không đánh dấu `slot`)
- Nhiều default slot cùng tên sẽ được hợp nhất (merged) thành 1 slot
- `::slotted(selector)` selector style phần tử trong slot

## 💡 Khi nào dùng
- Card component với header/body/footer linh hoạt
- Modal/dialog có custom content
- Layout wrapper (sidebar + main + aside)

## 🎯 Ví dụ minh họa

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

## 📚 Tham khảo & Bài tập
- File: `app.js`, `index.html`, `style.css` trong folder `example2/`
- Thực hành: tạo `<alert-box>` component có slot "icon" và slot mặc định
- Câu hỏi: `::slotted()` có áp dụng được cho element trong shadow DOM không?
