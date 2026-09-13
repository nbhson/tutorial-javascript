# Tutorial JavaScript — Roadmap.sh Aligned

> Tutorial được restructure theo [roadmap.sh/javascript](https://roadmap.sh/javascript) — 13 modules, thứ tự học từ cơ bản → nâng cao. **Đã bổ sung đầy đủ 58 nodes roadmap (các mục trước là 🚧 nay đã có code mẫu).**

## 🚀 Lộ trình học (đánh số để đi theo thứ tự)

| # | Module | Nội dung | Trạng thái |
|---|--------|----------|------------|
| **00** | [Introduction](00_introduction/) | What is JS, History, Versions, How to run JS (browser caching, runtime) | ✅ có nội dung |
| **01** | [Variables](01_variables/) | Declarations (let/const/var), Hoisting, Scopes, Naming | ✅ |
| **02** | [Data Types](02_data-types/) | Primitive types (string/number/bigint/symbol/null/undefined/boolean), Objects & Prototype, Type Casting/Coercion, Built-in Objects (Math/Date/RegExp/Error) | ✅ |
| **03** | [Data Structures](03_data-structures/) | Arrays, Keyed Collections (Map/WeakMap/Set/WeakSet), Typed Arrays, JSON, Equality (==/===/Object.is/SameValueZero) | ✅ |
| **04** | [Control Flow](04_control-flow/) | Conditionals (if/switch/ternary), Loops, Error Handling (throw/try-catch/Error Objects) | ✅ |
| **05** | [Expressions & Operators](05_expressions-and-operators/) | Arithmetic/String/Assignment/Comparison/Logical/Bitwise/BigInt/String/Conditional/Comma/Unary | ✅ |
| **06** | [Functions](06_functions/) | Params/Arrow/Callbacks/Recursion/arguments, Scope/Closure/IIFE/Strict/Stack, this (5 contexts)/bind/call/apply/polyfill | ✅ |
| **07** | [Async](07_async/) | Event Loop & Runtime, setTimeout/Interval, Callback Hell, Promises/Async-Await, Fetch/XHR/JSON-Server/CRUD | ✅ |
| **08** | [DOM & Browser](08_dom-and-browser/) | DOM Basics (F8), How Browser Reads HTML, Advanced (Shadow/Virtual/Reactivity), Events | ✅ |
| **09** | [Classes / Generators / Modules](09_modules-classes-generators/) | Classes, Iterators/Generators, Modules (CommonJS vs ESM) | ✅ |
| **10** | [Memory & Performance](10_memory-and-performance/) | GC/Memory Leaks, DevTools Memory/Performance, V8 Engine, Meta Programming (Proxy/Reflect) | ✅ |
| **11** | [Modern JavaScript](11_modern-javascript/) | Template Literals, Destructuring/Spread/Rest, Optional Chaining/Nullish, Enhanced Literals, Misc | ✅ |
| **12** | [Graphics](12_graphics/) | Raster/SVG, 2D Animation, SVG Bar Chart, Canvas — elective | ✅ code-only |
| | [_archive](_archive/) | Tài liệu cũ (.docx) | 📦 |

> 🚧 = placeholder đã tạo sẵn, bạn chỉ cần điền nội dung theo TODO trong README của folder đó.

## 📂 Cấu trúc chi tiết

```
00_introduction/
  01_what-is-javascript/          # What is JS + first-class fn + prototype
  02_history-of-javascript/
  03_versions/                    # 🚧 placeholder
  04_how-to-run-javascript/       # browser caching + js-runtime deep dive
01_variables/
  01_declarations/                # var/let/const + screenshot
  02_hoisting/
  03_scopes/
  04_naming-and-practices/        # 🚧
02_data-types/
  01_primitive-types/             # string, number, value vs reference
  02_objects-and-prototype/       # objects, prototype, shallow/deep clone
  03_type-casting-and-coercion/   # dynamic typing (325 dòng)
  04_builtin-objects/             # 🚧
03_data-structures/
  01_arrays/                      # 01_array-basics + app.js
  02_keyed-collections/           # 🚧 Map/Set
  03_typed-arrays/                # 🚧
  04_json/
  05_equality-comparisons/        # 🚧 == vs === vs Object.is
04_control-flow/
  01_conditionals/                # if/switch/ternary
  02_loops-and-iterations/        # for/while/break
  03_error-handling/              # 🚧 try/catch
05_expressions-and-operators/
  01_operators/                   # 6 files toán tử
06_functions/
  01_parameters-and-arrow/        # callbacks, builtin, arrow
  02_scope-closure-strict-mode/   # strict, IIFE, closure, non-blocking
  03_this-and-binding/            # this, bind/call/apply/polyfill
07_async/
  01_event-loop/                  # runtime deep dive, event loop, intro
  02_callbacks-promises/          # promise theory → chain → async/await
  03_fetch-and-apis/              # fetch, json-server, postman, crud, service-worker
08_dom-and-browser/
  01_dom-basics/                  # 01_f8-basic-dom (12 bài), 02_how-browser-reads-html
  02_dom-advanced/                # manipulation, shadow, virtual, combination, reactivity
  03_events/                      # (nằm trong 01_f8-basic-dom)
09_modules-classes-generators/
  01_classes/
  02_iterators-generators/        # generators + placeholder iterator
  03_modules/                     # logger ESM
10_memory-and-performance/
  01_memory-lifecycle-gc/         # GC + memory leaks
  02_debugging-performance/       # 🚧
  03_v8-engine/
  04_meta-programming/
11_modern-javascript/
  01_template-literals/           # template string, tagged
  02_destructuring-spread-rest/
  03_optional-chaining-nullish/
  04_enhanced-literals-default-params/
  05_misc/                        # logical-or
12_graphics/                      # elective, không trong roadmap core
```

## 🔧 Thay đổi chính trong lần restructure này

- **Fix typo:** `histoy` → `history`, `temple` → `template`, `chanining` → `chaining`, `coallescing` → `coalescing`, `atribute` → `attribute`, `continute` → `continue`, `programing` → `programming`, `techical` → `technical`
- **Gộp trùng lặp:** DOM (2 track → 08), Promise/Async (2 track → 07), Variables/let-const (3 nơi → 01), GC/Memory (3 nơi → 10)
- **Sắp xếp theo roadmap.sh:** 00 → 12, đi từ Introduction → Variables → Data Types → Control Flow → Functions → Async → DOM → Modules → Memory → Modern JS → Graphics
- **.gitignore:** thêm, xoá `.DS_Store` khỏi index
- **Placeholder:** tạo sẵn folder + README TODO cho các topic roadmap.sh chưa có (Map/Set, Typed Arrays, Equality, Error Handling, Bitwise/BigInt, Debugging Performance…)

## 📚 Tham khảo

- Roadmap: https://roadmap.sh/javascript (PDF: https://roadmap.sh/pdfs/roadmaps/javascript.pdf)
- MDN: https://developer.mozilla.org/en-US/docs/Web/JavaScript
- javascript.info: https://javascript.info/

## ▶️ Cách học

1. Đi theo thứ tự 00 → 11 (12 là elective)
2. Mỗi folder có `README.md` lý thuyết + `app.js`/`index.html` thực hành
3. Folder 🚧: đọc TODO trong README rồi tự điền — giữ cùng format (README + app.js + index.html)
4. Chạy ví dụ: mở `index.html` bằng Live Server hoặc `node app.js`

---
*Restructure: 2026-09-13 — từ 7 top-folders rời rạc → 13 modules theo roadmap.sh*
