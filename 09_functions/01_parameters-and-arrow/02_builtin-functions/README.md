# Hàm có sẵn (Built-in Functions) — Thực hành chi tiết — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

**Built-in functions** là **các hàm do JavaScript (hoặc môi trường chạy) cung cấp sẵn**, ta không phải tự viết mà chỉ cần gọi ra dùng. Trong file `app.js`, tác giả liệt kê một số hàm quen thuộc trong môi trường **trình duyệt**:

| Hàm | Công dụng | Browser | Node.js |
|---|---|---|---|
| `alert(message)` | Hiện hộp thoại thông báo | ✅ | ❌ |
| `confirm(question)` | Hỏi Có/Không, trả về `true`/`false` | ✅ | ❌ |
| `prompt(label)` | Ô nhập liệu, trả về chuỗi người dùng nhập | ✅ | ❌ |
| `console.log()` | In ra console (DevTools) | ✅ | ✅ |
| `setTimeout(fn, ms)` | Chạy hàm sau `ms` mili-giây | ✅ | ✅ |
| `clearTimeout(id)` | Hủy timeout đã đăng ký | ✅ | ✅ |
| `setInterval(fn, ms)` | Chạy hàm lặp lại đều đặn | ✅ | ✅ |
| `clearInterval(id)` | Hủy interval đã đăng ký | ✅ | ✅ |

**Phân biệt với Built-in Objects**: nhóm này khác với **Built-in Object** (như `Math`, `JSON`, `Date`) — đó là "đối tượng có sẵn", còn đây là "hàm có sẵn" (functions mà bạn gọi trực tiếp, không cần `.method()`).

Trong `app.js`, tác giả chỉ demo các hàm tương tác trình duyệt ở trên; còn nhóm hàm chuyển kiểu/chuyển mã hay gặp khác như `parseInt`, `parseFloat`, `isNaN`, `isFinite`, `encodeURI`, `eval` cũng là built-in (riêng `eval` hiện khuyến cáo tránh vì chạy mã nguy hiểm).

**Cơ chế bên trong**: built-in functions được implement bởi JavaScript engine (V8, SpiderMonkey...) ở cấp độ native code — chạy nhanh hơn nhiều so với JavaScript code thuần. Chúng là cầu nối giữa JS runtime và môi trường (browser DOM, Node.js OS API).

## 📐 Cấu trúc / Cú pháp

### Dialog functions (chỉ trong browser)
```js
alert("Thông báo");                    // popup với nút OK
const result = confirm("Xác nhận?");   // popup Có/Không → true/false
const input = prompt("Nhập tên:");     // popup nhập liệu → string/null
```

### Console functions
```js
console.log("value");           // in ra console
console.warn("warning message"); // in cảnh báo (màu vàng)
console.error("error message");  // in lỗi (màu đỏ)
console.table([{a:1}, {a:2}]);   // in bảng
console.time("label");          // bắt timer
console.timeEnd("label");       // kết thúc timer, in elapsed ms
```

### Timer functions
```js
// setTimeout — chạy 1 lần sau ms milliseconds
const timerId = setTimeout(() => console.log("hi"), 1000);
clearTimeout(timerId); // hủy trước khi chạy

// setInterval — chạy lặp lại mỗi ms milliseconds
const intervalId = setInterval(() => console.log("tick"), 1000);
clearInterval(intervalId); // hủy
```

### Type conversion functions
```js
parseInt("42px");     // 42 — cắt đến ký tự không phải số
parseFloat("3.14a");  // 3.14
isNaN("abc");         // true — ép kiểu ngầm!
Number.isNaN("abc");  // false — không ép kiểu, chính xác hơn
isFinite(Infinity);   // false
encodeURI("a b");     // "a%20b" — encode space
decodeURI("a%20b");   // "a b"
```

### Eval (TRÁNH DÙNG)
```js
// ❌ Nguy hiểm — chạy arbitrary code, slow, security risk
eval("return 2 + 2");

// ✅ Thay thế
new Function("return 2 + 2")(); // tương đương nhưng vẫn không nên dùng
```

## ✅ Điểm mạnh

1. **Tiết kiệm thời gian**: không phải tự dựng các chức năng hệ thống — dùng thẳng.
2. **`setTimeout`/`setInterval` giúp làm quen với bất đồng bộ** — nền tảng của JS event loop.
3. **`confirm`/`prompt` giúp tương tác người dùng** mà không cần xây UI phức tạp — prototype nhanh.
4. **Chạy demo trong trình duyệt** thấy kết quả ngay và trực quan — học qua quan sát.
5. **Liệt kê rõ từng hàm kèm tác vụ** — dễ học từng cái, tra cứu nhanh.
6. **`console.*` methods** — công cụ debug mạnh mẽ: `log`, `table`, `time`, `assert`, `trace`.
7. **Parser functions** (`parseInt`, `parseFloat`) — xử lý input từ form HTML rất phổ biến.
8. **URI functions** (`encodeURI`, `decodeURI`) — xử lý URL parameters, query strings.
9. **Native implementation** — chạy nhanh hơn JavaScript equivalent vì được implement ở C++ level.
10. **Cross-environment** (trừ dialog functions) — `console.log`, `setTimeout` hoạt động cả browser và Node.js.

