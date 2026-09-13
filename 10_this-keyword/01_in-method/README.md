# `this` bên trong method của object

## 🔑 Khái niệm

Khi một hàm được gọi **dưới dạng method** của một object (`obj.method()`), quy tắc **implicit binding** được áp dụng: `this` bên trong hàm chính là **object đang gọi method đó**.

```js
obj.hi(); // this bên trong hi() === obj
```

Nếu object có object con (nested object), `this` sẽ trỏ tới **object ngay trước dấu chấm gọi** — chính là object trực tiếp sở hữu method, không phải object ngoài cùng.

## ✅ Điểm mạnh

- Viết code hướng object tự nhiên: method truy cập trực tiếp dữ liệu của chính nó.
- Cùng một method nhưng mỗi object lại trả về dữ liệu của riêng mình.
- Không phải khai báo biến global, dữ liệu "đóng gói" trong từng object.
- Kết hợp tốt với prototype/class để dùng chung method giữa nhiều object.

## ⚠️ Lưu ý / Hạn chế

- `this` chỉ đúng khi gọi qua `obj.method()`; gán `const fn = obj.method` rồi gọi `fn()` sẽ mất context.
- Với object lồng nhau, `this` là object **trực tiếp** chứa method (đứng ngay trước dấu chấm cuối cùng), dễ nhầm với object ngoài.
- Nếu method là arrow function thì `this` không phải object sở hữu method (xem bài arrow-function).

## 💡 Khi nào dùng

- Định nghĩa hành vi (behavior) gắn với dữ liệu của một object.
- Viết các đối tượng như user, cart, player... mỗi object tự quản lý dữ liệu của nó.
- Làm nền tảng trước khi học prototype và Class.

## 🎯 Ví dụ minh họa

```js
const iPhone7 = {
  name: "iPhone 7",
  color: "pink",
  take() {
    console.log(this);          // → object iPhone7
    console.log(this.name);     // → iPhone 7
  },
  objChild: {
    name: "child",
    methodChild() {
      console.log(this);        // → objChild (object trực tiếp)
    },
  },
};

iPhone7.take();        // iPhone7  | iPhone 7
iPhone7.objChild.methodChild(); // objChild
```

## 📚 Tham khảo / Bài tập

- Chạy `01_in-method/app.js` qua `index.html`: file tổng hợp nhiều ngữ cảnh của `this` — `button.onclick` (this là button), `this` global, `this` trong hàm thường, và `this` trong function constructor (`new Car`).
- Tự thử: thêm method `getInfo()` in ra `name + color` bằng `this`, sau đó thử đổi một thuộc tính rồi gọi lại.