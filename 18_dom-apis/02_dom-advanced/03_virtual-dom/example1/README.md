# Virtual DOM — Nguyên Lý Hoạt Động

## 🔑 Khái niệm

**Virtual DOM (VDOM)** là bản sao trong bộ nhớ JS của DOM thật. Khi state thay đổi:
1. Tạo VDOM tree mới từ state (render function)
2. **Diffing**: so sánh VDOM cũ vs mới (reconciliation)
3. **Patch**: áp dụng thay đổi nhỏ nhất lên DOM thật

React, Preact, Inferno… đều dùng cơ chế này.

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

## ✅ Điểm mạnh
- **Batch updates**: nhiều state change hợp nhất thành 1 DOM update
- **Cross-browser**: abstraction layer, developer không lo browser quirks
- **Predictable**: mỗi lần render cùng state → cùng output (pure function)
- **Optimized diff**: O(n) algorithm thay vì O(n³) brute force

## ⚠️ Lưu ý
- VDOM overhead: bộ nhớ + CPU cho diffing — không free
- Không phải lúc nào cũng nhanh hơn DOM trực tiếp (simple app)
- React 18+ có concurrent mode giảm bớt issue này
- Framework không dùng VDOM (Solid, Svelte, Vue 3 with signals) đang lên ngôi

## 💡 Khi nào dùng
- App có UI phức tạp, nhiều component re-render
- State change liên tục (dashboard, game, chat)
- Cần declarative UI (describe what, not how)

## 🎯 Ví dụ minh họa

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
//每次 setCount → React diff + patch, không re-render toàn bộ DOM
```

## 📚 Tham khảo & Bài tập
- File: `app.js`, `helper.js`, `index.html`, `style.css` trong folder `example1/`
- Thực hành: viết hàm `render(vnode)` đơn giản, không diff
- Câu hỏi: Tại sao React key quan trọng trong list diffing?
