# F8 Basic DOM — 12 Bài Nền Tảng — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

Chuỗi **12 bài thực hành** (phong cách F8) đi từ khái niệm đến nâng cao về DOM. Mỗi thư mục con là một bài với code mở sẵn — hầu hết gồm `app.js` + `index.html`, bạn mở `index.html` trên trình duyệt và bấm Console để xem output.

### Lộ trình chi tiết

| # | Thư mục | Chủ đề | File chính | Nội dung chính |
|---|---|---|---|---|
| 1 | `1_dom-api` | HTML DOM là gì, DOM API là gì | `1.Html-Dom-Dom-Api.js` | `document` object, cấu trúc cây |
| 2 | `2_dom-object` | `document` — object gốc của DOM | `2.Dom-object.js` | `title`, `URL`, `cookie`, `location` |
| 3 | `3_element` | Chọn element (id/class/tag/selector) | `app.js` + `index.html` | `getElementById`, `querySelector`, `querySelectorAll` |
| 4 | `4_attribute` | Thao tác attribute | `app.js` + `index.html` | `getAttribute`, `setAttribute`, `dataset` |
| 5 | `5_text` | `innerText` vs `textContent` | `app.js` + `index.html` | Khác biệt parse HTML vs raw text |
| 6 | `6_innerHTML-outerHTML` | Sửa nội dung / thẻ bao ngoài | `app.js` + `index.html` | `innerHTML`, `insertAdjacentHTML`, XSS safety |
| 7 | `7_node-property` | Node property | `app.js` + `index.html` | `childNodes`, `children`, `sibling` |
| 8 | `8_dom-css-style` | Đổi style qua JS | `app.js` + `index.html` | `element.style`, `getComputedStyle` |
| 9 | `9_class-property` | `classList` methods | `app.js` + `index.html` | `add`, `remove`, `toggle`, `contains` |
| 10 | `10_dom-event` | Gán sự kiện qua property | `app.js` + `index.html` | `onclick`, `MouseEvent` |
| 11 | `11_PreventDefault-StopPropagation` | Chặn hành vi mặc định & bubbling | `app.js` + `index.html` | `preventDefault()`, `stopPropagation()` |
| 12 | `12_EventListener` | `addEventListener`/`removeEventListener` | `app.js` + `index.html` | Multiple handlers, options, cleanup |

### Điểm mấu chốt để bật ra ngay

- **HTML DOM**: chuẩn mô hình do W3C; **DOM API**: bộ Web API để JS truy/xuất và chỉnh sửa model đó.
- `document` là object đại diện toàn bộ website — mọi truy cập đều qua nó.
- `innerHTML` phân tích thẻ HTML; `innerText`/`textContent` chỉ là text (bài 5).
- **Node ≠ Element**: `childNodes` tính cả "text node"; `children` chỉ tính element (bài 7).
- Sự kiện: `onclick` gán được một handler; `addEventListener` cho nhiều handler và có thể gỡ (bài 10, 12).
- `preventDefault` chặn hành vi mặc định (link không navigate); `stopPropagation` chặn bubbling lên parent.

## 📐 Cấu trúc / Cú pháp — Tổng hợp 12 bài

### Bài 1-2: Document basics
```js
console.log(document.documentElement.tagName); // "HTML"
console.log(document.head.tagName);            // "HEAD"
console.log(document.body.tagName);            // "BODY"
document.title = "Trang mới";
console.log(document.URL, document.domain);
```

### Bài 3: Element selection
```js
// getElementById — O(1), nhanh nhất
const el = document.getElementById("app");

// querySelector — CSS selector, trả phần tử đầu
const first = document.querySelector(".item.active");

// querySelectorAll — trả NodeList (static)
const all = document.querySelectorAll("div > p.highlight");
[...all].forEach(el => el.style.color = "red");
```

### Bài 4: Attribute CRUD
```js
const img = document.querySelector("img");
img.getAttribute("src");          // đọc
img.setAttribute("loading", "lazy"); // ghi
img.hasAttribute("data-src");      // kiểm tra
img.removeAttribute("loading");   // xóa
img.dataset.userId;               // data-user-id → dataset.userId
```

### Bài 5: Text content
```js
el.textContent;   // raw text, nhanh, an toàn XSS
el.innerText;     // rendered text, theo CSS, chậm hơn
el.outerText;     // (IE only) — thay thế element bằng text
```

### Bài 6: HTML content
```js
el.innerHTML = "<b> Bold </b>";           // parse HTML
el.outerHTML = "<span> replaced </span>"; // thay thế chính element
el.insertAdjacentHTML("beforeend", "<li>new</li>"); // giữ event listeners cũ
```

