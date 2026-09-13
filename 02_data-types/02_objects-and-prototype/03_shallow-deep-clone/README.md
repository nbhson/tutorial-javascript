# Shallow vs Deep Clone (Copy nông vs Copy sâu)

## 🔑 Khái niệm

Khi "copy" một object/array, JavaScript chỉ gán **tham chiếu** nếu bạn viết `const person2 = person1`. Muốn thật sự có một bản sao độc lập, bạn cần **clone**. Có hai mức:

**1. Shallow copy (copy nông)** — chỉ copy **tầng đầu tiên**. Tầng sâu (object/mảng lồng nhau) **vẫn dính tham chiếu** với bản gốc:

```js
const person1 = {
  name: "Sơn",
  age: 22,
  networks: { facebook: "http://facebook.com" },
};

// Các cách shallow copy:
const a = { ...person1 };
const b = Object.assign({}, person1);   // Chú ý: dùng đối số "đích" rỗng {}

// Đổi networks.facebook → các bản clone cũng đổi theo (vì cùng tham chiếu!)
person1.networks.facebook = "http://facebook.com/nbhson43";
console.log(b.networks.facebook); // "http://facebook.com/nbhson43" ← dính!
```

> Lưu ý `Object.assign`: đối số **đầu tiên** là object đích — nếu bạn ghi `Object.assign(person1, {...})` thì chính `person1` bị sửa. Luôn đặt "đích" rỗng.

**2. Deep copy (copy sâu)** — tạo bản sao **hoàn toàn độc lập**, mọi tầng đều được nhân bản:

```js
// Cách truyền thống: JSON
const person2 = JSON.parse(JSON.stringify(person1));
```

Tuy nhiên **JSON clone có yếu điểm**: các giá trị đặc biệt bị "phá" — `NaN` → `null`, `Date` → string chuỗi ISO, và **mất** `undefined`/`function`.

**3. Giải pháp hiện đại — `structuredClone` (có từ ES2022, trình duyệt/Node hiện tại đều hỗ trợ):**

```js
const obj = {
  firstName: "David",
  moreInfo: {
    age: 18,
    countries: { anGiang: true, hoChiMinh: true },
    birthday: new Date(),   // Date giữ nguyên là Date ✓
    love: NaN,              // NaN giữ nguyên ✓
  },
};

const objCopy = structuredClone(obj);
objCopy.moreInfo.age = 25;                        // sửa bản copy
objCopy.moreInfo.countries.hoChiMinh = false;

console.log(objCopy);                             // đã đổi
console.log(obj);                                 // gốc KHÔNG đổi ✓
```

> **Tóm tắt công cụ:** `person2 = person1` → không phải clone (chỉ chung tham chiếu). `{...obj}` / `Object.assign({}, obj)` → shallow. `JSON.parse(JSON.stringify(obj))` → deep nhưng dính NaN/Date/function. `structuredClone(obj)` → deep, xử lý tốt các kiểu đặc biệt (dùng làm lựa chọn mặc định). Với dự án lớn, có thể dùng thư viện **lodash** (`_.cloneDeep`).

## ✅ Điểm mạnh

- Hiểu shallow/deep → biết được "bản sao đó có tách khỏi gốc hay không".
- `structuredClone` deep copy an toàn với `Date`, `NaN`, Map/Set... không cần thư viện.
- Shallow copy nhanh và đủ dùng cho object "một tầng" (config, props).
- Tránh bug "sửa copy làm đổi cả gốc" — nguyên nhân số 1 khi xử lý dữ liệu form/state.

## ⚠️ Lưu ý / Hạn chế

- `const b = a` **không** phải clone — chỉ thêm một "biệt danh" trỏ cùng vùng nhớ.
- Shallow copy không tách lớp lồng nhau → `person1.networks` vẫn dính.
- JSON clone làm hỏng `NaN` → `null`, `Date` → string, mất `undefined`, mất `function`.
- `structuredClone` chưa server-side (cũ nhất) hỗ trợ; sử dụng node/browser các bản hiện tại đều OK, kiểm tra nếu cần hỗ trợ cũ.

## 💡 Khi nào dùng

- Sửa dữ liệu form mà không muốn động đến giá trị gốc (state management — React/Vue).
- Lưu "snapshot" dữ liệu cấu hình trước khi đổi.
- Object đơn tầng → `{...obj}` (nhanh). Object lồng nhau hoặc chứa Date/NaN → `structuredClone`.
- Codebase cũ/cần tương thích mọi nơi → lodash `cloneDeep`.

## 🎯 Ví dụ minh họa

```js
const goc = { a: 1, nested: { b: 2 } };

// 1. Không clone: chỉ tham chiếu
const dongThamChieu = goc;

// 2. Shallow: tầng trong vẫn dính
const shallow = { ...goc };
goc.nested.b = 99;
console.log(shallow.nested.b); // 99 ← dính

// 3. Deep (JSON) — cẩn thận với NaN/Date
const deepJson = JSON.parse(JSON.stringify(goc));

// 4. Deep (structuredClone) — khuyên dùng
const deep = structuredClone(goc);
goc.nested.b = 1;
console.log(deep.nested.b); // 99 ← đã tách
```

## 📚 Tham khảo / Bài tập

- Chạy `app.js` trong thư mục (mở `index.html` → Console hoặc `node app.js`): nó demo shallow (`{...person1}`, `Object.assign`) bị dính tầng `networks`, JSON clone "phá" `NaN`/`Date`, và so sánh `structuredClone` giữ đúng các giá trị này.
- Tự thử: 1) bỏ comment ba dòng shallow ở trên và chạy để thấy dính; 2) thử `structuredClone` với một object chứa cả `Map` và `Set`; 3) dùng `JSON.parse(JSON.stringify(...))` clone một object chứa `function` và quan sát hàm "biến mất".
- Tài liệu: [MDN — structuredClone](https://developer.mozilla.org/en-US/docs/Web/API/structuredClone).