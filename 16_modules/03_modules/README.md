# Module — ESM (ECMAScript Modules) — [Level: Intermediate]

## 🔑 Khái niệm cốt lõi

Thư mục này tập trung vào **ES Modules (ESM)** — hệ module chuẩn ECMAScript 6, dùng cú pháp `import` / `export`. ESM là tương lai của JavaScript module system, được thiết kế để hoạt động tốt trên cả browser và Node.js.

Khác với CommonJS (CJS) của Node.js, ESM có những đặc tính then chốt:

- **Tĩnh (static)**: mọi `import` / `export` được phân tích ngay khi parse file — trước khi code chạy. Engine biết trước toàn bộ đồ thị phụ thuộc, cho phép **tree-shaking** (loại bỏ code không dùng) và tối ưu load song song.
- **Bất đồng bộ**: trình duyệt / Node tải module theo kiểu async — module con có thể tải trong khi parent vẫn đang parse.
- **Hoisted**: tên export "nhô lên" đầu scope, thứ tự khai báo `import`/`export` không quan trọng.
- **Singleton**: mỗi module được "đánh giá" (evaluate) **một lần duy nhất** trong suốt lifecycle. Các bên import đều thấy cùng một instance — kể cả khi import nhiều lần từ nhiều file.

Cấu trúc thư mục:
- `01_commonjs-vs-esm/` — bảng so sánh CommonJS vs ESM kèm demo chạy được.
- `logger/` — module logger thuần ESM gồm 4 file nhỏ: `const.js`, `function.js`, `logger.js`, `index.js`.

### Quy tắc vàng của ESM

1. `import`/`export` **phải ở top-level** — không đặt trong `if`, `function`, hay vòng lặp (trừ dynamic `import()`).
2. Path phải **tương đối** (`./`, `../`) và có **đuôi `.js`** — browser không tự thêm extension.
3. Chỉ được **một `export default`** mỗi file — named export thì bao nhiêu cũng được.
4. Module được **evaluate một lần** — import nhiều lần cùng module vẫn chỉ chạy code một lần.

## 📐 Cấu trúc / Cú pháp

### Các dạng export

```js
// Named export — bao nhiêu cũng được
export const PI = 3.14159;
export function greet(name) { return `Hello ${name}`; }
export class Person { constructor(name) { this.name = name; } }

// Default export — tối đa 1 per file
export default function main() { console.log('main'); }
// hoặc
const helper = () => {};
export { helper as default };
```

### Các dạng import

```js
// Default import — đặt tên tùy ý
import main from './module.js';

// Named import — phải đúng tên
import { PI, greet, Person } from './module.js';

// Namespace import — tất cả vào object
import * as math from './module.js';
math.PI; math.greet('World');

// Rename khi import
import { greet as sayHello } from './module.js';

// Side-effect only (chạy code, không lấy gì)
import './module.js';
```

### Re-export (thủy lôi / barrel pattern)

```js
// Forward export — chuyển tiếp từ module khác
export { default } from './logger.js';
export { default as newLogger } from './logger.js';
export { PI } from './math.js';

// Barrel file — gom nhiều export thành một điểm
export { loggerFunction } from './logger.js';
export { func_1, func_2 } from './function.js';
export { TYPE_LOG, TYPE_ERROR } from './const.js';
```

### Dynamic import

```js
// Trả về Promise — load module theo yêu cầu
const mod = await import('./heavy-module.js');
mod.default(); // gọi default export

// Trong function/condition — được phép
if (featureFlag) {
  const mod = await import('./feature.js');
  mod.init();
}
```

## ✅ Điểm mạnh — Tại sao nên dùng

