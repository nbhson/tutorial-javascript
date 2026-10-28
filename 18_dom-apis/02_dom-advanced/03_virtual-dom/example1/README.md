# Virtual DOM — Nguyên Lý Hoạt Động — [Level: Intermediate]

## 🔑 Khái niệm cốt lõi

**Virtual DOM (VDOM)** là bản sao trong bộ nhớ JS của DOM thật. Khi state thay đổi:
1. Tạo VDOM tree mới từ state (render function)
2. **Diffing**: so sánh VDOM cũ vs mới (reconciliation)
3. **Patch**: áp dụng thay đổi nhỏ nhất lên DOM thật

React, Preact, Inferno… đều dùng cơ chế này. Ý tưởng cốt lõi: **thay vìthủ công tính toán phần nào cần đổi, hãy mô tả toàn bộ UI mới rồi để algorithm tìm difference**.

```
State change
    ↓
render() → VDOM tree (JS object)
    ↓
diff(oldVDOM, newVDOM)
    ↓
computes minimal patch set
    ↓
applyPatch(actual DOM)
```

### Tại sao diff lại quan trọng?

Giả sử bạn có list 1000 items và chỉ thêm 1 item ở cuối:
- **Without VDOM**: rebuild toàn bộ 1000 DOM nodes → 1000 createElement + 1000 appendChild.
- **With VDOM**: diff chỉ tìm ra 1 difference → 1 createElement + 1 appendChild.

### Key prop — tại sao quan trọng?

Khi diff lists, algorithm cần biết item nào đã tồn tại, item nào mới, item nào bị xóa. **Key** là identifier ổn định giúp diff chính xác:
```js
// ✅ Good — stable unique key
items.map(item => h('li', { key: item.id }, item.name))

// ❌ Bad — index as key (problematic khi reorder/delete)
items.map((item, index) => h('li', { key: index }, item.name))
```

## 📐 Cấu trúc / Cú pháp

### VDOM đơn giản (không dùng thư viện)
```js
// 1. Định nghĩa VDOM tree
const vdom = {
  tag: "div",
  props: { className: "app" },
  children: [
    { tag: "h1", props: {}, children: ["Hello"] },
    { tag: "p", props: {}, children: ["Virtual DOM demo"] }
  ]
};

// 2. Render VDOM → actual DOM
function render(vnode, container) {
  const el = document.createElement(vnode.tag);
  Object.entries(vnode.props || {}).forEach(([k, v]) => {
    if (k.startsWith("on")) el.addEventListener(k.slice(2).toLowerCase(), v);
    else el.setAttribute(k, v);
  });
  vnode.children?.forEach(child => {
    el.appendChild(
      typeof child === "string" 
        ? document.createTextNode(child)
        : render(child, container)
    );
  });
  container.appendChild(el);
  return el;
}

// 3. Diff đơn giản
function diff(oldTree, newTree) {
  if (oldTree.tag !== newTree.tag) return "REPLACE";
  // so sánh props, children recurse...
}
```

### React example (declarative)
```jsx
function Counter() {
  const [count, setCount] = useState(0);
  return (
    <button onClick={() => setCount(c => c + 1)}>
      Clicked {count} times
    </button>
  );
}
// mỗi lần setCount → React diff + patch, không re-render toàn bộ DOM
```

### Minimal Virtual DOM implementation
```js
function h(tag, props, ...children) {
  return { tag, props: props || {}, children };
}

function render(vnode, parent) {
  let el = parent._vnode ? parent._vnode.el : null;
  
  if (!el) {
    el = document.createElement(vnode.tag);
    Object.entries(vnode.props || {}).forEach(([k, v]) => {
      if (k.startsWith('on')) el.addEventListener(k.slice(2).toLowerCase(), v);
      else el.setAttribute(k, v);
    });
    vnode.children.forEach(child => {
      render(typeof child === 'string' 
        ? { tag: '#text', props: {}, children: [], text: child }
        : child, el);
    });
    parent.appendChild(el);
  } else {
    // Diff and patch
    const oldVnode = parent._vnode;
    if (vnode.tag !== oldVnode.tag) {
      parent.replaceChild(document.createElement(vnode.tag), el);
    }
    // ... deeper diff logic
  }
  
  parent._vnode = vnode;
  vnode.el = el;
}
```

