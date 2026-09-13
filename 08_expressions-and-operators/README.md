# Biểu thức và Toán tử (Expressions & Operators) — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

Một **expression** (biểu thức) là bất kỳ đoạn code nào **trả về một giá trị** — ví dụ `5 + 3`, `a > b`, `x = 10`, `"hello"`. Mọi thứ trong JavaScript đều là expression (hoặc có thể dùng ở vị trí expression), kể cả function call, object literal, array literal.

Một **operator** (toán tử) là ký hiệu thực hiện thao tác lên các *operand* (toán hạng) để tạo ra giá trị mới. JavaScript có rất nhiều nhóm toán tử, và đây là lộ trình học đầy đủ theo roadmap.sh — từ cơ bản đến các toán tử ít dùng nhưng vẫn cần biết mặt:

| Thư mục | Nhóm toán tử | Ví dụ | Mức độ phổ biến |
|---|---|---|---|
| `01_operators/` | Cơ bản: số học, chuỗi, gán, so sánh, logical, prefix/postfix | `+`, `**`, `=`, `===`, `&&`, `++` | ⭐⭐⭐⭐⭐ Rất phổ biến |
| `02_bitwise/` | Bitwise — thao tác trên từng bit | `&`, `|`, `^`, `~`, `<<`, `>>`, `>>>` | ⭐⭐ Trung bình |
| `03_bigint-operators/` | Toán tử trên số BigInt | `10n + 5n`, `2n ** 10n` | ⭐⭐ Ngày càng quan trọng |
| `04_comma/` | Dấu phẩy — trả về toán hạng cuối | `(1, 2, 3) → 3` | ⭐ Hiếm dùng |
| `05_unary/` | Toán tử một ngôi | `typeof`, `void`, `delete`, `+`, `-`, `!` | ⭐⭐⭐ Phổ biến |
| `06_string-operators/` | Nối chuỗi | `+`, `+=`, `.concat()` | ⭐⭐⭐⭐ Phổ biến |

**Quan điểm then chốt**: hiểu rõ operator giúp bạn đọc code của người khác (npm packages, thư viện) không lúng túng, và viết code đúng意图 — không bị bẫy bởi implicit type coercion hay operator precedence.

## 📐 Cấu trúc / Cú pháp

### Nhóm 1: Arithmetic (Số học) — `01_operators/1_toan-tu-so-hoc.js`
```js
+   // cộng / nối chuỗi
-   // trừ
*   // nhân
**  // lũy thừa (ES2016)
/   // chia
%   // chia lấy dư
++  // tăng 1 (prefix/postfix)
--  // giảm 1 (prefix/postfix)
```

### Nhóm 2: Assignment (Gán) — `01_operators/3_toan-tu-gan.js`
```js
=   // gán
+=  // cộng rồi gán
-=  // trừ rồi gán
*=  // nhân rồi gán
**= // lũy thừa rồi gán
/=  // chia rồi gán
%=  // modulo rồi gán
```

### Nhóm 3: Comparison (So sánh) — `01_operators/4_toan-tu-so-sanh.js`
```js
==  // bằng (ép kiểu)
!=  // không bằng (ép kiểu)
=== // bằng nghiêm ngặt (không ép kiểu) ⭐ NÊN DÙNG
!== // không bằng nghiêm ngặt ⭐ NÊN DÙNG
>   // lớn hơn
<   // nhỏ hơn
>=  // lớn hơn hoặc bằng
<=  // bé hơn hoặc bằng
```

### Nhóm 4: Logical (Logic) — `01_operators/5_toan-tu-logical.js`
```js
&&  // AND — short-circuit: nếu trái falsy thì trả trái, không評価右
||  // OR  — short-circuit: nếu trái truthy thì trả trái, không評価右
!   // NOT  — phủ định, ép thành boolean
```

### Nhóm 5: Bitwise — `02_bitwise/app.js`
```js
&   // AND từng bit
|   // OR từng bit
^   // XOR từng bit
~   // NOT (đảo bit)
<<  // dịch trái (nhân lũy thừa 2)
>>  // dịch phải có dấu (chia lũy thừa 2, giữ sign)
>>> // dịch phải không dấu (chia lũy thừa 2, fill 0)
```

### Nhóm 6: BigInt — `03_bigint-operators/app.js`
```js
10n + 5n  // 15n
10n * 2n  // 20n
10n / 3n  // 3n  ← luôn trả về số nguyên!
10n % 3n  // 1n
2n ** 10n // 1024n
```

