# Error Objects — Các đối tượng lỗi chuẩn (Thực hành chi tiết) — [Level: Intermediate]

## 🔑 Khái niệm cốt lõi

JavaScript cung cấp sẵn các **"họ" lỗi chuẩn** (built-in error types) để biểu thị từng kiểu lỗi khác nhau. Tất cả đều kế thừa từ `Error` và có ba thuộc tính quan trọng:

| Thuộc tính | Mô tả |
|---|---|
| `name` | Tên loại lỗi (`"TypeError"`, `"SyntaxError"`, ...) |
| `message` | Mô tả chi tiết lỗi |
| `stack` | Dấu vết ngăn xếp gọi hàm — giúp debug chính xác vị trí lỗi |

Các loại lỗi chuẩn phổ biến:

| Loại | Khi nào xuất hiện | Ví dụ |
|---|---|---|
| `Error` | Lỗi chung, hoặc do bạn `throw new Error(...)` | `throw new Error("something went wrong")` |
| `TypeError` | Gọi hàm/đọc thuộc tính sai kiểu | `null.f()`, `undefined()` |
| `ReferenceError` | Truy cập biến chưa khai báo | `console.log(undeclaredVar)` |
| `SyntaxError` | Sai cú pháp (thường gặp khi `eval` chuỗi sai) | `eval("a b")` |
| `RangeError` | Số nằm ngoài phạm vi hợp lệ | `new Array(-1)`, đệ quy vô hạn |
| `URIError` | Dùng hàm URI với chuỗi sai quy tắc | `decodeURIComponent("%")` |

File `app.js` trong thư mục có ba lần kiểm chứng điển hình:
1. `null.f()` → `TypeError` (`e.name === "TypeError"`, `instanceof TypeError` là `true`).
2. `eval("a b")` → `SyntaxError` (chuỗi không phải cú pháp hợp lệ).
3. `new RangeError("range").name` → `"RangeError"`.

**Cơ chế bên trong**: khi lỗi xảy ra, engine tạo một instance của error class tương ứng,填充 `name`, `message`, và `stack`. `stack` là chuỗi mô tả call stack tại thời điểm throw — mỗi dòng là một frame hàm, giúp truy vết từ lỗi đến nguyên nhân gốc.

## 📐 Cấu trúc / Cú pháp

### Tạo Error objects
```js
// Generic Error
new Error("message")

// Typed Errors
new TypeError("wrong type")
new ReferenceError("variable not defined")
new SyntaxError("unexpected token")
new RangeError("out of range")
new URIError("malformed URI")

// Custom Error subclass
class AppError extends Error {
  constructor(message, code) {
    super(message);
    this.name = "AppError";
    this.code = code;
  }
}
```

### Kiểm tra loại lỗi
```js
try {
  riskyOperation();
} catch (e) {
  // Cách 1: instanceof
  if (e instanceof TypeError) { /* handle type error */ }

  // Cách 2: check name
  if (e.name === "TypeError") { /* handle type error */ }

  // Cách 3: check constructor
  if (e.constructor === TypeError) { /* handle type error */ }
}
```

### Error properties
```js
const err = new TypeError("bad value");
console.log(err.name);    // "TypeError"
console.log(err.message); // "bad value"
console.log(err.stack);   // "TypeError: bad value\n    at ...".split('\n')[0]
```

## ✅ Điểm mạnh

1. **Chuẩn hóa thông tin lỗi**: `name` + `message` + `stack`, ai cũng hiểu được — không cần docs riêng.
2. **Phân loại lỗi bằng `instanceof` và `name`** → viết `catch` theo từng loại lỗi cụ thể, xử lý đúng cách.
3. **Kế thừa từ `Error`** nên dùng chung được với tất cả cấu trúc xử lý lỗi (`try/catch`, promises, async/await).
4. **Giúp debug nhanh**: nhìn `name` biết ngay lỗi kiểu gì (gọi sai phương thức, biến thiếu, cú pháp sai...).
5. **Có thể tự tạo subclass của `Error`** cho lỗi nghiệp vụ của dự án — thêm `code`, `field`, `status` tùy chỉnh.
6. **`stack` trace tự động** — biết chính xác file/dòng nào, hàm nào gọi, giúp fix bug nhanh hơn nhiều.
7. **Browser và Node.js đều support** — cross-platform error handling.
8. **Error cause chaining** (ES2022) — `new Error("wrapper", { cause: innerError })` giữ lại chain lỗi.
9. **Có thể serialize** — `JSON.stringify` bỏ qua `stack`, nhưng `message` và `name` vẫn giữ được.
10. **Internationalization friendly** — `message` có thể chứa tiếng Việt, dễ hiển thị cho user.

## ⚠️ Bẫy thường gặp & Hạn chế

