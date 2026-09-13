# Virtual DOM — Cập Nhật DOM Tối Thiểu

## 🔑 Khái niệm

Thao tác DOM thủ công rất lộn xộn: khó theo dõi trạng thái trước/sau, và cập nhật toàn bộ DOM mỗi lần state đổi khiến ứng dụng chậm. **Virtual DOM** giải quyết bằng cách: bạn **mô tả lại toàn bộ giao diện** mỗi khi state thay đổi (viết code như đang "tạo lại cả DOM"), nhưng thay vì đụng DOM thật, bạn chỉ tạo một **cây ảo (VTree / VNode)** trong bộ nhớ. Một lớp trung gian (thư viện `virtual-dom`, hay chính React) sẽ:

1. **Tạo Virtual DOM mới** từ state hiện tại.
2. **Diff** cây mới với cây cũ → tìm **những phần khác biệt** (patch list).
3. **Patch**: chỉ cập nhật đúng các phần đổi lên **DOM thực tế** — giảm tối đa thao tác trực tiếp và render lại toàn trang.

Thư mục này có `example1/` — một **mini virtual-dom tự viết**:

- `helper.js`: `createVNode(tag, props, children)` tạo node ảo; `render(vNode, container)` giữ `container._vNode` để diff; `createElementFromVNode` chuyển VNode → DOM thật (nhận biết text/event bắt đầu với `on`); `diff(oldVNode, newVNode)` so sánh text con và sinh patch `SET_PROP`; `patch/applyPatch` áp lên đúng node.
- `app.js`: state `{ counter }`, hàm `updateCounter()` tăng counter rồi `renderApp()` dựng lại VNode — nhờ diff, chỗ bị sửa chính là text của thẻ `<p>` counter.

## ✅ Điểm mạnh

- **Hiệu năng**: chỉ sửa phần thay đổi thay vì rebuild toàn bộ DOM → ít layout/paint, mượt hơn.
- **Viết kiểu declarative**: tư duy "UI = f(state)" — dễ đọc, dễ test.
- **Quản lý state dễ**: nhờ tách mô hình dữ liệu khỏi thao tác DOM.
- **Nền tảng React/Vue**: hiểu diff → hiểu bản năng tối ưu key trong `list.map`.
- **Batch cập nhật**: framework gom nhiều thay đổi state thành một lần render.

## ⚠️ Lưu ý / Hạn chế

- **Overhead thêm**: tạo + diff cây ảo tốn CPU/memory — với UI nhỏ, sửa DOM trực tiếp nhanh hơn.
- **Diff không phải "miễn phí"**: cây càng lớn, so sánh càng tốn; sai `key` làm React render lại nhầm nhánh.
- **Không thay được quản lý state**: vẫn cần công cụ khác (useState, Vuex, domain state) phía trên.
- Code vanilla kiểu này khó đọc hơn so với tách framework ra cho đúng bài toán.

## 💡 Khi nào dùng

- Ứng dụng **có nhiều trạng thái động**, render lại liên tục trên nhiều thành phần.
- **Danh sách lớn** cần cập nhật từng dòng — khai báo `key` ổn định để diff chính xác.
- Cần **tách biết "dữ liệu → UI"** rõ ràng — model truyền thẳng vào render.
- Khi build **multi-component app** — mỗi component trả về VNode, framework chỉ patch phần đổi.
- Muốn tự viết một **renderer tí hon** — chính là `example1/helper.js`.

## 🎯 Ví dụ minh họa

```js
// app.js — state và render lại từ đầu (diff chỉ sửa phần đổi)
let state = { counter: 0 };
function updateCounter() { state.counter += 1; renderApp(); }

function createAppVNode() {
  return createVNode('div', null, [
    createVNode('h1', null, ['Virtual DOM']),
    createVNode('p',  null, [`Counter: ${state.counter}`]),
    createVNode('button', { onclick: updateCounter }, ['Increment']),
  ]);
}
function renderApp() {
  render(createAppVNode(), document.getElementById('app'));
}
renderApp();   // lần đầu: tạo toàn bộ; mỗi lần bấm: chỉ patch text counter
```

## 📚 Tham khảo / Bài tập

- Mở `example1/index.html` và bấm nút **Increment**: quan sát `counter` tăng; thử thêm `console.log` vào `applyPatch` trong `helper.js` để thấy **chỉ đúng nút `<p>` bị sửa**, không phải cả cây.
- Đọc tuần tự `helper.js`: `createVNode` → `render` (cache `_vNode`) → `createElementFromVNode` (text, event) → `diff` (SET_PROP) → `patch`.
- Tự làm: sửa `diff` để so cả **class** của nút khi props thay đổi (thêm type `SET_PROP` với key `className`).
- Tự làm: thêm một nút "Reset" làm `state.counter = 0` rồi `renderApp()`.
- Tự làm: thử đổi nút button thành 2 button (cộng/trừ) để thấy diff xử lý nhiều node con.
- Tham khảo thư viện nguồn: <https://github.com/Matt-Esch/virtual-dom> và tài liệu React reconciliation.