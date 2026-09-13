# Call Stack và Scope Chain (Function Stack) — Thực hành chi tiết — [Level: Advanced]

## 🔑 Khái niệm cốt lõi

**Call stack** (ngăn xếp gọi hàm) là cơ chế JavaScript dùng để theo dõi "đang chạy hàm nào, hàm nào chờ kết quả". Hoạt động theo nguyên tắc **LIFO** (Last In, First Out): hàm nào được gọi sau cùng thì chạy xong và **pop** ra trước, hàm gọi trước "đứng chờ".

```js
function a() { b(); }
function b() { c(); }
function c() { console.trace(); } // in ra stack trace
a();
```

Thứ tự khi chạy: `a` → `b` → `c` (push lần lượt), rồi `c` xong → pop, `b` xong → pop, `a` xong → pop. Mỗi lần gọi hàm tạo **một execution context** (bối cảnh thực thi) — chứa biến cục bộ, `this`, phạm vi — và context đó nằm trên ngăn xếp cho đến khi hàm trả về.

**Scope chain** (chuỗi phạm vi) là chuỗi các phạm vi mà JavaScript **dò tìm biến** từ trong ra ngoài. Hàm con nhìn thấy biến của mình, rồi của hàm cha, rồi global — nhưng không phải ngược lại.

```js
let g = 1;
function outer() {
  let o = 2;
  function inner() {
    console.log(g, o); // tìm g (global), rồi o (outer) — theo scope chain
  }
  inner();
}
outer(); // 1 2
```

Khi tìm biến `g` trong `inner`: không có trong `inner` → nhìn lên `outer` → không có → nhìn ra global → thấy `g = 1`. Đó chính là scope chain.

**Hai khái niệm này kết hợp**: call stack quản lý execution context (ai đang chạy), scope chain quản lý variable lookup (biến tìm ở đâu). Cùng nhau chúng tạo nên **dynamic scoping model** của JavaScript.

## 📐 Cấu trúc / Cú pháp

### Call Stack mechanics
```js
// Mỗi function call = push execution context lên stack
function first() {
  second(); // push second
  console.log("first done"); // pop second, tiếp tục first
}

function second() {
  third(); // push third
  console.log("second done"); // pop third
}

function third() {
  console.log("third running"); // pop third (return)
}

first();
// Stack: [first] → [first, second] → [first, second, third]
// Pop: third → second → first
```

### Scope chain lookup
```js
let globalVar = "global";

function level1() {
  let l1Var = "level1";
  function level2() {
    let l2Var = "level2";
    function level3() {
      let l3Var = "level3";
      // Scope chain: level3 → level2 → level1 → global
      console.log(l3Var, l2Var, l1Var, globalVar);
    }
    level3();
  }
  level2();
}
level1(); // "level3" "level2" "level1" "global"
```

### console.trace() — inspect call stack
```js
function a() { b(); }
function b() { c(); }
function c() {
  console.log("--- Stack trace ---");
  console.trace(); // in ra call stack tại thời điểm này
}
a();
// stack:
//     at c (<anonymous>:5:11)
//     at b (<anonymous>:2:17)
//     at a (<anonymous>:1:17)
//     at <anonymous>:7:1
```

### Error stack trace
```js
function thrower() {
  throw new Error("Something went wrong");
}
function caller() {
  thrower();
}
caller();
// Error: Something went wrong
//     at thrower (<anonymous>:2:9)
//     at caller (<anonymous>:5:3)
//     at <anonymous>:7:1
// Stack trace giúp debug: biết lỗi từ đâu đến
```

## ✅ Điểm mạnh

