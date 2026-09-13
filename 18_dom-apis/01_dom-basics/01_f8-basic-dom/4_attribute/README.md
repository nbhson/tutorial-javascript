# Bài 4 — DOM Attribute: Đọc/Ghi Thuộc Tính HTML

## 🔑 Khái niệm

**Attribute** là thông tin đi kèm element trong HTML: `id`, `class`, `src`, `href`, `disabled`, `data-*`, `title`... JavaScript truy cập qua 4 phương thức chính:

| Method | Hành vi |
|---|---|
| `getAttribute(name)` | Đọc giá trị attribute (hoặc `null` nếu không có) |
| `setAttribute(name, value)` | Ghi/ghi đè attribute |
| `removeAttribute(name)` | Xóa attribute |
| `hasAttribute(name)` | Kiểm tra tồn tại → boolean |
| `dataset` | Property object truy cập `data-*` attributes |

## ✅ Điểm mạnh
- `getAttribute` không tự convert type — giữ nguyên string
- `dataset` chuyển `data-user-id` → `el.dataset.userId`
- `hasAttribute` an toàn hơn so với `el.attr !== undefined`

## ⚠️ Lưu ý
- **Thuộc tính HTML ≠ property DOM**: `el.getAttribute("checked")` ≠ `el.checked`. Sau này là state JS, trước là HTML source.
- `classList` (bài sau) ưu tiên hơn `className += " ..."` vì tránh duplicate và parse sai
- `setAttribute` với giá trị không phải string sẽ bị convert ngầm — hãy luôn dùng string
- `dataset` chỉ làm việc với `data-*`, không áp dụng cho `id/class/name`

## 💡 Khi nào dùng
- Đọc/ghi `href`, `src` động (lazy loading ảnh)
- Toggle attribute `disabled`, `hidden`, `aria-*`
- Lưu metadata custom qua `data-*` attributes

## 🎯 Ví dụ minh họa

### CRUD attribute cơ bản
```js
const img = document.querySelector("img");

// Đọc
console.log(img.getAttribute("src"));   // "photo.jpg"

// Ghi
img.setAttribute("alt", "Mô tả ảnh");
img.setAttribute("loading", "lazy");

// Kiểm tra
if (img.hasAttribute("data-src")) {
  img.src = img.getAttribute("data-src");
}

// Xóa
img.removeAttribute("loading");
```

### Dataset — data-* attributes
```html
<div id="card" data-user-id="42" data-role="admin" data-is-active="true"></div>
```
```js
const card = document.getElementById("card");
console.log(card.dataset.userId);     // "42" (string)
console.log(card.dataset.role);       // "admin"
console.log(card.dataset.isActive);   // "true"

card.dataset.isActive = "false";      // tự thêm data-is-active="false"
card.dataset.newKey = "value";        // thêm thuộc tính mới
```

### Lazy loading ảnh
```js
const imgs = document.querySelectorAll("[data-src]");
imgs.forEach(img => {
  img.addEventListener("load", () => img.src = img.dataset.src);
  img.src = img.dataset.src;
});
```

## 📚 Tham khảo & Bài tập
- File: `app.js`, `index.html` trong folder `4_attribute/`
- Thực hành: tạo button toggle `disabled` trên input form
- Câu hỏi: `el.className` và `el.getAttribute("class")` có giống nhau?
