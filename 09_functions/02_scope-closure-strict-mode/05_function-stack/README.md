# Call Stack và Scope Chain (Function Stack)

## 🔑 Khái niệm

**Call stack (ngăn xếp gọi hàm)** là cơ chế JavaScript dùng để theo dõi "đang chạy hàm nào, hàm nào chờ kết quả". Hoạt động theo nguyên tắc **LIFO** (Last In, First Out): hàm nào được gọi sau cùng thì chạy xong và **pop** ra trước, hàm gọi trước "đứng chờ".

```js
function a() { b(); }
function b() { c(); }
function c() { console.trace(); } // in ra stack trace
a();
```

Thứ tự khi chạy: `a` → `b` → `c` (push lần lượt), rồi `c` xong → pop, `b` xong → pop, `a` xong → pop. Mỗi lần gọi hàm tạo **một execution context** (bối cảnh thực thi) — chứa biến cục bộ, `this`, phạm vi — và context đó nằm trên ngăn xếp cho đến khi hàm trả về.

**Scope chain (chuỗi phạm vi)** là chuỗi các phạm vi mà JavaScript **dò tìm biến** từ trong ra ngoài. Hàm con nhìn thấy biến của mình, rồi của hàm cha, rồi global — nhưng không phải ngược lại.

```js
let g = 1;
function outer() {
  let o = 2;
  function inner() {
    console.log(g, o); // tìm g (global), rồi o (outer) — theo scope chain
  }
  inner();
}
outer(); // 1 2
```

Khi tìm biến `g` trong `inner`: không có trong `inner` → nhìn lên `outer` → không có → nhìn ra global → thấy `g = 1`. Đó chính là scope chain.

## ✅ Điểm mạnh

- Giúp **debug stack trace** dễ dàng: đọc từ dưới lên biết "ai gọi ai".
- `console.trace()` là công cụ in call stack chuẩn, sẵn sàng ngay.
- Hiểu call stack giải thích được lỗi **"Maximum call stack size exceeded"** (đệ quy vô hạn).
- Scope chain giải thích cơ chế closure và phạm vi biến một cách trực quan.
- Nhận biết được giới hạn: đệ quy sâu bao nhiêu có thể nổ ngăn xếp.
- Là nền tảng để hiểu bất đồng bộ (event loop) và `this` binding.

## ⚠️ Lưu ý / Hạn chế

- Call stack có **giới hạn độ sâu** — đệ quy không kiểm soát sẽ tràn ngăn xếp (stack overflow).
- Mỗi lần gọi hàm đều tốn bộ nhớ cho execution context — lồng/đệ quy quá nhiều gây tốn tài nguyên.
- Scope chain giúp truy cập biến ngoài nhưng cũng là nơi phát sinh **closure giữ tham chiếu** (xem `03_closure`).
- Thứ tự "ngược" của stack (hàm gọi sau chạy trước) khiến người mới dễ nhầm thứ tự thực thi.
- Không thể nhìn trực tiếp call stack khi code chưa chạy — cần breakpoint hoặc `console.trace`.

## 💡 Khi nào dùng

- Debug 1 lỗi "hàm này được gọi từ đâu" — mở DevTools Sources/Console stack trace.
- Kiểm tra ngăn xếp trong thời gian chạy bằng `console.trace()`.
- Giải thích lỗi tràn ngăn xếp khi đệ quy.
- Tối ưu vòng lặp/đệ quy để tránh gọi hàm lồng quá sâu.
- Học closure, bất đồng bộ và event loop — mọi thứ đều xoay quanh call stack.

## 🎯 Ví dụ minh họa

```js
// Nội dung app.js trong thư mục
function a() { b(); }
function b() { c(); }
function c() {
  console.log("stack:");
  console.trace(); // in ra a → b → c
}
a();

// Scope chain: inner tìm g, o qua chuỗi phạm vi
let g = 1;
function outer() {
  let o = 2;
  function inner() {
    console.log(g, o); // 1 2
  }
  inner();
}
outer();
```

## 📚 Tham khảo / Bài tập

- Mở `index.html` (Console) hoặc chạy `node app.js` để xem **stack trace** in ra 3 cấp `a → b → c` và kết quả `1 2`.
- Tự thử: đổi `console.trace()` thành `console.log(new Error().stack)` — cùng ý nghĩa.
- Tự thử: thêm `function d() { return c(); }` để stack dài hơn, quan sát thứ tự.
- Tự thử đệ quy không dừng: `function boom() { boom(); } boom();` → xem báo "Maximum call stack size exceeded".
- Tự thử: trong `inner`, thêm biến `let x = 9;` và đổi `console.log(g, o, x)` — thấy tìm trong nội bộ trước.