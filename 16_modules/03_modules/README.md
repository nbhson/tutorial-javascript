# Module — ESM

## 🔑 Khái niệm

Thư mục này tập trung vào **ES Modules (ESM)** — hệ module chuẩn ECMAScript 6 dùng `import` / `export`. Khác với CommonJS của Node, ESM:

- **Tĩnh (static)**: mọi `import` / `export` được phân tích ngay khi parse file (phải ở top-level), nhờ đó tooling biết trước đồ thị phụ thuộc để **tree-shake** và nạp song song.
- **Bất đồng bộ**: trình duyệt / Node tải module theo kiểu async — module con tải xong trong khi parent vẫn đang xử lý.
- **Có hoisted**: tên export "nhô lên" đầu scope, thứ tự khai báo không quan trọng.
- **Singleton**: mỗi module được "đánh giá" một lần duy nhất, các bên import đều thấy cùng một instance.

Cấu trúc thư mục:

- `01_commonjs-vs-esm/` — bảng so sánh CommonJS vs ESM kèm demo.
- `logger/` — module logger thuần ESM gồm `const.js`, `function.js`, `logger.js`, `index.js`.

## ✅ Điểm mạnh

- **Tree-shaking được**: bởi cấu trúc tĩnh, bundler loại bỏ export không dùng — bundle nhỏ hơn.
- **Chạy natively** trên cả trình duyệt hiện đại và Node (với `"type": "module"`).
- **Nạp bất đồng bộ và hoisted** giúp khởi động nhanh hơn so với chuỗi `require` đồng bộ.
- **Lazy-load dễ dàng** bằng `import()` khi cần.
- **Cú pháp gọn rõ**: `import {x} from ...` / `export default` tách bạch.

## ⚠️ Lưu ý / Hạn chế

- Phải khai báo môi trường ESM: `package.json` với `"type": "module"`, hoặc file đuôi `.mjs`, thẻ `<script type="module">`.
- `import` bắt buộc ở top-level — không nạp theo điều kiện nếu không dùng `import()`.
- Không dùng `require` trong file ESM (trừ khi dùng `createRequire`).
- Trong Node, file `.js` không có `"type": "module"` bị hiểu là CommonJS -> `import`/`export` lỗi cú pháp.

## 💡 Khi nào dùng

- Project JavaScript mới trên **Node.js** — ESM là chuẩn được khuyến khích.
- Chạy code **trực tiếp trong trình duyệt** (không bundle) — thẻ `<script type="module" src="app.js">`.
- Xây dựng **thư viện / package** phát hành trên npm — sử dụng ESM làm chuẩn nguồn.
- Cần **tree-shaking / bundle gọn** khi build bằng Vite, Webpack, Rollup.
- Muốn **lazy-load** theo yêu cầu — kết hợp dynamic `import()`.

## 🎯 Ví dụ minh họa

```js
// logger/logger.js
import { TYPE_LOG } from './const.js';
export default function loggerFunction(log, type = TYPE_LOG) {
  console[type](log);
}

// app.js
import { func_1 } from "./logger/function.js";     // named import
import * as constant from "./logger/const.js";      // namespace import
import newLogger from "./logger/index.js";          // default import

newLogger("Sơn Nguyên", constant.TYPE_ERROR);       // console.error
func_1("New message");                              // console.warn
```

## 📚 Tham khảo / Bài tập

- Chạy demo bằng cách mở `index.html` trong thư mục này (nó load `app.js` qua `<script type="module">`); mở Console DevTools để thấy 2 dòng từ `console.error` và `console.warn`. (Repo không có `package.json` `"type": "module"` nên chạy qua `.js` thuần bằng `node` sẽ báo lỗi cú pháp import — đây cũng là điểm đáng ghi nhớ ở phần `01_commonjs-vs-esm`.)
- Mở `logger/index.js`: nó chỉ tái xuất (`export { default }`) — đây là "barrel file". Hãy thử set named exports lại từ `logger.js` để thấy khác biệt giữa default và named.
- Mở `01_commonjs-vs-esm` để đối chiếu cách nạp CommonJS (`require`) tương ứng.
- Tự làm: thêm một `logger/debug.js` với `export function debug(msg)`, rồi import named `{ debug }` từ `app.js`.