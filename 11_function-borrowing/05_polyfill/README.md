# Polyfill cho `call` / `apply` / `bind` — [Level: Advanced]

## 🔑 Khái niệm cốt lõi

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

## 📐 Cấu trúc / Cú pháp

### myCall implementation

```js
Function.prototype.myCall = function (ctx, ...args) {
  ctx = ctx || globalThis;        // fallback global
  const key = Symbol("fn");       // unique key tránh clash
  ctx[key] = this;                // attach function as property
  const result = ctx[key](...args); // call with correct this
  delete ctx[key];                // cleanup
  return result;
};
```

### myApply implementation

```js
Function.prototype.myApply = function (ctx, argsArray) {
  ctx = ctx || globalThis;
  const key = Symbol("fn");
  ctx[key] = this;
  const result = argsArray 
    ? ctx[key](...argsArray)      // spread array
    : ctx[key]();                 // no args
  delete ctx[key];
  return result;
};
```

### myBind implementation

```js
Function.prototype.myBind = function (ctx, ...bindArgs) {
  const fn = this;
  return function (...rest) {
    return fn.apply(ctx, [...bindArgs, ...rest]);
  };
};
```

### Bảng đặc điểm polyfill

| Polyfill | Input | Output | Ghi chú |
|----------|-------|--------|---------|
| `myCall` | `ctx, ...args` | Kết quả fn | Giống `call` |
| `myApply` | `ctx, [args]` | Kết quả fn | Giống `apply` |
| `myBind` | `ctx, ...bindArgs` | Function mới | Giống `bind` |

## ✅ Điểm mạnh — Tại sao nên dùng

1. **Hiểu sâu bản chất `this` và `call`/`apply`/`bind`** — "mã nguồn" tự tay viết.
2. **Tạo code tương thích ngược** cho browser cũ (IE, Edge cũ) thiếu method hiện đại.
3. **Tự tin gỡ lỗi** khi behavior của built-in không như mong đợi.
4. **Phong cách lập trình áp dụng cho cả** `Array.prototype.includes`, `String.prototype.includes`...
5. **Learning tool** — cách tốt nhất để hiểu cách engine hoạt động.
6. **Custom behavior** — thêm logging, error handling vào polyfill.
7. **Avoid dependency** — không cần thư viện ngoài cho feature nhỏ.
8. **Interview preparation** — viết polyfill là câu hỏi phỏng vấn phổ biến.

## ⚠️ Bẫy thường gặp & Hạn chế

### Bẫy 1: Không được dùng chính `call`/`apply`/`bind` trong polyfill

```js
// ❌ Sai — circular dependency
Function.prototype.myCall = function (ctx, ...args) {
  return Function.prototype.call.call(this, ctx, ...args); // dùng call trong myCall!
};
// ✅ Đúng — dùng property attachment pattern
```

### Bẫy 2: Property tạm đụng tên có sẵn

```js
// ❌ Dùng key strings dễ clash
ctx.fn = this;
// ✅ Dùng Symbol để tránh xung đột
const key = Symbol("fn");
ctx[key] = this;
```

### Bẫy 3: Quên `delete` — rò rỉ property

```js
// ❌ Không xóa property tạm
ctx._fn = this;
ctx._fn(...args);
// ctx bây giờ có property _fn —làm bẩn (pollute) object
// ✅ Luôn delete sau khi dùng
delete ctx._fn;
```

### Bẫy 4: `bind` trong polyfill phải trả về hàm mới

```js
// ❌ Sai — return kết quả ngay
Function.prototype.myBind = function (ctx) {
  return this.call(ctx); // gọi ngay, không phải bind
};
// ✅ Đúng — return function mới
Function.prototype.myBind = function (ctx) {
  const fn = this;
  return function (...args) { return fn.call(ctx, ...args); };
};
```

### Bẫy 5: Polyfill chỉ nên thêm khi chưa tồn tại

```js
// ❌ Override built-in — nguy hiểm
Function.prototype.call = function (...) { ... };
// ✅ Chỉ thêm nếu chưa có
if (!Function.prototype.myCall) {
  Function.prototype.myCall = function (...) { ... };
}
```

### Bẫy 6: Arrow function không hoạt động với polyfill call/apply

```js
const arrow = () => console.log(this);
arrow.myCall({ x: 1 }); // không đổi được this — arrow không có this riêng
```

## 💡 Khi nào dùng — Tình huống thực tế

1. **Hỗ trợ trình duyệt cũ** (IE, phiên bản cũ) thiếu method hiện đại.
2. **Viết thư viện dùng chung** cần bảo đảm luôn có method (`Array.prototype.includes`).
3. **Học sâu** bằng cách tự tái hiện cơ chế lõi của ngôn ngữ.
4. **Debugging built-in** — hiểu cách polyfill hoạt động giúp debug native method.
5. **Custom behavior** — thêm logging, analytics vào method call.
6. **Education/training** — teaching tool cho junior developers.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: myCall cơ bản

