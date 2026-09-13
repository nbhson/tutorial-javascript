# Promise Chain — nối chuỗi `.then()`

## 🔑 Khái niệm

`.then()` luôn trả về **một promise mới**, nên bạn có thể **nối tiếp** nhiều bước xử lý thành một chuỗi (chain). Giá trị đẩy xuống bước kế tiếp quyết định bởi những gì bước trước **return**:

- `return` một giá trị thường → bước sau nhận giá trị đó.
- `return` một **promise** → bước sau **chờ promise đó settle xong** rồi mới chạy (đây là cách nối 2 tác vụ bất đồng bộ phụ thuộc nhau).
- Không `return` gì → bước sau nhận `undefined`.

Khi bất kỳ mắt xích nào **throw/reject** → chuỗi dừng tại đó và rơi thẳng xuống `.catch()` gần nhất; các `.then()` phía sau bị bỏ qua. `.finally()` luôn chạy cuối cùng dù thành công hay thất bại.

## ✅ Điểm mạnh

- Biểu diễn quy trình nhiều bước phụ thuộc nhau một cách tuyến tính, dễ đọc.
- Chờ promise trong promise (`return` promise) giúp nối các tác vụ async.
- Lỗi dừng chuỗi ngay và chỉ cần một `.catch()` cho cả chuỗi.
- Linh hoạt: pha trộn giá trị thường và promise trong cùng chain.

## ⚠️ Lưu ý / Hạn chế

- Quên `return` → bước sau nhận `undefined` (bug phổ biến nhất).
- `.then` không được return promise sẽ không chờ bất đồng bộ bên trong.
- Một mắt xích reject sẽ bỏ qua mọi `.then()` sau đó cho tới `.catch`.
- Chain quá dài cũng khó đọc — cân nhắc `async/await`.

## 💡 Khi nào dùng

- Quy trình: `getComment()` → lấy `userId` → `getUsersByIds()` → render.
- Gọi API tuần tự: lấy user, lấy bài viết của user, lấy bình luận...
- Xử lý dữ liệu qua nhiều bước phép biến đổi.

## 🎯 Ví dụ minh họa

```js
Promise.resolve(1)
  .then((v) => v + 1)                      // 2 (giá trị thường)
  .then((v) => new Promise((res) =>
    setTimeout(() => res(v * 10), 0)))     // chờ promise → 20
  .then((v) => console.log(v))             // 20
  .catch((err) => console.log("Fail", err))
  .finally(() => console.log("Done"));     // luôn chạy
```

## 📚 Tham khảo / Bài tập

- Chạy `04_promise-chain/app.js` (qua `index.html` hoặc `node app.js`): chuỗi có `setTimeout` 3s, spam `resolve`/`reject`, và kết thúc bằng `.catch`/`.finally`.
- Tự thử: xóa dòng `return promise` trong `.then` đầu tiên và chạy lại — quan sát dữ liệu `.then` sau nhận `undefined`.