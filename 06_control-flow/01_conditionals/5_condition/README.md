# Điều kiện rẽ nhánh (Conditionals thực hành)

## 🔑 Khái niệm

Thư mục này chứa 3 file thực hành các cách rẽ nhánh cơ bản:

- `1_if.js` — cấu trúc `if ... else if ... else`, kiểm tra giá trị biến theo thứ tự.
- `2_switch-case.js` — `switch`, so sánh nghiêm ngặt (`===`) một giá trị với từng `case`.
- `3_toan-tu-3-ngoi.js` — toán tử ba ngôi `điều kiện ? đúng : sai`.

Cả ba cùng giải bài toán "kiểm tra một giá trị rồi in ra kết quả" — nhưng với cách tư duy khác nhau: `if` cho phép điều kiện phức tạp nhất, `switch` gọn cho nhiều giá trị rời rạc, ternary ngắn gọn khi chỉ có 2 nhánh đơn giản.

## ✅ Điểm mạnh

- Ba file bổ sung lẫn nhau, giúp so sánh trực tiếp cách viết của từng cú pháp.
- Ví dụ dùng dữ liệu đời thường: số thứ ngày trong tuần, tên có dấu tiếng Việt.
- Chạy độc lập được bằng `node` — không cần trình duyệt.
- Chung một chủ đề nên dễ tự viết phiên bản mở rộng.
- Khối code ngắn, dễ hiểu ngay cả với người mới.

## ⚠️ Lưu ý / Hạn chế

- Trong `1_if.js`, các nhánh `else if` chạy theo thứ tự — hoán đổi thứ tự có thể đổi kết quả nếu điều kiện trùng nhau.
- Trong `2_switch-case.js`, nhớ `break` sau mỗi `case`, nếu không sẽ fall-through sang case kế tiếp.
- `switch` chỉ phù hợp khi so sánh **bằng** một giá trị; không dùng được cho "lớn hơn", "trong khoảng".
- Ternary không nên dùng khi nhánh đúng/sai có nhiều câu lệnh — mất tính rõ ràng.

## 💡 Khi nào dùng

- `1_if.js` — khi điều kiện không tương đương đơn giản (khoảng giá trị, kết hợp nhiều điều kiện).
- `2_switch-case.js` — khi một biến chỉ nhận vài giá trị cụ thể (ngày 2-7, mã trạng thái, id menu).
- `3_toan-tu-3-ngoi.js` — khi chỉ cần chọn 1 trong 2 giá trị để in/gán/trả về.
- Muốn so sánh cách tiếp cận để chọn phong cách phù hợp dự án.

## 🎯 Ví dụ minh họa

```js
// 1_if.js
var date = 2;
if (date === 2) {
  console.log("Hôm nay là thứ 2"); // in ra
} else if (date === 3) {
  console.log("Hôm nay là thứ 3");
} else {
  console.log("Thứ khác");
}

// 2_switch-case.js
switch (date) {
  case 2:
    console.log(2); // in ra 2
    break;
  default:
    console.log("default");
}

// 3_toan-tu-3-ngoi.js
console.log("Sơn".length > 3 ? true : false); // true
```

## 📚 Tham khảo / Bài tập

- `node 1_if.js` — đổi `date` thành 3 để nhánh thứ 2 in, thành 9 để rơi vào `else`.
- `node 2_switch-case.js` — thêm `case 3:` in `3` rồi chạy; sau đó thử **xóa break** của `case 2` để thấy fall-through.
- `node 3_toan-tu-3-ngoi.js` — sửa thành `("An".length > 3 ? ...)` để kết quả thành `false`.
- Tự thử: viết lại 3 tình huống trên nhưng cho biến kiểu số/phân số (ví dụ điểm thi) bằng từng cú pháp.