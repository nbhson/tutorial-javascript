# Toán tử Bitwise

## 🔑 Khái niệm

Toán tử bitwise thao tác trực tiếp lên **từng bit** của số nhị phân (biểu diễn 32-bit có dấu). Máy tính lưu mọi số dưới dạng bit, nên các toán tử này cho phép bạn "nói chuyện" với phần cứng theo đúng cách máy hiểu.

Các toán tử trong nhóm:

| Toán tử | Tên | Ví dụ `5` và `1` |
|---|---|---|
| `&` | AND | `5 & 1` → `1` |
| `\|` | OR | `5 \| 1` → `5` |
| `^` | XOR | `5 ^ 1` → `4` |
| `~` | NOT (đảo bit) | `~5` → `-6` |
| `<<` | dịch trái | `5 << 1` → `10` (Nhân 2) |
| `>>` | dịch phải | `5 >> 1` → `2` (Chia 2) |
| `>>>` | dịch phải không dấu | `-5 >>> 1` → `2147483645` |

Giải thích nhanh ví dụ gốc trong `app.js`:

- `5` là `101` (nhị phân), `1` là `001`.
- `101 & 001` = `001` = `1`; `101 | 001` = `101` = `5`; `101 ^ 001` = `100` = `4`.
- `~5` đảo tất cả bit → `-6` (vì bit đầu là bit dấu).
- `5 << 1` dời bit trái 1 vị trí → `1010` = `10` (tương đương ×2); `5 >> 1` → `10` = `2` (tương đương ÷2 và làm tròn xuống).
- `>>>` không giữ bit dấu nên `-5 >>> 1` ra một số dương rất lớn.

**Ứng dụng hay nhất: bit flags** (như code mẫu `README`/`WRITE`/`EXEC`): dùng bit để bật/tắt và kiểm tra quyền.

## ✅ Điểm mạnh

- **Cực nhanh và tiết kiệm bộ nhớ**: gói nhiều cờ boolean vào một số nguyên.
- Kiểm tra quyền, cờ trạng thái rất gọn: `perm & READ` cho biết có quyền đọc hay không.
- Dịch bit là phép nhân/chia cho lũy thừa của 2 cực nhanh.
- Kỹ thuật này xuất hiện trong các thư viện, chuẩn giao thức, game, image processing.
- Giúp hiểu sâu cách máy tính lưu số — nền tảng cho nhiều chủ đề hệ thống.
- Output minh họa rõ ràng từng phép toán trong một dòng.

## ⚠️ Lưu ý / Hạn chế

- **Chỉ an toàn với số nguyên 32-bit**; số thực bị cắt phần thập phân, số vượt quá 32-bit cho kết quả bất ngờ.
- `~` là phép đảo bit, **không phải** phép phủ định "logic" — `~5` không phải "không có 5".
- `~` hay dùng để phát hiện index không tìm thấy: `~arr.indexOf(x)` là `true` khi không có (vì `-1` đảo thành `0`).
- `>>>` với số âm cho số rất lớn, dễ nhầm nếu không hiểu số không dấu.
- Ít dùng trong code nghiệp vụ thường ngày nên dễ bị lãng quên — cần ôn lại khi gặp.

## 💡 Khi nào dùng

- Kiểm tra quyền/cờ: `perm & WRITE`, gộp cờ bằng `READ | WRITE`.
- Xử lý ảnh, màu sắc (rgba), điều kiện trong game (bitmask).
- Tối ưu nhân/chia lũy thừa 2 khi cần hiệu năng cao.
- Thuật toán mã hóa, băm, checksum.
- Đọc/ghi packet dữ liệu nhị phân trong networking.

## 🎯 Ví dụ minh họa

```js
// Nội dung app.js trong thư mục
console.log(5 & 1, 5 | 1, 5 ^ 1, ~5, 5 << 1, 5 >> 1, -5 >>> 1);
// => 1 5 4 -6 10 2 2147483645

// Bit flags — quyền đọc ghi chạy
const READ = 1, WRITE = 2, EXEC = 4;
let perm = READ | WRITE;                    // 3
console.log(perm & READ);                   // 1  → có quyền đọc
console.log(perm & EXEC);                   // 0  → không có quyền chạy
```

## 📚 Tham khảo / Bài tập

- Mở `index.html` trong trình duyệt (Console) hoặc chạy `node app.js` để xem toàn bộ kết quả.
- Tự thử: `console.log(8 >> 2)`, `console.log(8 << 3)`, `console.log(0b1010 | 0b0101)`.
- Tự thử cờ: gộp `perm = READ | WRITE | EXEC` rồi kiểm tra `perm & EXEC` → `4`.
- Thêm quyền thứ tư `DELETE = 8` và tách quyền bằng `perm ^ DELETE` (XOR để bật/tắt).