# Shadow DOM — Encapsulation cho Component UI

## 🔑 Khái niệm

**Shadow DOM** là công nghệ Web Components cho phép **gắn một cây DOM con riêng biệt** vào một element (gọi là **Shadow Host**) và bao nó trong **Shadow Boundary** — ranh giới cách ly:

- **Shadow Host**: phần tử thường của trang mà bạn gắn Shadow DOM vào (`host.attachShadow({ mode: 'open'|'closed' })`).
- **Shadow Tree**: cây DOM ẩn bên trong host — bao gồm style và các element riêng.
- **Shadow Boundary**: "hộp kín" — **CSS và DOM bên trong không bị ảnh hưởng bởi trang**, và ngược lại, trang không nhìn thấy hay chỉnh được nội dung bên trong (khi mode `closed` càng chặt).

Mục tiêu: **encapsulation (đóng gói)** — build UI component **tái sử dụng độc lập** mà không lo xung đột style với phần còn lại của trang: không "CSS leak" ra ngoài, không bị CSS toàn cục xâm nhập, selector nội bộ không đụng nhau. Cùng với `customElements.define`, đây chính là bộ khung của tiêu chuẩn **Web Components** (như thẻ `<video>`, `<input>` nội bộ trình duyệt cũng dùng shadow tree).

Thư mục này có 2 ví dụ:

- `example1/app.js` — tạo shadow DOM **mode `closed`** trên `#appContainer`, thêm một `<div>` chữ "Hello from Shadow DOM!" cùng class `red_color`.
- `example2/app.js` — định nghĩa **custom element** `<custom-widget>` với shadow root **mode `open`**, style qua `:host`, đăng ký bằng `customElements.define`.

## ✅ Điểm mạnh

- **Cô lập CSS triệt để**: style component không "tràn" ra trang, không bị trang làm hỏng.
- **Che giấu cấu trúc nội bộ**: logic/DOM bên trong là chi tiết cài đặt — truy cập bên ngoài bị hạn chế.
- **Tái sử dụng an toàn**: cùng một component dùng nhiều nơi, nhiều dự án mà không đụng nhau.
- **Bảo mật kiểu**: ngăn thành phần bên ngoài (thư viện UI tích hợp) làm rối giao diện.
- **Hiệu năng render tốt hơn**: trình duyệt biết rõ phạm vi, quản lý style scoped hiệu quả.

## ⚠️ Lưu ý / Hạn chế

- **Giao tiếp ngoài-trong khó hơn**: cần cẩn thận để truyền dữ liệu/sự kiện qua boundary (thường qua attributes, events, hoặc `composed: true`).
- **Mode `closed` hạn chế debug**: DevTools và code ngoài không "mở khóa" được shadowRoot để xem bên trong.
- Style slider/các pseudo-class trình duyệt bên trong shadow tree hoạt động giới hạn hơn.
- Đúng một mình Shadow DOM (không kèm `customElements`) vẫn chỉ là cách cô lập — chưa phải "component đầy đủ".

## 💡 Khi nào dùng

- Xây dựng **thư viện/marketplace UI widget** cần bọc kín style và hành vi.
- Tố chức **multiple apps / plugin** trên cùng trang mà không được xung đột CSS.
- Build **Web Components** để tái sử dụng xuyên framework (dùng trong React lẫn Vue).
- Nhúng **third-party UI** mà không thể kiểm soát CSS toàn cục.
- Ý tưởng encapsulation rèn luyện trước khi gặp scoped CSS của Vue (`<style scoped>`) hay CSS Modules.

## 🎯 Ví dụ minh họa

```js
// example1 — gắn shadow cây riêng (mode closed)
const host = document.getElementById('appContainer');
const shadowRoot = host.attachShadow({ mode: 'closed' });
const el = document.createElement('div');
el.textContent = 'Hello from Shadow DOM!';
el.classList.add('red_color');
shadowRoot.appendChild(el);        // ngoài không truy cập được shadowRoot

// example2 — custom element với style scoped qua :host
class CustomWidget extends HTMLElement {
  constructor() {
    super();
    const root = this.attachShadow({ mode: 'open' });
    root.innerHTML = `
      <style>:host { display:block; border:2px solid green; padding:10px; }</style>
      <div>I'm a custom widget!</div>`;
  }
}
customElements.define('custom-widget', CustomWidget);
// dùng: <custom-widget></custom-widget>
```

## 📚 Tham khảo / Bài tập

- Mở `example1/index.html` + `example1/style.css`: quan sát class `red_color` không tô màu được nội dung bên shadow tree (style ngoài không vào được); trong Console thử `appContainer.shadowRoot` — kết quả `null` vì mode `closed`.
- Mở `example2/index.html`: có `<custom-widget>` được render với viền xanh từ `:host` — thử đổi `mode` và CSS để thấy hành vi scoped.
- Tự làm: trong `example2`, thêm một attribute `label` và đọc nó trong `constructor()` để hiển thị lên widget.
- Tự làm: đổi `example1` sang `{ mode: 'open' }`, sửa `.shadowRoot` rồi `shadowRoot.querySelector('div').textContent` — thấy rõ khác biệt giữa open/closed.
- Đọc thêm: DigitalOcean/網 bài viết Shadow DOM in-depth: <https://github.com/praveenpuglia/shadow-dom-in-depth> và MDN Shadow DOM.