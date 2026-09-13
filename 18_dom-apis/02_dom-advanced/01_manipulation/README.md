# DOM Manipulation — Thao Tác Trực Tiếp DOM

## 🔑 Khái niệm

**DOM Manipulation** (hay *JS DOM Manipulation*) là **quá trình thay đổi cấu trúc, nội dung và kiểu dáng của trang web** bằng cách tương tác trực tiếp với cây DOM qua JavaScript. Không qua framework, không qua lớp trung gian ảo — bạn gọi API của trình duyệt để:

- **Tìm phần tử**: `document.getElementById`, `querySelector`, `querySelectorAll`.
- **Sửa nội dung**: `textContent`, `innerText`, `innerHTML`, `appendChild`, `remove`.
- **Sửa thuộc tính/style/class**: `setAttribute`, `element.style`, `classList`.
- **Lắng nghe sự kiện**: `addEventListener`.

Ưu điểm cốt lõi: **linh hoạt, tức thì, không phụ thuộc framework, tương thích mọi trình duyệt**. Nhược điểm cũng nằm ở chỗ đó: nếu thao tác quá nhiều (nhất là trong vòng lặp, hoặc làm rải rác nhiều chỗ cùng lúc) mỗi lần đổi DOM đều gây **reflow/layout và paint lại** → hiệu năng giảm, xác suất lỗi tăng khi code phình to.

Thư mục này có 2 ví dụ:

- `example-1/` — nút "Click me": khi click sẽ cập nhật `innerText`, đổi `setAttribute("style", ...)` và thay luôn `outerHTML` thành một `<image>`.
- `example-2/` — **to-do list** thuần JS: `DOMContentLoaded`, `createElement('li')`, gắn sự kiện click để `remove()` task.

## ✅ Điểm mạnh

- **Độ linh hoạt cao**: đóng/mở, thêm/sửa/xóa bất kỳ phần nào của trang không cần reload.
- **Phản hồi nhanh, trực tiếp**: thao tác tức thì, không phải chờ change detection của framework.
- **Tương thích rộng**: API chuẩn trên mọi trình duyệt, không yêu cầu framework/thư viện.
- **Dễ học, dễ debug**: không có lớp diff — bạn thấy đúng hành vi mình viết.
- **Kết hợp tốt với framework**: dùng trong hook/no-FW case, micro-interaction.

## ⚠️ Lưu ý / Hạn chế

- **Hiệu suất**: nhiều lần thay đổi trong vòng lặp / quá nhiều listener → reflow, render lại, giật.
- **Bảo trì khó khi to**: cây DOM lớn, ít cấu trúc — việc quản lý code thao tác tay trở nên phức tạp.
- **Rò rỉ bộ nhớ**: quên `removeEventListener`, giữ ref tới node đã gỡ → detached DOM, memory leak.
- **Khác biệt trình duyệt nhỏ** trong vài API/khoảng trắng text node — thường phải tinh chỉnh.

## 💡 Khi nào dùng

- **Ứng dụng nhỏ / prototype** — thao tác trực tiếp đơn giản, linh hoạt.
- **Thay đổi DOM tức thời** khi sự kiện xảy ra (đổi màu, hiện/ẩn, filter phía client).
- **Thêm widget nhỏ** vào trang có sẵn mà không muốn đưa cả framework vào.
- Khi cần **điều khiển chính xác từng nút** — micro-animation, được đo đếm thủ công.
- Hai ví dụ ở `example-1`/`example-2` chính là mô hình tối giản cho các case trên.

## 🎯 Ví dụ minh họa

```js
document.addEventListener('DOMContentLoaded', function () {
  const btn = document.getElementById('btnClickMe');
  btn.addEventListener('click', function () {
    btn.innerText = "What's up";                       // đổi text
    btn.setAttribute('style', 'color:red; padding:4px'); // đổi inline style
    // example-1 còn thay luôn outerHTML bằng ảnh đại diện
  });
});

// example-2: thêm task
const item = document.createElement('li');
item.textContent = taskText;
item.addEventListener('click', () => item.remove()); // xóa khi click
taskList.appendChild(item);
```

## 📚 Tham khảo / Bài tập

- Mở `example-1/index.html`: bấm nút **Click me** rồi quan sát text/style/outerHTML biến thành gì (field toàn ảnh base64).
- Mở `example-2/index.html`: gõ task vào ô input, thêm rồi click task để xóa — theo dõi `taskList` thay đổi trên DOM.
- Tự làm trong `example-2`: thêm nút "Xoá tất cả" (`taskList.innerHTML=''`) và đếm số task đang có qua `taskList.children.length`.
- Tự làm: thay `innerHTML` bằng `textContent` ở một chỗ nhập dữ liệu để so sánh an toàn XSS.
- Tham khảo tài liệu API: <https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model/Introduction>; kiểm tra tương thích tại <https://caniuse.com/>.