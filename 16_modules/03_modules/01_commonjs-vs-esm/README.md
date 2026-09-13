# CommonJS vs ESM — [Level: Intermediate]

## 🔑 Khái niệm cốt lõi

JavaScript có **hai hệ module chính** đang tồn tại song song: **CommonJS (CJS)** và **ES Modules (ESM)**. Hiểu rõ sự khác biệt giữa chúng là yếu tố sống còn khi làm việc với cả Node.js và browser.

**CommonJS** — hệ module nguyên thủy của Node.js (trước khi ESM ra đời), dùng cú pháp `require()` và `module.exports`. Đặc điểm then chốt:
- **Đồng bộ (sync)**: khi `require()` chạy tới đâu, module đó được đánh giá ngay lúc đó. Thứ tự quan trọng.
- **Động (dynamic)**: `require()` có thể gọi trong hàm, điều kiện, vòng lặp — path là string runtime.
- **Không tree-shake**: bundler không biết export nào không dùng vì cấu trúc động.
- **File extension**: `.js` (mặc định) hoặc `.cjs` (bắt buộc chỉ định CJS trong ESM project).

**ESM (ES Modules)** — chuẩn chính thức ECMAScript 6 (2015), dùng `import`/`export`. Đặc điểm then chốt:
- **Tĩnh (static)**: tất cả `import`/`export` được phân tích lúc parse, trước khi code chạy. Engine biết trước toàn bộ dependency graph.
- **Bất đồng bộ (async)**: module được tải song song, không chặn main thread.
- **Top-level only**: `import`/`export` phải ở cấp cao nhất của file — không đặt trong hàm/điều kiện.
- **Tree-shakeable**: bundler có loại bỏ export không dùng vì cấu trúc tĩnh.
- **File extension**: `.js` (khi `package.json` có `"type": "module"`) hoặc `.mjs` (luôn ESM).

Điểm mấu chốt để nhớ: **sync vs async**, **dynamic (require có thể gọi trong hàm/theo điều kiện) vs static (import ở top-level)**.

Trong repo này, `app.js` của thư mục `01_commonjs-vs-esm/` chạy demo ESM, import từ `./logger/index.js` (thư mục cùng cấp). Phần CommonJS chỉ là minh họa comment — cả hai hệ đều tồn tại trong cùng project nhưng không trộn trực tiếp.

## 📐 Cấu trúc / Cú pháp

### So sánh syntax

| Tính năng | CommonJS | ESM |
|---|---|---|
| Import | `const mod = require('./mod.js')` | `import mod from './mod.js'` |
| Named import | `const { x } = require('./mod.js')` | `import { x } from './mod.js'` |
| Export | `module.exports = ...` | `export default ...` |
| Named export | `exports.x = ...` | `export const x = ...` |
| Dynamic import | `require('./mod.js')` (sync) | `import('./mod.js')` (async, Promise) |
| Side-effect | `require('./mod.js')` | `import './mod.js'` |
| File extension | `.js` hoặc `.cjs` | `.js` (với `"type": "module"`) hoặc `.mjs` |

### Bảng so sánh chi tiết

|  | CommonJS (Node.js) | ESM (ES6+) |
|---|---|---|
| **Syntax** | `require` / `module.exports` | `import` / `export` |
| **Load** | Synchronous | Asynchronous, static |
| **Top-level?** | Không bắt buộc (gọi trong hàm được) | Bắt buộc (trừ `import()`) |
| **File type** | `.js`/`.cjs` (Node mặc định) | `.mjs`/`"type": "module"` |
| **Tree-shaking** | Không | Có |
| **Module caching** |cache theo path string | cache theo module instance (singleton) |
| **Hoisting** | Không | Có — import names hoisted |
| **Dynamic path** | ✅ `require('./' + name + '.js')` | ❌ (trừ `import()`) |
| **Browser native** | ❌ Cần polyfill/bundler | ✅ `<script type="module">` |

## ✅ Điểm mạnh

### CommonJS:
1. **Nạp đồng bộ đơn giản** — dễ hiểu, dễ debug, thứ tự execute rõ ràng.
2. **Gọi được `require` trong điều kiện/vòng lặp** — flexible, tiện cho lazy-load thủ công.
3. **Đã thống trị Node.js suốt nhiều năm** — hàng loạt thư viện cũ viết theo chuẩn này (Express, Sequelize, v.v.).
4. **Không cần config** — Node hiểu `.js` là CJS mặc định, không cần `package.json`.

### ESM:
1. **Tĩnh → tree-shaking** — bundle gọn hơn, ít code thừa hơn đáng kể.
2. **Chuẩn quốc tế** — chạy trên cả trình duyệt và Node.js mà không cần transform.
3. **Nạp bất đồng bộ** — không chặn rendering, load song song các module.
4. **Hỗ trợ `import()` lazy** — tải module theo yêu cầu runtime.
5. **Better tooling** — ESLint, TypeScript, IDE có thể static analysis chính xác.
6. **Dead code elimination** — compiler biết chắc export nào không dùng để bỏ hẳn.

## ⚠️ Bẫy thường gặp & Hạn chế

### Bẫy 1: Không dán code CommonJS vào file ESM
```js
// File có "type": "module" trong package.json
const fs = require('fs'); // ❌ ReferenceError: require is not defined
// Fix: import fs from 'fs';
```

### Bẫy 2: `require` trong ESM báo lỗi `ERR_REQUIRE_ESM`
```js
// Khi package.json có "type": "module"
const chalk = require('chalk'); // ❌ ERR_REQUIRE_ESM
// Fix: import chalk from 'chalk';
// Hoặc: const { createRequire } = await import('module');
//        const require = createRequire(import.meta.url);
```

