# Toán tử Chuỗi (String Operators)

## 🔑 Khái niệm

Trong JavaScript, **toán tử `+`** khi gặp ít nhất một toán hạng là chuỗi sẽ thực hiện **nối chuỗi** (concatenation) thay vì phép cộng — đó gọi là string operator. Ngoài ra còn có biến thể gán **`+=`** để nối và gán cùng lúc.

```js
console.log("a" + "b");           // "ab"
console.log("a".concat("b"));     // "ab" — phương thức concat tương đương
let s = "hi";
s += " there";                    // s = "hi there"
console.log(s);
```

Ba cách nối chuỗi phổ biến:

1. Toán tử `+` — nhanh, được dùng rộng rãi.
2. `+=` — nối thêm vào biến hiện tại.
3. `.concat(string)` — phương thức của String, ít dùng hơn.
4. (Nâng cao) Template literal với backtick `` ` `` — `` `Hello ${name}` `` là cách hiện đại nhất, tránh những phiền phức của dấu `+`.

## ✅ Điểm mạnh

- **Đơn giản, dễ đọc** với `+` và `+=` — không cần thư viện gì cả.
- Nối được đủ mọi kiểu: `"Số: " + 42` tự đổi 42 thành chuỗi.
- Template literal giúp nối kèm biến rõ ràng và xuống dòng dễ.
- `+=` giúp cộng dồn chuỗi trong vòng lặp/accumulator gọn gàng.
- Là nền tảng cho việc tạo URL, câu thông báo, giao diện hiển thị.

## ⚠️ Lưu ý / Hạn chế

- Thứ tự quan trọng: `1 + 2 + "3"` → `"33"` (cộng số trước) nhưng `"1" + 2 + 3` → `"123"` (nối hết). Kết quả phụ thuộc vị trí của chuỗi.
- Nối quá nhiều chuỗi bằng `+` trong vòng lặp lớn có thể chậm — lúc đó gom vào mảng rồi `join("")`.
- Số được *tự* ép thành chuỗi khi nối, đôi khi gây ngạc nhiên (vd: giá trị từ form bất ngờ ra "12" thay vì 3).
- `.concat()` không chấp nhận mọi kiểu linh hoạt như `+`.

## 💡 Khi nào dùng

- Ghép tên đầy đủ: `firstName + " " + lastName`.
- Xây URL động, route, query string.
- Tạo thông báo / string log cho người dùng.
- Gộp chuỗi lặp lại theo điều kiện bằng `+=`.
- Dựng chuỗi HTML/giao diện đơn giản (nên dùng template literal cho rõ ràng hơn).

## 🎯 Ví dụ minh họa

```js
// Nội dung app.js trong thư mục
console.log("a" + "b", "a".concat("b")); // "ab" "ab"

let s = "hi";
s += " there";
console.log(s); // "hi there"

// Thứ tự ảnh hưởng kết quả
console.log(1 + 2 + "3"); // "33"
console.log("1" + 2 + 3); // "123"
```

## 📚 Tham khảo / Bài tập

- Mở `index.html` (Console) hoặc chạy `node app.js` để xem `ab ab`, `hi there`.
- Tự thử: `console.log("Tổng: " + (1 + 2))` (cần ngoặc để cộng trước) so với `"Tổng: " + 1 + 2`.
- Tự thử dùng template literal: `` `Chào ${"Sơn"}, bạn có ${2} thông báo` ``.
- Thử `["HTML","CSS","JS"].join(" - ")` — cách ghép chuỗi hàng loạt hiệu quả.