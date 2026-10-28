# Toán tử một ngôi (Unary Operators) — Thực hành chi tiết — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

**Toán tử một ngôi** (unary operator) là toán tử chỉ cần **một toán hạng duy nhất** để tạo ra giá trị. Khác với binary operator (`+`, `-`, `===`) cần 2 operand, unary operator chỉ hoạt động trên một giá trị.

Nhóm này đặc biệt quan trọng vì chứa những phép **"kiểm tra và biến đổi"** sử dụng hằng ngày trong JavaScript:

| Toán tử | Công dụng | Ví dụ | Kết quả |
|---|---|---|---|
| `typeof` | Trả về tên kiểu dữ liệu | `typeof 123` | `"number"` |
| `void` | Trả về `undefined` | `void 0` | `undefined` |
| `delete` | Xóa thuộc tính của object | `delete o.a` | `true`/`false` |
| `+` (unary) | Ép sang Number | `+"42"` | `42` |
| `-` (unary) | Đổi dấu / ép sang Number | `-"42"` | `-42` |
| `!` | Phủ định boolean | `!0` | `true` |
| `!!` | Ép thành boolean | `!!1` | `true` |
| `~` | Đảo bit (bitwise NOT) | `~5` | `-6` |
| `++` / `--` | Tăng/giảm 1 | `++n` / `n--` | n+1 / n-1 |

**Điểm thú vị** trong `app.js` (file mẫu của thư mục):

```js
console.log(typeof 123, typeof null); // "number" "object"  ← typeof null là "object" (lỗi lịch sử của JS!)
console.log(void 0, void (1 + 1));    // undefined undefined
let o = { a: 1, b: 2 };
delete o.a;
console.log(o);                       // { b: 2 }
console.log(+"42", -"42", !0, !!1);   // 42 -42 true true
```

**Lưu ý quan trọng**: `typeof null === "object"` là một **lỗi lịch sử** (bug từ phiên bản đầu của JavaScript) — null KHÔNG PHẢI là object. Đây là một trong những câu hỏi phỏng vấn kinh điển.

## 📐 Cấu trúc / Cú pháp

### `typeof` — Kiểm tra kiểu
```js
typeof 42           // "number"
typeof "hello"      // "string"
typeof true         // "boolean"
typeof undefined    // "undefined"
typeof null         // "object" ← BUG LỊCH SỬ!
typeof {}           // "object"
typeof []           // "object" ← array cũng là object!
typeof (() => {})   // "function"
typeof Symbol()     // "symbol"
typeof BigInt(1)    // "bigint"
```

### `void` — Ép thành undefined
```js
void 0                 // undefined
void (1 + 1)           // undefined
void console.log("hi") // undefined (log "hi", return undefined)
void function() {}     // undefined
```
`void` hữu ích khi bạn muốn **bỏ qua giá trị trả về** của một expression — đảm bảo kết quả là `undefined`.

### `delete` — Xóa property
```js
const obj = { a: 1, b: 2 };
delete obj.a;           // true — xóa thành công
console.log(obj);       // { b: 2 }

delete obj.b;           // true
delete obj.c;           // true — không lỗi dù key không tồn tại
console.log('c' in obj); // false

// ❌ Không xóa được biến khai báo bằng let/const/var
let x = 1;
delete x;               // false (non-strict) / TypeError (strict mode)
```

### Unary `+` và `-` — Ép kiểu
```js
+"42"       // 42  — string → number
-"42"       // -42 — string → number, đổi dấu
+true       // 1   — boolean → number
+false      // 0
+null       // 0
+undefined  // NaN
+""         // 0
+[]         // 0
+[1, 2]     // NaN
```

### `!` và `!!` — Phép phủ định
```js
!0       // true   — 0 là falsy → !0 = true
!5       // false  — 5 là truthy → !5 = false
!"hello" // false
!""      // true

!!0      // false  — ép thành boolean
!!5      // true
!!""     // false
!!"hi"   // true
```
`!!` là cách **ép bất kỳ giá trị nào thành boolean** — rất tiện khi cần rõ ràng `true`/`false`.

### `~` — Bitwise NOT (xem thêm `02_bitwise/`)
```js
~5    // -6  (đảo tất cả bit của 5)
~-6   // 5
~0    // -1
~-1   // 0
```
`~x = -(x + 1)` — công thức nhớ nhanh.

