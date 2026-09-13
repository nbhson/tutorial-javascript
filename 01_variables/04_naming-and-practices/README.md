# Quy tắc đặt tên biến & Best Practices — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

Tên biến là **"giấy tờ tùy thân"** của dữ liệu trong code. JavaScript có **quy tắc hợp lệ** (cú pháp — vi phạm là lỗi) và **quy ước hay** (thói quen — vi phạm thì chạy được nhưng code khó đọc). Nhóm bài này tập trung vào cả hai khía cạnh.

### Quy tắc hợp lệ (Rules — bắt buộc, vi phạm = SyntaxError)

| Quy tắc | Mô tả | Ví dụ đúng | Ví dụ sai |
|---------|-------|-----------|-----------|
| **Ký tự hợp lệ** | Chỉ dùng `a-z A-Z`, `0-9`, `_`, `$` | `userName`, `total_1` | `my name`, `1a` |
| **Không bắt đầu bằng số** | Ký tự đầu phải là chữ, `_`, hoặc `$` | `_temp`, `$elem` | `1a`, `2ndPlace` |
| **Không chứa khoảng trắng** | Dấu `-` bị hiểu là phép trừ | `myVariable` | `my-variable` |
| **Không trùng reserved keyword** | `var`, `let`, `const`, `class`, `function`, `return`, `if`, `else`, `for`, `while`, `new`, `this`, `true`, `false`, `null`, `undefined`, `typeof`, `instanceof`, `throw`, `try`, `catch`, `finally`, `switch`, `case`, `break`, `continue`, `default`, `do`, `in`, `of`, `yield`, `import`, `export`, `extends`, `super`, `implements`, `interface`, `package`, `private`, `protected`, `public`, `static`, `await`, `async` | `let data = 1;` | `let class = 1;` ❌ SyntaxError |
| **Phân biệt hoa/thường** | `myAge` ≠ `myage` ≠ `MYAGE` | `userCount`, `UserCount` | — |

```js
let $ = 1;    // hợp lệ (hiếm dùng — xung đột jQuery)
let _ = 2;    // hợp lệ (thường cho biến "bỏ qua" trong destructuring)
let _tmp = 3; // hợp lệ
```

### Quy ước đặt tên (Conventions — khuyến nghị, vi phạm = chạy được nhưng khó đọc)

| Pattern | Mục đích | Ví dụ |
|---------|----------|-------|
| **camelCase** | Biến, hàm, method | `userName`, `totalScore`, `getFullName` |
| **PascalCase** | Constructor function, class | `User`, `Product`, `DataLoader` |
| **UPPER_SNAKE_CASE** | Hằng số, configuration | `MAX_SIZE`, `API_URL`, `DEFAULT_TIMEOUT` |
| **snake_case** | (hiếm trong JS, dùng trong SQL/query) | `user_id`, `created_at` |
| **prefix `is/has/can`** | Boolean biến | `isVisible`, `hasPermission`, `canEdit` |
| **prefix `get/set`** | Method truy cập property | `getName()`, `setName()` |
| **prefix `_`** | Private convention (thường bằng ES2022 `#private`) | `_internalCache`, `_tempResult` |

### Best practices chính

1. **Ưu tiên `const` trước, dùng `let` khi cần gán lại, tránh `var`.**
2. **Đặt tên theo ý nghĩa dữ liệu, không theo cách triển khai** — `cart` thay vì `arr2`, `userList` thay vì `data`.
3. **Khai báo biến gần nơi sử dụng nhất** — giảm scope, dễ garbage collect.
4. **Khai báo rõ ràng, có từ khóa** — không phụ thuộc implicit global (`num = 5` trong non-strict mode).
5. **Tên đủ dài để rõ nghĩa, không quá dài đến mức rườm rà** — `userAge` tốt hơn `x`, nhưng `numberOfUsersInTheSystem` có thể viết tắt thành `userCount`.

## 📐 Cấu trúc nhóm

```
01_variables/04_naming-and-practices/
└── README.md         ← bài này (không có file app.js riêng)
```

## ✅ Điểm mạnh — Tại sao đặt tên quan trọng

