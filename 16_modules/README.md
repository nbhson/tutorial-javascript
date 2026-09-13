# Module trong JavaScript

## 🔑 Khái niệm

**Module** là cách chia ứng dụng thành nhiều tệp nhỏ, mỗi tệp phạm vi riêng (không làm bẩn global scope), chỉ *export* những thứ muốn chia sẻ và *import* đúng những gì cần dùng. JavaScript có hai hệ module phổ biến:

- **CommonJS**: dùng `require()` / `module.exports`, là chuẩn của **Node.js**, nạp đồng bộ (synchronous). Tệp được "đánh giá" ngay khi `require` chạy đến.
- **ESM (ES Modules)**: dùng `import` / `export`, là chuẩn của ECMAScript 6, nạp **bất đồng bộ** và **tĩnh** (các `import` được phân tích trước khi code chạy). Nhờ tĩnh mà có **tree-shaking** — bundle tool loại bỏ code không dùng.
- **Dynamic `import()`**: dạng nạp theo yêu cầu (lazy loading), trả về Promise — dùng khi cần tải module lúc runtime.

Hai hệ này **không tương thích trực tiếp**: file `package.json` có trường `"type": "module"` (hoặc đuôi `.mjs`) để Node hiểu là ESM; nếu dùng `require` trong ESM sẽ bị lỗi `ERR_REQUIRE_ESM` (có thể dùng `createRequire`).

Trong repo này:

- `03_modules/app.js` — ví dụ ESM: `import` lần lượt từ `logger/function.js`, `logger/const.js`, `logger/index.js`.
- `03_modules/01_commonjs-vs-esm` — bảng so sánh kèm demo.
- `03_modules/logger/` — module logger dạng ESM gồm 4 file nhỏ.

## ✅ Điểm mạnh

- **Tổ chức code rõ ràng**: tách được đúng nơi chức năng, dễ bảo trì và tái sử dụng.
- **Tránh xung đột tên global**: mỗi file có scope riêng.
- **Nạp có kiểm soát**: ESM tĩnh + tree-shaking giúp bundle gọn hơn; `import()` lazy giảm dung lượng tải ban đầu.
- **Chuẩn hóa cho cả browser và Node**: ESM chạy gốc trên trình duyệt hiện đại, không cần bundler cho các trường hợp đơn giản.
- **Phụ thuộc rõ ràng**: nhìn lướt phần `import` là biết module cần gì.

## ⚠️ Lưu ý / Hạn chế

- **Không trộn lẫn trực tiếp** CommonJS với ESM: khác cơ chế nạp (sync vs async/static), dễ gặp lỗi khi chuyển đổi.
- ESM buộc khai báo `import` ở **top-level** (tĩnh); muốn nạp có điều kiện phải dùng `import()`.
- Không khai báo `"type": "module"` (hay đuôi `.mjs`) thì Node mặc định hiểu file là CommonJS -> `import`/`export` bị lỗi cú pháp.
- `export default` và named export cách dùng khác nhau; dễ nhầm khi tái xuất (`export { default } from ...` — đúng ví dụ trong `logger/index.js`).

## 💡 Khi nào dùng

- Chạy JavaScript **trên Node.js** và muốn chia file — chọn ESM (hiện đại) hoặc CommonJS theo chuẩn project.
- Chạy code **trực tiếp trên trình duyệt** — dùng ESM, thêm `type="module"` vào thẻ `<script>`.
- Thư viện, tiện ích **dùng chung nhiều nơi** trong project — đóng gói thành module rồi export.
- Cần **lazy-load** nặng (chunk lớn, màn hình hiếm vào) — dùng dynamic `import()`.
- Build với **tree-shaking** (Vite/Webpack) — chỉ giữ function/component thực sự được dùng.

## 🎯 Ví dụ minh họa

```js
// logger/const.js
export const TYPE_LOG = 'log';
export const TYPE_ERROR = 'error';

// logger/logger.js
import { TYPE_LOG } from './const.js';
export default function loggerFunction(log, type = TYPE_LOG) {
  console[type](log);
}

// app.js (ESM) — chạy trong môi trường "type": "module"
import newLogger, * as constant from './logger/index.js';
newLogger("Sơn Nguyên", constant.TYPE_ERROR); // console.error("Sơn Nguyên")
```

## 📚 Tham khảo / Bài tập

- Chạy demo ESM bằng cách mở `03_modules/index.html` trong trình duyệt (file này dùng `<script type="module" src="app.js">`); mở Console để quan sát output — `newLogger("Sơn Nguyên", TYPE_ERROR)` in qua `console.error`, `func_1` in qua `console.warn`. Nếu muốn chạy bằng Node, phải đặt tên `.mjs` hoặc bổ sung `"type": "module"` trong `package.json`.
- Trong `03_modules/logger/index.js` có 2 dòng tái xuất (`export { default } from`); hãy bỏ comment cả hai cách dùng trong `app.js` để thấy tên import khác nhau (`mặc định` vs `newLogger`).
- So sánh với CommonJS: viết thêm đoạn `const { log } = require('./logger')` trong `01_commonjs-vs-esm` để thấy lỗi nếu file bị ép chạy như ESM — từ đó nắm rõ sự khác biệt sync/async giữa hai hệ.
- Tự làm: chuyển một phần logic nhỏ trong project thành module riêng, thử thêm dynamic `import()` để nạp có điều kiện một module bất kỳ.