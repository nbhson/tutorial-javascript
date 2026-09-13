# Built-in: RegExp (Biểu thức chính quy) — [Level: Intermediate]

## 🔑 Khái niệm cốt lõi

**RegExp** (Regular Expression) là object đại diện cho **mẫu tìm kiếm trong chuỗi** theo quy tắc pattern matching. RegExp được dùng để **tìm kiếm, kiểm tra, thay thế** text theo quy luật — mạnh hơn nhiều so với string methods thủ công.

### Hai cách tạo RegExp

```js
// 1. Regex literal — khuyên dùng cho pattern tĩnh
const re = /ab+c/g;

// 2. Constructor — chỉ dùng khi pattern được build động từ string
const re2 = new RegExp("ab+c", "g");

// ⚠️ Khác nhau về escape: constructor cần double-escape vì string parser xử lý trước
const dynamicPattern = "hello";
const re3 = new RegExp(dynamicPattern + " world");   // "hello world"
const re4 = /hello world/;                            // tương đương
```

### Cấu trúc pattern cơ bản

| Syntax | Ý nghĩa | Ví dụ |
|--------|---------|-------|
| `abc` | literal characters | `/cat/` khớp "cat", "category" |
| `.` | bất kỳ ký tự nào (trừ newline) | `/a.c/` khớp "abc", "aXc" |
| `\d` | chữ số [0-9] | `/\d{3}/` khớp 3 chữ số |
| `\w` | word character [a-zA-Z0-9_] | `/\w+/` khớp word |
| `\s` | whitespace [ \t\n\r] | `/\s+/` khớp khoảng trắng liên tiếp |
| `*` | 0 hoặc nhiều | `/ab*c/` khớp "ac", "abc", "abbbc" |
| `+` | 1 hoặc nhiều | `/ab+c/` khớp "abc", "abbbc" nhưng không "ac" |
| `?` | 0 hoặc 1 | `/ab?c/` khớp "ac", "abc" |
| `[abc]` | một trong a, b, c | `/[aeiou]/` khớp nguyên âm |
| `[^abc]` | KHÔNG phải a, b, c | `/[^0-9]/` khớp ký tự không phải số |
| `^` | bắt đầu chuỗi | `/^Hello/` khớp string bắt đầu bằng "Hello" |
| `$` | kết thúc chuỗi | `/world$/` khớp string kết thúc bằng "world" |
| `(xyz)` | capture group | `/(ab)+/` khớp "ab", "abab" |
| `x\|y` | OR | `/cat\|dog/` khớp "cat" hoặc "dog" |
| `{n}` | đúng n lần | `/\d{3}/` khớp đúng 3 chữ số |
| `{n,m}` | từ n đến m lần | `/\d{2,4}/` khớp 2-4 chữ số |

### Cờ flags (tùy chọn)

| Cờ | Tên | Mục đích |
|----|-----|---------|
| `g` | global | Tìm TẤT CẢ match thay vì dừng ở lần đầu |
| `i` | ignore case | Không phân biệt hoa/thường |
| `m` | multiline | `^` và `$` khớp bắt đầu/kết thúc MỖI dòng |
| `s` | dotAll (ES2018) | `.` cũng khớp newline `\n` |
| `u` | unicode | Hỗ trợ Unicode đầy đủ (surrogate pairs) |
| `y` | sticky | Chỉ khớp tại vị trí `lastIndex` hiện tại |
| `d` | hasIndices (ES2022) | Kết quả match có property `indices` |

## 📐 Cấu trúc nhóm

```
02_data-types/04_builtin-objects/03_regexp/
├── README.md         ← bài này
├── app.js            ← demo test, match, replace
└── index.html
```

## ✅ Điểm mạnh — Tại sao nên dùng RegExp

| # | Điểm mạnh | Lý do |
|---|-----------|-------|
| 1 | **Validation cực nhanh** | Một regex thay hàng chục dòng if/else logic |
| 2 | **Engine tối ưu native** | V8 JIT-compile regex — nhanh hơn JS loop tay xử lý text |
| 3 | **Replace pattern-based** | `replace(/pattern/g, replacement)` gọn cho bulk transform |
| 4 | **Extract structured data** | Capture groups trích xuất thông tin có cấu trúc từ string |
| 5 | **Universal support** | Có trong mọi JavaScript runtime — không dependency |
| 6 | **Reusable pattern objects** | Compiler regex một lần, dùng nhiều lần — cache hiệu quả |

## ⚠️ Bẫy thường gặp & Hạn chế

