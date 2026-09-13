# Phương thức `apply()`

## 🔑 Khái niệm

`fn.apply(thisArg, [arg1, arg2, ...])` **gọi ngay lập tức** hàm `fn` với `this` = `thisArg`, nhưng đối số được truyền **dưới dạng mảng** (array) thay vì danh sách.

Về bản chất `apply` giống hệt `call`, chỉ khác hình thức truyền đối số:

| | `call` | `apply` |
|---|--------|---------|
| Cách truyền | từng đối số: `fn.call(ctx, a, b)` | mảng: `fn.apply(ctx, [a, b])` |
| Gọi ngay | ✅ | ✅ |
| Ứng dụng nổi bật | đối số cố định | mảng/`arguments` động |

`apply` rất hợp khi số lượng đối số không biết trước — ví dụ rải (`spread`) một mảng vào hàm nhận lẻ từng giá trị như `Math.max`, `Math.min`.

## ✅ Điểm mạnh

- Làm việc tự nhiên với mảng và object `arguments` (đối số mềm của hàm).
- Dùng chung với `call` cho mọi nhu cầu mượn hàm, bind this, kế thừa.
- Khi cần gọi hàm cha trong constructor: `Parent.apply(this, arguments)` truyền thẳng toàn bộ đối số.
- Linh hoạt khi đối số đến từ mảng xây dựng động.

## ⚠️ Lưu ý / Hạn chế

- Khác `call` duy nhất ở dạng đối số — đừng nhầm lẫn thứ tự: `apply` luôn cần **mảng** ở tham số thứ 2.
- `arguments` không phải array thật (thiếu `map`, `filter`...) — cần `Array.prototype` mượn thêm nếu xử lý phức tạp.
- Với đối số cố định thì dùng `call` gọn hơn.
- `apply` cũng gọi ngay, không tạo hàm mới để dùng cho callback.

## 💡 Khi nào dùng

- Gọi constructor cha: `Animal.apply(this, arguments)`.
- `Math.max.apply(null, numbers)` tìm max của mảng không biết trước độ dài.
- Ghép/gộp mảng vào hàm nhận danh sách.
- Mượn hàm với đối số tập hợp sẵn trong mảng.

## 🎯 Ví dụ minh họa

```js
const teacher = {
  firstName: "Thu",
  lastName: "Minh",
};

function greet(greeting, message) {
  return `${greeting} ${this.firstName} ${this.lastName}, ${message}`;
}

// apply: đối số trong mảng
console.log(greet.apply(teacher, ["Em chào cô", "Cô dạy môn gì thế?"]));
// Em chào cô Thu Minh, Cô dạy môn gì thế?

// tương đương với call (danh sách)
console.log(greet.call(teacher, "Em chào cô", "Cô dạy môn gì thế?"));

// kế thừa qua arguments
function Animal(name, weight) { this.name = name; this.weight = weight; }
function Parrot() {
  Animal.apply(this, arguments); // rải toàn bộ arguments
  this.speak = function () { console.log("Nhà có khách"); };
}
new Parrot("Vẹt", 300).speak(); // Nhà có khách
```

## 📚 Tham khảo / Bài tập

- Chạy `04_apply/app.js` (qua `index.html` hoặc `node app.js`): xem `Animal.apply(this, arguments)` trong `Parrot` gán đúng `name = "Vẹt"`, `weight = 300`.
- Tự thử: viết lại bằng `Animal.call(this, "Vẹt", 300)` và so sánh; sau đó dùng `Math.max.apply(null, [3, 7, 1])` để thấy sức mạnh của mảng đối số.