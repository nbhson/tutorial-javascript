# V8 Engine — Cách JavaScript được thực thi và tối ưu

## 🔑 Khái niệm

**JavaScript engine** là chương trình/thông dịch viên thực thi mã JavaScript. Có nhiều engine: **V8** (Google, mã nguồn mở, viết bằng C++, dùng cho Chrome và Node.js), **JavaScriptCore/Nitro** (Apple/Safari), **SpiderMonkey** (Mozilla/Firefox), **Chakra** (IE/Edge cũ), **JerryScript** (IoT).

**Tại sao V8 ra đời?** Để tăng tốc JS trong trình duyệt, V8 **biên dịch JS thành machine code** thay vì chỉ thông dịch. Với thời đại hiện tại, V8 chạy theo pipeline:

1. **Parser** đọc mã nguồn → dựng **AST** (cây cú pháp trừu tượng).
2. **Ignition** (interpreter) sinh **bytecode** từ AST — bộ nhớ chỉ bằng ~nửa so với phương pháp biên dịch trước, giúp ích cho mobile.
3. **TurboFan** (optimizing JIT compiler) nhận bytecode và **generate machine code tối ưu** trực tiếp, thay vì biên dịch lại từ nguồn (điểm khác biệt so với Crankshaft cũ). Cả hai ra đời thay cho Full-codegen và Crankshaft.

Để truy cập property **nhanh như ngôn ngữ tĩnh**, V8 dùng:

- **Hidden Class (class ẩn)**: mỗi lần thêm property vào object đồng dạng, V8 tạo class ẩn mới với offset cố định cho property đó; các object cùng shape chia sẻ hidden class → truy cập như "fixed offset" thay vì tra cứu dictionary. Thêm/xóa property theo thứ tự khác nhau tạo **nhánh hidden class riêng** (kém tối ưu).
- **Inline Cache (IC)**: ghi nhớ hidden class của object ở mỗi điểm truy cập property; lần sau nếu cùng loại, bỏ qua quá trình tra cứu và nhảy thẳng tới offset — khi kiểu đổi thì vá lại (cache miss).

Các ảnh trong thư mục minh họa: `rdxxidul7q_4.png` (so sánh dictionary vs fixed offset), `id968au9dy_1.png` + `9jzw4uu3x6_2.png` + `maegljn53n_3.png` (hidden class tăng dần theo `this.firstName`, `this.lastName`), `gq17f5a8fs_8.opt.png` (các nhánh hidden class), `wr2012-inline-cache.png` (cơ chế inline cache), `workflow.jpeg` / `zJeoQML.png` / `code.png` (pipeline Ignition → TurboFan → machine code).

## ✅ Điểm mạnh

- **Tốc độ gần ngôn ngữ biên dịch**: JIT + hidden class + inline cache giúp code "hot" chạy rất nhanh.
- **Bytecode nhẹ**: Ignition giảm bộ nhớ, phù hợp thiết bị di động.
- **Kiến trúc tách tầng**: tối ưu cấp cao (<span>TurboFan</span>) và cấp thấp tách biệt, dễ thêm tính năng ngôn ngữ mới.
- **Reusable hidden classes**: các object cùng shape tái sử dụng class ẩn, tăng tốc cho vòng lặp tạo nhiều object.
- **Inline caching** cắt giảm chi phí lookup lặp lại cho property truy cập nhiều lần.

## ⚠️ Lưu ý / Hạn chế

- Có **deoptimization** khi hidden class/IC đoán sai → quay về bản chậm, tốn thời gian vá lại.
- Cấu trúc object **không nhất quán** (thêm property chỗ này, xóa chỗ kia) → nhiều nhánh hidden class, mất lợi ích tối ưu.
- `Object.freeze` / thiết lập property động theo kiểu dictionary có thể **khóa shape**, ngăn V8 tạo hidden class.
- Hiểu sâu V8 giúp viết code nhanh nhưng **không nên "ép" tối ưu quá mức** để chống lại engine — đo bằng profiler trước khi can thiệp.

## 💡 Khi nào dùng

- Viết **vòng lặp nóng / hot path** (xử lý dữ liệu lớn, game loop) — khai báo object đồng dạng, tránh đổi shape.
- Quyết định đặt property **cùng thứ tự** khi tạo object hàng loạt — tái sử dụng hidden class.
- Nghiên cứu **cách JIT tối ưu** khi benchmark hàm — đo trước thật rồi mới tinh chỉnh.
- Phân biệt interpreter vs compiler để hiểu vì sao cùng đoạn code chạy nhanh hơn sau vài lần lặp (warm-up).
- Khi tự xây dựng **runtime/embed V8** (Node, Deno, Electron...) muốn nắm vòng đời thực thi.

## 🎯 Ví dụ minh họa

```js
// Tạo cùng một lúc nhiều object đồng dạng -> cùng hidden class => truy cập nhanh
function idol(firstName, lastName) {
  this.firstName = firstName;   // tạo hidden class mới, offset 0
  this.lastName  = lastName;    // tạo hidden class mới, offset 1
}
const a = new idol('Takizawa', 'Laura');
const b = new idol('Ivana',    'Baquero');
// a và b cùng shape -> chia sẻ hidden class, IC nhảy thẳng tới offset

// Hỏng: thêm property khác nhau giữa các instance -> nhánh riêng -> chậm hơn
function flaky(x) { this.a = x; }
const p1 = new flaky(1); p1.b = 2; p1.c = 3;   // shape 3 property
const p2 = new flaky(1); p2.c = 2; p2.b = 3;   // thứ tự khác -> khác hidden class
```

## 📚 Tham khảo / Bài tập

- Xem ảnh minh họa trong thư mục này theo thứ tự: `rdxxidul7q_4.png` → `id968au9dy_1.png` → `9jzw4uu3x6_2.png` → `maegljn53n_3.png` → `gq17f5a8fs_8.opt.png` (hidden class), rồi `wr2012-inline-cache.png` (inline cache), cuối cùng `workflow.jpeg` → `zJeoQML.png` → `code.png` (Ignition → TurboFan).
- Tự làm: mở DevTools → Performance, record một vòng lặp 1 triệu lần tạo object đồng dạng vs không đồng dạng; so sánh thời gian để thấy lợi ích hidden class.
- Tự làm: thêm `--trace-opt --trace-deopt` khi chạy Node (`node --trace-deopt script.js`) để xem hàm nào bị deopt — nhận biết nguyên nhân mất tối ưu.
- Tự làm: chạy node với cờ `--print-opt-code` cho một hàm nhỏ để đọc machine code TurboFan tạo ra (khó, chỉ để trải nghiệm pipeline).