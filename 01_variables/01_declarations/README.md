# Khai báo biến (Declarations)

## 🔑 Khái niệm

**Khai báo biến (declaration)** là tạo ra một biến; **khởi tạo (initialization)** là gán giá trị đầu tiên cho nó; **gán (assignment)** là đổi giá trị sau đó. JavaScript có **3 từ khóa** khai báo: `var`, `let`, `const`.

```js
let myName;                        // khai báo → giá trị mặc định: undefined
myName = "Chris";                  // khởi tạo (gán giá trị lần đầu)
myName = "Bob";                    // gán lại (assignment)
```

**Điểm khác biệt cốt lõi:**

| | `var` | `let` | `const` |
|---|---|---|---|
| Scope | hàm | block `{}` | block `{}` |
| Khai báo lại | được | không | không |
| Gán lại | được | được | **không** |
| Hoisting | khai báo được kéo lên, giá trị `undefined` | có TDZ → lỗi nếu dùng trước | có TDZ → lỗi nếu dùng trước |
| Phải khởi tạo ngay | không | không | **bắt buộc** |

**Dynamic typing:** JS là ngôn ngữ kiểu động — biến không khai báo kiểu, và có thể đổi kiểu trong lúc chạy:

```js
let myNumber = "500";   // string
typeof myNumber;        // "string"
myNumber = 500;         // number
typeof myNumber;        // "number"
```

**Gán cho biến chưa khai báo:** nếu không có `"use strict"`, `num = 5` tự tạo một biến global (việc xấu). Trong strict mode, dòng đó báo lỗi:

```js
"use strict";
num = 5; // ReferenceError: num is not defined
```

**const với object/array:** `const` khóa tham chiếu của biến, **không** đóng băng nội dung — vẫn đổi được thuộc tính/phần tử:

```js
const bird = { species: "Kestrel" };
bird.species = "Striated Caracara"; // OK
// bird = {}; // TypeError: Assignment to constant variable
```

**Kiểm tra biến có tồn tại:** dùng `typeof` (trả về `"undefined"` cho cả biến chưa khai báo lẫn biến chưa gán giá trị):

```js
var x = 10;
typeof x !== "undefined"; // true
typeof z !== "undefined"; // false
```

## ✅ Điểm mạnh

- `let`/`const` an toàn hơn `var` nhờ block scope và chống khai báo trùng.
- `const` biểu đạt ý định "đây là tham chiếu không đổi", giúp code dễ đọc hơn.
- Dynamic typing cho phép viết code linh hoạt, không phải viết nhiều boilerplate.
- `typeof` giúp kiểm tra biến tồn tại an toàn trước khi dùng.
- 3 từ khóa nhỏ gọn, phù hợp cả script ngắn lẫn dự án lớn (kết hợp TypeScript khi cần).

## ⚠️ Lưu ý / Hạn chế

- `var` nhảy ra khỏi block `{}` → hay gây bug không ngờ (dùng `let` thay thế).
- Truy cập `let`/`const` trước khi khai báo → `ReferenceError` (TDZ).
- `const` với object/array không "bất biến" như bạn tưởng — nội dung vẫn đổi được.
- Dynamic typing dễ gây lỗi ngầm (cộng số với chuỗi...); cần hiểu ép kiểu ở nhóm `02_data-types`.

## 💡 Khi nào dùng

- Giá trị không đổi tham chiếu (config, DOM element, kết quả tính toán) → `const`.
- Biến cần gán lại (bộ đếm, biến lặp, trạng thái thay đổi) → `let`.
- Không bao giờ dùng `var` trong code mới (trừ khi phải hỗ trợ trình duyệt rất cũ).
- Kiểm tra biến ngoài ý muốn tồn tại hay không → `typeof`.

## 🎯 Ví dụ minh họa

```js
// var: khai báo lại được, có function scope
var x = 10;
var x = 20;         // không lỗi
console.log(x);     // 20

// let: không khai báo lại được
let y = 10;
// let y = 20;      // SyntaxError: Identifier 'y' has already been declared

// const: phải khởi tạo ngay, không gán lại tham chiếu
const a = 11;
// a = 12;          // TypeError

// object literal + const
let dog = { name: "Spot", breed: "Dalmatian" };
console.log(dog.name); // "Spot"
dog.name = "Rex";
console.log(dog.name); // "Rex"
```

## 📚 Tham khảo / Bài tập

- Hãy chạy `app.js` trong thư mục (ví dụ: `node app.js`; nó minh họa `number` đổi kiểu string→number→string và `var` nhảy ra khỏi `if`) hoặc mở `Screenshot 2025-07-28 at 07.29.44.png` để xem lại hình minh họa "biến là container".
- Chuyển sang bài con `01_let-and-const/` (có `app.js` demo trực quan `var`/`let`, hoisting, gán lại với `const`).
- Tự thử: trong file `app.js`, thay `var y = 10` thành `let y = 10` rồi chạy và đọc thông báo lỗi; thử gán `number = { a: 1 }` xem kiểu thay đổi thế nào.
- Tài liệu: [javascript.info/variables](https://javascript.info/variables), [javascript.info/var](https://javascript.info/var).