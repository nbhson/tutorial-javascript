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
- Short-circuit: dừng chain ngay khi gặp nullish

## ⚠️ Bẫy thường gặp

### Bẫy 1: Chỉ check nullish, không check falsy
```js
const obj = { count: 0 };
obj.count?.toFixed(2);  // "0.00" — 0 KHÔNG phải nullish, vẫn access được
obj.missing?.foo;       // undefined — nullish, an toàn
```

### Bẫy 2: Optional call với không phải function
```js
const obj = { prop: "not-a-func" };
obj.prop?.();  // TypeError: obj.prop is not a function
// Chỉ an toàn khi prop tồn tại và là function
```

### Bẫy 3: Không dùng thay thế && cho điều kiện
```js
// ❌ Không nên
if (user?.isAdmin && user.age > 18) { ... }
// ✅ Đúng: dùng && riêng biệt
if (user?.isAdmin === true && user?.age > 18) { ... }
```

## 💡 Khi nào dùng

- Access nested API response có thể thiếu field
- Optional method call
- Safe array access với index có thể out-of-bounds
- Deep property chain với optional segments

## 🎯 Ví dụ

```js
const user = { profile: { name: "A" } };

// Safe nested access
console.log(user?.profile?.name);     // "A"
console.log(user?.address?.city);     // undefined (không lỗi)
console.log(user?.nonExistent);       // undefined

// Optional function call
const obj = { maybeFn: null };
obj.maybeFn?.(); // không lỗi, trả undefined

// Safe array access
const arr = [1, 2, 3];
console.log(arr?.[5]);   // undefined (không lỗi index out of range)
console.log(arr?.length); // 3

// Kết hợp với ??
const userName = user?.name ?? "Guest";
const theme = settings?.ui?.theme ?? "light";

// Optional chaining trong condition
if (user?.permissions?.includes("admin")) {
  showAdminPanel();
}
```

## 🔗 Liên kết chéo
- Xem: `20_modern-javascript/03_optional-chaining-nullish/02_nullish-coalescing`
- Xem: `04_equality-comparisons/01_loose-strict`
