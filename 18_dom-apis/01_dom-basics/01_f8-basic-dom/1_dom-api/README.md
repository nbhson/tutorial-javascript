# DOM API (Bài 1)

## Khái niệm
`document` là entrypoint vào DOM. `document.documentElement` là `<html>`, `document.body` là `<body>`, `document.head` là `<head>`. `document.getElementById(id)` tìm element theo id.

## Điểm mạnh
- API cơ bản nhất, có sẵn, không cần thư viện
- `getElementById` O(1), nhanh nhất

## Khi nào dùng
- Khi cần lấy element duy nhất theo id để gắn sự kiện hoặc đọc giá trị.

## Ví dụ
```js
const el = document.getElementById("myId");
console.log(el.tagName); // DIV
console.log(document.body.nodeName); // BODY
```

## 📚 Tham khảo
- `1.Html-Dom-Dom-Api.js` — chạy bằng Live Server, mở Console
