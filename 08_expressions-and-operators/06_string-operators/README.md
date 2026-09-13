# Toán tử Chuỗi (String Operators) — Thực hành chi tiết — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

Trong JavaScript, **toán tử `+`** khi gặp ít nhất một toán hạng là chuỗi sẽ thực hiện **nối chuỗi** (string concatenation) thay vì phép cộng số học — đây được gọi là string operator behavior. Ngoài ra còn có biến thể gán **`+=`** để nối và gán cùng lúc.

```js
console.log("a" + "b");           // "ab"
console.log("a".concat("b"));     // "ab" — phương thức concat tương đương
let s = "hi";
s += " there";                    // s = "hi there"
console.log(s);
```

Ba cách nối chuỗi phổ biến:

1. **Toán tử `+`** — nhanh, được dùng rộng rãi, tự động ép kiểu các toán hạng khác thành chuỗi.
2. **`+=`** — nối thêm vào biến hiện tại, gọn gàng cho accumulator.
3. **`.concat(string)`** — phương thức của String, ít dùng hơn nhưng cho nhiều đối số.
4. **(Nâng cao) Template literal** với backtick `` ` `` — `` `Hello ${name}` `` là cách **hiện đại nhất**, tránh những phiền phức của dấu `+`.

**Cơ chế ép kiểu**: khi `+` gặp string, JavaScript ép TOÀN BỘ các toán hạng thành chuỗi rồi nối. Điều này có nghĩa `1 + 2 + "3"` cho kết quả khác `"1" + 2 + 3`.

## 📐 Cấu trúc / Cú pháp

### Toán tử `+` — Nối chuỗi
```js
"hello" + " " + "world"  // "hello world"
"Score: " + 42           // "Score: 42" — số được ép thành chuỗi
"Prefix: " + true        // "Prefix: true"
"Value: " + null         // "Value: null"
"Value: " + undefined    // "Value: undefined"
```

### Toán tử `+=` — Nối và gán
```js
let message = "Xin";
message += " chào";      // "Xin chào"
message += " bạn!";      // "Xin chào bạn!"
```

### `.concat()` — Phương thức chuỗi
```js
"hello".concat(" ", "world");        // "hello world"
"hello".concat(" ", "world", "!");   // "hello world!" — multiple args
"a".concat(1, 2, 3);                 // "a123" — ép tất cả thành string
```

### Template Literal (ES6) — Cách hiện đại nhất
```js
const name = "Sơn";
const age = 18;
const greeting = `Xin chào, ${name}! Bạn ${age} tuổi.`;
// "Xin chào, Sơn! Bạn 18 tuổi."

// Multiline string
const html = `
  <div class="card">
    <h2>${title}</h2>
    <p>${description}</p>
  </div>
`;

