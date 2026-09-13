# Arrow function — lexical `this` (Chi tiết) — [Level: Advanced]

## 🔑 Khái niệm cốt lõi

"Lexical `this`" nghĩa là `this` của arrow function được xác định bởi **cấu trúc code (scope lồng nhau)** tại nơi nó được khai báo, không phải cách nó được gọi. Khi inside một arrow function, `this` chính là `this` của hàm/scope bao bọc nó **tại thời điểm khai báo**.

Điều này khác hoàn toàn với function thường — function thường có **dynamic `this`** (xác định lúc gọi), trong khi arrow có **static `this`** (xác định lúc khai báo). once the arrow is created, its `this` can never change.

Cơ chế hoạt động: mỗi lần engine gặp arrow function, nó "ghi nhớ" `this` hiện tại của execution context bao quanh. Khi arrow được gọi sau đó (dù ở đâu, bằng cách nào), engine dùng `this` đã ghi nhớ — không tính toán lại.

```js
const outer = {
  x: 42,
  make() {
    // make() có this = outer
    const fn = () => console.log(this.x);
    // fn ghi nhớ this = outer tại thời điểm khai báo
    fn(); // → 42, dù fn được gọi thế nào sau đó
  },
};
```

## 📐 Cấu trúc / Cú pháp

### Mức độ lexical binding

```
Global scope        → this = window/globalThis
  └─ Function A     → this = A's caller
      └─ Arrow 1    → this = A's this (kế thừa)
          └─ Arrow 2 → this = A's this (kế thừa 2 cấp)
```

### Bảng so sánh lexical vs dynamic

| Đặc tính | Arrow function (lexical) | Function thường (dynamic) |
|----------|--------------------------|---------------------------|
| `this` xác định lúc | Khai báo | Gọi hàm |
| `call`/`apply`/`bind` ảnh hưởng | ❌ Không | ✅ Có |
| Dùng làm method | ❌ Không nên | ✅ Được |
| Dùng làm callback | ✅ Perfect | ⚠️ Cần bind |
| Readable `this` | Nhìn lên scope chain | Nhìn xuống call-site |

### Các quy tắc kế thừa `this`

1. **Arrow trong global scope** → `this` = `globalThis`
2. **Arrow trong function thường** → `this` = function thường's `this`
3. **Arrow trong method** → `this` = method's `this` (object gọi method)
4. **Arrow trong arrow** → kế thừa từ arrow cha (không từ object)

## ✅ Điểm mạnh — Tại sao nên dùng

1. **Giữ `this` ổn định trong callback bất đồng bộ** — `setTimeout(() => this.x, 0)` luôn đúng object ban đầu.
2. **Không cần `const that = this` hay `.bind(this)`** — code sạch, ít bug hơn.
3. **Nhất quán cho mọi nesting depth** — càng lồng sâu, `this` càng rõ ràng theo từng cấp.
4. **Dễ suy luận** — nhìn vào nơi khai báo là biết `this`, không cần trace call-site.
5. **Perfect cho React hooks** — `useEffect(() => { ... }, [])` giữ context component.
6. **Tránh được "this lost" bug** — nguyên nhân số 1 của junior developer.
7. **Kết hợp với Promise chain** — `.then(() => this.method())` an toàn.
8. **Tương thích với IIFE và module pattern** — giữ context xuyên suốt.

## ⚠️ Bẫy thường gặp & Hạn chế

### Bẫy 1: `this` bị "chốt" từ scope khai báo — không đổi được

```js
const globalThisVal = { x: "global" };
const obj = { x: "obj" };

const arrow = () => console.log(this.x);
arrow.call(obj);  // "global" — không đổi được, đã chốt lúc khai báo
```

### Bẫy 2: Arrow trong object literal — `this` là global, không phải object

```js
const o = {
  x: 1,
  method: () => console.log(this.x)  // undefined — this = globalThis
};
o.method();
```

### Bẫy 3: Deeply nested arrows — khó theo dõi `this`

```js
function outer() {
  const a = () => {
    const b = () => {
      const c = () => console.log(this); // this của outer()
    };
    c();
  };
  a();
}
outer.call({ x: 99 }); // {x: 99} — all the way up
```

### Bẫy 4: Không dùng được làm method cần `this` động

```js
const calculator = {
  base: 10,
  // ❌ Arrow không biết base vì this = global
  add: (n) => this.base + n,
};
calculator.add(5); // NaN (this.base = undefined)
```

### Bẫy 5: Scope bên ngoài là global → arrow `this` = global

```js
const standaloneArrow = () => this;
standaloneArrow(); // window/globalThis — có thể là bug nếu không để ý
```

## 💡 Khi nào dùng — Tình huống thực tế

