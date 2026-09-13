# DOM APIs — Nâng cao — [Level: Intermediate]

## 🔑 Khái niệm cốt lõi

Phần nâng cao chuẩn bị cho bạn những khái niệm mà mọi framework frontend hiện đại đều xoay quanh. Đây là cầu nối từ vanilla DOM sang understanding React, Vue, Angular.

### 5 Nhóm kiến thức

1. **01_manipulation** — kỹ thuật **DOM Manipulation** và các sự kiện vòng đời trang (`DOMContentLoaded`, `load`, `beforeunload`, `hashchange`, `resize`...) với ví dụ to-do list.
2. **02_shadow-dom** — **Shadow DOM**: encapsulation — cây DOM con được cô lập về CSS và cấu trúc khỏi trang chính (nền tảng Web Components).
3. **03_virtual-dom** — **Virtual DOM**: biểu diễn ảo của DOM trong bộ nhớ; khi state thay đổi thì tạo cây ảo mới, **diff** với cây cũ, chỉ **patch** phần khác lên DOM thật (đúng tinh thần React).
4. **04_dom-combination** — kết hợp Virtual DOM + Shadow DOM trong một ứng dụng (mỗi loại giải quyết một bài toán khác nhau).
5. **05_reactivity** — mức độ "phản ứng tự động": DOM manip (thấp) → Virtual DOM (cao) → Shadow DOM (trung bình-cao); minh họa reactive state bằng **Proxy**.

### Phân biệt 3 khái niệm then chốt

- **Virtual DOM** tối ưu **hiệu năng cập nhật** — giảm số lần đụng DOM thật thông qua diff + patch.
- **Shadow DOM** tập trung **cô lập và tái sử dụng** — CSS/DOM riêng, không xung đột giữa component và trang.
- **Reactivity** là "tự theo dõi dữ liệu thay đổi → tự cập nhật giao diện" — cách hiện thực có thể là Virtual DOM (React/Vue) hoặc Proxy + re-render thủ công.

### Levels of Reactivity

| Level | Cơ chế | Tự động update UI? | Performance | Framework example |
|---|---|---|---|---|
| **DOM Manipulation** | Hand-written DOM updates | ❌ Không — developer phải gọi tay | ⭐⭐⭐ Fastest | jQuery, vanilla JS |
| **Shadow DOM** | Encapsulated subtree | ❌ Không tự động — cần manual update | ⭐⭐⭐ Fast | Web Components |
| **Virtual DOM** | Diff + patch tree | ✅ Có — framework auto diff | ⭐⭐ Medium | React, Preact |
| **Proxy Reactivity** | Trap set/get on object | ✅ Có — fine-grained update | ⭐⭐ Medium | Vue 2, Polymer |
| **Signals** | Dependency tracking | ✅ Có — most granular | ⭐⭐⭐ Fast | Solid, Svelte, Vue 3 |

## 📐 Cấu trúc / Cú pháp

### DOM Manipulation pattern
```js
document.addEventListener('DOMContentLoaded', function () {
  const btn = document.getElementById('btnClickMe');
  btn.addEventListener('click', function () {
    btn.innerText = "What's up";
    btn.setAttribute('style', 'color:red; padding:4px');
  });
});

// To-do list pattern
const item = document.createElement('li');
item.textContent = taskText;
item.addEventListener('click', () => item.remove());
taskList.appendChild(item);
```

