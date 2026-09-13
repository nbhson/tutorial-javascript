# IIFE — Hàm được gọi ngay lập tức

## 🔑 Khái niệm

**IIFE** (Immediately Invoked Function Expression) là một hàm được **định nghĩa và gọi ngay lập tức** trong cùng một biểu thức. Cú pháp điển hình:

```js
(function () {
  console.log("NOW NOW");
})();
```

Giải thích các phần:
- `(function () { ... })` — bọc hàm trong `()` để nó được hiểu là một **expression** (không phải khai báo).
- `()` ngay sau đó — **gọi hàm** luôn.

IIFE còn được gọi là **self-invoking function** và tạo ra một **phạm vi riêng (private scope)**: biến bên trong không truy cập được từ ngoài, nhưng bên trong có thể dùng mọi thứ bên ngoài. Đó chính là công cụ "che giấu dữ liệu" cổ điển trước khi ES6 có module.

Ví dụ mạnh nhất trong README cũ — mô-đun `app2` bằng IIFE: biến `cars` giữ kín bên trong, bên ngoài chỉ thao tác qua các hàm `all`, `add`, `delete`, `update` được trả về. Điểm lợi: bên ngoài không thể đặt `app.cars = null` làm hỏng dữ liệu như phiên bản `app` thường.

## ✅ Điểm mạnh

- **Tạo phạm vi riêng** — không tạo biến global, không xung đột tên khi dùng nhiều thư viện.
- **Private dữ liệu thật sự** — dễ dàng giấu trạng thái nội bộ và chỉ lộ API cần thiết.
- Gọi ngay, trả về luôn kết quả/object — gọn cho khởi tạo.
- Là nền tảng của pattern "module pattern" trước ES6.
- Gom được logic khởi tạo, ví dụ gắn sự kiện, khởi tạo state, một lần duy nhất.
- Trả về object/function qua biến gán: `const app = (function(){ ... return {...} })();`

## ⚠️ Lưu ý / Hạn chế

- **Phải có dấu `;` trước IIFE** — nếu dòng trước kết thúc bằng biểu thức (nhiểu lúc do tự động chèn `;` bị bỏ qua), dễ gây lỗi ghép hai câu lệnh lại với nhau.
- Có thể ép bằng toán tử khác thay `()` như `!function(){...}()`, `+`, `-`... nhưng kém đọc.
- IIFE tạo ra một phạm vi qua mỗi lần gọi — tạo quá nhiều thì tốn bộ nhớ như các hàm thường.
- Bản thân nó không giải quyết hoàn toàn việc chia module lớn — hiện đại nên dùng ES modules (`import`/`export`).
- Cú pháp dễ quên dấu `()` gọi — viết sai thành khai báo thường.

## 💡 Khi nào dùng

- Bọc code khởi tạo/khởi tạo một lần (hide helpers, khởi tạo state).
- Tạo module "private" cho dữ liệu nhạy cảm (như ví dụ `app2` với `cars`).
- Tránh xung đột biến toàn cục khi nhúng nhiều thư viện.
- Khi cần một phạm vi đóng gói nhanh trong script không có module.

## 🎯 Ví dụ minh họa

```js
// Nội dung app.js trong thư mục
const callNow = function () {
  console.log("NOW");
};
callNow();                    // gọi thường, cần ; trước IIFE

(function () {
  console.log("NOW NOW");
})();                         // IIFE — gọi ngay khi tạo

(function PrintMessage(message) {
  console.log("Message:", message);
  return message;
})("Chao ban");               // Message: Chao ban

// Module private bằng IIFE
const app2 = (function () {
  const cars = [];            // private — ngoài không đổi được
  return {
    all() { return cars; },
    add(car) { cars.push(car); },
    update(index) { cars.splice(index, 1); },
  };
})();
app2.add("Winner 2022");
console.log(app2.all());      // ["Winner 2022"]
```

## 📚 Tham khảo / Bài tập

- Mở `index.html` (Console) hoặc chạy `node app.js` để thấy `NOW`, `NOW NOW`, `Message: Chao ban`.
- Tự thử: xóa dòng `callNow();` và đặt IIFE ngay sau `const callNow = function(){...}` **không có `;`** — chạy để xem lỗi và hiểu vì sao phải có `;`.
- Tự thử: thử `app2.cars` bên ngoài → trả `undefined` (private); còn `app2.add("Xe mới")` vẫn hoạt động.
- Tự thử: viết IIFE trả về một function đếm `next()` mỗi lần gọi tăng 1, mà biến đếm nằm kín bên trong.