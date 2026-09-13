# Luồng điều khiển (Control Flow)

## 🔑 Khái niệm

Control flow (luồng điều khiển) là cách chương trình JavaScript **quyết định đoạn code nào sẽ chạy, và chạy theo thứ tự nào**, dựa trên điều kiện và vòng lặp. Code đọc từ trên xuống gọi là "chạy tuần tự" (sequential); khi gặp điều kiện, chương trình rẽ nhánh (branching) — chỉ chạy nhánh phù hợp.

Trong nhóm này JavaScript có 3 công cụ điều kiện chính, nằm trong thư mục `01_conditionals/`:

- `if...else if...else` — linh hoạt nhất, kiểm tra điều kiện phức tạp.
- `switch...case` — so sánh **nghiêm ngặt** (`===`) một giá trị với nhiều trường hợp, thích hợp khi có nhiều nhánh rời rạc.
- Ternary (`điều kiện ? a : b`) — viết gọn if/else chỉ với **một phép gán**, thường dùng làm giá trị trả về.

## ✅ Điểm mạnh

- **Kiểm soát chương trình rõ ràng**: biết chính xác nhánh nào chạy trong tình huống nào.
- **Ba cú pháp phủ hết tình huống**: kiểm tra phức tạp → `if`, nhiều giá trị rời rạc → `switch`, biểu thức ngắn → ternary.
- `switch` dùng so sánh nghiêm ngặt (`===`) → không gặp bẫy ép kiểu của `==`.
- Ternary rất gọn, phù hợp khi gán giá trị có điều kiện trong một dòng.
- Kết hợp với `&&`, `||`, `!` để viết điều kiện phức tạp một cách tự nhiên.
- Không giới hạn số nhánh `else if`, dễ mở rộng dần.

## ⚠️ Lưu ý / Hạn chế

- **Quên `break` trong `switch`** là lỗi kinh điển: các trường hợp bên dưới sẽ vẫn chạy (fall-through).
- `switch` dùng so sánh nghiêm ngặt `===`: `case "2"` không khớp với giá trị `2`.
- Ternary không phù hợp khi phải chạy nhiều câu lệnh phức tạp — nhồi nhét quá sẽ khó đọc.
- `if (x)` kiểm tra **truthy/falsy**, không phải `x !== undefined` hay `x === true` — cẩn thận với `0`, `""`, `null`, `NaN`.

## 💡 Khi nào dùng

- Thẩm định dữ liệu đầu vào (form, API) trước khi xử lý.
- Điều hướng logic nghiệp vụ: quyền truy cập, trạng thái đơn hàng, loại tài khoản.
- Render UI có điều kiện (hiện/ẩn, khóa nút, chọn theme).
- Chọn nhánh theo giá trị cụ thể (số thứ ngày trong tuần, mã trạng thái HTTP).
- Gán giá trị mặc định ngắn gọn cho biến.

## 🎯 Ví dụ minh họa

```js
const date = 2;

if (date === 2) {
  console.log("Hôm nay là thứ 2"); // → được in
} else {
  console.log("Thứ khác");
}

switch (date) {
  case 2:
    console.log(2);
    break;          // quên break là sẽ in thêm "default"
  default:
    console.log("default");
}

console.log("Sơn".length > 3 ? true : false); // true
```

## 📚 Tham khảo / Bài tập

- `01_conditionals/5_condition/` — thực hành `if` (`1_if.js`), `switch` (`2_switch-case.js`), ternary (`3_toan-tu-3-ngoi.js`).
- `01_conditionals/03_ternary/` — ví dụ ternary ngắn trong `app.js` kèm `index.html`.
- Chạy thử: bỏ `break` trong `2_switch-case.js` và xem kết quả dính `default`.
- Tự thử: viết hàm trả về "Chẵn"/"Lẻ" theo một số nhập vào bằng cả 3 cách (if, switch-hóa, ternary).