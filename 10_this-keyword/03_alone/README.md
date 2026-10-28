# `this` đứng một mình (global scope) — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

Ở **global scope** — tức bên ngoài mọi function, tại vị trí top-level của script — `this` trỏ tới **object toàn cục** của môi trường chạy:

- **Browser:** `this === window` và `window === globalThis` — cùng một object.
- **Node.js:** ở top-level module, `this` thường bằng `module.exports`, nhưng `globalThis` luôn trỏ object toàn cục (dùng được ở cả browser và Node).

Khi gọi một hàm **trần** (không phải method, không bind, không `new`) trong **non-strict mode**, `this` bên trong hàm cũng rơi về global object — đây chính là **default binding** (quy tắc thấp nhất trong 4 quy tắc). Nếu thuộc mọi quy tắc khác không, mặc định quay về global.

Trong **strict mode** (`"use strict"`), default binding trả về `undefined` thay vì global — đây là sự cải tiến quan trọng để tránh bug.

`this` ở global scope là "con số 0" của mọi binding: khi không có rule nào áp dụng, giá trị mặc định là global/undefined.

## 📐 Cấu trúc / Cú pháp

### Bảng `this` theo môi trường

| Môi trường | `this` tại global scope | `this` trong hàm trần (non-strict) | `this` trong hàm trần (strict) |
|------------|-------------------------|-------------------------------------|--------------------------------|
| Browser | `window` | `window` | `undefined` |
| Node.js (module) | `module.exports` | `globalThis` | `undefined` |
| Node.js (script) | `global` | `global` | `undefined` |

### Các cách truy cập global object

| Cách | Browser | Node.js | Gợi ý |
|------|---------|---------|-------|
| `this` | `window` | `module.exports` | Không khuyên |
| `window` | ✅ | ❌ ReferenceError | Chỉ browser |
| `global` | ❌ ReferenceError | ✅ | Chỉ Node |
| `globalThis` | ✅ | ✅ | **Khuyên dùng** — cross-platform |

## ✅ Điểm mạnh — Tại sao nên dùng

1. **Hiểu hành vi mặc định** — là nền tảng suy luận mọi trường hợp `this` khác.
2. **Truy cập object toàn cục an toàn** — `globalThis` hoạt động đồng nhất trên mọi môi trường.
3. **Kiểm tra môi trường chạy** — `typeof window !== "undefined"` phân biệt browser/Node.
4. **Ghi log debugging** — `console.log(this)` ở global cho biết môi trường hiện tại.
5. **Nền tảng strict mode** — hiểu vì sao strict mode đổi default binding thành `undefined`.
6. **Avoid global pollution** — hiểu `this` giúp tránh vô tình gán vào `window`.

## ⚠️ Bẫy thường gặp & Hạn chế

### Bẫy 1: `this` khác nhau giữa browser và Node

```js
// Browser:
console.log(this === window);    // true
// Node.js:
console.log(this === module.exports); // true (ở module level)
```

### Bẫy 2: `window` không tồn tại trong Node.js

```js
console.log(window); // ReferenceError: window is not defined (Node.js)
console.log(globalThis); // ✅ hoạt động mọi nơi
```

### Bẫy 3: Strict mode đổi hoàn toàn hành vi

```js
function whoAmI() { return this; }
whoAmI();     // window (non-strict)
// Với "use strict":
whoAmI();     // undefined
```

### Bẫy 4: Gán biến global qua `this` — naming clash

```js
"use strict";
this.myVar = 1; // TypeError: Cannot set properties of undefined
// Không strict:
this.myVar = 1; // tạo global variable — nguy hiểm
```

### Bẫy 5: `this` trong top-level arrow function

```js
const arrow = () => console.log(this);
arrow(); // globalThis (kế thừa từ scope ngoài)
```

## 💡 Khi nào dùng — Tình huống thực tế

