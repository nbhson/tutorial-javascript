# Toán tử ba ngôi (Ternary) — Thực hành chi tiết — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

**Toán tử ba ngôi** (ternary operator / conditional operator) là cách **viết gọn của `if...else`** trong một biểu thức duy nhất, có đúng **3 thành phần**:

```
điều_kiện ? giá_trị_nếu_đúng : giá_trị_nếu_sai
```

Nó là một **expression** — nghĩa là luôn **trả về một giá trị** — nên thường được dùng để gán cho biến, làm đối số hàm, hoặc trả về từ hàm. Khác với `if...else` là statement (khối lệnh), ternary là expression (trả kết quả).

Ví dụ trong `app.js`:
```js
let a = true ? "Success" : "Error"; // a = "Success"
```

Thay vì viết 5-7 dòng `if/else`:
```js
let a;
if (true) {
  a = "Success";
} else {
  a = "Error";
}
```

Ternary **rút gọn** thành 1 dòng, cùng ý nghĩa, cùng kết quả. Điều này đặc biệt hữu ích khi bạn cần **chọn một trong hai giá trị** để gán, trả về, hoặc truyền vào hàm.

**Nguyên lý hoạt động**: JavaScript engine đánh giá `điều_kiện` → nếu truthy thì trả về `giá_trị_nếu_đúng`, nếu falsy thì trả về `giá_trị_nếu_sai`. Cả hai nhánh đều được **đánh giá lazy** — chỉ nhánh được chọn mới thực thi.

## 📐 Cấu trúc / Cú pháp

### Cú pháp cơ bản
```js
điều_kiện ? giá_trị_đúng : giá_trị_sai
```

### Quy tắc viết tắt
| Trường hợp | Cú pháp | Ghi chú |
|---|---|---|
| Thân có `{}` | `(a, b) => { return a + b; }` | Cần `return` rõ ràng |
| Thân 1 biểu thức | `(a, b) => a + b` | Implicit return — tự động return |
| Trả về object | `(a, b) => ({ a, b })` | Bắt buộc bọc `()` — `{}` sẽ bị hiểu là phần thân hàm (function body) |
| Một tham số | `x => x * 2` | Có thể bỏ `()` |
| Không tham số | `() => 42` | Bắt buộc có `()` |

### Ternary lồng nhau
```js
const grade = score >= 9 ? "Xuất sắc" : score >= 8 ? "Giỏi" : score >= 6.5 ? "Khá" : "Yếu";
// ⚠️ Chỉ dùng khi <= 3 nhánh — quá nhiều nên chuyển sang if/else
```

### Ternary trong expression khác
```js
// Làm đối số hàm
console.log(age >= 18 ? "Người lớn" : "Trẻ em");

// Gán biến
const status = isConnected ? "online" : "offline";

// Trong template literal
const msg = `Trạng thái: ${isConnected ? "🟢" : "🔴"}`;
```

## ✅ Điểm mạnh

1. **Rất gọn gàng**: chuyển 5-7 dòng `if/else` thành 1 dòng duy nhất — code sạch, dễ đọc khi logic đơn giản.
2. **Là expression** — linh hoạt: gán biến, trả về từ hàm, điền trực tiếp vào template literal, làm đối số hàm.
3. **Dùng được với mọi giá trị truthy/falsy** — điều kiện có thể là bất kỳ biểu thức nào trả về boolean hoặc giá trị coerces thành boolean.
4. **Dễ đọc khi mệnh đề đúng/sai là giá trị ngắn** — đặc biệt khi giá trị là string số, number, hoặc boolean.
5. **Thể hiện rõ ý đồ "chọn một trong hai"** — người đọc hiểu ngay đây là phép chọn đôi, không phải nhánh phức tạp.
6. **Perfect cho JSX/React** — inline conditional rendering: `{isActive ? <Active /> : <Inactive />}`.
7. **Zero overhead** — không có performance penalty so với `if/else`, compiler tối ưu tương đương.
8. **Functional programming friendly** — pure expression, không side-effect, dễ compose với các hàm khác.

## ⚠️ Bẫy thường gặp & Hạn chế

1. **Không dùng để chạy nhiều câu lệnh** — ternary sinh ra để **trả về giá trị**, không phải để **thực thi hành động phức tạp**.
   ```js
   // ❌ Không nên — side-effect trong ternary
   const result = condition ? { doA(); doB(); } : { doC(); doD(); };
   // ✅ Nên dùng if/else
   ```

2. **Ternary lồng ternary rất khó đọc** — 3 nhánh trở lên nên chuyển sang `if...else`.
   ```js
   // ❌ Khó đọc
   const x = a ? b : c ? d : e ? f : g;
   // ✅ Nên viết
   if (a) x = b;
   else if (c) x = d;
   else if (e) x = f;
   else x = g;
   ```

