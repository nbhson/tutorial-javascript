# null / undefined / boolean — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

Ba kiểu nguyên thủy này có vẻ "nhỏ" nhưng **gây nhiều nhầm lẫn nhất** trong JavaScript. Cần phân biệt rõ bản chất và cách dùng của từng loại.

### 1. `undefined` — giá trị do engine tự đặt

`undefined` là giá trị mặc định khi:
- Biến được khai báo nhưng **chưa gán giá trị**.
- Truy cập **thuộc tính không tồn tại** trên object.
- Truy cập **phần tử mảng bỏ trống** (sparse array).
- Hàm **không trả về gì** (không có `return` hoặc `return` không có giá trị).

```js
let x;
console.log(x);          // undefined
console.log(typeof x);   // "undefined"

function f() {}         // không có return
console.log(f());        // undefined

const o = {};
console.log(o.ten);      // undefined — property không tồn tại

const arr = [1, , 3];  // sparse array — phần tử giữa undefined
console.log(arr[1]);     // undefined
```

### 2. `null` — giá trị do lập trình viên cố ý đặt

`null` biểu thị **"rỗng có chủ đích"** — lập trình viên chủ động set để nói "không có giá trị gì ở đây".

```js
const user = null;       // rõ ràng: chưa có user nào
const connection = null; // chưa kết nối
const result = search(id); // có thể trả về null nếu không tìm thấy
```

> ⚠️ **Bug lịch sử:** `typeof null` trả `"object"` (engine tạo từ năm đầu, không sửa được vì sẽ phá hàng tỉ trang web). Trên thực tế `null` **KHÔNG phải object** — nó là primitive. Luôn dùng `=== null` để kiểm tra.

### So sánh null và undefined

```js
null == undefined;   // true  (loose equality: cùng "không có giá trị")
null === undefined;  // false (strict: khác kiểu — null ≠ undefined)

// Thủ thuật hay: `value != null` bắt CẢ null LẨN undefined
const maybeValue = null;
if (maybeValue != null) {    // false — bắt cả null và undefined
  console.log(maybeValue);
}

const another = undefined;
if (another != null) {       // false — cũng bắt undefined
  console.log(another);
}

const hasValue = "hello";
if (hasValue != null) {      // true — có giá trị thật
  console.log(hasValue);     // "hello"
}
```

### 3. `boolean` — `true` / `false`

Boolean là kết quả của biểu thức so sánh (`5 > 3` → `true`). Có thể chuyển đổi bằng `Boolean(value)` hoặc toán tử `!!`:

```js
console.log(Boolean(0));       // false
console.log(Boolean(""));      // false
console.log(Boolean(null));    // false
console.log(Boolean([]));      // true  — mảng rỗng vẫn "truthy"!
console.log(Boolean({}));      // true  — object rỗng cũng "truthy"!
console.log(Boolean("0"));     // true  — chuỗi "0" KHÔNG rỗng!
console.log(Boolean("false")); // true  — chuỗi chứa ký tự là truthy!
```

## 📐 Truthy / Falsy — bảng đầy đủ 8 giá trị falsy

Trong JavaScript, mọi giá trị đều có thể được "ép" thành boolean trong ngữ cảnh điều kiện (`if`, `&&`, `||`, `!`). Có đúng **8 giá trị falsy** — tất cả còn lại đều là **truthy**:

| Falsy (đúng 8 giá trị) | Truthy (mọi thứ còn lại) |
|------------------------|--------------------------|
| `false` | mọi `number` khác 0, kể cả `Infinity`, `-0` |
| `0`, `-0`, `0n` (BigInt zero) | `"0"`, `"false"`, `" "` (chuỗi chứa ký tự) |
| `""` (chuỗi rỗng) | `[]`, `{}`, `function(){}` |
| `null` | `Symbol()`, `new Date()` |
| `undefined` | |
| `NaN` | |

> **Mẹo nhớ:** "**F**alse, **Z**ero, **N**aN, **N**ull, **U**ndefined, **E**mpty string" → **"FZNNUE"** → đọc trại thành "Phải nhớ_null_undefined" trong đầu.

```js
// Kiểm chứng falsy
console.log(Boolean(false));       // false
console.log(Boolean(0));           // false
console.log(Boolean(-0));          // false
console.log(Boolean(0n));          // false
console.log(Boolean(""));          // false
console.log(Boolean(null));        // false
console.log(Boolean(undefined));   // false
console.log(Boolean(NaN));         // false

// Kiểm chứng truthy
console.log(Boolean(1));           // true
console.log(Boolean(-1));          // true
console.log(Boolean(Infinity));    // true
console.log(Boolean("0"));         // true — chuỗi "0" không rỗng!
console.log(Boolean("false"));     // true
console.log(Boolean([]));          // true — mảng rỗng vẫn truthy!
console.log(Boolean({}));          // true — object rỗng vẫn truthy!
console.log(Boolean(" "));         // true — chuỗi có khoảng trắng
```

