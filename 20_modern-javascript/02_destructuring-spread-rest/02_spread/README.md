# Spread Syntax (...)

## 🔑 Khái niệm

Spread `...` **mở rộng** iterable (array, string) hoặc enumerable properties (object) thành các phần tử riêng lẻ.

| Ngữ cảnh | Cú pháp | Ví dụ |
|---|---|---|
| Array | `[...arr]` | Clone array |
| Object | `{...obj}` | Merge object |
| Function call | `fn(...args)` | Pass array as args |
| Destructuring | `[...rest]` | Collect remaining items |

## ✅ Điểm mạnh
- Clone nông (shallow) array/object nhanh gọn
- Merge/overwrite property dễ dàng
- Spread array vào function args thay `apply`
- Combine nhiều array/object thành 1

## ⚠️ Lưu ý
- **Shallow copy only**: nested object/array vẫn shared reference
- Object spread **không merge đệ quy** — property sau ghi đè property trước
- Spread string: `"abc"` → `["a", "b", "c"]`
- Không spread Promise, Set (Set spread được), Map (cần ` [...map.entries()] `)

## 💡 Khi nào dùng
- Immutable update (Redux pattern)
- Merge config objects
- Pass array elements làm function arguments
- Concatenate arrays ngắn gọn

## 🎯 Ví dụ minh họa

### Clone array (shallow)
```js
const original = [1, 2, [3, 4]];
const clone = [...original];
clone[0] = 99;
console.log(original[0]); // 1 (không đổi)
console.log(clone[2][0]); // 3 — nested vẫn shared!
```

### Merge object
```js
const defaults = { theme: "light", lang: "vi" };
const userPrefs = { theme: "dark" };
const config = { ...defaults, ...userPrefs };
// { theme: "dark", lang: "vi" }
```

### Spread vào function call
```js
const nums = [1, 2, 3];
console.log(Math.max(...nums)); // 3
console.log(Math.min(...nums)); // 1

function add(a, b, c) { return a + b + c; }
console.log(add(...nums)); // 6
```

### Combine arrays
```js
const a = [1, 2];
const b = [3, 4];
const c = [0, ...a, ...b, 5];
// [0, 1, 2, 3, 4, 5]
```

## 📚 Tham khảo & Bài tập
- File: `app.js`, `index.html` trong folder `02_spread/`
- Thực hành: viết hàm `deepClone` dùng spread + recursion
- Câu hỏi: spread array và `concat` khác nhau ở điểm nào?
