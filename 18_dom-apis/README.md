# DOM APIs — Tổng quan — [Level: Beginner → Intermediate]

## 🔑 Khái niệm cốt lõi

**DOM (Document Object Model)** là biểu diễn cây mà trình duyệt dựng từ tài liệu HTML — mỗi thẻ HTML trở thành một **node**, mỗi node có quan hệ cha/con, và toàn bộ cây treo dưới gốc `document`. **DOM API** là tập Web API mà JavaScript dùng để *truy xuất và chỉnh sửa* cây này: tìm element (`getElementById`, `querySelector`), sửa nội dung (`textContent`, `innerHTML`), thêm/xóa node (`appendChild`, `remove`), gắn sự kiện (`addEventListener`)...

DOM không phải là JavaScript — nó là một **interface được trình duyệt cung cấp**. JavaScript chỉ là ngôn ngữ bạn dùng để gọi các method trên DOM API. Điều này có nghĩa: DOM API tồn tại độc lập với JS, và có thể được gọi từ WebAssembly, Python (via Brython), v.v.

### Node vs Element — phân biệt quan trọng
- **Node** là khái niệm cha (root của mọi thứ trong DOM). Có nhiều loại node:
  - `Element` (nodeType 1): thẻ HTML như `<div>`, `<p>`, `<span>`
  - `Text` (nodeType 3): văn bản bên trong element
  - `Comment` (nodeType 8): `<!-- comment -->`
  - `Document` (nodeType 9): gốc của cây DOM
  - `DocumentFragment` (nodeType 11): container tạm thời
- **Element** là tập con của Node — chỉ riêng thẻ HTML.
- API như `childNodes` (mọi node) khác `children` (chỉ element) — đây là bẫy phổ biến.

### Event Bubbling vs Capturing
Sự kiện lan theo hai pha:
- **Capturing (bắt)**: từ `window` đi xuống element đích — `addEventListener(type, fn, { capture: true })`.
- **Bubbling (nổi bọt)**: từ element đích đi ngược lên `window` — mặc định.
- `stopPropagation()` dừng đường lan truyền tại điểm gọi.

### Shadow DOM
Encapsulation — cây DOM riêng biệt bên trong một element, CSS/DOM cô lập khỏi trang. Nền tảng Web Components.

### Virtual DOM
Bản sao ảo trong bộ nhớ JS — khi state thay đổi, tạo cây ảo mới, **diff** với cây cũ, chỉ **patch** phần khác lên DOM thật. Tinh thần React.

### Reactivity
Hệ thống tự động đồng bộ data → UI — Proxy + re-render. Nền tảng Vue/Polymer.

Cấu trúc thư mục:
- `01_dom-basics/` — fundamentals: cây DOM, cách trình duyệt đọc HTML để dựng DOM/CSSOM/Render Tree.
- `02_dom-advanced/` — nâng cao phục vụ framework: DOM Manipulation, Shadow DOM, Virtual DOM, kết hợp các loại DOM, và **reactivity**.
- `03_events/` — sự kiện DOM: `addEventListener`, bubbling/capturing, preventDefault/stopPropagation, event delegation.

## 📐 Cấu trúc / Cú pháp

### Cây DOM cơ bản
```
document (Document Node, nodeType 9)
 └─ <html> (Element Node, nodeType 1)
      ├─ <head>
      │    └─ <title>...</title>
      └─ <body>
           ├─ <h1 id="title">Hello</h1>
           └─ <div class="box">
                ├─ Text node: "Content"
                └─ <span>Inline</span>
```

### Chọn phần tử — 5 phương thức chính
| Method | Trả về | Selector | Performance |
|---|---|---|---|
| `getElementById(id)` | Element hoặc null | id duy nhất | ⭐⭐⭐ nhanh nhất |
| `getElementsByClassName(name)` | HTMLCollection (live) | class | ⭐⭐ |
| `getElementsByTagName(tag)` | HTMLCollection (live) | tag name | ⭐⭐ |
| `querySelector(sel)` | Element hoặc null | CSS selector | ⭐ |
| `querySelectorAll(sel)` | NodeList (static) | CSS selector | ⭐ |

> **HTMLCollection** (live) — tự cập nhật khi DOM thay đổi.  
> **NodeList** (static) — snapshot tại thời điểm gọi, không đổi khi DOM thay đổi.

### Sửa nội dung
| Property | Mô tả | Parse HTML? |
|---|---|---|
| `textContent` | Raw text, giữ whitespace | ❌ Không |
| `innerText` | Rendered text, theo CSS | ❌ Không |
| `innerHTML` | HTML string, parse và render | ✅ Có |
| `outerHTML` | HTML bao gồm cả element | ✅ Có |

