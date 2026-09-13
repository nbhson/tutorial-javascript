# Toán tử cơ bản (Operators — Basics) — Thực hành chi tiết — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

Thư mục này chứa **6 file demo** các toán tử nền tảng mà bạn dùng hằng ngày trong JavaScript. Đây là **nền tảng của mọi biểu thức** — không hiểu operator = không thể viết code đúng.

| File | Nhóm | Toán tử chính | File tương ứng |
|---|---|---|---|
| `1_toan-tu-so-hoc.js` | Số học (Arithmetic) | `+ - * ** / % ++ --` | Số học cơ bản |
| `2_toan-tu-chuoi.js` | Chuỗi (String) | `+` nối chuỗi | Nối string |
| `3_toan-tu-gan.js` | Gán (Assignment) | `= += -= *= /= **=` | Gán có điều kiện |
| `4_toan-tu-so-sanh.js` | So sánh (Comparison) | `== != > < >= <= === !==` | Phân biệt `==` vs `===` |
| `5_toan-tu-logical.js` | Logic (Logical) | `&& \|\| !` | Short-circuit evaluation |
| `6_toan-tu-prefix-postfix.js` | Tăng/giảm | `++ --` (tiền tố / hậu tố) | Prefix vs Postfix |

**Hai kiến thức quan trọng nhất** cần nắm từ nhóm này:

1. **`==` vs `===`**: `==` ép kiểu trước khi so sánh (`3 == "3"` → `true`), còn `===` so sánh nghiêm ngặt cả kiểu lẫn giá trị (`3 === "3"` → `false`). **Luôn dùng `===`** trừ khi có lý do đặc biệt.

2. **Prefix vs Postfix**: `n++` trả về **giá trị cũ** rồi mới tăng; `++n` tăng trước rồi **trả về giá trị mới**. Nhầm lẫn hai dạng này là nguồn lỗi kinh điển.

File `4_toan-tu-so-sanh.js` liệt kê **7 giá trị falsy** quan trọng: `0`, `NaN`, `""`, `''`, `false`, `null`, `undefined` — những giá trị này đều đánh giá là `false` trong điều kiện `if`.

## 📐 Cấu trúc / Cú pháp

### Arithmetic — `1_toan-tu-so-hoc.js`
```js
var a = 1, b = "5";
console.log(a + b);  // "15"  — nối chuỗi vì có string
console.log(a - b);  // -4    — ép "5" thành số
console.log(a * b);  // 5
console.log(3 ** 2); // 9    — lũy thừa (ES2016)
```

**Quy tắc ép kiểu ngầm định**:
- `+` với string → nối: `1 + "5" === "15"`
- `- * / %` với string → ép thành số: `"5" - 1 === 4`
- `NaN` xuất hiện khi ép không được: `"abc" - 1 === NaN`

### Assignment — `3_toan-tu-gan.js`
```js
let x = 10;
x += 5;   // x = 15  (x = x + 5)
x -= 3;   // x = 12  (x = x - 3)
x *= 2;   // x = 24  (x = x * 2)
x /= 4;   // x = 6   (x = x / 4)
x **= 3;  // x = 216 (x = x ** 3)
x %= 4;   // x = 0   (x = x % 4)
```

### Comparison — `4_toan-tu-so-sanh.js`
```js
console.log(3 == "3");   // true  — ép kiểu: "3" → 3
console.log(3 === "3");  // false — nghiêm ngặt: khác kiểu
console.log(undefined == null);   // true  — special case
console.log(undefined === null);  // false
console.log(true == "1");  // true  — rất dễ nhầm!
console.log(true === "1"); // false
```

**7 Falsy values** (đều đánh giá `false` trong `if`):
| Kiểu | Falsy values |
|---|---|
| number | `0`, `NaN` |
| string | `""`, `''` |
| boolean | `false` |
| null | `null` |
| undefined | `undefined` |

### Logical — `5_toan-tu-logical.js`
```js
// Short-circuit AND: nếu trái falsy → trả trái, không evaluate phải
console.log(0 && 42);   // 0
console.log(5 && 42);   // 42

// Short-circuit OR: nếu trái truthy → trả trái, không evaluate phải
console.log(0 || 42);   // 42
console.log(5 || 42);   // 5

// NOT
console.log(!true);     // false
console.log(!0);        // true
console.log(!"");       // true
```