### Nhóm 7: Comma — `04_comma/app.js`
```js
let x = (1, 2, 3); // x = 3 — trả về giá trị cuối
for (let i = 0, j = 10; i < j; i++, j--) {} // gộp nhiều bước
```

### Nhóm 8: Unary — `05_unary/app.js`
```js
typeof 123       // "number"
void 0           // undefined
delete obj.prop  // true/false
+"42"            // 42 (ép string → number)
-"42"            // -42
!0               // true
!!1              // true (ép thành boolean)
```

### Nhóm 9: String — `06_string-operators/app.js`
```js
"a" + "b"         // "ab"
"a".concat("b")   // "ab"
let s = "hi"; s += " there" // "hi there"
```

## ✅ Điểm mạnh

1. **Phủ đầy đủ lộ trình roadmap.sh** — từ cơ bản đến các toán tử ít dùng nhưng vẫn cần biết.
2. **Mỗi nhóm có thư mục riêng** với ví dụ chạy được ngay, dễ tìm lại khi cần.
3. **Biết đủ nhóm toán tử** giúp đọc code của người khác (npm, thư viện) không lúng túng.
4. **Là nền tảng hiểu rõ "biểu thức"** — khái niệm xuyên suốt mọi part sau này (ternary, short-circuit, template...).
5. **Ví dụ minh họa tính toán thực tế** — so sánh `3 == "3"` vs `3 === "3"`, bit flags, BigInt.
6. **Toán tử bitwise** cho phép tối ưu thấp level — bit flags, mask, rapid multiply/divide.
7. **BigInt** khắc phục giới hạn Number — chính xác tuyệt đối với số nguyên lớn.
8. **Unary operators** (`typeof`, `!!`, `+`) là công cụ ép kiểu nhanh gọn không cần hàm.
9. **String operators** (`+`, `+=`, `.concat()`) là nền tảng của string manipulation.
10. **Comma operator** tuy hiếm nhưng hữu ích trong `for` loop với nhiều biến đếm.

## ⚠️ Bẫy thường gặp & Hạn chế

1. **`==` dễ gây lỗi ngầm do tự ép kiểu** — ưu tiên `===` / `!==` trong mọi trường hợp.
   ```js
   console.log(3 == "3");   // true  ← ép kiểu ngầm
   console.log(3 === "3");  // false ← nghiêm ngặt
   console.log(true == "1"); // true ← rất dễ nhầm!
   ```

2. **Prefix (`++i`) và postfix (`i++`) cho kết quả khác nhau khi nằm trong biểu thức**.
   ```js
   let a = 5;
   let b = a++; // b = 5 (cũ), a = 6 (mới)
   let c = ++a; // a = 7 (mới), c = 7
   ```

3. **BigInt không trộn được với Number** trong cùng phép toán — lỗi `TypeError`.
   ```js
   10n + 1; // TypeError: Cannot mix BigInt and other types
   ```

4. **Bitwise chỉ hoạt động trên số 32-bit** — kết quả có thể gây bất ngờ với số lớn.
   ```js
   console.log(5 << 30); // 2147483640 — gần sát giới hạn 32-bit signed
   console.log(5 << 31); // -1073741824 — overflow, bit sign bị ảnh hưởng
   ```

5. **`typeof null` trả về `"object"`** — lỗi lịch sử của JavaScript, đừng dùng để kiểm tra null.
   ```js
   typeof null === "object"; // true ← bug lịch sử!
   null === null;            // true ← dùng cái này
   ```

6. **Thứ tự operator precedence** — `+` ưu tiên cao hơn `===`, cần `()` rõ ràng.
   ```js
   1 + 2 === 3;    // (1+2) === 3 → true
   1 + (2 === 3);  // 1 + false → 1 ← khác hoàn toàn!
   ```

7. **`delete` chỉ xóa property của object**, không xóa biến.
   ```js
   let x = 1;
   delete x; // false — không xóa được biến
   const obj = { a: 1 };
   delete obj.a; // true
   ```

8. **`eval()` chạy mã động** — nguy hiểm (code injection) và chậm — hạn chế tối đa.

## 💡 Khi nào dùng