1. **Nhầm lẫn `TypeError`**: là do **thao tác trên giá trị sai kiểu** (như `null.f()`, gọi số như hàm), chứ không phải "kiểu dữ liệu sai khi so sánh".
   ```js
   // ❌ Không phải TypeError
   if (a == "2") {} // chỉ là loose equality

   // ✅ Đúng — TypeError khi gọi hàm trên number
   (42)(); // TypeError: 42 is not a function
   ```

2. **Lỗi cú pháp của chương trình** (file JS bị sai cú pháp) không bắt được bằng `try...catch` — nó xảy ra lúc parse, không phải lúc chạy.
   ```js
   // ❌ Không thể catch lỗi cú pháp file
   try {
     eval("function {"); // SyntaxError lúc parse, không phải runtime
   } catch (e) {
     // Có thể catch nếu dùng eval, nhưng không catch được syntax error trong file
   }
   ```

3. **Dùng `instanceof` đáng tin hơn** so với đọc chuỗi `message` — vì message có thể được tùy biến, còn `instanceof` dựa vào prototype chain.
   ```js
   // ❌ Dựa vào message string — fragile
   if (e.message.includes("type")) { ... }
   // ✅ Dựa vào instanceof — robust
   if (e instanceof TypeError) { ... }
   ```

4. **Khi phải handle mọi kiểu lỗi**, đừng chỉ dựa vào `TypeError` — có cả `EvalError`, `URIError`, lỗi custom, lỗi từ third-party library.
   ```js
   // ❌ Bắt chung chung
   catch (e) { handleAll(e); }
   // ✅ Bắt có chọn lọc
   catch (e) {
     if (e instanceof TypeError) handleType(e);
     else if (e instanceof ReferenceError) handleRef(e);
     else throw e; // re-throw
   }
   ```

5. **`stack` trace có thể bị truncate** trong browser nếu error được tạo sớm (trước khi throw).
6. **Error objects tạo overhead** — không nên tạo quá nhiều trong vòng lặp tight.
7. **Một số lỗi không có `stack`** — ví dụ lỗi từ `eval()` trong một số environment.

## 💡 Khi nào dùng

1. **Bắt lỗi và hiển thị thông báo phù hợp** theo từng loại lỗi — TypeError hiện "Sai kiểu dữ liệu", SyntaxError hiện "Cấu trúc dữ liệu sai".
2. **Debug ngay tại console**: đọc `e.name`/`e.message`/`e.stack` để truy vết nhanh.
3. **`JSON.parse` / `eval`** — bắt `SyntaxError` để xử lý chuỗi đầu vào xấu, fallback sang default.
4. **Viết guard cho thư viện**: `throw new TypeError("tham số phải là number")` — self-documenting API.
5. **Giám sát lỗi sản phẩm** (Sentry, logging) dựa trên `name` và `stack` — group lỗi theo type.
6. **Validation layer** — throw specific error types cho từng trường validation fail.
7. **API error responses** — map error type to HTTP status code (TypeError → 400, RangeError → 422).

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: TypeError — null.f() (file `app.js`)
```js
try {
  null.f(); // đọc thuộc tính/method của null
} catch (e) {
  console.log(e.name, e instanceof TypeError); // "TypeError" true
  console.log(e.message); // "Cannot read properties of null (reading 'f')"
  console.log(e.stack.split('\n')[0]); // "TypeError: Cannot read..."
}
```

### Ví dụ 2: SyntaxError — eval chuỗi sai (file `app.js`)
```js
try {
  eval("a b"); // chuỗi không phải cú pháp hợp lệ
} catch (e) {
  console.log(e.name); // "SyntaxError"
  console.log(e.message); // "Unexpected identifier"
}
```

### Ví dụ 3: RangeError — constructor mảng âm (file `app.js`)
```js
console.log(new RangeError("range").name); // "RangeError"

// Thực tế: new Array(-1) throw RangeError
try {
  new Array(-1);
} catch (e) {
  console.log(e.name); // "RangeError"
  console.log(e.message); // "Invalid array length"
}
```

### Ví dụ 4: ReferenceError — biến chưa khai báo
```js
try {
  console.log(undeclaredVariable);
} catch (e) {
  console.log(e.name); // "ReferenceError"
  console.log(e.message); // "undeclaredVariable is not defined"
}
```

### Ví dụ 5: URIError — decodeURIComponent chuỗi sai
```js
try {
  decodeURIComponent("%"); // percent encode sai
} catch (e) {
  console.log(e.name); // "URIError"
  console.log(e.message); // "URI malformed"
}
```

