# BigInt — [Level: Intermediate]

## 🔑 Khái niệm cốt lõi

**BigInt** là kiểu primitive dành cho **số nguyên lớn hơn** `Number.MAX_SAFE_INTEGER` (= `9007199254740991`, tức 2⁵³ − 1). Number thông thường mất độ chính xác khi vượt giới hạn an toàn:

```js
const maxSafe = Number.MAX_SAFE_INTEGER;
console.log(maxSafe);          // 9007199254740991
console.log(maxSafe + 1);      // 9007199254740992 ✓
console.log(maxSafe + 2);      // 9007199254740992 ✗ — mất chính xác!
//                        ^^^—đáng lẽ phải là 9007199254740993
```

BigInt giải quyết điều này bằng cách biểu diễn số nguyên **không giới hạn độ lớn** — chỉ bị giới hạn bởi bộ nhớ máy.

### Tạo BigInt

```js
// Cách 1: hậu tố `n` trên numeric literal (ES2020)
const big = 9007199254740993n;
console.log(typeof big);       // "bigint"

// Cách 2: hàm khởi tạo BigInt()
const viaCtor = BigInt("9007199254740993");
const viaNum = BigInt(42);     // chuyển number → bigint
console.log(viaCtor === viaNum + 9007199254740951n); // true

// Cách 3: từ binary/octal/hex literal
const binBig = 0b10n;          // BigInt từ binary
const hexBig = 0xFFn;          // BigInt từ hex
console.log(binBig, hexBig);   // 2n 255n
```

### Toán tử với BigInt

```js
const a = 10n;
const b = 3n;

console.log(a + b);            // 13n  — cộng
console.log(a - b);            // 7n   — trừ
console.log(a * b);            // 30n  — nhân
console.log(a / b);            // 3n   — CHIA LẤY PHẦN NGUYÊN (khác number!)
console.log(a % b);            // 1n   — modulo
console.log(a ** b);           // 1000n — lũy thừa
console.log(-a);               // -10n — unary negate

// ⚠️ PHÉP CHIA KHÁC SỐ: 10n / 3n = 3n (không phải 3.333...)
console.log(10n / 3n);         // 3n — phần nguyên
```

## ✅ Điểm mạnh — Tại sao nên dùng bigint

| # | Điểm mạnh | Lý do |
|---|-----------|-------|
| 1 | **Số nguyên chính xác tuyệt đối** | Không giới hạn 2⁵³ — phù hợp ID, hash, crypto |
| 2 | **Đọc rất rõ nhờ hậu tố `n`** | `9007199254740993n` — phân biệt ngay với number |
| 3 | **Phù hợp ID, timestamp nano, tiền tệ** | Sai số precision là "tử hình" trong financial/crypto |
| 4 | **`BigInt()` chuyển đổi an toàn** | `BigInt("9007199254740993")` — string → bigint không mất độ chính xác |
| 5 | **Dùng chung với hash/crypto APIs** | Web Crypto API trả BigInt, match native |

## ⚠️ Bẫy thường gặp & Hạn chế

| # | Bẫy | Ví dụ | Cách tránh |
|---|-----|-------|-----------|
| 1 | **KHÔNG trộn BigInt với Number** | `1n + 1` → `TypeError: Cannot mix BigInt and other types` | Chuyển cùng kiểu trước khi toán tử: `Number(1n) + 1` hoặc `1n + BigInt(1)` |
| 2 | **`1n == 1` true, `1n === 1` false** | Loose equality ép kiểu, strict thì không | Dùng `Object.is(1n, BigInt(1))` hoặc chuyển cùng kiểu |
| 3 | **Không dùng được `Math.*`** | `Math.max(1n, 2n)` → TypeError | Dùng `reduce` với manual compare, hoặc ` > ` operator |
| 4 | **`JSON.stringify(BigInt(1))` lỗi** | `TypeError: Do not know how to serialize a BigInt` | Chuyển về string trước: `JSON.stringify({ id: big.toString() })` |
| 5 | **Phép chia lấy phần nguyên** | `5n / 2n` → `2n` (không phải 2.5) | Hiểu rõ bigint division behavior — không có float |
| 6 | **Không so sánh được với `<`/`>` mixed type** | `1n < 2` → TypeError | Chuyển cùng kiểu trước khi so sánh |
| 7 | **`typeof 1n === "bigint"`** | Khác `typeof 1 === "number"` | Dùng `typeof` để phân biệt |