## ⚠️ Bẫy thường gặp & Hạn chế

1. **`alert`, `confirm`, `prompt` chỉ chạy trong trình duyệt** — dùng trong Node.js sẽ lỗi (`ReferenceError: alert is not defined`).
   ```js
   // Node.js
   alert("hi"); // ReferenceError: alert is not defined
   ```

2. **`alert`/`confirm` chặn luồng chạy** (blocking) — không nên lạm dụng trong sản phẩm thật.
   ```js
   alert("hello"); // ⬇️ UI đóng băng cho đến khi user click OK
   console.log("world"); // KHÔNG chạy cho đến khi đóng alert
   ```

3. **`setTimeout(fn, ms)` thời gian thực thi không chính xác tuyệt đối** — bị độ trễ, phụ thuộc event loop và load của browser.
   ```js
   setTimeout(() => console.log("hi"), 0);
   // Có thể chạy sau 10ms, 50ms, hoặc حتی 100ms tùy browser load
   ```

4. **`eval` chạy mã động cực kỳ nguy hiểm** (code injection) và chậm — hạn chế tối đa.
   ```js
   // ❌ Nguy hiểm
   eval(userInput); // user có thể inject arbitrary code!
   // ✅ Thay thế
   const safeResult = JSON.parse(userInput); // chỉ parse JSON
   ```

5. **`isNaN("abc")` cũng trả `true`** do ép kiểu ngầm — nếu muốn kiểm tra chặt, dùng `Number.isNaN`.
   ```js
   isNaN("abc");       // true  — "abc" → NaN
   Number.isNaN("abc"); // false — không ép kiểu, "abc" là string
   isNaN(NaN);         // true
   Number.isNaN(NaN);  // true
   ```

6. **`parseInt` với radix** — không truyền radix có thể parse nhầm số octal trong older browsers.
   ```js
   parseInt("010");     // 8 (octal) trong IE, 10 trong modern browsers
   parseInt("010", 10); // 10 — luôn đúng, truyền radix rõ ràng
   ```

7. **`clearTimeout`/`clearInterval` cần lưu ID** — không clear được nếu không giữ reference.
   ```js
   setTimeout(() => {}, 1000);
   // Không clear được — quên lưu ID!
   const id = setTimeout(() => {}, 1000);
   clearTimeout(id); // ✅
   ```

8. **Callback trong setTimeout bị mất `this`** — dùng arrow function hoặc `.bind()`.
   ```js
   const obj = {
     name: "Sơn",
     sayName() {
       setTimeout(function() { console.log(this.name); }, 100);
       // ❌ this === window, in undefined
     }
   };
   // ✅ Sửa
   sayName() {
     setTimeout(() => console.log(this.name), 100);
   }
   ```

## 💡 Khi nào dùng

1. **Gửi thông báo/tương tác đơn giản** với người dùng — bản demo, prototype, admin panel.
2. **Hẹn giờ chạy tác vụ một lần** (`setTimeout`) — delay action, animation timing, debounce.
3. **Chạy tác vụ định kỳ** (`setInterval`) — polling data, countdown timer, game loop.
4. **Parse số từ chuỗi input**: `parseInt`, `parseFloat` — xử lý form input, URL params.
5. **Kiểm tra số hữu hạn/an toàn** với `isFinite`, `Number.isNaN` (bản chặt).
6. **Mã hóa URL** khi truyền tham số: `encodeURI`, `encodeURIComponent`.
7. **Debug với console** — `console.log`, `console.table`, `console.time` cho performance profiling.
8. **Inline JS trong HTML** — `href="javascript:void(0)"` dùng `void` để tránh navigate.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Dialog functions (file `app.js`)
```js
// Chỉ chạy trong browser
alert("Xin chào đến với website!");
const approved = confirm("Xác nhận đã đủ 18 tuổi?");
console.log("User confirmed:", approved); // true / false

const name = prompt("Nhập tên của bạn:");
console.log("Hello,", name); // trả về chuỗi nhập vào, hoặc null nếu cancel
```

