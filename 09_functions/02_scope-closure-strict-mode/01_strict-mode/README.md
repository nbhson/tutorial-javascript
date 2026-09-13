# Strict Mode (Chế độ nghiêm ngặt)

## 🔑 Khái niệm

Strict mode xuất hiện từ **ES5 (ECMAScript 2009)** với mục đích giúp JavaScript "chặt tay" hơn: **báo lỗi** thay vì âm thầm bỏ qua những tình huống nguy hiểm, từ đó code an toàn và dễ bảo trì hơn.

Bật bằng cách đặt chuỗi **`"use strict";`** ở một trong ba vị trí:
1. **Đầu file** (`app.js`) — áp dụng cho toàn file.
2. **Ngay sau thẻ mở `<script>`** — áp dụng cho cả script đó.
3. **Đầu thân hàm** — chỉ áp dụng trong hàm (local scope).

Quan trọng: chuỗi khai báo phải nằm **trước mọi câu lệnh/nhận xét định nghĩa** — nếu phía trước đã có code, nó không có tác dụng.

**Strict mode cấm / báo lỗi khi:**

| Hành động | Ví dụ |
|---|---|
| Gán biến chưa khai báo | `x = 100;` → lỗi |
| `delete` biến, hàm, prototype của object | `delete women;` → lỗi |
| Gán lại thuộc tính `writable: false` | poperty đóng băng → lỗi |
| Gán số octal dạng `010` | `let octal = 010;` → lỗi |
| Dùng từ khóa nhạy cảm (eval, arguments, public...) làm tên biến | `let public = 100;` → lỗi |
| Hàm có hai tham số trùng tên | `function sum(a, a) {}` → lỗi cú pháp |
| Khai báo hàm trong block rồi gọi ngoài block | `if (true) { function sum(){} } sum();` → lỗi |
| `this` không có đối tượng gọi | `function test(){ console.log(this) } test()` → `undefined` |

Nguyên nhân cốt lõi: strict mode **ngăn các lỗi ngầm** (silent errors) của bản thân JS ở thời kỳ đầu — như tự tạo biến global từ một phép gán "lỡ tay", không cho xóa, và **tránh tạo nhiều biến global** (tiết kiệm bộ nhớ).

## ✅ Điểm mạnh

- **Bắt lỗi từ sớm**: tên biến sai chính tả trong phép gán sẽ lỗi ngay thay vì âm thầm tạo biến global mới.
- **Ngăn dùng biến global không định trước** → sử dụng bộ nhớ hiệu quả và tránh xung đột.
- Cấm các cú pháp không an toàn (octal, duplicate params) → chuẩn hóa code.
- `this` rõ ràng hơn: hàm thường gọi trực tiếp có `this === undefined`, không ngầm trỏ `window`.
- Được toàn bộ mô-đun ES6, class, và đa số framework tự bật mặc định.
- Dễ áp dụng: chỉ cần một dòng `"use strict";` ở đầu.

## ⚠️ Lưu ý / Hạn chế

- **Chỉ có tác dụng từ vị trí khai báo trở đi** — đặt sau code thì phần trước không bị kiểm soát.
- Khác với một số lầm tưởng: `"use strict"` là **chuỗi**, không phải câu lệnh thông thường; đặt không đúng chỗ sẽ bị bỏ qua im lặng.
- Kết hợp với code cũ (viết theo kiểu "xả láng") có thể vỡ vì vô tình vi phạm quy tắc.
- Các object frozen / `writable: false` — strict mode sẽ `throw` (chứ không bỏ qua), đừng bất ngờ khi thấy lỗi.
- Không khắc phục mọi lỗi lập trình — chỉ giúp phát hiện sớm một lớp lỗi nhất định.

## 💡 Khi nào dùng

- Khởi đầu mọi file script/mô-đun mới — thói quen tốt mặc định.
- Sửa bug "biến toàn cục mọc tùy tiện" trong code cũ.
- Viết thư viện — ép người dùng khai báo đúng.
- Học tập để hiểu chính xác hành vi của JS (đặc biệt về `this`, gán, delete).

## 🎯 Ví dụ minh họa

```js
// Nội dung app.js trong thư mục (sau khi thêm "use strict")
"use strict";

function test() {
  console.log(this); // undefined (không phải window/global)
}
test();

console.log(0 == false); // true — so sánh trừu tượng không bị cấm, còn dùng === để an toàn
```

```js
// Các hành vi bị cấm
"use strict";
x = 100;              // TypeError: assignment to undeclared variable
delete someFn;        // TypeError
let v = 010;          // SyntaxError — octal
function f(a, a) {}   // SyntaxError — trùng tham số
```

## 📚 Tham khảo / Bài tập

- Thêm `"use strict";` vào đầu `app.js` rồi mở `index.html` (Console) hoặc chạy `node app.js` — quan sát `this` thành `undefined`.
- Tự thử: bỏ `"use strict"` và log `this` trong hàm — thấy nó trỏ global (`window`), chứng minh sự khác biệt.
- Tự thử từng trường hợp bị cấm ở README (gán biến chưa khai báo, duplicate params, octal) và xem kiểu lỗi.
- Ghi nhớ 3 cách bật: đầu file, đầu `<script>`, đầu hàm.