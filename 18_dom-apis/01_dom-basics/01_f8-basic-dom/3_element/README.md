# DOM Element (Bài 3)

## Khái niệm
Element là node loại ELEMENT_NODE (nodeType === 1). Lấy qua `getElementById`, `querySelector`, `getElementsByTagName`, `getElementsByClassName`.

## Điểm mạnh
- `querySelector` hỗ trợ CSS selector linh hoạt
- `getElementsByTagName` trả HTMLCollection live

## Khi nào dùng
- Khi cần lấy nhiều element theo class/tag hoặc selector phức tạp.

## Ví dụ
```js
const h1 = document.querySelector("h1");
const items = document.getElementsByClassName("item");
const divs = document.getElementsByTagName("div");
```

## 📚 Tham khảo
- `app.js`, `index.html` — chạy Live Server
