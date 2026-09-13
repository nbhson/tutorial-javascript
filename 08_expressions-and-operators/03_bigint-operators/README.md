# Toán tử BigInt — Thực hành chi tiết — [Level: Intermediate]

## 🔑 Khái niệm cốt lõi

**BigInt** là kiểu số nguyên chính xác tuyệt đối trong JavaScript, khắc phục giới hạn của `Number` khi làm việc với các số nguyên rất lớn. Giới hạn an toàn của Number là `Number.MAX_SAFE_INTEGER = 2^53 - 1 = 9007199254740991` — mọi số nguyên lớn hơn con số này có thể bị **mất precision** (mất chữ số cuối).

Viết BigInt bằng cách **thêm hậu tố `n`**: `10n`, `9007199254740991n`, `BigInt("9007199254740993")`.

BigInt dùng các toán tử **giống hệt** Number: `+ - * / % **`. Tuy nhiên có một khác biệt quan trọng: **`10n / 3n` → `3n`** — phép chia BigInt **luôn trả về số nguyên** (phần thập phân bị cắt), không phải `3.333...`.

**Khi nào cần BigInt?**
- Xử lý ID lớn từ API/CSDL (Google Firebase IDs, Instagram IDs, blockchain addresses).
- Tính toán tài chính với số tiền lớn vượt `MAX_SAFE_INTEGER`.
- Mật mã học, hash, cryptographic operations.
- Bất kỳ tình huống nào yêu cầu **chính xác tuyệt đối** với số nguyên > 2^53.

File `app.js` trong thư mục demo các phép toán cơ bản với BigInt.

## 📐 Cấu trúc / Cú pháp

### Khai báo BigInt
```js
// Literal syntax — thêm "n" ở cuối
const big = 9007199254740993n;

// Constructor — từ string hoặc number
const fromString = BigInt("9007199254740993");
const fromNumber = BigInt(42); // chỉ an toàn với số ≤ MAX_SAFE_INTEGER

// ❌ Không được: BigInt(0.5) — throw TypeError (chỉ accept integer)
```

### Phép toán với BigInt
```js
console.log(10n + 5n);  // 15n
console.log(10n - 3n);  // 7n
console.log(10n * 2n);  // 20n
console.log(10n / 3n);  // 3n  ← luôn nguyên, cắt thập phân!
console.log(10n % 3n);  // 1n
console.log(2n ** 10n); // 1024n

// Mixed operations throw TypeError
10n + 1;  // TypeError: Cannot mix BigInt and other types
```

### So sánh
```js
console.log(10n > 9);   // true — so sánh được giữa BigInt và Number
console.log(10n === 10); // false — khác kiểu!
console.log(10n == 10);  // true  — == ép kiểu, === nghiêm ngặt
```

### Chuyển đổi
```js
// BigInt → Number (có thể mất precision!)
const num = Number(bigIntValue);

// Number → BigInt (chỉ được với số nguyên ≤ MAX_SAFE_INTEGER)
const big = BigInt(42);

// BigInt → String
const str = bigIntValue.toString(); // "9007199254740993"

// String → BigInt
const fromStr = BigInt("9007199254740993");
```

## ✅ Điểm mạnh

1. **Chính xác tuyệt đối** với số nguyên cực lớn — không sợ mất chữ số cuối như Number.
   ```js
   // Number mất precision
   console.log(9007199254740993);    // 9007199254740992 ← sai!
   console.log(9007199254740993 + 1); // 9007199254740992 ← vẫn sai!

   // BigInt chính xác
   console.log(9007199254740993n);         // 9007199254740992n ✓
   console.log(9007199254740993n + 1n);    // 9007199254740994n ✓
   ```

