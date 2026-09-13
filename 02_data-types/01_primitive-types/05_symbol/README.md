# Symbol — [Level: Intermediate]

## 🔑 Khái niệm cốt lõi

**Symbol** là kiểu primitive **duy nhất (unique)** và **bất biến (immutable)**. Mỗi lần gọi `Symbol("mô tả")` ta nhận một instance mới **không bao giờ trùng** với Symbol khác — ngay cả khi cùng mô tả:

```js
const s1 = Symbol("id");
const s2 = Symbol("id");
console.log(s1 === s2); // false ← mỗi Symbol là duy nhất!
```

**Mô tả (description)** chỉ dùng để debug — không ảnh hưởng giá trị:

```js
const a = Symbol("foo");
const b = Symbol("foo");
console.log(a.description); // "foo"
console.log(b.description); // "foo"
console.log(a === b);       // false — cùng description nhưng khác symbol
```

### Công dụng chính: làm key ẩn (hidden key) cho object

Khác với string key, **Symbol key không xuất hiện** trong `Object.keys()`, `for...in`, hay `JSON.stringify()` — rất hợp để làm "private field" trước khi ES2022 có `#private`:

```js
const s1 = Symbol("id");
const obj = {
  name: "A",
  [s1]: 42,               // computed property key — symbol key
};

console.log(Object.keys(obj));               // ["name"] ← không thấy s1
console.log(Object.getOwnPropertySymbols(obj)); // [Symbol(id)] ← chỉ thấy qua API này
console.log(obj[s1]);                        // 42 — truy cập bằng chính biến symbol
```

> Muốn "liệt kê" các Symbol key thì dùng `Object.getOwnPropertySymbols(obj)`.

### Well-known Symbols (built-in symbols)

JavaScript quy ước một loạt `Symbol.xxx` để móc vào hành vi nội bộ của object. Hai ví dụ kinh điển:

**`Symbol.iterator`** — đánh dấu object "iterate được" (dùng trong `for...of`, spread):

```js
const arr = [1, 2];
console.log(arr[Symbol.iterator].toString());
// function values() { [native code] }

// Object tự thân đã có iterator — nên for...of làm việc được
for (const item of arr) {
  console.log(item); // 1, 2
}
```

**`Symbol.toStringTag`** — tùy biến kết quả `Object.prototype.toString`:

```js
const customObj = { [Symbol.toStringTag]: "MyType" };
console.log(Object.prototype.toString.call(customObj));
// "[object MyType]" — thay vì "[object Object]"
```

**Các well-known symbol phổ biến:**

| Symbol | Mục đích |
|--------|----------|
| `Symbol.iterator` | Định nghĩa default iterator cho `for...of` |
| `Symbol.asyncIterator` | Định nghĩa async iterator cho `for await...of` |
| `Symbol.toStringTag` | Tùy biến `Object.prototype.toString.call(obj)` |
| `Symbol.toPrimitive` | Tùy biến chuyển object về primitive (`[Symbol.toPrimitive](hint)`) |
| `Symbol.hasInstance` | Tùy biến `instanceof` check |
| `Symbol.match`, `Symbol.replace`, `Symbol.search`, `Symbol.split` | RegExp method overrides |

## 📐 Cấu trúc nhóm

```
02_data-types/01_primitive-types/05_symbol/
├── README.md         ← bài này
└── app.js            ← demo symbol usage
    └── index.html
```

## ✅ Điểm mạnh — Tại sao nên dùng symbol

| # | Điểm mạnh | Lý do |
|---|-----------|-------|
| 1 | **Bảo đảm duy nhất** | Không bao giờ trùng khóa — tránh ghi đè ngẫu nhiên từ bên ngoài |
| 2 | **Ẩn với vòng lặp/Object.keys** | Thêm metadata mà không "vấy bẩn" dữ liệu enumerable |
| 3 | **Truy cập cần đúng biến symbol** | Tự nhiên thành "private" — code khác không biết key tồn tại |
| 4 | **Well-known Symbols tùy biến hành vi** | `Symbol.iterator`, `Symbol.toStringTag` — override built-in behavior |
| 5 | **Là primitive — nhẹ** | Memory footprint nhỏ, được nhiều thư viện (React key cache, redux) sử dụng |
| 6 | **Mixin pattern an toàn** | Ghép nhiều prototype không sợ name collision |

