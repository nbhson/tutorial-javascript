# Xử lý ngoại lệ (Exceptional Handling) — [Level: Intermediate]

## 🔑 Khái niệm cốt lõi

**Xử lý ngoại lệ** (exception handling) là kỹ thuật **kiểm soát lỗi** để chương trình không "chết" giữa chừng khi có lỗi xảy ra. Trong JavaScript, khi một lỗi phát sinh (gọi hàm sai đối số, truy cập thuộc tính của `null`, parse JSON thất bại...), engine sẽ **ném ra một exception** — nếu không có gì bắt nó, chương trình dừng hẳn và in stack trace ra console (cảnh "màn hình đỏ" mà mọi lập trình viên đều gặp).

JavaScript cung cấp bộ ba công cụ xử lý lỗi:

| Từ khóa | Vai trò | Hành vi |
|---|---|---|
| `throw` | Chủ động ném lỗi | Dừng luồng hiện tại, truyền thông tin lỗi ra ngoài |
| `try` | Khối thử nghiệm | Chạy code có thể gây lỗi |
| `catch` | Khối bắt lỗi | Chạy khi có lỗi được ném trong `try` |
| `finally` | Khối dọn dẹp | **Luôn chạy** dù có lỗi hay không, có `return` hay `throw` trong `try` |

**Base error types** (`Error`, `TypeError`, `ReferenceError`, `SyntaxError`, `RangeError`, `URIError`) đều kế thừa từ `Error` và có 3 thuộc tính quan trọng: `name` (tên lỗi), `message` (mô tả), `stack` (dấu vết ngăn xếp gọi hàm).

Khi lỗi không được bắt, chương trình sẽ dừng và in stack trace — đúng cái cảnh "trang web đã dừng phản hồi" mà ai lập trình lâu ngày cũng từng gặp. Hiểu cơ chế này giúp bạn viết code **resilient** (kiên cường) — tiếp tục hoạt động ngay cả khi có lỗi.

## 📐 Cấu trúc / Cú pháp

### `try...catch...finally`
```js
try {
  // Code có thể ném lỗi
  riskyOperation();
} catch (error) {
  // Chạy khi có lỗi trong try
  console.error(error.message);
} finally {
  // Luôn chạy — thành công hay thất bại
  cleanup();
}
```

### `throw` — Ném lỗi chủ động
```js
function divide(a, b) {
  if (b === 0) throw new Error("Cannot divide by zero");
  return a / b;
}
```

### Error Objects
```js
// Các lỗi chuẩn của JavaScript
new Error("message")           // Lỗi chung
new TypeError("not a function") // Gọi hàm trên giá trị sai kiểu
new ReferenceError("x is not defined") // Truy cập biến chưa khai báo
new SyntaxError("unexpected token")     // Sai cú pháp
new RangeError("array length invalid")  // Số ngoài phạm vi hợp lệ
new URIError("malformed URI")           // URI sai quy tắc
```

### Catch không cần tham số (ES2019)
```js
try {
  somethingRisky();
} catch {
  // ES2019+: bỏ qua tên parameter khi không cần dùng
  handleError();
} finally {
  cleanup();
}
```

## ✅ Điểm mạnh

1. **Chương trình không chết oan**: lỗi được kiểm soát và thông báo thân thiện thay vì treo app.
2. **Tách biệt logic và xử lý lỗi**: code chính gọn gàng, phần xử lý lỗi gom vào `catch`.
3. **`finally` đảm bảo dọn dẹp** trong mọi trường hợp — kể cả khi có `return` hoặc `throw` trong `try`.
4. **Throw được mọi giá trị** → linh hoạt trong việc truyền thông tin lỗi tùy ngữ cảnh.
5. Error objects chuẩn giúp phân biệt loại lỗi bằng `instanceof`, `name` hoặc `message`.
6. **Catch không cần tham số** (ES2019) — gọn hơn khi chỉ cần `finally`.
7. **Stack trace** (`error.stack`) giúp debug nhanh — biết chính xác lỗi xảy ra ở file/dòng nào.
8. **Custom Error subclasses** — tạo lớp lỗi riêng cho business logic của dự án.
9. **Graceful degradation** — fallback sang dữ liệu mặc định khi API lỗi, thay vì crash.
10. **Testable** — dễ viết unit test kiểm tra các path lỗi (error paths).

## ⚠️ Bẫy thường gặp & Hạn chế

1. **Ném string/object thay vì Error object** — mất `stack` trace, khó debug.
   ```js
   // ❌ Tránh
   throw "đây là lỗi";
   throw { code: 400, message: "Bad request" };
   // ✅ Nên dùng
   throw new Error("đây là lỗi");
   throw new TypeError("tham số phải là string");
   ```

2. **`try...catch` chỉ bắt lỗi đồng bộ** — lỗi trong callback, promise, `setTimeout` không bị bắt trực tiếp.
   ```js
   try {
     setTimeout(() => { throw new Error("lỗi async"); }, 1000);
   } catch (e) {
     // KHÔNG bao giờ chạy — lỗi async nằm ngoài try block
   }
   // Phải dùng .catch() hoặc async/await
   ```