## ✅ Điểm mạnh — Tại sao hiểu rõ 3 kiểu này quan trọng

| # | Điểm mạnh | Lý do |
|---|-----------|-------|
| 1 | **Phân biệt null/undefined** | Tránh bug hiển thị "undefined" ra UI thay vì "không có dữ liệu" |
| 2 | **Quy tắc 8 falsy** | Nhớ một lần, dùng mọi nơi — điều kiện, validation, default values |
| 3 | **Boolean/`!` đánh giá nhanh** | `!!value` chuyển mọi thứ về boolean — tiện cho validation |
| 4 | **`Boolean()` tường minh** | Code dễ đọc, tránh coercion ngầm khó đoán |
| 5 | **`value != null` pattern** | Bắt cả null và undefined — thủ thuật phổ biến trong codebase |

## ⚠️ Bẫy thường gặp & Hạn chế

| # | Bẫy | Ví dụ | Cách tránh |
|---|-----|-------|-----------|
| 1 | **`typeof null === "object"`** | Bug lịch sử, không sửa được | Dùng `=== null` thay `typeof` |
| 2 | **`null == undefined` → true, `null === undefined` → false** | Thường nhầm khi debug | Dùng `===` cho strict comparison |
| 3 | **`Boolean([])` và `Boolean({})` đều `true`** | Bẫy kinh điển khi kiểm tra mảng rỗng | Dùng `Array.isArray(arr) && arr.length === 0` |
| 4 | **`Boolean("0")` là `true`** | Chuỗi "0" không rỗng → truthy | Hiểu rõ falsy chỉ có `""` (empty string) |
| 5 | **JSON serialize bỏ `undefined`** | `{a: undefined}` → `"{}"` | Dùng `null` thay `undefined` nếu cần serialize |
| 6 | **`NaN !== NaN`** | NaN không bằng chính nó | Dùng `Number.isNaN(x)` |
| 7 | **Falsy check `if (arr)` với mảng rỗng** | `if ([])` → true — mảng rỗng vẫn truthy | Dùng `if (arr.length > 0)` thay `if (arr)` |

## 💡 Khi nào dùng — Tình huống thực tế

1. **Kiểm tra biến có tồn tại/đã gán** → `value != null` (bắt cả null lẫn undefined) hoặc `value !== undefined && value !== null`.
2. **Trả về "không có kết quả" từ hàm** → `null` (có chủ đích) thay vì để lẫn lộn với undefined.
3. **Điều kiện đúng/sai khi validation** → `if (email)` — hiểu rõ email string rỗng là falsy.
4. **Ép sang boolean tường minh** → `Boolean(input.includes("@"))` — rõ ý định hơn `!!input.includes("@")`.
5. **Default value pattern** → `const name = user.name ?? "Khách"` — nullish coalescing (ES2020).
6. **Optional chaining** → `user?.address?.city ?? "Không có"` — kết hợp `?.` và `??`.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: So sánh null và undefined

```js
console.log(typeof null);          // "object" ← BUG LỊCH SỬ!
console.log(null == undefined);    // true  (loose equality)
console.log(null === undefined);   // false (strict: khác kiểu)

let x;
console.log(x, typeof x);          // undefined "undefined"

const y = null;
console.log(y, typeof y);          // null "object"

// Pattern thường gặp: kiểm tra "có giá trị"
function greet(name) {
  if (name != null) {              // bắt cả null VÀ undefined
    return `Xin chào, ${name}!`;
  }
  return "Xin chào, Khách!";
}
console.log(greet("Nam"));         // "Xin chào, Nam!"
console.log(greet(null));          // "Xin chào, Khách!"
console.log(greet(undefined));     // "Xin chào, Khách!"
```

### Ví dụ 2: Truthy/Falsy — bảng đầy đủ

```js
// 8 falsy values
console.log(!!false);              // false
console.log(!!0);                  // false
console.log(!!-0);                 // false
console.log(!!0n);                 // false
console.log(!!"");                 // false
console.log(!!null);               // false
console.log(!!undefined);          // false
console.log(!!NaN);                // false

// Các giá trị truthy phổ biến
console.log(!!1);                  // true
console.log(!!"hello");            // true
console.log(!![]);                 // true — mảng rỗng vẫn truthy!
console.log(!!{});                 // true — object rỗng vẫn truthy!
console.log(!!function(){});       // true
console.log(!!new Date());         // true
```

### Ví dụ 3: Bẫy falsy — mảng rỗng và object rỗng

```js
// Bẫy kinh điển: if ([]) là TRUE
if ([]) {
  console.log("Mảng rỗng là truthy!"); // Dòng này CHẠY!
}

if ({}) {
  console.log("Object rỗng là truthy!"); // Dòng này CHẠY!
}

// Đúng cách kiểm tra mảng rỗng
const emptyArr = [];
if (Array.isArray(emptyArr) && emptyArr.length === 0) {
  console.log("Mảng thực sự rỗng");
}

// Đúng cách kiểm tra object rỗng
const emptyObj = {};
const keys = Object.keys(emptyObj);
if (keys.length === 0) {
  console.log("Object thực sự rỗng");
}
```

