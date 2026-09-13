# DOM Object (Bài 2)

## Khái niệm
`document` là một đối tượng DOM, bất kỳ thẻ HTML nào trong cây đều là DOM Node/Element. Có thể truy cập qua `document.URL`, `document.title`, `document.domain`.

## Điểm mạnh
- Trực tiếp, phản ánh trạng thái HTML
- Đọc nhanh, đơn giản

## Khi nào dùng
- Debug meta info trang (title, URL, domain)
- Đọc thuộc tính document cấu hình

## Ví dụ
```js
console.log(document.title);
console.log(document.domain);
console.log(document.URL);
```

## 📚 Tham khảo
- `2.Dom-object.js`
