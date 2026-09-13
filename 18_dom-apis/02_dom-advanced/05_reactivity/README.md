# Reactivity — Tự Động Đồng Bộ Dữ Liệu ↔ Giao Diện

## 🔑 Khái niệm

**Reactivity** là khả năng hệ thống **tự theo dõi sự thay đổi của dữ liệu** và **tự cập nhật giao diện** tương ứng — bạn không phải gọi tay "sửa DOM lại" sau mỗi lần đổi state. Mức độ reactivity khác nhau giữa các cách tiếp cận:

- **DOM Manipulation — thấp**: không có theo dõi tự động; bạn tự `innerText = ...` sau mỗi thay đổi. Phù hợp trang đơn giản; thường đi kèm jQuery/Backbone tự quản lý.
- **Virtual DOM — cao**: framework (React, Vue) theo dõi state → dựng cây ảo mới → diff → patch phần đổi lên DOM thật. Nhờ vậy mỗi lần click/chỉnh dữ liệu là UI cập nhật đúng, ít tốn DOM.
- **Shadow DOM — trung bình → cao**: nhờ **encapsulation + scoped CSS**, thay đổi trong shadow tree không làm rối phần còn lại của trang; khả năng "react" tốt khi kết hợp với cơ chế theo dõi của Web Components.
- **Reactivity thuần (kiểu Vue/Polymer)**: dùng **Proxy** để *bắt* mọi thao tác đọc/ghi trên state — mỗi lần `set` chạy, lập tức cập nhật UI tương ứng (xem ví dụ trong thư mục này).

Đoạn code trong thư mục minh họa một **reactive counter** bằng `Proxy`:

- `state` là `new Proxy({ count: 0 }, { set })`.
- Trong trap `set`: gán `target[key] = value` **và trực tiếp** `document.getElementById('counter').innerText = ...`.
- Click nút → `state.count += 1` → trap `set` chạy → UI tự đổi.

Tóm lược: *DOM thực = reactivity thấp (thao tác tay)*; *Virtual DOM = reactivity cao (tự diff/patch)*; *Proxy = nền tảng reactivity "fine-grained" dùng trong Vue/Polymer*.

## ✅ Điểm mạnh

- **Tự động**: UI luôn khớp state, không quên cập nhật, không sai lệch chỗ này chỗ kia.
- **Giảm code thao tác tay** — bớt boilerplate DOM update lặp lại.
- **Hiệu năng tốt hơn** với Virtual DOM: chỉ patch phần thực sự đổi.
- **Proxy không xâm lấn**: đọc/ghi qua state như bình thường, trap làm phần "phản ứng".
- **Nền tảng của framework hiện đại**: nắm reactivity là hiểu được Vue/Polymer/Svelte.

## ⚠️ Lưu ý / Hạn chế

- Proxy có **overhead nhỏ** mỗi lần truy cập và `set` phải `return true` (nếu `false` → gán coi như thất bại).
- `Array` qua Proxy cũng bắt được nhưng cần **xử lý riêng** (chỉ số, push) — dễ bỏ sót.
- Reactivity không miễn phí: việc **re-render quá rộng** (diff cả cây) vẫn tốn chi phí ở app lớn.
- Khó **gỡ lỗi** khi "tự cập nhật" vô hình trung — cần tooling như Vue devtools để nhìn nguồn.
- Đừng nhầm reactivity "tự cập nhật" với **hiệu năng tự nhiên** — vẫn phải tối ưu đúng chỗ.

## 💡 Khi nào dùng

- **Ứng dụng có nhiều state** và nhiều nơi phụ thuộc vào state đó (user login, cart, form liên quan).
- **Chọn framework**: cần reactivity cao → React/Vue (Virtual DOM) hoặc Vue/Polymer (Proxy).
- **Widget nhỏ cần tự cập nhật** — dùng một `Proxy` reactive thay vì rải `document.getElementById` khắp nơi.
- Muốn theo dõi sự thay đổi của **một object cụ thể** (log, trigger fetch, save).
- Học nền tảng để hiểu cơ chế **two-way/tracked state** của các framework.

## 🎯 Ví dụ minh họa

```js
const state = new Proxy(
  { count: 0 },
  {
    set(target, key, value) {
      target[key] = value;                            // lưu state
      document.getElementById('counter').innerText =
        `Số lần click: ${value}`;                     // tự cập nhật UI
      return true;                                    // báo gán thành công
    },
  }
);

document.getElementById('clickButton')
  .addEventListener('click', () => { state.count += 1; });  // UI tự đổi
```

## 📚 Tham khảo / Bài tập

- Chép đoạn `Proxy` + `counter` trong thư mục này vào một `index.html` tạm (hoặc bật Console trên một trang trống) — bấm nút, quan sát text counter tự tăng.
- Tự làm: thêm `state.name = 'Teo'` rồi gắn `#nameOutput`; trong trap `set`, cập nhật cả hai phần tử — thấy hết khả năng "multi-target update".
- Tự làm: cho một mảng `state.items = [];state.items.push('a')` và in ra Console — để ý vì sao `push` qua Proxy vẫn pass qua `set` (chỉ số được gán) và bạn cần bắt thêm gì nếu muốn trigger khi push.
- Tự làm: so sánh với phiên bản **Virtual DOM** trong `03_virtual-dom/example1` — ghi nhận hai cách đạt "UI tự khớp state": diff-cây (React) vs trap-set (Proxy).
- Đọc lại bảng so sánh ở đầu thư mục để phân biệt 3 mức: DOM thực (thấp) / Virtual DOM (cao) / Shadow DOM (trung bình-cao).