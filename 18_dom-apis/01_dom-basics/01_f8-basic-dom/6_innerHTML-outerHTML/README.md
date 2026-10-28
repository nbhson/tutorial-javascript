# Bài 6 — innerHTML / outerHTML: Chèn HTML Động — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

| Thuộc tính | Mô tả |
|---|---|
| `innerHTML` | Đọc/giá trị HTML **bên trong** element (children) |
| `outerHTML` | Đọc/giá trị HTML **bao gồm cả chính element đó** |
| `insertAdjacentHTML(pos, html)` | Chèn HTML tại vị trí relative với element |

### insertAdjacentHTML positions
| Position | Ý nghĩa | Ví dụ |
|---|---|---|
| `"beforebegin"` | Trước element (sibling trước) | `<div>Trước</div><original/>` |
| `"afterbegin"` | Bên trong, trước child đầu tiên | `<original><div>Trước</div>...` |
| `"beforeend"` | Bên trong, sau child cuối cùng | `...<div>Sau</div></original>` |
| `"afterend"` | Sau element (sibling sau) | `<original/><div>Sau</div>` |

### innerHTML vs insertAdjacentHTML — điểm khác biệt then chốt
- **`innerHTML` thay thế toàn bộ children** → mất hết event listeners trên children.
- **`insertAdjacentHTML` chèn thêm mà không destroy children** → giữ nguyên event listeners cũ.

## 📐 Cấu trúc / Cú pháp

### innerHTML cơ bản
```js
const container = document.querySelector("#list");

// Ghi — thay thế toàn bộ children
container.innerHTML = `
  <li>Apple</li>
  <li>Banana</li>
  <li>Cherry</li>
`;

// Đọc — trả về HTML string của children
console.log(container.innerHTML);
// "<li>Apple</li><li>Banana</li><li>Cherry</li>"
```

### outerHTML — bao gồm cả element
```js
const box = document.querySelector("#box");

// Đọc
console.log(box.outerHTML);
// "<div id=\"box\" class=\"red\">Content</div>"

// Ghi — thay thế chính element bằng HTML mới
box.outerHTML = '<span id="box">Replaced!</span>';
// element #box gốc bị thay bằng <span> mới
// reference `box` vẫn trỏ đến element CŨ (bây giờ detached)
```

### insertAdjacentHTML — 4 vị trí
```js
const card = document.querySelector(".card");

// Trước element
card.insertAdjacentHTML("beforebegin", '<div class="before">Trước</div>');

// Bên trong, trước child đầu
card.insertAdjacentHTML("afterbegin", '<span class="inner-before">Trong-trước</span>');

// Bên trong, sau child cuối
card.insertAdjacentHTML("beforeend", '<span class="inner-after">Trong-sau</span>');

// Sau element
card.insertAdjacentHTML("afterend", '<div class="after">Sau</div>');
```

### render danh sách động
```js
function renderUsers(users) {
  const ul = document.querySelector("#user-list");
  ul.innerHTML = users.map(u => `
    <li>${escapeHtml(u.name)} — ${escapeHtml(u.email)}</li>
  `).join("");
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}
```

## ✅ Điểm mạnh

1. **Viết HTML phức tạp trong 1 dòng JavaScript** — template literal + innerHTML gọn hơn createElement nhiều lần.
2. **`insertAdjacentHTML` giữ event listener đã gắn sẵn** — khác innerHTML replace toàn bộ.
3. **Parser HTML native** — hiểu semantic tags tốt, auto-close tags, handle nesting đúng.
4. **Batch DOM insertion** — 1 lần parse + append thay vì N lần createElement + appendChild.
5. **Read + write cùng property** — `innerHTML` vừa đọc được HTML string, vừa ghi được.
6. **Template literal integration** — `${variable}` interpolation tự nhiên trong HTML string.
7. **outerHTML thay thế element hoàn toàn** — tiện cho component swap (modal open/close).

## ⚠️ Bẫy thường gặp & Hạn chế — QUAN TRỌNG