1. **Giúp debug stack trace** dễ dàng: đọc từ dưới lên biết "ai gọi ai" — xác định origen lỗi nhanh.
2. **`console.trace()` là công cụ in call stack chuẩn**, sẵn có — không cần thư viện bên ngoài, debug inline.
3. **Hiểu call stack giải thích được lỗi "Maximum call stack size exceeded"** (đệ quy vô hạn) — known limitation.
4. **Scope chain giải thích cơ chế closure** và phạm vi biến một cách trực quan — closure = function + reference to outer scope.
5. **Nhận biết được giới hạn**: đệ quy sâu bao nhiêu có thể nổ ngăn xếp — thường ~10k-15k frames trong V8.
6. **Là nền tảng để hiểu bất đồng bộ** (event loop) và `this` binding — call stack empty = event loop processing callbacks.
7. **Visualizing execution** — vẽ call stack giúp understanding flow, đặc biệt với recursive functions.
8. **Profiler integration** — Chrome DevTools Performance tab hiển thị call stack timeline — identify bottlenecks.
9. **Error boundaries in React** — error stack trace giúp component identify where error originated.
10. **Understanding hoisting** — call stack + scope chain explain why function declarations hoisted but not expressions.

## ⚠️ Bẫy thường gặp & Hạn chế

1. **Call stack có giới hạn độ sâu** — đệ quy không kiểm soát sẽ tràn ngăn xếp (stack overflow).
   ```js
   function boom() { boom(); } // vô hạn đệ quy
   boom(); // RangeError: Maximum call stack size exceeded
   // Giới hạn: ~10,000-15,000 frames trong V8 (Chrome/Node)
   ```

2. **Mỗi lần gọi hàm đều tốn bộ nhớ** cho execution context — lồng/đệ quy quá nhiều gây tốn tài nguyên.
   ```js
   // Deep nesting — memory pressure
   function deep(n) {
     if (n === 0) return;
     return deep(n - 1) + 1; // mỗi call tạo new execution context
   }
   deep(10000); // có thể stack overflow!
   ```

3. **Scope chain giúp truy cập biến ngoài nhưng cũng là nơi phát sinh closure giữ tham chiếu** (xem `03_closure`) — memory leak risk.
4. **Thứ tự "ngược" của stack** (hàm gọi sau chạy trước) khiến người mới dễ nhầm thứ tự thực thi.
   ```js
   function a() { console.log("a start"); b(); console.log("a end"); }
   function b() { console.log("b"); }
   a();
   // Output: "a start" → "b" → "a end"
   // b chạy GIỮA a, không phải sau a — vì b pushed onto stack, runs, pops, then a continues
   ```

5. **Không thể nhìn trực tiếp call stack khi code chưa chạy** — cần breakpoint hoặc `console.trace()` tại runtime.
6. **Async callbacks không nằm trên call stack cùng lúc** — chúng enqueue vào callback queue, chỉ push khi stack empty.
   ```js
   console.log("1");
   setTimeout(() => console.log("2"), 0);
   console.log("3");
   // Output: 1 → 3 → 2 (callback chạy sau sync code, khi stack empty)
   ```
7. **Stack trace bị truncate** trong một số environment — deep recursion只显示 top frames.

## 💡 Khi nào dùng

1. **Debug 1 lỗi "hàm này được gọi từ đâu"** — mở DevTools Sources/Console stack trace, đọc từ dưới lên.
2. **Kiểm tra ngăn xếp trong thời gian chạy** bằng `console.trace()` — inline debugging, no breakpoint needed.
3. **Giải thích lỗi tràn ngăn xếp** khi đệ quy — identify missing base case hoặc depth too large.
4. **Tối ưu vòng lặp/đệ quy** để tránh gọi hàm lồng quá sâu — convert to iterative nếu depth > 1000.
5. **Học closure, bất đồng bộ và event loop** — mọi thứ đều xoay quanh call stack (ai đang chạy) và scope chain (biến ở đâu).
6. **Performance profiling** — Chrome DevTools Call Tree xem function call hierarchy, identify hot paths.
7. **Error monitoring** (Sentry, LogRocket) — stack trace giúp group và prioritize errors by origin.
8. **Code review** — understand call depth and potential stack overflow risks in recursive code.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Call stack trace (file `app.js`)
```js
// Nội dung app.js trong thư mục
function a() { b(); }
function b() { c(); }
function c() {
  console.log("stack:");
  console.trace(); // in ra a → b → c
}
a();
// stack:
//     at c (<anonymous>:5:11)
//     at b (<anonymous>:2:17)
//     at a (<anonymous>:1:17)
//     at <anonymous>:6:1
```

