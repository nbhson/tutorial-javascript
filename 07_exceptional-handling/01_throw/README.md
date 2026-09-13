# throw — Ném ngoại lệ (Thực hành chi tiết) — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

`throw` là từ khóa dùng để **chủ động phát ra một lỗi** (throw an exception) khi gặp tình huống bất thường mà bạn muốn dừng luồng chạy lại. Khi gặp `throw`, chương trình lập tức **thoát khỏi luồng bình thường** và: nếu có `try...catch` bao quanh thì rơi vào `catch`, còn không thì dừng hẳn và in lỗi ra console.

Điểm quan trọng nhất cần nhớ: **bạn có thể `throw` bất cứ giá trị nào** — không chỉ riêng lỗi. Tuy nhiên, thực tiễn tốt nhất là **luôn throw Error object** vì nó mang đầy đủ thông tin debug.

```js
throw new Error("oops");   // ✅ Tốt nhất — có name, message, stack
throw "string";            // ⚠️ Vẫn chạy được nhưng mất thông tin
throw { code: 400 };       // ⚠️ Tránh — mất stack trace, khó debug
throw 42;                  // ❌ Không nên — không có message gì cả
```

File `app.js` trong thư mục minh họa bằng hàm `div` — hàm này ném lỗi `"divide by zero"` khi mẫu số bằng `0`, sau đó bắt lỗi bằng `try...catch`.

**Cơ chế hoạt động bên trong engine**: khi `throw` được thực thi, JavaScript engine tạo một **exception object** (hoặc dùng giá trị bạn throw), sau đó **unwind call stack** — quay ngược lại qua các frame function cho đến khi tìm thấy `catch` handler phù hợp. Nếu không tìm thấy, chương trình terminate với unhandled exception.

## 📐 Cấu trúc / Cú pháp

### Cú pháp throw
```js
throw expression;
// expression có thể là:
throw new Error("message");          // Error object (recommended)
throw new TypeError("wrong type");   // Specific error type
throw "string message";              // String (avoid in production)
throw { code: 400, message: "Bad" }; // Object (avoid)
throw 42;                            // Number (avoid)
```

### Kết hợp với try...catch
```js
function divide(a, b) {
  if (b === 0) throw new Error("divide by zero");
  return a / b;
}

try {
  const result = divide(1, 0);
  console.log(result);
} catch (e) {
  console.log("Lỗi:", e.message); // "Lỗi: divide by zero"
}
```

### Custom Error với constructor
```js
function createError(code, message) {
  const err = new Error(message);
  err.code = code;
  return err;
}
throw createError(400, "Invalid input");
```

## ✅ Điểm mạnh

1. **Dừng sớm, fail-fast**: phát hiện dữ liệu sai thì báo ngay thay vì để lỗi lan xa khó truy vết — giúp debug nhanh hơn nhiều.
2. **Có thể truyền thông tin phong phú** qua Error object: `message` để đọc, `stack` để debug, `name` để giám sát, `code` tùy chỉnh.
3. **Kết hợp tự nhiên với `try...catch` và `finally`** — tạo thành cơ chế xử lý lỗi hoàn chỉnh.
4. **Không giới hạn kiểu throw** — linh hoạt khi cần giao tiếp giữa các phần hệ thống (mặc dù nên throw Error).
5. **Giúp viết helper an toàn**: người dùng hàm nhận được lỗi rõ ràng khi truyền sai tham số — self-documenting API.
6. **Là nền tảng xây dựng hệ thống lỗi nghiệp vụ** — tạo custom Error subclass cho từng loại lỗi business.
7. **Throw có thể dùng ở bất kỳ đâu** — trong hàm, trong callback, trong class constructor, trong module.
8. **Stack trace tự động** — `Error.stack` cho biết chính xác lỗi xảy ra ở file/dòng nào, cuộc gọi từ đâu đến.
9. **Rõ ràng ý đồ** — `throw` báo hiệu "điều này KHÔNG ĐƯỢC xảy ra" — khác với return giá trị lỗi ẩn.
10. **Compatible với mọi environment** — browser và Node.js đều hỗ trợ `throw` và Error objects.

## ⚠️ Bẫy thường gặp & Hạn chế

1. **`throw "string"` / `throw {code}` bị mất thông tin**: không có `stack`, khó biết lỗi từ đâu ra — tránh trong code thật.
   ```js
   // ❌ Khó debug — không biết lỗi từ đâu
   throw "divide by zero";
   // ✅ Dễ debug — có stack trace
   throw new Error("divide by zero");
   ```

