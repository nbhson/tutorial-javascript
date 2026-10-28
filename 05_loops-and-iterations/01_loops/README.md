# Vòng Lặp (Loops) — Thực hành chi tiết — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

Thư mục này chứa **7 file thực hành** các loại vòng lặp cơ bản nhất trong JavaScript, được sắp xếp theo thứ tự độ phức tạp tăng dần. Mỗi file `.js` minh họa một khái niệm riêng biệt, chạy độc lập được bằng `node <tên-file>.js`.

JavaScript có 5 loại vòng lặp chính, và thư mục này cover đầy đủ:

| File | Loại vòng lặp | Đặc điểm then chốt |
|---|---|---|
| `1_for.js` | `for` | Đếm từ 0 đến N, kiểm tra điều kiện trước mỗi lần lặp |
| `2_for-in.js` | `for...in` | Duyệt **key** của object / index của mảng / vị trí ký tự của string |
| `3_for-of.js` | `for...of` | Duyệt **value** của iterable (array, string, Set, Map...) |
| `4_while.js` | `while` | Kiểm tra điều kiện **trước** khi chạy thân — có thể không chạy lần nào |
| `5_do-while.js` | `do...while` | Chạy thân **trước**, rồi kiểm tra — luôn chạy ít nhất 1 lần |
| `6_break-continue.js` | `break` / `continue` | Điều khiển luồng: thoát sớm hoặc bỏ qua iter hiện tại |
| `7_lap-long-nhau.js` | Nested loop | Vòng lặp trong vòng lặp — duyệt cấu trúc 2 chiều |

**Khác biệt cốt lõi giữa `while` và `do...while`**: nếu điều kiện sai từ đầu (`i < 0` với `i = 5`), `while` không chạy lần nào, còn `do...while` vẫn chạy đúng 1 lần rồi mới kiểm tra. Đây là khác biệt quan trọng nhất trong việc chọn loại vòng lặp.

**Khác biệt then chốt giữa `for...in` và `for...of`**:
- `for...in`: trả về **key** (dạng chuỗi `"0"`, `"name"`...) — phù hợp object, không phải array thuần.
- `for...of`: trả về **value** thực tế (`"HTML"`, `1`, ký tự...) — phù hợp array, string, và mọi iterable.

## 📐 Cấu trúc / Cú pháp

### `1_for.js` — For kinh điển
```js
for (let i = 0; i < 5; i++) {
  console.log(i); // 0 1 2 3 4
}
```
- Ba phần trong `()` cách nhau bởi `;`: **khởi tạo**, **điều kiện**, **bước nhảy**.
- Ba phần đều **tùy chọn** — `for (;;) {}` là vòng lặp vô hạn (cần `break` bên trong).

### `2_for-in.js` — Duyệt key
```js
const myInfo = { name: "Sơn Nguyễn", age: 18 };
for (const key in myInfo) {
  console.log(key, myInfo[key]); // name Sơn Nguyễn / age 18
}

const langs = ["HTML", "CSS", "JS"];
for (const key in langs) {
  console.log(key, langs[key]); // "0" HTML / "1" CSS / "2" JS
}
```
- Với **object**: `key` là tên thuộc tính (chuỗi).
- Với **mảng**: `key` là index dạng chuỗi (`"0"`, `"1"`).
- Với **string**: `key` là vị trí ký tự (`"0"`, `"1"`...).

### `3_for-of.js` — Duyệt value
```js
const langs = ["HTML", "CSS", "JS"];
for (const value of langs) {
  console.log(value); // HTML / CSS / JS
}

const str = "JS";
for (const char of str) {
  console.log(char); // J / S
}
```
- **Không dùng trực tiếp cho object thường**:
  ```js
  const obj = { a: 1, b: 2 };
  for (const v of obj) {} // TypeError: obj is not iterable
  // Phải dùng Object.values(obj) hoặc Object.entries(obj)
  ```