1. **Code đa môi trường** — dùng `globalThis` thay vì `window`/`global` để chạy được cả browser và Node.
2. **Debug environment** — `console.log(typeof this)` xác định đang chạy ở đâu.
3. **Kiểm tra strict mode** — `console.log(this)` trong hàm xem là `undefined` hay không.
4. **Plugin/Library pattern** — một số thư viện cũ dùng `this` để attach plugin vào global.
5. **Nền tảng hiểu `this`** — trước khi học binding, cần nắm default binding tại global scope.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: `this` tại global scope trong browser

```js
// Chạy trong browser
console.log(this === globalThis);  // true
console.log(this === window);      // true
console.log(window === globalThis); // true

// Thêm property vào global (non-strict)
this.myGlobal = 42;
console.log(myGlobal);             // 42 (biến toàn cục)
console.log(globalThis.myGlobal);  // 42
```

### Ví dụ 2: Khác biệt browser vs Node

```js
// Code chạy được cả hai môi trường
console.log("Env:", typeof globalThis !== "undefined" ? "globalThis available" : "missing");
console.log("Is browser:", typeof window !== "undefined");
console.log("Is Node:", typeof process !== "undefined" && process.versions?.node);
```

### Ví dụ 3: Default binding trong hàm trần

```js
function inspectThis() {
  return this;
}

// Non-strict
console.log(inspectThis() === window); // true (browser)
console.log(inspectThis() === globalThis); // true (mọi nơi)

// Strict
"use strict";
function inspectStrict() {
  return this;
}
console.log(inspectStrict()); // undefined
```

### Ví dụ 4: Dùng `globalThis` cross-platform

```js
// Cách an toàn nhất để truy cập global
const globalObj = globalThis;
console.log(globalObj === window); // true trong browser
console.log(typeof globalObj.fetch); // "function" — có fetch API
```

### Ví dụ 5: So sánh strict vs non-strict

```js
// Non-strict: this = window
function nonStrictFn() {
  return this;
}
console.log(nonStrictFn() === window); // true

// Strict: this = undefined
"use strict";
function strictFn() {
  return this;
}
console.log(strictFn()); // undefined
console.log(strictFn() === undefined); // true
```

### Ví dụ 6: Cảnh báo — global pollution

```js
// Non-strict: gán qua this = tạo global variable (nguy hiểm!)
this.secretKey = "abc123"; // tạo window.secretKey — dễ bị override
console.log(secretKey);    // "abc123" — biến toàn cục ẩn

// Fix: dùng strict mode hoặc declare var/let explicitly
"use strict";
// this.secretKey = "abc"; // TypeError — bảo vệ global scope
```

## 🔬 So sánh với alternatives

| Cách truy cập global | Browser | Node.js | Khuyến nghị |
|----------------------|---------|---------|-------------|
| `this` (global scope) | `window` | `module.exports` | ❌ Không đáng tin |
| `window` | ✅ | ❌ Error | ❌ Chỉ browser |
| `global` | ❌ Error | ✅ | ❌ Chỉ Node |
| `globalThis` | ✅ | ✅ | ✅ **Khuyên dùng** |

## 📊 Performance & Best Practices

- **Ưu tiên `globalThis`** — cross-platform, an toàn, chuẩn ES2020.
- **Luôn bật strict mode** — tránh `this` vô tình gán vào global, dễ debug hơn.
- **Không dùng `this` trong global scope để gán biến** — gây naming clash, khó maintain.
- **Kiểm tra `typeof window`** khi viết code chạy đa môi trường.
- **Dùng `globalThis` thay cho `window`** trong library đểtương thích cả Node.

## 🔗 Liên kết chéo

- **Xem thêm:** `10_this-keyword/02_in-function` — default binding chi tiết
- **Xem thêm:** `10_this-keyword/01_in-method` — implicit binding (đối lập)
- **Xem thêm:** `10_this-keyword/03_alone` — bài này đang đọc
- **Xem thêm:** `12_asynchronous-javascript/01_event-loop/00_js-runtime-deep-dive` — runtime environment