## ⚠️ Bẫy thường gặp & Hạn chế

| # | Bẫy | Ví dụ | Cách tránh |
|---|-----|-------|-----------|
| 1 | **Symbol không phải private hard** | `Object.getOwnPropertySymbols(obj)` vẫn liệt kê được | ES2022 dùng `#privateField` cho private thật sự |
| 2 | **`JSON.stringify` bỏ qua Symbol keys** | `JSON.stringify({[Symbol("x")]:1})` → `"{}"` | Không dùng symbol cho dữ liệu cần serialize |
| 3 | **`Symbol.for()` tạo global registry** | `Symbol.for("x") === Symbol.for("x")` → true (shared) | Dùng `Symbol()` local nếu không muốn shared |
| 4 | **Không dùng được `new Symbol()`** | `new Symbol()` → TypeError | Luôn dùng `Symbol()` function call |
| 5 | **Symbol key không enumerable** | `for...in` bỏ qua symbol keys | Hiểu rõ enumerable vs non-enumerable |

## 💡 Khi nào dùng — Tình huống thực tế

1. **Thêm tính năng "private"/metadata cho object** truyền qua API — tránh đụng độ tên key với code khác.
2. **Tạo "enum" kiểu che giấu**: `const Status = { DONE: Symbol("done"), FAIL: Symbol("fail") }` — chỉ đúng giá trị của nó.
3. **Custom iterator**: gắn `[Symbol.iterator]` cho object học tự chạy được trong `for...of`.
4. **Cache key bảo mật**: tránh ghi đè từ bên ngoài bằng symbol key thay string key.
5. **Plugin/mixin pattern**: thêm method vào prototype mà không sợ collision với existing methods.
6. **Internal framework state**: lưu internal data trên DOM element безpolluting public API.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Symbol uniqueness — foundational concept

```js
const s1 = Symbol("id");
const s2 = Symbol("id");
console.log(s1 === s2);        // false — MỖI symbol là duy nhất!
console.log(s1.description);   // "id"
console.log(s2.description);   // "id" — cùng description nhưng khác symbol

// Symbol khác nhau hoàn toàn, ngay cả cùng description
console.log(Symbol("a") === Symbol("a")); // false
console.log(Symbol() === Symbol());        // false
```

### Ví dụ 2: Symbol làm hidden key trong object

```js
const s1 = Symbol("id");
const s2 = Symbol("name");
const obj = {
  name: "A",
  [s1]: 42,
  [s2]: "hidden-name",
};

console.log(Object.keys(obj));                    // ["name"] — chỉ string keys
console.log(Object.getOwnPropertyNames(obj));      // ["name"]
console.log(Object.getOwnPropertySymbols(obj));    // [Symbol(id), Symbol(name)]

console.log(obj[s1]);                              // 42 — truy cập bằng symbol variable
console.log(obj[s2]);                              // "hidden-name"

// JSON bỏ qua symbol keys
console.log(JSON.stringify(obj));                  // {"name":"A"} — s1, s2 biến mất!
```

### Ví dụ 3: Well-known Symbol — Symbol.iterator

```js
// Array có Symbol.iterator sẵn
const arr = [1, 2, 3];
const iterator = arr[Symbol.iterator]();
console.log(iterator.next()); // { value: 1, done: false }
console.log(iterator.next()); // { value: 2, done: false }
console.log(iterator.next()); // { value: 3, done: false }
console.log(iterator.next()); // { value: undefined, done: true }

// for...of tự động dùng Symbol.iterator
for (const item of arr) {
  console.log(item); // 1, 2, 3
}

// Spread also uses Symbol.iterator
const copied = [...arr];
console.log(copied); // [1, 2, 3]
```

