# Bài 6 — innerHTML / outerHTML: Chèn HTML Động

## 🔑 Khái niệm

| Thuộc tính | Mô tả |
|---|---|
| `innerHTML` | Đọc/giá trị HTML **bên trong** element (children) |
| `outerHTML` | Đọc/giá trị HTML **bao gồm cả chính element đó** |
| `insertAdjacentHTML(pos, html)` | Chèn HTML tại vị trí relative với element |

Vị trí trong `insertAdjacentHTML`:
- `"beforebegin"` — trước element
- `"afterbegin"` — bên trong, trước child đầu tiên
- `"beforeend"` — bên trong, sau child cuối cùng
- `"afterend"` — sau element

## ✅ Điểm mạnh
- Viết HTML phức tạp trong 1 dòng JavaScript
- `insertAdjacentHTML` giữ event listener đã gắn sẵn (khác innerHTML replace toàn bộ)
- Parser HTML native → hiểu semantic tags tốt

## ⚠️ Lưu ý — QUAN TRỌNG
- **XSS Vulnerability**: nếu gán HTML từ user input chưa sanitize → hacker chèn `<script>`
- `innerHTML` thay thế **toàn bộ** children → mất event listeners cũ trên children
- `outerHTML` thay thế chính element → DOM reference biến mất

```js
// ❌ NGUY HIỂM
el.innerHTML = userInput;

// ✅ AN TOÀN — escape trước
el.innerHTML = escapeHtml(userInput);

// ✅ AN TOÀN — dùng textContent thay innerHTML
el.textContent = userInput;
```

## 💡 Khi nào dùng
- Render template HTML động (danh sách sản phẩm, comment)
- Chèn nhiều element con cùng lúc (hiệu năng tốt hơn append từng cái)
- Thay thế component hoàn toàn (modal, dialog)

## 🎯 Ví dụ minh họa

### innerHTML cơ bản
```js
const container = document.querySelector("#list");
container.innerHTML = `
  <li>Apple</li>
  <li>Banana</li>
  <li>Cherry</li>
`;
```

### insertAdjacentHTML — giữ event listener
```js
const card = document.querySelector(".card");

// Thêm vào cuối children (giữ event listener cũ)
card.insertAdjacentHTML("beforeend", '<span class="badge">New</span>');

// Thêm trước element (không làm hỏng child)
card.insertAdjacentHTML("beforebegin", '<div class="before">Trước</div>');
```

### Render danh sách động an toàn
```js
function renderUsers(users) {
  const ul = document.querySelector("#user-list");
  ul.innerHTML = users.map(u => `
    <li>${escapeHtml(u.name)} — ${escapeHtml(u.email)}</li>
  `).join("");
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}
```

## 📚 Tham khảo & Bài tập
- File: `app.js`, `index.html` trong folder `6_innerHTML-outerHTML/`
- Thực hành: tạo function `renderList(items)` dùng `innerHTML` + `escapeHtml`
- Câu hỏi: `innerHTML` vs `insertAdjacentHTML` khác nhau như thế nào về hiệu năng?