### Bẫy 1: XSS Vulnerability — NGUY HIỂM NHẤT
```js
const userInput = '<script>alert(1)</script>';

// ❌ NGUY HIỂM — parse và execute HTML từ user input
el.innerHTML = userInput;

// ✅ AN TOÀN — escape trước
el.innerHTML = escapeHtml(userInput);

// ✅ AN TOÀN hơn — dùng textContent thay innerHTML
el.textContent = userInput;
```

### Bẫy 2: innerHTML thay thế toàn bộ children → mất event listeners
```js
const list = document.querySelector('#list');
list.innerHTML = '<li>New item</li>';
// Tất cả <li> cũ và event listeners trên chúng bị destroy!
// Fix: dùng insertAdjacentHTML('beforeend', ...) thay vì innerHTML
```

### Bẫy 3: outerHTML thay thế chính element → DOM reference biến mất
```js
const box = document.querySelector('#box');
box.outerHTML = '<span>replaced</span>';
// box vẫn trỏ đến <div> CŨ (bây giờ detached từ DOM)
// querySelector('#box') giờ trả về <span> mới
console.log(box.tagName); // "DIV" — old element
console.log(document.querySelector('#box').tagName); // "SPAN" — new element
```

### Bẫy 4: innerHTML không self-closing cho SVG/MathML
```js
// ❌ Có thể gây vấn đề trong SVG context
svgContainer.innerHTML = '<circle cx="50" cy="50" r="40"/>';
// ✅ Nên dùng createElementNS cho SVG
const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
```

### Bẫy 5: Performance — innerHTML parse HTML string tốn CPU
```js
// ❌ Trong loop — chậm vì parse HTML mỗi iteration
for (let i = 0; i < 1000; i++) {
  el.innerHTML += `<li>Item ${i}</li>`; // DOM parse + reflow mỗi lần
}

// ✅ Tốt hơn — DocumentFragment
const fragment = document.createDocumentFragment();
for (let i = 0; i < 1000; i++) {
  const li = document.createElement('li');
  li.textContent = `Item ${i}`;
  fragment.appendChild(li);
}
el.appendChild(fragment); // 1 reflow
```

## 💡 Khi nào dùng — Tình huống thực tến

1. **Render template HTML động** — danh sách sản phẩm, comment, feed.
2. **Chèn nhiều element con cùng lúc** — hiệu năng tốt hơn append từng cái (1 parse vs N append).
3. **Thay thế component hoàn toàn** — modal, dialog, loading state swap.
4. **Quick HTML injection** — prototyping, bookmarklet, userscript.
5. **Server-rendered HTML chunk injection** — paste HTML from API response.
6. **Template-based UI generation** — JSON data → HTML string → innerHTML.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: innerHTML cơ bản
```js
const container = document.querySelector("#list");
container.innerHTML = `
  <li>Apple</li>
  <li>Banana</li>
  <li>Cherry</li>
`;
```

### Ví dụ 2: insertAdjacentHTML — giữ event listener
```js
const card = document.querySelector(".card");

// Thêm vào cuối children (giữ event listener cũ)
card.insertAdjacentHTML("beforeend", '<span class="badge">New</span>');

// Thêm trước element (không làm hỏng child)
card.insertAdjacentHTML("beforebegin", '<div class="before">Trước</div>');

// Sau element
card.insertAdjacentHTML("afterend", '<div class="after">Sau</div>');
```

### Ví dụ 3: Render danh sách động an toàn
```js
function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

function renderUsers(users) {
  const ul = document.querySelector("#user-list");
  ul.innerHTML = users.map(u => `
    <li>${escapeHtml(u.name)} — ${escapeHtml(u.email)}</li>
  `).join("");
}

renderUsers([
  { name: 'Nguyễn Văn A', email: 'a@example.com' },
  { name: 'Trần Thị B', email: 'b@example.com' }
]);
```

### Ví dụ 4: outerHTML thay thế element
```js
const box = document.querySelector("#box");
// Thay thế div#box bằng span mới
box.outerHTML = '<span id="box" class="replaced">Nội dung mới</span>';
// box reference vẫn trỏ old div (detached)
```

