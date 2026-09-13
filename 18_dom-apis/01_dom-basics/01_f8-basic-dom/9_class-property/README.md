# Bài 9 — classList: Quản Lý Class — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

`element.classList` là **DOMTokenList** — một collection-like object chứa danh sách class tokens của element, với các phương thức tiện ích để thao tác an toàn. Khác với `className` (string), `classList` tránh được lỗi duplicate class và parse sai.

### Bảng phương thức classList

| Method | Mô tả | Trả về |
|---|---|---|
| `.add(cls1, cls2, ...)` | Thêm một hoặc nhiều class | — (void) |
| `.remove(cls1, cls2, ...)` | Xóa một hoặc nhiều class | — (void) |
| `.toggle(className, force?)` | Bật/tắt class | boolean (true=đã có class) |
| `.contains(className)` | Kiểm tra có class không | boolean |
| `.replace(old, new)` | Thay thế class | boolean (thay đổi thành công) |
| `.item(index)` | Lấy class tại index | string hoặc null |
| `.toString()` | Chuyển thành string | string (giống className) |

### classList vs className — so sánh
```js
const el = document.querySelector('.box');

// className — string, manual manipulation
el.className += ' active';        // ⚠️ có thể duplicate: "box active active"
el.className = el.className.replace(/\bactive\b/g, ''); // ⚠️ phức tạp

// classList — safe, clean
el.classList.add('active');       // ✅ không duplicate
el.classList.remove('active');    // ✅ an toàn
el.classList.toggle('active');    // ✅ bật/tắt
el.classList.contains('active');  // ✅ check
```

## 📐 Cấu trúc / Cú pháp

### Toggle class cơ bản
```js
const btn = document.querySelector("button");
btn.addEventListener("click", () => {
  btn.classList.toggle("active");
});
```

### Toggle có force parameter
```js
function setOpen(isOpen) {
  panel.classList.toggle("open", isOpen); // true = add, false = remove
  toggleBtn.setAttribute("aria-expanded", String(isOpen));
}
setOpen(true);   // thêm class "open"
setOpen(false);  // xóa class "open"
```

### Multiple classes và kiểm tra
```js
const box = document.querySelector(".box");
box.classList.add("red", "large", "shadow"); // thêm nhiều class cùng lúc
console.log(box.classList.contains("red"));   // true
console.log(box.classList.contains("green")); // false
box.classList.replace("red", "blue");          // đổi red → blue
```

### Dark mode toggle pattern
```js
const themeBtn = document.getElementById("theme-toggle");
themeBtn.addEventListener("click", () => {
  document.body.classList.toggle("dark-mode");
  const isDark = document.body.classList.contains("dark-mode");
  themeBtn.textContent = isDark ? "Light" : "Dark";
  localStorage.setItem("theme", isDark ? "dark" : "light");
});
// Restore on load
if (localStorage.getItem("theme") === "dark") {
  document.body.classList.add("dark-mode");
}
```

### Duyệt tất cả classes
```js
const el = document.querySelector('.box');
// NodeList-like iteration
[...el.classList].forEach(cls => console.log(cls));
// Hoặc
for (const cls of el.classList) {
  console.log(cls);
}
```

## ✅ Điểm mạnh

1. **Tránh lỗi duplicate class** — `className += "active"` có thể tạo `"active active"`; `classList.add` tự check.
2. **`toggle` có mode force** — `el.classList.toggle("open", isVisible)` — rõ ràng hơn if/else.
3. **`contains` nhanh O(1)** — tránh so sánh chuỗi thủ công `className.indexOf('active') > -1`.
4. **`replace` đổi class gốc** — giữ token khác nguyên vẹn, chỉ đổi class được chỉ định.
5. **Multi-class add/remove** — `.add('a', 'b', 'c')` thêm nhiều class cùng lúc.
6. **Boolean return từ toggle/replace** — biết được state trước/sau operation.
7. **Iterable** — `[...el.classList]` hoặc `for...of` để duyệt tất cả class names.

## ⚠️ Bẫy thường gặp & Hạn chế

1. **Không thể `classList.add("a b")` thêm 2 class cùng lúc như string** — phải tách rời: `.add('a', 'b')` hoặc `.add(...'a b'.split(' '))`.
2. **`className` (string) vẫn có ích** khi cần đọc toàn bộ class làm 1 chuỗi ( ví dụ send lên server).
3. **`toggle(className, force)`** — nếu không truyền force, tự quyết định dựa trên presence. Hiểu rõ behavior này.
4. **classList là read-only collection** — không thể gán trực tiếp `el.classList = ...`.
5. **Empty class string** — element không có class nào → `classList.length === 0`, `toArray()` trả `[]`.
6. **Whitespace trong class name** — `.add("my class")` sẽ thêm token `"my class"` (có space) — thường không phải ý muốn. Dùng `.add('my', 'class')` thay thế.

## 💡 Khi nào dùng — Tình huống thực tến

