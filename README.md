# JavaScript Tutorial — Khóa học toàn diện (Tiếng Việt)

> Khóa học JavaScript từ nền tảng đến nâng cao — 23 nhóm chủ đề, hơn 200 bài viết, hoàn toàn bằng tiếng Việt. Biên soạn dựa trên [javascript.info](https://javascript.info/) và tài liệu chuẩn ECMAScript.

## 📌 Thông tin quan trọng

- Repo chứa **23 nhóm chủ đề** (thư mục `00_introduction/` → `23_es2026-features/`), mỗi nhóm có `README.md` riêng mô tả cấu trúc và lộ trình học.
- Thư mục `js-info/` là **tài liệu tham khảo được vendored** từ javascript.info (bản gốc tiếng Việt) — **không phải nội dung khóa học**, không nằm trong lộ trình. Bạn có thể bỏ qua hoàn toàn.
- Mỗi nhóm chủ đề gồm các thư mục con được đánh số (`01_...`, `02_...`), trong đó có bài học `README.md` và file ví dụ chạy được (`app.js`, `index.html`) nếu có.

## 🗂️ Cấu trúc 23 nhóm chủ đề

```
tutorial-javascript/
├── 00_introduction/               ← JavaScript là gì? Lịch sử, phiên bản, cách chạy
├── 01_variables/                  ← Khai báo, hoisting, scope, đặt tên biến
├── 02_data-types/                 ← Primitive types, objects, ép kiểu, built-in objects
├── 03_data-structures/            ← Array, Map/Set/WeakMap, TypedArray, JSON
├── 04_equality-comparisons/       ← == vs ===, Object.is, SameValueZero
├── 05_loops-and-iterations/       ← for, while, for...of, for...in
├── 06_control-flow/               ← if/else, switch, ternary
├── 07_exceptional-handling/       ← throw, try/catch/finally, Error objects
├── 08_expressions-and-operators/  ← Toán tử, bitwise, BigInt, comma, unary
├── 09_functions/                  ← Tham số, arrow functions, scope, closure, IIFE
├── 10_this-keyword/               ← this trong method, function, arrow function
├── 11_function-borrowing/         ← bind, call, apply, polyfill
├── 12_asynchronous-javascript/    ← Event loop, callback, Promise, async/await
├── 13_working-with-apis/          ← Fetch, XMLHttpRequest, CRUD, Postman, service worker
├── 14_classes/                    ← Class, constructor, inheritance, static/private
├── 15_iterators-and-generators/   ← Iterator protocol, generator functions
├── 16_modules/                    ← ESM import/export, dynamic import, barrel files
├── 17_memory-management/          ← Memory lifecycle, GC, V8 engine, meta-programming
├── 18_dom-apis/                   ← DOM basics, Shadow DOM, Virtual DOM, events
├── 19_browser-devtools/           ← DevTools Memory, Performance, Network
├── 20_modern-javascript/          ← Tổng hợp ES6+: template literals, destructuring...
├── 21_graphics/                   ← Canvas, SVG, 2D animation, bar chart
├── 22_es2025-features/            ← ES2025: Iterator Helpers, Set Methods, RegExp.escape
├── 23_es2026-features/            ← ES2026: Array.fromAsync, Map.getOrInsert, Math.sumPrecise...
└── js-info/                       ← (vendored reference — bỏ qua)
```

## 🚀 Quick start

```bash
# Xem tổng quan một nhóm chủ đề
cat 00_introduction/README.md

# Đọc một bài học cụ thể
cat 02_data-types/01_primitive-types/01_string/README.md

# Tìm kiếm nội dung
grep -r "Promise" 12_asynchronous-javascript/

# Đếm tổng số bài học
find . -name "*.md" ! -name "README.md" ! -path "./js-info/*" | wc -l
```

## 🧭 Lộ trình học đề xuất

### Giai đoạn 1 — Nền tảng ngôn ngữ (~2 tuần)

`00_introduction` → `01_variables` → `02_data-types` → `03_data-structures` → `04_equality-comparisons` → `05_loops-and-iterations` → `06_control-flow` → `08_expressions-and-operators`

### Giai đoạn 2 — Hàm & Lập trình hướng đối tượng (~2 tuần)

`09_functions` → `10_this-keyword` → `11_function-borrowing` → `14_classes` → `15_iterators-and-generators`

### Giai đoạn 3 — Bất đồng bộ & Hệ sinh thái (~2 tuần)

`07_exceptional-handling` → `12_asynchronous-javascript` → `13_working-with-apis` → `16_modules` → `17_memory-management`

### Giai đoạn 4 — Trình duyệt & Giao diện (~2 tuần)

`18_dom-apis` → `19_browser-devtools` → `21_graphics`

### Giai đoạn 5 — JavaScript hiện đại (khi đã vững nền tảng)

`20_modern-javascript` → `22_es2025-features` → `23_es2026-features`

## 📖 Các phiên bản ECMAScript

| Phiên bản | Ngày phát hành | Tính năng nổi bật |
|---|---|---|
| ES5 | 12/2009 | Strict mode, JSON, getters/setters |
| ES6 (ES2015) | 06/2015 | Classes, arrow functions, let/const, modules, Promise |
| ES2016–2019 | hằng năm | async/await, spread, optional catch binding, flat/flatMap |
| ES2020 | 06/2020 | BigInt, `?.`, `??`, `globalThis`, dynamic import |
| ES2022 | 06/2022 | Top-level await, class fields, `.at()` |
| ES2023 | 06/2023 | `toSorted/toReversed/toSpliced/with` |
| ES2024 | 06/2024 | `Object.groupBy`, `Promise.withResolvers`, `ArrayBuffer.transfer` |
| ES2025 | 06/2025 | Iterator Helpers, Set Methods, `Promise.try`, `RegExp.escape` |
| ES2026 | 06/2026 | `Array.fromAsync`, `Map.getOrInsert`, `Math.sumPrecise`, `Error.isError`, Uint8Array Base64/Hex |

> **Lưu ý:** Temporal API đạt Stage 3 → dự kiến hoàn thiện cho **ES2027**, không phải ES2025/ES2026. Luôn kiểm tra [TC39 finished proposals](https://github.com/tc39/proposals/blob/main/finished-proposals.md) trước khi dùng tính năng mới trong production.

## 🔗 Nguồn tham khảo

- [MDN Web Docs — JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
- [javascript.info](https://javascript.info/) — nguồn chính của khóa học (bản gốc tiếng Anh, bản Việt do cộng đồng dịch tại `js-info/`)
- [TC39 Proposals](https://github.com/tc39/proposals)
- [caniuse.com](https://caniuse.com/) — kiểm tra browser support
- [web.dev Baseline](https://web.dev/baseline/)
