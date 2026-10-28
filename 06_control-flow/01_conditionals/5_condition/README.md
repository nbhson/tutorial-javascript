# Điều kiện rẽ nhánh — Thực hành (Conditionals thực hành) — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

Thư mục này chứa **3 file thực hành** các cách rẽ nhánh cơ bản nhất trong JavaScript. Cả ba cùng giải quyết một bài toán mẫu — "kiểm tra một giá trị rồi in ra kết quả tương ứng" — nhưng với **cách tư duy và cú pháp khác nhau**:

| File | Cú pháp | Tư duy | Phù hợp nhất khi |
|---|---|---|---|
| `1_if.js` | `if...else if...else` | "Nếu A thì..., nếu B thì..., còn lại thì..." | Điều kiện phức tạp, so sánh khoảng |
| `2_switch-case.js` | `switch...case` | "Giá trị này là gì? Nếu là X thì..., nếu là Y thì..." | So sánh một giá trị với nhiều trường hợp cố định |
| `3_toan-tu-3-ngoi.js` | Ternary `? :` | "Điều kiện đúng thì lấy A, sai thì lấy B" | Chọn 1 trong 2 giá trị, viết trong 1 dòng |

Điểm khác biệt then chốt:
- `if` **linh hoạt nhất** — dùng được với mọi phép so sánh (`>`, `<`, `>=`, `!=`, `&&`, `||`).
- `switch` **chỉ so sánh bằng** (`===`) — không so sánh được khoảng giá trị.
- Ternary **chỉ có 2 nhánh** — không mở rộng được thành nhiều điều kiện phức tạp.

Tất cả ba đều chạy độc lập bằng `node <tên-file>.js` — thay đổi giá trị biến `date` trong mỗi file để quan sát cách mỗi cú pháp xử lý cùng một đầu vào.

## 📐 Cấu trúc / Cú pháp

### `1_if.js` — if...else if...else
```js
var date = 2;

if (date === 2) {
  console.log("Hôm nay là thứ 2"); // date = 2 → chạy
} else if (date === 3) {
  console.log("Hôm nay là thứ 3"); // date = 3 → chạy
} else {
  console.log("Thứ khác");        // date ≠ 2 và ≠ 3 → chạy
}
```
- Chạy **theo thứ tự từ trên xuống**.
- Nhánh đầu tiên **đúng** sẽ thắng — các nhánh sau bị bỏ qua dù cũng đúng.
- `else` là tùy chọn — có thể bỏ nếu không cần nhánh mặc định.

### `2_switch-case.js` — switch...case
```js
var date = 2;

switch (date) {
  case 2:
    console.log(2); // date = 2 → in 2
    break;          // thoát switch
  default:
    console.log("default"); // date ≠ 2 → in "default"
    break;
}
```
- So sánh **nghiêm ngặt `===`** — `case "2"` không khớp với `2`.
- `break` **bắt buộc** nếu không muốn fall-through.
- `default` chạy khi không case nào khớp — nên luôn có.

### `3_toan-tu-3-ngoi.js` — Ternary
```js
// "Sơn" có 3 ký tự → length > 3 là false → trả về false
console.log(("Sơn").length > 3 ? true : false); // false

// "Nguyễn" có 6 ký tự → length > 3 là true → trả về true
console.log(("Nguyễn").length > 3 ? true : false); // true
```
- Cấu trúc: `điều_kiện ? giá_trị_đúng : giá_trị_sai`.
- Là **expression** — trả về giá trị, có thể gán biến hoặc truyền vào hàm.

## ✅ Điểm mạnh

1. **Ba file bổ sung lẫn nhau** — so sánh trực tiếp cách viết của từng cú pháp cùng một bài toán.
2. **Dữ liệu đời thường** — số thứ ngày trong tuần, tên có dấu tiếng Việt — dễ hình dung.
3. **Chạy độc lập** — mỗi file chạy bằng `node` không cần trình duyệt, kết quả hiện ngay trong terminal.
4. **Ghép cặp thực hành — lý thuyết** — mỗi file tương ứng với một khái niệm trong tài liệu conditionals.
5. **Khối code ngắn** — dễ hiểu ngay cả với người mới bắt đầu, không có boilerplate phức tạp.
6. **Thay đổi 1 biến** — chỉ cần đổi `date` để test tất cả các nhánh, dễ dàng quan sát behavior.
7. **Minh họa fall-through** — file `2_switch-case.js` dễ dàng minh họa lỗi quên `break`.
8. **Dùng được trong interview** — viết cùng một logic bằng 3 cách khác nhau là câu hỏi phỏng vấn kinh điển.

