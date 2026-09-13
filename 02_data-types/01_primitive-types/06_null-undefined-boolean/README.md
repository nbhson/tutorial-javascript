# null / undefined / boolean

## 🔑 Khái niệm

Ba kiểu nguyên thủy này có vẻ "nhỏ" nhưng gây nhiều nhầm lẫn nhất. Cần phân biệt rõ:

**1. `undefined`** — giá trị do **engine tự đặt** khi biến được khai báo nhưng **chưa gán giá trị**, hoặc khi truy cập thuộc tính không tồn tại, phần tử mảng bỏ trống, hàm không trả gì:

```js
let x;            // x === undefined, typeof x === "undefined"
function f() {}   // f() === undefined
const o = {};     // o.ten === undefined
```

**2. `null`** — giá trị do **lập trình viên cố ý đặt** để biểu diễn trạng thái "rỗng/có chủ đích", ví dụ "chưa có dữ liệu nào":

```js
const user = null;   // rõ ràng: chưa có user nào
```

> ⚠️ **Bug lịch sử:** `typeof null` trả `"object"` (engine tạo từ năm đầu, không sửa được vì sẽ phá hàng tỉ trang web). Trên thực tế `null` KHÔNG phải object — nó là primitive.

**So sánh null/undefined:**

```js
null == undefined;   // true  (loose: "" tương đương trong so sánh thả")
null === undefined;  // false (strict: khác kiểu)
```

**3. `boolean`** — chỉ có `true` / `false`, thường là kết quả của biểu thức so sánh (`5 > 3`). Có thể chuyển đổi bằng `Boolean(value)` hoặc toán tử `!!`:

```js
Boolean(0);     // false
Boolean("");    // false
Boolean(null);  // false
Boolean([]);    // true  — mảng rỗng vẫn "truthy"!
Boolean({});    // true  — object rỗng cũng "truthy"!
```

**Truthy / Falsy (giá trị bị "coi là sai"):**

| Falsy (đúng 6 giá trị) | Truthy |
|---|---|
| `false` | mọi `number` khác 0, kể cả `Infinity`, và cả `-0` trần ... |
| `0`, `-0`, `0n`, `NaN` | `"0"`, `"false"`, `" "` (chứa ký tự) |
| `""` (chuỗi rỗng) | `[]`, `{}`, `function(){}` |
| `null`, `undefined` | `Symbol()`, `new Date()` |

## ✅ Điểm mạnh

- Phân biệt rõ hai trạng thái "không có" → tránh hàng loạt bug hiển thị/phí đối.
- Quy tắc 6 falsy chỉ cần nhớ một lần, dùng mọi nơi (điều kiện, validation).
- Booleans/`!` có thể "đánh giá" giá trị bất kỳ thành true/false nhanh.
- `Boolean()` chuyển đổi tường minh giúp code dễ đọc (tránh coercion ngầm).

## ⚠️ Lưu ý / Hạn chế

- `typeof null === "object"` — bug lịch sử, đừng dùng để nhận biết kiểu null; thay bằng `=== null`.
- `null == undefined` → `true`, `null === undefined` → `false` — thường nhầm ít chú ý.
- `Boolean([])` và `Boolean({})` đều là **`true`** — bẫy kinh điển khi kiểm tra mảng rỗng cách sai.
- Trong JSON: `null` tồn tại, còn `undefined` bị "mất" khi serialize (thành thuộc tính bị bỏ).

## 💡 Khi nào dùng

- Kiểm tra biến có tồn tại/đã gán: `value !== undefined && value !== null` hoặc `value != null`.
- Trả về "không có kết quả" từ hàm: `null` (có chủ đích) thay vì để lẫn lộn.
- Điều kiện đúng/sai khi validation: `if (email)`.
- Ép sang boolean tường minh: `Boolean(input.includes("@")))`.

## 🎯 Ví dụ minh họa

```js
console.log(typeof null); // "object" (bug lịch sử!)
console.log(null == undefined);  // true
console.log(null === undefined); // false

let x;
console.log(x, typeof x); // undefined "undefined"

console.log(Boolean(0));     // false
console.log(Boolean(""));    // false
console.log(Boolean(null));  // false
console.log(Boolean([]));    // true
console.log(Boolean({}));    // true
```

## 📚 Tham khảo / Bài tập

- Chạy `app.js` trong thư mục (`node app.js` hoặc mở `index.html`): in ra `typeof null`, `null == undefined`, `null === undefined`, biến chưa gán, và `Boolean` của một loạt giá trị.
- Tự thử: 1) kiểm tra `Boolean("0")`, `Boolean(-0)`, `Boolean(" " )` rồi đoán trước khi chạy; 2) viết hàm `isEmptyArray(arr)` dùng đúng cách: `Array.isArray(arr) && arr.length === 0`; 3) dùng `value != null` (vừa bắt cả `null` lẫn `undefined`) ở một điều kiện thật.
- Tài liệu: [MDN — null](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/null), [MDN — Truthy](https://developer.mozilla.org/en-US/docs/Glossary/Truthy).