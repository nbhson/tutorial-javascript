# Luồng điều khiển (Control Flow) — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

**Control flow** (luồng điều khiển) là cách chương trình JavaScript **quyết định đoạn code nào sẽ chạy, và chạy theo thứ tự nào**. Mặc định, JavaScript chạy code **theo thứ tự từ trên xuống dưới** (sequential execution) — đây là dòng chảy mặc định. Khi cần thay đổi dòng chảy này, ta dùng **cấu trúc điều kiện** hoặc **vòng lặp**.

Nhóm này tập trung vào **cấu trúc điều kiện** — công cụ cho phép chương trình **rẽ nhánh** (branching) dựa trên điều kiện đúng/sai. JavaScript cung cấp ba cú pháp điều kiện chính, mỗi cú pháp phù hợp một kiểu bài toán:

| Cú pháp | Mức độ linh hoạt | Trường hợp dùng tốt nhất |
|---|---|---|
| `if...else if...else` | Cao nhất | Điều kiện phức tạp, so sánh khoảng, kết hợp nhiều điều kiện |
| `switch...case` | Trung bình | So sánh **bằng** một giá trị với nhiều trường hợp rời rạc |
| Ternary (`? :`) | Thấp nhất | Chọn một trong hai giá trị, viết gọn trong một biểu thức |

Dưới bề mặt, mỗi cấu trúc điều kiện đều dựa trên **cơ chế đánh giá truthy/falsy** của JavaScript. Giá trị `true`, số khác 0, chuỗi khác rỗng, object — đều là truthy. Giá trị `false`, `0`, `NaN`, `""`, `null`, `undefined` — đều là falsy. Điều kiện trong `if` được JavaScript **ép ngầm thành boolean** thông qua cơ chế này.

**Tại sao có nhiều cách?** Vì mỗi cách tối ưu cho một tình huống khác nhau: `if` linh hoạt với so sánh `>` `<` `&&` `||`, `switch` gọn gàng khi so sánh nhiều giá trị cố định, ternary tiện lợi khi gán biến trong một dòng.

## 📐 Cấu trúc / Cú pháp

### `if...else if...else`
```js
if (điều_kiện_1) {
  // chạy khi điều_kiện_1 đúng
} else if (điều_kiện_2) {
  // chạy khi điều_kiện_1 sai VÀ điều_kiện_2 đúng
} else if (điều_kiện_3) {
  // chạy khi điều_kiện_1 và 2 đều sai, điều_kiện_3 đúng
} else {
  // chạy khi TẤT CẢ điều kiện trên đều sai
}
```
- Các nhánh `else if` chạy **theo thứ tự từ trên xuống** — nhánh đầu tiên **đúng** sẽ thắng, các nhánh sau bị bỏ qua.
- Không giới hạn số lượng `else if`.
- `else` là tùy chọn — có thể bỏ qua nếu không cần nhánh mặc định.

### `switch...case`
```js
switch (biểu_thức_cần_so_sánh) {
  case giá_trị_1:
    // code chạy khi biểu_thức === giá_trị_1
    break; // QUAN TRỌNG: thoát khỏi switch
  case giá_trị_2:
    // code chạy khi biểu_thức === giá_trị_2
    break;
  default:
    // code chạy khi không case nào khớp
}
```
- So sánh dùng **nghiêm ngặt** (`===`) — kiểu dữ liệu cũng phải khớp.
- `break` là **bắt buộc** nếu không muốn fall-through (chạy tiếp các case phía dưới).
- `default` là tùy chọn — chạy khi không có case nào khớp.
- Một giá trị có thể có nhiều `case` gộp chung hành vi (fall-through có chủ đích).

### Ternary (`? :`)
```js
biểu_thức_điều_kiện ? giá_trị_nếu_đúng : giá_trị_nếu_sai
// Ví dụ:
const status = age >= 18 ? "người lớn" : "trẻ em";
```
- Là **expression** (trả về giá trị), không phải statement — có thể gán biến, truyền đối số.
- Chỉ hỗ trợ **2 nhánh** (đúng / sai) — không có `else if`.
- Có thể lồng nhau (`a ? b : c ? d : e`) nhưng **rất khó đọc** — không khuyến khích.

