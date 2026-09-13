# Value types và Reference types

## 🔑 Khái niệm

JavaScript chia thành hai nhóm theo **cách lưu và gán giá trị**:

**1. Value type (kiểu tham trị) — primitive:**
Mỗi lần gán hoặc truyền vào hàm, giá trị được **sao chép vào ô nhớ mới hoàn toàn**. Biến `b = a` tạo bản sao độc lập — thay đổi `a` sau đó không ảnh hưởng `b`.

```js
let a = 1;
let b = a;    // sao chép GIÁ TRỊ
a = 2;
console.log(b); // 1 — b vẫn là 1
```

- Tất cả primitive đều là value type: `string`, `number`, `boolean`, `bigint`, `symbol`, `undefined`, `null`.

**2. Reference type (kiểu tham chiếu) — object, array, function:**
Biến chỉ lưu **tham chiếu (địa chỉ)** trỏ đến object trong bộ nhớ. Khi `b = a`, cả hai biến trỏ cùng một object — sửa `a` sẽ thấy kết quả ở `b`.

```js
let a = { name: "Mercedes" };
let b = a;       // cả hai trỏ CÙNG MỘT object
a.name = "BMW";
console.log(b);  // { name: "BMW" } — b cũng đổi theo
console.log(b === a); // true — cùng tham chiếu
```

**Vấn đề thường gặp:** `const` không ngăn thay đổi nội dung object/array:

```js
const arr = { name: "Sơn" };
arr.name = "Nguyễn"; // OK — đổi nội dung object
console.log(arr);     // { name: "Nguyễn" }
// arr = {};           // TypeError — không gán lại được tham chiếu
```

**Khi truyền primitive vào hàm → giá trị sao chép:**

```js
function sum(a, b) {
  a = 0;
  b = 0;
  console.log(a, b); // 0 0
}
const c = 1;
const d = 2;
sum(c, d);           // 0 0
console.log(c, d);   // 1 2 ← gốc không bị ảnh hưởng
```

**Khi truyền object vào hàm → truyền tham chiếu (nhưng vẫn "giống copy" vì ta chỉ modify nội dung):**

```js
function updateName(obj) {
  obj.name = 'Mercedes';
}
const f = { name: 'BMW' };
updateName(f);
console.log(f); // { name: 'Mercedes' }
```

## ✅ Điểm mạnh

- Primitive an toàn khi truyền vào hàm — không lo bị thay đổi ngoài ý muốn.
- Object/shared data dùng tham chiếu → tiết kiệm bộ nhớ, thay đổi đồng bộ.
- Hiểu cơ chế này giúp dùng đúng `const` (không phải "bất biến") và tránh bug khi copy dữ liệu.
- Biết khi nào cần **deep copy** (structuredClone, JSON.parse/stringify) thay vì spread shallow copy.

## ⚠️ Lưu ý / Hạn chế

- `let b = a` với object **không tạo bản sao** — cả hai cùng trỏ một chỗ.
- `const` với object chỉ khóa tham chiếu, **không đóng băng nội dung** (dễ hiểu sai).
- `===` so sánh primitive theo giá trị, so sánh object theo tham chiếu (cùng reference).
- Shallow copy (`{...obj}` hay `[...arr]`) chỉ copy một lớp — object lồng nhau vẫn bị dính.
- `JSON.parse(JSON.stringify(obj))` mất giá trị đặc biệt: `undefined`, `function`, `Date` → “…”.

## 💡 Khi nào dùng

- Primitive: lưu ID, số, chuỗi — muốn mỗi biến tự trị, thay đổi không "lây".
- Object: lưu cấu trúc dữ liệu phức tạp (user, product, config) — muốn share chung.
- Khi cần giữ nguyên object gốc → copy sâu (`structuredClone`, `JSON.parse(JSON.stringify(obj))`, hoặc library `lodash`).
- Truyền object vào hàm có thể "accidentally modify" → cần cẩn thận hoặc tạo bản sao trước khi dùng.

## 🎯 Ví dụ minh họa

```js
// Value type — primitive
let x = "hello";
let y = x;
x = "world";
console.log(y);       // "hello" — không đổi

// Reference type — object
let obj1 = { a: 1 };
let obj2 = obj1;      // cùng tham chiếu
obj1.a = 99;
console.log(obj2.a);  // 99

// Reference type — array
const arr = [1, 2, 3];
const arr2 = arr;
arr2.push(4);
console.log(arr);     // [1, 2, 3, 4] — arr cũng đổi!

// Truyền primitive vào hàm
function doi(a) { a = 100; }
let v = 1;
doi(v);
console.log(v);       // 1 — không thay đổi
```

## 📚 Tham khảo / Bài tập

- Chạy `app.js` trong thư mục (mở `index.html` → Console hoặc `node app.js`): demo object const đổi nội dung được, và hàm nhận primitive (c, d) bị set = 0 nhưng giá trị gốc không thay đổi — minh chứng copy theo giá trị.
- Tự thử: 1) thêm hàm `updateName(obj)` nhận object và sửa `obj.name`, gọi nó và quan sát; 2) dùng `structuredClone(obj)` copy một object lồng nhau, sửa object copy và xác nhận object gốc không đổi.
- Tài liệu: [MDN — Reference types](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures), [javascript.info/variables](https://javascript.info/variables).