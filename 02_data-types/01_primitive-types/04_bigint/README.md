# BigInt

## 🔑 Khái niệm

**BigInt** là kiểu primitive dành cho **số nguyên lớn hơn** `Number.MAX_SAFE_INTEGER` (= `9007199254740991`, tức 2⁵³ − 1). Number thông thường mất độ chính xác khi vượt giới hạn an toàn:

```js
const maxSafe = Number.MAX_SAFE_INTEGER;
console.log(maxSafe);          // 9007199254740991
console.log(maxSafe + 1);      // 9007199254740992 ✓
console.log(maxSafe + 2);      // 9007199254740992 ✗ — mất chính xác!
```

BigInt giải quyết điều này bằng cách biểu diễn số nguyên **không giới hạn độ lớn**.

**Tạo BigInt:**

```js
const big = 9007199254740993n;        // thêm chữ n cuối
const viaCtor = BigInt("9007199254740993"); // hoặc qua BigInt("..."/number)
console.log(typeof big);              // "bigint"
```

## ✅ Điểm mạnh

- Số nguyên chính xác tuyệt đối, không giới hạn độ lớn.
- Đọc rất rõ nhờ hậu tố `n` (khác number).
- Phù hợp ID, timestamp nano, tiền tệ hoặc crypto — nơi sai số là "tử hình".
- `BigInt(...)` chuyển đổi tử string/số một cách an toàn.
- Rất dễ dùng chung với các hàm hash, giải mã.

## ⚠️ Lưu ý / Hạn chế

- **KHÔNG trộn** BigInt với Number trong phép toán: `1n + 1` → `TypeError` (quy tắc của roadmap.sh).
- `1n == 1` là `true` (loose equality), nhưng `1n === 1` là `false` — dễ nhầm.
- Không thể dùng `Math.max`, `Math.random()` trực tiếp với BigInt.
- `JSON.stringify(BigInt(1))` ném lỗi — phải chuyển về string trước.
- Phép chia chỉ lấy phần nguyên: `5n / 2n` → `2n`.

## 💡 Khi nào dùng

- ID từ database vượt `Number.MAX_SAFE_INTEGER` (LOT số ID Google/Facebook…).
- Timestamp ở granularity nano giày (Ngôi sao đểu quan tâm).
- Tính toán mật mã (hash, số nguyên lớn) hoặc mô phỏng tiền tệ.
- Khi cần số nguyên chính xác 100% tránh lỗi rounding.

## 🎯 Ví dụ minh họa

```js
const maxSafe = Number.MAX_SAFE_INTEGER;
console.log(maxSafe, maxSafe + 1, maxSafe + 2); // 9007199254740991, ...992, ...992 (mất)

const big = 9007199254740993n;
console.log(big, typeof big);      // 9007199254740993n bigint
console.log(big + 1n);             // 9007199254740994n ✓ chính xác

try { console.log(big + 1); }     // TypeError: Cannot mix BigInt and other types
catch (e) { console.log("Mix error:", e.message); }

console.log(1n == 1, 1n === 1, Object.is(1n, 1n)); // true false true
```

## 📚 Tham khảo / Bài tập

- Chạy `app.js` trong thư mục (`node app.js` hoặc mở `index.html`): in ra `maxSafe` tăng dần mất chính xác, BigInt chính xác, lỗi khi trộn kiểu, la các so sánh `==`/`===`/`Object.is`.
- Tự thử: 1) tính `2n ** 64n` (lũy thừa lớn) và so sánh với `2 ** 64`; 2) thử `JSON.stringify({ id: 9007199254740993n })` và đọc `TypeError: Do not know how to serialize a BigInt`; 3) chuyển BigInt về string số có dấu nối để "đọc" cho đúng.
- Tài liệu: [MDN — BigInt](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/BigInt).