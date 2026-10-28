# Module trong JavaScript — [Level: Intermediate]

## 🔑 Khái niệm cốt lõi

**Module** là đơn vị gói gọn code nhỏ nhất có thể tái sử dụng — mỗi module có **scope riêng**, không làm bẩn global namespace, chỉ export những gì muốn chia sẻ và import những gì cần dùng. Trong JavaScript có ba hệ module chính:

**ESM (ECMAScript Modules)** — chuẩn chính thức của ECMAScript 6 (2015), dùng cú pháp `import` / `export`. ESM có hai đặc tính quan trọng:
- **Tĩnh (static)**: tất cả `import`/`export` được phân tích lúc parse, trước khi code chạy. Điều này cho phép tooling biết trước toàn bộ đồ thị phụ thuộc, từ đó thực hiện **tree-shaking** — loại bỏ code không dùng đến khi build.
- **Bất đồng bộ**: module được tải song song, không chặn main thread.

**CommonJS (CJS)** — hệ module nguyên thủy của Node.js, dùng `require()` / `module.exports`. CJS nạp **đồng bộ** — khi `require` chạy tới đâu, module đó được đánh giá ngay lúc đó. Không hỗ trợ tree-shaking vì cấu trúc động.

**Dynamic `import()`** — cú pháp nạp module theo yêu cầu (lazy loading), trả về Promise. Dùng khi muốn tải module chỉ khi thực sự cần (routing chunk, feature flag, heavy UI).

Hai hệ **không tương thích trực tiếp**: file ESM không thể `require()`, file CJS không thể `import`. Trong Node.js, bạn phải khai báo `"type": "module"` trong `package.json` (hoặc dùng đuôi `.mjs`/`.cjs`) để engine biết dùng hệ nào.

Trong repo này:
- `03_modules/app.js` — ví dụ ESM: import từ `logger/function.js`, `logger/const.js`, `logger/index.js`.
- `03_modules/01_commonjs-vs-esm/` — bảng so sánh chi tiết CommonJS vs ESM.
- `03_modules/logger/` — module logger ESM mẫu gồm 4 file: `const.js`, `function.js`, `logger.js`, `index.js`.

## 📐 Cấu trúc / Cú pháp

### ESM Syntax

```js
// Named exports — nhiều cái trong một file
// const.js
export const TYPE_LOG = 'log';
export const TYPE_WARN = 'warn';
export const TYPE_ERROR = 'error';

// Default export — một cái chính mỗi file
// logger.js
import { TYPE_LOG } from './const.js';
export default function logger(log, type = TYPE_LOG) {
  console[type](log);
}

// Import trong file khác
// app.js
import newLogger from './logger/index.js';          // default import
import { func_1 } from './logger/function.js';       // named import
import * as constant from './logger/const.js';       // namespace import
```

### Bảng cú pháp ESM

| Cú pháp | Mô tả |
|---|---|
| `export const/func/class Name = ...` | Named export — phải import đúng tên |
| `export default fn` | Default export — import đặt tên tùy ý |
| `import x from './mod.js'` | Import default |
| `import { x, y } from './mod.js'` | Import named |
| `import * as ns from './mod.js'` | Import all vào namespace |
| `export { x } from './mod.js'` | Re-export (thủy lôi barrel) |
| `export { default } from './mod.js'` | Re-export default |
| `import('./mod.js')` | Dynamic import → Promise |

### CommonJS Syntax

```js
// module.js
const TYPE_LOG = 'log';
function logger(log) { console.log(log); }
module.exports = { TYPE_LOG, logger };
// hoặc
exports.logger = logger;

// consumer.js
const { TYPE_LOG, logger } = require('./module.js');
```

### Cấu trúc thư mục module trong repo

```
16_modules/
├── README.md                          ← Tổng quan module
└── 03_modules/
    ├── README.md                      ← ESM chi tiết
    ├── app.js                         ← Entry point ESM demo
    ├── index.html                     ← Chạy app.js trong browser
    ├── logger/
    │   ├── README.md                  ← Module logger chi tiết
    │   ├── const.js                   ← export const TYPE_LOG/WARN/ERROR
    │   ├── function.js                ← export func_1/2/3
    │   ├── logger.js                  ← export default loggerFunction
    │   └── index.js                   ← barrel file: re-export default
    └── 01_commonjs-vs-esm/
        ├── README.md                  ← So sánh CJS vs ESM
        ├── app.js                     ← Demo ESM
        └── index.html                 ← Chạy demo
```

## ✅ Điểm mạnh — Tại sao nên dùng

