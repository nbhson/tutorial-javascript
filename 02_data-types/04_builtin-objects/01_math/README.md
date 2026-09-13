# Built-in: Math — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

**`Math`** là một built-in object "namespace" chứa **hàm toán học và hằng số** dùng ngay mà không cần khởi tạo. Đặc điểm riêng độc nhất: `Math` **không có constructor** — gọi `new Math()` sẽ ném `TypeError`. Bạn chỉ truy cập `Math.hàm` hoặc `Math.hằng_số`.

### Vì sao Math không có constructor?

Trong ECMAScript spec, `Math` được định nghĩa là một **ordinary object** bình thường (không phải function object) — nó không có internal slot `[[Construct]]` nên không thể `new`. Đây là thiết kế có chủ đích: không có lý do gì để tạo "một instance Math" — các hàm toán học là **pure functions** dùng chung toàn cục.

Ngược lại, `Date`, `RegExp`, `Error` là constructor vì chúng tạo instance đại diện cho giá trị cụ thể.

### Các hằng số & hàm thường dùng

| Thành viên | Ý nghĩa | Ví dụ |
|---|---|---|
| `Math.PI` | số π ≈ 3.14159 | `Math.PI` → 3.141592653589793 |
| `Math.E` | số e ≈ 2.71828 | `Math.E` → 2.718281828459045 |
| `Math.max(a, b, ...)` | giá trị lớn nhất trong các đối số | `Math.max(1, 5, 3)` → 5 |
| `Math.min(a, b, ...)` | giá trị nhỏ nhất | `Math.min(1, 5, 3)` → 1 |
| `Math.round(x)` | làm tròn (0.5 làm tròn lên) | `Math.round(3.5)` → 4 |
| `Math.ceil(x)` | làm tròn lên | `Math.ceil(3.1)` → 4 |
| `Math.floor(x)` | làm tròn xuống | `Math.floor(3.9)` → 3 |
| `Math.trunc(x)` | bỏ phần thập phân | `Math.trunc(-3.9)` → -3 |
| `Math.abs(x)` | giá trị tuyệt đối | `Math.abs(-15.41)` → 15.41 |
| `Math.random()` | số ngẫu nhiên `>= 0` và `< 1` | `Math.random()` → 0.xxxxx |
| `Math.pow(x, y)` / `x ** y` | lũy thừa | `Math.pow(2, 3)` → 8 |
| `Math.sqrt(x)` | căn bậc hai | `Math.sqrt(16)` → 4 |
| `Math.cbrt(x)` | căn bậc ba | `Math.cbrt(27)` → 3 |
| `Math.hypot(...)` | căn bậc 2 tổng bình phương | `Math.hypot(3, 4)` → 5 |
| `Math.sign(x)` | dấu: 1, -1, 0, -0, NaN | `Math.sign(-5)` → -1 |
| `Math.log(x)` | logarit tự nhiên | `Math.log(Math.E)` → 1 |
| `Math.sin/cos/tan(x)` | lượng giác (radian) | `Math.sin(Math.PI / 2)` → 1 |

```js
console.log(Math.PI, Math.max(1,5,3), Math.floor(1.9), Math.random());
// 3.141592653589793 5 1 <số ngẫu nhiên 0≤r<1>
```

### Công thức random integer trong khoảng `[min, max]`

```js
function randomInt(min, max) {
  // Math.random()       → [0, 1)
  // * (max - min + 1)   → [0, max - min + 1)
  // Math.floor()        → [0, max - min]
  // + min               → [min, max] ✓ inclusive cả hai đầu
  return Math.floor(Math.random() * (max - min + 1)) + min;
}
```

## 📐 Cấu trúc nhóm

```
02_data-types/04_builtin-objects/01_math/
├── README.md         ← bài này
├── app.js            ← demo Math.PI, Math.max, Math.floor, Math.random
└── index.html
```

## ✅ Điểm mạnh — Tại sao dùng Math

| # | Điểm mạnh | Lý do |
|---|-----------|-------|
| 1 | **Không cần cài thư viện** | Math có sẵn ở mọi môi trường JS — browser, Node, Deno, Bun |
| 2 | **Được engine tối ưu native** | V8 compile `Math.floor` thành 1 instruction CPU — nhanh hơn tay viết |
| 3 | **Pure functions** | Không side effect — an toàn dùng trong functional pipeline |
| 4 | **Đủ cho 90% nhu cầu** | round, abs, min/max, random, sqrt — giải quyết việc thường gặp |
| 5 | **Kết hợp toFixed() format hiển thị** | `(42.678).toFixed(2)` → "42.68" cho UI |
| 6 | **Hằng số chuẩn** | `Math.PI`, `Math.E` chính xác double-precision |
| 7 | **`Math.hypot` tránh overflow** | Tính khoảng cách an toàn hơn `sqrt(x²+y²)` thủ công |

## ⚠️ Bẫy thường gặp & Hạn chế

