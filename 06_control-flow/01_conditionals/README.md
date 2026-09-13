# Điều kiện (Conditionals) — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

**Conditionals** (cấu trúc điều kiện) là các cấu trúc cho phép chương trình **chọn nhánh thực thi dựa trên điều kiện**. Khi JavaScript gặp câu lệnh điều kiện, engine sẽ **đánh giá biểu thức điều kiện** thành `true` hoặc `false` (thực ra là truthy/falsy), rồi **rẽ sang nhánh tương ứng** — chỉ chạy nhánh được chọn, bỏ qua các nhánh khác.

JavaScript cung cấp **ba cú pháp điều kiện chính**, mỗi cú pháp phù hợp một kiểu bài toán:

| Cú pháp | Phạm vi | Đặc điểm nhận dạng |
|---|---|---|
| `if...else if...else` | Mọi loại điều kiện | So sánh phức hợp, khoảng giá trị, kết hợp `&&` `||` `!` |
| `switch...case` | Giá trị cố định | So sánh `===` một biểu thức với nhiều trường hợp rời rạc |
| `x ? a : b` | Hai lựa chọn | Viết gọn if/else thành một expression, thường dùng gán/trả về |

Phân nhánh trong thư mục này:

- **`5_condition/`** — ba file thực hành: `1_if.js` (if/else if/else), `2_switch-case.js` (switch/case/break/default), `3_toan-tu-3-ngoi.js` (ternary operator).
- **`03_ternary/`** — ví dụ ternary được load qua `index.html` + `app.js`, chạy trong browser Console.

Điểm khác biệt cốt lõi cần nhớ: `if` dùng được với **mọi phép so sánh** (`>`, `<`, `>=`, `<=`, `!=`), `switch` chỉ dùng được với **so sánh bằng** (`===`), và ternary chỉ hỗ trợ **2 nhánh đúng/sai**.

## 📐 Cấu trúc / Cú pháp

### `if...else if...else`
```js
if (điều_kiện_1) {
  // Chạy khi điều_kiện_1 truthful
} else if (điều_kiện_2) {
  // Chạy khi điều_kiện_1 falsy VÀ điều_kiện_2 truthful
} else if (điều_kiện_3) {
  // Chạy khi điều_kiện_1, 2 đều falsy VÀ điều_kiện_3 truthful
} else {
  // Chạy khi TẤT CẢ điều kiện trên đều falsy
}
```

**Lưu ý quan trọng**: các nhánh `else if` chạy **theo thứ tự từ trên xuống**. Nhánh đầu tiên **đúng** sẽ thắng — các nhánh phía sau, dù đúng cũng không chạy. Do đó, **thứ tự sắp xếp điều kiện rất quan trọng**.

### `switch...case`
```js
switch (biểu_thức) {
  case giá_trị_1:
    // Code chạy khi biểu_thức === giá_trị_1
    break; // Bắt buộc thoát switch
  case giá_trị_2:
    // Code chạy khi biểu_thức === giá_trị_2
    break;
  case giá_trị_3:
  case giá_trị_4:
    // Nhiều case gộp chung hành vi (fall-through có chủ đích)
    doSomething();
    break;
  default:
    // Chạy khi không case nào khớp
}
```

**Cơ chế hoạt động**: `switch` so sánh biểu thức với từng `case` bằng **nghiêm ngặt `===`** (kiểu dữ liệu cũng phải khớp). Khi tìm thấy case khớp, chạy code từ đó xuống cho đến khi gặp `break` hoặc hết switch.

### Ternary (`? :`)
```js
const result = điều_kiện ? giá_trị_đúng : giá_trị_sai;
// Ví dụ:
const status = age >= 18 ? "người lớn" : "trẻ em";
```

**Quy tắc viết tắt**:
- Một tham số: `cond ? a : b`
- Không tham số: `cond ? a : b` (vẫn cần `()`)
- Return object: `() => ({ key: value })` — bắt buộc bọc `()`
- Implicit return: `x => x * 2` — tự động return (chỉ khi thân là 1 biểu thức)

