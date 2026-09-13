# Strict Mode (Chế độ nghiêm ngặt) — Thực hành chi tiết — [Level: Intermediate]

## 🔑 Kh khái niệm cốt lõi

Strict mode xuất hiện từ **ES5 (ECMAScript 2009)** với mục đích giúp JavaScript "chặt tay" hơn: **báo lỗi** thay vì âm thầm bỏ qua những tình huống nguy hiểm, từ đó code an toàn và dễ bảo trì hơn.

Bật bằng cách đặt chuỗi **`"use strict";`** ở một trong ba vị trí:
1. **Đầu file** (`app.js`) — áp dụng cho toàn file.
2. **Ngay sau thẻ mở `<script>`** — áp dụng cho cả script đó.
3. **Đầu thân hàm** — chỉ áp dụng trong hàm (local scope).

**Quan trọng**: chuỗi khai báo phải nằm **trước mọi câu lệnh/nhận xét định nghĩa** — nếu phía trước đã có code, nó không có tác dụng.

**Strict mode cấm / báo lỗi khi:**

| Hành động | Ví dụ | Hành vi |
|---|---|---|
| Gán biến chưa khai báo | `x = 100;` | `TypeError: assignment to undeclared variable` |
| `delete` biến, hàm, prototype | `delete women;` | `TypeError` |
| Gán lại thuộc tính `writable: false` | property đóng băng | `TypeError` |
| Gán số octal dạng `010` | `let octal = 010;` | `SyntaxError` |
| Dùng từ khóa nhạy cảm làm tên biến | `let public = 100;` | `SyntaxError` |
| Hàm có hai tham số trùng tên | `function sum(a, a) {}` | `SyntaxError` |
| Khai báo hàm trong block rồi gọi ngoài | `if (true) { function sum(){} } sum();` | `TypeError` (trong strict) |
| `this` không có đối tượng gọi | `function test(){ console.log(this) } test()` | `undefined` (thay vì window) |

**Nguyên nhân cốt lõi**: strict mode **ngăn các lỗi ngầm** (silent errors) của bản thân JS ở thời kỳ đầu — như tự tạo biến global từ một phép gán "lỡ tay", không cho xóa, và **tránh tạo nhiều biến global** (tiết kiệm bộ nhớ).

File `app.js` trong thư mục demo `this` trong strict mode — `test()` in `undefined` thay vì `window/global`.

## 📐 Cấu trúc / Cú pháp

### Bật strict mode
```js
// 1. Toàn file
"use strict";
function example() { /* strict rules apply */ }

// 2. Trong <script> tag
<script>"use strict";</script>

// 3. Trong hàm (local strict)
function localStrict() {
  "use strict";
  // chỉ áp dụng trong hàm này
}
```

### Các hành vi bị cấm
```js
"use strict";

// ❌ Gán biến chưa khai báo
x = 100; // TypeError

// ❌ Delete biến
let v = 10;
delete v; // TypeError

// ❌ Octal literal
let octal = 010; // SyntaxError

// ❌ Duplicate parameters
function sum(a, a) {} // SyntaxError

// ❌ with statement
with (Math) { log(1); } // SyntaxError

// ❌ delete on non-configurable property
const obj = Object.freeze({ a: 1 });
delete obj.a; // TypeError
```

### Thay đổi `this` behavior
```js
"use strict";
function test() {
  console.log(this); // undefined (không phải window/global)
}
test();

// Trong non-strict: this === window (browser) hoặc global (Node)
```

### Functions trong block scope
```js
"use strict";
if (true) {
  function blockFn() { return 42; }
}
// blockFn() có thể throw TypeError trong strict mode
// vì function declaration trong block có behavior không xác định
```

## ✅ Điểm mạnh

