# Toán tử một ngôi (Unary Operators)

## 🔑 Khái niệm

Toán tử một ngôi (unary) là toán tử chỉ cần **một toán hạng duy nhất** để tạo ra giá trị. Nhóm này đặc biệt quan trọng vì chứa những phép "kiểm tra và biến đổi" sử dụng hằng ngày:

| Toán tử | Công dụng | Ví dụ |
|---|---|---|
| `typeof` | trả về tên kiểu dữ liệu | `typeof 123` → `"number"` |
| `void` | trả về `undefined` | `void 0` → `undefined` |
| `delete` | xóa thuộc tính của object | `delete o.a` |
| `+` | ép sang Number | `+"42"` → `42` |
| `-` | đổi dấu / ép sang Number | `-"42"` → `-42` |
| `!` | phủ định boolean | `!0` → `true` |
| `~` | đảo bit (bitwise NOT) | `~5` → `-6` |
| `++` / `--` | tăng/giảm 1 | `++n` / `n++` |

Điểm thú vị trong `app.js` (file mẫu của thư mục):

```js
console.log(typeof 123, typeof null); // "number" "object"  ← typeof null là "object" (lỗi lịch sử của JS!)
console.log(void 0, void (1 + 1));    // undefined undefined
let o = { a: 1, b: 2 };
delete o.a;
console.log(o);                       // { b: 2 }
console.log(+"42", -"42", !0, !!1);   // 42 -42 true true
```

## ✅ Điểm mạnh

- **`typeof`** kiểm tra kiểu an toàn mà không cần biết biến có tồn tại hay không.
- **`+`/"-"** chuyển chuỗi số (hoặc kiểu khác) thành Number cực gọn — thay cho `Number()`.
- **`! và !!`** ép bất cứ giá trị nào thành boolean để kiểm tra truthy/falsy.
- **`void 0`** — cách viết an toàn lấy `undefined` (không sợ bị gán đè).
- **`delete`** xóa thuộc tính của object, hữu ích khi dọn dữ liệu.
- Viết tay dễ, không cần thư viện.

## ⚠️ Lưu ý / Hạn chế

- `typeof null` trả về `"object"` — một "bug lịch sử" của JavaScript, đừng dùng nó để kiểm tra null.
- `delete` chỉ xóa **thuộc tính của object**; không dùng để xóa biến, và không ảnh hưởng đến biến local.
- `+""` → `0`, `+[]` → `0`, `+null` → `0`: ép với giá trị "rỗng" dễ ra số 0 không ngờ.
- `++`/`--` có sự khác nhau prefix (trả giá trị mới) và postfix (trả giá trị cũ) — xem chi tiết file `6_toan-tu-prefix-postfix.js`.
- `~` là đảo bit, đừng nhầm với phủ định logic `!`.

## 💡 Khi nào dùng

- Kiểm tra kiểu giá trị trước khi xử lý: `typeof value === "number"`.
- Ép chuỗi kết quả API/form về số: `+"123"` rồi cộng trừ.
- Bỏ qua giá trị của một thao tác và chỉ cần `undefined` (vd: `href="javascript:void(0)"`).
- Xóa trường không cần thiết khỏi object trước khi gửi API.
- Kiểm tra nhanh truthy bằng `!!` trong điều kiện hoặc gán boolean.

## 🎯 Ví dụ minh họa

```js
// Nội dung app.js trong thư mục
console.log(typeof 123, typeof null); // "number" "object"
console.log(void 0, void(1 + 1));     // undefined undefined

let o = { a: 1, b: 2 };
delete o.a;
console.log(o);                       // { b: 2 }

console.log(+"42", -"42", !0, !!1);   // 42 -42 true true
```

## 📚 Tham khảo / Bài tập

- Mở `index.html` (Console) hoặc chạy `node app.js` để xem toàn bộ kết quả.
- Tự thử `typeof` với: `typeof undefined`, `typeof [1,2]` (`"object"`), `typeof NaN`, `typeof (() => {})` (`"function"`).
- Tự thử ép kiểu: `+true` (`1`), `+false` (`0`), `+null` (`0`), `+""` (`0`).
- Tự thử `delete` với mảng: `let arr=[1,2,3]; delete arr[1]; console.log(arr)` — thấy ô trống `[1, <1 empty item>, 3]`, không rút ngắn mảng (muốn rút ngắn dùng `splice`).
- Xem lại `01_operators/6_toan-tu-prefix-postfix.js` để phân biệt `++i` và `i++`.