### Ví dụ 6: Custom Error subclass
```js
class ValidationError extends Error {
  constructor(field, message) {
    super(message);
    this.name = "ValidationError";
    this.field = field;
  }
}

function validateUser(user) {
  if (!user.name) throw new ValidationError("name", "Name is required");
  if (user.age < 0) throw new ValidationError("age", "Age cannot be negative");
  return true;
}

try {
  validateUser({ age: -5 });
} catch (e) {
  if (e instanceof ValidationError) {
    console.log(`Field: ${e.field}, Message: ${e.message}`);
    // "Field: age, Message: Age cannot be negative"
  }
}
```

### Ví dụ 7: Phân loại lỗi bằng instanceof trong catch
```js
function processInput(input) {
  try {
    const num = Number(input);
    if (isNaN(num)) throw new TypeError("Input cannot be converted to number");
    if (num < 0) throw new RangeError("Number must be non-negative");
    return Math.sqrt(num);
  } catch (e) {
    if (e instanceof TypeError) {
      console.log("TypeError handled:", e.message);
      return null;
    }
    if (e instanceof RangeError) {
      console.log("RangeError handled:", e.message);
      return 0;
    }
    throw e; // re-throw lỗi không biết xử lý
  }
}
```

### Ví dụ 8: Error cause chaining (ES2022)
```js
try {
  try {
    JSON.parse("{ invalid }");
  } catch (inner) {
    throw new Error("Config parsing failed", { cause: inner });
  }
} catch (outer) {
  console.log(outer.message);       // "Config parsing failed"
  console.log(outer.cause.message); // "Unexpected token i in JSON..."
}
```

### Ví dụ 9: Map lỗi sang HTTP status
```js
function mapErrorToStatus(error) {
  const mapping = {
    TypeError: 400,
    RangeError: 422,
    SyntaxError: 400,
    ReferenceError: 500,
  };
  return mapping[error.name] || 500;
}

console.log(mapErrorToStatus(new TypeError("bad"))); // 400
console.log(mapErrorToStatus(new RangeError("out"))); // 422
```

### Ví dụ 10: Logger errors with context
```js
function logError(error, context = "") {
  console.error(`[${context}] ${error.name}: ${error.message}`);
  console.error("Stack:", error.stack);
}

try {
  fetchData("/api/users");
} catch (e) {
  logError(e, "fetchData");
  // "[fetchData] TypeError: Failed to fetch"
  // "Stack: TypeError: Failed to fetch..."
}
```

## 🔬 So sánh với alternatives

| Phương án | Ưu điểm | Nhược điểm | Phù hợp khi |
|---|---|---|---|
| Built-in Error types | Chuẩn, có sẵn, `instanceof` works | Hạn chế loại lỗi | Lỗi runtime thông thường |
| Custom Error subclass | Mở rộng thêm field/code | Cần viết thêm code | Business logic errors |
| String throw | Đơn giản | Mất stack, khó debug | Quick scripts, không production |
| Object throw | Tự do cấu trúc | Không có stack, không instanceof | API internal, non-standard |
| Result/Either (thư viện) | Functional, type-safe | Cần thư viện | Enterprise FP codebase |

## 📊 Performance & Best Practices

**Performance**: Tạo Error object có overhead nhỏ (~microseconds) do cần capture stack trace. Trong **vòng lặp tight** (>100k), nên tránh tạo Error — dùng guard clause thay thế.

**Best practices**:
- Luôn **throw Error object** thay vì string/number — có stack trace để debug.
- Dùng **`instanceof`** để phân loại lỗi — robust hơn so với đọc chuỗi `message`.
- Tạo **custom Error subclass** cho business logic errors — thêm `code`, `field`, `status`.
- Luôn **log lỗi** trong `catch` — đừng swallow im lặng.
- **Re-throw** lỗi không biết cách xử lý — đừng bắt mọi thứ.
- Dùng **Error cause** (ES2022) để giữ chain lỗi: `new Error("wrapper", { cause: inner })`.
- Tránh **tạo Error trong vòng lặp** — dùng sentinel value thay thế nếu performance критичен.
- Map lỗi sang **HTTP status code** trong API layer — TypeError → 400, RangeError → 422.

## 🔗 Liên kết chéo

- Throw lỗi: `07_exceptional-handling/01_throw/` — cách dùng `throw` đúng chuẩn.
- Try/Catch/Finally: `07_exceptional-handling/02_try-catch-finally/` — thứ tự hoạt động, finally lồng.
- Tổng quan Exceptional Handling: `07_exceptional-handling/README.md` — khái niệm cốt lõi.
- Hàm và throw: `09_functions/01_parameters-and-arrow/` — throw lỗi trong hàm khi tham số sai.
- Strict mode: `09_functions/02_scope-closure-strict-mode/01_strict-mode/` — strict mode phát hiện lỗi sớm hơn.
- Arrow functions: `09_functions/01_parameters-and-arrow/03_arrow-functions/` — arrow function trong error handling context.
