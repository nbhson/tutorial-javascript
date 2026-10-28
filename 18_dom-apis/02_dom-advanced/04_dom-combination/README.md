# DOM Combination — Kết Hợp Nhiều Loại DOM — [Level: Intermediate]

## 🔑 Khái niệm cốt lõi

Virtual DOM và Shadow DOM giải quyết **hai bài toán khác nhau** — chúng không loại trừ nhau:

- **Virtual DOM** tối ưu **hiệu năng cập nhật**: giảm số lần đụng DOM thật bằng cách diff → patch tối thiểu.
- **Shadow DOM** tạo **encapsulation**: cô lập CSS và cây con của một component khỏi trang.

Không có lý do gì để chỉ chọn một. Trong một ứng dụng thực tế bạn có thể **kết hợp cả ba tầng**:

1. **Virtual DOM** ở tầng ứng dụng (React/Vue) quyết định "state thay đổi → UI nào cần sửa".
2. **DOM Manipulation** ở tầng render thực thi — `appendChild`, đổi `textContent`, `innerHTML`.
3. **Shadow DOM** ở tầng component (Web Components riêng biệt, widget của bên thứ ba) bọc kín giao diện con.

Ví dụ trong `README` hiện tại chính là demo như vậy: một trang có `#app-container` được **Virtual DOM-style render** (hàm `renderVirtualDOM(count)` viết lại toàn bộ `innerHTML` theo biến `count`, bấm nút thì tăng và render lại), cạnh đó một `#shadow-root-container` dùng **`attachShadow({ mode: "open" })`** để dựng nội dung cô lập (style `p { color: blue }` chỉ áp dụng trong shadow). Hai mảng DOM này cùng nằm trong một trang mà không xung đột.

Tóm lược: *Virtual DOM = tối ưu cập nhật*; *Shadow DOM = cô lập và tái sử dụng*; biết kết hợp là kỹ năng của frontend thực chiến.

## 📐 Cấu trúc / Cú pháp

### Combined pattern — Virtual DOM area + Shadow DOM area
```js
// Part 1: Virtual DOM-style rendering
let count = 0;
const virtualContainer = document.getElementById('app-container');

function renderVirtualDOM(count) {
  virtualContainer.innerHTML = `
    <p>Số lần click: ${count}</p>
    <button id="inc-btn">Click me</button>
  `;
  virtualContainer.querySelector('#inc-btn')
    .addEventListener('click', () => { count++; renderVirtualDOM(count); });
}
renderVirtualDOM(count);

// Part 2: Shadow DOM component (encapsulated)
const shadowHost = document.createElement('div');
shadowHost.id = 'shadow-host';
const shadowRoot = shadowHost.attachShadow({ mode: 'open' });
shadowRoot.innerHTML = '<style>p{color:blue}</style><p>inside Shadow DOM</p>';
document.body.appendChild(shadowHost);
```

### Three-tier architecture diagram
```
┌──────────────────────────────────────┐
│  Application Layer (Virtual DOM)     │  State management, diffing
│  React/Vue component tree            │
├──────────────────────────────────────┤
│  Render Layer (DOM Manipulation)     │  Actual DOM operations
│  appendChild, textContent, etc.      │
├──────────────────────────────────────┤
│  Component Layer (Shadow DOM)        │  Encapsulation
│  Web Components, scoped styles       │
└──────────────────────────────────────┘
```

### When to use which approach

| Scenario | Recommended Approach |
|---|---|
| Simple page tweak | Vanilla DOM manipulation |
| Complex stateful app | Virtual DOM (React/Vue) |
| Reusable widget/library | Shadow DOM + Custom Elements |
| Third-party widget integration | Shadow DOM encapsulation |
| Micro-frontend architecture | Shadow DOM per micro-frontend |
| Design system components | Shadow DOM + Custom Elements |

## ✅ Điểm mạnh

