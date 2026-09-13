# Bài 7 — Node Property: Thuộc Tính Node Cơ Bản

## 🔑 Khái niệm

Mỗi node trong DOM đều có các thuộc tính chung (kể cả element, text, comment):

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
| `nextSibling` / `previousSibling` | Node | Anh/em cùng cấp |
| `nextElementSibling` / `previousElementSibling` | Element | Element anh/em |

## ✅ Điểm mạnh
- `nodeType` kiểm tra chính xác loại node
- `children` (chỉ element) thường tiện hơn `childNodes` (có cả text node trống)
- `nodeType === 3` để lọc text node

## ⚠️ Lưu ý
- `childNodes` bao gồm **text node** (dấu cách/newline giữa các thẻ) → length lớn hơn mong đợi
- `children` bỏ qua text node → độ dài chính xác số element con
- Thuộc tính này là **đọc-only**, không thể gán lại

## 💡 Khi nào dùng
- Duyệt toàn bộ cây DOM để sinh HTML/export
- Tìm kiếm node theo điều kiện loại
- Xử lý comment nodes

## 🎯 Ví dụ minh họa

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

### childNodes vs children
```js
const ul = document.querySelector("ul");
console.log(ul.childNodes.length);  // 7 (bao gồm whitespace text nodes)
console.log(ul.children.length);    // 3 (chỉ 3 <li>)

for (const child of ul.children) {
  console.log(child.tagName); // LI, LI, LI
}
```

### Duyệt siblings
```js
const li = document.querySelector("li.active");
console.log(li.previousElementSibling?.textContent);
console.log(li.nextElementSibling?.textContent);
```

## 📚 Tham khảo & Bài tập
- File: `app.js`, `index.html` trong folder `7_node-property/`
- Thực hành: đếm số text node và element node trong một section
- Câu hỏi: Tại sao `childNodes.length` thường lớn hơn `children.length`?
