# Nullish Coalescing (??)

## 🔑 Khái niệm

`a ?? b` trả về `b` **chỉ khi** `a` là `null` hoặc `undefined`. Khác với `||` — `||` trả `b` khi `a` là **bất kỳ falsy value** nào (`0`, `""`, `false`, `NaN`).

```js
0 ?? 10   // 0  (giữ nguyên vì 0 không phải null/undefined)
"" ?? "default"  // ""
false ?? true   // false
null ?? "fallback"  // "fallback"
undefined ?? "fallback"  // "fallback"
```

## ✅ Điểm mạnh
- Phân biệt đúng `null`/`undefined` vs giá trị hợp lệ (0, "", false)
- Mặc định value an toàn cho form input, config
- Thay thế pattern `var = var || default` gây bug

## ⚠️ Lưu ý
- **Không** dùng `??` thay `||` cho mọi trường hợp — chọn đúng ngữ cảnh
- Operator precedence: `??` thấp hơn `&&`/`||` → cần dấu ngoặc nếu trộn
- `??` không short-circuit kiểu `&&` — vế phải vẫn evaluate

## 💡 Khi nào dùng
- Default config value cho số (0 là hợp lệ)
- Form input default text
- API response fallback

## 🎯 Ví dụ minh họa

### So sánh ?? vs ||
```js
const count = 0;
console.log(count || 10);   // 10  ← Sai! 0 là hợp lệ
console.log(count ?? 10);   // 0   ← Đúng! giữ nguyên 0

const name = "";
console.log(name || "Guest");  // "Guest"
console.log(name ?? "Guest");  // ""  (empty string là hợp lệ)
```

### Form input default
```js
const age = parseInt(input.value) ?? 0;
const limit = config.limit ?? 100; // giữ 0 nếu config.limit = 0
```

### Kết hợp với optional chaining
```js
const city = user?.address?.city ?? "Chưa cập nhật";
const theme = settings?.ui?.theme ?? "light";
```

## 📚 Tham khảo & Bài tập
- File: `app.js`, `index.html` trong folder `02_nullish-coalescing/`
- Thực hành: viết function `resolveDefault(value, fallback)` dùng `??`
- Câu hỏi: `a || b || c` vs `a ?? b ?? c` khác nhau như thế nào?
