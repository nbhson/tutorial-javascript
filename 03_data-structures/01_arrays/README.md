# Arrays (Mảng)

## 🔑 Khái niệm

**Array** là cấu trúc dữ liệu **có thứ tự** lưu danh sách phần tử, truy cập bằng **chỉ số (index) bắt đầu từ 0**. Trong JavaScript, array thực chất là **object đặc biệt** dùng index làm key — vì vậy `typeof []` trả `"object"`. Array có thể chứa **mọi kiểu** trộn lẫn: `[1, "Sơn", null, {}]`.

**Tạo array:**

```js
var arr_1 = [1, 'Sơn', null, {}];     // literal — khuyên dùng
var arr_2 = new Array(1, 'Sơn', null, {}); // constructor — tránh trừ khi cố tình

console.log(typeof arr_1); // "object" — array là object đặc biệt!
```

**Kiểm tra có phải array:** đừng tin `typeof` (luôn `"object"`), dùng `Array.isArray`:

```js
console.log(Array.isArray({}));    // false
console.log(Array.isArray(arr_1)); // true
```

**Thao tác cơ bản:** `.length`, truy cập `arr[0]`, `arr.push(...)`, `arr.pop()`, `arr.shift()`, `arr.unshift(...)`, `arr.splice(...)`, `arr.slice(...)`, `arr.concat(...)`, `arr.join(...)`.

**Hai nhóm phương thức quan trọng theo roadmap:**

1. **Làm thay đổi mảng gốc (mutating):** `push`, `pop`, `shift`, `unshift`, `splice`, `sort`, `reverse`...
2. **Trả mảng mới (immutable):** `map`, `filter`, `slice`, `concat`, `flat`...

> Lưu ý `splice` vs `slice`: `splice` **sửa mảng gốc** và được dùng để xóa/chèn, còn `slice` **trả về mảng con mới** không đụng mảng gốc.

**Array methods "functional" (nền tảng lập trình hiện đại):**
- `forEach` — duyệt từng phần tử (không trả về gì).
- `every` — `true` nếu **tất cả** thỏa điều kiện.
- `some` — `true` nếu **chỉ cần một** thỏa.
- `find` — trả **object đầu tiên** thỏa điều kiện.
- `filter` — trả **mảng tất cả** phần tử thỏa điều kiện.
- `map` — trả **mảng mới** đã biến đổi từng phần tử.
- `reduce` — **tích lũy** toàn mảng về một giá trị.
- `includes` — kiểm tra sự tồn tại.

## ✅ Điểm mạnh

- Đa dụng: chứa mọi kiểu dữ liệu, trộn lẫn thoải mái.
- Nhiều methods chuẩn, khai báo nhiều, tối ưu sẵn từ engine.
- `map/filter/reduce` giúp viết logic "functional" ngắn gọn, ít bug hơn vòng lặp tay.
- `includes` kiểm tra sự tồn tại nhanh và dễ đọc.
- Spread `[...arr]` + `map` cho copy/bất biến an toàn.

## ⚠️ Lưu ý / Hạn chế

- `typeof [] === "object"` — phải `Array.isArray()` để kiểm tra.
- `splice` **sửa gốc** còn `slice` thì không — nhầm lẫn rất hay gây bug.
- `includes` phân biệt hoa/thường và dùng `===`: `[NaN].includes(NaN)` → `true` nhưng `arr.indexOf(NaN)` → `-1`.
- `reduce` con đầu tiên (`accumulator`) với `initial value` không truyền thì lấy phần tử đầu — dễ tính sai tổng nếu không để ý.
- `forEach` không "break" được như vòng lặp — muốn dừng sớm hãy dùng `for...of` hoặc `some`.

## 💡 Khi nào dùng

- Danh sách phần tử có thứ tự (sản phẩm, tin nhắn, người dùng) → array.
- Duyệt + biến đổi mảng → `map` (không đụng gốc).
- Lọc theo điều kiện → `filter`.
- Kiểm tra tồn tại → `some`, `includes`.
- Tính tổng/ghép chuỗi từ mảng → `reduce`.

## 🎯 Ví dụ minh họa

```js
var courses = [
  { id: 1, name: "HTML", coin: 100 },
  { id: 2, name: "CSS", coin: 0 },
  { id: 3, name: "JS", coin: 150 },
];

console.log(courses.every((c) => c.coin === 0)); // false (không phải tất cả free)
console.log(courses.some((c) => c.coin === 0));  // true (có khóa free)
console.log(courses.find((c) => c.name === "CSS").coin); // 0
console.log(courses.filter((c) => c.coin > 0).map((c) => c.name)); // ["HTML","JS"]
console.log(courses.reduce((sum, c) => sum + c.coin, 0)); // 250
```

## 📚 Tham khảo / Bài tập

- Bắt đầu bằng `app.js` trong thư mục này (demo các kiểu dữ liệu lưu trong mảng `myArr = [1, 0, "Sơn", -5, true]`), sau đó học sâu ở `01_array-basics/` với 5 file: `1_mang.js`, `2_lam-viec-voi-mang.js`, `3_foreach-every-some-find-filter.js`, `4_map-reduce.js`, `6_include.js`.
- Tự thử: với mảng trên, 1) `filter` lấy các khóa có `coin > 0`; 2) `reduce` tính tổng `coin`; 3) dùng `map` thêm chuỗi `"Khoa hoc: "` vào tên và in kết quả.
- Tài liệu: [MDN — Array](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array), [javascript.info/array-methods](https://javascript.info/array-methods).