# Logical OR / AND Short-Circuit

## Khái niệm

`&&` và `||` trong JS không chỉ trả boolean -- chúng **trả về operand thực tế** (short-circuit evaluation):

| Operator | Logic | Return |
|---|---|---|
| `a && b` | Nếu `a` falsy --> `a`, còn lại --> `b` | Operand cuối cùng |
| `a || b` | Nếu `a` truthy --> `a`, còn lại --> `b` | Operand đầu tiên truthy |
| `a ?? b` | Nếu `a` null/undefined --> `b`, còn lại --> `a` | Operand first non-nullish |

Falsy values: `false`, `0`, `""`, `null`, `undefined`, `NaN`

## Điểm mạnh

- Gọn điều kiện trong 1 dòng
- Default value pattern: `const val = input || "default"`
- Conditional render: `isLoggedIn && <Dashboard />`

## Bẫy thường gặp

### Bẫy 1: || coi 0, "", false là falsy
```js
const count = 0;
const result = count || 10; // 10 -- SAI! 0 là hợp lệ
const result2 = count ?? 10; // 0 -- Đúng
```

### Bẫy 2: && không short-circuit nếu vế trái truthy
```js
function risky() { console.log("called"); return true; }
false && risky(); // "called" KHÔNG log -- short-circuit đúng
true && risky();  // "called" LOG -- vế phải vẫn evaluate
```

### Bẫy 3: Precedence && > ||
```js
const result = a || b && c;
// JavaScript parse: a || (b && c) -- KHÔNG phải (a || b) && c
// Cần dấu ngoặc nếu muốn group khác
```

## Khi nào dùng

- Default parameter (tương đương `??` với nullable)
- Conditional rendering (React, JSX)
- Guard clause early return
- Falsy check tổng quát

## Ví dụ

```js
// || default value
const port = process.env.PORT || 3000;
const name = userInput || "Anonymous";

// && conditional render (React pattern)
const UserDashboard = ({ isAdmin }) => (
  <div>
    {isAdmin && <AdminPanel />}
    {user && <Welcome name={user.name} />}
  </div>
);

// && guard clause
function processUser(user) {
  if (!user) return null; // tương đương: user && ...
  return user.name.toUpperCase();
}

// Phân biệt || vs ??
const count = 0;
console.log(count || 10);   // 10  <-- Sai: 0 là hợp lệ
console.log(count ?? 10);   // 0   <-- Đúng

// Ứng dụng thực tế: feature detection
const storage = window.localStorage || sessionStorage;
const logger = config.logger || console;
```

## Liên kết chéo

- Xem: `20_modern-javascript/03_optional-chaining-nullish/02_nullish-coalescing`
- Xem: `08_expressions-and-operators/01_operators`