// Expression trong template
const result = `Tổng: ${1 + 2 + 3} = ${6}`; // "Tổng: 6 = 6"
```

## ✅ Điểm mạnh

1. **Đơn giản, dễ đọc** với `+` và `+=` — không cần thư viện gì cả, ai cũng hiểu được.
2. **Nối được đủ mọi kiểu**: `"Số: " + 42` tự đổi 42 thành chuỗi — implicit coercion tiện lợi.
3. **Template literal giúp nối kèm biến** rõ ràng và xuống dòng dễ — đọc như ngôn ngữ tự nhiên.
4. **`+=` giúp cộng dồn chuỗi trong vòng lặp/accumulator** gọn gàng — pattern phổ biến.
5. **Là nền tảng cho việc tạo URL**, câu thông báo, giao diện hiển thị — gần như every web app cần.
6. **`.concat()` chấp nhận nhiều đối số** — nối nhiều chuỗi cùng lúc mà không cần `+` nhiều lần.
7. **Template literal hỗ trợ expression** — `${1 + 2}` tính toán ngay trong string.
8. **Multiline string** — template literal hỗ trợ xuống dòng thật sự, khác `+` phải `\n`.
9. **Performance tốt** — V8 tối ưu string concatenation, đặc biệt với `+=` trong loop.
10. **Cross-platform** — hoạt động giống nhau trên browser và Node.js.

## ⚠️ Bẫy thường gặp & Hạn chế

1. **Thứ tự quan trọng**: `1 + 2 + "3"` → `"33"` (cộng số trước) nhưng `"1" + 2 + 3` → `"123"` (nối hết). **Kết quả phụ thuộc vị trí của chuỗi**.
   ```js
   console.log(1 + 2 + "3"); // "33" — (1+2) + "3" = 3 + "3" = "33"
   console.log("1" + 2 + 3); // "123" — ("1"+2) +3 = "12" + 3 = "123"
   console.log(1 + "2" + 3); // "123" — (1+"2") +3 = "12" + 3 = "123"
   ```

2. **Nối quá nhiều chuỗi bằng `+` trong vòng lặp lớn** có thể chậm — lúc đó gom vào mảng rồi `join("")` hiệu quả hơn.
   ```js
   // ❌ Chậm với loop lớn
   let result = "";
   for (let i = 0; i < 10000; i++) {
     result += "item" + i;
   }

   // ✅ Nhanh hơn — array join pattern
   const parts = [];
   for (let i = 0; i < 10000; i++) {
     parts.push("item" + i);
   }
   const result2 = parts.join("");
   ```

3. **Số được tự ép thành chuỗi khi nối**, đôi khi gây ngạc nhiên (vd: giá trị từ form bất ngờ ra "12" thay vì 3).
   ```js
   const input = "5";
   console.log(input + 7); // "57" ← không phải 12!
   console.log(parseInt(input) + 7); // 12 ← đúng
   ```

4. **`.concat()` không chấp nhận mọi kiểu linh hoạt như `+`** — nhưng thực tế `.concat()` cũng ép kiểu tương đương.
   ```js
   "a".concat(1, 2); // "a12" — tương đương "a" + 1 + 2
   ```

5. **Template literal với `${}`** — nếu biểu thức trong `${}` throw error, toàn bộ template lỗi.
   ```js
   const name = null;
   const msg = `Hello ${name.toUpperCase()}`; // TypeError!
   // ✅ Safe: `Hello ${name?.toUpperCase() ?? "Guest"}`
   ```

6. **Trộn template literal với `+`** — dễ nhầm `${}` với `{}` object literal.
   ```js
   // ❌ Nhầm lẫn
   const obj = `{ name: "${name}" }`; // string, không phải object!
   // ✅ Đúng
   const obj = { name }; // object literal
   ```

## 💡 Khi nào dùng

1. **Ghép tên đầy đủ**: `firstName + " " + lastName` — đơn giản, rõ ràng.
2. **Xây URL động**, route, query string — `` `https://api.com/users/${id}` ``.
3. **Tạo thông báo / string log** cho người dùng — `` `User ${name} logged in` ``.
4. **Gộp chuỗi lặp lại theo điều kiện** bằng `+=` — accumulator pattern.
5. **Dựng chuỗi HTML/giao diện đơn giản** — nên dùng template literal cho rõ ràng hơn.
6. **Multi-line string** (log, SQL query, HTML template) — template literal down dòng thật.
7. **Escape sequence trong string** — `` `Line 1\nLine 2` `` dễ đọc hơn `'Line 1\\nLine 2'`.
8. **Tagged template literals** — advanced: `` sql`SELECT * FROM users WHERE id = ${id}` ``.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Cơ bản — nối chuỗi (file `app.js`)
```js
// Nội dung app.js trong thư mục
console.log("a" + "b", "a".concat("b")); // "ab" "ab"

let s = "hi";
s += " there";
console.log(s); // "hi there"
```

