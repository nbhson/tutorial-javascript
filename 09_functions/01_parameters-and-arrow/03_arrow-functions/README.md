# Arrow Functions (Hàm mũi tên)

## 🔑 Khái niệm

Arrow function là cú pháp viết hàm **ngắn gọn** với ký hiệu `=>`, ra đời từ ES6. Có ba cách viết function cho cùng một việc (file `app.js`):

```js
// 1. Function declaration
function myFunc1(param) { console.log(param); }

// 2. Function expression
const myFunc2 = function (param) { console.log(param); };

// 3. Arrow function
const myFunc3 = (param) => { console.log(param); };
```

Các quy tắc viết ngắn của arrow:

| Trường hợp | Cú pháp | Ghi chú |
|---|---|---|
| Có thân `{}` | `(a, b) => { return a + b; }` | cần `return` như thường |
| Thân một biểu thức | `(a, b) => a + b` | **tự trả về** (implicit return) |
| Trả về object | `(a, b) => ({ a, b })` | phải bọc `()` vì `{}` bị hiểu là thân hàm |
| Một tham số | `log => console.log(log)` | có thể bỏ ngoặc |
| Không tham số | `() => 42` | bắt buộc có `()` |

**Khu vực nguy hiểm** (được demo ở cuối `app.js`):

- Arrow **không có `this` riêng** — `this` trong arrow chính là `this` ở nơi hàm được *định nghĩa* (lexical this). Nên với object method dùng arrow, `this` sẽ không phải object đó.
- Arrow **không thể dùng làm constructor**: `new funcConstruct(1, 2)` với arrow → lỗi (file mẫu chạy ra lỗi).
- Arrow **không có `arguments`** riêng (xem `05_arguments-object`).

## ✅ Điểm mạnh

- **Ngắn gọn** — đặc biệt với callback `value => value * 2`.
- **Implicit return** — viết tỉnh bất kỳ biểu thức nào là hàm trả về luôn.
- **`this` tĩnh (lexical)** — rất tiện khi làm việc với event handler, timer, promise: không lo bị đổi `this`.
- Bọc `({...})` để trả object gọn và đẹp, phù hợp kiểu "functional".
- Không ghi từ khóa `function` → code sạch hơn.
- Là chuẩn viết hiện đại trong phần lớn dự án JS/React.

## ⚠️ Lưu ý / Hạn chế

- Không có `this`, `arguments`, `new.target` riêng — không phù hợp làm method của object, constructor.
- Implicit return đôi khi gây nhầm: muốn trả object mà quên `()` → lỗi `SyntaxError`.
- Không **hoisted** như function declaration — phải khai báo trước khi dùng.
- Đôi khi ít rõ ràng hơn hàm thường vì quá gọn (đặt tên không tốt khó đọc).
- Không dùng làm `function*` (generator) được.

## 💡 Khi nào dùng

- Callback ngắn: `arr.map(x => x * 2)`, `arr.filter(c => c.price > 100)`.
- Truyền hàm cho `setTimeout`, event listener, promise chain — giữ `this` từ ngoài.
- Hàm tiện ích không cần thay đổi `this`.
- Viết hàm một biểu thức để tăng tính biểu cảm.

## 🎯 Ví dụ minh họa

```js
// Ngắn gọn với implicit return
const func2 = (a, b) => a + b;        // tự return
const func3 = (a, b) => ({ a, b });   // return object cần ()

// Arrow cho callback
const double = [1, 2, 3].map(n => n * 2);
console.log(double); // [2, 4, 6]

// this trong arrow: giữ this của nơi định nghĩa
const course = {
  name: "JS Basic",
  getName() {
    setTimeout(() => console.log(this.name), 0); // JS Basic — không mất this
  },
};
```

## 📚 Tham khảo / Bài tập

- Mở `index.html` (Console) hoặc chạy `node app.js`.
- Bỏ comment dòng `func3(2, 2)` `logger('log message')` `course.getName()` và chạy để quan sát.
- Tự thử: đổi `getName` thành arrow `getName: () => { ... }` để thấy `this` thành `undefined` (trong strict mode) hoặc `window`.
- Tự thử: thử `new funcContruct(1, 2)` khi đã sửa thành function thường — constructor hoạt động bình thường, chứng minh arrow không dùng được.