| # | Bẫy | Ví dụ | Cách tránh |
|---|-----|-------|-----------|
| 1 | **`lastIndex` stateful với cờ `g`** | `re.test(str)` lần 1 = true, lần 2 = false nếu str cũ | Tạo regex mới mỗi lần hoặc `str.match(regex)` |
| 2 | **`match` không `g` → return detailed array** | `str.match(/(ab)+/)` → có thêm index, groups | Dùng `g` flag nếu muốn chỉ danh sách kết quả |
| 3 | **BREDO (ReDoS) — catastrophic backtracking** | `/(a+)+b/` với input "aaaaaaaaaaaaaaaaaaac" → hang | Tránh nested quantifiers, giới hạn độ dài input |
| 4 | **Constructor double-escape** | `new RegExp("\\d+")` cần 2 backslash; `/\\d+/` chỉ 1 | Ưu tiên regex literal cho static patterns |
| 5 | **`^`/`$` mặc định là toàn string, không phải line** | `^abc$` chỉ khớp toàn bộ string | Dùng cờ `m` cho multiline mode |
| 6 | **Regex escape khác string escape** | `/\\/ ` = escaped backslash, `new RegExp("\\\\")` cần 4 backslash | Thử tại regex101.com trước khi dùng |

```js
// Bẫy 1: lastIndex stateful
const re = /hello/g;
console.log(re.test("say hello"));   // true, lastIndex = 4
console.log(re.test("say hello"));   // false — từ vị trí 4 trở đi không có "hello"
console.log(re.lastIndex);           // 0 (reset sau match fail)

// Giải pháp: dùng str.match() thay vì re.test() lặp lại
console.log("say hello".match(/hello/g)); // ["hello"]

// Bẫy 3: ReDoS nguy hiểm
const bad = /(a+)+b/;
bad.test("a".repeat(30) + "b"); // có thể treo browser
```

## 💡 Khi nào dùng — Tình huống thực tế

1. **Validate email, phone, zip code** — regex chuẩn, tránh viết if/else dài.
2. **Tách token từ text** — `str.split(/\s+/)` chia theo whitespace, bỏ khoảng trắng thừa.
3. **Chuẩn hóa format** — `replace(/\s+/g, " ")`, `replace(/-/g, "")`.
4. **Trích xuất thông tin có cấu trúc** — ngày giờ, mã sản phẩm, URL parts.
5. **Censor/sanitize input** — thay thế từ cấm `replace(/badword/g, "***")`.
6. **Custom search with wildcards** — `*` → `.*`, exact match regex.
7. **Diff-style matching** — tìm string khác biệt trong log, git output.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Các method cơ bản

```js
const re = /ab+c/g;

console.log(re.test("abbbc"));          // true — có khớp không
console.log(re.lastIndex);              // 5 — vị trí kết thúc match cuối

console.log("abc".match(re));           // ["abc"] — mảng các match
console.log("abbbcabc".match(/ab+c/g)); // ["abbbc", "abc"] — all matches

// search — trả về index hoặc -1
console.log("Hello world".search(/world/));     // 6
console.log("Hello world".search(/xyz/));       // -1

// replace
console.log("a2 b4 c8".replace(/[a-z]/g, "X")); // "X2 X4 X8" — thay tất cả letter
console.log("Jan,Feb,Mar".replace(/,/g, "\n")); // đổi dấu phẩy thành newline
```

### Ví dụ 2: Capture groups — trích xuất có cấu trúc

```js
// Trích giờ/phút/giây từ định dạng HH:MM:SS
const timeStr = "14:30:05";
const m = timeStr.match(/(\d{2}):(\d{2}):(\d{2})/);
if (m) {
  console.log(m[0]);       // "14:30:05" — toàn bộ match
  console.log(m[1]);       // "14"   — group 1
  console.log(m[2]);       // "30"   — group 2
  console.log(m[3]);       // "05"   — group 3
}

// replace với backreference
const dateUS = "01/15/2024";
const dateVN = dateUS.replace(/(\d{2})\/(\d{2})\/(\d{4})/, "$3-$2-$1");
console.log(dateVN);        // "2024-15-01"

// Named capture groups (ES2018)
const logLine = "[2024-01-15 14:30] INFO: server started";
const logRe = /\[(?<date>\d{4}-\d{2}-\d{2}) (?<time>\d{2}:\d{2})\] (?<level>\w+): (?<msg>.+)/;
const parts = logLine.match(logRe);
console.log(parts.groups.date);   // "2024-01-15"
console.log(parts.groups.level);  // "INFO"
```

### Ví dụ 3: Validation — real-world patterns

