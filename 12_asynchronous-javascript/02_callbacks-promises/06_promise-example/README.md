# Promise — Ví dụ thực tế (bình luận & người dùng)

## 🔑 Khái niệm

Ví dụ tổng hợp ứng dụng promise trong một luồng xử lý dữ liệu thực tế có **3 bước phụ thuộc nhau**:

1. Lấy danh sách **comments**.
2. Từ comments lấy ra các `userId`.
3. Từ userIds lấy các **user** tương ứng → ghép lại → render UI.

Trong đó dữ liệu là mảng object `users` và `comments`; hai hàm `getComment()` và `getUsersByIds(userId)` đều trả về promise (qua `Promise.resolve`) để mô phỏng dữ liệu từ server. Các bước được nối bằng `Promise chain`, kết quả cuối cùng là object `{ users, comments }` được render vào `<ul id="comments-block">`.

## ✅ Điểm mạnh

- Khuôn mẫu chuẩn cho mọi ứng dụng "lấy dữ liệu → biến đổi → hiển thị".
- Tách logic lấy dữ liệu (promise) khỏi logic render (function).
- Ghép nhiều nguồn dữ liệu (users + comments) trong một chain.
- Dễ chuyển sang `fetch` + `async/await` thật khi có server.

## ⚠️ Lưu ý / Hạn chế

- `.then` lồng trong `.then` (để gộp users + comments) làm chain hơi phức tạp — có thể thay bằng `Promise.all`.
- Nếu comments chứa userId không tồn tại, sẽ không tìm được user tương ứng → cần kiểm tra.
- Dữ liệu mẫu cứng (hard-code) trong file, muốn thật thì thay bằng API.
- Chưa xử lý ripple khi dữ liệu trống (render chuỗi rỗng).

## 💡 Khi nào dùng

- Bất kỳ màn hình nào cần lấy nhiều nguồn dữ liệu rồi gộp để render.
- Quy trình: comments → userIds → users (dữ liệu quan hệ kiểu "khóa ngoại").
- Học cách tổ chức code bất đồng bộ gọn gàng trước khi dùng framework.

## 🎯 Ví dụ minh họa

```js
function getComments() {
  return Promise.resolve(comments); // mô phỏng gọi API
}

getComments()
  .then((comments) => {
    const userIds = comments.map((c) => c.userId);
    return getUsersByIds(userIds).then((users) => ({ users, comments }));
  })
  .then(({ users, comments }) => {
    // render: "Kien Nguyen: Anh Son chua ra video"
    const html = users
      .map((u) => {
        const c = comments.find((c) => c.userId === u.id);
        return `<li><strong>${u.name}</strong>: ${c.content}</li>`;
      })
      .join("");
    document.querySelector("#comments-block").innerHTML = html;
  });
```

## 📚 Tham khảo / Bài tập

- Mở `06_promise-example/index.html` trong trình duyệt: xem danh sách bình luận được render vào `#comments-block`; `app.js` chứa toàn bộ logic.
- Tự thử: thêm một user/comment mới vào mảng `users`/`comments` rồi refresh — thêm cả trường hợp userId không có user để thấy lỗi và tự sửa bằng `if`. Cuối cùng, viết lại bằng `async/await`.