# Bài 4 — DOM Attribute: Đọc/Ghi Thuộc Tính HTML — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

**Attribute** là thông tin đi kèm element trong HTML: `id`, `class`, `src`, `href`, `disabled`, `data-*`, `title`, `aria-*`... JavaScript truy cập qua 4 phương thức chính:

### 4 Phương thức attribute CRUD

| Method | Hành vi | Trả về |
|---|---|---|
| `getAttribute(name)` | Đọc giá trị attribute (hoặc `null` nếu không có) | string hoặc null |
| `setAttribute(name, value)` | Ghi/ghi đè attribute | void |
| `removeAttribute(name)` | Xóa attribute | void |
| `hasAttribute(name)` | Kiểm tra tồn tại | boolean |

### Dataset — shortcut cho `data-*` attributes
```html
<div id="card" data-user-id="42" data-role="admin" data-is-active="true"></div>
```
```js
const card = document.getElementById("card");
card.dataset.userId;     // "42" (string)
card.dataset.role;       // "admin"
card.dataset.isActive;   // "true" (vẫn là string!)
card.dataset.isActive = "false"; // tự thêm data-is-active="false"
card.dataset.newKey = "value";   // thêm thuộc tính mới data-new-key
```

### Phân biệt Attribute vs Property — bẫy kinh điển
```html
<input type="checkbox" id="check" checked>
```
```js
const el = document.getElementById('check');
el.getAttribute('checked');  // "" (empty string) — attribute tồn tại trong HTML
el.checked;                  // true — property DOM (state hiện tại)

el.checked = false;          // bỏ tick
el.getAttribute('checked');  // vẫn "" — attribute HTML không đổi!
el.hasAttribute('checked');  // true — attribute vẫn có trong markup
```
**Quy tắc**: attribute = định nghĩa trong HTML source; property = trạng thái hiện tại trong DOM. Với các attribute chuẩn (checked, disabled, selected), dùng property (`el.checked`) thay vì attribute getter/setter.

## 📐 Cấu trúc / Cú pháp

### CRUD attribute cơ bản
```js
const img = document.querySelector("img");

// Đọc
console.log(img.getAttribute("src"));      // "photo.jpg"
console.log(img.getAttribute("alt"));      // "Mô tả"
console.log(img.getAttribute("data-src")); // null (nếu không có)

// Ghi
img.setAttribute("alt", "Mô tả ảnh mới");
img.setAttribute("loading", "lazy");
img.setAttribute("data-src", "lazy-photo.jpg");

// Kiểm tra
if (img.hasAttribute("data-src")) {
  img.src = img.getAttribute("data-src");
}

// Xóa
img.removeAttribute("loading");
img.removeAttribute("data-src");
```

### Dataset pattern
```js
const card = document.getElementById("card");

// Đọc dataset
console.log(card.dataset.userId);     // "42"
console.log(card.dataset.role);       // "admin"
console.log(card.dataset.isActive);   // "true" (string!)

// Ghi dataset
card.dataset.isActive = "false";      // tự thêm data-is-active="false"
card.dataset.newKey = "value";        // thêm thuộc tính mới data-new-key

// Xóa dataset
delete card.dataset.newKey;           // xóa data-new-key attribute
```

### Lazy loading ảnh với data-src
```js
const imgs = document.querySelectorAll("[data-src]");
imgs.forEach(img => {
  img.addEventListener("load", () => {
    img.classList.add('loaded');
  });
  img.src = img.getAttribute("data-src"); // trigger load
});
```

### Boolean attributes
```js
const btn = document.querySelector("button");

// ❌ Không nên — attribute value luôn là string
btn.setAttribute("disabled", "disabled");
btn.getAttribute("disabled"); // "disabled" (string)

// ✅ Nên — dùng property
btn.disabled = true;
btn.disabled = false;

// Kiểm tra
if (btn.hasAttribute("disabled")) { /* attribute có trong HTML */ }
if (btn.disabled) { /* button thực sự disabled */ }
```

