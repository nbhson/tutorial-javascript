# Arrow function không có `this`

## 🔑 Khái niệm

Arrow function (`() => {}`) **không có `this` riêng của nó**. Thay vì tạo `this` mới theo cách được gọi (call-site), nó **mượn lexical this** — tức `this` từ phạm vi bao bọc ngay bên ngoài nơi nó được khai báo.

Hệ quả quan trọng:

- Gọi `arrow.call(obj)` / `arrow.apply(obj)` / `arrow.bind(obj)` đều **không đổi** được `this`.
- Gọi `arrow()` như method của object (`obj.arrow()`) `this` vẫn không phải `obj`.
- `this` bên trong arrow được "chốt" ngay lúc khai báo, dựa vào scope LEXICAL chứ không phải lúc gọi.

## ✅ Điểm mạnh

- Tránh bẫy "mất context" khi truyền method làm callback (setTimeout, addEventListener, array methods).
- Không cần mẹo `const that = this` hay `bind` như thời trước arrow function.
- Giữ `this` ổn định xuyên suốt các hàm lồng nhau — dễ đọc, dễ đoán.
- Cú pháp ngắn gọn, không cần quan tâm call-site.

## ⚠️ Lưu ý / Hạn chế

- `call`/`apply`/`bind` trở nên **vô dụng** với arrow function — đừng dùng chúng để ép `this`.
- Dùng arrow làm event handler sẽ **không lấy được element** qua `this` (phải dùng `event.target`).
- Arrow function cũng không có `arguments` riêng và không phù hợp làm phương thức cần `this` động.
- Nếu scope bên ngoài là global, `this` của arrow chính là global/undefined (strict).

## 💡 Khi nào dùng

- Callback bất đồng bộ (setTimeout, fetch, promise) cần giữ `this` của context bao quanh.
- Truyền hàm vào `forEach`, `map`, `filter`... bên trong method của object.
- Viết hàm tiện ích ngắn không phụ thuộc call-site.

## 🎯 Ví dụ minh họa

```js
const o = { name: "object" };

const arrow = () => console.log(this);
arrow.call(o);   // → global (this KHÔNG đổi thành o)
arrow();         // → global

// method là arrow → this không phải object chứa nó
const arrowObj = { name: "arrow", hi: () => console.log(this) };
arrowObj.hi();   // → global (không phải arrowObj)
```

## 📚 Tham khảo / Bài tập

- Chạy `05_arrow-function/app.js` (qua `index.html` hoặc `node app.js`): xem `cb.call(el)` khiến hàm thường nhận `this = el`, còn arrow (`arrowBtn.handle`) thì không.
- Tự thử: đổi `arrowBtn.handle` thành hàm thường rồi gọi bằng `call(arrowBtn)` — so sánh kết quả `this`.