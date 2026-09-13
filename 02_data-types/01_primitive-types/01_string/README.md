# String (Chuỗi) — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

**String** là kiểu primitive dùng để biểu diễn **chuỗi ký tự** (văn bản). Trong JavaScript, string là **bất biến (immutable)** — mọi thao tác trên string đều tạo ra string mới, không sửa string gốc.

### 3 cách tạo string

```js
var fullName_1 = 'Sơn Nguyễn';          // 1. dấu nháy đơn (single quotes)
var fullName_2 = "Sơn Nguyễn";          // 2. dấu nháy kép (double quotes)
var fullName_3 = `Tôi là ${firstName}`; // 3. template string (backticks, ES6)
```

**Cách nên dùng:** Template string `` ` `` khi cần chèn biến (`${ten}`) hoặc viết chuỗi nhiều dòng; nháy đơn/kép tùy quán đội nhóm nhưng **giữ nhất quán** ( ESLint `quotes` rule enforce).

**Cách tránh:** `new String('...')` — kết quả là **object** wrapper, không phải primitive:

```js
var fullName_2 = new String('Sơn Nguyễn'); // typeof === "object" ❌
console.log(typeof fullName_2);            // "object"
// Đừng dùng — mất tính primitive, methods khác primitive string
```

### Ký tự đặc biệt (escape) bằng backslash `\`

```js
var fullName_3 = 'Sơn Nguyễn \\ là \'Siêu Nhân\'';
console.log(fullName_3);
// Sơn Nguyễn \ là 'Siêu Nhân'

// Common escape sequences
console.log("Line 1\nLine 2");     // newline
console.log("Tab\there");         // tab
console.log("Quote: \"hello\"");  // escaped quote
console.log("Path: C:\\Users\\name"); // escaped backslash
```

### Độ dài chuỗi — `.length`

```js
var fullName_4 = 'Sơn Nguyễn';
console.log(fullName_4.length); // 10

// Chú ý: `.length` đếm theo UTF-16 code units — ký tự Unicode phức tạp (emoji,某些 characters) có thể tính thành 2
console.log("😀".length);        // 2 — emoji là surrogate pair
console.log("😀".length === 1);  // false
// Dùng `[..."😀"].length` hoặc `Array.from("😀").length` để đếm đúng code points
```

### Template string (ES6) — chèn biến + xuống dòng thoải mái

```js
var firstName = 'Sơn';
var lastName = 'Nguyễn';
var age = 23;

var fullName_5 = `Tôi là ${firstName} ${lastName}, ${age} tuổi.`;
console.log(fullName_5); // Tôi là Sơn Nguyễn, 23 tuổi.

// Multi-line string — xuống dòng tự nhiên
var html = `
  <div class="card">
    <h1>${title}</h1>
    <p>${description}</p>
  </div>
`;