| # | Bẫy | Ví dụ | Cách tránh |
|---|-----|-------|-----------|
| 1 | **`Math.random()` không an toàn mật mã** | Có thể predict seed | Dùng `crypto.getRandomValues()` cho token/password |
| 2 | **`Math.random()` không bao giờ trả 1** | Range `[0, 1)` — quên `+1` mất giá trị max | Dùng công thức `floor(random() * (max - min + 1)) + min` |
| 3 | **Không thể `new Math()`** | `new Math()` → `TypeError: Math is not a constructor` | Chỉ access static: `Math.xxx` |
| 4 | **`Math.round(-1.5)` → -1 (không phải -2)** | Round luôn "lên" theo hướng dương | Dùng `Math.floor(x + 0.5)` nếu muốn banker rounding |
| 5 | **`Math.max()` không nhận mảng** | `Math.max([1,2,3])` → `NaN` | Spread: `Math.max(...arr)` hoặc `arr.reduce()` |
| 6 | **`Math.max(...hugeArr)` stack overflow** | Mảng > 100K phần tử tràn call stack | Dùng `arr.reduce((a,b) => Math.max(a,b))` |
| 7 | **Không hoạt động với BigInt** | `Math.abs(10n)` → `TypeError` | Convert `Number()` hoặc xử lý tay |
| 8 | **Float precision** | `Math.round(0.49999999999999994 + 0.5)` → 1 sai | Cộng epsilon nhỏ trước khi round |

```js
// Bẫy 4: round với số âm
console.log(Math.round(-1.5));   // -1 — "lên" là về phía +∞
console.log(Math.floor(-1.5));   // -2 — "xuống" là về phía -∞
console.log(Math.trunc(-1.5));   // -1 — cắt thập phân, tiến về 0

// Bẫy 6: mảng lớn
const huge = new Array(200000).fill(0).map((_, i) => i);
// Math.max(...huge);            // ❌ RangeError: Maximum call stack size exceeded
console.log(huge.reduce((a, b) => (a > b ? a : b))); // ✅ 199999
```

## 💡 Khi nào dùng — Tình huống thực tế

1. **Hiển thị giá tiền** — `Math.round(price * 100) / 100` giữ number type, `toFixed(2)` khi cần string.
2. **Max/min trong danh sách** — `Math.max(...scores)` với mảng nhỏ; `reduce` với mảng lớn.
3. **Sinh số ngẫu nhiên** — game xúc xắc `randomInt(1, 6)`, shuffle, sampling.
4. **Tính khoảng cách 2 điểm** — `Math.hypot(x2 - x1, y2 - y1)` an toàn overflow.
5. **Clamp giá trị** — `Math.min(Math.max(value, 0), 100)` cho progress bar, opacity.
6. **Vẽ tròn trong Canvas** — `Math.cos/sin` + `Math.PI` tính tọa độ điểm trên đường tròn.
7. **Đếm trang pagination** — `Math.ceil(total / perPage)`.
8. **Truncate text/scroll position** — `Math.floor` cho index, offset.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Các hàm làm tròn — phân biệt rõ

```js
console.log(Math.round(3.4));     // 3  — làm tròn chuẩn
console.log(Math.round(3.5));     // 4  — .5 luôn lên
console.log(Math.round(-3.5));    // -3 — "lên" theo hướng +∞!
console.log(Math.ceil(3.1));      // 4  — trần
console.log(Math.ceil(-3.9));     // -3 — trần của -3.9 là -3
console.log(Math.floor(3.9));     // 3  — sàn
console.log(Math.floor(-3.1));    // -4 — sàn của -3.1 là -4
console.log(Math.trunc(3.9));     // 3  — cắt phần thập phân
console.log(Math.trunc(-3.9));    // -3 — cắt về phía 0
```

### Ví dụ 2: Random integer — công thức chuẩn + kiểm chứng

```js
function randomInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

// Xúc xắc: [1, 6]
for (let i = 0; i < 5; i++) console.log(randomInt(1, 6));

// Kiểm chứng bounds: chạy 10000 lần luôn trong [10, 20]
let ok = true;
for (let i = 0; i < 10000; i++) {
  const r = randomInt(10, 20);
  if (r < 10 || r > 20) ok = false;
}
console.log("All in [10,20]:", ok); // true

// Chọn phần tử ngẫu nhiên từ mảng
const fruits = ["🍎", "🍌", "🍇", "🍊"];
const pick = fruits[randomInt(0, fruits.length - 1)];
console.log("Fruit:", pick);
```

### Ví dụ 3: Max/min với nhiều nguồn dữ liệu

```js
const scores = [88, 95, 72, 91, 79];

// Cách 1: spread (mảng nhỏ — OK)
console.log(Math.max(...scores));            // 95
console.log(Math.min(...scores));            // 72

// Cách 2: reduce (an toàn mọi kích thước)
const max = scores.reduce((a, b) => Math.max(a, b), -Infinity);
const min = scores.reduce((a, b) => Math.min(a, b), Infinity);
console.log(max, min);                       // 95 72

// Cách 3: tìm object theo field
const students = [
  { name: "An", score: 85 },
  { name: "Bình", score: 92 },
  { name: "Cường", score: 78 },
];
const top = students.reduce((a, b) => (a.score > b.score ? a : b));
console.log(top.name);                       // "Bình"
```