1. **Tổ chức code rõ ràng** — tách đúng nơi chức năng, dễ bảo trì, dễ tìm code.
2. **Tránh xung đột global** — mỗi file có scope riêng, không lo tên biến trùng nhau.
3. **Tree-shaking** — ESM tĩnh cho phép bundler loại bỏ code không dùng → bundle nhỏ hơn.
4. **Lazy loading** — `import()` tải module theo yêu cầu, giảm dung lượng tải ban đầu.
5. **Chuẩn hóa cross-platform** — ESM chạy gốc trên browser hiện đại và Node.js.
6. **Phụ thuộc rõ ràng** — nhìn phần `import` là biết module cần gì, không phải mò code.
7. **Singleton module** — mỗi module được evaluate một lần, các import đều thấy cùng instance.
8. **Hoisted imports** — tên export "nhô lên" đầu scope, thứ tự khai báo không quan trọng.
9. **Async loading** — ESM tải module bất đồng bộ, không chặn rendering.
10. **Tooling hiện đại** — Vite/Webpack/Rollup tối ưu mạnh với ESM.

## ⚠️ Bẫy thường gặp & Hạn chế

### Bẫy 1: Trộn ESM và CommonJS
```js
// Trong file ESM (package.json có "type": "module")
const mod = require('./mod.js'); // ❌ TypeError: require is not defined
// Fix: dùng import, hoặc createRequire
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
```

### Bẫy 2: `import` không gọi được trong điều kiện
```js
if (condition) {
  import('./heavy-module.js'); // ❌ SyntaxError — import phải ở top-level
}
// Fix: dùng dynamic import()
if (condition) {
  import('./heavy-module.js').then(mod => mod.default()); // ✅
}
```

### Bẫy 3: Quên `"type": "module"` trong Node.js
```bash
# Không có "type": "module" trong package.json
node app.js  # ❌ SyntaxError: Cannot use import statement outside a module
# Fix: thêm "type": "module" vào package.json, hoặc đổi đuôi .mjs
```

### Bẫy 4: Default export vs named export nhầm lẫn
```js
// logger/index.js
export { default } from './logger.js';  // re-export default
export { default as newLogger } from './logger.js';  // re-export with alias

// app.js
import newLogger from './logger/index.js';  // ✅ default
import { newLogger } from './logger/index.js'; // ✅ named alias
import { default } from './logger/index.js';   // ✅ also works but awkward
```

### Bẫy 5: Circular dependency
```js
// a.js
import { b } from './b.js';
export const a = 'A';
export const bVal = b;  // b chưa được gán vì b.js đang import a.js

// b.js
import { a } from './a.js';
export const b = 'B';
```

### Bẫy 6: Relative path phải có đuôi `.js`
```js
import logger from './logger';     // ❌ ESM bắt buộc đuôi
import logger from './logger.js';  // ✅
```

### Bẫy 7: `export default` chỉ được một cái mỗi file
```js
export default function a() {}
export default function b() {}  // ❌ SyntaxError
```

## 💡 Khi nào dùng — Tình huống thực tế

1. **Project Node.js mới** — ESM là chuẩn được khuyến khích, dùng `"type": "module"`.
2. **Browser code trực tiếp** — `<script type="module" src="app.js">` không cần bundler.
3. **Thư viện phát hành npm** — ESM làm chuẩn nguồn, CJS làm fallback qua build.
4. **Lazy-load chunk lớn** — dynamic `import()` cho route-based code splitting.
5. **Tree-shaking cần thiết** — project Vite/Webpack/Rollup muốn bundle nhỏ nhất.
6. **Share code giữa nhiều file** — module logger, utils, constants tách riêng.
7. **Feature flag** — chỉ load module khi user bật tính năng đó.
8. **Micro-frontend** — mỗi submodule độc lập, load khi cần.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Cấu trúc module logger (file `logger/`)
```js
// logger/const.js — constants
export const TYPE_LOG = 'log';
export const TYPE_WARN = 'warn';
export const TYPE_ERROR = 'error';

// logger/function.js — utility functions
export function func_1(msg) {
  console.warn('func 1:', msg);
}
export function func_2(msg) {
  console.warn('func 2:', msg);
}
export function func_3(msg) {
  console.warn('func 3:', msg);
}

// logger/logger.js — core logic (default export)
import { TYPE_LOG } from './const.js';
export default function loggerFunction(log, type = TYPE_LOG) {
  console[type](log);
}

// logger/index.js — barrel file (re-export từ một điểm)
export { default } from './logger.js';
export { default as newLogger } from './logger.js';
```

