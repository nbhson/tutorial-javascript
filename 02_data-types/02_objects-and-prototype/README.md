# Objects và Prototype

## 🔑 Khái niệm

Trong JavaScript, **object** là kiểu tham chiếu lưu dữ liệu dạng cặp **khóa – giá trị** (`property: value`), trong đó giá trị có thể là dữ liệu hoặc hàm (khi đó gọi là **method**). Gần như mọi thứ trong JS đều là object hoặc kế thừa từ object: array, function, Date, RegExp...

**Prototype** là nền tảng của object: mỗi object đều "mang theo" một prototype — một object khác để **học theo**. Khi truy cập một thuộc tính không có sẵn, JS lần qua **chuỗi prototype (prototype chain)** từ trong ra ngoài cho đến khi gặp `null`.

Nhóm này gồm 3 bài con:

- `01_object-basics/` — tạo và thao tác object, constructor function, prototype.
- `02_functions-as-objects/` — vì sao "hàm cũng là object" và các loại hàm.
- `03_shallow-deep-clone/` — copy object đúng cách (shallow vs deep).

## ✅ Điểm mạnh

- Object là "đơn vị dữ liệu" linh hoạt: thêm/xóa/key thuộc tính bất cứ lúc nào.
- Prototype giúp tái sử dụng phương thức cho hàng nghìn instance mà không tốn bộ nhớ.
- Constructor function là cách "OOP kiểu cũ" nền tảng — hiểu để đọc code cũ và class ES6.
- Clone đúng cách (structuredClone, lodash) bảo vệ dữ liệu gốc khỏi bị sửa ngoài ý muốn.
- Hàm là object → có thể mang thêm `length`, `name`, `arguments`, properties.

## ⚠️ Lưu ý / Hạn chế

- `person2 = person1` không phải "clone", chỉ tăng tham chiếu — ai sửa ai cũng thấy.
- Object / array là reference type (học ở `01_primitive-types/03_value-vs-reference`).
- Shallow copy (`{...obj}`, `Object.assign`) không sâu nhất — lớp lồng nhau vẫn dính.
- `JSON.parse(JSON.stringify(obj))` mất `undefined`, `function`, và làm `NaN`→`null`, `Date`→string.
- Prototype chain có thể khiến debug khó nếu không chú ý: sửa `Object.prototype` là "đừng làm".

## 💡 Khi nào dùng

- Lưu dữ liệu có cấu trúc (user, product, cart) → object literal.
- Chia sẻ phương thức dùng chung → gắn vào `prototype` thay vì lặp trong từng instance.
- Tạo nhiều đối tượng cùng "khuôn" → constructor function / class.
- Cần bản sao độc lập để sửa mà không phá dữ liệu gốc → deep clone.

## 🎯 Ví dụ minh họa

```js
const user = {
  name: "Sơn",
  getFullName() {
    return `${this.name} Nguyễn`;
  },
};
console.log(user.getFullName()); // Sơn Nguyễn

// Prototype — chia sẻ phương thức
function Person(firstName) { this.firstName = firstName; }
Person.prototype.who = function () { return `Tôi là ${this.firstName}`; };
const p = new Person("Nam");
console.log(p.who()); // Tôi là Nam

// Deep clone
const original = { a: { b: 1 } };
const copy = structuredClone(original);
copy.a.b = 99;
console.log(original.a.b); // 1 — gốc không đổi
```

## 📚 Tham khảo / Bài tập

- Lần lượt học 3 bài con trong nhóm, mỗi bài đều có file thực hành: `01_object-basics` (`1_object.js`, `2_object_constructor.js`, `3_object_prototype.js`), `02_functions-as-objects` (`1_app.js`, `2_Cac-loai-function.js`), `03_shallow-deep-clone` (`app.js`).
- Chạy từng file bằng `node <file>.js` và quan sát console.
- Tự thử: tạo object hình chữ nhật với 2 thuộc tính + method `dienTich()`; sau đó nâng lên constructor function dùng prototype.