# Virtual DOM — Cập Nhật DOM Tối Thiểu — [Level: Intermediate]

## 🔑 Khái niệm cốt lõi

Thao tác DOM thủ công rất lộn xộn: khó theo dõi trạng thái trước/sau, và cập nhật toàn bộ DOM mỗi lần state đổi khiến ứng dụng chậm. **Virtual DOM** giải quyết bằng cách: bạn **mô tả lại toàn bộ giao diện** mỗi khi state thay đổi (viết code như đang "tạo lại cả DOM"), nhưng thay vì đụng DOM thật, bạn chỉ tạo một **cây ảo (VTree / VNode)** trong bộ nhớ. Một lớp trung gian (thư viện `virtual-dom`, hay chính React) sẽ:

1. **Tạo Virtual DOM mới** từ state hiện tại.
2. **Diff** cây mới với cây cũ → tìm **những phần khác biệt** (patch list).
3. **Patch**: chỉ cập nhật đúng các phần đổi lên **DOM thực tế** — giảm tối đa thao tác trực tiếp và render lại toàn trang.

### Thuật toán Diff — vì sao nhanh?

Thuật toán diff cây cây với độ phức tạp O(n³) về lý thuyết, nhưng React và các library dùng **heuristic O(n)**:
- **Chỉ so sánh cùng level** — không diff cross-level (element A không so với element B ở level khác).
- **Type different → replace whole subtree** — nếu tag khác nhau (div → span), replace toàn bộ.
- **Key-based list diff** — dùng `key` prop để identify individual items, tránh reorder diff lãng phí.
- **Same type, different props → update props only** — không recreate element.

Thư mục này có `example1/` — một **mini virtual-dom tự viết**:
- `helper.js`: `createVNode(tag, props, children)` tạo node ảo; `render(vNode, container)` giữ `container._vNode` để diff; `createElementFromVNode` chuyển VNode → DOM thật (nhận biết text/event bắt đầu với `on`); `diff(oldVNode, newVNode)` so sánh text con và sinh patch `SET_PROP`; `patch/applyPatch` áp lên đúng node.
- `app.js`: state `{ counter }`, hàm `updateCounter()` tăng counter rồi `renderApp()` dựng lại VNode — nhờ diff, chỗ bị sửa chính là text của thẻ `<p>` counter.

## 📐 Cấu trúc / Cú pháp

### VNode (Virtual Node) structure
```js
// VNode là plain JavaScript object
const vNode = {
  tag: 'div',
  props: { className: 'container', id: 'app' },
  children: [
    { tag: 'h1', props: {}, children: ['Virtual DOM Demo'] },
    { tag: 'p', props: {}, children: ['Counter: 0'] },
    { tag: 'button', props: { onclick: increment }, children: ['Increment'] }
  ]
};
```

### Hàm cốt lõi
```js
// Tạo VNode
function createVNode(tag, props, children) {
  return { tag, props: props || {}, children: children || [] };
}

// Render VNode → actual DOM
function render(vNode, container) {
  const oldVNode = container._vNode || null;
  const patch = diff(oldVNode, vNode);
  applyPatch(container, patch);
  container._vNode = vNode; // cache for next diff
}

// Diff two VNodes
function diff(oldVNode, newVNode) {
  if (!oldVNode) return { type: 'MOUNT', element: createElementFromVNode(newVNode) };
  if (oldVNode.tag !== newVNode.tag) return { type: 'REPLACE', newElement: createElementFromVNode(newVNode) };
  // same tag — diff props and children
  const patches = [];
  // diff props
  // diff children recursively
  return patches;
}
```

### State → VNode → Render pattern
```js
let state = { counter: 0 };

function renderApp() {
  const vNode = createVNode('div', null, [
    createVNode('h1', null, ['Virtual DOM']),
    createVNode('p', null, [`Counter: ${state.counter}`]),
    createVNode('button', { onclick: updateCounter }, ['Increment'])
  ]);
  render(vNode, document.getElementById('app'));
}

function updateCounter() {
  state.counter += 1;
  renderApp(); // diff + patch, chỉ sửa text counter
}
```

## ✅ Điểm mạnh

1. **Hiệu năng** — chỉ sửa phần thay đổi thay vì rebuild toàn bộ DOM → ít layout/paint, mượt hơn.
2. **Viết kiểu declarative** — tư duy "UI = f(state)" — dễ đọc, dễ test, dễ reason về UI.
3. **Quản lý state dễ** — nhờ tách mô hình dữ liệu khỏi thao tác DOM.
4. **Nền tảng React/Vue** — hiểu diff → hiểu bản năng tối ưu key trong `list.map`.
5. **Batch cập nhật** — framework gom nhiều thay đổi state thành một lần render.
6. **Predictable updates** — cùng state → cùng VNode → cùng DOM output (pure function).
7. **Cross-browser abstraction** — developer không lo browser DOM quirks.
8. **Server-side rendering** — VNode tree có thể render thành HTML string trên server.

