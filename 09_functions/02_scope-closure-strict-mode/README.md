# Hàm — Phạm vi, Closure, Strict Mode — [Level: Intermediate]

## 🔑 Khái niệm cốt lõi

Nhóm này đi sâu vào **vòng đời và phạm vi của hàm** — trả lời các câu hỏi: biến tồn tại ở đâu, hàm nhớ được gì, chương trình chạy theo thứ tự nào. Đây là phần **nền tảng quan trọng nhất** để hiểu các khái niệm nâng cao: `this`, event loop, module, hooks (React).

Cụ thể 5 thư mục con:

| Thư mục | Nội dung | File chính |
|---|---|---|
| `01_strict-mode/` | Chế độ nghiêm ngặt `"use strict"` — gắt gao hơn, an toàn hơn | `app.js` + `index.html` |
| `02_iife/` | IIFE — hàm được gọi ngay lập tức, mang tính "private" | `app.js` + `index.html` |
| `03_closure/` | Closure — hàm nhớ biến của phạm vi bên ngoài khi đã tạo | `app.js` + `index.html` |
| `04_non-blocking-io/` | Lý thuyết: cách JavaScript xử lý bất đồng bộ, không chặn luồng | README only |
| `05_function-stack/` | Call stack (ngăn xếp gọi hàm) và scope chain | `app.js` + `index.html` |

**Mối quan hệ giữa các khái niệm**:
- **Strict mode** → enforce rules chặt chẽ hơn, prevent silent errors.
- **IIFE** → tạo private scope, precursor của ES modules.
- **Closure** → hàm "nhớ" scope ngoài, nền tảng của IIFE pattern.
- **Call stack** → cơ chế thực thi hàm, giải thích stack overflow.
- **Non-blocking I/O** → event loop, tại sao setTimeout không chặn main thread.

Hiểu closure và scope chain, bạn sẽ hiểu tại sao mảng/object bị "giữ tham chiếu", tại sao IIFE tồn tại, và vì sao cần `"use strict"`.

## 📐 Cấu trúc / Cú pháp

### Strict Mode
```js
"use strict"; // bật strict mode cho toàn file

// Hoặc trong hàm
function myFunc() {
  "use strict"; // chỉ áp dụng trong hàm này
}
```

### IIFE (Immediately Invoked Function Expression)
```js
// Basic IIFE
(function() {
  const privateVar = 42;
  console.log(privateVar); // 42
})();

// IIFE với params
(function(greeting) {
  console.log(greeting, "world"); // "hello world"
})("hello");

// IIFE trả về object (module pattern)
const module = (function() {
  let count = 0;
  return {
    increment: () => ++count,
    getCount: () => count
  };
})();
```

### Closure
```js
function createCounter() {
  let count = 0; // biến "bị giữ lại" bởi closure
  return function() {
    return ++count; // hàm con nhớ count từ scope ngoài
  };
}
const counter = createCounter();
console.log(counter()); // 1
console.log(counter()); // 2
```

### Call Stack
```js
function a() { b(); }
function b() { c(); }
function c() { console.trace(); }
a();
// Call stack: a → b → c (push), c → b → a (pop)
```

### Scope Chain
```js
let globalVar = "global";
function outer() {
  let outerVar = "outer";
  function inner() {
    console.log(globalVar, outerVar); // tìm qua scope chain
  }
  inner();
}
outer(); // "global" "outer"
```

## ✅ Điểm mạnh