1. **Tree-shaking được** — bundler (Vite/Webpack/Rollup) loại bỏ export không dùng → bundle nhỏ hơn 30-70%.
2. **Chạy natively** trên browser hiện đại — chỉ cần `<script type="module" src="app.js">`, không cần bundler cho app đơn giản.
3. **Nạp bất đồng bộ và hoisted** — khởi động nhanh hơn so với chuỗi `require` đồng bộ của CJS.
4. **Lazy-load dễ dàng** — dynamic `import()` tải module khi runtime cần, giảm initial bundle size.
5. **Cú pháp gọn rõ** — `import {x} from ...` / `export default` tách bạch, dễ đọc.
6. **Static analysis** — tooling (ESLint, TypeScript, bundler) phân tích dependency graph chính xác.
7. **Cross-environment** — cùng code chạy được trên browser và Node.js (với cấu hình đúng).
8. **Module caching** — evaluate một lần, các import sau dùng cache → tiết kiệm CPU.
9. **Dead code elimination** — compiler biết chắc export nào không dùng để bỏ hẳn.
10. **Future-proof** — ESM là chuẩn chính thức của ECMAScript, được tất cả engine hiện đại support.

## ⚠️ Bẫy thường gặp & Hạn chế

### Bẫy 1: Phải khai báo môi trường ESM
```bash
# Node.js mặc định hiểu .js là CommonJS
node app.js   # ❌ SyntaxError: Cannot use import statement outside a module
# Fix 1: package.json có "type": "module"
# Fix 2: đổi thành app.mjs
```

### Bẫy 2: `import` không gọi được trong điều kiện
```js
if (condition) {
  import('./mod.js'); // ❌ SyntaxError
}
// Fix: dùng dynamic import()
if (condition) {
  import('./mod.js').then(mod => mod.default());
}
```

### Bẫy 3: Không dùng `require` trong ESM
```js
import fs from 'fs';
const data = require('./data.json'); // ❌ ReferenceError: require is not defined
// Fix: import() hoặc createRequire
```

### Bẫy 4: Relative path thiếu đuôi `.js`
```js
import logger from './logger';      // ❌ browser yêu cầu đuôi
import logger from './logger.js';   // ✅
```

### Bẫy 5: Circular dependency
```js
// a.js
import { b } from './b.js';
export const a = 1;

// b.js
import { a } from './a.js';
export const b = a + 1;  // a có thể là undefined nếu load order sai
```

### Bẫy 6: Default export vs named export nhầm
```js
// logger/index.js
export { default } from './logger.js';  // re-export default
// app.js
import newLogger from "./logger/index.js";  // ✅ default
import { newLogger } from "./logger/index.js"; // cũng ✅ nếu index.js có re-export named
```

## 💡 Khi nào dùng — Tình huống thực tế

1. **Project Node.js mới** — ESM là chuẩn khuyến khích, dùng `"type": "module"` trong `package.json`.
2. **Code browser thuần** — `<script type="module" src="app.js">`, không cần build step.
3. **Thư viện/npm package** — ESM làm chuẩn nguồn, build ra CJS nếu cần backward compatibility.
4. **Tree-shaking cần thiết** — project dùng Vite/Webpack/Rollup muốn bundle nhỏ nhất.
5. **Lazy-load chunk nặng** — dynamic `import()` cho route-based code splitting trong SPA.
6. **Micro-frontend** — mỗi submodule độc lập, load khi user navigate đến.
7. **Feature flags** — chỉ import module khi flag bật, tiết kiệm bandwidth.
8. **Shared utilities** — tách constants, helpers thành module riêng để tái sử dụng.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Logger module structure (file `logger/`)
```js
// logger/const.js
export const TYPE_LOG = 'log';
export const TYPE_WARN = 'warn';
export const TYPE_ERROR = 'error';

// logger/function.js
export function func_1(msg) {
  console.warn('func 1:', msg);
}
export function func_2(msg) {
  console.warn('func 2:', msg);
}
export function func_3(msg) {
  console.warn('func 3:', msg);
}

// logger/logger.js
import { TYPE_LOG } from './const.js';
export default function loggerFunction(log, type = TYPE_LOG) {
  console[type](log);
}

// logger/index.js — barrel file
export { default } from './logger.js';
export { default as newLogger } from './logger.js';
```

### Ví dụ 2: App importing multiple styles (file `03_modules/app.js`)
```js
// Named import
import { func_1 } from "./logger/function.js";

// Namespace import
import * as constant from "./logger/const.js";

// Default import
import newLogger from "./logger/index.js";

// Usage
newLogger("Sơn Nguyên", constant.TYPE_ERROR); // console.error
func_1("New message");                       // console.warn
```

