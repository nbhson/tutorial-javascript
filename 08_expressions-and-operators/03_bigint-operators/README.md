# Toán tử BigInt

## 🔑 Khái niệm

`BigInt` là kiểu số nguyên chính xác tuyệt đối trong JavaScript, khắc phục giới hạn của `Number` khi làm việc với các số nguyên rất lớn (lớn hơn `Number.MAX_SAFE_INTEGER = 2^53 - 1`). Viết BigInt bằng cách **thêm hậu tố `n`**: `10n`, `9007199254740991n + 1n`.

BigInt dùng các toán tử **giống hệt** Number: `+ - * / % **`:

```js
console.log(10n + 5n, 10n * 2n, 10n / 3n, 10n % 3n, 2n ** 10n);
// 15n 20n 3n 1n 1024n
```

Lưu ý đặc biệt: **`10n / 3n` → `3n`** — phép chia BigInt luôn trả về số nguyên (phần thập phân bị cắt), không phải `3.333...`.

## ✅ Điểm mạnh

- **Chính xác tuyệt đối** với số nguyên cực lớn — không sợ mất chữ số cuối như Number.
- Dùng chung cú pháp toán tử với Number → học nhanh, code tương tự.
- Tốt cho: số ID ngân hàng, số serial, hash, tiền tệ kỹ thuật số, mật mã.
- Kết hợp được với hàm `BigInt(value)` để chuyển đổi từ chuỗi/số.
- Không bao giờ trả về số thập phân trong phép `/` — tránh sai số lẻ.
- An toàn hơn khi so sánh các số cực lớn trong dữ liệu API.

## ⚠️ Lưu ý / Hạn chế

- **Không trộn lẫn BigInt với Number** trong cùng phép toán: `10n + 1` → `TypeError`. Phải chuyển đổi qua lại bằng `Number(n)` / `BigInt(x)`.
- Phép `/` trên BigInt cắt phần thập phân — cần tự xử lý nếu muốn số thập phân.
- Một số thư viện/hàm như `Math.*` không hỗ trợ BigInt (vd: `Math.max(1n, 2n)` gây lỗi).
- `JSON.stringify(BigInt)` không hỗ trợ trực tiếp (phải chuyển thành chuỗi trước).
- Vẫn có giới hạn bộ nhớ khi số quá khổng lồ.

## 💡 Khi nào dùng

- Xử lý ID lớn vượt quá 2^53 từ API/CSDL (vd: ID chuỗi số dài).
- Các phép toán chính xác trong tài chính, blockchain, mật mã.
- Tính toán số học có độ chính xác cao (hệ số, phép đếm lớn).
- Khi so sánh hoặc lưu trữ các con số cực lớn không muốn mất precision.

## 🎯 Ví dụ minh họa

```js
// Nội dung app.js trong thư mục
console.log(10n + 5n, 10n * 2n, 10n / 3n, 10n % 3n, 2n ** 10n);
// 15n 20n 3n 1n 1024n

// Số lớn hơn giới hạn an toàn của Number
console.log(9007199254740991n + 1n); // 9007199254740992n (chính xác)

// Để so sánh với Number phải chuyển đổi
console.log(10n > 9); // true — so sánh được, chỉ phép toán hỗn hợp mới lỗi
```

## 📚 Tham khảo / Bài tập

- Mở `index.html` hoặc chạy `node app.js` để thấy dãy kết quả `15n 20n 3n 1n 1024n`.
- Tự thử: `console.log(10n + 1)` và xem `TypeError` — đó chính là quy tắc không trộn kiểu.
- Tự thử: `console.log(Number("9007199254740993"))` (mất chính xác) so với `9007199254740993n` (đúng nguyên vẹn).
- Viết hàm cộng hai chuỗi số lớn bằng cách chuyển thành BigInt rồi nối kết quả với `toString()`.