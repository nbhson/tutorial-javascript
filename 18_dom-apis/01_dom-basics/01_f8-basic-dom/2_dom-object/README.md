# Bài 2 — DOM Object: Thông Tin Document

## 🔑 Khái niệm

Ngoài việc lấy element, `document` còn cung cấp nhiều thuộc tính mô tả **trạng thái trang hiện tại**. Những thuộc tính này phản ánh metadata mà browser tự cập nhật.

| Thuộc tính | Kiểu | Mô tả |
|---|---|---|
| `document.title` | `string` | Tiêu đề `<title>`, đọc/ghi được |
| `document.URL` | `string` | URL đầy đủ của trang |
| `document.domain` | `string` | Tên miền (không có path) |
| `document.location` | `Location` object | Đối tượng `Location` đầy đủ, gán được để navigate |
| `document.cookie` | `string` | Cookie của trang (read/write) |
| `document.referrer` | `string` | URL trang người dùng đến trước đó |
| `document.lastModified` | `string` | Ngày sửa đổi cuối (theo UTC) |

## ✅ Điểm mạnh
- Đọc/giữ được cả 5 thuộc tính trên mà không cần query selector
- `document.location` gán giá trị = redirect trang (`location.href = "/new"` )
- `document.referrer` hữu ích cho analytics, back button logic

## ⚠️ Lưu ý
- `document.URL` có encode `%20` etc, dùng `document.location.href` cho URL đã decode
- `document.cookie` chỉ đọc được cookie không có flag `HttpOnly`
- `document.lastModified` có thể sai nếu server cache không cập nhật timestamp

## 💡 Khi nào dùng
- Debugging: log metadata trang khi test
- Redirect động dựa trên điều kiện
- Lấy referrer để hiển thị "Bạn đang đến từ..."

## 🎯 Ví dụ minh họa

### Thông tin trang
```js
const info = {
  url: document.URL,
  title: document.title,
  domain: document.domain,
  lastModified: document.lastModified,
  referrer: document.referrer || "(trang mới)",
};
console.table(info);
```

### Redirect bằng location
```js
// Chuyển hướng sau 3 giây
setTimeout(() => {
  document.location.href = "https://example.com";
}, 3000);
```

### Đọc/ghi cookie
```js
document.cookie = "theme=dark; max-age=86400; path=/";
console.log(document.cookie); // "theme=dark"
```

## 📚 Tham khảo & Bài tập
- File: `2.Dom-object.js` trong folder `2_dom-object/`
- Thực hành: tạo button "Đổi tiêu đề" gọi `document.title = "..."`
- Câu hỏi: Tại sao `document.cookie` không hiện cookie HttpOnly?
