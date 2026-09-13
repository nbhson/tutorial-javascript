# Bài 5 — DOM Text: Nội Dung Text — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

Có 2 thuộc tính chính để đọc/ghi text nội dung element, và chúng **KHÔNG giống nhau**:

| Thuộc tính | Mô tả | Parse HTML? | Chạy CSS? | Tốc độ |
|---|---|---|---|---|
| `textContent` | Raw text — giữ toàn bộ whitespace, tags bị bỏ | ❌ Không | ❌ Không | ⭐⭐⭐ Nhanh nhất |
| `innerText` | Rendered text — theo CSS visibility | ❌ Không | ✅ Có | ⭐⭐ Chậm hơn |
| `outerText` | Text + thay thế element cha | ❌ Không | ✅ Có | ⭐ Chậm |

### Khác biệt then chốt

- **`textContent`** đọc/giữ nguyên seluruh text trong DOM tree — kể cả text trong tag ẩn (`<style>`, `<script>`, `display:none`). Không trigger layout recalculation.
- **`innerText`** đọc text **như người dùng nhìn thấy** — bỏ qua text trong tag ẩn do CSS (`display:none`, `visibility:hidden`). Có trigger layout recalculation → chậm hơn đáng kể.
- Cả 2 đều **escape HTML** — gán `<b>text</b>` qua `textContent` sẽ hiển thị literal `<b>text</b>`, không phải in đậm.

## 📐 Cấu trúc / Cú pháp

### So sánh textContent vs innerText
```js
const el = document.querySelector(".container");
// HTML: <div class="container">Hello <span style="display:none">Hidden</span> World</div>

console.log(el.textContent); // "Hello Hidden World" (bao gồm hidden span text)
console.log(el.innerText);   // "Hello World" (bỏ hidden do CSS)
```

### Gán text — an toàn chống XSS
```js
const userInput = prompt("Nhập tên:");

// ✅ AN TOÀN — escapes < > & " '
const greeting = document.createElement("p");
greeting.textContent = "Xin chào, " + userInput;
document.body.appendChild(greeting);

// ❌ NGUY HIỂM — nếu userInput chứa <script>alert(1)</script>
// greeting.innerHTML = "Xin chào, " + userInput; // KHÔNG DÙNG với user input
```

### Tạo text node thủ công
```js
const textNode = document.createTextNode("Nội dung mới");
const p = document.createElement("p");
p.appendChild(textNode);
// Tương đương: p.textContent = "Nội dung mới";
```

### Performance benchmark
```js
const el = document.querySelector(".large-container");
const iterations = 10000;

// textContent — nhanh
const t0 = performance.now();
for (let i = 0; i < iterations; i++) {
  el.textContent = `Item ${i}`;
}
console.log(`textContent: ${(performance.now() - t0).toFixed(2)}ms`);

// innerText — chậm hơn (layout recalc mỗi lần)
const t1 = performance.now();
for (let i = 0; i < iterations; i++) {
  el.innerText = `Item ${i}`;
}
console.log(`innerText: ${(performance.now() - t1).toFixed(2)}ms`);
```

## ✅ Điểm mạnh

1. **`textContent` nhanh hơn** vì không phải tính toán layout/CSS — chỉ đọc/giá trị raw text.
2. **`textContent` an toàn chống XSS** khi gán user input — không parse HTML, escape tự động.
3. **`innerText` hiển thị đúng những gì người dùng nhìn thấy** — bỏ qua CSS-hidden content.
4. **Cả 2 đều escape HTML** — `<b>` hiện thành text literal, không phải tag.
5. **`createTextNode`** cho phép tạo text node riêng — useful cho DOM manipulation phức tạp.
6. **`textContent` bao gồm text trong `<script>` và `<style>`** — hữu ích khi cần scrape toàn bộ text.
7. **Đơn giản, không có side effect** — gán textContent không trigger reflow đáng kể.

## ⚠️ Bẫy thường gặp & Hạn chế

1. **`textContent` bao gồm text trong tag ẩn** (`<style>`, `<script>`, `display:none`) — nếu muốn chỉ text hiển thị, dùng `innerText`.
2. **`innerText` gây layout recalculation** → chậm nếu gọi nhiều lần trong loop. Tránh trong performance-critical code.
3. **Cả 2 đều escape HTML** — `<b>` hiện thành text literal, không phải in đậm. Để render HTML, dùng `innerHTML`.
4. **`innerText` có thể không hoạt động đồng nhất trên Safari cũ** — prefer `textContent` cho cross-browser compatibility.
5. **`outerText` chỉ hỗ trợ trên IE cũ** — không dùng trong code hiện đại.
6. **Gán `textContent` lên element rỗng vẫn trigger repaint** — dù ít hơn innerText.
7. **Đọc `innerText` trên element `display:none`** — luôn return empty string, dù child có text.

## 💡 Khi nào dùng — Tình huống thực tến

