# DOM APIs — Cơ bản

## 🔑 Khái niệm

Phần này xây nền móng cho toàn bộ DOM. Gồm hai nhóm:

- **01_f8-basic-dom** — chuỗi **12 bài thực hành** (theo lộ trình F8) từ nền tảng đến sự kiện: HTML DOM & DOM API → `document` object → chọn element → attribute → text → `innerHTML/outerHTML` → node property → style → class → sự kiện → `preventDefault`/`stopPropagation` → `EventListener`.
- **02_how-browser-reads-html** — **rendering pipeline**: trình duyệt nhận HTTP → parse HTML → dựng **DOM Tree + CSSOM** → kết hợp thành **Render Tree** → layout → paint → JS execution → `load`. Kèm nhiều ảnh minh họa (`DOM.png`, `HTML-Parsing.png`, `Painting-Phase*.png`, `node-structure-in-dom.png`).

Mấu chốt cần nắm ở phần cơ bản:

- **DOM là gì**: mô hình cây do W3C định nghĩa; **DOM API** là tập Web API truy xuất/chỉnh sửa cây đó.
- **Node vs Element**: node bao gồm element, text, comment; element chỉ là thẻ HTML.
- Cách **chọn phần tử**: `getElementById` (nhanh, 1 phần tử), `getElementsByClassName`/`getElementsByTagName` (HTMLCollection), `querySelector`/`querySelectorAll` (chọn theo CSS selector, trả NodeList).
- Cách **sửa nội dung**: `textContent`, `innerText`, `innerHTML`, `outerHTML`, `style`, `classList`.

## ✅ Điểm mạnh

- **Học theo cấp độ**: 12 bài đi từ "DOM là gì" đến "sự kiện hoạt động thế nào" — không bỏ sót nền tảng.
- **Thực hành ngay**: mỗi bài có `app.js`/`index.html` sẵn, chạy trong browser để xem kết quả.
- **Bắt nhịp diff cho framework**: hiểu render pipeline trước khi học React/Vue.
- **Kiến thức tổ chức theo mảng**: selector, attribute, text, style, class, event — đúng thứ tự hay dùng.

## ⚠️ Lưu ý / Hạn chế

- `innerHTML` với dữ liệu người dùng gốc = **lỗ hổng XSS** — nên dùng `textContent` khi chỉ cần text.
- `querySelectorAll` trả **NodeList tĩnh**, không phải array — muốn dùng `map` cần `Array.from`.
- `innerText` (theo những gì *hiển thị*) khác `textContent` (theo nguồn HTML) — dễ nhầm.
- `classList.toggle/add/remove` an toàn hơn sửa trực tiếp `className` khi có nhiều class.

## 💡 Khi nào dùng

- Bạn **mới học DOM** hoặc cần ôn lại nền tảng trước khi làm UI phức tạp.
- Cần chọn/sửa phần tử **tự động trong trang** (thêm class, đổi text, thay attribute).
- Muốn hiểu **vì sao trình duyệt vẽ lại trang** khi bạn sửa DOM.
- Sof tảng để hiểu các khái niệm nâng cao ở `02_dom-advanced`.

## 🎯 Ví dụ minh họa

```js
// Chọn + đổi text (5_text/app.js)
const heading = document.querySelector('h1');
console.log(heading.innerText);      // text hiển thị
heading.innerText = '<i>Mới</i>';    //NHẬP LÀ text, không render tag

// Node vs Element (7_node-property/app.js)
const box = document.querySelector('.box');
box.childNodes.length;   // kể cả text node
box.children.length;     // chỉ element
```

## 📚 Tham khảo / Bài tập

- Trong `01_f8-basic-dom`, chạy tuần tự 12 bài: `1_dom-api` → `12_EventListener`. Với mỗi bài mở `index.html` trong trình duyệt (và Console DevTools) — một số file như `2_dom-object/2.Dom-object.js` chỉ log trực tiếp.
- Đọc `02_how-browser-reads-html` kèm các ảnh để nắm pipeline: `DOM.png`, `HTML-Parsing.png`, `Painting-Phase*.png`, `node-structure-in-dom.png`.
- Tự làm: chọn một trang bất kỳ, dùng Console thử `document.querySelector('h1').textContent`, `...querySelectorAll('a').length`, đổi màu bằng `element.style.color = 'red'`.
- Tự làm: bài 5 — so sánh rõ `innerText` vs `textContent` khi dùng một element chứa thẻ `<b>`; bài 12 — thử `removeEventListener` với callback đặt tên.