### Ví dụ 4: Default values — các pattern

```js
const user = { name: null, age: undefined };

// Pattern 1: || (logical OR) — falsy check
const displayName1 = user.name || "Khách";       // "Khách" — null falsy
const displayAge1 = user.age || 0;               // 0 — undefined falsy

// Pattern 2: ?? (nullish coalescing, ES2020) — chỉ null/undefined
const displayName2 = user.name ?? "Khách";        // "Khách" — null → default
const displayAge2 = user.age ?? 0;               // 0 — undefined → default

// DIFFERENCE quan trọng: || thay mọi falsy, ?? chỉ thay nullish
const zeroValue = 0;
console.log(zeroValue || 10);      // 10 — 0 là falsy, || thay thế
console.log(zeroValue ?? 10);      // 0  — 0 không phải nullish, ?? giữ nguyên

const emptyString = "";
console.log(emptyString || "default"); // "default"
console.log(emptyString ?? "default"); // "" — empty string giữ nguyên
```

### Ví dụ 5: Ứng dụng thực tế — validate input

```js
function validateUser(input) {
  // Kiểm tra input có giá trị (không null/undefined/empty)
  if (input == null || input === "") {
    throw new Error("Input không được để trống");
  }

  // Chuyển về string, trim
  const name = String(input).trim();

  // Kiểm tra truthy
  if (!name) {
    throw new Error("Tên không hợp lệ");
  }

  return name;
}

console.log(validateUser("  Sơn  "));   // "Sơn"
// validateUser(null);                  // Error
// validateUser("");                    // Error
```

### Ví dụ 6: Optional chaining + nullish coalescing — pattern hiện đại

```js
const company = {
  name: "F8",
  address: {
    city: "Hà Nội",
    // không có street
  }
};

// Optional chaining (?.) — an toàn truy cập nested property
const street = company?.address?.street;   // undefined — không lỗi
const city = company?.address?.city;        // "Hà Nội"
const country = company?.address?.country?.name; // undefined — safe

// Nullish coalescing (??) — default value
const displayStreet = company?.address?.street ?? "Chưa cập nhật";
console.log(displayStreet); // "Chưa cập nhật"

// Kết hợp: pattern phổ biến trong React/API handling
const userCity = user?.profile?.address?.city ?? "Không có thành phố";
```

## 🔬 So sánh với alternatives

| Phương án | Ưu điểm | Nhược điểm |
|-----------|---------|------------|
| **`value == null`** | Bắt cả null lẫn undefined — ngắn gọn | Loose equality (nói chung nên tránh `==`) |
| **`value !== null && value !== undefined`** | Strict, rõ ràng | Dài dòng |
| **`value != null`** | Ngắn gọn, strict cho null/undefined | Không bắt các falsy khác (0, "") |
| **`Boolean(value)`** | Tường minh, rõ ý định |Verbose hơn `!!value` |
| **`??` (nullish coalescing)** | ES2020, chỉ nullish → default | Không thay thế falsy khác (0, "", false) |
| **`||` (logical OR)** | Thay mọi falsy → default | Có thể thay thế giá trị hợp lệ (0, "") |

## 📊 Performance & Best Practices

- **Dùng `=== null`** thay `typeof x === "object"` để kiểm tra null — chính xác, tránh bug typeof null.
- **Dùng `value != null`** pattern — bắt cả null và undefined, ngắn gọn, phổ biến trong codebase.
- **Dùng `??` (nullish coalescing)** thay `||` khi muốn default chỉ cho nullish — giữ nguyên 0, "", false.
- **Dùng `Boolean()` hoặc `!!`** khi cần chuyển tường minh về boolean — rõ ý định hơn ngầm định.
- **Kiểm tra mảng rỗng đúng cách** — `Array.isArray(arr) && arr.length === 0` thay vì `if (arr)`.
- **Avoid `if (string)`** để check empty — dùng `string.length > 0` hoặc `string !== ""` rõ ràng hơn.
- **Throw Error thay return null** khi input invalid — fail fast, dễ debug hơn.

## 🔗 Liên kết chéo

- Xem thêm: `02_data-types/01_primitive-types/` — overview 7 primitive types
- Xem thêm: `02_data-types/03_type-casting-and-coercion/03_implicit/` — implicit coercion và truthy/falsy
- Xem thêm: `04_equality-comparisons/01_loose-strict/` — `==` vs `===` detail
- Xem thêm: `20_modern-javascript/03_optional-chaining-nullish/` — `?.` và `??` hiện đại
- Tài liệu: [MDN — null](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/null), [MDN — Undefined](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/undefined), [MDN — Truthy](https://developer.mozilla.org/en-US/docs/Glossary/Truthy)