### Ví dụ 2: Scope chain — inner tìm biến qua chuỗi phạm vi
```js
// Nội dung app.js trong thư mục
let g = 1;
function outer() {
  let o = 2;
  function inner() {
    console.log(g, o); // 1 2 — scope chain: inner → outer → global
  }
  inner();
}
outer();
```

### Ví dụ 3: Stack overflow — đệ quy không base case
```js
function infiniteRecursion() {
  infiniteRecursion(); // không có base case — forever pushing onto stack
}
infiniteRecursion();
// RangeError: Maximum call stack size exceeded
//     at infiniteRecursion (<anonymous>:2:3)
//     at infiniteRecursion (<anonymous>:2:3)
//     ... (many more frames)
```

### Ví dụ 4: Stack depth test — giới hạn bao nhiêu?
```js
function countDepth(fn, depth = 0) {
  try {
    return countDepth(fn, depth + 1);
  } catch (e) {
    return depth; // stack overflow tại depth này
  }
}
// ⚠️ Không chạy hàm này — sẽ crash!
// Trên Chrome/Node: ~10,000-15,000 frames
// Trên Firefox SpiderMonkey: ~50,000+ frames
```

### Ví dụ 5: Async — call stack vs callback queue
```js
console.log("A"); // 1. push console, run, pop

setTimeout(() => {
  console.log("B"); // 4. callback pushed to macrotask queue, runs when stack empty
}, 0);

console.log("C"); // 2. push console, run, pop

Promise.resolve().then(() => {
  console.log("D"); // 3. microtask — runs before macrotasks
});

console.log("E"); // 3. push console, run, pop

// Output: A → C → E → D → B
// Call stack: [console(A)] → [console(C)] → [console(E)] → empty
// Then microtask queue: [Promise.then(D)] → runs
// Then macrotask queue: [setTimeout(B)] → runs
```

### Ví dụ 6: Understanding "who called whom" with trace
```js
function alpha() { beta(); }
function beta() { gamma(); }
function gamma() {
  console.log("In gamma");
  console.trace();
}
alpha();
// In gamma
// stack:
//     at gamma (<anonymous>:6:11)
//     at beta (<anonymous>:3:17)
//     at alpha (<anonymous>:2:17)
//     at <anonymous>:8:1
// Đọc từ dưới lên: main → alpha → beta → gamma
// Vậy gamma được gọi bởi beta, beta được gọi bởi alpha
```

### Ví dụ 7: Scope chain với block scope (let/const)
```js
let globalVar = "global";

function outer() {
  let outerVar = "outer";
  if (true) {
    let blockVar = "block"; // block-scoped, not accessible outside
    function inner() {
      let innerVar = "inner";
      // Scope chain: inner → if-block → outer → global
      console.log(innerVar, blockVar, outerVar, globalVar);
    }
    inner();
  }
  // console.log(blockVar); // ReferenceError — block-scoped
}
outer(); // "inner" "block" "outer" "global"
```

### Ví dụ 8: Execution context creation steps
```js
// Mỗi function call tạo 2 giai đoạn:
// 1. Creation phase: tạo variable object, scope chain, this binding
// 2. Execution phase: chạy code, push/pop call stack

function example(x) {
  var y = x + 2;
  return y;
}
example(3);
// Creation: [executionContext { variables: {x:3, y:undefined}, scopeChain: [...], this: global }]
// Execution: y = 3 + 2 = 5, return 5
// Stack: [example] → pop after return
```

### Ví dụ 9: Stack visualization — recursive factorial
```js
function factorial(n) {
  if (n <= 1) return 1;           // base case
  return n * factorial(n - 1);    // recursive case
}
// factorial(3) call stack visualization:
// factorial(3) → push
//   factorial(2) → push
//     factorial(1) → push → return 1 → pop
//   return 2 * 1 = 2 → pop
// return 3 * 2 = 6 → pop
// Result: 6
console.log(factorial(3)); // 6
```