### Ví dụ 2: setTimeout và clearTimeout
```js
// Chạy sau 1 giây
const timerId = setTimeout(() => {
  console.log("setTimeout fired!");
}, 1000);

// Hủy trước khi chạy
// clearTimeout(timerId);

// setTimeout không chính xác — có thể chậm hơn ms quy định
setTimeout(() => console.log("delayed"), 0); // có thể chạy sau 10-50ms
```

### Ví dụ 3: setInterval và clearInterval
```js
let count = 0;
const intervalId = setInterval(() => {
  count++;
  console.log(`Tick ${count}`);
  if (count >= 5) {
    clearInterval(intervalId); // dừng sau 5 lần
    console.log("Stopped!");
  }
}, 1000);
// Tick 1 (after 1s)
// Tick 2 (after 2s)
// ...
// Tick 5 (after 5s)
// "Stopped!"
```

### Ví dụ 4: Parse functions — xử lý input form
```js
// parseInt — cắt đến ký tự đầu không phải số
console.log(parseInt("42px"));     // 42
console.log(parseInt("42.5px"));   // 42 — cắt phần thập phân
console.log(parseInt("abc42"));    // NaN — không bắt đầu bằng số
console.log(parseInt("  42  "));   // 42 — ignore whitespace

// Truyền radix rõ ràng
console.log(parseInt("1010", 2));  // 10 — binary
console.log(parseInt("ff", 16));   // 255 — hexadecimal
console.log(parseInt("010", 10));  // 10 — explicit decimal (avoid octal)

// parseFloat — giữ phần thập phân
console.log(parseFloat("3.14em")); // 3.14
console.log(parseFloat("2.5px"));  // 2.5
```

### Ví dụ 5: NaN and Finite checks
```js
// isNaN (deprecated) — ép kiểu ngầm
console.log(isNaN("abc"));    // true  — "abc" → NaN
console.log(isNaN(null));     // false — null → 0
console.log(isNaN(undefined)); // true  — undefined → NaN

// Number.isNaN — không ép kiểu, chính xác hơn
console.log(Number.isNaN("abc"));  // false
console.log(Number.isNaN(NaN));    // true
console.log(Number.isNaN(undefined)); // false

// isFinite — kiểm tra số hữu hạn
console.log(isFinite(42));      // true
console.log(isFinite(Infinity)); // false
console.log(isFinite("abc"));   // false — ép kiểu: "abc" → NaN → false
console.log(isFinite(null));    // true — null → 0

// Number.isFinite — không ép kiểu
console.log(Number.isFinite("abc")); // false
console.log(Number.isFinite(42));    // true
```

### Ví dụ 6: URI encoding
```js
// encodeURI — encode toàn bộ URL (không encode special chars như : / ? & =)
const url = "https://example.com/search?q=hello world&lang=vi";
console.log(encodeURI(url));
// "https://example.com/search?q=hello%20world&lang=vi"

// encodeURIComponent — encode ALL special chars (dùng cho query value)
console.log(encodeURIComponent("hello world")); // "hello%20world"
console.log(encodeURIComponent("a=b&c=d"));     // "a%3Db%26c%3Dd"

// Decode
console.log(decodeURI("https://example.com/search?q=hello%20world"));
// "https://example.com/search?q=hello world"
console.log(decodeURIComponent("hello%20world")); // "hello world"
```

### Ví dụ 7: Console methods — debug tools
```js
// Basic logging
console.log("Normal log");
console.warn("Warning message"); // màu vàng trong DevTools
console.error("Error message");  // màu đỏ trong DevTools

// Table display
console.table([{ name: "Sơn", age: 18 }, { name: "An", age: 20 }]);
// ┌─────────┬────────┬──────┐
// │ (index) │ name   │ age  │
// ├─────────┼────────┼──────┤
// │    0    │ "Sơn"  │  18  │
// │    1    │ "An"   │  20  │
// └─────────┴────────┴──────┘

// Timer for performance
console.time("operation");
for (let i = 0; i < 1000000; i++) {}
console.timeEnd("operation"); // "operation: 5.234ms"

// Assert — throw nếu condition false
console.assert(1 + 1 === 2, "Math is broken!"); // không in gì
console.assert(1 + 1 === 3, "Math is broken!"); // throw AssertionError
```

### Ví dụ 8: setTimeout với arrow function giữ this
```js
const counter = {
  count: 0,
  increment() {
    setTimeout(() => {
      this.count++; // arrow giữ this của increment()
      console.log(this.count);
    }, 100);
  }
};
counter.increment(); // 1 (after 100ms)

// ❌ Nếu dùng regular function — this === window
const badCounter = {
  count: 0,
  increment() {
    setTimeout(function() {
      this.count++; // this === window, không phải badCounter
      console.log(this.count); // NaN hoặc undefined
    }, 100);
  }
};
```