## ✅ Điểm mạnh

1. **`typeof` kiểm tra kiểu an toàn** — không cần biết biến có tồn tại hay không, không throw ReferenceError.
   ```js
   typeof undeclaredVar; // "undefined" — KHÔNG lỗi!
   undeclaredVar;        // ReferenceError
   ```

2. **`+`/"-" ép sang Number cực gọn** — thay thế `Number()` với cú pháp ngắn hơn.
   ```js
   +"3.14"    // 3.14
   +"0xFF"    // 255
   +"\t\n42"  // 42  — whitespace ignored
   ```

3. **`! và !!` ép bất cứ giá trị nào thành boolean** — rõ ràng intent, không ambiguity.
   ```js
   const isActive = !!(user && user.status === "active");
   // Rõ ràng hơn: const isActive = Boolean(user && user.status === "active");
   ```

4. **`void 0` — cách viết an toàn lấy `undefined`** — không sợ bị gán đè (trong code non-strict, `undefined` có thể bị override).
   ```js
   // Thay vì:
   let x = undefined;
   // Dùng:
   let y = void 0; // luôn là undefined, bất kể biến toàn cục
   ```

5. **`delete` xóa thuộc tính object** — hữu ích khi dọn dữ liệu trước khi gửi API.
   ```js
   const payload = { id: 1, password: "secret", name: "Sơn" };
   delete payload.password; // dọn sebelum send
   fetch("/api/update", { body: JSON.stringify(payload) });
   ```

6. **Viết tay dễ, không cần thư viện** — tất cả đều là built-in operators.
7. **`typeof` hoạt động với mọi giá trị** — kể cả `null`, `undefined`, symbol, bigint.
8. **`void` guarantee undefined** — tuyệt vời cho `href="javascript:void(0)"` trong HTML.

## ⚠️ Bẫy thường gặp & Hạn chế

1. **`typeof null` trả về `"object"`** — một "bug lịch sử" của JavaScript, đừng dùng nó để kiểm tra null.
   ```js
   typeof null === "object"; // true ← sai! null không phải object
   null === null;            // true ← dùng cái này để check null
   ```

2. **`typeof [] === "object"`** — mảng cũng là object trong JS.
   ```js
   typeof [];        // "object"
   Array.isArray([]); // true ← dùng cái này để check array
   ```

3. **`delete` chỉ xóa thuộc tính của object** — không dùng để xóa biến, và không ảnh hưởng đến biến local.
   ```js
   const obj = { a: 1 };
   delete obj.a; // true

   let x = 1;
   delete x;     // false (non-strict) / TypeError (strict)
   ```

4. **`+""` → `0`, `+[]` → `0`, `+null` → `0`** — ép với giá trị "rỗng" dễ ra số 0 không ngờ.
   ```js
   console.log(+"");     // 0
   console.log(+[]);     // 0
   console.log(+null);   // 0
   console.log(+undefined); // NaN ← khác biệt!
   ```

5. **`++`/`--` có sự khác nhau prefix (trả giá trị mới) và postfix (trả giá trị cũ)** — xem chi tiết `01_operators/6_toan-tu-prefix-postfix.js`.
   ```js
   let a = 5;
   let b = a++; // b = 5 (cũ), a = 6
   let c = ++a; // a = 7, c = 7 (mới)
   ```

6. **`~` là đảo bit, đừng nhầm với phủ định logic `!`** — `~5 = -6`, `!5 = false`.
   ```js
   console.log(~5);   // -6  ← bitwise NOT
   console.log(!5);   // false ← logical NOT
   ```

7. **Unary `+` với object/array phức tạp** — có thể ra kết quả không mong đợi.
   ```js
   +{}       // NaN
   +["5"]    // 5
   +["5", "6"] // NaN
   ```

## 💡 Khi nào dùng

