# DOM APIs — Cơ bản — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

Phần này xây nền móng cho toàn bộ DOM. Gồm hai nhóm chính:

### 01_f8-basic-dom — Chuỗi 12 bài thực hành (theo lộ trình F8)
Đi từ khái niệm đến nâng cao về DOM, mỗi thư mục con là một bài với code mở sẵn:

| # | Thư mục | Chủ đề | File chính |
|---|---|---|---|
| 1 | `1_dom-api` | HTML DOM là gì, DOM API là gì | `1.Html-Dom-Dom-Api.js` |
| 2 | `2_dom-object` | `document` — object gốc của DOM | `2.Dom-object.js` |
| 3 | `3_element` | Chọn element (id/class/tag/selector) | `app.js` + `index.html` |
| 4 | `4_attribute` | Thao tác attribute (`set/getAttribute`) | `app.js` + `index.html` |
| 5 | `5_text` | `innerText` vs `textContent` | `app.js` + `index.html` |
| 6 | `6_innerHTML-outerHTML` | Sửa nội dung / thẻ bao ngoài | `app.js` + `index.html` |
| 7 | `7_node-property` | Node property (`childNodes`, `children`, `sibling`...) | `app.js` + `index.html` |
| 8 | `8_dom-css-style` | Đổi style qua `element.style`, `Object.assign` | `app.js` + `index.html` |
| 9 | `9_class-property` | `classList.add/remove/contains/toggle` | `app.js` + `index.html` |
| 10 | `10_dom-event` | Gán sự kiện (`onclick`), object `MouseEvent` | `app.js` + `index.html` |
| 11 | `11_PreventDefault-StopPropagation` | Chặn hành vi mặc định & chặn nổi bọt | `app.js` + `index.html` |
| 12 | `12_EventListener` | `addEventListener`/`removeEventListener` | `app.js` + `index.html` |

### 02_how-browser-reads-html — Rendering Pipeline
Trình duyệt nhận HTTP → parse HTML → dựng **DOM Tree + CSSOM** → kết hợp thành **Render Tree** → layout → paint → JS execution → `load`. Kèm nhiều ảnh minh họa (`DOM.png`, `HTML-Parsing.png`, `Painting-Phase*.png`, `node-structure-in-dom.png`).

Mấu chốt cần nắm ở phần cơ bản:
- **DOM là gì**: mô hình cây do W3C định nghĩa; **DOM API** là tập Web API truy xuất/chỉnh sửa cây đó.
- **Node vs Element**: node bao gồm element, text, comment; element chỉ là thẻ HTML.
- Cách **chọn phần tử**: `getElementById` (nhanh nhất), `querySelector`/`querySelectorAll` (phổ biến nhất).
- Cách **sửa nội dung**: `textContent` (an toàn), `innerHTML` (linh hoạt nhưng XSS risk).
- **Node property**: `childNodes` (kể text node), `children` (chỉ element).

## 📐 Cấu trúc / Cú pháp

### Chọn phần tử
```js
// Bằng ID (nhanh nhất — O(1))
const el = document.getElementById('myId');

// Bằng CSS selector (linh hoạt nhất)
const el = document.querySelector('.class');           // phần tử đầu tiên
const els = document.querySelectorAll('div.active');   // tất cả → NodeList

// Bằng tag/class (HTMLCollection — live)
const divs = document.getElementsByTagName('div');
const items = document.getElementsByClassName('item');
```

### Sửa nội dung
```js
// Text (an toàn, không parse HTML)
el.textContent = 'Hello <b>World</b>'; // hiển thị literal "<b>World</b>"

// HTML (parse và render tag)
el.innerHTML = '<b>Hello</b> World';   // in đậm "Hello"

// Read text
console.log(el.textContent);
console.log(el.innerText);  // theo CSS visibility (chậm hơn textContent)
```

### Node properties
```js
const box = document.querySelector('.box');
box.childNodes.length;    // kể cả text node (whitespace giữa tags)
box.children.length;      // chỉ element children
box.firstChild;           // node đầu tiên (có thể là text node)
box.firstElementChild;    // element đầu tiên (bỏ text node)
box.parentNode;           // cha
box.nextElementSibling;   // anh/em element cùng cấp
```

