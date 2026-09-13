# Bài 8 — DOM CSS Style: Đổi Màu/Size Động — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

Có 2 cách đọc/ghi style element trong JS, và chúng **khác nhau căn bản**:

| Cách | Đọc | Ghi | Mô tả |
|---|---|---|---|
| `element.style.prop` | Inline style hiện tại | Ghi inline style | Chỉ đọc được style inline (directly set via JS/HTML `style=""`) |
| `getComputedStyle(el)` | Giá trị thực tế (sau cascade) | Không ghi được | Đọc computed value — tổng hợp CSS file + inline + inherited |

### CSS property naming in JS
Thuộc tính CSS viết **camelCase** trong JavaScript:
- `background-color` → `style.backgroundColor`
- `font-size` → `style.fontSize`
- `z-index` → `style.zIndex`
- `margin-top` → `style.marginTop`
- `border-radius` → `style.borderRadius`
- `box-shadow` → `style.boxShadow`

### Khi nào `style.prop` trả về empty string
```js
// CSS file: .box { color: red; }
const box = document.querySelector('.box');
console.log(box.style.color); // "" — empty! Vì color đến từ CSS class, không phải inline
box.style.color = 'blue';     // giờ có inline style
console.log(box.style.color); // "blue"
```

## 📐 Cấu trúc / Cú pháp

### Đổi inline style
```js
const box = document.querySelector(".box");
box.style.width = "200px";
box.style.height = "100px";
box.style.backgroundColor = "coral";
box.style.borderRadius = "8px";
box.style.transition = "all 0.3s ease";
```

### Đọc computed style
```js
const box = document.querySelector(".box");
const styles = getComputedStyle(box);

console.log(styles.width);          // "200px" (kể cả từ class)
console.log(styles.backgroundColor); // "rgb(255, 127, 80)" (converted to rgb)
console.log(styles.display);        // "block"
console.log(styles.opacity);        // "1"
```

### Hover effect động
```js
box.addEventListener("mouseenter", () => {
  const current = getComputedStyle(box).width;
  box.style.width = `calc(${current} * 1.2)`;
});
box.addEventListener("mouseleave", () => {
  box.style.width = ""; // revert về CSS class
});
```

### Object.assign để set nhiều style cùng lúc
```js
Object.assign(box.style, {
  width: '200px',
  height: '100px',
  backgroundColor: 'coral',
  borderRadius: '8px',
  transition: 'all 0.3s ease'
});
```

### Đọc giá trị số từ computed style
```js
const styles = getComputedStyle(box);
const width = parseInt(styles.width, 10); // 200 (number)
const opacity = parseFloat(styles.opacity); // 0.8 (number)
```

## ✅ Điểm mạnh

1. **`style.prop` thay đổi inline style ngay lập tức** — visible ngay, không cần reload CSS.
2. **`getComputedStyle` cho biết giá trị thực** (kể cả từ class, selector, inherit) — đọc được giá trị sau CSS cascade.
3. **Kết hợp 2 cách** — đọc computed, gán inline khi cần override.
4. **`Object.assign` batch multiple styles** — một lần set nhiều property.
5. **Transition support** — `style.transition` tạo animation mượt mà.
6. **Read-return-modify pattern** — đọc computed value, modify, set back (ví dụ: scale up).
7. **Zero dependency** — native browser API, không cần thư viện CSS-in-JS.

## ⚠️ Bẫy thường gặp & Hạn chế

1. **`style.prop` trả về string rỗng `""` nếu value đến từ CSS class/file** — không phải từ inline style. Phải dùng `getComputedStyle` để đọc giá trị thực.
2. **Đơn vị `px` phải thêm vào khi gán** — `el.style.width = "100px"` (không chỉ `"100"`). Trừ khi property không cần unit (opacity, zIndex).
3. **`getComputedStyle` là đọc-only** — không thể dùng để set style. Muốn set phải dùng `element.style.prop`.
4. **Gọi `getComputedStyle` nhiều lần trong loop** → chậm (browser phải tính lại cascade mỗi lần). Cache result.
5. **Computed value được normalize** — `#ff7f50` → `"rgb(255, 127, 80)"`, `2em` → `"32px"` (depending on font-size).
6. **`style.cssText`** — read/write toàn bộ inline style như string: `el.style.cssText = 'color:red;width:100px;'`.
7. **CSS custom properties (variables)** — `getComputedStyle` đọc `--my-var`, set qua `style.setProperty('--my-var', 'value')`.

## 💡 Khi nào dùng — Tình huống thực tến

1. **Animation/transition động** — color, position, size thay đổi theo tương tác người dùng.
2. **Tooltip position theo chuột** — đọc scroll position + mouse coordinates → set `left/top`.
3. **Responsive adjustments dựa trên window size** — đọc computed width, adjust khác element.
4. **Dynamic theme** — đổi màu sắc theme realtime qua style changes.
5. **Measurement before animation** — đọc computed dimension trước khi animate (calc-based).
6. **Progress bar / loader** — set `width` theo percentage động.
7. **CSS variable manipulation** — `style.setProperty('--primary-color', '#ff0000')`.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Đổi inline style cơ bản
```js
const box = document.querySelector(".box");
box.style.width = "200px";
box.style.height = "100px";
box.style.backgroundColor = "coral";
box.style.borderRadius = "8px";
box.style.transition = "all 0.3s ease";
```