1. **Kiểm tra kiểu giá trị trước khi xử lý**: `typeof value === "number"` — guard clause phổ biến.
2. **Ép chuỗi kết quả API/form về số**: `+"123"` rồi cộng trừ — nhanh hơn `Number()`.
3. **Bỏ qua giá trị của một thao tác** và chỉ cần `undefined` — vd: `void someFunc()`.
4. **Xóa trường không cần thiết khỏi object** trước khi gửi API — dọn payload.
5. **Kiểm tra nhanh truthy bằng `!!`** trong điều kiện hoặc gán boolean.
6. **Kiểm tra undefined an toàn**: `typeof x === "undefined"`.
7. **Guaranteed undefined**: `void 0` trong callback, event handler (`href="javascript:void(0)"`).
8. **Debug type**: `console.log(typeof input)` để nhanh chóng xác định kiểu dữ liệu.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: typeof — kiểm tra kiểu (file `app.js`)
```js
// Nội dung app.js trong thư mục
console.log(typeof 123, typeof null); // "number" "object"
// ⚠️ typeof null === "object" là bug lịch sử! Dùng null === null để check null.

console.log(typeof "hello"); // "string"
console.log(typeof true);    // "boolean"
console.log(typeof undefined); // "undefined"
console.log(typeof []);      // "object" ← array là object!
console.log(typeof {});      // "object"
console.log(typeof (() => {})); // "function"
console.log(typeof Symbol());   // "symbol"
console.log(typeof BigInt(1));  // "bigint"
```

### Ví dụ 2: void — ép thành undefined
```js
// Nội dung app.js trong thư mục
console.log(void 0, void (1 + 1)); // undefined undefined

// Ứng dụng: đảm bảo undefined tuyệt đối
let undefined = "not really undefined"; // override biến toàn cục (non-strict)
console.log(undefined); // "not really undefined"
console.log(void 0);    // undefined ← vẫn đúng!
```

### Ví dụ 3: delete — xóa property
```js
// Nội dung app.js trong thư mục
let o = { a: 1, b: 2 };
delete o.a;
console.log(o);                       // { b: 2 }
console.log("a" in o);               // false

// Xóa property không tồn tại — không lỗi
delete o.c;                          // true (không có lỗi)
console.log(o);                       // { b: 2 }

// ❌ Không xóa được biến
let x = 1;
delete x;                            // false (non-strict)
console.log(x);                      // 1 — vẫn tồn tại
```

### Ví dụ 4: Unary + và - — ép kiểu
```js
// Nội dung app.js trong thư mục
console.log(+"42", -"42", !0, !!1); // 42 -42 true true

// Ép nhiều kiểu khác nhau
console.log(+"");     // 0
console.log(+null);   // 0
console.log(+true);   // 1
console.log(+false);  // 0
console.log(+undefined); // NaN
console.log(+"abc");  // NaN
```

### Ví dụ 5: ! và !! — ép boolean
```js
console.log(!0);     // true   — 0 là falsy
console.log(!5);     // false  — 5 là truthy
console.log(!"");    // true   — "" là falsy
console.log(!"hi");  // false  — "hi" là truthy

console.log(!!0);    // false
console.log(!!5);    // true
console.log(!!"");   // false
console.log(!!null); // false
console.log(!!undefined); // false
console.log(!!{});   // true   — object luôn truthy
console.log(!![]);   // true   — array luôn truthy
```

### Ví dụ 6: typeof với biến chưa khai báo — an toàn
```js
// ✅ Không lỗi — undefined
console.log(typeof undeclaredVariable); // "undefined"

// ❌ Lỗi — ReferenceError
console.log(undeclaredVariable); // ReferenceError: undeclaredVariable is not defined

// Ứng dụng: safe check
if (typeof window !== "undefined") {
  // code chỉ chạy trong browser
}
```

### Ví dụ 7: Delete trong object cleanup before API
```js
function sanitizeUser(user) {
  const sanitized = { ...user };
  delete sanitized.password;    // xóa password before send
  delete sanitized.__v;         // xóa version field
  delete sanitized.createdAt;   // xóa timestamp
  return sanitized;
}

const rawUser = {
  id: 1,
  name: "Sơn",
  password: "secret123",
  __v: 1,
  createdAt: "2024-01-01"
};
console.log(sanitizeUser(rawUser));
// { id: 1, name: "Sơn" }
```

### Ví dụ 8: Void trong HTML attribute
```js
// Trong HTML:
// <a href="javascript:void(0)" onclick="doSomething()">Click</a>
// void(0) đảm bảo không navigate đi đâu cả

// Trong JS thuần:
const noop = () => void console.log("this logs but returns undefined");
noop(); // in "this logs but returns undefined" rồi return undefined
```

