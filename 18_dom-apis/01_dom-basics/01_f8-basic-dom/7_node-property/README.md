# Bài 7 — Node Property: Thuộc Tính Node Cơ Bản — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

Mỗi node trong DOM đều có các thuộc tính chung (kể cả element, text, comment node). Hiểu rõ các property này giúp bạn **duyệt cây DOM chính xác**, phân biệt được element con vs text node, và tránh bẫy `childNodes.length` lớn hơn mong đợi.

### Bảng node properties

| Property | Giá trị | Mô tả |
|---|---|---|
| `nodeType` | số | Loại node: 1=Element, 3=Text, 8=Comment, 9=Document, 11=DocumentFragment |
| `nodeName` | string | Tên node: `"DIV"`, `"#text"`, `"#comment"`, `"#document"` |
| `nodeValue` | string/null | Giá trị node: null với Element, text với Text/Comment |
| `parentNode` | Node | Node cha |
| `childNodes` | NodeList | Tất cả children (element + text + comment) |
| `children` | HTMLCollection | Chỉ element children (bỏ text/comment) |
| `firstChild` / `lastChild` | Node | Node đầu/cuối |
| `firstElementChild` / `lastElementChild` | Element | Element đầu/cuối |
| `nextSibling` / `previousSibling` | Node | Anh/em cùng cấp (any node type) |
| `nextElementSibling` / `previousElementSibling` | Element | Element anh/em cùng cấp |

### Bẫy phổ biến: childNodes vs children

```html
<ul>
  <li>One</li>
  <li>Two</li>
  <li>Three</li>
</ul>
```
```js
const ul = document.querySelector('ul');
console.log(ul.childNodes.length);   // 7 — kể cả text nodes (xuống dòng, khoảng trắng)
console.log(ul.children.length);     // 3 — chỉ 3 <li>

// childNodes content:
// [text("\n  "), li, text("\n  "), li, text("\n  "), li, text("\n")]
// children content:
// [li, li, li]
```

## 📐 Cấu trúc / Cú pháp

### Kiểm tra nodeType
```js
const el = document.querySelector("#app");

console.log(el.nodeType);       // 1 (Element)
console.log(el.nodeName);       // "DIV"
console.log(el.nodeValue);      // null (element không có nodeValue)

const textNode = el.firstChild;
console.log(textNode.nodeType); // 3 (Text)
console.log(textNode.nodeName); // "#text"
console.log(textNode.nodeValue); // "Hello "
```

### childNodes vs children — thực tế
```js
const ul = document.querySelector("ul");
console.log(ul.childNodes.length);  // 7 (bao gồm whitespace text nodes)
console.log(ul.children.length);    // 3 (chỉ 3 <li>)

// Duyệt chỉ element children
for (const child of ul.children) {
  console.log(child.tagName); // LI, LI, LI
}

// Duyệt tất cả nodes (kể text)
for (const child of ul.childNodes) {
  if (child.nodeType === Node.ELEMENT_NODE) {
    console.log('Element:', child.tagName);
  } else if (child.nodeType === Node.TEXT_NODE) {
    const text = child.textContent.trim();
    if (text) console.log('Text:', text);
  }
}
```

### Duyệt siblings
```js
const li = document.querySelector("li.active");

// Element siblings (bỏ text node)
console.log(li.previousElementSibling?.textContent);
console.log(li.nextElementSibling?.textContent);

// Any siblings (kể text node)
console.log(li.previousSibling?.nodeType); // 3 (text) hoặc 1 (element)
console.log(li.nextSibling?.nodeType);
```

### Filter text nodes hữu ích
```js
function getVisibleText(element) {
  return [...element.childNodes]
    .filter(node => node.nodeType === Node.TEXT_NODE && node.textContent.trim())
    .map(node => node.textContent.trim())
    .join(' ');
}

const text = getVisibleText(document.querySelector('p'));
```

## ✅ Điểm mạnh

1. **`nodeType` kiểm tra chính xác loại node** — phân biệt element/text/comment rõ ràng.
2. **`children` (chỉ element) thường tiện hơn `childNodes` (có cả text node trống)** — length chính xác số element con.
3. **`nodeType === 3` để lọc text node** — useful khi cần xử lý chỉ text content.
4. **`firstElementChild`/`lastElementChild`** — bỏ qua text node, lấy element thật.
5. **`nextElementSibling`/`previousElementSibling`** — duyệt element cùng cấp, bỏ whitespace.
6. **`parentNode` universal** — mọi node đều có cha (trừ Document).
7. **Properties read-only** — không thể gán lại, đảm bảo DOM integrity.

## ⚠️ Bẫy thường gặp & Hạn chế

1. **`childNodes` bao gồm text node** (dấu cách/newline giữa các thẻ) → length lớn hơn mong đợi. Đây là bẫy phổ biến nhất.
2. **`children` bỏ qua text node** → độ dài chính xác số element con — dùng khi chỉ quan tâm element.
3. **Thuộc tính này là đọc-only** — không thể gán lại `el.childNodes = ...`.
4. **`firstChild` có thể là text node** — whitespace/newline giữa tags tạo text node. Dùng `firstElementChild` để an toàn.
5. **`nodeValue` của element luôn null** — chỉ text/comment node có nodeValue.
6. **`childNodes` là NodeList static** — không tự update khi DOM đổi (khác `children` là HTMLCollection live).
7. **Whitespace text nodes** — browser tạo text node cho mỗi xuống dòng trong HTML source. Cần `.trim()` khi đọc text.

## 💡 Khi nào dùng — Tình huống thực tến