1. **Bắt lỗi từ sớm**: tên biến sai chính tả trong phép gán sẽ lỗi ngay thay vì âm thầm tạo biến global mới — prevent hard-to-find bugs.
2. **Ngăn dùng biến global không định trước** → sử dụng bộ nhớ hiệu quả và tránh xung đột tên giữa các script.
3. **Cấm các cú pháp không an toàn** (octal, duplicate params, with statement) → chuẩn hóa code, dễ maintain.
4. **`this` rõ ràng hơn**: hàm thường gọi trực tiếp có `this === undefined`, không ngầm trỏ `window` — prevent accidental global access.
5. **Được toàn bộ mô-đun ES6**, class, và đa số framework tự bật mặc định — học strict mode = học chuẩn hiện đại.
6. **Dễ áp dụng**: chỉ cần một dòng `"use strict";` ở đầu — không cần config phức tạp.
7. **Detects silent failures** — nhiều lỗi từng bị bỏ qua giờ throw exception, giúp developer sửa sớm.
8. **Prevents eval misuse** — `eval` trong strict mode không thể tạo variables trong outer scope.
9. **Better garbage collection** — không tạo biến global vô ý = less memory leak risk.
10. **Self-documenting** — code strict mode thể hiện intent rõ ràng, developer nghiêm túc về quality.

## ⚠️ Bẫy thường gặp & Hạn chế

1. **Chỉ có tác dụng từ vị trí khai báo trở đi** — đặt sau code thì phần trước không bị kiểm soát.
   ```js
   console.log("non-strict part"); // chạy được, không bị check
   "use strict"; // quá muộn cho dòng trên
   x = 100; // TypeError — strict activated from here
   ```

2. **Khác với một số lầm tưởng**: `"use strict"` là **chuỗi**, không phải câu lệnh thông thường; đặt không đúng chỗ sẽ bị bỏ qua im lặng.
   ```js
   // ❌ Không hoạt động — có comment trước
   // "use strict"; ← bị comment out
   function test() {}

   // ✅ Đúng — đứng đầu file, không có gì trước
   "use strict";
   function test() {}
   ```

3. **Kết hợp với code cũ** (viết theo kiểu "xả láng") có thể vỡ vì vô tình vi phạm quy tắc.
   ```js
   // Legacy code không strict
   function oldCode() {
     i = 10; // tạo global i — OK trong non-strict
   }
   // Bật strict + gọi oldCode → TypeError
   "use strict";
   oldCode(); // TypeError: i is not defined
   ```

4. **Các object frozen / `writable: false`** — strict mode sẽ `throw` (chứ không bỏ qua), đừng bất ngờ khi thấy lỗi.
   ```js
   "use strict";
   const obj = Object.defineProperty({}, "x", { value: 1, writable: false });
   obj.x = 2; // TypeError: Cannot assign to read only property 'x'
   ```

5. **Không khắc phục mọi lỗi lập trình** — chỉ giúp phát hiện sớm một lớp lỗi nhất định. Logic error vẫn cần test.
6. **Strict mode trong hàm** không ảnh hưởng outer scope — có thể gây inconsistent behavior.
7. **Class body mặc định strict** — không cần `"use strict";` trong class — nhưng vẫn nên đặt ở đầu file cho clarity.
8. **Module script mặc định strict** — `<script type="module">` auto strict — nhưng IIFE hay inline script thì không.

## 💡 Khi nào dùng

1. **Khởi đầu mọi file script/mô-đun mới** — thói quen tốt mặc định, prevent silent bugs ngay từ đầu.
2. **Sửa bug "biến toàn cục mọc tùy tiện"** trong code cũ — bật strict để find và fix tất cả implicit globals.
3. **Viết thư viện** — ép người dùng khai báo đúng, prevent side effects từ library code.
4. **Học tập để hiểu chính xác hành vi của JS** (đặc biệt về `this`, gán, delete) — strict mode làm rõ behavior.
5. **Trước khi convert sang ES modules** — strict mode là prerequisite cho module system.
6. **Code review checklist** — enforce strict mode trong project-wide linting rule.
7. **Migration from non-strict** — từng bước bật strict, fix errors, rồi deploy.
8. **Performance-critical code** — strict mode giúp engine optimize tốt hơn (V8 có strict mode fast path).

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Strict mode basic — `this` behavior (file `app.js`)
```js
// Nội dung app.js trong thư mục
"use strict";

function test() {
  console.log(this); // undefined (không phải window/global)
}
test();
```

### Ví dụ 2: So sánh strict vs non-strict `this`
```js
// Non-strict
function nonStrictTest() {
  console.log(this); // window (browser) hoặc global (Node)
}
nonStrictTest();

// Strict
"use strict";
function strictTest() {
  console.log(this); // undefined
}
strictTest();
// this === undefined trong strict — giúp detect accidental global access
```

