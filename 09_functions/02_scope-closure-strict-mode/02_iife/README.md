# IIFE — Hàm được gọi ngay lập tức (Thực hành chi tiết) — [Level: Intermediate]

## 🔑 Khái niệm cốt lõi

**IIFE** (Immediately Invoked Function Expression) là một hàm được **định nghĩa và gọi ngay lập tức** trong cùng một biểu thức. Cú pháp điển hình:

```js
(function () {
  console.log("NOW NOW");
})();
```

Giải thích các phần:
- `(function () { ... })` — bọc hàm trong `()` để nó được hiểu là một **expression** (không phải khai báo hàm thông thường).
- `()` ngay sau đó — **gọi hàm** luôn.

IIFE còn được gọi là **self-invoking function** và tạo ra một **phạm vi riêng (private scope)**: biến bên trong không truy cập được từ ngoài, nhưng bên trong có thể dùng mọi thứ bên ngoài. Đó chính là công cụ "che giấu dữ liệu" cổ điển trước khi ES6 có module system.

Ví dụ mạnh nhất trong README — mô-đun `app2` bằng IIFE: biến `cars` giữ kín bên trong, bên ngoài chỉ thao tác qua các hàm `all`, `add`, `delete`, `update` được trả về. Điểm lợi: bên ngoài không thể đặt `app.cars = null` làm hỏng dữ liệu như phiên bản `app` thường.

**Cơ chế**: IIFE tạo một execution context mới, push lên call stack, thực thi, rồi pop ra. Biến local trong IIFE bị discard sau khi hàm return — chỉ những gì được trả về qua closure mới sống sót.

## 📐 Cấu trúc / Cú pháp

### Cú pháp cơ bản
```js
// Parentheses wrap
(function() {
  console.log("IIFE runs immediately");
})();

// Arrow IIFE
(() => {
  console.log("Arrow IIFE");
})();

// Newton's binomial (alternative wrapping)
!function() { console.log("Exclamation IIFE"); }();
+function() { console.log("Plus IIFE"); }();
-function() { console.log("Minus IIFE"); }();
~function() { console.log("Tilde IIFE"); }();
```

### IIFE với parameters
```js
(function(greeting, name) {
  console.log(greeting, name);
})("Hello", "Sơn"); // "Hello Sơn"
```

### IIFE trả về giá trị — module pattern
```js
const module = (function() {
  // Private variables
  let privateCount = 0;
  const privateItems = [];

  // Private method
  function helper() { return privateCount * 2; }

  // Public API
  return {
    increment() { return ++privateCount; },
    addItem(item) { privateItems.push(item); },
    getCount() { return privateCount; },
    getAll() { return [...privateItems]; } // return copy, not reference
  };
})();

module.increment(); // 1
module.increment(); // 2
console.log(module.getCount()); // 2
// console.log(module.privateCount); // undefined — private!
```

### IIFE với return object (enhanced)
```js
const counter = (function(initial = 0) {
  let count = initial;
  return {
    get() { return count; },
    inc() { return ++count; },
    dec() { return --count; },
    reset(val = 0) { count = val; return count; }
  };
})(10); // start from 10

console.log(counter.get()); // 10
console.log(counter.inc()); // 11
console.log(counter.dec()); // 10
```

## ✅ Điểm mạnh

1. **Tạo phạm vi riêng** — không tạo biến global, không xung đột tên khi dùng nhiều thư viện — solve namespace pollution problem.
2. **Private dữ liệu thật sự** — dễ dàng giấu trạng thái nội bộ và chỉ lộ API cần thiết qua returned object.
3. **Gọi ngay, trả về luôn kết quả/object** — gọn cho khởi tạo một lần, setup code.
4. **Là nền tảng của pattern "module pattern"** trước ES6 modules — giải pháp encapsulation đầu tiên trong JS.
5. **Gom được logic khởi tạo** — ví dụ gắn sự kiện, khởi tạo state, one-time setup — một chỗ, một lần duy nhất.
6. **Trả về object/function qua biến gán** — `const app = (function(){ ... return {...} })();` — clean assignment.
7. **Closure-based privacy** — biến private được closure giữ lại, không accessible từ external scope.
8. **No global leakage** — mọi biến trong IIFE là local, không rò rỉ ra global scope.
9. **Self-documenting** — IIFE structure signals "this is a module, here's its public API".
10. **Works in all JS environments** — browser, Node.js, strict/non-strict mode đều hoạt động.