1. **Tính toán, so sánh, gán giá trị** — diễn ra trong gần như mọi dòng code.
2. **Viết điều kiện phức tạp** với `&&`, `||`, `!` — đặc biệt với short-circuit để đặt giá trị mặc định.
3. **Xử lý quyền, cờ trạng thái** (permissions) với phép toán bitwise — `READ | WRITE`, `perm & READ`.
4. **Làm việc với số nguyên siêu lớn** vượt quá `Number.MAX_SAFE_INTEGER` → BigInt.
5. **Kiểm tra kiểu** với `typeof`, trả về `undefined` bằng `void` (vd: THJS `void 0`), xóa thuộc tính bằng `delete`.
6. **Nối chuỗi động** — template literal hiện đại hơn, nhưng `+` vẫn phổ biến trong code legacy.
7. **Arrow function implicit return** — `x => x * 2` dùng toán tử trong expression body.
8. **Ternary operator** — `cond ? a : b` chọn giá trị trong một expression.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Arithmetic + String coercion (file `1_toan-tu-so-hoc.js`)
```js
var a = 1, b = "5";
console.log(a + b); // "15"  — nối chuỗi vì có string
console.log(a - b); // -4    — ép "5" thành số
console.log(3 ** 2); // 9    — lũy thừa
```

### Ví dụ 2: Comparison — `==` vs `===` (file `4_toan-tu-so-sanh.js`)
```js
console.log(3 == "3");   // true  — ép kiểu: "3" → 3
console.log(3 === "3");  // false — nghiêm ngặt: khác kiểu
console.log(undefined == null);   // true  — đặc biệt case
console.log(undefined === null);  // false
console.log(true == "1");  // true  — rất dễ nhầm!
console.log(true === "1"); // false
```

### Ví dụ 3: Prefix vs Postfix (file `6_toan-tu-prefix-postfix.js`)
```js
var a = 69;
var b = a++; // b nhận giá trị CŨ (69), sau đó a tăng thành 70
console.log(a, b); // 70 69

var number = 6;
var output1 = number++; // output1 = 6 (cũ)
var output2 = --number; // number giảm thành 6, output2 = 6 (mới)
console.log(output1 + output2); // 12
```

### Ví dụ 4: Bitwise — bit flags (file `app.js` trong `02_bitwise/`)
```js
console.log(5 & 1, 5 | 1, 5 ^ 1, ~5, 5 << 1, 5 >> 1, -5 >>> 1);
// => 1 5 4 -6 10 2 2147483645

// Bit flags — quyền đọc ghi chạy
const READ = 1, WRITE = 2, EXEC = 4;
let perm = READ | WRITE; // 3
console.log(perm & READ); // 1  → có quyền đọc
console.log(perm & EXEC); // 0  → không có quyền chạy
```

### Ví dụ 5: BigInt — số nguyên chính xác (file `app.js` trong `03_bigint-operators/`)
```js
console.log(10n + 5n, 10n * 2n, 10n / 3n, 10n % 3n, 2n ** 10n);
// 15n 20n 3n 1n 1024n

// Số lớn hơn giới hạn an toàn của Number
console.log(9007199254740991n + 1n); // 9007199254740992n (chính xác)
```

### Ví dụ 6: Comma operator (file `app.js` trong `04_comma/`)
```js
let x = (1, 2, 3);
console.log(x); // 3 — chỉ lấy giá trị cuối

for (let i = 0, j = 10; i < j; i++, j--) {
  console.log(i, j); // 0 10 / 1 9 / 2 8 / 3 7 / 4 6
}
```

### Ví dụ 7: Unary operators (file `app.js` trong `05_unary/`)
```js
console.log(typeof 123, typeof null); // "number" "object"
console.log(void 0, void(1 + 1));     // undefined undefined
let o = { a: 1, b: 2 };
delete o.a;
console.log(o);                       // { b: 2 }
console.log(+"42", -"42", !0, !!1);   // 42 -42 true true
```

### Ví dụ 8: String operators (file `app.js` trong `06_string-operators/`)
```js
console.log("a" + "b", "a".concat("b")); // "ab" "ab"
let s = "hi";
s += " there";
console.log(s); // "hi there"

// Thứ tự ảnh hưởng kết quả
console.log(1 + 2 + "3"); // "33" — cộng số trước, rồi nối
console.log("1" + 2 + 3); // "123" — nối hết
```

### Ví dụ 9: Logical operators — short-circuit evaluation
```js
// && — short-circuit: nếu trái falsy thì trả trái
console.log(0 && 42);   // 0 (không evaluate phải)
console.log(5 && 42);   // 42 (trái truthy → trả phải)

// || — short-circuit: nếu trái truthy thì trả trái
console.log(0 || 42);   // 42 (trái falsy → evaluate phải)
console.log(5 || 42);   // 5 (trái truthy → trả trái)

// Giá trị mặc định với ||
const name = userInput || "Ẩn danh";
// ES2020: const name = userInput ?? "Ẩn danh"; // chỉ xét null/undefined
```

