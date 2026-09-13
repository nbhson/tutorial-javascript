# Arrow function — lexical `this`

## 🔑 Khái niệm

"Lexical this" nghĩa là `this` của arrow function được xác định bởi **cấu trúc code (scope lồng nhau)** tại nơi khai báo, không phải cách gọi. Khi inside một arrow function, `this` chính là `this` của hàm/scope bao bọc nó tại thời điểm **khai báo**:

```js
const outer = {
  x: 42,
  make() {
    const fn = () => console.log(this.x); // this = outer (kế thừa từ make())
    fn();
  },
};
```

Vì `fn` được khai báo bên trong method `make()` (đang có `this = outer`), nên kể cả khi `fn` được gọi trần hay trễ đi qua `setTimeout`, `this` bên trong vẫn là `outer`.

## ✅ Điểm mạnh

- Giữ `this` ổn định trong callback bất đồng bộ: `setTimeout(() => this.x, 0)` vẫn đúng object ban đầu.
- Không cần `const that = this` hay `.bind(this)` — code sạch hơn nhiều.
- Nhất quán cho mọi trường hợp: lồng càng sâu, `this` càng rõ ràng theo từng cấp.
- Dễ suy luận: nhìn vào nơi khai báo là biết `this`.

## ⚠️ Lưu ý / Hạn chế

- `this` bị "chốt" từ scope khai báo — nếu scope đó là global thì `this` là global, không đổi được.
- Không thể dùng arrow để "đổi chủ" `this` như hàm thường bằng `call/apply/bind`.
- Khi cần `this` động (ví dụ event handler lấy element), arrow không phù hợp.
- Dễ nhầm nếu khai báo arrow trong nhiều cấp function — cần xác định đúng cấp chứa `this` mong muốn.

## 💡 Khi nào dùng

- Dùng `this` của object bên trong `setTimeout`/`setInterval`/`fetch`/`.then()`.
- Truyền method nội bộ của object/class làm callback.
- Playwright của hầu hết các hàm gọi callback theo kiểu method (map, forEach).

## 🎯 Ví dụ minh họa

```js
const outer = {
  x: 42,
  make() {
    const fn = () => console.log(this.x);
    fn(); // → 42 (lexical this = outer)
  },
};
outer.make();

const o = {
  x: 1,
  hi() {
    setTimeout(() => {
      console.log(this.x); // → 1 (dù chạy trễ, vẫn giữ this của hi())
    }, 0);
  },
};
o.hi();
```

## 📚 Tham khảo / Bài tập

- Chạy `06_arrow-lexical/app.js` (qua `index.html` hoặc `node app.js`): xem `outer.make()` in `42` và `o.hi()` sau `setTimeout` vẫn in `1`.
- Tự thử: đổi arrow `fn` thành hàm thường `function () {}` trong cùng chỗ — output sẽ khác (mất context), giải thích tại sao.