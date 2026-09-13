# Vòng Lặp và Lặp (Loops & Iterations) — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

**Vòng lặp (loop)** là cơ chế cho phép JavaScript thực hiện **lặp đi lặp lại một khối lệnh** nhiều lần mà không cần viết lặp lại cùng một đoạn code. Dưới nền tảng, mỗi lần vòng lặp chạy, JavaScript engine (V8, SpiderMonkey, JavaScriptCore...) tạo ra một **execution context** mới trong call stack, đánh giá điều kiện, thực thi thân vòng lặp, rồi quay lại kiểm tra điều kiện lần nữa. Nếu không có cơ chế dừng, loop sẽ chạy vô hạn và chiếm toàn bộ main thread — trình duyệt sẽ hiển thị "trang web đang bận" và người dùng có thể phải đóng tab.

JavaScript cung cấp **5 loại vòng lặp chính**, mỗi loại tối ưu cho một kịch bản khác nhau:

| Cú pháp | Mục đích | Khi nào nên dùng |
|---|---|---|
| `for` | Lặp với bộ đếm rõ ràng | Biết trước số lần lặp, cần truy cập index |
| `while` | Lặp khi điều kiện đúng | Chưa biết số lần, chỉ biết điều kiện dừng |
| `do...while` | Lặp ít nhất 1 lần | Luôn cần chạy thân trước rồi mới kiểm tra |
| `for...in` | Duyệt key của object | Khi cần liệt kê tên thuộc tính (property keys) |
| `for...of` | Duyệt value của iterable | Khi cần từng giá trị thực tế (array, string, Set, Map) |

**Khác biệt then chốt**: `for...in` trả về **key dạng chuỗi** (`"0"`, `"name"`, ...), còn `for...of` trả về **giá trị thực** (số, object, ký tự...). Đây là nguồn lỗi phổ biến nhất: dùng nhầm `for...in` để duyệt mảng khiến index bị ép thành chuỗi, gây khó khăn khi tính toán số học.

## 📐 Cấu trúc / Cú pháp

### `for` — Vòng lặp đếm kinh điển
```js
for (khởi_tạo; điều_kiện; bước_nhảy) {
  // thân vòng lặp
}
// Ví dụ:
for (let i = 0; i < 5; i++) {
  console.log(i); // 0 1 2 3 4
}
```
- `khởi_tạo`: chạy **1 lần duy nhất** trước khi vòng lặp bắt đầu.
- `điều_kiện`: được đánh giá **trước mỗi lần lặp**; nếu sai (`false`) thì dừng.
- `bước_nhảy`: chạy **sau mỗi lần lặp** hoàn tất.

### `while` — Vòng lặp theo điều kiện
```js
while (điều_kiện) {
  // thân vòng lặp
}
// Ví dụ:
let i = 0;
while (i < 5) {
  console.log(i); // 0 1 2 3 4
  i++;
}
```
Điều kiện được kiểm tra **trước** thân — nếu sai ngay từ đầu, thân **không bao giờ chạy**.

### `do...while` — Đảm bảo chạy ít nhất 1 lần
```js
do {
  // thân vòng lặp
} while (điều_kiện);
// Ví dụ:
let i = 0;
do {
  console.log(i); // vẫn in 0 dù i >= 5
  i++;
} while (i < 5);
```
Thân luôn chạy **ít nhất 1 lần** trước khi điều kiện được kiểm tra.

### `for...in` — Duyệt key
```js
const obj = { a: 1, b: 2 };
for (const key in obj) {
  console.log(key);         // "a", "b"
  console.log(obj[key]);    // 1, 2
}
```
- Duyệt qua **tất cả enumerable keys**, kể cả **thuộc tính kế thừa** từ prototype chain.
- **Luôn dùng `hasOwnProperty()`** để lọc chỉ các thuộc tính trực tiếp:
  ```js
  for (const key in obj) {
    if (obj.hasOwnProperty(key)) {
      console.log(key, obj[key]);
    }
  }
  ```

### `for...of` — Duyệt value
```js
const arr = ["HTML", "CSS", "JS"];
for (const value of arr) {
  console.log(value); // HTML, CSS, JS
}
```
- Duyệt qua **giá trị** của các đối tượng iterable: `Array`, `String`, `Map`, `Set`, `arguments`, DOM NodeList.
- **Không dùng trực tiếp cho object thường** — phải chuyển qua `Object.keys()`, `Object.values()`, hoặc `Object.entries()`.

