# Callbacks (Hàm gọi lại) — Thực hành chi tiết — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

**Callback** là một hàm được **truyền vào như đối số của hàm khác** và được hàm đó **gọi lại** từ bên trong. Ba tính chất để nhận diện (ghi rõ trong `1_call-back.js`):

1. Nó **là một hàm**.
2. Nó **là một đối số** khi gọi hàm khác.
3. Nó **được gọi lại** bên trong hàm nhận đối số.

Ví dụ gốc trong `1_call-back.js`:

```js
function myFunction(param) {
  if (typeof param === "function") {
    param("Sơn Nguyễn");      // gọi callback
  }
}
function myCallback(value) {
  console.log("Value: ", value);
}
myFunction(myCallback);        // Value: Sơn Nguyễn
```

Sáu file trong thư mục đi từ **hiểu callback** đến **tự tái tạo các phương thức mảng**:

| File | Phương thức tái tạo | Ý nghĩa |
|---|---|---|
| `1_call-back.js` | — | định nghĩa callback cơ bản |
| `2_foreach.js` | `forEach2` | chạy callback với từng phần tử (kết hợp `for...in` + `hasOwnProperty`) |
| `3_filter.js` | `filter2` | giữ phần tử khi callback trả `true` |
| `4_some.js` | `some2` | `true` nếu có ít nhất một phần tử thỏa điều kiện |
| `5_every.js` | `every2` | `true` nếu **tất cả** phần tử thỏa điều kiện |
| `6_map.js` | `map2` | biến đổi và trả về mảng mới |

**Callback signature chuẩn** của array methods: `callback(currentValue, index, array)`.

## 📐 Cấu trúc / Cú pháp

### Callback cơ bản
```js
function myFunction(param) {
  if (typeof param === "function") {
    param("Sơn Nguyễn");
  }
}
function myCallback(value) {
  console.log("Value:", value);
}
myFunction(myCallback);
```

### Tự viết forEach2
```js
Array.prototype.forEach2 = function(callBack) {
  for (let key in this) {
    if (this.hasOwnProperty(key)) {
      callBack(this[key], key, this);
    }
  }
};
```

### Tự viết filter2
```js
Array.prototype.filter2 = function(callBack) {
  var result = [];
  for (let i = 0; i < this.length; i++) {
    if (callBack(this[i], i, this)) {
      result.push(this[i]);
    }
  }
  return result;
};
```

### Tự viết map2
```js
Array.prototype.map2 = function(callBack) {
  var result = [];
  for (let i = 0; i < this.length; i++) {
    result.push(callBack(this[i], i, this));
  }
  return result;
};
```

### Some vs Every
```js
// some: return true nếu CÓ ít nhất 1 phần tử thỏa
Array.prototype.some2 = function(callBack) {
  for (let i = 0; i < this.length; i++) {
    if (callBack(this[i], i, this)) return true; // early exit
  }
  return false;
};

// every: return true nếu TẤT CẢ phần tử thỏa
Array.prototype.every2 = function(callBack) {
  for (let i = 0; i < this.length; i++) {
    if (!callBack(this[i], i, this)) return false; // early exit
  }
  return true;
};
```

## ✅ Điểm mạnh

1. **Cách học "tự viết lại map/filter"** giúp hiểu gốc rễ các phương thức mảng phổ biến — không chỉ dùng "thuộc lòng".
2. **Callback trong `forEach`/`map`/`filter` được gọi với 3 đối số** `(giá trị, index, mảng)` — các file tái tạo thể hiện rõ điều này.
3. **`hasOwnProperty` được dùng khéo léo** để lọc các key kế thừa từ prototype (tránh duyệt nhầm `forEach2` khi dùng `for...in`).
4. **`some2`/`every2` minh họa early exit** — dừng ngay khi đã đủ kết quả, tiết kiệm thời gian.
5. **Tách từng khái niệm ra 1 file** — dễ đọc, dễ test, dễ sửa từng phần.
6. **Nền tảng cho cách hiểu về event**, API callback, Promise ở các bài sau.
7. **Hiểu callback = hiểu functional programming** cơ bản — map/reduce/filter pattern.
8. **Real-world application** — event listener, AJAX success/fail, timeout, debounce/throttle.
9. **Callback as first-class citizen** — truyền hàm như dữ liệu, trả về hàm, lưu trong biến.
10. **Early exit pattern** (`some`/`every`) — optimization quan trọng cho large arrays.

