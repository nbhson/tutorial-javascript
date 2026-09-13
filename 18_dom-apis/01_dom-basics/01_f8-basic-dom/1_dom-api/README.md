# Bài 1 — DOM API: Einstieg Vào DOM — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

**DOM (Document Object Model)** là biểu diễn cây của một tài liệu HTML trong bộ nhớ trình duyệt. Mỗi thẻ HTML, mỗi đoạn text, mỗi comment đều là một **node** trong cây. `document` là gateway chính để truy cập DOM từ JavaScript.

### Cấu trúc cây DOM

```
document                     ← Document Node (nodeType 9)
 └─ <html>                   ← Element Node (nodeType 1)
      ├─ <head>              ← Document.head
      │   └─ <title>...</title>
      └─ <body>              ← Document.body
          ├─ <h1 id="title">Hello</h1>
          └─ <div class="box">
               ├─ Text node: "Content"  (nodeType 3)
               └─ <span>Inline</span>
```

### Các thuộc tính quan trọng trên `document`

| Thuộc tính | Trả về | Mô tả |
|---|---|---|
| `document.documentElement` | `<html>` element | Phần tử root của cây |
| `document.head` | `<head>` element | Đầu trang (meta, link, script) |
| `document.body` | `<body>` element | Thân trang (content hiển thị) |
| `document.title` | string | Tiêu đề trang (đọc/ghi được) |
| `document.URL` | string | URL đầy đủ của trang (encoded) |
| `document.domain` | string | Tên miền (không có path) |
| `document.location` | Location object | Đối tượng Location đầy đủ, gán được để navigate |
| `document.cookie` | string | Cookie của trang (read/write, không có HttpOnly) |
| `document.referrer` | string | URL trang người dùng đến trước đó |
| `document.lastModified` | string | Ngày sửa đổi cuối (UTC) |

### Node types trong DOM
| nodeType | Giá trị | Ý nghĩa |
|---|---|---|
| 1 | Element | Thẻ HTML `<div>`, `<p>`, v.v. |
| 3 | Text | Văn bản trong element |
| 8 | Comment | `<!-- comment -->` |
| 9 | Document | Gốc cây DOM |
| 11 | DocumentFragment | Container tạm thời |

## 📐 Cấu trúc / Cú pháp

### Truy cập document properties
```js
// Root elements
console.log(document.documentElement.tagName); // "HTML"
console.log(document.head.tagName);            // "HEAD"
console.log(document.body.tagName);            // "BODY"

// Metadata
console.log(document.title);        // đọc tiêu đề
document.title = "Trang mới";       // đổi tiêu đề (visible trên tab)
console.log(document.URL);          // URL đầy đủ
console.log(document.domain);       // tên miền
console.log(document.referrer);     // trang đến trước
console.log(document.lastModified); // ngày sửa đổi
```

### Kiểm tra null — tránh lỗi phổ biến
```js
const el = document.getElementById("no-exist");
if (el) {
  el.textContent = "An toàn vì đã check null";
} else {
  console.warn("Element không tồn tại — có thể DOM chưa sẵn sàng");
}
```

### Trang information object
```js
console.log({
  url: document.URL,
  domain: document.domain,
  title: document.title,
  bodyHeight: document.body.scrollHeight,
  charCount: document.body.innerText.length,
  cookieCount: document.cookie.split(';').length
});
```

## ✅ Điểm mạnh

1. **Không cần thư viện** — native browser, hoạt động trên mọi trình duyệt hiện đại.
2. **`getElementById` chạy O(1)** — nhanh nhất trong mọi selector, dùng khi có id.
3. **Cấu trúc cây rõ ràng** — dễ debug qua DevTools (tab Elements), nhìn thấy hierarchy.
4. **Document properties phản ánh real-time** — `document.title`, `document.URL` luôn update theo trạng thái trang.
5. **`document.location` gán được** — redirect trang `location.href = "/new"` đơn giản.
6. **`document.cookie` read/write** — quản lý cookie từ JS (trừ HttpOnly).
7. **`document.referrer` hữu ích** — analytics, back button logic, know where user came from.

## ⚠️ Bẫy thường gặp & Hạn chế

