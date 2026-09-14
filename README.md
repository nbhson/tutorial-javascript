# Tutorial JavaScript — Roadmap.sh Aligned (20 groups)

> Tutorial được restructure **1:1 theo [roadmap.sh/javascript](https://roadmap.sh/javascript)** — 20 nhóm lớn (mỗi ô roadmap = 1 thư mục top-level `00→19`) + 2 elective. Đã bổ sung đầy đủ 58 nodes roadmap. Mỗi README đều có phần **Khái niệm / Điểm mạnh / Khi nào dùng / Ví dụ**.

## 🚀 Lộ trình học — 20 nhóm lớn (theo thứ tự roadmap)

| # | Group | Thư mục | Tóm tắt | Trạng thái |
|---|---|---|---|---|
| **00** | Introduction | `00_introduction/` | JS là gì, lịch sử, các phiên bản, cách chạy JS, caching & runtime | ✅ |
| **01** | Variables | `01_variables/` | khai báo, hoisting, scope (block/function/global), var/let/const, naming | ✅ |
| **02** | Data Types | `02_data-types/` | string/number/bigint/symbol, object, type casting, built-in objects | ✅ |
| **03** | Data Structures | `03_data-structures/` | Arrays, Map/Set, Typed Arrays, JSON | ✅ |
| **04** | Equality | `04_equality-comparisons/` | == vs ===, Object.is, SameValue/SameValueZero | ✅ |
| **05** | Loops | `05_loops-and-iterations/` | for, while, do...while, for...in, for...of, break/continue | ✅ |
| **06** | Control Flow | `06_control-flow/` | if/else, switch, ternary | ✅ |
| **07** | Exceptional Handling | `07_exceptional-handling/` | throw, try/catch/finally, Error objects | ✅ |
| **08** | Operators | `08_expressions-and-operators/` | assignment, comparison, arithmetic, bitwise, logical, string, unary | ✅ |
| **09** | Functions | `09_functions/` | parameters, arrow, recursion, closure, strict mode, call stack | ✅ |
| **10** | This Keyword | `10_this-keyword/` | this trong method, function, event, arrow (lexical) | ✅ |
| **11** | Function Borrowing | `11_function-borrowing/` | call, apply, bind, polyfill | ✅ |
| **12** | Async JS | `12_asynchronous-javascript/` | Event loop, promises, async/await, callback hell | ✅ |
| **13** | Working with APIs | `13_working-with-apis/` | Fetch, XHR, JSON Server, CRUD, Service Worker | ✅ |
| **14** | Classes | `14_classes/` | constructor, inheritance, static, private (#) | ✅ |
| **15** | Iterators & Generators | `15_iterators-and-generators/` | Symbol.iterator, function\* yield | ✅ |
| **16** | Modules | `16_modules/` | ESM import/export, CommonJS vs ESM | ✅ |
| **17** | Memory Management | `17_memory-management/` | GC, memory leaks, V8 engine, Proxy/Reflect | ✅ |
| **18** | DOM APIs | `18_dom-apis/` | DOM basics, Shadow DOM, Virtual DOM, Reactivity | ✅ |
| **19** | Browser DevTools | `19_browser-devtools/` | Memory heap, Performance FPS/long tasks | ✅ |
| — | Elective | `20_modern-javascript/` | Template literals, Destructuring, Optional chaining | ✅ |
| — | Elective | `21_graphics/` | Canvas, SVG, Animation | ✅ |

## 🔍 Chi tiết 20 nhóm (khái niệm, điểm mạnh, khi nào dùng)

### 00 — Introduction to JavaScript

**Khái niệm**: JavaScript là ngôn ngữ kịch bản multiparadigm, chủ yếu dùng cho web (client-side), giờ còn Node.js (server-side). Được Brendan Eich tạo ra năm 1995, chuẩn hóa bởi ECMA (ES3, ES5, ES2015/ES6…).

**Điểm mạnh**:
- Đa năng: chạy cả browser lẫn server
- Syntax dễ học, không kiểu tĩnh (dynamic typing)
- Hệ sinh thái npm lớn nhất thế giới
- Event-driven, non-blocking I/O (Node.js)

**Khi nào dùng**: Frontend interactive, backend API, CLI tools, desktop apps (Electron).

**Xem thêm**: `00_introduction/01_what-is-javascript`, `02_history`, `03_versions`, `04_how-to-run`

---

### 01 — Variables & Scopes

**Khái niệm**: `var`, `let`, `const` khai báo biến. Scope xác định vùng truy cập: global, function, block. Hoisting là hiện tượng biến/hàm được đưa lên đầu scope.

**Điểm mạnh**:
- `let`/`const` không bị hoisting giống `var`, tránh lỗi ghost
- Block scope giúp đóng gói, tránh biến toàn cục
- `const` ngăn gán lại, phù hợp hằng số, object frozen

**Khi nào dùng**: Luôn dùng `const` trước, `let` khi cần gán lại, tránh `var`.

**Xem thêm**: `01_variables/01_declarations`, `02_hoisting`, `03_scopes`, `04_naming-and-practices`

---

### 02 — Data Types

**Khái niệm**: JavaScript có 6 primitive types (string, number, bigint, symbol, null, undefined, boolean) và Object (không phải primitive). Type casting: explicit (convert thủ công) vs implicit (coercion tự động).

**Điểm mạnh**:
- Dynamically typed → linh hoạt, viết code nhanh
- Built-in objects (Math, Date, RegExp, Error) phong phú
- `typeof`, `instanceof` kiểm tra type nhanh

**Khi nào dùng**: Mọi lúc — đây là nền tảng xử lý dữ liệu. Cần cẩn trọng với implicit coercion (`"" == false`).

**Xem thêm**: `02_data-types/01_primitive-types`, `02_objects`, `03_type-casting`, `04_builtin-objects`

---

### 03 — Data Structures

**Khái niệm**: Cấu trúc lưu trữ dữ liệu: Array (danh sách), Map (key-value, any key), Set (unique values), TypedArray (binary data), JSON (dữ liệu dạng text).

**Điểm mạnh**:
- Array: tích hợp sẵn map/filter/reduce/sort — cực mạnh
- Map/Set: O(1) lookup, không bị hoisted kiểu object
- JSON: chuẩn interchange format, đọc dễ

**Khi nào dùng**: Array cho danh sách có thứ tự; Map khi cần key phức tạp (object, symbol); Set để loại bỏ trùng lặp.

**Xem thêm**: `03_data-structures/01_arrays`, `02_keyed-collections`, `03_typed-arrays`, `04_json`

---

### 04 — Equality Comparisons

**Khái niệm**: So sánh giá trị (`==`) hay kiểu + giá trị (`===`). `Object.is(a, b)` so sánh chính xác như typeof + !== (xử lý NaN và -0).

**Điểm mạnh**:
- `===` tránh được lỗi coercion (như `"" == false` là true)
- `Object.is` xử lý đúng NaN === NaN và -0 !== +0

**Khi nào dùng**: Luôn dùng `===` trừ khi thực sự cần `==` (hiểu rõ hệ quả). Dùng `Object.is` khi cần chính xác tuyệt đối (so sánh object, numeric).

**Xem thêm**: `04_equality-comparisons/01_loose-strict`, `02_object-is`, `03_samevaluezero`

---

### 05 — Loops and Iterations

**Khái niệm**: Lặp qua dữ liệu: `for` (biết số lần), `while`/`do...while` (điều kiện), `for...in` (keys), `for...of` (values iterable).

**Điểm mạnh**:
- `for...of` an toàn, không duyệt prototype chain
- `break`/`continue` điều khiển luồng nhanh
- `for` truyền thống kiểm soát index rõ

**Khi nào dùng**: `for...of` cho array/iterable; `for...in` cho object keys (nhưng thường dùng `Object.keys`/`for..of` thay thế); loop có điều kiện dùng `while`.

**Xem thêm**: `05_loops-and-iterations/01_loops`

---

### 06 — Control Flow

**Khái niệm**: Quyết định luồng thực thi: `if...else` (điều kiện), `switch` (nhiều case), ternary (expression).

**Điểm mạnh**:
- `if` linh hoạt, kiểm tra được nhiều điều kiện
- `switch` rõ ràng khi so sánh nhiều giá trị cố định
- Ternary gọn trong expression context ( JSX, return )

**Khi nào dùng**: `if/else` cho điều kiện phức tạp; `switch` khi 1 biến so sánh nhiều giá trị; ternary trong expression đơn giản.

**Xem thêm**: `06_control-flow/01_conditionals`

---

### 07 — Exceptional Handling

**Khái niệm**: Xử lý lỗi bằng `try/catch/finally`, `throw` có thể ném bất kỳ giá trị nào. Error objects (Error, TypeError, RangeError…) mang `message` và `stack`.

**Điểm mạnh**:
- `try/catch` giữ chương trình tiếp tục dù lỗi
- `finally` luôn chạy (giải phóng tài nguyên)
- Custom error classes dễ mở rộng

**Khi nào dùng**: Khi gọi API không đáng tin, parse JSON, hoặc thao tác file. Bắt lỗi cụ thể (kiểm tra `instanceof`).

**Xem thêm**: `07_exceptional-handling/01_throw`, `02_try-catch-finally`, `03_error-objects`

---

### 08 — Expressions & Operators

**Khái niệm**: Toán tử: assignment, comparison, arithmetic, bitwise, logical, comma, unary, string.

**Điểm mạnh**:
- Logical `&&`/`||` vừa điều kiện vừa giá trị mặc định
- Nullish coalescing `??` chỉ bỏ null/undefined, khác `||`
- Unary `++`/`--` prefix/postfix khác nhau về thứ tự

**Khi nào dùng**: `??` thay `||` khi mặc định số; bitwise cho thao tác bit thấp (flag, màu RGB); short-circuit cho default params đơn giản.

**Xem thêm**: `08_expressions-and-operators/01_operators` → `06_string-operators`

---

### 09 — Functions

**Khái niệm**: Blocks of reusable code. Có parameter/default/rest. Arrow functions ngắn gọn, `this` lexical. Recursion là hàm gọi chính nó. Closure giữ reference đến scope cha.

**Điểm mạnh**:
- Arrow function ngắn, không binding this riêng → phù hợp callback
- Closure tạo private state, factory, module pattern
- Rest params `...args` linh hoạt xử lý số lượng variable

**Khi nào dùng**: Arrow cho callback ngắn; function declaration khi cần hoisting; generator khi cần pause/resume.

**Xem thêm**: `09_functions/01_parameters-and-arrow`, `02_scope-closure-strict-mode`

---

### 10 — Using (this) keyword

**Khái niệm**: `this` là reference đến object đang gọi hàm. 4 rules: default (global/window), implicit (obj.method), explicit (call/apply/bind), new (instance mới). Arrow function kế thừa `this` lexical từ nơi định nghĩa.

**Điểm mạnh**:
- Hiểu `this` giúp tránh bug "undefined this" trong callback
- Arrow function giúp giữ `this` của component (React handler)
- Bind/bind helper cho sự kiện DOM

**Khi nào dùng**: Method object → `this`; callback cần context → arrow hoặc `.bind()`; constructor/class → `this` = instance.

**Xem thêm**: `10_this-keyword/01_in-method` → `06_arrow-lexical`

---

### 11 — Function Borrowing

**Khái niệm**: Dùng lại method của object này trên object khác qua `call`, `apply`, `bind`. Polyfill là tự viết implementation của native method.

**Điểm mạnh**:
- Tránh copy code, reuse logic
- `call`/`apply` cùng thực thi, `bind` tạo hàm mới
- Polyfill cho phép dùng method trên môi trường cũ

**Khi nào dùng**: Khi muốn dùng `Array.prototype.slice.call(arguments)` (trước ES6), hoặc `Math.max.apply(null, arr)`.

**Xem thêm**: `11_function-borrowing/01_bind` → `05_polyfill`

---

### 12 — Asynchronous JavaScript

**Khái niệm**: JS single-threaded, dùng Event Loop để xử lý đồng thời. Callback → Promise → async/await là 3 thế hệ xử lý async. Microtasks (promise) chạy trước macrotasks (setTimeout).

**Điểm mạnh**:
- Non-blocking I/O → hiệu suất cao
- `async/await` viết async như sync code
- Promise `.then/.catch` xử lý chain rõ ràng

**Khi nào dùng**: Gọi API, đọc file, timer, streaming data.

**Xem thêm**: `12_asynchronous-javascript/01_event-loop`, `02_callbacks-promises`

---

### 13 — Working with APIs

**Khái niệm**: Giao tiếp server qua HTTP. `fetch` hiện đại (promise-based), `XMLHttpRequest` cũ (callback). JSON Server tạo fake REST API local. CRUD: Create/Read/Update/Delete.

**Điểm mạnh**:
- Fetch đơn giản, native, không cần thư viện
- JSON Server chạy nhanh `npx json-server --watch db.json`
- Postman test API mà không code

**Khi nào dùng**: Frontend gọi REST API, backend mock data, testing thủ công.

**Xem thêm**: `13_working-with-apis/01_fetch` → `06_service-worker`

---

### 14 — Classes

**Khái niệm**: OOP pattern trong JS (syntactic sugar over prototypes). `constructor`, `extends`, `super`, `static`, `#private`. Private field `#name` không truy cập từ ngoài.

**Điểm mạnh**:
- Code tổ chức, tái sử dụng cao
- `extends` tạo hierarchy rõ ràng
- `#private` đảm bảo encapsulation

**Khi nào dùng**: Model dữ liệu phức tạp, component base class, utility class.

**Xem thêm**: `14_classes/01_basics` → `04_static-private`

---

### 15 — Iterators and Generators

**Khái niệm**: Iterator là object có `next()` trả `{value, done}`. `Symbol.iterator` làm object iterable. Generator `function*` + `yield` tạo iterator tự động, có thể pause/resume.

**Điểm mạnh**:
- Generator tạo infinite sequence, lazy evaluation
- Tự định nghĩa iterable cho class
- Async iterators kết hợp async/await

**Khi nào dùng**: Stream data, pagination, custom collections, reactive-like patterns.

**Xem thêm**: `15_iterators-and-generators/01_generators`, `02_iterators`

---

### 16 — Modules

**Khái niệm**: Chia code thành file độc lập. ESM: `import`/`export` tĩnh, hỗ trợ tree-shaking, load async. CommonJS: `require`/`module.exports` đồng bộ.

**Điểm mạnh**:
- ESM được chuẩn hóa, tối ưu bundle
- Module scope tránh global pollution
- Tree-shaking giảm size bundle

**Khi nào dùng**: Project lớn, React/Vite/Webpack dùng ESM. Node cũ dùng CommonJS.

**Xem thêm**: `16_modules/03_modules/01_commonjs-vs-esm`, `logger`

---

### 17 — Memory Management

**Khái niệm**: JavaScript tự quản lý bộ nhớ qua Garbage Collection (Mark & Sweep). Memory leak thường do global variable, closure giữ reference, detached DOM node, setInterval không clear.

**Điểm mạnh**:
- GC tự động, developer ít quan tâm
- DevTools Memory giúp phát hiện leak
- Proxy/Reflect cho meta-programming

**Khi nào dùng**: Performance-sensitive app, long-running SPA, worker.

**Xem thêm**: `17_memory-management/01_memory-lifecycle-gc`, `03_v8-engine`, `04_meta-programming`

---

### 18 — DOM APIs

**Khái niệm**: Document Object Model — cấu trúc cây nodes của HTML. Thao tác qua `document.getElementById/querySelector`, `appendChild`, `addEventListener`. Shadow DOM encapsulate nội dung component. Virtual DOM so sánh diff (React). Reactivity tự cập nhật UI.

**Điểm mạnh**:
- DOM chuẩn, không cần thư viện để manipulate cơ bản
- Shadow DOM bảo vệ style/scope
- Virtual DOM tăng performance với updates phức tạp

**Khi nào dùng**: Tương tác user, form validation, SPA (với framework).

**Xem thêm**: `18_dom-apis/01_dom-basics`, `02_dom-advanced`, `03_events`

---

### 19 — Browser DevTools

**Khái niệm**: Công cụ debug built-in browser. Memory tab: Heap snapshot, tìm GC root leak. Performance tab: FPS, long tasks, script profiling.

**Điểm mạnh**:
- Miễn phí, có sẵn
- Heap snapshot tìm object giữ内存 lâu
- Performance timeline visualize execution

**Khi nào dùng**: Debug memory leak, tối ưu render, tìm CPU bottleneck.

**Xem thêm**: `19_browser-devtools/01_devtools-memory`, `02_devtools-performance`

---

## 📂 Cây chi tiết

```
00_introduction/               # What is JS, History, Versions, How to run
01_variables/                  # Declarations, Hoisting, Scopes, Naming
02_data-types/                 # Primitive types, Objects, Type Casting, Built-in
03_data-structures/            # Arrays, Keyed Collections, Typed Arrays, JSON
04_equality-comparisons/       # Loose/Strict, Object.is, SameValueZero
05_loops-and-iterations/       # for, while, break, continue
06_control-flow/               # if/switch/ternary
07_exceptional-handling/       # throw, try/catch, Error objects
08_expressions-and-operators/  # All operator categories
09_functions/                  # Params, Arrow, Recursion, Closure, Strict
10_this-keyword/               # this in method/function/event/arrow
11_function-borrowing/         # call/apply/bind, Polyfill
12_asynchronous-javascript/    # Event Loop, Promises, async/await
13_working-with-apis/          # Fetch, XHR, JSON Server, CRUD
14_classes/                    # Basics, Constructor, Inheritance, Static/Private
15_iterators-and-generators/   # Symbol.iterator, function*
16_modules/                    # ESM vs CommonJS
17_memory-management/          # GC, Leaks, V8, Meta-programming
18_dom-apis/                   # Basics, Advanced, Shadow/Virtual/Reactivity
19_browser-devtools/           # Memory, Performance
20_modern-javascript/          # elective
21_graphics/                   # elective
```

## 🔧 Thay đổi chính

- **Fix typo**: `histoy→history`, `temple→template`, `chanining→chaining`, `coallescing→coalescing`, `atribute→attribute`, `continute→continue`, `programing→programming`, `techical→technical`
- **Restructure 7 → 20 top-level** khớp 1:1 với 20 ô roadmap.sh
- **137 files updated** (04-09 2026) — thêm 100% sub-module READMEs chi tiết (khái niệm, điểm mạnh, khi nào dùng, ví dụ)
- **.gitignore** + xóa `.DS_Store`
- **Bổ sung đầy đủ 58 nodes roadmap**

## 📚 Tham khảo

- Roadmap: https://roadmap.sh/javascript
- MDN: https://developer.mozilla.org/en-US/docs/Web/JavaScript
- javascript.info: https://javascript.info/

## ▶️ Cách học

1. Đi theo thứ tự `00 → 19` (20, 21 là elective)
2. Mỗi folder có `README.md` + `app.js` — chạy `node app.js` hoặc mở `index.html`
3. Đọc phần "Khái niệm / Điểm mạnh / Khi nào dùng" trong mỗi README

## 📖 Mirror javascript.info — `js/` (175 bài, 100% coverage)

> Chi tiết từng bài xem `js/README.md`. Toàn bộ 175 bài leaf của https://javascript.info đã được mirror 1:1 vào `js/` (27 thư mục: `01_introduction` → `36_regular-expressions`), mỗi file có `> Source: https://javascript.info/<slug>` và `<!-- fetched: 2026-09-14 -->`, giữ nguyên Tasks/solutions, không cắt bớt.

| Phần | Thư mục `js/` | Số bài |
|---|---|---|
| Part 1 — The JavaScript Language | `01_introduction` → `14_misc` (14 chương) | 76 |
| Part 2 — Browser: Document, Events | `20_browser-document` → `25_ui-misc` (6 chương) | 44 |
| Part 3 — Additional articles | `30_frames-windows` → `36_regular-expressions` (8 chương) | 55 |
| **Tổng** | **27 thư mục** | **175** |

Xác minh `2026-09-14`: `curl https://javascript.info/tutorial/map` → 205 href unique, trừ 27 section + 3 meta = 175 leaf → khớp `find js -name "*.md" | wc -l`.

---
*Last update: 2026-09-14 — 137 files roadmap (00→21) + 175 files js mirror (100% javascript.info), verified via tutorial/map*