### `break` và `continue`
```js
for (let i = 0; i < 10; i++) {
  if (i === 5) continue; // Bỏ qua lần lặp hiện tại (i = 5)
  if (i === 8) break;    // Dừng hoàn toàn vòng lặp
  console.log(i);        // 0 1 2 3 4 6 7
}
```
- `break`: thoát ngay khỏi vòng lặp.
- `continue`: bỏ qua phần còn lại của lần lặp hiện tại, nhảy sang lần lặp tiếp theo.
- Cả hai đều **có thể chỉ định label** để thoát/bỏ qua vòng lặp ngoài (advanced).

## ✅ Điểm mạnh — Tại sao nên dùng

1. **Giảm thiểu code lặp**: thay vì viết 100 dòng để in 100 số, chỉ cần 3-5 dòng với vòng lặp — code ngắn gọn, dễ bảo trì.
2. **Linh hoạt theo ngữ cảnh**: mỗi loại loop sinh ra để giải quyết một tình huống cụ thể, chọn đúng loại giúp code tự nhiên, dễ đọc.
3. **Duyệt object theo key/value**: `for...in` cho key, `for...of` cho value — phân biệt rõ ràng tránh bug.
4. **Hỗ trợ điều khiển luồng**: `break` và `continue` cho phép dừng sớm hoặc bỏ qua phần tử không phù hợp.
5. **Lồng nhau (nested)**: giải quyết bài toán 2 chiều như ma trận, bảng điểm, cờ vua, grid layout.
6. **Nền tảng thuật toán**: mọi giải thuật tìm kiếm, sắp xếp, lọc dữ liệu đều dựa trên vòng lặp ở tầng thấp.
7. **Tương thích ngược**: `for`, `while`, `for...in`, `for...of` đều hoạt động trên mọi trình duyệt và Node.js.
8. **Kết hợp hàm cao cấp**: `forEach`, `map`, `filter` thực chất là sugar trên `for`/`for...of` — hiểu loop giúp hiểu sâu các phương thức mảng.
9. **Hiệu năng tốt**: `for` kinh điển thường nhanh nhất vì engine tối ưu tốt cho pattern đếm số.
10. **Dễ debug**: mỗi lần lặp chạy tuần tự, có thể đặt breakpoint hoặc `console.log` để theo dõi trạng thái biến.

## ⚠️ Bẫy thường gặp & Hạn chế

1. **Vòng lặp vô hạn**: quên điều kiện dừng hoặc quên tăng biến đếm → treo browser.
   ```js
   // SAI — i không bao giờ tăng
   let i = 0;
   while (i < 5) {
     console.log(i); // in mãi 0
   }
   ```

2. **`for...in` duyệt cả prototype**: thuộc tính kế thừa từ prototype chain cũng xuất hiện.
   ```js
   const arr = [1, 2];
   Array.prototype.custom = 99;
   for (const key in arr) {
     console.log(key); // "0", "1", "custom" ← không mong muốn!
   }
   ```

3. **`for...in` trên mảng với ô trống**: chỉ lặp qua ô có giá trị thực, bỏ qua ô `empty`.
   ```js
   const courses = ["HTML", "CSS"];
   courses.length = 5; // tạo 3 ô trống
   for (const k in courses) console.log(k); // chỉ in "0", "1"
   ```

4. **Nhầm `for...in` vs `for...of`**: `for...in` trả key (chuỗi), `for...of` trả value.
   ```js
   const langs = ["HTML", "CSS"];
   for (const v of langs) console.log(typeof v); // "string", "string"
   for (const k in langs) console.log(typeof k); // "string", "string" ← đây là key "0", "1"
   ```

5. **`let` trong vòng `for` bị closure bắt hold**: `var` chia sẻ cùng 1 biến trên các lần lặp.
   ```js
   for (var i = 0; i < 3; i++) {}
   console.log(i); // 3 — var rò rỉ ra ngoài!
   ```

6. **Dùng `break` trước `continue` trong cùng iter**: `continue` bị bỏ qua vì vòng đã exit.
   ```js
   for (let i = 0; i < 5; i++) {
     if (i === 2) break;
     continue; // không bao giờ đến được
     console.log(i);
   }
   // Kết quả: chỉ in 0, 1 rồi break
   ```

