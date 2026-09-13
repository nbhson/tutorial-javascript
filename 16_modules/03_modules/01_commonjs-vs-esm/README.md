# CommonJS vs ESM

## 🔑 Khái niệm

Hai hệ module chính của JavaScript:

- **CommonJS** — chuẩn Node.js, dùng `require()` / `module.exports`. Nạp **đồng bộ**: khi `require` chạy tới đâu, module đó được đánh giá ngay lúc đó, theo thứ tự. Thường dùng trong các file chạy trên server (Node).
- **ESM (ES Modules)** — chuẩn ECMAScript 6, dùng `import` / `export`. Nạp **tĩnh và bất đồng bộ**: toàn bộ `import` được parse trước khi chạy, engine tải song song rồi mới thực thi (hoisted). Cho phép tree-shaking.

Điểm mấu chốt để nhớ: **sync vs async**, **dynamic (require có thể gọi trong hàm / theo điều kiện) vs static (import ở top-level)**.

Trong repo này, `app.js` của thư mục này chạy demo ESM, import từ `./logger/index.js` (thư mục cùng cấp). Phần CommonJS chỉ là minh họa comment — kể cả khi file chạy dưới dạng CommonJS, thư mục `logger/` vẫn đủ điều kiện để tái sử dụng.

## ✅ Điểm mạnh

CommonJS:
- Nạp **đồng bộ đơn giản**, dễ hiểu; gọi được `require` trong điều kiện / vòng lặp.
- Đã thống trị Node.js suốt nhiều năm — hàng loạt thư viện cũ viết theo chuẩn này.

ESM:
- **Tĩnh -> tree-shaking**, bundle gọn hơn.
- **Chuẩn quốc tế**: chạy trên cả trình duyệt và Node.
- Nạp **bất đồng bộ**, hỗ trợ `import()` lazy.

## ⚠️ Lưu ý / Hạn chế

- Không dán code CommonJS (require) vào file ESM; tách biệt bằng `"type": "module"` hoặc đuôi `.mjs` / `.cjs`.
- `require` trong ESM báo lỗi `ERR_REQUIRE_ESM` (trừ khi dùng `createRequire`).
- `import` không gọi được động trong điều kiện — phải dùng `import()`.
- Node dùng trường `"type"` trong `package.json` mới phân biệt được; để mặc định thì `.js` là CommonJS.

## 💡 Khi nào dùng

- **Node project mới / thư viện phát hành npm** → ưu tiên ESM.
- **Code trình duyệt thuần** (không bundle) → ESM với `<script type="module">`.
- **Tooling / script cũ của Node** vẫn dùng CommonJS tốt, không bắt buộc đổi.
- Cần **tree-shaking** → ESM (ví dụ project Vite/Webpack).
- Cần **module-load theo yêu cầu** → dynamic `import()`.

## 🎯 Ví dụ minh họa

```js
// ── ESM (browser / Node với "type": "module") ──
import { log } from "./logger/index.js";
log("hi");

// ── CommonJS (Node thuần, không "type": "module") ──
const { log } = require("./logger");
log("hi");
```

Bảng so sánh nhanh:

|  | CommonJS (Node) | ESM (ES6) |
|---|---|---|
| Syntax | `require` / `module.exports` | `import` / `export` |
| Load | sync | async, static |
| Top-level? | Không bắt buộc | Bắt buộc (trừ `import()`) |
| File | `.js`/`.cjs` (Node) | `.mjs`/`"type": "module"` |
| Tree-shaking | Không | Có |

## 📚 Tham khảo / Bài tập

- Chạy `app.js` của thư mục này (ESM demo): mở `index.html` lên trình duyệt (nó dùng `<script type="module" src="app.js">`) — import từ `./logger/index.js` cùng cấp, sửa nội dung thông điệp rồi refresh để chạy lại.
- Tự làm (tiêu cực test): chạy file này bằng `node app.js` — vì repo không có `package.json` `"type": "module"`, Node hiểu `.js` là CommonJS nên sẽ báo lỗi cú pháp `import`. Đổi đuôi sang `.mjs` rồi chạy lại để thấy nó chạy ngon — hiểu luôn vai trò của `"type": "module"`/`.mjs`.
- Tự làm: viết file `.cjs` đối ứng dùng `require("./logger")` với cấu trúc `module.exports` để thấy rõ sự khác nhau sync/async giữa hai hệ.