2. **Ném ngầm một giá trị không phải Error** khiến `catch(e)` khó nhận biết loại lỗi.
   ```js
   throw 404;
   catch (e) {
     console.log(e.message); // undefined — number không có message!
   }
   ```

3. **`throw` luôn dừng hàm hiện tại** — code phía sau `throw` trong cùng khối không bao giờ chạy.
   ```js
   function example() {
     throw new Error("stop");
     console.log("không bao giờ chạy"); // dead code
   }
   ```

4. **Lỗi `throw` không được bắt** sẽ làm chương trình chết — luôn đi kèm `try...catch` ở tầng phù hợp.
   ```js
   // ❌ Chương trình chết nếu div(1,0) được gọi
   div(1, 0);

   // ✅ An toàn
   try { div(1, 0); } catch (e) { console.log(e.message); }
   ```

5. **Throw trong constructor có thể phá hủy object** — object partially constructed sẽ leak memory.
6. **Throw từ getter/setter** có thể gây khó hiểu cho người dùng API.
7. **Nhiều throw trong cùng một hàm** — khó theo dõi flow, nên gom logic throw vào đầu hàm (guard clause).

## 💡 Khi nào dùng

1. **Kiểm tra dữ liệu đầu vào**: chia cho 0, tham số thiếu, định dạng sai, giá trị ngoài phạm vi.
2. **Xác thực nghiệp vụ**: tài khoản không đủ tiền, sản phẩm hết hàng, quyền truy cập không đủ.
3. **Ném lỗi lập trình viên gọi sai API của hàm thư viện** — self-documenting, giúp developer nhanh chóng sửa lỗi.
4. **Khi cần đưa chương trình về trạng thái báo lỗi rõ ràng** thay vì lỗi mơ hồ (return `-1` hoặc `null`).
5. **Trong constructor** — nếu object không thể khởi tạo hợp lệ, throw lỗi thay vì tạo object half-baked.
6. **Trước khi xử lý dữ liệu không hợp lệ** — guard clause pattern: throw ngay khi phát hiện input sai.
7. **Khi trạng thái hệ thống bất hợp lệ** — invariant violation, state machine ở trạng thái không mong đợi.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Throw cơ bản — chia cho 0 (file `app.js`)
```js
function div(a, b) {
  if (b === 0) throw new Error("divide by zero"); // ném lỗi khi mẫu số = 0
  return a / b;
}

try {
  div(1, 0);
} catch (e) {
  console.log(e.message); // "divide by zero"
}
```

### Ví dụ 2: Throw không có try/catch — program crashes
```js
function div(a, b) {
  if (b === 0) throw new Error("divide by zero");
  return a / b;
}

// Không có try/catch — chương trình dừng
div(1, 0);
// Uncaught Error: divide by zero
//    at div (<anonymous>:3:23)
//    at <anonymous>:7:1
```

### Ví dụ 3: Throw string vs Error object — so sánh thông tin
```js
// Throw string — mất thông tin
try {
  throw "string error";
} catch (e) {
  console.log(typeof e, e.message, e.stack);
  // "string" undefined undefined ← không có stack!
}

// Throw Error — đầy đủ thông tin
try {
  throw new Error("object error");
} catch (e) {
  console.log(typeof e, e.message, e.stack);
  // "object" object error [stack trace...] ← có stack!
}
```

### Ví dụ 4: Throw trong hàm validate
```js
function validateAge(age) {
  if (typeof age !== "number") throw new TypeError("Age must be a number");
  if (age < 0) throw new RangeError("Age cannot be negative");
  if (age > 150) throw new RangeError("Age seems unrealistic");
  return true;
}

try {
  validateAge(-5);
} catch (e) {
  console.log(`${e.name}: ${e.message}`); // "RangeError: Age cannot be negative"
}
```

### Ví dụ 5: Throw với custom error code
```js
function createUser(data) {
  if (!data.name) throw Object.assign(new Error("Name is required"), { code: "ERR_NAME_MISSING" });
  if (!data.email) throw Object.assign(new Error("Email is required"), { code: "ERR_EMAIL_MISSING" });
  return { ...data, id: Date.now() };
}

try {
  createUser({ email: "a@b.com" });
} catch (e) {
  console.log(e.code); // "ERR_NAME_MISSING"
  console.log(e.message); // "Name is required"
}
```