### Ví dụ 2: Import trong app.js (file `03_modules/app.js`)
```js
// Import nhiều kiểu cùng lúc
import { func_1 } from "./logger/function.js";         // named import
import * as constant from "./logger/const.js";         // namespace import
import newLogger from "./logger/index.js";             // default import

// Sử dụng
newLogger("Sơn Nguyên", constant.TYPE_ERROR);  // console.error("Sơn Nguyên")
func_1("New message");                          // console.warn("func 1: New message")
console.log(constant.TYPE_LOG);                 // "log"
```

### Ví dụ 3: Dynamic import (lazy loading)
```js
async function loadChart() {
  // Chỉ load khi user click, không phải lúc page load
  const chartModule = await import('./chart-library.js');
  chartModule.createChart('#canvas');
}
document.getElementById('btn').addEventListener('click', loadChart);
```

### Ví dụ 4: Barrel file pattern (tập trung export)
```js
// index.js — barrel file
export { default as logger } from './logger.js';
export { func_1, func_2, func_3 } from './function.js';
export { TYPE_LOG, TYPE_WARN, TYPE_ERROR } from './const.js';

// Consumer
import { logger, func_1, TYPE_ERROR } from './logger/index.js';
```

### Ví dụ 5: ESM trong browser (index.html)
```html
<!DOCTYPE html>
<html>
<head><title>ESM Demo</title></head>
<body>
  <script type="module" src="app.js"></script>
</body>
</html>
```

### Ví dụ 6: Re-export với alias
```js
// logger/index.js
export { default } from './logger.js';           // import mặc định
export { default as newLogger } from './logger.js'; // với alias

// app.js — hai cách import khác nhau từ cùng file
import loggerFunc from './logger/index.js';
import { newLogger } from './logger/index.js';
```

### Ví dụ 7: So sánh import/default vs import/named
```js
// ✅ Default — đặt tên tùy ý
import MyLogger from './logger.js';

// ✅ Named — phải đúng tên export
import { loggerFunction } from './logger.js';

// ✅ Namespace — tất cả vào object
import * as Logger from './logger.js';
Logger.loggerFunction('msg');
Logger.TYPE_LOG; // undefined nếu không export named
```

### Ví dụ 8: Module graph — đồ thị phụ thuộc
```
app.js
  ├── logger/index.js  (barrel)
  │     └── logger.js (default)
  │           └── const.js (TYPE_LOG)
  ├── logger/function.js (func_1)
  └── logger/const.js (TYPE_ERROR namespace)
```
Nhờ ESM tĩnh, bundler có thể hiển thị đồ thị này và tree-shake phần không dùng.

## 🔬 So sánh với alternatives

| Hệ module | Syntax | Load | Tree-shake | Browser native | Node native |
|---|---|---|---|---|---|
| **ESM** | `import`/`export` | Async, static | ✅ Có | ✅ `type="module"` | ✅ `"type": "module"` |
| **CommonJS** | `require`/`module.exports` | Sync, dynamic | ❌ Không | ❌ (cần polyfill) | ✅ Mặc định |
| **AMD** | `define`/`require` | Async | ❌ Khó | ✅ RequireJS | ❌ |
| **UMD** | Wrapper nhiều hệ | Tùy implementation | ❌ | ✅ | ✅ |
| **SystemJS** | `System.import` | Async | ✅ | ✅ | ✅ |

## 📊 Performance & Best Practices

- **Tree-shaking**: chỉ hoạt động với ESM cấu trúc tĩnh — đừng dùng `export default` +ghép động tên.
- **Module size**: ESM có overhead nhỏ (~1-2KB) so với IIFE, nhưng bù lại bằng tree-shaking.
- **Load order**: ESM hoisted, nên `import` ở đầu file giúp tooling phân tích dễ hơn.
- **Relative paths**: luôn dùng đuôi `.js` trong ESM — browser không tự thêm.
- **Avoid deep dependency chains**: mỗi module tăng thời gian parse; chia nhỏ hợp lý.
- **Barrel files**: hữu ích cho API public, nhưng có thể gây circular dependency nếu không cẩn thận.
- **Dynamic import**: giảm initial load time — chỉ load khi cần, phù hợp route-based splitting.
- **Node.js**: dùng `"type": "module"` trong `package.json` cho project mới; `.mjs`/`.cjs` cho mixed projects.

## 🔗 Liên kết chéo

- Xem thêm: `16_modules/03_modules/01_commonjs-vs-esm/` — so sánh chi tiết CJS vs ESM.
- Xem thêm: `16_modules/03_modules/logger/` — module logger mẫu hoàn chỉnh.
- Xem thêm: `15_iterators-and-generators/` — generator có thể export từ module.
- Xem thêm: `17_memory-management/` — module singleton behavior và memory.
- Xem thêm: `18_dom-apis/` — DOM API có thể import thành module riêng.