### Ví dụ 3: Các hành vi bị cấm trong strict mode
```js
"use strict";

// 1. Gán biến chưa khai báo — TypeError
try {
  x = 100;
} catch (e) {
  console.log(e.message); // "x is not defined"
}

// 2. Delete biến — TypeError
let v = 10;
try {
  delete v;
} catch (e) {
  console.log(e.message); // "Cannot delete variable 'v'"
}

// 3. Octal literal — SyntaxError
// let octal = 010; // SyntaxError

// 4. Duplicate parameters — SyntaxError
// function sum(a, a) {} // SyntaxError

// 5. with statement — SyntaxError
// with (Math) { log(1); } // SyntaxError

// 6. delete on non-configurable — TypeError
const frozen = Object.freeze({ a: 1 });
try {
  delete frozen.a;
} catch (e) {
  console.log(e.message); // "Cannot delete property 'a' of..."
}
```

### Ví dụ 4: eval trong strict mode — scoped differently
```js
"use strict";
function testEval() {
  eval("var x = 10;");
  // Trong strict mode, eval tạo variable scoped TO eval, not outer
  try {
    console.log(x); // ReferenceError: x is not defined
  } catch (e) {
    console.log("eval variable not accessible:", e.message);
  }
}
testEval();

// Non-strict: eval creates variable in outer scope
function nonStrictEval() {
  eval("var y = 20;");
  console.log(y); // 20 — accessible in outer scope
}
nonStrictEval();
```

### Ví dụ 5: Strict mode với object property assignment
```js
"use strict";
const obj = Object.defineProperty({}, "secret", {
  value: 42,
  writable: false, // read-only
  configurable: false
});

try {
  obj.secret = 100; // TypeError — không thể gán cho writable: false
} catch (e) {
  console.log(e.message); // "Cannot assign to read only property 'secret'"
}

// Non-strict: silently fails, obj.secret vẫn = 42
```

### Ví dụ 6: Strict mode detect typo in variable name
```js
"use strict";
let userName = "Sơn";

// ❌ Typo — trong non-strict sẽ tạo global `us erName` vô ý
// us erName = "An"; // tạo biến toàn cục mới!

// ✅ Trong strict — TypeError ngay lập tức
try {
  us erName = "An"; // SyntaxError hoặc TypeError tùy cách viết
} catch (e) {
  console.log("Detected typo:", e.message);
}

// ✅ Cách đúng
userName = "An"; // sửa đúng tên biến
console.log(userName); // "An"
```

### Ví dụ 7: Strict mode trong function vs global
```js
// Global non-strict
let globalVar = "outside";

function mixedScope() {
  "use strict"; // chỉ áp dụng trong hàm này
  console.log(this); // undefined — strict inside function
  globalVar = "modified"; // vẫn có thể access global (strict không cấm)
}
mixedScope();
console.log(globalVar); // "modified" — global access vẫn allowed
```

### Ví dụ 8: Strict mode với JSON and parse
```js
"use strict";
// JSON.parse trong strict mode — same behavior, nhưng detect more errors
const valid = JSON.parse('{"name": "Sơn"}');
console.log(valid); // { name: "Sơn" }

try {
  JSON.parse('{name: "Sơn"}'); // missing quotes around key
} catch (e) {
  console.log(e.name); // "SyntaxError"
}
```

### Ví dụ 9: Strict mode và prototype manipulation
```js
"use strict";
// Không thể delete prototype properties
function Person(name) { this.name = name; }
try {
  delete Person.prototype; // TypeError in strict mode
} catch (e) {
  console.log(e.message); // "Cannot delete property 'prototype' of function..."
}

// Non-strict: delete Person.prototype returns true (silently fails)
```

### Ví dụ 10: Strict mode — comprehensive test
```js
"use strict";

// ✅ Allowed in strict mode
const a = 1;
const b = "hello";
const c = { x: 1 };
const d = [1, 2, 3];
function e() { return 42; }
class F {}

// ❌ Forbidden in strict mode
try {
  NaN = 5; // TypeError: Cannot assign to read only property 'NaN'
} catch (e) { console.log("NaN:", e.message); }

try {
  Infinity = 5; // TypeError
} catch (e) { console.log("Infinity:", e.message); }

try {
  let obj = { get x() {} , set x(_) {} };
  // Duplicate property names in object literal — allowed in strict? No, different behavior
} catch (e) { console.log("Object:", e.message); }

// ✅ Strict mode makes code more predictable
console.log(typeof undefined); // "undefined"
console.log(typeof NaN);       // "nan"
console.log(typeof Infinity);  // "infinity"
```

