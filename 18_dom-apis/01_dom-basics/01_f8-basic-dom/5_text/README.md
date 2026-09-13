# Bài 5 — DOM Text: Nội Dung Text

## 🔑 Khái niệm

Có 2 thuộc tính chính để đọc/ghi text nội dung element:

| Thuộc tính | Mô tả | Parse HTML? | Chạy CSS? |
|---|---|---|---|
| `textContent` | Raw text (giữ toàn bộ whitespace, tags bị bỏ) | ❌ | ❌ |
| `innerText` | Rendered text (theo CSS visibility) | ❌ | ✅ |
| `outerText` | Text + thay thế element cha (chỉ IE cũ) | ❌ | ✅ |

## ✅ Điểm mạnh
- `textContent` **nhanh hơn** vì không phải tính toán layout/CSS
- `textContent` an toàn chống XSS khi gán user input (không parse HTML)
- `innerText` hiển thị đúng những gì người dùng nhìn thấy (ẩn `display:none` không hiện)

## ⚠️ Lưu ý
- `textContent` bao gồm text trong tag ẩn (`<style>`, `<script>`, `display:none`)
- `innerText` gây **layout recalculation** → chậm nếu gọi nhiều lần trong loop
- Cả 2 đều **escape HTML** — `<b>` hiện thành text literal, không phải in đậm
- `innerText` có thể không hoạt động đồng nhất trên Safari cũ

## 💡 Khi nào dùng
- Gán user-generated content → ưu tiên `textContent` (an toàn + nhanh)
- Đọc text hiển thị thực tế cho UX (tooltip, counter) → `innerText`
- Clone/nối text node → `document.createTextNode()`

## 🎯 Ví dụ minh họa

### So sánh textContent vs innerText
```js
const el = document.querySelector(".container");
// <div class="container">Hello <span style="display:none">Hidden</span> World</div>

console.log(el.textContent); // "Hello Hidden World" (bao gồm hidden)
console.log(el.innerText);   // "Hello World" (bỏ hidden do CSS)
```

### Gán an toàn (chống XSS)
```js
const userInput = prompt("Nhập tên:");
// AN TOÀN — escapes < > & " '
const greeting = document.createElement("p");
greeting.textContent = "Xin chào, " + userInput;
document.body.appendChild(greeting);

// NGUY HIỂM — nếu userInput chứa <script>
// greeting.innerHTML = "Xin chào, " + userInput; // KHÔNG DÙNG
```

### Tạo text node thủ công
```js
const textNode = document.createTextNode("Nội dung mới");
const p = document.createElement("p");
p.appendChild(textNode);
```

## 📚 Tham khảo & Bài tập
- File: `app.js`, `index.html` trong folder `5_text/`
- Thực hành: so sánh tốc độ `textContent` vs `innerText` trong vòng lặp 10000 lần
- Câu hỏi: Tại sao gán `innerHTML` từ input người dùng dễ bị XSS?
