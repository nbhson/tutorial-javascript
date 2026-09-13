# Logical OR / AND Short-Circuit

## 🔑 Khái niệm

`&&` và `||` trong JS không chỉ trả boolean — chúng **trả về operand thực tế** (short-circuit evaluation):

| Operator | Logic | Return |
|---|---|---|
| `a && b` | Nếu `a` falsy → `a`, còn lại → `b` | Operand cuối cùng |
| `a \|\| b` | Nếu `a` truthy → `a`, còn lại → `b` | Operand đầu tiên truthy |
| `a ?? b` | Nếu `a` null/undefined → `b`, còn lại → `a` | Operand first non-nullish |

Falsy values: `false`, `0`, `""`, `null`, `undefined`, `NaN`

## ✅ Điểm mạnh
- Gọn điều kiện trong 1 dòng
- Default value pattern: `const val = input || "default"`
- Conditional render: `isLoggedIn && <Dashboard />`

## ⚠️ Lưu ý
- `||` coi `0`, `""`, `false` là falsy → có thể gây bug nếu những giá trị này hợp lệ
- `??` an toàn hơn khi muốn giữ `0`, `""`, `false`
- `&&` không short-circuit nếu vế trái truthy → vế phải **vẫn evaluate**

## 💡 Khi nào dùng
- Default parameter (tương đương `??` với nullable)
- Conditional rendering (React, JSX)
- Guard clause early return

## 🎯 Ví dụ minh họa

### || default value
```js
const port = process.env.PORT || 3000;
const name = userInput || "Anonymous";
```

### && conditional render
```js
const UserDashboard = ({ isAdmin }) => (
  <div>
    {isAdmin && <AdminPanel />}
    {user && <Welcome name={user.name} />}
  </div>
);
```

### && guard clause
```js
function processUser(user) {
  if (!user) return null; // tương đương: user && ...
  return user.name.toUpperCase();
}
```

### Phân biệt || vs ??
```js
const count = 0;
console.log(count || 10);   // 10  ← Sai: 0 là hợp lệ
console.log(count ?? 10);   // 0   ← Đúng
```

## 📚 Tham khảo & Bài tập
- File: `app.js`, `index.html` trong folder `01_logical-or/`
- Thực hành: viết hàm `findFirstTruthy(arr, predicate)` dùng &&
- Câu hỏi: `a && b || c` evaluated như thế nào? Thứ tự precedence ra sao?