## ✅ Điểm mạnh

1. **`if...else` đọc tự nhiên** — giống ngôn ngữ tiếng Việt, linh hoạt với mọi loại điều kiện kết hợp `&&`, `||`, `!`, phép so sánh.
2. **`switch` gọn gàng** khi có từ 3-4 nhánh giá trị rời rạc trở lên — dễ thêm bớt trường hợp, code ngắn hơn if/else chain.
3. **`switch` dùng `===`** nên không có bẫy ép kiểu như `==` — an toàn hơn, kết quả dự đoán được.
4. **Ternary giúp giảm dòng code** — chuyển 5-7 dòng `if/else` thành 1 dòng, đặc biệt hữu ích khi gán biến hoặc làm giá trị trả về.
5. **Các cấu trúc này lồng nhau được** — kết hợp với vòng lặp và hàm để tạo logic phức tạp.
6. **Được minh họa bằng dữ liệu thực tế** — thứ trong tuần, tên tiếng Việt có dấu — dễ liên tưởng.
7. **Fall-through có chủ đích** trong `switch` — gộp nhiều case cùng hành vi (ví dụ: thứ 2-6 đều là "ngày làm việc").
8. **Guard clause pattern** — dùng `if (condition) return` sớm để tránh `else` lồng nhau, code phẳng hơn.
9. **Ternary là expression** — có thể dùng trong JSX, template literal, làm đối số hàm, gán biến.
10. **Kết hợp với toán tử logic** — `&&` `||` `!` giúp viết điều kiện ngắn gọn (short-circuit evaluation).

## ⚠️ Bẫy thường gặp & Hạn chế

1. **Quên `break` trong `switch`** — fall-through chạy tiếp các `case` phía sau, gây kết quả sai. Đây là lỗi kinh điển nhất.
   ```js
   switch (2) {
     case 2: console.log("hai");
       // quên break → rơi xuống default
     default: console.log("default");
   }
   // In: "hai" rồi "default" ← không mong muốn
   ```

2. **`switch` dùng so sánh nghiêm ngặt `===`** — `"2"` (chuỗi) không khớp với `2` (số).
   ```js
   const day = "2";
   switch (day) {
     case 2: console.log("số 2"); break; // KHÔNG chạy
     default: console.log("không khớp"); // → chạy cái này
   }
   ```

3. **`if (x)` kiểm tra truthy/falsy** — `0`, `""`, `null`, `NaN` đều falsy, không phải lúc nào cũng là `false`.
   ```js
   if (0) console.log("chạy");     // KHÔNG chạy — 0 là falsy
   if ("") console.log("chạy");    // KHÔNG chạy — "" là falsy
   if (null) console.log("chạy");  // KHÔNG chạy
   if (NaN) console.log("chạy");   // KHÔNG chạy
   ```

4. **`else if` theo thứ tự** — nhánh đầu tiên đúng sẽ thắng, các nhánh sau dù đúng cũng bỏ qua. Sắp xếp sai điều kiện = kết quả sai.
   ```js
   const score = 85;
   if (score > 70) { console.log("Tốt"); }      // Chạy đầu tiên, chặn các nhánh dưới
   else if (score > 80) { console.log("Giỏi"); } // Bỏ qua — dù 85 > 80
   ```

5. **Nếu đã `return` trong mọi nhánh** — không cần `else` — code dài dòng hơn mức cần.
   ```js
   // ❌ Dài dòng
   if (condition) { return a; } else { return b; }
   // ✅ Ngắn gọn hơn
   if (condition) return a;
   return b;
   ```

6. **Ternary lồng nhau quá nhiều** — khó đọc, khó bảo trì. Chuyển sang `if/else` khi logic phức tạp.
   ```js
   // ❌ Khó đọc
   const x = a ? b : c ? d : e ? f : g;
   // ✅ Nên viết
   if (a) x = b;
   else if (c) x = d;
   else if (e) x = f;
   else x = g;
   ```

