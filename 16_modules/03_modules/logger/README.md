# Logger — Ví dụ Module ESM

## 🔑 Khái niệm

Thư mục này là một **module logger** viết hoàn toàn bằng ESM, minh họa cách tách một chức năng (log) thành nhiều tệp chỉ với `import` / `export`. Đây chính là "thư viện con" được `03_modules/app.js` sử dụng.

Các tệp và vai trò:

- `const.js` — export các **hằng số** loại log (`TYPE_LOG`, `TYPE_WARN`, `TYPE_ERROR`) — các "hằng" thường để riêng để dùng chung.
- `function.js` — export các **hàm tiện ích** (`func_1`, `func_2`, `func_3`) — ví dụ nhóm hàm dùng nhiều nơi.
- `logger.js` — export **default một hàm log**: nhận `log` và loại `type` (mặc định `log`), gọi `console[type](log)`.
- `index.js` — **"barrel file"**: chỉ tái xuất (`export { default } from`) từ `logger.js` để các nơi khác import từ một điểm duy nhất.

Cách hoạt động: `logger.js` import `TYPE_LOG` từ `const.js` để làm mặc định; `index.js` nhận default-export từ `logger.js` rồi "mở lại" cho bên ngoài. Vì ESM mang tính tĩnh, bạn chỉ cần nhìn các dòng `import/export` là hiểu toàn bộ đồ thị phụ thuộc.

## ✅ Điểm mạnh

- **Tách biệt rõ ràng**: hằng số, hàm tiện ích, core logic và cổng xuất nằm riêng — dễ bảo trì.
- **Barrel file** giúp bên ngoài chỉ import một đường dẫn duy nhất thay vì nhớ từng file.
- **Default + named export song song** minh họa đầy đủ cú pháp ESM.
- **Nhiều mức log** (`log` / `warn` / `error`) chỉ bằng một tham số mặc định — code linh hoạt.
- **Có thể tái sử dụng** như mẫu chuẩn cho mọi module tự viết.

## ⚠️ Lưu ý / Hạn chế

- `index.js` tái xuất **default** nên khi import phải đặt tên tùy ý (`import newLogger from ...`) — dễ lầm nếu nghĩ nó là named export.
- File này là ESM thuần: **không dùng được bằng `require`** nếu môi trường chạy là CommonJS.
- Trong `app.js`, dòng `import * as constant from "./logger/const.js"` lấy namespace — gọi đúng qua `constant.TYPE_ERROR`, đừng gọi `constant.???` với tên khác.
- Console `console[type]` với type không hợp lệ sẽ **lỗi runtime** (ví dụ type trống, sai tên hàm).

## 💡 Khi nào dùng

- Làm **khuôn mẫu tổ chức module nhỏ** trong ứng dụng của bạn.
- Xây dựng **thư viện log / debug** tái sử dụng trong nhiều file.
- Khi cần **tách hằng số cấu hình** (như mức log) khỏi logic chính.
- Làm quen với **barrel file / re-export** trước khi gặp mô hình này ở các thư viện lớn.

## 🎯 Ví dụ minh họa

```js
// logger.js
import { TYPE_LOG } from './const.js';
export default function loggerFunction(log, type = TYPE_LOG) {
  console[type](log);
}

// app.js
import newLogger from "./logger/index.js";        // default import
import { func_1 } from "./logger/function.js";      // named import
import * as constant from "./logger/const.js";      // namespace import
newLogger("Sơn Nguyên", constant.TYPE_WARN);        // console.warn
func_1("New message");                              // console.warn
```

## 📚 Tham khảo / Bài tập

- Chạy demo bằng cách mở `../index.html` (trong `03_modules/`) lên trình duyệt — nó load `app.js` (ESM) và import tương đối vào `logger/`; quan sát Console: 2 dòng từ `console.error` (qua `TYPE_ERROR`) và `console.warn` (qua `func_1`).
- Tự làm: gọi `newLogger("log thường")` *không* truyền type — nó nên in qua `console.log` nhờ mặc định `TYPE_LOG`.
- Tự làm: mở `index.js` và đổi `export { default } from './logger.js'` thành `export { default as nhap_thu_x }` để thấy cách đặt alias khi tái xuất; sửa lại gọi tương ứng trong `app.js`.
- Tự làm: truyền type không hợp lệ (`newLogger("x", "nonexistent")`) để thấy lỗi `TypeError` khi `console[type]` không tồn tại — từ đó hiểu lý do nên validate type.