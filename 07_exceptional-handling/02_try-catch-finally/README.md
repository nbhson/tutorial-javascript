# try / catch / finally — Thực hành chi tiết — [Level: Intermediate]

## 🔑 Khái niệm cốt lõi

`try...catch...finally` là cấu trúc **bắt và xử lý lỗi** trong JavaScript. Cơ chế hoạt động như sau:

- **`try`** — khối code có thể gây lỗi, JavaScript "thử" chạy nó.
- **`catch`** — chỉ chạy khi có lỗi được ném trong `try`; nhận tham số là giá trị bị ném (thường là Error object).
- **`finally`** — **luôn luôn chạy**, bất kể thành công hay thất bại, kể cả khi có `return` hoặc `throw` trong `try`/`catch`.

```js
try {
  riskyOperation(); // code có thể ném lỗi
} catch (error) {
  handleError(error); // chạy nếu có lỗi
} finally {
  cleanup(); // luôn chạy, thường để dọn dẹp
}
```

**Hai quy tắc cốt lõi** được minh họa trong `app.js`:

1. **`finally` luôn chạy** — kể cả khi `try` ném lỗi và `catch` xử lý xong.
2. **`finally` lồng nhau** — cấp trong chạy trước, rồi lỗi mới được cấp ngoài bắt.

Ví dụ trong `app.js`:
```js
try { risky(); }
catch (e) { console.log("catch", e.message); }
finally { console.log("finally"); }
// Kết quả: "catch fail" → "finally"
```

**Thứ tự thực thi** chi tiết:
1. Chạy code trong `try`.
2. Nếu có lỗi → nhảy ngay đến `catch` (bỏ qua phần còn lại của `try`).
3. Sau `catch` (hoặc sau `try` nếu không lỗi) → chạy `finally`.
4. Nếu `catch` có `return`/`throw` → `finally` vẫn chạy trước khi thoát hàm.
5. Nếu `finally` có `return`/`throw` → nó **override** kết quả từ `try`/`catch`.

## 📐 Cấu trúc / Cú pháp

### Cú pháp cơ bản
```js
try {
  // code có thể ném lỗi
} catch (error) {
  // xử lý lỗi — error là giá trị bị throw
} finally {
  // luôn chạy — dọn dẹp
}
```

### Cú pháp không có catch (ES2019+)
```js
try {
  riskyOperation();
} finally {
  cleanup(); // vẫn chạy dù không có catch
}
```
ES2019 cho phép `try...finally` mà không cần `catch` — hữu ích khi chỉ cần dọn dẹp.

### Catch không tham số (ES2019)
```js
try {
  riskyOperation();
} catch {
  // bỏ qua tên parameter khi không cần dùng
  handleError();
} finally {
  cleanup();
}
```

### Return trong try/catch/finally — thứ tự ưu tiên
```js
function example() {
  try {
    return "from try";
  } catch (e) {
    return "from catch";
  } finally {
    console.log("from finally"); // vẫn chạy trước khi return
    // return "from finally";   // nếu có return ở đây → override tất cả
  }
}
console.log(example());
// "from finally"
// "from try"
```

### Nested try/catch
```js
try {
  try {
    throw new Error("inner");
  } finally {
    console.log("inner finally"); // chạy trước
  }
} catch (e) {
  console.log("outer catch", e.message); // chạy sau
}
// Kết quả: "inner finally" → "outer catch inner"
```

## ✅ Điểm mạnh

1. **An toàn tuyệt đối cho tài nguyên**: dọn dẹp bằng `finally` không bao giờ bị bỏ sót — connection, timer, lock đều được giải phóng.
2. **Riêng `catch` có thể bỏ tham số** (ES2019) khi chỉ cần `finally` để xử lý hậu kỳ — code gọn hơn.
3. **Nhiều khối `try...catch` lồng nhau** giúp xử lý lỗi theo từng tầng trách nhiệm — mỗi tầng catch lỗi của riêng mình.
4. **Lỗi được bắt đúng chỗ** — chương trình tiếp tục chạy phần còn lại thay vì dừng hẳn.
5. **Phân tách rõ ba giai đoạn**: chạy thử / xử lý lỗi / dọn dẹp — code có cấu trúc, dễ đọc.
6. **`finally` override bởi return trong finally** — cơ chế đảm bảo cleanup luôn xảy ra trước khi hàm kết thúc.
7. **Catch error object có `stack` trace** — debug dễ dàng, biết chính xác lỗi từ đâu đến.
8. **Kết hợp được với async** — `async/await` + `try/catch` cho code bất đồng bộ sạch sẽ.
9. **Có thể re-throw** — bắt lỗi, xử lý một phần, rồi ném lại cho tầng cao hơn.
10. **ES2022 Error cause** — `new Error("msg", { cause: innerError })` giữ lại chain lỗi.

## ⚠️ Bẫy thường gặp & Hạn chế