## ✅ Điểm mạnh

1. **Batch updates** — nhiều state change hợp nhất thành 1 DOM update.
2. **Cross-browser** — abstraction layer, developer không lo browser quirks.
3. **Predictable** — mỗi lần render cùng state → cùng output (pure function).
4. **Optimized diff** — O(n) algorithm thay vì O(n³) brute force.
5. **Declarative UI** — mô tả "what" thay vì "how", code dễ đọc hơn.
6. **Server-side rendering** — VNode tree có thể serialize thành HTML string.
7. **Hot reload** — state preserved khi code thay đổi (development).
8. **Testing-friendly** — VNode tree là plain JS object, dễ mock và test.

## ⚠️ Bẫy thường gặp & Hạn chế

1. **VDOM overhead** — bộ nhớ + CPU cho diffing — không free. App đơn giản có thể fasterdirect DOM.
2. **Không phải lúc nào cũng nhanh hơn DOM trực tiếp** — cho simple app, DOM manipulation raw nhanh hơn.
3. **React 18+ có concurrent mode** giảm bớt issue này — time-slicing, progressive rendering.
4. **Framework không dùng VDOM** (Solid, Svelte, Vue 3 with signals) đang lên ngôi — fine-grained reactivityefficient hơn.
5. **Key prop sai** — dùng index khi list reorder → wrong updates, lost focus/scroll state.
6. **Unnecessary re-renders** — parent re-render trigger con re-render dù con props không đổi (React.memo fix).

## 💡 Khi nào dùng — Tình huống thực tến

1. **App có UI phức tạp, nhiều component re-render** — VDOM diff giảm DOM operations.
2. **State change liên tục** (dashboard, game, chat) — batch updates mượt mà.
3. **Cần declarative UI** (describe what, not how) — code dễ maintain.
4. **Cross-platform** — cùng VNode tree render thành DOM (web), native (React Native), terminal (ink).

## 🎯 Ví dụ minh họa

### Ví dụ 1: Counter với VDOM
```js
let count = 0;

function render() {
  const container = document.getElementById('app');
  const oldVNode = container._vnode;
  
  const newVNode = {
    tag: 'div',
    children: [
      { tag: 'p', children: [`Count: ${count}`] },
      { tag: 'button', props: { onclick: () => { count++; render(); } }, children: ['Increment'] }
    ]
  };
  
  const patch = diff(oldVNode, newVNode);
  applyPatch(container, patch);
  container._vnode = newVNode;
}
```

### Ví dụ 2: List rendering với key
```js
function renderList(items) {
  const ul = document.querySelector('ul');
  const oldVNode = ul._vnode;
  
  const newVNode = {
    tag: 'ul',
    children: items.map(item => ({
      tag: 'li',
      key: item.id,  // stable key!
      children: [item.text]
    }))
  };
  
  const patch = diff(oldVNode, newVNode);
  applyPatch(ul, patch);
  ul._vnode = newVNode;
}
```

## 🔬 So sánh với alternatives

| Approach | Update Granularity | Performance | Learning Curve |
|---|---|---|---|
| **Virtual DOM** | Component/Tree level | ⭐⭐ Good | Thấp-Trung bình |
| **Fine-grained (Signals)** | Individual DOM node | ⭐⭐⭐ Best | Cao |
| **Direct DOM** | Exact node | ⭐⭐⭐ Best (simple) | Thấp |
| **Template strings** | Full replacement | ⭐⭐ Medium | Thấp |

## 📊 Performance & Best Practices

- **Use stable keys** — unique ID, không dùng index khi list reorderable.
- **Memoize expensive computations** — `useMemo`/`memo` tránh re-render không cần.
- **Keep VDOM tree small** — phân chia component hợp lý, tránh giant component.
- **Batch state updates** — framework tự batch, nhưng hiểu cơ chế giúp write better code.
- **Profile before optimizing** — DevTools Performance panel identify real bottlenecks.

## 🔗 Liên kết chéo

- Xem thêm: `18_dom-apis/02_dom-advanced/03_virtual-dom/` — Virtual DOM overview.
- Xem thêm: `18_dom-apis/02_dom-advanced/05_reactivity/` — Proxy reactivity so với VDOM.
- File tham khảo: `app.js`, `helper.js`, `index.html`, `style.css` trong folder `example1/`.
