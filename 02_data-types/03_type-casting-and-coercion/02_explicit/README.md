# Explicit Type Casting (Ép kiểu tường minh)

## 🔑 Khái niệm

**Explicit type casting** là việc lập trình viên **chủ động** chuyển một giá trị từ kiểu này sang kiểu khác bằng các hàm quy đổi chuẩn của JavaScript. Đây là cách được khuyến nghị nhất vì **code tự mô tả ý định** và không phụ thuộc quy tắc ngầm của engine.

**Bộ 6 hàm quy đổi chính:**

| Hàm | Ví dụ | Kết quả | Ghi chú |
|---|---|---|---|
| `String(x)` | `String(123)` | `"123"` | `String(null)` → `"null"` |
| `Number(x)` | `Number("42")` | `42` | `Number("  ")` → `0`; `Number("abc")` → `NaN` |
| `Boolean(x)` | `Boolean(0)` | `false` | `Boolean([])` → `true` |
| `BigInt(x)` | `BigInt("123")` | `123n` | số nguyên lớn |
| `Symbol(x)` | `Symbol("id")` | `Symbol(id)` | giá trị duy nhất |
| `parseInt/parseFloat` | `parseInt("12px")` | `12` | đọc số từ đầu chuỗi |

**Các trường hợp "kỳ lạ" bạn phải nhớ:**

```js
Number("42");      // 42
Number("  ");      // 0     ← chuỗi toàn khoảng trắng → 0
Number("abc");     // NaN   ← không phải số → NaN
Number(true);      // 1     ← boolean → 1/0
String(null);      // "null"
String(undefined); // "undefined"
Boolean(0);        // false
Boolean("");       // false
Boolean([]);       // true  ← mảng rỗng vẫn truthy!
```

**Kiểm tra kiểu sau khi ép:**

```js
typeof String(1);  // "string"
typeof Number("1");// "number"
```

## ✅ Điểm mạnh

- Code rõ ràng, tự giải thích — người đọc biết ngay dòng này đang đổi kiểu.
- Không phụ thuộc quy tắc implicit → kết quả đoán trước được 100%.
- `parseInt("12px")` thực dụng khi xử lý CSS value có đơn vị.
- An toàn hơn nhiều so với coercion khi làm việc với dữ liệu ngoài (form, API).

## ⚠️ Lưu ý / Hạn chế

- `Number("abc")` → `NaN` (không lỗi!) — đừng tin rằng "ép số" luôn thành công.
- `Number("  ")` → `0` cũng gây nhầm lẫn khi xử lý input rỗng — thường phải kiểm tra `trim()` trước.
- `Boolean([])`/`Boolean({})` là `true` — bẫy khi kiểm tra "mảng rỗng".
- `parseInt` khác `Number`: `parseInt("12px")` → `12`, nhưng `Number("12px")` → `NaN`.

## 💡 Khi nào dùng

- Chuyển input form (luôn là string) sang số để tính toán: `Number(input.value)`.
- Hiển thị giá trị động vào chuỗi: `String(id)`.
- Chuẩn hóa dữ liệu đầu vào trước khi validate/so sánh.
- Đọc thuộc tính CSS: `parseInt(style.width)` bỏ đơn vị `px`.

## 🎯 Ví dụ minh họa

```js
console.log(String(123), String(null), String(undefined));
// "123" "null" "undefined"

console.log(Number("42"), Number("  "), Number("abc"), Number(true));
// 42 0 NaN 1

console.log(Boolean(0), Boolean(""), Boolean([]));
// false false true

console.log(BigInt("123"));       // 123n
console.log(typeof String(1), typeof Number("1"));
// string number
```

## 📚 Tham khảo / Bài tập

- Chạy `app.js` trong thư mục (`node app.js` hoặc mở `index.html`): in ra các kết quả trên — đặc biệt `Number("  ")` → `0` và `Number("abc")` → `NaN`.
- Tự thử: 1) đoán rồi chạy `Number("12px")` so với `parseInt("12px")`; 2) viết hàm `parseAge(input)` trả về số, nếu không hợp lệ trả về `null` — dùng `Number` + kiểm tra `isNaN`; 3) ép `Symbol()` và `Symbol("id")` xem kết quả có phải unique.
- Tài liệu: [MDN — Number()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/Number), [javascript.info/type-conversions](https://javascript.info/type-conversions).