### Ví dụ 2: Đọc computed style
```js
const box = document.querySelector(".box");
const styles = getComputedStyle(box);

console.log(styles.width);           // "200px" (kể cả từ class)
console.log(styles.backgroundColor); // "rgb(255, 127, 80)"
console.log(styles.display);         // "block"
console.log(styles.opacity);         // "1"

// Parse thành số
const w = parseInt(styles.width, 10); // 200
const h = parseInt(styles.height, 10); // 100
```

### Ví dụ 3: Hover effect động (read-compute-set)
```js
box.addEventListener("mouseenter", () => {
  const current = getComputedStyle(box).width;
  box.style.width = `calc(${current} * 1.2)`;
  box.style.backgroundColor = 'darkcoral';
});
box.addEventListener("mouseleave", () => {
  box.style.width = ""; // revert về CSS class
  box.style.backgroundColor = "";
});
```

### Ví dụ 4: Batch style với Object.assign
```js
const box = document.querySelector(".box");
Object.assign(box.style, {
  width: '300px',
  height: '150px',
  backgroundColor: '#3498db',
  borderRadius: '12px',
  boxShadow: '0 4px 12px rgba(0,0,0,0.2)',
  transition: 'all 0.3s ease'
});
```

### Ví dụ 5: Dynamic CSS variable
```js
const root = document.documentElement;

// Set CSS custom property
root.style.setProperty('--primary-color', '#e74c3c');
root.style.setProperty('--font-size', '18px');

// Read CSS custom property
const primaryColor = getComputedStyle(root).getPropertyValue('--primary-color').trim();
console.log(primaryColor); // "#e74c3c"
```

### Ví dụ 6: Scroll-based parallax
```js
window.addEventListener('scroll', () => {
  const scrolled = window.pageYOffset;
  const hero = document.querySelector('.hero');
  hero.style.transform = `translateY(${scrolled * 0.5}px)`;
});
```

### Ví dụ 7: Read all computed styles (debug)
```js
function logComputedStyles(el) {
  const styles = getComputedStyle(el);
  const props = [
    'display', 'width', 'height', 'padding', 'margin',
    'border', 'color', 'backgroundColor', 'fontSize',
    'fontWeight', 'lineHeight', 'position', 'top', 'left'
  ];
  props.forEach(prop => {
    console.log(`${prop}: ${styles[prop]}`);
  });
}
logComputedStyles(document.querySelector('.box'));
```

## 🔬 So sánh với alternatives

| Cách | Đọc CSS file? | Ghi được? | Speed | Use case |
|---|---|---|---|---|
| **`style.prop`** | ❌ Chỉ inline | ✅ Có | ⭐⭐⭐ Nhanh | Set inline style |
| **`getComputedStyle`** | ✅ Tất cả | ❌ Không | ⭐⭐ Trung bình | Read actual rendered value |
| **`window.getComputedStyle`** | ✅ Tất cả | ❌ Không | ⭐⭐ | Same as above (global) |
| **CSS class toggle** | ✅ (via class) | ✅ (indirect) | ⭐⭐⭐ | Theme switching |
| **`element.sheet`** | ✅ (read CSSOM) | ✅ (modify CSSOM) | ⭐ Chậm | Dynamic stylesheet |

## 📊 Performance & Best Practices

- **Cache `getComputedStyle` result** — gọi nhiều lần trong loop → chậm. Gán biến rồi dùng lại.
- **Prefer class toggle over inline style** — CSS class được browser optimize tốt hơn, dễ maintain.
- **Use `transition` CSS property** — `style.transition = 'all 0.3s'` tạo animation mượt mà.
- **Avoid style reads in write loop** — đọc `offsetWidth` rồi ghi `style.width` trong cùng iteration gây layout thrashing.
- **Batch style changes** — gộp nhiều `style.prop = ...` thành 1 lần repaint.
- **Use CSS variables for theming** — `setProperty('--var', val)` + read via `getPropertyValue`.
- **`cssText` for bulk inline** — `el.style.cssText = 'a:1;b:2;c:3'` — overwrite all inline styles.
- **Unit reminder** — hầu hết property cần unit (`px`, `%`, `em`); trừ opacity, zIndex, index-based properties.

## 🔗 Liên kết chéo

- Xem thêm: `18_dom-apis/01_dom-basics/01_f8-basic-dom/9_class-property/` — classList vs style.
- Xem thêm: `18_dom-apis/01_dom-basics/01_f8-basic-dom/4_attribute/` — attribute vs style.
- Xem thêm: `18_dom-apis/02_dom-advanced/02_shadow-dom/` — Shadow DOM scoped styles.
- File tham khảo: `app.js`, `index.html` trong folder `8_dom-css-style/`.