### `4_while.js` — While
```js
let i = 0;
while (i < 5) {
  console.log(i);
  i++;
}
```

### `5_do-while.js` — Do...while
```js
let i = 0;
do {
  i++;
  console.log(i); // 1 2 3 4 5
} while (i < 5);
```

### `6_break-continue.js` — Break / Continue
```js
for (let i = 0; i < 10; i++) {
  if (i === 5) continue; // bỏ qua i = 5
  if (i === 8) break;    // dừng hẳn tại i = 8
  console.log(i);        // 0 1 2 3 4 6 7
}
```

### `7_lap-long-nhau.js` — Nested Loop
```js
const matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]];
for (let i = 0; i < matrix.length; i++) {
  for (let j = 0; j < matrix[i].length; j++) {
    console.log(matrix[i][j]);
  }
}
// In: 1 2 3 4 5 6 7 8 9
```

## ✅ Điểm mạnh

1. **Mỗi file một chủ đề** — học từng khái niệm riêng lẻ, không bị quá tải thông tin.
2. **Sắp xếp theo độ phức tạp tăng dần** — từ đơn giản nhất (`for`) đến phức tạp nhất (nested loop).
3. **Chạy độc lập** — mỗi file có thể chạy bằng `node <file>.js` để quan sát kết quả ngay.
4. **Dữ liệu thực tế** — object thông tin cá nhân, mảng ngôn ngữ lập trình, ma trận số.
5. **Minh họa rõ sự khác biệt** — cùng một bài toán (duyệt mảng) nhưng `for...in` vs `for...of` cho kết quả khác nhau, giúp người học ghi nhớ sâu.
6. **Ghép cặp trực tiếp lý thuyết — thực hành** — mỗi khái niệm trong tài liệu roadmap.sh đều có file demo tương ứng.
7. **File nhỏ, dễ đọc** — không có boilerplate thừa, tập trung vào cú pháp cần học.
8. **Hello world của debugging** — chạy từng file giúp người mới làm quen với terminal và Node.js.

## ⚠️ Bẫy thường gặp & Hạn chế

1. **Quên `let` trong `for`** — dùng `var` khiến biến đếm rò rỉ ra ngoài scope.
   ```js
   for (var i = 0; i < 3; i++) {}
   console.log(i); // 3 — rò rỉ ra ngoài! Phải dùng let.
   ```

2. **`for...in` trên mảng có ô trống** — chỉ lặp qua ô có giá trị thực, bỏ qua ô `empty`.
   ```js
   const courses = ["HTML", "CSS"];
   courses.length = 5; // tạo 3 ô trống
   for (const k in courses) console.log(k); // chỉ in "0", "1"
   // for...of sẽ in "HTML", "CSS", undefined, undefined, undefined
   ```

3. **`for...in` duyệt prototype chain** — thuộc tính thêm vào prototype cũng xuất hiện.
   ```js
   Array.prototype.customProp = 99;
   const arr = [1, 2];
   for (const k in arr) console.log(k); // "0", "1", "customProp" ← hại!
   ```

4. **Dùng `for...of` trực tiếp trên object thường** — throw TypeError.
   ```js
   const obj = { a: 1 };
   for (const v of obj) {} // TypeError: obj is not iterable
   ```

5. **Nested loop O(n²)** — dữ liệu lớn khiến chương trình chậm nghiêm trọng.
   ```js
   // Tránh: với mảng 10.000 phần tử → 100 triệu phép so sánh
   for (let i = 0; i < arr.length; i++) {
     for (let j = 0; j < arr.length; j++) {}
   }
   ```

6. **Nhầm `break` và `continue`** — `break` thoát hoàn toàn, `continue` chỉ bỏ qua iter hiện tại. Đặt `continue` sau `break` trong cùng iter là dead code.

7. **Vòng `while` vô hạn do quên cập nhật biến** — điều kiện luôn luôn đúng.
   ```js
   let i = 0;
   while (i < 5) {
     console.log(i); // in mãi 0, không bao giờ tăng i
   }
   ```