### Style và Class
```js
// Inline style (camelCase)
el.style.color = 'red';
el.style.fontSize = '16px';
Object.assign(el.style, { color: 'blue', fontSize: '20px' });

// Class list (an toàn, không duplicate)
el.classList.add('active', 'highlight');
el.classList.remove('inactive');
el.classList.toggle('open');
el.classList.contains('active'); // boolean
el.classList.replace('old', 'new');
```

### Sự kiện
```js
// Property assignment (chỉ 1 handler)
el.onclick = function(e) { console.log(e); };

// addEventListener (nhiều handler, có thể gỡ)
el.addEventListener('click', handler, { capture: false, once: false, passive: false });
el.removeEventListener('click', handler);
```

## ✅ Điểm mạnh

1. **Học theo cấp độ** — 12 bước từ lý thuyết tới sự kiện, đúng chuỗi phụ thuộc kiến thức.
2. **Thực hành ngay** — mỗi bài có `app.js`/`index.html` sẵn, chạy trong browser để xem kết quả.
3. **Bắt nhịp diff cho framework** — hiểu render pipeline trước khi học React/Vue.
4. **Kiến thức tổ chức theo mảng** — selector, attribute, text, style, class, event — đúng thứ tự hay dùng.
5. **Ghi chú ngay trong code** — các comment giải thích cặn kẽ từng dòng, tiện tự học.
6. **Zero setup** — mở `index.html` trong browser là chạy được, không cần install gì.
7. **Foundation cho advanced** — `02_dom-advanced` và `03_events` đều dựa trên kiến thức phần này.
8. **Interview-ready** — 12 chủ đề này là câu hỏi thường gặp trong phỏng vấn frontend.

## ⚠️ Bẫy thường gặp & Hạn chế

1. **`innerHTML` với dữ liệu người dùng gốc = lỗ hổng XSS** — nên dùng `textContent` khi chỉ cần text.
2. **`querySelectorAll` trả NodeList tĩnh, không phải array** — muốn dùng `map` cần `Array.from` hoặc `[...nodes]`.
3. **`innerText` (theo những gì hiển thị) khác `textContent` (theo nguồn HTML)** — dễ nhầm. `innerText` trigger layout recalculation → chậm hơn.
4. **`classList.toggle/add/remove` an toàn hơn sửa trực tiếp `className`** khi có nhiều class — tránh duplicate.
5. **`getElementsByClassName`/`getElementsByTagName` trả HTMLCollection sống** — tự cập nhật khi DOM đổi; `querySelectorAll` trả NodeList tĩnh.
6. **`setAttribute(name, value)` mới cho phép attribute không chuẩn** — các thuộc tính hợp lệ thì buộc qua setter trực tiếp (`link.href = ...`).
7. **Quên `event.stopPropagation()`** trong bài 11 khiến sự kiện vẫn lan lên phần tử cha.
8. **`onclick` chỉ giữ được 1 handler** — nhiều handler cần `addEventListener`.

## 💡 Khi nào dùng — Tình huống thực tế

1. **Bạn mới học DOM** hoặc cần ôn lại nền tảng trước khi làm UI phức tạp.
2. **Cần chọn/sửa phần tử tự động trong trang** — thêm class, đổi text, thay attribute.
3. **Muốn hiểu vì sao trình duyệt vẽ lại trang** khi bạn sửa DOM (render pipeline).
4. **Làm foundation để hiểu các khái niệm nâng cao** ở `02_dom-advanced` (Shadow DOM, Virtual DOM, reactivity).
5. **Viết script tự động hóa trang** — greasemonkey/userjs style.
6. **Prototype nhanh** tính năng UI mà không muốn cài framework.
7. **Debug issue CSS/layout** — inspect DOM tree qua DevTools Elements panel.
8. **Tích hợp third-party widget** — inject DOM vào trang có sẵn.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Chọn + đổi text (bài 5)
```js
const heading = document.querySelector('h1');
console.log(heading.innerText);      // text hiển thị (theo CSS)
heading.innerText = '<i>Mới</i>';    // nhập literal text, không render tag
// So sánh: heading.innerHTML = '<i>Mới</i>' → in đậm "Mới"
```

### Ví dụ 2: Node vs Element (bài 7)
```js
const box = document.querySelector('.box');
box.childNodes.length;   // kể cả text node (xuống dòng, khoảng trắng)
box.children.length;     // chỉ element
for (const child of box.children) {
  console.log(child.tagName); // chỉ in tag name của element children
}
```

