# Built-in: Error (Xử lý lỗi) — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

**`Error`** là built-in object đại diện cho **runtime exception** — sự kiện xảy ra khi chương trình gặp điều kiện bất thường không thể tiếp tục thực thi bình thường. Ngoài `Error` base class, JS có **7 sub-class chuyên biệt** dành cho từng loại lỗi khác nhau.

### Cơ chế throw/catch nội tại

Khi engine gặp lỗi runtime:
1. **Tạo Error object** — allocate trên heap với `name`, `message`, `stack`.
2. **Unwind call stack** — pop các frame từ điểm lỗi lên đến try/catch block gần nhất.
3. **Transfer control to catch** — chạy handler với error object.
4. **Nếu không có catch** — propagate lên top-level → app crash (Node kill process, Browser show red).

### Tạo và ném lỗi

```js
// Error constructor: Error(message)
throw new Error("Something went wrong");

// Specific subclasses (tự gán `name` property đúng)
throw new TypeError("Expected a number, got string");
throw new RangeError("Value out of range: " + value);
throw new ReferenceError("Variable is not defined");
throw new SyntaxError("Unexpected token '}'");
```

### Thuộc tính cơ bản của Error object

| Property | Type | Ý nghĩa |
|----------|------|---------|
| `name` | `string` | Tên loại lỗi: `"TypeError"`, `"RangeError"`, `"Error"`... |
| `message` | `string` | Thông điệp mô tả chi tiết lỗi |
| `stack` | `string` | Call stack trace — nơi lỗi xảy ra và gọi qua đâu |
| `cause` | `Error\|undefined` | (ES2022) lỗi gốc gây ra lỗi này |

```js
try {
  throw new TypeError("bad type");
} catch (e) {
  console.log(e.name);      // "TypeError"
  console.log(e.message);   // "bad type"
  console.log(e.stack);     // "TypeError: bad type\n    at ..." — stack trace dài
}
```

## 📐 Cấu trúc nhóm

```
02_data-types/04_builtin-objects/04_error/
├── README.md         ← bài này
├── app.js            ← demo throw, catch, Error properties
└── index.html
```

## ✅ Điểm mạnh — Tại sao cần Error handling

| # | Điểm mạnh | Lý do |
|---|-----------|-------|
| 1 | **Kiểm soát flow lỗi** | App không "chết" khi gặp input xấu — graceful degradation |
| 2 | **Debug nhanh** | `e.stack` cho biết chính xác file:line gây lỗi |
| 3 | **Phân loại xử lý** | `instanceof TypeError` → xử lý khác `instanceof RangeError` |
| 4 | **Propagate lỗi qua nhiều tầng** | `throw` truyền data error từ deep call lên handler cấp cao |
| 5 | **Custom error types** | `class ValidationError extends Error` — domain-specific errors |
| 6 | **Async error chaining** | `.catch()` + `try/catch(try-catch)` kết nối sync-async |
| 7 | **Logging production** | `console.error(e.name, e.message, e.stack)` — report chính xác |

## ⚠️ Bẫy thường gặp & Hạn chế

| # | Bẫy | Ví dụ | Cách tránh |
|---|-----|-------|-----------|
| 1 | **Quên `try/catch` → crash chương trình** | `JSON.parse("bad")` không bọc → uncaught exception | Bọc mọi thao tác rủi ro (parse, async API) |
| 2 | **`throw "string"` mất `message`/`stack`** | `e.stack` → undefined | Luôn `throw new Error(...)` để có đủ properties |
| 3 | **`catch {}` (rỗng) nuốt lỗi** | Bug bị ẩn, khó debug | Luôn log hoặc re-throw: `catch (e) { console.error(e); throw e; }` |
| 4 | **Sync try/catch không bắt được async error** | `asyncFn().catch(...)` cần `.catch()`, không dùng `try` | Dùng `.catch()` với Promise, `try/await` với async/await |
| 5 | **Nested try/catch chồng chéo** | Catch wrong layer, mask real error | Catch at appropriate level — let unhandled errors surface |
| 6 | **Custom error subclass bị mất stack** | `Object.create(Error.prototype)` không auto-set stack | Dùng `class CustomError extends Error` hoặc `Object.setPrototypeOf(e, CustomError.prototype)` |
| 7 | **`SyntaxError` bắt lúc parse, không lúc runtime** | `eval("return;")` → SyntaxError không bắt bằng try/catch bên trong cùng scope | Catch ở scope parser — thường là top-level module |

```js
// Bẫy 2: throw string mất stack trace
try {
  throw "something broke";
} catch (e) {
  console.log(e.message);  // undefined — string không có message!
  console.log(e.stack);    // undefined
}

// Fix: always throw Error instance
try {
  throw new Error("something broke");
} catch (e) {
  console.log(e.name);     // "Error"
  console.log(e.message);  // "something broke"
  console.log(typeof e.stack); // "string"
}
```

## 💡 Khi nào dùng — Tình huống thực tế

1. **Validate input parameters** — ném `TypeError` nếu argument sai kiểu, `RangeError` nếu ra ngoài range.
2. **Wrap API calls** — `try { await fetch(...) } catch (e) { ... }` handle network failure.
3. **Parse risky JSON** — `JSON.parse()` ném `SyntaxError` nếu input bad.
4. **Class constructors** — validate và throw `Error` nếu config không hợp lệ.
5. **Middleware error handling** — Express/Next.js error middleware phân loại error type.
6. **Production logging** — log `e.stack` + `e.name` vào Sentry/Bugsnag/LogRocket.
7. **Fail-fast early** — throw sớm khi invariant vi phạm thay vì silent failure sau đó.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Error basics — throw và catch

