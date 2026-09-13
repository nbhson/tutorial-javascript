# Type Casting & Coercion (Ép kiểu tường minh và ngầm định)

## 🔑 Khái niệm

JavaScript là ngôn ngữ **kiểu động (dynamic typing)** — kiểu của biến được xác định tại runtime, và cùng một biến có thể đổi kiểu. Hệ quả tất yếu: JavaScript **tự động chuyển đổi kiểu dữ liệu** khi cần, gọi chung là **type conversion**. Có hai "hình thức":

1. **Conversion (explicit — tường minh):** lập trình viên **chủ động** gọi `String()`, `Number()`, `Boolean()`... để quy đổi kiểu:
   ```js
   String(123);  // "123"
   Number("42"); // 42
   Boolean(0);   // false
   ```

2. **Coercion (implicit — ngầm định):** **engine tự ép kiểu** trong các phép toán/bối cảnh mà không ai chủ động chuyển:
   ```js
   "5" + 3;         // "53"  — ưu tiên nối chuỗi
   "5" - 3;         // 2     — ưu tiên số học
   null == undefined; // true — loose equality tự "thả"
   if ("") { /* falsy */ }
   ```

**Tại sao phải nắm vững?** `"5" + 3` cho `"53"` còn `"5" - 3` cho `2` — cùng toán hạng, kết quả khác hoàn toàn tùy theo toán tử. Nắm vững quy tắc này tránh vô số bug "khó hiểu" nhất của JavaScript.

**General về truthy/falsy (dùng trong `if`, `&&`, `||`, `!`):**
- **Falsy (đúng 7 giá trị):** `false`, `0`, `-0`, `0n`, `""`, `null`, `undefined`, `NaN` → xem bài con `03_implicit` để nắm đủ.
- **Truthy:** mọi thứ còn lại (kể cả `[]`, `{}`, `"0"`, `"false"`, `Infinity`).

## ✅ Điểm mạnh

- Code gọn, linh hoạt: không cần khai báo kiểu, dữ liệu "tự thích nghi".
- Coercion đôi lúc rất tiện (nối chuỗi với số, kiểm tra truthy/falsy nhanh).
- Triết lý "duck typing" — chỉ cần đối tượng "đi như vịt, kêu như vịt" thì dùng được.
- Rapid prototyping nhanh vì không bị ràng buộc kiểu ở giai đoạn đầu.

## ⚠️ Lưu ý / Hạn chế

- Ép kiểu ngầm dễ gây bug: `[] + []` → `""`, `{} + []` → `0`, `"9" > "10"` → `true` (so sánh chuỗi theo ký tự đầu!).
- Production nên **ưu tiên explicit**: `Number(value)` thay vì đinh ninh `+value` luôn đúng ý bạn.
- `Number("abc")` → `NaN`, `Number("  ")` → `0` — kết quả "buồn cười" của quy tắc whitespace.
- `null == undefined` là `true` nhưng `null === undefined` là `false`.
- Dùng `==` (loose) dễ rơi vào bộ quy tắc coercion phức tạp — nên dùng `===` (xem `04_equality-comparisons`).

## 💡 Khi nào dùng

- Đọc input từ form/API (luôn là string) và cần tính toán → `Number(...)`.
- Gửi dữ liệu lên server → chuyển object về chuỗi JSON, số về string.
- Kiểm tra một giá trị "có đáng tin" hay không → rely truthy/falsy trong điều kiện.
- Khi cần so sánh lỏng thật sự có chủ đích → `==` (hiểu rõ luật).

## 🎯 Ví dụ minh họa

```js
// Explicit — chủ động, dễ đọc
console.log(String(123), typeof String(123)); // "123" string
console.log(Number("42"), Number("  "), Number("abc"), Number(true));
// 42 0 NaN 1

// Implicit — engine tự ép kiểu
console.log("5" + 3);   // "53"  (nối chuỗi)
console.log("5" - 3);   // 2     (số học)
console.log(null == undefined); // true

// Truthy/Falsy trong điều kiện
if ("") console.log("truthy"); else console.log("falsy empty string");
```

## 📚 Tham khảo / Bài tập

- Học 3 bài con theo thứ tự: `01_conversion-vs-coercion/` (phân biệt 2 loại), `02_explicit/` (ép kiểu tường minh), `03_implicit/` (coercion ngầm định).
- Mỗi thư mục đều có `app.js` — chạy lần lượt bằng `node app.js` (hoặc mở `index.html`) để thấy kết quả thực tế.
- Tự thử: đoán rồi kiểm chứng `[] + []`, `[] + {}`, `{} + []`, `"9" > "10"` trong Console; giải thích từng cái bằng quy tắc coercion và truthy/falsy.
- Tài liệu: [MDN — Type coercion](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators), [javascript.info/type-conversions](https://javascript.info/type-conversions).