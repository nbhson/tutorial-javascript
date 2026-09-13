# Template String (Template Literals)

## 🔑 Khái niệm

Template literal dùng **backtick** `` `...` `` thay cho single/double quotes `'...'` / `"..."`. Ra mắt trong **ES2015 (ES6)**.

2 tính năng chính:
1. **Interpolation**: `` `Hello ${name}` `` — nhúng expression bất kỳ
2. **Multi-line**: xuống dòng thực tế trong string, không cần `\n`

**Tagged template**: `` tag`hello ${name}` `` — gọi function `tag(strings, ...values)` để custom xử lý.

## ✅ Điểm mạnh
- Đọc/giữ nguyên cấu trúc multi-line (CSS, SQL, HTML template)
- Không cần `+` nối string — giảm lỗi `" + " `
- Expression evaluation toàn diện: `\` \${a + b * 2}\` `
- `String.raw` giữ escape sequence nguyên bản

## ⚠️ Lưu ý
- Backtick trong template phải escape: `` \` `` hoặc `` \${'\`'} ``
- `` `${}` `` phức tạp (nested template) cần lưu ý priority operator
- Tagged template function phải định nghĩa sẵn — `` tag \`...\` `` không tự động hoạt động nếu không có tag
- Performance: tagged template chậm hơn literal thường (~10x) — không dùng trong loop tight

## 💡 Khi nào dùng
- HTML/CSS/SQL template string
- Log message format phức tạp
- Internationalization (i18n) string builder
- DSL (Domain-Specific Language) qua tagged template

## 🎯 Ví dụ minh họa

### Interpolation cơ bản
```js
const name = "Nguyễn Văn A";
const age = 25;
console.log(`Tên: ${name}, Tuổi: ${age}`);
// "Tên: Nguyễn Văn A, Tuổi: 25"
```

### Multi-line string
```js
const html = `
  <div class="card">
    <h2>${title}</h2>
    <p>${description}</p>
    <button>Xem thêm</button>
  </div>
`;
```

### Math expression trong interpolation
```js
const a = 10, b = 5;
console.log(`${a} + ${b} = ${a + b}`);  // "10 + 5 = 15"
console.log(`${a} × ${b} = ${a * b}`);  // "10 × 5 = 50"
```

### String.raw — giữ escape
```js
console.log(`C:\\Users\\name`);          // "C:\Users\name"
console.log(String.raw`C:\Users\name`);   // "C:\Users\name" (giữ nguyên)
```

### Tagged template cơ bản
```js
function highlight(strings, ...values) {
  return strings[0] + 
    values.map(v => `<mark>${v}</mark>`).join("") + 
    strings[strings.length - 1];
}

const result = highlight`Hello ${"World"}, welcome to ${"JavaScript"}!`;
// "<mark>Hello </mark>World<mark>, welcome to </mark>JavaScript<mark>!</mark>"
```

## 📚 Tham khảo & Bài tập
- File: `app.js`, `index.html` trong folder `01_template-string/`
- Thực hành: viết function `sql` tag cho SQL query builder
- Câu hỏi: tagged template function nhận bao nhiêu arguments? Argument đầu là gì?
