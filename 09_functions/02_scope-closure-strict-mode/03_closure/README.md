# Closure (Bao đóng) — Thực hành chi tiết — [Level: Advanced]

## 🔑 Khái niệm cốt lõi

**Closure** là một hàm có khả năng **"ghi nhớ" nơi nó được tạo** và **truy cập được các biến ở phạm vi bên ngoài** của chính nó — ngay cả sau khi hàm ngoài đã chạy xong. Nói cách khác: hàm con "đóng gói" (bao đóng) môi trường nơi nó sinh ra.

Khái niệm này có **3 yếu tố cùng xuất hiện**:
1. Có **hàm lồng trong hàm** (`increase` nằm trong `createCounter`).
2. Hàm trong **tham chiếu biến của hàm ngoài** (`counter`).
3. Hàm trong được **trả ra ngoài** hoặc giữ lại → "sống sót" sau khi hàm ngoài kết thúc.

Ví dụ kinh điển trong `app.js`:

```js
function createCounter() {
  let counter = 0;
  function increase() {
    return ++counter; // tham chiếu biến ngoài phạm vi
  }
  return increase;
}

const _counter1 = createCounter();
console.log(_counter1()); // 1
console.log(_counter1()); // 2 — vẫn "nhớ" counter = 1 ở lần trước
console.log(_counter1()); // 3
```

Bạn gọi `createCounter()` **một lần** → tạo **một phạm vi** riêng với biến `counter = 0`. Hàm `increase` trả về được giữ ở biến ngoài, nhờ closure mà nó vẫn "nhìn thấy" `counter` và mỗi lần gọi lấy **giá trị mới nhất** của biến đó → `1, 2, 3`.

**Cơ chế bên trong engine**: khi `createCounter()` return, normally scope của nó会被 GC destroy. Nhưng vì `increase` (được trả về) còn reference đến `counter`, V8/SpiderMonkey **giữ lại scope object** đó trong memory — đây chính là closure. Scope object chứa `counter` và mọi biến outer scope mà `increase` cần access.

README cũ còn cho hai ứng dụng thực tế:
- **`createLogger(namespace)`** — trả về hàm log "nhớ" namespace, ra `[Info] Bắt đầu gửi mail!`, `[Error] Có lỗi!`.
- **`createStorage(key)`** — trả về module đọc/ghi localStorage; `store` được closure giữ kín.

## 📐 Cấu trúc / Cú pháp

### Basic closure
```js
function outer(outerVar) {
  return function(innerVar) {
    // closure: inner function remembers outerVar
    return `${outerVar} ${innerVar}`;
  };
}
const greet = outer("Xin chào");
console.log(greet("Sơn")); // "Xin chào Sơn"
// outerVar = "Xin chào" được closure giữ lại
```

### Closure với mutable state
```js
function createManager() {
  let tasks = [];
  return {
    add(task) { tasks.push(task); },
    get() { return [...tasks]; }, // return copy
    complete(index) { tasks.splice(index, 1); }
  };
}
const manager = createManager();
manager.add("task1");
manager.add("task2");
console.log(manager.get()); // ["task1", "task2"]
```

### Closure factory
```js
function createValidator(rules) {
  return function(value) {
    for (const rule of rules) {
      if (!rule(value)) {
        return false;
      }
    }
    return true;
  };
}
const isPositiveAndEven = createValidator([
  v => v > 0,
  v => v % 2 === 0
]);
console.log(isPositiveAndEven(4)); // true
console.log(isPositiveAndEven(-2)); // false
```

### Closure with IIFE — module pattern
```js
const module = (function() {
  let privateState = 0;
  return {
    getState() { return privateState; },
    setState(val) { privateState = val; }
  };
})();
```

## ✅ Điểm mạnh

1. **Viết code gọn**: tạo function factory (hàm sản xuất hàm) mà không cần class — functional style, less boilerplate.
2. **Biểu diễn tính private trong OOP**: biến nội bộ không lộ ra ngoài, chỉ lộ API trả về — encapsulation mà không cần class.
3. **Lưu giữ trạng thái** giữa các lần gọi (counter, cache, storage) một cách tự nhiên — stateful function without class.
4. **Giữ giá trị mới nhất** của biến (như `counter` tăng dần) — không bị snapshot cũ, closure luôn access current value.
5. **Là nền tảng của các pattern hiện đại**: currying, memoization, module, hooks (React `useState`/`useEffect` về bản chất dựa trên closure).
6. **Tạo ra nhiều "instance" độc lập**: mỗi lần gọi `createX()` có phạm vi riêng — như factory tạo objects mà không cần `new`.
7. **Data hiding without class** — trước ES2022 private fields (`#field`), closure là cách duy nhất để private state.
8. **Function composition friendly** — closures dễ compose thành pipeline: `pipe(f, g, h)(x)`.
9. **Event handler state retention** — mỗi listener có state riêng qua closure — không cần global variables.
10. **Memoization natural** — cache trong closure persist across calls, no external state needed.

