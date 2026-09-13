# Template String (Template Literals)

## 🔑 Khái niệm

Template literal dùng **backtick** `` `...` `` thay single/double quotes. Ra mắt ES2015 (ES6).

2 tính năng chính:
1. **Interpolation**: `` `Hello ${name}` `` — nhúng expression bất kỳ
2. **Multi-line**: xuống dòng thực tế trong string, không cần `\n`

**String.raw**: giữ nguyên escape sequences — `` String.raw`C:\Users\name` `` → `"C:\Users\name"`

## ✅ Điểm mạnh

| Ưu điểm | Mô tả |
|---|---|
| Multi-line tự nhiên | Giữ nguyên cấu trúc HTML/CSS/SQL |
| Expression inline | `` `${a + b * 2}` `` evaluate trực tiếp |
| Không cần `+` nối | Giảm lỗi `" + " ` và space thừa |
| String.raw | Giữ nguyên backslash cho paths |
| Readable format | Code trông như output cuối cùng |

## ⚠️ Bẫy thường gặp

### Bẫy 1: Backtick trong template
```js
const msg = `Anh ấy nói \`hello\` với tôi`; // escape backtick
const bad = `Anh ấy nói `hello` với tôi`;   // SyntaxError!
```

### Bẫy 2: Nested template priority
```js
const outer = `a is ${`b is ${2 + 2}`}`;
// inner ${} evaluated first: "b is 4"
// outer: "a is b is 4"
```

### Bẫy 3: Tagged template performance
```js
// Tagged template ~10x chậm hơn plain literal
// Không dùng trong tight loop hoặc hot path
for (let i = 0; i < 1000000; i++) {
  tag`hello ${i}`; // đáng ngại performance
}
```

## 💡 Khi nào dùng

- HTML/CSS/SQL template string (giữ cấu trúc)
- Log message format phức tạp
- Internationalization (i18n) string builder
- DSL qua tagged template

## 🎯 Ví dụ

```js
const name = "Nguyễn Văn A";
const age = 25;

// Interpolation cơ bản
console.log(`Tên: ${name}, Tuổi: ${age}`);
// "Tên: Nguyễn Văn A, Tuổi: 25"

// Multi-line HTML
const card = `
  <div class="card">
    <h2>${title}</h2>
    <p>${description}</p>
    <button>Xem thêm</button>
  </div>
`;

// Math expression
const a = 10, b = 5;
console.log(`${a} + ${b} = ${a + b}`);  // "10 + 5 = 15"
console.log(`${a} × ${b} = ${a * b}`);  // "10 × 5 = 50"

// String.raw
console.log(`C:\\Users\\name`);         // "C:\Users\name"
console.log(String.raw`C:\Users\name`);   // "C:\Users\name" (giữ nguyên)

// SQL query
const query = `SELECT * FROM users WHERE name = '${name}' AND age > ${age}`;
```

## 🔗 Liên kết chéo
- Xem: `20_modern-javascript/01_template-literals/02_tagged-templates`
- Xem: `02_data-types/01_primitive-types/01_string`