1. **Bóc tách đúng những khái niệm người phỏng vấn thường hỏi**: closure, IIFE, call stack, strict mode — nắm vững = tự tin interview.
2. **Lý thuyết (non-blocking I/O) kết hợp thực hành** (strict mode, IIFE, closure, function stack) — hiểu cả concept lẫn code.
3. **Mỗi thư mục con có ví dụ chạy ngay được** — `node app.js` hoặc mở `index.html` trên browser.
4. **Các ví dụ theo tình huống thật**: module "private" bằng IIFE, biến đếm bằng closure, `console.trace()` xem call stack.
5. **Có tài liệu tham khảo về quản lý bộ nhớ** (thất thoát bộ nhớ do closure) trong `03_closure` — kiến thức production-ready.
6. **Kết nối tốt với phần callbacks/async** — tạo cây kiến thức mạch lạc, không rời rạc.
7. **Strict mode phát hiện lỗi sớm** — prevent silent bugs như biến toàn cục vô ý, gán readonly.
8. **IIFE là tiền thân của ES modules** — hiểu IIFE = hiểu tại sao module system ra đời.
9. **Closure là nền tảng của React hooks** — `useState`, `useEffect` về bản chất là closure pattern.
10. **Call stack + scope chain** — hiểu tại sao code chạy theo thứ tự nào, biến tìm thấy ở đâu — debug skill quan trọng.

## ⚠️ Bẫy thường gặp & Hạn chế

1. **Closure giữ tham chiếu biến nên không được dọn** — có thể gây memory leak nếu không kiểm soát.
   ```js
   function processData(data) {
     const result = heavyComputation(data);
     return () => result; // closure giữ result — result không bao giờ GC'd
   }
   ```

2. **IIFE phải có dấu `;` trước đó** — nếu dòng trước kết thúc bằng biểu thức (tự động chèn `;` bị bỏ qua), dễ gây lỗi ghép hai câu lệnh.
   ```js
   const x = 1
   (function() { console.log("iife"); })();
   // ❌ Có thể lỗi nếu engine không tự chèn ;
   // ✅ Luôn có ; trước IIFE
   const x = 1;
   (function() { console.log("iife"); })();
   ```

3. **Strict mode áp dụng cho toàn file hoặc toàn hàm** — khai báo giữa chừng sẽ không có tác dụng với phần trước.
   ```js
   console.log("non-strict"); // không bị kiểm tra
   "use strict"; // quá muộn cho dòng trên
   x = 100; // vẫn chạy được ở non-strict part
   ```

4. **`04_non-blocking-io` chỉ có lý thuyết** (không có file code) — nên tự tìm thêm demo event loop.
5. **Call stack có giới hạn độ sâu** — đệ quy không kiểm soát sẽ "tràn ngăn xếp".
6. **Closure trong vòng lặp** — biến bị share across iterations nếu dùng `var` thay `let`.
   ```js
   // ❌ Bug kinh điển
   for (var i = 0; i < 3; i++) {
     setTimeout(() => console.log(i), 100); // in 3 3 3
   }
   // ✅ Sửa bằng let
   for (let i = 0; i < 3; i++) {
     setTimeout(() => console.log(i), 100); // in 0 1 2
   }
   ```
7. **IIFE không giải quyết hoàn toàn việc chia module lớn** — hiện đại nên dùng ES modules (`import`/`export`).
8. **Strict mode có thể "vỡ" code cũ** — viết theo kiểu "xả láng" sẽ gặp lỗi khi bật strict.

## 💡 Khi nào dùng

1. **Bọc code riêng tư, tránh xung đột biến toàn cục** → IIFE (trong code legacy không có module).
2. **Tạo biến "nhớ" trạng thái giữa các lần gọi** (counter, memoized function, hooks) → closure.
3. **Bật `"use strict"` cho script/module mới** — thói quen tốt mặc định, prevent silent bugs.
4. **Hiệu thứ tự chạy và độ sâu của lời gọi hàm** khi debug stack trace → call stack.
5. **Nắm bắt bản chất bất đồng bộ của JS** khi làm việc với timer, fetch, event → event loop.
6. **Tạo private state trong object** — closure + IIFE pattern (trước class/private fields).
7. **Memoization/caching** — closure giữ cache giữa các lần gọi hàm.
8. **Module pattern** — IIFE trả về object public API, giữ internals private.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Closure — biến đếm nhớ trạng thái (file `app.js` trong `03_closure/`)
```js
function createCounter() {
  let count = 0; // biến "bị đóng gói" trong closure
  return () => ++count; // hàm con nhớ count từ scope ngoài
}
const c = createCounter();
console.log(c(), c(), c()); // 1 2 3 — mỗi lần gọi tăng dần
// count = 0 ban đầu, nhưng sau mỗi lần gọi c(), count được giữ lại
```