## ⚠️ Bẫy thường gặp & Hạn chế

1. **Biến trong closure không bị dọn** khỏi bộ nhớ khi hàm ngoài kết thúc — nếu giữ tham chiếu lâu, có thể **thất thoát bộ nhớ (memory leak)**. Đây là 1 trong 4 nguyên nhân chính gây rò rỉ bộ nhớ trong JS.
   ```js
   function attachHandler() {
     const largeData = new Array(1000000).fill("data"); // large array
     document.getElementById("btn").addEventListener("click", function() {
       console.log(largeData.length); // closure giữ largeData
     });
     // largeData KHÔNG bao giờ bị GC vì closure giữ reference
   }
   // ✅ Giải pháp: null reference khi không cần
   // document.getElementById("btn").removeEventListener(...)
   ```

2. **Nếu không hiểu rõ "tham chiếu mới nhất"**, dễ code ra bug trong vòng lặp (ví dụ gắn `setTimeout` trong `for`).
   ```js
   // ❌ Bug kinh điển — var share same scope
   for (var i = 0; i < 3; i++) {
     setTimeout(() => console.log(i), 100); // in 3 3 3 — i = 3 ở lúc callback chạy
   }
   // ✅ Sửa bằng let (block scope)
   for (let i = 0; i < 3; i++) {
     setTimeout(() => console.log(i), 100); // in 0 1 2 — mỗi closure có i riêng
   }
   ```

3. **Quá nhiều closure lồng nhau** làm code khó đọc, khó debug — scope chain dài, khó track variable origin.
4. **Cần chủ động "release" (null ra tham chiếu)** khi không còn dùng module lớn — prevent memory leak.
5. **Closure overhead** — mỗi closure tạo scope chain mới, memory cost cao hơn plain function.
6. **Debug khó** — stack trace hiện closure function tên anonymous, khó trace origin.
7. **Testing khó** — private state trong closure không thể unit test trực tiếp, cần qua public API.
8. **Circular reference risk** — closure giữ reference đến object cũng giữ reference đến closure → GC không collect được.

## 💡 Khi nào dùng

1. **Tạo factory/function riêng với cấu hình cố định** (`createLogger("Info")`) — hàm được customize bởi closure state.
2. **Bộ đếm, cache, storage private** có API nhỏ gọn — counter, memoized function, localStorage wrapper.
3. **Đóng gói state cho widget/module** mà không cần class — lightweight alternative to OOP.
4. **Trong hàm `useState`/`useEffect` của React** — hooks thực chất là closure pattern, tránh bắt được biến cũ — hiểu closure để tránh bug.
5. **Xử lý sự kiện/timer cần nhớ biến tại thời điểm tạo** — each listener có captured state riêng.
6. **Currying và partial application** — `const add = a => b => a + b; const add5 = add(5);`
7. **Middleware pattern** — mỗi middleware có closure state, chainable.
8. **Event bus với private listeners** — module pattern với closure giữ listeners array.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Counter kinh điển (file `app.js`)
```js
// Nội dung app.js trong thư mục
function createCounter() {
  let counter = 0;
  function increase() {
    return ++counter; // tham chiếu biến ngoài phạm vi
  }
  return increase;
}

const _counter1 = createCounter();   // một phạm vi riêng
console.log(_counter1()); // 1
console.log(_counter1()); // 2
console.log(_counter1()); // 3

// Mỗi lần gọi createCounter() tạo closure MỚI, ĐỘC LẬP
const _counter2 = createCounter();
console.log(_counter2()); // 1 ← bắt đầu từ 0, không ảnh hưởng _counter1
console.log(_counter1()); // 4 ← _counter1 vẫn tiếp tục từ 3
```

### Ví dụ 2: Factory nhớ "namespace" (file `app.js`)
```js
// Nội dung app.js trong thư mục
function createLogger(namespace) {
  return function(message) {
    console.log(`[${namespace}] ${message}`);
  };
}
const logInfo = createLogger("Info");
const logError = createLogger("Error");
logInfo("Bắt đầu gửi mail!"); // [Info] Bắt đầu gửi mail!
logError("Có lỗi!");          // [Error] Có lỗi!
// Mỗi logger nhớ namespace riêng — closure giữ giá trị tại thời điểm create
```

### Ví dụ 3: Multiple independent counters
```js
function createCounter(initial = 0) {
  let count = initial;
  return {
    increment() { return ++count; },
    decrement() { return --count; },
    getValue() { return count; },
    reset(val = 0) { count = val; return count; }
  };
}
const c1 = createCounter(10);
const c2 = createCounter(100);
console.log(c1.increment()); // 11
console.log(c2.increment()); // 101
console.log(c1.getValue());  // 11 — độc lập với c2
console.log(c2.getValue());  // 101 — mỗi closure có count riêng
```

