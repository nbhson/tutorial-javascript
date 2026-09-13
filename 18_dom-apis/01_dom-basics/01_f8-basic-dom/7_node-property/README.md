# Node Property (Bài 7)

## Khái niệm
Mỗi node có: `nodeType` (1=Element, 3=Text, 8=Comment, 9=Document), `nodeName`, `nodeValue`. `childNodes` trả NodeList, `children` trả HTMLCollection (chỉ element).

## Điểm mạnh
- Phân biệt node vs element rõ ràng
- `children` lọc sẵn chỉ element, tiện hơn `childNodes`

## Khi nào dùng
- Duyệt cây DOM chi tiết; kiểm tra text node trống.

## Ví dụ
```js
const div = document.querySelector("div");
console.log(div.nodeType, div.nodeName); // 1 DIV
console.log(div.children.length);
console.log(div.childNodes.length);
```

## 📚 Tham khảo
- `app.js`, `index.html`