2. **Dùng chung cú pháp toán tử với Number** → học nhanh, code tương tự.
3. **Tốt cho**: số ID ngân hàng, số serial, hash, tiền tệ kỹ thuật số, mật mã.
4. **Kết hợp được với hàm `BigInt(value)`** để chuyển đổi từ chuỗi/số.
5. **Không bao giờ trả về số thập phân trong phép `/`** — tránh sai số lẻ, phù hợp cho tính toán nguyên.
6. **An toàn hơn khi so sánh các số cực lớn** trong dữ liệu API.
7. **Hỗ trợ template literal** — `` `ID: ${bigId}` `` hoạt động bình thường.
8. **Native trong JavaScript** — không cần thư viện bên ngoài, supported từ ES2020.
9. **Works với arrays, objects, JSON (với custom replacer)** — linh hoạt trong data structures.
10. **Precision guarantee** — quan trọng cho financial applications, blockchain, cryptography.

## ⚠️ Bẫy thường gặp & Hạn chế

1. **Không trộn lẫn BigInt với Number** trong cùng phép toán: `10n + 1` → `TypeError`. Phải chuyển đổi qua lại bằng `Number(n)` / `BigInt(x)`.
   ```js
   10n + 1;  // TypeError: Cannot mix BigInt and other types
   10n + BigInt(1); // 11n ✓
   Number(10n) + 1; // 11 ✓
   ```

2. **Phép `/` trên BigInt cắt phần thập phân** — cần tự xử lý nếu muốn số thập phân.
   ```js
   console.log(10n / 3n); // 3n — không phải 3.333...
   // Nếu cần precision, chuyển sang Number rồi tính
   const result = Number(10n) / Number(3n); // 3.333...
   ```

3. **Một số thư viện/hàm không hỗ trợ BigInt**: `Math.*`, `toFixed()`, `parseFloat()`, `parseInt()`.
   ```js
   Math.max(1n, 2n); // TypeError: Cannot convert a BigInt value to a number
   (10n).toFixed(2); // TypeError
   ```

4. **`JSON.stringify(BigInt)` không hỗ trợ trực tiếp** — phải chuyển thành chuỗi trước.
   ```js
   JSON.stringify({ id: 123n }); // TypeError: Do not know how to serialize a BigInt
   // ✅ Workaround
   JSON.stringify({ id: "123" }, (_, v) => typeof v === "bigint" ? v.toString() : v);
   ```

5. **Vẫn có giới hạn bộ nhớ** khi số quá khổng lồ — BigInt lưu trữ động, số càng lớn càng tốn内存.
6. **Performance chậm hơn Number** — BigInt operations không được hardware accelerate như Number.
7. **`typeof 10n === "bigint"`** — khác với Number, phải check riêng.
8. **BigInt không có NaN, Infinity, -0** — chỉ có số nguyên.

## 💡 Khi nào dùng

1. **Xử lý ID lớn vượt quá 2^53** từ API/CSDL (Firebase, Instagram, Shopify IDs).
2. **Các phép toán chính xác trong tài chính**, blockchain, tiền tệ kỹ thuật số — không chấp nhận sai số.
3. **Tính toán số học có độ chính xác cao** — hệ số, phép đếm lớn, combinatorics.
4. **Khi so sánh hoặc lưu trữ các con số cực lớn** không muốn mất precision.
5. **Mật mã học** — RSA, elliptic curve đều cần số nguyên超大.
6. **Checksum, hash computation** — MD5, SHA đều thao tác trên bit của số lớn.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Cơ bản — các phép toán (file `app.js`)
```js
// Nội dung app.js trong thư mục
console.log(10n + 5n, 10n * 2n, 10n / 3n, 10n % 3n, 2n ** 10n);
// 15n 20n 3n 1n 1024n
```

### Ví dụ 2: Số lớn hơn giới hạn an toàn của Number
```js
// Number mất precision ở đây
console.log(9007199254740991);       // 9007199254740991
console.log(9007199254740991 + 1);   // 9007199254740992 ← sai! Number không phân biệt được
console.log(9007199254740991 + 2);   // 9007199254740992 ← vẫn sai!

// BigInt chính xác
console.log(9007199254740991n);      // 9007199254740991n
console.log(9007199254740991n + 1n); // 9007199254740992n ✓
console.log(9007199254740991n + 2n); // 9007199254740993n ✓
```