### Ví dụ 2: Thứ tự ảnh hưởng kết quả
```js
// Thứ tự đánh giá从左 sang phải
console.log(1 + 2 + "3"); // "33" — (1+2)="3", then "3"+"3"="33"
console.log("1" + 2 + 3); // "123" — ("1"+2)="12", then "12"+3="123"
console.log(1 + "2" + 3); // "123" — (1+"2")="12", then "12"+3="123"
console.log("A" + "B" + 1 + 2); // "AB12" — tất cả nối chuỗi
console.log(1 + 2 + "A" + "B"); // "3AB" — (1+2)=3, then "3"+"A"+"B"="3AB"
```

### Ví dụ 3: Tự ép kiểu với các giá trị đặc biệt
```js
console.log("Value: " + null);     // "Value: null"
console.log("Value: " + undefined); // "Value: undefined"
console.log("Value: " + true);     // "Value: true"
console.log("Value: " + false);    // "Value: false"
console.log("Value: " + NaN);      // "Value: NaN"
console.log("Value: " + []);       // "Value: "
console.log("Value: " + [1, 2]);   // "Value: 1,2"
console.log("Value: " + {});       // "Value: [object Object]"
```

### Ví dụ 4: Template literal — cách hiện đại
```js
const name = "Sơn Nguyễn";
const age = 18;
const city = "An Giang";

// Template literal
const bio = `Tên: ${name}
Tuổi: ${age}
Quê quán: ${city}`;
console.log(bio);
// Tên: Sơn Nguyễn
// Tuổi: 18
// Quê quán: An Giang

// Expression trong template
const doubled = 21;
console.log(`21 × 2 = ${21 * 2}`); // "21 × 2 = 42"
```

### Ví dụ 5: Accumulator pattern với +=
```js
// Gộp nhiều phần tử thành chuỗi
const items = ["HTML", "CSS", "JS", "PHP"];
let result = "";
for (const item of items) {
  result += item + ", ";
}
result = result.slice(0, -2); // bỏ ", " cuối
console.log(result); // "HTML, CSS, JS, PHP"

// ✅ Tốt hơn: Array.join()
console.log(items.join(", ")); // "HTML, CSS, JS, PHP"
```

### Ví dụ 6: Xây URL động
```js
const baseUrl = "https://api.example.com";
const endpoint = "users";
const userId = 123;
const apiKey = "abc123";

// Template literal — rõ ràng
const url = `${baseUrl}/${endpoint}/${userId}?key=${apiKey}`;
console.log(url); // "https://api.example.com/users/123?key=abc123"

// + concatenation — dài dòng hơn
const url2 = baseUrl + "/" + endpoint + "/" + userId + "?key=" + apiKey;
```

### Ví dụ 7: HTML generation với template literal
```js
const user = { name: "Sơn", role: "admin" };

// ❌ Dài dòng với +
const html1 = "<div class='user'>" +
  "<span>" + user.name + "</span>" +
  "<span>" + user.role + "</span>" +
  "</div>";

// ✅ Rõ ràng với template literal
const html2 = `
  <div class="user">
    <span>${user.name}</span>
    <span>${user.role}</span>
  </div>
`;
```

### Ví dụ 8: escape sequence trong template literal
```js
// Template literal hỗ trợ escape sequence bình thường
const path = "C:\\Users\\Sơn\\Documents";
console.log(path); // C:\Users\Sơn\Documents

// Multiline — template literal down dòng thật sự
const sql = `
  SELECT name, age
  FROM users
  WHERE age > 18
  ORDER BY name
`;
console.log(sql);
// (in ra multiline SQL đúng như viết)

// + concatenation — phải dùng \n thủ công
const sql2 = "SELECT name, age\nFROM users\nWHERE age > 18\nORDER BY name";
```

### Ví dụ 9: String concat với nhiều arguments
```js
// .concat() chấp nhận nhiều arguments
console.log("hello".concat(" ", "world"));           // "hello world"
console.log("hello".concat(" ", "world", "!"));      // "hello world!"
console.log("a".concat(1, 2, 3));                    // "a123"
console.log("foo".concat(undefined, null));          // "fooundefinednull"

// + tương đương nhưng cần nhiều + signs
console.log("hello" + " " + "world" + "!");          // "hello world!"
```

