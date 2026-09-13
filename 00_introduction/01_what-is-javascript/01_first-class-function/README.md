# First-class Function (Hàm hạng nhất) — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

Một ngôn ngữ được gọi là có **first-class function** (hàm hạng nhất) khi các hàm trong ngôn ngữ đó được đối xử như **bất kỳ giá trị nào khác** — tức hàm "bình đẳng" với số, chuỗi, boolean, object. Trong JavaScript, điều này có nghĩa bạn có thể:

1. **Gán hàm cho một biến** — hàm không cần tên (anonymous function), được lưu vào biến giống như số hay chuỗi.
2. **Truyền hàm như một đối số** cho một hàm khác — đây chính là nền tảng của **callback**, giúp bạn "gửi hành vi" chứ không chỉ "gửi dữ liệu".
3. **Trả về một hàm từ một hàm khác** — nền tảng của **higher-order function** và **closure**, cho phép hàm "ghi nhớ" trạng thái từ scope ngoài.

Cơ chế này được JavaScript engine xử lý như thế nào? Khi bạn viết `const fn = () => {}`, engine tạo một **function object** trong bộ nhớ — function object cũng là object (xem thêm `02_data-types/02_objects-and-prototype/02_functions-as-objects/`), nên nó có thể được gán, truyền, trả về y hệt một object bình thường. Mỗi khi hàm được gọi `fn()`, engine đẩy một **execution context** mới lên call stack, thực thi thân hàm, rồi pop context đó ra.

## 📐 Cấu trúc / Cú pháp

```js
// 1. Gán hàm cho biến (function expression)
const greet = function (name) {
  return `Xin chào, ${name}!`;
};
// Hoặc arrow function (ES6)
const greetArrow = (name) => `Xin chào, ${name}!`;

// 2. Truyền hàm làm đối số (callback)
function chayXửLý(dữLiệu, hàmXửLý) {
  return hàmXửLý(dữLiệu);
}
chayXửLý("Nam", greet);              // "Xin chào, Nam!"

// 3. Trả về hàm từ hàm (higher-order function)
function nhânVới(x) {
  return function (y) {
    return x * y;
  };
}
const nhân3 = nhânVới(3);
console.log(nhân3(10));              // 30
```

Lưu ý quan trọng: khi truyền hàm làm đối số, viết **tên hàm không có `()`** — viết `greet()` là gọi hàm và truyền kết quả, viết `greet` mới là truyền **tham chiếu hàm**.

## ✅ Điểm mạnh — Tại sao nên dùng

| # | Điểm mạnh | Lý do & Khi nào |
|---|-----------|----------------|
| 1 | **Callback & asynchronous** | `setTimeout(() => {...}, 1000)`, `fetch(url).then(...)`, `addEventListener` — tất cả đều dựa trên first-class function |
| 2 | **Higher-order functions** | `map`, `filter`, `reduce` nhận function làm đối số, trả về kết quả mới — code ngắn gọn, dễ đọc |
| 3 | **Closure** | Hàm trả về "nhớ" biến của scope ngoài, tạo private state, factory function |
| 4 | **Function composition** | Ghép nhiều hàm nhỏ thành pipeline phức tạp: `compose(f, g, h)(x)` |
| 5 | **Event-driven programming** | Gắn handler vào sự kiện DOM (`click`, `submit`, `keydown`) một cách tự nhiên |
| 6 | **Middleware pattern** | Truyền hàm vào hàm để mở rộng hành vi — phổ biến trong Express, Redux |
| 7 | **Strategy pattern** | Đóng gói thuật toán khác nhau thành hàm, chọn lúc runtime |
| 8 | **Memoization** | Lưu kết quả tính toán theo đối số, tránh tính lại — dùng closure + object cache |

## ⚠️ Bẫy thường gặp & Hạn chế