## ⚠️ Bẫy thường gặp & Hạn chế

1. **Overhead thêm** — tạo + diff cây ảo tốn CPU/memory — với UI nhỏ, sửa DOM trực tiếp nhanh hơn.
2. **Diff không phải "miễn phí"** — cây càng lớn, so sánh càng tốn; sai `key` làm React render lại nhầm nhánh.
3. **Không thay được quản lý state** — vẫn cần công cụ khác (useState, Vuex, domain state) phía trên.
4. **Code vanilla kiểu này khó đọc** hơn so với tách framework ra cho đúng bài toán.
5. **Key prop quan trọng** — list diff tanpa stable key → performance degradation + wrong updates.
6. **False sharing** — VNode recreate unnecessary nếu state object reference change (React shallow compare).
7. **Debug abstraction leak** — khó trace từ DOM behavior ngược về VNode code.

## 💡 Khi nào dùng — Tình huống thực tến

1. **Ứng dụng có nhiều trạng thái động**, render lại liên tục trên nhiều thành phần.
2. **Danh sách lớn** cần cập nhật từng dòng — khai báo `key` ổn định để diff chính xác.
3. **Cần tách biết "dữ liệu → UI"** rõ ràng — model truyền thẳng vào render function.
4. **Khi build multi-component app** — mỗi component trả về VNode, framework chỉ patch phần đổi.
5. **Muốn tự viết một renderer tí hon** — chính là `example1/helper.js`.
6. **Learning framework internals** — hiểu Virtual DOM giúp hiểu cơ chế hoạt động của React/Vue.
7. **Progressive enhancement** — bắt đầu với vanilla, gradually add virtual layer.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Mini Virtual DOM — State & Render (file `app.js`)
```js
let state = { counter: 0 };

function updateCounter() {
  state.counter += 1;
  renderApp();
}

function createAppVNode() {
  return createVNode('div', null, [
    createVNode('h1', null, ['Virtual DOM']),
    createVNode('p', null, [`Counter: ${state.counter}`]),
    createVNode('button', { onclick: updateCounter }, ['Increment'])
  ]);
}

function renderApp() {
  render(createAppVNode(), document.getElementById('app'));
}

renderApp(); // lần đầu: tạo toàn bộ DOM
// Mỗi lần bấm button: chỉ patch text của <p> counter
```

### Ví dụ 2: Diff algorithm cơ bản
```js
function diff(oldVNode, newVNode) {
  if (!oldVNode) return [{ type: 'MOUNT', element: createElementFromVNode(newVNode) }];
  if (oldVNode.tag !== newVNode.tag) {
    const newEl = createElementFromVNode(newVNode);
    return [{ type: 'REPLACE', element: newEl }];
  }
  
  const patches = [];
  
  // Diff props
  const propPatches = diffProps(oldVNode.props, newVNode.props);
  patches.push(...propPatches);
  
  // Diff children
  const childPatches = diffChildren(oldVNode.children, newVNode.children);
  patches.push(...childPatches);
  
  return patches;
}
```

### Ví dụ 3: Key-based list diff
```js
function diffChildren(oldChildren, newChildren) {
  const patches = [];
  const keyMap = new Map();
  
  oldChildren.forEach((child, index) => {
    if (child.key) keyMap.set(child.key, index);
  });
  
  newChildren.forEach((newChild, index) => {
    const oldIndex = keyMap.get(newChild.key);
    if (oldIndex === undefined) {
      patches.push({ type: 'INSERT', index, child: newChild });
    } else if (oldIndex !== index) {
      patches.push({ type: 'MOVE', from: oldIndex, to: index });
    } else {
      // same position — diff recursively
      patches.push(...diff(oldChildren[oldIndex], newChild));
    }
  });
  
  return patches;
}
```

### Ví dụ 4: createElementFromVNode
```js
function createElementFromVNode(vNode) {
  if (typeof vNode === 'string' || typeof vNode === 'number') {
    return document.createTextNode(String(vNode));
  }
  
  const el = document.createElement(vNode.tag);
  
  // Set props
  Object.entries(vNode.props || {}).forEach(([key, value]) => {
    if (key.startsWith('on')) {
      el.addEventListener(key.slice(2).toLowerCase(), value);
    } else {
      el.setAttribute(key, value);
    }
  });
  
  // Set children
  vNode.children.forEach(child => {
    el.appendChild(createElementFromVNode(child));
  });
  
  return el;
}
```