1. **Toggle trạng thái UI** — active, open/close, dark mode, loading state.
2. **Conditional styling** — highlight selected item, error state, success state.
3. **Animation trigger bằng class change** — CSS transition chạy khi class thêm/bớt.
4. **Accessibility state** — `aria-expanded`, `aria-hidden` kết hợp class toggle.
5. **Form validation visual** — `.add('error')` / `.remove('error')` trên input.
6. **Component state management** — class như state machine trong vanilla JS.
7. **Feature detection fallback** — add `.no-js` trên `<html>`, JS load xong đổi thành `.js`.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Toggle class cơ bản
```js
const btn = document.querySelector("button");
btn.addEventListener("click", () => {
  btn.classList.toggle("active");
  // equivalent to:
  // if (btn.classList.contains("active")) {
  //   btn.classList.remove("active");
  // } else {
  //   btn.classList.add("active");
  // }
});
```

### Ví dụ 2: Toggle có force parameter
```js
function setOpen(isOpen) {
  panel.classList.toggle("open", isOpen);
  toggleBtn.setAttribute("aria-expanded", String(isOpen));
}
// isOpen = true → thêm "open"
// isOpen = false → xóa "open"
```

### Ví dụ 3: Multiple classes và kiểm tra
```js
const box = document.querySelector(".box");
box.classList.add("red", "large", "shadow");
console.log(box.classList.contains("red"));    // true
console.log(box.classList.contains("green"));  // false
box.classList.replace("red", "blue");
console.log(box.className); // "box large shadow blue"
```

### Ví dụ 4: Dark mode toggle hoàn chỉnh
```js
const themeBtn = document.getElementById("theme-toggle");
themeBtn.addEventListener("click", () => {
  document.body.classList.toggle("dark-mode");
  const isDark = document.body.classList.contains("dark-mode");
  themeBtn.textContent = isDark ? "☀️ Light" : "🌙 Dark";
  localStorage.setItem("theme", isDark ? "dark" : "light");
});

// Restore on page load
(function() {
  const saved = localStorage.getItem("theme");
  if (saved === "dark") document.body.classList.add("dark-mode");
})();
```

### Ví dụ 5: Form validation with classList
```js
const input = document.querySelector('#email');
input.addEventListener('blur', () => {
  const isValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(input.value);
  input.classList.toggle('error', !isValid);
  input.classList.toggle('success', isValid);
});
```

### Ví dụ 6: Accordion pattern
```js
document.querySelectorAll('.accordion-header').forEach(header => {
  header.addEventListener('click', () => {
    const panel = header.nextElementSibling;
    const isOpen = header.classList.toggle('opened');
    panel.classList.toggle('open', isOpen);
    // Close other panels
    document.querySelectorAll('.accordion-header').forEach(other => {
      if (other !== header) {
        other.classList.remove('opened');
        other.nextElementSibling.classList.remove('open');
      }
    });
  });
});
```

### Ví dụ 7: Reading all classes
```js
const el = document.querySelector('.box');
console.log([...el.classList]); // ['box', 'active', 'large']
console.log(el.classList.length); // 3
console.log(el.classList.item(0)); // "box"
console.log(el.classList.toString()); // "box active large"
```

### Ví dụ 8: Conditional class based on data
```js
function updateStatus(element, status) {
  element.classList.remove('status-pending', 'status-success', 'status-error');
  element.classList.add(`status-${status}`);
}
updateStatus(el, 'success'); // adds "status-success"
```

## 🔬 So sánh với alternatives

| Cách | Duplicate safe? | Multi-class? | Return value? | Browser support |
|---|---|---|---|---|
| **classList.add/remove/toggle** | ✅ Có | ✅ Nhiều args | toggle: boolean | ✅ IE10+ |
| **className +=** | ❌ Không | ✅ String concat | — | ✅ Tất cả |
| **className = ...** | ✅ Control | ✅ Full replace | — | ✅ Tất cả |
| **setAttribute('class',..)** | ✅ Có | ✅ | — | ✅ Tất cả |

## 📊 Performance & Best Practices

- **Prefer classList over className manipulation** — safer, cleaner, no duplicate risk.
- **Batch class changes** — `.add('a', 'b', 'c')` một lần thay vì 3 lần gọi riêng.
- **Use toggle with force** — `classList.toggle('open', isVisible)` rõ nghĩa hơn if/else.
- **Cache classList reference** — `const cls = el.classList` nếu dùng nhiều lần.
- **Avoid className string ops** — regex replace trên className dễ lỗi edge cases.
- **classList is iterable** — `[...el.classList]` để convert sang array khi cần.
- **CSS class preference** — để browser optimize rendering khi đổi class (thay vì inline style).

## 🔗 Liên kết chéo

- Xem thêm: `18_dom-apis/01_dom-basics/01_f8-basic-dom/8_dom-css-style/` — style manipulation.
- Xem thêm: `18_dom-apis/01_dom-basics/01_f8-basic-dom/4_attribute/` — attribute vs class.
- Xem thêm: `18_dom-apis/02_dom-advanced/02_shadow-dom/` — Shadow DOM scoped styles.
- File tham khảo: `app.js`, `index.html` trong folder `9_class-property/`.
