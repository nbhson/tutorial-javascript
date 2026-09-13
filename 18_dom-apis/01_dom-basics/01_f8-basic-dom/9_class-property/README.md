# Bài 9 — classList: Quản Lý Class

## 🔑 Khái niệm

`element.classList` là DOMTokenList — tập hợp token class với các phương thức:

| Method | Mô tả | Trả về |
|---|---|---|
| `.add(cls1, cls2, ...)` | Thêm một hoặc nhiều class | — |
| `.remove(cls1, cls2, ...)` | Xóa một hoặc nhiều class | — |
| `.toggle(className, force?)` | Bật/tắt class | boolean (true=đã có) |
| `.contains(className)` | Kiểm tra có class không | boolean |
| `.replace(old, new)` | Thay thế class | boolean (thay đổi thành công) |
| `.item(index)` | Lấy class tại index | string hoặc null |

## ✅ Điểm mạnh
- Tránh lỗi duplicate class (`className += "active"` có thể trùng)
- `toggle` có mode force: `el.classList.toggle("open", isVisible)`
- `contains` nhanh O(1), tránh so sánh chuỗi thủ công
- `replace` đổi class gốc → giữ token khác nguyên vẹn

## ⚠️ Lưu ý
- Không thể `classList.add("a b")` thêm 2 class cùng lúc — phải tách rời hoặc dùng spread
- `className` (string) vẫn có ích khi cần đọc toàn bộ class làm 1 chuỗi
- `toggle(className, force)` —若不传 force, tự quyết định dựa trên presence

## 💡 Khi nào dùng
- Toggle trạng thái UI: active, open/close, dark mode
- Conditional styling: highlight selected item
- Animation trigger bằng class change

## 🎯 Ví dụ minh họa

### Toggle class cơ bản
```js
const btn = document.querySelector("button");
btn.addEventListener("click", () => {
  btn.classList.toggle("active");
});
```

### Toggle có force
```js
function setOpen(isOpen) {
  panel.classList.toggle("open", isOpen);
  toggleBtn.setAttribute("aria-expanded", String(isOpen));
}
```

### Multiple classes và kiểm tra
```js
const box = document.querySelector(".box");
box.classList.add("red", "large", "shadow");
console.log(box.classList.contains("red"));   // true
console.log(box.classList.contains("green"));  // false
box.classList.replace("red", "blue");
```

### Dark mode toggle
```js
const themeBtn = document.getElementById("theme-toggle");
themeBtn.addEventListener("click", () => {
  document.body.classList.toggle("dark-mode");
  const isDark = document.body.classList.contains("dark-mode");
  themeBtn.textContent = isDark ? "☀️ Light" : "🌙 Dark";
});
```

## 📚 Tham khảo & Bài tập
- File: `app.js`, `index.html` trong folder `9_class-property/`
- Thực hành: tạo toggle button đổi theme sáng/tối
- Câu hỏi: `classList.toggle` vs `className +=` khác nhau ở đâu?