```js
// Email Việt Nam (đơn giản)
function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email);
}
console.log(isValidEmail("nam@example.com"));    // true
console.log(isValidEmail("@invalid"));           // false

// Số điện thoại VN (0xxxxxxxxx, 10 ký tự, bắt đầu 03/05/07/08/09)
function isValidVNPhone(phone) {
  return /^0[35789]\d{8}$/.test(phone);
}
console.log(isValidVNPhone("0901234567"));       // true
console.log(isValidVNPhone("0123456789"));       // false — đầu số sai

// Mã bưu chính VN (6 chữ số)
function isValidPostcode(code) {
  return /^\d{6}$/.test(code);
}
console.log(isValidPostcode("700000"));          // true
```

### Ví dụ 4: Text processing patterns

```js
// Chuẩn hóa nhiều khoảng trắng thành một
const messy = "Lỗi     cách      chữ";
console.log(messy.replace(/\s+/g, " "));       // "Lỗi cách chữ"

// Bỏ tag HTML (cơ bản — không an toàn cho HTML phức tạp)
const html = "<p>Xin <b>chào</b></p>";
console.log(html.replace(/<[^>]+>/g, ""));     // "Xin chào"

// Trích URL từ text
const text = "Visit https://example.com for more info.";
console.log(text.match(/https?:\/\/[^\s]+/g));  // ["https://example.com"]

// Tách CSV — chú ý field có dấu phẩy trong ngoặc kép
const csv = 'name,age,"Smith, John",city';
// split đơn giản (chưa handle quoted fields)
console.log(csv.split(","));                    // ["name","age","\"Smith"," John\"","city"]
```

### Ví dụ 5: Performance — compile once, reuse many

```js
// ❌ Lạm dụng: compiler mỗi lần gọi
function checkEmailBad(str) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(str);
}
checkEmailBad("a@b.c"); // compile regex mới mỗi lần!

// ✅ Hiệu quả: compiler 1 lần, lưu cache
const emailRe = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
function checkEmailGood(str) {
  return emailRe.test(str);
}
checkEmailGood("a@b.c"); // regex đã compile, chỉ chạy match
```

### Ví dụ 6: Regex flags — khi nào dùng cái nào

```js
const poem = "Hello\nWorld\nhello\nWORLD";

// i — ignore case
console.log(/hello/.test(poem));           // false (vì "Hello" viết hoa H)
console.log(/hello/i.test(poem));          // true
console.log(poem.match(/hello/gi));        // ["Hello", "hello"]

// m — multiline: ^ và $ khớp từng dòng
console.log(/^Hello/.test(poem));          // true
console.log(/^hello/m.test(poem));         // false
console.log(/^hello/mi.test(poem));        // true (cả Hello và hello)
console.log(poem.match(/^wo/iim));         // ["World", "hello"] — per-line match

// y — sticky: chỉ khớp tại lastIndex
const stickyRe = /abc/y;
console.log(stickyRe.test("xabc"));        // false (bắt đầu tại index 0, không có abc)
stickyRe.lastIndex = 1;
console.log(stickyRe.test("xabc"));        // true (bắt đầu tại index 1)
```

## 🔬 So sánh với alternatives

| Phương án | Ưu điểm | Nhược điểm | Phù hợp khi |
|-----------|---------|------------|-------------|
| **Native RegExp** | Fast, built-in, zero dependency | Cú pháp khó đọc/write đúng | Validation, simple extraction |
| **String methods** (`includes`, `indexOf`) | Simple, readable | No pattern matching | Exact substring check |
| **Validator.js** | Well-tested, many formats | Extra dependency (~70KB) | Project cần nhiều format validation |
| **Joi/Yup** | Declarative schema, composable | Overhead for simple check | Form validation in app |
| **Templating engine** | Regex-free pattern | Different skill set | Template substitution |

## 📊 Performance & Best Practices

- **Compile regex một lần** — đặt ngoài function loop để tránh recreate mỗi lần gọi.
- **Dùng `str.match(regex)` thay `regex.test(str)` lặp lại** — tránh `lastIndex` state bug.
- **Anchor pattern khi validate full string** — `^...$` để tránh partial match.
- **Tránh nested quantifiers** — `/(a+)+/` gây catastrophic backtracking (ReDoS).
- **Dùng non-capturing group `(?:...)`** khi không cần extract — nhanh hơn, ít memory.
- **Test trên regex101.com** — visual debug pattern trước khi đưa vào code.
- **ESLint `no-useless-escape`** — phát hiện escape không cần thiết trong regex literal.
- **Limit input length** trước khi regex match — phòng ReDoS attack trên user input.

## 🔗 Liên kết chéo

- Xem thêm: `02_data-types/04_builtin-objects/` — overview built-in objects
- Xem thêm: `02_data-types/01_primitive-types/01_string/` — string methods có regex params
- Xem thêm: `08_expressions-and-operators/01_operators/` — string operators
- Tài liệu: [MDN — RegExp](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/RegExp), [regex101.com](https://regex101.com)
