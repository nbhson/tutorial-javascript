# Bài 8 — DOM CSS Style: Đổi Màu/Size Động

## 🔑 Khái niệm

Có 2 cách đọc/ghi style element trong JS:

| Cách | Đọc | Ghi | Notes |
|---|---|---|---|
| `element.style.prop` | Inline style hiện tại | Ghi inline style | Chỉ đọc inline, không đọc CSS file |
| `getComputedStyle(el)` | Giá trị thực tế (sau cascade) | Không ghi được | Toàn bộ CSS được tính |

Thuộc tính CSS trong JS viết **camelCase**:
- `background-color` → `style.backgroundColor`
- `font-size` → `style.fontSize`
- `z-index` → `style.zIndex`
- `margin-top` → `style.marginTop`

## ✅ Điểm mạnh
- `style.prop` thay đổi inline style ngay lập tức
- `getComputedStyle` cho biết giá trị thực (kể cả từ class, selector, inherit)
- Kết hợp 2 cách: đọc computed, gán inline khi cần override

## ⚠️ Lưu ý
- `style.prop` trả về string rỗng `""` nếu value đến từ CSS class/file (không phải inline)
- Đơn vị `px` phải thêm vào khi gán: `el.style.width = "100px"` (không chỉ `"100"`)
- `getComputedStyle` là **đọc-only**, không dùng để set style
- Gọi `getComputedStyle` nhiều lần trong loop → chậm (caching)

## 💡 Khi nào dùng
- Animation/transition động (color, position, size)
- Tooltip position theo chuột
- Responsive adjustments dựa trên window size

## 🎯 Ví dụ minh họa

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

console.log(styles.width);      // "200px" (kể cả từ class)
console.log(styles.backgroundColor); // "rgb(255, 127, 80)"
console.log(styles.display);    // "block"
console.log(getComputedStyle(box).opacity); // "1"
```

### Hover effect động
```js
box.addEventListener("mouseenter", () => {
  const current = getComputedStyle(box).width;
  box.style.width = `calc(${current} * 1.2)`;
});
box.addEventListener("mouseleave", () => {
  box.style.width = ""; // revert về CSS
});
```

## 📚 Tham khảo & Bài tập
- File: `app.js`, `index.html` trong folder `8_dom-css-style/`
- Thực hành: tạo button đổi màu box ngẫu nhiên
- Câu hỏi: Khi nào `style.color` trả về `""` dù CSS có set color?
