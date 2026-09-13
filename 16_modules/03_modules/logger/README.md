# Logger — Ví dụ Module ESM — [Level: Intermediate]

## 🔑 Khái niệm cốt lõi

Thư mục này là một **module logger** viết hoàn toàn bằng ESM, minh họa cách tách một chức năng (log) thành nhiều tệp nhỏ với `import` / `export`. Đây chính là "thư viện con" được `03_modules/app.js` sử dụng để demo các kiểu import khác nhau.

Cấu trúc 4 file và vai trò từng file:

| File | Vai trò | Export |
|---|---|---|
| `const.js` | **Hằng số** loại log | `TYPE_LOG`, `TYPE_WARN`, `TYPE_ERROR` |
| `function.js` | **Hàm tiện ích** | `func_1`, `func_2`, `func_3` |
| `logger.js` | **Core logic** — hàm log chính | `default` (loggerFunction) |
| `index.js` | **Barrel file** — cổng xuất duy nhất | Re-export `default` và alias `newLogger` |

Cách hoạt động: `logger.js` import `TYPE_LOG` từ `const.js` để làm giá trị mặc định cho tham số `type`. `index.js` (barrel file) nhận default-export từ `logger.js` rồi "mở lại" cho bên ngoài qua cả default export lẫn named export có alias. Vì ESM mang tính **tĩnh**, bạn chỉ cần nhìn các dòng `import`/`export` là hiểu toàn bộ đồ thị phụ thuộc.

**Barrel file** (`index.js`) là pattern phổ biến trong các project lớn: thay vì consumer phải nhớ đúng đường dẫn `./logger/logger.js`, họ chỉ cần import từ `./logger/index.js` — một điểm vào duy nhất.

## 📐 Cấu trúc / Cú pháp

### File: `const.js`
```js
export const TYPE_LOG = 'log';
export const TYPE_WARN = 'warn';
export const TYPE_ERROR = 'error';
```
Export 3 hằng số string — dùng làm loại log cho `console[type]()`.

### File: `function.js`
```js
export function func_1(msg) {
  console.warn('func 1:', msg);
}
export function func_2(msg) {
  console.warn('func 2:', msg);
}
export function func_3(msg) {
  console.warn('func 3:', msg);
}
```
3 hàm tiện ích cùng pattern — example cho việc nhóm nhiều named export trong 1 file.

### File: `logger.js`
```js
import { TYPE_LOG } from './const.js';  // import named from同级 file

function loggerFunction(log, type = TYPE_LOG) {
  console[type](log);                    // dynamic method call: console['log'](log)
}
export default loggerFunction;           // default export
```
Hàm chính: nhận message và type (mặc định `TYPE_LOG`), gọi `console[type](log)`.

### File: `index.js` (Barrel)
```js
export { default } from './logger.js';           // dòng 4 trong app.js (commented)
export { default as newLogger } from './logger.js'; // dòng 5 trong app.js
```
Hai dòng re-export: một default, một có alias `newLogger`. Consumer có thể chọn cách import nào phù hợp.

### Đồ thị phụ thuộc
```
app.js
  ├── logger/index.js (barrel)
  │       └── logger.js (default)
  │             └── const.js (TYPE_LOG)
  ├── logger/function.js (func_1)
  └── logger/const.js (TYPE_ERROR namespace)
```

## ✅ Điểm mạnh — Tại sao nên dùng

1. **Tách biệt rõ ràng** — hằng số, hàm tiện ích, core logic và cổng xuất nằm riêng — dễ bảo trì, dễ test từng phần.
2. **Barrel file** giúp bên ngoài chỉ import một đường dẫn duy nhất thay vì nhớ từng file con.
3. **Default + named export song song** minh họa đầy đủ cú pháp ESM — học được cả hai pattern.
4. **Nhiều mức log** (`log` / `warn` / `error`) chỉ bằng một tham số mặc định — code linh hoạt, mở rộng dễ.
5. **Có thể tái sử dụng** như mẫu chuẩn cho mọi module tự viết — constants → logic → barrel.
6. **Dependency graph rõ ràng** — mỗi file import những gì từ file nào, nhìn là hiểu.
7. **Testable** — mỗi file có thể test độc lập (mock const.js khi test logger.js).
8. **Scalable** — thêm hàm mới vào `function.js` không ảnh hưởng logger core.
9. **Pattern production-ready** — đây chính là cách các thư viện lớn (React, Lodash) tổ chức code.
10. **Giáo dục toàn diện** — bao phủ cả named export, default export, re-export, barrel pattern.

