# JSON (Structured Data) — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

**JSON** (JavaScript Object Notation) là định dạng **dữ liệu dạng chuỗi** (text) dựa trên cú pháp object JavaScript. JSON là **"ngôn ngữ chung"** của web: API REST trả về JSON, `localStorage` lưu JSON string, hầu hết client-server communication đều dùng JSON.

### 6 loại giá trị JSON hợp lệ

| Loại | Cú pháp | Ví dụ |
|------|---------|-------|
| **Object** | `{ "key": value }` | `{"name": "Sơn", "age": 23}` |
| **Array** | `[value1, value2]` | `[1, 2, 3]` |
| **String** | `"text"` | `"Hello, JavaScript!"` |
| **Number** | `123`, `-45.6` | `42`, `3.14` |
| **Boolean** | `true`, `false` | `true` |
| **Null** | `null` | `null` |

> ❌ **KHÔNG hợp lệ trong JSON:** `undefined`, `function`, `Symbol`, `Date` object (chỉ serialize thành ISO string), `NaN`, `Infinity`.

### Hai hàm cốt lõi

```js
// Serialize: object/array → JSON string
JSON.stringify(value, replacer?, space?)

// Deserialize: JSON string → object/array
JSON.parse(text, reviver?)
```

## 📐 Cấu trúc nhóm

```
03_data-structures/04_json/
├── README.md         ← bài này
├── app.js            ← demo JSON.parse/stringify
└── index.html
```

## ✅ Điểm mạnh

- **Chuẩn universal** — mọi ngôn ngữ đều có JSON parser.
- **Human-readable** — dễ debug, dễ viết tay.
- **Native support** — browser và Node.js đều có `JSON` built-in.
- **Compact** — nhỏ hơn XML đáng kể, parse nhanh.
- **Type-safe với schema** — kết hợp JSON Schema validate structure.

## ⚠️ Bẫy thường gặp

| # | Bẫy | Ví dụ | Cách tránh |
|---|-----|-------|-----------|
| 1 | **Mất `undefined`, `function`, `Symbol`** | `{a: undefined}` → `"{}"` | Chuyển về string/null trước stringify |
| 2 | **Date → ISO string** | `new Date()` → `"2024-01-01T..."` | Custom replacer khôi phục Date |
| 3 | **Circular reference → TypeError** | `a.self = a; JSON.stringify(a)` | Dùng replacer hoặc library (flatted) |
| 4 | **JSON.parse không validate type** | `JSON.parse("42")` → number 42 | Post-parse validation required |
| 5 | **`JSON.stringify` không gọi getter** | `{ get x() { return 1; } }` → `"{}"` | Copy values explicitly |

```js
// Bẫy 1: mất undefined/function
const special = {
  num: NaN,
  undef: undefined,
  fn: () => "hello",
  sym: Symbol("id"),
  date: new Date("2024-01-01"),
};
console.log(JSON.stringify(special));
// '{"date":"2024-01-01T00:00:00.000Z"}'
// NaN → bị bỏ qua
// undefined → bị bỏ qua
// function → bị bỏ qua
// Symbol → bị bỏ qua
// Date → chuyển thành ISO string
```

## 💡 Khi nào dùng

- **Gửi/nhận dữ liệu với server API** — HTTP body JSON là standard.
- **Lưu dữ liệu vào `localStorage` / `sessionStorage`** — chỉ lưu được string.
- **Configuration files** — `package.json`, `tsconfig.json` đều là JSON.
- **Clipboard/data transfer** — paste JSON between apps.
- **Logging structured data** — log object dạng string readable.

## 🎯 Ví dụ minh họa

### Ví dụ 1: Basic parse and stringify

```js
const apiData = '{"users":[{"name":"Sơn"},{"name":"Nam"}]}';
const parsed = JSON.parse(apiData);
console.log(parsed.users[0].name); // "Sơn"

const user = { name: "Sơn", age: 23, active: true };
console.log(JSON.stringify(user));
// '{"name":"Sơn","age":23,"active":true}'

console.log(JSON.stringify(user, null, 2));
// {
//   "name": "Sơn",
//   "age": 23,
//   "active": true
// }
```

### Ví dụ 2: Replacer và Reviver — transform data