### Ví dụ 9: Debounce pattern với setTimeout
```js
function debounce(fn, delay) {
  let timerId;
  return function(...args) {
    clearTimeout(timerId); // hủy timeout cũ
    timerId = setTimeout(() => {
      fn.apply(this, args); // gọi sau delay ms
    }, delay);
  };
}

// Ứng dụng: search input — chỉ gọi API sau khi ngưng gõ 300ms
const searchInput = document.querySelector("#search");
const debouncedSearch = debounce((query) => {
  console.log("Searching for:", query);
  // fetch(`/api/search?q=${query}`)
}, 300);
searchInput.addEventListener("input", (e) => debouncedSearch(e.target.value));
```

### Ví dụ 10: Promise-based wrapper cho setTimeout
```js
// Wrap setTimeout thành Promise — dễ chain hơn
function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// Usage
async function main() {
  console.log("Start");
  await delay(1000);
  console.log("After 1 second");
  await delay(500);
  console.log("After 1.5 seconds total");
}
main();
```

## 🔬 So sánh với alternatives

| Phương án | Ưu điểm | Nhược điểm | Phù hợp khi |
|---|---|---|---|
| `setTimeout` | Native, đơn giản | Blocking dialog, approximate timing | Simple delay |
| `setInterval` | Lặp lại tự động | Cần clear thủ công, drift over time | Periodic tasks |
| `requestAnimationFrame` | Sync với screen refresh | Chỉ 60fps max, browser only | Animations |
| Web Workers | Background thread | Complex communication | CPU-heavy tasks |
| `async/await` + Promise | Clean syntax | Requires Promise wrapper | Modern async code |
| `setImmediate` (Node) | Chạy ngay sau event loop | Node.js only | Node-specific timing |

## 📊 Performance & Best Practices

**Performance**:
- `setTimeout(fn, 0)` KHÔNG chạy ngay — mindestens chờ đến lần event loop tiếp theo (~4ms+).
- `setInterval` có **drift** — khoảng cách thực tế giữa các lần chạy có thể lớn hơn ms quy định nếu main thread bận.
- Dùng `requestAnimationFrame` thay `setInterval` cho animation — sync với monitor refresh rate (60fps).
- `console.log` trong vòng lặp tight có thể làm chậm đáng kể — dùng `console.time` thay thế cho benchmark.

**Best practices**:
- **Luôn lưu timer ID** để có thể `clearTimeout`/`clearInterval` khi không cần.
- **Dùng arrow function** trong setTimeout để giữ `this` context.
- **Tránh `setInterval` cho animation** — dùng `requestAnimationFrame` thay thế.
- **Tránh `alert`/`confirm`/`prompt`** trong production — dùng custom modal/toast.
- **Tránh `eval()` hoàn toàn** — security risk, performance penalty.
- **Dùng `Number.isNaN`** thay `isNaN` — không ép kiểu, chính xác hơn.
- **Luôn truyền radix** cho `parseInt`: `parseInt(str, 10)`.
- **Dùng `encodeURIComponent`** cho query values, `encodeURI` cho toàn bộ URL.
- **Dọn dẹp timer** khi component unmount (React) hoặc page unload — tránh memory leak.
- ** debounce/throttle** cho input events — giảm frequency của handler calls.

**Quy tắc "3 nên — 3 không"**:
- ✅ Nên dùng arrow function trong setTimeout để giữ `this`.
- ✅ Nên lưu timer ID và clear khi không cần.
- ✅ Nên dùng `Number.isNaN` thay `isNaN`.
- ❌ Không nên dùng `alert`/`confirm`/`prompt` trong production.
- ❌ Không nên dùng `eval()` — security risk.
- ❌ Không nên dùng `setInterval` cho animation — dùng `requestAnimationFrame`.

## 🔗 Liên kết chéo

- Tổng quan Functions: `09_functions/README.md` — khái niệm hàm, first-class citizens.
- Callbacks: `09_functions/01_parameters-and-arrow/01_callbacks/` — callback pattern foundation.
- Arrow functions: `09_functions/01_parameters-and-arrow/03_arrow-functions/` — arrow trong setTimeout.
- Recursion: `09_functions/01_parameters-and-arrow/04_recursion/` — recursive setTimeout pattern.
- Non-blocking I/O: `09_functions/02_scope-closure-strict-mode/04_non-blocking-io/` — async concept behind timers.
- Operators: `08_expressions-and-operators/01_operators/` — toán tử trong built-in function args.
- Expressions: `08_expressions-and-operators/06_string-operators/` — string ops với prompt/confirm results.
- Control flow: `06_control-flow/01_conditionals/5_condition/1_if.js` — if/else với confirm result.
