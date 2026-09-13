# `this` trong hàm thường (không phải method của object)

## 🔑 Khái niệm

Khi một hàm **không được gọi như method của object** — tức gọi trần `fn()` hoặc gọi qua biến tham chiếu tách ra từ object — JavaScript áp dụng **default binding**:

- **Non-strict mode:** `this` = `window` (browser) / `globalThis` (Node).
- **Strict mode (`"use strict"`):** `this` = `undefined`.

Trường hợp "mất context" kinh điển: gán `const fn = obj.hi;` rồi gọi `fn()`. Lúc đó hàm vẫn là hàm cũ nhưng **không còn ai đứng trước dấu chấm** nên `this` không còn là `obj` nữa.

## ✅ Điểm mạnh

- Giúp hiểu rõ cốt lõi của cơ chế `this` (call-site), nền tảng cho mọi quy tắc binding khác.
- Chủ động truy cập object toàn cục qua `this` khi cần (non-strict).
- Nhận diện được lỗi "detached method" ngay khi nhìn vào code.
- Kết hợp strict mode để bắt lỗi sớm thay vì âm thầm trỏ vào `window`.

## ⚠️ Lưu ý / Hạn chế

- `this` cũng có thể là một **biến tham chiếu** — do đó method tách ra khỏi object sẽ trỏ sai object.
- Trong non-strict mode không có lỗi nhưng dễ gây kết quả sai (chuỗi `undefined`), khó debug.
- Strict mode giúp bắt lỗi nhưng bắt buộc bạn phải để ý từ đầu.
- Default binding chỉ xảy ra khi hàm gọi trần, không áp dụng cho arrow function.

## 💡 Khi nào dùng

- Gọi hàm tiện ích (helper) độc lập, không cần `this`.
- Debug các lỗi `this` mất context trong code thật.
- Hiểu vì sao phải dùng `bind`/arrow function khi truyền method làm callback.

## 🎯 Ví dụ minh họa

```js
"use strict";
function fn() {
  console.log(this); // → undefined (strict)
}
fn(); // default binding + strict → undefined

function nonStrict() {
  console.log(this === globalThis); // → true (nếu không strict)
}
nonStrict();

// mất context khi tách method
const obj = { name: "A", hi() { console.log("traves", this.name); } };
obj.hi();       // this = obj → A
const fn2 = obj.hi;
fn2();          // this = window/undefined → undefined hoặc lỗi
```

## 📚 Tham khảo / Bài tập

- Chạy `02_in-function/app.js` (qua `index.html` hoặc `node app.js`): so sánh output khi gọi `obj.hi()` so với `const fn = obj.hi; fn()`.
- Tự thử: chạy lại file sau khi thêm `"use strict";` ở đầu — so sánh xem kết quả đổi thế nào.