### Ví dụ 3: Sự kiện qua property (bài 10)
```js
const h = document.querySelector('h1').nextElementSibling;
h.onclick = function (e) {
  console.log(e);                  // MouseEvent đầy đủ thông tin
  h.style.color = 'red';
};
// ⚠️ Chỉ đặt được 1 onclick — gán lần sau ghi đè lần trước
```

### Ví dụ 4: PreventDefault (bài 11)
```js
for (const a of document.links) {
  a.onclick = (e) => {
    if (e.target.href !== "http://facebook.com/") {
      e.preventDefault(); // chặn navigate mặc định
    }
  };
}
// Link đến facebook.com vẫn hoạt động, các link khác bị chặn
```

### Ví dụ 5: Multiple listeners + gỡ listener (bài 12)
```js
function viec1() { console.log("Việc 1"); }
const btn = document.querySelector('button');
btn.addEventListener("click", viec1);
btn.addEventListener("click", () => console.log("Việc 2"));
// Bây giờ click vào btn → in "Việc 1" rồi "Việc 2"
setTimeout(() => btn.removeEventListener("click", viec1), 5000);
// Sau 5 giây → chỉ còn "Việc 2"
```

### Ví dụ 6: Batch DOM change với DocumentFragment
```js
const ul = document.querySelector('#list');
const fragment = document.createDocumentFragment();
for (let i = 0; i < 100; i++) {
  const li = document.createElement('li');
  li.textContent = `Item ${i}`;
  fragment.appendChild(li);
}
ul.appendChild(fragment); // 1 reflow thay vì 100
```

### Ví dụ 7: Event delegation pattern
```js
const table = document.querySelector('table');
table.addEventListener('click', (e) => {
  const cell = e.target.closest('td');
  if (cell) {
    cell.style.backgroundColor = 'lightblue';
  }
});
// 1 listener ở table lo được mọi td — thêm/xóa td mới vẫn hoạt động
```

### Ví dụ 8: Render pipeline awareness
```js
// DOMContentLoaded: DOM parse xong, ảnh chưa load
document.addEventListener('DOMContentLoaded', () => {
  initApp(); // an toàn gọi DOM manipulation
});

// load: mọi tài nguyên (ảnh, CSS) đã xong
window.addEventListener('load', () => {
  lazyLoadImages(); // đo kích thước ảnh an toàn
});
```

## 🔬 So sánh với alternatives

| Cách tiếp cận | Ưu điểm | Nhược điểm | Phù hợp khi |
|---|---|---|---|
| **Vanilla DOM (12 bài này)** | Không dependency, kiểm soát 100% | Bảo trì khó khi app lớn | Học tập, app nhỏ |
| **jQuery** | Selector mạnh, chainable | Thư viện nặng (~30KB) | Legacy project |
| **Vanilla + frameworks** |-best of both | Learning curve | App trung bình |
| **React/Vue** | Declarative, diff optimized | Overhead, dependency | App phức tạp |

## 📊 Performance & Best Practices

- **`getElementById` nhanh nhất** — O(1) lookup, dùng khi có id.
- **`querySelector` đủ cho 90% case** — CSS selector mạnh, readable.
- **Cache reference** — gán `const el = document.querySelector(...)` thay vì gọi lặp trong loop.
- **Batch DOM writes** — gộp nhiều style/class changes thành một lần repaint.
- **Avoid synchronous layout read** — đọc `offsetWidth` rồi ghi `style.width` trong cùng loop gây layout thrashing.
- **Passive listener cho scroll** — `addEventListener('scroll', fn, { passive: true })` giúp browser optimize scroll.
- **DOMContentLoaded vs load** — DOMContentLoaded sớm hơn, dùng cho init app; load muộn hơn, dùng cho image-dependent code.

## 🔗 Liên kết chéo

- Xem thêm: `18_dom-apis/01_dom-basics/01_f8-basic-dom/` — 12 bài chi tiết từng chủ đề.
- Xem thêm: `18_dom-apis/01_dom-basics/02_how-browser-reads-html/` — rendering pipeline.
- Xem thêm: `18_dom-apis/02_dom-advanced/` — DOM manipulation, Shadow DOM, Virtual DOM.
- Xem thêm: `18_dom-apis/03_events/` — event system chi tiết.
- Xem thêm: `17_memory-management/` — DOM node và memory leak relationship.
- Xem thêm: `19_browser-devtools/` — debug DOM qua Elements/Console panels.
