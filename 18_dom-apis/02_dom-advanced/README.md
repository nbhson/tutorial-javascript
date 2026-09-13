# DOM APIs — Nâng cao

## 🔑 Khái niệm

Phần nâng cao chuẩn bị cho bạn những khái niệm mà mọi framework frontend hiện đại đều xoay quanh. Gồm 5 nhóm:

- **01_manipulation** — kỹ thuật **DOM Manipulation** và các sự kiện trang (`DOMContentLoaded`, `load`, `beforeunload`, `hashchange`, `resize`...) với ví dụ to-do list.
- **02_shadow-dom** — **Shadow DOM**: encapsulation — cây DOM con được cô lập về CSS và cấu trúc khỏi trang chính (nền tảng Web Components).
- **03_virtual-dom** — **Virtual DOM**: biểu diễn ảo của DOM trong bộ nhớ; khi state thay đổi thì tạo cây ảo mới, **diff** với cây cũ, chỉ **patch** phần khác lên DOM thật (đúng tinh thần React).
- **04_dom-combination** — kết hợp Virtual DOM + Shadow DOM trong một ứng dụng (mỗi loại giải quyết một bài toán).
- **05_reactivity** — mức độ "phản ứng tự động": DOM manip (thấp) → Virtual DOM (cao) → Shadow DOM (trung bình-cao); minh họa reactive state bằng **Proxy**.

Mấu chốt phân biệt:

- **Virtual DOM** tối ưu **hiệu năng cập nhật** (ít đụng DOM thật).
- **Shadow DOM** tập trung **cô lập và tái sử dụng** (CSS/DOM riêng, không xung đột).
- **Reactivity** là "tự theo dõi dữ liệu thay đổi → tự cập nhật giao diện" — cách hiện thực có thể là Virtual DOM (React/Vue) hoặc Proxy + re-render thủ công.

## ✅ Điểm mạnh

- **Đúng thứ kiến thức framework cần**: nắm Virtual DOM / reactivity là hiểu vì sao React/Vue làm việc như họ làm.
- **Encapsulation thật**: Shadow DOM chống CSS leak giữa component và trang.
- **Hiệu năng tối ưu**: cập nhật tối thiểu lên DOM thật thay vì rebuild toàn bộ.
- **Bản thân các ví dụ là module nhỏ chạy được** trong thư mục — học bằng thực hành.
- **Bắc cầu từ DOM thường sang framework**: hiểu được cả cách làm tay (vanilla) lẫn "bên trong" thư viện lớn.

## ⚠️ Lưu ý / Hạn chế

- Virtual DOM có **overhead** (tạo/diff cây ảo) — với ứng dụng nhỏ, sửa DOM trực tiếp nhanh hơn.
- Shadow DOM làm **truyền dữ liệu/events** giữa ngoài-trong phức tạp hơn.
- Reactivity (Proxy) đọc/ghi qua proxy chậm hơn một chút và khó gỡ lỗi hơn.
- Có ba loại DOM với mục đích khác nhau — đừng coi chúng là "hoán đổi cho nhau".

## 💡 Khi nào dùng

- Làm **SPA phức tạp, state thay đổi liên tục** → cần Virtual DOM / reactivity (chọn framework).
- Build **thư viện UI / widget dùng chung nhiều trang** → Shadow DOM để bọc kín style.
- Trang đơn giản, cần thêm tính năng nhỏ → không cần framework, DOM Manipulation là đủ.
- Cần **validate/đồng bộ tự động** dữ liệu ↔ UI → lắp một layer reactivity bằng Proxy.
- Nghiên cứu kiến trúc trước khi chọn framework (React: Virtual DOM; Vue: reactivity + Virtual DOM; Stencil/lit: Shadow DOM).

## 🎯 Ví dụ minh họa

```js
// Virtual DOM tinh thần: state -> VNode -> diff -> patch (chỉ sửa phần đổi)
const vNode = { tag: 'p', props: {}, children: [`Counter: ${state.counter}`] };
// ...so khác với cây cũ rồi chỉ set textContent cho nút thay đổi

// Shadow DOM: cô lập cấu trúc + style
host.attachShadow({ mode: 'open' });
shadow.innerHTML = '<style>p{color:blue}</style><p>trong bong tối</p>';

// Reactivity bằng Proxy (thấy ở 05_reactivity)
const state = new Proxy({ count: 0 }, {
  set(target, key, value) { target[key] = value; updateUI(value); return true; }
});
```

## 📚 Tham khảo / Bài tập

- Lần lượt đọc và chạy từng mục: `01_manipulation` (mở `example-1/index.html` bấm nút xem thay đổi; `example-2` là to-do list) → `02_shadow-dom` (chạy `example1`, `example2`) → `03_virtual-dom` (chạy `example1` — bấm nút Increment, quan sát diff) → `04_dom-combination` → `05_reactivity`.
- Tự làm: trong `03_virtual-dom/example1`, sửa `helper.js` để so sánh cả thuộc tính `class` khi diff — thấy chiều sâu patch thực tế.
- Tự làm: trong `02_shadow-dom/example1`, đổi `mode: "closed"` thành `"open"` và thử `document.getElementById('appContainer').shadowRoot` để hiểu encapsulation.
- Tự làm: trong `05_reactivity`, thêm một property `name` vào `state` và hiển thị lên UI khi thay đổi — làm rõ vai trò Proxy `set`.