7. **`for...of` không hoạt động trên plain object**: object thường không phải iterable.
   ```js
   const obj = { a: 1, b: 2 };
   for (const v of obj) {} // TypeError: obj is not iterable
   ```

8. **Nested loop O(n²)**: lồng quá nhiều vòng lặp với dữ liệu lớn sẽ chậm nghiêm trọng.
   ```js
   // Tránh với dữ liệu > 1000 phần tử
   for (let i = 0; i < 1000; i++) {
     for (let j = 0; j < 1000; j++) {}
   } // 1 triệu lần — chậm
   ```

## 💡 Khi nào dùng — Tình huống thực tế

1. **In bảng cửu chương**: `for` với hai vòng lồng nhau, một biến đếm hàng, một biến đếm cột — vì biết trước kích thước 9×9.
2. **Duyệt mảng để tính tổng**: `for...of` lấy từng số, cộng dồn — đơn giản hơn `reduce` khi cần debug trung gian.
3. **Lặp cho đến khi dữ liệu hợp lệ** (input validation): `while` chờ người dùng nhập đúng email format — không biết trước cần bao nhiêu lần thử.
4. **Hiển thị menu luôn hỏi lại**: `do...while` — bắt buộc hiện menu ít nhất 1 lần rồi mới kiểm tra chọn hợp lệ.
5. **Duyệt properties của object cấu hình**: `for...in` + `hasOwnProperty` — khi cấu hình có thể thêm bớt key động.
6. **Duyệt DOM NodeList**: `for...of` vòng qua các phần tử `document.querySelectorAll('.item')` — NodeList là iterable.
7. **Ma trận / bảng 2 chiều**: nested `for` — tính tổng ma trận, in bàn cờ, thuật toán pathfinding.
8. **Tìm kiếm phần tử đầu tiên thỏa điều kiện**: `for` + `break` — dừng ngay khi tìm thấy để tiết kiệm thời gian.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: `for` cơ bản — In 5 số
```js
// Khởi tạo i=0, chạy khi i<5, tăng i sau mỗi lần
for (let i = 0; i < 5; i++) {
  console.log("Lần thứ", i); // Lần thứ 0 → Lần thứ 4
}
```

### Ví dụ 2: `for...in` duyệt object
```js
const user = { name: "Sơn", age: 18 };
for (const key in user) {
  // key là "name", sau đó là "age"
  console.log(`${key}: ${user[key]}`);
  // name: Sơn
  // age: 18
}
```

### Ví dụ 3: `for...of` duyệt mảng
```js
const langs = ["HTML", "CSS", "JS"];
for (const value of langs) {
  // value lần lượt là "HTML", "CSS", "JS"
  console.log(value);
}
```

### Ví dụ 4: `while` với điều kiện thay đổi
```js
let remaining = 3;
while (remaining > 0) {
  console.log(`Còn ${remaining} lượt thử`);
  remaining--; // quan trọng: phải thay đổi biến điều kiện
}
// Còn 3 lượt thử
// Còn 2 lượt thử
// Còn 1 lượt thử
```

### Ví dụ 5: `do...while` — menu luôn hiện ít nhất 1 lần
```js
let choice;
do {
  choice = prompt("Chọn 1: Start / 2: Exit");
  if (choice !== "1" && choice !== "2") {
    alert("Lựa chọn không hợp lệ!");
  }
} while (choice !== "1" && choice !== "2");
console.log("Đã chọn:", choice);
```

### Ví dụ 6: `for...in` với `hasOwnProperty` lọc prototype
```js
const hero = { name: "Sơn", power: "code" };
// Thêm thuộc tính prototype — for...in sẽ thấy nếu không lọc
Array.prototype.fake = "x";
for (const key in hero) {
  if (hero.hasOwnProperty(key)) { // chỉ lấy thuộc tính trực tiếp
    console.log(key, hero[key]); // name Sơn / power code
  }
}
```

### Ví dụ 7: `break` và `continue` kết hợp
```js
for (let i = 0; i < 10; i++) {
  if (i === 5) continue; // bỏ qua 5, tiếp tục lần tiếp
  if (i === 8) break;    // dừng hẳn ở 8
  console.log(i);        // 0 1 2 3 4 6 7
}
```