## 💡 Khi nào dùng

- `for` — khi biết trước **số lần lặp** (duyệt mảng theo index, in bảng cửu chương).
- `for...in` — khi cần **liệt kê key** của object (duyệt config, liệt kê thuộc tính).
- `for...of` — khi cần **lấy từng value** của array/string/Set/Map (biến đổi, tính tổng).
- `while` — khi **chưa biết số lần lặp**, chỉ biết điều kiện dừng (chờ API phản hồi, retry logic).
- `do...while` — khi thân **bắt buộc chạy ít nhất 1 lần** (menu, input validation, poll).
- `break`/`continue` — khi cần **thoát sớm** hoặc **bỏ qua** phần tử không phù hợp.
- Nested loop — khi xử lý **bảng 2 chiều** (ma trận, grid, cờ vua, render canvas).

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: `for` — In 5 số (file `1_for.js`)
```js
for (let i = 0; i < 5; i++) {
  // i = 0, 1, 2, 3, 4 — mỗi lần lặp in ra giá trị hiện tại của i
  console.log(i);
}
```

### Ví dụ 2: `for...in` — Duyệt object (file `2_for-in.js`)
```js
const myInfo = {
  name: "Sơn Nguyễn",
  age: 18,
  address: "An Giang"
};
for (const key in myInfo) {
  // key lần lượt là "name", "age", "address"
  console.log(myInfo[key]); // Sơn Nguyễn / 18 / An Giang
}

// Duyệt mảng — key là index dạng chuỗi
const language = ["HTML", "CSS", "JS", "PHP", "LARAVEL"];
for (const key in language) {
  console.log(language[key]); // HTML / CSS / JS / PHP / LARAVEL
}
```

### Ví dụ 3: `for...in` trên string (file `2_for-in.js`)
```js
const myString = "Sơn Nguyễn";
for (const key in myString) {
  // key là vị trí ký tự: "0", "1", "2"...
  console.log(myString[key]); // S / ơ / n / (space) / N / g / u / y / ễ / n
}
```

### Ví dụ 4: `for...of` — Duyệt value của mảng (file `3_for-of.js`)
```js
const language = ["HTML", "CSS", "JS", "PHP", "LARAVEL"];
for (const iterator of language) {
  // iterator là value thực: "HTML", "CSS"...
  console.log(iterator);
}
```

### Ví dụ 5: `for...of` trên object (phải convert trước) (file `3_for-of.js`)
```js
const myInfo = { name: "Sơn Nguyễn", age: 18, address: "An Giang" };

// Lấy keys trước
const arrKeys = Object.keys(myInfo); // ["name", "age", "address"]
for (const iterator of arrKeys) {
  console.log(myInfo[iterator]); // Sơn Nguyễn / 18 / An Giang
}

// Hoặc lấy values trực tiếp
const arrValue = Object.values(myInfo); // ["Sơn Nguyễn", 18, "An Giang"]
for (const iterator of arrValue) {
  console.log(iterator);
}
```

### Ví dụ 6: `while` (file `4_while.js`)
```js
let i = 0;
while (i < 10) {
  console.log(i); // 0 1 2 ... 9
  i++; // quan trọng: tăng i để tiến tới điều kiện dừng
}
```

### Ví dụ 7: `do...while` (file `5_do-while.js`)
```js
let i = 0;
do {
  i++;
  console.log(i); // 1 2 3 ... 10
} while (i < 10);
// Khác while: nếu i khởi tạo = 10, do...while vẫn chạy 1 lần in 10
```

### Ví dụ 8: `break` và `continue` (file `6_break-continue.js`)
```js
for (let i = 0; i < 10; i++) {
  if (i === 8) {
    break; // Dừng vòng lặp hoàn toàn khi i = 8
  }
  if (i === 5) {
    continue; // Bỏ qua lần lặp i = 5, tiếp tục với i = 6
  }
  console.log(i); // 0 1 2 3 4 6 7
}
```