7. **Side-effect trong nhánh ternary** — gây khó kiểm tra và bảo trì.
   ```js
   const result = isValid ? saveData() : loadData(); // saveData/loadData có side effect
   ```

## 💡 Khi nào dùng

1. **`if`** — khi điều kiện không tương đương đơn giản: so sánh khoảng giá trị (`score >= 8`), kết hợp nhiều điều kiện (`age >= 18 && hasID`), hoặc kiểm tra truthy/falsy.
2. **`switch`** — khi một biến chỉ nhận vài giá trị cụ thể: ngày trong tuần (1-7), mã trạng thái HTTP (200, 404, 500), role người dùng (`"admin"`, `"user"`).
3. **Ternary** — khi chỉ cần chọn 1 trong 2 giá trị để gán/trả về/in ra: `const label = isActive ? "Bật" : "Tắt"`.
4. **Kết hợp cả ba** — khi một hàm cần nhiều bước rẽ nhánh, ví dụ: kiểm tra đầu vào (`if`), chọn hành vi theo type (`switch`), gán giá trị mặc định (ternary).

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: `if...else if...else` cơ bản (file `1_if.js`)
```js
var date = 2; // Đổi số này để thử các nhánh

if (date === 2) {
  console.log("Hôm nay là thứ 2"); // date = 2 → in dòng này
} else if (date === 3) {
  console.log("Hôm nay là thứ 3"); // date = 3 → in dòng này
} else {
  console.log("Thứ khác");        // date = 1,4,5,6,7 → in dòng này
}
```

### Ví dụ 2: `switch...case` (file `2_switch-case.js`)
```js
var date = 2;

switch (date) {
  case 2:
    console.log(2); // date = 2 → in 2
    break;          // break thoát switch, không chạy default
  default:
    console.log("default"); // date ≠ 2 → in "default"
    break;
}
```

### Ví dụ 3: Ternary — toán tử ba ngôi (file `3_toan-tu-3-ngoi.js`)
```js
// "Sơn" có 3 ký tự → "Sơn".length > 3 → false → trả về false
console.log("Sơn".length > 3 ? true : false); // false

// "Nguyễn" có 6 ký tự → "Nguyễn".length > 3 → true → trả về true
console.log("Nguyễn".length > 3 ? true : false); // true

// Kiểm tra chẵn/lẻ
console.log(100 % 2 === 0 ? "Chẵn" : "Lẻ"); // "Chẵn"
console.log(99 % 2 === 0 ? "Chẵn" : "Lẻ");  // "Lẻ"
```

### Ví dụ 4: Ternary trong app.js (file `03_ternary/app.js`)
```js
// app.js — giá trị đúng là "Success"
let a = true ? "Success" : "Error";
console.log(a); // "Success"

// Mở index.html trên trình duyệt → DevTools Console sẽ hiện "Success"
```

### Ví dụ 5: Switch với nhiều case gộp chung (fall-through có chủ đích)
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
    console.log("Mùa hè"); break; // → in ra
  case 9:
  case 10:
  case 11:
    console.log("Mùa thu"); break;
  default:
    console.log("Tháng không hợp lệ");
}
```

### Ví dụ 6: If với guard clause — tránh else lồng
```js
function getTier(score) {
  if (score == null) return "Chưa có điểm";
  if (score >= 9) return "Xuất sắc";
  if (score >= 8) return "Giỏi";
  if (score >= 6.5) return "Khá";
  if (score >= 5) return "Trung bình";
  return "Yếu";
  // Không cần else — mỗi if return sớm, code phẳng, dễ đọc
}
```

### Ví dụ 7: Ternary chọn UI component
```js
const isLoggedIn = true;
const avatar = isLoggedIn
  ? '<img src="/avatar.jpg" alt="Avatar">'
  : '<span class="guest">Khách</span>';
console.log(avatar);
// <img src="/avatar.jpg" alt="Avatar">
```

### Ví dụ 8: If kết hợp && || — điều kiện phức tạp
```js
const age = 25;
const hasID = true;
const isStudent = false;

