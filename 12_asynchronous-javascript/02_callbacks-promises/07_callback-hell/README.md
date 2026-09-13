# Callback Hell (Pyramid of Doom)

## 🔑 Khái niệm

**Callback hell** xảy ra khi bạn lồng callback này vào callback khác nhiều tầng để xử lý các tác vụ bất đồng bộ tuần tự. Càng lồng sâu, thụt vào càng nhiều — hình dạng giống một **kim tự tháp** (pyramid of doom), khiến code **khó đọc và khó gỡ lỗi**.

```js
async1((a) =>
  async2(a, (b) =>
    async3(b, (c) =>
      console.log(c))));
```

Thông thường các hàm `async1/async2/async3` là các tác vụ bất đồng bộ (timer, fetch, I/O) nhận callback, và mỗi bước cần dữ liệu của bước trước.

**Giải pháp:** dùng **Promises** (chuỗi `.then()`) hoặc **async/await** để "giải nén" kim tự tháp thành các dòng tuần tự, dễ đọc.

## ✅ Điểm mạnh (của việc hiểu rõ callback hell)

- Nhận diện ngay "mùi code" khi viết callback lồng nhau.
- Biết lý do vì sao Promise/async/await tồn tại — đánh giá đúng công cụ.
- Duy trì code cũ viết bằng callback (nhiều thư viện Node.js vẫn dùng callback).
- Chuyển đổi callback → promise bằng `new Promise`.

## ⚠️ Lưu ý / Hạn chế

- Mỗi cấp lồng làm tăng biến cục bộ/gian nan khi đổi tên, thay đổi logic.
- Lỗi phải truyền bằng tay qua từng callback → dễ bỏ sót.
- Luồng rẽ nhánh, lỗi, hay thoát sớm rất khó viết/kiểm soát.
- Dùng `setTimeout` mô phỏng giống demo giúp học nhưng không phải tốc độ thật.

## 💡 Khi nào dùng (khi nào gặp phải)

- Đọc/ghi file tuần tự trong Node.js với callback API.
- Gọi API nối tiếp nhau, bước sau cần dữ liệu bước trước, dùng callback style.
- Giảm thiểu: refactor bằng promise/async-await ngay khi thấy 2-3 cấp lồng.

## 🎯 Ví dụ minh họa

```js
// Callback hell
async1((a) => async2(a, (b) => async3(b, (c) => console.log("hell result", c))));
// hell result 3

// Cùng logic bằng Promise — thẳng hàng, dễ đọc
Promise.resolve(1)
  .then((x) => x + 1)
  .then((x) => x + 1)
  .then(console.log); // 3
```

## 📚 Tham khảo / Bài tập

- Chạy `07_callback-hell/app.js` (qua `index.html` hoặc `node app.js`): thấy cả hai bản — callback lồng 3 tầng in `hell result 3`, promise chain thẳng hàng cũng in `3`.
- Tự thử: thêm bước `async4` vào cả hai phiên bản, so sánh độ khó đọc; sau đó viết lại bản callback bằng `async/await` để thấy lợi ích cuối cùng.