```js
try {
  // Thao tác có rủi ro
  const user = JSON.parse('{"name": "Sơn"}');
  console.log(user.name);        // "Sơn"
} catch (error) {
  console.error("❌ Parse failed:", error.name, error.message);
}

// Phân loại lỗi
try {
  null.toFixed();                // TypeError
} catch (error) {
  if (error instanceof TypeError) {
    console.log("TypeError:", error.message);
  } else if (error instanceof RangeError) {
    console.log("RangeError:", error.message);
  } else {
    console.log("Unknown:", error.name, error.message);
  }
}
```

### Ví dụ 2: Throw custom Error subclass

```js
// Define custom error class (ES6 class syntax)
class ValidationError extends Error {
  constructor(field, message) {
    super(message);
    this.name = "ValidationError";
    this.field = field;        // property bổ sung
  }
}

class AuthenticationError extends Error {
  constructor(reason) {
    super(reason);
    this.name = "AuthenticationError";
    this.reason = reason;
  }
}

// Usage
function loginUser(username, password) {
  if (!username || !password) {
    throw new ValidationError("credentials", "Username and password required");
  }
  if (password.length < 8) {
    throw new ValidationError("password", "Password must be at least 8 characters");
  }
  return { user: username, loggedIn: true };
}

try {
  loginUser("", "short");
} catch (e) {
  if (e instanceof ValidationError) {
    console.log(`Field ${e.field}: ${e.message}`);
  } else {
    console.error("Login failed:", e.message);
  }
}
```

### Ví dụ 3: Async error handling — Promise và Async/Await

```js
// Pattern 1: Promise .catch()
async function fetchUser(id) {
  const res = await fetch(`/api/users/${id}`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

// Sử dụng
fetchUser(42)
  .then(user => console.log(user))
  .catch(err => console.error("Fetch failed:", err.message));

// Pattern 2: try/catch với async/await (clean hơn)
async function getUser(id) {
  try {
    const user = await fetchUser(id);
    console.log(user);
  } catch (err) {
    console.error("Failed to get user:", err);
    // Re-throw để caller xử lý tiếp
    throw err;
  }
}

// Pattern 3: Unhandled rejection warning
process.on("unhandledRejection", (reason, promise) => {
  console.error("Unhandled Rejection:", reason);
});
```

### Ví dụ 4: Error chaining — cause property (ES2022)

```js
try {
  try {
    JSON.parse(undefined);           // SyntaxError: ...
  } catch (inner) {
    // ES2022: chain error with cause
    throw new Error("Failed to load config", { cause: inner });
  }
} catch (outer) {
  console.log(outer.message);        // "Failed to load config"
  console.log(outer.cause.message);  // "Unexpected token u in JSON at position 0"
}
```

### Ví dụ 5: Defensive programming — validate before act

```js
function divide(a, b) {
  if (typeof a !== "number" || typeof b !== "number") {
    throw new TypeError(`Expected numbers, got ${typeof a} and ${typeof b}`);
  }
  if (b === 0) {
    throw new RangeError("Division by zero");
  }
  return a / b;
}

// Or use optional chaining + guard
function safeDivide(a, b) {
  if (typeof a !== "number" || typeof b !== "number" || b === 0) return null;
  return a / b;
}
```

### Ví dụ 6: Finally — luôn chạy, bất kể error

```js
function readFile(path) {
  let fileHandle;
  try {
    fileHandle = openFile(path);
    return parseContent(fileHandle);
  } catch (error) {
    console.error("Read error:", error.message);
    throw error; // re-throw after logging
  } finally {
    // Luôn chạy — release resource
    if (fileHandle) closeFile(fileHandle);
    console.log("File closed.");
  }
}
```

## 🔬 So sánh với alternatives

| Phương án | Ưu điểm | Nhược điểm | Phù hợp khi |
|-----------|---------|------------|-------------|
| **Native Error** | Built-in, stack trace, fast | Limited customization | General purpose errors |
| **Custom subclass** | Domain-specific properties | More boilerplate | Enterprise, library |
| **Result type** (fp) | Return value vs exception | Different paradigm | Rust/Haskell style |
| **Try-pattern functions** | No exceptions, explicit error field | Verbose, no stack trace | Hot-path performance |
| **Promise rejection** | Async-first design | Harder to trace | Async pipeline |

## 📊 Performance & Best Practices

- **Ghi log `e.stack`** trong production — debug lỗi runtime chính xác hơn `console.error(e.message)`.
- **Không swallow errors** — `catch {}` là anti-pattern; log + re-throw nếu không xử lý được.
- **Throw specific error types** — `TypeError` cho kiểu sai, `RangeError` cho giá trị ngoài range.
- **Avoid creating large error objects** trong hot loop — stack trace allocation tốn kém.
- **Use `cause` option** (ES2022) cho error chaining — giữ inner exception information.
- **Global handlers for uncaught errors** — `window.onerror`, `process.on('uncaughtException')` cho crash recovery.
- **Test error paths** — unit test cả happy path và error path để đảm bảo recover graceful.

## 🔗 Liên kết chéo

- Xem thêm: `07_exceptional-handling/01_throw/` — throw mechanism detail
- Xem thêm: `07_exceptional-handling/02_try-catch-finally/` — try/catch/finally structure
- Xem thêm: `07_exceptional-handling/03_error-objects/` — error object deep dive
- Xem thêm: `12_asynchronous-javascript/02_callbacks-promises/03_promise-concept/` — async error handling
- Tài liệu: [MDN — Error](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error), [javascript.info/try-catch](https://javascript.info/try-catch)