## 💡 Khi nào dùng — Tình huống thực tế

1. **ID từ database vượt `Number.MAX_SAFE_INTEGER`** — MongoDB ObjectId, Facebook userID, Google API IDs.
2. **Timestamp ở granularity nano/micro giây** — hệ thống distributed cần unique ID chính xác.
3. **Tính toán mật mã (hash, số nguyên lớn)** — RSA, ECC, blockchain — BigInt là bắt buộc.
4. **Mô phỏng tiền tệ giá trị lớn** — khi số vượt quá độ chính xác của float, dùng bigint + fix decimal places.
5. **Scientific computing với số nguyên lớn** — factorial, combination, permutation calculations.
6. **Crypto key generation** — Web Crypto API trả BigInt cho modular exponentiation.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Giới hạn an toàn của Number vs BigInt

```js
const maxSafe = Number.MAX_SAFE_INTEGER;
console.log(maxSafe);             // 9007199254740991
console.log(maxSafe + 1);         // 9007199254740992 ✓
console.log(maxSafe + 2);         // 9007199254740992 ✗ mất chính xác!
console.log(maxSafe + 3);         // 9007199254740994 ✗

// BigInt không có giới hạn này
const bigA = 9007199254740991n;
const bigB = 9007199254740992n;
const bigC = 9007199254740993n;
console.log(bigA + 1n);           // 9007199254740992n ✓
console.log(bigA + 2n);           // 9007199254740993n ✓ chính xác!
console.log(bigA + 3n);           // 9007199254740994n ✓
```

### Ví dụ 2: Toán tử BigInt — quy tắc quan trọng

```js
const x = 10n;
const y = 3n;

console.log(x + y);     // 13n
console.log(x - y);     // 7n
console.log(x * y);     // 30n
console.log(x / y);     // 3n  ← CHIA LẤY PHẦN NGUYÊN!
console.log(x % y);     // 1n
console.log(x ** y);    // 1000n

// ⚠️ Không trộn kiểu
try {
  console.log(x + 1);   // ❌ TypeError: Cannot mix BigInt and other types
} catch (e) {
  console.log("Mix error:", e.message);
}

// Chuyển kiểu an toàn
console.log(Number(x) + 1);   // 11 — bigint → number (mất precision nếu quá lớn)
console.log(x + BigInt(1));   // 11n — number → bigint
```

### Ví dụ 3: So sánh `==` vs `===` với BigInt

```js
console.log(1n == 1);       // true  — loose equality ép kiểu number→bigint
console.log(1n === 1);      // false — strict: khác kiểu (bigint vs number)
console.log(Object.is(1n, BigInt(1))); // true — cùng giá trị, cùng kiểu

// Pattern an toàn: luôn cùng kiểu trước khi so sánh
const a = 100n;
const b = BigInt(100);
console.log(a === b);       // true — cùng bigint, cùng giá trị

const c = 100;
console.log(a === BigInt(c)); // true — chuyển cùng kiểu trước
```

### Ví dụ 4: BigInt với JSON — bẫy serialize

```js
const record = { id: 9007199254740993n, name: "product" };

// ❌ JSON.stringify không hỗ trợ bigint
try {
  console.log(JSON.stringify(record));
} catch (e) {
  console.log("JSON error:", e.message);
  // "Do not know how to serialize a BigInt"
}

// ✅ Chuyển bigint về string trước khi stringify
const safeRecord = {
  ...record,
  id: record.id.toString()   // bigint → string
};
console.log(JSON.stringify(safeRecord));
// {"id":"9007199254740993","name":"product"}

// ✅ Parse ngược lại — cần custom reviver
const parsed = JSON.parse(JSON.stringify(safeRecord), (key, value) =>
  key === "id" ? BigInt(value) : value
);
console.log(parsed.id);      // 9007199254740993n
console.log(typeof parsed.id); // "bigint"
```

