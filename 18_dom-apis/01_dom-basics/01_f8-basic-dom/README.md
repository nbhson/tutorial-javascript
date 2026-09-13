# F8 Basic DOM — 12 Bài Nền Tảng

## 🔑 Khái niệm

Chuỗi **12 bài thực hành** (phong cách F8) đi từ khái niệm đến nâng cao về DOM. Mỗi thư mục con là một bài với code mở sẵn — hầu hết gồm `app.js` + `index.html`, bạn mở `index.html` trên trình duyệt và bấm Console để xem output.

| # | Thư mục | Chủ đề | File chính |
|---|---------|--------|-----------|
| 1 | `1_dom-api` | HTML DOM là gì, DOM API là gì | `1.Html-Dom-Dom-Api.js` |
| 2 | `2_dom-object` | `document` — object gốc của DOM | `2.Dom-object.js` |
| 3 | `3_element` | Chọn element (id/class/tag/selector) | `app.js` + `index.html` |
| 4 | `4_attribute` | Thao tác attribute (`set/getAttribute`) | `app.js` + `index.html` |
| 5 | `5_text` | `innerText` vs `textContent` | `app.js` + `index.html` |
| 6 | `6_innerHTML-outerHTML` | Sửa nội dung / thẻ bao ngoài | `app.js` + `index.html` |
| 7 | `7_node-property` | Node property (`childNodes`, `children`, `sibling`...) | `app.js` + `index.html` |
| 8 | `8_dom-css-style` | Đổi style qua `element.style`, `Object.assign` | `app.js` + `index.html` |
| 9 | `9_class-property` | `classList.add/remove/contains/toggle` | `app.js` + `index.html` |
| 10 | `10_dom-event` | Gán sự kiện (`onclick`), object `MouseEvent` | `app.js` + `index.html` |
| 11 | `11_PreventDefault-StopPropagation` | Chặn hành vi mặc định & chặn nổi bọt | `app.js` + `index.html` |
| 12 | `12_EventListener` | `addEventListener`/`removeEventListener` | `app.js` + `index.html` |

Điểm mấu chốt để bật ra ngay:
- **HTML DOM**: chuẩn mô hình do W3C; **DOM API**: bộ Web API để JS truy/xuất và chỉnh sửa model đó.
- `document` là object đại diện toàn bộ website — mọi truy cập đều qua nó.
- `innerHTML` phân tích thẻ HTML; `innerText`/`textContent` chỉ là text (bài 5).
- **Node ≠ Element**: `childNodes` tính cả "text node"; `children` chỉ tính element (bài 7).
- Sự kiện: `onclick` gán được một handler; `addEventListener` cho nhiều handler và có thể gỡ (bài 10, 12).

## ✅ Điểm mạnh

- **Lộ trình bài bản**: 12 bước từ lý thuyết tới sự kiện, đúng chuỗi phụ thuộc kiến thức.
- **Mỗi bài có code chạy được**: workflow mở `index.html` → xem Console → sửa thử, không cần cài đặt.
- **Ghi chú ngay trong code**: các comment giải thích cặn kẽ từng dòng, tiện tự học.
- **Bao phủ đủ API tần suất cao**: selector, attribute, text, HTML, style, class, event — thứ bạn code hàng ngày.
- **Chuẩn bị nền tảng DOM nâng cao** cho `02_dom-advanced` và events chuyên sâu trong `03_events`.

## ⚠️ Lưu ý / Hạn chế

- `getElementsByClassName`/`getElementsByTagName` trả **HTMLCollection sống**; `querySelectorAll` trả **NodeList tĩnh** — đừng nhầm khi dùng `length` hay `map`.
- `setAttribute(name, value)` mới cho phép attribute **không chuẩn**; các thuộc tính hợp lệ thì buộc qua setter trực tiếp (`link.href = ...`).
- `innerText` (bài 5) đọc theo **cái hiển thị**, còn setter `innerText` lại hoạt động như đặt text; sự lệch này hay bẫy người mới.
- Quên `event.stopPropagation()` trong bài 11 khiến sự kiện vẫn lan lên phần tử cha.

## 💡 Khi nào dùng

- Bắt đầu học DOM hoặc **ôn nhanh** trước khi bước vào DOM nâng cao/framework.
- Cần mẫu thao tác cụ thể: sửa text, đổi class theo điều kiện, đổi style qua `Object.assign`.
- Code trong công việc hàng ngày cần nhớ lại cách dùng `classList.toggle` / `removeEventListener` / `preventDefault`.
- Làm giáo án / hướng dẫn học viên đi từng bước nhỏ dễ hiểu.

## 🎯 Ví dụ minh họa

```js
// Bài 10 — gán sự kiện qua element node
const h = document.querySelector('h1').nextElementSibling;
h.onclick = function (e) {
  console.log(e);                  // MouseEvent đầy đủ thông tin
  h.style.color = 'red';
};

// Bài 11 — chặn hành vi mặc định link
for (const a of document.links) {
  a.onclick = (e) => {
    if (e.target.href !== "http://facebook.com/") e.preventDefault();
  };
}

// Bài 12 — nhiều listener + gỡ listener
function viec1() { console.log("Việc 1"); }
btn.addEventListener("click", viec1);
btn.addEventListener("click", () => console.log("Việc 2"));
setTimeout(() => btn.removeEventListener("click", viec1), 5000);
```

## 📚 Tham khảo / Bài tập

- Chạy tuần tự các bài có `index.html` trên trình duyệt (mở Console F12 để xem log); các bài chỉ có `.js` (bài 1, 2) chạy trực tiếp bằng `node` hoặc dán vào Console.
- Tự làm bài 3: thử `document.querySelectorAll("html .content h3:nth-child(2)")` rồi đếm `length`.
- Tự làm bài 5: chèn `<i>New heading</i>` qua `textContent` và `innerHTML` để thấy khác biệt.
- Tự làm bài 8: dùng `Object.assign(boxElement.style, {...})` để đổi nhiều style một lúc.
- Tự làm bài 11: thêm nhiều `ul li` và bấm để thấy bubbling dừng lại khi có `stopPropagation()` ở button.