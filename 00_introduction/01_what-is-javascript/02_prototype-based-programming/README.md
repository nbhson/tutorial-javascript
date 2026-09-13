# Prototype-based Programming — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

**Prototype-based programming** là một phong cách **lập trình hướng đối tượng** trong đó **không có khái niệm "class" được định nghĩa tường minh** (trước ES6). Thay vì định nghĩa blueprint (khuôn mẫu) rồi tạo đối tượng từ nó, JavaScript cho phép:

1. **Tạo đối tượng trực tiếp** từ đối tượng rỗng hoặc object literal `{}`.
2. **Một đối tượng mới kế thừa** từ một đối tượng có sẵn (gọi là *prototype*) qua cơ chế **prototype chain** — chuỗi các object nối tiếp nhau bằng `__proto__` (truy cập qua `Object.getPrototypeOf()`).
3. **Thêm/sửa thuộc tính và phương thức** bất cứ lúc nào — tính dynamic của prototype là sức mạnh cốt lõi.

### Cơ chế hoạt động bên trong JavaScript engine

Khi bạn truy cập `obj.tênThuộcTính`, engine thực hiện **prototype lookup** theo các bước sau:

1. Kiểm tra xem `obj` có sở hữu thuộc tính `tênThuộcTính` không (own property). Nếu có → trả về giá trị, dừng.
2. Nếu không, engine theo `obj.__proto__` (prototype của `obj`) — tìm thuộc tính đó trong object prototype.
3. Tiếp tục leo lên chuỗi: `prototype.__proto__` → `Object.prototype.__proto__` → `null`.
4. Nếu tìm hết chuỗi mà không thấy → trả về `undefined`.

Đây gọi là **prototype chain**. Mỗi object trong JavaScript (trừ `Object.create(null)`) đều có một prototype — và prototype đó cũng là một object, cũng có prototype của riêng nó. Chuỗi kết thúc tại `null`.

```
obj
 └── __proto__ → Person.prototype
      └── __proto__ → Object.prototype
           └── __proto__ → null
```

### Cách tạo đối tượng trong JavaScript

| Cách | Cú pháp | Ghi chú |
|------|---------|---------|
| Object literal | `const obj = { a: 1 }` | Prototype mặc định là `Object.prototype` |
| `Object.create()` | `const obj = Object.create(proto)` | Tạo object kế thừa trực tiếp từ `proto` |
| Constructor function | `function Person() {}` + `new Person()` | Gắn method qua `Person.prototype` |
| ES6 `class` | `class Person {}` | Syntactic sugar trên constructor + prototype — bản chất vẫn là prototype |

## 📐 Cấu trúc / Cú pháp

```js
// Cách 1: Object literal
const person = {};
person.tên = "Sơn";
person.chào = function () {
  return `Xin chào, tôi là ${this.tên}`;
};

// Cách 2: Object.create — kế thừa tường minh
const độngVật = {
  thở() { console.log("thở bằng phổi"); },
};
const chó = Object.create(độngVật);
chô.tên = "Buddy";
chó.thở(); // "thở bằng phổi" — từ prototype

// Cách 3: Constructor function + prototype
function Người(tên, tuổi) {
  this.tên = tên;
  this.tuổi = tuổi;
}
// Gắn method chung vào prototype — tiết kiệm bộ nhớ
Người.prototype.chào = function () {
  return `Tôi là ${this.tên}, ${this.tuổi} tuổi`;
};
const ngườIMới = new Người("Hoa", 25);

// Cách 4: ES6 class (syntactic sugar)
class NgườiTuyendt {
  constructor(tên, tuổi) {
    this.tên = tên;
    this.tuổi = tuổi;
  }
  chào() {
    return `Tôi là ${this.tên}, ${this.tuổi} tuổi`;
  }
}
// Về bản chất: class → constructor function + prototype methods
```

## ✅ Điểm mạnh — Tại sao nên dùng

| # | Điểm mạnh | Lý do & Khi nào |
|---|-----------|----------------|
| 1 | **Linh hoạt / dynamic** | Thêm, sửa, xóa thuộc tính bất cứ lúc nào — không cần biên dịch lại |
| 2 | **Tiết kiệm bộ nhớ qua prototype chain** | Phương thức đặt trên prototype dùng chung cho hàng nghìn instance |
| 3 | **Không cần boilerplate class** | Tạo object nhanh, prototyping MVP nhanh hơn |
| 4 | **Kế thừa thay đổi đồng bộ** | Sửa một method trên prototype → tất cả instance thấy ngay |
| 5 | **Mở rộng runtime** | Thêm method vào prototype của built-in object (cẩn trọng — xem bẫy) |
| 6 | **Foundation của ES6 class** | Hiểu prototype → hiểu `class` ES6 thực chất hoạt động thế nào |
| 7 | **Polyfill-friendly** | Thêm tính năng mới vào built-in prototype để tương thích ngược |
| 8 | **Flexible inheritance** | Kế thừa từ bất kỳ object nào, không bị giới hạn "single class tree" |