1. **Lợi ích kép**: cập nhật nhanh (Virtual DOM) + component an toàn, đóng gói (Shadow DOM).
2. **Giảm xung đột khi integrate**: widget Shadow DOM không bị CSS của Virtual DOM app làm hỏng.
3. **Tái sử dụng xuyên dự án**: component "bọc kín" nhập vào bất kỳ React/Vue app nào.
4. **Tách trách nhiệm rõ**: ai lo render, ai lo cô lập — dễ bảo trì.
5. **Lộ trình giải thích framework**: hiểu vì sao khái niệm này đi cùng nhau trong thực tế.
6. **Gradual migration**: giữ widget cũ (Shadow DOM) bên trong app mới (Virtual DOM).
7. **Best of both worlds**: performance của Virtual DOM + isolation của Shadow DOM.
8. **Framework flexibility**: chọn Virtual DOM cho app logic, Shadow DOM cho UI components.

## ⚠️ Bẫy thường gặp & Hạn chế

1. **Đừng "cắm" Virtual DOM chồng Shadow DOM cùng chỗ một cách dư thừa** — trong trang demo, mỗi phần dùng đúng loại phù hợp.
2. **Shadow DOM cản trở diff của framework** nếu framework định vẽ trực tiếp vào bên trong — cần qua slot/composed khéo léo.
3. **Virtual DOM render toàn bộ bằng `innerHTML`** (như demo) làm mất focus/đổi state form — không đúng bản chất "patch từng phần". Về sau nên diff như `example1/helper.js`.
4. **Tăng độ phức tạp codebase** khi phối hai hệ — cần architecture rõ ràng.
5. **Debug phức tạp hơn** — phải hiểu cả two layers để trace issue.
6. **Performance overhead compound** — cả diff + shadow boundary có chi phí riêng.
7. **Event communication across boundary** — cần `composed: true` để event vượt qua shadow boundary.

## 💡 Khi nào dùng — Tình huống thực tến

1. **App chính dùng Virtual DOM (React/Vue)** nhưng cần nhúng **widget/bộ sưu tập Web Components** có Shadow DOM.
2. **Xây micro-frontend / plugin** — mỗi plugin là component đóng gói, phần layout chung dùng Virtual DOM.
3. **Thiết kế giao diện ghép nối**: bảng điều khiển (Virtual DOM) + popup/badge thành phần riêng (Shadow DOM).
4. **Gradual migration** — giữ widget cũ (Shadow DOM) bên trong app mới (Virtual DOM).
5. **Third-party widget integration** — nhúng widget từ vendor mà không lo CSS conflict.
6. **Design system distribution** — ship components dưới dạng Web Components (Shadow DOM) cho nhiều frameworks.
7. **E-commerce product page** — Virtual DOM cho product config, Shadow DOM cho review widget từ third-party.

## 🎯 Ví dụ minh họa

### Ví dụ 1: Combo demo — Virtual DOM area + Shadow DOM area
```js
// Virtual DOM-style area
let count = 0;
const appContainer = document.getElementById('app-container');

function render() {
  appContainer.innerHTML = `
    <h2>Virtual DOM Area</h2>
    <p>Số lần click: ${count}</p>
    <button id="inc">Tăng</button>
  `;
  appContainer.querySelector('#inc').addEventListener('click', () => {
    count++;
    render();
  });
}
render();

// Shadow DOM area
const shadowContainer = document.getElementById('shadow-container');
const shadowRoot = shadowContainer.attachShadow({ mode: 'open' });
shadowRoot.innerHTML = `
  <style>
    :host { display: block; padding: 16px; border: 2px dashed blue; }
    p { color: blue; }
  </style>
  <h2>Shadow DOM Area</h2>
  <p>Nội dung này được encapsulate — CSS ngoài không ảnh hưởng.</p>
`;
```