3. **Dễ nhầm do thiếu dấu ngoặc** khi kết hợp nhiều toán tử — đặt `()` rõ ràng nếu cần.
   ```js
   // ❌ Nhầm lẫn thứ tự ưu tiên
   const x = a + b ? c : d; // (a + b) ? c : d hay a + (b ? c : d)?
   // ✅ Rõ ràng
   const x = (a + b) ? c : d;
   ```

4. **Side-effect trong nhánh ternary** — gọi hàm có tác dụng phụ gây khó kiểm tra và bảo trì.
   ```js
   const result = isValid ? saveToDB(data) : loadFromCache(); // khó test
   ```

5. **Nếu cả hai nhánh cùng công việc khá dài** — ternary không còn "gọn" nữa mà chỉ là rối.
   ```js
   // ❌ Không gọn
   const msg = condition ? doComplexThing1() : doComplexThing2();
   // ✅ Dùng if/else
   ```

6. **Quên dấu `:` phân cách** — SyntaxError.
   ```js
   const x = condition ? "yes" "no"; // ❌ Thiếu ":"
   ```

7. **Ternary trong object property** — cú pháp `{ key: condition ? a : b }` dễ nhầm với `{ condition ? a : b }` (sai cú pháp).

## 💡 Khi nào dùng

1. **Gán giá trị mặc định theo điều kiện**: `let status = age >= 18 ? "người lớn" : "trẻ em";` — đơn giản, 1 dòng.
2. **Chọn văn bản/icon hiển thị theo trạng thái UI**: `const icon = isActive ? "✅" : "❌";` — inline trong render.
3. **Trả về giá trị khác nhau từ hàm một cách ngắn gọn**: `const label = count > 0 ? \`${count} items\` : "Empty";`
4. **Xây chuỗi động (template literal) có nhánh điều kiện**: `` `Hello ${name ? name : "Guest"}` ``.
5. **Sửa/thẩm định biến một dòng thay cho `if` dài**: `const safeValue = input ?? defaultValue;` (nullish coalescing, ES2020).
6. **JSX conditional rendering trong React**: `{isLoggedIn ? <Dashboard /> : <Login />}`.
7. **Chọn class CSS theo state**: `className={error ? "input-error" : "input-normal"}`.
8. **Hàm một biểu thức trả về**: `const abs = x => x < 0 ? -x : x;` — pure function, không branch verbose.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Cơ bản — gán biến (file `app.js`)
```js
// app.js — ví dụ gốc trong thư mục
let a = true ? "Success" : "Error";
console.log(a); // "Success" — điều kiện true → lấy nhánh đúng

// Đổi điều kiện thành false
let b = false ? "Success" : "Error";
console.log(b); // "Error" — điều kiện false → lấy nhánh sai
```

### Ví dụ 2: Kiểm tra độ dài tên (file `3_toan-tu-3-ngoi.js`)
```js
// "Sơn" có 3 ký tự → length > 3 là false → trả về false
console.log(("Sơn").length > 3 ? true : false); // false

// "Nguyễn" có 6 ký tự → length > 3 là true → trả về true
console.log(("Nguyễn").length > 3 ? true : false); // true
```

### Ví dụ 3: Kiểm tra chẵn/lẻ
```js
console.log(100 % 2 === 0 ? "Chẵn" : "Lẻ");  // "Chẵn"
console.log(99 % 2 === 0 ? "Chẵn" : "Lẻ");   // "Lẻ"
console.log(0 % 2 === 0 ? "Chẵn" : "Lẻ");    // "Chẵn" — 0 là chẵn
console.log(-4 % 2 === 0 ? "Chẵn" : "Lẻ");   // "Chẵn"
```

### Ví dụ 4: Gán giá trị mặc định
```js
const username = "";
const displayName = username ? username : "Ẩn danh";
console.log(displayName); // "Ẩn danh" — username rỗng là falsy

const username2 = "Sơn";
const displayName2 = username2 ? username2 : "Ẩn danh";
console.log(displayName2); // "Sơn"
```

### Ví dụ 5: Trong template literal
```js
const hour = 14;
const greeting = hour < 12 ? "Chào buổi sáng" : "Chào buổi chiều";
console.log(`${greeting}, bạn!`); // "Chào buổi chiều, bạn!"
```

### Ví dụ 6: Hàm một biểu thức với ternary
```js
// Hàm tính giá trị tuyệt đối
const abs = (x) => x < 0 ? -x : x;
console.log(abs(-5)); // 5
console.log(abs(5));  // 5
console.log(abs(0));  // 0

// Hàm phân loại điểm
const grade = (score) =>
  score >= 9 ? "Xuất sắc" :
  score >= 8 ? "Giỏi" :
  score >= 6.5 ? "Khá" :
  score >= 5 ? "Trung bình" : "Yếu";

console.log(grade(8.5)); // "Giỏi"
console.log(grade(4));   // "Yếu"
```