### Bài 7: Node properties
```js
el.childNodes;      // tất cả nodes (element + text + comment)
el.children;        // chỉ element children
el.firstChild;      // node đầu
el.firstElementChild; // element đầu (bỏ text node)
el.nextElementSibling; // element anh/em cùng cấp
```

### Bài 8: CSS style
```js
el.style.backgroundColor = "coral"; // camelCase
el.style.fontSize = "16px";         // phải có đơn vị
const computed = getComputedStyle(el);
computed.width;  // "200px" — giá trị thực sau cascade
```

### Bài 9: classList
```js
el.classList.add("active", "highlight");
el.classList.remove("inactive");
el.classList.toggle("open");           // boolean return
el.classList.contains("active");       // boolean
el.classList.replace("old", "new");    // boolean
```

### Bài 10: DOM event property
```js
const h = document.querySelector('h1').nextElementSibling;
h.onclick = function(e) {
  console.log(e);              // MouseEvent
  h.style.color = 'red';
};
```

### Bài 11: PreventDefault & StopPropagation
```js
// preventDefault — chặn hành vi mặc định
a.onclick = (e) => { e.preventDefault(); };

// stopPropagation — chặn bubbling lên parent
child.onclick = (e) => { e.stopPropagation(); };
// parent.onclick sẽ KHÔNG chạy
```

### Bài 12: EventListener
```js
function viec1() { console.log("Việc 1"); }
btn.addEventListener("click", viec1);
btn.addEventListener("click", () => console.log("Việc 2"));
// Sau 5s gỡ viec1:
setTimeout(() => btn.removeEventListener("click", viec1), 5000);
```

## ✅ Điểm mạnh

1. **Lộ trình bài bản** — 12 bước từ lý thuyết tới sự kiện, đúng chuỗi phụ thuộc kiến thức.
2. **Mỗi bài có code chạy được** — workflow mở `index.html` → xem Console → sửa thử, không cần cài đặt.
3. **Ghi chú ngay trong code** — các comment giải thích cặn kẽ từng dòng, tiện tự học.
4. **Bao phủ đủ API tần suất cao** — selector, attribute, text, HTML, style, class, event — thứ bạn code hàng ngày.
5. **Chuẩn bị nền tảng DOM nâng cao** cho `02_dom-advanced` và events chuyên sâu trong `03_events`.
6. **Zero dependency** — chạy được trên mọi browser hiện đại, không cần build tool.
7. **Tự học hiệu quả** — mỗi bài độc lập, có thể học theo tốc độ riêng.
8. **Interview ready** — 12 chủ đề này cover hầu hết câu hỏi DOM trong phỏng vấn frontend.

## ⚠️ Bẫy thường gặp & Hạn chế

1. **`getElementsByClassName`/`getElementsByTagName` trả HTMLCollection sống**; `querySelectorAll` trả **NodeList tĩnh** — đừng nhầm khi dùng `length` hay `map`.
2. **`setAttribute(name, value)` mới cho phép attribute không chuẩn**; các thuộc tính hợp lệ thì buộc qua setter trực tiếp (`link.href = ...`).
3. **`innerText` đọc theo cái hiển thị**, còn setter `innerText` lại hoạt động như đặt text — sự lệch này hay bẫy người mới.
4. **Quên `event.stopPropagation()`** trong bài 11 khiến sự kiện vẫn lan lên phần tử cha.
5. **`innerHTML` với user input = XSS risk** — luôn escape hoặc dùng `textContent` cho dữ liệu người dùng.
6. **Anonymous function không remove được** bằng `removeEventListener` — phải lưu reference.
7. **`nodeType === 3` (text node)** thường gây nhầm lẫn khi đếm `childNodes.length`.
8. **`getComputedStyle` là read-only** — không thể dùng để set style.

## 💡 Khi nào dùng — Tình huống thực tế

1. **Bắt đầu học DOM** hoặc **ôn nhanh** trước khi bước vào DOM nâng cao/framework.
2. **Cần mẫu thao tác cụ thể** — sửa text, đổi class theo điều kiện, đổi style qua `Object.assign`.
3. **Code trong công việc hàng ngày** cần nhớ lại cách dùng `classList.toggle` / `removeEventListener` / `preventDefault`.
4. **Làm giáo án / hướng dẫn học viên** đi từng bước nhỏ dễ hiểu.
5. **Debug trang web** — dùng Console để test DOM API trực tiếp mà không cần sửa code.
6. **Viết bookmarklet / userscript** — automate task trên trang web.
7. **Prototype feature** nhanh trước khi đưa vào framework.
8. **Onboarding developer mới** — 12 bài này là curriculum DOM chuẩn.

## 🎯 Ví dụ minh họa — Tổng hợp từ 12 bài