### Ví dụ 6: Guard clause — throw sớm trước khi xử lý
```js
function processOrder(order) {
  // Guard clauses — throw ngay khi phát hiện vấn đề
  if (!order) throw new Error("Order is required");
  if (!Array.isArray(order.items)) throw new TypeError("items must be an array");
  if (order.items.length === 0) throw new Error("Order must have at least one item");
  if (order.total < 0) throw new RangeError("Total cannot be negative");

  // Chỉ chạy khi tất cả guard pass
  return { ...order, processedAt: new Date() };
}
```

### Ví dụ 7: Throw trong class constructor
```js
class BankAccount {
  constructor(initialBalance) {
    if (typeof initialBalance !== "number") {
      throw new TypeError("Initial balance must be a number");
    }
    if (initialBalance < 0) {
      throw new RangeError("Initial balance cannot be negative");
    }
    this.balance = initialBalance;
  }
}

try {
  new BankAccount(-100);
} catch (e) {
  console.log(e.message); // "Initial balance cannot be negative"
}
```

### Ví dụ 8: Rethrow — bắt lỗi rồi ném lại
```js
function riskyOperation() {
  try {
    // code có thể lỗi
    return doSomething();
  } catch (e) {
    console.error("Caught in wrapper:", e.message);
    throw e; // re-throw để caller cũng xử lý được
  }
}
```

### Ví dụ 9: Throw trong callback (phải try/catch trong callback)
```js
function processCallbacks(callbacks) {
  for (const cb of callbacks) {
    try {
      cb(); // nếu cb throw, chỉ ảnh hưởng callback đó
    } catch (e) {
      console.error("Callback error:", e.message);
    }
  }
}
```

### Ví dụ 10: Throw + Error Cause (ES2022)
```js
try {
  try {
    JSON.parse("{ invalid json }");
  } catch (inner) {
    throw new Error("Failed to parse config", { cause: inner });
  }
} catch (outer) {
  console.log(outer.message); // "Failed to parse config"
  console.log(outer.cause.message); // "Unexpected token i in JSON..."
}
```

## 🔬 So sánh với alternatives

| Phương án | Ưu điểm | Nhược điểm | Phù hợp khi |
|---|---|---|---|
| `throw` + `try/catch` | Clear intent, stack trace | Phá vỡ flow nếu không catch | Lỗi quan trọng, cần xử lý đặc biệt |
| Return sentinel value (`null`, `-1`) | Không phá flow, đơn giản |caller phải check every return | API đơn giản, lỗi hiếm |
| Return `{ success, data, error }` | Functional, explicit |Verbose, mỗi nơi phải destruct | Modern APIs, functional style |
| Callback error-first (`(err, data)`) | Node.js convention | Callback hell nếu nested | Legacy Node.js code |
| Promise `.catch()` | Chainable, async-friendly | Chỉ cho async code | Promise-based workflows |
| Result type (thư viện) | Type-safe, explicit | Requires library | Enterprise, FP codebase |

## 📊 Performance & Best Practices

**Performance**: `throw` có overhead nhỏ khi không có lỗi (engine setup exception frame), nhưng đáng kể nếu throw trong vòng lặp tight. Trong 99% trường hợp, overhead này không đáng lo.

**Best practices**:
- Luôn `throw new Error(...)` — không throw string/number/object thông thường.
- Dùng `instanceof` để phân loại lỗi trong `catch`.
- Thêm `code` tùy chỉnh vào Error để dễ xử lý programmatic.
- Dùng **guard clause** — throw sớm, đừng để logic chạy với input sai.
- **Re-throw** lỗi không biết cách xử lý — đừng swallow.
- **Log lỗi** trong `catch` — im lặng吞 lỗi là nguyên nhân số 1 của production bugs.
- Giới hạn **nested try/catch** — tối đa 2层级, quá sâu thì refactor.

## 🔗 Liên kết chéo

- Tổng quan Exceptional Handling: `07_exceptional-handling/README.md` — khái niệm cốt lõi, các loại lỗi chuẩn.
- Try/Catch/Finally: `07_exceptional-handling/02_try-catch-finally/` — thứ tự hoạt động, finally lồng.
- Error Objects: `07_exceptional-handling/03_error-objects/` — TypeError, SyntaxError, RangeError chi tiết.
- Hàm và throw: `09_functions/01_parameters-and-arrow/` — throw lỗi trong hàm khi tham số sai.
- Strict mode: `09_functions/02_scope-closure-strict-mode/01_strict-mode/` — strict mode phát hiện lỗi sớm hơn.
