# Implicit Type Coercion (Ép kiểu ngầm định)

## 🔑 Khái niệm

**Implicit coercion** xảy ra khi **engine tự ép kiểu** mà bạn không gõ bất kỳ hàm chuyển đổi nào. Nó được kích hoạt trong ba bối cảnh chính:

**1. Toán tử cộng `+`** — nếu có ít nhất một toán hạng là **string**, nó **nối chuỗi**; ngược lại cộng số:

```js
"5" + 3;   // "53"  (string thắng → nối chuỗi)
1 + true;  // 2     (true → 1, cộng số)
"a" + true; // "atrue" (có string → nối)
```

**2. Các toán tử số học `-`, `*`, `/`** — **luôn ép sang number**:

```js
"5" - 3;  // 2
"5" * 2;  // 10
```

**3. `==` (loose equality)** — nếu hai vế khác kiểu, engine ép kiểu trước khi so sánh (so với `===` không ép):

```js
null == undefined; // true
0 == false;        // true (false → 0)
"" == 0;           // true ("" → 0)
```

**4. Ngữ cảnh điều kiện (`if`, `&&`, `||`, `!`)** — mọi giá trị bị quy về boolean theo bảng truthy/falsy:

```js
if ("") console.log("không chạy"); // "" là falsy
```

**Bảng truthy/falsy (thuộc lòng để đọc coercion đúng):**

| Nhóm | Giá trị |
|---|---|
| **Falsy (đúng 8 giá trị)** | `false`, `0`, `-0`, `0n`, `""` (chuỗi rỗng), `null`, `undefined`, `NaN` |
| **Truthy (còn lại)** | mọi thứ khác: `[]`, `{}`, `"0"`, `"false"`, `Infinity`, `Symbol()`, `function(){}` |

> Hãy tự kiểm chứng: `Boolean("")` → `false`, `Boolean("0")` → `true`, `Boolean([])` → `true`, `Boolean({})` → `true`.

## ✅ Điểm mạnh

- Viết ngắn gọn: `if (username)` thay cho chuỗi kiểm tra dài lê thê.
- Tận dụng truthy/falsy kiểm tra nhanh "có giá trị hay không".
- Coercion số học giúp xử lý dữ liệu string-form một cách tiện lợi khi biết trước format.
- Hiểu rõ quy tắc → đọc được vô số code đời thực viết theo phong cách này.

## ⚠️ Lưu ý / Hạn chế

- Kết quả dễ gây sốc: `[] + []` → `""`, `{} + []` → `0`, `"9" > "10"` → `true` (so sánh chuỗi theo từng ký tự).
- `0 == false`, `"" == 0`, `null == undefined` đều `true` — ít người đoán chuẩn lần đầu.
- `NaN` không bằng chính nó: `NaN == NaN` → `false`.
- Trong production, ưu tiên `===` và ép kiểu tường minh để tránh phụ thuộc luật ngầm.

## 💡 Khi nào dùng

- Điều kiện nhanh theo độ "có dữ liệu": `if (data && data.length)`.
- Default value dựa trên truthy: `const name = user.name || "Khách"`.
- Cố tình so sánh có chủ đích: `== null` để bắt cả `null` lẫn `undefined` (thủ thuật hay).
- Khi logic muốn "number hoặc string đều OK".

## 🎯 Ví dụ minh họa

```js
console.log("5" + 3, "5" - 3, "5" * 2);   // "53" 2 10
console.log(Boolean(""), Boolean("0"), Boolean([]), Boolean({}));
// false true true true
console.log(null == undefined, 0 == false, "" == 0);
// true true true
console.log(1 + true, "a" + true);        // 2 "atrue"
if ("") console.log("truthy"); else console.log("falsy empty string");
// falsy empty string
```

## 📚 Tham khảo / Bài tập

- Chạy `app.js` trong thư mục (`node app.js` hoặc mở `index.html`): in ra các coercion đặc trưng `"5"+3`, `1+true`, `"a"+true`, các so sánh `==` và câu lệnh `if("")`.
- Tự thử: 1) kiểm tra `Boolean(0n)`, `Boolean(NaN)`, `Boolean(Symbol())` và thêm vào danh sách falsy/truthy; 2) giải thích `[] + []` và `[] + {}` dựa trên quy tắc (cả hai đưa về string rỗng/`[object Object]`); 3) viết hàm `isFalsy(value)` trả về `true` nếu Falsy.
- Tài liệu: [MDN — Type coercion](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators), [javascript.info/type-conversions](https://javascript.info/type-conversions).