# 01. Biến (Variables) — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

**Biến (variable)** là một "chiếc hộp có tên" dùng để **lưu trữ giá trị** trong chương trình: số, chuỗi, mảng, object… Thay vì viết đi viết lại một giá trị, bạn gán nó vào biến và dùng tên biến ở mọi nơi. Biến là **đơn vị cơ bản nhất** của mọi ngôn ngữ lập trình — hiểu biến là hiểu nền tảng để viết code đúng và an toàn.

```js
let tuoi = 20;
console.log(tuoi);   // 20
tuoi = 21;           // gán lại giá trị (assignment)
console.log(tuoi);   // 21
```

**Lưu ý quan trọng:** Biến **không phải là giá trị** — nó là chỗ đứng (container/reference) chứa giá trị. Khi bạn viết `let a = 1; let b = a;`, với primitive thì `b` nhận **bản sao giá trị**, thay đổi `a` sau đó không ảnh hưởng `b`. Với object thì `b` nhận **tham chiếu** đến cùng object — sửa `b` sẽ thấy ở `a`. Xem chi tiết ở `02_data-types/01_primitive-types/03_value-vs-reference/`.

Nhóm này trả lời 4 câu hỏi cốt lõi:

1. **Khai báo như thế nào?** — `var` (ES5, nên tránh), `let`, `const` (ES6, ưu tiên dùng). Xem: `01_declarations/`.
2. **Hoisting hoạt động ra sao?** — vì sao `var` in ra `undefined` còn `let`/`const` báo `ReferenceError`. Xem: `02_hoisting/`.
3. **Scope (phạm vi) ảnh hưởng thế nào?** — global, block scope, function scope. Xem: `03_scopes/`.
4. **Đặt tên thế nào cho chuẩn?** — camelCase, tránh keyword, mô tả đúng ý nghĩa. Xem: `04_naming-and-practices/`.

Bởi JavaScript là **ngôn ngữ kiểu động** (dynamic typing), một biến có thể đổi kiểu khi chạy: `let x = 5; x = "hello";` hợp lệ. Việc khai báo đúng cách (ưu tiên `const`/`let`) là nền tảng để tránh vô số bug về sau.

## 📐 Cấu trúc nhóm

```
01_variables/
├── README.md                 ← bài tổng quan này
├── 01_declarations/
│   ├── README.md             ← var vs let vs const
│   └── 01_let-and-const/     ← let/const chi tiết, block scope, TDZ
├── 02_hoisting/              ← hoisting mechanism, TDZ
├── 03_scopes/                ← global, block, function scope
└── 04_naming-and-practices/  ← quy tắc đặt tên, best practices
```

## ✅ Điểm mạnh — Tại sao nên học kỹ

| # | Lợi ích | Khi nào quan trọng |
|---|---------|-------------------|
| 1 | **Code rõ ràng hơn** | Tên biến mô tả đúng dữ liệu nó chứa → đọc code như đọc văn |
| 2 | **`const`/`let` có block scope** | Thay thế `var` rối rắm — biến chỉ tồn tại trong khối `{}` mong muốn |
| 3 | **Hiểu hoisting + TDZ** | Tránh được các lỗi `ReferenceError` khó hiểu khi debug |
| 4 | **Nắm scope** | Viết được hàm không bị "ô nhiễm" biến toàn cục |
| 5 | **Tái sử dụng giá trị** | Dễ bảo trì, dễ gỡ lỗi — log tên biến rõ nghĩa thay vì hardcode |
| 6 | **Phân biệt giá trị/tham chiếu** | Tránh bug "sửa copy làm đổi gốc" — cần biết primitive vs object |
| 7 | **Viết code an toàn hơn** | `const` ngăn gán lại vô tình — phát hiện lỗi sớm |

## ⚠️ Bẫy thường gặp & Hạn chế

| # | Bẫy | Ví dụ code | Cách tránh |
|---|-----|-----------|-----------|
| 1 | **Dùng `var` trong code hiện đại** | `for(var i=0;i<3;i++){}; console.log(i)` → `i` vẫn tồn tại sau loop | Luôn dùng `let`/`const`, config ESLint `no-var` |
| 2 | **Truy cập biến `let`/`const` trước khai báo** | `console.log(x); let x = 1;` → `ReferenceError` (TDZ) | Khai báo biến trước khi dùng |
| 3 | **Hiểu sai `const` với object** | `const obj = {}; obj.x = 1;` — vẫn đổi được thuộc tính! | `const` chỉ khóa **tham chiếu**, không khóa nội dung |
| 4 | **Gán cho biến chưa khai báo trong strict mode** | `"use strict"; num = 5;` → `ReferenceError` | Luôn khai báo `let`/`const` trước khi gán |
| 5 | **Khai báo trùng trong cùng scope** | `let x = 1; let x = 2;` → `SyntaxError` | Dùng tên khác hoặc gán lại `x = 2` |
| 6 | **Biến global vô tình leaking** | `count = 0;` (thiếu `let`) → tạo biến global ngầm | `"use strict"` + ESLint `no-undef` |
| 7 | **Shadowing vô tình** | `let x = 1; if(true){ let x = 2; } console.log(x)` → `1` — không lỗi nhưng dễ nhầm | Tránh đặt tên trùng trong nested scope |

