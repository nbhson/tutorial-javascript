# DOM Attribute (Bài 4)

## Khái niệm
Element attributes: `id`, `class`, `src`, `href`, `data-*`. Đọc qua `getAttribute(name)`, ghi qua `setAttribute(name, value)`, xóa qua `removeAttribute(name)`.

## Điểm mạnh
- `setAttribute` tạo attribute nếu chưa có
- `hasAttribute` kiểm tra tồn tại nhanh
- `dataset` truy cập `data-*` thuận tiện

## Khi nào dùng
- Đọc/ghi thuộc tính HTML động, toggle `disabled`, update `data-id`.

## Ví dụ
```js
const a = document.querySelector("a");
console.log(a.href);
a.setAttribute("target", "_blank");
a.removeAttribute("download");
```

## 📚 Tham khảo
- `app.js`, `index.html`