3. **`finally` có thể che lấp lỗi gốc** — nếu `finally` tự ném lỗi, lỗi đó sẽ override lỗi từ `try`.
   ```js
   try {
     throw new Error("nguồn");
   } finally {
     throw new Error("finally"); // → lỗi "finally" override "nguồn"
   }
   ```

4. **Lạm dụng `try...catch` để "nuốt" lỗi** — bỏ `console.error` trong `catch` khiến việc debug sau này cực kỳ khó.
   ```js
   try {
     fetchData();
   } catch (e) {
     // Im lặngnuốt lỗi — rất tệ!
   }
   // ✅ Luôn log hoặc re-throw
   ```

5. **Overhead performance** — `try...catch` có chi phí nhỏ khi không có lỗi, nhưng đáng kể trong vòng lặp tight.
   ```js
   // ❌ Tránh trong vòng lặp tight
   for (let i = 0; i < 1000000; i++) {
     try { parseInt(str); } catch(e) {}
   }
   // ✅ Kiểm tra trước thay catch
   for (let i = 0; i < 1000000; i++) {
     if (isNaN(parseInt(str))) handleInvalid();
   }
   ```

6. **Catch tất cả lỗi chung chung** — không phân biệt loại lỗi, khó xử lý đúng cách.
   ```js
   // ❌ Quá chung
   catch (e) { console.log(e); }
   // ✅ Phân loại
   catch (e) {
     if (e instanceof TypeError) handleTypeError(e);
     else if (e instanceof ReferenceError) handleRefError(e);
     else throw e; // re-throw lỗi không mong đợi
   }
   ```

## 💡 Khi nào dùng

1. **Thẩm định dữ liệu đầu vào** — chia cho 0, nhập sai định dạng, JSON lỗi cú pháp.
2. **Gọi API / đọc file** — mạng không ổn định, cần bắt lỗi và thông báo graceful.
3. **Phân tích cú pháp** — `JSON.parse`, `eval` — dễ ném lỗi với input không hợp lệ.
4. **Code thư viện/helper** — `throw` lỗi rõ ràng cho người dùng hàm biết đã truyền sai tham số.
5. **Dọn dẹp tài nguyên bắt buộc** — đóng modal, xóa spinner, ngắt kết nối — đặt ở `finally`.
6. **Tầng giao diện** — catch lỗi từ deep call stack, hiển thị toast/message thân thiện.
7. **Transaction database** — rollback nếu có lỗi giữa chừng, commit nếu mọi thứ OK.
8. **Retry logic** — catch lỗi network, thử lại N lần trước khi báo failure.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: `throw` cơ bản (file `app.js` trong `01_throw/`)
```js
function div(a, b) {
  if (b === 0) throw new Error("divide by zero"); // ném lỗi khi mẫu số = 0
  return a / b;
}

try {
  div(1, 0); // gọi hàm có thể ném lỗi
} catch (e) {
  console.log(e.message); // "divide by zero" — bắt và xử lý
}
```

### Ví dụ 2: `try...catch...finally` (file `app.js` trong `02_try-catch-finally/`)
```js
function risky() {
  throw new Error("fail");
}

try {
  risky();
} catch (e) {
  console.log("catch", e.message); // "catch fail"
} finally {
  console.log("finally");          // "finally" — luôn chạy
}
```

### Ví dụ 3: Finally lồng trong finally (file `app.js` trong `02_try-catch-finally/`)
```js
try {
  try {
    throw new Error("inner");
  } finally {
    console.log("inner finally");  // chạy trước
  }
} catch (e) {
  console.log("outer catch");      // chạy sau
}
// Kết quả: "inner finally" → "outer catch"
```

### Ví dụ 4: Error objects — phân biệt TypeError, SyntaxError, RangeError (file `app.js` trong `03_error-objects/`)
```js
try {
  null.f(); // đọc thuộc tính của null → TypeError
} catch (e) {
  console.log(e.name, e instanceof TypeError); // "TypeError" true
}

try {
  eval("a b"); // cú pháp sai → SyntaxError
} catch (e) {
  console.log(e.name); // "SyntaxError"
}

console.log(new RangeError("range").name); // "RangeError"
```

### Ví dụ 5: Custom Error subclass
```js
class ValidationError extends Error {
  constructor(field, message) {
    super(message);
    this.name = "ValidationError";
    this.field = field;
  }
}

function validateAge(age) {
  if (age < 0) throw new ValidationError("age", "Age cannot be negative");
  if (age > 150) throw new ValidationError("age", "Age too high");
}

try {
  validateAge(-5);
} catch (e) {
  if (e instanceof ValidationError) {
    console.log(`Lỗi tại ${e.field}: ${e.message}`);
  } else {
    throw e; // re-throw lỗi không mong đợi
  }
}
```

