# Khai báo biến (Declarations) — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

**Khai báo biến (declaration)** là hành động tạo ra một biến trong scope hiện tại. **Khởi tạo (initialization)** là gán giá trị đầu tiên cho biến. **Gán lại (assignment)** là đổi giá trị đã có của biến. JavaScript có **3 từ khóa khai báo**: `var`, `let`, `const` — mỗi từ khóa có behavior khác nhau về scope, hoisting, và khả năng gán lại.

```js
let myName;                        // khai báo → giá trị mặc định: undefined
myName = "Chris";                  // khởi tạo (gán giá trị lần đầu)
myName = "Bob";                    // gán lại (assignment)
```

### Bảng so sánh 3 từ khóa

| Đặc điểm | `var` | `let` | `const` |
|----------|-------|-------|---------|
| **Scope** | function scope | block scope `{}` | block scope `{}` |
| **Khai báo lại** | được (không lỗi) | không — SyntaxError | không — SyntaxError |
| **Gán lại giá trị** | được | được | **không** — TypeError |
| **Hoisting** | khai báo kéo lên, giá trị `undefined` | có TDZ → ReferenceError nếu dùng trước | có TDZ → ReferenceError nếu dùng trước |
| **Phải khởi tạo ngay** | không | không | **bắt buộc** |
| **Global object property** | `var x = 1` trong browser → `window.x` | `let x = 1` → không attach vào `window` | same as `let` |

### Dynamic typing trong JavaScript

JS là ngôn ngữ **kiểu động** — biến không khai báo kiểu, và có thể đổi kiểu trong lúc chạy:

```js
let myNumber = "500";   // string
typeof myNumber;        // "string"
myNumber = 500;         // number
typeof myNumber;        // "number"
myNumber = [1, 2, 3];   // array
typeof myNumber;        // "object"
```

### Gán cho biến chưa khai báo — strict mode bảo vệ bạn

```js
// Non-strict mode: tự động tạo biến global (việc xấu!)
num = 5;              // tạo window.num = 5 — ngầm!
console.log(num);     // 5

// Strict mode: bắt lỗi ngay
"use strict";
num = 5;              // ❌ ReferenceError: num is not defined
```

### `const` với object/array — khóa tham chiếu, không khóa nội dung

```js
const bird = { species: "Kestrel" };
bird.species = "Striated Caracara"; // ✅ OK — sửa thuộc tính bên trong object
bird.color = "brown";               // ✅ OK — thêm thuộc tính mới
// bird = {};                       // ❌ TypeError: Assignment to constant variable

const numbers = [1, 2, 3];
numbers.push(4);         // ✅ OK — mutate array (push thay đổi nội dung)
// numbers = [5, 6];     // ❌ TypeError — không gán lại được tham chiếu
```

### Kiểm tra biến có tồn tại — dùng `typeof`

```js
var x = 10;
console.log(typeof x !== "undefined");  // true — biến tồn tại

console.log(typeof z !== "undefined");  // false — z chưa bao giờ khai báo
// Không lỗi ReferenceError vì typeof an toàn với undeclared variables
```

## 📐 Cấu trúc nhóm

```
01_variables/01_declarations/
├── README.md                 ← bài tổng quan var/let/const
└── 01_let-and-const/         ← let/const chi tiết hơn
    ├── README.md
    ├── app.js
    └── index.html
```

## ✅ Điểm mạnh — Tại sao nên học kỹ

| # | Điểm mạnh | Lý do |
|---|-----------|-------|
| 1 | **`let`/`const` an toàn hơn `var`** | Block scope + chống khai báo trùng → ít bug hơn hẳn |
| 2 | **`const` biểu đạt ý định rõ ràng** | Người đọc biết ngay "đây là tham chiếu không đổi" |
| 3 | **Dynamic typing linh hoạt** | Không cần viết boilerplate kiểu, rapid prototyping nhanh |
| 4 | **`typeof` an toàn** | Kiểm tra biến tồn tại mà không gây ReferenceError |
| 5 | **Strict mode bảo vệ** | Ngăn accidental global variables, phát hiện lỗi sớm |
| 6 | **3 từ khóa ngắn gọn** | Phù hợp cả script ngắn lẫn dự án lớn (kết hợp TypeScript khi cần) |