## ⚠️ Bẫy thường gặp & Hạn chế

1. **Phải có dấu `;` trước IIFE** — nếu dòng trước kết thúc bằng biểu thức (tự động chèn `;` bị bỏ qua), dễ gây lỗi ghép hai câu lệnh lại với nhau.
   ```js
   const x = 1
   (function() { console.log("iife"); })();
   // ❌ Có thể gây SyntaxError hoặc unexpected behavior
   // ✅ Luôn có ;
   const x = 1;
   (function() { console.log("iife"); })();
   ```

2. **Có thể ép bằng toán tử khác** thay `()` như `!function(){...}()`, `+`, `-`... nhưng kém đọc — không khuyến khích.
   ```js
   // Tất cả đều valid IIFE patterns
   !function() {}();
   +function() {}();
   -function() {}();
   ~function() {}();
   // ✅ Nhưng () là clear nhất — dùng parentheses
   ```

3. **IIFE tạo ra một phạm vi qua mỗi lần gọi** — tạo quá nhiều thì tốn bộ nhớ như các hàm thường (mỗi execution context tốn memory).
4. **Bản thân nó không giải quyết hoàn toàn việc chia module lớn** — hiện đại nên dùng ES modules (`import`/`export`) thay IIFE.
5. **Cú pháp dễ quên dấu `()` gọi** — viết sai thành khai báo thường (function declaration) thay vì expression.
   ```js
   // ❌ Function declaration — không phải IIFE
   function() { console.log("wrong"); }(); // SyntaxError

   // ✅ IIFE — có () wrap
   (function() { console.log("right"); })();
   ```
6. **IIFE không có tên** — khó debug, stack trace sẽ hiện `anonymous`.
7. **Cannot be hoisted** — phải định nghĩa trước khi gọi (nhưng vì gọi ngay nên không có vấn đề).
8. **Return value lost if not assigned** — `(function(){ return 42; })(); // 42 lost!`

## 💡 Khi nào dùng

1. **Bọc code khởi tạo/khởi tạo một lần** (hide helpers, khởi tạo state) — setup code chạy một lần duy nhất.
2. **Tạo module "private"** cho dữ liệu nhạy cảm — như ví dụ `app2` với `cars` được giữ kín.
3. **Tránh xung đột biến toàn cục** khi nhúng nhiều thư viện — mỗi thư viện trong IIFE riêng.
4. **Khi cần một phạm vi đóng gói nhanh** trong script không có module system — legacy code, browser < ES2015.
5. **Plugin/widget initialization** — encapsulate plugin state, expose public API.
6. **One-time configuration** — read config from DOM/server, compute derived state, return initialized object.
7. **Avoiding global namespace pollution** — trong page có nhiều scripts từ nhiều sources.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Cơ bản IIFE (file `app.js`)
```js
// Nội dung app.js trong thư mục
const callNow = function() {
  console.log("NOW");
};
callNow();                    // gọi thường, cần ; trước IIFE

(function() {
  console.log("NOW NOW");
})();                         // IIFE — gọi ngay khi tạo

(function PrintMessage(message) {
  console.log("Message:", message);
  return message;
})("Chao ban");               // Message: Chao ban
```

### Ví dụ 2: Module private bằng IIFE (file `app.js`)
```js
// Nội dung app.js trong thư mục
const app2 = (function() {
  const cars = []; // private — ngoài không truy cập được

  return {
    all() { return cars; },
    add(car) { cars.push(car); },
    update(index) { cars.splice(index, 1); },
    // Không expose delete/remove — chỉ thông qua update
  };
})();

app2.add("Winner 2022");
console.log(app2.all()); // ["Winner 2022"]
// console.log(app2.cars); // undefined — private!
```