### Prefix/Postfix — `6_toan-tu-prefix-postfix.js`
```js
var a = 69;
var b = a++; // b nhận giá trị CŨ (69), a tăng thành 70
console.log(a, b); // 70 69

var number = 6;
var output1 = number++; // output1 = 6 (cũ)
var output2 = --number; // number giảm thành 6, output2 = 6 (mới)
console.log(output1 + output2); // 12
```

## ✅ Điểm mạnh

1. **Bao phủ trọn bộ toán tử cơ bản** cần cho mọi dự án JavaScript.
2. **Mỗi file nhỏ, gọn** — chú thích tiếng Việt rõ ràng về ý nghĩa từng ký hiệu.
3. **Có ví dụ thực tế về ép kiểu** — `a + b` với `b` là chuỗi kết quả `"15"`, `a - b` ra số `-4`.
4. **Ghi rõ 7 falsy value** — kiến thức chống ngộ nhận khi dùng `if`.
5. **Nhấn mạnh `===` và sự khác nhau** giữa string và String object.
6. **Prefix vs Postfix minh họa rõ** — `a++` vs `++a` cho kết quả khác khi trong biểu thức.
7. **Chạy độc lập được từng file** bằng `node` — kiểm tra kết quả ngay.
8. **Short-circuit evaluation** giải thích rõ `&&` `||` hoạt động thế nào.
9. **File `1_toan-tu-so-hoc.js`** minh họa `**` (lũy thừa) — toán tử hiện đại thay `Math.pow()`.
10. **Code comment tiếng Việt** — dễ hiểu ngay cả với người mới.

## ⚠️ Bẫy thường gặp & Hạn chế

1. **`+` có hai nghĩa**: cộng số hoặc nối chuỗi, phụ thuộc vào kiểu toán hạng.
   ```js
   console.log(1 + 2);     // 3    — số + số
   console.log(1 + "2");   // "12" — số + chuỗi = nối
   console.log("1" + 2);   // "12" — chuỗi + số = nối
   ```

2. **Với `- * / %`, chuỗi số sẽ được ép thành số**:
   ```js
   console.log("5" - 1);  // 4
   console.log("5" * 2);  // 10
   console.log("abc" - 1); // NaN — không ép được
   ```

3. **`==` với `null`/`undefined` và object** dễ gây kết quả bất ngờ — dùng `===` để an toàn.
   ```js
   console.log(null == undefined);   // true  — special case duy nhất
   console.log(null === undefined);  // false
   console.log("" == false);         // true  — rất dễ nhầm!
   console.log("" === false);        // false
   console.log([] == false);         // true  — [] → "" → false
   console.log([] === false);        // false
   ```

4. **Quên thứ tự `a++`/`++a` khi kẹp trong biểu thức lớn** sẽ cho kết quả sai mà khó tìm.
   ```js
   var a = 5;
   var b = a++ + ++a; // b = 5 + 7 = 12, a = 7
   // a++: dùng 5 rồi thành 6
   // ++a: tăng thành 7 rồi dùng 7
   ```

5. **`==` có những cặp "lạ"** như `true == "1"` → `true`, `[] == ![]` → `true` — rất dễ hiểu nhầm nếu chỉ đọc lướt.
   ```js
   console.log(true == "1");     // true
   console.log(true === "1");    // false
   console.log([] == ![]);       // true ← rất khó tin!
   console.log([] === ![]);      // false
   ```

6. **`NaN === NaN` là `false`** — phải dùng `Number.isNaN()` để kiểm tra.
   ```js
   console.log(NaN === NaN);  // false ← đặc biệt!
   console.log(Number.isNaN(NaN)); // true
   ```

## 💡 Khi nào dùng

