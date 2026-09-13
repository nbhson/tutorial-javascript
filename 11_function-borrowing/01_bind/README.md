# Phương thức `bind()`

## 🔑 Khái niệm

`fn.bind(thisArg, arg1, arg2, ...)` trả về một **hàm mới** với `this` được khóa lại thành `thisArg` (và các đối số đầu có thể được truyền trước). **`bind` không gọi hàm ngay** — bạn phải tự gọi hàm mới trả về:

```js
const newFn = fn.bind(thisArg, arg1, arg2, ...);
newFn(arg1, arg2);
```

Điểm then chốt:

- Hàm mới có **vùng nhớ riêng** (không bằng hàm gốc).
- `this` của hàm mới là `thisArg`, bất kể sau đó gọi theo kiểu gì.
- Các đối số truyền vào lúc `bind` được **ưu tiên hơn** khi gọi (partial application).
- `bind` ràng buộc **method** chứ không bind được thuộc tính.

## ✅ Điểm mạnh

- Tạo hàm "đóng gói sẵn" `this` dùng cho callback, event handler mà không sợ mất context.
- Partial application: chốt trước một phần đối số, gọi sau với phần còn lại.
- Mượn method của object này cho object khác mà vẫn giữ vùng nhớ riêng.
- Kết hợp dùng chung một method cho hàng loạt object.

## ⚠️ Lưu ý / Hạn chế

- `bind` **không gọi hàm** — quên `()` phần trước là bug kinh điển.
- Chỉ "chốt" `this`/đối số **tại thời điểm bind**; sau đó không gỡ ra được.
- Hàm được bind không thể đổi `this` lại bằng `call`/`apply`.
- Không bind được thuộc tính (property), chỉ bind được phương thức/hàm.

## 💡 Khi nào dùng

- Gán method làm callback: `submit.onclick = obj.handle.bind(obj)`.
- Chốt context cho list handlers: `document.querySelector.bind(document)`.
- Tạo hàm chuyên biệt từ hàm tổng quát (prefix greeting, formatter...).

## 🎯 Ví dụ minh họa

```js
const student = { firstName: "Dang", lastName: "Son" };

function getFullName(age) {
  return `${this.firstName} ${this.lastName} - ${age}`;
}

// bind this = student, đồng thời chốt sẵn đối số age = 18
const getName = getFullName.bind(student, 18);
console.log(getName()); // Dang Son - 18

console.log(getName === getFullName); // false — hàm mới, vùng nhớ khác
```

## 📚 Tham khảo / Bài tập

- Chạy `01_bind/app.js` (qua `index.html`): xem `sonNguyen.getFullName.bind(trinhHuynh, 18)` in ra `Trinh Huynh - 18` — mượn method `getFullName` của Person cho Student.
- Tự thử: bỏ đối số `18` ra khỏi `bind` rồi gọi `trinhHuynhFullName(20)` — quan sát `age` được lấy từ đâu.