| # | Điểm mạnh | Lý do |
|---|-----------|-------|
| 1 | **Tên tốt giúp code tự giải thích** | Giảm comment thừa, đọc là hiểu — "self-documenting code" |
| 2 | **Tránh lỗi cảnh báo từ linter** | ESLint: `camelcase`, `no-undef`, `prefer-const` — enforce rules tự động |
| 3 | **`const` + tên mô tả giúp người khác nắm ý định** | Nhìn dòng khai báo đã hiểu ngay biến dùng để làm gì |
| 4 | **Tên nhất quán giúp tìm kiếm (grep) dễ** | `grep -r "userName"` tìm được mọi nơi dùng biến này |
| 5 | **Tránh shadowing/trùng tên gây bug** | Tên rõ ràng → ít khả năng đặt trùng trong scope lồng nhau |
| 6 | **Hỗ trợ autocomplete trong IDE** | Tên rõ nghĩa → IDE gợi ý đúng → coding faster |
| 7 | **Code review nhanh hơn** | Reviewer hiểu ý định từ tên, không phải đọc logic |

## ⚠️ Bẫy thường gặp & Hạn chế

| # | Bẫy | Ví dụ | Cách tránh |
|---|-----|-------|-----------|
| 1 | **Tên quá dài** | `thisIsAReallyLongVariableNameLord` | Đủ rõ, không quá dài — `userRole` thay vì `userAccessRoleInSystem` |
| 2 | **Tên 1 ký tự hoặc chung chung** | `let x = 5;`, `let data = "abc"` | `let score = 5;`, `let userName = "abc"` |
| 3 | **`$`/`_` đứng đầu xung đột thư viện** | jQuery dùng `$`, underscore dùng `_` | Tránh dùng prefix này trừ khi có lý do |
| 4 | **Tên không phản ánh hành vi** | `let temp = doSomething()` — `temp` nghĩa là gì? | `let result = doSomething()` |
| 5 | **Inconsistent naming trong team** | Một người `userName`, người khác `username` | Đặt rule trong ESLint config, enforce by PR review |
| 6 | **Dùng keyword làm tên** | `let class = "JS";` | ESLint `no-reserved-keys` hoặc kiểm tra manual |
| 7 | **Mixed case style** | `userName`, `user_Name`, `UserName` — lộn xộn | Chọn camelCase hoặc PascalCase và tuân thủ |

## 💡 Khi nào dùng — Tình huống thực tế

1. **Khai báo biến mới bất kỳ** — ưu tiên `const` + tên mô tả rõ hành vi/dữ liệu.
2. **Hằng số cấu hình app** — `UPPER_SNAKE_CASE`: `API_BASE_URL`, `MAX_RETRY_COUNT`.
3. **Làm việc nhóm / open source** — tuân thủ chặt chẽ rules + conventions, đặt trong ESLint/Prettier config.
4. **Viết test** — tên biến trong test phản ánh scenario: `expectedError`, `actualResult`, `mockResponse`.
5. **Viết hàm tái sử dụng** — tên hàm = verb + noun: `getUserById`, `calculateTotal`, `formatDate`.
6. **Boolean flags** — prefix `is/has/can`: `isLoading`, `hasPermission`, `canDelete`.
7. **DOM elements** — prefix `el` hoặc suffix `Ref`: `submitBtn`, `formEl`, `containerRef`.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Tên tốt vs tên kém

```js
// ❌ Kém — không rõ nghĩa
let x = 5;
let data = "abc";
let arr2 = [1, 2];
let temp = someFunction();

// ✅ Tốt — tên mô tả rõ dữ liệu/hành vi
let score = 5;
let userName = "abc";
let secondaryArray = [1, 2];
let result = someFunction();
```

### Ví dụ 2: camelCase vs PascalCase vs UPPER_SNAKE

```js
// camelCase — biến và hàm
let userCount = 5;
let totalScore = 0;
function calculateTotal(items) { return items.reduce((s, i) => s + i.price, 0); }

// PascalCase — class/constructor
class User { constructor(name) { this.name = name; } }
const product = new Product();

// UPPER_SNAKE_CASE — hằng số
const MAX_RETRY_COUNT = 3;
const API_BASE_URL = "https://api.example.com";
const DEFAULT_TIMEOUT_MS = 5000;
```

