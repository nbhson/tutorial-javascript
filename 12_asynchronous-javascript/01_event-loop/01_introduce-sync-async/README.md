# Giới thiệu Synchronous và Asynchronous

## 🔑 Khái niệm

**Lập trình đồng bộ (synchronous)**: code chạy từng dòng một theo thứ tự viết; mỗi dòng phải xử lý xong mới đến dòng tiếp theo. Nếu một hàm chạy lâu (ví dụ đọc file, gọi mạng), mọi thứ phía sau phải **đứng chờ** — chương trình bị chặn.

**Lập trình bất đồng bộ (asynchronous)**: chương trình có thể **bắt đầu** một tác vụ dài rồi **trả quyền điều khiển ngay lập tức**, tiếp tục đáp ứng các sự kiện khác. Khi tác vụ hoàn thành, kết quả được thông báo qua callback/promise.

Các ví dụ thực tế của tác vụ bất đồng bộ:

- Gửi HTTP request bằng `fetch()`, `observable`, timer...
- Truy cập camera/microphone bằng `getUserMedia()`.
- Chọn file bằng `showOpenFilePicker()`.
- Mọi **event handler** (click, scroll...) đều là bất đồng bộ: chờ người dùng tương tác mà không chặn UI.

## ✅ Điểm mạnh

- UI không bị "đứng hình" khi chờ dữ liệu/timer.
- Nhiều tác vụ chờ (network, I/O) có thể chạy đan xen, tận dụng tối đa thời gian rảnh.
- Nền tảng để hiểu callback, promise, async/await.
- Event handler phản ứng tức thì với người dùng.

## ⚠️ Lưu ý / Hạn chế

- Kết quả in ra **không theo thứ tự khai báo** — gây bất ngờ nếu không nắm event loop.
- Code đồng bộ đơn giản hơn nhưng nguy hiểm khi tác vụ lâu.
- Callback lồng nhau nhanh chóng thành "callback hell" (pyramid of doom).
- `await` chỉ dùng được trong hàm `async`; không chạy được ở global scope thông thường.

## 💡 Khi nào dùng

- Mọi tác vụ mạng, file, timer — không nên đồng bộ hóa.
- Lắng nghe hành vi người dùng (async theo bản chất).
- Khi cần đáp ứng nhanh: autocomplete, tải dữ liệu nền, chat realtime.

## 🎯 Ví dụ minh họa

```js
// Đồng bộ: mỗi dòng phải xong mới đến dòng sau
const name = "Miriam";
const greeting = `Hello, my name is ${name}!`;
console.log(greeting); // Hello, my name is Miriam!

// Bất đồng bộ: fetch không chặn, kết quả đến sau
fetch("https://jsonplaceholder.typicode.com/posts/1")
  .then((res) => res.json())
  .then((post) => console.log(post.title)); // chạy sau, không chặn UI
```

## 📚 Tham khảo / Bài tập

- Chạy `01_introduce-sync-async/app.js` (qua `node app.js` hoặc trình duyệt): quan sát `console.log(greeting)` in ra **undefined** — vì `makeGreeting` trả về một Promise và `setTimeout` không phải Promise nên `await` không lấy được giá trị đó.
- Tự thử: sửa lại `makeGreeting` trả về `Promise.resolve(...)` và thử lại bằng `await` thật sự.