### Ví dụ 5: Loading state pattern
```js
async function loadData(url) {
  const container = document.querySelector('#content');
  
  // Loading state
  container.innerHTML = '<p class="loading">Đang tải...</p>';
  
  try {
    const res = await fetch(url);
    const data = await res.json();
    
    // Render data
    container.innerHTML = data.items.map(item => `
      <div class="item">
        <h3>${escapeHtml(item.title)}</h3>
        <p>${escapeHtml(item.description)}</p>
      </div>
    `).join('');
  } catch (err) {
    container.innerHTML = '<p class="error">Tải thất bại, vui lòng thử lại.</p>';
  }
}
```

### Ví dụ 6: Avoid innerHTML in loop — use DocumentFragment
```js
// ❌ BAD — innerHTML trong loop
const ul = document.querySelector('ul');
for (let i = 0; i < 1000; i++) {
  ul.innerHTML += `<li>Item ${i}</li>`; // 1000 lần parse + reflow
}

// ✅ GOOD — DocumentFragment
const ul = document.querySelector('ul');
const fragment = document.createDocumentFragment();
for (let i = 0; i < 1000; i++) {
  const li = document.createElement('li');
  li.textContent = `Item ${i}`;
  fragment.appendChild(li);
}
ul.appendChild(fragment); // 1 lần reflow
```

### Ví dụ 7: Template literal với data binding
```js
function renderProduct(product) {
  return `
    <article class="product-card">
      <img src="${escapeHtml(product.image)}" alt="${escapeHtml(product.name)}">
      <h3>${escapeHtml(product.name)}</h3>
      <p class="price">${product.price.toLocaleString('vi-VN')}₫</p>
      <button data-id="${product.id}">Thêm vào giỏ</button>
    </article>
  `;
}
```

## 🔬 So sánh với alternatives

| Method | Parse HTML? | Keeps listeners? | XSS Risk? | Speed |
|---|---|---|---|---|
| **innerHTML** | ✅ Có | ❌ Destroy children | ⚠️ Cao nếu user input | Trung bình |
| **outerHTML** | ✅ Có | ❌ Replace element | ⚠️ Cao nếu user input | Trung bình |
| **insertAdjacentHTML** | ✅ Có | ✅ Giữ children | ⚠️ Cao nếu user input | Nhanh |
| **createElement + appendChild** | ❌ Không | ✅ Giữ listeners | ✅ An toàn | Chậm hơn (N append) |
| **DocumentFragment** | ❌ Không | ✅ Giữ listeners | ✅ An toàn | Nhanh (batch) |
| **textContent** | ❌ Không | ✅ Giữ listeners | ✅ An toàn | Nhanh nhất |

## 📊 Performance & Best Practices

- **Escape user input luôn** — hàm `escapeHtml()` với `createElement+textContent` pattern.
- **Prefer `insertAdjacentHTML` over `innerHTML`** khi muốn giữ existing children/listeners.
- **Avoid `innerHTML +=` trong loop** — mỗi lần tạo mới HTML string + parse + reflow. Dùng DocumentFragment.
- **Batch với `innerHTML = join('')`** — 1 lần parse thay vì N lần append.
- **SVG/MathML**: dùng `createElementNS` thay vì innerHTML — browser handling khác.
- **Read innerHTML sparingly** — đọc innerHTML trigger style recalculation trong một số browser.
- **Use template `<template>` element** — `<template>` chứa HTML fragment, cloneNode(true) để insert — efficient + safe.

## 🔗 Liên kết chéo

- Xem thêm: `18_dom-apis/01_dom-basics/01_f8-basic-dom/5_text/` — textContent vs innerText.
- Xem thêm: `18_dom-apis/01_dom-basics/01_f8-basic-dom/7_node-property/` — node structure.
- Xem thêm: `18_dom-apis/02_dom-advanced/01_manipulation/example-1/` — DOM manipulation advanced.
- File tham khảo: `app.js`, `index.html` trong folder `6_innerHTML-outerHTML/`.
