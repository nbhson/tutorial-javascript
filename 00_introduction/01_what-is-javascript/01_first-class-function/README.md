# First-class Function (Hàm hạng nhất)

## 🔑 Khái niệm

Một ngôn ngữ được gọi là có **first-class function** khi các hàm trong ngôn ngữ đó được xử lý như **bất kỳ giá trị nào khác** — tức hàm cũng "bình đẳng" với số, chuỗi, boolean. Cụ thể, trong một ngôn ngữ như vậy bạn có thể:

1. **Gán hàm cho một biến.**

```js
const foo = () => {
  console.log("foobar");
};
foo(); // foobar
```

Ở đây ta gán một *anonymous function* (hàm không tên) vào biến `foo`, sau đó dùng biến đó kèm cặp `()` để gọi hàm.

2. **Truyền hàm như một đối số** cho một hàm khác (chính là nền tảng của callback).

```js
function sayHello() {
  return "Hello, ";
}
function greeting(helloMessage, name) {
  console.log(helloMessage() + name);
}
// Truyền sayHello như một "giá trị" cho greeting
greeting(sayHello, "JavaScript!"); // Hello, JavaScript!
```

Lưu ý khi truyền ta viết `sayHello` **không có dấu ngoặc** — đây là lúc ta đang truyền *bản thân hàm* chứ không phải kết quả chạy của nó.

3. **Trả về một hàm từ một hàm khác** (nền tảng của higher-order function, closure).

```js
function sayHello() {
  return () => {
    console.log("Hello!");
  };
}
const hello = sayHello();
hello(); // Hello!
```

Nhờ đặc tính này, JavaScript hỗ trợ tốt lập trình **functional**: các hàm như `map`, `filter`, `reduce`, `setTimeout`, và thư viện như Redux hay các HOC trong React đều xoay quanh first-class function.

## ✅ Điểm mạnh

- **Callback & asynchronous**: dễ dàng truyền hàm xử lý sau khi có kết quả (`setTimeout`, `fetch`, promise).
- **Higher-order functions**: viết hàm nhận/trả hàm để tái sử dụng logic (`map`, `filter`, `reduce`).
- **Closure**: hàm trả hàm giúp "nhớ" biến của phạm vi bên ngoài, tạo được các mô hình như factory, private state.
- **Composition**: ghép nhiều hàm nhỏ thành quy trình phức tạp, code dễ đọc và kiểm thử.
- **Event handlers**: gắn hàm vào sự kiện DOM một cách tự nhiên.

## ⚠️ Lưu ý / Hạn chế

- Khi **truyền hàm làm đối số**, phải truyền *tên hàm không có `()`*. Viết `greeting(sayHello(), ...)` là truyền *kết quả* chứ không phải hàm.
- Hàm trả về từ hàm khác dễ gây **rò rỉ bộ nhớ** nếu giữ tham chiếu tới các biến không cần thiết (closure giữ biến lâu hơn dự kiến).
- Lạm dụng callback lồng nhau sẽ sinh "callback hell" — hãy dùng Promise / async-await khi cần.
- Nắm chắc sự khác nhau giữa *gọi hàm ngay* (`foo()`) và *tham chiếu hàm* (`foo`).

## 💡 Khi nào dùng

- Viết xử lý bất đồng bộ: `setTimeout(() => {...}, 1000)`, quản lý sự kiện.
- Xử lý mảng theo phong cách functional: `arr.map(...)`, `arr.filter(...)`, `arr.reduce(...)`.
- Tạo hàm "nhà máy" sinh ra các hàm theo cấu hình (`function makeMultiplier(x)`).
- Viết middleware / HOC (truyền hàm vào hàm để mở rộng hành vi).

## 🎯 Ví dụ minh họa

```js
// Gán hàm cho biến
const binhPhuong = (n) => n * n;

// Truyền hàm làm đối số (callback)
function apDung(fn, giaTri) {
  return fn(giaTri);
}
console.log(apDung(binhPhuong, 5)); // 25

// Trả về hàm từ hàm (closure)
function taoBoNhan(x) {
  return (y) => x + y;
}
const congMot = taoBoNhan(1);
console.log(congMot(10)); // 11

// Thực tế: map nhận một hàm
const so = [1, 2, 3];
console.log(so.map((n) => n * 10)); // [10, 20, 30]
```

## 📚 Tham khảo / Bài tập

- Nhóm này **chưa có file `app.js`** — bạn hãy tạo file `.js` bất kỳ hoặc mở DevTools (F12 → Console) để chạy trực tiếp các ví dụ trên.
- Tự thử: viết hàm `taoPhanTram(mau)` trả về một hàm cho biết chuỗi ký tự có nằm trong `mau` không; dùng nó với `some`/`filter` để lọc danh sách.
- Tài liệu: [MDN — Glossary: First-class Function](https://developer.mozilla.org/en-US/docs/Glossary/First-class_Function).