| # | Bẫy | Ví dụ code |
|---|-----|-----------|
| 1 | **Truyền hàm sai**: viết `greeting(sayHello())` thay vì `greeting(sayHello)` | Truyền kết quả thay vì bản thân hàm — `TypeError` nếu kết quả không phải hàm |
| 2 | **Closure giữ biến lâu hơn dự kiến** | Vòng lặp `for` với `var` + setTimeout: tất cả callback cùng đọc biến cuối cùng |
| 3 | **Memory leak qua closure** | Giữ tham chiếu tới DOM element lớn trong closure lâu — GC không thu hồi được |
| 4 | **Callback hell** | Lồng quá nhiều callback → code khó đọc, khó debug; dùng Promise/async-await thay thế |
| 5 | **`this` bị mất** | `const obj = { fn: function(){ return this } }`, truyền `obj.fn` vào setTimeout → `this` trỏ `window` |
| 6 | **Arrow function không có `arguments`** | `const f = () => arguments` → `ReferenceError`; dùng rest params `(...args)` thay thế |
| 7 | **Hàm trả về arrow với body block** | `const fn = (x) => { return x * 2; }` — `{}` là block, phải có `return` tường minh |
| 8 | **Nesting sâu gây overhead** | Function creation cost trong vòng lặp — mỗi lần lặp tạo function object mới |

## 💡 Khi nào dùng — Tình huống thực tế

1. **Xử lý bất đồng bộ** — `setTimeout`, `setInterval`, `Promise.then()`, `fetch().catch()` đều nhận callback.
2. **Biến đổi mảng** — `arr.map(fn)`, `arr.filter(fn)`, `arr.reduce(fn, init)` là 3 method phổ biến nhất.
3. **Event handling** — `element.addEventListener('click', handler)` truyền handler function.
4. **Factory function** — `function tạoUser(role) { return { role, isAdmin: role === 'admin' }; }`
5. **Middleware / HOC** — Express middleware, React Higher-Order Component, Redux enhancer.
6. **Debounce / Throttle** — giới hạn tần suất gọi hàm (tìm kiếm tự động hoàn thành).
7. **Memoization** — cache kết quả hàm expensive tính toán (Fibonacci, recursive).
8. **Strategy pattern** — chọn thuật toán sort/search tại runtime qua hàm được truyền vào.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Gán hàm cho biến + gọi qua biến

```js
// Gán function expression cho biến
const binhPhuong = function (n) {
  return n * n;
};
console.log(binhPhuong(5));          // 25

// Arrow function tương đương
const binhPhuongArrow = (n) => n * n;
console.log(binhPhuongArrow(5));     // 25
```

### Ví dụ 2: Truyền hàm làm đối số (callback)

```js
// Hàm nhận một function làm đối số
function apDung(hàm, giáTri) {
  return hàm(giáTri);
}

const congMot = (n) => n + 1;
const nhanHai = (n) => n * 2;

console.log(apDung(congMot, 5));     // 6
console.log(apDung(nhânHai, 5));     // 10
```

### Ví dụ 3: Trả về hàm từ hàm (closure cơ bản)

```js
// Factory function tạo bộ nhân
function taoBộNhân(nhânSố) {
  // Trả về một hàm "nhớ" nhânSố từ scope ngoài
  return function (số) {
    return số * nhânSố;
  };
}

const nhânBa = taoBộNhân(3);
const nhânMười = taoBộNhân(10);
console.log(nhânBa(7));              // 21
console.log(nhânMười(7));            // 70
// Nhân số 3 và 10 được "nhớ" trong closure của mỗi hàm
```

### Ví dụ 4: Higher-order function — map / filter / reduce

```js
const sốs = [1, 2, 3, 4, 5];

// map: biến đổi từng phần tử → mảng mới
const gấpĐôi = sốs.map((n) => n * 2);
console.log(gấpĐôi);                 // [2, 4, 6, 8, 10]

// filter: giữ lại phần tử thỏa điều kiện
const sốChẵn = sốs.filter((n) => n % 2 === 0);
console.log(sốChẵn);                 // [2, 4]

// reduce: tích lũy về một giá trị duy nhất
const tổng = sốs.reduce((t, n) => t + n, 0);
console.log(tổng);                   // 15
```

### Ví dụ 5: Promise callback — real-world example

