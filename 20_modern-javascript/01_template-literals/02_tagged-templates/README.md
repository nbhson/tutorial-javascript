# Tagged Templates

## 🔑 Khái niệm

Tagged template là function được gọi tự động khi template literal có prefix là tên function:

```js
tag`hello ${name}`
```

Tương đương:
```js
tag(["hello ", ""], name)
```

Signature: `function tag(strings, ...values)`
- `strings`: mảng các phần text (đã split bởi `${}`)
- `...values`: các giá trị expression đã evaluate

## ✅ Điểm mạnh
- Tạo **DSL (Domain-Specific Language)**: SQL query, i18n, styled-components
- Escape tự động (tránh SQL injection, XSS)
- Custom formatting, validation trước khi render

## ⚠️ Lưu ý
- Phải định nghĩa function trước khi dùng
- Function phải xử lý `strings` — index 0 là text trước `${}` đầu, index cuối là text sau `${}` cuối
- Không dùng `raw` property trên strings array nếu cần escape sequences nguyên bản → dùng `String.raw`

## 💡 Khi nào dùng
- SQL query builder an toàn (escape values tự động)
- CSS-in-JS (styled-components, glamor)
- i18n translation với placeholder
- JSON path builder

## 🎯 Ví dụ minh họa

### SQL query builder
```js
function sql(strings, ...values) {
  const escaped = values.map(v => 
    typeof v === "string" ? `'${v.replace(/'/g, "''")}'` : v
  );
  return strings[0] + escaped.reduce((acc, v, i) => acc + v + strings[i + 1], "");
}

const name = "John O'Brien";
const query = sql`SELECT * FROM users WHERE name = ${name} AND age > ${25}`;
// "SELECT * FROM users WHERE name = 'John O''Brien' AND age > 25"
```

### CSS-in-JS đơn giản
```js
function css(strings, ...values) {
  let result = strings[0];
  values.forEach((v, i) => {
    result += v + strings[i + 1];
  });
  return result;
}

const theme = { color: "blue", size: "16px" };
const style = css`color: ${theme.color}; font-size: ${theme.size};`;
// "color: blue; font-size: 16px;"
```

### i18n đơn giản
```js
const messages = {
  greeting: ["Xin chào, ", "! Bạn có ", " tin nhắn mới."],
};

function i18n(key, ...values) {
  const parts = messages[key];
  return parts[0] + values.map((v, i) => v + parts[i + 1]).join("");
}

console.log(i18n("greeting", "Nguyễn", 3));
// "Xin chào, Nguyễn! Bạn có 3 tin nhắn mới."
```

## 📚 Tham khảo & Bài tập
- File: `app.js`, `index.html` trong folder `02_tagged-templates/`
- Thực hành: viết tag `json` parse JSON từ template literal
- Câu hỏi: tại sao `strings.raw` property lại quan trọng với SQL injection?