1. **Duyệt toàn bộ cây DOM** để sinh HTML/export — cần access cả text và element nodes.
2. **Tìm kiếm node theo điều kiện loại** — filter only ELEMENT_NODE, only TEXT_NODE.
3. **Xử lý comment nodes** — `nodeType === 8` để tìm và xử lý `<!-- comment -->`.
4. **Count chính xác element children** — dùng `children.length` thay vì `childNodes.length`.
5. **Traverse sibling elements** — `nextElementSibling` bỏ qua whitespace text nodes.
6. **DOM serialization** — convert DOM tree thành string, cần biết loại node.
7. **Custom DOM walker** — recursive traversal với nodeType check.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Kiểm tra nodeType cơ bản
```js
const el = document.querySelector("#app");

console.log(el.nodeType);       // 1 (Element)
console.log(el.nodeName);       // "DIV"
console.log(el.nodeValue);      // null (element không có nodeValue)

const textNode = el.firstChild;
console.log(textNode.nodeType); // 3 (Text)
console.log(textNode.nodeName); // "#text"
console.log(textNode.nodeValue); // "Hello "
```

### Ví dụ 2: childNodes vs children
```js
const ul = document.querySelector("ul");
console.log(ul.childNodes.length);  // 7 (bao gồm whitespace text nodes)
console.log(ul.children.length);    // 3 (chỉ 3 <li>)

for (const child of ul.children) {
  console.log(child.tagName); // LI, LI, LI
}

// Đếm số text nodes thực sự có content
const textNodes = [...ul.childNodes].filter(
  n => n.nodeType === Node.TEXT_NODE && n.textContent.trim()
);
console.log('Text nodes with content:', textNodes.length);
```

### Ví dụ 3: Duyệt siblings an toàn
```js
const li = document.querySelector("li.active");

// Element siblings — bỏ qua whitespace
console.log(li.previousElementSibling?.tagName); // "LI" hoặc undefined
console.log(li.nextElementSibling?.tagName);     // "LI" hoặc undefined

// Any siblings — kể text node
console.log(li.previousSibling?.nodeType); // 3 (text) hoặc 1 (element)
console.log(li.nextSibling?.nodeType);
```

### Ví dụ 4: Recursive DOM walker
```js
function walkTree(node, callback, depth = 0) {
  callback(node, depth);
  for (const child of node.childNodes) {
    if (child.nodeType === Node.ELEMENT_NODE) {
      walkTree(child, callback, depth + 1);
    }
  }
}

walkTree(document.body, (node, depth) => {
  const indent = '  '.repeat(depth);
  if (node.nodeType === Node.ELEMENT_NODE) {
    console.log(`${indent}<${node.tagName.toLowerCase()}>`);
  } else if (node.nodeType === Node.TEXT_NODE && node.textContent.trim()) {
    console.log(`${indent}"${node.textContent.trim()}"`);
  }
});
```

### Ví dụ 5: Tìm và xử lý comment nodes
```js
function findComments(node, results = []) {
  if (node.nodeType === Node.COMMENT_NODE) {
    results.push({ text: node.nodeValue, parent: node.parentNode });
  }
  for (const child of node.childNodes) {
    findComments(child, results);
  }
  return results;
}

const comments = findComments(document.body);
comments.forEach(c => console.log('Comment:', c.text, 'in', c.parent.tagName));
```

### Ví dụ 6: Extract all text (ignore tags)
```js
function extractText(node) {
  if (node.nodeType === Node.TEXT_NODE) return node.textContent;
  if (node.nodeType !== Node.ELEMENT_NODE) return '';
  return [...node.childNodes].map(extractText).join('');
}

const pureText = extractText(document.querySelector('article'));
console.log(pureText); // "Hello World This is a paragraph"
```

### Ví dụ 7: Node relationship chain
```js
const li = document.querySelector('ul li:nth-child(2)');

console.log('Tag:', li.tagName);           // "LI"
console.log('Parent tag:', li.parentNode.tagName); // "UL"
console.log('Grandparent:', li.parentElement.tagName); // "BODY"
console.log('First sibling tag:', li.previousElementSibling?.tagName);
console.log('Last sibling tag:', li.nextElementSibling?.tagName);
console.log('Document root:', li.ownerDocument === document); // true
```

## 🔬 So sánh với alternatives

| Approach | Access | Includes text? | Live? | Use case |
|---|---|---|---|---|
| **childNodes** | All nodes | ✅ Có | ❌ Static | Full tree traversal |
| **children** | Elements only | ❌ Không | ✅ Live | Count/loop elements |
| **firstChild** | Any node | ✅ Có | ❌ Static | Find first node |
| **firstElementChild** | Element only | ❌ Không | ❌ Static | Find first element |
| **querySelector** | CSS selector | N/A | ❌ Static | Targeted selection |

## 📊 Performance & Best Practices

- **Prefer `children` over `childNodes`** khi chỉ cần element — tránh xử lý whitespace text nodes.
- **Use `firstElementChild` thay `firstChild`** — tránh text node whitespace trap.
- **`.trim()` text nodes** — whitespace text nodes thường empty sau trim.
- **Cache `childNodes` length** — không gọi lại nhiều lần trong loop.
- **NodeList là iterable** — dùng `for...of` thay vì `forEach` (NodeList không có forEach trong older browsers).
- **Avoid deep recursive traversal** — cây DOM sâu > 10 level có thể stack overflow.

## 🔗 Liên kết chéo

- Xem thêm: `18_dom-apis/01_dom-basics/01_f8-basic-dom/3_element/` — element selection.
- Xem thêm: `18_dom-apis/01_dom-basics/01_f8-basic-dom/5_text/` — text content properties.
- Xem thêm: `18_dom-apis/01_dom-basics/01_f8-basic-dom/6_innerHTML-outerHTML/` — HTML manipulation.
- File tham khảo: `app.js`, `index.html` trong folder `7_node-property/`.