```js
// setTimeout nhận callback, gọi sau 1 giây
setTimeout(() => {
  console.log("Chạy sau 1 giây");
}, 1000);

// Promise .then() nhận callback khi resolve
Promise.resolve("Dữ liệu đã sẵn sàng")
  .then((dữLiệu) => {
    console.log(dữLiệu);             // "Dữ liệu đã sẵn sàng"
    return dữLiệu.toUpperCase();
  })
  .then((result) => {
    console.log(result);             // "DỮ LIỆU ĐÃ SẴN SÀNG"
  });
```

### Ví dụ 6: Debounce — hạn chế tần suất gọi hàm

```js
// Debounce: chờ đến khi user ngưng gõ mới xử lý
function debounce(hàm, trễ = 300) {
  let timer;
  return function (...args) {
    clearTimeout(timer);             // hủy timer cũ
    timer = setTimeout(() => {
      hàm.apply(this, args);         // gọi hàm sau `trễ` ms
    }, trễ);
  };
}

const tìmKiếm = debounce((query) => {
  console.log(`Tìm kiếm: ${query}`);
  // Gọi API tìm kiếm tại đây
}, 500);

// Khi user gõ "javascript", chỉ gọi API khi ngưng gõ 500ms
// Input: j → a → v → a → không gọi API
// Input: ... → t → (ngưng 500ms) → gọi API với "javascript"
```

## 🔬 So sánh với alternatives

| Cách tiếp cận | Ưu điểm | Nhược điểm |
|--------------|---------|------------|
| **First-class function (JS native)** | Không cần thư viện, performance tối ưu | Dễ gây callback hell nếu lồng quá sâu |
| **Callback tradisional** | Đơn giản, hiểu rõ flow | Không xử lý được error dễ dàng trong chain |
| **Promise + async/await** | Code tuần tự, xử lý error rõ ràng, không lồng sâu | Cần hiểu event loop và microtask queue |
| **RxJS Observable** | Xử lý stream event phức tạp, compose mạnh | Learning curve cao, overhead lớn |
| **Events (EventEmitter)** | Decoupling tốt giữa producer/consumer | Khó debug event flow, leak memory nếu unlisten sai |

## 📊 Performance & Best Practices

- **Tránh tạo function trong vòng lặp** nếu không cần — mỗi lần tạo là một function object mới, tốn bộ nhớ.
- **Dùng arrow function cho callback ngắn** — code gọn, nhưng lưu ý arrow không có `this` riêng.
- **Dùng function declaration cho hàm chính** — được hoist trọn vẹn, gọi trước khi định nghĩa.
- **Arrow function `=>` có `this` lexical** — kế thừa từ scope bao quanh, phù hợp callback DOM.
- **Regular function `function` có `this` dynamic** — thay đổi tùy cách gọi, phù hợp object method.
- **Kiểm tra `typeof fn === 'function'`** trước khi gọi callback — phòng tránh runtime error.
- **Dùng rest parameter `...args`** thay vì `arguments` object trong arrow function.

## 🔗 Liên kết chéo

- Xem thêm: `00_introduction/01_what-is-javascript/02_prototype-based-programming/` — prototype chain và hàm là object
- Xem thêm: `01_variables/02_hoisting/` — function declaration được hoist, arrow function thì không
- Xem thêm: `02_data-types/02_objects-and-prototype/02_functions-as-objects/` — hàm cũng là object, có property/method
- Xem thêm: `09_functions/01_parameters-and-arrow/01_callbacks/` — callbacks chi tiết hơn
- Xem thêm: `09_functions/01_parameters-and-arrow/03_arrow-functions/` — arrow function sâu hơn
- Xem thêm: `09_functions/02_scope-closure-strict-mode/03_closure/` — closure nâng cao
- Xem thêm: `10_this-keyword/` — `this` binding trong first-class function
- Tài liệu: [MDN — First-class Function](https://developer.mozilla.org/en-US/docs/Glossary/First-class_Function), [javascript.info/function-basics](https://javascript.info/function-basics)