## ⚠️ Bẫy thường gặp & Hạn chế

1. **Khi tự viết phương thức bằng `for...in`**, phải dùng `hasOwnProperty` để **không duyệt cả thuộc tính prototype** — `this` của callback không đảm bảo (với arrow sẽ dùng `this` ngoài).
   ```js
   // ❌ Thiếu hasOwnProperty — duyệt cả prototype methods
   for (let key in this) {
     callBack(this[key], key, this);
   }
   // ✅ Đúng — chỉ own properties
   for (let key in this) {
     if (this.hasOwnProperty(key)) {
       callBack(this[key], key, this);
     }
   }
   ```

2. **`some` dừng ngay khi gặp phần tử thỏa mãn**; `every` dừng ngay khi gặp phần tử không thỏa — đừng nhầm ý nghĩa trả về.
   ```js
   [1, 2, 3].some(x => x > 5); // false — không có phần tử > 5
   [1, 2, 3].every(x => x > 0); // true — tất cả > 0
   [1, 2, 3].every(x => x > 0); // true (early exit tại x=1? không, check all)
   ```

3. **`map` luôn trả mảng cùng độ dài**; `filter` có thể trả mảng ngắn hơn.
   ```js
   [1, 2, 3].map(x => x * 2);      // [2, 4, 6] — cùng length
   [1, 2, 3].filter(x => x > 1);   // [2, 3] — ngắn hơn
   ```

4. **Callback không phải là hàm** → gọi sẽ lỗi `TypeError`; nên kiểm tra `typeof callback === "function"` (cách làm đúng trong `1_call-back.js`).
   ```js
   function safeCall(fn) {
     if (typeof fn !== "function") throw new TypeError("Expected a function");
     return fn();
   }
   ```

5. **Lạm dụng callback lồng sâu** sẽ rơi vào "callback hell" — gợi ý dùng Promise/async sau này.
   ```js
   // ❌ Callback hell
   step1(function(a) {
     step2(a, function(b) {
       step3(b, function(c) {
         step4(c, function(d) { ... });
       });
     });
   });
   ```

6. **`for...in` trên array với ô trống** — chỉ lặp qua ô có giá trị thực.
   ```js
   const arr = [1, 2];
   arr.length = 5;
   for (let key in arr) console.log(key); // "0", "1" — bỏ qua empty slots
   ```

7. **Callback receive wrong `this`** — nếu dùng function method thay arrow, `this` có thể không như mong đợi.
   ```js
   const obj = {
     values: [1, 2, 3],
     printAll() {
       this.values.forEach(function(v) {
         console.log(this); // window/global, not obj!
       });
     }
   };
   // ✅ Sửa: dùng arrow hoặc bind
   printAll() {
     this.values.forEach((v) => console.log(this));
   }
   ```

## 💡 Khi nào dùng

1. **Duyệt và biến đổi mảng**: `map` (đổi giá trị), `filter` (lọc), `forEach` (chạy tác động phụ).
2. **Kiểm tra sự tồn tại**: `some` (có bất kỳ), `every` (tất cả) — với early exit optimization.
3. **Xử lý sự kiện DOM**, hẹn giờ, gọi API thành công/thất bại — callback là cơ chế gốc.
4. **Truyền "hành vi" cho thư viện** (sort theo tiêu chí, validate theo rule) — dependency inversion.
5. **Async operations** — `fs.readFile(path, callback)`, `http.get(url, callback)`.
6. **Timer functions** — `setTimeout(fn, ms)`, `setInterval(fn, ms)` đều nhận callback.
7. **Higher-order components** trong React — nhận callback để trigger parent state update.
8. **Middleware pattern** — Express.js, Koa đều dựa trên callback chain.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Callback cơ bản (file `1_call-back.js`)
```js
function myFunction(param) {
  if (typeof param === "function") {
    param("Sơn Nguyễn"); // gọi callback với argument
  }
}
function myCallback(value) {
  console.log("Value:", value);
}
myFunction(myCallback); // "Value: Sơn Nguyễn"

// Arrow callback version
myFunction((value) => console.log("Arrow:", value));
```