### Ví dụ 5: Tính giai thừa lớn — nơi BigInt tỏa sáng

```js
// Factorial với number — mất precision sau 20!
function factorialNumber(n) {
  let result = 1;
  for (let i = 2; i <= n; i++) result *= i;
  return result;
}
console.log(factorialNumber(20));     // 2432902008176640000 ✓
console.log(factorialNumber(21));     // 51090942171709440000 ✓
console.log(factorialNumber(50));     // 3.0414093201713376e+64 ✗ mất precision!

// Factorial với BigInt — chính xác tuyệt đối
function factorialBigInt(n) {
  let result = 1n;
  for (let i = 2n; i <= BigInt(n); i++) result *= i;
  return result;
}
console.log(factorialBigInt(50));
// 30414093201713378043612608166064768843662485853188219615265711721152965402219848670387286965374658997284862141754795297360000000000000n
// ✅ Chính xác 65 chữ số!

console.log(factorialBigInt(100).toString().length); // 158 digits — số có 158 chữ số!
```

### Ví dụ 6: Ứng dụng thực tế — sinh số ngẫu nhiên lớn

```js
// Tạo random BigInt trong khoảng [0, max)
function randomBigInt(max) {
  const maxBytes = Math.ceil(max.toString(16).length / 2);
  const bytes = new Uint8Array(maxBytes);
  crypto.getRandomValues(bytes); // cryptographic secure random
  let result = 0n;
  for (const byte of bytes) {
    result = (result * 256n) + BigInt(byte);
  }
  return result % max;
}

const hugeRandom = randomBigInt(10n ** 50n); // random số đến 50 chữ số
console.log(hugeRandom);
console.log(typeof hugeRandom); // "bigint"
```

## 🔬 So sánh với alternatives

| Phương án | Ưu điểm | Nhược điểm | Phù hợp khi |
|-----------|---------|------------|-------------|
| **BigInt (native)** | Built-in, chính xác tuyệt đối cho integer | Không hoạt động với Math.*, không JSON serialize được | ID lớn, crypto, scientific integer math |
| **Number (IEEE-754)** | Fast, mọi operator support | Precision loss > 2⁵³ | Daily calculations, non-integer math |
| **decimal.js** | Arbitrary precision decimal (không chỉ integer) | Extra dependency | Financial calculations với decimal places |
| **bigint + string** | Serialize được qua JSON | Phải convert roundtrip | Storage/transmission |
| **Immutable.js BigNumber** | Rich API, immutable | Heavy dependency | Redux/complex state với large numbers |

## 📊 Performance & Best Practices

- **Chỉ dùng BigInt khi thực sự cần** — number fast hơn bigint (~2-3x) vì CPU native support.
- **Không trộn bigint và number** — luôn convert cùng kiểu trước khi toán tử.
- **Dùng `.toString()` trước `JSON.stringify`** — bigint không serialize được trực tiếp.
- **Dùng `BigInt()` constructor thay `new BigInt()`** — `new BigInt()` throw TypeError.
- **Phép chia bigint lấy phần nguyên** — `5n / 2n === 2n`, không phải `2.5n`.
- **Dùng `crypto.getRandomValues`** thay `Math.random` cho cryptographic BigInt random.
- **Factorial/big number calculators** — BigInt cho phép tính chính xác mà number không làm được.

## 🔗 Liên kết chéo

- Xem thêm: `02_data-types/01_primitive-types/` — overview primitive types
- Xem thêm: `02_data-types/01_primitive-types/02_number/` — number giới hạn và NaN
- Xem thêm: `02_data-types/03_type-casting-and-coercion/02_explicit/` — BigInt() explicit conversion
- Xem thêm: `04_equality-comparisons/` — `==` vs `===` với bigint
- Xem thêm: `08_expressions-and-operators/03_bigint-operators/` — bigint operators chi tiết
- Tài liệu: [MDN — BigInt](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/BigInt)
