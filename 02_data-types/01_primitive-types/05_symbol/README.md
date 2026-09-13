# Symbol

## 🔑 Khái niệm

**Symbol** là kiểu primitive **duy nhất (unique)** và **bất biến (immutable)**. Mỗi lần gọi `Symbol("mô tả")` ta nhận một instance mới không bao giờ trùng với Symbol khác — ngay cả khi cùng mô tả:

```js
const s1 = Symbol("id");
const s2 = Symbol("id");
console.log(s1 === s2); // false ← mỗi Symbol là duy nhất!
```

**Công dụng chính:** làm **key ẩn (hidden key)** cho object. Khác với string key, Symbol key **không xuất hiện** trong `Object.keys()` hay `for...in` — rất hợp để làm "private field":

```js
const s1 = Symbol("id");
const obj = { name: "A", [s1]: 42 };

console.log(Object.keys(obj));        // ["name"] ← không thấy s1
console.log(Object.getOwnPropertySymbols(obj)); // [Symbol(id)] ← chỉ thấy qua API này
console.log(obj[s1]);                 // 42 — truy cập bằng chính biến symbol
```

Muốn "liệt kê" các Symbol key thì dùng `Object.getOwnPropertySymbols(obj)`.

**Well-known Symbols (built-in):** JavaScript quy ước một loạt `Symbol.xxx` để móc vào hành vi nội bộ của object. Hai ví dụ kinh điển:

- **`Symbol.iterator`** — đánh dấu object "iterate được" (dùng trong `for...of`, spread):
  ```js
  const arr = [1, 2];
  console.log(arr[Symbol.iterator].toString()); // function values() { [native code] }
  ```
- **`Symbol.toStringTag`** — tùy biến kết quả `Object.prototype.toString`: `({ [Symbol.toStringTag]: "MyType" })` → `"[object MyType]"`.

## ✅ Điểm mạnh

- **Bảo đảm duy nhất** — không bao giờ trùng khóa, tránh ghi đè ngẫu nhiên.
- **Ẩn với vòng lặp/Object.keys** → thêm metadata mà không "vấy bẩn" dữ liệu enumerable.
- Truy cập cần đúng biến symbol → tự nhiên thành "private".
- Well-known Symbols cho phép tùy biến iterator, `toStringTag`, `toPrimitive`... của object.
- Là primitive — nhẹ, được nhiều thư viện (React key cache, redux) sử dụng.

## ⚠️ Lưu ý / Hạn chế

- Symbol **không** bị "hack" bằng `Object.keys` nhưng vẫn truy cập được qua `Object.getOwnPropertySymbols` — không phải private cứng (đây là điều khó tạo private field thật; ES2022 có `#field`).
- `JSON.stringify({ [s1]: 1 })` **bỏ qua** Symbol keys.
- Không thể dùng `Symbol.for("x")` để "chia sẻ" Symbol với code khác nếu quên — Symbol thường là local; muốn chia sẻ dùng `Symbol.for`.
- `typeof Symbol()` là `"symbol"`, không dùng được với `new Symbol()` (sẽ `TypeError`).

## 💡 Khi nào dùng

- Thêm tính năng "private"/metadata cho object truyền qua API (tránh đụng độ tên).
- Tạo "enum" kiểu che giấu: `const Status = { DONE: Symbol("done"), FAIL: Symbol("fail") }` — chỉ đúng giá trị của nó.
- Custom iterator: gắn `[Symbol.iterator]` cho object học tự chạy trong `for...of`.
- Cache key bảo mật / tránh ghi đè từ bên ngoài.

## 🎯 Ví dụ minh họa

```js
const s1 = Symbol("id");
const s2 = Symbol("id");
console.log(s1 === s2);        // false

const obj = { name: "A", [s1]: 42 };
console.log(Object.keys(obj));          // ["name"]
console.log(Object.getOwnPropertySymbols(obj)); // [Symbol(id)]
console.log(obj[s1]);                    // 42

// Well-known: Symbol.iterator
const arr = [1, 2];
console.log(arr[Symbol.iterator].toString()); // function values() { [native code] }

// Ẩn với JSON
console.log(JSON.stringify(obj)); // {"name":"A"}
```

## 📚 Tham khảo / Bài tập

- Chạy `app.js` trong thư mục (`node app.js` hoặc mở `index.html`): hiển thị `s1 === s2` là `false`, `Object.keys` không thấy symbol, `obj[s1]` vẫn truy cập được, và `Symbol.iterator` của array.
- Tự thử: 1) dùng `Symbol.for("cache")` trong hai "module" tách biệt và kiểm tra chúng "chia sẻ" cùng giá trị hay không; 2) tạo một object có `[Symbol.iterator]` tự chạy được với `for...of`; 3) dùng `Object.getOwnPropertySymbols` để tìm ẩn Symbol trong một object khác.
- Tài liệu: [MDN — Symbol](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Symbol).