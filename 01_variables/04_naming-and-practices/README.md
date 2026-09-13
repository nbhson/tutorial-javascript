# Quy tắc đặt tên biến & Best Practices

## 🔑 Khái niệm

Tên biến là "giấy tờ tùy thân" của dữ liệu trong code. JS có **quy tắc hợp lệ** (cú pháp — vi phạm là lỗi) và **quy ước hay** (thói quen — vi phạm thì chạy được nhưng code khó đọc). Nhóm bài này tập trung vào cả hai.

**Quy tắc (rules — bắt buộc):**

- Chỉ dùng chữ cái `a-z A-Z`, số `0-9`, `_` và `$`.
- **Không bắt đầu bằng số**: `let 1a;` → lỗi cú pháp.
- **Không chứa khoảng trắng**: `my-name` → lỗi (dấu `-` bị hiểu là phép trừ).
- **Không trùng từ khóa reserved** (`var`, `let`, `class`, `function`...).
- Phân biệt chữ hoa/thường: `myAge` ≠ `myage`.

```js
let $ = 1; // hợp lệ (hiếm dùng)
let _ = 2; // hợp lệ (thường cho biến "bỏ qua")
```

**Quy ước (conventions — khuyến nghị):**

- **camelCase** cho biến và hàm: `userName`, `totalScore`, `myAge`.
- **UPPER_SNAKE_CASE** cho hằng số: `MAX_SIZE`, `API_URL`.
- Tên **mô tả rõ ý nghĩa**: `userCount` thay vì `x`, `initialColor` thay vì `c`.
- Tránh viết tắt tối nghĩa, tránh tên chung chung (data, temp, obj).

**Best practices chính:**

1. Ưu tiên **`const`** trước, dùng **`let`** khi cần gán lại, **tránh `var`**.
2. Đặt tên theo **ý nghĩa dữ liệu**, không theo cách triển khai (`cart` thay vì `arr2`).
3. Khai báo biến **gần nơi sử dụng** nhất; khai báo **rõ ràng, có từ khóa** (không phụ thuộc implicit global).

## ✅ Điểm mạnh

- Tên tốt giúp code **tự giải thích** — giảm comment thừa, đọc là hiểu.
- Tránh lỗi cảnh báo từ linter (ESLint: `camelcase`, `no-undef`...).
- `const` + tên mô tả giúp người khác nắm ý định ngay khi nhìn dòng khai báo.
- Đặt tên nhất quán giúp tìm kiếm (grep) và tái cấu trúc dễ dàng.
- Tránh shadowing/trùng tên gây bug khó lường.

## ⚠️ Lưu ý / Hạn chế

- Tên quá trang trọng/đầy đủ (`thisIsAReallyLongVariableNameLord`) cũng phản tác dụng — hãy đủ rõ, không quá dài.
- Tên 1 ký tự (`a`) hoặc chung chung (`data`) gần như vô nghĩa trong code dài.
- `$`/`_` đứng đầu dễ xung đột quy ước thư viện (jQuery dùng `$`, underscore dùng `_`).
- Bắt buộc trong team phải **nhất quán cùng một quy ước** (đặt trong ESLint/Prettier), không tự sáng tạo cá nhân.

## 💡 Khi nào dùng

- Khai báo biến mới bất kỳ: ưu tiên `const` và tên rõ nghĩa.
- Hằng số cấu hình của app → `UPPER_SNAKE`.
- Làm việc nhóm/code công khai (open source) → tuân thủ chặt chẽ rules + conventions.
- Viết test, viết hàm tái sử dụng → tên phản ánh hành vi (verb cho hàm, noun cho dữ liệu).

## 🎯 Ví dụ minh họa

```js
// Tốt
const userCount = 5;
let totalScore = 0;
const API_BASE_URL = "https://api.example.com";

// Kém
let x = 5;             // x nghĩa là gì?
const data = "abc";    // data loại nào?
let arr2 = [1, 2];     // arr2 so với arr1?

// Tránh kiểu này
// let 1a = 3;         // SyntaxError: khởi đầu bằng số
// let my-name = "x";  // SyntaxError: dấu nối
```

## 📚 Tham khảo / Bài tập

- Thư mục này **không có file `app.js`** — hãy mở `01_declarations/` để xem `app.js` (demo dynamic typing + `var`/`let`) và `01_declarations/README.md` để đọc lại toàn bộ quy tắc đặt tên kèm ví dụ đúng/sai.
- Tự thử: lấy một đoạn code cũ của bạn, đổi toàn bộ tên biến `x`, `a`, `data` sang tên mô tả; sau đó khai báo thử `let 1a` và `let my-name` trong Console để thấy lỗi cú pháp thực sự.
- Tài liệu: [javascript.info/variables#variable-naming](https://javascript.info/variables#variable-naming), [MDN — Grammar and types](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Grammar_and_types).