1. **Chỉ bắt được lỗi đồng bộ trong `try`** — lỗi bên trong callback, `setTimeout`, promise không bị bắt trực tiếp.
   ```js
   try {
     setTimeout(() => { throw new Error("async"); }, 0);
   } catch (e) {
     // KHÔNG chạy — lỗi async nằm ngoài try
   }
   ```

2. **Nếu `finally` tự ném lỗi, lỗi đó sẽ che lỗi gốc của `try`** — khó debug vì mất stack trace ban đầu.
   ```js
   try {
     throw new Error("nguồn");
   } finally {
     throw new Error("finally"); // override "nguồn"
   }
   // Uncaught Error: finally
   ```

3. **`return` trong `try` không ngăn được `finally` chạy** — nhưng giá trị return của `try` vẫn được giữ (trừ khi finally có return).
   ```js
   try { return 42; } finally { console.log("cleanup"); }
   // In: "cleanup" rồi return 42
   ```

4. **Quá nhiều `try...catch` lồng nhau** làm code khó theo dõi — hãy để lỗi "nổi lên" tầng xử lý cao nhất.
   ```js
   // ❌ Nest quá sâu
   try { try { try { risky(); } catch(e1) {} } catch(e2) {} } catch(e3) {}
   // ✅ Một tầng catch ở nơi phù hợp
   ```

5. **Swallow lỗi im lặng** — `catch` không log không re-throw khiến bug khó phát hiện trong production.
   ```js
   try {
     dangerousCode();
   } catch (e) {
     // Im lặngnuốt lỗi — rất tệ!
   }
   ```

6. **Catch quá rộng** — bắt mọi lỗi chung chung thay vì phân biệt `instanceof`.
   ```js
   // ❌ Bắt mọi lỗi, kể cả lỗi không mong đợi
   catch (e) { console.log("error"); }
   // ✅ Phân biệt và re-throw lỗi không biết xử lý
   catch (e) {
     if (e instanceof NetworkError) handleNetwork(e);
     else throw e;
   }
   ```

## 💡 Khi nào dùng

1. **Gọi API, đọc file, thao tác localStorage** — dễ lỗi mạng/lỗi dữ liệu, cần fallback an toàn.
2. **Đóng tài nguyên bắt buộc** — xóa loading spinner, đóng modal, xóa timers, ngắt kết nối DB — đặt ở `finally`.
3. **Xử lý JSON chưa chắc hợp lệ** — `JSON.parse` dễ ném `SyntaxError` với input xấu.
4. **Chuyển lỗi hệ thống thành thông báo thân thiện** với người dùng — catch và hiển thị toast.
5. **Retry logic** — catch lỗi network, thử lại N lần trước khi báo failure.
6. **Transaction/database** — commit nếu OK, rollback nếu có lỗi, always close connection in finally.
7. **File I/O trong Node.js** — đọc/ghi file có thể fail, cần catch và cleanup handle.
8. **Eval/Function constructor** — parse code động dễ throw SyntaxError.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Try/Catch/Finally cơ bản (file `app.js`)
```js
function risky() {
  throw new Error("fail");
}

try {
  risky();
} catch (e) {
  console.log("catch", e.message); // "catch fail"
} finally {
  console.log("finally");          // "finally" — luôn in ra
}
```

### Ví dụ 2: Finally lồng trong Finally (file `app.js`)
```js
try {
  try {
    throw new Error("inner");
  } finally {
    console.log("inner finally");  // chạy trước — finally luôn chạy
  }
} catch (e) {
  console.log("outer catch");      // chạy sau — lỗi inner được nổi lên
}
// Kết quả: "inner finally" → "outer catch"
```

### Ví dụ 3: Return trong try, finally vẫn chạy
```js
function example() {
  try {
    return "from try";
  } catch (e) {
    return "from catch";
  } finally {
    console.log("finally block"); // in ra trước khi return
  }
}
console.log(example());
// "finally block"
// "from try"
```

### Ví dụ 4: Finally có return — override try/catch return
```js
function example2() {
  try {
    return "from try";
  } finally {
    return "from finally"; // override tất cả return khác
  }
}
console.log(example2()); // "from finally"
```

### Ví dụ 5: JSON.parse với fallback
```js
function parseConfig(raw) {
  try {
    return JSON.parse(raw);
  } catch (e) {
    console.warn("Invalid JSON, using defaults");
    return { version: "1.0", debug: false };
  } finally {
    console.log("Config parsed (or defaulted)"); // luôn chạy
  }
}
console.log(parseConfig("{ bad json }"));
// "Invalid JSON, using defaults"
// "Config parsed (or defaulted)"
// { version: "1.0", debug: false }
```

