# Toán tử Bitwise — Thực hành chi tiết — [Level: Intermediate]

## 🔑 Khái niệm cốt lõi

**Toán tử bitwise** thao tác trực tiếp lên **từng bit** của số nhị phân (biểu diễn 32-bit có dấu). Máy tính lưu mọi số dưới dạng bit, nên các toán tử này cho phép bạn "nói chuyện" với phần cứng theo đúng cách máy hiểu.

JavaScript **ép mọi số thành 32-bit signed integer** trước khi thực hiện bitwise operation. Điều này có nghĩa là số thực bị cắt phần thập phân, và số vượt quá 32-bit cho kết quả bất ngờ.

Các toán tử trong nhóm:

| Toán tử | Tên | Ví dụ `5` và `1` | Giải thích |
|---|---|---|---|
| `&` | AND | `5 & 1` → `1` | Chỉ giữ bit khi CẢ HAI đều 1 |
| `\|` | OR | `5 \| 1` → `5` | Giữ bit khi ÍT NHẤT MỘT là 1 |
| `^` | XOR | `5 ^ 1` → `4` | Giữ bit khi CHỈ MỘT là 1 |
| `~` | NOT (đảo bit) | `~5` → `-6` | Đảo tất cả bit (0→1, 1→0) |
| `<<` | Dịch trái | `5 << 1` → `10` | Nhân đôi (×2) |
| `>>` | Dịch phải có dấu | `5 >> 1` → `2` | Chia đôi (÷2), giữ sign bit |
| `>>>` | Dịch phải không dấu | `-5 >>> 1` → `2147483645` | Chia đôi, fill 0 |

