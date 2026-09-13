# String (Chuỗi)

## 🔑 Khái niệm

**String** là kiểu primitive dùng để biểu diễn **chuỗi ký tự** (văn bản). Có **3 cách tạo chuỗi**:

```js
var fullName_1 = 'Sơn Nguyễn';          // 1. dấu nháy đơn
var fullName_2 = "Sơn Nguyễn";          // 2. dấu nháy kép
var fullName_3 = `Tôi là ${firstName}`; // 3. template string (ES6)
```

- **Cách nên dùng:** template string `` ` `` khi cần chèn biến (`${ten}`) hoặc viết chuỗi nhiều dòng; nháy đơn/kép tùy quán đội ngũ nhưng **giữ nhất quán**.
- **Cách tránh:** `new String('...')` — kết quả là **object** wrapper, không phải primitive:

```js
var fullName_2 = new String('Sơn Nguyễn'); // typeof === "object" ❌
```

**Ký tự đặc biệt (escape) bằng backslash `\`:**

```js
var fullName_3 = 'Sơn Nguyễn \\ là \'Siêu Nhân\'';
console.log(fullName_3);
// Sơn Nguyễn \ là 'Siêu Nhân'
```

**Độ dài chuỗi** — dùng `.length`:

```js
var fullName_4 = 'Sơn Nguyễn';
console.log(fullName_4.length); // 10
```

> Chú ý: giữ dòng code dưới ~80 ký tự, và `.length` đếm theo code unit — ký tự Unicode phức tạp (emoji) có thể tính thành 2.

**Template string (ES6)** — chèn biến + xuống dòng thoải mái:

```js
var firstName = 'Sơn';
var lastName = 'Nguyễn';
var fullName_5 = `Tôi là ${firstName} ${lastName}`;
console.log(fullName_5); // Tôi là Sơn Nguyễn
```

**Các phương thức thao tác chuỗi thường dùng:**

| Phương thức | Ý nghĩa |
|---|---|
| `indexOf(tìm)` / `lastIndexOf(tìm)` | vị trí ký tự đầu/cuối, `-1` nếu không thấy |
| `search(regex)` | tìm theo biểu thức chính quy |
| `slice(from, to)` | cắt chuỗi (hỗ trợ index âm) |
| `replace(a, b)` / `replace(/a/g, b)` | thay thế, có `g` mới thay tất cả |
| `toUpperCase()` / `toLowerCase()` | viết hoa / thường |
| `trim()` | bỏ khoảng trắng hai đầu |
| `split(dấu_phân_cách)` | tách thành mảng |
| `charAt(i)` / `str[i]` | lấy ký tự theo vị trí |

## ✅ Điểm mạnh

- Primitive bất biến → an toàn, không lo bị thay đổi ngoài ý muốn.
- Template string giúp nối chuỗi sạch sẽ thay cho dấu `+` chồng chất.
- Hệ thống phương thức (slice, trim, split...) đủ mạnh cho phần lớn thao tác văn bản.
- `replace` kết hợp regex → chỉnh sửa một cụm linh hoạt.
- Đọc/gỡ lỗi dễ vì chuỗi hiển thị trực tiếp.

## ⚠️ Lưu ý / Hạn chế

- **Bất biến**: mọi phương thức đều **trả về chuỗi mới**, không sửa chuỗi gốc.
- `replace('a','b')` chỉ thay **kết quả đầu tiên** — muốn thay hết phải dùng regex `/g`.
- `search` không hỗ trợ tham số vị trí bắt đầu (khác `indexOf`), nhưng nhận regex.
- `new String()` tạo object (typeof `"object"`) — không nên dùng.
- So sánh & tìm kiếm phân biệt hoa/thường mặc định.

## 💡 Khi nào dùng

- Hiển thị/chèn dữ liệu động vào giao diện: `` `Chào ${name}` ``.
- Xử lý form: `trim()` đầu vào, kiểm tra `includes('@')`.
- Tách/ghép văn bản: `split(',')` để đọc CSV, `join()` để ghép lại.
- Kiểm tra từ khóa: `indexOf`/`includes` trong tìm kiếm.
- Làm sạch dữ liệu từ API: `replace(/ +/g, ' ')`, `toLowerCase()` để chuẩn hóa.

## 🎯 Ví dụ minh họa

```js
var myString = 'Hoc JS tai JS F8 JS!';

console.log(myString.length);        // 20
console.log(myString.indexOf('JS')); // 4  (vị trí đầu tiên)
console.log(myString.lastIndexOf('JS')); // 17
console.log(myString.slice(4, 6));   // "JS"
console.log(myString.slice(-6, -4)); // "F8" (index âm tính từ cuối)
console.log(myString.replace('JS', 'Javascript'));      // thay 1 chỗ đầu
console.log(myString.replace(/JS/g, 'Javascript'));     // thay tất cả

var language = 'PHP, JS, CSS, HTML';
console.log(language.split(','));    // ['PHP',' JS',' CSS',' HTML']
console.log('Javascript'.split('')); // ['J','a','v',...]
```

## 📚 Tham khảo / Bài tập

- Chạy `1_chuoi.js` (tạo chuỗi, backslash, length, template string) rồi `2_lam-viec-voi-chuoi.js` (indexOf, slice, replace, split, charAt) bằng `node`.
- Tự thử: 1) dùng `slice` cắt lấy phần tên miền từ `https://example.com/x`; 2) dùng `replace(/JS/g, ...)` trên `1_chuoi.js` để thấy khác biệt giữa có và không có cờ `g`; 3) viết chuỗi template dựng thẻ HTML: `` `<h1>${title}</h1>` ``.
- Tài liệu: [MDN — String](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String), [javascript.info/string](https://javascript.info/string).