### Từ bài 3: Chọn element linh hoạt
```js
// ID — nhanh nhất
const box = document.getElementById("app");

// Class — HTMLCollection live
const items = document.getElementsByClassName("item");

// Tag — HTMLCollection live
const lis = document.getElementsByTagName("li");

// CSS selector — NodeList static
const firstActive = document.querySelector(".item.active");
const allLinks = document.querySelectorAll("a[href^='https://']");

// Spread NodeList thành array
const arr = [...document.querySelectorAll("div.box")];
arr.reverse(); // giờ có array methods
```

### Từ bài 5-6: Text vs HTML
```js
const el = document.querySelector(".container");

// textContent — an toàn, nhanh
el.textContent = '<b>Safe</b>'; // hiển thị literal "<b>Safe</b>"

// innerHTML — parse HTML, cần escape user input
el.innerHTML = '<b>Bold</b>';   // in đậm "Bold"

// insertAdjacentHTML — giữ event listeners cũ (khác innerHTML replace)
el.insertAdjacentHTML("beforeend", '<span class="badge">New</span>');
```

### Từ bài 7: Node vs Element
```js
const ul = document.querySelector("ul");
console.log(ul.childNodes.length);  // 7 (bao gồm whitespace text nodes)
console.log(ul.children.length);    // 3 (chỉ 3 <li>)

for (const child of ul.children) {
  console.log(child.tagName); // LI, LI, LI
}
```

### Từ bài 10-12: Event system
```js
// Bài 10: onclick property
const h = document.querySelector('h1').nextElementSibling;
h.onclick = function(e) {
  console.log(e); // MouseEvent đầy đủ
  h.style.color = 'red';
};

// Bài 11: preventDefault + stopPropagation
for (const a of document.links) {
  a.onclick = (e) => {
    if (e.target.href !== "http://facebook.com/") e.preventDefault();
  };
}
div.onclick = () => console.log('div');
button.onclick = (e) => { e.stopPropagation(); console.log('button'); };

// Bài 12: addEventListener multiple + remove
function viec1() { console.log("Việc 1"); }
btn.addEventListener("click", viec1);
btn.addEventListener("click", () => console.log("Việc 2"));
setTimeout(() => btn.removeEventListener("click", viec1), 5000);
```

### Tổng hợp: Mini to-do list (kết hợp nhiều bài)
```js
document.addEventListener('DOMContentLoaded', () => {
  const input = document.getElementById('taskInput');
  const btn = document.getElementById('addTaskBtn');
  const list = document.getElementById('taskList');

  btn.addEventListener('click', () => {
    const text = input.value.trim();
    if (!text) return;

    const li = document.createElement('li');
    li.textContent = text;                    // bài 5
    li.classList.add('task-item');            // bài 9
    li.addEventListener('click', () => li.remove()); // bài 12
    list.appendChild(li);                     // bài 7
    input.value = '';
  });
});
```

## 🔬 So sánh với alternatives

| Phương pháp | Ưu điểm | Nhược điểm | Phù hợp khi |
|---|---|---|---|
| **12 bài F8 này** | Bài bản, dễ theo dõi | Chỉ vanilla DOM | Học nền tảng |
| **jQuery** | Selector mạnh, chainable | Thư viện nặng | Legacy codebase |
| **Vanilla raw** | Không dependency | Boilerplate nhiều | App nhỏ, performance-critical |
| **Framework (React/Vue)** | Declarative, diff | Overhead, learning curve | App phức tạp |

## 📊 Performance & Best Practices

- **Cache query results** — `const el = document.querySelector(...)` thay vì gọi lặp.
- **Prefer `textContent` over `innerHTML`** cho user data — an toàn XSS + faster.
- **Use `classList` over `className` concatenation** — tránh duplicate, cleaner.
- **Batch DOM writes** — gộp nhiều style changes → 1 reflow.
- **DOMContentLoaded > window.load** cho init code — sớm hơn, không chờ ảnh.
- **Event delegation** khi có nhiều similar elements — 1 listener thay N listeners.
- **Passive listener cho scroll/ touch** — `{ passive: true }` giúp browser optimize.
- **Avoid synchronous layout read in write loop** — `offsetWidth` rồi `style.width` trong cùng iteration gây layout thrashing.

## 🔗 Liên kết chéo

- Xem thêm: `18_dom-apis/01_dom-basics/02_how-browser-reads-html/` — rendering pipeline.
- Xem thêm: `18_dom-apis/02_dom-advanced/01_manipulation/` — DOM manipulation nâng cao.
- Xem thêm: `18_dom-apis/03_events/` — event system chi tiết (bubbling, delegation).
- Xem thêm: `17_memory-management/01_memory-lifecycle-gc/02_memory-leaks/` — listener leak pattern.
- Xem thêm: `19_browser-devtools/` — debug DOM qua Elements panel.
- Các file `app.js` + `index.html` trong từng thư mục con là code runnable thực tế.