### Ví dụ 9: Combine typeof + !! — safe type check
```js
function getTypeSafe(value) {
  const type = typeof value;
  if (type === "object") {
    if (value === null) return "null";
    if (Array.isArray(value)) return "array";
    return "object";
  }
  return type;
}

console.log(getTypeSafe(null));     // "null"
console.log(getTypeSafe([]));       // "array"
console.log(getTypeSafe({}));       // "object"
console.log(getTypeSafe(42));       // "number"
console.log(getTypeSafe("hi"));     // "string"
```

### Ví dụ 10: Unary operators trong real-world pattern
```js
// Pattern 1: Safe Number conversion
function toNumber(val) {
  const num = +val;
  if (isNaN(num)) throw new TypeError(`Cannot convert ${val} to number`);
  return num;
}

// Pattern 2: Boolean coercion
const isEnabled = !!(config && config.features && config.features.enable);

// Pattern 3: Unique ID with void
function createCounter() {
  let count = 0;
  return {
    inc: () => ++count,
    get: () => count,
    reset: () => (count = 0, void 0) // return undefined after reset
  };
}
```

## 🔬 So sánh với alternatives

| Toán tử | Alternative | Khi nào dùng alternative |
|---|---|---|
| `typeof x` | `x instanceof Constructor` | `instanceof` cho object type check, `typeof` cho primitive |
| `void 0` | `undefined` | `void 0` an toàn hơn nếu `undefined` bị override |
| `+str` | `Number(str)` | `+` ngắn gọn hơn, `Number()` rõ nghĩa hơn |
| `!!x` | `Boolean(x)` | Tương đương — `!!` ngắn hơn, `Boolean()` rõ hơn |
| `delete obj.prop` | `obj.prop = undefined` | `delete` xóa property thật sự, `= undefined` chỉ set value |
| `typeof null === "object"` | `value === null` | Luôn dùng `=== null` để check null |

## 📊 Performance & Best Practices

**Performance**: Unary operators **rất nhanh** — đều là native engine operations, không có function call overhead. `typeof` đặc biệt tối ưu vì engine có thể check type tag trực tiếp.

**Best practices**:
- **Luôn dùng `null === null`** thay `typeof x === "object"` để check null.
- **Dùng `Array.isArray(x)`** thay `typeof x === "object"` để check array.
- **Dùng `Number.isNaN(x)`** thay `typeof x === "number" && isNaN(x)` — chính xác hơn.
- **Prefix `++i` trong vòng for** — convention phổ biến, performance tương đương postfix.
- **Dùng `??` thay `||`** cho default values — `||` treat `0`, `""`, `false` như null.
- **Hạn chế `delete`** — có thể de-optimize V8 engine, dùng immutable patterns thay thế.
- **Dùng `void 0`** thay `undefined` trong minified code — an toàn hơn.

**Quy tắc "3 nên — 3 không"**:
- ✅ Nên dùng `typeof` để check type trước khi process.
- ✅ Nên dùng `!!` để ép rõ ràng thành boolean.
- ✅ Nên dùng `void 0` để get guaranteed undefined.
- ❌ Không nên dùng `typeof null === "object"` để check null.
- ❌ Không nên lạm dụng `delete` — dùng spread/copy thay thế.
- ❌ Không nên dùng `+` với object/array phức tạp — kết quả không dự đoán được.

## 🔗 Liên kết chéo

- Tổng quan Operators: `08_expressions-and-operators/README.md` — all operator groups.
- Prefix/Postfix: `08_expressions-and-operators/01_operators/6_toan-tu-prefix-postfix.js` — `++`/`--` chi tiết.
- Bitwise: `08_expressions-and-operators/02_bitwise/app.js` — `~` operator chi tiết.
- Comparison: `08_expressions-and-operators/01_operators/4_toan-tu-so-sanh.js` — `===` vs `==`.
- Arrow functions: `09_functions/01_parameters-and-arrow/03_arrow-functions/` — arrow function với unary operators.
- Strict mode: `09_functions/02_scope-closure-strict-mode/01_strict-mode/` — strict mode ảnh hưởng `delete`.
- callbacks: `09_functions/01_parameters-and-arrow/01_callbacks/` — callback pattern.
