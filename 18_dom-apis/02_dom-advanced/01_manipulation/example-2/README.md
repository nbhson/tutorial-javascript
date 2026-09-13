# Sự kiện trang web và vòng đời load — Ví dụ To-do List

## 🔑 Khái niệm

Ví dụ này là một **to-do list thuần JavaScript** (`app.js` + `index.html` + `style.css`), tận dụng *các sự kiện vòng đời của trang* và DOM Manipulation để vận hành:

- **`DOMContentLoaded`** — bắn khi toàn bộ HTML đã được parse xong (ảnh, stylesheet, font, video **chưa** cần xong). Đây là thời điểm đúng nhất để gắn handler vào các phần tử — bảo đảm `getElementById` tìm được nút như `taskInput`, `addTaskBtn`, `taskList`.
- **`load`** — bắn khi trang **và mọi tài nguyên** (ảnh, stylesheet...) đã tải xong. Dùng để kiểm tra "mọi thứ sẵn sàng" (ví dụ đo kích thước ảnh).
- **`beforeunload`** — khi người dùng chuẩn bị rời trang (đóng tab/điều hướng); thường dùng để xác nhận hoặc cảnh báo.
- **`unload`** — khi trang đang bị đóng; nơi dọn dẹp cuối (clear timers, gửi ping...).
- **`hashchange`** — khi phần `#...` của URL đổi — kỹ thuật nền tảng của **SPA router** kiểu hash-based.
- **`resize`** — khi cửa sổ đổi kích thước — làm giao diện phản ứng theo viewport.

Cơ chế core của to-do list: mỗi lần bấm **Add task**, app `createElement('li')`, set `textContent`, gắn listener riêng để `remove()` khi click vào task. Vòng lặp DOM + events như vậy là nền tảng của mọi ứng dụng động.

## ✅ Điểm mạnh

- **Thao tác DOM tối giản** nhưng đủ: tạo element, gắn text, thêm vào list, xóa bằng chính sự kiện click.
- **Sự kiện vòng đời** bao phủ đủ tình huống load/tải/rời trang — một bộ kiến thức hay gặp khi làm SPA.
- **Vanilla JS** — không phụ thuộc framework, hiểu được luồng trực tiếp.
- **`removeEventListener` dễ thử** cùng mẫu — ôn lại bài 12 của `01_f8-basic-dom`.

## ⚠️ Lưu ý / Hạn chế

- `DOMContentLoaded` ≠ `load`: gắn handler vào `load` sau khi DOM xong khiến trang **phản ứng chậm** hơn với user.
- `unload`/`beforeunload` **không đáng tin để lưu state quan trọng** (có thể bị cancel, chạy không đủ hoàn tất) — nên lưu qua `pagehide`/`visibilitychange`.
- Trong `example-2`, listener remove gắn trực tiếp vào **từng `<li>`** — list nhiều thêm sẽ nhiều listener; nên dùng **event delegation** (gắn một listener ở `taskList`) khi scale.
- `resize`/`hashchange` thường xuyên kích hoạt: nếu callback nặng nên **debounce/throttle**.

## 💡 Khi nào dùng

- Gắn handlers **sau khi DOM parse xong** — chuẩn của mọi trang dùng JS.
- Xác nhận rời trang có dữ liệu chưa lưu (`beforeunload`).
- Điều hướng SPA đơn giản bằng hash (`hashchange`).
- Hiển thị UI đáp ứng đúng kích thước (`resize`).
- Vẽ danh sách động kiểu to-do: thêm/xóa phần tử theo sự kiện.

## 🎯 Ví dụ minh họa

```js
document.addEventListener('DOMContentLoaded', function () {
  const taskInput = document.getElementById('taskInput');
  const addTaskBtn = document.getElementById('addTaskBtn');
  const taskList = document.getElementById('taskList');

  addTaskBtn.addEventListener('click', function () {
    const text = taskInput.value.trim();
    if (text !== '') {
      const li = document.createElement('li');
      li.textContent = text;
      li.addEventListener('click', () => li.remove());
      taskList.appendChild(li);
      taskInput.value = '';
    }
  });
});

window.addEventListener('beforeunload', () => { event.returnValue = ''; });
window.addEventListener('hashchange', () => console.log('Hash changed'));
window.addEventListener('resize', () => console.log('Window resized'));
```

## 📚 Tham khảo / Bài tập

- Mở `index.html` trong trình duyệt (Console bật): bấm **Add task**, gõ chữ rồi thêm; click chuột vào task để xóa.
- Tự làm: chuyển listener remove từng `<li>` sang **event delegation** — đặt một `click` ở `taskList`, lọc bằng `event.target.tagName === 'LI'`.
- Tự làm: thay log `hashchange`/`resize` bằng **throttle/debounce** 300ms để thấy tần suất callback giảm.
- Tự làm: thêm sự kiện **Enter** để thêm task không cần bấm nút (`taskInput.addEventListener('keydown', ...)`), và một nút **Xóa tất cả**.
- Ôn lý thuyết sự kiện tiếp theo tại `03_events/README.md`.