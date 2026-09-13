# Optional Chaining (?.)

## 🔑 Khái niệm

Optional chaining `?.` truy cập property/method **an toàn** — nếu bên trái là `null` hoặc `undefined` thì trả về `undefined` thay vì throw `TypeError`.

```js
// Trước ES2020
const city = user && user.address && user.address.city;

// ES2020+
const city = user?.address?.city;
```

Hỗ trợ:
- Property access: `obj?.prop`
- Element access: `arr?.[i]`
- Function call: `fn?.()`
- Method chain: `obj?.method?.()`

## ✅ Điểm mạnh
- Ngăn `Cannot read properties of undefined` crash
- Code ngắn gọn, đọc tự nhiên
- Kết hợp `??` default value đẹp

## ⚠️ Lưu ý
- Chỉ check `null`/`undefined`, **không** check falsy khác (`0`, `""`, `false`)
- `?.` không short-circuit được trong điều kiện phức tạp (cần `&&` thay thế)
- `?.()` — nếu `fn` là `null` → trả `undefined`, không gọi
- Không dùng `?.` thay `&&` nếu cần phân biệt `null` vs `0`/`false`/`""`

## 💡 Khi nào dùng
- Access nested API response có thể thiếu field
- Optional method call
- Safe array access với index có thể out-of-bounds

## 🎯 Ví dụ minh họa

### Safe nested access
```js
const user = { profile: { name: "A" } };
console.log(user?.profile?.name);     // "A"
console.log(user?.address?.city);     // undefined (không lỗi)
console.log(user?.nonExistent);       // undefined
```

### Optional function call
```js
const obj = { maybeFn: null };
obj.maybeFn?.(); // không lỗi, trả undefined

// So với obj.maybeFn() → TypeError
```

### Safe array access
```js
const arr = [1, 2, 3];
console.log(arr?.[5]);   // undefined (không lỗi index out of range)
console.log(arr?.length); // 3
```

### Kết hợp với ??
```js
const userName = user?.name ?? "Guest";
// nếu user === null → userName = "Guest"
```

## 📚 Tham khảo & Bài tập
- File: `app.js`, `index.html` trong folder `01_optional-chaining/`
- Thực hành: xử lý API response có nested optional fields
- Câu hỏi: `obj?.prop` và `obj && obj.prop` khác nhau ở đâu?