## ⚠️ Bẫy thường gặp & Hạn chế

| # | Bẫy | Ví dụ code |
|---|-----|-----------|
| 1 | **`Object.create(null)` không có prototype** | `const obj = Object.create(null); obj.toString` → `undefined` — mất các method mặc định |
| 2 | **Monkey-patching global prototype** | `Array.prototype.push = ...` — ảnh hưởng TẤT CẢ mảng trong app, có thể phá code thư viện khác |
| 3 | **Khó truy vết hơn class** | Prototype chain dài, debug khó; nhiều team chọn `class` ES6 để rõ ràng hơn |
| 4 | **Kiểm tra kiểu bằng `instanceof` không an toàn** | `obj instanceof Person` chỉ đúng nếu prototype chain khớp — iframe khác nhau sẽ sai |
| 5 | **Ghi đè prototype accidental** | `Person.prototype = { ... }` sau khi đã tạo instance → instance cũ không thấy prototype mới |
| 6 | **Thuộc tính prototype không enumerable** | `for...in` bỏ qua method trên prototype nếu không setup đúng |
| 7 | **Constructor không phải lúc nào cũng `new`** | Gọi `Person()` thiếu `new` → `this` trỏ `window` (hoặc `undefined` trong strict mode) |
| 8 | **ES6 `class` khiến người mới nghĩ JS có class thật** | `class` ES6 chỉ là syntactic sugar — bản chất vẫn là prototype, không phải compile-time class |

## 💡 Khi nào dùng — Tình huống thực tế

1. **Tạo họ đối tượng chia sẻ hành vi chung** — động vật, phương tiện, nhân vật game — không cần class blueprint.
2. **Define polyfill / thêm tiện ích** — thêm method vào `Array.prototype` cho trình duyệt cũ (làm cẩn thận).
3. **Kế thừa từ đối tượng model có sẵn** — ORM, mô hình dữ liệu từ API — dùng `Object.create()` để mở rộng.
4. **Hiểu cách `class` ES6 hoạt động** — debug lỗi prototype chain, tối ưu bộ nhớ, viết library.
5. **Cache metadata gắn với object** — dùng `WeakMap` (xem `03_data-structures/02_keyed-collections/02_weakmap/`) thay vì thêm property vào object.
6. **Tạo singleton / factory** — object duy nhất được chia sẻ, instance mới kế thừa cấu hình từ factory.
7. **Mixin pattern** — ghép nhiều prototype lại thành một object lai (common trong thư viện như jQuery, Ember).

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Tạo đối tượng từ object rỗng

```js
// Tạo object trống, thêm thuộc tính động
const person = {};
person.tên = "Nguyễn Văn A";
person.nămSinh = 1990;
person.chào = function () {
  return `Xin chào, tôi là ${this.tên}, sinh năm ${this.nămSinh}`;
};
console.log(person.chào());          // "Xin chào, tôi là Nguyễn Văn A, sinh năm 1990"

// Kiểm tra prototype chain
console.log(Object.getPrototypeOf(person) === Object.prototype); // true
```

### Ví dụ 2: Object.create — kế thừa tường minh

```js
// Prototype gốc: hành vi chung của động vật
const độngVật = {
  thở() { console.log("Đang thở..."); },
  diChuyển() { console.log("Đang di chuyển..."); },
};

// Tạo chó kế thừa từ độngVật
const chó = Object.create(độngVật);
chô.tên = "Buddy";
chó.tuổi = 3;

// Chó dùng phương thức từ prototype
chô.thở();                          // "Đang thở..."
chô.diChuyển();                     // "Đang di chuyển..."

// Chó override phương thức riêng
chô.sủa = function () {
  console.log("Gâu gâu! Tên tôi là " + this.tên);
};
chô.sủa();                          // "Gâu gâu! Tên tôi là Buddy"
```

### Ví dụ 3: Constructor function + prototype (OOP kiểu cũ)

```js
// Constructor function — tạo instance mới
function NhãnHieu(tên, năm) {
  this.tên = tên;
  this.năm = năm;
  // Method đặt trong constructor — MỖI instance có bản sao riêng (tốn bộ nhớ)
  this.getInfo = function () {
    return `${this.tên} (${this.năm})`;
  };
}

// Nâng cấp: đặt method lên prototype — dùng chung cho tất cả instance
NhãnHieu.prototype.toString = function () {
  return `[NhãnHiệu: ${this.tên}, ${this.năm}]`;
};

const honda = new NhãnHieu("Honda", 1948);
const toyota = new NhãnHieu("Toyota", 1937);

console.log(honda.getInfo());        // "Honda (1948)"
console.log(toyota.getInfo());       // "Toyota (1937)"
console.log(honda.toString === toyota.toString); // true — cùng function object trên prototype!
```

