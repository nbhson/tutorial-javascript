# let và const

## 🔑 Khái niệm

`let` và `const` là hai từ khóa khai báo biến hiện đại (có từ **ES6**), thay thế cho `var` đầy rắc rối của JavaScript cũ. Cả hai có **block scope** (`{}`, `if`, `for`...) và **không thể khai báo lại** trong cùng một phạm vi. Điểm khác nhau duy nhất: `let` cho phép **gán lại giá trị**, còn `const` **không** (khóa tham chiếu).

```js
{
  let course = "JS Basic";
  {
    let course = "JS enhancement"; // biến trùng tên trong block lồng nhau là hợp lệ
    console.log(course);           // "JS enhancement" — truy cập thằng gần nhất
  }
}
console.log(course); // ReferenceError — course không tồn tại ngoài block
```

**Vì sao phải phân biệt `let` và `const`?** Vì nó ghi lại **ý định của lập trình viên**: `const` nói "tham chiếu này là cố định, không được trỏ sang nơi khác" — trình biên dịch sẽ chặn bạn nếu vô tình gán lại:

```js
const b = { name: "JS" };
b.name = "PHP";  // OK — sửa thuộc tính bên trong object
b.age = 89;      // OK — thêm thuộc tính mới
// b = {};       // TypeError: Assignment to constant variable
```

Nguyên nhân: `const` chỉ khóa **tham chiếu (reference)** của biến trỏ đến object, không "đóng băng" object đó. Đây chính là sự khác biệt giữa **tham trị** (primitive) và **tham chiếu** (object) — sẽ học kỹ ở `02_data-types/01_primitive-types/03_value-vs-reference`.

## ✅ Điểm mạnh

- **Block scope**: biến chỉ tồn tại trong khối `{}`, không "rò rỉ" ra ngoài như `var`.
- **Không khai báo trùng**: bắt lỗi sớm khi vô tình viết trùng tên.
- `const` truyền tải ý định rõ ràng: "đừng gán lại cho biến này".
- Code an toàn hơn, dễ đoán hành vi hơn `var` (không hoisting kiểu gây `undefined` bất ngờ).
- Trong block lồng nhau, vẫn tạo được biến trùng tên (shadowing) dùng riêng cho block trong.

## ⚠️ Lưu ý / Hạn chế

- `const` **không** làm object bất biến — vẫn đổi sửa được thuộc tính bên trong.
- Truy cập `let`/`const` trước khi khai báo → `ReferenceError` (temporal dead zone, học ở bài `02_hoisting`).
- Không dùng khai báo lại `let x` trong cùng một scope → `SyntaxError`.
- `const` buộc phải khởi tạo ngay khi khai báo: `const x;` sẽ báo lỗi cú pháp.

## 💡 Khi nào dùng

- Mặc định dùng **`const`** cho mọi biến, vì ràng buộc chặt chẽ nhất.
- Chỉ chuyển sang **`let`** khi chắc chắn biến cần gán lại (bộ đếm, biến lặp `for`).
- `var` còn dùng trong các đoạn script rất cũ, hoặc khi mô phỏng hành vi code cũ.

## 🎯 Ví dụ minh họa

```js
// const dùng trỏ tới các phần tử DOM cố định
const button = document.getElementById("btn");

// let dùng cho biến thay đổi
let count = 0;
button.onclick = () => (count += 1);

// const + object: đổi thuộc tính được, gán lại biến thì không
const user = { name: "Sơn" };
user.name = "Nam";
console.log(user.name); // Nam

// block scope trong if/loop
if (true) {
  let x = 5;   // chỉ tồn tại trong if
  var y = 10;  // var thoát ra ngoài if!
}
console.log(y); // 10
// console.log(x); // ReferenceError: x is not defined
```

## 📚 Tham khảo / Bài tập

- Chạy `app.js` trong thư mục này (mở `index.html` trong trình duyệt rồi xem Console, hoặc `node app.js`): nó demo **scope** (block lồng nhau, truy cập thằng gần nhất), **hoisting** của `var` (`console.log(a)` in `undefined`), và **assignment** với `const` object (`b.name = "PHP"`).
- Tự thử: trong `app.js`, 1) đổi `var a = 1` thành `let a = 1` và quan sát lỗi `ReferenceError`; 2) gán `b = 1` và đọc `TypeError`; 3) thử `const c;` và đọc lỗi cú pháp.
- Tài liệu: [MDN — let](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/let), [MDN — const](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/const).