# Polyfill cho `call` / `apply` / `bind`

## 🔑 Khái niệm

**Polyfill** là đoạn code bạn tự viết để **bổ sung tính năng** mà môi trường cũ (trình duyệt cũ) chưa hỗ trợ — bằng cách định nghĩa lại trên prototype. Thay vì chờ trình duyệt nâng cấp, ta tự "vá" một cách tương thích, hoạt động như bản gốc.

Để hiểu cơ chế `call`/`apply`/`bind`, kỹ thuật phổ biến là viết lại chúng; kết quả chạy tương đương. Ý tưởng cốt lõi của `myCall`/`myApply`/`myBind`:

- Gắn hàm vào một **property tạm** của `context` (obj) — nhờ vậy gọi được với đúng `this`.
- Gọi property đó với các đối số, rồi **xóa property tạm** đi để không làm bẩn object.
- Không có `context` → gán bằng `globalThis` (hoặc undefined nếu strict).

Các bước của một `myCall(ctx, ...args)`:

1. Nếu `ctx` rỗng, dùng `globalThis`.
2. Đặt `ctx.fn = this` (hàm gốc).
3. `const result = ctx.fn(...args)` — `this` của hàm = `ctx`.
4. `delete ctx.fn`, trả về `result`.

## ✅ Điểm mạnh

- Hiểu sâu bản chất `this` và `call/apply/bind` — "mã nguồn" tự tay viết.
- Tạo code tương thích ngược cho browser cũ.
- Tự tin gỡ lỗi khi behavior của built-in không như mong đợi.
- Phong cách lập trình áp dụng cho cả `Array.prototype.includes`, `String.prototype.includes`...

## ⚠️ Lưu ý / Hạn chế

- Không được dùng chính `call/apply/bind` trong lúc viết polyfill cho chúng.
- Property tạm có thể đụng tên property có sẵn của object — nên chọn tên hiếm (`fn`, `__fn__`...).
- Phải `delete` sau khi gọi để tránh rò rỉ thuộc tính vào object.
- `bind` trong polyfill phải trả về hàm mới — quên sẽ sai hoàn toàn.
- Polyfill chỉ nên thêm **khi chưa tồn tại**: `if (!String.prototype.includes) { ... }`.

## 💡 Khi nào dùng

- Hỗ trợ trình duyệt cũ (IE, phiên bản cũ) thiếu method hiện đại.
- Viết thư viện dùng chung cần bảo đảm luôn có method.
- Học sâu bằng cách tự tái hiện cơ chế lõi của ngôn ngữ.

## 🎯 Ví dụ minh họa

```js
// myCall — mô phỏng call()
Function.prototype.myCall = function (ctx, ...args) {
  ctx = ctx || globalThis;      // rỗng → global
  ctx._fn = this;               // gắn hàm vào property tạm
  const result = ctx._fn(...args);
  delete ctx._fn;               // dọn dẹp
  return result;
};

const obj = { name: "Sơn" };
function hi() { console.log(this.name); }
hi.myCall(obj); // Sơn

// myBind — trả về hàm mới
Function.prototype.myBind = function (ctx, ...bindArgs) {
  const fn = this;
  return function (...rest) {
    return fn.apply(ctx, [...bindArgs, ...rest]);
  };
};
const bound = hi.myBind({ name: "Trinh" });
bound(); // Trinh
```

## 📚 Tham khảo / Bài tập

- Chạy `05_polyfill/app.js` (qua `index.html` hoặc `node app.js`): file demo polyfill cho `String.prototype.includes` — chỉ định nghĩa khi trình duyệt chưa có.
- Tự thử: viết tiếp `myApply` (nhận mảng đối số) và `myBind` rồi so sánh output với `call`/`apply`/`bind` gốc cho cùng một hàm.