### Ví dụ 3: IIFE so sánh với regular object — privacy
```js
// ❌ Regular object — properties accessible
const app = {
  cars: [],
  add(car) { this.cars.push(car); },
  all() { return this.cars; }
};
app.cars = null; // ⚠️ Có thể phá hủy data từ outside!

// ✅ IIFE — private closure
const appIIFE = (function() {
  const cars = []; // private
  return {
    add(car) { cars.push(car); },
    all() { return cars; } // return copy or reference? careful!
  };
})();
appIIFE.cars = null; // không ảnh hưởng — cars vẫn an toàn trong closure
```

### Ví dụ 4: IIFE với params — module factory
```js
const createStore = (function() {
  let storeId = 0; // private counter

  return function(name) {
    storeId++;
    const data = {};
    return {
      name,
      id: storeId,
      set(key, value) { data[key] = value; },
      get(key) { return data[key]; },
      getAll() { return { ...data }; } // return copy
    };
  };
})();

const store1 = createStore("Shop A");
const store2 = createStore("Shop B");
store1.set("item", "book");
console.log(store1.get("item")); // "book"
console.log(store2.get("item")); // undefined — separate instances
console.log(store1.id); // 1
console.log(store2.id); // 2 — storeId được closure giữ
```

### Ví dụ 5: IIFE return function — counter pattern
```js
// Tạo counter với closure
const createCounter = (function() {
  let id = 0; // private ID counter

  return function(label = "counter") {
    id++;
    let count = 0;
    return {
      label: `${label}_${id}`,
      get() { return count; },
      inc() { return ++count; },
      dec() { return --count; }
    };
  };
})();

const c1 = createCounter("A");
const c2 = createCounter("B");
console.log(c1.inc()); // 1
console.log(c2.inc()); // 1
console.log(c1.label); // "A_1"
console.log(c2.label); // "B_2"
// id và count của mỗi counter độc lập — closure đảm bảo
```

### Ví dụ 6: IIFE — one-time setup
```js
const app = (function() {
  // One-time initialization
  const config = { debug: false, version: "1.0.0" };
  const events = {};

  // Private helper
  function emit(event, data) {
    if (events[event]) {
      events[event].forEach(fn => fn(data));
    }
  }

  // Public API
  return {
    on(event, fn) {
      (events[event] = events[event] || []).push(fn);
      return this; // chainable
    },
    off(event, fn) {
      if (events[event]) {
        events[event] = events[event].filter(f => f !== fn);
      }
    },
    emit,
    getConfig() { return { ...config }; }
  };
})();

app.on("click", (data) => console.log("clicked", data));
app.emit("click", { x: 10, y: 20 }); // "clicked { x: 10, y: 20 }"
// events và config không accessible từ outside
```

### Ví dụ 7: IIFE với arrow function
```js
// Arrow IIFE — lưu ý: không có arguments riêng
const result = (() => {
  const secret = 42;
  return secret;
})();
console.log(result); // 42

// Arrow IIFE với params
const greet = ((name) => `Hello, ${name}!`)("Sơn");
console.log(greet); // "Hello, Sơn!"

// ❌ Arrow IIFE không có this binding — cẩn thận
const obj = {
  value: 10,
  // ❌ Arrow IIFE — this không trỏ obj
  // getValue: (() => this.value)(),
  // ✅ Function expression IIFE — this trỏ obj
  getValue() {
    return (function() { return this.value; }).call(this);
  }
};
console.log(obj.getValue()); // 10
```

### Ví dụ 8: IIFE — avoiding global pollution
```js
// Script 1 — library A
(function(global) {
  global.LibA = {
    name: "Library A",
    version: "1.0"
  };
})(window || global);

// Script 2 — library B
(function(global) {
  global.LibB = {
    name: "Library B",
    version: "2.0"
  };
})(window || global);

// Global scope chỉ có LibA và LibB — không có biến rogue
console.log(LibA.name); // "Library A"
console.log(LibB.name); // "Library B"
```

### Ví dụ 9: IIFE với AMD/UMD pattern (legacy module systems)
```js
// UMD — Universal Module Definition
(function(root, factory) {
  if (typeof define === "function" && define.amd) {
    // AMD (RequireJS)
    define([], factory);
  } else if (typeof module === "object" && module.exports) {
    // CommonJS (Node.js)
    module.exports = factory();
  } else {
    // Browser global
    root.myModule = factory();
  }
})(typeof self !== "undefined" ? self : this, function() {
  // Module implementation
  function privateFn() { return "private"; }
  return {
    publicFn() { return privateFn(); }
  };
});
```

