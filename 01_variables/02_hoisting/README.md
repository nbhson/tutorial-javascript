# Hoisting

## 🔑 Khái niệm

**Hoisting** (nâng lên) là hành vi của JavaScript engine: khi phân tích một phạm vi, nó "kéo" (hoist) các **khai báo** — biến `var`, `let`, `const` và **function declaration** — lên **đầu phạm vi** trước khi thực thi. Tuy nhiên, cách "kéo" của từng loại rất khác nhau:

**1. Hoisting với `var`** — khai báo được kéo lên, nhưng **không kéo giá trị khởi tạo**. Vì vậy biến tồn tại với giá trị mặc định `undefined` từ đầu:

```js
console.log(age); // undefined — khai báo `var age` đã được hoist lên trên
var age = 16;
```

**2. Hoisting với `let`/`const`** — khai báo cũng được hoist, **nhưng không** được gán mặc định `undefined` như `var`. Từ đầu phạm vi cho đến dòng khai báo là vùng **Temporal Dead Zone (TDZ)** — truy cập tại đây sẽ ném `ReferenceError`:

```js
console.log(fullName);
// ReferenceError: Cannot access 'fullName' before initialization
let fullName = "Sơn Nguyễn";
```

TDZ là "vùng chết tạm thời": biến *đã tồn tại* trong phạm vi nhưng chưa thể dùng. Nhờ vậy, `let`/`const` giúp tránh lỗi logic khi vô tình dùng biến trước khi khai báo — đúng như ví dụ trong `app.js`: một `let x` trong block bên trong **ngăn** việc vô tình truy cập `x` của block bên ngoài (shadowing + TDZ).

**3. Hoisting với function declaration** — hàm được khai báo bằng từ khóa `function` được kéo lên **hoàn chỉnh** (cả phần thân), nên gọi trước khi định nghĩa vẫn chạy được:

```js
console.log(sum(6, 9)); // 15
function sum(a, b) {
  return a + b;
}
```

**4. Hoisting bên trong closure** — function declaration nằm trong thân hàm khác (closure) vẫn được hoist trong phạm vi của hàm đó, nên gọi *ngược* cũng OK:

```js
function makeCounter() {
  let counter = 0;
  return increase; // trả về tham chiếu dù increase định nghĩa phía dưới
  function increase() {
    return ++counter;
  }
}
const c = makeCounter();
console.log(c()); // 1
console.log(c()); // 2
```

> Lưu ý: hoisting chỉ áp dụng cho khai báo **`function sum() {}`**, không áp dụng cho **arrow function** `const sum = () => {}` — arrow là biến, nên rơi vào TDZ như `let`/`const`.

## ✅ Điểm mạnh

- Function declaration có thể gọi trước khi định nghĩa → code có thể sắp xếp "ý nghĩa" trước, chi tiết sau.
- TDZ của `let`/`const` bắt lỗi "dùng biến trước khi khai báo" ngay khi chạy.
- Hiểu hoisting → đọc được những đoạn code cũ viết bằng `var` mà không bị lừa.
- Closures mô tả quan hệ hàm-lồng-hàm tự nhiên nhờ hoisting của function declaration.

## ⚠️ Lưu ý / Hạn chế

- `var` bị hoist thành `undefined` → kiểm tra `console.log(age)` in `undefined` **không báo lỗi**, rất dễ gây nhầm lẫn (lỗi logic).
- `let`/`const` bị hoist nhưng nằm trong TDZ → nếu bạn nghĩ "hoisting = dùng trước được" là sai với chúng.
- Arrow function / function expression **không** được hoist → gọi trước sẽ `ReferenceError`.
- Đừng chủ ý dựa vào hoisting của `var` để viết code; hãy khai báo trước khi dùng.

## 💡 Khi nào dùng

- Tổ chức file có mục: hàm "tiện ích" đặt dưới, logic chính gọi ở trên (function declaration).
- Debug lỗi `Cannot access 'fullName' before initialization` → nhận ra dấu hiệu TDZ.
- Nhận diện code cũ: thấy `console.log(x)` in `undefined` mà không lỗi → xem có phải `var`.

## 🎯 Ví dụ minh họa

```js
// var: hoisted về undefined
console.log(str); // undefined
var str = "Hoisting";

// let: TDZ → ReferenceError
// console.log(x); // ReferenceError
let x = 10;

// Function declaration: hoist trọn vẹn
console.log(gapDoi(4)); // 8
function gapDoi(n) {
  return n * 2;
}

// Function expression (arrow): KHÔNG hoist
// console.log(gapBa(4)); // ReferenceError
const gapBa = (n) => n * 3;
```

## 📚 Tham khảo / Bài tập

- Chạy `app.js` trong thư mục (mở `index.html` → Console, hoặc `node app.js`): dòng `console.log(x)` trong block `let x = "xxx"` chứng minh rằng **khai báo `let x` bên trong block vẫn được hoist**, nên không tìm ra ngoài, gây `ReferenceError`; còn `console.log(y)` trước `const y = 10` cũng báo lỗi TDZ. Tắt `index.html` mở bằng trình duyệt rồi xem từng dòng lỗi đỏ.
- Tự thử: 1) chép nhóm dòng `console.log(gapDoi(4))`/`function gapDoi` đổi thành arrow và đọc lỗi; 2) viết ví dụ riêng dùng `function` gọi trước định nghĩa và xác nhận nó chạy được.
- Tài liệu: [MDN — Hoisting](https://developer.mozilla.org/en-US/docs/Glossary/Hoisting), [javascript.info/var](https://javascript.info/var).