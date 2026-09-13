# Từ khóa `this` trong JavaScript

## 🔑 Khái niệm

`this` là một từ khóa đặc biệt trong JavaScript, trỏ đến đối tượng mà hàm đang được gọi. Điểm quan trọng: **giá trị của `this` không cố định** — nó phụ thuộc vào **cách hàm được gọi** (call-site), không phải nơi hàm được khai báo (trừ arrow function).

JavaScript có **4 quy tắc binding** cho `this`:

| Quy tắc | Khi nào | `this` là gì |
|--------|---------|-------------|
| **Default binding** | Gọi hàm trần `fn()` | `window`/`globalThis` (non-strict) hoặc `undefined` (strict mode) |
| **Implicit binding** | Gọi như method `obj.fn()` | chính là `obj` |
| **Explicit binding** | Dùng `call`/`apply`/`bind` | đối tượng bạn truyền vào |
| **New binding** | `new Fn()` | object mới được tạo bởi constructor |

Thứ tự ưu tiên: **new > explicit (call/apply/bind) > implicit > default**. Arrow function là ngoại lệ: nó **không có `this` riêng** mà kế thừa `this` từ phạm vi bao bọc (lexical this).

## ✅ Điểm mạnh

- Tái sử dụng một method cho nhiều đối tượng khác nhau (nhờ implicit/explicit binding).
- Linh hoạt: cùng một hàm, gọi khác cách thì `this` khác nhau, giúp viết code gọn và động.
- Kết hợp `call`/`apply`/`bind` để mượn hàm (function borrowing) và kế thừa constructor.
- Class, object method, event handler đều dựa trên cơ chế `this` để truy cập dữ liệu của chính chúng.
- `new` giúp tạo instance riêng biệt, mỗi instance có dữ liệu của riêng nó.
- Arrow function giữ `this` ổn định khi lồng trong callback (setTimeout, listener...).

## ⚠️ Lưu ý / Hạn chế

- `this` rất dễ nhầm: chỉ vì hàm được khai báo trong object chưa chắc `this` là object đó — phụ thuộc cách *gọi*.
- Tách method ra khỏi object (gán `const fn = obj.method`) thì mất context: `this` rơi về default binding.
- Trong strict mode, default binding trả về `undefined` thay vì `window`.
- Arrow function **không thể** dùng `bind`/`call`/`apply` để đổi `this`.
- `this` trong event handler là element nhận sự kiện, không phải object bạn định nghĩa handler.

## 💡 Khi nào dùng

- Truy cập thuộc tính/phương thức của object bên trong method của chính object đó.
- Viết event handler: `this` trỏ tới element kích hoạt sự kiện.
- Dùng Constructor/Class để tạo nhiều instance dữ liệu riêng biệt.
- Mượn hàm từ object/Array khác thông qua `call`/`apply`/`bind`.
- Giữ `this` của scope ngoài trong callback bất đồng bộ bằng arrow function.

## 🎯 Ví dụ minh họa

```js
// this phụ thuộc cách gọi
const obj = {
  name: "A",
  hi() {
    console.log("this:", this);       // obj
    console.log("traversal", this.name); // A
  },
};
obj.hi();             // implicit → this = obj

const detached = obj.hi;
detached();           // default binding → this = window/undefined (strict)

// new binding
function Car(name) {
  this.name = name;   // this = object mới
}
const porsche = new Car("Porsche");
console.log(porsche.name); // Porsche
```

## 📚 Tham khảo / Bài tập

- Nhóm này gồm 6 chủ đề: `01_in-method`, `02_in-function`, `03_alone`, `04_event-handler`, `05_arrow-function`, `06_arrow-lexical` — mở từng folder theo thứ tự.
- Mỗi folder có `app.js` + `index.html`; chạy `index.html` trong trình duyệt và mở DevTools Console để xem kết quả.
- Tự thử: viết 1 object có method, tách method ra biến rồi gọi, đoán `this` trước khi xem output.