1. **So sánh giá trị trong mọi điều kiện** `if`/`while`/`switch` — luôn ưu tiên `===`/`!==`.
2. **Tính toán số học**, lũy thừa (`**`), chia lấy dư (`%`) để kiểm tra chẵn/lẻ.
3. **Cộng dồn dữ liệu** với `+=`, `*=`, tăng đếm trong vòng lặp bằng `++`.
4. **Nối chuỗi** tên, địa chỉ, chuỗi thông báo — nhưng ưu tiên template literal cho code hiện đại.
5. **Kiểm tra truthy/falsy** để quyết định nhánh code — nhớ 7 falsy values.
6. **Short-circuit với `&&` `||`** để gán giá trị mặc định: `const name = input || "Ẩn danh"`.
7. **`!!` để ép thành boolean** rõ ràng: `const isActive = !!(user && user.active)`.
8. **`typeof` để kiểm tra kiểu** trước khi xử lý: `if (typeof value === "number")`.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Arithmetic — ép kiểu ngầm (file `1_toan-tu-so-hoc.js`)
```js
var a = 1, b = "5";
var c = a + b;   // "15" — nối chuỗi
var d = a - b;   // -4   — ép "5" thành số
var e = a * b;   // 5
console.log(c, d, e);

var d2 = "3", e2 = "2";
var f = d2 * e2; // 6   — ép cả hai thành số
console.log(f);
console.log(3 ** 2); // 9 — lũy thừa
```

### Ví dụ 2: Comparison — `==` vs `===` (file `4_toan-tu-so-sanh.js`)
```js
console.log(3 == "3");   // true  — ép kiểu
console.log(3 === "3");  // false — nghiêm ngặt

console.log(true == "1");   // true  — ép kiểu: true→1, "1"→1
console.log(true === "1");  // false

console.log(undefined == null);   // true  — special case
console.log(undefined === null);  // false

console.log("This is a string." == new String("This is a string.")); // true
console.log("This is a string." === new String("This is a string.")); // false — object vs primitive
```

### Ví dụ 3: 7 Falsy Values — kiểm tra trong if
```js
const falsyValues = [0, NaN, "", '', false, null, undefined];
for (const val of falsyValues) {
  if (val) {
    console.log(val, "is truthy");
  } else {
    console.log(val, "is falsy"); // tất cả đều vào đây
  }
}
// 0 is falsy
// NaN is falsy
// "" is falsy
// "" is falsy
// false is falsy
// null is falsy
// undefined is falsy
```

### Ví dụ 4: Logical short-circuit (file `5_toan-tu-logical.js`)
```js
// && — short-circuit AND
console.log(0 && console.log("không chạy")); // 0 — không evaluate right side
console.log(5 && console.log("chạy"));       // undefined — in "chạy", trả về result của console.log

// || — short-circuit OR
console.log(0 || 42);   // 42
console.log(5 || 42);   // 5

// Giá trị mặc định
const config = { timeout: 0 };
const timeout = config.timeout || 5000; // 0 là falsy → dùng 5000 ← có thể không mong muốn!
// ✅ Dùng ?? thay ||
const timeout2 = config.timeout ?? 5000; // 0 — chỉ null/undefined mới fallback
```

### Ví dụ 5: Prefix vs Postfix (file `6_toan-tu-prefix-postfix.js`)
```js
var a = 69;
var b = a++; // b = 69 (giá trị CŨ), sau đó a = 70
console.log(a, b); // 70 69

var number = 6;
var output1 = number++; // output1 = 6 (cũ), number = 7
var output2 = --number; // number = 6 (giảm trước), output2 = 6
console.log(output1 + output2); // 12

// Trong biểu thức phức tạp
var x = 5;
var y = x++ + ++x; // y = 5 + 7 = 12, x = 7
console.log(y, x); // 12 7
```

### Ví dụ 6: Assignment operators (file `3_toan-tu-gan.js`)
```js
let score = 100;
score += 10;  // score = 110
score -= 20;  // score = 90
score *= 2;   // score = 180
score **= 2;  // score = 32400
score /= 10;  // score = 3240
score %= 7;   // score = 3  (3240 % 7 = 3)
console.log(score);
```

### Ví dụ 7: String concatenation (file `2_toan-tu-chuoi.js`)
```js
var firstName = "Nguyễn";
var lastName = "Sơn";
var fullName = firstName + " " + lastName;
console.log(fullName); // "Nguyễn Sơn"

// Template literal (hiện đại hơn)
const greeting = `Xin chào, ${fullName}!`;
console.log(greeting); // "Xin chào, Nguyễn Sơn!"
```

### Ví dụ 8: NaN — đặc biệt của JavaScript
```js
console.log(NaN === NaN);        // false ← đặc biệt!
console.log(Number.isNaN(NaN));  // true  — cách đúng để check NaN
console.log(isNaN("abc"));       // true  — isNaN ép kiểu ngầm: "abc"→NaN
console.log(Number.isNaN("abc"));// false — Number.isNaN không ép kiểu

//NaN trong arithmetic
console.log(5 / "abc");    // NaN
console.log(5 - "abc");    // NaN
console.log("abc" * 2);    // NaN
```

