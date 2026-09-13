# Type Conversion vs Coercion

|  | Conversion (Explicit) | Coercion (Implicit) |
|---|---|---|
| Ai làm | developer | engine |
| Ví dụ | `String(123)` | `"5" + 3` → `"53"` |

- **Conversion**: chủ động gọi `String()`, `Number()`, `Boolean()`
- **Coercion**: engine tự làm khi `==`, `+`, `if()`

Xem `02_explicit` và `03_implicit`.