### Ví dụ 2: Tự viết forEach2 (file `2_foreach.js`)
```js
var courses = ["HTML", "CSS", "JS"];
Array.prototype.forEach2 = function(callBack) {
  for (let key in this) {
    if (this.hasOwnProperty(key)) {
      callBack(this[key], key, this);
    }
  }
};
courses.forEach2(function(course, index, rootArray) {
  console.log(course, index, rootArray);
});
// HTML 0 ["HTML","CSS","JS"]
// CSS 1 ["HTML","CSS","JS"]
// JS 2 ["HTML","CSS","JS"]
```

### Ví dụ 3: Tự viết filter2 (file `3_filter.js`)
```js
var courses = [
  { name: "HTML", coin: 0 },
  { name: "CSS", coin: 0 },
  { name: "JS", coin: 100 },
  { name: "PHP", coin: 200 }
];
Array.prototype.filter2 = function(callBack) {
  var result = [];
  for (let i = 0; i < this.length; i++) {
    if (callBack(this[i], i, this)) {
      result.push(this[i]);
    }
  }
  return result;
};
const freeCourses = courses.filter2(c => c.coin === 0);
console.log(freeCourses); // [{name:"HTML",coin:0}, {name:"CSS",coin:0}]
```

### Ví dụ 4: Tự viết some2 (file `4_some.js`)
```js
Array.prototype.some2 = function(callBack) {
  for (let i = 0; i < this.length; i++) {
    if (callBack(this[i], i, this)) return true; // early exit
  }
  return false;
};
const hasFree = courses.some2(c => c.coin === 0);
console.log(hasFree); // true
const hasExpensive = courses.some2(c => c.coin > 500);
console.log(hasExpensive); // false
```

### Ví dụ 5: Tự viết every2 (file `5_every.js`)
```js
Array.prototype.every2 = function(callBack) {
  for (let i = 0; i < this.length; i++) {
    if (!callBack(this[i], i, this)) return false; // early exit
  }
  return true;
};
const allFree = courses.every2(c => c.coin === 0);
console.log(allFree); // false
const allHaveName = courses.every2(c => typeof c.name === "string");
console.log(allHaveName); // true
```

### Ví dụ 6: Tự viết map2 (file `6_map.js`)
```js
var courses = ["HTML", "CSS", "JS", "PHP"];
Array.prototype.map2 = function(callBack) {
  var result = [];
  for (let i = 0; i < this.length; i++) {
    result.push(callBack(this[i], i, this));
  }
  return result;
};
console.log(courses.map2((c, i) => c + " (free)"));
// ["HTML (free)", "CSS (free)", "JS (free)", "PHP (free)"]

// So sánh với native map
console.log(courses.map(c => c + " (free)")); // same result
```

### Ví dụ 7: Callback với 3 arguments — value, index, array
```js
const numbers = [10, 20, 30];
numbers.forEach(function(value, index, array) {
  console.log(`index ${index}: ${value} (of ${array.length} items)`);
});
// index 0: 10 (of 3 items)
// index 1: 20 (of 3 items)
// index 2: 30 (of 3 items)
```

### Ví dụ 8: Callback pattern trong custom utility
```js
function fetchData(url, onSuccess, onError) {
  // giả lập async
  setTimeout(() => {
    if (url === "/api/users") {
      onSuccess([{ name: "Sơn" }, { name: "An" }]);
    } else {
      onError(new Error("Not found"));
    }
  }, 100);
}

fetchData("/api/users",
  (users) => console.log("Success:", users),
  (err) => console.error("Error:", err.message)
);
// Success: [ { name: 'Sơn' }, { name: 'An' } ]
```

