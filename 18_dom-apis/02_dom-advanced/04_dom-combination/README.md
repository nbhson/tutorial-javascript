# DOM Combination — Kết Hợp Nhiều Loại DOM

## 🔑 Khái niệm

Virtual DOM và Shadow DOM giải quyết **hai bài toán khác nhau** — chúng không loại trừ nhau:

- **Virtual DOM** tối ưu **hiệu năng cập nhật**: giảm số lần đụng DOM thật bằng cách diff → patch tối thiểu.
- **Shadow DOM** tạo **encapsulation**: cô lập CSS và cây con của một component khỏi trang.

Không có lý do gì để chỉ chọn một. Trong một ứng dụng thực tế bạn có thể **kết hợp cả ba tầng**:

1. **Virtual DOM** ở tầng ứng dụng (React/Vue) quyết định "state thay đổi → UI nào cần sửa".
2. **DOM Manipulation** ở tầng render thực thi — `appendChild`, đổi `textContent`, `innerHTML`.
3. **Shadow DOM** ở tầng component (Web Components riêng biệt, widget của bên thứ ba) bọc kín giao diện con.

Ví dụ trong `README` hiện tại chính là demo như vậy: một trang có `#app-container` được **Virtual DOM-style render** (hàm `renderVirtualDOM(count)` viết lại toàn bộ `innerHTML` theo biến `count`, bấm nút thì tăng và render lại), cạnh đó một `#shadow-root-container` dùng **`attachShadow({ mode: "open" })`** để dựng nội dung cô lập (style `p { color: blue }` chỉ áp dụng trong shadow). Hai mảng DOM này cùng nằm trong một trang mà không xung đột.

Tóm lược: *Virtual DOM = tối ưu cập nhật*; *Shadow DOM = cô lập và tái sử dụng*; biết kết hợp là kỹ năng của frontend thực chiến.

## ✅ Điểm mạnh

- **Lợi ích kép**: cập nhật nhanh (Virtual DOM) + component an toàn, đóng gói (Shadow DOM).
- **Giảm xung đột khi integrate**: widget Shadow DOM không bị CSS của Virtual DOM app làm hỏng.
- **Tái sử dụng xuyên dự án**: component "bọc kín" nhập vào bất kỳ React/Vue app nào.
- **Tách trách nhiệm rõ**: ai lo render, ai lo cô lập — dễ bảo trì.
- **Lộ trình giải thích framework**: hiểu vì sao khái niệm này đi cùng nhau trong thực tế.

## ⚠️ Lưu ý / Hạn chế

- **Đừng "cắm" Virtual DOM chồng Shadow DOM cùng chỗ một cách dư thừa** — trong trang demo, mỗi phần dùng đúng loại phù hợp.
- Shadow DOM **cản trở diff của framework** nếu framework định vẽ trực tiếp vào bên trong — cần qua slot/composed khéo léo.
- Virtual DOM render toàn bộ bằng `innerHTML` (như demo) làm **mất focus/đổi state form**, không đúng bản chất "patch từng phần" — về sau nên diff như `example1/helper.js`.
- Tăng độ phức tạp codebase khi phối hai hệ.

## 💡 Khi nào dùng

- App chính dùng **Virtual DOM (React/Vue)** nhưng cần nhúng **widget/bộ sưu tập Web Components** có Shadow DOM.
- Xây **micro-frontend / plugin** — mỗi plugin là component đóng gói, phần layout chung dùng Virtual DOM.
- Thiết kế **giao diện ghép nối**: bảng điều khiển (Virtual DOM) + popup/badge thành phần riêng (Shadow DOM).
- Gradual migration — giữ widget cũ (Shadow DOM) bên trong app mới (Virtual DOM).

## 🎯 Ví dụ minh họa

```js
// Phần "Virtual DOM-style": mỗi state đổi -> render lại vùng container
let count = 0;
function render() {
  container.innerHTML = `
    <p>Số lần click: ${count}</p>
    <button>Click me</button>`;
}
// (thực chất bạn sẽ diff & patch như example1/helper.js ⟶)

// Phần Shadow DOM: nội dung cô lập, style riêng không chạm nhau
const shadowHost = document.createElement('div');
const root = shadowHost.attachShadow({ mode: 'open' });
root.innerHTML = '<style>p{color:blue}</style><p>inside Shadow DOM</p>';
document.body.appendChild(shadowHost);
```

## 📚 Tham khảo / Bài tập

- Đọc lại code đoạn combo trong `README.md` của thư mục này — đặc biệt hai khối: `renderVirtualDOM(count)` và `attachShadow({ mode: 'open' })` (chạy thử bằng cách dán vào Console một trang trống hoặc viết `index.html` tạm).
- Tự làm: nâng cấp phần "Virtual DOM" trong demo sang dùng **diff/patch thật** như `03_virtual-dom/example1/helper.js` (chỉ sửa text `count`), giữ nguyên phần Shadow DOM.
- Tự làm: thêm một `custom-widget` (Shadow DOM) vào bên trong `#app-container` của Virtual DOM — kiểm tra click + style không bị ảnh hưởng lẫn nhau.
- Tự làm: để một `input` HTML có value, render Virtual DOM bằng `innerHTML` rồi bấm nút — quan sát `input` bị "reset focus/value", minh họa lý do framework phải patch thay vì render lại toàn bộ.
- So sánh lại bảng: **Virtual DOM → hiệu năng cập nhật; Shadow DOM → cô lập/ tái sử dụng**.