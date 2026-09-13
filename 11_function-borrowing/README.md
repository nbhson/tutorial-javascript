# Function Borrowing (Mượn hàm) trong JavaScript

## 🔑 Khái niệm

**Function borrowing** là kỹ thuật **dùng chung một hàm** của object/class này cho object khác mà không cần copy hay kế thừa: bạn mượn function và ép cho nó chạy với `this` = object mong muốn.

Công cụ thực hiện là **3 phương thức explicit binding** có sẵn trên mọi hàm:

| Phương thức | Chạy ngay lập tức? | Truyền đối số | Trả về |
|-------------|--------------------|---------------|--------|
| `fn.call(thisArg, a, b, ...)` | ✅ Có | Từng đối số, danh sách | Kết quả của `fn` |
| `fn.apply(thisArg, [a, b, ...])` | ✅ Có | Mảng đối số | Kết quả của `fn` |
| `fn.bind(thisArg, ...)` | ❌ Không | Từng đối số (tùy chọn) | **Hàm mới** đã khóa `this` |

Bản chất: cả ba đều làm đúng một việc — **quyết định `this` là ai**, rồi gọi hàm (hoặc chuẩn bị gọi sau). Khác nhau ở việc gọi ngay hay không và cách nhận đối số.

## ✅ Điểm mạnh

- Tái sử dụng code tối đa: một hàm dùng cho vô số object.
- Kế thừa constructor dễ dàng: `Parent.call(this, ...)` trong child constructor.
- Mượn method built-in: `Array.prototype.forEach.call(arguments, ...)`, `Math.max.apply(null, arr)`.
- `bind` tạo hàm mới tiện cho callback, event handler, partial application.
- Áp dụng được cho cả class lẫn object literal, không cần đổi code nguồn.

## ⚠️ Lưu ý / Hạn chế

- `call` vs `apply` chỉ khác hình thức truyền đối số (danh sách vs mảng) — kết quả giống nhau.
- `bind` **không gọi hàm ngay**; quên gọi hàm mới trả về sẽ không thấy gì.
- `bind` chỉ ràng buộc `this` và đối số, không thay đổi thân hàm hay prototype.
- Arrow function không có `this` nên `call/apply/bind` không đổi được gì.
- Truyền `null`/`undefined` làm `thisArg` thường bị hiểu nhầm; nên dùng đối tượng cụ thể.

## 💡 Khi nào dùng

- Mượn `Array.prototype` method cho `arguments`, `NodeList`, object giống mảng.
- Gọi hàm cha (super) trong function-constructor khi chưa có `class`.
- Khóa `this` cho callback/event handler bằng `bind`.
- Truyền `Math.max.apply(null, arr)` để tìm max của mảng.
- Viết polyfill, mixin, utility dùng chung giữa nhiều đối tượng.

## 🎯 Ví dụ minh họa

```js
const teacher = {
  firstName: "Minh",
  lastName: "Thao",
  getFullName() {
    return `${this.firstName} ${this.lastName}`;
  },
};

const student = { firstName: "Dang", lastName: "Son" };

console.log(teacher.getFullName());                 // Minh Thao
console.log(teacher.getFullName.call(student));     // Dang Son (mượn)
console.log(teacher.getFullName.apply(student));    // Dang Son (mượn)
const bound = teacher.getFullName.bind(student);
console.log(bound());                               // Dang Son (hàm mới)
```

## 📚 Tham khảo / Bài tập

- Nhóm này gồm: `01_bind`, `02_bind-advanced`, `03_call`, `04_apply`, `05_polyfill` — đọc theo thứ tự.
- Mỗi folder có `app.js` + `index.html`; chạy và quan sát console.
- Tự thử: mượn `getFullName` cho object `{ firstName: "A", lastName: "B" }` bằng cả 3 cách và so sánh kết quả.