## ✅ Điểm mạnh

1. **Tương tác trực tiếp, linh hoạt** — sửa bất kỳ phần nào của trang mà không cần tải lại.
2. **Chuẩn Web API** — chạy trên mọi trình duyệt hiện đại, không cần framework.
3. **Nền tảng cho mọi UI framework** — React/Vue/Angular đều xoay quanh DOM (qua Virtual DOM / reactivity).
4. **Kiểm soát sự kiện mịn** — bubbling + delegation giảm số listener, dễ quản lý.
5. **Encapsulation có sẵn** qua Shadow DOM giúp build component tái sử dụng an toàn.
6. **Không cần thư viện** — DOM API có sẵn trong browser, zero dependency.
7. **Debug dễ** — DevTools Elements panel hiển thị DOM realtime, có thể edit trực tiếp.
8. **Performance可控** — biết reflow/threshold giúp tối ưu đúng chỗ.
9. **Accessibility built-in** — ARIA attributes qua DOM API giúp screen reader đọc đúng.
10. **Foundation cho Web Components** — Shadow DOM + Custom Elements = component system chuẩn.

## ⚠️ Bẫy thường gặp & Hạn chế

1. **Hiệu năng**: sửa DOM quá nhiều (trong vòng lặp) gây **reflow/render lại** → giật. Hãy batch changes hoặc dùng DocumentFragment.
2. **Cần kiểm tra tồn tại**: `querySelector` trả `null` nếu không tìm thấy — quên check dễ lỗi "Cannot read properties of null".
3. `nodeList` từ `querySelectorAll` **không phải array** — cần `Array.from` hoặc `[...nodes]` trước khi dùng `map/filter`.
4. **XSS qua innerHTML** — gán HTML từ user input chưa sanitize → hacker chèn `<script>`. Luôn dùng `textContent` cho user content.
5. **innerText vs textContent** — `innerText` trigger layout recalculation → chậm hơn; `textContent` nhanh hơn nhưng không xử lý CSS visibility.
6. **Event listener leak** — quên `removeEventListener` khi unmount → closure giữ reference → memory leak.
7. **classList vs className** — `className += ' new'` dễ duplicate; `classList.add()` an toàn hơn.
8. **Virtual DOM overhead** — với app nhỏ, sửa DOM trực tiếp nhanh hơn tạo/diff VNode.

## 💡 Khi nào dùng — Tình huống thực tế

1. **Ứng dụng nhỏ / prototype** — thao tác DOM trực tiếp nhanh hơn cài framework.
2. **Thêm tính năng nhỏ** vào trang có sẵn (tự động fill, validate form, đếm lượt click).
3. **Web Components** (Shadow DOM) — đóng gói UI tái sử dụng cho nhiều dự án.
4. **Toàn bộ ứng dụng phức tạp** — dùng framework (Virtual DOM + reactivity) để dễ bảo trì.
5. **Debug & optimize** — nắm DOM để đo Performance và sửa các vấn đề layout/reflow.
6. **Micro-interaction** — animation, hover effect, tooltip — DOM manipulation trực tiếp là đủ.
7. **Integration với third-party widget** — inject DOM vào trang có sẵn mà không cần framework.
8. **SEO-critical content** — server-rendered HTML + DOM enhancement (progressive enhancement).

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Tìm → đổi nội dung → gắn sự kiện
```js
// Tìm element
const btn = document.querySelector('#myButton');
if (!btn) { console.warn('Button not found'); }

// Đổi nội dung
btn.textContent = 'Đã click';

// Gắn sự kiện
btn.addEventListener('click', () => {
  console.log('clicked!');
  btn.style.backgroundColor = 'blue';
});
```

### Ví dụ 2: Node vs Element — hiểu khác biệt
```js
const el = document.querySelector('ul');
console.log(el.childNodes.length); // kể cả text node (xuống dòng, khoảng trắng)
console.log(el.children.length);    // chỉ đếm thẻ <li>
// childNodes: [text, li, text, li, text, li, text]
// children: [li, li, li]
```

### Ví dụ 3: Batch DOM changes — DocumentFragment
```js
const fragment = document.createDocumentFragment();
for (let i = 0; i < 1000; i++) {
  const li = document.createElement('li');
  li.textContent = `Item ${i}`;
  fragment.appendChild(li); // thêm vào fragment, chưa vào DOM
}
document.getElementById('list').appendChild(fragment);
// Chỉ 1 reflow thay vì 1000 reflows
```