### Ví dụ 2: Shadow DOM component inside Virtual DOM app
```js
// Define Web Component
class StatCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' }).innerHTML = `
      <style>
        :host { display: block; padding: 12px; background: #f5f5f5; border-radius: 8px; }
        .value { font-size: 24px; font-weight: bold; }
        .label { color: #666; }
      </style>
      <div class="value"><slot name="value">0</slot></div>
      <div class="label"><slot name="label">Label</slot></div>
    `;
  }
}
customElements.define('stat-card', StatCard);

// Use inside Virtual DOM app
let stats = { users: 100, orders: 50 };

function renderApp() {
  document.getElementById('app').innerHTML = `
    <h1>Dashboard</h1>
    <stat-card>
      <span slot="value">${stats.users}</span>
      <span slot="label">Users</span>
    </stat-card>
    <stat-card>
      <span slot="value">${stats.orders}</span>
      <span slot="label">Orders</span>
    </stat-card>
  `;
}
renderApp();
// Shadow DOM components encapsulated inside Virtual DOM-rendered page
```

### Ví dụ 3: Event communication across shadow boundary
```js
// Shadow DOM component dispatches custom event
class CounterWidget extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' }).innerHTML = `
      <button id="btn">Click: <span id="count">0</span></button>
    `;
    this.shadowRoot.getElementById('btn').addEventListener('click', () => {
      const count = parseInt(this.shadowRoot.getElementById('count').textContent) + 1;
      this.shadowRoot.getElementById('count').textContent = count;
      this.dispatchEvent(new CustomEvent('count-change', {
        detail: { count },
        bubbles: true,
        composed: true
      }));
    });
  }
}
customElements.define('counter-widget', CounterWidget);

// Parent app listens
document.querySelector('counter-widget').addEventListener('count-change', (e) => {
  console.log('Parent received count:', e.detail.count);
});
```

### Ví dụ 4: Avoid redundant Virtual DOM inside Shadow DOM
```js
// ❌ BAD — Virtual DOM rendering inside Shadow DOM (redundant)
const shadow = host.attachShadow({ mode: 'open' });
function renderInsideShadow() {
  shadow.innerHTML = `<p>Count: ${count}</p>`; // full re-render every time
}

// ✅ GOOD — Direct DOM manipulation inside Shadow DOM
const shadow = host.attachShadow({ mode: 'open' });
const countEl = document.createElement('p');
shadow.appendChild(countEl);
function updateCount(newCount) {
  countEl.textContent = `Count: ${newCount}`; // targeted update
}
```

### Ví dụ 5: Micro-frontend with Shadow DOM
```js
// Each micro-frontend is a Shadow DOM component
class AuthMicroFrontend extends HTMLElement {
  connectedCallback() {
    this.attachShadow({ mode: 'open' }).innerHTML = `
      <style>
        :host { display: block; padding: 16px; background: #fff; border: 1px solid #ddd; }
        button { background: #007bff; color: white; border: none; padding: 8px 16px; border-radius: 4px; }
      </style>
      <div class="auth-widget">
        <h3>Authentication</h3>
        <input type="text" placeholder="Username">
        <button id="login">Login</button>
      </div>
    `;
  }
}
customElements.define('auth-micro-frontend', AuthMicroFrontend);

// Main app (Virtual DOM or vanilla) renders it alongside other components
document.getElementById('app').innerHTML = `
  <h1>Main Dashboard</h1>
  <auth-micro-frontend></auth-micro-frontend>
  <div class="content">Main app content...</div>
`;
```

## 🔬 So sánh với alternatives

| Architecture | Virtual DOM | Shadow DOM | DOM Manipulation | Best for |
|---|---|---|---|---|
| **Pure Vanilla** | ❌ | ❌ | ✅ | Small apps |
| **VDOM only** | ✅ | ❌ | ✅ (internal) | Complex SPAs |
| **Shadow only** | ❌ | ✅ | ✅ | Widget libraries |
| **Combined** | ✅ | ✅ | ✅ | Mixed apps, micro-frontend |

## 📊 Performance & Best Practices

- **Use each layer for its purpose**: Virtual DOM for app-level state, Shadow DOM for component encapsulation.
- **Avoid double-wrapping**: don't put Virtual DOM inside Shadow DOM or vice versa unnecessarily.
- **Event composed**: use `composed: true` for events crossing shadow boundary.
- **Measure combined overhead**: profile to ensure combination doesn't hurt performance.
- **Clear boundaries**: document which layer owns which part of the UI.
- **Slot-based communication**: prefer slots over direct shadowRoot access from parent.
- **Lazy load shadow components**: chỉ create custom element khi cần render.

## 🔗 Liên kết chéo

- Xem thêm: `18_dom-apis/02_dom-advanced/03_virtual-dom/` — Virtual DOM details.
- Xem thêm: `18_dom-apis/02_dom-advanced/02_shadow-dom/` — Shadow DOM details.
- Xem thêm: `18_dom-apis/02_dom-advanced/01_manipulation/` — DOM manipulation.
- Xem thêm: `18_dom-apis/02_dom-advanced/05_reactivity/` — Reactivity levels comparison.