## ✅ Điểm mạnh

1. **`getAttribute` không tự convert type** — giữ nguyên string, predictible behavior.
2. **`dataset` chuyển `data-user-id` → `el.dataset.userId`** — camelCase auto-conversion, gọn gàng.
3. **`hasAttribute` an toàn** — trả boolean, không null exception.
4. **`setAttribute` cho phép attribute không chuẩn** — `data-*`, `aria-*`, custom attributes đều được.
5. **Dataset tự động sync** — gán `dataset.x = 'y'` tự thêm/cập nhật `data-x` attribute.
6. **Read-only khi cần** — `getAttribute` không đổi DOM, safe cho inspection.
7. **HTML5 semantic** — `data-*` attributes là cách chuẩn lưu custom metadata trên element.

## ⚠️ Bẫy thường gặp & Hạn chế

1. **Thuộc tính HTML ≠ property DOM** — `el.getAttribute("checked")` ≠ `el.checked`. Sau này là state JS, trước là HTML source. Với boolean attributes (checked, disabled, selected), luôn dùng property.
2. **`classList` (bài sau) ưu tiên hơn `className += " ..."`** — tránh duplicate và parse sai.
3. **`setAttribute` với giá trị không phải string sẽ bị convert ngầm** — `el.setAttribute("data-num", 42)` → `"42"` (string). Luôn dùng string.
4. **`dataset` chỉ làm việc với `data-*`** — không áp dụng cho `id`/`class`/`name`.
5. **Dataset key là camelCase** — `data-user-id` → `dataset.userId`, `data-is-active` → `dataset.isActive`. Dấu gạch ngang thành chữ thường sau dấu.
6. **`getAttribute` trả null chứ không throw** — nếu attribute không tồn tại, nhận null, không lỗi. Nhưng null check vẫn cần.
7. **SVG attributes khác HTML** — `getAttribute("cx")` trên SVG circle trả number string, không phải qua DOM property.

## 💡 Khi nào dùng — Tình huống thực tến

1. **Đọc/ghi `href`, `src` động** — lazy loading ảnh, dynamic link routing.
2. **Toggle attribute `disabled`, `hidden`, `aria-*`** — accessibility, form validation state.
3. **Lưu metadata custom qua `data-*` attributes** — store ID, state, config trên element.
4. **Accessibility audit** — đọc/ghi `aria-label`, `aria-expanded`, `role` attributes.
5. **Data-driven UI** — element tự chứa data qua dataset, render từ đó.
6. **Form validation state** — `setCustomValidity()`, `reportValidity()` kết hợp attribute.
7. **Custom element development** — `data-*` attributes làm configuration.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: CRUD attribute cơ bản
```js
const img = document.querySelector("img");

// Đọc
console.log(img.getAttribute("src"));    // "photo.jpg"
console.log(img.getAttribute("title"));  // "Ảnh sản phẩm"
console.log(img.getAttribute("data-src")); // null (nếu không có)

// Ghi
img.setAttribute("alt", "Mô tả ảnh");
img.setAttribute("loading", "lazy");
img.setAttribute("data-src", "high-res.jpg");

// Kiểm tra và xử lý
if (img.hasAttribute("data-src")) {
  img.src = img.getAttribute("data-src");
  img.removeAttribute("data-src"); // clean up sau khi load
}

// Xóa
img.removeAttribute("loading");
```

### Ví dụ 2: Dataset — data-* attributes
```html
<div id="card" data-user-id="42" data-role="admin" data-is-active="true"></div>
```
```js
const card = document.getElementById("card");

// Đọc
console.log(card.dataset.userId);     // "42" (luôn là string)
console.log(card.dataset.role);       // "admin"
console.log(card.dataset.isActive);   // "true" (string, không phải boolean!)

// Parse số
const id = parseInt(card.dataset.userId, 10); // 42

// Ghi
card.dataset.isActive = "false";      // tự thêm data-is-active="false"
card.dataset.newKey = "value";        // thêm thuộc tính mới data-new-key

// Xóa
delete card.dataset.newKey;           // xóa data-new-key attribute
```

