# Service Worker & Web Worker — chạy ngầm, không chặn UI

## 🔑 Khái niệm

**Service Worker** và **Web Worker** đều là các script chạy **ở background**, tách khỏi trang web — giúp thực hiện việc không cần đến tương tác trực tiếp với User UI, giảm tải cho luồng chính (main thread).

**Service Worker** (phục vụ **Offline Web App**):

- Là **proxy** giữa trình duyệt và mạng — có thể chặn request và trả dữ liệu từ **cache**.
- Yêu cầu để web app chạy offline: (**resources**: html/js/css/ảnh) + (**router**). Service Worker đáp ứng cả hai: listener `install`/`activate` để lưu resources vào cache, listener `fetch` để định tuyến.
- Đặc điểm: không gắn với trang cụ thể, **không truy cập DOM**, có thể dừng khi không dùng, **chỉ hoạt động trên HTTPS** (hoặc localhost).
- Đăng ký: `navigator.serviceWorker.register('/service_worker.js')` — trả về **Promise**; phải **same-origin**; vị trí file quyết định phạm vi URL nó quản lý.

**Web Worker** (trong folder này):

- Chạy tính toán nặng trên **thread riêng**, không chặn UI.
- Giao tiếp bằng `postMessage()` / `onmessage`.

## ✅ Điểm mạnh

- Web app chạy nhanh hơn và **chạy được khi offline** (cache + router).
- Tính năng nền: **push notification**, **background sync**.
- Tải công việc nặng khỏi luồng chính → UI mượt, không đơ.
- Dữ liệu cache giúp tải lại trang nhanh như "giật từ local".

## ⚠️ Lưu ý / Hạn chế

- Chỉ hỗ trợ HTTPS (trừ localhost) — dev local cần `localhost`.
- Không truy cập DOM; phải qua `postMessage` để trả kết quả.
- `register()` trả Promise — phải xử lý lỗi, kiểm tra trình duyệt hỗ trợ.
- Vị trí file Service Worker quyết định scope (URL nó điều khiển).
- Lifecycle install → activate cần hiểu rõ để cache đúng phiên bản.

## 💡 Khi nào dùng

- PWA muốn chạy offline (blog, docs, mua hàng...).
- Push notification, background sync dữ liệu.
- Tính toán nặng (xử lý dữ liệu, mã hóa...) không muốn làm đơ UI.

## 🎯 Ví dụ minh họa

```js
// Đăng ký Service Worker (trả Promise, phải HTTPS/same-origin)
if ("serviceWorker" in navigator) {
  navigator.serviceWorker
    .register("/service_worker.js")
    .then((reg) => console.log("SW registered", reg.scope))
    .catch((err) => console.error("SW registration failed", err));
}
```

```js
// Tương tác Web Worker qua postMessage
const worker = new Worker("service_worker.js");
worker.postMessage("hello, worker");     // gửi việc sang worker
worker.onmessage = (msg) => console.log(msg); // nhận kết quả
```

## 📚 Tham khảo / Bài tập

- Mở `06_service-worker/index.html` trong trình duyệt (file dùng `main.js` + `style.css`): bấm **"Calculate Sum"** — worker tính tổng vòng lặp 10 tỷ, bấm **"Change Background"** ngay sau đó: nền vẫn đổi màu (green/blue) vì việc nặng không chặn UI.
- Đọc `main.js` và `service_worker.js`: hiểu luồng `postMessage` → tính toán → `postMessage(sum)` trả về.
- Tự thử: thử đặt vòng lặp 10 tỷ **chạy ngay trong main thread** để thấy UI "đơ" hoàn toàn; sau đó nghiên cứu thêm `navigator.serviceWorker.register` để cảm nhận khác biệt với Service Worker (cache, offline).
- Tham khảo: completejavascript.com (Service Worker cơ bản), MDN "Using Service Workers", video YouTube "Service Worker" liên quan.