### Ví dụ 5: applyPatch
```js
function applyPatch(container, patches) {
  patches.forEach(patch => {
    switch (patch.type) {
      case 'MOUNT':
        container.appendChild(patch.element);
        break;
      case 'REPLACE':
        container.replaceChild(patch.element, container.firstChild);
        break;
      case 'SET_TEXT':
        patch.element.textContent = patch.text;
        break;
      case 'SET_PROP':
        patch.element.setAttribute(patch.prop, patch.value);
        break;
    }
  });
}
```

### Ví dụ 6: Full example — counter app
```js
// helper.js
function createVNode(tag, props, children) {
  return { tag, props: props || {}, children: children || [] };
}

function render(vNode, container) {
  const oldVNode = container._vNode || null;
  const patches = diff(oldVNode, vNode);
  applyPatches(container, patches);
  container._vNode = vNode;
}

function diff(oldVNode, newVNode) {
  if (!oldVNode) return [{ type: 'MOUNT', element: createElement(newVNode) }];
  if (oldVNode.tag !== newVNode.tag) {
    return [{ type: 'REPLACE', element: createElement(newVNode) }];
  }
  const patches = [];
  if (oldVNode.children.length !== newVNode.children.length) {
    patches.push({ type: 'REPLACE', element: createElement(newVNode) });
  } else {
    newVNode.children.forEach((child, i) => {
      patches.push(...diff(oldVNode.children[i], child));
    });
  }
  return patches;
}

function createElement(vNode) {
  if (typeof vNode === 'string') return document.createTextNode(vNode);
  const el = document.createElement(vNode.tag);
  Object.entries(vNode.props || {}).forEach(([k, v]) => {
    if (k.startsWith('on')) el.addEventListener(k.slice(2).toLowerCase(), v);
    else el.setAttribute(k, v);
  });
  vNode.children.forEach(c => el.appendChild(createElement(c)));
  return el;
}

function applyPatches(container, patches) {
  patches.forEach(patch => {
    if (patch.type === 'MOUNT') container.appendChild(patch.element);
    else if (patch.type === 'REPLACE') {
      container.textContent = '';
      container.appendChild(patch.element);
    }
  });
}

// app.js
let count = 0;
function render() {
  const vnode = createVNode('div', null, [
    createVNode('h1', null, ['Counter App']),
    createVNode('p', null, [`Count: ${count}`]),
    createVNode('button', { onclick: () => { count++; render(); } }, ['Increment'])
  ]);
  render(vnode, document.getElementById('app'));
}
render();
```

## 🔬 So sánh với alternatives

| Approach | Update Strategy | Performance | Complexity | Use case |
|---|---|---|---|---|
| **Direct DOM** | Manual patch | ⭐⭐⭐ Fastest (small UI) | Thấp | App nhỏ |
| **Virtual DOM** | Diff + patch | ⭐⭐ Medium | Trung bình | Complex SPAs |
| **Fine-grained reactivity** | Dependency tracking | ⭐⭐⭐ Fast | Cao | Vue 3, Solid |
| **Server-side render** | HTML string | ⭐⭐⭐ Best FCP | Cao | SEO-critical |
| **Template strings** | Full replace | ⭐⭐ Medium | Thấp | Simple lists |

## 📊 Performance & Best Practices

- **Stable keys in lists** — dùng index chỉ khi list không reorder; dùng unique ID tốt hơn.
- **Avoid unnecessary re-renders** — memoize VNode creation khi state không đổi.
- **Batch state updates** — gom nhiều state changes thành một render cycle.
- **Lazy render** — chỉ render phần visible (virtual scrolling).
- **Key prop importance** — thiếu key → worst-case O(n²) diff; có key → O(n).
- **Don't over-optimize** — với UI nhỏ, direct DOM manipulation có thể nhanh hơn VDOM overhead.
- **Measure real impact** — dùng Performance panel để verify diff savings thực tế.

## 🔗 Liên kết chéo

- Xem thêm: `18_dom-apis/02_dom-advanced/03_virtual-dom/example1/` — nguyên lý hoạt động chi tiết.
- Xem thêm: `18_dom-apis/02_dom-advanced/01_manipulation/` — DOM manipulation basics.
- Xem thêm: `18_dom-apis/02_dom-advanced/05_reactivity/` — Proxy reactivity so với Virtual DOM.
- Xem thêm: `17_memory-management/04_meta-programming/` — Proxy foundation.
- Tham khảo thư viện: <https://github.com/Matt-Esch/virtual-dom>.
