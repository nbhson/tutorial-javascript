# Phương thức `call()`

## 🔑 Khái niệm

`fn.call(thisArg, arg1, arg2, ...)` **gọi ngay lập tức** hàm `fn` với `this` được gán bằng `thisArg`, các đối số truyền theo kiểu **danh sách** (list). Nếu không truyền `thisArg`, `this` mặc định là object global (window).

Khác biệt quan trọng với `bind`: `call` **không tạo hàm mới** — nó gọi luôn và trả về kết quả của hàm. `bind` chỉ khóa `this` để dùng sau.

Ba ứng dụng lớn của `call`:

1. **Bind `this` khi gọi** — `obj2.method.call(obj1)` mượn method của obj2 cho obj1.
2. **Kế thừa trong constructor** — `Parent.call(this, ...)` để child nhận property của parent.
3. **Mượn method built-in** — `Array.prototype.forEach.call(arguments, fn)` xử lý object giống mảng.

## ✅ Điểm mạnh

- Gọi hàm và ép `this` trong một cú pháp duy nhất, trả về ngay kết quả.
- Kế thừa property+method từ constructor khác không cần prototype phức tạp.
- Mượn method của Array/Math cho mọi object "giống mảng" (arguments, NodeList).
- Hoạt động tốt kể cả trong strict mode khi `this` được truyền tường minh.

## ⚠️ Lưu ý / Hạn chế

- `call()` **gọi ngay** — không dùng được để chuẩn bị hàm cho callback.
- Không truyền `thisArg` trong strict mode sẽ gây lỗi (this mặc định undefined).
- Chỉ nhận đối số **từng cái danh sách**; có sẵn mảng thì dùng `apply`.
- Kế thừa qua `call` chỉ copy property, không tự động nối prototype chain.

## 💡 Khi nào dùng

- Gọi constructor cha ngay trong constructor con: `Animal.call(this, name, weight)`.
- Mượn array method cho `arguments`/`NodeList`: `[].forEach.call(...)`, `[].slice.call(...)`.
- Ép `this` tức thời khi muốn chạy hàm với object khác ngay lập tức.

## 🎯 Ví dụ minh họa

```js
function Animal(name, weight) {
  this.name = name;
  this.weight = weight;
}

function Chicken(name, weight, legs) {
  Animal.call(this, name, weight); // kế thừa name, weight
  this.legs = legs;
}

const son = new Chicken("Sơn", 53, 2);
console.log(son); // Chicken { name: "Sơn", weight: 53, legs: 2 }

// mượn hàm
const me = { firstName: "Sơn", lastName: "Nguyễn" };
function showFullName() {
  console.log(`${this.firstName} ${this.lastName}`);
}
showFullName.call(me); // Sơn Nguyễn
```

## 📚 Tham khảo / Bài tập

- Chạy `03_call/app.js` (qua `index.html` hoặc `node app.js`): file demo `Animal.call(this, name, weight)` trong `Chicken` — chú ý dòng comment `Animal.bind(...)` không hoạt động để sinh property.
- Tự thử: đổi `Animal.call(this, name, weight)` thành `Animal(this, name, weight)` (không có `.call`) và giải thích vì sao `this.name` không được gán.