## ⚠️ Bẫy thường gặp & Hạn chế

1. **Nhầm `=` (gán) với `===` (so sánh)** trong điều kiện — `if (date = 2)` gán 2 vào date rồi so sánhTruthy.
   ```js
   if (date = 2) { console.log("luôn chạy"); } // date bây giờ = 2, điều kiện = true
   ```

2. **Quên `break` trong `switch`** — fall-through chạy tiếp case phía dưới, kết quả sai.
   ```js
   switch (2) {
     case 2: console.log("hai");
       // quên break → chạy tiếp
     default: console.log("default");
   }
   // In: "hai" rồi "default" ← bug!
   ```

3. **`switch` không so sánh được khoảng** — không thể viết `case > 8: return "Giỏi"`.
   ```js
   switch (score) {
     // case score > 8: return "Giỏi" // ❌ Cú pháp sai
   }
   // Phải dùng if...else nếu cần so sánh khoảng
   ```

4. **Ternary không nên dùng khi nhánh đúng/sai có nhiều câu lệnh** — mất tính rõ ràng.
   ```js
   // ❌ Không nên
   const x = condition ? { doA(); doB(); } : { doC(); doD(); };
   // ✅ Nên dùng if/else
   ```

5. **`else if` chạy theo thứ tự** — hoán đổi thứ tự điều kiện có thể đổi kết quả nếu điều kiện chồng chéo.
   ```js
   if (score > 70) { /* "Tốt" */ }
   else if (score > 80) { /* "Giỏi" */ } // Bỏ qua nếu score = 85 vì đã trúng if trên
   ```

6. **Ternary lồng nhau quá nhiều** — khó đọc, khó debug.
   ```js
   // ❌ 4 nhánh lồng — tệ
   const x = a ? b : c ? d : e ? f : g;
   // ✅ Chuyển sang if/else
   ```

## 💡 Khi nào dùng

1. **`1_if.js`** — khi điều kiện không tương đương đơn giản: so sánh khoảng (`score >= 8`), kết hợp nhiều điều kiện (`age >= 18 && hasID`), hoặc kiểm tra truthy/falsy.
2. **`2_switch-case.js`** — khi một biến chỉ nhận vài giá trị cụ thể: ngày trong tuần (1-7), mã trạng thái (200, 404, 500), type user (`"admin"`, `"user"`).
3. **`3_toan-tu-3-ngoi.js`** — khi chỉ cần chọn 1 trong 2 giá trị để gán/trả về/in ra: `const label = isActive ? "Bật" : "Tắt"`.
4. **So sánh cách tiếp cận** — muốn chọn phong cách phù hợp với dự án (công ty ưa switch hay if).
5. **Viết code test-friendly** — if/switch dễ mock hơn ternary trong unit test.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: `1_if.js` — If...else if...else
```js
var date = 2; // Đổi thành 1, 3, 4, 5, 6, 7 để thử các nhánh

if (date === 2) {
  console.log("Hôm nay là thứ 2"); // date = 2 → in dòng này
} else if (date === 3) {
  console.log("Hôm nay là thứ 3"); // date = 3 → in dòng này
} else {
  console.log("Thứ khác");        // date = 1,4,5,6,7 → in dòng này
}
```

### Ví dụ 2: `2_switch-case.js` — Switch...case
```js
var date = 2; // Đổi thành 3, 4, 5 để thấy default chạy

switch (date) {
  case 2:
    console.log(2); // date = 2 → in 2
    break;          // break thoát switch
  default:
    console.log("default"); // date ≠ 2 → in "default"
    break;
}
```

### Ví dụ 3: `3_toan-tu-3-ngoi.js` — Ternary
```js
// "Sơn" có 3 ký tự → length > 3 là false → trả về false
console.log(("Sơn").length > 3 ? true : false); // false

// Thử với tên dài hơn
console.log(("Nguyễn").length > 3 ? true : false); // true

// Ứng dụng thực tế: check chẵn lẻ
console.log(100 % 2 === 0 ? "Chẵn" : "Lẻ"); // "Chẵn"
console.log(99 % 2 === 0 ? "Chẵn" : "Lẻ");  // "Lẻ"
```