### Ví dụ 4: Event delegation — 1 listener cho N items
```js
const list = document.querySelector('#task-list');
list.addEventListener('click', (e) => {
  if (e.target.tagName === 'LI') {
    e.target.remove(); // xóa task khi click vào LI
  }
});
// 1 listener ở cha lo được hàng nghìn con — thêm/xóa con tùy ý
```

### Ví dụ 5: CSS style qua JS
```js
const box = document.querySelector('.box');
// Inline style
box.style.width = '200px';
box.style.backgroundColor = 'coral';
box.style.transition = 'all 0.3s ease';

//toggleClass class-based (preferred)
box.classList.toggle('active');
box.classList.add('highlight', 'shadow');
box.classList.remove('inactive');
```

### Ví dụ 6: Safe innerHTML với escape
```js
function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str; // tự động escape
  return div.innerHTML;
}

function renderUsers(users) {
  const ul = document.querySelector('#user-list');
  ul.innerHTML = users.map(u =>
    `<li>${escapeHtml(u.name)} — ${escapeHtml(u.email)}</li>`
  ).join('');
}
```

### Ví dụ 7: Shadow DOM encapsulation
```js
const host = document.getElementById('widget');
const shadow = host.attachShadow({ mode: 'open' });
shadow.innerHTML = `
  <style>
    :host { display: block; padding: 16px; border: 1px solid #ccc; }
    .title { color: blue; }
  </style>
  <h2 class="title">Shadow Component</h2>
  <p>CSS global không ảnh hưởng đến nội dung này.</p>
`;
// Class 'title' trong shadow DOM không bị ảnh hưởng bởi CSS ngoài trang
```

### Ví dụ 8: Proxy reactivity cơ bản
```js
const state = { count: 0 };
const proxy = new Proxy(state, {
  set(target, key, value) {
    target[key] = value;
    document.getElementById('counter').textContent = value;
    return true;
  }
});
document.getElementById('btn').addEventListener('click', () => {
  proxy.count++; // UI tự cập nhật
});
```

## 🔬 So sánh với alternatives

| Cách tiếp cận | Ưu điểm | Nhược điểm | Phù hợp khi |
|---|---|---|---|
| **Vanilla DOM** | Không dependency, kiểm soát 100% | Bảo trì khó khi app lớn | App nhỏ, prototype |
| **Virtual DOM (React)** | Declarative, diff efficient | Overhead create+diff | App phức tạp, state nhiều |
| **Reactivity (Vue)** | Auto-update, fine-grained | Proxy overhead, hard debug | Data-driven UI |
| **Shadow DOM** | Encapsulation, reusable | Communication across boundary | Web Components, widgets |
| **Template strings** | Fast render | XSS risk, no diff | Static content injection |

## 📊 Performance & Best Practices

- **Batch DOM mutations**: dùng `DocumentFragment` hoặc `innerHTML` batch thay vì append từng node.
- **Avoid reflow in loop**: đọc `offsetWidth`/`offsetHeight` trong loop gây layout thrashing — batch reads trước, writes sau.
- **Prefer classList over style**: CSS class dựa vào engine optimization; inline style trigger reflow every change.
- **Use event delegation**: 1 listener ở parent thay vì N listeners ở children — giảm memory, tăng performance.
- **textContent > innerHTML for user data**: tránh XSS, faster (không parse HTML).
- **Debounce scroll/resize**: event fire nhiều lần → debounce 100-300ms để giảm work.
- **Lazy load DOM**: chỉ tạo element khi cần (virtual scroll, infinite scroll).
- **Use requestAnimationFrame**: cho animation DOM changes — sync với browser paint cycle.

## 🔗 Liên kết chéo

- Xem thêm: `18_dom-apis/01_dom-basics/` — 12 bài fundamentals DOM.
- Xem thêm: `18_dom-apis/01_dom-basics/01_f8-basic-dom/` — chuỗi 12 bài thực hành F8.
- Xem thêm: `18_dom-apis/01_dom-basics/02_how-browser-reads-html/` — rendering pipeline.
- Xem thêm: `18_dom-apis/02_dom-advanced/` — DOM manipulation, Shadow DOM, Virtual DOM.
- Xem thêm: `18_dom-apis/03_events/` — event system chi tiết.
- Xem thêm: `17_memory-management/` — DOM node và memory leak relationship.
- Xem thêm: `19_browser-devtools/` — debug DOM qua DevTools.