## ⚠️ Bẫy thường gặp & Hạn chế

### Bẫy 1: Barrel file re-export default nên import phải dùng default syntax
```js
// logger/index.js có: export { default } from './logger.js'
// app.js — đúng:
import newLogger from "./logger/index.js";
// app.js — cũng đúng (vì index.js còn re-export named alias):
import { newLogger } from "./logger/index.js";
// Hai cách này cho cùng một hàm nhưng tên import khác nhau
```

### Bẫy 2: File ESM thuần — không dùng được bằng `require`
```js
// Nếu môi trường là CommonJS:
const logger = require('./logger/index.js'); // ❌ TypeError: require is not defined
// Fix: chuyển project sang ESM hoặc dùng createRequire
```

### Bẫy 3: Namespace import cần đúng key
```js
import * as constant from "./logger/const.js";
console.log(constant.TYPE_ERROR); // ✅ 'error'
console.log(constant.TYPE_LOGG);  // ❌ undefined — tên phải khớp exact
```

### Bẫy 4: `console[type]` với type không hợp lệ → runtime error
```js
newLogger("test", "nonexistent"); // ❌ TypeError: console.nonexistent is not a function
// Luôn validate type trước khi gọi
```

### Bẫy 5: Circular dependency nguy hiểm
```js
// Nếu const.js import từ logger.js → circular!
// const.js ← logger.js ← const.js
// Fix: chỉ import one-way: logger.js → const.js, không ngược lại
```

### Bẫy 6: Barrel file có thể gây circular
```js
// index.js import từ logger.js, logger.js import từ const.js
// Nếu const.js lại import từ index.js → circular dependency
// Fix: đảm bảo graph là DAG (Directed Acyclic Graph)
```

## 💡 Khi nào dùng — Tình huống thực tế

1. **Làm khuôn mẫu tổ chức module nhỏ** trong ứng dụng — constants → logic → barrel.
2. **Xây dựng thư viện log / debug** tái sử dụng trong nhiều file của project.
3. **Tách hằng số cấu hình** (mức log, config flags) khỏi logic chính — dễ thay đổi không động chạm code.
4. **Làm quen với barrel file / re-export** trước khi gặp mô hình này ở thư viện lớn (React, Vue plugins).
5. **Prototype nhanh** một utility module có cấu trúc production-ready.
6. **Demonstration trong interview** — thể hiện hiểu biết về module system, tree-shaking, barrel pattern.
7. **Base cho design system** — component library thường có pattern tương tự (index.js barrel).
8. **Micro-frontend shared utilities** — logger module dùng chung nhiều submodule.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Full import chain (file `app.js`)
```js
// Named import từ function.js
import { func_1 } from "./logger/function.js";

// Namespace import từ const.js
import * as constant from "./logger/const.js";

// Default import từ barrel file
import newLogger from "./logger/index.js";

// Sử dụng
newLogger("Sơn Nguyên", constant.TYPE_ERROR); // console.error("Sơn Nguyên")
func_1("New message");                        // console.warn("func 1: New message")
```

### Ví dụ 2: Barrel file re-export两种写法
```js
// logger/index.js
export { default } from './logger.js';           // cách 1: re-export default
export { default as newLogger } from './logger.js'; // cách 2: re-export có alias

//两种 export đều khả dụng từ consumer
import loggerFunc from './logger/index.js';  // nhận default
import { newLogger } from './logger/index.js'; // nhận named alias
```

