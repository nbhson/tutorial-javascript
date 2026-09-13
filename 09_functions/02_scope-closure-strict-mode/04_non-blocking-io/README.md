# Non-blocking I/O — Xử lý không chặn

## 🔑 Khái niệm

**Non-blocking I/O** là cơ chế *không chặn* luồng xử lý khi chờ thao tác nhập/xuất (I/O). Nghĩa là: khi chương trình đang chờ dữ liệu (đọc file, gọi API, nhập liệu), nó **vẫn tiếp tục chạy các công việc khác** thay vì đứng yên chờ.

Hai khái niệm đối lập:

| | Blocking I/O | Non-blocking I/O |
|---|---|---|
| Hành vi | đợi thao tác xong rồi mới chạy tiếp | bắt đầu thao tác, quay lại khi có kết quả |
| Hệ quả | lãng phí thời gian chờ | tận dụng thời gian để làm việc khác |
| Nhiều việc cùng lúc | không (đơn luồng, tuần tự) | "đa nhiệm" trên cùng một luồng |

Tác giả liên hệ trực quan: hệ điều hành Windows xử lý "đa luồng" vì bạn có thể vừa copy, vừa xóa, vừa chạy nhiều chương trình dù thao tác trước chưa xong. Ngược lại, JavaScript là ngôn ngữ **đơn luồng** — một main thread xử lý mọi việc. Vì vậy JS dùng cơ chế **bất đồng bộ và sự kiện** (async + event loop) để không bị "đứng hình" khi gặp thao tác I/O chậm.

Điểm mấu chốt cần hiểu:
- JavaScript **một luồng** nhưng **không chặn** — nhờ `setTimeout`, `fetch`, sự kiện, event loop.
- Khi gặp I/O, gọi hàm **callback / promise** và rời đi làm việc khác; khi xong, tác vụ quay lại thực thi.
- Lập trình hướng sự kiện: chỉ khi có tác động (click, dữ liệu về...) mới xử lý thêm → **tiết kiệm tài nguyên hệ thống** so với chạy quá nhiều luồng thật.

## ✅ Điểm mạnh

- **Không lãng phí thời gian chờ**: một luồng vẫn phục vụ được rất nhiều tác vụ I/O.
- **Hiệu năng phục vụ đồng thời tốt** (đặc biệt Node.js cho Web server: nhiều request cùng lúc).
- **Tiết kiệm tài nguyên**: không cần tạo hàng trăm luồng như các ngôn ngữ khác.
- Mô hình dựa trên sự kiện tự nhiên, dễ hiểu với UI: click → xử lý.
- Hệ sinh thái async hiện đại: Promise, `async/await` làm code bất đồng bộ gần như code đồng bộ.

## ⚠️ Lưu ý / Hạn chế

- Đơn luồng + không chặn nghĩa là **một tác vụ nặng (tính toán lớn, vòng lặp dài) sẽ "chiếm" luồng** và làm mọi thứ khác đứng hình — phải chia nhỏ hoặc dùng Worker.
- Tư duy bất đồng bộ khó hơn — dễ viết gián đoạn logic, thiếu await, quên xử lý lỗi.
- Thứ tự thực thi không theo thứ tự viết code — cần hiểu event loop.
- Không phải "đa luồng thật sự" như C++/Java — song song CPU-bound không tốt.
- Callback sâu gây callback hell nếu không dùng Promise/async.

## 💡 Khi nào dùng

- Gọi API / `fetch` — UI cần phản hồi ngay dù mạng chậm.
- Đọc/ghi file trong Node.js (không chặn server).
- Timer, sự kiện người dùng, socket, realtime.
- Query cơ sở dữ liệu, gọi service bên thứ ba.
- Batch xử lý nhiều request đồng thời (ví dụ gửi nhiều request song song rồi `Promise.all`).

## 🎯 Ví dụ minh họa

```js
console.log("1. bắt đầu");

setTimeout(() => console.log("3. timer xong (bất đồng bộ)"), 0);

console.log("2. chạy tiếp ngay — không bị chặn");

// Kết quả in ra: 1. bắt đầu → 2. chạy tiếp → 3. timer xong
// Dù timeout = 0, nó vẫn chạy SAU các câu lệnh đồng bộ
```

```js
// Ví dụ blocking (giả lập — chờ đợi thủ công) sẽ làm UI đứng hình:
// while (true) {} // vòng lặp vô hạn chiếm luồng — tránh!
```

## 📚 Tham khảo / Bài tập

- Thư mục này **không có file code** — chỉ có README lý thuyết (kiểm tra bằng `ls`).
- Tự thử: mở Console trình duyệt rồi chạy ví dụ `setTimeout` ở trên để thấy thứ tự in ra.
- Tự thử: gọi API giả lập với `fetch` và so sánh UI không bị đơ trong lúc chờ.
- Liên hệ: đọc lại `02_builtin-functions/app.js` (setTimeout/setInterval) và phần callbacks để thấy non-blocking trong thực tế.
- Tự nghiên cứu "event loop" + microtask (`Promise`) để hiểu chi tiết thứ tự thực thi.