**Giải thích nhị phân** (file `app.js`):
- `5` = `101` (nhị phân), `1` = `001`.
- `101 & 001` = `001` = `1`; `101 | 001` = `101` = `5`; `101 ^ 001` = `100` = `4`.
- `~5` đảo tất cả bit → `-6` (vì bit đầu là bit dấu trong two's complement).
- `5 << 1` dời bit trái 1 vị trí → `1010` = `10` (tương đương ×2); `5 >> 1` → `10` = `2` (tương đương ÷2 làm tròn xuống).
- `>>>` không giữ bit dấu nên `-5 >>> 1` ra một số dương rất lớn.

**Ứng dụng hay nhất: bit flags** — dùng bit để bật/tắt và kiểm tra quyền (READ=1, WRITE=2, EXEC=4).

## 📐 Cấu trúc / Cú pháp

### 7 Bitwise Operators
```js
// AND — chỉ giữ bit khi cả hai đều 1
5 & 1  // 101 & 001 = 001 = 1

// OR — giữ bit khi ít nhất một là 1
5 | 1  // 101 | 001 = 101 = 5

// XOR — giữ bit khi chỉ một là 1
5 ^ 1  // 101 ^ 001 = 100 = 4

// NOT — đảo tất cả bit
~5     // ~000...0101 = 111...1010 = -6 (two's complement)

// Shift trái — nhân 2^n
5 << 1 // 1010 = 10 (5 × 2)
5 << 2 // 10100 = 20 (5 × 4)

// Shift phải có dấu — chia 2^n, giữ sign
5 >> 1 // 10 = 2 (5 ÷ 2, làm tròn xuống)
-5 >> 1 // -3 (-5 ÷ 2, làm tròn xuống)

// Shift phải không dấu — chia 2^n, fill 0
-5 >>> 1 // 2147483645 (bit dấu bị mất, coi như số dương)
```

### Bit Flags Pattern
```js
const READ    = 1;  // 0001
const WRITE   = 2;  // 0010
const EXEC    = 4;  // 0100
const DELETE  = 8;  // 1000

let perm = READ | WRITE;      // 0011 = 3 — có READ và WRITE
perm |= EXEC;                  // 0111 = 7 — thêm EXEC
perm &= ~EXEC;                 // 0011 = 3 — tắt EXEC
const hasRead = (perm & READ) !== 0; // true
const hasExec = (perm & EXEC) !== 0; // false
```

## ✅ Điểm mạnh

1. **Cực nhanh và tiết kiệm bộ nhớ**: gói nhiều cờ boolean vào một số nguyên duy nhất — 32 flag chỉ tốn 4 bytes.
2. **Kiểm tra quyền, cờ trạng thái rất gọn**: `perm & READ` cho biết có quyền đọc hay không — một phép toán.
3. **Dịch bit là phép nhân/chia cho lũy thừa của 2 cực nhanh** — engine tối ưu tốt hơn so với `Math.floor(x / 2)`.
4. **Kỹ thuật này xuất hiện trong nhiều thư viện, chuẩn giao thức, game, image processing** — cần biết để đọc hiểu code.
5. **Giúp hiểu sâu cách máy tính lưu số** — nền tảng cho nhiều chủ đề hệ thống và optimization.
6. **Output minh họa rõ ràng** từng phép toán trong một dòng — dễ học, dễ nhớ.
7. **XOR toggle pattern** — `perm ^ FLAG` để bật/tắt flag mà không cần điều kiện.
8. **BITMASK** — mask nhiều flags cùng lúc: `perm & (READ | WRITE)` kiểm tra đồng thời nhiều quyền.
9. **Compact encoding** — encode nhiều thông tin thành một số (ví dụ: màu RGB thành một số nguyên).
10. **Sử dụng trong crypto, hash, checksum** — các thuật toán low-level đều dựa trên bitwise.

## ⚠️ Bẫy thường gặp & Hạn chế

1. **Chỉ an toàn với số nguyên 32-bit**; số thực bị cắt phần thập phân, số vượt quá 32-bit cho kết quả bất ngờ.
   ```js
   console.log(5.5 & 1); // 1 — .5 bị cắt!
   console.log(TooBigNumber << 1); // kết quả không như mong đợi
   ```

2. **`~` là phép đảo bit, không phải phép phủ định "logic"** — `~5` không phải "không có 5".
   ```js
   console.log(~5);   // -6  ← NOT 5 = -6 (two's complement)
   console.log(!5);   // false ← logical NOT
   ```

3. **`~` hay dùng để phát hiện index không tìm thấy**: `~arr.indexOf(x)` là `true` khi không có (vì `-1` đảo thành `0`).
   ```js
   const arr = [1, 2, 3];
   console.log(~arr.indexOf(4)); // 0 → falsy ← không tìm thấy
   console.log(~arr.indexOf(2)); // -2 → truthy ← tìm thấy
   // ❌ Cách cũ — khó đọc
   // ✅ Hiện đại: arr.includes(4)
   ```

4. **`>>>` với số âm cho số rất lớn**, dễ nhầm nếu không hiểu số không dấu.
   ```js
   console.log(-1 >>> 0); // 4294967295 — -1 thành unsigned 32-bit max
   console.log(-1 >> 0);  // -1 — giữ sign bit
   ```

5. **Ít dùng trong code nghiệp vụ thường ngày** nên dễ bị lãng quên — cần ôn lại khi gặp.
6. **Kết quả luôn là số 32-bit có dấu** — overflow âm silently xảy ra.
7. **Không dùng được cho BigInt** — BigInt không hỗ trợ bitwise operators.
8. **Code bitwise khó đọc** với người mới — cần comment giải thích intent.

## 💡 Khi nào dùng

1. **Kiểm tra quyền/cờ**: `perm & READ`, gộp cờ bằng `READ | WRITE`, toggle bằng `perm ^ DELETE`.
2. **Xử lý ảnh, màu sắc** (rgba), điều kiện trong game (bitmask cho trạng thái entity).
3. **Tối ưu nhân/chia lũy thừa 2** khi cần hiệu năng cao: `x << 3` thay `x * 8`.
4. **Thuật toán mã hóa, băm, checksum** — MD5, SHA, CRC đều dùng bitwise.
5. **Đọc/ghi packet dữ liệu nhị phân** trong networking — parse binary protocol.
6. **CSS/JS animation** — encode nhiều property vào một số để truyền nhanh.
7. **Permission systems** — database Permission Table dùng bitmask thay vì nhiều cột boolean.
8. **WebGL / canvas pixel manipulation** — thao tác trực tiếp trên bit của màu pixel.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Cơ bản — 7 toán tử (file `app.js`)
```js
// Nội dung app.js trong thư mục
console.log(5 & 1, 5 | 1, 5 ^ 1, ~5, 5 << 1, 5 >> 1, -5 >>> 1);
// => 1 5 4 -6 10 2 2147483645
```

### Ví dụ 2: Bit flags — quyền đọc ghi (file `app.js`)
```js
// Bit flags — quyền đọc ghi chạy
const READ = 1, WRITE = 2, EXEC = 4;
let perm = READ | WRITE;                    // 3 = 0011
console.log(perm & READ);                   // 1  → có quyền đọc (truthy)
console.log(perm & EXEC);                   // 0  → không có quyền chạy (falsy)

// Thêm quyền EXEC
perm |= EXEC;                               // 7 = 0111
console.log(perm & EXEC);                   // 4  → giờ có quyền chạy

// Tắt quyền WRITE
perm &= ~WRITE;                             // 5 = 0101
console.log(perm & WRITE);                  // 0  → đã tắt quyền viết
```

### Ví dụ 3: Dịch bit — nhân/chia lũy thừa 2
```js
// Dịch trái = nhân 2
console.log(5 << 1); // 10  (5 × 2)
console.log(5 << 2); // 20  (5 × 4)
console.log(5 << 3); // 40  (5 × 8)

// Dịch phải = chia 2, làm tròn xuống
console.log(10 >> 1); // 5   (10 ÷ 2)
console.log(10 >> 2); // 2   (10 ÷ 4)
console.log(10 >> 3); // 1   (10 ÷ 8)

// Dịch phải có dấu giữ sign
console.log(-10 >> 1); // -5
console.log(-10 >> 2); // -3

// Dịch phải không dấu — luôn dương
console.log(-1 >>> 0); // 4294967295
console.log(-10 >>> 1); // 2147483643
```

### Ví dụ 4: XOR toggle pattern
```js
const ON  = 1;
const OFF = 0;

// XOR với 1 để toggle
console.log(ON  ^ 1); // 0 (toggle từ ON → OFF)
console.log(OFF ^ 1); // 1 (toggle từ OFF → ON)

// Toggle flag mà không cần if
let flag = 0;
flag ^= 1; // flag = 1
flag ^= 1; // flag = 0
flag ^= 1; // flag = 1
console.log(flag); // 1
```

### Ví dụ 5: AND mask — kiểm tra nhiều bit cùng lúc
```js
const READ   = 1;  // 0001
const WRITE  = 2;  // 0010
const EXEC   = 4;  // 0100
const DELETE = 8;  // 1000

let permissions = READ | WRITE | DELETE; // 0111 = 7

// Kiểm tra có READ không
console.log((permissions & READ) !== 0);   // true

// Kiểm tra có WRITE không
console.log((permissions & WRITE) !== 0);  // true

// Kiểm tra có EXEC không
console.log((permissions & EXEC) !== 0);   // false

// Mask multiple: có READ HOẶC WRITE
const hasReadWrite = (permissions & (READ | WRITE)) === (READ | WRITE);
console.log(hasReadWrite); // true

// Mask: có READ HOẶC WRITE (ít nhất một)
const hasAny = (permissions & (READ | WRITE)) !== 0;
console.log(hasAny); // true
```

### Ví dụ 6: Color encoding — RGB thành số nguyên
```js
// Encode RGB thành 1 số 32-bit
function rgbToNumber(r, g, b) {
  return (r << 16) | (g << 8) | b;
}

// Decode
function numberToRgb(n) {
  return {
    r: (n >> 16) & 0xFF,
    g: (n >> 8) & 0xFF,
    b: n & 0xFF,
  };
}

const color = rgbToNumber(255, 128, 0);
console.log(color);          // 16744576
console.log(numberToRgb(color)); // { r: 255, g: 128, b: 0 }
```

### Ví dụ 7: Dùng `!` thay `~` để check existence (hiện đại hơn)
```js
const arr = [10, 20, 30];

// ❌ Cách cũ — dùng ~indexOf
if (~arr.indexOf(20)) {
  console.log("Tìm thấy 20");
}

// ✅ Cách mới — dùng includes (rõ ràng hơn nhiều)
if (arr.includes(20)) {
  console.log("Tìm thấy 20");
}

// ❌ Cách cũ — dùng ~lastIndexOf
if (~arr.lastIndexOf(99)) { ... }

// ✅ Cách mới
if (!arr.includes(99)) { ... }
```

### Ví dụ 8: Bitwise với số âm — two's complement
```js
// ~x = -(x + 1) — công thức two's complement
console.log(~5);   // -6  (-(5+1))
console.log(~(-6)); // 5   (-(−6+1) = 5)
console.log(~0);   // -1  (-(0+1))
console.log(~-1);  // 0   (-(−1+1) = 0)

// Ứng dụng: ~indexOf để check existence (cách cũ)
const list = ["a", "b", "c"];
console.log(~list.indexOf("b")); // -2 (truthy = tồn tại)
console.log(~list.indexOf("z")); //  0 (falsy = không tồn tại)
```

### Ví dụ 9: Sử dụng trong algorithm — đếm số bit 1
```js
// Đếm số bit 1 trong số nguyên (Brian Kernighan's algorithm)
function countSetBits(n) {
  let count = 0;
  while (n > 0) {
    n &= n - 1; // xóa bit 1 thấp nhất
    count++;
  }
  return count;
}
console.log(countSetBits(7));   // 3  (7 = 111)
console.log(countSetBits(8));   // 1  (8 = 1000)
console.log(countSetBits(255)); // 8  (255 = 11111111)
```

### Ví dụ 10: Swap hai số không cần biến trung gian
```js
let a = 5, b = 3;

// Swap bằng XOR — cổ điển nhưng hiếm dùng trong practice
a ^= b;
b ^= a;
a ^= b;
console.log(a, b); // 3 5

// Cách hiện đại và đọc easier
[a, b] = [b, a];
console.log(a, b); // 3 5
```

## 🔬 So sánh với alternatives

| Mục đích | Bitwise | Alternative | Khi nào chọn |
|---|---|---|---|
| Nhân/chia 2^n | `x << n` / `x >> n` | `x * 2^n` / `Math.floor(x / 2^n)` | Bitwise nhanh hơn ~10%, nhưng readability kém |
| Kiểm tra flag | `perm & FLAG` | `flags.includes(FLAG)` | Bitwise compact hơn, array dễ đọc hơn |
| Toggle flag | `perm ^ FLAG` | `perm &= ~FLAG` / `perm |= FLAG` | XOR gọn hơn 1 dòng |
| Check existence | `~arr.indexOf(x)` | `arr.includes(x)` | `includes` rõ ràng hơn, bitwise là cách cũ |
| Encode color | `(r<<16)|(g<<8)|b` | `[r,g,b]` array | Bitwise compact (4 bytes vs 24 bytes) |

## 📊 Performance & Best Practices

**Performance**: Bitwise operations là **nhANH NHẤT** trong tất cả arithmetic operations — được thực hiện trực tiếp ở cấp CPU. `x << n` thường nhanh hơn `x * Math.pow(2, n)` ~2-3x.

**Best practices**:
- **Dùng bit flags** khi cần lưu nhiều boolean vào một số — tiết kiệm bộ nhớ, truy xuất nhanh.
- **Dùng `<<` `>>`** thay `*` `/` khi nhân/chia lũy thừa 2 trong tight loop — performance gain thực sự.
- **Comment giải thích intent** — code bitwise khó đọc, luôn thêm comment `// READ flag = 1`.
- **Dùng `!== 0` thay `!== -1`** khi check flag — rõ ràng hơn `~indexOf`.
- **Tránh bitwise với số float** — phần thập phân bị cắt, kết quả không dự đoán được.
- **Dùng `includes()` thay `~indexOf()`** — modern JavaScript đã có API rõ ràng hơn.
- **Giới hạn 32-bit** — nhớ rằng mọi số được ép thành 32-bit signed integer.

**Quy tắc "3 nên — 3 không"**:
- ✅ Nên dùng bit flags cho permission systems.
- ✅ Nên dùng `<<` `>>` trong performance-critical code.
- ✅ Nên comment giải thích bitmask.
- ❌ Không dùng bitwise thay cho logic thông thường.
- ❌ Không dùng `~indexOf()` — dùng `includes()`.
- ❌ Không dùng bitwise với số thực (float).

## 🔗 Liên kết chéo

- Tổng quan Operators: `08_expressions-and-operators/README.md` — all operator groups.
- Số học cơ bản: `08_expressions-and-operators/01_operators/1_toan-tu-so-hoc.js` — arithmetic operators.
- BigNint: `08_expressions-and-operators/03_bigint-operators/app.js` — BigInt không support bitwise.
- Unary: `08_expressions-and-operators/05_unary/app.js` — `typeof`, `void`, `delete`.
- Callbacks: `09_functions/01_parameters-and-arrow/01_callbacks/` — bitwise flags trong callback context.
- Functions: `09_functions/01_parameters-and-arrow/03_arrow-functions/` — arrow function với bitwise logic.