### Ví dụ 9: Nested loop — duyệt ma trận 3×3 (file `7_lap-long-nhau.js`)
```js
const myArr = [
  [1, 2, 3],
  [4, 5, 6],
  [7, 8, 9]
];
for (let i = 0; i < myArr.length; i++) {
  for (let j = 0; j < myArr[i].length; j++) {
    // myArr[i][j] truy cập phần tử tại hàng i, cột j
    console.log(myArr[i][j]);
  }
}
// Kết quả: 1 2 3 4 5 6 7 8 9
```

### Ví dụ 10: In bảng cửu chương với nested loop (tự mở rộng)
```js
for (let i = 2; i <= 9; i++) {
  for (let j = 1; j <= 10; j++) {
    console.log(`${i} x ${j} = ${i * j}`);
  }
  console.log("---"); // ngăn cách giữa các bảng cửu chương
}
```

## 🔬 So sánh với alternatives

| Tình huống | Loop nào nên dùng | Lý do |
|---|---|---|
| Duyệt mảng theo index | `for` hoặc `for...of` | `for` cho index, `for...of` cho value — cả hai đều đúng |
| Duyệt object keys | `for...in` | Thiết kế riêng cho object enumeration |
| Duyệt object values | `for...of` + `Object.values()` | Không thể `for...of` trực tiếp object |
| Lặp cho đến điều kiện sai | `while` | Kiểm tra điều kiện trước, linh hoạt |
| Luôn chạy ít nhất 1 lần | `do...while` | Thân chạy trước, điều kiện kiểm tra sau |
| Dừng sớm khi tìm thấy | `for` + `break` | `break` thoát ngay, tiết kiệm thời gian |
| Bỏ qua phần tử không phù hợp | `for` + `continue` | Tiếp tục iter tiếp theo mà không thoát |

## 📊 Performance & Best Practices

**Quy tắc vàng**: dùng đúng loại loop cho đúng bài toán.

- **Với mảng/array-like**: ưu tiên `for` (nhanh nhất) hoặc `for...of` (sạch nhất).
- **Với object**: dùng `for...in` + `hasOwnProperty()`, hoặc `Object.keys()/values()/entries()` + `for...of`.
- **Với string**: dùng `for...of` (dùng được với unicode đúng đắn) thay `for...in`.
- **Tránh nested loop quá sâu**: giới hạn 2-3 tầng; với dữ liệu lớn (>10k), cân nhắc dùng Map/Set để giảm O(n²).
- **Luôn dùng `let`/`const` trong `for`**: `var` rò rỉ biến ra ngoài scope, gây bug khó tìm.
- **Đặt điều kiện dừng rõ ràng**: kiểm tra lại biến đếm có tiến về điều kiện dừng hay không.

**Benchmark tương đối** (1 triệu lần lặp, Node.js V8):
- `for` (kinh điển):tốc độ cơ bản 1x
- `for...of`: ~1.1x (chậm hơn ~10%)
- `while`: ~1.05x
- `for...in` (trên object): ~1.3x
- `for...in` (trên mảng có prototype Pollution): ~2x+

## 🔗 Liên kết chéo

- So sánh với **Control Flow (if/switch)**: `06_control-flow/01_conditionals/5_condition/1_if.js` — loop thường đi kèm điều kiện `if` bên trong thân.
- So sánh với **Callbacks**: `09_functions/01_parameters-and-arrow/01_callbacks/` — `forEach`/`map`/`filter` là vòng lặp dạng callback.
- So sánh với **Arrow Functions**: `09_functions/01_parameters-and-arrow/03_arrow-functions/` — arrow function thường đi kèm callback trong loop.
- So sánh với **Scope & Closure**: `09_functions/02_scope-closure-strict-mode/03_closure/` — biến trong vòng lặp `var` bị closure bắt hold, dẫn đến bug kinh điển.