### Ví dụ 4: Memoization với closure
```js
function memoize(fn) {
  const cache = new Map(); // closure giữ cache
  return function(...args) {
    const key = JSON.stringify(args);
    if (cache.has(key)) {
      return cache.get(key);
    }
    const result = fn.apply(this, args);
    cache.set(key, result);
    return result;
  };
}

// Fibonacci memoized — O(n) thay vì O(2^n)
const fibMemo = memoize(function(n) {
  if (n <= 1) return n;
  return fibMemo(n - 1) + fibMemo(n - 2);
});
console.log(fibMemo(50)); // 12586269025 — instant! (memoized)
console.log(fibMemo(50)); // same — lấy từ cache, không tính lại
```

### Ví dụ 5: Closure trong vòng lặp — bug và fix
```js
// ❌ Bug — var share same closure scope
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log("var bug:", i), 10);
}
// Kết quả: 3 3 3 — vì i = 3 khi timeout callback chạy

// ✅ Fix — let tạo block scope, mỗi iter có closure riêng
for (let i = 0; i < 3; i++) {
  setTimeout(() => console.log("let fix:", i), 10);
}
// Kết quả: 0 1 2 — mỗi setTimeout closure capture i riêng

// ✅ Fix — IIFE tạo scope riêng cho mỗi iter
for (var j = 0; j < 3; j++) {
  (function(index) {
    setTimeout(() => console.log("IIFE fix:", index), 10);
  })(j);
}
// Kết quả: 0 1 2
```

### Ví dụ 6: CreateStorage — localStorage wrapper với closure
```js
function createStorage(prefix) {
  return {
    set(key, value) {
      localStorage.setItem(`${prefix}_${key}`, JSON.stringify(value));
    },
    get(key) {
      const val = localStorage.getItem(`${prefix}_${key}`);
      return val ? JSON.parse(val) : null;
    },
    remove(key) {
      localStorage.removeItem(`${prefix}_${key}`);
    },
    clear() {
      // Xóa tất cả keys với prefix này
      for (let i = localStorage.length - 1; i >= 0; i--) {
        const key = localStorage.key(i);
        if (key && key.startsWith(`${prefix}_`)) {
          localStorage.removeItem(key);
        }
      }
    }
  };
}
const userStorage = createStorage("user");
userStorage.set("profile", { name: "Sơn", age: 18 });
console.log(userStorage.get("profile")); // { name: "Sơn", age: 18 }
// prefix = "user" được closure giữ — không cần truyền mỗi lần gọi
```

### Ví dụ 7: Currying với closure
```js
// Curry — transform multi-arg function into sequence of unary functions
const add = a => b => c => a + b + c;
console.log(add(1)(2)(3)); // 6

// Partial application — fix some args, return new function
const multiply = a => b => a * b;
const double = multiply(2);
const triple = multiply(3);
console.log(double(5)); // 10
console.log(triple(5)); // 15

// Thực tế: API builder
const createFetcher = baseUrl => endpoint => `/api/${baseUrl}/${endpoint}`;
const usersApi = createFetcher("users");
console.log(usersApi("list"));    // "/api/users/list"
console.log(usersApi("details")); // "/api/users/details"
```

### Ví dụ 8: Event handler với closure state
```js
// Mỗi button có counter riêng qua closure
function attachCounter(buttonId, initialValue = 0) {
  const btn = document.getElementById(buttonId);
  let count = initialValue; // closure state

  btn.addEventListener("click", function() {
    count++;
    btn.textContent = `Clicked: ${count}`;
  });

  // Return reset function — also closure
  return function reset() {
    count = 0;
    btn.textContent = "Clicked: 0";
  };
}
const resetBtn1 = attachCounter("btn1");
const resetBtn2 = attachCounter("btn2", 10); // start from 10
// resetBtn1 và resetBtn2 là các closure riêng — đếm độc lập
```

### Ví dụ 9: Module pattern — complete example
```js
const ShoppingCart = (function() {
  // Private state
  let items = [];
  let nextId = 1;

  // Private helper
  function calculateTotal() {
    return items.reduce((sum, item) => sum + item.price, 0);
  }

  // Public API
  return {
    addItem(name, price) {
      items.push({ id: nextId++, name, price });
    },
    removeItem(id) {
      items = items.filter(item => item.id !== id);
    },
    getTotal() {
      return calculateTotal();
    },
    getItems() {
      return [...items]; // return copy, not reference
    },
    clear() {
      items = [];
      nextId = 1;
    }
  };
})();

ShoppingCart.addItem("Áo", 200000);
ShoppingCart.addItem("Quần", 300000);
console.log(ShoppingCart.getTotal()); // 500000
console.log(ShoppingCart.getItems()); // [{id:1,name:"Áo",price:200000}, ...]
// items và nextId không accessible từ outside
```