1. **Gán user-generated content** → ưu tiên `textContent` (an toàn + nhanh).
2. **Đọc text hiển thị thực tế cho UX** (tooltip, counter, accessibility scan) → `innerText`.
3. **Clone/nối text node** → `document.createTextNode()` cho control chính xác.
4. **Scrape toàn bộ text từ trang** (SEO tool, crawler) → `textContent` capture cả hidden text.
5. **Display dynamic message** (notification, status) → `textContent` — nhanh, an toàn.
6. **Accessibility audit** → đọc `innerText` để biết screen reader sẽ đọc gì.
7. **Text animation** (typing effect) → `textContent` — không trigger layout mỗi frame.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: So sánh textContent vs innerText
```js
const el = document.querySelector(".container");
// <div class="container">Hello <span style="display:none">Hidden</span> World</div>

console.log(el.textContent); // "Hello Hidden World" (bao gồm hidden)
console.log(el.innerText);   // "Hello World" (bỏ hidden do CSS)

// Element hoàn toàn ẩn
const fullyHidden = document.querySelector(".fully-hidden");
console.log(fullyHidden.textContent); // "I exist" (vẫn đọc được)
console.log(fullyHidden.innerText);   // "" (rỗng vì display:none)
```

### Ví dụ 2: Gán an toàn (chống XSS)
```js
const userInput = prompt("Nhập tên:");
// AN TOÀN — escapes < > & " '
const greeting = document.createElement("p");
greeting.textContent = "Xin chào, " + userInput;
document.body.appendChild(greeting);

// Nếu userInput = "<script>alert(1)</script>"
// Kết quả hiển thị: Xin chào, <script>alert(1)</script> (literal text)
// Không execute!
```

### Ví dụ 3: Tạo text node thủ công
```js
const textNode = document.createTextNode("Nội dung mới");
const p = document.createElement("p");
p.appendChild(textNode);
document.body.appendChild(p);

// hoặc mix text node với element node
const fragment = document.createDocumentFragment();
fragment.appendChild(document.createTextNode("Hello "));
const strong = document.createElement("strong");
strong.textContent = "World";
fragment.appendChild(strong);
fragment.appendChild(document.createTextNode(" !"));
document.body.appendChild(fragment);
// Result: <body>Hello <strong>World</strong> !</body>
```

### Ví dụ 4: Dynamic title với textContent
```js
function updateNotificationCount(count) {
  const badge = document.querySelector('.notification-badge');
  if (count > 0) {
    badge.textContent = `(${count})`;
    badge.style.display = 'inline';
  } else {
    badge.textContent = '';
    badge.style.display = 'none';
  }
}
```

### Ví dụ 5: Reading rendered text for tooltip
```js
const el = document.querySelector('.tooltip-target');
el.addEventListener('mouseenter', () => {
  const visibleText = el.innerText; // chỉ text người dùng nhìn thấy
  showTooltip(visibleText);
});
```

### Ví dụ 6: Typing animation effect
```js
async function typeText(element, text, speed = 50) {
  element.textContent = ''; // start empty
  for (const char of text) {
    element.textContent += char; // textContent nhanh, không reflow nhiều
    await new Promise(r => setTimeout(r, speed));
  }
}
typeText(document.querySelector('#output'), 'Hello World!', 80);
```

### Ví dụ 7: Escape HTML helper (cho trường hợp cần innerHTML an toàn)
```js
function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str; // tự động escape
  return div.innerHTML;  // trả về escaped HTML string
}

function renderUserContent(htmlContainer, userInput) {
  htmlContainer.innerHTML = escapeHtml(userInput);
}
```

## 🔬 So sánh với alternatives

| Method | Parse HTML | XSS Safe | Speed | Cross-browser |
|---|---|---|---|---|
| **textContent** | ❌ | ✅ | ⭐⭐⭐ | ✅ Tất cả |
| **innerText** | ❌ | ✅ | ⭐⭐ | ✅ Hầu hết (Safari cũ hạn chế) |
| **innerHTML** | ✅ | ❌ (risk) | ⭐ | ✅ Tất cả |
| **createTextNode** | ❌ | ✅ | ⭐⭐⭐ | ✅ Tất cả |
| **outerText** | ❌ | ✅ | ⭐ | ❌ Chỉ IE |

## 📊 Performance & Best Practices

- **Prefer `textContent`** trong hầu hết trường hợp — nhanh hơn, an toàn hơn, predictible hơn.
- **Avoid `innerText` trong loop** — layout recalculation mỗi lần gọi → severe performance hit.
- **Batch text changes** — gán một lần với string dài thay vì many small appends.
- **Use `textContent` for dynamic content** — never `innerHTML` với user input tanpa sanitization.
- **`createTextNode` + `appendChild`** khi cần mix text và element nodes — precise control.
- **Read `innerText` only when you need rendered text** — accessibility, tooltip, visible content check.
- **For large text operations**, consider `DocumentFragment` + batch `textContent` assignment.

## 🔗 Liên kết chéo

- Xem thêm: `18_dom-apis/01_dom-basics/01_f8-basic-dom/6_innerHTML-outerHTML/` — so sánh với innerHTML.
- Xem thêm: `18_dom-apis/01_dom-basics/01_f8-basic-dom/4_attribute/` — attribute manipulation.
- Xem thêm: `18_dom-apis/01_dom-basics/01_f8-basic-dom/7_node-property/` — text node là nodeType 3.
- File tham khảo: `app.js`, `index.html` trong folder `5_text/`.