### Ví dụ 9: Early exit optimization — find first match
```js
function findFirst(arr, predicate) {
  for (let i = 0; i < arr.length; i++) {
    if (predicate(arr[i])) return arr[i]; // early exit — không duyệt hết
  }
  return undefined;
}
const scores = [55, 72, 91, 48, 85];
console.log(findFirst(scores, s => s >= 90)); // 91 — dừng ngay, không check 48, 85
```

### Ví dụ 10: Callback chaining — pipeline pattern
```js
function pipe(value, ...fns) {
  return fns.reduce((acc, fn) => fn(acc), value);
}
const result = pipe(
  [1, 2, 3, 4, 5],
  arr => arr.filter(x => x > 2),  // [3, 4, 5]
  arr => arr.map(x => x * 2),      // [6, 8, 10]
  arr => arr.reduce((a, b) => a + b, 0) // 24
);
console.log(result); // 24
```

## 🔬 So sánh với alternatives

| Phương án | Ưu điểm | Nhược điểm | Phù hợp khi |
|---|---|---|---|
| Callback | Đơn giản, native JS | Callback hell khi nested sâu | Simple async, event handlers |
| Promise | Chainable, error handling | Learning curve, boilerplate | Complex async flows |
| `async/await` | Code đồng bộ-like | Same as Promise underneath | Modern async code (recommended) |
| Observable | Streaming, multiple values |RxJS heavy, overkill for simple cases | Real-time data, complex streams |
| Event emitter | Decoupled, pub/sub | Manual management | Complex event systems |

## 📊 Performance & Best Practices

**Performance**:
- Callback invocation có overhead nhỏ (~10-20% so với inline code) — acceptable trong 99% cases.
- `some`/`every` early exit — quan trọng cho large arrays, tránh unnecessary iterations.
- Tự viết `forEach2`/`map2` chậm hơn native ~2-3x do prototype chain lookup — chỉ để học, không dùng production.

**Best practices**:
- **Luôn check `typeof callback === "function"`** trước khi gọi — prevent TypeError.
- **Dùng arrow function cho callback ngắn** — giữ `this` từ outer scope.
- **Early exit trong `some`/`every`** — tiết kiệm iterations khi đã có kết quả.
- **Avoid callback hell** — refactor thành Promise/async-await khi >3 levels.
- **Named callback** thay anonymous khi callback phức tạp — dễ debug, test.
- **Error-first callback pattern** (Node.js convention): `callback(error, result)`.
- **Don't mutate input array** trong callback — dùng `map` thay `forEach` + push.
- **Cache callback reference** nếu gọi nhiều lần — avoid re-creation overhead.

**Quy tắc "3 nên — 3 không"**:
- ✅ Nên dùng `typeof fn === "function"` guard.
- ✅ Nên dùng early exit trong `some`/`every`.
- ✅ Nên dùng named callback cho complex logic.
- ❌ Không nên nested callback >3 levels.
- ❌ Không nên mutate array trong callback.
- ❌ Không nên tạo callback mới trong vòng lặp tight.

## 🔗 Liên kết chéo

- Tổng quan Functions: `09_functions/README.md` — khái niệm hàm, first-class citizens.
- Arrow functions: `09_functions/01_parameters-and-arrow/03_arrow-functions/` — arrow trong callback.
- Builtin functions: `09_functions/01_parameters-and-arrow/02_builtin-functions/` — setTimeout, setInterval.
- Recursion: `09_functions/01_parameters-and-arrow/04_recursion/` — recursive callback pattern.
- Arguments object: `09_functions/01_parameters-and-arrow/05_arguments-object/` — arguments trong callback.
- Scope & Closure: `09_functions/02_scope-closure-strict-mode/03_closure/` — closure trong callback.
- Non-blocking I/O: `09_functions/02_scope-closure-strict-mode/04_non-blocking-io/` — callback trong async context.
- Loops: `05_loops-and-iterations/01_loops/` — loop kết hợp callback.
- Operators: `08_expressions-and-operators/01_operators/5_toan-tu-logical.js` — logical operators trong callback condition.