### Ví dụ 2: IIFE — module private (file `app.js` trong `02_iife/`)
```js
// Module pattern bằng IIFE
const app = (function() {
  const cars = []; // private — ngoài không truy cập được
  return {
    add: car => cars.push(car),
    all: () => [cars]
  };
})();
app.add("Winner 2022");
console.log(app.all()); // [["Winner 2022"]]
// console.log(app.cars); // undefined — private!
```

### Ví dụ 3: Strict mode — this behavior (file `app.js` trong `01_strict-mode/`)
```js
"use strict";
function test() {
  console.log(this); // undefined (không phải window/global)
}
test();
// Không có strict mode: this === window (browser) hoặc global (Node)
// Có strict mode: this === undefined — rõ ràng hơn
```

### Ví dụ 4: Call stack trace (file `app.js` trong `05_function-stack/`)
```js
function a() { b(); }
function b() { c(); }
function c() {
  console.log("stack:");
  console.trace(); // in ra a → b → c
}
a();
// stack:
//     at c (<anonymous>:3:15)
//     at b (<anonymous>:2:17)
//     at a (<anonymous>:1:17)
//     at <anonymous>:6:1
```

### Ví dụ 5: Non-blocking I/O — setTimeout concept (file `04_non-blocking-io/` README)
```js
console.log("1. bắt đầu");

setTimeout(() => console.log("3. timer xong (bất đồng bộ)"), 0);

console.log("2. chạy tiếp ngay — không bị chặn");

// Kết quả in ra: 1. bắt đầu → 2. chạy tiếp → 3. timer xong
// Dù timeout = 0, nó vẫn chạy SAU các câu lệnh đồng bộ
```

### Ví dụ 6: Closure factory — createLogger
```js
function createLogger(namespace) {
  return function(message) {
    console.log(`[${namespace}] ${message}`);
  };
}
const logInfo = createLogger("Info");
const logError = createLogger("Error");
logInfo("Bắt đầu gửi mail!"); // [Info] Bắt đầu gửi mail!
logError("Có lỗi xảy ra!");   // [Error] Có lỗi xảy ra!
// Mỗi closure nhớ namespace riêng — độc lập với nhau
```

### Ví dụ 7: Closure memory leak pattern
```js
function init() {
  const largeData = new Array(1000000).fill("data"); // large array
  return function() {
    return largeData[0]; // closure giữ reference đến largeData
  };
}
const getter = init();
// largeData KHÔNG bao giờ bị GC vì closure getter giữ reference
// ✅ Giải pháp: null reference khi không cần
getter = null; // bây giờ largeData có thể bị GC
```

### Ví dụ 8: IIFE với tham số — module factory
```js
const createModule = (function() {
  let moduleCount = 0; // private counter
  return function(name) {
    moduleCount++;
    return {
      name,
      id: moduleCount,
      greet() { return `Hello from ${this.name}#${this.id}`; }
    };
  };
})();
const m1 = createModule("Alpha");
const m2 = createModule("Beta");
console.log(m1.greet()); // "Hello from Alpha#1"
console.log(m2.greet()); // "Hello from Beta#2"
// moduleCount được closure giữ — tăng dần qua các lần gọi
```

### Ví dụ 9: Scope chain — biến tìm từ trong ra ngoài
```js
let globalVar = "global";

function outer() {
  let outerVar = "outer";
  function inner() {
    let innerVar = "inner";
    console.log(globalVar, outerVar, innerVar);
    // scope chain: inner → outer → global
  }
  inner();
}
outer(); // "global" "outer" "inner"

// Inner KHÔNG thể nhìn thấy biến của outer caller's scope
// Chỉ có thể nhìn thấy: own scope → parent scope → ... → global
```

### Ví dụ 10: Strict mode — các hành vi bị cấm
```js
"use strict";

