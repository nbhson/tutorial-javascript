# Nullish Coalescing (??)

## Khái niệm

`a ?? b` trả về `b` **chỉ khi** `a` là `null` hoặc `undefined`. Khác với `||` -- `||` trả `b` khi `a` là **bất kỳ falsy value** nào (`0`, `""`, `false`, `NaN`).

```js
0 ?? 10            // 0  (giữ nguyên vì 0 không phải null/undefined)
"" ?? "default"    // ""
false ?? true      // false
null ?? "fallback" // "fallback"
undefined ?? "fallback" // "fallback"
```

## Điểm mạnh

- Phân biệt đúng `null`/`undefined` vs giá trị hợp lệ (0, "", false)
- Mặc định value an toàn cho form input, config
- Thay thế pattern `var = var || default` gây bug

## Bẫy thường gặp

### Bẫy 1: Precedence thấp hơn && / ||
```js
const result = a && b ?? c;
// JavaScript parse là: a && (b ?? c) -- KHÔNG phải (a && b) ?? c
// Cần dấu ngoặc nếu muốn group khác
const result = (a && b) ?? c;
```

### Bẫy 2: Không thay thế || cho mọi trường hợp
```js
// Nếu muốn bỏ TẤT CẢ falsy (包括 0, "", false) --> dùng ||
const input = "" || "default"; // "default" <-- có thể đúng hoặc sai tùy ngữ cảnh
const input = "" ?? "default"; // "" <-- giữ empty string hợp lệ
```

## Khi nào dùng

- Default config value cho số (0 là hợp lệ)
- Form input default text
- API response fallback
- Kết hợp với optional chaining: `user?.name ?? "Guest"`

## Ví dụ

```js
// So sánh ?? vs ||
const count = 0;
console.log(count || 10);   // 10  <-- Sai! 0 là hợp lệ
console.log(count ?? 10);   // 0   <-- Đúng! giữ nguyên 0

const name = "";
console.log(name || "Guest");  // "Guest"
console.log(name ?? "Guest");  // ""  (empty string là hợp lệ)

// Form input default
const age = parseInt(input.value) ?? 0;
const limit = config.limit ?? 100; // giữ 0 nếu config.limit = 0

// Kết hợp với optional chaining
const city = user?.address?.city ?? "Chưa cập nhật";
const theme = settings?.ui?.theme ?? "light";

//实际应用: API response handling
const response = await fetch("/api/user");
const data = await response.json();
const displayName = data?.user?.display_name ?? data?.user?.name ?? "Anonymous";
```

## Liên kết chéo

- Xem: `20_modern-javascript/03_optional-chaining-nullish/01_optional-chaining`
- Xem: `20_modern-javascript/05_misc/01_logical-or` (|| vs &&)