1. **Callback trong `setTimeout`/`setInterval`** — giữ `this` của component/object.
2. **`Promise.then` chain** — `.then(() => this.processData())`
3. **`fetch().then()`** — parse JSON rồi xử lý với `this.state`.
4. **React class component** — `this.handleClick.bind(this)` không cần nếu dùng arrow.
5. **Event handler nội bộ** — method của class gọi callback arrow giữ context.
6. **Nested callbacks** — vài tầng callback lồng nhau, arrow duy trì context xuyên suốt.
7. **IIFE pattern** — `(function() { const that = this; ... })()` thay bằng arrow.
8. **Functional programming helpers** — `compose`, `pipe` với arrow giữ scope đúng.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Lexical this cơ bản

```js
const outer = {
  x: 42,
  make() {
    // make()'s this = outer
    const fn = () => console.log(this.x);
    // fn captures this = outer at declaration time
    fn(); // → 42
  },
};
outer.make();
```

### Ví dụ 2: setTimeout giữ context

```js
const o = {
  x: 1,
  hi() {
    setTimeout(() => {
      // arrow's this = hi()'s this = o
      console.log(this.x); // → 1 (dù chạy trễ, vẫn giữ this của hi())
    }, 0);
  },
};
o.hi();
```

### Ví dụ 3: So sánh với function thường (sai)

```js
const o = {
  x: 1,
  hi() {
    setTimeout(function () {
      // function thường → default binding → window
      console.log(this.x); // → undefined (hoặc window.x)
    }, 0);
  },
};
o.hi();
```

### Ví dụ 4: Promise chain với lexical this

```js
const apiClient = {
  baseUrl: "https://jsonplaceholder.typicode.com",
  async fetchData(endpoint) {
    const res = await fetch(`${this.baseUrl}${endpoint}`);
    // arrow giữ this = apiClient xuyên suốt chain
    return res.json();
  }
};
apiClient.fetchData("/posts/1").then(data => console.log(data));
```

### Ví dụ 5: Deep nesting — tất cả arrow đều cùng one this

```js
function configure() {
  const config = { debug: true };
  
  const setup = () => {
    const init = () => {
      const ready = () => {
        console.log(this.debug); // → undefined (this của configure() = global/undefined)
      };
      ready();
    };
    init();
  };
  setup();
}
configure.call(config); // still undefined — configure's this is set by call but arrow captures at declaration
```

### Ví dụ 6: Thực tế — React-style component pattern

```js
class Button {
  constructor(label) {
    this.label = label;
    this.count = 0;
  }
  
  render() {
    return {
      onClick: () => {
        // arrow kế thừa this từ render() → this = Button instance
        this.count++;
        console.log(`${this.label}: clicked ${this.count} times`);
      }
    };
  }
}

const btn = new Button("Submit");
const handler = btn.render().onClick;
handler(); // "Submit: clicked 1 times" — this vẫn đúng!
```

### Ví dụ 7: Arrow trong object method — khi nào đúng, khi nào sai

```js
// ✅ ĐÚNG: arrow trong method, kế thừa this của method
const tracker = {
  visits: 0,
  log() {
    setTimeout(() => {
      this.visits++; // ✅ this = tracker
      console.log("Visit:", this.visits);
    }, 100);
  }
};

// ❌ SAI: arrow làm property method
const trackerBad = {
  visits: 0,
  log: () => {
    setTimeout(() => {
      this.visits++; // ❌ this = globalThis, không phải trackerBad
    }, 100);
  }
};
```

## 🔬 So sánh với alternatives

| Cách | `this` khi gọi | Ưu điểm | Nhược điểm |
|------|----------------|---------|------------|
| Arrow lexical | Kế thừa từ scope khai báo | Dự đoán, không cần bind | Không đổi được |
| Function dynamic | Xác định lúc gọi | Linh hoạt | Dễ mất context |
| `.bind(this)` | Ép thành object | Giữ function thường | Cần nhớ bind mỗi chỗ |
| `const that = this` | Tham chiếu closure | Works in all environments | Dài dòng |

## 📊 Performance & Best Practices

- **Arrow function được tối ưu tốt** bởi V8 và engine hiện đại — callback pattern là use case chính.
- **Không bind lặp lại trong loop** — tạo closure mới mỗi iteration, dùng arrow thay thế.
- **Class field arrow methods** (`method = () => {}`) tự bind `this` — pattern phổ biến trong React.
- **Deep nesting > 3 cấp** — nên refactor, arrow quá sâu khó debug `this`.
- **Test `this` bằng `console.log`** — nếu kết quả bất ngờ, trace ngược lên scope khai báo.

## 🔗 Liên kết chéo

- **Xem thêm:** `10_this-keyword/05_arrow-function` — arrow function không có `this` riêng
- **Xem thêm:** `10_this-keyword/04_event-handler` — arrow sai trong event handler
- **Xem thêm:** `10_this-keyword/README` — 4 quy tắc this overview
- **Xem thêm:** `11_function-borrowing/01_bind` — alternative khi cần bind explicit
- **Xem thêm:** `09_functions/01_parameters-and-arrow/03_arrow-functions` — cú pháp arrow chi tiết
- **Xem thêm:** `12_asynchronous-javascript/02_callbacks-promises/02_async-await` — async/await + arrow pattern