// ❌ Gán biến chưa khai báo
// x = 100; // TypeError: assignment to undeclared variable

// ❌ delete biến
// let v = 10; delete v; // TypeError

// ❌ Octal literal
// let octal = 010; // SyntaxError

// ❌ Duplicate parameter names
// function sum(a, a) {} // SyntaxError

// ❌ this trong function gọi trực tiếp = undefined
function test() { console.log(this); }
test(); // undefined (không phải window)
```

## 🔬 So sánh với alternatives

| Khái niệm | Cách tiếp cận cổ điển | Cách hiện đại |
|---|---|---|
| Private scope | IIFE module pattern | ES modules (`import`/`export`) |
| State persistence | Closure + counter | Class với private field (`#count`) |
| Global prevention | `"use strict"` + IIFE | ES modules (module scope mặc định) |
| Async handling | Callbacks + setTimeout | Promise + `async/await` |
| Call tracking | `console.trace()` | Browser DevTools Sources panel |

## 📊 Performance & Best Practices

**Performance**:
- Closure có overhead nhỏ do tạo thêm scope chain — negligible trong 99% cases.
- IIFE không có overhead đặc biệt — chỉ là function call thông thường.
- Call stack depth giới hạn ~10k-15k frames trong V8 — recursive functions >10k sẽ overflow.
- Strict mode có overhead rất nhỏ (~1-5%) — chấp nhận được cho safety gain.

**Best practices**:
- **Luôn bật `"use strict"`** trong file mới — prevent silent bugs, enforce better coding.
- **Dùng IIFE** chỉ khi cần private scope trong legacy code — hiện đại dùng ES modules.
- **Hiểu closure để tránh memory leak** — null reference khi không cần state nữa.
- **Dùng `let` thay `var` trong loop** + setTimeout — tránh closure share variable bug.
- **Giới hạn recursive depth** — dùng iterative hoặc tail recursion khi depth > 1000.
- **Dùng `console.trace()`** khi debug stack overflow hoặc call order issues.
- **ES modules thay thế IIFE** — cleaner syntax, tree-shaking support, static analysis.
- **Private class fields** (`#count`) thay closure cho encapsulation — modern, performant.
- **Avoid deep nesting** — max 2-3层级 scope chain để maintainability.
- **Test closure behavior** — đảm bảo variable không bị shared across instances unintended.

**Quy tắc "3 nên — 3 không"**:
- ✅ Nên bật `"use strict"` trong mọi file mới.
- ✅ Nên hiểu closure để debug memory leaks.
- ✅ Nên dùng `let` trong loop + async callback.
- ❌ Không nên giữ closure reference lâu không cần — memory leak risk.
- ❌ Không nên nest IIFE quá sâu — khó đọc, khó debug.
- ❌ Không nên dùng IIFE thay ES modules trong code mới.

## 🔗 Liên kết chéo

- Strict mode chi tiết: `09_functions/02_scope-closure-strict-mode/01_strict-mode/` — rules, cấm behaviors.
- IIFE chi tiết: `09_functions/02_scope-closure-strict-mode/02_iife/` — private scope, module pattern.
- Closure chi tiết: `09_functions/02_scope-closure-strict-mode/03_closure/` — capture variables, memory leak.
- Non-blocking I/O: `09_functions/02_scope-closure-strict-mode/04_non-blocking-io/` — event loop concept.
- Call stack: `09_functions/02_scope-closure-strict-mode/05_function-stack/` — execution context, scope chain.
- Arrow functions: `09_functions/01_parameters-and-arrow/03_arrow-functions/` — lexical this trong closure.
- Callbacks: `09_functions/01_parameters-and-arrow/01_callbacks/` — callback trong closure context.
- Recursion: `09_functions/01_parameters-and-arrow/04_recursion/` — call stack overflow in recursion.
- Arguments object: `09_functions/01_parameters-and-arrow/05_arguments-object/` — arguments trong nested scope.
- Exceptional handling: `07_exceptional-handling/02_try-catch-finally/` — error trong call stack.