### Ví dụ 4: Kiểm tra prototype chain

```js
const a = {};
console.log(a.__proto__ === Object.prototype);       // true
console.log(Object.getPrototypeOf(a) === Object.prototype); // true (cách hiện đại)

// Object.create(null) — không có prototype
const b = Object.create(null);
console.log(b.__proto__);                            // undefined
console.log(Object.getPrototypeOf(b));               // null
console.log(b.toString);                             // undefined — không có method mặc định

// Custom prototype
const proto = { x: 10 };
const c = Object.create(proto);
console.log(c.x);                                    // 10 — từ prototype
console.log(Object.getPrototypeOf(c) === proto);     // true
```

### Ví dụ 5: ES6 class — bản chất vẫn là prototype

```js
// Class syntax (ES6)
class SinhViên {
  constructor(tên, mãSinhViên) {
    this.tên = tên;
    this.mãSinhViên = mãSinhViên;
  }
  // Method được đặt lên SinhViên.prototype, KHÔNG phải từng instance
  giớiThiệu() {
    return `Tôi là ${this.tên}, mã SV: ${this.mãSinhViên}`;
  }
}

const sv1 = new SinhViên("Lan", "SV001");
const sv2 = new SinhViên("Mai", "SV002");

// Cả hai dùng chung một phương thức trên prototype
console.log(sv1.giớiThiệu === sv2.giớiThiệu);        // true
console.log(Object.getPrototypeOf(sv1) === SinhViên.prototype); // true

// ES6 class thực chất compiler-transpile thành:
// function SinhViên(tên, mãSinhViên) { this.tên = tên; ... }
// SinhViên.prototype.giớiThiệu = function() { ... }
```

## 🔬 So sánh với alternatives

| Phương pháp | Ưu điểm | Nhược điểm |
|------------|---------|------------|
| **Prototype raw (Object.create)** | Linh hoạt, không boilerplate | Khó đọc với người quen OOP truyền thống |
| **Constructor function + prototype** | Nền tảng JS thật sự, hiểu được class | Nhiều boilerplate, `new` dễ quên |
| **ES6 `class` (syntactic sugar)** | Cú pháp quen thuộc, rõ ràng | Same value as constructor + prototype — chỉ là syntax layer |
| **Mixin pattern** | Ghép hành vi từ nhiều source | Dễ gây name collision, khó debug |
| **Factory function** | Không cần `new`, trả về object tùy ý | Không có `instanceof`, prototype chain phẳng hơn |

## 📊 Performance & Best Practices

- **Đặt method lên prototype** thay vì trong constructor — mỗi instance chỉ trỏ đến một function object duy nhất, tiết kiệm bộ nhớ đáng kể khi có hàng nghìn instance.
- **Tránh sửa prototype của built-in object** — `Array.prototype`, `Object.prototype` là global; sửa chúng ảnh hưởng toàn bộ app và có thể phá thư viện khác.
- **Dùng `Object.create(null)` khi cần object pure** — cho cache, dictionary, hash table — tránh xung đột với các method mặc định của `Object.prototype`.
- **Kiểm tra prototype chain** — `Object.getPrototypeOf(obj)`, `obj instanceof Constructor` — hữu ích khi debug.
- **Class ES6 vẫn dùng prototype** — hiểu prototype giúp bạn debug lỗi `this`, `super`, và hiểu tại sao `instanceof` hoạt động như vậy.
- **Shallow copy qua spread `{...obj}`** giữ prototype chain — `const copy = { ...obj }` → copy vẫn kế thừa từ prototype gốc.

## 🔗 Liên kết chéo

- Xem thêm: `00_introduction/01_what-is-javascript/01_first-class-function/` — hàm là giá trị, nền tảng của prototype
- Xem thêm: `01_variables/02_hoisting/` — function declaration hoisted, function expression thì không
- Xem thêm: `02_data-types/02_objects-and-prototype/` — tổng quan object và prototype
- Xem thêm: `02_data-types/02_objects-and-prototype/01_object-basics/` — constructor function, prototype method
- Xem thêm: `02_data-types/02_objects-and-prototype/02_functions-as-objects/` — hàm cũng là object, có `prototype` property
- Xem thêm: `03_data-structures/02_keyed-collections/02_weakmap/` — WeakMap với prototype keys
- Xem thêm: `10_this-keyword/` — `this` binding ảnh hưởng bởi cách gọi method trên prototype
- Tài liệu: [MDN — Prototype](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Inheritance_and_the_prototype_chain), [javascript.info/prototype-inheritance](https://javascript.info/prototype-inheritance)
