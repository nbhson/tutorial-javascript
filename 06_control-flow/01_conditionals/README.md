# Điều kiện (Conditionals)

## 🔑 Khái niệm

Conditionals là các cấu trúc cho phép chương trình **chọn nhánh thực thi dựa trên điều kiện**. JavaScript cung cấp ba cách chính, mỗi cách phù hợp một kiểu bài toán:

| Cú pháp | Đặc điểm |
|---|---|
| `if (điều kiện) { } else if { } else { }` | kiểm tra điều kiện logic phức tạp, nhiều nhánh |
| `switch (x) { case: break; default: }` | so sánh nghiêm ngặt một giá trị với nhiều trường hợp |
| `x ? a : b` | viết gọn của if/else, dùng làm giá trị gán/trả về |

Phân nhánh trong thư mục này:

- `5_condition/` — ba file thực hành: `1_if.js`, `2_switch-case.js`, `3_toan-tu-3-ngoi.js`.
- `03_ternary/` — ví dụ ternary được load qua `index.html` + `app.js`.

## ✅ Điểm mạnh

- `if...else` đọc tự nhiên, linh hoạt với mọi loại điều kiện (kết hợp `&&`, `||`, `!`, phép so sánh).
- `switch` gọn gàng khi có từ 3-4 nhánh giá trị rời rạc trở lên, dễ thêm bớt trường hợp.
- `switch` dùng `===` nên không có bẫy ép kiểu như `==`.
- Ternary giúp giảm dòng code khi chỉ cần chọn một trong hai giá trị.
- Các cấu trúc này lồng nhau được, kết hợp được với vòng lặp và hàm.
- Được minh họa bằng dữ liệu thực tế (thứ trong tuần, tên tiếng Việt có dấu).

## ⚠️ Lưu ý / Hạn chế

- **Quên `break`** trong `switch` gây fall-through: chạy tiếp các `case` phía sau. Đôi khi người ta cố tình dùng fall-through để gộp case, nhưng phải viết rõ ràng.
- `switch` dùng so sánh nghiêm ngặt: `case 2` không khớp với `"2"`.
- `else if` xử lý theo thứ tự từ trên xuống — nhánh đầu tiên **đúng** sẽ thắng, các nhánh sau dù đúng cũng không chạy. Sắp xếp thứ tự điều kiện cần cẩn thận.
- Nếu đã `return` hoặc `throw` trong mọi nhánh thì không cần `else` — code dài dòng hơn mức cần.
- Ternary lồng nhau quá nhiều (ternary trong ternary) rất khó đọc — hãy dùng `if`.

## 💡 Khi nào dùng

- `if` — xử lý logic theo khoảng giá trị hoặc điều kiện phức tạp (ví dụ: điểm >= 8 → giỏi).
- `switch` — xử lý theo một giá trị cụ thể với nhiều trường hợp (ngày trong tuần, mã trạng thái, loại dụng cụ).
- Ternary — gán biến mặc định, chọn giá trị/văn bản hiển thị theo trạng thái.
- Kết hợp cả ba khi một hàm cần nhiều bước rẽ nhánh.

## 🎯 Ví dụ minh họa

```js
// 1_if.js
var date = 2;
if (date === 2) {
  console.log("Hôm nay là thứ 2");
} else if (date === 3) {
  console.log("Hôm nay là thứ 3");
} else {
  console.log("Thứ khác");
}

// 2_switch-case.js
switch (date) {
  case 2:
    console.log(2);
    break;
  default:
    console.log("default");
}

// 3_toan-tu-3-ngoi.js
console.log("Sơn".length > 3 ? true : false); // true
```

## 📚 Tham khảo / Bài tập

- `node 5_condition/1_if.js` — đổi `date` sang 3, 4 và quan sát nhánh in ra.
- `node 5_condition/2_switch-case.js` — thêm nhiều `case` cho các ngày 3, 4, 5; thử bỏ một `break` để thấy fall-through.
- `node 5_condition/3_toan-tu-3-ngoi.js` — đổi tên trong `"Sơn"` để kết quả đổi thành `false`.
- Mở `03_ternary/index.html` trên trình duyệt (DevTools → Console) để thấy giá trị `"Success"` gán cho `a` trong `app.js`.
- Tự thử: viết lại thuật toán xếp loại "Giỏi/Khá/TB/Yếu" theo điểm bằng cả `if...else` và một hàm trả ternary.