### Ví dụ 3: So sánh BigInt với Number
```js
// So sánh được giữa BigInt và Number
console.log(10n > 9);   // true
console.log(10n >= 10); // true
console.log(10n < 11);  // true

// Nhưng === phân biệt kiểu
console.log(10n === 10); // false — khác kiểu (bigint vs number)
console.log(10n == 10);  // true  — == ép kiểu, so sánh giá trị

// ✅ Best practice: so sánh cùng kiểu
console.log(10n === 10n); // true
```

### Ví dụ 4: Chuyển đổi giữa BigInt và Number
```js
// BigInt → Number (có thể mất precision!)
const big = 9007199254740993n;
const num = Number(big);
console.log(num); // 9007199254740992 ← mất precision!

// Number → BigInt (chỉ an toàn với số ≤ MAX_SAFE_INTEGER)
const safeNum = 42;
const safeBig = BigInt(safeNum);
console.log(safeBig); // 42n

// String → BigInt (an toàn với mọi độ dài)
const fromString = BigInt("9007199254740993");
console.log(fromString); // 9007199254740993n

// BigInt → String
console.log(big.toString()); // "9007199254740993"
```

### Ví dụ 5: BigInt trong function — tính giai thừa lớn
```js
function factorial(n) {
  let result = 1n;
  for (let i = 2n; i <= BigInt(n); i++) {
    result *= i;
  }
  return result;
}

console.log(factorial(50)); // 30414093201713378043612608166064768843612604160768000000000000n
console.log(factorial(100)); // 933262154439441526816992388562667004907159682643816214685929638952175999932299156089414640671394971074233120827223758251185210916864000000000000000000000000n

// So với Number — mất precision từ 21!
console.log(factorial(20)); // 2432902008176640000n ✓
// console.log(20!); using Number: 2432902008176640000 ← đúng
// console.log(21!); using Number: 51090942171709440000 ← SAI (Number losing precision)
```

### Ví dụ 6: BigInt array — xử lý danh sách ID lớn
```js
const largeIds = [
  BigInt("9007199254740991"),
  BigInt("9007199254740992"),
  BigInt("9007199254740993"),
];

// Tìm ID lớn nhất
const maxId = largeIds.reduce((a, b) => (a > b ? a : b));
console.log(maxId); // 9007199254740993n

// Lọc ID > threshold
const threshold = BigInt("9007199254740992");
const filtered = largeIds.filter(id => id > threshold);
console.log(filtered); // [9007199254740993n]
```

### Ví dụ 7: BigInt trong JSON (với custom serializer)
```js
const data = {
  userId: 9007199254740993n,
  amount: 10000000000000001n,
  timestamp: Date.now(),
};

// Serialize — phải convert BigInt to string
const json = JSON.stringify(data, (_, value) =>
  typeof value === "bigint" ? value.toString() + "n" : value
);
console.log(json); // '{"userId":"9007199254740993n","amount":"10000000000000001n","timestamp":...}'

// Deserialize
const parsed = JSON.parse(json, (_, value) =>
  typeof value === "string" && value.endsWith("n") ? BigInt(value.slice(0, -1)) : value
);
console.log(parsed.userId); // 9007199254740993n
```

### Ví dụ 8: BigInt và toán tử logical
```js
// BigInt có truthy/falsy như Number
console.log(0n ? "truthy" : "falsy");    // "falsy"
console.log(5n ? "truthy" : "falsy");    // "truthy"
console.log(-3n ? "truthy" : "falsy");   // "truthy"

// && và || hoạt động với BigInt
console.log(5n && 3n);   // 3n — left truthy → return right
console.log(0n && 3n);   // 0n — left falsy → return left
console.log(5n || 3n);   // 5n — left truthy → return left
console.log(0n || 3n);   // 3n — left falsy → return right

// ! ép BigInt thành boolean
console.log(!0n);        // true
console.log(!5n);        // false
```