### Ví dụ 3: HTML entry point (file `03_modules/index.html`)
```html
<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <title>ESM Demo</title>
</head>
<body>
  <!-- type="module" là bắt buộc để browser hiểu ESM -->
  <script type="module" src="app.js"></script>
</body>
</html>
```

### Ví dụ 4: Re-export với nhiều alias
```js
// logger/index.js
export { default } from './logger.js';              // export mặc định
export { default as newLogger } from './logger.js'; // export có alias

// app.js — 2 cách import khác nhau từ cùng 1 file
import loggerFunc from "./logger/index.js";    // nhận default
import { newLogger } from "./logger/index.js";  // nhận named alias
```

### Ví dụ 5: Dynamic import — lazy load chart library
```js
async function initDashboard() {
  const chartModule = await import('./chart-lib.js');
  chartModule.createChart('#chart', data);
}
button.addEventListener('click', initDashboard);
```

### Ví dụ 6: Tree-shaking trong thực tế
```js
// utils/math.js — có nhiều function
export function add(a, b) { return a + b; }
export function subtract(a, b) { return a - b; }
export function multiply(a, b) { return a * b; }
export function divide(a, b) { return a / b; }

// app.js — chỉ dùng add
import { add } from './utils/math.js';
console.log(add(2, 3)); // 5

// Bundler sẽ bỏsubtract, multiply, divide ra khỏi bundle (tree-shaking)
```

### Ví dụ 7: Module evaluation chỉ một lần
```js
// counter.js
let count = 0;
export function increment() { count++; return count; }
export function getCount() { return count; }
console.log('counter.js evaluated'); // chỉ in 1 lần dù import ở nhiều nơi

// a.js
import { increment } from './counter.js';
increment();

// b.js
import { getCount } from './counter.js';
console.log(getCount()); // 1 — cùng instance, không reset
```

## 🔬 So sánh với alternatives

| Tiêu chí | ESM | CommonJS | AMD | UMD |
|---|---|---|---|---|
| Syntax | `import`/`export` | `require`/`module.exports` | `define`/`require` | Wrapper nhiều hệ |
| Load | Async, static | Sync, dynamic | Async | Tùy implementation |
| Tree-shake | ✅ Hỗ trợ | ❌ Không | ❌ Khó | ❌ |
| Browser native | ✅ `type="module"` | ❌ Cần polyfill | ✅ RequireJS | ✅ SystemJS |
| Node native | ✅ `"type": "module"` | ✅ Mặc định | ❌ | ✅ |
| Learning curve | Trung bình | Thấp | Cao | Cao |

## 📊 Performance & Best Practices

- **Tree-shaking effectiveness**: phụ thuộc vào static structure — đừng dùng `eval()` hay dynamic string trong import path.
- **Bundle size**: ESM module overhead ~1-2KB/một file, nhưng tree-shaking có thể giảm bundle 30-70%.
- **Load parallelism**: browser tải nhiều ESM song song — tận dụng bằng cách chia module nhỏ, độc lập.
- **Avoid deep nesting**: dependency chain quá sâu làm tăng thời gian resolve — giữ flat structure.
- **Use bare imports for packages**: `import lodash from 'lodash'` — bundler resolve từ `node_modules`.
- **Prefer named exports over default**: named export clear hơn, tree-shaking chính xác hơn, refactor dễ hơn.
- **Barrel files trade-off**: dễ dùng nhưng có thể gây circular dependency — cân nhắc dùng direct import thay vì barrel.
- **TypeScript integration**: ESM + TypeScript là combo chuẩn — type-checking tại compile time, tree-shaking tại build.

## 🔗 Liên kết chéo

- Xem thêm: `16_modules/03_modules/01_commonjs-vs-esm/` — so sánh chi tiết CommonJS vs ESM.
- Xem thêm: `16_modules/03_modules/logger/` — module logger mẫu hoàn chỉnh.
- Xem thêm: `15_iterators-and-generators/` — generator có thể export từ module.
- Xem thêm: `17_memory-management/` — module singleton và GC behavior.
- Xem thêm: `18_dom-apis/` — DOM API có thể import thành module riêng.
