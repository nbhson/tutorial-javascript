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

| Ưu điểm | Ví dụ |
|---|---|
| Clone nông nhanh gọn | `const clone = [...original];` |
| Merge/overwrite props | `{...defaults, ...override}` |
| Spread vào function args | `Math.max(...nums)` |
| Combine arrays ngắn | `[0, ...a, ...b, 5]` |

## ⚠️ Bẫy thường gặp

### Bẫy 1: Shallow copy only
```js
const original = [1, 2, [3, 4]];
const clone = [...original];
clone[2][0] = 99;
console.log(original[2][0]); // 99 — nested vẫn shared!
```

### Bẫy 2: Object spread không merge đệ quy
```js
const a = { x: { a: 1 } };
const b = { x: { b: 2 } };
const merged = { ...a, ...b };
// { x: { b: 2 } } — a.x bị ghi đè hoàn toàn, không merge
```

### Bẫy 3: Spread string thành chars
```js
[..."hello"]; // ['h','e','l','l','o']
```

## 💡 Khi nào dùng

- Immutable update (Redux pattern)
- Merge config objects
- Pass array elements làm function arguments
- Concatenate arrays ngắn gọn

## 🎯 Ví dụ

```js
// Clone array (shallow)
const original = [1, 2, [3, 4]];
const clone = [...original];
clone[0] = 99;
console.log(original[0]); // 1 (không đổi)

// Merge object
const defaults = { theme: "light", lang: "vi" };
const userPrefs = { theme: "dark" };
const config = { ...defaults, ...userPrefs };
// { theme: "dark", lang: "vi" }

// Spread vào function call
const nums = [1, 2, 3];
console.log(Math.max(...nums)); // 3
console.log(Math.min(...nums)); // 1

function add(a, b, c) { return a + b + c; }
console.log(add(...nums)); // 6

// Combine arrays
const a = [1, 2];
const b = [3, 4];
const c = [0, ...a, ...b, 5];
// [0, 1, 2, 3, 4, 5]

// Redux-style immutable update
const state = { items: [1, 2, 3], filter: "all" };
const newState = { ...state, items: [...state.items, 4] };
// state.items vẫn [1,2,3], newState.items = [1,2,3,4]
```

## 🔗 Liên kết chéo
- Xem: `20_modern-javascript/02_destructuring-spread-rest/01_destructuring-rest`
- Xem: `09_functions/01_parameters-and-arrow/06_function-parameters`