### Ví dụ 4: Clamp + format — utility functions thực tế

```js
// Clamp: giới hạn giá trị trong [min, max]
function clamp(value, min, max) {
  return Math.min(Math.max(value, min), max);
}
console.log(clamp(150, 0, 100));  // 100
console.log(clamp(-10, 0, 100));  // 0
console.log(clamp(50, 0, 100));   // 50

// Format phần trăm
function pct(value, total, decimals = 1) {
  return ((value / total) * 100).toFixed(decimals) + "%";
}
console.log(pct(3, 7));           // "42.9%"

// Khoảng cách Euclidean — hypot an toàn hơn sqrt(x²+y²)
function distance(p1, p2) {
  return Math.hypot(p2.x - p1.x, p2.y - p1.y);
}
console.log(distance({x:0,y:0}, {x:3,y:4})); // 5
```

### Ví dụ 5: Lượng giác — vẽ đa giác đều trên Canvas

```js
// Tính tọa độ n đỉnh của đa giác đều bán kính r, tâm (cx, cy)
function polygonPoints(cx, cy, r, n) {
  const points = [];
  for (let i = 0; i < n; i++) {
    const angle = (2 * Math.PI * i) / n - Math.PI / 2; // bắt đầu từ đỉnh trên
    points.push({
      x: cx + r * Math.cos(angle),
      y: cy + r * Math.sin(angle),
    });
  }
  return points;
}

const hexagon = polygonPoints(100, 100, 50, 6);
console.log(hexagon[0]); // { x: 100, y: 50 } — đỉnh đầu tiên
console.log(hexagon.length); // 6
```

### Ví dụ 6: Random secure — crypto thay Math.random

```js
// ❌ Math.random() — predict được seed, KHÔNG dùng cho bảo mật
// ✅ crypto.getRandomValues() — CSPRNG

function secureRandomInt(min, max) {
  const range = max - min + 1;
  const limit = Math.floor(0xFFFFFFFF / range) * range;
  const arr = new Uint32Array(1);
  let value;
  do {
    crypto.getRandomValues(arr);
    value = arr[0];
  } while (value >= limit); // reject sampling — tránh modulo bias
  return (value % range) + min;
}

console.log(secureRandomInt(1, 100)); // random an toàn mật mã
```

### Ví dụ 7: Đo hiệu năng với timestamp

```js
const start = performance.now();     // độ chính xác sub-ms

// Đoán thuật cần test
let sum = 0;
for (let i = 0; i < 1e7; i++) sum += Math.sqrt(i);

const elapsed = performance.now() - start;
console.log(`10M sqrt: ${elapsed.toFixed(2)}ms`);
```

## 🔬 So sánh với alternatives

| Phương án | Ưu điểm | Nhược điểm | Phù hợp khi |
|-----------|---------|------------|-------------|
| **Native `Math`** | Built-in, JIT-optimized, zero dependency | Thiếu matrix/complex/units | 95% nhu cầu thông thường |
| **`math.js`** | Big numbers, matrix, unit conversion | ~700KB bundle | Scientific computing |
| **`decimal.js`** | Chính xác decimal tuyệt đối | Chậm hơn float | Tiền tệ chính xác cao |
| **WebAssembly SIMD** | Tính vector cực nhanh | Phức tạp, cần toolchain | ML, xử lý ảnh bulk |
| **Tự viết (`x*x` thay `pow(x,2)`)** | Nhanh hơn cho phép lặp | Duplicate logic | Hot loop micro-optimization |

## 📊 Performance & Best Practices

- **`x * x` nhanh hơn `Math.pow(x, 2)`** — JIT inline multiplication; dùng `**` hoặc `pow` cho số mũ khác.
- **`Math.hypot(x, y)` thay `Math.sqrt(x*x + y*y)`** — an toàn overflow/underflow, engine tối ưu riêng.
- **Tránh spread với mảng lớn** — `Math.max(...arr)` crash với arr > ~125K phần tử; dùng `reduce`.
- **`| 0` hoặc `~~x` thay `Math.floor` cho số dương** — micro-opt bitwise, nhưng `Math.trunc` readable hơn; ưu tiên readability.
- **Cache kết quả lặp** — `Math.sqrt` trong loop 1M+ lần: nếu input lặp lại, memoize.
- **`crypto.getRandomValues` cho security** — token, password, session ID không bao giờ dùng `Math.random()`.
- **ESLint `no-bitwise`** cân nhắc nếu dùng `| 0` trong team cần rõ nghĩa.

## 🔗 Liên kết chéo

- Xem thêm: `02_data-types/01_primitive-types/02_number/` — Number type, NaN, Infinity
- Xem thêm: `02_data-types/04_builtin-objects/` — tổng quan built-in objects
- Xem thêm: `08_expressions-and-operators/01_operators/` — toán tử số học, `**`
- Xem thêm: `21_graphics/04_canvas/` — ứng dụng Math.sin/cos vẽ canvas
- Tài liệu: [MDN — Math](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math)
