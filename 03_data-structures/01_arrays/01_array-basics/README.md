# Array Basics (Tạo & thao tác mảng)

## 🔑 Khái niệm

**Array** — cấu trúc dữ liệu có thứ tự, truy cập bằng index `0, 1, 2...`. Bài này gồm 2 phần lớn: **tạo & truy xuất mảng** (file `1_mang.js`) và **thao tác bằng array methods** (`2_lam-viec-voi-mang.js`, `3_foreach-every-some-find-filter.js`, `4_map-reduce.js`, `6_include.js`).

**1. Tạo mảng:**

```js
var arr_1 = [1, 'Sơn', null, {}];            // literal — nên dùng
var arr_2 = new Array(1, 'Sơn', null, {});   // constructor

console.log(typeof arr_1);   // "object" (array là object đặc biệt)
console.log(Array.isArray(arr_1)); // true — mới là cách kiểm tra đúng
console.log(Array.isArray({}));    // false
```

**2. Các phương thức thay đổi mảng gốc (mutating):**

```js
var language = ['HTML', 'CSS', 'JS', 'PHP'];

language.pop();                    // xóa PHẦN TỬ CUỐI, trả về phần tử vừa xóa
language.push('Node', 'OPS');      // thêm vào cuối
language.shift();                  // xóa PHẦN TỬ ĐẦU, trả về phần tử đã xóa
language.unshift('First', 'Second'); // thêm vào đầu
language.splice(1, 2);             // xóa từ index 1, 2 phần tử (delete)
language.splice(1, 0, 'A', 'B');   // chèn 'A','B' tại index 1 (không xóa gì)
```

**3. Các phương thức TRẢ về giá trị/mảng mới (không đổi gốc):**

- `toString()` / `join()` — chuyển mảng thành chuỗi: `language.join(' - ')` → `"HTML - CSS - JS"`.
- `concat(mảng khác)` — nối mảng.
- `slice(from, to)` — cắt phần mảng con (không sửa gốc, khác `splice`).
- `includes(x)` — kiểm tra tồn tại.

**4. Nhóm phương thức "functional" (học kỹ trong bài này):**

- `forEach(fn)` — duyệt từng phần tử (không trả về gì).
- `every(fn)` — `true` khi **tất cả** thỏa điều kiện.
- `some(fn)` — `true` khi **một** phần tử thỏa.
- `find(fn)` — trả **object đầu tiên** thỏa (hoặc `undefined`).
- `filter(fn)` — trả **mảng chứa tất cả** phần tử thỏa.
- `map(fn)` — trả **mảng mới đã biến đổi**.
- `reduce(fn, initial)` — **tích lũy** toàn mảng về một giá trị.
- `includes(x)` / `Array.includes` — kiểm tra phần tử có trong mảng.

```js
courses.forEach((course, index) => console.log(index, course));
courses.every((course) => course.coin === 0); // false — không phải tất cả free
courses.some((course) => course.coin === 0);  // true — có khóa free
courses.find((course) => course.name === "PHP"); // { id:4, name:'PHP', coin:0 }
courses.filter((course) => course.coin === 0);    // 2 khóa free
```

## ✅ Điểm mạnh

- Duyệt + biến đổi với `map/filter/reduce` ngắn gọn gấp đôi vòng lặp tay.
- `every/some/find` thay thế vòng lặp `for` + `if` cồng kềnh.
- `push/pop/unshift/shift` cung cấp dùng như queue/stack đơn giản.
- `splice` cho palindrome cut/chèn trong một lệnh.
- `includes` dễ đọc hơn `indexOf > -1`.

## ⚠️ Lưu ý / Hạn chế

- **`pop`/`shift` sửa mảng gốc** — muốn giữ gốc hãy copy trước (`[...arr]`).
- **`splice` vs `slice`**: `splice` sửa gốc, `slice` trả mảng mới.
- `map/filter` không thay đổi mảng gốc — đó là điều tốt, nhưng cũng dễ quên lưu kết quả.
- `find` trả `undefined` khi không tìm thấy; `filter` trả `[]`.
- `forEach` không break giữa chừng.

## 💡 Khi nào dùng

- Xử lý lặp + biến đổi dữ liệu → `map`.
- Lọc danh sách theo điều kiện → `filter`.
- Kiểm tra "tồn tại ít nhất 1" → `some`, "tất cả" → `every`.
- Tính tổng/ghép → `reduce`.
- Thêm/xóa ở cuối/đầu (stack, queue) → `push/pop/shift/unshift`.

## 🎯 Ví dụ minh họa

```js
var language = ['HTML', 'CSS', 'JS', 'PHP'];

console.log(language.join(' - '));    // HTML - CSS - JS - PHP
language.push('Node');                // thêm cuối
language.unshift('First');            // thêm đầu
console.log(language.slice(1, 3));    // [ 'First'?? ] → cắt index 1..2

// functional
const courses = [
  { id: 1, name: "HTML", coin: 100 },
  { id: 2, name: "CSS", coin: 0 },
  { id: 3, name: "JS", coin: 150 },
];
console.log(courses.map((c) => `Khoa: ${c.name}`));  // ["Khoa: HTML", ...]
console.log(courses.reduce((t, c) => t + c.coin, 0)); // 250
```

> Lưu ý ví dụ `slice(1, 3)` áp dụng sau `push`/`unshift` → mảng lúc này là `["First","HTML","CSS","JS","PHP","Node"]`, vậy `slice(1, 3)` = `["HTML","CSS"]`.

## 📚 Tham khảo / Bài tập

- Chạy lần lượt các file theo thứ tự:
  1. `1_mang.js` — tạo mảng (2 cách), `Array.isArray`.
  2. `2_lam-viec-voi-mang.js` — `toString/join/pop/push/shift/unshift/splice/slice`.
  3. `3_foreach-every-some-find-filter.js` — các vòng `forEach/every/some/find/filter` với mảng courses.
  4. `4_map-reduce.js` — `map` biến đổi object và `reduce` tính tổng coin.
  5. `6_include.js` — `includes` cho chuỗi lẫn mảng.
- Tự thử: bỏ comment các dòng `console.log` trong `3_foreach...` và `4_map-reduce.js` để xem từng kết quả; tự viết một mảng `books` và lọc sách giá rẻ hơn 100k bằng `filter`.
- Tài liệu: [MDN — Array methods](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array), [javascript.info/array-methods](https://javascript.info/array-methods).