### Shadow DOM pattern
```js
// Basic shadow DOM
const host = document.getElementById('appContainer');
const shadowRoot = host.attachShadow({ mode: 'open' });
shadowRoot.innerHTML = '<style>p{color:blue}</style><p>inside shadow</p>';

// Custom element with shadow DOM
class CustomWidget extends HTMLElement {
  constructor() {
    super();
    const root = this.attachShadow({ mode: 'open' });
    root.innerHTML = `
      <style>:host { display:block; border:2px solid green; padding:10px; }</style>
      <div>I'm a custom widget!</div>`;
  }
}
customElements.define('custom-widget', CustomWidget);
```

### Virtual DOM pattern
```js
// Create VNode
const vNode = { tag: 'p', props: {}, children: [`Counter: ${state.counter}`] };
// Diff old vs new VNode
// Patch only changed parts to real DOM
```

### Proxy Reactivity pattern
```js
const state = new Proxy({ count: 0 }, {
  set(target, key, value) {
    target[key] = value;
    updateUI(value); // auto-update
    return true;
  }
});
```

## ✅ Điểm mạnh

1. **Đúng thứ kiến thức framework cần** — nắm Virtual DOM / reactivity là hiểu vì sao React/Vue làm việc như họ làm.
2. **Encapsulation thật** — Shadow DOM chống CSS leak giữa component và trang.
3. **Hiệu năng tối ưu** — cập nhật tối thiểu lên DOM thật thay vì rebuild toàn bộ.
4. **Bản thân các ví dụ là module nhỏ chạy được** — học bằng thực hành.
5. **Bắc cầu từ DOM thường sang framework** — hiểu được cả cách làm tay (vanilla) lẫn "bên trong" thư viện lớn.
6. **Hiểu trade-offs** — biết khi nào dùng DOM direct vs Virtual DOM vs Shadow DOM.
7. **Foundation cho Web Components** — Shadow DOM + Custom Elements = chuẩn component system của web.
8. **Reactivity understanding** — nắm được cơ chế bên dưới Vue/Polymer/Svelte.

## ⚠️ Bẫy thường gặp & Hạn chế

1. **Virtual DOM có overhead** (tạo/diff cây ảo) — với ứng dụng nhỏ, sửa DOM trực tiếp nhanh hơn.
2. **Shadow DOM làm truyền dữ liệu/events giữa ngoài-trong phức tạp hơn** — cần cẩn thận với composed events.
3. **Reactivity (Proxy) đọc/ghi qua proxy chậm hơn một chút** và khó gỡ lỗi hơn direct access.
4. **Có ba loại DOM với mục đích khác nhau** — đừng coi chúng là "hoán đổi cho nhau". Mỗi loại giải quyết bài toán khác.
5. **Virtual DOM không free** — diff tree vẫn tốn CPU, đặc biệt với cây rất lớn.
6. **Shadow DOM closed mode** — không thể truy cập shadowRoot từ bên ngoài, khó debug.
7. **Proxy không work với primitive values** — chỉ wrap object/array, không wrap number/string trực tiếp.

## 💡 Khi nào dùng — Tình huống thực tến

1. **SPA phức tạp, state thay đổi liên tục** → cần Virtual DOM / reactivity (chọn framework).
2. **Build thư viện UI / widget dùng chung nhiều trang** → Shadow DOM để bọc kín style.
3. **Trang đơn giản, cần thêm tính năng nhỏ** → không cần framework, DOM Manipulation là đủ.
4. **Cần validate/đồng bộ tự động dữ liệu ↔ UI** → lắp một layer reactivity bằng Proxy.
5. **Nghiên cứu kiến trúc trước khi chọn framework** — React: Virtual DOM; Vue: reactivity + Virtual DOM; Stencil/lit: Shadow DOM.
6. **Integrate third-party widget** → Shadow DOM encapsulation prevents CSS conflicts.
7. **Build design system** → Web Components (Shadow DOM + Custom Elements) cross-framework reuse.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Virtual DOM spirit — state to DOM
```js
let state = { counter: 0 };

function render() {
  const container = document.getElementById('app');
  // In real framework, this would diff old vs new VNode
  // Here we just re-render for illustration
  container.innerHTML = `
    <p>Counter: ${state.counter}</p>
    <button id="inc">Increment</button>
  `;
  document.getElementById('inc').addEventListener('click', () => {
    state.counter++;
    render(); // re-render on state change
  });
}
render();
```

### Ví dụ 2: Shadow DOM encapsulation
```js
const host = document.getElementById('appContainer');
const shadowRoot = host.attachShadow({ mode: 'open' });
shadowRoot.innerHTML = `
  <style>
    :host { display: block; padding: 16px; }
    p { color: blue; }
  </style>
  <p>Trong bong tối — CSS global không ảnh hưởng.</p>
`;
// Class 'p' trong shadow DOM luôn blue, không bị CSS ngoài Override
```

### Ví dụ 3: Proxy reactivity cơ bản
```js
const state = new Proxy({ count: 0 }, {
  set(target, key, value) {
    target[key] = value;
    document.getElementById('counter').innerText = `Số lần click: ${value}`;
    return true;
  }
});