### Ví dụ 3: Lazy loading ảnh
```js
const imgs = document.querySelectorAll("[data-src]");
imgs.forEach(img => {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        img.src = img.getAttribute("data-src");
        observer.unobserve(img);
      }
    });
  }, { rootMargin: '50px' });
  observer.observe(img);
});
```

### Ví dụ 4: Toggle button state với attributes
```js
const btn = document.querySelector('#submit-btn');

btn.addEventListener('click', async () => {
  // Loading state
  btn.setAttribute('disabled', 'disabled');
  btn.setAttribute('aria-busy', 'true');
  btn.textContent = 'Đang xử lý...';
  
  try {
    await fetch('/api/submit', { method: 'POST', body: formData });
    btn.textContent = 'Thành công!';
    btn.setAttribute('aria-live', 'polite');
  } catch (err) {
    btn.textContent = 'Lỗi, thử lại';
    btn.setAttribute('aria-live', 'assertive');
  } finally {
    btn.removeAttribute('disabled');
    btn.removeAttribute('aria-busy');
  }
});
```

### Ví dụ 5: Read all dataset keys dynamically
```js
const elements = document.querySelectorAll('[data-*]');
elements.forEach(el => {
  const data = {};
  for (const key in el.dataset) {
    data[`data-${key}`] = el.dataset[key];
  }
  console.log(el.tagName, data);
});
```

### Ví dụ 6: Attribute vs Property divergence
```js
const input = document.querySelector('input[type="checkbox"]');
console.log(input.getAttribute('checked')); // null (HTML source)
console.log(input.checked);                  // false (current state)

input.checked = true;
console.log(input.getAttribute('checked')); // null (attribute không tự đổi!)
console.log(input.checked);                  // true (property mới)

input.setAttribute('checked', '');
console.log(input.getAttribute('checked')); // "" (attribute now set)
console.log(input.checked);                  // true (property sync)
```

## 🔬 So sánh với alternatives

| Cách | Ưu điểm | Nhược điểm | Phù hợp khi |
|---|---|---|---|
| **getAttribute/setAttribute** | Chuẩn, mọi attribute | String-only, verbose | Custom attributes, aria |
| **dataset** | Gọn, camelCase auto | Chỉ data-*, string values | Custom data storage |
| **Property direct** | Type-safe, auto-sync | Chỉ built-in attributes | checked, disabled, selected |
| **className** | Cả class string | Duplicate risk, parse needed | Read all classes at once |
| **classList** | Safe add/remove/toggle | Không đọc raw class string | Toggle classes |

## 📊 Performance & Best Practices

- **Prefer property over attribute** cho boolean attributes (checked, disabled, selected) — type-safe, auto-sync.
- **Use dataset for custom data** — cleaner API, auto camelCase conversion.
- **Batch attribute changes** — gộp nhiều `setAttribute` thành `innerHTML` hoặc `Object.assign` khi có thể.
- **Null-check getAttribute result** — `const val = el.getAttribute('x') || 'default'`.
- **Avoid attribute changes in hot loop** — mỗi `setAttribute` trigger attribute change events + potential reflow.
- **Use hasAttribute before getAttribute** — nếu cần check tồn tại trước khi đọc.
- **dataset values are always strings** — parse với `parseInt()`, `parseFloat()`, `JSON.parse()` khi cần type khác.

## 🔗 Liên kết chéo

- Xem thêm: `18_dom-apis/01_dom-basics/01_f8-basic-dom/3_element/` — element selection.
- Xem thêm: `18_dom-apis/01_dom-basics/01_f8-basic-dom/9_class-property/` — classList vs className.
- Xem thêm: `18_dom-apis/01_dom-basics/01_f8-basic-dom/5_text/` — textContent vs innerText.
- File tham khảo: `app.js`, `index.html` trong folder `4_attribute/`.