### Ví dụ 9: Ép kiểu kỳ lạ với `==`
```js
console.log("" == 0);       // true  — "" → 0, 0 === 0
console.log("" === 0);      // false
console.log("0" == false);  // true  — "0"→0, false→0
console.log("0" === false); // false
console.log([] == false);   // true  — []→""→0, false→0
console.log([] === false);  // false
console.log([1] == 1);      // true  — [1]→"1"→1
console.log([1] === 1);     // false
```

### Ví dụ 10: Unary `+` ép kiểu nhanh
```js
console.log(+"42");   // 42  — ép string thành số
console.log(+true);   // 1   — true → 1
console.log(+false);  // 0   — false → 0
console.log(+null);   // 0   — null → 0
console.log(+"");     // 0   — "" → 0
console.log(+"abc");  // NaN — không ép được

// So sánh với Number()
console.log(Number("42")); // 42 — tương đương +
console.log(Number("abc")); // NaN
```

## 🔬 So sánh với alternatives

| Toán tử | Alternative | Khi nào thay thế |
|---|---|---|
| `===` | `==` | Không bao giờ — luôn `===` |
| `**` | `Math.pow()` | `**` ngắn gọn hơn, `Math.pow` legacy |
| `||` | `??` | `??` chỉ xét null/undefined, `||` xét mọi falsy |
| `+` nối chuỗi | Template literal | Template literal hiện đại hơn, dễ đọc hơn |
| `Number()` | `+` unary | `+` ngắn gọn hơn, `Number()` rõ nghĩa hơn |
| `isNaN()` | `Number.isNaN()` | `Number.isNaN` không ép kiểu, chính xác hơn |
| `typeof null` | `value === null` | `typeof null === "object"` là bug lịch sử |

## 📊 Performance & Best Practices

**Performance**: Các toán tử cơ bản (`+`, `-`, `*`, `/`, `===`) đều **rất nhanh** — được tối ưu ở cấp độ engine. Không có difference đáng kể giữa các cách viết tương đương.

**Quy tắc coding**:
- **Luôn dùng `===` / `!==`** — trừ khi có lý do đặc biệt (so sánh `null` với `undefined`).
- **Dùng `()` rõ ràng** khi operator precedence không rõ — tránh bug khó tìm.
- **Prefers `??` over `||`** cho default values — `||` treat `0`, `""`, `false` như null.
- **Dùng `Number.isNaN()`** thay `isNaN()` — không ép kiểu ngầm.
- **Prefix `++i`** trong vòng for — mặc dù performance difference không đáng kể, nhưng convention phổ biến.
- **Tránh ép kiểu ngầm** — `+"42"`, `Number("42")` rõ ràng hơn `42 + ""` để convert.
- **Ghi chú 7 falsy values** — nhớ thuộc lòng để tránh bug trong `if` conditions.

**Benchmark** (không đáng kể trong app thông thường):
- `===` nhanh hơn `==` ~5-10% vì không cần type coercion.
- `**` nhanh hơn `Math.pow()` ~2x vì là native operator.
- `+` unary nhanh hơn `Number()` ~10% vì ít function call overhead.

## 🔗 Liên kết chéo

- Tổng quan Operators: `08_expressions-and-operators/README.md` — all operator groups overview.
- Bitwise: `08_expressions-and-operators/02_bitwise/app.js` — thao tác bit, bit flags.
- BigInt: `08_expressions-and-operators/03_bigint-operators/app.js` — số nguyên chính xác.
- Unary: `08_expressions-and-operators/05_unary/app.js` — typeof, void, delete, ép kiểu.
- String: `08_expressions-and-operators/06_string-operators/app.js` — nối chuỗi nâng cao.
- Comparison sâu: `08_expressions-and-operators/01_operators/4_toan-tu-so-sanh.js` — 7 falsy values chi tiết.
- Conditionals: `06_control-flow/01_conditionals/5_condition/1_if.js` — dùng operator trong if condition.
- Callbacks: `09_functions/01_parameters-and-arrow/01_callbacks/` — arrow function dùng operator.
