# Built-in: RegExp (Biểu thức chính quy)

## 🔑 Khái niệm

**`RegExp`** (Regular Expression) là mẫu (pattern) dùng để **tìm, kiểm tra, thay thế** chuỗi theo quy tắc. Cú pháp tạo mẫu:

```js
const re = /ab+c/g;              // literal — khuyên dùng
const re2 = new RegExp("ab+c", "g"); // constructor — dùng khi pattern động
```

**Giải thích mẫu `/ab+c/g`:** chữ `a`, theo sau **một hoặc nhiều** `b` (`b+`), rồi chữ `c`. Cờ `g` = global (tìm tất cả, không dừng ở kết quả đầu).

**Các phương thức quan trọng:**

```js
const re = /ab+c/g;

re.test("abbbc");      // true   — có khớp hay không (boolean)
"abc".match(re);       // ["abc"] — danh sách kết quả khớp (với cờ g)
"abbbcabc".match(/ab+c/g); // ["abbbc", "abc"]
"abbbc".replace(/b+/, "X"); // "aXc"
"abbbc".search(/b+/);       // 1 (vị trí khớp đầu tiên, -1 nếu không có)
```

> Lưu ý: mẫu `/ab+c/` đọc là chữ `a`, rồi **một hoặc nhiều** chữ `b` (`b+`), rồi chữ `c`. Vì thế cả `"abc"` (một chữ `b`) lẫn `"abbbc"` (ba chữ `b`) đều khớp. Cờ `g` (global) khiến `match` trả về **mảng mọi kết quả** thay vì chỉ kết quả đầu.

**Một số ký tự mẫu thường gặp:**

| Ký tự | Ý nghĩa |
|---|---|
| `.` | một ký tự bất kỳ |
| `*`, `+`, `?` | lặp 0-nhiều / 1-nhiều / 0-1 |
| `[abc]` | một trong a, b, c |
| `\d`, `\w`, `\s` | chữ số, ký tự word, khoảng trắng |
| `^`, `$` | bắt đầu / kết thúc chuỗi |
| Cờ `g`, `i`, `m` | global, không phân biệt hoa/thường, đa dòng |

## ✅ Điểm mạnh

- Cực mạnh cho validation & tìm kiếm trong thời gian ngắn.
- Viết một dòng thay cho hàng chục dòng kiểm tra phức tạp.
- Được engine tối ưu ở tầng thấp → nhanh hơn xử lý thủ công.
- Có luôn trong mọi môi trường JS — không cần thư viện.
- `replace` kết hợp regex xử lý text định kỳ (chuẩn hóa khoảng trắng, email...) cực gọn.

## ⚠️ Lưu ý / Hạn chế

- Cú pháp mật mã hóa, dễ viết sai mà không lỗi ngay — nên test kỹ.
- `test` với cờ `g` có **trạng thái lastIndex**: chạy lại cũng chuỗi cho kết quả khác — ngạc nhiên dễ gặp.
- `match` **không có cờ `g`** trả về mảng chi tiết (kèm `index`, `groups`), có cờ `g` chỉ trả danh sách kết quả.
- Regex phức tạp (backtracking) dễ gây **chậm/REDOS** với input xấu.

## 💡 Khi nào dùng

- Kiểm tra định dạng email, số điện thoại, mã bưu chính → `test`.
- Tìm/trích xuất các phần tử khớp: ngày giờ trong text, khoảng trắng thừa → `match`.
- Thay thế hàng loạt theo quy luật → `replace(/pattern/g, ...)`.
- Validate form ngay khi gõ.

## 🎯 Ví dụ minh họa

```js
const re = /ab+c/g;
console.log(re.test("abbbc"));     // true
console.log("abc".match(re));      // ["abc"] — global match trả mảng kết quả khớp
console.log("abbbcabc".match(re)); // ["abbbc", "abc"]

// Validate email đơn giản
console.log(/^[\w.-]+@[\w.-]+\.\w+$/.test("nam@example.com")); // true

// Thay tất cả với cờ g
console.log("a2 b4 c8".replace(/\d/g, "X")); // "aX bX cX"
```

## 📚 Tham khảo / Bài tập

- Chạy `app.js` trong thư mục (`node app.js` hoặc mở `index.html`): in ra `re.test("abbbc")` (true) và `"abc".match(re)` (["abc"]) để thấy hành vi `match` với cờ g.
- Tự thử: 1) regex kiểm tra số điện thoại Việt Nam dạng `0[0-9]{9}`; 2) trích số từ chuỗi `"Giá: 1.250.000đ"` bằng `match(/\d/g)` rồi nối lại; 3) dùng `replace(/\s+/g, " ")` để chuẩn hóa nhiều khoảng trắng.
- Tài liệu: [MDN — RegExp](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/RegExp), [regex101](https://regex101.com) để thử mẫu trực quan.