# Built-in: Date

## 🔑 Khái niệm

**`Date`** là built-in object biểu diễn **một khoảnh khắc thời gian** (timestamp — số mili giây từ 1970-01-01 UTC, gọi là **epoch**). Tất cả logic thời gian đều nên nói bằng `Date`, vì JS engine xử lý múi giờ, leap year, định dạng... hộ bạn.

**Tạo Date:**

```js
new Date();                          // thời điểm hiện tại
new Date(1725012345678);             // từ timestamp (ms)
new Date("2024-01-01T12:00:00Z");    // từ chuỗi ISO (UTC)
new Date(2024, 0, 1, 12, 30, 0);     // từ thành phần — LƯU Ý tháng tính từ 0!
```

**Các phương thức chính:**

| Phương thức | Ý nghĩa |
|---|---|
| `d.toISOString()` | chuỗi ISO 8601 theo UTC: `"2025-08-30T07:00:00.000Z"` |
| `d.getTime()` | timestamp số ms kể từ epoch |
| `d.getFullYear()`, `getMonth()`, `getDate()`, `getHours()`... | lấy từng thành phần (theo **giờ địa phương**) |
| `d.toLocaleDateString("vi-VN")` | hiển thị theo ngôn ngữ/quốc gia |
| `Date.now()` | timestamp hiện tại (không cần tạo object) |

```js
const d = new Date();
console.log(d.toISOString(), d.getTime());
// "2025-08-30T07:00:00.000Z" 1725012345678
```

## ✅ Điểm mạnh

- Chuẩn hóa toàn cầu bằng timestamp — so sánh/trừ ngày bằng số rất an toàn.
- `toISOString()` chuẩn máy tính đọc được, tránh lỗi khi truyền qua API.
- Hỗ trợ múi giờ và định dạng địa phương sẵn có.
- `Date.now()` nhanh gọn — thích hợp đo hiệu năng.
- Làm việc với JSON trở nên quen thuộc: `JSON.stringify` tự chuyển Date về chuỗi ISO.

## ⚠️ Lưu ý / Hạn chế

- **Tháng bắt đầu từ `0`**: `new Date(2024, 0, 1)` là **tháng 1**; ghi `new Date(2024, 1, 1)` là tháng 2 — lỗi 1 tháng kinh điển.
- `Date` **mutable** — cần clone (`new Date(d.getTime())`) nếu không muốn sửa biến gốc.
- So sánh `new Date()` bằng `==`/`===` với Date khác là **so sánh tham chiếu**, luôn `false`; so sánh timestamp: `a.getTime() === b.getTime()`.
- Parse chuỗi không chuẩn (`"12/11/2024"`) có hành vi khác nhau giữa trình duyệt — dùng ISO hoặc thư viện (date-fns/luxon) nếu cần.

## 💡 Khi nào dùng

- Lưu/hiển thị thời điểm tạo bản ghi, bài viết → `new Date()` + `toISOString()`.
- Tính khoảng thời gian: `end.getTime() - start.getTime()` → quy đổi ngày/giờ.
- Đồng hồ hiện thị: cập nhật `setInterval(() => render(new Date()), 1000)`.
- Đếm ngược deadline, đo thời gian chạy hàm.

## 🎯 Ví dụ minh họa

```js
const d = new Date();
console.log(d.toISOString());        // "2025-08-30T07:00:00.000Z"
console.log(d.getTime());            // 1725012345678
console.log(Date.now());             // gần bằng getTime()

// Chú ý: tháng tính từ 0
console.log(new Date(2024, 0, 1).toLocaleDateString("vi-VN")); // 1/1/2024

// Tính chênh lệch thời gian
const start = new Date("2024-01-01");
const end = new Date("2024-01-03");
console.log((end.getTime() - start.getTime()) / 86400000); // 2 (ngày)
```

## 📚 Tham khảo / Bài tập

- Chạy `app.js` trong thư mục (`node app.js` hoặc mở `index.html`): in ra `toISOString()` và `getTime()` của thời điểm hiện tại.
- Tự thử: 1) tạo `Date` bằng `new Date(2024, 0, 1)` và `new Date("2024-01-01")` để so sánh, kiểm tra sự khác biệt về tháng; 2) viết hàm `daysBetween(a, b)` trả số ngày chênh lệch; 3) hiển thị giờ Việt Nam `toLocaleString("vi-VN")`.
- Tài liệu: [MDN — Date](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date).