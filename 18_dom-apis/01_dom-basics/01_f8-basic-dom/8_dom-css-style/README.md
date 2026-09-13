# DOM CSS Style (Bài 8)

## Khái niệm
Đọc/ghi CSS qua `element.style.property`. Thuộc tính camelCase (ví dụ `backgroundColor`), đọc computed qua `getComputedStyle(el)`.

## Điểm mạnh
- Thay đổi style tức thì, không cần class
- `getComputedStyle` trả giá trị thực tế sau khi CSS cascade

## Khi nào dùng
- Animation/transition động; toggle style theo user action.

## Ví dụ
```js
const box = document.querySelector(".box");
box.style.width = "100px";
box.style.backgroundColor = "red";
const styles = getComputedStyle(box);
console.log(styles.width);
```

## 📚 Tham khảo
- `app.js`, `index.html`
