# Tutorial JavaScript — Roadmap.sh Aligned (20 groups)

> Tutorial được restructure **1:1 theo [roadmap.sh/javascript](https://roadmap.sh/javascript)** — 20 nhóm lớn (mỗi ô trên roadmap = 1 thư mục top-level `00→19`) + 2 elective. Đã bổ sung đầy đủ 58 nodes roadmap.

## 🚀 Lộ trình học — 20 nhóm lớn (theo thứ tự roadmap)

| # | Group (roadmap box) | Thư mục | Nội dung chính | Trạng thái |
|---|---|---|---|---|
| **00** | Introduction to JavaScript | `00_introduction/` | What is JS, History, Versions, How to run JS (caching, runtime deep dive) | ✅ |
| **01** | Variables & Scopes | `01_variables/` | Declarations, Hoisting, Scopes (Block/Function/Global), var/let/const, Naming | ✅ |
| **02** | Data Types | `02_data-types/` | string/number/bigint/symbol/null/undefined/boolean, Object/Prototype, Type Casting (Explicit/Implicit/Conversion vs Coercion), Built-in Objects (Math/Date/RegExp/Error) | ✅ |
| **03** | Data Structures | `03_data-structures/` | Arrays, Keyed Collections (Map/WeakMap/Set/WeakSet), Typed Arrays, JSON | ✅ |
| **04** | Equality Comparisons | `04_equality-comparisons/` | `==` vs `===`, `Object.is` (SameValue), SameValueZero, Equality Algorithms | ✅ |
| **05** | Loops and Iterations | `05_loops-and-iterations/` | for, do...while, while, for...in, for...of, break/continue | ✅ |
| **06** | Control Flow | `06_control-flow/` | if...else, Switch, Ternary | ✅ |
| **07** | Exceptional Handling | `07_exceptional-handling/` | throw, try/catch/finally, Error Objects | ✅ |
| **08** | Expressions & Operators | `08_expressions-and-operators/` | Assignment/Comparison/Arithmetic/Bitwise/Logical/BigInt/String/Conditional/Comma/Unary | ✅ |
| **09** | Functions | `09_functions/` | Params/Arrow/IIFE/arguments/Built-in/Default/Rest/Recursion/Lexical/Closure/Scope & Stack, Strict Mode | ✅ |
| **10** | Using (this) keyword | `10_this-keyword/` | this in method / in function / alone / in event handler / in arrow (lexical) | ✅ |
| **11** | Function Borrowing | `11_function-borrowing/` | Explicit Binding: call / apply / bind, Polyfill | ✅ |
| **12** | Asynchronous JavaScript | `12_asynchronous-javascript/` | Event Loop, setTimeout/setInterval, Callbacks, Promises, Callback Hell, async/await | ✅ |
| **13** | Working with APIs | `13_working-with-apis/` | Fetch, XMLHttpRequest, JSON Server, Postman, CRUD, Service Worker | ✅ |
| **14** | Classes | `14_classes/` | Basics, Constructor, Inheritance (extends/super), Static & Private (#) | ✅ |
| **15** | Iterators and Generators | `15_iterators-and-generators/` | Iterators (Symbol.iterator), Generators | ✅ |
| **16** | Modules in JavaScript | `16_modules/` | ESM (import/export), CommonJS vs ESM | ✅ |
| **17** | Memory Management | `17_memory-management/` | Memory Lifecycle, Garbage Collection, V8 Engine, Meta Programming (Proxy/Reflect) | ✅ |
| **18** | DOM APIs | `18_dom-apis/` | DOM Basics (12 bài F8), How Browser Reads HTML, Advanced (Shadow/Virtual/Reactivity) | ✅ |
| **19** | Using Browser DevTools | `19_browser-devtools/` | DevTools Memory (Heap), Performance (FPS/Long tasks) | ✅ |
| | _Elective_ | `20_modern-javascript/` | Template Literals, Destructuring/Spread/Rest, Optional Chaining/Nullish, Enhanced Literals (phân tán trong roadmap, giữ lại để tham khảo) | ✅ |
| | _Elective_ | `21_graphics/` | Raster/SVG, 2D Animation, SVG Bar Chart, Canvas | ✅ |
| | _Archive_ | `_archive/` | Kiểu dữ liệu.docx, Mục tiêu.docx | 📦 |

> Mỗi nhóm lớn bên trong có nhiều items nhỏ (ví dụ `10_this-keyword` có 6 sub: in-method, in-function, alone, event-handler, arrow, ...). Xem cây chi tiết bên dưới.

## 📂 Cây chi tiết (20 top-level)

```
00_introduction/               # 01_what-is-javascript, 02_history, 03_versions, 04_how-to-run
01_variables/                  # 01_declarations/01_let-and-const, 02_hoisting, 03_scopes, 04_naming
02_data-types/                 # 01_primitive-types (string/number/bigint/symbol/null...), 02_objects, 03_type-casting (conversion/explicit/implicit), 04_builtin-objects
03_data-structures/            # 01_arrays, 02_keyed-collections (Map/Set...), 03_typed-arrays, 04_json
04_equality-comparisons/       # 01_loose-strict, 02_object-is, 03_samevaluezero
05_loops-and-iterations/       # 01_loops (for/while/break...)
06_control-flow/               # 01_conditionals (if/switch/ternary)
07_exceptional-handling/       # 01_throw, 02_try-catch-finally, 03_error-objects
08_expressions-and-operators/  # 01_operators, 02_bitwise, 03_bigint, 04_comma, 05_unary, 06_string
09_functions/                  # 01_parameters-and-arrow (callbacks/arrow/recursion/arguments...), 02_scope-closure-strict-mode (IIFE/closure/strict/stack)
10_this-keyword/               # 01_in-method, 02_in-function, 03_alone, 04_event-handler, 05_arrow, 06_arrow-lexical
11_function-borrowing/         # 01_bind, 02_bind-advanced, 03_call, 04_apply, 05_polyfill
12_asynchronous-javascript/    # 01_event-loop (runtime/deep-dive/setTimeout), 02_callbacks-promises (promise/hell/async-await)
13_working-with-apis/          # 01_fetch, 02_xhr, 03_json-server, 04_postman, 05_crud, 06_service-worker
14_classes/                    # 01_basics, 02_constructor, 03_inheritance, 04_static-private
15_iterators-and-generators/   # 01_generators, 02_iterators
16_modules/                    # 01_commonjs-vs-esm, logger (ESM)
17_memory-management/          # 01_memory-lifecycle-gc (GC + leaks), 03_v8-engine, 04_meta-programming
18_dom-apis/                   # 01_dom-basics (12 bài), 02_how-browser-reads, 02_dom-advanced (shadow/virtual...)
19_browser-devtools/           # 01_devtools-memory, 02_devtools-performance
20_modern-javascript/          # elective - template/destructuring/optional...
21_graphics/                   # elective - canvas/svg
```

## 🔧 Thay đổi chính

- **Fix typo:** `histoy→history`, `temple→template`, `chanining→chaining`, `coallescing→coalescing`, `atribute→attribute`, `continute→continue`, `programing→programming`, `techical→technical`
- **Restructure 7 → 20 top-level** để khớp 1:1 với 20 ô lớn trên roadmap.sh (trước gộp thành 13 để gọn, nay tách theo yêu cầu)
  - Tách `Equality` khỏi `Data Structures`, `Loops` khỏi `Control Flow`, `Exceptional Handling` riêng, `this` và `Function Borrowing` riêng, `Working with APIs` riêng, `Classes/Iterators/Modules` riêng, `DOM` và `DevTools` riêng
  - `Type Casting` đã tách thành `01_conversion-vs-coercion`, `02_explicit`, `03_implicit`
  - `Classes` tách thành 4 sub: basics/constructor/inheritance/static-private
- **.gitignore** + xóa `.DS_Store`
- **Bổ sung đầy đủ 58 nodes:** BigInt/Symbol, Built-in Objects, Map/Set/TypedArrays, Equality, Error Handling, Bitwise/BigInt/Comma/Unary, Recursion/arguments, Callback Hell/XHR, CommonJS vs ESM, DevTools...

## 📚 Tham khảo

- Roadmap: https://roadmap.sh/javascript (PDF: https://roadmap.sh/pdfs/roadmaps/javascript.pdf)
- MDN: https://developer.mozilla.org/en-US/docs/Web/JavaScript
- javascript.info: https://javascript.info/

## ▶️ Cách học

1. Đi theo thứ tự `00 → 19` (20, 21 là elective)
2. Mỗi sub-folder có `README.md` + `app.js` + `index.html` — mở `index.html` bằng Live Server hoặc `node app.js`
3. Tự điền thêm ví dụ vào `app.js` nếu muốn

---
*Restructure: 2026-09-13 — từ 7 top-folders → 20 groups (1:1 roadmap.sh) + 2 elective*
