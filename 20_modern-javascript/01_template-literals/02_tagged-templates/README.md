# Tagged Templates

## Khái niệm

Tagged template là function gọi tự động khi template literal có prefix:

```js
tag`hello ${name}`
// Tương đương: tag(["hello ", ""], name)
```

Signature: `function tag(strings, ...values)`
- `strings`: mảng text parts
- `...values`: các expression đã evaluate

## Điểm mạnh

- Tạo **DSL**: SQL, i18n, CSS-in-JS
- Escape tự động (tránh injection)
- Custom formatting/validation

## Bẫy thường gặp

- Phải định nghĩa function tag trước
- Index 0 là text trước `${}` đầu, index cuối là text sau `${}` cuối
- `strings.raw` giữ escape sequences nguyên bản

## Khi nào dùng

- SQL query builder an toàn
- CSS-in-JS (styled-components)
- i18n translation với placeholder

## Ví dụ

### SQL builder
```js
function sql(strings, ...values) {
  const escaped = values.map(v =>
    typeof v === "string" ? `'${v.replace(/'/g, "''")}'` : v
  );
  return strings[0] + escaped.reduce((acc, v, i) => acc + v + strings[i+1], "");
}

const query = sql`SELECT * FROM users WHERE name = ${name} AND age > ${25}`;
```

### i18n
```js
const messages = {
  greeting: ["Xin chào, ", "! Bạn có ", " tin nhắn."]
};
function i18n(key, ...vals) {
  const parts = messages[key];
  return parts[0] + vals.reduce((acc, v, i) => acc + v + parts[i+1], "");
}
console.log(i18n("greeting", "Nguyễn", 3));
// "Xin chào, Nguyễn! Bạn có 3 tin nhắn."
```

## Liên kết chéo

- Xem: `20_modern-javascript/01_template-literals/01_template-string`