### Bẫy 3: `import` không gọi được động trong điều kiện
```js
if (process.env.NODE_ENV === 'production') {
  import('./prod-config.js'); // ❌ SyntaxError
}
// Fix:
if (process.env.NODE_ENV === 'production') {
  const mod = await import('./prod-config.js'); // ✅ dynamic import
}
```

### Bẫy 4: Node dùng trường `"type"` trong `package.json` để phân biệt
```json
{ "type": "module" }  // Tất cả .js trong project này là ESM
```
Nếu không có field này, `.js` được hiểu là **CommonJS** — `import`/`export` sẽ lỗi cú pháp.

### Bippy 5: Relative path trong ESM bắt buộc có đuôi `.js`
```js
import logger from './logger';   // ❌ browser/Node yêu cầu đuôi
import logger from './logger.js'; // ✅
```

### Bẫy 6: Circular dependency khác nhau giữa hai hệ
- CJS: module.exports là object, có thể gán sau — circular ít nghiêm trọng hơn.
- ESM: import là binding sống (live binding), circular có thể gây `undefined` tạm thời.

## 💡 Khi nào dùng — Tình huống thực tế

1. **Node project mới / thư viện phát hành npm** → ưu tiên ESM, thêm `"type": "module"` vào `package.json`.
2. **Code trình duyệt thuần (không bundle)** → ESM với `<script type="module" src="app.js">`.
3. **Tooling/script cũ của Node** vẫn dùng CommonJS tốt — không bắt buộc đổi nếu chưa cần.
4. **Cần tree-shaking** → ESM (Vite/Webpack/Rollup đều tối ưu với ESM).
5. **Cần module-load theo yêu cầu** → dynamic `import()` trong ESM.
6. **Legacy codebase CJS** → tiếp tục dùng CJS, chỉ chuyển sang ESM khi rewrite hoặc migrate.
7. **Mixed project** → dùng `.mjs` cho ESM, `.cjs` cho CJS, `package.json` không set `"type"`.
8. **Browser polyfill cho old IE** → CJS qua bundler (Webpack) vẫn là lựa chọn thực tế.

## 🎯 Ví dụ minh họa

### Ví dụ 1: ESM demo (file `app.js`)
```js
// ESM — chạy được trong browser với <script type="module"> hoặc Node "type":"module"
import { log } from "./logger/index.js";
log("hi");
```

### Ví dụ 2: CommonJS demo (file `app.cjs`)
```js
// CommonJS — chỉ chạy được trong Node không có "type":"module"
const { log } = require("./logger");
log("hi");
```

### Ví dụ 3: Dynamic import trong ESM (lazy load)
```js
// ESM — load module theo điều kiện runtime
async function loadModule(flag) {
  if (flag) {
    const mod = await import('./heavy-module.js');
    mod.init();
  }
}
button.addEventListener('click', () => loadModule(true));
```

### Ví dụ 4: Mixed project (`.mjs` + `.cjs`)
```js
// app.mjs — ESM file
import { func_1 } from './logger/function.mjs';
func_1('from ESM');

// legacy.cjs — CommonJS file
const { legacyFunc } = require('./legacy-module.cjs');
legacyFunc();
```

### Ví dụ 5: Tạo require trong ESM (workaround)
```js
// ESM file — cần dùng require
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const lodash = require('lodash'); // ✅ work around
```

### Ví dụ 6: Package.json config
```json
{
  "name": "my-project",
  "type": "module",
  "main": "dist/index.js",
  "exports": {
    ".": "./src/index.js",
    "./logger": "./src/logger/index.js"
  }
}
```

## 🔬 So sánh với alternatives

| Tiêu chí | CommonJS | ESM | AMD (RequireJS) | UMD |
|---|---|---|---|---|
| Syntax | `require`/`module.exports` | `import`/`export` | `define`/`require` | Wrapper |
| Load | Sync | Async | Async | Tùy |
| Tree-shake | ❌ | ✅ | ❌ | ❌ |
| Browser native | ❌ | ✅ | ✅ | ✅ |
| Node native | ✅ | ✅ (config) | ❌ | ✅ |
| Learning curve | Thấp | Trung bình | Cao | Cao |
| Current trend | Legacy | **Standard** | Deprecated | Niche |

## 📊 Performance & Best Practices

- **Performance ESM**: async load cho phép song song download — nhanh hơn CJS sequential require.
- **Bundle size**: ESM + tree-shaking giảm bundle đáng kể so với CJS (đôi khi 40-60% nhỏ hơn).
- **Migration tip**: đổi `package.json` → `"type": "module"`, đổi `.js` → `.cjs` cho file CJS cũ.
- **Tooling**: dùng `--input-type=module` với Node cho file `.js` chạy ESM mà không cần `"type"`.
- **Avoid mixed system**: không mix `require` và `import` trong cùng file — gây lỗi.
- **Use `.mjs`/`.cjs` explicit**: khi project có cả hai hệ, dùng đuôi rõ ràng thay vì `"type"` flag.
- **Test both**: kiểm tra code chạy được trên cả browser và Node trước khi deploy.

## 🔗 Liên kết chéo

- Xem thêm: `16_modules/03_modules/` — Tổng quan ESM module system.
- Xem thêm: `16_modules/03_modules/logger/` — Module logger ESM mẫu.
- Xem thêm: `15_iterators-and-generators/` — generator export từ module.
- Xem thêm: `17_memory-management/` — module singleton và memory.
- Xem thêm: MDN Web Docs — JavaScript modules: import and export.