## ⚠️ Bẫy thường gặp & Hạn chế

| # | Bẫy | Ví dụ code | Cách tránh |
|---|-----|-----------|-----------|
| 1 | **`var` nhảy ra khỏi block `{}`** | `if(true){ var x=1 }; console.log(x)` → `1` — `var` thoát block! | Dùng `let`/`const` |
| 2 | **TDZ với `let`/`const`** | `console.log(x); let x = 1;` → `ReferenceError` | Khai báo trước khi dùng |
| 3 | **`const` object vẫn mutate được** | `const a = {}; a.x = 1;` — OK! Không phải "bất biến" | Dùng `Object.freeze()` nếu cần immutable thật sự |
| 4 | **Dynamic typing ẩn bug** | `let x = 5; x = "hello"; x + 1` → `"hello1"` | Dùng TypeScript hoặc `typeof` check trước khi cộng |
| 5 | **Không khởi tạo `const`** | `const x;` → `SyntaxError` | Luôn gán giá trị ngay khi khai báo `const` |
| 6 | **Khai báo lại `let` trong cùng scope** | `let x = 1; let x = 2;` → `SyntaxError` | Gán lại `x = 2` thay vì `let x = 2` |

## 💡 Khi nào dùng — Tình huống thực tế

1. **Giá trị không đổi tham chiếu** (config, DOM element, hằng số) → `const`.
2. **Biến cần gán lại** (bộ đếm, biến lặp, trạng thái thay đổi) → `let`.
3. **Không bao giờ dùng `var`** trong code mới — trừ khi bảo trì legacy code hoặc hỗ trợ trình duyệt rất cũ (IE11).
4. **Kiểm tra biến tồn tại hay không** → `typeof` (an toàn hơn `if (x)` vì `typeof undeclaredVar` không lỗi).
5. **Strict mode project** → `"use strict";` ở đầu file để ngăn accidental globals.
6. **Immutable data cần thiết** → `const` + `Object.freeze()` cho object, hoặc array copy trước mutate.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: So sánh var, let, const trong cùng scenario

```js
// var: function-scoped, có thể khai báo lại, gán lại được
var x = 10;
var x = 20;         // ✅ không lỗi — khai báo lại
console.log(x);     // 20

// let: block-scoped, không khai báo lại được, gán lại được
let y = 10;
// let y = 20;      // ❌ SyntaxError: Identifier 'y' has already been declared
y = 20;             // ✅ gán lại được
console.log(y);     // 20

// const: block-scoped, không khai báo lại, không gán lại
const a = 11;
// a = 12;          // ❌ TypeError: Assignment to constant variable
// const a = 13;    // ❌ SyntaxError: Identifier 'a' has already been declared
console.log(a);     // 11
```

### Ví dụ 2: const với object và array

```js
// Object: const khóa tham chiếu, nội dung vẫn đổi được
let dog = { name: "Spot", breed: "Dalmatian" };
console.log(dog.name);      // "Spot"
dog.name = "Rex";           // ✅ sửa thuộc tính
console.log(dog.name);      // "Rex"
// dog = {};                // ❌ TypeError

// Array: const khóa tham chiếu, vẫn push/pop được
const scores = [85, 90, 78];
scores.push(95);            // ✅ thêm phần tử
console.log(scores);        // [85, 90, 78, 95]
// scores = [];             // ❌ TypeError

// Object.freeze() — tạo immutable shallow copy
const frozen = Object.freeze({ name: "immutable" });
frozen.name = "changed";    // silently fails in strict mode
console.log(frozen.name);   // "immutable" — không đổi
```

### Ví dụ 3: Dynamic typing — biến đổi kiểu tự do