### Ví dụ 8: Vòng lặp lồng nhau — ma trận 3×3
```js
const matrix = [
  [1, 2, 3],
  [4, 5, 6],
  [7, 8, 9]
];
for (let i = 0; i < matrix.length; i++) {
  for (let j = 0; j < matrix[i].length; j++) {
    console.log(`[${i}][${j}] = ${matrix[i][j]}`);
  }
}
// [0][0]=1, [0][1]=2, [0][2]=3, [1][0]=4 ...
```

### Ví dụ 9: Duyệt string bằng `for...of`
```js
const str = "JS";
for (const char of str) {
  console.log(char); // J, S
}
// String là iterable — mỗi ký tự là một value
```

### Ví dụ 10: Tìm phần tử đầu tiên thỏa điều kiện (early exit)
```js
const scores = [55, 72, 48, 91, 67];
for (const s of scores) {
  if (s >= 90) {
    console.log("Đạt:", s); // Đạt: 91
    break; // dừng ngay, không cần kiểm tra 67
  }
}
```

## 🔬 So sánh với alternatives

| Phương án | Khi nào thay thế được loop | Ưu điểm | Nhược điểm |
|---|---|---|---|
| `forEach` | Duyệt mảng chỉ để side-effect | Cú pháp gọn, callback nhận `(val, idx, arr)` | Không `break` được, return trong callback chỉ thoát callback |
| `map` | Khi cần biến đổi mảng thành mảng mới | Trả về mảng mới, immutable style | Tạo mảng phụ — tốn bộ nhớ |
| `filter` | Khi cần lọc phần tử | Trả về mảng con | Tương tự map — tốn bộ nhớ |
| `for...of` + `break` | Khi cần early exit | Hỗ trợ `break`/`continue`, không tạo mảng phụ | Chỉ duyệt array/string/Set/Map |
| `reduce` | Khi cần gom dữ liệu thành 1 giá trị | Linh hoạt: tổng, object, map đều được | Khó đọc với logic phức tạp |
| `while`/`do...while` | Khi điều kiện không dựa vào index | Linh hoạt hơn `for` khi không biết số lần lặp | Dễ quên tăng biến → infinite loop |

## 📊 Performance & Best Practices

**Thứ tự hiệu năng** (từ nhanh nhất đến chậm nhất, trong hầu hết engine hiện đại):
1. `for` kinh điển — engine tối ưu tốt cho pattern đếm số
2. `for...of` — gần bằng `for`, có chút overhead kiểm tra iterator
3. `while` — tương đương `for`, nhưng cần tự quản lý biến đếm
4. `for...in` — chậm nhất với mảng vì phải kiểm tra prototype chain
5. `forEach`/`map`/`filter` — overhead do callback invocation

**Quy tắc coding nên tuân thủ**:
- Luôn dùng `let`/`const` thay `var` trong `for` để tránh rò rỉ scope.
- Ưu tiên `for...of` cho array/string; `for...in` chỉ cho object (với `hasOwnProperty`).
- Với mảng lớn (>10k phần tử), dùng `for` thông thường để tránh overhead iterator.
- Tránh nested loop sâu hơn 2-3 tầng; dùng hàm riêng hoặc thư viện hỗ trợ.
- Luôn đảm bảo biến đếm tiến về điều kiện dừng — kiểm tra kỹ trước khi deploy.

**Benchmark tham khảo** (Node.js V8, 1 triệu lần lặp):
- `for (let i=0; i<N; i++)`: ~10ms
- `forEach()`: ~25ms (gấp 2.5 lần do callback)
- `for...in` trên mảng: ~15ms (chậm hơn `for` nhẹ)

## 🔗 Liên kết chéo

- Xem chi tiết từng loại vòng lặp: `05_loops-and-iterations/01_loops/`
  - `1_for.js` — vòng lặp `for` chuẩn
  - `2_for-in.js` — `for...in` duyệt object, mảng, string
  - `3_for-of.js` — `for...of` duyệt value của iterable
  - `4_while.js` — `while` lặp theo điều kiện
  - `5_do-while.js` — `do...while` đảm bảo chạy 1 lần
  - `6_break-continue.js` — điều khiển luồng với break/continue
  - `7_lap-long-nhau.js` — vòng lặp lồng nhau (nested loop)
- So sánh với **Callbacks**: `09_functions/01_parameters-and-arrow/01_callbacks/` — hiểu cách `forEach`/`map` hoạt động bên dưới.
- So sánh với **Control Flow**: `06_control-flow/` — vòng lặp là một dạng điều khiển luồng, kết hợp với `if/switch` tạo thành logic hoàn chỉnh.