## 💡 Khi nào dùng — Tình huống thực tế

1. **Bất kỳ lúc nào cần lưu và tái sử dụng một giá trị** — bộ đếm, trạng thái, config.
2. **Đếm số lần lặp, đếm số click** — dùng `let` vì cần gán lại.
3. **Lưu cấu hình không đổi** — `const API_URL = "https://...";` dùng `const`.
4. **Lưu kết quả DOM query** — `const btn = document.querySelector('#btn');` dùng nhiều lần.
5. **Lặp qua mảng bằng `for...of`** — `for (const item of arr)` — `const` đủ vì không gán lại.
6. **State trong React component** — `const [count, setCount] = useState(0);` — hook pattern dùng const cho state variable.
7. **Configuration constants** — `const MAX_RETRIES = 3;` — `const` + UPPER_SNAKE_CASE.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Khai báo + khởi tạo + gán lại

```js
// Khai báo và khởi tạo cùng lúc
let count = 0;
console.log(count);  // 0

// Gán lại (assignment)
count += 1;          // tương đương count = count + 1
console.log(count);  // 1

// const: không gán lại được
const PI = 3.14159;
// PI = 4;            // TypeError: Assignment to constant variable
```

### Ví dụ 2: const với object — hiểu rõ "tham chiếu" vs "giá trị"

```js
// const khóa THAM CHIẾU, không khóa NỘI DUNG
const user = { name: "Nam", age: 25 };

user.name = "Hoa";   // ✅ OK — sửa thuộc tính bên trong object
user.age = 26;       // ✅ OK — thêm/sửa thuộc tính
console.log(user);   // { name: 'Hoa', age: 26 }

// user = {};         // ❌ TypeError: Assignment to constant variable
```

### Ví dụ 3: var vs let — block scope difference

```js
// var: function-scoped, thoát khỏi block
if (true) {
  var legacy = "ES5";
}
console.log(legacy);   // "ES5" — var thoát khỏi if!

// let: block-scoped, chỉ tồn tại trong {}
if (true) {
  const modern = "ES6+";
}
// console.log(modern);  // ❌ ReferenceError: modern is not defined
```

### Ví dụ 4: Dynamic typing — biến đổi kiểu linh hoạt

```js
let data = "chuỗi ban đầu";
console.log(typeof data);  // "string"

data = 42;                  // giờ là number
console.log(typeof data);  // "number"

data = { key: "value" };    // giờ là object
console.log(typeof data);  // "object"
// Không có lỗi nào — JS là dynamic typing
```

### Ví dụ 5: TDZ — Temporal Dead Zone

```js
// let/const có TDZ: từ đầu scope đến dòng khai báo
console.log(x);  // ❌ ReferenceError: Cannot access 'x' before initialization
let x = 10;

// var không có TDZ — hoisted về undefined
console.log(y);  // undefined (không lỗi!)
var y = 20;
```

## 🔬 So sánh với alternatives

| Phương án | Ưu điểm | Nhược điểm |
|-----------|---------|------------|
| **`let`/`const` (ES6+)** | Block scope, TDZ an toàn, hiện đại | Không support IE11 |
| **`var` (ES5)** | Hỗ trợ mọi browser | Function scope, hoisted về undefined, dễ gây bug |
| **TypeScript `let`/`const`** | Static type + block scope | Cần transpile, học curve cao hơn |
| **Global variables** | Truy cập mọi nơi | Ô nhiễm namespace, khó debug, memory leak |
| **Module-scoped const** | Encapsulation tự nhiên | Cần setup module system |

## 📊 Performance & Best Practices

- **Mặc định dùng `const`** — nếu không cần gán lại, `const` là lựa chọn an toàn nhất.
- **Chỉ dùng `let`** khi chắc chắn biến cần gán lại (bộ đếm, biến lặp `for`).
- **Không bao giờ dùng `var`** — block scope của `let`/`const` an toàn hơn hẳn, engine tối ưu tốt hơn.
- **Luôn khởi tạo `const`** — cú pháp bắt buộc, tránh SyntaxError.
- **Dùng `"use strict"`** ở đầu file — phát hiện accidental globals, tăng tốc JIT compilation.
- **Kết hợp ESLint** — rule `prefer-const`, `no-var`, `no-undef` enforce best practices tự động.
- **Tránh dynamic typing lạm dụng** — nếu code liên tục đổi kiểu, cân nhắc TypeScript để catch lỗi compile-time.

## 🔗 Liên kết chéo

- Xem thêm: `01_variables/01_declarations/` — var vs let vs const so sánh chi tiết
- Xem thêm: `01_variables/01_declarations/01_let-and-const/` — let/const block scope, TDZ chi tiết
- Xem thêm: `01_variables/02_hoisting/` — hoisting cơ chế hoạt động
- Xem thêm: `01_variables/03_scopes/` — global, block, function scope
- Xem thêm: `01_variables/04_naming-and-practices/` — quy tắc đặt tên
- Xem thêm: `02_data-types/01_primitive-types/03_value-vs-reference/` — value vs reference assignment
- Tài liệu: [MDN — var](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/var), [MDN — let](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/let), [javascript.info/variables](https://javascript.info/variables)
