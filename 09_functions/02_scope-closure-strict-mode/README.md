# Hàm — Phạm vi, Closure, Strict Mode

## 🔑 Khái niệm

Nhóm này đi sâu vào **vòng đời và phạm vi của hàm** — trả lời các câu hỏi: biến tồn tại ở đâu, hàm nhớ được gì, chương trình chạy theo thứ tự nào. Cụ thể:

| Thư mục | Nội dung |
|---|---|
| `01_strict-mode/` | chế độ nghiêm ngặt `"use strict"` — gắt gao hơn, an toàn hơn |
| `02_iife/` | IIFE — hàm được gọi ngay lập tức, mang tính "private" |
| `03_closure/` | closure — hàm nhớ biến của phạm vi bên ngoài khi đã tạo |
| `04_non-blocking-io/` | lý thuyết bất đồng bộ: JavaScript không chặn luồng |
| `05_function-stack/` | call stack (ngăn xếp gọi hàm) và scope chain |

Đây là phần **nền tảng quan trọng nhất** để hiểu các khái niệm nâng cao: `this`, event loop, module, hooks (React). Khi hiểu closure và scope chain, bạn sẽ hiểu tại sao mảng/object bị "giữ tham chiếu", tại sao IIFE tồn tại, và vì sao cần `"use strict"`.

## ✅ Điểm mạnh

- Bóc tách đúng những khái niệm người phỏng vấn thường hỏi: closure, IIFE, call stack, strict mode.
- Lý thuyết (non-blocking I/O) kết hợp thực hành (strict mode, IIFE, closure, function stack).
- Mỗi thư mục con có ví dụ chạy ngay được.
- Các ví dụ theo tình huống thật: module "private" bằng IIFE, biến đếm bằng closure, `console.trace()` xem call stack.
- Có tài liệu tham khảo về quản lý bộ nhớ (thất thoát bộ nhớ do closure) trong `03_closure`.
- Kết nối tốt với phần callbacks/async — tạo cây kiến thức mạch lạc.

## ⚠️ Lưu ý / Hạn chế

- Closure giữ tham chiếu biến nên **không được dọn** — có thể gây memory leak nếu không kiểm soát.
- IIFE phải có dấu `;` trước đó (hoặc trước khi viết IIFE) tránh lỗi kết hợp với dòng trước.
- Strict mode áp dụng cho toàn file hoặc toàn hàm — khai báo giữa chừng sẽ không có tác dụng với phần trước.
- `04_non-blocking-io` chỉ có **lý thuyết** (không có file code) — nên tự tìm thêm demo event loop.
- Call stack có giới hạn độ sâu — đệ quy không kiểm soát sẽ "tràn ngăn xếp".

## 💡 Khi nào dùng

- Bọc code riêng tư, tránh xung đột biến toàn cục → IIFE.
- Tạo biến "nhớ" trạng thái giữa các lần gọi (counter, memoized function, hooks) → closure.
- Bật `"use strict"` cho script/module để bắt lỗi tiềm ẩn (quên khai báo biến, gán readonly...).
- Hiểu thứ tự chạy và độ sâu của lời gọi hàm khi debug stack trace.
- Nắm bắt bản chất bất đồng bộ của JS khi làm việc với timer, fetch, event.

## 🎯 Ví dụ minh họa

```js
// Closure — biến đếm nhớ trạng thái
function createCounter() {
  let count = 0;
  return () => ++count;
}
const c = createCounter();
console.log(c(), c(), c()); // 1 2 3

// IIFE — private + gọi ngay
const app = (() => {
  const cars = [];
  return { add: car => cars.push(car), all: () => [cars] };
})();
```

## 📚 Tham khảo / Bài tập

- Đọc lý thuyết + chạy thử từng file trong các thư mục con theo thứ tự: `01_strict-mode/app.js` → `02_iife/app.js` → `03_closure/app.js` → `05_function-stack/app.js`.
- `04_non-blocking-io` chỉ có README lý thuyết — đọc kỹ và tìm thêm demo `setTimeout`/`Promise` so sánh blocking.
- Tự thử: kết hợp IIFE + closure để tạo module `counter` được, đếm tăng từ bên ngoài nhưng biến `count` không truy cập trực tiếp được.