document.getElementById('clickButton').addEventListener('click', () => {
  state.count += 1; // UI tự đổi qua proxy set trap
});
```

### Ví dụ 4: DOM Manipulation — to-do list
```js
document.addEventListener('DOMContentLoaded', function () {
  const taskInput = document.getElementById('taskInput');
  const addTaskBtn = document.getElementById('addTaskBtn');
  const taskList = document.getElementById('taskList');

  addTaskBtn.addEventListener('click', function () {
    const text = taskInput.value.trim();
    if (text !== '') {
      const li = document.createElement('li');
      li.textContent = text;
      li.addEventListener('click', () => li.remove());
      taskList.appendChild(li);
      taskInput.value = '';
    }
  });
});
```

### Ví dụ 5: Event delegation trong manipulation
```js
const taskList = document.getElementById('taskList');
taskList.addEventListener('click', (e) => {
  if (e.target.tagName === 'LI') {
    e.target.remove();
  }
});
// 1 listener ở parent lo được mọi LI — thêm/xóa LI mới vẫn hoạt động
```

### Ví dụ 6: Shadow DOM + Slot content projection
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

// Usage:
// <my-card>
//   <img slot="media" src="photo.jpg" alt="Photo">
//   <h3>Card Title</h3>
//   <p>Card body content.</p>
// </my-card>
```

### Ví dụ 7: Combination — Virtual DOM + Shadow DOM
```js
// Virtual DOM part — manages state and diffing
let count = 0;
function renderVirtualDOM() {
  const container = document.getElementById('app-container');
  const oldVNode = container._vNode;
  const newVNode = { tag: 'div', children: [
    { tag: 'p', text: `Clicks: ${count}` },
    { tag: 'button', text: 'Increment' }
  ]};
  // diff and patch...
  container._vNode = newVNode;
}

// Shadow DOM part — encapsulated component
const shadowHost = document.createElement('div');
const root = shadowHost.attachShadow({ mode: 'open' });
root.innerHTML = '<style>p{color:blue}</style><p>inside Shadow DOM</p>';
document.body.appendChild(shadowHost);
```

### Ví dụ 8: Reactive state with multiple properties
```js
const state = new Proxy({ count: 0, name: 'App' }, {
  set(target, key, value) {
    target[key] = value;
    // Update all dependent UI elements
    const countEl = document.getElementById('counter');
    const nameEl = document.getElementById('name-display');
    if (countEl) countEl.textContent = `Count: ${target.count}`;
    if (nameEl) nameEl.textContent = `Name: ${target.name}`;
    return true;
  }
});
```

## 🔬 So sánh với alternatives

| Approach | Automation | Performance | Learning Curve | Best for |
|---|---|---|---|---|
| **DOM Manipulation** | Manual | ⭐⭐⭐ Fastest | Thấp | App nhỏ, prototype |
| **Shadow DOM** | Semi (encapsulation) | ⭐⭐⭐ Fast | Trung bình | Web Components, widgets |
| **Virtual DOM** | Auto (diff+patch) | ⭐⭐ Medium | Trung bình | Complex SPAs |
| **Proxy Reactivity** | Auto (fine-grained) | ⭐⭐ Medium | Cao | Data-driven UI |
| **Signals** | Auto (granular) | ⭐⭐⭐ Fast | Cao | Modern frameworks |

## 📊 Performance & Best Practices

- **DOM Manipulation**: batch changes, avoid reflow in loops, use DocumentFragment.
- **Shadow DOM**: prefer `mode: 'open'` for debuggability; use `::slotted()` for styled projected content.
- **Virtual DOM**: ensure stable `key` in lists for efficient diffing; avoid unnecessary re-renders.
- **Proxy Reactivity**: wrap only top-level state; use shallow proxies for large nested objects.
- **Combination**: Virtual DOM for app-level state, Shadow DOM for component encapsulation —各司其职.
- **Test in target browsers**: Shadow DOM support varies (all modern browsers except IE).
- **Accessibility**: Shadow DOM accessible content still needs ARIA attributes inside shadow.
- **Bundle size**: Shadow DOM + Custom Elements ~5KB minified; Virtual DOM frameworks ~30-100KB.

## 🔗 Liên kết chéo

- Xem thêm: `18_dom-apis/02_dom-advanced/01_manipulation/` — DOM manipulation techniques.
- Xem thêm: `18_dom-apis/02_dom-advanced/02_shadow-dom/` — Shadow DOM encapsulation.
- Xem thêm: `18_dom-apis/02_dom-advanced/03_virtual-dom/` — Virtual DOM diffing.
- Xem thêm: `18_dom-apis/02_dom-advanced/05_reactivity/` — Proxy-based reactivity.
- Xem thêm: `18_dom-apis/03_events/` — event system foundation.
- Xem thêm: `17_memory-management/04_meta-programming/` — Proxy/Reflect fundamentals.