// Expression trong template — tính toán được
var result = `Tổng: ${1 + 2 + 3} | Format: ${(42).toFixed(2)}`;
console.log(result); // "Tổng: 6 | Format: 42.00"
```

### Các phương thức thao tác chuỗi thường dùng

| Phương thức | Ý nghĩa | Trả về | Mutable? |
|-------------|---------|--------|----------|
| `indexOf(tìm)` | vị trí ký tự đầu tiên, `-1` nếu không thấy | number | — |
| `lastIndexOf(tìm)` | vị trí ký tự cuối cùng | number | — |
| `search(regex)` | tìm theo biểu thức chính quy | number (-1 if not found) | — |
| `slice(from, to)` | cắt chuỗi (hỗ trợ index âm) | string | — |
| `substring(from, to)` | tương tự slice, không hỗ trợ âm | string | — |
| `replace(a, b)` | thay thế lần đầu | string | — |
| `replace(/a/g, b)` | thay thế TẤT CẢ (cờ `g`) | string | — |
| `replaceAll(a, b)` | ES2021: thay thế tất cả | string | — |
| `toUpperCase()` | viết hoa | string | — |
| `toLowerCase()` | viết thường | string | — |
| `trim()` | bỏ khoảng trắng hai đầu | string | — |
| `trimStart()` / `trimLeft()` | bỏ khoảng trắng đầu | string | — |
| `trimEnd()` / `trimRight()` | bỏ khoảng trắng cuối | string | — |
| `split(dấu_phân_cách)` | tách thành mảng | array | — |
| `charAt(i)` / `str[i]` | lấy ký tự theo vị trí | string (1 char) | — |
| `charCodeAt(i)` | mã Unicode tại vị trí | number | — |
| `concat(str2, str3...)` | nối chuỗi (ít dùng, `+` hoặc template tiện hơn) | string | — |
| `includes(searchString)` | ES2015: có chứa không? | boolean | — |
| `startsWith(prefix)` | ES2015: bắt đầu bằng? | boolean | — |
| `endsWith(suffix)` | ES2015: kết thúc bằng? | boolean | — |
| `repeat(n)` | ES2015: lặp n lần | string | — |
| `padStart/targetWidth, padString)` | ES2017: padding đầu | string | — |
| `padEnd(targetWidth, padString)` | ES2017: padding cuối | string | — |

## ✅ Điểm mạnh — Tại sao nên dùng string

| # | Điểm mạnh | Lý do |
|---|-----------|-------|
| 1 | **Primitive bất biến** | An toàn, không lo bị thay đổi ngoài ý muốn — pass around freely |
| 2 | **Template string sạch** | Nối chuỗi phức tạp gọn gàng thay cho dấu `+` chồng chất |
| 3 | **Hệ thống phương thức đầy đủ** | slice, trim, split, replace... đủ mạnh cho phần lớn thao tác văn bản |
| 4 | **`replace` kết hợp regex** | Chỉnh sửa cụm linh hoạt — chuẩn hóa định dạng, validate |
| 5 | **Đọc/gỡ lỗi dễ** | Chuỗi hiển thị trực tiếp trong console, log rõ nghĩa |
| 6 | **Native JSON serialization** | `JSON.stringify()` serialize object → string, `JSON.parse()` ngược lại |
| 7 | **DOM text content** | `.textContent`, `.innerText` — tương tác trực tiếp với DOM |

## ⚠️ Bẫy thường gặp & Hạn chế

| # | Bẫy | Ví dụ | Cách tránh |
|---|-----|-------|-----------|
| 1 | **Bất biến — method không sửa gốc** | `"abc".toUpperCase()` → `"ABC"`, `"abc"` vẫn nguyên | Hiểu rằng mọi string method trả về string MỚI |
| 2 | **`replace('a','b')` chỉ thay kết quả đầu** | `"aaa".replace('a','b')` → `"baa"`, không phải `"bbb"` | Dùng regex `/a/g` với cờ `g` để thay tất cả |
| 3 | **`search` không hỗ trợ start position** | `str.search('x', 5)` — tham số thứ 2 bị ignore | Dùng `str.indexOf('x', 5)` nếu cần start position |
| 4 | **`new String()` tạo object** | `typeof new String('x')` → `"object"` | Dùng `String(x)` thay `new String(x)` |
| 5 | **So sánh & tìm kiếm phân biệt hoa/thường** | `"abc".includes("ABC")` → `false` | Dùng `.toLowerCase()` trước khi so sánh |
| 6 | **Emoji length ≠ visual length** | `"😀".length` → `2` (surrogate pair) | Dùng `[...str].length` hoặc `Array.from(str).length` |
| 7 | **`slice` vs `substring` khác âm index** | `"-1"`: `slice(-1)` = last char, `substring(-1)` = same as `substring(0)` | Dùng `slice` cho flexibility, nhớ `substring` không support âm |

## 💡 Khi nào dùng — Tình huống thực tế

1. **Hiển thị/chèn dữ liệu động vào giao diện** — `` `Chào ${name}` `` template string.
2. **Xử lý form input** — `trim()` đầu vào, `includes('@')` validate email sơ bộ.
3. **Tách/ghép văn bản** — `split(',')` đọc CSV, `join(' - ')` ghép lại.
4. **Kiểm tra từ khóa/tìm kiếm** — `indexOf`/`includes` trong tìm kiếm text.
5. **Làm sạch dữ liệu từ API** — `replace(/ +/g, ' ')` chuẩn hóa khoảng trắng, `toLowerCase()` normalize.
6. **Format số tiền/ngày** — `toFixed(2)` cho giá tiền, `padStart(2, '0')` cho ngày/tháng.
7. **Trích xuất thông tin từ chuỗi** — `match(regex)`, `slice` cắt lấy phần cần.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Các phương thức cơ bản

```js
var myString = 'Hoc JS tai JS F8 JS!';

