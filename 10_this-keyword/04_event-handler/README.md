# `this` trong event handler

## 🔑 Khái niệm

Khi bạn đăng ký một listener bằng `addEventListener` hoặc `element.onclick`, trình duyệt sẽ gọi callback như **method của element**: bên trong callback, `this` chính là **element đã kích hoạt sự kiện**.

```js
button.addEventListener("click", function () {
  this; // → button (element)
});
```

Điều này hữu ích khi bạn muốn biết **chính xác element nào** được click mà không cần `event.target`. Lưu ý: hành vi này chỉ đúng với **function thường**. Nếu dùng **arrow function** thì `this` không phải element mà là `this` của scope bên ngoài (xem bài arrow-function).

## ✅ Điểm mạnh

- Truy cập element kích hoạt sự kiện mà không cần truyền tham số hay dùng `event.target`.
- Kết hợp với event delegation để xử lý nhiều element bằng một listener duy nhất.
- Tái sử dụng một handler cho nhiều element — `this` tự động trỏ đúng element.
- Cú pháp ngắn gọn, trực quan khi làm việc với DOM.

## ⚠️ Lưu ý / Hạn chế

- `this` là element chứ **không phải** object bạn định nghĩa handler trong đó — lỗi rất hay gặp khi gắn `obj.handler` làm listener.
- Arrow function trong listener **không nhận** `this` từ element; hãy dùng `event.target` nếu cần.
- Khi dùng `onclick` (property) thay vì `addEventListener`, về cơ bản `this` vẫn là element, nhưng chỉ gắn được một handler.
- Nếu listener được gọi qua `bind`, `this` sẽ bị ép theo giá trị đã bind.

## 💡 Khi nào dùng

- Xử lý click, hover, focus... của button, input, menu item.
- Ghi log hoặc đổi style cho chính element vừa được tương tác.
- Event delegation: một listener trên container, dùng `this`/`event.target` để tìm phần tử con.

## 🎯 Ví dụ minh họa

```js
// mô phỏng cách addEventListener gọi callback với this = element
const btn = { name: "btn", id: 1 };

function addListener(el, cb) {
  cb.call(el); // this bên trong cb = el
}

function handle() {
  console.log(this === btn); // → true
}
addListener(btn, handle);
```

## 📚 Tham khảo / Bài tập

- Mở `04_event-handler/index.html` (kèm `app.js`) trong trình duyệt: file minh họa `this` ở **global scope** (`this === globalThis`) — nền tảng của default binding.
- Tự thử: thêm một nút `<button>` vào file rồi viết `btn.onclick = function () { console.log(this); }`, click và xem `this` in ra chính là element đó.