### Ví dụ 6: Retry logic với try/catch
```js
async function fetchWithRetry(url, retries = 3) {
  for (let i = 0; i < retries; i++) {
    try {
      const response = await fetch(url);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return await response.json();
    } catch (e) {
      if (i === retries - 1) throw e; // lần cuối cùng — re-throw
      console.log(`Retry ${i + 1}/${retries}...`);
    }
  }
}
```

### Ví dụ 7: Finally đảm bảo cleanup
```js
function loadData() {
  let connection;
  try {
    connection = openConnection();
    const data = queryDatabase(connection);
    return data;
  } catch (e) {
    console.error("Query failed:", e.message);
    throw e; // re-throw sau khi log
  } finally {
    if (connection) closeConnection(connection); // luôn đóng connection
  }
}
```

### Ví dụ 8: JSON.parse với fallback
```js
function parseConfig(raw) {
  try {
    return JSON.parse(raw);
  } catch (e) {
    console.warn("Invalid JSON, using default config");
    return { version: "1.0", debug: false }; // default values
  }
}
```

### Ví dụ 9: Error handling trong callback (phải dùng try/catch bên trong)
```js
function processItems(items, processor) {
  const results = [];
  for (const item of items) {
    try {
      results.push(processor(item));
    } catch (e) {
      console.error(`Failed to process ${item}:`, e.message);
      // Tiếp tục xử lý các item khác
    }
  }
  return results;
}
```

### Ví dụ 10: Không bắt lỗi async trong try đồng bộ
```js
// ❌ Sai — lỗi trong setTimeout không bị catch
try {
  setTimeout(() => { throw new Error("async error"); }, 100);
} catch (e) {
  console.log("caught"); // KHÔNG bao giờ chạy
}

// ✅ Đúng — dùng Promise.catch hoặc async/await
async function safeAsync() {
  try {
    await someAsyncOperation();
  } catch (e) {
    console.log("caught async:", e.message);
  }
}
```

## 🔬 So sánh với alternatives

| Phương án | Ưu điểm | Nhược điểm | Phù hợp khi |
|---|---|---|---|
| `try...catch` | Bắt lỗi runtime, cấu trúc rõ ràng | Chỉ bắt lỗi đồng bộ trong khối | Lỗi có thể dự đoán, cần fallback |
| `throw` + kiểm tra return value | Không cần try/catch, code phẳng | Phải kiểm tra mọi return, dễ bỏ sót | API đơn giản, lỗi hiếm |
| Promise `.catch()` | Xử lý async error, chainable | Chỉ áp dụng cho promise-based code | Async operations, fetch, DB queries |
| `async/await` + try/catch | Code đồng bộ hóa, dễ đọc | Tương tự try/catch về mặt error handling | Modern async code |
| Guard clauses | Phòng lỗi từ đầu, không cần catch | Không bắt được mọi lỗi runtime | Input validation, early exit |
| Result/Either pattern (thư viện) | Functional, explicit về success/failure | Cần thư viện, học curve | Codebase functional, enterprise |

## 📊 Performance & Best Practices

**Performance**: `try...catch` có **overhead nhỏ** ngay cả khi không có lỗi (engine phải setup exception handling frame). Trong vòng lặp tight (>100k iter), nên dùng **guard clause** thay thế.

**Best practices**:
- Luôn `throw new Error(...)` thay vì `throw "string"` — có `stack` trace để debug.
- Log lỗi trong `catch` — đừng swallow (nuốt) lỗi im lặng.
- Dùng `instanceof` để phân biệt loại lỗi và xử lý phù hợp.
- Luôn có `finally` khi cần dọn dẹp tài nguyên (connection, timer, lock).
- Re-throw lỗi không biết cách xử lý — đừng cố bắt mọi thứ.
- Dùng custom Error subclass cho business logic errors.
- Tránh nested try/catch quá sâu — để lỗi nổi lên tầng xử lý cao nhất.

**Quy tắc "3 không"**:
1. Không swallow lỗi (bỏ `console.error`).
2. Không nested try/catch quá 2 cấp.
3. Không catch lỗi async trong synchronous try.

## 🔗 Liên kết chéo

- Throw lỗi: `07_exceptional-handling/01_throw/` — cách dùng `throw` đúng chuẩn với Error object (`app.js`).
- Try/catch/finally: `07_exceptional-handling/02_try-catch-finally/` — thứ tự hoạt động, finally lồng (`app.js`).
- Error objects: `07_exceptional-handling/03_error-objects/` — phân biệt TypeError, SyntaxError, RangeError (`app.js`).
- Kết hợp với Functions: `09_functions/01_parameters-and-arrow/` — throw lỗi trong hàm khi tham số sai.
- Kết hợp với Arrow: `09_functions/01_parameters-and-arrow/03_arrow-functions/` — arrow function trong try/catch.
- Non-blocking I/O: `09_functions/02_scope-closure-strict-mode/04_non-blocking-io/` — lỗi async không bị bắt bởi synchronous try/catch.