```js
let mixed = "chuỗi ban đầu";
console.log(typeof mixed);   // "string"

mixed = 42;
console.log(typeof mixed);   // "number"

mixed = true;
console.log(typeof mixed);   // "boolean"

mixed = null;
console.log(typeof mixed);   // "object" — typeof null === "object" (bug lịch sử)

mixed = undefined;
console.log(typeof mixed);   // "undefined"
```

### Ví dụ 4: Strict mode — bảo vệ khỏi accidental globals

```js
"use strict";

// Non-strict: num tự động trở thành global property
// num = 5;  // nếu bỏ "use strict", dòng này tạo window.num

// Strict: phải khai báo biến trước khi gán
let num = 5;
num = 10;         // ✅ gán lại
console.log(num); // 10

// var trong strict mode vẫn hoạt động nhưng vẫn function-scoped
var legacy = "ES5";
console.log(legacy); // "ES5"
```

### Ví dụ 5: Kiểm tra tồn tại biến với typeof

```js
// typeof an toàn với undeclared variable — không gây ReferenceError
console.log(typeof stillUndeclared);  // "undefined"
console.log(typeof stillUndeclared !== "undefined"); // false

// So sánh với truy cập trực tiếp — sẽ lỗi
// console.log(stillUndeclared);      // ❌ ReferenceError

// Pattern phổ biến: kiểm tra trước khi dùng
if (typeof myConfig !== "undefined") {
  console.log(myConfig.theme);
} else {
  console.log("Không có config, dùng default");
}
```

## 🔬 So sánh với alternatives

| Phương án | Ưu điểm | Nhược điểm | Phù hợp khi |
|-----------|---------|------------|-------------|
| **`let`/`const` (ES6+)** | Block scope, TDZ an toàn, hiện đại | Không support IE11 | Mọi project hiện đại |
| **`var` (ES5)** | Hỗ trợ mọi browser | Function scope, hoisted về undefined, dễ gây bug | Legacy codebase, IE11 support |
| **TypeScript `let`/`const`** | Static type + block scope | Cần transpile, học curve cao | Project lớn, enterprise |
| **Global variables** | Truy cập mọi nơi | Ô nhiễm namespace, khó debug, memory leak | Quick prototype, not production |
| **Module-scoped const** | Encapsulation tự nhiên | Cần setup module system | Library, package development |

## 📊 Performance & Best Practices

- **Mặc định dùng `const`** — nếu không cần gán lại, `const` giúp code an toàn hơn và dễ đọc hơn.
- **Chỉ dùng `let`** khi chắc chắn biến cần gán lại (bộ đếm `for`, biến trạng thái).
- **Không bao giờ dùng `var`** — block scope của `let`/`const` an toàn hơn hẳn, engine tối ưu tốt hơn.
- **Luôn khởi tạo `const`** — cú pháp bắt buộc, tránh SyntaxError.
- **Dùng `"use strict"`** ở đầu file — phát hiện accidental globals, tăng tốc JIT compilation.
- **Kết hợp ESLint** — rule `prefer-const`, `no-var`, `no-undef` enforce best practices tự động.
- **Tránh dynamic typing lạm dụng** — nếu code liên tục đổi kiểu, cân nhắc TypeScript để catch lỗi compile-time.

## 🔗 Liên kết chéo

- Xem thêm: `01_variables/01_declarations/01_let-and-const/` — let/const block scope, TDZ chi tiết
- Xem thêm: `01_variables/02_hoisting/` — hoisting cơ chế hoạt động
- Xem thêm: `01_variables/03_scopes/` — global, block, function scope
- Xem thêm: `01_variables/04_naming-and-practices/` — quy tắc đặt tên
- Xem thêm: `02_data-types/01_primitive-types/03_value-vs-reference/` — value vs reference assignment
- Tài liệu: [MDN — var](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/var), [MDN — let](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/let), [javascript.info/var](https://javascript.info/var)
