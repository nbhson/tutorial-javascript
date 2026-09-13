# 02. Kiểu dữ liệu (Data Types)

## 🔑 Khái niệm

Mọi giá trị trong JavaScript đều thuộc một trong **8 kiểu dữ liệu**. Chúng được chia làm hai nhóm lớn:

**Kiểu nguyên thủy (primitive types):**

| Kiểu | Ví dụ | Ghi chú |
|---|---|---|
| `string` | `"Xin chào"` | chuỗi ký tự (bất biến) |
| `number` | `3.14`, `NaN`, `Infinity` | số dấu phẩy động chuẩn IEEE-754 |
| `bigint` | `9007199254740993n` | số nguyên vượt giới hạn an toàn |
| `boolean` | `true`, `false` | đúng/sai |
| `undefined` | `let x; x === undefined` | chưa được gán giá trị |
| `symbol` | `Symbol("id")` | giá trị duy nhất, dùng làm key |
| `null` | `null` | cố ý "rỗng" (typeof trả `"object"` — bug lịch sử) |

**Kiểu tham chiếu (reference types):**

- `object` — và các biến thể: `array` (mảng — cũng là object), `function` (hàm — cũng là object), Date, RegExp, Map, Set...

**Hai quy luật nền tảng:** (1) primitive so sánh và được gán **theo giá trị** (value), object theo **tham chiếu** (reference); (2) JavaScript có khả năng **ép kiểu (coercion)** — tự chuyển đổi kiểu khi cần (`"1" + 1` → `"11"`). Bốn khối con của nhóm này giúp bạn nắm chắc: primitive types, object & prototype, ép kiểu, và các built-in object (Math, Date, RegExp, Error).

## ✅ Điểm mạnh

- Nắm được 7 primitive + object → đọc `typeof` đúng, hiểu mọi giá trị trong JS.
- Hiểu tham trị/tham chiếu → tránh vô số bug clone/sửa dữ liệu.
- Hiểu ép kiểu → đoán chính xác kết quả của biểu thức như `"5" - 2`, `1 == "1"`.
- Biết sức mạnh của built-in objects → viết code ngắn, đúng chuẩn (không tự viết hàm thay cho `Math`, `Date`, `RegExp`).
- Nền tảng vững để học các chủ đề nâng cao (bất đồng bộ, class, module...) ở nhóm sau.

## ⚠️ Lưu ý / Hạn chế

- `typeof null === "object"` là **bug lịch sử** được giữ lại — hãy nhớ riêng trường hợp này.
- `number` không chính xác tuyệt đối với số thập phân: `0.1 + 0.2 !== 0.3`.
- Object (kể cả array, function) là tham chiếu — việc so sánh `===` hay gán biến phải cẩn thận.
- Ép kiểu ngầm định (implicit coercion) có nhiều bẫy; code production nên ép kiểu **tường minh** (explicit).

## 💡 Khi nào dùng

- Kiểm tra kiểu dữ liệu của biến → `typeof` / `Array.isArray` / `instanceof`.
- Tính toán số an toàn → `number`; số cực lớn (ID, timestamp nano) → `bigint`.
- Khóa duy nhất/hidden trong object → `symbol`.
- Biểu diễn "chưa có gì" → `undefined` (engine tự đặt) và `null` (lập trình viên đặt).
- Thao tác thời gian, số học, regex, báo lỗi → các built-in objects trong `04_builtin-objects/`.

## 🎯 Ví dụ minh họa

```js
// 8 kiểu dữ liệu
console.log(typeof "text");   // string
console.log(typeof 42);       // number
console.log(typeof 10n);      // bigint
console.log(typeof true);     // boolean
console.log(typeof undefined);// undefined
console.log(typeof null);     // object  ← bug lịch sử!
console.log(typeof Symbol()); // symbol
console.log(typeof {});       // object
console.log(typeof []);       // object  (array vẫn là object)
console.log(typeof function(){}); // function
```

## 📚 Tham khảo / Bài tập

- Nhóm này gồm 4 bài con: `01_primitive-types/`, `02_objects-and-prototype/`, `03_type-casting-and-coercion/`, `04_builtin-objects/`.
- Mỗi bài con đều có `app.js`/`*.js` để chạy thử — bắt đầu với `01_primitive-types/06_null-undefined-boolean/app.js` để thấy `typeof null` thực tế.
- Tự thử: chạy từng file JS bằng `node <file>` hoặc mở `index.html` tương ứng trong trình duyệt rồi quan sát Console.