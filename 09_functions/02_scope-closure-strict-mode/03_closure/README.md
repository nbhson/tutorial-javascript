# Closure (Bao đóng)

## 🔑 Khái niệm

**Closure** là một hàm có khả năng **"ghi nhớ" nơi nó được tạo** và **truy cập được các biến ở phạm vi bên ngoài** của chính nó — ngay cả sau khi hàm ngoài đã chạy xong. Nói cách khác: hàm con "đóng gói" (bao đóng) môi trường nơi nó sinh ra.

Khái niệm này có **3 yếu tố cùng xuất hiện**:
1. Có **hàm lồng trong hàm** (`increase` nằm trong `createCouter`).
2. Hàm trong **tham chiếu biến của hàm ngoài** (`couter`).
3. Hàm trong được **trả ra ngoài** hoặc giữ lại → "sống sót" sau khi hàm ngoài kết thúc.

Ví dụ kinh điển trong `app.js`:

```js
function createCouter() {
  let couter = 0;
  function increase() {
    return ++couter; // tham chiếu biến ngoài phạm vi
  }
  return increase;
}

const _couter1 = createCouter();
console.log(_couter1()); // 1
console.log(_couter1()); // 2 — vẫn "nhớ" couter = 1 ở lần trước
console.log(_couter1()); // 3
```

Bạn gọi `createCouter()` **một lần** → tạo **một phạm vi** riêng với biến `couter = 0`. Hàm `increase` trả về được giữ ở biến ngoài, nhờ closure mà nó vẫn "nhìn thấy" `couter` và mỗi lần gọi lấy **giá trị mới nhất** của biến đó → `1, 2, 3`.

README cũ còn cho hai ứng dụng thực tế:
- **`createLogger(namespace)`** — trả về hàm log "nhớ" namespace, ra `[Info] Bắt đầu gửi mail!`, `[Error] Có lỗi!`.
- **`createStorage(key)`** — trả về module đọc/ghi localStorage; `store` được closure giữ kín.

## ✅ Điểm mạnh

- **Viết code gọn**: tạo function factory (hàm sản xuất hàm) mà không cần class.
- **Biểu diễn tính private trong OOP**: biến nội bộ không lộ ra ngoài, chỉ lộ API trả về.
- **Lưu giữ trạng thái** giữa các lần gọi (counter, cache, storage) một cách tự nhiên.
- Giữ giá trị **mới nhất** của biến (như `couter` tăng dần) — không bị snapshot cũ.
- Là nền tảng của các pattern hiện đại: currying, memoization, module, hooks (React `useState`/`useEffect` về bản chất dựa trên closure).
- Tạo ra nhiều "instance" độc lập: mỗi lần gọi `createX()` có phạm vi riêng.

## ⚠️ Lưu ý / Hạn chế

- **Biến trong closure không bị dọn** khỏi bộ nhớ khi hàm ngoài kết thúc — nếu giữ tham chiếu lâu, có thể **thất thoát bộ nhớ (memory leak)**. Đây là 1 trong 4 nguyên nhân chính gây rò rỉ bộ nhớ trong JS.
- Nếu không hiểu rõ "tham chiếu mới nhất", dễ code ra bug trong vòng lặp (ví dụ gắn `setTimeout` trong `for`).
- Quá nhiều closure lồng nhau làm code khó đọc, khó debug.
- Cần chủ động "release" (null ra tham chiếu) khi không còn dùng module lớn.

## 💡 Khi nào dùng

- Tạo factory/function riêng với cấu hình cố định (`createLogger("Info")`).
- Bộ đếm, cache, storage private có API nhỏ gọn.
- Đóng gói state cho widget/module mà không cần class.
- Trong hàm `useState`/`useEffect` của React, tránh bắt được biến cũ — hiểu closure để tránh bug.
- Xử lý sự kiện/timer cần nhớ biến tại thời điểm tạo.

## 🎯 Ví dụ minh họa

```js
// Nội dung app.js trong thư mục
function createCouter() {
  let couter = 0;
  function increase() {
    return ++couter;
  }
  return increase;
}

const _couter1 = createCouter();   // một phạm vi riêng
console.log(_couter1()); // 1
console.log(_couter1()); // 2
console.log(_couter1()); // 3

// Factory nhớ "namespace"
function createLogger(namespace) {
  return (message) => `[${namespace}] ${message}`;
}
const logInfo = createLogger("Info");
console.log(logInfo("Bắt đầu gửi mail!")); // [Info] Bắt đầu gửi mail!
```

## 📚 Tham khảo / Bài tập

- Mở `index.html` (Console) hoặc chạy `node app.js` để thấy `1 2 3`.
- Tự thử: gọi `createCouter()` **hai lần** tạo hai biến `_c1`, `_c2` và kiểm tra chúng tăng **độc lập** với nhau (mỗi cái bắt đầu từ 1).
- Tự thử: viết `createLogger` với `logError` có namespace `"Error"` để thấy hai closure độc lập.
- Đọc thêm về thất thoát bộ nhớ do closure: https://viblo.asia/p/cach-javascript-hoat-dong-quan-ly-vung-nho-4-cach-giai-quyet-van-de-that-thoat-vung-nho-3Q75w9Q7ZWb