1. **`getElementById` trả null nếu không tìm thấy** — gọi `.xxx` tiếp theo sẽ lỗi "Cannot read properties of null". Luôn check null trước.
2. **DOM manipulation đồng bộ** — nếu quá nhiều lần đổi DOM liên tiếp gây reflow/render lại → giật. Batch changes.
3. **`document` chỉ tồn tại trong browser** — không có trong Node.js (dùng `jsdom` thay thế khi test).
4. **`document.URL` có encode `%20`** — dùng `document.location.href` cho URL đã decode.
5. **`document.cookie` không hiện HttpOnly cookies** — security restriction của browser.
6. **`document.lastModified` có thể sai** — nếu server cache không cập nhật timestamp.
7. **DOMContentLoaded vs load** — `document` object tồn tại sớm, nhưng children có thể chưa fully parsed. Dùng `DOMContentLoaded` event để đảm bảo.

## 💡 Khi nào dùng — Tình huống thực tến

1. **Lấy phần tử duy nhất theo id** → dùng `getElementById` (nhanh nhất).
2. **Truy vấn meta info trang** → `document.title`, `document.URL`, `document.cookie`.
3. **Lấy `<body>`, `<head>`, `<html>`** để append/remove children động.
4. **Redirect động** → `document.location.href = "/new-page"`.
5. **Hiển thị "Bạn đang đến từ..."** → `document.referrer`.
6. **Đổi tiêu đề tab** dynamically → `document.title = "New Title"`.
7. **Debug metadata trang** → log `document.URL`, `document.domain`, `document.body.scrollHeight`.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Lấy và kiểm tra các phần tử root
```js
console.log(document.documentElement.tagName); // "HTML"
console.log(document.head.tagName);            // "HEAD"
console.log(document.body.tagName);            // "BODY"

// Đổi tiêu đề trang
document.title = "Trang mới";
console.log(document.title); // "Trang mới"
```

### Ví dụ 2: Tránh lỗi null phổ biến
```js
const el = document.getElementById("no-exist");
if (el) {
  el.textContent = "An toàn vì đã check null";
} else {
  console.warn("Element không tồn tại");
  // Có thể: khởi tạo element thay thế, hoặc skip operation
}
```

### Ví dụ 3: Sử dụng trong thực tế — trang info dashboard
```js
function logPageInfo() {
  console.log({
    url: document.URL,
    domain: document.domain,
    title: document.title,
    bodyHeight: document.body.scrollHeight,
    bodyWidth: document.body.clientWidth,
    charCount: document.body.innerText.length,
    elementCount: document.body.children.length,
    lastModified: document.lastModified,
    referrer: document.referrer || "(trang mới)"
  });
}
logPageInfo();
```

### Ví dụ 4: Redirect dựa trên điều kiện
```js
function redirectBasedOnTime() {
  const hour = new Date().getHours();
  if (hour < 8 || hour >= 22) {
    document.location.href = "/night-mode";
  }
}
redirectBasedOnTime();
```

### Ví dụ 5: Set cookie và đọc lại
```js
function setThemeCookie(theme) {
  document.cookie = `theme=${theme}; max-age=86400; path=/`;
}
function getThemeCookie() {
  const match = document.cookie.match(/(?:^|;)theme=([^;]*)/);
  return match ? match[1] : 'light';
}
setThemeCookie('dark');
console.log(getThemeCookie()); // "dark"
```

### Ví dụ 6: Kiểm tra DOM readiness
```js
// Cách 1: DOMContentLoaded — DOM parse xong
document.addEventListener('DOMContentLoaded', () => {
  console.log('DOM ready — elements available');
  const el = document.getElementById('app');
  console.log('Element found:', !!el);
});

// Cách 2: window.load — mọi tài nguyên xong
window.addEventListener('load', () => {
  console.log('All resources loaded — images have dimensions');
  const img = document.querySelector('img');
  console.log('Image natural size:', img?.naturalWidth, 'x', img?.naturalHeight);
});
```

## 🔗 Liên kết chéo

- Xem thêm: `18_dom-apis/01_dom-basics/01_f8-basic-dom/2_dom-object/` — chi tiết document properties.
- Xem thêm: `18_dom-apis/01_dom-basics/01_f8-basic-dom/3_element/` — element selection methods.
- Xem thêm: `18_dom-apis/01_dom-basics/02_how-browser-reads-html/` — rendering pipeline.
- File tham khảo: `1.Html-Dom-Dom-Api.js` — mở bằng Live Server, xem Console.