### Ví dụ 10: Operator precedence — dùng `()` để rõ ràng
```js
// Không dùng () — đọc theo precedence
console.log(1 + 2 * 3);     // 7 — * ưu tiên cao hơn +
console.log((1 + 2) * 3);   // 9 — () ép tính trước

// Ternary precedence thấp hơn many operators
console.log(true ? 1 : 2 + 3);     // 1 — ternary đánh giá trước +
console.log(true ? 1 : (2 + 3));   // 1 — rõ ràng hơn

// typeof có precedence cao hơn ===
console.log(typeof "hi" === "string"); // true
console.log(typeof ("hi" === "string")); // "boolean" ← khác!
```

## 🔬 So sánh với alternatives

| Toán tử | Alternatives |所以当 |
|---|---|---|
| `===` | `==` | Luôn dùng `===` — tránh bẫy ép kiểu |
| `**` | `Math.pow()` | `**` ngắn gọn hơn, ES2016 |
| `??` | `\|\|` | `??` chỉ xét null/undefined, `||` xét mọi falsy |
| Template literal | String concat `+` | Template literal đọc dễ hơn, hỗ trợ multiline |
| Bitwise | Math operations | Bitwise nhanh hơn cho nhân/chia lũy thừa 2 |
| BigInt | Number | BigInt cho số > 2^53-1, Number cho số thông thường |
| `typeof` | `instanceof` | `typeof` cho primitive, `instanceof` cho object type |

## 📊 Performance & Best Practices

**Operator precedence** (từ cao xuống thấp, quan trọng cho readability):
1. `()` — grouping
2. `.` `[]` — property access
3. `new` `()` — function call
4. `++` `--` — unary increment/decrement
5. `!` `~` `+` `-` `typeof` `void` `delete` — unary operators
6. `*` `/` `%` — multiplication
7. `+` `-` — addition
8. `<<` `>>` `>>>` — bitwise shift
9. `<` `>` `<=` `>=` — comparison
10. `===` `!==` `==` `!=` — equality
11. `&` — bitwise AND
12. `^` — bitwise XOR
13. `|` — bitwise OR
14. `&&` — logical AND
15. `||` — logical OR
16. `??` — nullish coalescing
17. `? :` — ternary
18. `=` `+=` `-=` etc. — assignment

**Best practices**:
- **Luôn dùng `===` / `!==`** thay `==` / `!=` — trừ khi có lý do rõ ràng.
- **Dùng `()` rõ ràng** khi precedence không rõ — code đọc easier.
- **Prefix vs Postfix**: dùng prefix (`++i`) khi cần giá trị mới ngay, postfix (`i++`) khi cần giá trị cũ.
- **BigInt**: dùng khi làm việc với số > `Number.MAX_SAFE_INTEGER` (ID, tài chính, crypto).
- **Bitwise**: chỉ dùng khi thực sự cần (bit flags, image processing) — không dùng thay cho math thông thường.
- **Tránh `delete`** trên object properties trong performance-critical code — có thể de-optimize engine.
- **Comma operator**: hạn chế dùng — chỉ trong `for` loop với nhiều biến đếm.
- **Unary `+`/`-`** ép kiểu nhanh hơn `Number()`: `+"42"` vs `Number("42")`.

## 🔗 Liên kết chéo

- operadores cơ bản: `08_expressions-and-operators/01_operators/` — 6 file từ số học đến prefix/postfix.
- Bitwise: `08_expressions-and-operators/02_bitwise/app.js` — bit flags, quyền đọcghi.
- BigInt: `08_expressions-and-operators/03_bigint-operators/app.js` — số nguyên chính xác.
- Comma: `08_expressions-and-operators/04_comma/app.js` — toán tử phẩy.
- Unary: `08_expressions-and-operators/05_unary/app.js` — typeof, void, delete, ép kiểu.
- String: `08_expressions-and-operators/06_string-operators/app.js` — nối chuỗi.
- Conditionals: `06_control-flow/01_conditionals/` — ternary operator dùng toán tử `? :`.
- Callbacks: `09_functions/01_parameters-and-arrow/01_callbacks/` — arrow function dùng operator trong body.