### Ví dụ 3: Prefix conventions

```js
// Boolean — prefix is/has/can
let isVisible = true;
let hasPermission = false;
let canEdit = true;

// DOM elements — suffix Ref hoặc prefix el
const submitBtn = document.getElementById("submit");
const formEl = document.querySelector("form");
const containerRef = useRef(null);  // React

// Private convention (pre-ES2022) — prefix _
let _internalCache = {};
function _helper() { /* private logic */ }

// ES2022+ private fields — # prefix (true private)
class Counter {
  #count = 0;                    // private field
  increment() { this.#count++; }
  get count() { return this.#count; }
}
```

### Ví dụ 4: Quy tắc hợp lệ — thử các trường hợp

```js
// ✅ Hợp lệ
let validName1 = "okay";
let valid_name2 = "okay";
let valid$name3 = "okay";
let _private = "okay";
let $jQueryLike = "okay";

// ❌ Không hợp lệ — SyntaxError
// let 1invalid = "no";           // không bắt đầu bằng số
// let my-name = "no";            // dấu - là phép trừ
// let class = "no";              // reserved keyword
// let my name = "no";            // khoảng trắng
```

### Ví dụ 5: ESLint config enforcement

```json
// .eslintrc.json
{
  "rules": {
    "camelcase": ["error", { "properties": "always" }],
    "prefer-const": "error",
    "no-var": "error",
    "no-undef": "error",
    "no-shadow": "warn"
  }
}
```

## 🔬 So sánh với alternatives

| Phương án | Ưu điểm | Nhược điểm |
|-----------|---------|------------|
| **camelCase (JavaScript standard)** | Phổ biến nhất, IDE hỗ trợ tốt | Không phù hợp với naming convention của ngôn ngữ khác (Python snake_case) |
| **PascalCase cho class** | Phân biệt rõ function vs constructor | Có thể nhầm với regular function naming |
| **UPPER_SNAKE cho constants** | Dễ nhận diện hằng số | Không enforced bởi engine — chỉ là convention |
| **TypeScript naming** | Type annotation thêm thông tin | Learning curve cao hơn |
| **Linter enforcement (ESLint)** | Tự động enforce rules | Cần config, có thể gây tranh cãi trong team |

## 📊 Performance & Best Practices

- **Dùng ESLint `camelcase`, `prefer-const`, `no-var`** — enforce naming + declaration rules tự động.
- **Prettier kết hợp ESLint** — format code nhất quán (indent, quotes, semicolons) + naming rules.
- **Đặt tên theo hành vi/dữ liệu, không theo implementation** — `userList` tốt hơn `arr2`, `formattedDate` tốt hơn `str`.
- **Giữ tên dưới 30 ký tự** — đủ rõ nghĩa nhưng không rườm rà; tránh `thisIsAReallyLongVariableName`.
- **One true naming convention per team** — quyết định trong team và document trong CONTRIBUTING.md / style guide.
- **Avoid `$` và `_` prefix trừ khi cần thiết** — xung đột với thư viện phổ biến (jQuery, lodash).
- **Boolean prefix `is/has/can`** — giúp reader hiểu ngay biến là flag, không phải dữ liệu thông thường.
- **Test file naming** — `component.test.js`, `utils.spec.js` — convention chung trong ecosystem.

## 🔗 Liên kết chéo

- Xem thêm: `01_variables/01_declarations/` — var vs let vs const quy tắc khai báo
- Xem thêm: `01_variables/01_declarations/01_let-and-const/` — const + tên descriptive best practice
- Xem thêm: `01_variables/02_hoisting/` — hoisting + naming (function declaration hoist nên có tên rõ)
- Xem thêm: `01_variables/03_scopes/` — scope rules ảnh hưởng naming (avoid shadowing)
- Xem thêm: `08_expressions-and-operators/` — operator naming convention (`+=`, `-=`, `++`, `--`)
- Tài liệu: [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript), [Google JavaScript Style Guide](https://google.github.io/styleguide/jsguide.html), [MDN — Naming conventions](https://developer.mozilla.org/en-US/docs/Glossary/Identifier)