### Ví dụ 4: Custom iterator với Symbol.iterator

```js
// Tạo object tự iterable
const range = {
  start: 1,
  end: 5,
  [Symbol.iterator]() {
    let current = this.start;
    const end = this.end;
    return {
      next() {
        if (current <= end) {
          return { value: current++, done: false };
        }
        return { value: undefined, done: true };
      },
    };
  },
};

for (const n of range) {
  console.log(n); // 1, 2, 3, 4, 5
}
console.log([...range]); // [1, 2, 3, 4, 5]
```

### Ví dụ 5: Symbol.for — global symbol registry

```js
// Symbol.local — unique, không share
const local1 = Symbol("shared");
const local2 = Symbol("shared");
console.log(local1 === local2); // false

// Symbol.for — global registry, cùng key string = cùng symbol
const global1 = Symbol.for("shared");
const global2 = Symbol.for("shared");
console.log(global1 === global2); // true — cùng symbol trong global registry!

// Useful cho cross-frame hoặc module communication
console.log(Symbol.for("app.version")); // Symbol(app.version)
console.log(Symbol.for("app.version") === Symbol.for("app.version")); // true
```

### Ví dụ 6: Symbol.toStringTag — customize object inspection

```js
class CustomCollection {
  constructor(items) {
    this.items = items;
  }
  // Tùy biến Object.prototype.toString
  get [Symbol.toStringTag]() {
    return "CustomCollection";
  }
}

const col = new CustomCollection([1, 2, 3]);
console.log(Object.prototype.toString.call(col));
// "[object CustomCollection]" — thay vì "[object Object]"

// Ứng dụng: library có thể tự định danh type
console.log(col + ""); // "[object CustomCollection]"
```

## 🔬 So sánh với alternatives

| Phương án | Ưu điểm | Nhược điểm | Phù hợp khi |
|-----------|---------|------------|-------------|
| **Symbol key** | Unique, hidden from enumeration | Không phải truly private (getOwnPropertySymbols) | Metadata, internal state, enum |
| **String key** | Visible, enumerable, JSON serializable | Dễ collision với key người dùng | Public API, data storage |
| **ES2022 `#privateField`** | Thật sự private, enforced by engine | Class syntax only, không áp dụng cho plain object | Class-based OOP |
| **WeakMap key** | Private data attached to object, GC-safe | Chỉ object key, không iterate được | Cache/metadata per object instance |
| **Closure private** | Truly private, no external access | Memory overhead per instance | Functional programming pattern |

## 📊 Performance & Best Practices

- **Dùng `Symbol()` cho unique keys** — mỗi lần gọi tạo symbol mới, tránh collision.
- **Dùng `Symbol.for()` cho shared symbols** — global registry, cùng string = cùng symbol instance.
- **Dùng Symbol cho metadata/enum** — tránh name collision, không enumerable trong JSON.
- **Tránh Symbol cho dữ liệu cần serialize** — `JSON.stringify` bỏ qua symbol keys.
- **Implement `Symbol.iterator`** cho custom iterable objects — `for...of` và spread sẽ tự work.
- **Combine với `Object.getOwnPropertySymbols`** — debug/list symbol keys khi cần.
- **ES2022 `#privateField`** thay thế Symbol cho private class fields — cleaner syntax.

## 🔗 Liên kết chéo

- Xem thêm: `02_data-types/01_primitive-types/` — overview 7 primitive types
- Xem thêm: `02_data-types/02_objects-and-prototype/01_object-basics/` — object key types
- Xem thêm: `03_data-structures/02_keyed-collections/` — Map/Set dùng symbol keys
- Xem thêm: `15_iterators-and-generators/02_iterators/` — iterator protocol chi tiết
- Xem thêm: `14_classes/04_static-private/` — ES2022 private class fields `#`
- Tài liệu: [MDN — Symbol](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Symbol), [javascript.info/symbol](https://javascript.info/symbol)