### Ví dụ 9: Tính tổng mảng BigInt
```js
function sumBigInts(arr) {
  return arr.reduce((acc, val) => acc + val, 0n);
}

const numbers = [10000000000000000n, 20000000000000000n, 30000000000000001n];
console.log(sumBigInts(numbers)); // 60000000000000001n
// ✅ Chính xác — Number sẽ mất precision
```

### Ví dụ 10: BigInt vs Number precision demonstration
```js
// Demonstrate Number precision loss
const bigNum = 9007199254740993;
console.log(bigNum);           // 9007199254740992 ← mất precision!
console.log(bigNum + 1);       // 9007199254740992 ← vẫn vậy, không tăng!
console.log(bigNum === bigNum + 2); // true ← sai! hai số khác nhau nhưng === true

// BigInt correct
const bigBig = 9007199254740993n;
console.log(bigBig);           // 9007199254740993n ✓
console.log(bigBig + 1n);      // 9007199254740994n ✓
console.log(bigBig === bigBig + 2n); // false ✓
```

## 🔬 So sánh với alternatives

| Phương án | Ưu điểm | Nhược điểm | Phù hợp khi |
|---|---|---|---|
| **BigInt** | Chính xác tuyệt đối, native JS | Không trộn với Number, chậm hơn | Số > 2^53, finance, crypto |
| **Number** | Nhanh, toán tử đầy đủ, library support | Mất precision > 2^53-1 | Số thông thường, performance-critical |
| **String** | Không mất precision, easy serialize | Khó tính toán, phải parse | ID display, JSON transport |
| **Library (Big.js, bignumber.js)** | Floating point, currency, API rich | Extra dependency, bundle size | Financial apps cần decimal precision |
| **Decimal.js** | Exact decimal representation | Extra dependency | Currency, exact decimal math |

## 📊 Performance & Best Practices

**Performance**: BigInt **chậm hơn Number** ~10-100x tùy operation — không được hardware accelerate. Tránh dùng trong **vòng lặp tight** hoặc **performance-critical path**.

**Quy tắc coding**:
- **Chỉ dùng BigInt khi cần precision > 2^53** — đừng dùng tràn lan.
- **Luôn cùng kiểu khi tính toán** — convert trước khi mixed operation.
- **Convert to String cho JSON** — `JSON.stringify` không support BigInt native.
- **Dùng `BigInt(string)` thay `BigInt(number)`** — number > MAX_SAFE_INTEGER đã mất precision trước khi convert.
- **Avoid `Math.*` với BigInt** — không supported, dùng custom function.
- **Cache BigInt results** — nếu tính nhiều lần, lưu vào variable thay vì tính lại.

**Khi nào KHÔNG dùng BigInt**:
- Số nằm trong range `[-2^53, 2^53]` → dùng Number.
- Cần floating point precision → dùng Decimal.js / bignumber.js.
- Performance-critical loop → dùng Number + round carefully.
- Display only (ID, reference) → String đủ, không cần tính toán.

## 🔗 Liên kết chéo

- Tổng quan Operators: `08_expressions-and-operators/README.md` — all operator groups overview.
- Arithmetic operators: `08_expressions-and-operators/01_operators/1_toan-tu-so-hoc.js` — basic arithmetic.
- Bitwise: `08_expressions-and-operators/02_bitwise/app.js` — bitwise không hỗ trợ BigInt.
- Unary: `08_expressions-and-operators/05_unary/app.js` — `typeof 10n` → `"bigint"`.
- Functions: `09_functions/01_parameters-and-arrow/04_recursion/app.js` — đệ quy với BigInt.
- Arrow functions: `09_functions/01_parameters-and-arrow/03_arrow-functions/` — arrow với BigInt return.