```js
const user = { name: "Sơn", age: 23, scores: [90, 85] };

// Replacer: chỉ export key "name"
console.log(JSON.stringify(user, ["name"], 2));
// { "name": "Sơn" }

// Replacer: transform giá trị (Nhân đôi age)
console.log(JSON.stringify(user, (key, value) => {
  if (key === "age") return value * 2;
  return value;
}, 2));
// { "name": "Sơn", "age": 46, "scores": [90, 85] }

// Reviver: khôi phục Date từ ISO string
const event = { name: "Meeting", time: new Date() };
const json = JSON.stringify(event);
const restored = JSON.parse(json, (key, value) => {
  if (typeof value === "string" && /^\d{4}-\d{2}-\d{2}T/.test(value)) {
    return new Date(value);
  }
  return value;
});
console.log(restored.time instanceof Date); // true
```

### Ví dụ 3: localStorage với JSON — pattern hoàn chỉnh

```js
// Save to localStorage
const cart = [{ id: 1, name: "Laptop", price: 25000000 }];
localStorage.setItem("cart", JSON.stringify(cart));

// Load from localStorage — null-safe pattern
const stored = JSON.parse(localStorage.getItem("cart") ?? "null");
console.log(stored[0].name); // "Laptop"

// Helper function
function storageGet(key, fallback = null) {
  const raw = localStorage.getItem(key);
  if (raw === null) return fallback;
  try { return JSON.parse(raw); }
  catch { return fallback; }
}
function storageSet(key, value) {
  localStorage.setItem(key, JSON.stringify(value));
}
storageSet("user", { name: "Sơn", role: "admin" });
console.log(storageGet("user")); // { name: 'Sơn', role: 'admin' }
```

### Ví dụ 4: Circular reference — xử lý thế nào

```js
const circular = { name: "parent" };
circular.self = circular; // self-reference!

// ❌ JSON.stringify(circular) → TypeError: Converting circular structure to JSON

// ✅ Tùy chọn 1: replacer để bỏ circular ref
console.log(JSON.stringify(circular, (key, value) => {
  if (key === "self") return "[Circular]";
  return value;
}));
// {"name":"parent","self":"[Circular]"}

// ✅ Tùy chọn 2: thư viện flatted xử lý circular reference
// npm install flatted
// const { stringify, parse } = require("flatted");
// stringify(circular); // {"0":{"name":"parent","self":"$0"}}
```

### Ví dụ 5: Error handling khi parse

```js
function safeParse(jsonStr, fallback = null) {
  try {
    return JSON.parse(jsonStr);
  } catch (e) {
    if (e instanceof SyntaxError) {
      console.warn("Invalid JSON:", e.message);
    }
    return fallback;
  }
}

safeParse('{"valid": true}');       // { valid: true }
safeParse("{invalid}");             // null (fallback), logs warning
safeParse('not json at all');       // null (fallback), logs warning
```

## 🔬 So sánh với alternatives

| Định dạng | Ưu điểm | Nhược điểm |
|-----------|---------|------------|
| **JSON** | Universal, human-readable, native JS support | Không hỗ trợ Date, function, undefined |
| **XML** | Schema validation, namespaces | Verbose, heavy, hard to parse manually |
| **YAML** | Human-friendly, comments supported | Slower parse, security concerns with eval |
| **MessagePack** | Compact binary, supports Date/binary | Not human-readable, requires library |
| ** BSON** | MongoDB standard, supports all BSON types | MongoDB-specific, not universal |

## 📊 Performance & Best Practices

- **Cache parsed result** — `JSON.parse` expensive; gọi 1 lần lưu vào biến.
- **Prefer `JSON.parse(text)` not `eval(text)`** — eval execute code, JSON.parse chỉ parse data.
- **Use replacer/reviver for type preservation** — custom handling cho Date, BigInt.
- **Always wrap in try/catch** — malformed JSON throws `SyntaxError`.
- **Limit JSON depth** — deep nesting causes memory explosion on parse.
- **Use JSONSchema** for validation of API responses — catch structural errors early.
- **Compress large payloads** — gzip JSON before send over network (transfer encoding).
- **Avoid JSON.stringify for circular objects** — use `flatted` library or custom replacer.

## 🔗 Liên kết chéo

- Xem thêm: `02_data-types/04_builtin-objects/` — built-in objects overview
- Xem thêm: `03_data-structures/` — data structures group
- Xem thêm: `13_working-with-apis/01_fetch/` — fetch returns JSON from API
- Tài liệu: [MDN — JSON](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON)
