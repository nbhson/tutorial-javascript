# Shadow DOM — Example 1: Basic Encapsulation

## 🔑 Khái niệm

**Shadow DOM** là kỹ thuật đóng gói markup + style bên trong một "shadow tree" tách biệt khỏi main document DOM. Element chứa shadow tree gọi là **shadow host**.

```js
const host = document.querySelector("#host");
const shadow = host.attachShadow({ mode: "open" | "closed" });
shadow.innerHTML = `<style>.box{color:red}</style><div class="box">Tôi trong shadow</div>`;
```

| Mode | Đặc điểm |
|---|---|
| `open` | `host.shadowRoot` truy cập được từ bên ngoài |
| `closed` | `host.shadowRoot` trả về `null` — encapsulation strict hơn |

## ✅ Điểm mạnh
- Style bên trong **không rò rỉ ra ngoài**, CSS global không ảnh hưởng
- HTML/CSS bên trong **không bị CSS global ghi đè** (trừ `::part` / `::slotted`)
- Basis của **Web Components** — component tự chứa đầy đủ

## ⚠️ Lưu ý
- `closed` không tuyệt đối — vẫn có thể leak qua `inspect()` DevTools
- Shadow DOM không share CSS variables từ host trừ khi define `:host`
- Debug khó hơn một chút vì element bị "ẩn" trong shadow boundary
- Không được iframe sandbox nếu không cho `allow-same-origin`

## 💡 Khi nào dùng
- Web Components tái sử dụng (custom element + shadow)
- Widget nhúng từ bên thứ ba (iframe alternative)
- Design system component cách ly style

## 🎯 Ví dụ minh họa

### Shadow DOM cơ bản
```js
const host = document.getElementById("widget");
const shadow = host.attachShadow({ mode: "open" });

shadow.innerHTML = `
  <style>
    :host { display: block; padding: 16px; }
    .title { color: blue; font-weight: bold; }
  </style>
  <h2 class="title">Shadow Component</h2>
  <p>Nội dung trong shadow DOM, CSS global không ảnh hưởng.</p>
`;
```

### So sánh CSS scope
```html
<!-- Main CSS -->
<style>
  .box { color: green; } /* cái này áp dụng cho host DOM */
</style>

<!-- Shadow CSS -->
<style>
  .box { color: red !important; } /* cái này áp dụng cho shadow DOM */
</style>
```
→ `.box` trong shadow luôn đỏ, `.box` bên ngoài luôn xanh — **không ảnh hưởng lẫn nhau**.

## 📚 Tham khảo & Bài tập
- File: `app.js`, `index.html`, `style.css` trong folder `example1/`
- Thực hành: tạo custom element `<my-card>` dùng shadow DOM
- Câu hỏi: `mode: "closed"` khác gì `"open"` khi debug?
