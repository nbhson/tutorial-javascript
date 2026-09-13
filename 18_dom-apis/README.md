# DOM APIs — Tổng quan

## 🔑 Khái niệm

**DOM (Document Object Model)** là biểu diễn cây mà trình duyệt dựng từ tài liệu HTML — mỗi thẻ HTML trở thành một **node**, mỗi node có quan hệ cha/con, và toàn bộ cây treo dưới gốc `document`. **DOM API** là tập Web API mà JS dùng để *truy xuất và chỉnh sửa* cây này: tìm element (`getElementById`, `querySelector`), sửa nội dung (`textContent`, `innerHTML`), thêm/xóa node (`appendChild`, `remove`), gắn sự kiện (`addEventListener`)...

Các lớp kiến thức trong nhóm này được chia làm ba phần:

- **01_dom-basics** — fundamentals: cây DOM, cách trình duyệt đọc HTML để dựng DOM/CSSOM/Render Tree.
- **02_dom-advanced** — nâng cao phục vụ framework: DOM Manipulation, Shadow DOM, Virtual DOM, kết hợp các loại DOM, và **reactivity**.
- **03_events** — sự kiện DOM: `addEventListener`, bubbling/capturing, preventDefault/stopPropagation, event delegation.

Một vài khái niệm nền quan trọng:

- **Node vs Element**: *Node* là khái niệm cha (element, text, comment, attribute đều là node); *Element* chỉ riêng thẻ HTML. API như `childNodes` (mọi node) khác `children` (chỉ element).
- **Bubble vs Capture**: sự kiện lan theo hai pha — từ `window` đi xuống (capturing) rồi từ phần tử đích đi ngược lên (bubbling); `stopPropagation()` dừng đường lan truyền.
- **Shadow DOM**: encapsulation — cây DOM riêng biệt bên trong một element, CSS/DOM cô lập khỏi trang.
- **Virtual DOM**: bản sao ảo để **diff và cập nhật tối thiểu** lên DOM thật (React).
- **Reactivity**: hệ thống tự động đồng bộ data → UI (Proxy + re-render).

## ✅ Điểm mạnh

- **Tương tác trực tiếp, linh hoạt**: sửa bất kỳ phần nào của trang mà không cần tải lại.
- **Chuẩn Web API**: chạy trên mọi trình duyệt, không cần framework.
- **Nền tảng cho mọi UI framework**: React/Vue/Angular đều xoay quanh DOM (qua Virtual DOM / reactivity).
- **Kiểm soát sự kiện mịn**: bubbling + delegation giảm số listener, dễ quản lý.
- **Encapsulation có sẵn** qua Shadow DOM giúp build component tái sử dụng an toàn.

## ⚠️ Lưu ý / Hạn chế

- **Hiệu năng**: sửa DOM quá nhiều (trong vòng lặp) gây **reflow/render lại** → giật.
- **Cần kiểm tra tồn tại**: `querySelector` trả `null` nếu không tìm thấy — quên check dễ lỗi "Cannot read properties of null".
- `nodeList` từ `querySelectorAll` **không phải array** — cần `Array.from` hoặc `...` trước khi dùng `map/filter`.
- Virtual DOM thêm overhead (tạo diff); DOM thao tác tay khó bảo trì khi cây lớn.

## 💡 Khi nào dùng

- **Ứng dụng nhỏ / prototype** — thao tác DOM trực tiếp nhanh hơn cài framework.
- **Thêm tính năng nhỏ** vào trang có sẵn (tự động fill, validate form, đếm lượt click).
- **Web Components** (Shadow DOM) — đóng gói UI tái sử dụng cho nhiều dự án.
- **Toàn bộ ứng dụng phức tạp** — dùng framework (Virtual DOM + reactivity) để dễ bảo trì.
- **Debug & optimize** — nắm DOM để đo Performance và sửa các vấn đề layout/reflow.

## 🎯 Ví dụ minh họa

```js
// Tìm -> đổi nội dung -> gắn sự kiện
const btn = document.querySelector('#myButton');
btn.textContent = 'Đã click';
btn.addEventListener('click', () => console.log('clicked!'));

// node vs element
const el = document.querySelector('ul');
console.log(el.childNodes.length); // kể cả text node (xuống dòng, khoảng trắng)
console.log(el.children.length);    // chỉ đếm thẻ <li>
```

## 📚 Tham khảo / Bài tập

- Bắt đầu từ `01_dom-basics/01_f8-basic-dom` (12 bài: từ `1_dom-api` đến `12_EventListener`) rồi `02_how-browser-reads-html` (rendering pipeline).
- Sang `02_dom-advanced`: chạy các ví dụ thao tác trong `01_manipulation`, xem encapsulation trong `02_shadow-dom`, diff trong `03_virtual-dom`, so sánh trong `04_dom-combination`, reactivity trong `05_reactivity`.
- Ôn sự kiện với `03_events`.
- Tự làm: viết một danh sách to-do nhỏ thuần DOM dựa trên mẫu `02_dom-advanced/01_manipulation/example-2` (thêm/xóa task bằng `createElement` + `remove` + `addEventListener`).