## ✅ Điểm mạnh

1. **Kiểm soát chương trình rõ ràng**: biết chính xác nhánh nào chạy trong tình huống nào — code dễ đọc, dễ debug.
2. **Ba cú pháp phủ hết mọi tình huống**: so sánh phức tạp → `if`, nhiều giá trị rời rạc → `switch`, biểu thức ngắn gọn → ternary.
3. **`switch` tránh được bẫy ép kiểu** của `==` — so sánh nghiêm ngặt `===` đảm bảo an toàn.
4. **Ternary viết gọn 1 dòng** — thay thế 5-7 dòng `if/else` thành một biểu thức, đặc biệt hữu ích khi gán biến.
5. **Kết hợp với toán tử logic** `&&`, `||`, `!` để viết điều kiện phức tạp một cách tự nhiên.
6. **Không giới hạn số nhánh `else if`** — có thể mở rộng logic dần mà không cần đổi cấu trúc.
7. **Fall-through trong `switch` có chủ đích** — gộp nhiều case cùng hành vi (`case 1: case 2: doSomething(); break;`).
8. **Ternary là expression** — có thể dùng trực tiếp trong JSX, template literal, hoặc làm đối số hàm.
9. **Readability cao** khi dùng đúng cú pháp: code tự nói lên ý đồ (switch cho giá trị cố định, if cho điều kiện linh hoạt).

## ⚠️ Bẫy thường gặp & Hạn chế

1. **Quên `break` trong `switch`** — fall-through chạy tiếp các case phía sau, gây kết quả sai.
   ```js
   switch (2) {
     case 2:
       console.log("hai");
       // quên break → chạy tiếp default
     default:
       console.log("default");
   }
   // In: "hai" rồi "default"
   ```

2. **`switch` dùng `===` nghiêm ngặt** — `"2"` không khớp với `2`.
   ```js
   const day = "2";
   switch (day) {
     case 2: console.log("số 2"); break; // KHÔNG chạy!
     default: console.log("không khớp"); // → in cái này
   }
   ```

3. **`if (x)` kiểm tra truthy/falsy, không phải `x !== undefined`** — `0`, `""`, `null`, `NaN` đều falsy.
   ```js
   if (0) console.log("vẫn chạy?"); // KHÔNG chạy — 0 là falsy
   if ("") console.log("vẫn chạy?"); // KHÔNG chạy — "" là falsy
   if (null) console.log("vẫn chạy?"); // KHÔNG chạy
   ```

4. **Ternary lồng nhau quá sâu** — mất readability, khó bảo trì.
   ```js
   // ❌ Khó đọc
   const result = a ? b : c ? d : e ? f : g;
   // ✅ Nên dùng if/else
   ```

5. **`else if` không chạy đồng thời** — nhánh đầu tiên đúng sẽ thắng, các nhánh sau dù đúng cũng bỏ qua.
   ```js
   const score = 85;
   if (score > 70) { console.log("Tốt"); }      // chạy
   else if (score > 80) { console.log("Giỏi"); } // BỎ QUA — score > 80 cũng đúng nhưng đã chặn ở if trên
   ```

6. **Quên dấu `:` trong ternary** — SyntaxError.
   ```js
   const x = condition ? "yes" "no"; // Sai — thiếu ":"
   ```

7. **Side-effect trong ternary** — gọi hàm có tác dụng phụ trong nhánh đúng/sai gây khó test.
   ```js
   const result = condition ? saveToDB() : loadFromCache(); // khó test vì có side effect
   ```

## 💡 Khi nào dùng — Tình huống thực tế