### Ví dụ 3: Thêm hàm mới vào module
```js
// function.js — thêm func_4
export function func_4(msg) {
  console.info('func 4:', msg);  // console.info thay vì warn
}

// app.js — import thêm
import { func_4 } from "./logger/function.js";
func_4("Info message");
```

### Ví dụ 4: Validate type trước khi log
```js
// logger/logger.js — thêm validation
import { TYPE_LOG } from './const.js';

const validTypes = ['log', 'warn', 'error', 'info'];

export default function loggerFunction(log, type = TYPE_LOG) {
  if (!validTypes.includes(type)) {
    console.error(`[Logger] Invalid type: ${type}. Using 'log' instead.`);
    type = TYPE_LOG;
  }
  console[type](log);
}
```

### Ví dụ 5: Module với nhiều default export (pattern advanced)
```js
// logger/logger.js — export default là function, named là config
import { TYPE_LOG } from './const.js';

export default function loggerFunction(log, type = TYPE_LOG) {
  console[type](log);
}

export const LOG_CONFIG = {
  enabled: true,
  timestamp: true,
  maxMessages: 1000
};

// logger/index.js — barrel cả default và named
export { default, LOG_CONFIG } from './logger.js';
```

### Ví dụ 6: Dynamic type selection
```js
// app.js — chọn type dựa trên điều kiện
import newLogger from "./logger/index.js";
import * as constant from "./logger/const.js";

function logWithSeverity(msg, severity) {
  const typeMap = {
    low: constant.TYPE_LOG,
    medium: constant.TYPE_WARN,
    high: constant.TYPE_ERROR
  };
  newLogger(msg, typeMap[severity] || constant.TYPE_LOG);
}

logWithSeverity("System ready", "low");       // console.log
logWithSeverity("Disk space low", "medium");  // console.warn
logWithSeverity("Database down", "high");     // console.error
```

### Ví dụ 7: Unit test pattern cho module
```js
// logger.test.js — test module độc lập
import loggerFunction from './logger/logger.js';
import { TYPE_ERROR } from './logger/const.js';

// Mock console
const originalError = console.error;
console.error = jest.fn();

test('logger uses correct console method', () => {
  loggerFunction('error msg', TYPE_ERROR);
  expect(console.error).toHaveBeenCalledWith('error msg');
});

console.error = originalError;
```

## 🔬 So sánh với alternatives

| Pattern | Ưu điểm | Nhược điểm | Phù hợp khi |
|---|---|---|---|
| **Barrel file (index.js)** | Một điểm import, API rõ | Có thể gây circular | Project lớn, nhiều submodule |
| **Direct import** | Không có abstraction overhead | Path dài, dễ nhầm | Project nhỏ, module ít |
| **Single file module** | Đơn giản, không cần barrel | File dài, khó navigate | Utility function ít |
| **Namespace import** | Group related exports | Không tree-shake tốt | Export nhiều items từ 1 file |

## 📊 Performance & Best Practices

- **Barrel file overhead**: negligible (~1ms parse), nhưng có thể gây circular nếu không cẩn thận.
- **Tree-shaking**: direct named import tốt hơn namespace import — `import { func_1 }` vs `import * as ns`.
- **Keep barrel flat**: `index.js` chỉ re-export, không nên có logic phức tạp.
- **Validate exports**: dùng TypeScript `export type` để enforce API contract.
- **Naming convention**: `index.js` = barrel, `logger.js` = core, `const.js` = constants — pattern nhất quán.
- **Avoid deep barrel chains**: `index.js` → `sub/index.js` → `module.js` — tăng complexity vô nghĩa.

## 🔗 Liên kết chéo

- Xem thêm: `16_modules/03_modules/` — Tổng quan ESM module system.
- Xem thêm: `16_modules/03_modules/01_commonjs-vs-esm/` — So sánh CJS vs ESM.
- Xem thêm: `15_iterators-and-generators/` — generator có thể export từ module.
- Xem thêm: `17_memory-management/` — module singleton behavior và memory implications.