## 🔬 So sánh với alternatives

| Đặc điểm | Strict Mode | Non-Strict Mode |
|---|---|---|
| `this` trong function | `undefined` | `window`/`global` |
| Implicit globals | ❌ TypeError | ✅ Silent creation |
| Octal literals | ❌ SyntaxError | ⚠️ Behavior varies |
| Duplicate params | ❌ SyntaxError | ⚠️ Last wins |
| `with` statement | ❌ SyntaxError | ✅ Allowed |
| `delete` variable | ❌ TypeError | ✅ Allowed (no-op) |
| `eval` scope | ❌ Local to eval | ✅ Outer scope |
| Engine optimization | ✅ Better | ⚠️ Slower path |
| Modern compatibility | ✅ Required | ❌ Deprecated |

## 📊 Performance & Best Practices

**Performance**:
- Strict mode giúp engine **tối ưu tốt hơn** — V8 có "fast path" cho strict code, skip một số runtime checks.
- Overhead thực tế: **strict mode nhanh hơn hoặc bằng** non-strict trong hầu hết cases — không có performance penalty.
- Module scripts (`<script type="module">`) mặc định strict — không cần `"use strict";` thêm.
- Class body mặc định strict — function/method trong class luôn strict.

**Best practices**:
- **Luôn thêm `"use strict";`** ở đầu mọi file JS mới — habit không tốn effort, prevents hàng tá bug.
- **Kiểm tra linter config** — ESLint `strict: "error"` enforce strict mode project-wide.
- **Migrate legacy code** — từng file bật strict, fix errors, rồi commit — không bật cùng lúc toàn bộ.
- **Document strict-dependent behavior** — comment tại sao một số pattern bị cấm trong strict.
- **Dùng class thay IIFE** — class body auto-strict, cleaner syntax, modern replacement.
- **Avoid `eval`** — strict mode restricts eval scope, nhưng best là không dùng eval.
- **Test với `typeof` guard** — `if (typeof useStrict !== "undefined")` để conditional strict.
- **Combine với ESLint** — rules như `no-unused-vars`, `no-implied-eval`, `strict` enforce strict compliance.
- **Module auto-strict** — nếu dùng ES modules, không cần `"use strict";` nhưng vẫn nên có cho clarity.
- **Node.js ESM auto-strict** — `.mjs` files auto strict, `.cjs` cần explicit `"use strict";`.

**Quy tắc "3 nên — 3 không"**:
- ✅ Nên thêm `"use strict";` ở đầu mọi file mới.
- ✅ Nên dùng ESLint `strict: "error"` enforce project-wide.
- ✅ Nên test strict mode behavior trước khi deploy legacy code.
- ❌ Không nên đặt `"use strict";` sau code — không có tác dụng cho phần trước.
- ❌ Không nên依靠 non-strict mode — deprecated, future browsers may remove support.
- ❌ Không nên mixed strict/non-strict in same file — inconsistent behavior.

## 🔗 Liên kết chéo

- Tổng quan Scope & Closure: `09_functions/02_scope-closure-strict-mode/README.md` — overview of all subtopics.
- IIFE: `09_functions/02_scope-closure-strict-mode/02_iife/` — IIFE trong strict vs non-strict context.
- Closure: `09_functions/02_scope-closure-strict-mode/03_closure/` — closure behavior in strict mode.
- Call stack: `09_functions/02_scope-closure-strict-mode/05_function-stack/` — strict mode effect on stack traces.
- Arrow functions: `09_functions/01_parameters-and-arrow/03_arrow-functions/` — arrow this in strict mode.
- Arguments object: `09_functions/01_parameters-and-arrow/05_arguments-object/` — arguments coupling in strict mode.
- Functions overview: `09_functions/README.md` — where strict mode fits in the learning path.
- Exceptional handling: `07_exceptional-handling/01_throw/` — strict mode makes throw more predictable.