if ((age >= 18 && hasID) || isStudent) {
  console.log("Được vào"); // in ra — age >= 18 và có ID
} else {
  console.log("Từ chối");
}
```

### Ví dụ 9: Switch thay thế if-chain dài
```js
function getDayName(dayNumber) {
  switch (dayNumber) {
    case 1: return "Thứ 2";
    case 2: return "Thứ 3";
    case 3: return "Thứ 4";
    case 4: return "Thứ 5";
    case 5: return "Thứ 6";
    case 6: return "Thứ 7";
    case 7: return "Chủ nhật";
    default: return "Số ngày không hợp lệ";
  }
}
console.log(getDayName(2)); // "Thứ 3"
```

### Ví dụ 10: Ternary trong function return
```js
const isWeekend = (day) => day === "Saturday" || day === "Sunday" ? true : false;
console.log(isWeekend("Saturday")); // true
console.log(isWeekend("Monday"));   // false

// Cách viết gọn hơn (không cần ? : vì phép || đã trả boolean)
const isWeekend2 = (day) => day === "Saturday" || day === "Sunday";
```

## 🔬 So sánh với alternatives

| Tình huống | Cú pháp phù hợp nhất | Lý do |
|---|---|---|
| So sánh khoảng (`>`, `<`, `>=`) | `if...else` | `switch` không hỗ trợ so sánh khoảng |
| Nhiều giá trị cố định (1-7 ngày) | `switch` | Ngắn gọn, dễ thêm case, tránh lặp `else if` |
| Gán 1 trong 2 giá trị | Ternary | Expression, 1 dòng, rõ ý đồ |
| Control flow phức tạp nhiều tầng | `if` + guard clause | Đọc dễ hơn switch nested hoặc ternary lồng |
| Chọn hành vi theo type string | Object lookup | Nhanh hơn switch khi số case > 5 |
| JSX conditional rendering | Ternary | Viết inline, gọn trong React/Vue template |

## 📊 Performance & Best Practices

**Quy tắc chọn**:
- 2-3 giá trị cố định → `switch` (rõ ràng, jump table tối ưu).
- Điều kiện so sánh linh hoạt → `if...else`.
- Gán giá trị điều kiện → ternary.
- Hơn 5-6 case trong `switch` → cân nhắc object lookup map.
- Nhiều điều kiện kết hợp (`&&` `||`) → `if`.

**Quy tắc code sạch**:
- Luôn có `default` trong `switch` để bắt trường hợp không mong đợi.
- Đặt điều kiện **chặt nhất lên đầu** trong `if...else if` chain.
- Dùng **guard clause** (return sớm) thay `else` lồng nhau.
- Tránh **ternary lồng quá 2层级** — chuyển sang if/else.
- Không dùng ternary cho side-effect — chỉ dùng khi cần **giá trị**.

**Benchmark** (không đáng kể trong app thông thường):
- `switch` với 5+ case: nhanh hơn `if...else if` chain (~10-20%) do engine tối ưu jump table.
- Ternary: không ảnh hưởng performance — chỉ syntax sugar.
- Object lookup map: O(1) so với O(n) của if-chain — đáng kể khi case > 10.

## 🔗 Liên kết chéo

- Thực hành `if`/`switch`/ternary: `06_control-flow/01_conditionals/5_condition/` — `1_if.js`, `2_switch-case.js`, `3_toan-tu-3-ngoi.js`.
- Ternary trong browser: `06_control-flow/01_conditionals/03_ternary/app.js` + `index.html`.
- Toán tử logic (`&&`, `||`, `!`): `08_expressions-and-operators/01_operators/5_toan-tu-logical.js`.
- So sánh nghiêm ngặt: `08_expressions-and-operators/01_operators/4_toan-tu-so-sanh.js`.
- Vòng lặp đi kèm điều kiện: `05_loops-and-iterations/01_loops/6_break-continue.js`.
- Throw lỗi khi điều kiện sai: `07_exceptional-handling/01_throw/app.js`.