```js
// Polyfill myCall
Function.prototype.myCall = function (ctx, ...args) {
  ctx = ctx || globalThis;
  const key = Symbol("fn");
  ctx[key] = this;
  const result = ctx[key](...args);
  delete ctx[key];
  return result;
};

const obj = { name: "Sơn" };
function hi() { console.log(this.name); }
hi.myCall(obj); // Sơn
```

### Ví dụ 2: myApply cơ bản

```js
Function.prototype.myApply = function (ctx, argsArray) {
  ctx = ctx || globalThis;
  const key = Symbol("fn");
  ctx[key] = this;
  const result = argsArray ? ctx[key](...argsArray) : ctx[key]();
  delete ctx[key];
  return result;
};

const user = { prefix: "Mr." };
function greet(title, name) {
  return `${this.prefix} ${title} ${name}`;
}
console.log(greet.myApply(user, ["Dr.", "Smith"])); // "Mr. Dr. Smith"
```

### Ví dụ 3: myBind cơ bản

```js
Function.prototype.myBind = function (ctx, ...bindArgs) {
  const fn = this;
  return function (...rest) {
    return fn.apply(ctx, [...bindArgs, ...rest]);
  };
};

const person = { name: "Alice" };
function introduce(greeting) {
  return `${greeting}, I'm ${this.name}`;
}
const bound = introduce.myBind(person, "Hi");
console.log(bound()); // "Hi, I'm Alice"
console.log(bound === introduce); // false — different function
```

### Ví dụ 4: Polyfill cho String.prototype.includes

```js
if (!String.prototype.includes) {
  String.prototype.includes = function (search, start = 0) {
    return this.indexOf(search, start) !== -1;
  };
}

console.log("hello".includes("ll")); // true
console.log("hello".includes("xyz")); // false
```

### Ví dụ 5: Polyfill cho Array.prototype.forEach

```js
if (!Array.prototype.forEach) {
  Array.prototype.forEach = function (callback, thisArg) {
    for (let i = 0; i < this.length; i++) {
      if (i in this) { // skip holes in sparse arrays
        callback.call(thisArg, this[i], i, this);
      }
    }
  };
}

const nums = [1, 2, 3];
nums.forEach(function (n) { console.log(n * 2); });
// 2, 4, 6
```

### Ví dụ 6: Polyfill cho Array.prototype.map

```js
if (!Array.prototype.map) {
  Array.prototype.map = function (callback, thisArg) {
    const result = [];
    for (let i = 0; i < this.length; i++) {
      if (i in this) {
        result[i] = callback.call(thisArg, this[i], i, this);
      }
    }
    return result;
  };
}

const words = ["hello", "world"];
const upper = words.map(w => w.toUpperCase());
console.log(upper); // ["HELLO", "WORLD"]
```

### Ví dụ 7: Complex — myBind với partial application

```js
Function.prototype.myBind = function (ctx, ...boundArgs) {
  const fn = this;
  return function (...callArgs) {
    // Ghép boundArgs + callArgs
    return fn.apply(ctx, [...boundArgs, ...callArgs]);
  };
};

function multiply(a, b, c) { return a * b * c; }
const double = multiply.myBind(null, 2);
console.log(double(3, 5)); // 30 (2 * 3 * 5) — boundArgs=[2], callArgs=[3,5]
```

## 🔬 So sánh với alternatives

| Cách | Độ tin cậy | Khó bảo trì | Use case |
|------|-----------|---------|----------|
| Native built-in | ✅ Cao | ❌ Không sửa được | Production code |
| Polyfill (custom) | ⚠️ Trung bình | ✅ Sửa được | Legacy support, education |
| Babel polyfill | ✅ Cao | ❌ External dependency | Build pipeline |
| Core.js / polyfill.io | ✅ Cao | ❌ External | Production |

## 📊 Performance & Best Practices

- **Polyfill chỉ dùng khi cần thiết** — native built-in luôn nhanh hơn và đã tối ưu.
- **Dùng `Symbol`** làm property key để tránh xung đột tên.
- **Luôn kiểm tra `if (!Proto.method)`** trước khi define — tránh override native.
- **Test polyfill với edge cases** — `null`, `undefined`, sparse array, hole.
- **Arrow function không polyfill được** — không có `this` riêng nên call/apply/bind không hoạt động.
- **Performance penalty**: polyfill chậm hơn native ~2-5x do thêm bước attach/detach property.

## 🔗 Liên kết chéo

- **Xem thêm:** `11_function-borrowing/01_bind` — bind native implementation
- **Xem thêm:** `11_function-borrowing/03_call` — call native implementation
- **Xem thêm:** `11_function-borrowing/04_apply` — apply native implementation
- **Xem thêm:** `11_function-borrowing/README` — overview function borrowing
- **Xem thêm:** `10_this-keyword/05_arrow-function` — arrow không polyfill được
- **Xem thêm:** `20_modern-javascript/02_destructuring-spread-rest/02_spread` — spread operator alternative