console.log(myString.length);           // 20 — độ dài
console.log(myString.indexOf('JS'));    // 4  — vị trí đầu tiên
console.log(myString.lastIndexOf('JS')); // 17 — vị trí cuối cùng
console.log(myString.slice(4, 6));      // "JS" — cắt từ index 4 đến 5
console.log(myString.slice(-6, -4));    // "F8" — index âm tính từ cuối
console.log(myString.replace('JS', 'Javascript'));  // thay 1 chỗ đầu: "Hoc Javascript tai JS F8 JS!"
console.log(myString.replace(/JS/g, 'Javascript')); // thay TẤT CẢ: "Hoc Javascript tai Javascript F8 Javascript!"

var language = 'PHP, JS, CSS, HTML';
console.log(language.split(','));       // ['PHP', ' JS', ' CSS', ' HTML'] — mảng 4 phần tử
console.log('Javascript'.split(''));    // ['J','a','v','a','s','c','r','i','p','t'] — mảng ký tự
```

### Ví dụ 2: Template string — chèn biến và expression

```js
var ten = 'Sơn';
var tuoi = 23;
var khoahoc = 'JavaScript';

// Cú pháp cơ bản
var greeting = `Xin chào, tôi là ${ten}, ${tuoi} tuổi, học ${khoahoc}.`;
console.log(greeting);
// "Xin chào, tôi là Sơn, 23 tuổi, học JavaScript."

// Expression phức tạp trong template
var result = `Tổng: ${1 + 2 + 3} | Trung bình: ${((1 + 2 + 3) / 3).toFixed(2)}`;
console.log(result);
// "Tổng: 6 | Trung bình: 2.00"

// Multi-line HTML generation
var cardHTML = `
  <div class="card">
    <h2>${ten}</h2>
    <p>Tuổi: ${tuoi}</p>
    <span>Khoa: ${khoahoc}</span>
  </div>
`;
console.log(cardHTML);
```

### Ví dụ 3: Tìm kiếm và thay thế

```js
var text = 'JavaScript là ngôn ngữ thú vị. Học JavaScript rất vui!';

// indexOf — vị trí đầu tiên
console.log(text.indexOf('ngôn ngữ'));   // 11
console.log(text.indexOf('Python'));     // -1 (không tìm thấy)

// lastIndexOf — vị trí cuối cùng
console.log(text.lastIndexOf('JavaScript')); // 31

// includes — kiểm tra tồn tại (ES2015)
console.log(text.includes('thú vị'));    // true
console.log(text.includes('Python'));    // false

// search — regex
console.log(text.search(/ngôn\s+ngữ/)); // 11

// replace — thay 1 lần
console.log(text.replace('JavaScript', 'TypeScript'));
// "TypeScript là ngôn ngữ thú vị. Học JavaScript rất vui!"

// replaceAll — thay tất cả (ES2021)
console.log(text.replaceAll('JavaScript', 'TypeScript'));
// "TypeScript là ngôn ngữ thú vị. Học TypeScript rất vui!"

// replace với regex + flag g
console.log(text.replace(/JavaScript/g, 'TypeScript'));
// "TypeScript là ngôn ngữ thú vị. Học TypeScript rất vui!"
```

### Ví dụ 4: Cắt và tách chuỗi

```js
var url = 'https://example.com/path/page.html';

// slice — cắt (hỗ trợ index âm)
console.log(url.slice(8));           // "example.com/path/page.html" — từ index 8 đến cuối
console.log(url.slice(-5));          // ".html" — 5 ký tự cuối
console.log(url.slice(8, 19));       // "example.com"

// substring — tương tự slice nhưng không hỗ trợ index âm
console.log(url.substring(8, 19));   // "example.com"

// split — tách thành mảng
var parts = url.split('/');
console.log(parts);  // ['https:', '', 'example.com', 'path', 'page.html']