### Ví dụ 10: IIFE — security sandbox
```js
// IIFE tạo sandbox — cách thức hoạt động của một số JS sandbox tools
const sandbox = (function() {
  const dangerous = {
    eval: eval,
    Function: Function,
    process: process // Node.js
  };

  return function(code) {
    // In real sandbox, you'd restrict access to dangerous globals
    // Here we just demonstrate the pattern
    try {
      return new Function(
        "console",
        `"use strict"; return (${code});`
      )(console);
    } catch (e) {
      return { error: e.message };
    }
  };
})();

console.log(sandbox("2 + 2")); // 4
console.log(sandbox("window.location")); // error (no window in Function scope)
```

## 🔬 So sánh với alternatives

| Phương án | Ưu điểm | Nhược điểm | Phù hợp khi |
|---|---|---|---|
| **IIFE** | Private scope, no deps | Verbose, manual management | Legacy code, simple modules |
| **ES Modules** | Native, tree-shaking, import/export | Browser/Node support needed | Modern projects (recommended) |
| **Class + #private** | Native privacy, OOP style | ES2022+, no IE support | Class-based architecture |
| **Object literal** | Simple, no boilerplate | No privacy, all public | Simple data containers |
| **Module pattern (Crockford)** | Proven, well-known | Verbose IIFE wrapper | Legacy codebases |

## 📊 Performance & Best Practices

**Performance**:
- IIFE có overhead tương đương function call — negligible.
- Closure trong IIFE giữ reference — memory được giữ until IIFE result GC'd.
- Multiple IIFEs — mỗi IIFE tạo new execution context — acceptable cost.
- IIFE return value assigned to variable — variable holds reference to returned object, not the IIFE scope.

**Best practices**:
- **Luôn có `;` trước IIFE** — phòng ngừa script concatenation issues.
- **Dùng `()` wrap** — clear nhất, readable nhất, recommended pattern.
- **Assign result to named variable** — `const module = (function(){ ... })();` — easier to debug.
- **Prefer ES modules** cho code mới — IIFE là legacy pattern, ES modules cleaner và có tooling support.
- **Keep IIFE small** — nếu logic phức tạp, split thành named functions bên trong.
- **Use arrow IIFE** cho concise one-liners — `const double = ((x) => x * 2)(5);`
- **Don't overuse** — mỗi IIFE thêm complexity, dùng khi thực sự cần privacy.
- **Return only public API** — keep internals truly private, don't expose internal references.
- **Test IIFE module** — ensure private state cannot be mutated from outside.

**Quy tắc "3 nên — 3 không"**:
- ✅ Nên dùng IIFE khi cần private scope trong legacy code.
- ✅ Nên luôn có `;` trước IIFE.
- ✅ Nên assign result to named constant.
- ❌ Không nên dùng IIFE thay ES modules trong project mới.
- ❌ Không nên quên `;` trước IIFE — risk syntax error.
- ❌ Không nên expose internal references qua returned object.

## 🔗 Liên kết chéo

- Tổng quan Scope & Closure: `09_functions/02_scope-closure-strict-mode/README.md` — overview of all concepts.
- Strict mode: `09_functions/02_scope-closure-strict-mode/01_strict-mode/` — strict mode trong IIFE context.
- Closure: `09_functions/02_scope-closure-strict-mode/03_closure/` — closure là cơ chế enabling IIFE privacy.
- Call stack: `09_functions/02_scope-closure-strict-mode/05_function-stack/` — IIFE execution context on stack.
- Arrow functions: `09_functions/01_parameters-and-arrow/03_arrow-functions/` — arrow IIFE pattern.
- Functions overview: `09_functions/README.md` — where IIFE fits in the function learning path.
- Callbacks: `09_functions/01_parameters-and-arrow/01_callbacks/` — callback trong IIFE module.
- Exceptional handling: `07_exceptional-handling/` — error handling trong IIFE.