### Ví dụ 6: Database transaction pattern
```js
function transferMoney(from, to, amount) {
  const conn = openConnection();
  try {
    conn.execute(`UPDATE accounts SET balance = balance - ${amount} WHERE id = ${from}`);
    conn.execute(`UPDATE accounts SET balance = balance + ${amount} WHERE id = ${to}`);
    conn.commit();
    return { success: true };
  } catch (e) {
    conn.rollback(); // rollback nếu có lỗi
    throw new Error(`Transfer failed: ${e.message}`);
  } finally {
    conn.close(); // luôn đóng connection
  }
}
```

### Ví dụ 7: Retry với exponential backoff
```js
async function fetchWithRetry(url, retries = 3, delay = 1000) {
  for (let i = 0; i < retries; i++) {
    try {
      const res = await fetch(url);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return await res.json();
    } catch (e) {
      if (i === retries - 1) throw e; // lần cuối — re-throw
      console.log(`Retry ${i + 1}/${retries} in ${delay}ms...`);
      await new Promise(r => setTimeout(r, delay * (i + 1)));
    }
  }
}
```

### Ví dụ 8: ES2019 — catch không tham số
```js
try {
  riskyOperation();
} catch {
  // Không cần (e) vì không dùng error object
  handleError();
} finally {
  cleanup();
}
```

### Ví dụ 9: Multiple catch tiers — phân loại lỗi
```js
try {
  processData(input);
} catch (e) {
  if (e instanceof TypeError) {
    console.error("Sai kiểu dữ liệu:", e.message);
  } else if (e instanceof RangeError) {
    console.error("Giá trị ngoài phạm vi:", e.message);
  } else if (e instanceof SyntaxError) {
    console.error("Lỗi cú pháp:", e.message);
  } else {
    throw e; // re-throw lỗi không biết cách xử lý
  }
} finally {
  console.log("Processing attempt finished");
}
```

### Ví dụ 10: finally luôn chạy dù có return sớm
```js
function processWithCleanup(data) {
  let resource;
  try {
    resource = acquireResource();
    if (!data) return null; // return sớm trong try
    return transform(resource, data);
  } catch (e) {
    console.error("Error:", e.message);
    return null;
  } finally {
    if (resource) releaseResource(resource); // vẫn chạy dù return sớm
  }
}
```

## 🔬 So sánh với alternatives

| Phương án | Ưu điểm | Nhược điểm | Phù hợp khi |
|---|---|---|---|
| `try...catch...finally` | Cấu trúc rõ, luôn cleanup | Chỉ bắt sync error | Lỗi có thể dự đoán, cần fallback |
| `if` guard + return | Đơn giản, không overhead | Dễ bỏ sót check | Validation đơn giản |
| Promise `.catch()` | Async-friendly, chainable | Chỉ cho promise | Async code, fetch, DB |
| `async/await` + try/catch | Code đồng bộ-like | Tương tự try/catch | Modern async |
| Result type (thư viện) | Type-safe, explicit | Cần thư viện | Enterprise, FP |

## 📊 Performance & Best Practices

**Performance**: `try...catch` có overhead nhỏ (~10-20%) ngay cả khi không có lỗi — engine phải setup exception handling frame. Trong **vòng lặp tight** (>100k iter), dùng **guard clause** thay thế.

**Best practices**:
- Luôn log lỗi trong `catch` — đừng swallow im lặng.
- Dùng `instanceof` để phân biệt loại lỗi.
- **Re-throw** lỗi không biết xử lý — đừng bắt mọi thứ.
- Dùng `finally` cho **dọn dẹp bắt buộc** (close connection, release lock, clear timer).
- Giới hạn **nested try/catch** — tối đa 2 cấp.
- Dùng **ES2019 `catch` không parameter** khi không cần error object.
- Dùng **Error cause** (ES2022) để giữ chain lỗi: `new Error("wrapper", { cause: inner })`.
- Tránh **throw trong finally** — sẽ che lấp lỗi gốc.

**Quy tắc "3 nên — 3 không"**:
- ✅ Nên log lỗi trong catch.
- ✅ Nên có finally khi cần cleanup.
- ✅ Nên phân loại lỗi bằng instanceof.
- ❌ Không swallow lỗi im lặng.
- ❌ Không nest quá 2 cấp.
- ❌ Không throw trong finally.

## 🔗 Liên kết chéo

- Throw lỗi: `07_exceptional-handling/01_throw/` — cách dùng `throw` đúng chuẩn.
- Error objects: `07_exceptional-handling/03_error-objects/` — TypeError, SyntaxError, RangeError.
- Tổng quan Exceptional Handling: `07_exceptional-handling/README.md` — khái niệm cốt lõi.
- Hàm và throw: `09_functions/01_parameters-and-arrow/` — throw lỗi trong hàm.
- Non-blocking I/O: `09_functions/02_scope-closure-strict-mode/04_non-blocking-io/` — lỗi async không bị bắt bởi synchronous try/catch.
- Arrow functions: `09_functions/01_parameters-and-arrow/03_arrow-functions/` — arrow trong try/catch context.