### Ví dụ 10: Memory leak detection và prevention
```js
function problematicPattern() {
  const largeArray = new Array(1000000).fill("data");
  return function() {
    return largeArray.length; // closure giữ largeArray — memory leak!
  };
}
const getter = problematicPattern();
console.log(getter()); // 1000000
// largeArray KHÔNG bao giờ bị GC vì getter closure giữ reference

// ✅ Prevention 1: Null reference when done
getter = null; // bây giờ largeArray có thể bị GC

// ✅ Prevention 2: Use weakref (ES2021)
const weakRef = new WeakRef(largeArray);
console.log(weakRef.deref()?.length); // 1000000 or undefined if GC'd

// ✅ Prevention 3: Don't close over large objects
function safePattern() {
  const largeArray = new Array(1000000).fill("data");
  const len = largeArray.length; // capture primitive, not reference
  return function() { return len; }; // chỉ giữ number, không giữ array
}
```

## 🔬 So sánh với alternatives

| Pattern | Ưu điểm | Nhược điểm | So với closure |
|---|---|---|---|
| **Closure** | Private state, no class needed | Memory leak risk, harder debug | Baseline |
| **Class + #private** | Native privacy, better tooling | ES2022+, class overhead | Closure lighter, class more explicit |
| **Module pattern (IIFE)** | Proven, works everywhere | Verbose, manual management | Closure is the mechanism behind it |
| **ES Modules** | Native, tree-shaking | No runtime privacy (all exports public) | Closure for private state, modules for public API |
| **Global variables** | Simple | Namespace pollution, no privacy | Closure: private vs global: public |
| **Object properties** | Accessible, editable | No true privacy | Closure: private vs object: public |

## 📊 Performance & Best Practices

**Performance**:
- Closure có overhead nhỏ do tạo scope chain — ~10-20% slower than plain function.
- Memory cost: mỗi closure giữ reference đến outer scope variables — không GC'd until closure dead.
- Deep closure chains (nested closures) — scope chain lookup slightly slower, negligible.
- **Memory leak là vấn đề thực sự** — closure giữ reference forever unless explicitly released.

**Best practices**:
- **Always null/release closure when done** — prevent memory leak, especially in long-running apps.
- **Prefer primitive capture over object capture** — `const len = arr.length; return () => len;` better than `return () => arr.length;`.
- **Use `let` in loops** — each iteration gets its own closure scope, avoid var sharing bug.
- **Limit closure depth** — max 2-3层级, quá sâu = khó debug, memory overhead.
- **Memoization with care** — cache size bounded, clear cache when memory pressure.
- **Document closure intent** — comment why closure is used, what state it captures.
- **Prefer classes for complex state** — class + `#private` fields clearer than deep closures.
- **Use WeakRef for optional retention** — ES2021 `WeakRef` allow GC to collect underlying object.
- **Avoid closure in hot loops** — function call + closure overhead can matter in tight loops.
- **Test for memory leaks** — Chrome DevTools Memory panel, look for retained closures.

**Quy tắc "3 nên — 3 không"**:
- ✅ Nên null reference khi không cần closure nữa.
- ✅ Nên dùng `let` trong loop + async callback.
- ✅ Nên document closure purpose in code.
- ❌ Không nên closure giữ large object không cần thiết.
- ❌ Không nên nested closure quá 3层级.
- ❌ Không nên quên release closure trong long-running app.

## 🔗 Liên kết chéo

- Tổng quan Scope & Closure: `09_functions/02_scope-closure-strict-mode/README.md` — overview.
- IIFE: `09_functions/02_scope-closure-strict-mode/02_iife/` — IIFE + closure = module pattern.
- Strict mode: `09_functions/02_scope-closure-strict-mode/01_strict-mode/` — strict mode effect on closure.
- Call stack: `09_functions/02_scope-closure-strict-mode/05_function-stack/` — closure execution context.
- Arrow functions: `09_functions/01_parameters-and-arrow/03_arrow-functions/` — arrow trong closure.
- Recursion: `09_functions/01_parameters-and-arrow/04_recursion/` — recursive closure (memoization).
- Arguments object: `09_functions/01_parameters-and-arrow/05_arguments-object/` — arguments trong closure.
- Callbacks: `09_functions/01_parameters-and-arrow/01_callbacks/` — callback trong closure context.
- Non-blocking I/O: `09_functions/02_scope-closure-strict-mode/04_non-blocking-io/` — closure trong async callbacks.