1. **Thẩm định form nhập liệu**: `if` kiểm tra email hợp lệ, password đủ mạnh, số điện thoại đúng định dạng — điều kiện phức tạp, cần nhiều nhánh.
2. **Xử lý quyền truy cập**: `switch` kiểm tra role (`"admin"`, `"editor"`, `"viewer"`) — mỗi role có hành vi khác nhau, so sánh bằng giá trị cố định.
3. **Render UI có điều kiện**: ternary chọn class CSS (`className={isActive ? "active" : "inactive"}`) — gán giá trị trong một dòng.
4. **Phân loại điểm số**: `if...else if` xếp loại (Giỏi ≥ 8, Khá ≥ 6.5, Trung bình ≥ 5, Yếu) — so sánh khoảng giá trị.
5. **Chọn nhánh theo mã trạng thái HTTP**: `switch` với `200`, `404`, `500` — mỗi mã có cách xử lý riêng.
6. **Gán giá trị mặc định**: ternary `const theme = userPref ? userPref : "dark"` — ngắn gọn, dễ đọc.
7. **Kiểm tra điều kiện kết hợp**: `if (age >= 18 && hasID)` — cần cả hai điều kiện cùng đúng.
8. **Ngày trong tuần / tháng trong năm**: `switch` với giá trị cố định 1-7 hoặc 1-12 — gọn gàng, dễ thêm case mới.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: `if...else` cơ bản (file `1_if.js`)
```js
var date = 2; // Thay đổi số này để thử các nhánh khác

if (date === 2) {
  console.log("Hôm nay là thứ 2"); // date = 2 → in dòng này
} else if (date === 3) {
  console.log("Hôm nay là thứ 3"); // date = 3 → in dòng này
} else {
  console.log("Thứ khác");        // date = 4,5,6,7 → in dòng này
}
```

### Ví dụ 2: `switch...case` (file `2_switch-case.js`)
```js
var date = 2;

switch (date) {
  case 2:
    console.log(2); // date = 2 → in 2
    break;          // break thoát switch
  default:
    console.log("default"); // date ≠ 2 → in "default"
    break;
}
```

### Ví dụ 3: Ternary cơ bản (file `3_toan-tu-3-ngoi.js`)
```js
// "Sơn" có 3 ký tự → length > 3 là false → trả về false
console.log("Sơn".length > 3 ? true : false); // false

// Đổi thành "Nguyễn" (6 ký tự) → length > 3 là true → trả về true
console.log("Nguyễn".length > 3 ? true : false); // true
```

### Ví dụ 4: Ternary gán biến (ứng dụng thực tế)
```js
const age = 20;
const status = age >= 18 ? "người lớn" : "trẻ em";
console.log(status); // "người lớn"

const score = 75;
const grade = score >= 8 ? "Giỏi" : score >= 6.5 ? "Khá" : score >= 5 ? "Trung bình" : "Yếu";
// ⚠️ Ternary lồng nhau — tốt cho 2-3 nhánh, quá nhiều nên chuyển sang if/else
```

### Ví dụ 5: Switch với nhiều case gộp chung
```js
const dayName = "Thứ 2";
switch (dayName) {
  case "Thứ 2":
  case "Thứ 3":
  case "Thứ 4":
  case "Thứ 5":
  case "Thứ 6":
    console.log("Ngày đi làm"); // in ra
    break;
  case "Thứ 7":
  case "Chủ nhật":
    console.log("Ngày nghỉ");
    break;
  default:
    console.log("Tên ngày không hợp lệ");
}
```

### Ví dụ 6: If với điều kiện kết hợp (logic phức tạp)
```js
const age = 25;
const hasLicense = true;

if (age >= 18 && hasLicense) {
  console.log("Đủ điều kiện lái xe"); // in ra
} else if (age >= 18 && !hasLicense) {
  console.log("Đủ tuổi nhưng chưa có bằng");
} else {
  console.log("Chưa đủ 18 tuổi");
}
```

### Ví dụ 7: Switch tránh được bẫy ép kiểu `==`
```js
const input = "2"; // Chuỗi "2", khác số 2

// ❌ with == (ép kiểu) — "2" == 2 là true
if (input == 2) {
  console.log("Như vậy có thể nhầm lẫn");
}

// ✅ with switch === (nghiêm ngặt) — "2" !== 2
switch (input) {
  case 2:
    console.log("Không vào đây"); // KHÔNG chạy
    break;
  case "2":
    console.log("Chuỗi '2' khớp"); // → in dòng này
    break;
}
```

