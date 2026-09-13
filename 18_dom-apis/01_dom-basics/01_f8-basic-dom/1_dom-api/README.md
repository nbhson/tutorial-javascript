# Bài 1 — DOM API: Einstieg Vào DOM

## 🔑 Khái niệm

**DOM (Document Object Model)** là biểu diễn cây của một tài liệu HTML trong bộ nhớ trình duyệt. Mỗi thẻ HTML, mỗi đoạn text, mỗi comment đều là một **node** trong cây. `document` là gateway chính để truy cập DOM từ JavaScript.

Cấu trúc cơ bản:
```
document                     ← Document Node (nodeType 9)
 └─ <html>                   ← Element Node (nodeType 1)
     ├─ <head>               ← Document.head
     │   └─ <title>...</title>
     └─ <body>               ← Document.body
         ├─ <h1 id="title">Hello</h1>
         └─ <div class="box">...</div>
```

Các thuộc tính quan trọng trên `document`:
| Thuộc tính | Trả về |
|---|---|
| `document.documentElement` | Thẻ `<html>` |
| `document.head` | Thẻ `<head>` |
| `document.body` | Thẻ `<body>` |
| `document.title` | Tiêu đề trang (đọc/ghi) |
| `document.URL` | URL hiện tại |
| `document.domain` | Tên miền |

## ✅ Điểm mạnh
- Không cần thư viện, native browser — hoạt động trên mọi trình duyệt hiện đại
- `getElementById` chạy O(1) — nhanh nhất trong mọi selector
- Cấu trúc cây rõ ràng → dễ debug qua DevTools (tab Elements)

## ⚠️ Lưu ý
- `document.getElementById` trả về **single element** hoặc `null` — nếu không tìm thấy sẽ lỗi ngay khi gọi `.xxx` tiếp theo (`Cannot read property of null`)
- DOM manipulation đồng bộ → chặn render main thread nếu quá nhiều lần đổi DOM liên tiếp
- `document` chỉ tồn tại trong browser, **không có trong Node.js** (dùng `jsdom` thay thế khi test)

## 💡 Khi nào dùng
- Lấy phần tử duy nhất theo `id` → dùng `getElementById` (nhanh nhất)
- Truy vấn meta info trang → `document.title`, `document.URL`, `document.cookie`
- Lấy `<body>`, `<head>`, `<html>` để append/remove children động

## 🎯 Ví dụ minh họa

### Lấy và kiểm tra các phần tử root
```js
console.log(document.documentElement.tagName); // "HTML"
console.log(document.head.tagName);            // "HEAD"
console.log(document.body.tagName);            // "BODY"

// Đổi tiêu đề trang
document.title = "Trang mới";
```

### Tránh lỗi `null` phổ biến
```js
const el = document.getElementById("no-exist");
if (el) {
  el.textContent = "An toàn vì đã check null";
} else {
  console.warn("Element không tồn tại");
}
```

### Sử dụng trong thực tế
```js
// Log thông tin trang hiện tại
console.log({
  url: document.URL,
  domain: document.domain,
  title: document.title,
  bodyHeight: document.body.scrollHeight,
  charCount: document.body.innerText.length,
});
```

## 📚 Tham khảo & Bài tập
- File: `1.Html-Dom-Dom-Api.js` — mở bằng Live Server, xem Console
- Thử nghiệm: thay `document.title`, quan sát tab browser đổi tên
- Câu hỏi: `document` có phải là node type 9 không? Dùng `instanceof` kiểm tra