### Ví dụ 4: Nếu đổi `date = 3` trong `1_if.js`
```js
var date = 3;
// Kết quả: "Hôm nay là thứ 3"
// Giải thích: date !== 2 (if đầu sai) → kiểm tra else if date === 3 (đúng) → in "Hôm nay là thứ 3"
```

### Ví dụ 5: Nếu đổi `date = 9` trong `1_if.js`
```js
var date = 9;
// Kết quả: "Thứ khác"
// Giải thích: date !== 2 (if sai), date !== 3 (else if sai) → rơi vào else
```

### Ví dụ 6: Switch fall-through — minh họa lỗi quen `break`
```js
var date = 2;
switch (date) {
  case 2:
    console.log("hai");
    // Quên break → rơi xuống default
  default:
    console.log("default");
}
// Kết quả: "hai" rồi "default" ← bug!
```

### Ví dụ 7: Ternary gán biến thực tế
```js
const age = 20;
const status = age >= 18 ? "người lớn" : "trẻ em";
console.log(status); // "người lớn"

const score = 7.5;
const grade = score >= 8 ? "Giỏi" : "Khá";
console.log(grade); // "Khá"
```

### Ví dụ 8: If với guard clause — code phẳng hơn
```js
function classify(score) {
  if (score == null) return "Chưa có điểm";
  if (score >= 9) return "Xuất sắc";
  if (score >= 8) return "Giỏi";
  if (score >= 6.5) return "Khá";
  if (score >= 5) return "Trung bình";
  return "Yếu";
}
console.log(classify(8)); // "Giỏi"
console.log(classify(null)); // "Chưa có điểm"
```

### Ví dụ 9: Switch với nhiều case gộp chung
```js
const month = 6;
switch (month) {
  case 12:
  case 1:
  case 2:
    console.log("Mùa đông"); break;
  case 3:
  case 4:
  case 5:
    console.log("Mùa xuân"); break;
  case 6:
  case 7:
  case 8:
    console.log("Mùa hè"); break; // month = 6 → in "Mùa hè"
  default:
    console.log("Mùa thu");
}
```

### Ví dụ 10: Ternary trong function return
```js
const getLabel = (count) => count > 0 ? `${count} sản phẩm` : "Không có sản phẩm";
console.log(getLabel(5));    // "5 sản phẩm"
console.log(getLabel(0));    // "Không có sản phẩm"

// Ternary chọn icon
const isConnected = true;
console.log(isConnected ? "🟢" : "🔴"); // "🟢"
```

## 🔬 So sánh với alternatives

| Cú pháp | Ưu điểm | Nhược điểm | Phù hợp nhất |
|---|---|---|---|
| `if...else` | Linh hoạt, mọi phép so sánh | Code dài với nhiều case | Điều kiện phức tạp, khoảng giá trị |
| `switch` | Gọn, dễ đọc khi nhiều case | Chỉ `===`, không so sánh khoảng | Giá trị cố định (ngày, mã, role) |
| Ternary | 1 dòng, expression | Chỉ 2 nhánh, khó đọc khi lồng | Gán biến, JSX, giá trị trả về |

## 📊 Performance & Best Practices

**Quy tắc chọn cú pháp**:
- 2-3 giá trị cố định → `switch` (rõ ràng, dễ bảo trì).
- Điều kiện so sánh linh hoạt → `if...else`.
- Gán 1 trong 2 giá trị → ternary.
- Hơn 6 case trong `switch` → cân nhắc object lookup map.

**Best practices**:
- Luôn có `default` trong `switch` để bắt trường hợp không mong đợi.
- Đặt điều kiện **chặt nhất lên đầu** trong `if...else if`.
- Dùng **guard clause** (return sớm) thay `else` lồng.
- Tránh **ternary lồng quá 2 cấp**.
- Luôn dùng `===` thay `==` — tránh bẫy ép kiểu.

## 🔗 Liên kết chéo

- Tổng quan Conditionals: `06_control-flow/README.md` — khái niệm cốt lõi, so sánh 3 cú pháp.
- Ternary chi tiết: `06_control-flow/01_conditionals/03_ternary/` — ví dụ ternary trong browser.
- Toán tử so sánh: `08_expressions-and-operators/01_operators/4_toan-tu-so-sanh.js` — hiểu `===` vs `==`.
- Toán tử logic: `08_expressions-and-operators/01_operators/5_toan-tu-logical.js` — kết hợp `&&` `||` `!`.
- Vòng lặp kết hợp điều kiện: `05_loops-and-iterations/01_loops/6_break-continue.js` — break/continue trong loop.
