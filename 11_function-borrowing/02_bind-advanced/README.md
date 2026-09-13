# Function Borrowing — `bind` nâng cao

## 🔑 Khái niệm

Khi đã nắm `bind` cơ bản, ta khai thác hai sức mạnh lớn:

1. **Bind cho phương thức của object khác** — phổ biến nhất là `document.querySelector.bind(document)`: gán `$` như một shortcut sạch, và giữ đúng `this` là `document`.
2. **Partial application / currying** — chốt trước vài đối số vào thời điểm `bind`, phần còn lại truyền khi gọi. Kết hợp chốt cả `this` lẫn đối số trong một lần.

Trong ứng dụng thực tế, `bind` còn dùng để tổ chức event delegation: một listener duy nhất trên container, `this` chính xác là object quản lý (app).

## ✅ Điểm mạnh

- Tạo shortcut an toàn: `const $ = document.querySelector.bind(document)` ngắn gọn và không bị mất context khi dùng ở nơi khác.
- Currying tự nhiên: hàm chuyên biệt từ hàm tổng quát (đóng sẵn greeting, suffix...).
- Phối hợp với event delegation giúp code tổ chức rõ ràng, ít listener thừa.
- Không phải dùng biến phụ `that`/`self` khi viết callback.

## ⚠️ Lưu ý / Hạn chế

- Nếu `bind(null)` hoặc quên bind, `this` bên trong `querySelector` rơi về global → lỗi runtime.
- Delegate + bind dễ nhầm: `root.onclick = this.handleDelete.bind(this)` — nếu không bind, `this` bên trong handler lại là `root` element (vì event binding).
- Currying làm hàm khó đọc nếu chốt quá nhiều đối số một lúc.
- Không thể bind lại nếu đã bind.

## 💡 Khi nào dùng

- Tạo alias cho DOM API: `const $ = document.querySelector.bind(document)`, `const $$ = document.querySelectorAll.bind(document)`.
- Gắn method của object vào event: `root.onclick = app.handleDelete.bind(app)`.
- Currying: hàm `greet(greeting, name)` → `sayHello = greet.bind({ suffix: "!" }, "Hello ")`.
- Viết library/framework kiểu module IIFE cần giữ context nội bộ.

## 🎯 Ví dụ minh họa

```js
const $ = document.querySelector.bind(document);   // an toàn, luôn giữ document
const $$ = document.querySelectorAll.bind(document);

function greet(greeting, name) {
  console.log(greeting + name + this.suffix);
}
const b = greet.bind({ suffix: "!" }, "Hello ");
b("An"); // Hello An!  (this = {suffix:"!"}, đối số đầu đã chốt)

// event delegation dùng bind giữ context của object app
const app = {
  cars: ["BMW"],
  handleDelete(e) {
    const btn = e.target.closest(".delete");
    if (btn) this.delete(btn.dataset.index);
    this.render();
  },
  delete(i) { this.cars.splice(i, 1); },
  render() { $("#root").innerHTML = this.cars.join(", "); },
  init() { $("#root").onclick = app.handleDelete.bind(app); },
};
app.init();
```

## 📚 Tham khảo / Bài tập

- Chạy `02_bind-advanced/app.js` qua `index.html`: thử bật/bỏ dòng `const $ = document.querySelector.bind(document)` — đổi lại `document.querySelector` trực tiếp để thấy lỗi mất context.
- App demo sử dụng `this.handleDelete.bind(this)` — tự thêm khả năng thêm xe (input) để hiểu rõ luồng `bind` + delegation.