### Ví dụ 10: Using new Error().stack for custom tracing
```js
function customTrace(msg) {
  const err = new Error(msg);
  console.log(err.stack); // tương đương console.trace()
}

function level1() { level2(); }
function level2() { level3(); }
function level3() {
  customTrace("Current position in stack");
}
level1();
// Error: Current position in stack
//     at customTrace (<anonymous>:2:17)
//     at level3 (<anonymous>:9:3)
//     at level2 (<anonymous>:8:17)
//     at level1 (<anonymous>:7:17)
//     at <anonymous>:10:1
```

## 🔬 So sánh với alternatives

| Khái niệm | Call Stack | Scope Chain | Alternative |
|---|---|---|---|
| **Execution tracking** | Call stack (LIFO) | — | Debuggers, profilers |
| **Variable lookup** | — | Scope chain (inner→outer) | Symbol tables, AST analysis |
| **Error origin** | Stack trace | — | Source maps, error boundaries |
| **Memory management** | Stack allocation | Closure heap allocation | GC traces, heap snapshots |

## 📊 Performance & Best Practices

**Performance**:
- Call stack push/pop: ~nanoseconds — negligible overhead.
- Scope chain lookup: O(depth) — deeper scopes = slightly slower variable access.
- Stack depth limit: ~10k-15k frames in V8 — recursive functions should respect this.
- `console.trace()` overhead: moderate — avoid in hot loops, use for debugging only.

**Best practices**:
- **Luôn có base case** trong recursive functions — prevent stack overflow.
- **Giới hạn recursion depth** — nếu > 1000, convert to iterative hoặc dùng tail recursion (không được JS optimize).
- **Dùng `console.trace()`** khi debug gọi hàm — hiểu flow, identify unexpected calls.
- **Profile call stack** trong DevTools — Performance tab → Call Tree — identify hot functions.
- **Avoid deep nesting** — max 2-3层级 function calls cho readability và performance.
- **Use tail-call optimization** (theoretical) — viết recursive function dạng tail call, mặc dù JS engines chưa optimize.
- **Understand async call stack** — callbacks không nằm trên stack cùng lúc, chúng enqueue vào queue.
- **Monitor stack size** trong production — error boundary, retry logic cho deep recursion.
- **Source maps** — debug minified code với stack trace readable.
- **Error.stack parsing** — automate error grouping by stack trace patterns.

**Quy tắc "3 nên — 3 không"**:
- ✅ Nên dùng `console.trace()` để debug call flow.
- ✅ Nên giới hạn recursion depth < 1000 — convert to iterative khi cần.
- ✅ Nên hiểu scope chain để debug closure và variable lookup bugs.
- ❌ Không nên đệ quy không có base case — stack overflow guaranteed.
- ❌ Không nên nest function calls quá 3层级 — khó debug, maintain.
- ❌ Không nên dùng `console.trace()` trong production hot path — performance hit.

## 🔗 Liên kết chéo

- Tổng quan Scope & Closure: `09_functions/02_scope-closure-strict-mode/README.md` — overview.
- Closure: `09_functions/02_scope-closure-strict-mode/03_closure/` — closure dựa trên scope chain.
- IIFE: `09_functions/02_scope-closure-strict-mode/02_iife/` — IIFE execution context trên stack.
- Strict mode: `09_functions/02_scope-closure-strict-mode/01_strict-mode/` — strict mode effect on execution.
- Recursion: `09_functions/01_parameters-and-arrow/04_recursion/` — recursion stack overflow.
- Non-blocking I/O: `09_functions/02_scope-closure-strict-mode/04_non-blocking-io/` — event loop + call stack interaction.
- Arrow functions: `09_functions/01_parameters-and-arrow/03_arrow-functions/` — lexical this trong scope chain.
- Arguments object: `09_functions/01_parameters-and-arrow/05_arguments-object/` — arguments trong execution context.
- Exceptional handling: `07_exceptional-handling/` — error stack trace trong try/catch.
- Callbacks: `09_functions/01_parameters-and-arrow/01_callbacks/` — callback queue vs call stack.