var csv = 'Sơn,23,JavaScript';
var [name, age, subject] = csv.split(',');
console.log(name, age, subject);  // "Sơn" "23" "JavaScript"
```

### Ví dụ 5: Chuẩn hóa và format

```js
var rawInput = '  Hello   World  ';

// trim — bỏ khoảng trắng hai đầu
console.log(rawInput.trim());        // "Hello   World"

// normalize khoảng trắng thừa
var normalized = rawInput.trim().replace(/\s+/g, ' ');
console.log(normalized);             // "Hello World"

// toLowerCase / toUpperCase
console.log('JavaScript'.toLowerCase()); // "javascript"
console.log('JavaScript'.toUpperCase()); // "JAVASCRIPT"

// padStart / padEnd — format số, ngày
console.log(String(5).padStart(2, '0'));   // "05"
console.log(String(42).padStart(5, '0'));  // "00042"
console.log('abc'.padEnd(5, '-'));         // "abc--"

// repeat
console.log('=-'.repeat(5));               // "=-=-=-=-="
```

### Ví dụ 6: Kiểm tra chuỗi — startsWith, endsWith, includes

```js
var email = 'user@example.com';
var filename = 'report.pdf';

// startsWith — kiểm tra prefix
console.log(email.startsWith('user'));     // true
console.log(email.startsWith('@'));        // false

// endsWith — kiểm tra suffix (phổ biến validate file extension)
console.log(filename.endsWith('.pdf'));    // true
console.log(filename.endsWith('.doc'));    // false

// includes — kiểm tra containment
console.log(email.includes('@'));          // true
console.log(email.includes('gmail'));      // false

// Kết hợp validate email đơn giản
function isValidEmail(email) {
  return email.includes('@') &&
         email.startsWith('user') &&
         email.endsWith('.com');
}
console.log(isValidEmail('user@example.com')); // true
```

## 🔬 So sánh với alternatives

| Phương án | Ưu điểm | Nhược điểm | Phù hợp khi |
|-----------|---------|------------|-------------|
| **Native string methods** | Built-in, fast, no dependency | Limited regex power | Thao tác cơ bản: trim, split, replace |
| **Regex (`match`, `test`)** | Powerful pattern matching | Cú pháp khó đọc, khó viết đúng | Validate complex format (email, phone) |
| **Intl API (`Intl.DateTimeFormat`)** | Locale-aware formatting | More verbose | Format ngày/giờ theo locale |
| **Library (Lodash `_.truncate`, `_.chars`)** | Consistent API, edge cases handled | Extra dependency | Large projects with many string ops |
| **Template literals (ES6)** | Clean interpolation, multi-line | Slightly more memory than concat | Dynamic content generation |

## 📊 Performance & Best Practices

- **Dùng template literals** thay string concatenation `+` — clean hơn, ít bug quote nesting.
- **Dùng `includes`/`startsWith`/`endsWith`** thay `indexOf > -1` — readable hơn, intent clear.
- **Dùng regex `/g` flag** khi cần thay thế TẤT CẢ — `replace('a','b')` chỉ thay lần đầu.
- **Dùng `replaceAll` (ES2021)** thay regex `/g` cho simple string replacement — cleaner syntax.
- **Dùng `trim()` trước khi validate** — loại bỏ whitespace ẩn từ user input.
- **Dùng `[...str].length`** thay `str.length` khi cần đếm đúng Unicode code points (emoji).
- **Tránh `new String()`** — luôn dùng literal hoặc `String()` function.
- **Cache kết quả `split`/`replace`** nếu dùng nhiều lần — string immutable, gọi lại tốn CPU.

## 🔗 Liên kết chéo

- Xem thêm: `02_data-types/01_primitive-types/` — overview 7 primitive types
- Xem thêm: `02_data-types/01_primitive-types/03_value-vs-reference/` — string là primitive, copy by value
- Xem thêm: `02_data-types/03_type-casting-and-coercion/03_implicit/` — string coercion trong arithmetic
- Xem thêm: `02_data-types/04_builtin-objects/03_regexp/` — regex pattern matching nâng cao
- Xem thêm: `08_expressions-and-operators/06_string-operators/` — string operators chi tiết
- Tài liệu: [MDN — String](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String), [javascript.info/string](https://javascript.info/string)