### Ví dụ 8: Ternary trong template literal
```js
const userName = "Sơn";
const greeting = `Xin chào, ${userName.length > 3 ? userName : "Bạn"}!`;
console.log(greeting); // "Xin chào, Sơn!"

// Ternary chọn icon theo trạng thái
const isConnected = true;
const statusIcon = isConnected ? "✅" : "❌";
console.log(`Trạng thái: ${statusIcon}`); // "Trạng thái: ✅"
```

### Ví dụ 9: If-elseif tối ưu thứ tự
```js
const score = 85;
// Sắp xếp từ điều kiện chặt nhất đến lỏng nhất
if (score >= 9) {
  console.log("Xuất sắc");
} else if (score >= 8) {
  console.log("Giỏi"); // → in ra
} else if (score >= 6.5) {
  console.log("Khá");
} else if (score >= 5) {
  console.log("Trung bình");
} else {
  console.log("Yếu");
}
```

### Ví dụ 10: Dùng return thay else khi mọi nhánh đều return
```js
function getDiscount(age) {
  if (age < 6) return "Miễn phí";
  if (age < 18) return "Giảm 50%";
  if (age < 60) return "Bình thường";
  return "Giảm 30%"; // người cao tuổi
  // Không cần else — mỗi if đều return, không cần nhánh mặc định
}
console.log(getDiscount(25)); // "Bình thường"
```

## 🔬 So sánh với alternatives

| Phương án | Ưu điểm | Nhược điểm | Nên dùng khi |
|---|---|---|---|
| `if...else` | Linh hoạt nhất, so sánh được mọi operator | Code dài hơn với nhiều giá trị cố định | Điều kiện phức tạp, so sánh khoảng |
| `switch...case` | Gọn gàng khi có nhiều giá trị rời rạc | Chỉ so sánh bằng `===`, không so sánh khoảng | Ngày trong tuần, mã trạng thái, role |
| Ternary | Một dòng, là expression | Chỉ 2 nhánh, khó đọc khi lồng nhau | Gán biến điều kiện ngắn, JSX/class |
| Map/Object lookup | Tra cứu O(1), code cực gọn | Không phù hợp với điều kiện phức tạp | Giá trị cố định → hành vi cố định |

## 📊 Performance & Best Practices

**Quy tắc chọn cú pháp**:
- 2-3 giá trị cố định → `switch` (rõ ràng, dễ đọc).
- Điều kiện phức tạp (kết hợp `&&`, `||`, `>` `<`) → `if...else`.
- Gán giá trị trong 1 dòng → ternary.
- Quá 5 case trong `switch` → cân nhắc dùng object lookup hoặc `if/else`.

**Tối ưu readability**:
- Đặt điều kiện chặt nhất lên đầu trong `if...else if`.
- Dùng `return` sớm thay `else` khi mỗi nhánh đều return (guard clause pattern).
- Tránh nest quá 2-3 tầng — refactor thành hàm riêng.
- Luôn có `default` trong `switch` để xử lý trường hợp không mong đợi.

**Benchmark** (không đáng kể trong hầu hết ứng dụng):
- `switch` nhanh hơn `if...else` khi số case nhiều (>5) vì engine tối ưu jump table.
- Ternary không ảnh hưởng performance — chỉ là syntax sugar cho if/else.

## 🔗 Liên kết chéo

- Xem chi tiết từng loại condition: `06_control-flow/01_conditionals/5_condition/` — `1_if.js`, `2_switch-case.js`, `3_toan-tu-3-ngoi.js`.
- Thực hành ternary trong browser: `06_control-flow/01_conditionals/03_ternary/app.js` + `index.html`.
- Kết hợp với vòng lặp: `05_loops-and-iterations/01_loops/` — loop thường đi kèm `if` bên trong thân.
- Xử lý lỗi khi điều kiện sai: `07_exceptional-handling/01_throw/` — throw lỗi khi điều kiện đầu vào không hợp lệ.
- Toán tử logic: `08_expressions-and-operators/01_operators/5_toan-tu-logical.js` — hiểu `&&`, `||`, `!` để viết điều kiện phức tạp.