### Ví dụ 7: Ternary với object return (cần `()`)
```js
// ✅ Đúng — bọc object trong ()
const createUser = (name, age) => ({ name, age });
console.log(createUser("Sơn", 18)); // { name: "Sơn", age: 18 }

// ❌ Sai — không bọc ()
// const createUser = (name, age) => { name, age }; // SyntaxError
```

### Ví dụ 8: Ternary trong array method
```js
const scores = [55, 72, 91, 48, 85];

// Lọc và phân loại
const labels = scores.map((s) => (s >= 60 ? "Đậu" : "Rớt"));
console.log(labels); // ["Rớt", "Đậu", "Đậu", "Rớt", "Đậu"]

// Tính tổng điểm đậu
const totalPass = scores.filter((s) => s >= 60).reduce((a, b) => a + b, 0);
console.log(totalPass); // 248
```

### Ví dụ 9: Safe navigation với ternary
```js
const user = { profile: { name: "Sơn" } };
const userName = user && user.profile ? user.profile.name : "Không có dữ liệu";
console.log(userName); // "Sơn"

const emptyUser = {};
const emptyName = emptyUser && emptyUser.profile ? emptyUser.profile.name : "Không có dữ liệu";
console.log(emptyName); // "Không có dữ liệu"
```

### Ví dụ 10: Nullish coalescing (ES2020) — thay thế ternary cho default value
```js
// Ternary truyền thống
const defaultName = name !== null && name !== undefined ? name : "Ẩn danh";

// Nullish coalescing (ngắn gọn hơn)
const defaultName2 = name ?? "Ẩn danh";

// Nullish chỉ xét null/undefined, không xét falsy khác (0, "", false)
const value = 0 ?? 100; // 0 — khác với 0 || 100 = 100
console.log(value); // 0
```

## 🔬 So sánh với alternatives

| Phương án | Ưu điểm | Nhược điểm | Nên dùng khi |
|---|---|---|---|
| Ternary `? :` | 1 dòng, expression | Chỉ 2 nhánh, khó đọc khi lồng | Gán biến điều kiện ngắn |
| `if...else` | Linh hoạt, mọi điều kiện | Dài dòng hơn | Điều kiện phức tạp, >2 nhánh |
| Nullish coalescing `??` | Ngắn hơn ternary cho default | Chỉ xét null/undefined | Gán giá trị mặc định khi null/undefined |
| Logical OR `||` | Ngắn, tự nhiên | Coerce falsy values (0, "", false) | Default value, không phân biệt 0/""/false |
| Object lookup | O(1), clean khi nhiều case | Không phù hợp điều kiện phức tạp |Mapping giá trị cố định → hành vi |

## 📊 Performance & Best Practices

**Performance**: Ternary không có overhead so với `if/else` — compiler tối ưu tương đương. Ưu tiên readability hơn micro-optimization.

**Quy tắc coding**:
- Dùng ternary khi **cả hai nhánh đều là expression ngắn** (1 giá trị, 1 hàm call đơn).
- Chuyển sang `if/else` khi **nhánh có nhiều câu lệnh** hoặc **logic phức tạp**.
- Giới hạn **ternary lồng tối đa 2 cấp** — quá nhiều = khó đọc.
- Luôn **bọc object trong `()`** khi implicit return: `() => ({ key: value })`.
- Tránh **side-effect trong nhánh** — ternary nên pure (không gây tác dụng phụ).
- Dùng `??` (nullish coalescing) thay ternary cho **mặc định null/undefined** — ngắn gọn hơn.

**Khi nào KHÔNG dùng ternary**:
- Khi nhánh đúng/sai là khối lệnh nhiều dòng.
- Khi cần >2 nhánh (chuyển sang if/else or switch).
- Khi có side-effect quan trọng (log, network call, DB write) — dùng if/else rõ ràng hơn.

## 🔗 Liên kết chéo

- Tổng quan Conditionals: `06_control-flow/README.md` — khái niệm, so sánh if/switch/ternary.
- Thực hành if/switch/ternary: `06_control-flow/01_conditionals/5_condition/3_toan-tu-3-ngoi.js` — file ternary cơ bản.
- Arrow functions (implicit return): `09_functions/01_parameters-and-arrow/03_arrow-functions/` — cách viết gọn của arrow kết hợp ternary.
- Toán tử logic: `08_expressions-and-operators/01_operators/5_toan-tu-logical.js` — `&&` `||` `!` kết hợp với ternary.
- Nullish coalescing: `08_expressions-and-operators/01_operators/` — ES2020 operator `??` thay thế ternary cho default.
- Callbacks: `09_functions/01_parameters-and-arrow/01_callbacks/` — ternary thường dùng trong callback return.
