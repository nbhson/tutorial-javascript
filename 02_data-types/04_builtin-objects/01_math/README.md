# Built-in: Math

## 🔑 Khái niệm

**`Math`** là một built-in object "namespace" chứa **hàm toán học và hằng số** dùng ngay mà không cần khởi tạo. Đặc điểm riêng: `Math` **không có constructor** — gọi `new Math()` sẽ lỗi. Bạn chỉ truy cập `Math.hàm` hoặc `Math.hằng_số`.

**Các hằng số & hàm thường dùng:**

| Thành viên | Ý nghĩa |
|---|---|
| `Math.PI` | số π ≈ 3.14159 |
| `Math.E` | số e ≈ 2.71828 |
| `Math.max(a, b, ...)` | giá trị lớn nhất trong các đối số |
| `Math.min(a, b, ...)` | giá trị nhỏ nhất |
| `Math.round(x)` | làm tròn (bỏ 0.5 trở lên thành 1) |
| `Math.ceil(x)` | làm tròn lên |
| `Math.floor(x)` | làm tròn xuống |
| `Math.abs(x)` | giá trị tuyệt đối |
| `Math.random()` | số ngẫu nhiên `>= 0` và `< 1` |
| `Math.pow(x, y)` / `x ** y` | lũy thừa |
| `Math.sqrt(x)` | căn bậc hai |
| `Math.trunc(x)` | bỏ phần thập phân |

```js
console.log(Math.PI, Math.max(1,5,3), Math.floor(1.9), Math.random());
// 3.141592653589793 5 1 <số ngẫu nhiên 0≤r<1>
```

**Ví dụ muốn số nguyên ngẫu nhiên trong khoảng `[min, max]`:**

```js
function randomInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}
```

## ✅ Điểm mạnh

- Không cần cài thư viện — `Math` có sẵn ở mọi môi trường JS.
- Gọn, đúng chuẩn, được các engine (V8, SpiderMonkey) tối ưu hiệu năng.
- Giá trị tuyệt đối, làm tròn, max/min, random... giải quyết đúng việc thường gặp.
- Kết hợp với `Number.prototype.toFixed()` để format số thập phân hiển thị.

## ⚠️ Lưu ý / Hạn chế

- `Math.random()` trả `>= 0` và `< 1` — **không bao giờ bằng 1**, và không an toàn cho mật mã (dùng `crypto.getRandomValues` thay khi cần mật mã).
- Không thể `new Math()` — chỉ dùng `Math.xxx`.
- `Math.round(-1.5)` → `-1` (về phía dương), khác `Math.floor(-1.5)` → `-2`.
- `Math.max()`/`Math.min()` không nhận mảng trực tiếp — muốn truyền mảng phải spread: `Math.max(...arr)`.
- Không hoạt động với BigInt.

## 💡 Khi nào dùng

- Làm tròn/hiển thị số (giá tiền, phần trăm) → `Math.round`/`toFixed`.
- Xác định max/min trong một dãy dữ liệu → `Math.max(...danhSach)`.
- Sinh số ngẫu nhiên cho game, kiểm tra, phân tích → `Math.random` + `Math.floor`.
- Tính khoảng cách, diện tích, tọa độ → `Math.sqrt`, `Math.pow`, `Math.abs`.

## 🎯 Ví dụ minh họa

```js
console.log(Math.PI);                 // 3.141592653589793
console.log(Math.max(1, 5, 3));       // 5
console.log(Math.floor(1.9));         // 1
console.log(Math.random());           // 0 ≤ r < 1
console.log(Math.abs(-15.41));        // 15.41
console.log(Math.ceil(3.1));          // 4
console.log(Math.round(3.4));         // 3
console.log(Math.min(...[8, 3, 5]));  // 3 (spread mảng)
```

## 📚 Tham khảo / Bài tập

- Chạy `app.js` trong thư mục (`node app.js` hoặc mở `index.html`): in ra `Math.PI`, `Math.max(1,5,3)`, `Math.floor(1.9)`, `Math.random()`.
- Tự thử: 1) viết `randomInt(1, 100)` và chạy 5 lần kiểm tra luôn nằm trong `[1, 100]`; 2) so sánh `Math.round(-1.5)` vs `Math.floor(-1.5)`; 3) `Math.max(...mang)` với mảng 10 phần tử.
- Tài liệu: [MDN — Math](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math).