### Ví dụ 10: Tagged template literal — advanced
```js
// Tagged template — function nhận parts và values
function sql(strings, ...values) {
  const result = strings.reduce((acc, str, i) => {
    return acc + str + (values[i] ?? "");
  }, "");
  return result;
}

const name = "Sơn";
const age = 18;
const query = sql`SELECT * FROM users WHERE name = ${name} AND age = ${age}`;
console.log(query); // "SELECT * FROM users WHERE name = Sơn AND age = 18"

// ⚠️ Lưu ý: tagged template KHÔNG escape — dễ SQL injection trong thực tế!
// Luôn dùng parameterized query trong production.
```

## 🔬 So sánh với alternatives

| Phương án | Ưu điểm | Nhược điểm | Phù hợp khi |
|---|---|---|---|
| `+` concatenate | Nhanh, đơn giản, phổ biến | Dài dòng với nhiều biến | String đơn giản, performance-critical |
| `+=` accumulator | Gọn cho loop accumulation | Tạo string mới mỗi iter | Vòng lặp ghép chuỗi |
| `.concat()` | Multiple args, chainable | Ít dùng hơn, verbose | Nối nhiều string cùng lúc |
| Template literal | Đọc dễ, multiline, expressions | ES6+ (không support IE) | Modern codebase (recommended) |
| `Array.join()` | Fast nhất cho nhiều parts | Cần array intermediate | Loop ghép nhiều phần tử |

## 📊 Performance & Best Practices

**Performance ranking** (từ nhanh nhất đến chậm nhất, với 10k+ parts):
1. `Array.join("")` — fastest, engine tối ưu memory allocation
2. Template literal — rất nhanh, compile-time optimized
3. `+=` trong loop — chậm hơn do tạo string mới mỗi lần
4. `.concat()` chain — chậm nhất do nhiều function calls

**Best practices**:
- **Ưu tiên template literal** cho code hiện đại — đọc dễ, viết nhanh, multiline support.
- **Dùng `Array.join("")`** khi ghép nhiều (>10) parts trong vòng lặp — performance gain thực sự.
- **Dùng `()` rõ ràng** khi trộn arithmetic với string: `` `Tổng: ${(1 + 2)} = 3` ``.
- **Tránh `+=` trong loop lớn** — dùng array join pattern thay thế.
- **Template literal với `${expr}`** — expr nào cũng được, kể cả function call, ternary.
- **Escape `${}` trong template** — `` `\${literal}` `` để in ra `${` thật sự.
- **Không trộn `+` và template** trong cùng expression — chọn một style cho consistent.

**Quy tắc "3 nên — 3 không"**:
- ✅ Nên dùng template literal cho string hiện đại.
- ✅ Nên dùng `Array.join()` cho loop concatenation lớn.
- ✅ Nên dùng `()` để rõ precedence khi trộn arithmetic.
- ❌ Không nên `+=` trong vòng lặp >100 iter.
- ❌ Không nên trộn `+` và template literal cùng lúc.
- ❌ Không nên `.concat()` chain dài — dùng `+` hoặc template.

## 🔗 Liên kết chéo

- Tổng quan Operators: `08_expressions-and-operators/README.md` — all operator groups overview.
- Arithmetic operators: `08_expressions-and-operators/01_operators/1_toan-tu-so-hoc.js` — `+` với số vs string.
- Unary operators: `08_expressions-and-operators/05_unary/app.js` — `+` unary ép string → number.
- Comparison: `08_expressions-and-operators/01_operators/4_toan-tu-so-sanh.js` — `==` vs `===` với string.
- Functions: `09_functions/01_parameters-and-arrow/03_arrow-functions/` — arrow function return template string.
- Callbacks: `09_functions/01_parameters-and-arrow/01_callbacks/` — callback return string value.
- Regex: (không có trong repo này nhưng liên quan) — string manipulation với regex replace.
